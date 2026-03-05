"""Main API router configuration."""

from fastapi import APIRouter

from sentiment_detector.api.routes.health import router as health_router
from sentiment_detector.api.routes.sentiment import router as sentiment_router
from sentiment_detector.api.routes.regime import router as regime_router
from sentiment_detector.api.routes.alerts import router as alerts_router
from sentiment_detector.api.routes.garch import router as garch_router
from sentiment_detector.api.routes.explainability import router as explainability_router
from sentiment_detector.api.routes.cron import router as cron_router
from sentiment_detector.api.routes.chatbot import router as chatbot_router

# Main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(sentiment_router, prefix="/sentiment", tags=["Sentiment"])
api_router.include_router(regime_router, prefix="/regime", tags=["Regime"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
api_router.include_router(garch_router, prefix="/garch", tags=["GARCH"])
api_router.include_router(explainability_router, prefix="/explainability", tags=["Explainability"])
api_router.include_router(cron_router, prefix="/cron", tags=["Cron"])
api_router.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
