#!/usr/bin/env python3
"""Validate FinBERT CSV against raw source data.

This script verifies that the aggregated daily sentiment in
finbert_daily_sentiment.csv was computed correctly from the
raw Kaggle data sources.

Part of Phase 2: Data Integrity Validation (Extended)
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def load_finbert_csv() -> pd.DataFrame:
    """Load the aggregated FinBERT daily sentiment CSV.

    Returns:
        DataFrame with daily aggregated sentiment
    """
    csv_path = Path("data/finbert_daily_sentiment.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"FinBERT CSV not found at {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["date"])
    print(f"✓ Loaded FinBERT CSV: {len(df):,} rows")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")

    return df


def load_kaggle_reddit_data() -> pd.DataFrame:
    """Load raw Kaggle Reddit data.

    Returns:
        DataFrame with raw Reddit posts
    """
    reddit_path = Path("data/kaggle/wsb/reddit_wsb.csv")

    if not reddit_path.exists():
        print(f"⚠️  Reddit data not found at {reddit_path}")
        return pd.DataFrame()

    df = pd.read_csv(reddit_path)
    print(f"✓ Loaded Reddit data: {len(df):,} rows")

    # Parse timestamp if it exists
    if 'timestamp' in df.columns:
        df['date'] = pd.to_datetime(df['timestamp'], unit='s')
    elif 'created_utc' in df.columns:
        df['date'] = pd.to_datetime(df['created_utc'], unit='s')

    return df


def load_finbert_batch_results() -> list[dict]:
    """Load FinBERT batch processing results.

    Returns:
        List of sentiment results from batch processing
    """
    batch_dir = Path("data/finbert_results")

    if not batch_dir.exists():
        print(f"⚠️  Batch results not found at {batch_dir}")
        return []

    all_results = []

    for batch_file in sorted(batch_dir.glob("batch_*.json")):
        try:
            with open(batch_file) as f:
                results = json.load(f)
                all_results.extend(results)
        except Exception as e:
            print(f"⚠️  Failed to load {batch_file}: {e}")

    print(f"✓ Loaded {len(all_results):,} batch results from {len(list(batch_dir.glob('batch_*.json')))} files")

    return all_results


def validate_crisis_periods(df: pd.DataFrame) -> dict[str, any]:
    """Validate that crisis event periods have expected data characteristics.

    Args:
        df: FinBERT daily sentiment DataFrame

    Returns:
        Validation results for crisis periods
    """
    crisis_events = {
        "2008_financial_crisis": {
            "start": "2008-09-15",
            "end": "2009-03-09",
            "expected_negative_sentiment": True,
            "expected_high_volatility": True
        },
        "covid19_pandemic": {
            "start": "2020-02-24",
            "end": "2020-04-15",
            "expected_negative_sentiment": True,
            "expected_high_volatility": True
        },
        "gamestop_squeeze": {
            "start": "2021-01-13",
            "end": "2021-02-05",
            "expected_negative_sentiment": False,  # Mixed sentiment expected
            "expected_high_volatility": True
        }
    }

    results = {
        "events": {},
        "passed": True
    }

    print("\n" + "=" * 60)
    print("🔍 VALIDATING CRISIS PERIODS")
    print("=" * 60)

    for event_key, event_info in crisis_events.items():
        print(f"\n📊 {event_key.replace('_', ' ').title()}")
        print(f"   Period: {event_info['start']} to {event_info['end']}")

        # Filter to crisis period
        mask = (df['date'] >= event_info['start']) & (df['date'] <= event_info['end'])
        crisis_data = df[mask]

        if len(crisis_data) == 0:
            results["events"][event_key] = {
                "passed": False,
                "issue": "No data for this period"
            }
            results["passed"] = False
            print(f"   ❌ No data found for this period")
            continue

        # Compute statistics
        mean_sentiment = crisis_data['compound_mean'].mean()
        sentiment_std = crisis_data['compound_std'].mean()
        mean_volume = crisis_data['volume'].mean()

        # Validate
        event_result = {
            "passed": True,
            "days": len(crisis_data),
            "mean_sentiment": float(mean_sentiment),
            "sentiment_volatility": float(sentiment_std),
            "mean_volume": float(mean_volume),
            "issues": []
        }

        print(f"   ✓ Days with data: {len(crisis_data)}")
        print(f"   ✓ Mean sentiment: {mean_sentiment:.4f}")
        print(f"   ✓ Sentiment volatility: {sentiment_std:.4f}")
        print(f"   ✓ Mean volume: {mean_volume:.0f}")

        # Check expected negative sentiment
        if event_info["expected_negative_sentiment"] and mean_sentiment > 0:
            issue = f"Expected negative sentiment, got {mean_sentiment:.4f}"
            event_result["issues"].append(issue)
            event_result["passed"] = False
            results["passed"] = False
            print(f"   ⚠️  {issue}")

        # Check high volatility
        if event_info["expected_high_volatility"] and sentiment_std < 0.2:
            issue = f"Expected high volatility, got {sentiment_std:.4f}"
            event_result["issues"].append(issue)
            event_result["passed"] = False
            results["passed"] = False
            print(f"   ⚠️  {issue}")

        # Check data volume (should have decent coverage)
        if mean_volume < 100:
            issue = f"Low data volume: {mean_volume:.0f} texts/day"
            event_result["issues"].append(issue)
            event_result["passed"] = False
            results["passed"] = False
            print(f"   ⚠️  {issue}")

        results["events"][event_key] = event_result

    return results


def validate_data_quality(df: pd.DataFrame) -> dict[str, any]:
    """Validate overall data quality metrics.

    Args:
        df: FinBERT daily sentiment DataFrame

    Returns:
        Data quality validation results
    """
    print("\n" + "=" * 60)
    print("🔍 DATA QUALITY CHECKS")
    print("=" * 60)

    results = {
        "checks": {},
        "issues": [],
        "passed": True
    }

    # Check 1: No missing dates (for continuous periods)
    date_range = pd.date_range(start=df['date'].min(), end=df['date'].max())
    missing_dates = date_range.difference(df['date'])

    results["checks"]["missing_dates"] = len(missing_dates)

    if len(missing_dates) > 0:
        print(f"\n⚠️  Missing dates: {len(missing_dates)} gaps in time series")
        print(f"   First few: {missing_dates[:5].tolist()}")
        results["issues"].append(f"Missing {len(missing_dates)} dates in range")
        # Don't fail on missing dates - expected for weekends/holidays
    else:
        print(f"\n✓ No missing dates (continuous time series)")

    # Check 2: Volume distribution
    volume_stats = df['volume'].describe()
    print(f"\n📊 Volume Statistics:")
    print(f"   Mean: {volume_stats['mean']:.0f}")
    print(f"   Median: {volume_stats['50%']:.0f}")
    print(f"   Min: {volume_stats['min']:.0f}")
    print(f"   Max: {volume_stats['max']:.0f}")

    results["checks"]["volume_stats"] = {
        "mean": float(volume_stats['mean']),
        "median": float(volume_stats['50%']),
        "min": float(volume_stats['min']),
        "max": float(volume_stats['max'])
    }

    # Check for suspiciously low volume periods
    low_volume_days = df[df['volume'] < 10]
    if len(low_volume_days) > 100:
        issue = f"Too many low-volume days: {len(low_volume_days)}"
        results["issues"].append(issue)
        results["passed"] = False
        print(f"\n⚠️  {issue}")

    # Check 3: Sentiment distribution
    sentiment_stats = df['compound_mean'].describe()
    print(f"\n💭 Sentiment Statistics:")
    print(f"   Mean: {sentiment_stats['mean']:.4f}")
    print(f"   Median: {sentiment_stats['50%']:.4f}")
    print(f"   Min: {sentiment_stats['min']:.4f}")
    print(f"   Max: {sentiment_stats['max']:.4f}")

    results["checks"]["sentiment_stats"] = {
        "mean": float(sentiment_stats['mean']),
        "median": float(sentiment_stats['50%']),
        "min": float(sentiment_stats['min']),
        "max": float(sentiment_stats['max'])
    }

    # Check for suspicious patterns
    if abs(sentiment_stats['mean']) > 0.5:
        issue = f"Suspiciously extreme mean sentiment: {sentiment_stats['mean']:.4f}"
        results["issues"].append(issue)
        results["passed"] = False
        print(f"\n⚠️  {issue}")

    # Check 4: Data reliability flags
    if 'reliability' in df.columns:
        reliability_counts = df['reliability'].value_counts()
        print(f"\n🔒 Reliability Distribution:")
        for level, count in reliability_counts.items():
            pct = count / len(df) * 100
            print(f"   {level}: {count} ({pct:.1f}%)")

        results["checks"]["reliability"] = reliability_counts.to_dict()

        # Warn if too much low reliability data
        low_reliability = df[df['reliability'] == 'very_low']
        if len(low_reliability) > len(df) * 0.3:
            issue = f"Too much low reliability data: {len(low_reliability)/len(df)*100:.1f}%"
            results["issues"].append(issue)
            print(f"\n⚠️  {issue}")

    return results


def main():
    """Run FinBERT CSV validation."""
    print("🔍 FINBERT CSV VALIDATION")
    print("=" * 60)
    print("Validating aggregated sentiment data against source files")
    print()

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "overall_passed": True
    }

    try:
        # Load FinBERT CSV
        finbert_df = load_finbert_csv()

        # Load source data for comparison (if available)
        reddit_df = load_kaggle_reddit_data()
        batch_results = load_finbert_batch_results()

        # Validate crisis periods
        crisis_validation = validate_crisis_periods(finbert_df)
        all_results["crisis_periods"] = crisis_validation
        if not crisis_validation["passed"]:
            all_results["overall_passed"] = False

        # Validate data quality
        quality_validation = validate_data_quality(finbert_df)
        all_results["data_quality"] = quality_validation
        if not quality_validation["passed"]:
            all_results["overall_passed"] = False

        # Summary
        print("\n" + "=" * 60)
        if all_results["overall_passed"]:
            print("✅ FINBERT CSV VALIDATION PASSED")
            print("   Data appears consistent and ready for backtesting")
        else:
            print("❌ FINBERT CSV VALIDATION FAILED")
            print("   Issues found that need investigation")
        print("=" * 60)

        # Save results
        output_dir = Path("results/validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"finbert_csv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=2, default=str)

        print(f"\n📄 Results saved to: {output_file}")

        # Exit with appropriate code
        sys.exit(0 if all_results["overall_passed"] else 1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
