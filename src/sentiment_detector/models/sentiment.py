"""Sentiment score models."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sentiment_detector.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from sentiment_detector.models.text_record import RawText


class SentimentScore(Base, TimestampMixin):
    """
    Sentiment scores for individual text records.
    
    Stores the output of sentiment analysis models.
    Each text can have multiple scores from different models.
    """

    __tablename__ = "sentiment_scores"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign key to raw text
    text_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("raw_texts.id", ondelete="CASCADE"),
        nullable=False,
    )
    
    # Model information
    model_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Model used: finbert, roberta, distilbert",
    )
    model_version: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Model version or checkpoint",
    )
    
    # Sentiment scores (probabilities)
    positive: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Positive sentiment probability",
    )
    negative: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Negative sentiment probability",
    )
    neutral: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Neutral sentiment probability",
    )
    compound: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Compound score (-1 to 1)",
    )
    
    # Confidence (max probability)
    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Model confidence (max of positive/negative/neutral)",
    )
    
    # Processing timestamp
    processed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="When this text was processed",
    )
    
    # Relationship to raw text
    text: Mapped["RawText"] = relationship(
        "RawText",
        back_populates="sentiment_scores",
    )

    __table_args__ = (
        # Unique constraint: one score per model per text
        Index(
            "ix_sentiment_scores_text_model",
            "text_id",
            "model_name",
            unique=True,
        ),
        # Index for time-based queries
        Index("ix_sentiment_scores_processed_at", "processed_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<SentimentScore(id={self.id}, model={self.model_name}, "
            f"compound={self.compound:.3f})>"
        )


class SentimentIndex(Base, TimestampMixin):
    """
    Aggregated sentiment indices (hourly/daily).
    
    Pre-computed aggregations for fast querying of
    historical sentiment trends.
    """

    __tablename__ = "sentiment_indices"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Classification
    asset_class: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Asset class: equity, crypto, forex, commodity",
    )
    source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="Data source (NULL = all sources aggregated)",
    )
    
    # Time period
    period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Start of aggregation period",
    )
    period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="End of aggregation period",
    )
    granularity: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Time granularity: hourly, daily",
    )
    
    # Aggregated metrics
    mean_compound: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Mean compound score for period",
    )
    std_compound: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Standard deviation of compound scores",
    )
    sample_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Number of texts in aggregation",
    )
    positive_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Ratio of positive texts",
    )
    negative_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Ratio of negative texts",
    )
    
    # Momentum indicators
    sentiment_momentum: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Rate of change from previous period",
    )
    sentiment_acceleration: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Second derivative of sentiment",
    )

    __table_args__ = (
        # Unique constraint: one index per asset/source/period
        Index(
            "ix_sentiment_indices_unique",
            "asset_class",
            "source",
            "period_start",
            "granularity",
            unique=True,
        ),
        # Index for time-series queries
        Index("ix_sentiment_indices_period", "period_start", "asset_class"),
    )

    def __repr__(self) -> str:
        return (
            f"<SentimentIndex(asset={self.asset_class}, "
            f"period={self.period_start}, mean={self.mean_compound:.3f})>"
        )
