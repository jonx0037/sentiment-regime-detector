#!/usr/bin/env python3
"""
Analyze raw texts and generate sentiment scores.

This script processes all pending raw texts through the SentimentEngine
and stores the results in the database.

Usage:
    python scripts/analyze_texts.py [--asset-class ASSET_CLASS] [--limit LIMIT]
"""

import asyncio
import argparse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sentiment_detector.core.config import get_settings
from sentiment_detector.services.sentiment_service import SentimentService


async def main(asset_class: str = None, limit: int = None) -> None:
    """Main execution function."""
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        str(settings.database_url),
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Create sentiment service
    service = SentimentService()
    
    try:
        async with async_session() as session:
            print("🤖 Starting sentiment analysis...")
            if asset_class:
                print(f"   Filtering by asset class: {asset_class}")
            if limit:
                print(f"   Limit: {limit} texts")
            print()
            
            # Analyze pending texts
            count = await service.analyze_pending_texts(
                session,
                limit=limit,
                asset_class=asset_class,
            )
            
            print(f"\n✅ Analysis complete! Processed {count} texts.")
            
            # Show summary
            if count > 0:
                print("\n📊 Current sentiment by asset class:")
                sentiments = await service.get_current_sentiment(session)
                
                for sentiment in sorted(sentiments, key=lambda x: x["asset_class"]):
                    ac = sentiment["asset_class"].upper()
                    compound = sentiment["compound_score"]
                    samples = sentiment["sample_count"]
                    
                    # Determine sentiment emoji
                    if compound > 0.1:
                        emoji = "📈"
                        label = "BULLISH"
                    elif compound < -0.1:
                        emoji = "📉"
                        label = "BEARISH"
                    else:
                        emoji = "↔️"
                        label = "NEUTRAL"
                    
                    print(f"  {emoji} {ac:10} | Score: {compound:+.3f} | Samples: {samples:4} | {label}")
            
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze raw texts for sentiment")
    parser.add_argument(
        "--asset-class",
        type=str,
        choices=["equity", "crypto", "forex", "commodity"],
        help="Filter by asset class",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of texts to analyze",
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("SENTIMENT REGIME DETECTOR - Text Analysis Script")
    print("=" * 70)
    print()
    
    asyncio.run(main(asset_class=args.asset_class, limit=args.limit))
    
    print()
    print("=" * 70)
    print("Next steps:")
    print("  1. Start API server: uvicorn sentiment_detector.main:app --reload")
    print("  2. View results: http://localhost:8000/api/v1/sentiment/current")
    print("  3. Check docs: http://localhost:8000/docs")
    print("=" * 70)
