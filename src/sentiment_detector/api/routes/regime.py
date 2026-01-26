"""Regime detection endpoints."""

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Query

from sentiment_detector.api.schemas.regime import (
    RegimeResponse,
    RegimeHistoryResponse,
    RegimeTransition,
)

router = APIRouter()

RegimeState = Literal["risk_on", "risk_off", "transition"]


@router.get("/current", response_model=RegimeResponse)
async def get_current_regime() -> RegimeResponse:
    """
    Get the current market regime state.
    
    Returns:
        - Current regime (risk_on, risk_off, transition)
        - Confidence level
        - Probability distribution across states
        - Key features driving the classification
    """
    # TODO: Implement real regime classification
    # For now, return mock data for API structure validation
    
    return RegimeResponse(
        timestamp=datetime.now(timezone.utc),
        regime="risk_on",
        confidence=0.72,
        probabilities={
            "risk_on": 0.72,
            "risk_off": 0.15,
            "transition": 0.13,
        },
        features={
            "cross_asset_sentiment_mean": 0.15,
            "sentiment_momentum_7d": 0.08,
            "sentiment_volatility": 0.12,
            "equity_crypto_correlation": 0.65,
        },
        model_version="rule-based-v1",  # Will change to trained model in Phase 2
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


@router.get("/transitions", response_model=list[RegimeTransition])
async def get_regime_transitions(
    start_date: datetime = Query(default=None, description="Start date filter"),
    limit: int = Query(default=10, le=100, description="Max transitions to return"),
) -> list[RegimeTransition]:
    """
    Get list of regime transitions.
    
    Each transition includes:
        - From/to regime states
        - Transition timestamp
        - Duration
        - Trigger features (what drove the change)
        - Validation status (confirmed by price action)
    """
    # TODO: Implement transition history retrieval
    
    return [
        RegimeTransition(
            id="trans_001",
            from_regime="risk_on",
            to_regime="transition",
            transition_start=datetime(2024, 1, 15, 14, 30, tzinfo=timezone.utc),
            transition_end=datetime(2024, 1, 16, 9, 0, tzinfo=timezone.utc),
            duration_hours=18.5,
            trigger_features={
                "crypto_sentiment_drop": -0.35,
                "equity_crypto_divergence": 0.42,
            },
            validated=True,
        ),
    ]


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
