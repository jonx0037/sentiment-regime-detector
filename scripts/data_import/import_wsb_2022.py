#!/usr/bin/env python3
"""
Import WSB 2022-2025 Data

Import the gpreda/wallstreetbets-2022 dataset covering 2022-2025.
This fills the gap between our 2020 data and present.

Key events this covers:
- 2022 Rate Hikes / Bear Market
- 2023 Bank Crisis (SVB)
- 2024-2025 Recent data
"""

import uuid
import json
import psycopg2
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

# Configuration
DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
DATA_FILE = Path('data/kaggle/wsb-2022/wallstreetbets_2022.csv')
BATCH_SIZE = 5000


def import_wsb_2022():
    """Import WSB 2022-2025 data."""
    print("=" * 60)
    print("IMPORTING WSB 2022-2025 DATA")
    print("=" * 60)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Check existing data
    cur.execute("SELECT COUNT(*) FROM raw_texts WHERE source = 'reddit' AND source_id LIKE 'wsb22_%'")
    existing = cur.fetchone()[0]
    print(f"Existing WSB 2022+ posts: {existing:,}")
    
    # Read CSV in chunks
    print(f"\nReading from: {DATA_FILE}")
    
    imported = 0
    skipped = 0
    batch = []
    
    for chunk_num, chunk in enumerate(pd.read_csv(DATA_FILE, chunksize=10000)):
        if chunk_num % 10 == 0:
            print(f"  Processing chunk {chunk_num}...")
        
        for _, row in chunk.iterrows():
            try:
                # Parse timestamp
                timestamp = pd.to_datetime(row['timestamp'])
                if pd.isna(timestamp):
                    skipped += 1
                    continue
                
                # Combine title and body
                title = str(row.get('title', '') or '')
                body = str(row.get('body', '') or '')
                
                # Skip comments that are just "Comment"
                if title == 'Comment':
                    title = ''
                
                content = f"{title}\n\n{body}".strip()
                
                # Skip empty/short content
                if len(content) < 10:
                    skipped += 1
                    continue
                
                post = {
                    'id': str(uuid.uuid4()),
                    'source': 'reddit',
                    'source_id': f"wsb22_{row.get('id', '')}",
                    'asset_class': 'equity',
                    'content_created_at': timestamp.to_pydatetime().replace(tzinfo=timezone.utc),
                    'collected_at': datetime.now(timezone.utc),
                    'title': title[:500] if title else None,
                    'content': content[:10000],
                    'metadata': json.dumps({
                        'subreddit': 'wallstreetbets',
                        'score': int(row.get('score', 0)) if pd.notna(row.get('score')) else 0,
                        'comms_num': int(row.get('comms_num', 0)) if pd.notna(row.get('comms_num')) else 0,
                    })
                }
                
                batch.append(post)
                
                if len(batch) >= BATCH_SIZE:
                    imported += insert_batch(cur, batch)
                    conn.commit()
                    batch = []
                    
            except Exception as e:
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
    print(f"Posts skipped: {skipped:,}")
    
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
            continue
    
    return inserted


if __name__ == "__main__":
    import_wsb_2022()
