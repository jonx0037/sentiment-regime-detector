#!/usr/bin/env python3
"""
Seed Railway PostgreSQL with pipeline results.

Seeds three tables:
1. sentiment_indices — daily sentiment per asset class
2. stress_indices — ECB CISS daily values
3. market_data — VIX daily (symbol='^VIX')

Usage:
    python scripts/seed_dashboard.py --database-url postgresql://...
    # or
    DATABASE_URL=postgresql://... python scripts/seed_dashboard.py
"""

import argparse
import os
import sys
from datetime import datetime, timezone
from uuid import uuid4

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def get_connection(database_url):
    """Get psycopg2 connection from URL."""
    # Convert asyncpg URL to psycopg2 if needed
    url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    return psycopg2.connect(url)


def seed_sentiment_indices(conn, sentiment_path, feature_matrix_path):
    """Seed sentiment_indices table with daily sentiment per asset class."""
    print("\n--- Seeding sentiment_indices ---")

    sent = pd.read_csv(sentiment_path, parse_dates=["date"], index_col="date")
    sent = sent[sent.index >= "2005-01-01"]

    # If we have the feature matrix, use its precomputed momentum
    features = None
    if os.path.exists(feature_matrix_path):
        features = pd.read_csv(
            feature_matrix_path, parse_dates=["date"], index_col="date"
        )

    # Asset class mapping from daily_sentiment.csv columns
    asset_classes = {
        "crypto": "crypto",
        "equities": "equity",
        "forex": "forex",
        "news": "news",
        "social": "social",
        "cross_asset": "cross_asset",
    }

    rows = []
    for idx, row_data in sent.iterrows():
        for csv_prefix, db_name in asset_classes.items():
            mean_col = f"{csv_prefix}_ensemble_mean"
            std_col = f"{csv_prefix}_ensemble_std"
            count_col = f"{csv_prefix}_count"

            if mean_col not in sent.columns:
                continue

            mean_val = row_data.get(mean_col)
            if pd.isna(mean_val):
                continue

            std_val = row_data.get(std_col, None)
            count_val = row_data.get(count_col, 1)

            # Derive positive/negative ratio from sign of compound
            pos_ratio = max(0, float(mean_val)) if not pd.isna(mean_val) else None
            neg_ratio = max(0, -float(mean_val)) if not pd.isna(mean_val) else None

            momentum = None
            if features is not None and "sent_momentum" in features.columns:
                if idx in features.index:
                    momentum = features.loc[idx, "sent_momentum"]
                    if pd.isna(momentum):
                        momentum = None

            rows.append(
                (
                    str(uuid4()),
                    db_name,
                    None,  # source = NULL for aggregated
                    idx.to_pydatetime().replace(tzinfo=timezone.utc),
                    (idx + pd.Timedelta(days=1))
                    .to_pydatetime()
                    .replace(tzinfo=timezone.utc),
                    "daily",
                    float(mean_val),
                    float(std_val)
                    if std_val is not None and not pd.isna(std_val)
                    else None,
                    int(count_val) if not pd.isna(count_val) else 1,
                    pos_ratio,
                    neg_ratio,
                    float(momentum) if momentum is not None else None,
                    None,  # sentiment_acceleration
                )
            )

    print(f"  Prepared {len(rows)} sentiment index rows")

    with conn.cursor() as cur:
        # Clear existing data
        cur.execute("DELETE FROM sentiment_indices")
        print("  Cleared existing sentiment_indices")

        execute_values(
            cur,
            """INSERT INTO sentiment_indices
               (id, asset_class, source, period_start, period_end, granularity,
                mean_compound, std_compound, sample_count,
                positive_ratio, negative_ratio,
                sentiment_momentum, sentiment_acceleration)
               VALUES %s
               ON CONFLICT DO NOTHING""",
            rows,
            page_size=1000,
        )
        conn.commit()
        print(f"  Inserted {len(rows)} rows into sentiment_indices")


