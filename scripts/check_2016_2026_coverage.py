#!/usr/bin/env python3
"""Check data coverage for 2016-2026 volatility events."""

import psycopg2

DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'

# Key volatility events 2016-2026
EVENTS = [
    ('Brexit', '2016-06-01', '2016-07-15'),
    ('2018 Volmageddon', '2018-01-25', '2018-02-28'),
    ('2018 Q4 Selloff', '2018-10-01', '2018-12-31'),
    ('COVID Crash', '2020-02-15', '2020-04-15'),
    ('COVID Recovery', '2020-04-01', '2020-06-30'),
    ('GameStop', '2021-01-15', '2021-02-15'),
    ('2022 Rate Hikes', '2022-01-01', '2022-06-30'),
    ('2022 Bear Market', '2022-06-01', '2022-10-31'),
    ('2023 Bank Crisis', '2023-03-01', '2023-03-31'),
    ('Recent 2024-2026', '2024-01-01', '2026-02-01'),
]

def main():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print('DATA COVERAGE FOR 2016-2026 EVENTS')
    print('=' * 70)
    print(f"{'Event':<25} | {'Texts':>8} | {'Days':>6} | {'Texts/Day':>10}")
    print('-' * 70)
    
    for name, start, end in EVENTS:
        cur.execute('''
            SELECT COUNT(*), COUNT(DISTINCT DATE(content_created_at))
            FROM raw_texts t
            JOIN sentiment_scores ss ON t.id = ss.text_id
            WHERE content_created_at >= %s AND content_created_at < %s
        ''', (start, end))
        count, days = cur.fetchone()
        days = days or 0
        per_day = count / days if days > 0 else 0
        status = '✓' if count > 100 else '✗'
        print(f"{status} {name:<23} | {count:>8,} | {days:>6} | {per_day:>10.1f}")
    
    # Also check by source
    print('\n' + '=' * 70)
    print('DATA BY SOURCE (2016-2026)')
    print('=' * 70)
    
    cur.execute('''
        SELECT source, 
               MIN(DATE(content_created_at)) as earliest,
               MAX(DATE(content_created_at)) as latest,
               COUNT(*) as count
        FROM raw_texts
        WHERE content_created_at >= '2016-01-01'
        GROUP BY source
        ORDER BY earliest
    ''')
    
    for source, earliest, latest, count in cur.fetchall():
        print(f"  {source:<15}: {earliest} to {latest} ({count:,} texts)")
    
    conn.close()

if __name__ == "__main__":
    main()
