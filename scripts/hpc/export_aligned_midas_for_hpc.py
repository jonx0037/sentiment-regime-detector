#!/usr/bin/env python3
"""
Export aligned MIDAS data for HPC GARCH-MIDAS estimation.

This script reads the aligned daily data (SPY + CISS + sentiment)
and exports it in the format expected by run_garch_midas_hpc.py.

Usage:
    python export_aligned_midas_for_hpc.py
"""

import pandas as pd
from pathlib import Path

def main():
    print("=" * 60)
    print("EXPORTING ALIGNED MIDAS DATA FOR HPC")
    print("=" * 60)

    # Read aligned daily data
    aligned_file = Path("data/midas_aligned/daily_aligned.csv")
    if not aligned_file.exists():
        print(f"ERROR: {aligned_file} not found")
        print("Please run download_spy_data.py first to create aligned data")
        return 1

    df = pd.read_csv(aligned_file, parse_dates=['date'])
    print(f"\nLoaded {len(df)} daily records from {aligned_file}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Columns: {df.columns.tolist()}")

    # Create HPC data directory
    hpc_data_dir = Path("scripts/hpc/hpc_data")
    hpc_data_dir.mkdir(parents=True, exist_ok=True)

    # Export VIX data
    vix_df = df[['date', 'vix']].rename(columns={'vix': 'close'})
    vix_df.to_csv(hpc_data_dir / "vix_data.csv", index=False)
    print(f"\n✓ Exported VIX: {len(vix_df)} records")

    # Export CISS data
    ciss_df = df[['date', 'ciss']].rename(columns={'ciss': 'value'})
    ciss_df.to_csv(hpc_data_dir / "ciss_data.csv", index=False)
    print(f"✓ Exported CISS: {len(ciss_df)} records")

    # Export sentiment data
    sentiment_df = df[['date', 'sentiment']]
    sentiment_df.to_csv(hpc_data_dir / "sentiment_daily.csv", index=False)
    print(f"✓ Exported Sentiment: {len(sentiment_df)} records")

    # Export returns data
    returns_df = df[['date', 'returns']]
    returns_df.to_csv(hpc_data_dir / "market_returns.csv", index=False)
    print(f"✓ Exported Returns: {len(returns_df)} records")

    # Print summary statistics
    print("\n" + "=" * 60)
    print("DATA SUMMARY")
    print("=" * 60)
    print(f"\nReturns:")
    print(f"  Mean: {df['returns'].mean():.6f}")
    print(f"  Std: {df['returns'].std():.6f}")
    print(f"  Annualized vol: {df['returns'].std() * (252**0.5):.2%}")

    print(f"\nSentiment:")
    print(f"  Mean: {df['sentiment'].mean():.6f}")
    print(f"  Std: {df['sentiment'].std():.6f}")
    print(f"  Range: [{df['sentiment'].min():.3f}, {df['sentiment'].max():.3f}]")

    print(f"\nCISS:")
    print(f"  Mean: {df['ciss'].mean():.6f}")
    print(f"  Max: {df['ciss'].max():.6f}")
    print(f"  Range: [{df['ciss'].min():.3f}, {df['ciss'].max():.3f}]")

    print(f"\nVIX:")
    print(f"  Mean: {df['vix'].mean():.2f}")
    print(f"  Max: {df['vix'].max():.2f}")
    print(f"  Range: [{df['vix'].min():.2f}, {df['vix'].max():.2f}]")

    print("\n" + "=" * 60)
    print(f"✓ All data exported to: {hpc_data_dir}")
    print("=" * 60)
    print("\nReady for HPC submission!")
    print("Next steps:")
    print("  1. Create HPC package: cd scripts/hpc && tar -czf hpc_garch_midas_aligned.tar.gz *.py hpc_data/ garch_midas.slurm")
    print("  2. Copy to HPC: scp hpc_garch_midas_aligned.tar.gz <username>@m3.smu.edu:~/")
    print("  3. Submit job: sbatch garch_midas.slurm")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
