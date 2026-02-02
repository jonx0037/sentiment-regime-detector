"""Stress Index models for systemic risk indicators."""

from datetime import date as python_date
from uuid import UUID, uuid4

from sqlalchemy import Date, Float, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from sentiment_detector.models.base import Base, TimestampMixin


class StressIndex(Base, TimestampMixin):
    """
    Systemic stress indicators like ECB CISS, VIX, etc.
    
    Used for:
    - Ground truth regime validation (identify known crisis periods)
    - GARCH-MIDAS low-frequency exogenous variable
    
    ECB CISS (Composite Indicator of Systemic Stress):
    - Values range from 0 to ~1
    - High stress threshold typically >= 0.35
    - Crisis peaks: 2008 (~0.7), 2011 (~0.5), 2020 (~0.5)
    """

    __tablename__ = "stress_indices"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Source identification
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="Source: ecb_ciss, vix, cleveland_fci, etc.",
    )
    
    # Temporal information
    date: Mapped[python_date] = mapped_column(
        Date,
        nullable=False,
        index=True,
        comment="Observation date",
    )
    
    # Geographic region (for CISS which has country-level data)
    region: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="ea",  # Euro Area
        comment="Region code: ea (Euro Area), de, fr, it, es, nl, be, at, fi, pt, ie, gr, us",
    )
    
    # Stress value
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Stress index value (typically 0-1 for CISS)",
    )
    
    # Optional metadata
    frequency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
        default="daily",
        comment="Data frequency: daily, weekly, monthly",
    )
    
    # Component values (for CISS sub-indices)
    money_market: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Money market component",
    )
    bond_market: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Bond market component",
    )
    equity_market: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Equity market component",
    )
    foreign_exchange: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Foreign exchange component",
    )
    financial_intermediaries: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Financial intermediaries component",
    )

    __table_args__ = (
        # Unique constraint: one observation per source/date/region
        UniqueConstraint(
            "source", "date", "region",
            name="uq_stress_index_source_date_region",
        ),
        # Composite index for common queries
        Index(
            "ix_stress_index_source_date",
            "source", "date",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<StressIndex(source={self.source!r}, date={self.date}, "
            f"region={self.region!r}, value={self.value:.4f})>"
        )
    
    @property
    def is_high_stress(self) -> bool:
        """Check if value indicates high systemic stress (ECB threshold)."""
        return self.value >= 0.35
    
    @property
    def is_crisis(self) -> bool:
        """Check if value indicates crisis level stress."""
        return self.value >= 0.50
