#!/usr/bin/env python3
"""
Post-HPC Processing: Fix taxonomy and produce clean daily CSV.

The HPC scorer groups data by folder-name keywords into flat categories.
This script corrects two issues:
  1. "news" and "social" are sources, not asset classes.
  2. "cross-asset" is a catch-all that includes misclassified datasets.

Parquet schema (from HPC):
  source:          dataset folder name (e.g., "wsb", "reddit-finance")
  asset_class:     inferred category (equities, crypto, forex, news, social, cross-asset)
  created_at:      date string
  text_content:    original text
  vader_score:     float
  textblob_score:  float
  finbert_score:   float
  roberta_score:   float
  distilbert_score: float
  ensemble_score:  float

Proper taxonomy after fix:
  asset_class: equities, crypto, forex, commodities, cross-asset
  data_source: news, social, market_data  (new column, replaces old misuse)
"""

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# ── Reclassification rules ──────────────────────────────────
# News datasets -> what asset class does their content primarily cover?
NEWS_ASSET_CLASS_MAP = {
    "apple_news_historical": "equities",
    "cnn_indonesia_economy_news": "cross-asset",
    "financial-news-nlp-2025": "cross-asset",
    "financial_news_2025_extended": "cross-asset",
    "high_quality_financial_news": "cross-asset",
    "russian_financial_news": "cross-asset",
    "sp500_news_2008_2024": "equities",
    "ticker_sentiment_news": "equities",
    "us_financial_news_comprehensive": "cross-asset",
    "news_cnbc_indonesia_2024_2025": "cross-asset",
    "news_sentiment_comprehensive": "cross-asset",
}

# Social datasets -> what asset class does their content primarily cover?
SOCIAL_ASSET_CLASS_MAP = {
    "reddit-finance": "cross-asset",
    "reddit-sentiment-2025": "cross-asset",
    "wsb": "equities",
    "wsb-2022": "equities",
    "wsb-echo-chamber": "equities",
    "wsb_2025_top10": "equities",
}

# Cross-asset catch-all reclassifications
CROSS_ASSET_RECLASSIFY = {
    "nasdaq_tech_2022_2024": "equities",
    "indices_financial_giants": "equities",
    "elon_tweets_2010_2025": "equities",  # about Tesla/SpaceX stocks
    "social-sentiment": "cross-asset",  # keep, general finance
}


def load_scored_parquets(scored_dir: str) -> pd.DataFrame:
    """Load all scored parquet files from partitioned directory."""
    frames = []
    scored_path = Path(scored_dir)

    for cat_dir in sorted(scored_path.iterdir()):
        if not cat_dir.is_dir() or not cat_dir.name.startswith("asset_class="):
            continue
        original_category = cat_dir.name.split("=", 1)[1]

        for pf in sorted(cat_dir.glob("*.parquet")):
            try:
                df = pd.read_parquet(pf)
                # Ensure asset_class column is populated from partition
                if "asset_class" not in df.columns:
                    df["asset_class"] = original_category
                frames.append(df)
                print(f"  Loaded {original_category}: {len(df):,} rows")
            except Exception as e:
                print(f"  ERROR loading {pf}: {e}")

    if not frames:
        print("ERROR: No parquet files found!")
        sys.exit(1)

    combined = pd.concat(frames, ignore_index=True)
    print(f"\nTotal loaded: {len(combined):,} rows")
    return combined


