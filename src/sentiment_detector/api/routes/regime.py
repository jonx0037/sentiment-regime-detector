"""Regime detection endpoints."""

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.api.schemas.regime import (
    RegimeResponse,
    RegimeHistoryResponse,
    RegimeTransition,
)
from sentiment_detector.core.database import get_session
from sentiment_detector.models import SentimentIndex
from sentiment_detector.services.regime_classifier import (
    RegimeClassifier,
    MLRegimeClassifier,
    SentimentFeatures,
)

router = APIRouter()

RegimeState = Literal["risk_on", "risk_off", "transition"]


async def get_latest_features(session: AsyncSession) -> SentimentFeatures:
    """Fetch latest sentiment features from database."""
    
    # Get latest indices by asset class
    result = await session.execute(text("""
        SELECT DISTINCT ON (asset_class)
            asset_class,
            mean_compound,
            std_compound,
            sentiment_momentum
        FROM sentiment_indices
        WHERE source IS NULL
        ORDER BY asset_class, period_start DESC
    """))
    rows = result.fetchall()
    
    sentiments = {}
    for row in rows:
        sentiments[row[0]] = row[1] or 0.0
    
    # Calculate cross-asset metrics
    values = list(sentiments.values())
    cross_mean = sum(values) / len(values) if values else 0.0
    cross_std = (sum((v - cross_mean) ** 2 for v in values) / len(values)) ** 0.5 if len(values) > 1 else 0.0
    max_divergence = max(values) - min(values) if values else 0.0
    
    # Get momentum from latest data
    result2 = await session.execute(text("""
        SELECT 
            period_start,
            AVG(mean_compound) as mean_sentiment
        FROM sentiment_indices
        WHERE source IS NULL
        GROUP BY period_start
        ORDER BY period_start DESC
        LIMIT 14
    """))
    historical = result2.fetchall()
    
    momentum = 0.0
    acceleration = 0.0
    if len(historical) >= 7:
        recent_avg = sum(h[1] or 0 for h in historical[:7]) / 7
        older_avg = sum(h[1] or 0 for h in historical[7:14]) / max(len(historical[7:14]), 1)
        momentum = recent_avg - older_avg
    
    # Get latest CISS value
    ciss_result = await session.execute(text("""
        SELECT value FROM stress_indices 
        WHERE source = 'ecb_ciss' 
        ORDER BY date DESC 
        LIMIT 1
    """))
    ciss_row = ciss_result.fetchone()
    ciss_level = float(ciss_row[0]) if ciss_row else None
    
    # Get latest VIX value
    vix_result = await session.execute(text("""
        SELECT close FROM market_data 
        WHERE symbol = '^VIX' 
        ORDER BY date DESC 
        LIMIT 1
    """))
    vix_row = vix_result.fetchone()
    vix_level = float(vix_row[0]) if vix_row else None
    
    return SentimentFeatures(
        equity_sentiment=sentiments.get('equity', 0.0),
        crypto_sentiment=sentiments.get('crypto', 0.0),
        forex_sentiment=sentiments.get('forex', 0.0),
        commodity_sentiment=sentiments.get('commodity', 0.0),
        cross_asset_mean=cross_mean,
        cross_asset_std=cross_std,
        sentiment_momentum=momentum,
        sentiment_acceleration=acceleration,
        max_divergence=max_divergence,
        vix_level=vix_level,
        ciss_level=ciss_level,
    )


@router.get("/current", response_model=RegimeResponse)
async def get_current_regime(
    session: AsyncSession = Depends(get_session),
) -> RegimeResponse:
    """
    Get the current market regime state.
    
    Returns:
        - Current regime (risk_on, risk_off, transition)
        - Confidence level
        - Probability distribution across states
        - Key features driving the classification
    """
    # Get real features from database
    features = await get_latest_features(session)
    
    # Try ML classifier first, fall back to rule-based
    try:
        classifier = MLRegimeClassifier()
        classification = classifier.classify(features)
    except Exception:
        classifier = RegimeClassifier()
        classification = classifier.classify(features)
    
    # Build features dict, filtering out None values
    features_dict = {
        "equity_sentiment": features.equity_sentiment,
        "crypto_sentiment": features.crypto_sentiment,
        "forex_sentiment": features.forex_sentiment,
        "commodity_sentiment": features.commodity_sentiment,
        "cross_asset_mean": features.cross_asset_mean,
        "sentiment_momentum_7d": features.sentiment_momentum,
        "max_divergence": features.max_divergence,
    }
    if features.ciss_level is not None:
        features_dict["ciss_level"] = features.ciss_level
    if features.vix_level is not None:
        features_dict["vix_level"] = features.vix_level

    return RegimeResponse(
        timestamp=datetime.now(timezone.utc),
        regime=classification.state.value,
        confidence=classification.confidence,
        probabilities={
            "risk_on": classification.prob_risk_on,
            "risk_off": classification.prob_risk_off,
            "transition": classification.prob_transition,
        },
        features=features_dict,
        model_version=classification.model_version,
    )


