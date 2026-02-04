#!/usr/bin/env python3
"""
Import multi-asset sentiment data:
- Crypto Reddit (4.7M posts from 50+ subreddits)
- Gold commodity news (10K headlines)
- Forex news (2.3K headlines with pre-labeled sentiment)
"""

import os
import sys
import csv
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

# Database connection - use docker exec instead
import subprocess

def run_sql(query):
    """Run SQL via docker exec."""
    result = subprocess.run(
        ['docker', 'exec', 'sentiment-db', 'psql', '-U', 'postgres', '-d', 'sentiment_db', '-c', query],
        capture_output=True, text=True
    )
    return result.stdout

def get_connection():
    """Get connection via docker network."""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="sentiment_db",
        user="postgres",
        password="password"  # From docker-compose
    )

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "kaggle"


def import_crypto_reddit():
    """Import crypto Reddit data from 50+ subreddits."""
    crypto_dir = DATA_DIR / "crypto"
    
    if not crypto_dir.exists():
        print("❌ Crypto data not found")
        return 0
    
    conn = get_connection()
    cur = conn.cursor()
    
    total_imported = 0
    subreddits = [d for d in crypto_dir.iterdir() if d.is_dir()]
    
    print(f"\n{'='*60}")
    print("IMPORTING CRYPTO REDDIT DATA")
    print(f"{'='*60}")
    print(f"Found {len(subreddits)} crypto subreddits")
    
    for subdir in sorted(subreddits):
        csv_file = subdir / "submission.csv"
        if not csv_file.exists():
            continue
        
        subreddit_name = subdir.name
        batch = []
        batch_size = 2000  # Smaller batches for large subreddits
        imported = 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        # Parse timestamp
                        created_ts = int(float(row.get('created', 0)))
                        if created_ts == 0:
                            continue
                        
                        created_at = datetime.fromtimestamp(created_ts, tz=timezone.utc)
                        
                        # Combine title and selftext
                        title = row.get('title', '') or ''
                        selftext = row.get('selftext', '') or ''
                        
                        # Remove null characters
                        title = title.replace('\x00', '')
                        selftext = selftext.replace('\x00', '')
                        
                        # Skip deleted/removed
                        if selftext in ['[deleted]', '[removed]', '']:
                            content = title
                        else:
                            content = f"{title}\n\n{selftext}" if selftext else title
                        
                        # Clean content of null chars
                        content = content.replace('\x00', '')
                        
                        if not content or len(content) < 10:
                            continue
                        
                        source_id = row.get('submission', row.get('id', ''))
                        
                        batch.append((
                            str(uuid.uuid4()),
                            'reddit',
                            f"crypto_{subreddit_name}_{source_id}",
                            'crypto',
                            created_at,
                            datetime.now(timezone.utc),
                            title[:500] if title else None,
                            content[:10000],
                            json.dumps({
                                'subreddit': subreddit_name,
                                'score': row.get('score', 0),
                                'num_comments': row.get('num_comments', 0),
                                'author': row.get('author', '')
                            }),
                            datetime.now(timezone.utc),
                            datetime.now(timezone.utc)
                        ))
                        
                        if len(batch) >= batch_size:
                            execute_values(
                                cur,
                                """INSERT INTO raw_texts 
                                   (id, source, source_id, asset_class, content_created_at, 
                                    collected_at, title, content, metadata, created_at, updated_at)
                                   VALUES %s
                                   ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL 
                                   DO NOTHING""",
                                batch
                            )
                            conn.commit()
                            imported += len(batch)
                            batch = []
                    
                    except Exception as e:
                        continue
                
                # Final batch
                if batch:
                    execute_values(
                        cur,
                        """INSERT INTO raw_texts 
                           (id, source, source_id, asset_class, content_created_at, 
                            collected_at, title, content, metadata, created_at, updated_at)
                           VALUES %s
                           ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL 
                           DO NOTHING""",
                        batch
                    )
                    conn.commit()
                    imported += len(batch)
        
        except Exception as e:
            print(f"  ⚠️  Error with {subreddit_name}: {e}")
            continue
        
        total_imported += imported
        print(f"  r/{subreddit_name}: {imported:,} posts")
    
    cur.close()
    conn.close()
    
    print(f"\n✅ Total crypto posts imported: {total_imported:,}")
    return total_imported


