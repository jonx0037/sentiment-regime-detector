"""
Sentiment analysis service layer.

Orchestrates sentiment analysis workflow:
1. Fetch raw texts from database
2. Analyze using SentimentEngine
3. Persist scores to database
4. Aggregate by asset class
"""

import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.models.sentiment import SentimentScore
from sentiment_detector.models.text_record import RawText
from sentiment_detector.services.sentiment_engine import (
    SentimentEngine,
    SentimentScore as EngineSentimentScore,
)

logger = logging.getLogger(__name__)


class SentimentService:
    """
    Service for analyzing texts and managing sentiment data.

    Responsibilities:
    - Analyze raw texts using SentimentEngine
    - Persist sentiment scores to database
    - Compute aggregated sentiment indices
    - Query historical sentiment data
    """

    def __init__(self, engine: Optional[SentimentEngine] = None):
        """
        Initialize sentiment service.

        Args:
            engine: SentimentEngine instance. Creates default if None.
        """
        self.engine = engine or SentimentEngine(model_type="distilbert")
        self._engine_loaded = False

    async def analyze_pending_texts(
        self,
        session: AsyncSession,
        limit: Optional[int] = None,
        asset_class: Optional[str] = None,
    ) -> int:
        """
        Analyze raw texts that haven't been processed yet.

        Args:
            session: Database session
            limit: Maximum number of texts to process
            asset_class: Filter by asset class (optional)

        Returns:
            Number of texts analyzed
        """
        # Load engine if needed
        if not self._engine_loaded:
            logger.info("Loading sentiment engine...")
            self.engine.load()
            self._engine_loaded = True

        # Find texts without sentiment scores
        query = (
            select(RawText)
            .outerjoin(SentimentScore, RawText.id == SentimentScore.text_id)
            .where(SentimentScore.id.is_(None))  # Texts with no scores
            .order_by(RawText.content_created_at.desc())
        )

        if asset_class:
            query = query.where(RawText.asset_class == asset_class)

        if limit:
            query = query.limit(limit)

        result = await session.execute(query)
        pending_texts = result.scalars().all()

        if not pending_texts:
            logger.info("No pending texts to analyze")
            return 0

        logger.info(f"Analyzing {len(pending_texts)} texts...")

        # Batch process texts
        texts_to_analyze = [text.content for text in pending_texts]
        sentiment_results = self.engine.analyze_batch(texts_to_analyze)

        # Persist scores to database
        scores_created = 0
        for raw_text, sentiment_result in zip(pending_texts, sentiment_results):
            score = self._create_sentiment_score(raw_text.id, sentiment_result)
            session.add(score)
            scores_created += 1

            logger.debug(
                f"Analyzed {raw_text.asset_class} text: "
                f"compound={sentiment_result.compound:.3f}, "
                f"label={sentiment_result.label}"
            )

        await session.commit()
        logger.info(f"✓ Created {scores_created} sentiment scores")

        # Update indices for affected asset classes
        asset_classes = set(text.asset_class for text in pending_texts)
        for ac in asset_classes:
            await self._update_sentiment_index(session, ac)

        return scores_created

    async def analyze_text(
        self,
        session: AsyncSession,
        text_id: UUID,
        force: bool = False,
    ) -> SentimentScore:
        """
        Analyze a specific text by ID.

        Args:
            session: Database session
            text_id: ID of raw text to analyze
            force: Re-analyze even if score exists

        Returns:
            Created or existing SentimentScore
        """
        # Load engine if needed
        if not self._engine_loaded:
            self.engine.load()
            self._engine_loaded = True

        # Fetch raw text
        result = await session.execute(select(RawText).where(RawText.id == text_id))
        raw_text = result.scalar_one_or_none()

        if not raw_text:
            raise ValueError(f"Text with id {text_id} not found")

        # Check if already analyzed
        if not force:
            result = await session.execute(
                select(SentimentScore)
                .where(SentimentScore.text_id == text_id)
                .where(SentimentScore.model_name == self.engine.model_type)
            )
            existing_score = result.scalar_one_or_none()
            if existing_score:
                logger.debug(f"Using existing score for text {text_id}")
                return existing_score

        # Analyze text
        sentiment_result = self.engine.analyze(raw_text.content)

        # Create score record
        score = self._create_sentiment_score(text_id, sentiment_result)
        session.add(score)
        await session.commit()
        await session.refresh(score)

        logger.info(f"Created sentiment score for text {text_id}: {sentiment_result.label}")

        # Update index for this asset class
        await self._update_sentiment_index(session, raw_text.asset_class)

        return score

    async def get_current_sentiment(
        self,
        session: AsyncSession,
        asset_class: Optional[str] = None,
    ) -> list[dict]:
        """
        Get current aggregated sentiment for asset class(es).

        Uses the most recent 7 days of pre-computed sentiment indices
        for responsive, meaningful current-state reporting. Falls back
        to raw scores if indices are unavailable.

        Args:
            session: Database session
            asset_class: Specific asset class or None for all

        Returns:
            List of sentiment aggregates with statistics
        """
        from sqlalchemy import text as sql_text

        if asset_class:
            asset_classes = [asset_class]
        else:
            # Dynamically discover asset classes from the database
            ac_result = await session.execute(
                sql_text(
                    "SELECT DISTINCT asset_class FROM sentiment_indices "
                    "WHERE source IS NULL ORDER BY asset_class"
                )
            )
            asset_classes = [row[0] for row in ac_result.fetchall()]
            if not asset_classes:
                # Fallback if table is empty
                asset_classes = ["commodity", "crypto", "equity", "forex"]
        results = []

        for ac in asset_classes:
            # Try sentiment_indices first (pre-computed daily aggregates)
            idx_result = await session.execute(
                sql_text("""
                WITH recent AS (
                    SELECT
                        mean_compound,
                        positive_ratio,
                        negative_ratio,
                        sample_count,
                        period_start,
                        1.0 - COALESCE(positive_ratio, 0) - COALESCE(negative_ratio, 0) AS neutral_ratio
                    FROM (
                        SELECT mean_compound, positive_ratio, negative_ratio,
                               sample_count, period_start
                        FROM sentiment_indices
                        WHERE asset_class = :ac
                          AND source IS NULL
                        ORDER BY period_start DESC
                        LIMIT 7
                    ) sub_recent
                ),
                prior AS (
                    SELECT AVG(mean_compound) as prior_avg
                    FROM (
                        SELECT mean_compound
                        FROM sentiment_indices
                        WHERE asset_class = :ac
                          AND source IS NULL
                        ORDER BY period_start DESC
                        LIMIT 7 OFFSET 7
                    ) sub_prior
                )
                SELECT
                    AVG(r.mean_compound) as avg_compound,
                    AVG(r.positive_ratio) as avg_positive,
                    AVG(r.negative_ratio) as avg_negative,
                    AVG(r.neutral_ratio) as avg_neutral,
                    SUM(r.sample_count) as total_count,
                    (SELECT prior_avg FROM prior) as prior_avg
                FROM recent r
            """),
                {"ac": ac},
            )

            stats = idx_result.one()

            if stats.total_count and stats.total_count > 0:
                avg_compound = float(stats.avg_compound or 0.0)
                prior_avg = float(stats.prior_avg) if stats.prior_avg else avg_compound
                momentum = round(avg_compound - prior_avg, 4) if prior_avg else 0.0

                results.append(
                    {
                        "asset_class": ac,
                        "compound_score": float(stats.avg_compound or 0.0),
                        "positive_ratio": float(stats.avg_positive or 0.0),
                        "negative_ratio": float(stats.avg_negative or 0.0),
                        "neutral_ratio": float(stats.avg_neutral or 0.0),
                        "sample_count": int(stats.total_count),
                        "momentum": momentum,
                        "timestamp": datetime.now(timezone.utc),
                    }
                )
                continue

            # Fallback: aggregate from raw sentiment_scores (last 7 days only)
            query = (
                select(
                    func.avg(SentimentScore.compound).label("avg_compound"),
                    func.avg(SentimentScore.positive).label("avg_positive"),
                    func.avg(SentimentScore.negative).label("avg_negative"),
                    func.avg(SentimentScore.neutral).label("avg_neutral"),
                    func.count(SentimentScore.id).label("count"),
                )
                .join(RawText, SentimentScore.text_id == RawText.id)
                .where(RawText.asset_class == ac)
                .where(SentimentScore.processed_at >= func.now() - sql_text("INTERVAL '7 days'"))
            )
            result = await session.execute(query)
            raw_stats = result.one()

            if raw_stats.count == 0:
                continue

            results.append(
                {
                    "asset_class": ac,
                    "compound_score": float(raw_stats.avg_compound or 0.0),
                    "positive_ratio": float(raw_stats.avg_positive or 0.0),
                    "negative_ratio": float(raw_stats.avg_negative or 0.0),
                    "neutral_ratio": float(raw_stats.avg_neutral or 0.0),
                    "sample_count": int(raw_stats.count),
                    "momentum": 0.0,
                    "timestamp": datetime.now(timezone.utc),
                }
            )

        return results

    async def get_sentiment_history(
        self,
        session: AsyncSession,
        asset_class: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
    ) -> list[dict]:
        """
        Get historical sentiment scores for an asset class.

        Args:
            session: Database session
            asset_class: Asset class to query
            start_date: Start of date range
            end_date: End of date range (defaults to now)

        Returns:
            List of sentiment score data points
        """
        if end_date is None:
            end_date = datetime.now(timezone.utc)

        # Query sentiment scores joined with raw texts
        query = (
            select(SentimentScore)
            .join(RawText, SentimentScore.text_id == RawText.id)
            .where(RawText.asset_class == asset_class)
            .where(SentimentScore.processed_at >= start_date)
            .where(SentimentScore.processed_at <= end_date)
            .order_by(SentimentScore.processed_at.asc())
        )

        result = await session.execute(query)
        scores = result.scalars().all()

        return [
            {
                "timestamp": score.processed_at,
                "compound_score": score.compound,
                "confidence": score.confidence,
            }
            for score in scores
        ]

    def _create_sentiment_score(
        self,
        text_id: UUID,
        sentiment: EngineSentimentScore,
    ) -> SentimentScore:
        """Create SentimentScore database model from engine result."""
        return SentimentScore(
            text_id=text_id,
            model_name=sentiment.model_name,
            model_version="v1.0",  # TODO: Track actual model versions
            positive=sentiment.positive,
            negative=sentiment.negative,
            neutral=sentiment.neutral,
            compound=sentiment.compound,
            confidence=sentiment.confidence,
            processed_at=datetime.now(timezone.utc),
        )

    async def _update_sentiment_index(
        self,
        session: AsyncSession,
        asset_class: str,
    ) -> None:
        """
        Log aggregated sentiment stats for asset class.

        For Phase 1, we compute aggregates on-the-fly in get_current_sentiment.
        This method just logs the update for now.

        Args:
            session: Database session
            asset_class: Asset class that was updated
        """
        # For now, just log that we updated this asset class
        # In Phase 2, we'll implement periodic index computation
        logger.debug(f"Sentiment scores updated for {asset_class}")
