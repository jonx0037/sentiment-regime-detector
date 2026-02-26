#!/usr/bin/env python3
"""
Lightweight CISS + VIX refresh — skips heavy NLP imports.

Usage:
    python scripts/refresh_ciss_vix.py
"""

import os
import uuid
import csv
from datetime import datetime, timedelta
from io import StringIO

import requests
import psycopg2
from psycopg2.extras import execute_values

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:rUxfHXftLGrOpqvQTbQynXfHXfnQrJOV@yamabiko.proxy.rlwy.net:19328/railway",
)


def update_vix(conn, from_date: str):
    """Fetch and insert recent VIX data via yfinance."""
    try:
        conn.rollback()
        import yfinance as yf

        print(f"  Downloading VIX from {from_date}...")
        vix = yf.download("^VIX", start=from_date, progress=False)
        if vix.empty:
            print("  No VIX data returned")
            return 0

        cur = conn.cursor()
        cur.execute(
            "SELECT DISTINCT date::date FROM market_data WHERE symbol = '^VIX' AND date >= %s",
            (from_date,),
        )
        existing = {str(r[0]) for r in cur.fetchall()}

        now = datetime.utcnow().isoformat() + "+00:00"
        rows = []
        for idx, row in vix.iterrows():
            day = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
            if day in existing:
                continue
            try:
                close_val = float(row["Close"].iloc[0]) if hasattr(row["Close"], "iloc") else float(row["Close"])
                open_val = float(row["Open"].iloc[0]) if hasattr(row["Open"], "iloc") else float(row["Open"])
                high_val = float(row["High"].iloc[0]) if hasattr(row["High"], "iloc") else float(row["High"])
                low_val = float(row["Low"].iloc[0]) if hasattr(row["Low"], "iloc") else float(row["Low"])
                vol_val = float(row["Volume"].iloc[0]) if hasattr(row["Volume"], "iloc") else float(row["Volume"])
            except Exception:
                close_val = float(row.iloc[0]) if len(row) > 0 else 0
                open_val = close_val
                high_val = close_val
                low_val = close_val
                vol_val = 0

            rows.append((
                str(uuid.uuid4()), "^VIX", "volatility_index", day,
                open_val, high_val, low_val, close_val,
                int(vol_val), "yfinance", now, now,
            ))

        if rows:
            execute_values(
                cur,
                """INSERT INTO market_data (id, symbol, asset_type, date, open, high, low, close, volume, source, created_at, updated_at)
                   VALUES %s ON CONFLICT DO NOTHING""",
                rows,
            )
            conn.commit()
            print(f"  ✅ Inserted {len(rows)} new VIX rows")
        else:
            print("  ℹ️  VIX already up to date")
        return len(rows)
    except Exception as e:
        print(f"  ❌ VIX update failed: {e}")
        return 0


def update_ciss(conn, from_date: str):
    """Fetch and insert recent CISS data from ECB Statistical Data Warehouse."""
    try:
        conn.rollback()
        url = (
            f"https://data-api.ecb.europa.eu/service/data/CISS/D.EU.CISS_CI?"
            f"startPeriod={from_date}&format=csvdata"
        )
        print(f"  Fetching ECB CISS from {from_date}...")
        resp = requests.get(url, timeout=30, headers={"Accept": "text/csv"})
        if resp.status_code != 200:
            print(f"  ⚠️  ECB CISS API returned {resp.status_code}, trying alternate URL...")
            url2 = f"https://sdw-wsrest.ecb.europa.eu/service/data/CISS/D.EU.CISS_CI?startPeriod={from_date}&format=csvdata"
            resp = requests.get(url2, timeout=30)
            if resp.status_code != 200:
                print(f"  ❌ ECB CISS API error: {resp.status_code}")
                return 0

        reader = csv.DictReader(StringIO(resp.text))

        cur = conn.cursor()
        cur.execute(
            "SELECT DISTINCT date::date FROM stress_indices WHERE source = 'ecb_ciss' AND date >= %s",
            (from_date,),
        )
        existing = {str(r[0]) for r in cur.fetchall()}

        now = datetime.utcnow().isoformat() + "+00:00"
        rows = []
        for record in reader:
            day = record.get("TIME_PERIOD", "")
            val = record.get("OBS_VALUE", "")
            if not day or not val or day in existing:
                continue
            try:
                ciss_val = float(val)
            except ValueError:
                continue

            rows.append((
                str(uuid.uuid4()), "ecb_ciss", day, "ea",
                ciss_val, now, now,
            ))

        if rows:
            execute_values(
                cur,
                """INSERT INTO stress_indices (id, source, date, region, value, created_at, updated_at)
                   VALUES %s ON CONFLICT DO NOTHING""",
                rows,
            )
            conn.commit()
            print(f"  ✅ Inserted {len(rows)} new CISS rows")
        else:
            print("  ℹ️  CISS already up to date")
        return len(rows)
    except Exception as e:
        print(f"  ❌ CISS update failed: {e}")
        return 0


def main():
    print("=" * 60)
    print("CISS & VIX DATA REFRESH")
    print("=" * 60)

    conn = psycopg2.connect(DB_URL, connect_timeout=10)
    cur = conn.cursor()

    # Determine VIX from_date based on latest VIX data
    cur.execute("SELECT MAX(date)::date FROM market_data WHERE symbol = '^VIX'")
    vix_latest = cur.fetchone()[0]
    vix_from = (vix_latest + timedelta(days=1)).strftime("%Y-%m-%d") if vix_latest else "2024-01-01"

    # Determine CISS from_date based on latest CISS data
    cur.execute("SELECT MAX(date)::date FROM stress_indices WHERE source = 'ecb_ciss'")
    ciss_latest = cur.fetchone()[0]
    ciss_from = (ciss_latest + timedelta(days=1)).strftime("%Y-%m-%d") if ciss_latest else "2024-01-01"

    print(f"\n📉 VIX latest in DB: {vix_latest} → filling from {vix_from}")
    update_vix(conn, vix_from)

    print(f"\n🏛️  CISS latest in DB: {ciss_latest} → filling from {ciss_from}")
    update_ciss(conn, ciss_from)

    # Verify
    conn.rollback()
    cur = conn.cursor()
    print(f"\n{'=' * 60}")
    print("VERIFICATION")
    print(f"{'=' * 60}")

    cur.execute("SELECT COUNT(*), MIN(date)::date, MAX(date)::date FROM market_data WHERE symbol = '^VIX'")
    vix_row = cur.fetchone()
    print(f"VIX: {vix_row[0]} rows ({vix_row[1]} → {vix_row[2]})")

    cur.execute("SELECT COUNT(*), MIN(date)::date, MAX(date)::date FROM stress_indices WHERE source = 'ecb_ciss'")
    ciss_row = cur.fetchone()
    print(f"CISS: {ciss_row[0]} rows ({ciss_row[1]} → {ciss_row[2]})")

    cur.close()
    conn.close()
    print(f"\n🎉 Done!")


if __name__ == "__main__":
    main()
