#!/usr/bin/env python3
"""
Import Historical WSB Data (2012-2020)

Import the shergreen/wallstreetbets-subreddit-submissions dataset
to fill the gap between DJIA news (ending 2016) and GameStop era (2021).

Key events this covers:
- 2018 Volmageddon (Feb 2018)
- 2018 Q4 Selloff (Oct-Dec 2018)
- COVID Crash (Feb-Apr 2020)
"""

import json
import uuid
import psycopg2
from datetime import datetime, timezone
from pathlib import Path
import sys

# Configuration
DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
DATA_FILE = Path('data/kaggle/wsb-historical/wallstreetbets_submission.json')

# Events to focus on (we'll import all, but prioritize sentiment for these)
TARGET_EVENTS = [
    ('2018 Volmageddon', '2018-01-25', '2018-02-28'),
    ('2018 Q4 Selloff', '2018-10-01', '2018-12-31'),
    ('COVID Crash', '2020-02-15', '2020-04-15'),
]

BATCH_SIZE = 1000


def parse_post(line: str) -> dict:
    """Parse a single JSON line into a post dict."""
    data = json.loads(line)
    
    # Combine title and selftext
    title = data.get('title', '') or ''
    selftext = data.get('selftext', '') or ''
    
    # Skip deleted/removed content
    if selftext in ['[deleted]', '[removed]']:
        selftext = ''
    
    content = f"{title}\n\n{selftext}".strip()
    
    # Skip empty content
    if len(content) < 10:
        return None
    
    # Parse timestamp
    created_utc = data.get('created_utc', 0)
    created_at = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    
    return {
        'id': str(uuid.uuid4()),
        'source': 'reddit',
        'source_id': f"wsb_{data.get('id', '')}",
        'asset_class': 'equity',
        'content_created_at': created_at,
        'collected_at': datetime.now(timezone.utc),
        'title': title[:500] if title else None,
        'content': content[:10000],  # Truncate very long posts
        'metadata': json.dumps({
            'subreddit': 'wallstreetbets',
            'score': data.get('score', 0),
            'num_comments': data.get('num_comments', 0),
            'author': data.get('author', ''),
        })
    }


def import_wsb_data(start_date: str = None, end_date: str = None):
    """Import WSB data, optionally filtered by date range."""
    print("=" * 60)
    print("IMPORTING HISTORICAL WSB DATA (2012-2020)")
    print("=" * 60)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Check existing data
    cur.execute("SELECT COUNT(*) FROM raw_texts WHERE source = 'reddit' AND source_id LIKE 'wsb_%'")
    existing = cur.fetchone()[0]
    print(f"Existing WSB historical posts: {existing:,}")
    
    # Parse date filters
    start_ts = None
    end_ts = None
    if start_date:
        start_ts = datetime.strptime(start_date, '%Y-%m-%d').timestamp()
    if end_date:
        end_ts = datetime.strptime(end_date, '%Y-%m-%d').timestamp()
    
    print(f"\nReading from: {DATA_FILE}")
    if start_date:
        print(f"Date filter: {start_date} to {end_date or 'end'}")
    
    # Process file
    imported = 0
    skipped = 0
    duplicates = 0
    batch = []
    
    with open(DATA_FILE) as f:
        for i, line in enumerate(f):
            if i % 50000 == 0:
                print(f"  Processing line {i:,}...")
            
            try:
                data = json.loads(line)
                created_utc = data.get('created_utc', 0)
                
                # Apply date filter
                if start_ts and created_utc < start_ts:
                    continue
                if end_ts and created_utc > end_ts:
                    continue
                
                post = parse_post(line)
                if not post:
                    skipped += 1
                    continue
                
                batch.append(post)
                
                if len(batch) >= BATCH_SIZE:
                    imported += insert_batch(cur, batch)
                    conn.commit()
                    batch = []
                    
            except json.JSONDecodeError:
                skipped += 1
                continue
    
    # Insert remaining
    if batch:
        imported += insert_batch(cur, batch)
        conn.commit()
    
    conn.close()
    
    print(f"\n{'=' * 60}")
    print(f"IMPORT COMPLETE")
    print(f"{'=' * 60}")
    print(f"Posts imported: {imported:,}")
    print(f"Posts skipped (empty/short): {skipped:,}")
    
    return imported


def insert_batch(cur, batch: list) -> int:
    """Insert a batch of posts, handling duplicates."""
    inserted = 0
    
    for post in batch:
        try:
            cur.execute('''
                INSERT INTO raw_texts 
                (id, source, source_id, asset_class, content_created_at, 
                 collected_at, title, content, metadata, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL
                DO NOTHING
            ''', (
                post['id'], post['source'], post['source_id'], 
                post['asset_class'], post['content_created_at'],
                post['collected_at'], post['title'], post['content'],
                post['metadata']
            ))
            if cur.rowcount > 0:
                inserted += 1
        except Exception as e:
            print(f"Error inserting: {e}")
            continue
    
    return inserted


def check_coverage():
    """Check data coverage for target events after import."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("\n" + "=" * 60)
    print("DATA COVERAGE CHECK")
    print("=" * 60)
    
    for name, start, end in TARGET_EVENTS:
        cur.execute('''
            SELECT COUNT(*), COUNT(DISTINCT DATE(content_created_at))
            FROM raw_texts
            WHERE content_created_at >= %s AND content_created_at < %s
        ''', (start, end))
        count, days = cur.fetchone()
        days = days or 0
        per_day = count / days if days > 0 else 0
        status = "✓" if count > 100 else "✗"
        print(f"{status} {name:<20}: {count:>6,} texts over {days:>3} days ({per_day:.1f}/day)")
    
    conn.close()


if __name__ == "__main__":
    # Import all data (or filter by command line args)
    if len(sys.argv) > 2:
        import_wsb_data(sys.argv[1], sys.argv[2])
    else:
        import_wsb_data()
    
    check_coverage()
