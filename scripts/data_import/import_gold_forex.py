#!/usr/bin/env python3
"""Quick import for gold and forex data only."""

import csv
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "kaggle"

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="sentiment_db",
        user="postgres",
        password="password"
    )

def import_gold():
    """Import gold commodity news."""
    gold_file = DATA_DIR / "commodity-gold" / "gold-dataset-sinha-khandait.csv"
    if not gold_file.exists():
        print("❌ Gold data not found")
        return 0
    
    print("Importing Gold commodity data...")
    conn = get_connection()
    cur = conn.cursor()
    batch = []
    
    with open(gold_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Handle BOM in column name
                date_str = row.get('Dates') or row.get('\ufeffDates', '')
                created_at = datetime.strptime(date_str, '%d-%m-%Y').replace(tzinfo=timezone.utc)
                news = row.get('News', '').replace('\x00', '')
                if not news or len(news) < 10:
                    continue
                
                batch.append((
                    str(uuid.uuid4()),
                    'news',
                    f"gold_{hash(news) % 10000000}",
                    'commodity',
                    created_at,
                    datetime.now(timezone.utc),
                    news[:500],
                    news,
                    json.dumps({
                        'commodity': 'gold',
                        'pre_labeled_sentiment': row.get('Price Sentiment', '')
                    }),
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
            except:
                continue
    
    if batch:
        execute_values(cur, """
            INSERT INTO raw_texts (id, source, source_id, asset_class, content_created_at, 
                collected_at, title, content, metadata, created_at, updated_at)
            VALUES %s ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL DO NOTHING
        """, batch)
        conn.commit()
    
    cur.close()
    conn.close()
    print(f"✅ Gold: {len(batch)} headlines imported")
    return len(batch)

def import_forex():
    """Import forex news."""
    forex_file = DATA_DIR / "forex" / "forex_sentiment_zenodo.csv"
    if not forex_file.exists():
        print("❌ Forex data not found")
        return 0
    
    print("Importing Forex data...")
    conn = get_connection()
    cur = conn.cursor()
    batch = []
    
    with open(forex_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date_str = row.get('published_at', '')
                created_at = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                title = row.get('title', '').replace('\x00', '')
                text = row.get('text', '').replace('\x00', '')
                content = f"{title}\n\n{text}" if text else title
                if not content or len(content) < 10:
                    continue
                
                batch.append((
                    str(uuid.uuid4()),
                    'news',
                    f"forex_{hash(title) % 10000000}",
                    'forex',
                    created_at,
                    datetime.now(timezone.utc),
                    title[:500],
                    content[:10000],
                    json.dumps({
                        'ticker': row.get('ticker', ''),
                        'true_sentiment': row.get('true_sentiment', ''),
                        'finbert_sentiment': row.get('finbert_sentiment', ''),
                        'finbert_score': row.get('finbert_sent_score', '')
                    }),
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
            except:
                continue
    
    if batch:
        execute_values(cur, """
            INSERT INTO raw_texts (id, source, source_id, asset_class, content_created_at, 
                collected_at, title, content, metadata, created_at, updated_at)
            VALUES %s ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL DO NOTHING
        """, batch)
        conn.commit()
    
    cur.close()
    conn.close()
    print(f"✅ Forex: {len(batch)} headlines imported")
    return len(batch)

if __name__ == "__main__":
    import_gold()
    import_forex()
