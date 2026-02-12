#!/usr/bin/env python3
"""
Restore sentiment_indices historical data to Railway PostgreSQL.
This script specifically handles the aggregated sentiment indices data.
"""
import json
import os
import sys
import time
from urllib.parse import urlparse

import psycopg2
from psycopg2.extras import execute_values


def wait_for_db(db_params, max_attempts=30):
    """Wait for database to be ready."""
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


def parse_database_url(url):
    """Parse DATABASE_URL into connection parameters."""
    # Handle both postgresql:// and postgresql+asyncpg://
    url = url.replace('postgresql+asyncpg://', 'postgresql://')

    result = urlparse(url)
    return {
        'dbname': result.path[1:],
        'user': result.username,
        'password': result.password,
        'host': result.hostname,
        'port': result.port or 5432
    }


def main():
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)

    print(f"Database URL: {database_url[:30]}...")

    # Parse connection parameters
    db_params = parse_database_url(database_url)
    print(f"Connecting to: {db_params['host']}:{db_params['port']}/{db_params['dbname']}")

    # Wait for database
    wait_for_db(db_params)

    # Load data from JSON
    print("Loading sentiment indices data...")
    with open('/app/sentiment_indices_export.json', 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} records")
    print(f"Date range: {data[0]['period_start']} to {data[-1]['period_start']}")

    # Connect and restore
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    try:
        # Check current data
        cur.execute("SELECT COUNT(*) FROM sentiment_indices WHERE source IS NULL")
        before_count = cur.fetchone()[0]
        print(f"Current sentiment_indices records (source IS NULL): {before_count}")

        # Clear existing aggregated data (source IS NULL) to avoid duplicates
        print("Clearing existing aggregated sentiment indices...")
        cur.execute("DELETE FROM sentiment_indices WHERE source IS NULL")
        deleted = cur.rowcount
        print(f"Deleted {deleted} existing records")

        # Prepare data for insertion
        values = []
        for record in data:
            values.append((
                record['id'],
                record['asset_class'],
                record['source'],
                record['period_start'],
                record['period_end'],
                record['granularity'],
                record['mean_compound'],
                record['std_compound'],
                record['sample_count'],
                record['positive_ratio'],
                record['negative_ratio'],
                record['sentiment_momentum'],
                record['sentiment_acceleration'],
                record['created_at'],
                record['updated_at']
            ))

        # Insert data in batches
        print(f"Inserting {len(values)} records...")
        execute_values(
            cur,
            """
            INSERT INTO sentiment_indices (
                id, asset_class, source, period_start, period_end, granularity,
                mean_compound, std_compound, sample_count, positive_ratio, negative_ratio,
                sentiment_momentum, sentiment_acceleration, created_at, updated_at
            ) VALUES %s
            """,
            values,
            page_size=100
        )

        conn.commit()
        print("Data inserted successfully!")

        # Verify
        cur.execute("""
            SELECT
                asset_class,
                COUNT(*),
                MIN(period_start)::date,
                MAX(period_start)::date
            FROM sentiment_indices
            WHERE source IS NULL
            GROUP BY asset_class
            ORDER BY asset_class
        """)

        print("\nVerification - Records by asset class:")
        for row in cur.fetchall():
            print(f"  {row[0]}: {row[1]} records from {row[2]} to {row[3]}")

        # Overall stats
        cur.execute("""
            SELECT
                COUNT(*),
                MIN(period_start)::date,
                MAX(period_start)::date
            FROM sentiment_indices
            WHERE source IS NULL
        """)
        total, min_date, max_date = cur.fetchone()
        print(f"\nTotal records: {total}")
        print(f"Date range: {min_date} to {max_date}")

        print("\n✅ Sentiment indices restoration completed successfully!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error during restoration: {e}")
        raise
    finally:
        cur.close()
        conn.close()

    # Keep container running briefly so logs can be viewed
    print("\nContainer will exit in 30 seconds...")
    time.sleep(30)


if __name__ == '__main__':
    main()
