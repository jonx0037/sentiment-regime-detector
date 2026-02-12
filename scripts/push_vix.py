#!/usr/bin/env python3
"""Push recent VIX data to Railway using yfinance."""

import uuid
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

DB = "postgresql://postgres:rUxfHXftLGrOpqvQTbQynXfHXfnQrJOV@yamabiko.proxy.rlwy.net:19328/railway"

# VIX closing prices from yfinance download (Feb 2-10, 2026)
VIX = [
    ("2026-02-02", 16.53, 16.34, 16.53, 15.87),
    ("2026-02-03", 17.39, 18.00, 18.57, 16.54),
    ("2026-02-04", 17.74, 18.64, 19.31, 17.03),
    ("2026-02-05", 18.79, 21.77, 21.80, 18.49),
    ("2026-02-06", 21.34, 20.37, 21.63, 17.62),
    ("2026-02-09", 17.78, 17.36, 18.32, 16.82),
    ("2026-02-10", 16.54, 17.79, 17.93, 16.45),
]

conn = psycopg2.connect(DB)
cur = conn.cursor()

cur.execute(
    "SELECT DISTINCT date::date FROM market_data WHERE symbol = '^VIX' AND date >= '2026-02-01'"
)
existing = {str(r[0]) for r in cur.fetchall()}
print(f"Existing VIX dates in Feb: {existing}")

now = datetime.utcnow().isoformat() + "+00:00"
rows = []
for day, open_v, close_v, high_v, low_v in VIX:
    if day in existing:
        continue
    rows.append(
        (
            str(uuid.uuid4()),
            "^VIX",
            "volatility_index",
            day,
            open_v,
            high_v,
            low_v,
            close_v,
            0,
            "yfinance",
            now,
            now,
        )
    )

if rows:
    execute_values(
        cur,
        """INSERT INTO market_data
           (id, symbol, asset_type, date, open, high, low, close, volume, source, created_at, updated_at)
           VALUES %s ON CONFLICT DO NOTHING""",
        rows,
    )
    conn.commit()
    print(f"✅ Inserted {len(rows)} VIX rows")
else:
    print("VIX already up to date")

cur.execute(
    "SELECT date::date, close FROM market_data WHERE symbol='^VIX' AND date>='2026-02-01' ORDER BY date"
)
for r in cur.fetchall():
    print(f"  {r[0]}: VIX={r[1]:.2f}")

cur.close()
conn.close()
print("Done")
