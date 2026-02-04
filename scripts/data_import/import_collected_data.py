#!/usr/bin/env python3
"""
Import collected data to PostgreSQL.

Imports raw text data from JSON collection files into the database
and optionally runs sentiment analysis.

Usage:
    python scripts/import_collected_data.py --input data/raw/scheduled/collection_2026-01-30.json
    python scripts/import_collected_data.py --input data/raw/scheduled/collection_2026-01-30.json --analyze
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import select
from sentiment_detector.core.database import get_session_context
from sentiment_detector.models import RawText
from sentiment_detector.collectors.base import DataSource, AssetClass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def parse_source(source_str: str) -> DataSource:
    """Parse source string to DataSource enum."""
    source_map = {
        "twitter": DataSource.TWITTER,
        "rss": DataSource.RSS,
        "news": DataSource.NEWS,
        "newsapi": DataSource.NEWS,
        "reddit": DataSource.REDDIT,
        "kaggle": DataSource.KAGGLE,
    }
    return source_map.get(source_str.lower(), DataSource.NEWS)


def parse_asset_class(asset_str: str) -> AssetClass:
    """Parse asset class string to AssetClass enum."""
    asset_map = {
        "equity": AssetClass.EQUITY,
        "crypto": AssetClass.CRYPTO,
        "forex": AssetClass.FOREX,
        "commodity": AssetClass.COMMODITY,
    }
    return asset_map.get(asset_str.lower(), AssetClass.EQUITY)


async def import_collection(input_path: Path, run_analysis: bool = False) -> dict:
    """Import a collection JSON file to the database."""
    
    logger.info(f"Loading collection from: {input_path}")
    
    with open(input_path) as f:
        data = json.load(f)
    
    items = data.get("items", [])
    logger.info(f"Found {len(items)} items to import")
    
    if not items:
        return {"texts_created": 0, "texts_skipped": 0}
    
    texts_created = 0
    texts_skipped = 0
    seen_in_batch = set()  # Track duplicates within this batch
    
    async with get_session_context() as session:
        for item in items:
            # Generate source_id from item id or content hash
            source_id = str(item.get("id") or hash(item.get("content", "")[:100]))
            source = parse_source(item.get("source", "other")).value
            
            # Skip duplicates within this batch
            batch_key = (source, source_id)
            if batch_key in seen_in_batch:
                texts_skipped += 1
                continue
            seen_in_batch.add(batch_key)
            
            # Check if already exists in database
            existing = await session.execute(
                select(RawText).where(
                    RawText.source == source,
                    RawText.source_id == source_id,
                )
            )
            if existing.scalar_one_or_none():
                texts_skipped += 1
                continue
            
            # Parse created_at
            created_at = None
            if item.get("created_at"):
                try:
                    created_at = datetime.fromisoformat(
                        item["created_at"].replace("Z", "+00:00")
                    )
                except (ValueError, AttributeError):
                    created_at = datetime.now(timezone.utc)
            
            # Create RawText
            raw_text = RawText(
                id=uuid4(),
                source=source,
                source_id=str(source_id),
                asset_class=parse_asset_class(item.get("asset_class", "mixed")).value,
                content=item.get("content", "")[:10000],
                title=item.get("title", "")[:500] if item.get("title") else None,
                content_created_at=created_at,
                collected_at=datetime.now(timezone.utc),
                metadata_=item.get("metadata", {}),
            )
            session.add(raw_text)
            texts_created += 1
            
            # Commit in batches
            if texts_created % 100 == 0:
                await session.commit()
                logger.info(f"  Imported {texts_created} texts...")
        
        await session.commit()
    
    logger.info(f"Import complete: {texts_created} created, {texts_skipped} skipped (duplicates)")
    
    # Run sentiment analysis if requested
    if run_analysis and texts_created > 0:
        logger.info("Running sentiment analysis on new texts...")
        await run_sentiment_analysis()
    
    return {
        "texts_created": texts_created,
        "texts_skipped": texts_skipped,
    }


async def run_sentiment_analysis():
    """Run sentiment analysis on unprocessed texts."""
    try:
        from sentiment_detector.services.analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        async with get_session_context() as session:
            # Find texts without scores
            result = await session.execute(
                select(RawText).where(
                    ~RawText.id.in_(
                        select(RawText.id).join(
                            RawText.sentiment_scores
                        )
                    )
                ).limit(1000)
            )
            unprocessed = result.scalars().all()
            
            if not unprocessed:
                logger.info("All texts already have sentiment scores")
                return
            
            logger.info(f"Analyzing {len(unprocessed)} unprocessed texts...")
            
            for text in unprocessed:
                score = await analyzer.analyze(text.content)
                # Score is saved by the analyzer
            
            logger.info("Sentiment analysis complete")
            
    except ImportError as e:
        logger.warning(f"Sentiment analyzer not available: {e}")
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="Import collected data to PostgreSQL",
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to collection JSON file",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Run sentiment analysis on imported texts",
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    result = await import_collection(input_path, run_analysis=args.analyze)
    
    print(f"\n✅ Import complete!")
    print(f"   Texts created: {result['texts_created']}")
    print(f"   Texts skipped: {result['texts_skipped']}")


if __name__ == "__main__":
    asyncio.run(main())
