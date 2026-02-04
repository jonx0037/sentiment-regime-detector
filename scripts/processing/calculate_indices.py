#!/usr/bin/env python3
"""Calculate aggregated sentiment indices from raw sentiment scores."""

import asyncio
from datetime import datetime, timezone, timedelta
from typing import Any
import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()


def get_db_url() -> str:
    """Get database URL from environment."""
    url = os.getenv("DATABASE_URL", "")
    return url.replace("postgresql+asyncpg://", "postgresql://")


async def calculate_sentiment_indices(
    granularity: str = "daily",
    lookback_days: int = 365,
) -> dict[str, Any]:
    """
    Calculate aggregated sentiment indices from raw scores.
    
    Args:
        granularity: 'hourly' or 'daily'
        lookback_days: How far back to calculate
        
    Returns:
        Summary of calculated indices
    """
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        print(f"\n📊 Calculating {granularity} sentiment indices...")
        
        # Clear existing indices for this granularity
        await conn.execute(
            "DELETE FROM sentiment_indices WHERE granularity = $1",
            granularity
        )
        
        # Time truncation function based on granularity
        if granularity == "hourly":
            trunc = "hour"
        else:
            trunc = "day"
        
        cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
        
        # Calculate aggregated indices by asset class, source, and time period
        query = f"""
        WITH aggregated AS (
            SELECT 
                rt.asset_class,
                rt.source,
                date_trunc('{trunc}', rt.content_created_at) as period_start,
                date_trunc('{trunc}', rt.content_created_at) + interval '1 {trunc}' as period_end,
                AVG(ss.compound) as mean_compound,
                STDDEV(ss.compound) as std_compound,
                COUNT(*) as sample_count,
                SUM(CASE WHEN ss.compound > 0.1 THEN 1 ELSE 0 END)::float / COUNT(*) as positive_ratio,
                SUM(CASE WHEN ss.compound < -0.1 THEN 1 ELSE 0 END)::float / COUNT(*) as negative_ratio
            FROM raw_texts rt
            JOIN sentiment_scores ss ON rt.id = ss.text_id
            WHERE rt.content_created_at >= $1
            GROUP BY rt.asset_class, rt.source, date_trunc('{trunc}', rt.content_created_at)
            HAVING COUNT(*) >= 1
        )
        INSERT INTO sentiment_indices (
            id, asset_class, source, period_start, period_end, granularity,
            mean_compound, std_compound, sample_count, positive_ratio, negative_ratio,
            created_at, updated_at
        )
        SELECT 
            gen_random_uuid(),
            asset_class,
            source,
            period_start,
            period_end,
            $2,
            mean_compound,
            std_compound,
            sample_count,
            positive_ratio,
            negative_ratio,
            NOW(),
            NOW()
        FROM aggregated
        RETURNING id;
        """
        
        rows = await conn.fetch(query, cutoff, granularity)
        indices_created = len(rows)
        
        # Also create aggregated indices across all sources (source = NULL)
        query_agg = f"""
        WITH aggregated AS (
            SELECT 
                rt.asset_class,
                date_trunc('{trunc}', rt.content_created_at) as period_start,
                date_trunc('{trunc}', rt.content_created_at) + interval '1 {trunc}' as period_end,
                AVG(ss.compound) as mean_compound,
                STDDEV(ss.compound) as std_compound,
                COUNT(*) as sample_count,
                SUM(CASE WHEN ss.compound > 0.1 THEN 1 ELSE 0 END)::float / COUNT(*) as positive_ratio,
                SUM(CASE WHEN ss.compound < -0.1 THEN 1 ELSE 0 END)::float / COUNT(*) as negative_ratio
            FROM raw_texts rt
            JOIN sentiment_scores ss ON rt.id = ss.text_id
            WHERE rt.content_created_at >= $1
            GROUP BY rt.asset_class, date_trunc('{trunc}', rt.content_created_at)
            HAVING COUNT(*) >= 1
        )
        INSERT INTO sentiment_indices (
            id, asset_class, source, period_start, period_end, granularity,
            mean_compound, std_compound, sample_count, positive_ratio, negative_ratio,
            created_at, updated_at
        )
        SELECT 
            gen_random_uuid(),
            asset_class,
            NULL,
            period_start,
            period_end,
            $2,
            mean_compound,
            std_compound,
            sample_count,
            positive_ratio,
            negative_ratio,
            NOW(),
            NOW()
        FROM aggregated
        RETURNING id;
        """
        
        rows_agg = await conn.fetch(query_agg, cutoff, granularity)
        indices_created += len(rows_agg)
        
        print(f"   ✅ Created {indices_created} indices")
        
        # Show summary
        print(f"\n📈 Sentiment Index Summary:")
        
        summary = await conn.fetch("""
            SELECT 
                asset_class,
                COALESCE(source, 'ALL') as source,
                COUNT(*) as periods,
                ROUND(AVG(mean_compound)::numeric, 4) as avg_sentiment,
                ROUND(AVG(sample_count)::numeric, 1) as avg_samples
            FROM sentiment_indices
            WHERE granularity = $1
            GROUP BY asset_class, source
            ORDER BY asset_class, source
        """, granularity)
        
        for row in summary:
            print(f"   {row['asset_class']:12} [{row['source']:8}] "
                  f"{row['periods']} periods, avg sentiment: {row['avg_sentiment']}, "
                  f"avg samples: {row['avg_samples']}")
        
        return {
            "granularity": granularity,
            "indices_created": indices_created,
            "lookback_days": lookback_days,
        }
        
    finally:
        await conn.close()


