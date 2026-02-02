#!/usr/bin/env python3
"""
Minimal CISS integration test - no model imports.
"""

import asyncio
import sys
import os
from datetime import date
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)


async def test_ciss_data():
    """Test loading CISS data from database."""
    from src.sentiment_detector.core.database import get_session_context
    from sqlalchemy import text
    
    print("\n" + "=" * 60)
    print("CISS DATA VERIFICATION")
    print("=" * 60)
    
    async with get_session_context() as session:
        # Check CISS data availability (column is 'source', not 'indicator_name')
        result = await session.execute(text("""
            SELECT 
                COUNT(*) as count,
                MIN(date) as min_date,
                MAX(date) as max_date,
                AVG(value) as avg_value,
                MAX(value) as max_value
            FROM stress_indices
            WHERE source = 'ecb_ciss'
        """))
        row = result.fetchone()
        
        print(f"\n✅ ECB CISS Data:")
        print(f"   Records: {row[0]}")
        print(f"   Date range: {row[1]} to {row[2]}")
        print(f"   Mean: {row[3]:.4f}" if row[3] else "   Mean: N/A")
        print(f"   Max: {row[4]:.4f}" if row[4] else "   Max: N/A")
        
        # Get sample crisis periods
        print("\n📊 High Stress Periods (CISS > 0.5):")
        result = await session.execute(text("""
            SELECT date, value
            FROM stress_indices
            WHERE source = 'ecb_ciss'
            AND value > 0.5
            ORDER BY value DESC
            LIMIT 10
        """))
        
        for row in result.fetchall():
            print(f"   {row[0]}: {row[1]:.4f}")


async def test_market_data():
    """Verify market data for backtests."""
    from src.sentiment_detector.core.database import get_session_context
    from sqlalchemy import text
    
    print("\n" + "=" * 60)
    print("CROSS-ASSET MARKET DATA")
    print("=" * 60)
    
    symbols = ["^VIX", "GC=F", "GLD", "SI=F", "SLV", "BTC-USD", "ETH-USD"]
    
    async with get_session_context() as session:
        for symbol in symbols:
            result = await session.execute(text("""
                SELECT 
                    COUNT(*) as count,
                    MIN(date) as min_date,
                    MAX(date) as max_date
                FROM market_data
                WHERE symbol = :symbol
            """), {"symbol": symbol})
            row = result.fetchone()
            
            print(f"\n   {symbol}:")
            print(f"     Records: {row[0]}")
            if row[0] > 0:
                print(f"     Range: {row[1]} to {row[2]}")


async def test_backtest_periods():
    """Check data for specific backtest periods."""
    from src.sentiment_detector.core.database import get_session_context
    from sqlalchemy import text
    
    print("\n" + "=" * 60)
    print("BACKTEST PERIOD DATA COVERAGE")
    print("=" * 60)
    
    backtests = [
        ("2008 Financial Crisis", "2007-06-01", "2010-06-30"),
        ("COVID-19 March 2020", "2019-06-01", "2021-06-30"),
        ("GameStop 2021", "2020-12-01", "2021-03-31"),
        ("Crypto Winter 2022", "2021-11-01", "2022-12-31"),
        ("Gold Rise Since COVID", "2020-01-01", "2026-01-31"),
    ]
    
    async with get_session_context() as session:
        for name, start, end in backtests:
            print(f"\n📊 {name} ({start} to {end})")
            
            # Check VIX
            result = await session.execute(text("""
                SELECT COUNT(*), MIN(date), MAX(date), AVG(close)
                FROM market_data
                WHERE symbol = '^VIX'
                AND date BETWEEN :start AND :end
            """), {"start": start, "end": end})
            row = result.fetchone()
            if row[0] > 0:
                print(f"   VIX: {row[0]} days, avg={row[3]:.2f}")
            
            # Check CISS
            result = await session.execute(text("""
                SELECT COUNT(*), AVG(value), MAX(value)
                FROM stress_indices
                WHERE source = 'ecb_ciss'
                AND date BETWEEN :start AND :end
            """), {"start": start, "end": end})
            row = result.fetchone()
            if row[0] > 0:
                print(f"   CISS: {row[0]} days, avg={row[1]:.4f}, max={row[2]:.4f}")
            
            # Check Gold
            result = await session.execute(text("""
                SELECT COUNT(*), MIN(close), MAX(close)
                FROM market_data
                WHERE symbol = 'GC=F'
                AND date BETWEEN :start AND :end
            """), {"start": start, "end": end})
            row = result.fetchone()
            if row[0] > 0:
                print(f"   Gold: {row[0]} days, range ${row[1]:.0f} - ${row[2]:.0f}")
            
            # Check BTC
            result = await session.execute(text("""
                SELECT COUNT(*), MIN(close), MAX(close)
                FROM market_data
                WHERE symbol = 'BTC-USD'
                AND date BETWEEN :start AND :end
            """), {"start": start, "end": end})
            row = result.fetchone()
            if row[0] > 0:
                print(f"   BTC: {row[0]} days, range ${row[1]:.0f} - ${row[2]:.0f}")


async def main():
    print("\n" + "=" * 60)
    print("CISS + CROSS-ASSET DATA VERIFICATION")
    print("=" * 60)
    
    await test_ciss_data()
    await test_market_data()
    await test_backtest_periods()
    
    print("\n" + "=" * 60)
    print("✅ DATA VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
