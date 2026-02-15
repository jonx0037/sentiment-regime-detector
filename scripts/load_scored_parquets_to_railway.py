#!/usr/bin/env python3
"""
Fast scores-only loader: HPC parquets → Railway PostgreSQL via COPY.
Loads sentiment scores + minimal raw_texts metadata (no text content).
This is 10-50x faster than shipping full text over the network.
"""

import io
import os
import sys
import uuid as uuid_mod
from datetime import datetime, timezone

import psycopg2
import pyarrow.parquet as pq
import pandas as pd
import numpy as np

DATABASE_URL = os.environ.get("DATABASE_URL", "").replace(
    "postgresql+asyncpg://", "postgresql://"
)

PARQUET_BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "results",
    "sentiment_processed",
)


def get_parquet_files():
    files = []
    for ac_dir in sorted(os.listdir(PARQUET_BASE)):
        ac_path = os.path.join(PARQUET_BASE, ac_dir)
        if not os.path.isdir(ac_path):
            continue
        for fname in os.listdir(ac_path):
            if fname.endswith(".parquet"):
                ac = ac_dir.split("=")[1] if "=" in ac_dir else ac_dir
                files.append((ac, os.path.join(ac_path, fname)))
    return files


def gen_uuids(n):
    return [str(uuid_mod.uuid4()) for _ in range(n)]


def main():
    if not DATABASE_URL:
        print("❌ DATABASE_URL not set")
        sys.exit(1)

    parquet_files = get_parquet_files()
    total_rows = 0
    for ac, path in parquet_files:
        n = pq.ParquetFile(path).metadata.num_rows
        total_rows += n
        print(f"   {ac}: {n:,} rows")
    print(f"   TOTAL: {total_rows:,}\n")

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    print("🗑️  Clearing...")
    cur.execute("DELETE FROM sentiment_scores")
    print(f"   scores: {cur.rowcount:,}")
    cur.execute("DELETE FROM raw_texts")
    print(f"   texts: {cur.rowcount:,}")
    conn.commit()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S+00")
    loaded = 0
    CHUNK = 200000  # larger chunks since no text payload

    for ac, path in parquet_files:
        # Only read the columns we need (skip text_content for speed)
        pf = pq.ParquetFile(path)
        cols_to_read = ["source", "created_at", "ensemble_score"]
        available_cols = pf.schema_arrow.names
        cols_to_read = [c for c in cols_to_read if c in available_cols]
        df = pf.read(columns=cols_to_read).to_pandas()
        n = len(df)
        print(f"\n📤 {ac}: {n:,} rows")

        for start in range(0, n, CHUNK):
            chunk = df.iloc[start : start + CHUNK]
            cn = len(chunk)

            text_ids = gen_uuids(cn)
            score_ids = gen_uuids(cn)

            # --- raw_texts (minimal — no content) ---
            rt = pd.DataFrame()
            rt["id"] = text_ids
            rt["source"] = (
                chunk["source"].fillna(ac).astype(str).str[:50].values
                if "source" in chunk.columns
                else ac
            )
            rt["asset_class"] = ac[:20]

            # Dates
            if "created_at" in chunk.columns:
                dates = pd.to_datetime(chunk["created_at"], errors="coerce", utc=True)
                rt["content_created_at"] = (
                    dates.dt.strftime("%Y-%m-%d %H:%M:%S+00").fillna(now).values
                )
            else:
                rt["content_created_at"] = now

            rt["collected_at"] = now
            rt["content"] = ""
            rt["created_at"] = now
            rt["updated_at"] = now

            buf = io.StringIO()
            rt.to_csv(buf, index=False, header=False, quoting=1)
            buf.seek(0)
            cur.copy_expert(
                "COPY raw_texts (id, source, asset_class, content_created_at, collected_at, content, created_at, updated_at) FROM STDIN WITH (FORMAT csv)",
                buf,
            )

            # --- sentiment_scores ---
            ss = pd.DataFrame()
            ss["id"] = score_ids
            ss["text_id"] = text_ids
            ss["model_name"] = "ensemble"
            ss["model_version"] = "v1.0-5model"

            ens = (
                chunk["ensemble_score"].fillna(0.0).astype(float)
                if "ensemble_score" in chunk.columns
                else pd.Series(np.zeros(cn))
            )
            ss["positive"] = np.maximum(0, ens).values
            ss["negative"] = np.abs(np.minimum(0, ens)).values
            ss["neutral"] = np.maximum(0, 1.0 - ss["positive"] - ss["negative"]).values
            ss["compound"] = ens.values
            ss["confidence"] = 0.95
            ss["processed_at"] = now
            ss["created_at"] = now
            ss["updated_at"] = now

            buf2 = io.StringIO()
            ss.to_csv(buf2, index=False, header=False, quoting=1)
            buf2.seek(0)
            cur.copy_expert(
                "COPY sentiment_scores (id, text_id, model_name, model_version, positive, negative, neutral, compound, confidence, processed_at, created_at, updated_at) FROM STDIN WITH (FORMAT csv)",
                buf2,
            )

            conn.commit()
            loaded += cn
            pct = loaded * 100 // total_rows
            print(f"   {loaded:,} / {total_rows:,} ({pct}%)")

        print(f"   ✅ {ac}")

    # Also reload the sentiment_indices from the daily aggregates
    print("\n📤 Reloading sentiment_indices from daily_sentiment.csv...")
    daily_csv = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "results",
        "daily_sentiment.csv",
    )
    if os.path.exists(daily_csv):
        os.system(
            f'DATABASE_URL="{DATABASE_URL}" python3 {os.path.join(os.path.dirname(os.path.abspath(__file__)), "load_sentiment_to_railway.py")}'
        )
    else:
        print("   ⚠️ daily_sentiment.csv not found, skipping indices")

    # Verify
    print("\n📊 Final Verification:")
    cur.execute(
        "SELECT asset_class, COUNT(*) FROM raw_texts GROUP BY asset_class ORDER BY asset_class"
    )
    for r in cur.fetchall():
        print(f"   {r[0]}: {r[1]:,}")
    cur.execute("SELECT COUNT(*) FROM raw_texts")
    rt_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM sentiment_scores")
    sc_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM sentiment_indices")
    si_count = cur.fetchone()[0]
    print(f"\n✅ raw_texts: {rt_count:,}")
    print(f"✅ sentiment_scores: {sc_count:,}")
    print(f"✅ sentiment_indices: {si_count:,}")
    print("🎉 Done!")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