def fix_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix asset_class and add data_source column.

    The 'source' column in parquets = dataset folder name.
    The 'asset_class' column = original inferred category.

    Rules:
    1. Rows with asset_class="news" → data_source="news",
       asset_class reassigned by NEWS_ASSET_CLASS_MAP
    2. Rows with asset_class="social" → data_source="social",
       asset_class reassigned by SOCIAL_ASSET_CLASS_MAP
    3. Rows with asset_class="cross-asset" → check CROSS_ASSET_RECLASSIFY
    4. All others → keep asset_class, data_source="market_data"
    """
    df = df.copy()

    # Initialize data_source column
    df["data_source"] = "market_data"

    # --- Fix "news" rows ---
    news_mask = df["asset_class"] == "news"
    n_news = news_mask.sum()
    if n_news > 0:
        df.loc[news_mask, "data_source"] = "news"
        # Reassign asset_class based on dataset folder name
        df.loc[news_mask, "asset_class"] = (
            df.loc[news_mask, "source"].map(NEWS_ASSET_CLASS_MAP).fillna("cross-asset")
        )
        print(f"  Reclassified {n_news:,} 'news' rows → data_source='news'")

    # --- Fix "social" rows ---
    social_mask = df["asset_class"] == "social"
    n_social = social_mask.sum()
    if n_social > 0:
        df.loc[social_mask, "data_source"] = "social"
        df.loc[social_mask, "asset_class"] = (
            df.loc[social_mask, "source"]
            .map(SOCIAL_ASSET_CLASS_MAP)
            .fillna("cross-asset")
        )
        print(f"  Reclassified {n_social:,} 'social' rows → data_source='social'")

    # --- Fix some cross-asset misclassifications ---
    for dataset_name, correct_class in CROSS_ASSET_RECLASSIFY.items():
        mask = (df["asset_class"] == "cross-asset") & (df["source"] == dataset_name)
        if mask.any():
            df.loc[mask, "asset_class"] = correct_class
            print(f"  Reclassified {mask.sum():,} '{dataset_name}' → '{correct_class}'")

    return df


def parse_dates_robust(series: pd.Series) -> pd.Series:
    """
    Parse dates from mixed formats:
    - Unix timestamps (e.g., '1641018251')
    - DD/MM/YYYY (e.g., '16/07/2023')
    - ISO 8601 with TZ (e.g., '2020-06-05 10:30:54-04:00')
    - ISO 8601 with UTC (e.g., '2024-11-27T16:39:00+00:00')
    - Standard datetime (e.g., '2021-01-01 00:26:15')
    """
    result = pd.Series(pd.NaT, index=series.index)
    remaining = series.dropna()
    if remaining.empty:
        return result

    # 1. Try Unix timestamps (all digits, typically 10 digits for seconds)
    numeric_mask = remaining.str.match(r"^\d{9,13}$", na=False)
    if numeric_mask.any():
        unix_vals = remaining[numeric_mask].astype(float)
        # Values > 1e12 are milliseconds, convert to seconds
        unix_vals = unix_vals.where(unix_vals < 1e12, unix_vals / 1000)
        parsed = pd.to_datetime(unix_vals, unit="s", errors="coerce", utc=True)
        result.loc[parsed.index] = parsed.dt.tz_localize(None)
        remaining = remaining[~numeric_mask]
        print(f"    Unix timestamps: {numeric_mask.sum():,} parsed")

    if remaining.empty:
        return result

    # 2. Try DD/MM/YYYY format
    ddmmyyyy_mask = remaining.str.match(r"^\d{2}/\d{2}/\d{4}$", na=False)
    if ddmmyyyy_mask.any():
        parsed = pd.to_datetime(
            remaining[ddmmyyyy_mask], format="%d/%m/%Y", errors="coerce"
        )
        result.loc[parsed.index] = parsed
        remaining = remaining[~ddmmyyyy_mask]
        print(f"    DD/MM/YYYY: {ddmmyyyy_mask.sum():,} parsed")

    if remaining.empty:
        return result

    # 3. Try ISO 8601 / standard datetime with utc=True for mixed TZ
    try:
        parsed = pd.to_datetime(remaining, utc=True, errors="coerce")
        valid_mask = parsed.notna()
        if valid_mask.any():
            result.loc[parsed[valid_mask].index] = parsed[valid_mask].dt.tz_localize(
                None
            )
            n_parsed = valid_mask.sum()
            remaining = remaining[~valid_mask]
            print(f"    ISO/standard with UTC: {n_parsed:,} parsed")
    except Exception:
        pass

    if remaining.empty:
        return result

    # 4. Fallback: try without UTC
    try:
        parsed = pd.to_datetime(remaining, errors="coerce")
        valid_mask = parsed.notna()
        if valid_mask.any():
            result.loc[parsed[valid_mask].index] = parsed[valid_mask]
            print(f"    Fallback: {valid_mask.sum():,} parsed")
    except Exception:
        pass

    return result


def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate to daily with proper taxonomy dimensions."""
    # Parse dates with robust multi-format handler
    print("  Parsing dates (multi-format)...")
    df["date"] = parse_dates_robust(df["created_at"].astype(str))
    valid = df.dropna(subset=["date"]).copy()
    valid["date"] = valid["date"].dt.date
    print(
        f"  Rows with valid dates: {len(valid):,} / {len(df):,} ({100 * len(valid) / len(df):.1f}%)"
    )
    print(f"  Date range: {valid['date'].min()} → {valid['date'].max()}")

    daily_parts = []

    # --- Per asset class ---
    asset_classes = sorted(valid["asset_class"].unique())
    print(f"\n  Asset classes: {asset_classes}")
    for ac in asset_classes:
        ac_df = valid[valid["asset_class"] == ac]
        agg = ac_df.groupby("date")["ensemble_score"].agg(
            **{
                f"{ac}_ensemble_mean": "mean",
                f"{ac}_ensemble_std": "std",
                f"{ac}_count": "count",
            }
        )
        daily_parts.append(agg)
        print(
            f"    {ac}: {len(ac_df):,} rows → {len(agg):,} days, mean={ac_df['ensemble_score'].mean():.4f}"
        )

    # --- Per data source ---
    data_sources = sorted(valid["data_source"].unique())
    print(f"\n  Data sources: {data_sources}")
    for src in data_sources:
        src_df = valid[valid["data_source"] == src]
        agg = src_df.groupby("date")["ensemble_score"].agg(
            **{
                f"src_{src}_ensemble_mean": "mean",
                f"src_{src}_ensemble_std": "std",
                f"src_{src}_count": "count",
            }
        )
        daily_parts.append(agg)
        print(f"    {src}: {len(src_df):,} rows → {len(agg):,} days")

    # --- Overall ---
    overall = valid.groupby("date")["ensemble_score"].agg(
        overall_ensemble_mean="mean",
        overall_ensemble_std="std",
        overall_count="count",
    )
    daily_parts.append(overall)

    # --- Per-model overall means ---
    model_cols = [
        "vader_score",
        "textblob_score",
        "finbert_score",
        "roberta_score",
        "distilbert_score",
    ]
    for mc in model_cols:
        if mc in valid.columns:
            model_agg = valid.groupby("date")[mc].mean()
            model_agg.name = f"overall_{mc.replace('_score', '')}_mean"
            daily_parts.append(model_agg)

    # Merge
    daily = daily_parts[0]
    for part in daily_parts[1:]:
        daily = daily.join(part, how="outer")

    daily = daily.sort_index()
    daily.index.name = "date"
    return daily


