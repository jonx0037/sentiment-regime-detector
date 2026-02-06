# src/sentiment_detector/explainability/cache.py
"""Two-tier caching for SHAP explanations: Redis (L1) + PostgreSQL (L2)."""

import json
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
import logging

import redis.asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class ExplainabilityCache:
    """Two-tier cache: Redis (L1, hot) + PostgreSQL (L2, cold storage).

    Design principles:
    - Redis: Fast retrieval (<50ms), 24h TTL
    - PostgreSQL: Permanent storage, complex queries, analytics
    - JSON serialization only (no pickle for security)
    - Automatic promotion from L2 to L1 on cache hits

    Performance targets:
    - Cache hit (Redis): <50ms
    - Cache miss (SHAP computation): <500ms
    - Cache hit rate: >80%
    """

    def __init__(self, redis_url: str, db_session: AsyncSession):
        """Initialize cache with Redis and database connections.

        Args:
            redis_url: Redis connection URL (e.g., redis://localhost:6379/0)
            db_session: SQLAlchemy async database session
        """
        self.redis_url = redis_url
        self.db_session = db_session
        self._redis = None

    async def _get_redis(self) -> aioredis.Redis:
        """Lazy Redis connection with connection pooling."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self.redis_url,
                decode_responses=True,
                encoding='utf-8'
            )
        return self._redis

    async def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get explanation from cache (L1 -> L2 fallback).

        Args:
            cache_key: Cache key (SHA256 hash of model version + features)

        Returns:
            Cached explanation dict or None if not found
        """
        # Try Redis first (L1 - hot cache)
        try:
            redis = await self._get_redis()
            value = await redis.get(cache_key)

            if value:
                logger.debug(f"Cache hit (Redis L1): {cache_key}")
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Redis L1 error: {e}, falling back to PostgreSQL")

        # Try PostgreSQL (L2 - cold storage)
        try:
            result = await self.db_session.execute(
                text("SELECT explanation_data FROM explainability_cache WHERE cache_key = :key"),
                {"key": cache_key}
            )
            row = result.fetchone()

            if row:
                logger.debug(f"Cache hit (PostgreSQL L2): {cache_key}")
                # Parse JSONB data
                value = row[0] if isinstance(row[0], dict) else json.loads(row[0])

                # Promote to Redis (L1)
                try:
                    redis = await self._get_redis()
                    await redis.setex(cache_key, 86400, json.dumps(value))
                    logger.debug(f"Promoted to Redis L1: {cache_key}")
                except Exception as e:
                    logger.warning(f"Redis promotion failed: {e}")

                return value
        except Exception as e:
            logger.error(f"PostgreSQL L2 error: {e}")

        logger.debug(f"Cache miss: {cache_key}")
        return None

    async def set(self, cache_key: str, value: Dict[str, Any]) -> None:
        """Set explanation in both cache tiers.

        Args:
            cache_key: Cache key (SHA256 hash)
            value: Explanation dict (JSON-serializable)
        """
        json_value = json.dumps(value)

        # Set in Redis (L1) with 24h TTL
        try:
            redis = await self._get_redis()
            await redis.setex(cache_key, 86400, json_value)
            logger.debug(f"Cached in Redis L1: {cache_key}")
        except Exception as e:
            logger.warning(f"Redis L1 set error: {e}")

        # Set in PostgreSQL (L2) permanently
        try:
            await self.db_session.execute(
                text("""
                    INSERT INTO explainability_cache (cache_key, explanation_data, model_version)
                    VALUES (:key, :data::jsonb, :version)
                    ON CONFLICT (cache_key) DO UPDATE
                    SET explanation_data = EXCLUDED.explanation_data,
                        computed_at = NOW()
                """),
                {
                    "key": cache_key,
                    "data": json_value,
                    "version": value.get("model_version", "unknown")
                }
            )
            await self.db_session.commit()
            logger.info(f"Cached in PostgreSQL L2: {cache_key}")
        except Exception as e:
            logger.error(f"PostgreSQL L2 set error: {e}")
            await self.db_session.rollback()

    @staticmethod
    def make_cache_key(model_version: str, features: Dict[str, float]) -> str:
        """Generate deterministic cache key from model version and features.

        Args:
            model_version: Model version string
            features: Feature dictionary (will be sorted for consistency)

        Returns:
            Cache key: "explain:{model_version}:{hash16}"
        """
        # Sort features for deterministic hashing
        features_str = json.dumps(features, sort_keys=True)
        hash_str = hashlib.sha256(features_str.encode()).hexdigest()[:16]
        return f"explain:{model_version}:{hash_str}"

    async def close(self) -> None:
        """Close Redis connection (PostgreSQL session managed externally)."""
        if self._redis is not None:
            await self._redis.close()
            self._redis = None
