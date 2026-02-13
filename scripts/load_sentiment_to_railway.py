#!/usr/bin/env python3
"""
Load the full HPC-processed daily_sentiment.csv into Railway PostgreSQL.

Transforms the wide-format CSV (columns per asset class) into rows for
the sentiment_indices table. This replaces the stale seed data with
the comprehensive 6,000+ day dataset processed via ensemble FinBERT/RoBERTa.

Usage:
    export DATABASE_URL="postgresql://user:pass@host:port/dbname"
    python scripts/load_sentiment_to_railway.py
"""

import csv
import os
import sys
import uuid
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import execute_values

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "daily_sentiment_corrected.csv",
)

# Map CSV column prefixes to sentiment_indices asset_class values
# Frontend expects: equity, crypto, forex, commodity
# Corrected CSV has: equities, crypto, forex, cross-asset (proper asset classes)
# Source-level columns: src_news_*, src_social_*, src_market_data_*
ASSET_MAP = {
    "equities": "equity",
    "crypto": "crypto",
    "forex": "forex",
    "cross-asset": "commodity",
}

# Source-level data (src_news_*, src_social_*, src_market_data_*)
# These get inserted with a non-null source column
SOURCE_MAP = {
    "src_news": "news",
    "src_social": "social",
    "src_market_data": "market_data",
}


def parse_float(val):
    """Parse a float value, returning None for empty strings."""
    if val is None or val == "" or val == "nan":
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def parse_int(val):
    """Parse an int value, returning 0 for empty strings."""
    if val is None or val == "" or val == "nan":
        return 0
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return 0


def transform_csv_to_rows(csv_path):
    """
    Read daily_sentiment_corrected.csv and transform into sentiment_indices rows.

    The corrected CSV has columns like:
      equities_ensemble_mean, equities_ensemble_std, equities_count,
      crypto_ensemble_mean, ..., cross-asset_ensemble_mean, ...
      src_news_ensemble_mean, src_social_ensemble_mean, src_market_data_ensemble_mean
      overall_ensemble_mean, overall_vader_mean, overall_finbert_mean, ...
    """
    rows = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for record in reader:
            date_str = record.get("date", "").strip()
            if not date_str or date_str == "":
                continue

            # Parse the date
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue

            # Skip bogus dates
            if dt.year < 2000:
                continue

            period_start = dt.isoformat() + "+00:00"
            period_end = (dt + timedelta(days=1)).isoformat() + "+00:00"
            now = datetime.utcnow().isoformat() + "+00:00"

            # --- Asset-class-level rows (source=NULL = aggregated) ---
            for csv_prefix, ac in ASSET_MAP.items():
                ensemble_mean = parse_float(record.get(f"{csv_prefix}_ensemble_mean"))
                ensemble_std = parse_float(record.get(f"{csv_prefix}_ensemble_std"))
                count_val = parse_int(record.get(f"{csv_prefix}_count"))

                if ensemble_mean is None and count_val == 0:
                    continue

                rows.append(
                    (
                        str(uuid.uuid4()),
                        ac,
                        None,
                        period_start,
                        period_end,
                        "daily",
                        ensemble_mean,
                        ensemble_std,
                        count_val,
                        None,
                        None,
                        None,
                        None,
                        now,
                        now,
                    )
                )

            # --- Source-level rows (source=news/social/market_data) ---
            for csv_prefix, src_name in SOURCE_MAP.items():
                ensemble_mean = parse_float(record.get(f"{csv_prefix}_ensemble_mean"))
                ensemble_std = parse_float(record.get(f"{csv_prefix}_ensemble_std"))
                count_val = parse_int(record.get(f"{csv_prefix}_count"))

                if ensemble_mean is None and count_val == 0:
                    continue

                # Source rows use "cross_asset" as the asset class since
                # they span multiple assets
                rows.append(
                    (
                        str(uuid.uuid4()),
                        "commodity",
                        src_name,
                        period_start,
                        period_end,
                        "daily",
                        ensemble_mean,
                        ensemble_std,
                        count_val,
                        None,
                        None,
                        None,
                        None,
                        now,
                        now,
                    )
                )

    return rows


def main():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print()
        print("Get your Railway public database URL:")
        print("  1. Go to Railway Dashboard → your Postgres service")
        print("  2. Click 'Connect' or 'Variables' tab")
        print("  3. Copy the public connection string")
        print()
        print("Then run:")
        print('  export DATABASE_URL="postgresql://..."')
        print("  python scripts/load_sentiment_to_railway.py")
        sys.exit(1)

    # Handle asyncpg URLs
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")

    print(f"📁 Reading CSV: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        print(f"❌ CSV file not found: {CSV_PATH}")
        sys.exit(1)

    rows = transform_csv_to_rows(CSV_PATH)
    print(f"✅ Transformed {len(rows)} records from CSV")

    # Show breakdown
    from collections import Counter

    ac_counts = Counter(r[1] for r in rows)
    for ac, count in sorted(ac_counts.items()):
        dates = [r[3][:10] for r in rows if r[1] == ac]
        print(f"   {ac}: {count} records ({min(dates)} to {max(dates)})")

    print(f"\n🔗 Connecting to Railway PostgreSQL...")
    conn = psycopg2.connect(database_url)
    cur = conn.cursor()

    try:
        # Check current state
        cur.execute("SELECT COUNT(*) FROM sentiment_indices WHERE source IS NULL")
        before = cur.fetchone()[0]
        print(f"   Current records (source IS NULL): {before}")

        # Clear existing aggregated data to avoid duplicates
        print("🗑️  Clearing existing aggregated indices...")
        cur.execute("DELETE FROM sentiment_indices WHERE source IS NULL")
        print(f"   Deleted {cur.rowcount} old records")

        # Insert in batches
        print(f"📤 Inserting {len(rows)} records...")
        execute_values(
            cur,
            """
            INSERT INTO sentiment_indices (
                id, asset_class, source, period_start, period_end, granularity,
                mean_compound, std_compound, sample_count, positive_ratio,
                negative_ratio, sentiment_momentum, sentiment_acceleration,
                created_at, updated_at
            ) VALUES %s
            """,
            rows,
            page_size=500,
        )
        conn.commit()
        print("✅ Data inserted successfully!")

        # Verify
        cur.execute("""
            SELECT
                asset_class,
                COUNT(*) as cnt,
                MIN(period_start)::date as min_date,
                MAX(period_start)::date as max_date,
                ROUND(AVG(mean_compound)::numeric, 4) as avg_sentiment
            FROM sentiment_indices
            WHERE source IS NULL
            GROUP BY asset_class
            ORDER BY asset_class
        """)
        print("\n📊 Verification — Records by asset class:")
        for row in cur.fetchall():
            print(f"   {row[0]}: {row[1]} records ({row[2]} to {row[3]}) avg={row[4]}")

        cur.execute("""
            SELECT COUNT(*), MIN(period_start)::date, MAX(period_start)::date
            FROM sentiment_indices WHERE source IS NULL
        """)
        total, min_d, max_d = cur.fetchone()
        print(f"\n✅ Total: {total} records from {min_d} to {max_d}")
        print("🎉 Migration complete! Dashboard will now show real data.")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
