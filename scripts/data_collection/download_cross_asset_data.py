#!/usr/bin/env python3
"""
Download market data for cross-asset backtesting.

Downloads:
- VIX (updated through present)
- Gold (GC=F futures, GLD ETF)
- Silver (SI=F futures, SLV ETF)
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)

Uses yfinance for Yahoo Finance data.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Optional
import logging

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import yfinance as yf
    import pandas as pd
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("ERROR: yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

from sqlalchemy import text
from sentiment_detector.core.database import get_session_context
from sentiment_detector.models.market_data import MarketData

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define symbols to download
SYMBOLS = {
    # VIX
    "^VIX": {"asset_type": "index", "region": "us", "exchange": "CBOE", "description": "CBOE Volatility Index"},
    # Gold
    "GC=F": {"asset_type": "commodity", "region": "us", "exchange": "COMEX", "description": "Gold Futures"},
    "GLD": {"asset_type": "etf", "region": "us", "exchange": "NYSE", "description": "SPDR Gold Shares ETF"},
    # Silver
    "SI=F": {"asset_type": "commodity", "region": "us", "exchange": "COMEX", "description": "Silver Futures"},
    "SLV": {"asset_type": "etf", "region": "us", "exchange": "NYSE", "description": "iShares Silver Trust ETF"},
    # Crypto
    "BTC-USD": {"asset_type": "crypto", "region": "global", "exchange": "crypto", "description": "Bitcoin USD"},
    "ETH-USD": {"asset_type": "crypto", "region": "global", "exchange": "crypto", "description": "Ethereum USD"},
}

# Date range - from 2010 to present for comprehensive historical coverage
START_DATE = "2010-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")


def download_symbol_data(symbol: str, start: str, end: str) -> Optional[pd.DataFrame]:
    """Download OHLCV data for a single symbol."""
    try:
        logger.info(f"Downloading {symbol} from {start} to {end}...")
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, auto_adjust=False)
        
        if df.empty:
            logger.warning(f"No data returned for {symbol}")
            return None
        
        # Standardize column names
        df = df.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        })
        
        # Reset index to get date as column
        df = df.reset_index()
        df = df.rename(columns={"Date": "date"})
        
        # Convert timezone-aware datetime to date
        if hasattr(df['date'].dtype, 'tz'):
            df['date'] = df['date'].dt.tz_localize(None)
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Drop any rows with NaN close prices
        df = df.dropna(subset=['close'])
        
        logger.info(f"Downloaded {len(df)} records for {symbol}: {df['date'].min()} to {df['date'].max()}")
        return df
        
    except Exception as e:
        logger.error(f"Error downloading {symbol}: {e}")
        return None


async def get_existing_dates(session, symbol: str) -> set:
    """Get existing dates for a symbol in the database."""
    result = await session.execute(text("""
        SELECT date FROM market_data WHERE symbol = :symbol
    """), {"symbol": symbol})
    rows = result.fetchall()
    return {row[0] for row in rows}


async def insert_market_data(session, symbol: str, df: pd.DataFrame, metadata: dict) -> int:
    """Insert market data into database, skipping existing dates."""
    
    # Get existing dates
    existing_dates = await get_existing_dates(session, symbol)
    logger.info(f"Found {len(existing_dates)} existing records for {symbol}")
    
    # Filter to new dates only
    df = df[~df['date'].isin(existing_dates)]
    
    if df.empty:
        logger.info(f"No new data to insert for {symbol}")
        return 0
    
    # Prepare batch insert using executemany
    inserted = 0
    batch_size = 100
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        try:
            for _, row in batch.iterrows():
                await session.execute(text("""
                    INSERT INTO market_data (id, symbol, asset_type, exchange, region, date, open, high, low, close, adj_close, volume, source, created_at, updated_at)
                    VALUES (gen_random_uuid(), :symbol, :asset_type, :exchange, :region, :date, :open, :high, :low, :close, :adj_close, :volume, :source, NOW(), NOW())
                    ON CONFLICT DO NOTHING
                """), {
                    "symbol": symbol,
                    "asset_type": metadata["asset_type"],
                    "exchange": metadata.get("exchange"),
                    "region": metadata.get("region"),
                    "date": row["date"],
                    "open": float(row["open"]) if pd.notna(row.get("open")) else None,
                    "high": float(row["high"]) if pd.notna(row.get("high")) else None,
                    "low": float(row["low"]) if pd.notna(row.get("low")) else None,
                    "close": float(row["close"]),
                    "adj_close": float(row["adj_close"]) if pd.notna(row.get("adj_close")) else None,
                    "volume": int(row["volume"]) if pd.notna(row.get("volume")) and row["volume"] > 0 else None,
                    "source": "yfinance",
                })
                inserted += 1
            
            await session.commit()
            logger.info(f"Inserted batch {i//batch_size + 1} ({inserted} total)")
            
        except Exception as e:
            logger.error(f"Error inserting batch for {symbol}: {e}")
            await session.rollback()
            # Continue with next batch
    
    logger.info(f"Inserted {inserted} new records for {symbol}")
    return inserted


async def main():
    """Main download and import function."""
    
    print("=" * 70)
    print("CROSS-ASSET MARKET DATA DOWNLOAD")
    print(f"Date Range: {START_DATE} to {END_DATE}")
    print("=" * 70)
    print()
    
    total_inserted = 0
    
    async with get_session_context() as session:
        for symbol, metadata in SYMBOLS.items():
            print(f"\n{'='*50}")
            print(f"Processing: {symbol} - {metadata['description']}")
            print(f"{'='*50}")
            
            # Download data
            df = download_symbol_data(symbol, START_DATE, END_DATE)
            
            if df is not None and not df.empty:
                # Insert into database
                inserted = await insert_market_data(session, symbol, df, metadata)
                total_inserted += inserted
            else:
                logger.warning(f"Skipping {symbol} - no data downloaded")
    
    print("\n" + "=" * 70)
    print(f"COMPLETE: Inserted {total_inserted} total records")
    print("=" * 70)
    
    # Verify results
    print("\n=== Verification ===")
    async with get_session_context() as session:
        for symbol in SYMBOLS.keys():
            result = await session.execute(text("""
                SELECT COUNT(*), MIN(date), MAX(date) 
                FROM market_data 
                WHERE symbol = :symbol
            """), {"symbol": symbol})
            row = result.fetchone()
            print(f"{symbol:12} | {row[0]:,} records | {row[1]} to {row[2]}")


if __name__ == "__main__":
    asyncio.run(main())