def seed_stress_indices(conn, ciss_path):
    """Seed stress_indices table with ECB CISS data."""
    print("\n--- Seeding stress_indices ---")

    df = pd.read_csv(ciss_path)
    date_col = [c for c in df.columns if "DATE" in c.upper()][0]
    val_col = [c for c in df.columns if "CISS" in c.upper() or "IDX" in c.upper()][0]

    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["ciss"] = pd.to_numeric(df[val_col], errors="coerce")
    df = df.dropna(subset=["date", "ciss"])

    rows = []
    for _, row_data in df.iterrows():
        rows.append(
            (
                str(uuid4()),
                "ecb_ciss",
                row_data["date"].date(),
                "ea",
                float(row_data["ciss"]),
                "daily",
            )
        )

    print(f"  Prepared {len(rows)} CISS rows")

    with conn.cursor() as cur:
        cur.execute("DELETE FROM stress_indices WHERE source = 'ecb_ciss'")
        print("  Cleared existing ECB CISS data")

        execute_values(
            cur,
            """INSERT INTO stress_indices
               (id, source, date, region, value, frequency)
               VALUES %s
               ON CONFLICT DO NOTHING""",
            rows,
            page_size=1000,
        )
        conn.commit()
        print(f"  Inserted {len(rows)} rows into stress_indices")


def seed_market_data(conn, vix_path):
    """Seed market_data table with VIX data."""
    print("\n--- Seeding market_data (VIX) ---")

    df = pd.read_csv(vix_path, parse_dates=["date"], index_col="date")
    df.columns = [c.lower() for c in df.columns]
    df = df.dropna(subset=["close"])

    # Compute daily returns
    df["daily_return"] = df["close"].pct_change()

    rows = []
    for date, row_data in df.iterrows():
        rows.append(
            (
                str(uuid4()),
                "^VIX",
                "index",
                None,  # exchange
                "us",  # region
                date.date(),
                float(row_data["open"])
                if "open" in row_data and not pd.isna(row_data["open"])
                else None,
                float(row_data["high"])
                if "high" in row_data and not pd.isna(row_data["high"])
                else None,
                float(row_data["low"])
                if "low" in row_data and not pd.isna(row_data["low"])
                else None,
                float(row_data["close"]),
                None,  # adj_close
                None,  # volume
                float(row_data["daily_return"])
                if not pd.isna(row_data.get("daily_return"))
                else None,
                None,  # volatility
                "vix_kaggle",
            )
        )

    print(f"  Prepared {len(rows)} VIX rows")

    with conn.cursor() as cur:
        cur.execute("DELETE FROM market_data WHERE symbol = '^VIX'")
        print("  Cleared existing VIX data")

        execute_values(
            cur,
            """INSERT INTO market_data
               (id, symbol, asset_type, exchange, region, date,
                open, high, low, close, adj_close, volume,
                daily_return, volatility, source)
               VALUES %s
               ON CONFLICT DO NOTHING""",
            rows,
            page_size=1000,
        )
        conn.commit()
        print(f"  Inserted {len(rows)} rows into market_data")


def main():
    parser = argparse.ArgumentParser(
        description="Seed Railway PostgreSQL with pipeline results"
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("DATABASE_URL"),
        help="PostgreSQL connection URL",
    )
    parser.add_argument("--sentiment", default="results/daily_sentiment.csv")
    parser.add_argument(
        "--features", default="results/pipeline_output/feature_matrix.csv"
    )
    parser.add_argument("--ciss", default="data/kaggle/ecb-ciss/ecb_ciss_daily.csv")
    parser.add_argument("--vix", default="data/kaggle/vix_daily_updated/vix_daily.csv")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print counts without inserting"
    )
    args = parser.parse_args()

    if not args.database_url:
        print("ERROR: No database URL provided.")
        print("  Use --database-url or set DATABASE_URL env variable.")
        print("  Example: postgresql://user:pass@host:port/dbname")
        sys.exit(1)

    print("=" * 60)
    print("SEEDING DASHBOARD DATABASE")
    print("=" * 60)
    print(f"Database: {args.database_url[:50]}...")

    conn = get_connection(args.database_url)
    try:
        seed_sentiment_indices(conn, args.sentiment, args.features)
        seed_stress_indices(conn, args.ciss)
        seed_market_data(conn, args.vix)

        print("\n" + "=" * 60)
        print("SEEDING COMPLETE")
        print("=" * 60)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
