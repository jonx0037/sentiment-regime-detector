#!/usr/bin/env python3
"""Check sentiment processing status across all data sources."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from sentiment_detector.core.database import get_session_context


async def main():
    async with get_session_context() as session:
        # Total texts vs scored texts
        total = (await session.execute(text("SELECT COUNT(*) FROM raw_texts"))).scalar()
        scored = (await session.execute(text("SELECT COUNT(*) FROM sentiment_scores"))).scalar()
        
        print("=" * 75)
        print("SENTIMENT PROCESSING STATUS")
        print("=" * 75)
        print(f"Total RawTexts: {total:,}")
        print(f"Total SentimentScores: {scored:,}")
        print(f"Gap (texts without scores): {total - scored:,}")
        print()
        
        await session.commit()
        
        # Breakdown by source - texts with and without scores
        result = await session.execute(text("""
            SELECT 
                rt.source,
                COUNT(DISTINCT rt.id) as total_texts,
                COUNT(DISTINCT ss.text_id) as scored_texts
            FROM raw_texts rt
            LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id
            GROUP BY rt.source
            ORDER BY total_texts DESC
        """))
        rows = result.fetchall()
        await session.commit()
        
        print("Processing status by source:")
        print(f"{'Source':<25} {'Total':>12} {'Scored':>12} {'Unscored':>12} {'Coverage':>10}")
        print("-" * 75)
        
        needs_processing = []
        for row in rows:
            source, total_t, scored_t = row
            unscored = total_t - scored_t
            coverage = (scored_t / total_t * 100) if total_t > 0 else 0
            status = "✅" if coverage >= 99 else "⚠️" if coverage >= 50 else "🔴"
            print(f"{source:<25} {total_t:>12,} {scored_t:>12,} {unscored:>12,} {coverage:>8.1f}% {status}")
            
            if unscored > 0 and coverage < 99:
                needs_processing.append((source, unscored))
        
        print()
        if needs_processing:
            print("Sources needing sentiment processing:")
            total_unprocessed = 0
            for source, count in needs_processing:
                print(f"  - {source}: {count:,} texts")
                total_unprocessed += count
            print(f"\nTotal unprocessed: {total_unprocessed:,}")
        else:
            print("All sources have sentiment scores! ✅")


if __name__ == "__main__":
    asyncio.run(main())
