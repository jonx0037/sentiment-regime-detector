#!/usr/bin/env python3
"""Check 2008 Financial Crisis sentiment data availability."""

import psycopg2
from datetime import datetime

def main():
    conn = psycopg2.connect('postgresql://postgres:password@localhost:5432/sentiment_db')
    cur = conn.cursor()

    # Check Sep-Nov 2008 data (peak crisis period)
    cur.execute('''
        SELECT DATE(t.content_created_at) as day, COUNT(*) as texts,
               AVG(ss.compound) as avg_sentiment,
               MIN(ss.compound) as min_sent,
               MAX(ss.compound) as max_sent
        FROM raw_texts t
        JOIN sentiment_scores ss ON t.id = ss.text_id
        WHERE t.content_created_at >= '2008-09-01' AND t.content_created_at < '2008-12-01'
        GROUP BY DATE(t.content_created_at)
        ORDER BY day
    ''')
    results = cur.fetchall()
    
    print(f"Days with sentiment data in Sep-Nov 2008: {len(results)}")
    if results:
        print(f"Date range: {results[0][0]} to {results[-1][0]}")
        print(f"Total texts: {sum(r[1] for r in results)}")
        
        print("\nFirst 10 days:")
        for r in results[:10]:
            print(f"  {r[0]}: {r[1]:3d} texts, avg_sentiment={r[2]:.3f}")
        
        print("\nLast 10 days:")
        for r in results[-10:]:
            print(f"  {r[0]}: {r[1]:3d} texts, avg_sentiment={r[2]:.3f}")
            
        # Find the most negative sentiment days
        print("\nMost negative sentiment days (should correlate with crisis peaks):")
        sorted_by_sent = sorted(results, key=lambda x: x[2])
        for r in sorted_by_sent[:10]:
            print(f"  {r[0]}: avg_sentiment={r[2]:.3f} ({r[1]} texts)")
    else:
        print("No data found for Sep-Nov 2008!")
    
    conn.close()

if __name__ == "__main__":
    main()
