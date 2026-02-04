#!/usr/bin/env python3
"""Import sentiment analysis results to PostgreSQL database."""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()


def get_db_url() -> str:
    """Get database URL from environment."""
    url = os.getenv("DATABASE_URL", "")
    # Convert asyncpg URL to standard format for asyncpg
    return url.replace("postgresql+asyncpg://", "postgresql://")


async def import_sentiment_data(
    data_path: Path,
    batch_size: int = 100,
    clear_existing: bool = False,
) -> dict[str, Any]:
    """
    Import sentiment data from JSON file to PostgreSQL.
    
    Args:
        data_path: Path to JSON file with sentiment results
        batch_size: Number of records to insert per batch
        clear_existing: Whether to clear existing data first
        
    Returns:
        Summary of import results
    """
    # Load data
    print(f"\n📂 Loading data from {data_path}...")
    with open(data_path) as f:
        data = json.load(f)
    
    # Handle nested format
    if isinstance(data, dict) and "items" in data:
        items = data["items"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Unknown data format")
    
    print(f"   Found {len(items)} items to import")
    
    # Connect to database
    db_url = get_db_url()
    print(f"\n🔌 Connecting to database...")
    conn = await asyncpg.connect(db_url)
    
    try:
        if clear_existing:
            print("   🗑️  Clearing existing data...")
            await conn.execute("DELETE FROM sentiment_scores")
            await conn.execute("DELETE FROM raw_texts")
        
        # Import counters
        texts_inserted = 0
        texts_skipped = 0
        scores_inserted = 0
        
        print(f"\n📥 Importing data in batches of {batch_size}...")
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                # Generate UUIDs
                text_id = uuid.uuid4()
                score_id = uuid.uuid4()
                
                # Parse timestamp
                created_at = item.get("created_at", "")
                if created_at:
                    try:
                        if "T" in created_at:
                            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        else:
                            dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                    except:
                        dt = datetime.now(timezone.utc)
                else:
                    dt = datetime.now(timezone.utc)
                
                now = datetime.now(timezone.utc)
                
                # Check for duplicate source_id
                source_id = item.get("id") or item.get("source_id")
                if source_id:
                    existing = await conn.fetchval(
                        "SELECT id FROM raw_texts WHERE source = $1 AND source_id = $2",
                        item.get("source", "unknown"),
                        source_id
                    )
                    if existing:
                        texts_skipped += 1
                        continue
                
                # Insert raw_text
                try:
                    await conn.execute(
                        """
                        INSERT INTO raw_texts (
                            id, source, source_id, asset_class, content_created_at,
                            collected_at, title, content, metadata, created_at, updated_at
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                        """,
                        text_id,
                        item.get("source", "unknown"),
                        source_id,
                        item.get("asset_class", "unknown"),
                        dt,
                        now,
                        item.get("title"),
                        item.get("content", ""),
                        json.dumps(item.get("metadata", {})),
                        now,
                        now,
                    )
                    texts_inserted += 1
                except asyncpg.UniqueViolationError:
                    texts_skipped += 1
                    continue
                
                # Insert sentiment_score if available
                if "sentiment_label" in item or "sentiment_score" in item:
                    label = item.get("sentiment_label", "neutral")
                    score = item.get("sentiment_score", 0.5)
                    
                    # Convert label to probabilities
                    if label == "positive":
                        positive, negative, neutral = score, 0.0, 1 - score
                    elif label == "negative":
                        positive, negative, neutral = 0.0, score, 1 - score
                    else:  # neutral
                        positive, negative, neutral = 0.0, 0.0, score
                    
                    # Compound score: positive is +, negative is -
                    if label == "positive":
                        compound = score
                    elif label == "negative":
                        compound = -score
                    else:
                        compound = 0.0
                    
                    await conn.execute(
                        """
                        INSERT INTO sentiment_scores (
                            id, text_id, model_name, model_version,
                            positive, negative, neutral, compound, confidence,
                            processed_at, created_at, updated_at
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                        """,
                        score_id,
                        text_id,
                        "finbert",
                        "ProsusAI/finbert",
                        positive,
                        negative,
                        neutral,
                        compound,
                        score,
                        now,
                        now,
                        now,
                    )
                    scores_inserted += 1
            
            # Progress update
            progress = min(i + batch_size, len(items))
            print(f"   Processed {progress}/{len(items)} items...", end="\r")
        
        print(f"\n\n✅ Import complete!")
        
        # Get final counts
        text_count = await conn.fetchval("SELECT COUNT(*) FROM raw_texts")
        score_count = await conn.fetchval("SELECT COUNT(*) FROM sentiment_scores")
        
        return {
            "texts_inserted": texts_inserted,
            "texts_skipped": texts_skipped,
            "scores_inserted": scores_inserted,
            "total_texts_in_db": text_count,
            "total_scores_in_db": score_count,
        }
        
    finally:
        await conn.close()


async def show_stats():
    """Show database statistics."""
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        print("\n" + "=" * 60)
        print("📊 Database Statistics")
        print("=" * 60)
        
        # Total counts
        text_count = await conn.fetchval("SELECT COUNT(*) FROM raw_texts")
        score_count = await conn.fetchval("SELECT COUNT(*) FROM sentiment_scores")
        print(f"\n📝 Total raw texts: {text_count}")
        print(f"📈 Total sentiment scores: {score_count}")
        
        # By source
        print("\n📡 By Source:")
        rows = await conn.fetch(
            "SELECT source, COUNT(*) as count FROM raw_texts GROUP BY source ORDER BY count DESC"
        )
        for row in rows:
            print(f"   {row['source']:15} {row['count']:,} items")
        
        # By asset class
        print("\n📊 By Asset Class:")
        rows = await conn.fetch(
            "SELECT asset_class, COUNT(*) as count FROM raw_texts GROUP BY asset_class ORDER BY count DESC"
        )
        for row in rows:
            print(f"   {row['asset_class']:15} {row['count']:,} items")
        
        # Sentiment distribution
        print("\n😊 Sentiment Distribution:")
        rows = await conn.fetch("""
            SELECT 
                CASE 
                    WHEN compound > 0.1 THEN 'positive'
                    WHEN compound < -0.1 THEN 'negative'
                    ELSE 'neutral'
                END as sentiment,
                COUNT(*) as count,
                ROUND(AVG(confidence)::numeric, 3) as avg_confidence
            FROM sentiment_scores
            GROUP BY 1
            ORDER BY count DESC
        """)
        for row in rows:
            print(f"   {row['sentiment']:15} {row['count']:,} items (avg conf: {row['avg_confidence']})")
        
        # Recent items
        print("\n🕐 Most Recent Items:")
        rows = await conn.fetch("""
            SELECT rt.source, rt.asset_class, rt.title, ss.compound
            FROM raw_texts rt
            JOIN sentiment_scores ss ON rt.id = ss.text_id
            ORDER BY rt.content_created_at DESC
            LIMIT 5
        """)
        for row in rows:
            title = (row['title'] or "")[:50]
            sentiment = "📈" if row['compound'] > 0.1 else "📉" if row['compound'] < -0.1 else "➖"
            print(f"   {sentiment} [{row['source']}] {title}...")
        
    finally:
        await conn.close()


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Import sentiment data to PostgreSQL")
    parser.add_argument(
        "--file",
        type=str,
        default="data/processed/kaggle_rss_combined_sentiment.json",
        help="Path to JSON file with sentiment results",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before import",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics only (no import)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for inserts",
    )
    
    args = parser.parse_args()
    
    if args.stats:
        await show_stats()
        return
    
    data_path = Path(args.file)
    if not data_path.exists():
        print(f"❌ File not found: {data_path}")
        return
    
    results = await import_sentiment_data(
        data_path,
        batch_size=args.batch_size,
        clear_existing=args.clear,
    )
    
    print("\n" + "=" * 60)
    print("📊 Import Summary")
    print("=" * 60)
    print(f"   Texts inserted:     {results['texts_inserted']}")
    print(f"   Texts skipped:      {results['texts_skipped']}")
    print(f"   Scores inserted:    {results['scores_inserted']}")
    print(f"   Total texts in DB:  {results['total_texts_in_db']}")
    print(f"   Total scores in DB: {results['total_scores_in_db']}")
    
    # Show stats after import
    await show_stats()


if __name__ == "__main__":
    asyncio.run(main())
