"""Ingest project documents into pgvector for RAG retrieval.

Usage:
    python scripts/ingest_rag_corpus.py

Idempotent: Clears existing chunks and re-ingests from scratch.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import asyncio
import json

from sentence_transformers import SentenceTransformer
from sqlalchemy import text

from sentiment_detector.core.database import async_session_maker


# --- Configuration ---
CHAR_CHUNK_SIZE = 2048
CHAR_OVERLAP = 200

CORPUS_PATHS = [
    ("docs", "docs/*.md"),
    ("research-summaries", "course_files/research/summaries/*.md"),
    ("research", "course_files/research/*.md"),
    ("readme", "README.md"),
]

MODEL_NAME = "all-MiniLM-L6-v2"


def discover_files(project_root: Path) -> list[tuple[str, Path]]:
    """Find all corpus files."""
    files = []
    seen = set()
    for label, pattern in CORPUS_PATHS:
        for p in sorted(project_root.glob(pattern)):
            if p.is_file() and p not in seen:
                seen.add(p)
                files.append((label, p))
    return files


def chunk_text(content: str, chunk_size: int = CHAR_CHUNK_SIZE, overlap: int = CHAR_OVERLAP) -> list[str]:
    """Split text into overlapping chunks by character count."""
    if len(content) <= chunk_size:
        return [content]

    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]

        # Try to break at paragraph or sentence boundary
        if end < len(content):
            last_para = chunk.rfind("\n\n")
            if last_para > chunk_size // 2:
                end = start + last_para + 2
                chunk = content[start:end]
            else:
                last_period = chunk.rfind(". ")
                if last_period > chunk_size // 2:
                    end = start + last_period + 2
                    chunk = content[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return [c for c in chunks if c]


async def ingest(project_root: Path) -> None:
    """Main ingestion pipeline."""
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # Discover files
    files = discover_files(project_root)
    print(f"Found {len(files)} corpus files")

    # Chunk all files
    all_chunks: list[dict] = []
    for label, filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        relative = str(filepath.relative_to(project_root))
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": relative,
                "chunk_text": chunk,
                "metadata": {"label": label, "chunk_index": i, "total_chunks": len(chunks)},
            })

    print(f"Generated {len(all_chunks)} chunks")

    # Embed all chunks
    print("Embedding chunks...")
    texts = [c["chunk_text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

    # Upsert to database
    print("Upserting to database...")
    async with async_session_maker() as session:
        # Clear existing chunks (idempotent)
        await session.execute(text("DELETE FROM document_chunks"))

        # Insert in batches
        batch_size = 50
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]

            for chunk, emb in zip(batch, batch_embeddings):
                # PostgreSQL array literal format: {1.0,2.0,3.0}
                emb_str = "{" + ",".join(str(float(x)) for x in emb) + "}"
                await session.execute(
                    text("""
                        INSERT INTO document_chunks (source, chunk_text, metadata, embedding, created_at, updated_at)
                        VALUES (:source, :chunk_text, :metadata::jsonb, :embedding::float8[], now(), now())
                    """),
                    {
                        "source": chunk["source"],
                        "chunk_text": chunk["chunk_text"],
                        "metadata": json.dumps(chunk["metadata"]),
                        "embedding": emb_str,
                    },
                )

            await session.commit()
            print(f"  Inserted batch {i // batch_size + 1}/{(len(all_chunks) + batch_size - 1) // batch_size}")

    print(f"Done! Ingested {len(all_chunks)} chunks from {len(files)} files.")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    asyncio.run(ingest(project_root))
