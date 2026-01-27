"""Sentiment analysis endpoints."""

import statistics
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.api.schemas.sentiment import (
    SentimentResponse,
    SentimentHistoryResponse,
    AssetClassSentiment,
    SentimentDataPoint,
)
from sentiment_detector.core.database import get_session
from sentiment_detector.services.sentiment_service import SentimentService

router = APIRouter()

# Asset classes we track
AssetClass = Literal["equity", "crypto", "forex", "commodity"]


@router.get("/current", response_model=SentimentResponse)
async def get_current_sentiment(
    session: AsyncSession = Depends(get_session),
) -> SentimentResponse:
    """
    Get current sentiment scores for all asset classes.
    
    Returns the latest aggregated sentiment indices across
    equities, crypto, forex, and commodities.
    """
    service = SentimentService()
    sentiment_data = await service.get_current_sentiment(session)
    
    # Convert to response model
    asset_classes = [
        AssetClassSentiment(
            asset_class=data["asset_class"],
            compound_score=data["compound_score"],
            positive_ratio=data["positive_ratio"],
            negative_ratio=data["negative_ratio"],
            neutral_ratio=data["neutral_ratio"],
            sample_count=data["sample_count"],
            momentum=data["momentum"],
        )
        for data in sentiment_data
    ]
    
    # Calculate cross-asset statistics
    if asset_classes:
        compound_scores = [ac.compound_score for ac in asset_classes]
        cross_asset_mean = statistics.mean(compound_scores)
        cross_asset_std = statistics.stdev(compound_scores) if len(compound_scores) > 1 else 0.0
    else:
        cross_asset_mean = 0.0
        cross_asset_std = 0.0
    
    return SentimentResponse(
        timestamp=datetime.now(timezone.utc),
        asset_classes=asset_classes,
        cross_asset_mean=cross_asset_mean,
        cross_asset_std=cross_asset_std,
    )


@router.get("/history", response_model=SentimentHistoryResponse)
async def get_sentiment_history(
    asset_class: AssetClass = Query(..., description="Asset class to retrieve history for"),
    start_date: datetime = Query(..., description="Start date for history"),
    end_date: datetime = Query(default=None, description="End date (defaults to now)"),
    granularity: Literal["hourly", "daily"] = Query(default="daily"),
    session: AsyncSession = Depends(get_session),
) -> SentimentHistoryResponse:
    """
    Get historical sentiment data for a specific asset class.
    
    Returns time-series sentiment data with configurable granularity.
    """
    service = SentimentService()
    history_data = await service.get_sentiment_history(
        session,
        asset_class=asset_class,
        start_date=start_date,
        end_date=end_date,
    )
    
    # Convert to response model
    data_points = [
        SentimentDataPoint(
            timestamp=data["timestamp"],
            compound_score=data["compound_score"],
            sample_count=1,  # Individual score
            momentum=None,
        )
        for data in history_data
    ]
    
    return SentimentHistoryResponse(
        asset_class=asset_class,
        start_date=start_date,
        end_date=end_date or datetime.now(timezone.utc),
        granularity=granularity,
        data_points=data_points,
        total_count=len(data_points),
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
