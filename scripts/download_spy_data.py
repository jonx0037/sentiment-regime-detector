#!/usr/bin/env python3
"""
Download SPY data to extend market returns through 2026.
Uses synchronous SQLAlchemy for simpler bulk inserts.
"""

import sys
from pathlib import Path
from datetime import datetime
import uuid

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text


def download_spy():
    """Download SPY data from Yahoo Finance and insert into database."""
    
    print("="*60)
    print("DOWNLOADING SPY DATA")
    print("="*60)
    
    # Download from Yahoo Finance
    print("\nDownloading SPY data from Yahoo Finance...")
    ticker = yf.Ticker("SPY")
    df = ticker.history(start="2010-01-01", end="2026-02-03", auto_adjust=False)
    
    if df.empty:
        print("ERROR: No data downloaded!")
        return
    
    print(f"Downloaded: {len(df)} records")
    print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")
    
    # Use synchronous connection
    engine = create_engine("postgresql://postgres:password@localhost:5432/sentiment_db")
    
    # Prepare data - use actual yfinance columns
    df = df.reset_index()
    df = df.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    })
    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.drop_duplicates(subset=['date'])
    
    print(f"After dedup: {len(df)} records")
    
    with engine.connect() as conn:
        # Delete existing SPY data
        result = conn.execute(text("DELETE FROM market_data WHERE symbol = 'SPY'"))
        conn.commit()
        print(f"Deleted existing SPY records")
        
        # Batch insert
        count = 0
        batch_size = 100
        now = datetime.now()
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            values = []
            for _, row in batch.iterrows():
                values.append({
                    "id": str(uuid.uuid4()),
                    "symbol": "SPY",
                    "date": row['date'],
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    "adj_close": float(row['adj_close']) if pd.notna(row['adj_close']) else float(row['close']),
                    "volume": int(row['volume']),
                    "asset_type": "etf",
                    "region": "us",
                    "exchange": "NYSE",
                    "source": "yfinance",
                    "created_at": now,
                    "updated_at": now,
                })
            
            conn.execute(text("""
                INSERT INTO market_data 
                (id, symbol, date, open, high, low, close, adj_close, volume, asset_type, region, exchange, source, created_at, updated_at)
                VALUES 
                (:id, :symbol, :date, :open, :high, :low, :close, :adj_close, :volume, :asset_type, :region, :exchange, :source, :created_at, :updated_at)
            """), values)
            conn.commit()
            count += len(batch)
            print(f"  Inserted {count}/{len(df)} records...")
    
    print(f"\n✓ Inserted {count} SPY records total!")
    
    # Verify
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MIN(date), MAX(date), COUNT(*) FROM market_data WHERE symbol = 'SPY'"))
        row = result.fetchone()
        print(f"  Date range: {row[0]} to {row[1]}")
        print(f"  Total records: {row[2]}")


if __name__ == "__main__":
    download_spy()
