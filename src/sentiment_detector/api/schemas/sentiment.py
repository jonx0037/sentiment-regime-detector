"""Sentiment-related schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AssetClass = Literal[
    "equity", "equities", "crypto", "forex", "commodity",
    "cross-asset", "cross_asset", "news", "social",
]


class AssetClassSentiment(BaseModel):
    """Sentiment data for a single asset class."""

    asset_class: AssetClass = Field(..., description="Asset class identifier")
    compound_score: float = Field(
        ..., ge=-1, le=1, description="Aggregated sentiment score (-1 to 1)"
    )
    positive_ratio: float = Field(
        ..., ge=0, le=1, description="Ratio of positive sentiment texts"
    )
    negative_ratio: float = Field(
        ..., ge=0, le=1, description="Ratio of negative sentiment texts"
    )
    neutral_ratio: float = Field(
        ..., ge=0, le=1, description="Ratio of neutral sentiment texts"
    )
    sample_count: int = Field(..., ge=0, description="Number of texts analyzed")
    momentum: float = Field(
        ..., description="Rate of change in sentiment (positive = improving)"
    )


class SentimentResponse(BaseModel):
    """Current sentiment response for all asset classes."""

    timestamp: datetime = Field(..., description="Timestamp of sentiment calculation")
    asset_classes: list[AssetClassSentiment] = Field(
        ..., description="Sentiment data per asset class"
    )
    cross_asset_mean: float = Field(
        ..., description="Mean sentiment across all asset classes"
    )
    cross_asset_std: float = Field(
        ..., description="Standard deviation of sentiment across asset classes"
    )


class SentimentDataPoint(BaseModel):
    """Single data point in sentiment time series."""

    timestamp: datetime
    compound_score: float
    sample_count: int
    momentum: float | None = None


class SentimentHistoryResponse(BaseModel):
    """Historical sentiment data response."""

    asset_class: AssetClass = Field(..., description="Asset class for this history")
    start_date: datetime = Field(..., description="Start of date range")
    end_date: datetime = Field(..., description="End of date range")
    granularity: Literal["hourly", "daily"] = Field(
        ..., description="Time granularity of data points"
    )
    data_points: list[SentimentDataPoint] = Field(
        ..., description="Time series data points"
    )
    total_count: int = Field(..., description="Total number of data points")
