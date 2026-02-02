#!/usr/bin/env python3
"""
Batch Sentiment Analysis for Historical WSB Data

Uses VADER for fast processing (can handle 442K texts in minutes).
"""

import uuid
import psycopg2
from datetime import datetime, timezone
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
BATCH_SIZE = 5000
MODEL_NAME = 'vader'
MODEL_VERSION = '3.3.2'


def main():
    print("=" * 60)
    print("BATCH SENTIMENT ANALYSIS (VADER)")
    print("=" * 60)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Get texts without sentiment scores
    print("Finding texts without sentiment scores...")
    cur.execute('''
        SELECT rt.id, rt.content
        FROM raw_texts rt
        LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id
        WHERE ss.id IS NULL
        ORDER BY rt.content_created_at
    ''')
    
    texts = cur.fetchall()
    total = len(texts)
    print(f"Found {total:,} texts to analyze")
    
    if total == 0:
        print("No texts to process!")
        return
    
    # Initialize VADER
    analyzer = SentimentIntensityAnalyzer()
    
    processed = 0
    batch = []
    start_time = datetime.now()
    
    for text_id, content in texts:
        # Analyze sentiment
        scores = analyzer.polarity_scores(content[:5000])  # Truncate long texts
        
        batch.append({
            'id': str(uuid.uuid4()),
            'text_id': text_id,
            'model_name': MODEL_NAME,
            'model_version': MODEL_VERSION,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound'],
            'confidence': 1.0,
            'processed_at': datetime.now(timezone.utc),
        })
        
        if len(batch) >= BATCH_SIZE:
            insert_batch(cur, batch)
            conn.commit()
            processed += len(batch)
            
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = processed / elapsed
            remaining = (total - processed) / rate if rate > 0 else 0
            
            print(f"  Processed {processed:,}/{total:,} ({processed/total*100:.1f}%) "
                  f"- {rate:.0f} texts/sec - ETA: {remaining/60:.1f} min")
            batch = []
    
    # Process remaining
    if batch:
        insert_batch(cur, batch)
        conn.commit()
        processed += len(batch)
    
    conn.close()
    
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {processed:,} texts in {elapsed:.1f}s ({processed/elapsed:.0f} texts/sec)")
    print("=" * 60)


def insert_batch(cur, batch: list):
    """Insert sentiment scores batch."""
    for score in batch:
        cur.execute('''
            INSERT INTO sentiment_scores
            (id, text_id, model_name, model_version, positive, negative, 
             neutral, compound, confidence, processed_at, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            ON CONFLICT (text_id, model_name) DO NOTHING
        ''', (
            score['id'], score['text_id'], score['model_name'], 
            score['model_version'], score['positive'], score['negative'],
            score['neutral'], score['compound'], score['confidence'],
            score['processed_at']
        ))


if __name__ == "__main__":
    main()
