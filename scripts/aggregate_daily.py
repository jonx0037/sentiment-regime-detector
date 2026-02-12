#!/usr/bin/env python3
"""
Aggregate per-text sentiment scores to daily time series per asset class.

Input:  Scored parquet files from score_sentiment.py
Output: CSV with daily sentiment per asset class, ready for regime detection pipeline.

Columns produced:
  - date: trading date
  - Per asset class: {asset}_ensemble_mean, {asset}_ensemble_std, {asset}_count
  - cross_asset_mean: mean of all asset ensemble scores
  - cross_asset_std: std across asset means (divergence signal)
  - compound: alias for cross_asset_mean (pipeline compatibility)
"""

import argparse
import os
import pandas as pd
import numpy as np


def load_scored_parquet(parquet_dir: str) -> pd.DataFrame:
    """Load all scored parquet files into a single DataFrame."""
    dfs = []
    for root, dirs, files in os.walk(parquet_dir):
        for f in files:
            if f.endswith(".parquet"):
                fp = os.path.join(root, f)
                # Extract asset class from directory name
                parent = os.path.basename(root)
                asset = (
                    parent.replace("asset_class=", "")
                    if "asset_class=" in parent
                    else "unknown"
                )
                df = pd.read_parquet(fp)
                df["asset_class"] = asset  # Override in case parquet doesn't have it
                dfs.append(df)
                print(f"  Loaded {asset}: {len(df):,} rows")

    if not dfs:
        raise ValueError(f"No parquet files found in {parquet_dir}")

    combined = pd.concat(dfs, ignore_index=True)
    print(
        f"\nTotal: {len(combined):,} rows across {combined['asset_class'].nunique()} asset classes"
    )
    return combined


def aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate per-text scores to daily granularity.

    For each day and asset class, compute:
    - Mean ensemble score
    - Std of ensemble scores
    - Count of texts
    - Individual model means
    """
    # Parse dates per-source — mixed formats (epochs, ISO, plain dates) fail
    # when parsed all at once. Per-source parsing lets each format resolve correctly.
    df["date"] = pd.NaT
    for src in df["source"].unique():
        mask = df["source"] == src
        ca = df.loc[mask, "created_at"]
        # Skip if all NaN
        first_valid = ca.first_valid_index()
        if first_valid is None:
            continue
        sample = str(ca.loc[first_valid])
        if sample in ("nan", "None", ""):
            continue
        # Detect Unix epoch timestamps (large numeric values)
        is_epoch = False
        try:
            val = float(sample)
            if val > 1e9:
                is_epoch = True
        except (ValueError, TypeError):
            pass
        if is_epoch:
            df.loc[mask, "date"] = pd.to_datetime(ca, errors="coerce", unit="s")
        else:
            parsed = pd.to_datetime(ca, errors="coerce", utc=True)
            if parsed.dt.tz is not None:
                parsed = parsed.dt.tz_localize(None)
            df.loc[mask, "date"] = parsed

    df["date"] = df["date"].dt.date
    df = df.dropna(subset=["date"])
    df["date"] = pd.to_datetime(df["date"])

    # Report per-asset date coverage
    print(f"\nDate coverage per asset class:")
    for asset in sorted(df["asset_class"].unique()):
        n = (df["asset_class"] == asset).sum()
        print(f"  {asset}: {n:,} rows with valid dates")

    print(f"\nDate range: {df['date'].min()} → {df['date'].max()}")
    print(f"Rows with valid dates: {len(df):,}")

    # Aggregate per asset class per day
    asset_classes = sorted(df["asset_class"].unique())
    print(f"Asset classes: {asset_classes}")

    # Build daily pivot: one row per day, columns for each asset class
    daily_dfs = []

    for asset in asset_classes:
        asset_df = df[df["asset_class"] == asset]
        safe = asset.replace("-", "_")

        daily = (
            asset_df.groupby("date")
            .agg(
                ensemble_mean=("ensemble_score", "mean"),
                ensemble_std=("ensemble_score", "std"),
                vader_mean=("vader_score", "mean"),
                finbert_mean=("finbert_score", "mean"),
                roberta_mean=("roberta_score", "mean"),
                textblob_mean=("textblob_score", "mean"),
                distilbert_mean=("distilbert_score", "mean"),
                count=("ensemble_score", "count"),
            )
            .rename(
                columns={
                    "ensemble_mean": f"{safe}_ensemble_mean",
                    "ensemble_std": f"{safe}_ensemble_std",
                    "vader_mean": f"{safe}_vader_mean",
                    "finbert_mean": f"{safe}_finbert_mean",
                    "roberta_mean": f"{safe}_roberta_mean",
                    "textblob_mean": f"{safe}_textblob_mean",
                    "distilbert_mean": f"{safe}_distilbert_mean",
                    "count": f"{safe}_count",
                }
            )
        )

        daily_dfs.append(daily)
        print(
            f"  {asset}: {len(daily)} days, "
            f"mean ensemble={asset_df['ensemble_score'].mean():.4f}"
        )

    # Merge all asset dailies on date
    result = daily_dfs[0]
    for ddf in daily_dfs[1:]:
        result = result.join(ddf, how="outer")

    # Cross-asset summary columns — only the 4 REAL asset classes
    # "news" and "social" are data sources, NOT asset classes (per Section 3.2)
    REAL_ASSET_CLASSES = ["equities", "crypto", "forex", "cross_asset"]
    ensemble_cols = [
        f"{ac}_ensemble_mean"
        for ac in REAL_ASSET_CLASSES
        if f"{ac}_ensemble_mean" in result.columns
    ]
    result["cross_asset_mean"] = result[ensemble_cols].mean(axis=1)
    result["cross_asset_std"] = result[ensemble_cols].std(axis=1)

    # Pipeline compatibility aliases
    result["compound"] = result["cross_asset_mean"]
    result["positive"] = result[ensemble_cols].clip(lower=0).mean(axis=1)
    result["negative"] = result[ensemble_cols].clip(upper=0).mean(axis=1)
    result["neutral"] = 1 - result["positive"].abs() - result["negative"].abs()

    # Total document count per day
    count_cols = [c for c in result.columns if c.endswith("_count")]
    result["total_count"] = result[count_cols].sum(axis=1)

    result = result.sort_index()
    result.index.name = "date"

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate scored parquet to daily CSV"
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Path to sentiment_processed parquet directory",
    )
    parser.add_argument(
        "--output-file", required=True, help="Path for output daily CSV"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("LOADING SCORED PARQUET")
    print("=" * 60)
    df = load_scored_parquet(args.input_dir)

    print("\n" + "=" * 60)
    print("AGGREGATING TO DAILY")
    print("=" * 60)
    daily = aggregate_daily(df)

    # Summary
    print(f"\n{'=' * 60}")
    print(f"DAILY AGGREGATION COMPLETE")
    print(f"{'=' * 60}")
    print(f"Days: {len(daily)}")
    print(f"Date range: {daily.index.min()} → {daily.index.max()}")
    print(f"Columns: {len(daily.columns)}")
    print(f"\nCross-asset ensemble stats:")
    print(f"  Mean:   {daily['cross_asset_mean'].mean():.4f}")
    print(f"  Std:    {daily['cross_asset_mean'].std():.4f}")
    print(f"  Min:    {daily['cross_asset_mean'].min():.4f}")
    print(f"  Max:    {daily['cross_asset_mean'].max():.4f}")
    print(f"\nSample (last 5 days):")
    print(daily[["cross_asset_mean", "cross_asset_std", "total_count"]].tail())

    # Write
    os.makedirs(os.path.dirname(args.output_file) or ".", exist_ok=True)
    daily.to_csv(args.output_file)
    print(
        f"\nSaved: {args.output_file} ({os.path.getsize(args.output_file) / 1024:.1f} KB)"
    )


if __name__ == "__main__":
    main()
