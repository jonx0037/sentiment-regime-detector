#!/usr/bin/env python3
"""Check database status for CISS integration and market data."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import text
from sentiment_detector.core.database import get_session_context


async def main():
    async with get_session_context() as session:
        # Check market data symbols
        result = await session.execute(text("""
            SELECT symbol, asset_type, COUNT(*) as cnt
            FROM market_data
            GROUP BY symbol, asset_type
            ORDER BY cnt DESC
            LIMIT 25
        """))
        symbols = result.fetchall()
        await session.commit()
        
        print('=== Top 25 Market Data Symbols ===')
        for s, t, c in symbols:
            print(f'{s:15} | {t:12} | {c:,} records')
        
        # Check for gold/crypto/commodities by asset_type
        print('\n=== Commodities/Crypto/Forex by Asset Type ===')
        result = await session.execute(text("""
            SELECT symbol, asset_type, COUNT(*) as cnt, MIN(date) as min_d, MAX(date) as max_d
            FROM market_data
            WHERE asset_type IN ('commodity', 'crypto', 'forex')
            GROUP BY symbol, asset_type
            ORDER BY cnt DESC
        """))
        commodities = result.fetchall()
        await session.commit()
        
        if commodities:
            for s, t, c, min_d, max_d in commodities:
                print(f'{s:15} | {t:12} | {c:,} records | {min_d} to {max_d}')
        else:
            print('No commodity/crypto/forex data found by asset_type')
        
        # Search by symbol patterns (gold, silver, btc, etc)
        print('\n=== Search for Gold/Silver/Crypto Symbols ===')
        result = await session.execute(text("""
            SELECT symbol, asset_type, COUNT(*) as cnt, MIN(date) as min_d, MAX(date) as max_d
            FROM market_data
            WHERE UPPER(symbol) LIKE '%GOLD%' 
               OR UPPER(symbol) LIKE '%GLD%' 
               OR UPPER(symbol) LIKE '%XAU%'
               OR UPPER(symbol) LIKE '%SLV%'
               OR UPPER(symbol) LIKE '%SILVER%'
               OR UPPER(symbol) LIKE '%BTC%'
               OR UPPER(symbol) LIKE '%ETH%'
               OR UPPER(symbol) LIKE '%CRYPTO%'
            GROUP BY symbol, asset_type
            ORDER BY cnt DESC
        """))
        search_results = result.fetchall()
        await session.commit()
        
        if search_results:
            for s, t, c, min_d, max_d in search_results:
                print(f'{s:15} | {t:12} | {c:,} records | {min_d} to {max_d}')
        else:
            print('No gold/silver/crypto symbols found')
        
        # Check stress indices
        print('\n=== Stress Index Sources ===')
        result = await session.execute(text("""
            SELECT source, region, COUNT(*) as cnt, MIN(date) as min_d, MAX(date) as max_d
            FROM stress_indices
            GROUP BY source, region
            ORDER BY cnt DESC
        """))
        stress = result.fetchall()
        await session.commit()
        
        for src, reg, cnt, min_d, max_d in stress:
            print(f'{src:15} | {reg:5} | {cnt:,} records | {min_d} to {max_d}')
        
        # Check for VIX in market data
        print('\n=== VIX Data ===')
        result = await session.execute(text("""
            SELECT symbol, COUNT(*) as cnt, MIN(date) as min_d, MAX(date) as max_d
            FROM market_data
            WHERE UPPER(symbol) LIKE '%VIX%'
            GROUP BY symbol
            ORDER BY cnt DESC
        """))
        vix = result.fetchall()
        await session.commit()
        
        if vix:
            for s, c, min_d, max_d in vix:
                print(f'{s:15} | {c:,} records | {min_d} to {max_d}')
        else:
            print('No VIX data found')
        
        # Show all unique asset types
        print('\n=== Unique Asset Types ===')
        result = await session.execute(text("""
            SELECT asset_type, COUNT(*) as cnt
            FROM market_data
            GROUP BY asset_type
            ORDER BY cnt DESC
        """))
        types = result.fetchall()
        await session.commit()
        
        for t, c in types:
            print(f'{t:15} | {c:,} records')


if __name__ == '__main__':
    asyncio.run(main())
