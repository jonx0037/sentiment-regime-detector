"""Sentiment analysis endpoints."""

import statistics
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query, Depends
from sqlalchemy import text
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

# The 4 real asset classes per the paper (Section 3.2)
AssetClass = Literal[
    "equity",
    "crypto",
    "forex",
    "commodity",
]


@router.get("/current", response_model=SentimentResponse)
async def get_current_sentiment(
    session: AsyncSession = Depends(get_session),
) -> SentimentResponse:
    """
    Get current sentiment scores for all asset classes.

    Returns the latest aggregated sentiment indices across
    equities, crypto, forex, and commodities.
    """
    import logging

    logger = logging.getLogger(__name__)

    try:
        service = SentimentService()
        sentiment_data = await service.get_current_sentiment(session)
    except Exception as e:
        logger.error(f"Error fetching sentiment data: {e}", exc_info=True)
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

    # Get the latest data date for freshness indicator
    from sqlalchemy import text as sql_text

    latest_date_result = await session.execute(
        sql_text("SELECT MAX(period_start)::date FROM sentiment_indices WHERE source IS NULL")
    )
    latest_date_row = latest_date_result.one_or_none()
    latest_data_date = str(latest_date_row[0]) if latest_date_row and latest_date_row[0] else None

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
        latest_data_date=latest_data_date,
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


@router.get("/cross-asset/history")
async def get_cross_asset_sentiment_history(
    days: int = Query(default=90, le=365, description="Number of days of history"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Get historical cross-asset sentiment data for all asset classes.

    Returns time-series sentiment data for equity, crypto, forex, and commodity.
    """
    # Query the last N days of AVAILABLE data (not relative to CURRENT_DATE,
    # since HPC data may end months/years before today)
    result = await session.execute(
        text("""
        WITH max_date AS (
            SELECT MAX(DATE(period_start)) as latest
            FROM sentiment_indices
            WHERE source IS NULL
              AND asset_class IN ('equity', 'crypto', 'forex', 'commodity')
        )
        SELECT
            DATE(period_start) as date,
            asset_class,
            AVG(mean_compound) as avg_sentiment,
            COUNT(*) as count
        FROM sentiment_indices, max_date
        WHERE source IS NULL
          AND asset_class IN ('equity', 'crypto', 'forex', 'commodity')
          AND DATE(period_start) >= max_date.latest - :days * INTERVAL '1 day'
        GROUP BY DATE(period_start), asset_class
        ORDER BY date, asset_class
    """),
        {"days": days},
    )
    rows = result.fetchall()

    # Organize data by date
    data_by_date = {}
    for row in rows:
        date_str = str(row[0])
        if date_str not in data_by_date:
            data_by_date[date_str] = {"date": date_str}
        data_by_date[date_str][row[1]] = float(row[2]) if row[2] else None

    return {
        "start_date": str(rows[0][0]) if rows else None,
        "end_date": str(rows[-1][0]) if rows else None,
        "count": len(data_by_date),
        "data": list(data_by_date.values()),
    }


@router.get("/by-source")
async def get_sentiment_by_source(
    asset_class: AssetClass = Query(..., description="Asset class to filter"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Get sentiment breakdown by data source (Reddit, Twitter, News).

    Useful for identifying divergence between retail and news sentiment.
    """
    # Query actual source-level breakdown from sentiment_indices
    result = await session.execute(
        text("""
        SELECT
            source,
            AVG(mean_compound) as avg_score,
            SUM(sample_count) as total_count
        FROM sentiment_indices
        WHERE asset_class = :asset_class
          AND source IS NOT NULL
        GROUP BY source
        ORDER BY total_count DESC
    """),
        {"asset_class": asset_class},
    )
    rows = result.fetchall()

    sources = {}
    scores = []
    for row in rows:
        source_name = row[0] or "unknown"
        avg_score = float(row[1]) if row[1] else 0.0
        count = int(row[2])
        sources[source_name] = {
            "compound_score": round(avg_score, 4),
            "sample_count": count,
        }
        scores.append(avg_score)

    # Compute divergence: how much sources disagree (std of scores)
    divergence = 0.0
    if len(scores) > 1:
        mean_score = sum(scores) / len(scores)
        divergence = round((sum((s - mean_score) ** 2 for s in scores) / len(scores)) ** 0.5, 4)

    return {
        "asset_class": asset_class,
        "sources": sources,
        "divergence_score": divergence,
    }
