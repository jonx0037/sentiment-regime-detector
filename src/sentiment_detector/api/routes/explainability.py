"""Explainability endpoints for SHAP-based model interpretation."""

from datetime import datetime, timezone
from typing import Optional
from io import BytesIO
import base64

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np
import matplotlib.pyplot as plt

from sentiment_detector.api.schemas.explainability import (
    ExplanationResponse,
    FeatureContribution,
    GlobalImportanceResponse,
    InteractionResponse,
    FeatureInteraction,
    EventExplanationResponse,
    CrisisEvent as APICrisisEvent,
)
from sentiment_detector.core.database import get_session
from sentiment_detector.explainability import (
    RegimeExplainer,
    ExplanationResult,
    get_event,
    list_events,
)
from sentiment_detector.explainability.viz import plot_waterfall

router = APIRouter()


def figure_to_base64(fig: plt.Figure) -> str:
    """Convert matplotlib figure to base64 PNG data URI.

    Args:
        fig: matplotlib Figure object

    Returns:
        Base64-encoded PNG data URI (data:image/png;base64,...)
    """
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)  # Clean up to prevent memory leaks
    return f"data:image/png;base64,{image_base64}"


async def build_feature_dict(
    session: AsyncSession,
    target_date: Optional[str] = None,
) -> dict[str, float]:
    """Build complete 28-feature dictionary from database.

    Args:
        session: Database session
        target_date: Specific date (YYYY-MM-DD) or None for latest

    Returns:
        Dictionary with all 28 features required by the model

    Raises:
        HTTPException: If insufficient data to compute features

    TODO: This is a simplified implementation. Full feature engineering should:
        1. Fetch 20+ days of historical data for moving averages
        2. Compute lags (ciss_lag1, etc.)
        3. Compute changes (ciss_change, ciss_change_5d, etc.)
        4. Compute moving averages (ciss_ma5, ciss_ma20, etc.)
        5. Compute binary indicators (ciss_above_ma20, vix_spike, etc.)
        6. Compute cross-asset metrics
    """
    # For MVP: Use latest values with simplified feature computation
    # In production, this would fetch historical data and compute all derived features

    # Get latest CISS
    ciss_query = text("""
        SELECT value, date
        FROM stress_indices
        WHERE source = 'ecb_ciss'
        ORDER BY date DESC
        LIMIT 20
    """)
    ciss_result = await session.execute(ciss_query)
    ciss_rows = ciss_result.fetchall()

    if not ciss_rows:
        raise HTTPException(status_code=404, detail="No CISS data available")

    # Get latest VIX
    vix_query = text("""
        SELECT close, date
        FROM market_data
        WHERE symbol = '^VIX'
        ORDER BY date DESC
        LIMIT 20
    """)
    vix_result = await session.execute(vix_query)
    vix_rows = vix_result.fetchall()

    if not vix_rows:
        raise HTTPException(status_code=404, detail="No VIX data available")

    # Get latest sentiment
    sentiment_query = text("""
        SELECT
            period_start,
            AVG(mean_compound) as mean_sentiment,
            STDDEV(mean_compound) as std_sentiment
        FROM sentiment_indices
        WHERE source IS NULL
        GROUP BY period_start
        ORDER BY period_start DESC
        LIMIT 20
    """)
    sentiment_result = await session.execute(sentiment_query)
    sentiment_rows = sentiment_result.fetchall()

    if not sentiment_rows:
        raise HTTPException(status_code=404, detail="No sentiment data available")

    # Extract latest values
    ciss_current = float(ciss_rows[0][0])
    ciss_values = [float(row[0]) for row in ciss_rows if row[0] is not None]

    vix_current = float(vix_rows[0][0])
    vix_values = [float(row[0]) for row in vix_rows if row[0] is not None]

    sentiment_current = float(sentiment_rows[0][1]) if sentiment_rows[0][1] else 0.0
    sentiment_values = [
        float(row[1]) for row in sentiment_rows if row[1] is not None
    ]

    # Compute derived features (simplified)
    ciss_ma5 = np.mean(ciss_values[:5]) if len(ciss_values) >= 5 else ciss_current
    ciss_ma20 = np.mean(ciss_values[:20]) if len(ciss_values) >= 20 else ciss_current
    ciss_std_20d = np.std(ciss_values[:20]) if len(ciss_values) >= 20 else 0.0

    vix_ma5 = np.mean(vix_values[:5]) if len(vix_values) >= 5 else vix_current
    vix_ma20 = np.mean(vix_values[:20]) if len(vix_values) >= 20 else vix_current
    vix_range = float(np.max(vix_values[:20]) - np.min(vix_values[:20])) if len(vix_values) >= 20 else 0.0

    sentiment_ma5 = np.mean(sentiment_values[:5]) if len(sentiment_values) >= 5 else sentiment_current
    sentiment_ma20 = np.mean(sentiment_values[:20]) if len(sentiment_values) >= 20 else sentiment_current
    sentiment_std = np.std(sentiment_values[:20]) if len(sentiment_values) >= 20 else 0.0

    # Build complete feature dictionary
    features = {
        # CISS features
        'ciss_lag1': float(ciss_values[1]) if len(ciss_values) > 1 else ciss_current,
        'ciss_change': ciss_current - float(ciss_values[1]) if len(ciss_values) > 1 else 0.0,
        'ciss_change_5d': ciss_current - float(ciss_values[5]) if len(ciss_values) > 5 else 0.0,
        'ciss_ma5': float(ciss_ma5),
        'ciss_ma20': float(ciss_ma20),
        'ciss_above_ma20': float(1 if ciss_current > ciss_ma20 else 0),
        'ciss_std_20d': float(ciss_std_20d),
        'ciss_trend': float(1 if ciss_current > float(ciss_values[5]) else -1) if len(ciss_values) > 5 else 0,

        # VIX features
        'vix': vix_current,
        'vix_change': vix_current - float(vix_values[1]) if len(vix_values) > 1 else 0.0,
        'vix_change_pct': (
            (vix_current - float(vix_values[1])) / float(vix_values[1]) * 100
            if len(vix_values) > 1 and vix_values[1] != 0
            else 0.0
        ),
        'vix_ma5': float(vix_ma5),
        'vix_ma20': float(vix_ma20),
        'vix_above_ma20': float(1 if vix_current > vix_ma20 else 0),
        'vix_spike': float(1 if vix_current > vix_ma20 * 1.2 else 0),
        'vix_range': vix_range,

        # Sentiment features
        'sentiment': sentiment_current,
        'sentiment_change': (
            sentiment_current - float(sentiment_values[1])
            if len(sentiment_values) > 1
            else 0.0
        ),
        'sentiment_momentum_5d': float(np.mean(sentiment_values[:5]) - np.mean(sentiment_values[5:10])) if len(sentiment_values) >= 10 else 0.0,
        'sentiment_momentum_20d': float(sentiment_ma5 - sentiment_ma20),
        'sentiment_ma5': float(sentiment_ma5),
        'sentiment_ma20': float(sentiment_ma20),
        'sentiment_acceleration': 0.0,  # TODO: Compute second derivative
        'sentiment_dispersion': float(sentiment_std),
        'sentiment_spread': float(sentiment_current - sentiment_ma20),

        # Cross-asset interaction features
        'cross_asset_divergence': float(sentiment_std),  # Proxy using sentiment dispersion
        'ciss_vix_ratio': ciss_current / vix_current if vix_current != 0 else 0.0,
        'sentiment_vix_interaction': sentiment_current * vix_current / 100.0,  # Scaled interaction
    }

    return features


