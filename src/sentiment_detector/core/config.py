"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/sentiment_db",
        description="PostgreSQL connection URL",
    )
    database_echo: bool = Field(default=False, description="Echo SQL queries")

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    redis_url: RedisDsn | None = Field(
        default=None,
        description="Redis connection URL (optional, app uses in-memory cache)",
    )

    @field_validator("redis_url", mode="before")
    @classmethod
    def empty_redis_url_to_none(cls, v):
        """Convert empty REDIS_URL to None so Pydantic doesn't try to parse it."""
        if v is None or v == "":
            return None
        return v

    # -------------------------------------------------------------------------
    # API Keys
    # -------------------------------------------------------------------------
    reddit_client_id: str = Field(default="", description="Reddit API client ID")
    reddit_client_secret: str = Field(default="", description="Reddit API client secret")
    reddit_user_agent: str = Field(
        default="sentiment-regime-detector:v0.1.0",
        description="Reddit API user agent",
    )

    twitter_bearer_token: str = Field(default="", description="Twitter API bearer token")
    news_api_key: str = Field(default="", description="NewsAPI key")
    finhub_api_key: str = Field(default="", description="Finnhub API key")
    tiingo_api_key: str = Field(default="", description="Tiingo API key")
    coinapi_key_1: str = Field(default="", description="CoinAPI key 1")
    coinapi_key_2: str = Field(default="", description="CoinAPI key 2")
    coinapi_key_3: str = Field(default="", description="CoinAPI key 3")
    alpha_vantage_api_key: str = Field(default="", description="Alpha Vantage API key")

    # -------------------------------------------------------------------------
    # Model Configuration
    # -------------------------------------------------------------------------
    model_name: str = Field(
        default="distilbert-base-uncased-finetuned-sst-2-english",
        description="Hugging Face model name for sentiment analysis",
    )
    model_device: Literal["cpu", "cuda", "mps"] = Field(
        default="cpu",
        description="Device for model inference",
    )
    model_batch_size: int = Field(default=32, description="Batch size for inference")

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Application environment",
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="DEBUG",
        description="Logging level",
    )
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(
        default=8000,
        description="API port (also accepts PORT environment variable from Railway)",
        alias="PORT",  # Railway uses PORT instead of API_PORT
    )
    api_reload: bool = Field(default=True, description="Enable auto-reload in development")
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Allowed CORS origins (comma-separated)",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # -------------------------------------------------------------------------
    # Data Collection
    # -------------------------------------------------------------------------
    reddit_subreddits: str = Field(
        default="wallstreetbets,investing,stocks,cryptocurrency,forex",
        description="Subreddits to monitor (comma-separated)",
    )
    news_sources: str = Field(
        default="bloomberg,reuters,financial-times",
        description="News sources to collect from (comma-separated)",
    )

    @property
    def reddit_subreddits_list(self) -> list[str]:
        """Parse subreddits from comma-separated string."""
        return [s.strip() for s in self.reddit_subreddits.split(",") if s.strip()]

    @property
    def news_sources_list(self) -> list[str]:
        """Parse news sources from comma-separated string."""
        return [s.strip() for s in self.news_sources.split(",") if s.strip()]

    collection_interval_minutes: int = Field(
        default=60,
        description="Interval between data collection runs",
    )

    # -------------------------------------------------------------------------
    # Observability
    # -------------------------------------------------------------------------
    sentry_dsn: str = Field(default="", description="Sentry DSN for error tracking")
    wandb_api_key: str = Field(default="", description="Weights & Biases API key")
    wandb_project: str = Field(default="sentiment-regime-detector", description="W&B project name")

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
