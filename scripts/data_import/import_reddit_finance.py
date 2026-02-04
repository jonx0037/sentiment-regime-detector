#!/usr/bin/env python3
"""
Import Reddit Finance Data for GameStop Backtest.

Imports WSB posts from the leukipp/reddit-finance-data dataset
and processes sentiment locally for the GameStop squeeze period.

This supplements our existing data with the missing Jan 25-27 peak.
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration
WSB_FILE = Path("data/kaggle/reddit-finance/wallstreetbets/submissions_reddit.csv")
START_DATE = "2021-01-20"
END_DATE = "2021-01-27"  # Focus on missing peak period first
BATCH_SIZE = 64  # Batch size for sentiment processing
DB_COMMIT_SIZE = 500  # Commit to DB every N records


def load_wsb_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load WSB posts for the specified date range."""
    logger.info(f"Loading WSB data from {WSB_FILE}")
    
    df = pd.read_csv(WSB_FILE)
    df['created'] = pd.to_datetime(df['created'])
    df['date'] = df['created'].dt.date
    
    # Filter by date range
    mask = (df['date'] >= pd.to_datetime(start_date).date()) & \
           (df['date'] <= pd.to_datetime(end_date).date())
    df = df[mask].copy()
    
    logger.info(f"Loaded {len(df):,} posts from {start_date} to {end_date}")
    
    # Show daily distribution
    daily = df.groupby('date').size()
    for date, count in daily.items():
        logger.info(f"  {date}: {count:,} posts")
    
    return df


def prepare_text(row: pd.Series) -> str:
    """Combine title and selftext for analysis."""
    title = str(row.get('title', '')) if pd.notna(row.get('title')) else ''
    selftext = str(row.get('selftext', '')) if pd.notna(row.get('selftext')) else ''
    
    # Skip removed/deleted content
    if selftext in ['[removed]', '[deleted]']:
        selftext = ''
    
    combined = f"{title} {selftext}".strip()
    return combined[:2000]  # Truncate for model


async def import_and_score(df: pd.DataFrame) -> dict:
    """Import posts to database and compute sentiment scores using batch processing."""
    from sqlalchemy import select, text
    from sentiment_detector.core.database import get_session_context
    from sentiment_detector.models import RawText, SentimentScore as SentimentScoreModel
    from sentiment_detector.services.sentiment_engine import SentimentEngine
    
    # Initialize sentiment analyzer
    logger.info("Initializing sentiment analyzer (DistilBERT on MPS)...")
    engine = SentimentEngine(model_type="distilbert")
    engine.load()  # Pre-load the model
    
    stats = {
        "total": len(df),
        "imported": 0,
        "skipped_duplicate": 0,
        "skipped_empty": 0,
        "scored": 0,
        "errors": 0,
    }
    
    async with get_session_context() as session:
        # First, get existing source_ids to skip duplicates
        logger.info("Checking for existing records...")
        existing_result = await session.execute(
            select(RawText.source_id).where(RawText.source == "reddit")
        )
        existing_ids = set(row[0] for row in existing_result.fetchall())
        logger.info(f"Found {len(existing_ids):,} existing reddit records")
        
        # Prepare all rows first
        rows_to_process = []
        for _, row in df.iterrows():
            content = prepare_text(row)
            if not content or len(content) < 10:
                stats["skipped_empty"] += 1
                continue
            
            source_id = f"wsb_{row['id']}"
            if source_id in existing_ids:
                stats["skipped_duplicate"] += 1
                continue
            
            rows_to_process.append((row, content, source_id))
        
        logger.info(f"Processing {len(rows_to_process):,} new records...")
        
        # Process in batches
        for batch_start in tqdm(range(0, len(rows_to_process), BATCH_SIZE), desc="Batches"):
            batch = rows_to_process[batch_start:batch_start + BATCH_SIZE]
            
            # Extract texts for batch sentiment
            texts = [item[1] for item in batch]
            
            # Batch sentiment analysis
            try:
                sentiment_results = engine.analyze_batch(texts)
            except Exception as e:
                logger.warning(f"Batch sentiment failed: {e}")
                sentiment_results = [None] * len(texts)
            
            # Create database records
            for i, (row, content, source_id) in enumerate(batch):
                try:
                    text_id = uuid4()
                    created_at = row['created'].to_pydatetime()
                    if created_at.tzinfo is None:
                        created_at = created_at.replace(tzinfo=timezone.utc)
                    
                    raw_text = RawText(
                        id=text_id,
                        source="reddit",
                        source_id=source_id,
                        asset_class="equity",
                        content_created_at=created_at,
                        collected_at=datetime.now(timezone.utc),
                        title=str(row.get('title', ''))[:500] if pd.notna(row.get('title')) else None,
                        content=content,
                        metadata={
                            "subreddit": "wallstreetbets",
                            "score": int(row.get('score', 0)) if pd.notna(row.get('score')) else 0,
                            "num_comments": int(row.get('num_comments', 0)) if pd.notna(row.get('num_comments')) else 0,
                        },
                    )
                    session.add(raw_text)
                    stats["imported"] += 1
                    
                    # Add sentiment score if available
                    if sentiment_results[i] is not None:
                        result = sentiment_results[i]
                        sentiment_score = SentimentScoreModel(
                            id=uuid4(),
                            text_id=text_id,
                            model_name="distilbert-sst2",
                            model_version="local",
                            positive=result.positive,
                            negative=result.negative,
                            neutral=result.neutral,
                            compound=result.compound,
                            confidence=result.confidence,
                            processed_at=datetime.now(timezone.utc),
                        )
                        session.add(sentiment_score)
                        stats["scored"] += 1
                    
                except Exception as e:
                    logger.debug(f"Row error: {e}")
                    stats["errors"] += 1
            
            # Commit every DB_COMMIT_SIZE records
            if stats["imported"] % DB_COMMIT_SIZE < BATCH_SIZE:
                await session.commit()
        
        # Final commit
        await session.commit()
    
    return stats


async def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("IMPORTING REDDIT FINANCE DATA FOR GAMESTOP BACKTEST")
    logger.info("=" * 60)
    
    # Load data
    df = load_wsb_data(START_DATE, END_DATE)
    
    if len(df) == 0:
        logger.error("No data found!")
        return
    
    # Import and score
    logger.info("\nImporting to database and computing sentiment...")
    stats = await import_and_score(df)
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("IMPORT COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Total posts:       {stats['total']:,}")
    logger.info(f"Imported:          {stats['imported']:,}")
    logger.info(f"Scored:            {stats['scored']:,}")
    logger.info(f"Skipped (dupe):    {stats['skipped_duplicate']:,}")
    logger.info(f"Skipped (empty):   {stats['skipped_empty']:,}")
    logger.info(f"Errors:            {stats['errors']:,}")


if __name__ == "__main__":
    asyncio.run(main())