def explanation_result_to_response(result: ExplanationResult) -> ExplanationResponse:
    """Convert ExplanationResult to API response format.

    Args:
        result: ExplanationResult from explainer

    Returns:
        ExplanationResponse for API
    """
    # Sort features by absolute SHAP value
    feature_shap_pairs = [
        (name, result.feature_values[name], float(shap_val), idx)
        for idx, (name, shap_val) in enumerate(
            zip(result.feature_names, result.shap_values)
        )
    ]
    feature_shap_pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    # Build feature contributions
    all_features = [
        FeatureContribution(
            feature_name=name,
            value=value,
            shap_value=shap_val,
            rank=rank + 1,
        )
        for rank, (name, value, shap_val, _) in enumerate(feature_shap_pairs)
    ]

    # Generate waterfall plot
    waterfall_plot_data_uri = None
    try:
        # Create waterfall plot (will be closed by plot_waterfall)
        # We need to capture it before it's closed, so we use output_path
        # to trigger saving, then read and encode
        import tempfile
        from pathlib import Path
        import logging

        logger = logging.getLogger(__name__)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            tmp_path = Path(tmp_file.name)

        logger.info(f"Creating waterfall plot at {tmp_path}")

        try:
            plot_waterfall(result, output_path=tmp_path, show=False, max_features=10)
            logger.info(f"Plot saved, file exists: {tmp_path.exists()}")

            if tmp_path.exists():
                # Read the saved file and convert to base64
                with open(tmp_path, 'rb') as f:
                    image_data = f.read()
                logger.info(f"Read {len(image_data)} bytes from plot file")

                image_base64 = base64.b64encode(image_data).decode('utf-8')
                waterfall_plot_data_uri = f"data:image/png;base64,{image_base64}"
                logger.info(f"Successfully generated waterfall plot data URI ({len(waterfall_plot_data_uri)} chars)")
            else:
                logger.warning(f"Plot file not found after generation: {tmp_path}")
        finally:
            # Clean up temp file
            if tmp_path.exists():
                tmp_path.unlink()
                logger.debug(f"Cleaned up temp file: {tmp_path}")
    except Exception as e:
        # Log error but don't fail the request if plot generation fails
        import logging
        logging.getLogger(__name__).error(f"Failed to generate waterfall plot: {e}", exc_info=True)

    return ExplanationResponse(
        timestamp=result.timestamp,
        predicted_regime=result.predicted_regime,
        confidence=result.confidence,
        base_value=result.base_value,
        prediction_value=result.prediction,
        waterfall_plot=waterfall_plot_data_uri,
        top_features=all_features[:10],
        all_features=all_features,
        model_version=result.model_version,
        cache_hit=False,  # TODO: Track cache hits
    )


