#!/usr/bin/env python3
"""Quick database count check."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from sentiment_detector.core.database import get_session_context


async def main():
    async with get_session_context() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM raw_texts"))
        print(f"RawTexts: {result.scalar()}")
        
        result = await session.execute(text("SELECT COUNT(*) FROM sentiment_scores"))
        print(f"SentimentScores: {result.scalar()}")
        
        # Latest 5 entries with scores
        result = await session.execute(text("""
            SELECT rt.source, LEFT(rt.content, 50), ss.compound
            FROM raw_texts rt
            JOIN sentiment_scores ss ON rt.id = ss.text_id
            ORDER BY ss.processed_at DESC
            LIMIT 5
        """))
        print("\nLatest imported records:")
        for row in result:
            print(f"  {row[0]}: \"{row[1]}...\" → compound={row[2]:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
