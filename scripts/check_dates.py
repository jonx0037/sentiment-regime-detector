#!/usr/bin/env python3
"""Check date distribution in database."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv
load_dotenv()

async def check():
    url = os.getenv('DATABASE_URL', '').replace('postgresql+asyncpg://', 'postgresql://')
    conn = await asyncpg.connect(url)
    
    # Check date distribution
    rows = await conn.fetch('''
        SELECT 
            EXTRACT(YEAR FROM content_created_at) as year,
            COUNT(*) as count
        FROM raw_texts
        WHERE content_created_at IS NOT NULL
        GROUP BY EXTRACT(YEAR FROM content_created_at)
        ORDER BY year
    ''')
    print('Texts by Year:')
    for r in rows:
        print(f'  {int(r["year"])}: {r["count"]:,}')
    
    # Check sentiment indices date range
    rows2 = await conn.fetch('''
        SELECT 
            MIN(period_start) as earliest,
            MAX(period_start) as latest,
            COUNT(DISTINCT period_start::date) as days
        FROM sentiment_indices
        WHERE source IS NULL
    ''')
    print(f'\nIndex Coverage:')
    print(f'  Earliest: {rows2[0]["earliest"]}')
    print(f'  Latest: {rows2[0]["latest"]}')
    print(f'  Total days: {rows2[0]["days"]}')
    
    # Sample of indices
    rows3 = await conn.fetch('''
        SELECT asset_class, period_start::date, mean_compound, sample_count
        FROM sentiment_indices
        WHERE source IS NULL
        ORDER BY period_start
        LIMIT 10
    ''')
    print('\nSample Indices (earliest):')
    for r in rows3:
        print(f'  {r["period_start"]}: {r["asset_class"]:12} sentiment={r["mean_compound"]:.4f} samples={r["sample_count"]}')
    
    await conn.close()

asyncio.run(check())
