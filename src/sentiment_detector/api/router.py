"""Main API router configuration."""

from fastapi import APIRouter

from sentiment_detector.api.routes.health import router as health_router
from sentiment_detector.api.routes.sentiment import router as sentiment_router
from sentiment_detector.api.routes.regime import router as regime_router
from sentiment_detector.api.routes.alerts import router as alerts_router

# Main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])
api_router.include_router(regime_router, prefix="/regime", tags=["Regime"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
