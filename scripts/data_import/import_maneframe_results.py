#!/usr/bin/env python3
"""
Import MANEFRAME processed sentiment results back to PostgreSQL.

This script:
1. Reads processed JSON files from MANEFRAME output
2. Imports raw texts and sentiment scores to PostgreSQL
3. Updates sentiment indices

Usage:
    python import_maneframe_results.py --input-dir data/processed/sentiment_results/
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.core.config import get_settings
from sentiment_detector.models.sentiment import SentimentScore
from sentiment_detector.models.text_record import RawText
from sentiment_detector.collectors.base import AssetClass, DataSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def parse_asset_class(value: str) -> AssetClass:
    """Parse asset class from string."""
    mapping = {
        "equity": AssetClass.EQUITY,
        "crypto": AssetClass.CRYPTO,
        "forex": AssetClass.FOREX,
        "commodity": AssetClass.COMMODITY,
    }
    return mapping.get(value.lower(), AssetClass.EQUITY)


def parse_source(value: str) -> DataSource:
    """Parse data source from string."""
    mapping = {
        "kaggle": DataSource.KAGGLE,
        "twitter": DataSource.TWITTER,
        "rss": DataSource.RSS,
        "reddit": DataSource.REDDIT,
    }
    return mapping.get(value.lower(), DataSource.KAGGLE)


async def import_results(
    session: AsyncSession,
    items: list[dict],
    batch_name: str,
) -> tuple[int, int]:
    """
    Import processed items to database.
    
    Returns:
        Tuple of (texts_created, scores_created)
    """
    texts_created = 0
    scores_created = 0
    
    for item in items:
        try:
            # Create or find raw text
            source_id = item.get("source_id", str(uuid4()))
            
            # Check if already exists
            existing = await session.execute(
                select(RawText).where(RawText.source_id == source_id)
            )
            raw_text = existing.scalar_one_or_none()
            
            if not raw_text:
                # Parse dates
                created_at = None
                if item.get("created_at"):
                    try:
                        created_at = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        created_at = datetime.now(timezone.utc)
                
                raw_text = RawText(
                    id=uuid4(),
                    source=parse_source(item.get("source", "kaggle")).value,
                    source_id=source_id,
                    asset_class=parse_asset_class(item.get("asset_class", "equity")).value,
                    content=item.get("content", "")[:10000],
                    title=item.get("title", "")[:500] if item.get("title") else None,
                    content_created_at=created_at,
                    collected_at=datetime.now(timezone.utc),
                    metadata_=item.get("metadata", {}),
                )
                session.add(raw_text)
                texts_created += 1
            
            # Check if sentiment score already exists
            existing_score = await session.execute(
                select(SentimentScore).where(SentimentScore.text_id == raw_text.id)
            )
            if existing_score.scalar_one_or_none():
                continue
            
            # Create sentiment score
            sentiment = item.get("sentiment", {})
            if sentiment:
                # Parse processed_at if available
                processed_at = None
                if item.get("processed_at"):
                    try:
                        processed_at = datetime.fromisoformat(item["processed_at"].replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        processed_at = datetime.now(timezone.utc)
                else:
                    processed_at = datetime.now(timezone.utc)
                
                score = SentimentScore(
                    id=uuid4(),
                    text_id=raw_text.id,
                    model_name=item.get("model", "ProsusAI/finbert"),
                    model_version="1.0",
                    compound=sentiment.get("compound", 0.0),
                    positive=sentiment.get("positive", 0.0),
                    negative=sentiment.get("negative", 0.0),
                    neutral=sentiment.get("neutral", 0.0),
                    confidence=max(
                        sentiment.get("positive", 0.0),
                        sentiment.get("negative", 0.0),
                        sentiment.get("neutral", 0.0),
                    ),
                    processed_at=processed_at,
                )
                session.add(score)
                scores_created += 1
                
        except Exception as e:
            logger.warning(f"Error importing item {item.get('source_id')}: {e}")
            continue
    
    await session.commit()
    return texts_created, scores_created


async def main_async(input_dir: Path, limit: int = None):
    """Main async function."""
    settings = get_settings()
    
    engine = create_async_engine(
        str(settings.database_url),
        echo=False,
        pool_pre_ping=True,
    )
    
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Find all JSON files
    json_files = sorted(input_dir.glob("*_sentiment.json"))
    if not json_files:
        logger.error(f"No sentiment JSON files found in {input_dir}")
        return 1
    
    logger.info(f"Found {len(json_files)} processed batch files")
    
    total_texts = 0
    total_scores = 0
    
    for json_file in json_files:
        logger.info(f"Importing: {json_file.name}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        
        if limit:
            items = items[:limit]
        
        async with async_session() as session:
            texts, scores = await import_results(session, items, json_file.stem)
            total_texts += texts
            total_scores += scores
            logger.info(f"  Created {texts} texts, {scores} scores")
    
    await engine.dispose()
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Import Complete!")
    logger.info(f"{'='*50}")
    logger.info(f"Total texts created: {total_texts:,}")
    logger.info(f"Total scores created: {total_scores:,}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description="Import MANEFRAME results to PostgreSQL")
    parser.add_argument("--input-dir", type=str, required=True, help="Directory with processed JSON files")
    parser.add_argument("--limit", type=int, default=None, help="Limit items per file (for testing)")
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        logger.error(f"Input directory not found: {input_dir}")
        return 1
    
    return asyncio.run(main_async(input_dir, args.limit))


if __name__ == "__main__":
    sys.exit(main())
