#!/usr/bin/env python3
"""Check data coverage for potential backtest events."""

import psycopg2
from datetime import datetime

DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'

# Historical events with approximate dates
EVENTS = [
    ('Flash Crash', '2010-05-01', '2010-05-31'),
    ('2011 Debt Ceiling', '2011-07-15', '2011-08-31'),
    ('2015 China Devaluation', '2015-08-01', '2015-09-15'),
    ('Brexit Referendum', '2016-06-01', '2016-07-15'),
    ('COVID Crash', '2020-02-15', '2020-04-15'),
    ('GameStop (already done)', '2021-01-15', '2021-02-15'),
]

def main():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("DATA COVERAGE FOR POTENTIAL BACKTESTS")
    print("=" * 70)
    
    for event, start, end in EVENTS:
        cur.execute('''
            SELECT COUNT(*), 
                   COUNT(DISTINCT DATE(content_created_at)) as days
            FROM raw_texts t
            JOIN sentiment_scores ss ON t.id = ss.text_id
            WHERE content_created_at >= %s AND content_created_at < %s
        ''', (start, end))
        
        count, days = cur.fetchone()
        
        if days and days > 0:
            avg_per_day = count / days
        else:
            avg_per_day = 0
        
        status = "✓" if count > 100 else "✗"
        print(f"{status} {event:25s}: {count:6d} texts over {days or 0:3d} days ({avg_per_day:.0f}/day)")
    
    # Also check what sources we have
    print("\n" + "=" * 70)
    print("DATA SOURCES BREAKDOWN")
    print("=" * 70)
    
    cur.execute('''
        SELECT source, 
               MIN(DATE(content_created_at)) as earliest,
               MAX(DATE(content_created_at)) as latest,
               COUNT(*) as count
        FROM raw_texts
        GROUP BY source
        ORDER BY earliest
    ''')
    
    for source, earliest, latest, count in cur.fetchall():
        print(f"{source:20s}: {earliest} to {latest} ({count:,} texts)")
    
    conn.close()

if __name__ == "__main__":
    main()
