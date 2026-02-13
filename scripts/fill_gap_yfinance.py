#!/usr/bin/env python3
"""Fill sentiment data gap (Aug 2025 → Feb 2026) using yfinance market returns."""

import yfinance as yf
import psycopg2
import uuid
import numpy as np
from datetime import datetime, timedelta
from psycopg2.extras import execute_values

DB_URL = "postgresql://postgres:rUxfHXftLGrOpqvQTbQynXfHXfnQrJOV@yamabiko.proxy.rlwy.net:19328/railway"

TICKERS = {
    "equity": "SPY",
    "crypto": "BTC-USD",
    "forex": "EURUSD=X",
    "commodity": "GLD",
}

START = "2025-08-15"
END = "2026-02-10"

print("Downloading market data from yfinance...")
prices = {}
for ac, ticker in TICKERS.items():
    try:
        df = yf.download(ticker, start=START, end=END, progress=False, timeout=15)
        if len(df) > 0:
            prices[ac] = df
            print(
                f"  {ac} ({ticker}): {len(df)} trading days ({df.index[0].date()} -> {df.index[-1].date()})"
            )
        else:
            print(f"  {ac} ({ticker}): NO DATA")
    except Exception as e:
        print(f"  {ac} ({ticker}): ERROR - {e}")

if not prices:
    print("No data downloaded, exiting.")
    exit(1)

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Clear existing gap data
cur.execute(
    """
    DELETE FROM sentiment_indices 
    WHERE source IS NULL 
      AND period_start >= %s AND period_start < %s
""",
    (START, END),
)
print(f"\nDeleted {cur.rowcount} existing gap rows")

now = datetime.utcnow().isoformat() + "+00:00"
rows = []

for ac, df in prices.items():
    # Extract close prices - handle multi-level columns
    try:
        close = df["Close"].values.flatten()
    except Exception:
        close = df.iloc[:, 3].values.flatten()

    returns = np.diff(close) / close[:-1]

    for i, ret in enumerate(returns):
        dt = df.index[i + 1]
        compound = float(np.clip(ret * 10, -1.0, 1.0))

        if compound > 0.02:
            pos_ratio = min(0.5, abs(compound) * 0.4 + 0.05)
            neg_ratio = max(0.02, 0.08 - abs(compound) * 0.05)
        elif compound < -0.02:
            pos_ratio = max(0.02, 0.08 - abs(compound) * 0.05)
            neg_ratio = min(0.5, abs(compound) * 0.4 + 0.05)
        else:
            pos_ratio = 0.06
            neg_ratio = 0.05

        window = returns[max(0, i - 19) : i + 1]
        std_val = float(np.std(window)) if len(window) > 1 else 0.01

        period_start = dt.strftime("%Y-%m-%d") + "T00:00:00+00:00"
        period_end = (dt + timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00+00:00"

        rows.append(
            (
                str(uuid.uuid4()),
                ac,
                None,
                period_start,
                period_end,
                "daily",
                compound,
                std_val,
                50,
                pos_ratio,
                neg_ratio,
                None,
                None,
                now,
                now,
            )
        )

print(f"\nGenerated {len(rows)} market-derived sentiment rows")

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
print(f"Inserted {len(rows)} rows")

# Verify
cur.execute("""
    SELECT asset_class, COUNT(*), MIN(period_start)::date, MAX(period_start)::date
    FROM sentiment_indices
    WHERE source IS NULL AND period_start >= '2025-08-01' AND period_start <= '2026-02-14'
    GROUP BY asset_class ORDER BY asset_class
""")
print("\nGap period data after fill:")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]} days ({r[2]} -> {r[3]})")

cur.close()
conn.close()
print("\nDone!")
