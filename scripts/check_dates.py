import pandas as pd
import os
import glob
from datetime import datetime

base_dir = "results/sentiment_processed/sentiment_processed"
classes = ["social", "news", "equities", "crypto", "cross-asset", "forex"]

print("Checking date ranges in HPC output...")
for c in classes:
    path = os.path.join(base_dir, f"asset_class={c}", "part-00000.parquet")
    if os.path.exists(path):
        try:
            # Only read the created_at column for speed
            df = pd.read_parquet(path, columns=["created_at"])
            df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
            min_date = df["created_at"].min()
            max_date = df["created_at"].max()
            print(f"{c.upper()}: {min_date} to {max_date} ({len(df)} rows)")

            # Additional check for recent data
            recent = df[df["created_at"] > "2024-01-01"]
            if not recent.empty:
                print(f"  --> FOUND RECENT DATA (2024+): {len(recent)} rows")
        except Exception as e:
            print(f"{c.upper()}: Error reading - {e}")
    else:
        print(f"{c.upper()}: File not found")
