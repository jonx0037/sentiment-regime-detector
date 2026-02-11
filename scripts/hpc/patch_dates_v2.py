#!/usr/bin/env python3
"""
Targeted patch for the 3 remaining dateless sources:
1. reddit-sentiment-2025 (42K rows) — join Post_ID to get Created dates
2. finsen_sentiment (13K rows) — read FinSen_US_Categorized_Timestamp.csv for Time
3. crypto_1000_realtime_2025 (7 rows) — market data, use last_updated
"""

import argparse
import os
import pandas as pd
import numpy as np


def patch_reddit_sentiment(data_dir, df, mask):
    """Join Post_ID from user_posts.csv to posts_df.csv to get Created dates."""
    src = os.path.join(data_dir, "reddit-sentiment-2025")
    posts_file = os.path.join(src, "posts_df.csv")

    if not os.path.exists(posts_file):
        print(f"  WARNING: {posts_file} not found")
        return 0

    posts = pd.read_csv(posts_file, usecols=["Post_ID", "Created"], low_memory=False)
    # Created is Unix epoch
    posts["Created"] = pd.to_datetime(posts["Created"], unit="s", errors="coerce")
    post_date_map = dict(zip(posts["Post_ID"].astype(str), posts["Created"]))
    print(f"  Loaded {len(post_date_map)} post IDs from posts_df.csv")

    # user_posts.csv has Post_ID column
    user_posts_file = os.path.join(src, "user_posts.csv")
    if os.path.exists(user_posts_file):
        up = pd.read_csv(
            user_posts_file, usecols=["Post_ID", "Title"], low_memory=False
        )
        # Title → Post_ID → Created
        title_date_map = {}
        for _, row in up.iterrows():
            pid = str(row["Post_ID"])
            title = str(row["Title"])[:5000]
            if pid in post_date_map and title and title != "nan":
                title_date_map[title] = str(post_date_map[pid])
        print(f"  Built {len(title_date_map)} title→date mappings from user_posts.csv")
    else:
        title_date_map = {}

    # Also try comments.csv — has Post_ID too
    comments_file = os.path.join(src, "comments.csv")
    if os.path.exists(comments_file):
        try:
            cm = pd.read_csv(comments_file, low_memory=False)
            if "Body" in cm.columns and "Post_ID" in cm.columns:
                for _, row in cm.iterrows():
                    pid = str(row.get("Post_ID", ""))
                    body = str(row.get("Body", ""))[:5000]
                    if pid in post_date_map and body and body != "nan":
                        title_date_map[body] = str(post_date_map[pid])
                print(f"  Added comment mappings, total: {len(title_date_map)}")
        except Exception as e:
            print(f"  WARNING reading comments: {e}")

    # Apply
    src_texts = df.loc[mask, "text_content"].astype(str).str[:5000]
    matched = src_texts.map(title_date_map)
    n_matched = matched.notna().sum()
    df.loc[mask, "created_at"] = matched
    return n_matched


def patch_finsen(data_dir, df, mask):
    """Use FinSen_US_Categorized_Timestamp.csv which has the Time column."""
    src = os.path.join(data_dir, "finsen_sentiment")
    ts_file = os.path.join(src, "FinSen_US_Categorized_Timestamp.csv")

    if not os.path.exists(ts_file):
        print(f"  WARNING: {ts_file} not found")
        return 0

    ts = pd.read_csv(ts_file, low_memory=False)
    if "Time" not in ts.columns or "Content" not in ts.columns:
        print(
            f"  WARNING: Expected Time and Content columns, got {ts.columns.tolist()}"
        )
        return 0

    # Parse dates: format is DD/MM/YYYY
    ts["parsed_date"] = pd.to_datetime(ts["Time"], format="%d/%m/%Y", errors="coerce")

    # Build title → date map (Title is more unique than Content for matching)
    content_date_map = {}
    for _, row in ts.iterrows():
        if pd.notna(row["parsed_date"]):
            # Try Title column (more unique)
            if "Title" in ts.columns:
                title = str(row["Title"])[:5000]
                if title and title != "nan":
                    content_date_map[title] = str(row["parsed_date"])
            content = str(row.get("Content", ""))[:5000]
            if content and content != "nan":
                content_date_map[content] = str(row["parsed_date"])

    print(f"  Built {len(content_date_map)} text→date mappings")

    # Match on text_content
    src_texts = df.loc[mask, "text_content"].astype(str).str[:5000]
    matched = src_texts.map(content_date_map)
    n_matched = matched.notna().sum()
    df.loc[mask, "created_at"] = matched
    return n_matched


def patch_crypto_realtime(data_dir, df, mask):
    """Use last_updated from crypto market data — minimal rows."""
    src = os.path.join(data_dir, "crypto_1000_realtime_2025")
    csv_file = os.path.join(src, "crypto_top1000_dataset.csv")

    if not os.path.exists(csv_file):
        return 0

    cr = pd.read_csv(csv_file, low_memory=False)
    if "last_updated" not in cr.columns or "name" not in cr.columns:
        return 0

    name_date_map = {}
    for _, row in cr.iterrows():
        name = str(row.get("name", ""))[:5000]
        lu = str(row.get("last_updated", ""))
        if name and name != "nan" and lu and lu != "nan":
            name_date_map[name] = lu

    src_texts = df.loc[mask, "text_content"].astype(str).str[:5000]
    matched = src_texts.map(name_date_map)
    n_matched = matched.notna().sum()
    df.loc[mask, "created_at"] = matched
    return n_matched


def main():
    parser = argparse.ArgumentParser(
        description="Targeted date patch for remaining sources"
    )
    parser.add_argument("--data-dir", required=True, help="Raw data directory")
    parser.add_argument("--parquet-dir", required=True, help="Scored parquet directory")
    args = parser.parse_args()

    # Sources to patch and their asset classes
    patches = {
        "social": {
            "reddit-sentiment-2025": patch_reddit_sentiment,
        },
        "cross-asset": {
            "finsen_sentiment": patch_finsen,
        },
        "crypto": {
            "crypto_1000_realtime_2025": patch_crypto_realtime,
        },
    }

    for asset_class, source_patches in patches.items():
        pf = os.path.join(
            args.parquet_dir, f"asset_class={asset_class}", "part-00000.parquet"
        )
        if not os.path.exists(pf):
            print(f"Parquet not found: {pf}")
            continue

        print(f"\n{'=' * 50}")
        print(f"Processing: {asset_class}")
        df = pd.read_parquet(pf)
        print(f"  Total rows: {len(df):,}")

        total_patched = 0
        for source_name, patch_fn in source_patches.items():
            src_mask = (df["source"] == source_name) & (
                df["created_at"].isna()
                | (df["created_at"].astype(str) == "None")
                | (df["created_at"].astype(str) == "nan")
            )
            n_missing = src_mask.sum()
            print(f"\n  {source_name}: {n_missing:,} missing dates")

            if n_missing == 0:
                print(f"  → Already patched!")
                continue

            n_patched = patch_fn(args.data_dir, df, src_mask)
            print(f"  → Patched {n_patched:,} / {n_missing:,}")
            total_patched += n_patched

        if total_patched > 0:
            df.to_parquet(pf, index=False)
            print(f"\n  Saved {pf} ({total_patched:,} dates patched)")
        else:
            print(f"\n  No new patches applied")

    print(f"\n{'=' * 50}")
    print("DONE")


if __name__ == "__main__":
    main()
