"""Sentiment analysis endpoints."""

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query

from sentiment_detector.api.schemas.sentiment import (
    SentimentResponse,
    SentimentHistoryResponse,
    AssetClassSentiment,
)

router = APIRouter()

# Asset classes we track
AssetClass = Literal["equity", "crypto", "forex", "commodity"]


@router.get("/current", response_model=SentimentResponse)
async def get_current_sentiment() -> SentimentResponse:
    """
    Get current sentiment scores for all asset classes.
    
    Returns the latest aggregated sentiment indices across
    equities, crypto, forex, and commodities.
    """
    # TODO: Implement real sentiment retrieval from database
    # For now, return mock data for API structure validation
    
    return SentimentResponse(
        timestamp=datetime.now(timezone.utc),
        asset_classes=[
            AssetClassSentiment(
                asset_class="equity",
                compound_score=0.15,
                positive_ratio=0.45,
                negative_ratio=0.25,
                neutral_ratio=0.30,
                sample_count=1250,
                momentum=0.02,
            ),
            AssetClassSentiment(
                asset_class="crypto",
                compound_score=-0.08,
                positive_ratio=0.35,
                negative_ratio=0.40,
                neutral_ratio=0.25,
                sample_count=3420,
                momentum=-0.05,
            ),
            AssetClassSentiment(
                asset_class="forex",
                compound_score=0.02,
                positive_ratio=0.38,
                negative_ratio=0.32,
                neutral_ratio=0.30,
                sample_count=680,
                momentum=0.01,
            ),
            AssetClassSentiment(
                asset_class="commodity",
                compound_score=0.22,
                positive_ratio=0.52,
                negative_ratio=0.20,
                neutral_ratio=0.28,
                sample_count=450,
                momentum=0.08,
            ),
        ],
        cross_asset_mean=0.0775,
        cross_asset_std=0.116,
    )


@router.get("/history", response_model=SentimentHistoryResponse)
async def get_sentiment_history(
    asset_class: AssetClass = Query(..., description="Asset class to retrieve history for"),
    start_date: datetime = Query(..., description="Start date for history"),
    end_date: datetime = Query(default=None, description="End date (defaults to now)"),
    granularity: Literal["hourly", "daily"] = Query(default="daily"),
) -> SentimentHistoryResponse:
    """
    Get historical sentiment data for a specific asset class.
    
    Returns time-series sentiment data with configurable granularity.
    """
    # TODO: Implement real historical data retrieval
    
    return SentimentHistoryResponse(
        asset_class=asset_class,
        start_date=start_date,
        end_date=end_date or datetime.now(timezone.utc),
        granularity=granularity,
        data_points=[],  # Will be populated from database
        total_count=0,
    )


@router.get("/by-source")
async def get_sentiment_by_source(
    asset_class: AssetClass = Query(..., description="Asset class to filter"),
) -> dict:
    """
    Get sentiment breakdown by data source (Reddit, Twitter, News).
    
    Useful for identifying divergence between retail and news sentiment.
    """
    # TODO: Implement source-level breakdown
    
    return {
        "asset_class": asset_class,
        "sources": {
            "reddit": {
                "compound_score": 0.18,
                "sample_count": 2500,
                "subreddits": ["wallstreetbets", "investing", "stocks"],
            },
            "news": {
                "compound_score": 0.05,
                "sample_count": 150,
                "sources": ["reuters", "bloomberg"],
            },
            "twitter": {
                "compound_score": 0.12,
                "sample_count": 800,
            },
        },
        "divergence_score": 0.13,  # How much sources disagree
    }
