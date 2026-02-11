#!/usr/bin/env python3
"""Quick audit of date coverage in scored parquet."""

import pandas as pd
import os

base = "/lustre/scratch/client/users/jarocha/sentiment-detector/results/sentiment_processed"

for asset_dir in sorted(os.listdir(base)):
    fp = os.path.join(base, asset_dir, "part-00000.parquet")
    if not os.path.exists(fp):
        continue
    df = pd.read_parquet(fp, columns=["source", "created_at"])
    asset = asset_dir.replace("asset_class=", "")
    print(f"\n{asset} ({len(df):,} total):")
    for src in sorted(df["source"].unique()):
        mask = df["source"] == src
        ca = df.loc[mask, "created_at"]
        has_date = ca.notna() & (ca.astype(str) != "nan") & (ca.astype(str) != "None")
        n_with = has_date.sum()
        n_total = mask.sum()
        pct = n_with / n_total * 100 if n_total > 0 else 0
        if n_with > 0:
            sample = str(ca[has_date].iloc[0])[:30]
        else:
            sample = "NO DATES"
        status = "OK" if pct > 90 else "PARTIAL" if pct > 0 else "MISSING"
        print(
            f"  [{status:7s}] {src}: {n_with:,}/{n_total:,} ({pct:.0f}%) sample='{sample}'"
        )
