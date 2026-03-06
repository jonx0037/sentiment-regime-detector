"""Chatbot service: RAG retrieval, context assembly, Claude API."""

import httpx
from cachetools import TTLCache
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.core.config import settings
from sentiment_detector.core.logging import get_logger

logger = get_logger(__name__)

# In-memory cache for live context (2 min TTL — dashboard refreshes every 30-60s)
_context_cache: TTLCache = TTLCache(maxsize=1, ttl=120)

COHERE_EMBED_URL = "https://api.cohere.com/v2/embed"
COHERE_EMBED_MODEL = "embed-english-v3.0"


async def _embed_query(query: str) -> list[float]:
    """Embed a query string using Cohere API. Returns embedding as list of floats."""
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
    return [float(x) for x in embedding]


async def retrieve_chunks(session: AsyncSession, query: str, top_k: int = 5) -> list[dict]:
    """Embed query and retrieve top-k similar document chunks via cosine similarity."""
    emb_str = await _embed_query(query)

    result = await session.execute(
        text("""
            SELECT source, chunk_text,
                   cosine_similarity(embedding, CAST(:emb AS float8[])) AS similarity
            FROM document_chunks
            ORDER BY cosine_similarity(embedding, CAST(:emb AS float8[])) DESC
            LIMIT :top_k
        """),
        {"emb": emb_str, "top_k": top_k},
    )
    rows = result.fetchall()
    return [{"source": r[0], "chunk_text": r[1], "similarity": float(r[2])} for r in rows]