def main():
    parser = argparse.ArgumentParser(
        description="Post-HPC taxonomy fix and daily aggregation"
    )
    parser.add_argument(
        "--scored-dir", required=True, help="Path to scored parquet dir"
    )
    parser.add_argument(
        "--output-csv",
        default="data/daily_sentiment_corrected.csv",
        help="Output daily CSV",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("POST-HPC PROCESSING: TAXONOMY FIX")
    print("=" * 60)

    print("\n[1/3] Loading scored parquets...")
    df = load_scored_parquets(args.scored_dir)

    print("\n[2/3] Fixing taxonomy...")
    df = fix_taxonomy(df)

    # Validation: no rows should have news/social as asset_class
    bad = df[df["asset_class"].isin(["news", "social"])]
    if len(bad) > 0:
        print(f"\n⚠️  WARNING: {len(bad)} rows still have news/social as asset_class!")
    else:
        print("\n  ✅ No rows have 'news' or 'social' as asset_class")

    print(f"\n  Asset class distribution:")
    for ac, cnt in df["asset_class"].value_counts().items():
        print(f"    {ac}: {cnt:,}")
    print(f"\n  Data source distribution:")
    for src, cnt in df["data_source"].value_counts().items():
        print(f"    {src}: {cnt:,}")

    print("\n[3/3] Aggregating to daily...")
    daily = aggregate_daily(df)

    print(f"\n{'=' * 60}")
    print(f"RESULTS")
    print(f"{'=' * 60}")
    print(f"Days: {len(daily):,}")
    print(f"Date range: {daily.index.min()} → {daily.index.max()}")
    print(f"Columns: {len(daily.columns)}")
    print(f"Column names: {list(daily.columns)}")

    if "overall_ensemble_mean" in daily.columns:
        print(f"\nOverall ensemble stats:")
        print(f"  Mean:  {daily['overall_ensemble_mean'].mean():.4f}")
        print(f"  Std:   {daily['overall_ensemble_mean'].std():.4f}")
        print(f"  Min:   {daily['overall_ensemble_mean'].min():.4f}")
        print(f"  Max:   {daily['overall_ensemble_mean'].max():.4f}")

    # Save
    os.makedirs(os.path.dirname(args.output_csv) or ".", exist_ok=True)
    daily.to_csv(args.output_csv)
    size_kb = os.path.getsize(args.output_csv) / 1024
    print(f"\nSaved: {args.output_csv} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
