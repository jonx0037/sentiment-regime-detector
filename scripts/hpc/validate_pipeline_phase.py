#!/usr/bin/env python3
"""
Pipeline Validation Script
Validates data quality at each phase of the HPC pipeline

Usage:
    python validate_pipeline_phase.py --phase collection --path /work/jarocha/sentiment_regime_data/raw_data
    python validate_pipeline_phase.py --phase sentiment --path /work/jarocha/sentiment_regime_data/sentiment_results
    python validate_pipeline_phase.py --phase final --path data/finbert_daily_sentiment_v2.csv

Configuration:
    Edit the ValidationThresholds class below to set your quality standards.
    See inline comments for guidance on each threshold.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple
from scipy import stats
import sys


# ============================================================================
# VALIDATION THRESHOLDS
# TODO: Set these based on your data quality requirements
# ============================================================================

class ValidationThresholds:
    """
    Central configuration for all validation thresholds

    INSTRUCTIONS: Replace None with your chosen values based on the guidance below.
    Start with suggested defaults, then adjust based on your validation results.
    """

    # =========================================================================
    # Phase 1: Data Collection Quality Control
    # =========================================================================

    # Minimum texts per day for valid data point
    # Consider: Your goal is ~1250/day, but early years (2008) and weekends
    # will be lower. Balances quality with coverage.
    # Too high = missing data on quiet days | Too low = noisy sentiment estimates
    MIN_DAILY_VOLUME = 75

    # Maximum consecutive days with missing data
    # Consider: Gaps require interpolation and reduce model accuracy
    # One week is reasonable threshold for financial data
    # Too high = model sees stale data during gaps | Too low = excessive false alarms
    MAX_GAP_DAYS = 7

    # Maximum percentage of null/empty text values
    # Consider: Nulls indicate collection failures
    # 1% tolerance for edge cases
    # Too high = sentiment based on incomplete data | Too low = overly strict on edge cases
    MAX_NULL_TEXT_PCT = 0.01

    # Minimum characters for valid text
    # Consider: Very short texts ("yes", "ok", "lol") lack sentiment signal
    # 30 chars is roughly 5-6 words, minimum for meaningful content
    # Too high = excludes valid short headlines | Too low = noise from non-meaningful text
    MIN_TEXT_LENGTH = 30

    # =========================================================================
    # Source Distribution Balance
    # =========================================================================

    # Minimum percentage of texts from GDELT (news)
    # Consider: GDELT provides professional news perspective
    # 15% ensures news coverage without dominating
    # Too high = miss Reddit social sentiment | Too low = miss news-driven events
    EXPECTED_GDELT_MIN = 0.15

    # Maximum percentage of texts from GDELT (news)
    # Consider: Balance professional news vs social media
    # 35% keeps social sentiment as primary signal
    # Too high = underweight social sentiment | Too low = overweight social noise
    EXPECTED_GDELT_MAX = 0.35

    # =========================================================================
    # Phase 2: Sentiment Processing Quality Control
    # =========================================================================

    # Standard deviation threshold for model disagreement
    # Consider: When models strongly disagree, the sentiment signal is ambiguous
    # 0.5 means models differ by ~1 point on [-1, 1] scale on average
    # Too high = miss ambiguous sentiment | Too low = too many false alarms
    HIGH_DISAGREEMENT_STD = 0.5

    # Maximum percentage of days with high disagreement
    # Consider: Some disagreement is normal, but too much indicates processing issues
    # 10% allows for natural variation without masking systematic issues
    # Too high = accept low-quality sentiment | Too low = overly strict on natural variation
    MAX_HIGH_DISAGREEMENT_PCT = 0.10

    # Minimum texts/day after sentiment processing
    # Consider: Should match or be slightly lower than collection minimum
    # 50 is conservative to allow for some processing losses
    # Too high = lose data on quiet days | Too low = noisy sentiment estimates
    MIN_PROCESSED_VOLUME = 50

    # =========================================================================
    # Phase 3: Final Dataset Quality Control
    # =========================================================================

    # Minimum percentage of expected date range covered
    # Consider: 18 years = ~6575 days. 95% = ~330 missing days acceptable
    # Balances completeness with realistic API/data availability
    # Too high = difficult to achieve over 18 years | Too low = insufficient data for training
    MIN_COVERAGE_PCT = 0.95

    # Minimum coverage during crisis periods
    # Consider: Crisis periods are CRITICAL for your model
    # 90% is stricter than general coverage - crises need better data
    # Too high = might fail on unavoidable gaps | Too low = miss key crisis dynamics
    MIN_CRISIS_COVERAGE_PCT = 0.90

    # Minimum texts/day during crisis periods
    # Consider: Crises generate more news/discussion, need stronger signal
    # 150 is 2x normal minimum - crises should have elevated volume
    # Too high = miss early crisis days with lower volume | Too low = insufficient signal during critical periods
    MIN_CRISIS_VOLUME = 150

    # =========================================================================
    # Statistical Outlier Detection
    # =========================================================================

    # Z-score threshold for statistical outliers
    # Consider: Financial data has fat tails (extreme events happen often)
    # 3.5 is more conservative than standard 3.0, accounts for financial extremes
    # Too high = miss data quality issues | Too low = flag legitimate extreme events as errors
    OUTLIER_Z_SCORE = 3.5

    # Maximum percentage of outliers acceptable
    # Consider: Some outliers are real (crashes, squeezes), not errors
    # 1% = ~66 days over 18 years allows for major events
    # Too high = accept too many anomalies | Too low = flag real extreme events
    MAX_OUTLIER_PCT = 0.01

    # =========================================================================
    # Expected Sentiment Distributions (Informational checks, not hard limits)
    # =========================================================================

    # Expected mean for FinBERT (financial domain)
    # Consider: Financial news tends slightly negative (risk focus)
    # -0.05 reflects typical financial news pessimism bias
    # Historical financial sentiment is often pessimistic
    EXPECTED_FINBERT_MEAN = -0.05

    # Expected mean for VADER (general domain)
    # Consider: VADER is more neutral on average
    # 0.05 reflects slight positive bias in general text
    # General text tends slightly positive
    EXPECTED_VADER_MEAN = 0.05


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_collection_batch(batch_file: Path, thresholds: ValidationThresholds) -> List[str]:
    """
    Validate a single collected quarter batch

    Args:
        batch_file: Path to parquet file
        thresholds: Validation threshold configuration

    Returns:
        List of validation issues (empty if all checks pass)
    """
    print(f"\n{'='*70}")
    print(f"Validating Collection Batch: {batch_file.name}")
    print(f"{'='*70}")

    df = pd.read_parquet(batch_file)
    issues = []

    # 1. Volume checks
    print(f"\n📊 Volume Analysis:")
    daily_counts = df.groupby('date').size()
    print(f"   Total texts: {len(df):,}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Days: {len(daily_counts)}")
    print(f"   Mean daily volume: {daily_counts.mean():.0f}")
    print(f"   Median daily volume: {daily_counts.median():.0f}")

    if thresholds.MIN_DAILY_VOLUME:
        low_volume_days = daily_counts[daily_counts < thresholds.MIN_DAILY_VOLUME]
        if len(low_volume_days) > 0:
            issues.append(
                f"⚠️  {len(low_volume_days)} days below {thresholds.MIN_DAILY_VOLUME} texts"
            )
            print(f"   ❌ {len(low_volume_days)} days below minimum volume")
        else:
            print(f"   ✅ All days meet minimum volume requirement")

    # 2. Date continuity
    print(f"\n📅 Date Continuity:")
    date_range = pd.date_range(df['date'].min(), df['date'].max())
    missing_dates = set(date_range) - set(df['date'].unique())
    print(f"   Expected days: {len(date_range)}")
    print(f"   Actual days: {len(df['date'].unique())}")
    print(f"   Missing days: {len(missing_dates)}")

    if thresholds.MAX_GAP_DAYS and len(missing_dates) > thresholds.MAX_GAP_DAYS:
        issues.append(f"⚠️  {len(missing_dates)} missing dates (exceeds threshold)")
        print(f"   ❌ Too many missing dates")
    elif len(missing_dates) > 0:
        print(f"   ⚠️  Some dates missing but within threshold")
    else:
        print(f"   ✅ Complete date coverage")

    # 3. Content quality
    print(f"\n📝 Content Quality:")
    null_text_count = df['text'].isna().sum()
    null_text_pct = null_text_count / len(df)
    print(f"   Null texts: {null_text_count:,} ({null_text_pct:.2%})")

    if thresholds.MAX_NULL_TEXT_PCT and null_text_pct > thresholds.MAX_NULL_TEXT_PCT:
        issues.append(f"⚠️  {null_text_pct:.1%} null text values")
        print(f"   ❌ Null text percentage exceeds threshold")
    else:
        print(f"   ✅ Null text within acceptable range")

    # 4. Text length distribution
    print(f"\n📏 Text Length Analysis:")
    df['text_length'] = df['text'].str.len()
    print(f"   Mean length: {df['text_length'].mean():.0f} chars")
    print(f"   Median length: {df['text_length'].median():.0f} chars")
    print(f"   Min length: {df['text_length'].min():.0f} chars")
    print(f"   Max length: {df['text_length'].max():.0f} chars")

    if thresholds.MIN_TEXT_LENGTH:
        short_texts = (df['text_length'] < thresholds.MIN_TEXT_LENGTH).sum()
        short_pct = short_texts / len(df)
        print(f"   Texts < {thresholds.MIN_TEXT_LENGTH} chars: {short_texts:,} ({short_pct:.2%})")

        if short_pct > 0.05:  # >5% too short
            issues.append(f"⚠️  {short_texts:,} texts below {thresholds.MIN_TEXT_LENGTH} chars ({short_pct:.1%})")
            print(f"   ❌ Too many short texts")
        else:
            print(f"   ✅ Text lengths acceptable")

    # 5. Source balance
    print(f"\n🔄 Source Distribution:")
    source_dist = df['source'].value_counts()
    source_pct = df['source'].value_counts(normalize=True)

    for source in source_dist.index:
        print(f"   {source}: {source_dist[source]:,} ({source_pct[source]:.1%})")

    if 'GDELT' in source_pct.index:
        gdelt_pct = source_pct['GDELT']
        if thresholds.EXPECTED_GDELT_MIN and thresholds.EXPECTED_GDELT_MAX:
            if gdelt_pct < thresholds.EXPECTED_GDELT_MIN or gdelt_pct > thresholds.EXPECTED_GDELT_MAX:
                issues.append(
                    f"⚠️  GDELT distribution {gdelt_pct:.1%} outside expected range "
                    f"[{thresholds.EXPECTED_GDELT_MIN:.1%}, {thresholds.EXPECTED_GDELT_MAX:.1%}]"
                )
                print(f"   ❌ Source balance outside expected range")
            else:
                print(f"   ✅ Source balance within expected range")

    # Summary
    print(f"\n{'='*70}")
    if issues:
        print(f"❌ VALIDATION FAILED - {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print(f"✅ VALIDATION PASSED - All checks successful")
    print(f"{'='*70}")

    return issues


def validate_sentiment_batch(batch_file: Path, thresholds: ValidationThresholds) -> List[str]:
    """
    Validate daily sentiment aggregates

    Args:
        batch_file: Path to CSV file with daily sentiment
        thresholds: Validation threshold configuration

    Returns:
        List of validation issues (empty if all checks pass)
    """
    print(f"\n{'='*70}")
    print(f"Validating Sentiment Batch: {batch_file.name}")
    print(f"{'='*70}")

    df = pd.read_csv(batch_file, parse_dates=['date'] if 'date' in pd.read_csv(batch_file, nrows=0).columns else None)
    issues = []

    # 1. Sentiment range checks
    print(f"\n🎯 Sentiment Value Ranges:")
    sentiment_models = ['finbert', 'vader', 'textblob', 'distilbert', 'llama3']

    for model in sentiment_models:
        col = f'{model}_sentiment'
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()
            mean_val = df[col].mean()

            print(f"   {model}: [{min_val:.3f}, {max_val:.3f}], μ={mean_val:.3f}")

            out_of_range = ((df[col] < -1) | (df[col] > 1)).sum()
            if out_of_range > 0:
                issues.append(f"⚠️  {model}: {out_of_range} values out of range [-1, 1]")
                print(f"      ❌ {out_of_range} values out of range")
            else:
                print(f"      ✅ All values in valid range")

    # 2. Model agreement check
    print(f"\n🤝 Model Agreement Analysis:")
    sentiment_cols = [c for c in df.columns if '_sentiment' in c and c != 'ensemble_sentiment']

    if len(sentiment_cols) >= 2:
        df['sentiment_std'] = df[sentiment_cols].std(axis=1)
        print(f"   Mean std dev across models: {df['sentiment_std'].mean():.3f}")
        print(f"   Max std dev: {df['sentiment_std'].max():.3f}")

        if thresholds.HIGH_DISAGREEMENT_STD:
            high_disagreement = (df['sentiment_std'] > thresholds.HIGH_DISAGREEMENT_STD).sum()
            high_disagreement_pct = high_disagreement / len(df)
            print(f"   Days with high disagreement (std > {thresholds.HIGH_DISAGREEMENT_STD}): "
                  f"{high_disagreement} ({high_disagreement_pct:.1%})")

            if (thresholds.MAX_HIGH_DISAGREEMENT_PCT and
                    high_disagreement_pct > thresholds.MAX_HIGH_DISAGREEMENT_PCT):
                issues.append(
                    f"⚠️  {high_disagreement} days ({high_disagreement_pct:.1%}) with high model disagreement "
                    f"(std > {thresholds.HIGH_DISAGREEMENT_STD})"
                )
                print(f"   ❌ Too many days with high disagreement")
            else:
                print(f"   ✅ Model agreement within acceptable range")

    # 3. Volume consistency
    print(f"\n📊 Volume Analysis:")
    if 'volume' in df.columns:
        print(f"   Mean volume: {df['volume'].mean():.0f}")
        print(f"   Median volume: {df['volume'].median():.0f}")
        print(f"   Min volume: {df['volume'].min():.0f}")
        print(f"   Max volume: {df['volume'].max():.0f}")

        if thresholds.MIN_PROCESSED_VOLUME:
            low_volume = (df['volume'] < thresholds.MIN_PROCESSED_VOLUME).sum()
            if low_volume > 0:
                issues.append(f"⚠️  {low_volume} days with volume < {thresholds.MIN_PROCESSED_VOLUME}")
                print(f"   ❌ {low_volume} days below minimum volume")
            else:
                print(f"   ✅ All days meet minimum volume requirement")

    # Summary
    print(f"\n{'='*70}")
    if issues:
        print(f"❌ VALIDATION FAILED - {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print(f"✅ VALIDATION PASSED - All checks successful")
    print(f"{'='*70}")

    return issues


def validate_final_dataset(csv_path: Path, thresholds: ValidationThresholds) -> Tuple[pd.DataFrame, List[str]]:
    """
    Comprehensive validation of aggregated final dataset

    Args:
        csv_path: Path to final CSV file
        thresholds: Validation threshold configuration

    Returns:
        Tuple of (dataframe, list of validation issues)
    """
    print(f"\n{'='*70}")
    print(f"COMPREHENSIVE FINAL DATASET VALIDATION")
    print(f"{'='*70}")

    df = pd.read_csv(csv_path, parse_dates=['date'])
    issues = []

    # 1. Coverage validation
    print(f"\n📅 Date Coverage:")
    expected_start = "2008-01-01"
    expected_end = "2026-02-06"
    date_range = pd.date_range(expected_start, expected_end)
    coverage_pct = len(df) / len(date_range)

    print(f"   Expected: {len(date_range):,} days ({expected_start} to {expected_end})")
    print(f"   Actual: {len(df):,} days")
    print(f"   Coverage: {coverage_pct:.1%}")

    if thresholds.MIN_COVERAGE_PCT and coverage_pct < thresholds.MIN_COVERAGE_PCT:
        issues.append(f"⚠️  Coverage {coverage_pct:.1%} below minimum {thresholds.MIN_COVERAGE_PCT:.1%}")
        print(f"   ❌ FAIL: Coverage below threshold")
    else:
        print(f"   ✅ PASS: Coverage meets requirements")

    # 2. Crisis period validation
    crisis_periods = {
        "2008 Financial Crisis": ("2008-09-15", "2009-03-09"),
        "COVID-19 Pandemic": ("2020-02-24", "2020-04-15"),
        "GameStop Squeeze": ("2021-01-13", "2021-02-05")
    }

    print(f"\n🚨 Crisis Period Coverage:")
    for name, (start, end) in crisis_periods.items():
        period_df = df[(df['date'] >= start) & (df['date'] <= end)]
        expected_days = len(pd.date_range(start, end))
        crisis_coverage = len(period_df) / expected_days
        avg_volume = period_df['volume'].mean() if 'volume' in period_df.columns else 0

        print(f"   {name}:")
        print(f"      Days: {len(period_df)}/{expected_days} ({crisis_coverage:.1%})")
        print(f"      Avg volume: {avg_volume:.0f} texts/day")

        crisis_issues = []
        if thresholds.MIN_CRISIS_COVERAGE_PCT and crisis_coverage < thresholds.MIN_CRISIS_COVERAGE_PCT:
            crisis_issues.append(f"coverage {crisis_coverage:.1%}")

        if thresholds.MIN_CRISIS_VOLUME and avg_volume < thresholds.MIN_CRISIS_VOLUME:
            crisis_issues.append(f"volume {avg_volume:.0f}")

        if crisis_issues:
            issue_str = f"⚠️  {name}: insufficient {', '.join(crisis_issues)}"
            issues.append(issue_str)
            print(f"      ❌ FAIL: {', '.join(crisis_issues)}")
        else:
            print(f"      ✅ PASS")

    # 3. Statistical distribution checks
    print(f"\n📊 Statistical Properties:")

    sentiment_cols = [c for c in df.columns if '_sentiment' in c and c != 'ensemble_sentiment']
    for col in sentiment_cols:
        mean_sent = df[col].mean()
        std_sent = df[col].std()
        median_sent = df[col].median()

        print(f"   {col}:")
        print(f"      μ={mean_sent:.3f}, σ={std_sent:.3f}, median={median_sent:.3f}")

        # Check expected ranges (if configured)
        if col == 'finbert_sentiment' and thresholds.EXPECTED_FINBERT_MEAN:
            if not (-0.2 <= mean_sent <= 0.1):  # Reasonable range for financial sentiment
                issues.append(f"⚠️  FinBERT mean {mean_sent:.3f} outside expected range")

        if col == 'vader_sentiment' and thresholds.EXPECTED_VADER_MEAN:
            if not (-0.2 <= mean_sent <= 0.2):  # VADER tends more neutral
                issues.append(f"⚠️  VADER mean {mean_sent:.3f} outside expected range")

    # Volume distribution
    if 'volume' in df.columns:
        print(f"\n   Volume statistics:")
        print(f"      Mean: {df['volume'].mean():.0f}")
        print(f"      Median: {df['volume'].median():.0f}")
        print(f"      Std: {df['volume'].std():.0f}")
        print(f"      Min: {df['volume'].min():.0f}")
        print(f"      Max: {df['volume'].max():.0f}")

    # 4. Outlier detection
    print(f"\n🔍 Outlier Detection:")

    if thresholds.OUTLIER_Z_SCORE:
        for col in sentiment_cols:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            outliers = (z_scores > thresholds.OUTLIER_Z_SCORE).sum()
            outlier_pct = outliers / len(df)

            print(f"   {col}: {outliers} outliers ({outlier_pct:.2%}) with |z| > {thresholds.OUTLIER_Z_SCORE}")

            if thresholds.MAX_OUTLIER_PCT and outlier_pct > thresholds.MAX_OUTLIER_PCT:
                issues.append(f"⚠️  {col}: {outlier_pct:.2%} outliers exceeds threshold")

    # Summary
    print(f"\n{'='*70}")
    if issues:
        print(f"❌ VALIDATION FAILED - {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"   {issue}")
        print(f"\n⚠️  Review issues before proceeding to backtesting")
    else:
        print(f"✅ VALIDATION PASSED - Dataset ready for backtesting")
    print(f"{'='*70}")

    return df, issues


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Validate HPC pipeline phases")
    parser.add_argument(
        "--phase",
        choices=['collection', 'sentiment', 'final'],
        required=True,
        help="Pipeline phase to validate"
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to data directory or file"
    )
    parser.add_argument(
        "--output",
        help="Path to save validation report (optional)"
    )

    args = parser.parse_args()

    # Initialize thresholds
    thresholds = ValidationThresholds()

    # Validate thresholds are configured
    if args.phase == 'collection' and thresholds.MIN_DAILY_VOLUME is None:
        print("⚠️  WARNING: Validation thresholds not configured!")
        print("   Please set thresholds in ValidationThresholds class")
        print("   Some validation checks will be skipped")
        print()

    # Run appropriate validation
    all_issues = []

    if args.phase == 'collection':
        path = Path(args.path)
        if path.is_dir():
            # Validate all parquet files in directory
            parquet_files = sorted(path.glob("*.parquet"))
            print(f"Found {len(parquet_files)} batch files to validate\n")

            for batch_file in parquet_files:
                issues = validate_collection_batch(batch_file, thresholds)
                all_issues.extend(issues)

        else:
            # Validate single file
            issues = validate_collection_batch(path, thresholds)
            all_issues.extend(issues)

    elif args.phase == 'sentiment':
        path = Path(args.path)
        if path.is_dir():
            # Validate all CSV files in directory
            csv_files = sorted(path.glob("daily_batch_*.csv"))
            print(f"Found {len(csv_files)} batch files to validate\n")

            for batch_file in csv_files:
                issues = validate_sentiment_batch(batch_file, thresholds)
                all_issues.extend(issues)

        else:
            # Validate single file
            issues = validate_sentiment_batch(path, thresholds)
            all_issues.extend(issues)

    elif args.phase == 'final':
        path = Path(args.path)
        df, issues = validate_final_dataset(path, thresholds)
        all_issues.extend(issues)

    # Final summary
    print(f"\n{'='*70}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"Phase: {args.phase}")
    print(f"Total issues found: {len(all_issues)}")

    if all_issues:
        print(f"\n❌ VALIDATION FAILED")
        sys.exit(1)
    else:
        print(f"\n✅ VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
