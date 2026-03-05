"""Chatbot service: RAG retrieval, context assembly, Claude API."""

import json

import httpx
from cachetools import TTLCache
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.core.config import settings
from sentiment_detector.core.logging import get_logger

logger = get_logger(__name__)

# In-memory cache for live context (15 min TTL)
_context_cache: TTLCache = TTLCache(maxsize=1, ttl=900)

COHERE_EMBED_URL = "https://api.cohere.com/v2/embed"
COHERE_EMBED_MODEL = "embed-english-v3.0"


async def _embed_query(query: str) -> str:
    """Embed a query string using Cohere API. Returns PostgreSQL array literal."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            COHERE_EMBED_URL,
            headers={
                "Authorization": f"Bearer {settings.cohere_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "texts": [query],
                "model": COHERE_EMBED_MODEL,
                "input_type": "search_query",
                "embedding_types": ["float"],
            },
        )
        resp.raise_for_status()
        embedding = resp.json()["embeddings"]["float"][0]
    return "{" + ",".join(str(float(x)) for x in embedding) + "}"


async def retrieve_chunks(session: AsyncSession, query: str, top_k: int = 5) -> list[dict]:
    """Embed query and retrieve top-k similar document chunks via cosine similarity."""
    emb_str = await _embed_query(query)

    result = await session.execute(
        text("""
            SELECT source, chunk_text, cosine_similarity(embedding, :emb::float8[]) AS similarity
            FROM document_chunks
            ORDER BY cosine_similarity(embedding, :emb::float8[]) DESC
            LIMIT :top_k
        """),
        {"emb": emb_str, "top_k": top_k},
    )
    rows = result.fetchall()
    return [{"source": r[0], "chunk_text": r[1], "similarity": float(r[2])} for r in rows]


async def fetch_live_context(session: AsyncSession) -> dict:
    """Fetch current dashboard state from database. Cached 15 min."""
    if "ctx" in _context_cache:
        return _context_cache["ctx"]

    regime = None
    sentiments: dict = {}
    stress = None
    transitions: list = []

    try:
        regime_row = await session.execute(text("""
            SELECT regime, confidence
            FROM regime_states
            ORDER BY timestamp DESC
            LIMIT 1
        """))
        regime = regime_row.fetchone()
    except Exception as e:
        logger.warning("Failed to fetch regime state", error=str(e))

    try:
        sent_rows = await session.execute(text("""
            SELECT DISTINCT ON (asset_class)
                asset_class, mean_compound
            FROM sentiment_indices
            WHERE source IS NULL
            ORDER BY asset_class, period_start DESC
        """))
        sentiments = {r[0]: round(float(r[1]), 4) for r in sent_rows.fetchall()}
    except Exception as e:
        logger.warning("Failed to fetch sentiment indices", error=str(e))

    try:
        stress_row = await session.execute(text("""
            SELECT value FROM stress_indices
            WHERE source = 'CISS'
            ORDER BY date DESC LIMIT 1
        """))
        stress = stress_row.fetchone()
    except Exception as e:
        logger.warning("Failed to fetch stress index", error=str(e))

    try:
        trans_rows = await session.execute(text("""
            SELECT from_regime, to_regime, transition_start, trigger_features
            FROM regime_transitions
            ORDER BY transition_start DESC
            LIMIT 5
        """))
        transitions = [
            {
                "from": r[0],
                "to": r[1],
                "date": str(r[2]),
                "trigger": r[3].get("description", "N/A") if isinstance(r[3], dict) else "N/A",
            }
            for r in trans_rows.fetchall()
        ]
    except Exception as e:
        logger.warning("Failed to fetch regime transitions", error=str(e))

    ctx = {
        "current_regime": regime[0] if regime else None,
        "regime_confidence": round(float(regime[1]), 4) if regime else None,
        "sentiment_scores": sentiments,
        "stress_level": round(float(stress[0]), 4) if stress else None,
        "recent_transitions": transitions,
    }

    regime_label = ctx["current_regime"] or "unknown"
    sent_summary = ", ".join(f"{k}: {v}" for k, v in sentiments.items()) or "no data"
    stress_str = f"{ctx['stress_level']}" if ctx["stress_level"] else "N/A"
    ctx["summary"] = (
        f"Current regime: {regime_label}. "
        f"Sentiment scores — {sent_summary}. "
        f"Stress index: {stress_str}."
    )

    _context_cache["ctx"] = ctx
    return ctx


SYSTEM_PREAMBLE = """You are Jon, the research assistant for the Cross-Asset Sentiment Regime Detector dashboard (market-sentiment.io).

Your role:
- Answer questions about the project's methodology, data sources, models, and architecture.
- Explain the current market regime, sentiment scores, and stress indicators shown on the dashboard.
- Cite your sources when referencing project documentation.

Rules:
- Stay strictly within the project domain. Do not answer questions about other topics.
- If asked for financial advice, respond: "I'm a research tool, not a financial advisor."
- If you don't know the answer, say so. Do not hallucinate.
- Be concise and use plain language. Use bullet points for lists.
"""


def build_system_prompt(live_context: dict, rag_chunks: list[dict]) -> str:
    """Assemble the full system prompt from static + live + RAG context."""
    parts = [SYSTEM_PREAMBLE]

    # Live context block
    parts.append("## Current Dashboard State\n")
    parts.append(live_context["summary"])
    if live_context["recent_transitions"]:
        parts.append("\nRecent regime transitions:")
        for t in live_context["recent_transitions"][:3]:
            parts.append(f"- {t['date']}: {t['from']} → {t['to']} ({t['trigger'] or 'N/A'})")

    # RAG context block
    if rag_chunks:
        parts.append("\n## Relevant Documentation\n")
        for i, chunk in enumerate(rag_chunks, 1):
            parts.append(f"[Source {i}: {chunk['source']}]\n{chunk['chunk_text']}\n")

    return "\n".join(parts)


async def chat(
    session: AsyncSession,
    query: str,
    conversation_history: list[dict],
    max_history_turns: int = 6,
) -> dict:
    """Full chatbot pipeline: retrieve → context → prompt → Claude API → response."""
    import anthropic

    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")

    # 1. Retrieve relevant document chunks
    rag_chunks = await retrieve_chunks(session, query)

    # 2. Fetch live dashboard context
    live_context = await fetch_live_context(session)

    # 3. Build system prompt
    system_prompt = build_system_prompt(live_context, rag_chunks)

    # 4. Trim conversation history
    trimmed_history = conversation_history[-(max_history_turns * 2):]

    # 5. Call Claude API
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    messages = [{"role": m["role"], "content": m["content"]} for m in trimmed_history]
    messages.append({"role": "user", "content": query})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    )

    answer = response.content[0].text

    # 6. Build sources list (only include chunks above relevance threshold)
    sources = [
        {"source": c["source"], "snippet": c["chunk_text"][:150] + "..."}
        for c in rag_chunks
        if c["similarity"] > 0.3
    ]

    return {
        "response": answer,
        "sources_used": sources,
        "regime_context_used": live_context["current_regime"] is not None,
    }