def import_gold_commodity():
    """Import gold commodity news headlines."""
    gold_file = DATA_DIR / "commodity-gold" / "gold-dataset-sinha-khandait.csv"
    
    if not gold_file.exists():
        print("❌ Gold commodity data not found")
        return 0
    
    print(f"\n{'='*60}")
    print("IMPORTING GOLD COMMODITY DATA")
    print(f"{'='*60}")
    
    conn = get_connection()
    cur = conn.cursor()
    
    batch = []
    imported = 0
    
    with open(gold_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Parse date (format: DD-MM-YYYY)
                date_str = row.get('Dates', '')
                try:
                    created_at = datetime.strptime(date_str, '%d-%m-%Y').replace(tzinfo=timezone.utc)
                except:
                    continue
                
                news = row.get('News', '')
                if not news or len(news) < 10:
                    continue
                
                # Pre-labeled sentiment
                sentiment = row.get('Price Sentiment', '')
                
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
                        'pre_labeled_sentiment': sentiment,
                        'url': row.get('URL', ''),
                        'price_direction_up': row.get('Price Direction Up', ''),
                        'price_direction_down': row.get('Price Direction Down', '')
                    }),
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
                imported += 1
                
            except Exception as e:
                continue
    
    if batch:
        execute_values(
            cur,
            """INSERT INTO raw_texts 
               (id, source, source_id, asset_class, content_created_at, 
                collected_at, title, content, metadata, created_at, updated_at)
               VALUES %s
               ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL 
               DO NOTHING""",
            batch
        )
        conn.commit()
    
    cur.close()
    conn.close()
    
    print(f"✅ Gold headlines imported: {imported:,}")
    return imported


def import_forex_news():
    """Import forex news with pre-labeled sentiment."""
    forex_file = DATA_DIR / "forex" / "forex_sentiment_zenodo.csv"
    
    if not forex_file.exists():
        print("❌ Forex data not found")
        return 0
    
    print(f"\n{'='*60}")
    print("IMPORTING FOREX NEWS DATA")
    print(f"{'='*60}")
    
    conn = get_connection()
    cur = conn.cursor()
    
    batch = []
    imported = 0
    
    with open(forex_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Parse datetime
                date_str = row.get('published_at', '')
                try:
                    created_at = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                except:
                    continue
                
                title = row.get('title', '')
                text = row.get('text', '')
                content = f"{title}\n\n{text}" if text else title
                
                if not content or len(content) < 10:
                    continue
                
                ticker = row.get('ticker', '')
                true_sentiment = row.get('true_sentiment', '')
                finbert_sentiment = row.get('finbert_sentiment', '')
                finbert_score = row.get('finbert_sent_score', '')
                
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
                        'ticker': ticker,
                        'forex_pair': ticker,
                        'true_sentiment': true_sentiment,
                        'finbert_sentiment': finbert_sentiment,
                        'finbert_score': finbert_score,
                        'source': row.get('source', ''),
                        'author': row.get('author', ''),
                        'url': row.get('url', '')
                    }),
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ))
                imported += 1
                
            except Exception as e:
                continue
    
    if batch:
        execute_values(
            cur,
            """INSERT INTO raw_texts 
               (id, source, source_id, asset_class, content_created_at, 
                collected_at, title, content, metadata, created_at, updated_at)
               VALUES %s
               ON CONFLICT (source, source_id) WHERE source_id IS NOT NULL 
               DO NOTHING""",
            batch
        )
        conn.commit()
    
    cur.close()
    conn.close()
    
    print(f"✅ Forex headlines imported: {imported:,}")
    return imported


def show_summary():
    """Show asset class distribution after import."""
    conn = get_connection()
    cur = conn.cursor()
    
    print(f"\n{'='*60}")
    print("UPDATED ASSET CLASS DISTRIBUTION")
    print(f"{'='*60}")
    
    cur.execute("""
        SELECT 
            asset_class,
            COUNT(*) as count,
            ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) as pct
        FROM raw_texts 
        GROUP BY asset_class
        ORDER BY count DESC
    """)
    
    for row in cur.fetchall():
        print(f"  {row[0]:12} {row[1]:>10,} texts ({row[2]:>5.2f}%)")
    
    cur.execute("SELECT COUNT(*) FROM raw_texts")
    total = cur.fetchone()[0]
    print(f"\n  {'TOTAL':12} {total:>10,} texts")
    
    cur.close()
    conn.close()


def main():
    print("\n" + "="*60)
    print("MULTI-ASSET DATA IMPORT")
    print("="*60)
    
    # Import each asset class
    crypto_count = import_crypto_reddit()
    gold_count = import_gold_commodity()
    forex_count = import_forex_news()
    
    # Show summary
    show_summary()
    
    print(f"\n{'='*60}")
    print("IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"  Crypto:    {crypto_count:,} posts")
    print(f"  Gold:      {gold_count:,} headlines")
    print(f"  Forex:     {forex_count:,} headlines")
    print(f"  TOTAL NEW: {crypto_count + gold_count + forex_count:,}")


if __name__ == "__main__":
    main()
