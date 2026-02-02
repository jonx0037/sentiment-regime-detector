#!/usr/bin/env python3
"""
Export data for GARCH-MIDAS HPC processing.

Creates CSV files that can be transferred to ManeFrame for
running the full GARCH-MIDAS model with the arch library.

Output files:
- hpc_data/vix_data.csv
- hpc_data/ciss_data.csv
- hpc_data/sentiment_daily.csv
- hpc_data/market_returns.csv
"""

import asyncio
import sys
import os
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from sqlalchemy import text


async def export_vix(session, output_dir: Path):
    """Export VIX data."""
    result = await session.execute(text("""
        SELECT date, open, high, low, close, adj_close, volume
        FROM market_data
        WHERE symbol = '^VIX'
        ORDER BY date
    """))
    
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
    
    output_file = output_dir / "vix_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Exported VIX: {len(df)} records to {output_file}")
    
    return df


async def export_ciss(session, output_dir: Path):
    """Export CISS stress index data."""
    result = await session.execute(text("""
        SELECT date, value, money_market, bond_market, equity_market,
               foreign_exchange, financial_intermediaries
        FROM stress_indices
        WHERE source = 'ecb_ciss'
        ORDER BY date
    """))
    
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=[
        'date', 'ciss', 'money_market', 'bond_market', 'equity_market',
        'foreign_exchange', 'financial_intermediaries'
    ])
    
    output_file = output_dir / "ciss_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Exported CISS: {len(df)} records to {output_file}")
    
    return df


async def export_sentiment(session, output_dir: Path):
    """Export daily aggregated sentiment."""
    result = await session.execute(text("""
        SELECT 
            DATE(rt.content_created_at) as date,
            AVG(ss.compound) as sentiment,
            AVG(ss.positive) as positive,
            AVG(ss.negative) as negative,
            AVG(ss.neutral) as neutral,
            COUNT(*) as count,
            rt.asset_class
        FROM sentiment_scores ss
        JOIN raw_texts rt ON ss.text_id = rt.id
        WHERE rt.content_created_at IS NOT NULL
        GROUP BY DATE(rt.content_created_at), rt.asset_class
        ORDER BY date
    """))
    
    rows = result.fetchall()
    df = pd.DataFrame(rows, columns=[
        'date', 'sentiment', 'positive', 'negative', 'neutral', 'count', 'asset_class'
    ])
    
    # Save full dataset
    output_file = output_dir / "sentiment_daily_by_asset.csv"
    df.to_csv(output_file, index=False)
    print(f"Exported Sentiment (by asset): {len(df)} records to {output_file}")
    
    # Also save aggregated across all assets
    df_agg = df.groupby('date').agg({
        'sentiment': 'mean',
        'positive': 'mean',
        'negative': 'mean',
        'neutral': 'mean',
        'count': 'sum'
    }).reset_index()
    
    output_file_agg = output_dir / "sentiment_daily.csv"
    df_agg.to_csv(output_file_agg, index=False)
    print(f"Exported Sentiment (aggregated): {len(df_agg)} records to {output_file_agg}")
    
    return df_agg


async def export_market_returns(session, output_dir: Path):
    """Export market returns for major indices."""
    # Use available symbols - we have ^IXIC, GLD, ^VIX etc
    symbols = ['^IXIC', 'GLD', '^VIX', 'GC=F', 'BTC-USD']
    
    all_returns = []
    
    for symbol in symbols:
        result = await session.execute(text("""
            SELECT date, symbol, close, adj_close
            FROM market_data
            WHERE symbol = :symbol
            ORDER BY date
        """), {"symbol": symbol})
        
        rows = result.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=['date', 'symbol', 'close', 'adj_close'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            # Use close price (adj_close may be null)
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df['returns'] = np.log(df['close'].astype(float) / df['close'].shift(1).astype(float))
            all_returns.append(df)
    
    if all_returns:
        # Use the first available equity index for returns
        for df in all_returns:
            if df['symbol'].iloc[0] in ['^IXIC', 'GLD', '^VIX']:
                returns_df = df[['date', 'returns']].dropna()
                break
        else:
            returns_df = all_returns[0][['date', 'returns']].dropna()
        
        output_file = output_dir / "market_returns.csv"
        returns_df.to_csv(output_file, index=False)
        print(f"Exported Returns: {len(returns_df)} records to {output_file}")
        
        return returns_df
    
    return pd.DataFrame()


async def export_cross_asset_prices(session, output_dir: Path):
    """Export cross-asset prices for additional analysis."""
    symbols = ['^VIX', 'GC=F', 'GLD', 'SI=F', 'SLV', 'BTC-USD', 'ETH-USD']
    
    all_data = []
    
    for symbol in symbols:
        result = await session.execute(text("""
            SELECT date, symbol, close, adj_close
            FROM market_data
            WHERE symbol = :symbol
            ORDER BY date
        """), {"symbol": symbol})
        
        rows = result.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=['date', 'symbol', 'close', 'adj_close'])
            all_data.append(df)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        output_file = output_dir / "cross_asset_prices.csv"
        combined.to_csv(output_file, index=False)
        print(f"Exported Cross-Asset Prices: {len(combined)} records to {output_file}")
        
        return combined
    
    return pd.DataFrame()


async def main():
    """Export all data for HPC."""
    from src.sentiment_detector.core.database import get_session_context
    
    print("=" * 60)
    print("EXPORTING DATA FOR HPC GARCH-MIDAS")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("scripts/hpc/hpc_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir.absolute()}")
    
    async with get_session_context() as session:
        # Export all datasets
        await export_vix(session, output_dir)
        await export_ciss(session, output_dir)
        await export_sentiment(session, output_dir)
        await export_market_returns(session, output_dir)
        await export_cross_asset_prices(session, output_dir)
    
    print("\n" + "=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)
    
    # Print file listing
    print("\nExported files:")
    for f in sorted(output_dir.glob("*.csv")):
        size = f.stat().st_size / 1024
        print(f"  {f.name}: {size:.1f} KB")
    
    # Print instructions
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("""
1. Create tarball for transfer:
   cd scripts/hpc
   tar -czvf hpc_garch_midas.tar.gz hpc_data/ run_garch_midas_hpc.py

2. Transfer to ManeFrame:
   scp hpc_garch_midas.tar.gz jarocha@m3.smu.edu:/scratch/users/jarocha/

3. On ManeFrame:
   cd /scratch/users/jarocha
   tar -xzvf hpc_garch_midas.tar.gz
   module load python/3.11.11
   pip install --user arch
   python run_garch_midas_hpc.py

4. Transfer results back:
   scp jarocha@m3.smu.edu:/scratch/users/jarocha/garch_midas_results*.json ./
""")


if __name__ == "__main__":
    asyncio.run(main())
