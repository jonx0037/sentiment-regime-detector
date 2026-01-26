"""Regime detection schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


RegimeState = Literal["risk_on", "risk_off", "transition"]


class RegimeResponse(BaseModel):
    """Current regime state response."""

    timestamp: datetime = Field(..., description="Timestamp of regime classification")
    regime: RegimeState = Field(..., description="Current market regime")
    confidence: float = Field(
        ..., ge=0, le=1, description="Confidence in the classification"
    )
    probabilities: dict[RegimeState, float] = Field(
        ..., description="Probability distribution across regime states"
    )
    features: dict[str, float] = Field(
        ..., description="Key features used for classification"
    )
    model_version: str = Field(..., description="Version of the regime classifier")


class RegimeDataPoint(BaseModel):
    """Single data point in regime time series."""

    timestamp: datetime
    regime: RegimeState
    confidence: float


class RegimeHistoryResponse(BaseModel):
    """Historical regime data response."""

    start_date: datetime = Field(..., description="Start of date range")
    end_date: datetime = Field(..., description="End of date range")
    regimes: list[RegimeDataPoint] = Field(..., description="Time series of regimes")
    transition_count: int = Field(
        ..., description="Number of regime transitions in period"
    )


class RegimeTransition(BaseModel):
    """Regime transition record."""

    id: str = Field(..., description="Unique transition identifier")
    from_regime: RegimeState = Field(..., description="Previous regime state")
    to_regime: RegimeState = Field(..., description="New regime state")
    transition_start: datetime = Field(
        ..., description="When transition was first detected"
    )
    transition_end: datetime | None = Field(
        default=None, description="When new regime stabilized"
    )
    duration_hours: float | None = Field(
        default=None, description="Duration of transition in hours"
    )
    trigger_features: dict[str, float] = Field(
        ..., description="Features that triggered the transition"
    )
    validated: bool = Field(
        default=False,
        description="Whether transition was validated by subsequent price action",
    )
