import os
import psycopg2
from urllib.parse import urlparse

# URL from previous context
DB_URL = "postgresql://postgres:rUxfHXftLGrOpqvQTbQynXfHXfnQrJOV@yamabiko.proxy.rlwy.net:19328/railway"


def check_db():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()

        queries = [
            "SELECT count(*) FROM raw_texts",
            "SELECT min(created_at), max(created_at) FROM raw_texts",
            "SELECT count(*) FROM sentiment_scores",
            "SELECT count(*) FROM sentiment_indices",  # Aggregated
            "SELECT min(date), max(date) FROM sentiment_indices",
        ]

        print(f"Checking DB at {DB_URL.split('@')[1]}...")

        cur.execute("SELECT count(*) FROM raw_texts")
        raw_count = cur.fetchone()[0]
        print(f"raw_texts count: {raw_count}")

        if raw_count > 0:
            cur.execute("SELECT min(created_at), max(created_at) FROM raw_texts")
            dates = cur.fetchone()
            print(f"raw_texts range: {dates[0]} to {dates[1]}")

        cur.execute("SELECT count(*) FROM sentiment_scores")
        print(f"sentiment_scores count: {cur.fetchone()[0]}")

        cur.execute("SELECT count(*) FROM sentiment_indices")
        idx_count = cur.fetchone()[0]
        print(f"sentiment_indices (aggregated) count: {idx_count}")

        if idx_count > 0:
            cur.execute("SELECT min(date), max(date) FROM sentiment_indices")
            idx_dates = cur.fetchone()
            print(f"sentiment_indices range: {idx_dates[0]} to {idx_dates[1]}")

        conn.close()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    check_db()
