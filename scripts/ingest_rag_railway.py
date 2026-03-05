"""One-shot RAG ingestion directly to Railway PostgreSQL via Cohere + psycopg2.

Uses Cohere embed-english-v3.0 API for embeddings (1024 dims).
Bypasses torch/sentence-transformers entirely.
Safe to delete after ingestion completes.
"""

import json
import os
import ssl
import sys
import time
import urllib.request
from pathlib import Path

import psycopg2

# --- Config ---
PROJECT_ROOT = Path(__file__).parent.parent
RAILWAY_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/railway")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "")
COHERE_EMBED_URL = "https://api.cohere.com/v2/embed"
COHERE_EMBED_MODEL = "embed-english-v3.0"
CHAR_CHUNK_SIZE = 2048
CHAR_OVERLAP = 200

CORPUS_PATHS = [
    ("docs", "docs/*.md"),
    ("research-summaries", "course_files/research/summaries/*.md"),
    ("research", "course_files/research/*.md"),
    ("readme", "README.md"),
]


def discover_files() -> list[tuple[str, Path]]:
    files = []
    seen = set()
    for label, pattern in CORPUS_PATHS:
        for p in sorted(PROJECT_ROOT.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append((label, p))
    return files


def chunk_text(content: str) -> list[str]:
    if len(content) <= CHAR_CHUNK_SIZE:
        return [content]
    chunks = []
    start = 0
    while start < len(content):
        end = start + CHAR_CHUNK_SIZE
        chunk = content[start:end]
        if end < len(content):
            last_para = chunk.rfind("\n\n")
            if last_para > CHAR_CHUNK_SIZE // 2:
                end = start + last_para + 2
                chunk = content[start:end]
            else:
                last_period = chunk.rfind(". ")
                if last_period > CHAR_CHUNK_SIZE // 2:
                    end = start + last_period + 2
                    chunk = content[start:end]
        chunks.append(chunk.strip())
        start = end - CHAR_OVERLAP
    return [c for c in chunks if c]


_SSL_CTX = ssl.create_default_context()


def embed_batch(texts: list[str], input_type: str = "search_document") -> list[list[float]]:
    """Embed a batch of texts using Cohere API via urllib. Max 96 texts per call."""
    payload = json.dumps({
        "texts": texts,
        "model": COHERE_EMBED_MODEL,
        "input_type": input_type,
        "embedding_types": ["float"],
    }).encode()
    req = urllib.request.Request(
        COHERE_EMBED_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    resp = urllib.request.urlopen(req, timeout=60, context=_SSL_CTX)
    return json.loads(resp.read())["embeddings"]["float"]


def main():
    if not COHERE_API_KEY:
        print("Error: COHERE_API_KEY environment variable required")
        sys.exit(1)
    print(f"Using Cohere {COHERE_EMBED_MODEL} for embeddings")

    # Discover and chunk
    files = discover_files()
    print(f"Found {len(files)} corpus files")

    all_chunks = []
    for label, filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        relative = str(filepath.relative_to(PROJECT_ROOT))
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": relative,
                "chunk_text": chunk,
                "metadata": {"label": label, "chunk_index": i, "total_chunks": len(chunks)},
            })
    print(f"Generated {len(all_chunks)} chunks from {len(files)} files")

    # Embed in batches (Cohere limit: 96 texts per request)
    print("Embedding chunks via Cohere API...")
    cohere_batch_size = 96
    all_embeddings = []
    for i in range(0, len(all_chunks), cohere_batch_size):
        batch_texts = [c["chunk_text"] for c in all_chunks[i:i + cohere_batch_size]]
        batch_embs = embed_batch(batch_texts)
        all_embeddings.extend(batch_embs)
        batch_num = i // cohere_batch_size + 1
        total_batches = (len(all_chunks) + cohere_batch_size - 1) // cohere_batch_size
        print(f"  Embedded batch {batch_num}/{total_batches} ({len(all_embeddings)}/{len(all_chunks)} chunks)")
        if i + cohere_batch_size < len(all_chunks):
            time.sleep(0.5)  # Rate limit courtesy

    print(f"Embedded {len(all_embeddings)} chunks (dim={len(all_embeddings[0])})")

    # Insert to Railway
    print("Connecting to Railway PostgreSQL...")
    conn = psycopg2.connect(RAILWAY_URL)
    cur = conn.cursor()

    # Clear existing
    cur.execute("DELETE FROM document_chunks")
    conn.commit()
    print("Cleared existing chunks")

    # Insert in batches
    db_batch_size = 50
    total_db_batches = (len(all_chunks) + db_batch_size - 1) // db_batch_size
    for i in range(0, len(all_chunks), db_batch_size):
        batch = all_chunks[i:i + db_batch_size]
        batch_embeddings = all_embeddings[i:i + db_batch_size]

        for chunk, emb in zip(batch, batch_embeddings):
            emb_str = "{" + ",".join(str(float(x)) for x in emb) + "}"
            cur.execute(
                """
                INSERT INTO document_chunks (source, chunk_text, metadata, embedding, created_at, updated_at)
                VALUES (%s, %s, %s::jsonb, %s::float8[], now(), now())
                """,
                (chunk["source"], chunk["chunk_text"], json.dumps(chunk["metadata"]), emb_str),
            )

        conn.commit()
        batch_num = i // db_batch_size + 1
        print(f"  DB batch {batch_num}/{total_db_batches}")

    # Verify
    cur.execute("SELECT COUNT(*) FROM document_chunks")
    count = cur.fetchone()[0]
    print(f"\nDone! Inserted {count} chunks from {len(files)} files.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