async def fetch_live_context(session: AsyncSession) -> dict:
    """Fetch current dashboard state using the same classifier logic as the dashboard.

    This mirrors what ``/api/v1/regime/current`` computes so the chatbot
    always agrees with what the user sees in the UI.  Cached for 2 min.
    """
    if "ctx" in _context_cache:
        return _context_cache["ctx"]

    # Lazy imports to avoid circular deps at module level
    from sentiment_detector.api.routes.regime import (
        get_latest_features,
        compute_volatility_state,
    )
    from sentiment_detector.services.regime_classifier import (
        MLRegimeClassifier,
        RegimeClassifier,
    )

    regime_label = "unknown"
    regime_confidence = None
    probabilities: dict = {}
    volatility_regime = None
    volatility_score = None
    sentiments: dict = {}
    ciss_level = None
    vix_level = None
    transitions: list = []

    # ── 1. Classify regime (same path as the dashboard endpoint) ──
    try:
        features = await get_latest_features(session)

        try:
            classifier = MLRegimeClassifier()
            classification = classifier.classify(features)
        except Exception:
            classifier = RegimeClassifier()
            classification = classifier.classify(features)

        regime_label = classification.state.value
        regime_confidence = round(classification.confidence, 4)
        probabilities = {
            "risk_on": round(classification.prob_risk_on, 4),
            "risk_off": round(classification.prob_risk_off, 4),
            "transition": round(classification.prob_transition, 4),
        }

        sentiments = {
            "equity": round(features.equity_sentiment, 4),
            "crypto": round(features.crypto_sentiment, 4),
            "forex": round(features.forex_sentiment, 4),
            "commodity": round(features.commodity_sentiment, 4),
        }

        ciss_level = round(features.ciss_level, 4) if features.ciss_level is not None else None
        vix_level = round(features.vix_level, 2) if features.vix_level is not None else None

        vol_state, vol_score = compute_volatility_state(features.ciss_level, features.vix_level)
        volatility_regime = vol_state
        volatility_score = round(vol_score, 4)
    except Exception as e:
        logger.warning("Failed to classify regime from features", error=str(e))

    # ── 2. Compute recent transitions from actual CISS/VIX data ──
    try:
        trans_result = await session.execute(text("""
            WITH regime_data AS (
                SELECT
                    si.date,
                    si.value AS ciss,
                    md.close AS vix,
                    CASE
                        WHEN si.value < 0.2 AND md.close < 20 THEN 'risk_on'
                        WHEN si.value > 0.4 OR md.close > 30 THEN 'risk_off'
                        ELSE 'transition'
                    END AS regime
                FROM stress_indices si
                LEFT JOIN market_data md
                    ON si.date = md.date AND md.symbol = '^VIX'
                WHERE si.source = 'ecb_ciss'
                ORDER BY si.date
            ),
            transitions AS (
                SELECT
                    date, regime,
                    LAG(regime) OVER (ORDER BY date) AS prev_regime,
                    ciss, vix
                FROM regime_data
            )
            SELECT date, prev_regime, regime, ciss, vix
            FROM transitions
            WHERE prev_regime IS NOT NULL AND prev_regime != regime
            ORDER BY date DESC
            LIMIT 5
        """))
        transitions = [
            {
                "from": r[1],
                "to": r[2],
                "date": str(r[0]),
                "ciss": round(float(r[3]), 4) if r[3] else None,
                "vix": round(float(r[4]), 2) if r[4] else None,
            }
            for r in trans_result.fetchall()
        ]
    except Exception as e:
        logger.warning("Failed to compute regime transitions", error=str(e))

    # ── 3. Assemble context dict ──
    ctx = {
        "current_regime": regime_label,
        "regime_confidence": regime_confidence,
        "probabilities": probabilities,
        "sentiment_scores": sentiments,
        "stress_level": ciss_level,
        "vix_level": vix_level,
        "volatility_regime": volatility_regime,
        "volatility_score": volatility_score,
        "recent_transitions": transitions,
    }

    sent_summary = ", ".join(f"{k}: {v}" for k, v in sentiments.items()) or "no data"
    prob_str = ", ".join(f"{k}: {v}" for k, v in probabilities.items()) if probabilities else "N/A"
    vol_str = f"{volatility_regime} (score: {volatility_score})" if volatility_regime else "N/A"
    ctx["summary"] = (
        f"Current regime: {regime_label} (confidence: {regime_confidence or 'N/A'}). "
        f"Probabilities — {prob_str}. "
        f"Volatility regime: {vol_str}. "
        f"Sentiment scores — {sent_summary}. "
        f"CISS stress index: {ciss_level if ciss_level is not None else 'N/A'}. "
        f"VIX: {vix_level if vix_level is not None else 'N/A'}."
    )

    _context_cache["ctx"] = ctx
    return ctx


SYSTEM_PREAMBLE = """You are Jon, the research assistant for the Cross-Asset Sentiment Regime Detector dashboard (market-sentiment.io).

Your role:
- Answer questions about the project's methodology, data sources, models, and architecture.
- Explain the current market regime, sentiment scores, and stress indicators shown on the dashboard.
- Cite your sources when referencing project documentation.

Important: The "Current Dashboard State" section below contains EXACTLY what the user sees on the dashboard right now. When the user asks about what the dashboard shows, refer to these values directly and confidently — they are the live values.

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

    # Regime probabilities
    if live_context.get("probabilities"):
        parts.append(f"\nRegime probabilities: {live_context['probabilities']}")

    # Volatility regime
    if live_context.get("volatility_regime"):
        parts.append(
            f"Volatility regime: {live_context['volatility_regime']} "
            f"(score: {live_context.get('volatility_score', 'N/A')})"
        )

    if live_context.get("recent_transitions"):
        parts.append("\nRecent regime transitions:")
        for t in live_context["recent_transitions"][:3]:
            ciss_str = f", CISS: {t['ciss']}" if t.get("ciss") else ""
            vix_str = f", VIX: {t['vix']}" if t.get("vix") else ""
            parts.append(f"- {t['date']}: {t['from']} → {t['to']}{ciss_str}{vix_str}")

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
        "regime_context_used": live_context["current_regime"] != "unknown",
    }
