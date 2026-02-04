#!/usr/bin/env python3
"""Quick status check for the project."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from sentiment_detector.core.database import get_session_context


async def main():
    async with get_session_context() as session:
        print("=" * 60)
        print("DATABASE STATUS CHECK - February 1, 2026 Evening")
        print("=" * 60)
        
        # Core tables
        result = await session.execute(text("SELECT COUNT(*) FROM raw_texts"))
        print(f"RawTexts: {result.scalar():,}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM sentiment_scores"))
        print(f"SentimentScores: {result.scalar():,}")
        
        # Commit to clear any pending transaction state
        await session.commit()
        
        # Check for stress_indices table
        print()
        try:
            result = await session.execute(text("SELECT COUNT(*) FROM stress_indices"))
            print(f"StressIndices: {result.scalar():,}")
            await session.commit()
        except Exception as e:
            print(f"StressIndices: Table error - {e}")
            await session.rollback()
        
        # Check for market_data table
        try:
            result = await session.execute(text("SELECT COUNT(*) FROM market_data"))
            print(f"MarketData: {result.scalar():,}")
            await session.commit()
        except Exception as e:
            print(f"MarketData: Table error - {e}")
            await session.rollback()
        
        # Check sources breakdown
        print()
        print("Sources breakdown:")
        try:
            result = await session.execute(text("""
                SELECT source, COUNT(*) as cnt 
                FROM raw_texts 
                GROUP BY source 
                ORDER BY cnt DESC 
                LIMIT 10
            """))
            for row in result:
                print(f"  {row[0]}: {row[1]:,}")
            await session.commit()
        except Exception as e:
            print(f"  Error: {e}")
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
