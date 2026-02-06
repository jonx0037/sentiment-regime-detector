"""Explainability schemas for SHAP/LIME analysis."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


RegimeState = Literal["risk_on", "risk_off", "transition"]


class FeatureContribution(BaseModel):
    """Single feature's contribution to prediction."""

    feature_name: str = Field(..., description="Name of the feature")
    value: float = Field(..., description="Feature value")
    shap_value: float = Field(..., description="SHAP contribution to prediction")
    rank: int = Field(..., ge=1, description="Importance rank (1=most important)")


class ExplanationResponse(BaseModel):
    """SHAP explanation for a regime prediction."""

    timestamp: datetime = Field(..., description="Timestamp of prediction")
    predicted_regime: RegimeState = Field(..., description="Predicted market regime")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    base_value: float = Field(..., description="Expected value (model average)")
    prediction_value: float = Field(..., description="Model output for predicted class")
    top_features: list[FeatureContribution] = Field(
        ...,
        description="Top contributing features (typically top 10)"
    )
    all_features: list[FeatureContribution] = Field(
        ...,
        description="All feature contributions"
    )
    model_version: str = Field(..., description="Model version used")
    cache_hit: bool = Field(
        default=False,
        description="Whether result came from cache"
    )


class GlobalImportanceResponse(BaseModel):
    """Global feature importance across all predictions."""

    computed_at: datetime = Field(..., description="When analysis was computed")
    sample_size: int = Field(..., ge=1, description="Number of samples analyzed")
    feature_importance: dict[str, float] = Field(
        ...,
        description="Feature -> mean |SHAP| value mapping"
    )
    top_features: list[tuple[str, float]] = Field(
        ...,
        description="Top 10 features by importance [(name, importance)]"
    )
    model_version: str = Field(..., description="Model version used")


class FeatureInteraction(BaseModel):
    """Interaction between two features."""

    feature_1: str = Field(..., description="First feature name")
    feature_2: str = Field(..., description="Second feature name")
    interaction_strength: float = Field(..., description="Mean |interaction| value")


class InteractionResponse(BaseModel):
    """Feature interaction analysis."""

    computed_at: datetime = Field(..., description="When analysis was computed")
    sample_size: int = Field(..., ge=1, description="Number of samples analyzed")
    top_interactions: list[FeatureInteraction] = Field(
        ...,
        description="Top feature pairs by interaction strength"
    )
    model_version: str = Field(..., description="Model version used")


class CrisisEvent(BaseModel):
    """Historical crisis event metadata."""

    event_id: str = Field(..., description="Unique event identifier")
    name: str = Field(..., description="Human-readable event name")
    date: str = Field(..., description="Peak crisis date (YYYY-MM-DD)")
    description: str = Field(..., description="Brief event description")
    ciss_peak: float | None = Field(default=None, description="CISS value at peak")
    vix_peak: float | None = Field(default=None, description="VIX value at peak")


class EventExplanationResponse(BaseModel):
    """SHAP explanation for a historical crisis event."""

    event: CrisisEvent = Field(..., description="Event metadata")
    explanation: ExplanationResponse = Field(..., description="SHAP explanation")
