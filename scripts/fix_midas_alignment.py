#!/usr/bin/env python3
"""
Check and fix MIDAS data alignment.

Analyzes the overlap between CISS, Sentiment, and Market data
and creates properly aligned datasets for GARCH-MIDAS.
"""

import asyncio
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def get_database_url() -> str:
    """Get database URL."""
    import os
    return os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/sentiment_db"
    )


async def get_session() -> AsyncSession:
    """Create async database session."""
    engine = create_async_engine(get_database_url(), echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session()


async def analyze_data_overlap():
    """Analyze date ranges and overlaps between data sources."""
    
    print("="*60)
    print("DATA OVERLAP ANALYSIS FOR GARCH-MIDAS")
    print("="*60)
    
    session = await get_session()
    
    try:
        # === CISS Date Range ===
        result = await session.execute(text("""
            SELECT MIN(date), MAX(date), COUNT(*) 
            FROM stress_indices 
            WHERE source = 'ecb_ciss'
        """))
        ciss_range = result.fetchone()
        print(f"\n📊 CISS: {ciss_range[0]} to {ciss_range[1]} ({ciss_range[2]:,} records)")
        
        # === Sentiment Date Range ===
        result = await session.execute(text("""
            SELECT 
                MIN(DATE(content_created_at)), 
                MAX(DATE(content_created_at)), 
                COUNT(DISTINCT DATE(content_created_at))
            FROM raw_texts rt 
            JOIN sentiment_scores ss ON rt.id = ss.text_id
        """))
        sent_range = result.fetchone()
        print(f"📊 Sentiment: {sent_range[0]} to {sent_range[1]} ({sent_range[2]:,} unique days)")
        
        # === VIX Date Range ===
        result = await session.execute(text("""
            SELECT MIN(date), MAX(date), COUNT(*) 
            FROM market_data 
            WHERE symbol = '^VIX'
        """))
        vix_range = result.fetchone()
        print(f"📊 VIX: {vix_range[0]} to {vix_range[1]} ({vix_range[2]:,} records)")
        
        # === SPY/Equity Returns ===
        result = await session.execute(text("""
            SELECT symbol, MIN(date), MAX(date), COUNT(*) 
            FROM market_data 
            WHERE symbol IN ('SPY', '^GSPC', '^IXIC')
            GROUP BY symbol
        """))
        equity_data = result.fetchall()
        print(f"\n📈 Equity Data Available:")
        for row in equity_data:
            print(f"   {row[0]}: {row[1]} to {row[2]} ({row[3]:,} records)")
        
        # === Two-Way Overlaps ===
        print("\n" + "="*60)
        print("DATA OVERLAPS")
        print("="*60)
        
        result = await session.execute(text("""
            WITH ciss_dates AS (SELECT DISTINCT date FROM stress_indices WHERE source = 'ecb_ciss'),
                 sent_dates AS (SELECT DISTINCT DATE(content_created_at) as date FROM raw_texts rt JOIN sentiment_scores ss ON rt.id = ss.text_id)
            SELECT COUNT(*) FROM ciss_dates c JOIN sent_dates s ON c.date = s.date
        """))
        cs_overlap = result.fetchone()[0]
        print(f"\n✓ CISS + Sentiment overlap: {cs_overlap:,} days")
        
        result = await session.execute(text("""
            WITH ciss_dates AS (SELECT DISTINCT date FROM stress_indices WHERE source = 'ecb_ciss'),
                 vix_dates AS (SELECT DISTINCT date FROM market_data WHERE symbol = '^VIX')
            SELECT COUNT(*) FROM ciss_dates c JOIN vix_dates v ON c.date = v.date
        """))
        cv_overlap = result.fetchone()[0]
        print(f"✓ CISS + VIX overlap: {cv_overlap:,} days")
        
        result = await session.execute(text("""
            WITH sent_dates AS (SELECT DISTINCT DATE(content_created_at) as date FROM raw_texts rt JOIN sentiment_scores ss ON rt.id = ss.text_id),
                 vix_dates AS (SELECT DISTINCT date FROM market_data WHERE symbol = '^VIX')
            SELECT COUNT(*) FROM sent_dates s JOIN vix_dates v ON s.date = v.date
        """))
        sv_overlap = result.fetchone()[0]
        print(f"✓ Sentiment + VIX overlap: {sv_overlap:,} days")
        
        # === Three-Way Overlap ===
        result = await session.execute(text("""
            WITH ciss_dates AS (SELECT DISTINCT date FROM stress_indices WHERE source = 'ecb_ciss'),
                 sent_dates AS (SELECT DISTINCT DATE(content_created_at) as date FROM raw_texts rt JOIN sentiment_scores ss ON rt.id = ss.text_id),
                 vix_dates AS (SELECT DISTINCT date FROM market_data WHERE symbol = '^VIX')
            SELECT COUNT(*) as overlap_count
            FROM ciss_dates c
            JOIN sent_dates s ON c.date = s.date
            JOIN vix_dates v ON c.date = v.date
        """))
        overlap = result.fetchone()[0]
        print(f"\n🔗 THREE-WAY OVERLAP (CISS + Sentiment + VIX): {overlap:,} days")
        
        # === Get the actual overlapping date range ===
        result = await session.execute(text("""
            WITH ciss_dates AS (SELECT DISTINCT date FROM stress_indices WHERE source = 'ecb_ciss'),
                 sent_dates AS (SELECT DISTINCT DATE(content_created_at) as date FROM raw_texts rt JOIN sentiment_scores ss ON rt.id = ss.text_id),
                 vix_dates AS (SELECT DISTINCT date FROM market_data WHERE symbol = '^VIX')
            SELECT MIN(c.date), MAX(c.date)
            FROM ciss_dates c
            JOIN sent_dates s ON c.date = s.date
            JOIN vix_dates v ON c.date = v.date
        """))
        overlap_range = result.fetchone()
        if overlap_range[0]:
            print(f"   Date range: {overlap_range[0]} to {overlap_range[1]}")
        
        # === Gap Analysis ===
        print("\n" + "="*60)
        print("GAP ANALYSIS")
        print("="*60)
        
        # Find gaps in sentiment data
        result = await session.execute(text("""
            WITH sent_dates AS (
                SELECT DISTINCT DATE(content_created_at) as date 
                FROM raw_texts rt 
                JOIN sentiment_scores ss ON rt.id = ss.text_id
                ORDER BY date
            ),
            date_gaps AS (
                SELECT date, 
                       LAG(date) OVER (ORDER BY date) as prev_date,
                       date - LAG(date) OVER (ORDER BY date) as gap_days
                FROM sent_dates
            )
            SELECT date, prev_date, gap_days
            FROM date_gaps
            WHERE gap_days > 7
            ORDER BY gap_days DESC
            LIMIT 10
        """))
        gaps = result.fetchall()
        if gaps:
            print("\n⚠️ Large gaps in sentiment data (>7 days):")
            for gap in gaps:
                print(f"   {gap[1]} to {gap[0]}: {gap[2]} days")
        else:
            print("\n✓ No major gaps in sentiment data")
        
        return {
            'ciss_range': ciss_range,
            'sent_range': sent_range,
            'vix_range': vix_range,
            'overlap': overlap,
            'cs_overlap': cs_overlap,
        }
        
    finally:
        await session.close()


async def create_aligned_midas_data():
    """Create aligned dataset for GARCH-MIDAS estimation."""
    
    print("\n" + "="*60)
    print("CREATING ALIGNED MIDAS DATASET")
    print("="*60)
    
    session = await get_session()
    
    try:
        # Load CISS data
        result = await session.execute(text("""
            SELECT date, value as ciss
            FROM stress_indices
            WHERE source = 'ecb_ciss'
            ORDER BY date
        """))
        ciss_df = pd.DataFrame(result.fetchall(), columns=['date', 'ciss'])
        ciss_df['date'] = pd.to_datetime(ciss_df['date'])
        ciss_df = ciss_df.set_index('date')
        print(f"\nLoaded CISS: {len(ciss_df)} records")
        
        # Load VIX data
        result = await session.execute(text("""
            SELECT date, close as vix
            FROM market_data
            WHERE symbol = '^VIX'
            ORDER BY date
        """))
        vix_df = pd.DataFrame(result.fetchall(), columns=['date', 'vix'])
        vix_df['date'] = pd.to_datetime(vix_df['date'])
        vix_df = vix_df.set_index('date')
        print(f"Loaded VIX: {len(vix_df)} records")
        
        # Load daily aggregated sentiment
        result = await session.execute(text("""
            SELECT 
                DATE(rt.content_created_at) as date,
                AVG(ss.compound) as sentiment,
                COUNT(*) as text_count
            FROM sentiment_scores ss
            JOIN raw_texts rt ON ss.text_id = rt.id
            WHERE rt.content_created_at IS NOT NULL
            GROUP BY DATE(rt.content_created_at)
            ORDER BY date
        """))
        sent_df = pd.DataFrame(result.fetchall(), columns=['date', 'sentiment', 'text_count'])
        sent_df['date'] = pd.to_datetime(sent_df['date'])
        sent_df = sent_df.set_index('date')
        print(f"Loaded Sentiment: {len(sent_df)} records")
        
        # Load market returns (use SPY for full 2010-2026 coverage)
        result = await session.execute(text("""
            SELECT date, close
            FROM market_data
            WHERE symbol = 'SPY'
            ORDER BY date
        """))
        returns_df = pd.DataFrame(result.fetchall(), columns=['date', 'close'])
        returns_df['date'] = pd.to_datetime(returns_df['date'])
        returns_df = returns_df.set_index('date')
        returns_df['returns'] = np.log(returns_df['close'] / returns_df['close'].shift(1))
        returns_df = returns_df[['returns']]
        print(f"Loaded Returns (SPY): {len(returns_df)} records")
        
        # Merge all data
        print("\nMerging datasets...")
        merged = ciss_df.join(vix_df, how='inner')
        merged = merged.join(sent_df, how='inner')
        merged = merged.join(returns_df, how='inner')
        
        # Drop NaN rows
        merged = merged.dropna()
        
        print(f"\n📊 ALIGNED DATASET:")
        print(f"   Records: {len(merged):,}")
        print(f"   Date range: {merged.index.min()} to {merged.index.max()}")
        print(f"   Columns: {list(merged.columns)}")
        
        # === Create Weekly Aggregations for MIDAS ===
        print("\n" + "="*60)
        print("CREATING MIDAS WEEKLY AGGREGATIONS")
        print("="*60)
        
        # Weekly sentiment
        weekly_sentiment = merged['sentiment'].resample('W').agg(['mean', 'std', 'count'])
        weekly_sentiment.columns = ['sentiment_mean', 'sentiment_std', 'sentiment_count']
        print(f"\nWeekly Sentiment: {len(weekly_sentiment)} weeks")
        
        # Weekly CISS
        weekly_ciss = merged['ciss'].resample('W').agg(['mean', 'max', 'min'])
        weekly_ciss.columns = ['ciss_mean', 'ciss_max', 'ciss_min']
        print(f"Weekly CISS: {len(weekly_ciss)} weeks")
        
        # Weekly realized volatility (annualized)
        weekly_vol = merged['returns'].resample('W').std() * np.sqrt(252)
        weekly_vol.name = 'realized_vol'
        print(f"Weekly Volatility: {len(weekly_vol)} weeks")
        
        # Combine weekly data
        weekly_data = weekly_sentiment.join(weekly_ciss, how='inner')
        weekly_data = weekly_data.join(weekly_vol, how='inner')
        weekly_data = weekly_data.dropna()
        
        print(f"\n📊 WEEKLY MIDAS DATA:")
        print(f"   Records: {len(weekly_data):,} weeks")
        print(f"   Date range: {weekly_data.index.min()} to {weekly_data.index.max()}")
        
        # === Save aligned data ===
        output_dir = project_root / "data" / "midas_aligned"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save daily aligned data
        daily_file = output_dir / "daily_aligned.csv"
        merged.to_csv(daily_file)
        print(f"\n✓ Saved daily data: {daily_file}")
        
        # Save weekly MIDAS data
        weekly_file = output_dir / "weekly_midas.csv"
        weekly_data.to_csv(weekly_file)
        print(f"✓ Saved weekly data: {weekly_file}")
        
        # === Print summary statistics ===
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        print("\nDaily Data:")
        print(merged.describe().round(4).to_string())
        
        print("\nWeekly MIDAS Data:")
        print(weekly_data.describe().round(4).to_string())
        
        # === Correlation matrix ===
        print("\n" + "="*60)
        print("CORRELATION MATRIX (Weekly)")
        print("="*60)
        corr = weekly_data[['sentiment_mean', 'ciss_mean', 'realized_vol']].corr()
        print(corr.round(4).to_string())
        
        return merged, weekly_data
        
    finally:
        await session.close()


async def main():
    """Main function."""
    # Analyze current data overlap
    overlap_info = await analyze_data_overlap()
    
    # Create aligned datasets
    daily_data, weekly_data = await create_aligned_midas_data()
    
    print("\n" + "="*60)
    print("MIDAS ALIGNMENT COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Use data/midas_aligned/daily_aligned.csv for GARCH component")
    print("2. Use data/midas_aligned/weekly_midas.csv for MIDAS component")
    print("3. Re-run HPC script with aligned data")


if __name__ == "__main__":
    asyncio.run(main())
