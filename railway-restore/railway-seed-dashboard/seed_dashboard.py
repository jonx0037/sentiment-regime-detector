#!/usr/bin/env python3
"""
Seed Railway PostgreSQL with pipeline results.
Runs inside Railway's network to access postgres.railway.internal.

Seeds:
1. sentiment_indices — daily sentiment per asset class
2. stress_indices — ECB CISS daily values
3. market_data — VIX daily (symbol='^VIX')
"""

import os
import sys
import time
from datetime import timezone
from uuid import uuid4
from urllib.parse import urlparse

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def parse_database_url(url):
    url = url.replace("postgresql+asyncpg://", "postgresql://")
    result = urlparse(url)
    return {
        "dbname": result.path[1:],
        "user": result.username,
        "password": result.password,
        "host": result.hostname,
        "port": result.port or 5432,
    }


def wait_for_db(db_params, max_attempts=30):
    print("Waiting for PostgreSQL to be ready...")
    for attempt in range(max_attempts):
        try:
            conn = psycopg2.connect(**db_params)
            conn.close()
            print("PostgreSQL is ready!")
            return True
        except psycopg2.OperationalError:
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 1}/{max_attempts} failed, retrying...")
                time.sleep(2)
            else:
                raise
    return False


def seed_sentiment_indices(conn):
    print("\n--- Seeding sentiment_indices ---")
    sent = pd.read_csv(
        "/app/daily_sentiment.csv", parse_dates=["date"], index_col="date"
    )
    sent = sent[sent.index >= "2005-01-01"]

    features = None
    if os.path.exists("/app/feature_matrix.csv"):
        features = pd.read_csv(
            "/app/feature_matrix.csv", parse_dates=["date"], index_col="date"
        )

    asset_classes = {
        "crypto": "crypto",
        "equities": "equity",
        "forex": "forex",
        "news": "news",
        "social": "social",
        "cross_asset": "cross_asset",
    }

    rows = []
    now = pd.Timestamp.now(tz="UTC")
    for idx, row_data in sent.iterrows():
        for csv_prefix, db_name in asset_classes.items():
            mean_col = f"{csv_prefix}_ensemble_mean"
            if mean_col not in sent.columns:
                continue
            mean_val = row_data.get(mean_col)
            if pd.isna(mean_val):
                continue

            std_col = f"{csv_prefix}_ensemble_std"
            count_col = f"{csv_prefix}_count"
            std_val = row_data.get(std_col, None)
            count_val = row_data.get(count_col, 1)

            momentum = None
            if (
                features is not None
                and "sent_momentum" in features.columns
                and idx in features.index
            ):
                m = features.loc[idx, "sent_momentum"]
                if not pd.isna(m):
                    momentum = float(m)

            rows.append(
                (
                    str(uuid4()),
                    db_name,
                    None,
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
                    max(0, float(mean_val)),
                    max(0, -float(mean_val)),
                    momentum,
                    None,
                    str(now),
                    str(now),
                )
            )

    print(f"  Prepared {len(rows)} rows")
    cur = conn.cursor()
    cur.execute("DELETE FROM sentiment_indices")
    execute_values(
        cur,
        """
        INSERT INTO sentiment_indices
        (id, asset_class, source, period_start, period_end, granularity,
         mean_compound, std_compound, sample_count,
         positive_ratio, negative_ratio,
         sentiment_momentum, sentiment_acceleration, created_at, updated_at)
        VALUES %s
    """,
        rows,
        page_size=1000,
    )
    conn.commit()
    print(f"  Inserted {len(rows)} rows")

    # Verify
    cur.execute("""
        SELECT asset_class, COUNT(*), MIN(period_start)::date, MAX(period_start)::date
        FROM sentiment_indices WHERE source IS NULL
        GROUP BY asset_class ORDER BY asset_class
    """)
    print("  Verification:")
    for row in cur.fetchall():
        print(f"    {row[0]}: {row[1]} records ({row[2]} to {row[3]})")
    cur.close()


def seed_stress_indices(conn):
    print("\n--- Seeding stress_indices (ECB CISS) ---")
    df = pd.read_csv("/app/ecb_ciss_daily.csv")
    date_col = [c for c in df.columns if "DATE" in c.upper()][0]
    val_col = [c for c in df.columns if "CISS" in c.upper() or "IDX" in c.upper()][0]
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["ciss"] = pd.to_numeric(df[val_col], errors="coerce")
    df = df.dropna(subset=["date", "ciss"])

    rows = [
        (str(uuid4()), "ecb_ciss", r["date"].date(), "ea", float(r["ciss"]), "daily")
        for _, r in df.iterrows()
    ]
    print(f"  Prepared {len(rows)} rows")

    cur = conn.cursor()
    cur.execute("DELETE FROM stress_indices WHERE source = 'ecb_ciss'")
    execute_values(
        cur,
        """
        INSERT INTO stress_indices (id, source, date, region, value, frequency)
        VALUES %s ON CONFLICT DO NOTHING
    """,
        rows,
        page_size=1000,
    )
    conn.commit()
    print(f"  Inserted {len(rows)} rows")
    cur.close()


def seed_market_data(conn):
    print("\n--- Seeding market_data (VIX) ---")
    df = pd.read_csv("/app/vix_daily.csv", parse_dates=["date"], index_col="date")
    df.columns = [c.lower() for c in df.columns]
    df = df.dropna(subset=["close"])
    df["daily_return"] = df["close"].pct_change()

    rows = []
    for date, r in df.iterrows():
        rows.append(
            (
                str(uuid4()),
                "^VIX",
                "index",
                None,
                "us",
                date.date(),
                float(r["open"]) if not pd.isna(r.get("open")) else None,
                float(r["high"]) if not pd.isna(r.get("high")) else None,
                float(r["low"]) if not pd.isna(r.get("low")) else None,
                float(r["close"]),
                None,
                None,
                float(r["daily_return"])
                if not pd.isna(r.get("daily_return"))
                else None,
                None,
                "vix_kaggle",
            )
        )

    print(f"  Prepared {len(rows)} rows")
    cur = conn.cursor()
    cur.execute("DELETE FROM market_data WHERE symbol = '^VIX'")
    execute_values(
        cur,
        """
        INSERT INTO market_data
        (id, symbol, asset_type, exchange, region, date,
         open, high, low, close, adj_close, volume,
         daily_return, volatility, source)
        VALUES %s ON CONFLICT DO NOTHING
    """,
        rows,
        page_size=1000,
    )
    conn.commit()
    print(f"  Inserted {len(rows)} rows")
    cur.close()


def main():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)

    db_params = parse_database_url(database_url)
    print(
        f"Connecting to: {db_params['host']}:{db_params['port']}/{db_params['dbname']}"
    )
    wait_for_db(db_params)

    conn = psycopg2.connect(**db_params)
    try:
        seed_sentiment_indices(conn)
        seed_stress_indices(conn)
        seed_market_data(conn)
        print("\n✅ All seeding complete!")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()

    print("\nContainer will exit in 30 seconds...")
    time.sleep(30)


if __name__ == "__main__":
    main()
