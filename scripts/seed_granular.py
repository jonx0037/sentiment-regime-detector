#!/usr/bin/env python3
"""
Seed granular sentiment data (RawText + SentimentScore) for dashboard drill-down.
Seeds a recent window (default: last 30 days) of data to avoid overwhelming the DB.
"""

import argparse
import os
import sys
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def get_connection(database_url):
    """Get psycopg2 connection from URL."""
    url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    if "railway" in url and "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}sslmode=require"
    return psycopg2.connect(url)


def seed_granular_data(conn, parquet_dir, days=30, limit_per_day=100):
    """Seed granular data for the specified window."""
    print(f"\n--- Seeding granular data (last {days} days) ---")

    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    print(f"  Cutoff: {cutoff_date.date()}")

    # Iterate over parquet files
    for root, _, files in os.walk(parquet_dir):
        for file in files:
            if not file.endswith(".parquet"):
                continue

            path = os.path.join(root, file)
            # Infer asset class from path if possible, else default
            asset_class = "cross_asset"
            if "asset_class=" in path:
                try:
                    asset_class = path.split("asset_class=")[1].split("/")[0]
                except:
                    pass

            print(f"  Processing {asset_class} from {file}...")

            try:
                df = pd.read_parquet(path)

                # Convert created_at to datetime
                df["created_at"] = (
                    pd.to_datetime(df["created_at"], errors="coerce")
                    .dt.tz_localize(None)
                    .dt.tz_localize(timezone.utc)
                )

                # Filter by date
                df = df[df["created_at"] >= cutoff_date]

                if df.empty:
                    print(f"    No recent data found for {asset_class}")
                    continue

                # Sample if needed (to avoid huge inserts)
                if len(df) > limit_per_day * days:
                    df = df.sample(n=limit_per_day * days, random_state=42)
                    print(f"    Sampled down to {len(df)} rows")

                # Prepare rows for RawText
                raw_text_rows = []
                sentiment_score_rows = []
                now = datetime.now(timezone.utc)

                for _, row in df.iterrows():
                    text_id = str(uuid4())
                    source = row.get("source", "unknown")

                    # RawText row
                    raw_text_rows.append(
                        (
                            text_id,
                            source,
                            str(row.get("id", uuid4())),  # source_id
                            asset_class,
                            row["created_at"],
                            now,  # collected_at
                            None,  # title
                            row.get("text_content", "")[:5000],  # Trucate content
                            None,  # metadata
                            now,  # created_at
                            now,  # updated_at
                        )
                    )

                    # SentimentScore rows (one for each model if available)
                    # We synthesize probs since we only have scalar scores
                    models = ["finbert", "roberta", "distilbert", "vader", "textblob"]
                    for model in models:
                        score_col = f"{model}_score"
                        if score_col in row and pd.notna(row[score_col]):
                            score = float(row[score_col])

                            # Synthesize probabilities
                            pos = max(0, score) if score > 0 else 0
                            neg = max(0, -score) if score < 0 else 0
                            neu = 1.0 - (pos + neg)

                            sentiment_score_rows.append(
                                (
                                    str(uuid4()),
                                    text_id,
                                    model,
                                    "v1",  # version
                                    pos,
                                    neg,
                                    neu,
                                    score,  # compound
                                    max(pos, neg, neu),  # confidence
                                    now,  # processed_at
                                    now,  # created_at
                                    now,  # updated_at
                                )
                            )

                # Batch insert RawText
                with conn.cursor() as cur:
                    execute_values(
                        cur,
                        """INSERT INTO raw_texts
                           (id, source, source_id, asset_class, content_created_at, collected_at, 
                            title, content, metadata, created_at, updated_at)
                           VALUES %s
                           ON CONFLICT DO NOTHING""",
                        raw_text_rows,
                        page_size=1000,
                    )

                # Batch insert SentimentScore
                with conn.cursor() as cur:
                    execute_values(
                        cur,
                        """INSERT INTO sentiment_scores
                           (id, text_id, model_name, model_version, positive, negative, neutral,
                            compound, confidence, processed_at, created_at, updated_at)
                           VALUES %s
                           ON CONFLICT DO NOTHING""",
                        sentiment_score_rows,
                        page_size=1000,
                    )

                conn.commit()
                print(
                    f"    Inserted {len(raw_text_rows)} texts and {len(sentiment_score_rows)} scores"
                )

            except Exception as e:
                print(f"    Error processing {file}: {e}")
                conn.rollback()


def main():
    parser = argparse.ArgumentParser(description="Seed granular sentiment data")
    parser.add_argument("--database-url", default=os.environ.get("DATABASE_URL"))
    parser.add_argument(
        "--parquet-dir", default="results/sentiment_processed"
    )
    parser.add_argument("--days", type=int, default=30, help="Days of history to seed")
    parser.add_argument(
        "--limit", type=int, default=100, help="Max rows per day per file"
    )

    args = parser.parse_args()

    if not args.database_url:
        print("Error: --database-url required")
        sys.exit(1)

    print(f"Connecting to {args.database_url.split('@')[-1]}...")
    conn = get_connection(args.database_url)

    try:
        seed_granular_data(conn, args.parquet_dir, args.days, args.limit)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
