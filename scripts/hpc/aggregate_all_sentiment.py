#!/usr/bin/env python3
"""Aggregate all sentiment batches into comprehensive daily dataset.

After all 72 batches complete, this script:
1. Loads all daily sentiment aggregates
2. Combines into single time series
3. Validates coverage and quality
4. Produces final dataset for backtesting

Run after all batch processing completes.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def load_all_batches(sentiment_dir: Path) -> pd.DataFrame:
    """Load all daily sentiment batch files.

    Args:
        sentiment_dir: Directory containing daily_batch_*.csv files

    Returns:
        Combined DataFrame with all daily sentiment
    """
    print("\n📊 Loading all sentiment batches...")

    batch_files = sorted(sentiment_dir.glob("daily_batch_*.csv"))

    if not batch_files:
        raise FileNotFoundError(f"No batch files found in {sentiment_dir}")

    print(f"  Found {len(batch_files)} batch files")

    all_data = []

    for batch_file in tqdm(batch_files, desc="Loading batches"):
        try:
            df = pd.read_csv(batch_file, parse_dates=['date'])
            all_data.append(df)
        except Exception as e:
            print(f"  ⚠️  Failed to load {batch_file}: {e}")

    combined = pd.concat(all_data, ignore_index=True)

    print(f"  ✓ Loaded {len(combined):,} days")

    return combined


def validate_coverage(df: pd.DataFrame) -> dict:
    """Validate date coverage and quality.

    Args:
        df: Combined daily sentiment DataFrame

    Returns:
        Validation results
    """
    print("\n🔍 Validating coverage...")

    results = {
        "passed": True,
        "issues": []
    }

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    # Check date range
    min_date = df['date'].min()
    max_date = df['date'].max()

    print(f"  Date range: {min_date.date()} to {max_date.date()}")
    results["date_range"] = (str(min_date.date()), str(max_date.date()))

    # Check for gaps
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    missing_dates = date_range.difference(df['date'])

    if len(missing_dates) > 0:
        pct_missing = len(missing_dates) / len(date_range) * 100
        print(f"  ⚠️  Missing {len(missing_dates)} dates ({pct_missing:.1f}%)")
        results["issues"].append(f"Missing {len(missing_dates)} dates")

        if pct_missing > 10:
            results["passed"] = False
    else:
        print(f"  ✓ No missing dates (complete time series)")

    # Check volume distribution
    volume_stats = df['volume'].describe()
    print(f"\n  📊 Volume statistics:")
    print(f"     Mean: {volume_stats['mean']:.0f} texts/day")
    print(f"     Median: {volume_stats['50%']:.0f} texts/day")
    print(f"     Min: {volume_stats['min']:.0f}")
    print(f"     Max: {volume_stats['max']:.0f}")

    results["volume_stats"] = {
        "mean": float(volume_stats['mean']),
        "median": float(volume_stats['50%']),
        "min": float(volume_stats['min']),
        "max": float(volume_stats['max'])
    }

    # Check for low-volume periods
    low_volume = df[df['volume'] < 10]
    if len(low_volume) > 0:
        pct_low = len(low_volume) / len(df) * 100
        print(f"  ⚠️  {len(low_volume)} days with <10 texts ({pct_low:.1f}%)")

        if pct_low > 20:
            results["issues"].append(f"Too many low-volume days: {pct_low:.1f}%")
            results["passed"] = False

    # Validate crisis periods
    crisis_periods = {
        "2008 Financial Crisis": ("2008-09-15", "2009-03-09"),
        "COVID-19 Pandemic": ("2020-02-24", "2020-04-15"),
        "GameStop Squeeze": ("2021-01-13", "2021-02-05")
    }

    print(f"\n  🔍 Crisis period coverage:")

    for name, (start, end) in crisis_periods.items():
        mask = (df['date'] >= start) & (df['date'] <= end)
        crisis_data = df[mask]

        if len(crisis_data) > 0:
            mean_volume = crisis_data['volume'].mean()
            mean_sentiment = crisis_data['compound_mean'].mean()

            print(f"     {name}:")
            print(f"       Days: {len(crisis_data)}")
            print(f"       Avg volume: {mean_volume:.0f} texts/day")
            print(f"       Avg sentiment: {mean_sentiment:.4f}")

            if mean_volume < 50:
                results["issues"].append(f"{name}: Low volume ({mean_volume:.0f})")
        else:
            print(f"     {name}: ❌ NO DATA")
            results["issues"].append(f"{name}: No data coverage")
            results["passed"] = False

    return results


def main():
    """Aggregate all sentiment batches."""
    parser = argparse.ArgumentParser(
        description="Aggregate all sentiment batches into final dataset"
    )
    parser.add_argument(
        "--sentiment-dir",
        type=str,
        required=True,
        help="Directory containing daily_batch_*.csv files"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file for final dataset"
    )

    args = parser.parse_args()

    print("🔍 SENTIMENT AGGREGATION")
    print("=" * 60)
    print(f"Input: {args.sentiment_dir}")
    print(f"Output: {args.output}")
    print("=" * 60)

    try:
        # Load all batches
        combined = load_all_batches(Path(args.sentiment_dir))

        # Remove duplicates (in case of overlapping batches)
        print(f"\n📊 Removing duplicates...")
        before = len(combined)
        combined = combined.drop_duplicates(subset=['date']).sort_values('date')
        after = len(combined)

        if before > after:
            print(f"  ✓ Removed {before - after} duplicate dates")
        else:
            print(f"  ✓ No duplicates found")

        # Validate
        validation = validate_coverage(combined)

        # Save final dataset
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        combined.to_csv(output_path, index=False)

        print(f"\n💾 Saved final dataset: {output_path}")
        print(f"   Total days: {len(combined):,}")
        print(f"   Date range: {combined['date'].min().date()} to {combined['date'].max().date()}")

        # Print summary
        print("\n" + "=" * 60)
        if validation["passed"]:
            print("✅ AGGREGATION COMPLETE - READY FOR BACKTESTING")
        else:
            print("⚠️  AGGREGATION COMPLETE - ISSUES FOUND")
            for issue in validation["issues"]:
                print(f"   • {issue}")
        print("=" * 60)

        # Exit code based on validation
        sys.exit(0 if validation["passed"] else 1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
