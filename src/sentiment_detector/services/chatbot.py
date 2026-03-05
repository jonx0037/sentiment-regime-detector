"""Chatbot service: RAG retrieval, context assembly, Claude API."""

import json

from cachetools import TTLCache
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.core.config import settings
from sentiment_detector.core.logging import get_logger

logger = get_logger(__name__)

# In-memory cache for live context (15 min TTL)
_context_cache: TTLCache = TTLCache(maxsize=1, ttl=900)

# Lazy-loaded embedding model
_embed_model: SentenceTransformer | None = None


def _get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embed_model


async def retrieve_chunks(session: AsyncSession, query: str, top_k: int = 5) -> list[dict]:
    """Embed query and retrieve top-k similar document chunks via pgvector."""
    model = _get_embed_model()
    query_embedding = model.encode(query)
    emb_str = "[" + ",".join(str(float(x)) for x in query_embedding) + "]"

    result = await session.execute(
        text("""
            SELECT source, chunk_text, 1 - (embedding <=> :emb::vector) AS similarity
            FROM document_chunks
            ORDER BY embedding <=> :emb::vector
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

    # Current regime
    regime_row = await session.execute(text("""
        SELECT regime_label, confidence
        FROM regime_states
        ORDER BY detected_at DESC
        LIMIT 1
    """))
    regime = regime_row.fetchone()

    # Latest sentiment indices by asset class
    sent_rows = await session.execute(text("""
        SELECT DISTINCT ON (asset_class)
            asset_class, mean_compound
        FROM sentiment_indices
        WHERE source IS NULL
        ORDER BY asset_class, period_start DESC
    """))
    sentiments = {r[0]: round(float(r[1]), 4) for r in sent_rows.fetchall()}

    # Stress level
    stress_row = await session.execute(text("""
        SELECT composite_score FROM stress_index
        ORDER BY as_of_date DESC LIMIT 1
    """))
    stress = stress_row.fetchone()

    # Recent regime transitions
    trans_rows = await session.execute(text("""
        SELECT from_regime, to_regime, transition_date, trigger_description
        FROM regime_transitions
        ORDER BY transition_date DESC
        LIMIT 5
    """))
    transitions = [
        {
            "from": r[0],
            "to": r[1],
            "date": str(r[2]),
            "trigger": r[3],
        }
        for r in trans_rows.fetchall()
    ]

    ctx = {
        "current_regime": regime[0] if regime else None,
        "regime_confidence": round(float(regime[1]), 4) if regime else None,
        "sentiment_scores": sentiments,
        "stress_level": round(float(stress[0]), 4) if stress else None,
        "recent_transitions": transitions,
    }

    # Build human-readable summary
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
