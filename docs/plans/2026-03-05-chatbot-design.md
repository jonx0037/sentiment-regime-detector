# Chatbot Design: Hybrid RAG + Live Context

**Date:** 2026-03-05
**Status:** Approved
**Based on:** `docs/chatbot-handoff-brief.md`

---

## Architecture Overview

AI-powered chatbot for the market sentiment dashboard that answers two classes of questions:

1. **Methodology/research** — answered via RAG over the project's static document corpus (pgvector)
2. **Live dashboard state** — answered via dynamic context injection from PostgreSQL at query time

Uses Anthropic Claude API (`claude-sonnet-4-20250514`). Scoped strictly to project domain.

## Key Decisions (Deviations from Brief)

| Brief | Validated Design | Rationale |
|-------|-----------------|-----------|
| OpenAI `text-embedding-3-small` (1536d) | Local `all-MiniLM-L6-v2` (384d) | Already installed via sentence-transformers, zero cost, no API key |
| IVFFlat index | HNSW index | Better accuracy for small corpus (<1K vectors) |
| `fastapi-cache2[redis]` | `cachetools.TTLCache` (in-memory) | Redis is optional in config — simpler, no new dep |
| pgvector `vector(1536)` | `vector(384)` | Matches local model output dimension |
| `langchain-text-splitters` | Manual chunker | Avoid LangChain dependency for one function |

## RAG Corpus

- **14 docs** — `docs/*.md` (methodology, architecture, deployment, etc.)
- **52 research summaries** — `course_files/research/summaries/*.md`
- **README.md**
- **Total:** ~67 source documents → ~300-500 chunks at 512 tokens/chunk, 50-token overlap

## Backend

### New Table: `document_chunks`

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    source VARCHAR NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX document_chunks_embedding_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops);
```

### New Endpoints

**`GET /api/v1/chatbot/context`**
- Aggregates live dashboard state from `sentiment_indices`, `regime_states`, `stress_index`
- Returns: current regime, sentiment scores, stress indicators, recent transitions, top drivers
- Cached 15 min via in-memory TTL cache

**`POST /api/v1/chatbot/query`**
- Request: `{ query, conversation_history, max_history_turns }`
- Response: `{ response, sources_used, regime_context_used }`
- Pipeline: embed query → pgvector top-5 → fetch live context → assemble prompt → Claude API

### New Script: `scripts/ingest_rag_corpus.py`
- Reads all source docs, chunks, embeds with `all-MiniLM-L6-v2`, upserts to `document_chunks`
- Idempotent (re-runnable)

## Frontend

### New Components: `frontend/src/components/chatbot/`

| File | Purpose |
|------|---------|
| `ChatbotWidget.tsx` | Floating button + slide-up panel |
| `ChatMessage.tsx` | Individual message bubble |
| `ChatInput.tsx` | Text input + send button |
| `useChatbot.ts` | Custom hook (state, API calls) |

### UI
- Floating `MessageSquare` button, bottom-right, z-50
- Panel: 380px x 520px, dark theme (`bg-gray-900 border-gray-700`)
- Three-dot typing indicator, auto-scroll
- Disclaimer: "Research tool only. Not financial advice."
- History trimmed to last 6 turns

### Integration
- Mounted in `page.tsx` as fixed overlay outside main content grid
- All API calls go through FastAPI backend (no direct Anthropic calls)

## System Prompt

Assembled dynamically from:
1. Static preamble (role, scope rules, tone)
2. Live context block (current regime, sentiment scores, stress indicators)
3. RAG context block (top-k retrieved chunks with source filenames)

## New Dependencies

### Backend (requirements.txt)
```
pgvector>=0.2.4
anthropic>=0.25.0
```

### Frontend
None — uses existing fetch API and Tailwind.

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...  # Backend only
```

## Implementation Phases

1. **Backend Foundation** — Alembic migration, ingestion script, context endpoint
2. **RAG + Claude Integration** — Retrieval function, prompt assembly, query endpoint
3. **Frontend Component** — Chat atoms, hook, widget, dashboard integration
4. **Polish** — Rate limiting, input sanitization, error boundary
