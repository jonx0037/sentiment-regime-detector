"""Raw text data models."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sentiment_detector.models.base import Base, TimestampMixin


class RawText(Base, TimestampMixin):
    """
    Raw text records from all data sources.
    
    Stores text content from Reddit, Twitter, News, etc.
    with metadata for tracking source and asset class.
    """

    __tablename__ = "raw_texts"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Source information
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Data source: reddit, twitter, news",
    )
    source_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Original ID from source platform",
    )
    
    # Classification
    asset_class: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Asset class: equity, crypto, forex, commodity",
    )
    
    # Timestamps
    content_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When the content was originally created",
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When we collected this content",
    )
    
    # Content
    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Title (for posts/articles)",
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Main text content",
    )
    
    # Source-specific metadata (flexible JSON storage)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
        comment="Source-specific metadata (score, author, etc.)",
    )
    
    # Relationships
    sentiment_scores: Mapped[list["SentimentScore"]] = relationship(
        "SentimentScore",
        back_populates="text",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        # Unique constraint on source + source_id to prevent duplicates
        Index(
            "ix_raw_texts_source_source_id",
            "source",
            "source_id",
            unique=True,
            postgresql_where=(source_id.isnot(None)),
        ),
        # Index for time-based queries
        Index("ix_raw_texts_content_created_at", "content_created_at"),
        # Index for asset class filtering
        Index("ix_raw_texts_asset_class", "asset_class"),
    )

    def __repr__(self) -> str:
        return f"<RawText(id={self.id}, source={self.source}, asset_class={self.asset_class})>"


# Import at bottom to avoid circular imports
from sentiment_detector.models.sentiment import SentimentScore
