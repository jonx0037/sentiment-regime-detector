"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentiment_detector.core.config import settings
from sentiment_detector.core.database import init_db, close_db
from sentiment_detector.core.logging import setup_logging, get_logger
from sentiment_detector.api.router import api_router

# Initialize logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager for startup/shutdown events."""
    # Startup
    logger.info(
        "Starting Sentiment Regime Detector",
        environment=settings.environment,
        model=settings.model_name,
    )
    
    # Initialize database (create tables if needed)
    # Note: In production, use Alembic migrations instead
    if settings.is_development:
        try:
            await init_db()
            logger.info("Database initialized")
        except Exception as e:
            logger.warning(
                "Database connection failed - running without database",
                error=str(e),
            )
    
    yield
    
    # Shutdown
    logger.info("Shutting down Sentiment Regime Detector")
    try:
        await close_db()
    except Exception:
        pass  # Ignore close errors if DB wasn't connected


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Sentiment Regime Detector",
        description=(
            "Cross-Asset Sentiment Regime Detector: "
            "Automating Market Psychology Analysis Through Multi-Source NLP"
        ),
        version="0.1.0",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    return app


# Create app instance
app = create_app()


def run() -> None:
    """Run the application using uvicorn."""
    uvicorn.run(
        "sentiment_detector.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )


if __name__ == "__main__":
    run()
