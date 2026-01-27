#!/usr/bin/env python3
"""Quick test of the sentiment API endpoint."""

import asyncio
import json
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import sys
sys.path.insert(0, '/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/src')

from sentiment_detector.core.config import get_settings
from sentiment_detector.services.sentiment_service import SentimentService


async def test_api():
    """Test the sentiment service directly."""
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
    
    service = SentimentService()
    
    async with async_session() as session:
        print("📊 Fetching current sentiment...")
        sentiments = await service.get_current_sentiment(session)
        
        print("\nCurrent Sentiment by Asset Class:")
        print("=" * 70)
        
        for sentiment in sorted(sentiments, key=lambda x: x["asset_class"]):
            ac = sentiment["asset_class"].upper()
            compound = sentiment["compound_score"]
            samples = sentiment["sample_count"]
            pos = sentiment["positive_ratio"]
            neg = sentiment["negative_ratio"]
            
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
            
            print(f"\n{emoji} {ac:10}")
            print(f"   Compound Score: {compound:+.3f} ({label})")
            print(f"   Positive: {pos:.1%} | Negative: {neg:.1%}")
            print(f"   Sample Count: {samples}")
        
        # Cross-asset stats
        compound_scores = [s["compound_score"] for s in sentiments]
        if compound_scores:
            import statistics
            mean = statistics.mean(compound_scores)
            std = statistics.stdev(compound_scores) if len(compound_scores) > 1 else 0.0
            
            print("\n" + "=" * 70)
            print(f"Cross-Asset Mean: {mean:+.3f}")
            print(f"Cross-Asset Std:  {std:.3f}")
        
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_api())