@router.get("/current", response_model=ExplanationResponse)
async def explain_current_prediction(
    session: AsyncSession = Depends(get_session),
) -> ExplanationResponse:
    """
    Explain the current regime prediction using SHAP values.

    Returns:
        - SHAP explanation showing which features drove the prediction
        - Top contributing features ranked by importance
        - Feature values and their contributions
        - Model version and confidence
    """
    # Build features from latest data
    features = await build_feature_dict(session)

    # Get explanation (cache-enabled)
    explainer = RegimeExplainer(model_path="models/regime_classifier_rf.pkl")
    result = explainer.explain_prediction(features)

    return explanation_result_to_response(result)


@router.get("/date/{date}", response_model=ExplanationResponse)
async def explain_prediction_for_date(
    date: str,
    session: AsyncSession = Depends(get_session),
) -> ExplanationResponse:
    """
    Explain regime prediction for a specific historical date.

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        SHAP explanation for that date's prediction

    TODO: Implement date-specific feature fetching
    Currently returns latest features (not date-specific)
    """
    # TODO: Fetch historical data for specific date
    # For now, use latest features (MVP)
    features = await build_feature_dict(session, target_date=date)

    explainer = RegimeExplainer(model_path="models/regime_classifier_rf.pkl")
    result = explainer.explain_prediction(features)

    return explanation_result_to_response(result)


@router.get("/events/{event_id}", response_model=EventExplanationResponse)
async def explain_crisis_event(
    event_id: str,
    session: AsyncSession = Depends(get_session),
) -> EventExplanationResponse:
    """
    Explain model prediction for a historical crisis event.

    Args:
        event_id: Crisis event identifier (e.g., 'financial_crisis_2008')

    Returns:
        Event metadata plus SHAP explanation

    Available events:
        - financial_crisis_2008: 2008 Financial Crisis (Nov 20, 2008)
        - covid_crash_2020: COVID-19 Market Crash (Mar 16, 2020)
        - gamestop_2021: GameStop/Meme Stock Episode (Jan 28, 2021)
        - luna_collapse_2022: Luna/Terra Collapse (May 9, 2022)
        - celsius_3ac_2022: Celsius/3AC Contagion (Jun 15, 2022)
        - out_of_sample_2024: Out-of-Sample Validation (Oct 1, 2024)
    """
    # Get event metadata
    event = get_event(event_id)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail=f"Event '{event_id}' not found. Use /events to list available events."
        )

    # Get explanation for event date
    features = await build_feature_dict(session, target_date=event.date)

    explainer = RegimeExplainer(model_path="models/regime_classifier_rf.pkl")
    result = explainer.explain_prediction(features)

    # Convert event to API schema
    api_event = APICrisisEvent(
        event_id=event.event_id,
        name=event.name,
        date=event.date,
        description=event.description,
        ciss_peak=event.ciss_peak,
        vix_peak=event.vix_peak,
    )

    return EventExplanationResponse(
        event=api_event,
        explanation=explanation_result_to_response(result),
    )


@router.get("/events", response_model=list[APICrisisEvent])
async def list_crisis_events() -> list[APICrisisEvent]:
    """
    List all available crisis events for analysis.

    Returns:
        List of crisis events with metadata
    """
    events = list_events()
    return [
        APICrisisEvent(
            event_id=event.event_id,
            name=event.name,
            date=event.date,
            description=event.description,
            ciss_peak=event.ciss_peak,
            vix_peak=event.vix_peak,
        )
        for event in events
    ]


@router.get("/global-importance", response_model=GlobalImportanceResponse)
async def get_global_feature_importance(
    days: int = Query(default=90, ge=7, le=365, description="Days of data to analyze"),
    session: AsyncSession = Depends(get_session),
) -> GlobalImportanceResponse:
    """
    Compute global feature importance across recent predictions.

    Analyzes mean |SHAP| values across multiple time periods to identify
    which features consistently drive predictions.

    Args:
        days: Number of days of historical data to analyze (7-365)

    Returns:
        - Mean absolute SHAP values for each feature
        - Top 10 most important features
        - Sample size used for computation

    Note: This is computationally expensive (computes SHAP for all samples)
    and should be cached or computed offline for production use.
    """
    # TODO: Implement batch feature fetching for date range
    # For MVP, return error with clear message
    raise HTTPException(
        status_code=501,
        detail=(
            "Global importance requires batch processing of historical data. "
            "This endpoint will be implemented in Day 7-9 (Visualization phase) "
            "as it requires the same feature engineering pipeline as plot generation."
        )
    )
