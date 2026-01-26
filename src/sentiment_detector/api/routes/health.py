"""Health check endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter

from sentiment_detector.api.schemas.common import HealthResponse
from sentiment_detector.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns the current status of the API and its dependencies.
    """
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        version="0.1.0",
        timestamp=datetime.now(timezone.utc),
        model_name=settings.model_name,
    )


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": "Sentiment Regime Detector API",
        "version": "0.1.0",
        "docs": "/docs",
    }