@router.get("/history", response_model=RegimeHistoryResponse)
async def get_regime_history(
    start_date: datetime = Query(..., description="Start date"),
    end_date: datetime = Query(default=None, description="End date (defaults to now)"),
) -> RegimeHistoryResponse:
    """
    Get historical regime states over a date range.
    
    Returns time-series of regime classifications with timestamps.
    """
    # TODO: Implement historical regime retrieval
    
    return RegimeHistoryResponse(
        start_date=start_date,
        end_date=end_date or datetime.now(timezone.utc),
        regimes=[],  # Will be populated from database
        transition_count=0,
    )


@router.get("/transitions")
async def get_regime_transitions(
    start_date: datetime = Query(default=None, description="Start date filter"),
    limit: int = Query(default=10, le=100, description="Max transitions to return"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Get list of regime transitions.

    Each transition includes:
        - From/to regime states
        - Transition timestamp
        - CISS and VIX levels at transition
    """
    # Calculate regime transitions from historical CISS data
    query = text("""
        WITH regime_data AS (
            SELECT
                si.date,
                si.value as ciss,
                md.close as vix,
                CASE
                    WHEN si.value < 0.2 AND md.close < 20 THEN 'risk_on'
                    WHEN si.value > 0.4 OR md.close > 30 THEN 'risk_off'
                    ELSE 'transition'
                END as regime
            FROM stress_indices si
            LEFT JOIN market_data md ON si.date = md.date AND md.symbol = '^VIX'
            WHERE si.source = 'ecb_ciss'
            ORDER BY si.date
        ),
        transitions AS (
            SELECT
                date,
                regime,
                LAG(regime) OVER (ORDER BY date) as prev_regime,
                ciss,
                vix
            FROM regime_data
        )
        SELECT
            date,
            prev_regime as from_regime,
            regime as to_regime,
            ciss,
            vix
        FROM transitions
        WHERE prev_regime IS NOT NULL
          AND prev_regime != regime
        ORDER BY date DESC
        LIMIT :limit
    """)

    result = await session.execute(query, {"limit": limit})
    rows = result.fetchall()

    transitions = []
    for row in rows:
        transitions.append({
            "date": str(row[0]),
            "from_regime": row[1],
            "to_regime": row[2],
            "ciss": float(row[3]) if row[3] else None,
            "vix": float(row[4]) if row[4] else None,
        })

    return {
        "count": len(transitions),
        "transitions": transitions,
    }


@router.get("/ciss/history")
async def get_ciss_history(
    days: int = Query(default=90, le=365, description="Number of days of history"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Get historical CISS values with VIX for charting.
    
    Returns daily CISS and VIX values for the specified period.
    """
    result = await session.execute(text("""
        SELECT si.date, si.value as ciss, md.close as vix
        FROM stress_indices si
        LEFT JOIN market_data md ON si.date = md.date AND md.symbol = '^VIX'
        WHERE si.source = 'ecb_ciss'
          AND si.date >= CURRENT_DATE - :days * INTERVAL '1 day'
        ORDER BY si.date
    """), {"days": days})
    rows = result.fetchall()
    
    return {
        "start_date": str(rows[0][0]) if rows else None,
        "end_date": str(rows[-1][0]) if rows else None,
        "count": len(rows),
        "data": [
            {
                "date": str(row[0]),
                "ciss": float(row[1]) if row[1] else None,
                "vix": float(row[2]) if row[2] else None,
            }
            for row in rows
        ],
    }


@router.get("/divergence")
async def get_cross_asset_divergence() -> dict:
    """
    Get cross-asset sentiment divergence analysis.
    
    Identifies when asset classes show conflicting sentiment signals,
    which often precedes regime transitions.
    """
    # TODO: Implement divergence calculation
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "divergence_score": 0.28,  # 0-1 scale
        "divergence_level": "moderate",  # low, moderate, high
        "pairs": [
            {
                "asset_1": "equity",
                "asset_2": "crypto",
                "correlation": 0.45,
                "sentiment_gap": 0.23,
            },
            {
                "asset_1": "equity",
                "asset_2": "commodity",
                "correlation": 0.72,
                "sentiment_gap": 0.07,
            },
        ],
        "alert": False,  # True if divergence exceeds threshold
    }
