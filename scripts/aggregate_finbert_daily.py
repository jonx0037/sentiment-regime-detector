#!/usr/bin/env python3
"""
Aggregate FinBERT HPC Results to Daily Sentiment CSV.

Reads the 30 batch_NNNN_sentiment.json files produced by FinBERT on ManeFrame III
and produces a clean daily-level CSV aligned to US equity trading days.

Fixes vs prior version:
  - Deduplicates records with identical content on the same date
  - Maps weekend/holiday posts to the next trading day
  - Adds per-label breakdown (pct_negative, pct_neutral) and reliability flag
  - Computes compound_std correctly across all records per trading day

Usage: python scripts/aggregate_finbert_daily.py
"""

import json
import hashlib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta
import sys


def content_hash(text: str, date: str) -> str:
    """Hash content+date so identical text on the same day is counted once."""
    key = f"{text.strip()}|{date}"
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def main():
    print("=" * 60)
    print("Aggregating FinBERT Results to Daily CSV")
    print("=" * 60)

    finbert_dir = Path("data/finbert_results")
    output_file = Path("data/finbert_daily_sentiment.csv")

    # Back up the old CSV if it exists
    if output_file.exists():
        backup = output_file.with_name("finbert_daily_sentiment_ORIGINAL.csv")
        if not backup.exists():
            import shutil
            shutil.copy2(output_file, backup)
            print(f"Backed up previous CSV -> {backup.name}")

    # --- Find HPC batch files ------------------------------------------------
    batch_files = sorted(
        finbert_dir.glob("batch_[0-9][0-9][0-9][0-9]_sentiment.json")
    )
    print(f"Found {len(batch_files)} HPC batch files")
    if not batch_files:
        print("ERROR: No batch files found in data/finbert_results/")
        sys.exit(1)

    # --- Phase 1: Load all records, deduplicate by content+date ---------------
    print("\nPhase 1  Loading & deduplicating records ...")
    rows = []
    total_raw = 0
    seen = set()
    dup_count = 0

    for i, bf in enumerate(batch_files):
        print(f"  {bf.name} ({i+1}/{len(batch_files)})", end=" ")
        with open(bf) as f:
            data = json.load(f)
        total_raw += len(data)
        batch_dup = 0

        for rec in data:
            sentiment = rec.get("sentiment")
            if not isinstance(sentiment, dict):
                continue

            date_str = rec.get("created_at", "")[:10]
            h = content_hash(rec.get("content", ""), date_str)
            if h in seen:
                batch_dup += 1
                dup_count += 1
                continue
            seen.add(h)

            rows.append(
                {
                    "date": date_str,
                    "compound": sentiment.get("compound", np.nan),
                    "label": sentiment.get("label", "unknown"),
                    "positive": sentiment.get("positive", 0.0),
                    "negative": sentiment.get("negative", 0.0),
                    "neutral": sentiment.get("neutral", 0.0),
                }
            )
        print(f"  {len(data):,} raw, {batch_dup} dupes")

    print(f"\n  Raw records : {total_raw:,}")
    print(f"  Duplicates  : {dup_count:,}")
    print(f"  Unique kept : {len(rows):,}")

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])

    # --- Phase 2: Map every date to a US trading day --------------------------
    print("\nPhase 2  Aligning to trading calendar ...")

    trading_days = pd.bdate_range(
        start=df["date"].min() - timedelta(days=7),
        end=df["date"].max() + timedelta(days=7),
        freq="B",
    )

    def to_trading_day(d):
        future = trading_days[trading_days >= d]
        return future[0] if len(future) else trading_days[-1]

    weekend_mask = df["date"].dt.dayofweek >= 5
    print(f"  Weekend records to remap: {weekend_mask.sum():,}")
    df["trading_date"] = df["date"].apply(to_trading_day)

    # --- Phase 3: Daily aggregation -------------------------------------------
    print("\nPhase 3  Daily aggregation ...")

    daily = (
        df.groupby("trading_date")
        .agg(
            compound_mean=("compound", "mean"),
            compound_std=("compound", "std"),
            compound_median=("compound", "median"),
            volume=("compound", "count"),
            pct_positive=("label", lambda x: (x == "positive").mean()),
            pct_negative=("label", lambda x: (x == "negative").mean()),
            pct_neutral=("label", lambda x: (x == "neutral").mean()),
            positive_mean=("positive", "mean"),
            negative_mean=("negative", "mean"),
            neutral_mean=("neutral", "mean"),
        )
        .reset_index()
        .rename(columns={"trading_date": "date"})
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Reliability flag  (useful for weighting / filtering in models)
    daily["reliability"] = pd.cut(
        daily["volume"],
        bins=[-1, 9, 29, 99, np.inf],
        labels=["very_low", "low", "medium", "high"],
    )

    # --- Phase 4: Save --------------------------------------------------------
    daily.to_csv(output_file, index=False)

    # --- Summary --------------------------------------------------------------
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Raw records processed  : {total_raw:,}")
    print(f"Duplicates removed     : {dup_count:,}")
    print(f"Unique records used    : {len(rows):,}")
    print(f"Trading days output    : {len(daily):,}")
    print(f"Date range             : {daily['date'].min().date()} to {daily['date'].max().date()}")
    print(f"Output file            : {output_file}")
    print(f"File size              : {output_file.stat().st_size / 1024:.1f} KB")
    print()
    print("Reliability breakdown:")
    print(daily["reliability"].value_counts().sort_index().to_string())
    print()
    print("Volume by year:")
    daily["year"] = daily["date"].dt.year
    print(
        daily.groupby("year")["volume"]
        .agg(["count", "sum", "mean", "median"])
        .rename(columns={"count": "days", "sum": "records", "mean": "avg_vol", "median": "med_vol"})
        .to_string()
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
