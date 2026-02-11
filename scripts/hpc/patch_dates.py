#!/usr/bin/env python3
"""
Patch missing dates in scored parquet files.

Reads original CSVs to extract dates for datasets where find_date_col()
failed (column names not in DATE_COL_NAMES), then updates the scored
parquet files in-place.

This avoids re-running the 9.5-hour scoring job.
"""

import argparse
import glob
import os
import pandas as pd
import numpy as np


# Map: source dataset name → (date column name in original CSV, text column name)
SOURCE_DATE_MAP = {
    "twitter_stocks_2015_2020": ("post_date", "body"),
    "reddit-finance": ("created", "title"),  # Unix epoch
    "reddit-sentiment-2025": ("Created", "Title"),
    "crypto": ("created", "title"),  # Unix epoch
    "forex": ("published_at", "text"),
    "finsen_sentiment": ("Time", "Content"),
    "crypto_1000_realtime_2025": (None, None),  # No fix available
}


def extract_dates_from_csv(data_dir, source_name, date_col, text_col):
    """
    Extract text → date mapping from original CSVs.
    Returns a dict: text_content[:5000] → date_string
    """
    src_dir = os.path.join(data_dir, source_name)
    if not os.path.isdir(src_dir):
        print(f"  WARNING: {src_dir} not found")
        return {}

    csv_files = glob.glob(os.path.join(src_dir, "*.csv"))
    if not csv_files:
        csv_files = glob.glob(os.path.join(src_dir, "**", "*.csv"), recursive=True)
    if not csv_files:
        print(f"  WARNING: No CSVs in {src_dir}")
        return {}

    all_dates = {}
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, low_memory=False)
            if text_col not in df.columns or date_col not in df.columns:
                continue

            # Check if date_col contains Unix epoch timestamps
            date_vals = df[date_col].dropna()
            if len(date_vals) > 0:
                sample = str(date_vals.iloc[0])
                try:
                    val = float(sample)
                    if val > 1e9:  # Unix epoch
                        dates = pd.to_datetime(df[date_col], unit="s", errors="coerce")
                    else:
                        dates = pd.to_datetime(df[date_col], errors="coerce", utc=True)
                except (ValueError, TypeError):
                    dates = pd.to_datetime(df[date_col], errors="coerce", utc=True)
            else:
                dates = pd.Series([pd.NaT] * len(df))

            # Strip timezone
            if dates.dt.tz is not None:
                dates = dates.dt.tz_localize(None)

            texts = df[text_col].astype(str).str[:5000]
            for text, date in zip(texts, dates):
                if pd.notna(date) and text and text != "nan":
                    all_dates[text] = str(date)

        except Exception as e:
            print(f"  WARNING: Error reading {csv_file}: {e}")

    return all_dates


def main():
    parser = argparse.ArgumentParser(description="Patch dates in scored parquet")
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Path to raw data directory (containing dataset subdirs)",
    )
    parser.add_argument(
        "--parquet-dir",
        required=True,
        help="Path to sentiment_processed output directory",
    )
    args = parser.parse_args()

    # Process each parquet file
    for root, dirs, files in os.walk(args.parquet_dir):
        for f in files:
            if not f.endswith(".parquet"):
                continue

            pf = os.path.join(root, f)
            asset_dir = os.path.basename(root)
            print(f"\n{'=' * 50}")
            print(f"Processing: {asset_dir}")

            df = pd.read_parquet(pf)
            print(f"  Total rows: {len(df):,}")

            # Find rows with missing dates
            has_date = df["created_at"].notna() & (
                df["created_at"].astype(str) != "None"
            )
            missing = ~has_date
            n_missing = missing.sum()
            print(f"  Missing dates: {n_missing:,}")

            if n_missing == 0:
                print(f"  → No patches needed")
                continue

            # Group by source and patch
            patched = 0
            for source in df[missing]["source"].unique():
                if source not in SOURCE_DATE_MAP:
                    print(f"  {source}: not in SOURCE_DATE_MAP, skipping")
                    continue

                date_col, text_col = SOURCE_DATE_MAP[source]
                if date_col is None:
                    print(f"  {source}: no date fix available, skipping")
                    continue

                print(f"  Extracting dates for {source}...")
                date_map = extract_dates_from_csv(
                    args.data_dir, source, date_col, text_col
                )
                print(f"    Found {len(date_map):,} text→date mappings")

                # Apply mappings
                src_mask = (df["source"] == source) & missing
                src_texts = df.loc[src_mask, "text_content"]
                matched = src_texts.map(date_map)
                n_matched = matched.notna().sum()
                df.loc[src_mask, "created_at"] = matched
                patched += n_matched
                print(f"    Patched {n_matched:,} / {src_mask.sum():,} rows")

            if patched > 0:
                df.to_parquet(pf, index=False)
                print(f"  Saved {pf} ({patched:,} dates patched)")
            else:
                print(f"  No patches applied")

    print(f"\n{'=' * 50}")
    print("DONE")


if __name__ == "__main__":
    main()
