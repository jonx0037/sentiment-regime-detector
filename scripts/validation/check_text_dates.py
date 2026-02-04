#!/usr/bin/env python3
"""Quick check of text date coverage."""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

async def main():
    from sentiment_detector.core.database import get_session_context
    from sqlalchemy import text
    
    async with get_session_context() as session:
        # Text date coverage
        r = await session.execute(text("""
            SELECT MIN(content_created_at::date), MAX(content_created_at::date), COUNT(*)
            FROM raw_texts WHERE content_created_at IS NOT NULL
        """))
        row = r.fetchone()
        print(f"Raw Texts: {row[2]:,} records")
        print(f"Date Range: {row[0]} to {row[1]}")
        
        # By year
        r = await session.execute(text("""
            SELECT EXTRACT(YEAR FROM content_created_at)::int as year, COUNT(*)
            FROM raw_texts WHERE content_created_at IS NOT NULL
            GROUP BY year ORDER BY year
        """))
        print("\nBy Year:")
        for row in r.fetchall():
            print(f"  {row[0]}: {row[1]:,}")

asyncio.run(main())
