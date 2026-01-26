"""Regime state models."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from sentiment_detector.models.base import Base, TimestampMixin


class RegimeState(Base, TimestampMixin):
    """
    Point-in-time regime classifications.
    
    Stores the output of the regime classifier at each
    timestamp, including probabilities for all states.
    """

    __tablename__ = "regime_states"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Timestamp of classification
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        unique=True,
        comment="Timestamp of regime classification",
    )
    
    # Classification result
    regime: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Regime: risk_on, risk_off, transition",
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Confidence in classification (0-1)",
    )
    
    # Model information
    model_version: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Model version used for classification",
    )
    
    # Probability distribution
    prob_risk_on: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Probability of risk_on state",
    )
    prob_risk_off: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Probability of risk_off state",
    )
    prob_transition: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        comment="Probability of transition state",
    )
    
    # Features used for classification (for explainability)
    features: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Input features used for classification",
    )

    __table_args__ = (
        Index("ix_regime_states_timestamp", "timestamp"),
        Index("ix_regime_states_regime", "regime"),
    )

    def __repr__(self) -> str:
        return (
            f"<RegimeState(timestamp={self.timestamp}, "
            f"regime={self.regime}, confidence={self.confidence:.2f})>"
        )


class RegimeTransition(Base, TimestampMixin):
    """
    Regime transition records.
    
    Tracks when the market transitions between regimes,
    along with duration and trigger features.
    """

    __tablename__ = "regime_transitions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Transition states
    from_regime: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Previous regime state",
    )
    to_regime: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="New regime state",
    )
    
    # Timestamps
    transition_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        unique=True,
        comment="When transition was first detected",
    )
    transition_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When new regime stabilized",
    )
    duration_hours: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Duration of transition in hours",
    )
    
    # Analysis
    trigger_features: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="Features that triggered the transition",
    )
    
    # Validation (was transition confirmed by price action?)
    validated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether validated by subsequent price action",
    )

    __table_args__ = (
        Index("ix_regime_transitions_start", "transition_start"),
        Index("ix_regime_transitions_from_to", "from_regime", "to_regime"),
    )

    def __repr__(self) -> str:
        return (
            f"<RegimeTransition({self.from_regime} → {self.to_regime}, "
            f"start={self.transition_start})>"
        )