async def calculate_momentum():
    """Calculate sentiment momentum (rate of change)."""
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        print("\n📉 Calculating sentiment momentum...")
        
        # Update momentum as difference from previous period
        await conn.execute("""
            WITH lagged AS (
                SELECT 
                    id,
                    mean_compound,
                    LAG(mean_compound) OVER (
                        PARTITION BY asset_class, source, granularity 
                        ORDER BY period_start
                    ) as prev_compound
                FROM sentiment_indices
            )
            UPDATE sentiment_indices si
            SET sentiment_momentum = lagged.mean_compound - lagged.prev_compound
            FROM lagged
            WHERE si.id = lagged.id AND lagged.prev_compound IS NOT NULL
        """)
        
        # Calculate acceleration (second derivative)
        await conn.execute("""
            WITH lagged AS (
                SELECT 
                    id,
                    sentiment_momentum,
                    LAG(sentiment_momentum) OVER (
                        PARTITION BY asset_class, source, granularity 
                        ORDER BY period_start
                    ) as prev_momentum
                FROM sentiment_indices
            )
            UPDATE sentiment_indices si
            SET sentiment_acceleration = lagged.sentiment_momentum - lagged.prev_momentum
            FROM lagged
            WHERE si.id = lagged.id AND lagged.prev_momentum IS NOT NULL
        """)
        
        print("   ✅ Momentum calculated")
        
    finally:
        await conn.close()


async def show_latest_indices():
    """Show the latest sentiment indices."""
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        print("\n" + "=" * 70)
        print("📊 Latest Sentiment Indices")
        print("=" * 70)
        
        rows = await conn.fetch("""
            SELECT DISTINCT ON (asset_class)
                asset_class,
                period_start,
                mean_compound,
                sample_count,
                positive_ratio,
                negative_ratio,
                sentiment_momentum
            FROM sentiment_indices
            WHERE source IS NULL
            ORDER BY asset_class, period_start DESC
        """)
        
        print(f"\n{'Asset':<12} {'Date':<12} {'Sentiment':>10} {'Samples':>8} "
              f"{'Pos%':>6} {'Neg%':>6} {'Momentum':>10}")
        print("-" * 70)
        
        for row in rows:
            momentum = row['sentiment_momentum'] or 0
            momentum_icon = "📈" if momentum > 0.05 else "📉" if momentum < -0.05 else "➖"
            
            print(f"{row['asset_class']:<12} "
                  f"{row['period_start'].strftime('%Y-%m-%d'):<12} "
                  f"{row['mean_compound']:>10.4f} "
                  f"{row['sample_count']:>8} "
                  f"{row['positive_ratio']*100:>5.1f}% "
                  f"{row['negative_ratio']*100:>5.1f}% "
                  f"{momentum_icon} {momentum:>+.4f}")
        
        # Overall market sentiment
        overall = await conn.fetchrow("""
            SELECT 
                AVG(mean_compound) as overall_sentiment,
                SUM(sample_count) as total_samples
            FROM sentiment_indices
            WHERE source IS NULL
            AND period_start = (
                SELECT MAX(period_start) FROM sentiment_indices WHERE source IS NULL
            )
        """)
        
        if overall:
            sentiment = overall['overall_sentiment'] or 0
            sentiment_label = "🟢 BULLISH" if sentiment > 0.1 else "🔴 BEARISH" if sentiment < -0.1 else "🟡 NEUTRAL"
            print(f"\n{'Overall Market':<12} {' '*12} {sentiment:>10.4f} "
                  f"{overall['total_samples']:>8} {' '*14} {sentiment_label}")
        
    finally:
        await conn.close()


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Calculate sentiment indices")
    parser.add_argument("--granularity", default="daily", choices=["hourly", "daily"])
    parser.add_argument("--lookback", type=int, default=365, help="Lookback days")
    
    args = parser.parse_args()
    
    # Calculate indices
    await calculate_sentiment_indices(args.granularity, args.lookback)
    
    # Calculate momentum
    await calculate_momentum()
    
    # Show results
    await show_latest_indices()


if __name__ == "__main__":
    asyncio.run(main())
