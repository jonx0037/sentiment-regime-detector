"""Document chunk model for RAG vector storage."""

from sqlalchemy import String, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from sentiment_detector.models.base import Base, TimestampMixin


class DocumentChunk(Base, TimestampMixin):
    """Stores embedded document chunks for RAG retrieval."""

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String, nullable=False, comment="Source file path")
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False, comment="Chunk content")
    metadata_: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True, comment="Chunk metadata (section, position)"
    )
    # Note: embedding column (VECTOR(384)) is added via raw SQL in migration
    # because pgvector type isn't natively supported by SQLAlchemy autogenerate
