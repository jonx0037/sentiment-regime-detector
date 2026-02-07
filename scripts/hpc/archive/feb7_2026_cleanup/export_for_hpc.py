#!/usr/bin/env python3
"""
Export new texts for HPC (ManeFrame) sentiment analysis.

Exports texts that don't have DistilBERT/FinBERT sentiment scores
to JSON batches for processing on SMU's ManeFrame cluster.
"""

import json
import psycopg2
from pathlib import Path
from datetime import datetime

DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
OUTPUT_DIR = Path('data/hpc_batches')
BATCH_SIZE = 50000  # 50K texts per batch file


def export_for_hpc():
    """Export unscored texts for HPC processing."""
    print("=" * 60)
    print("EXPORTING TEXTS FOR HPC SENTIMENT ANALYSIS")
    print("=" * 60)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Get texts without DistilBERT/FinBERT scores
    print("Finding texts without transformer-based sentiment...")
    cur.execute('''
        SELECT rt.id, rt.content, rt.content_created_at, rt.source_id
        FROM raw_texts rt
        LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id 
            AND ss.model_name IN ('distilbert-sst2', 'ProsusAI/finbert', 'ensemble_finbert_roberta')
        WHERE ss.id IS NULL
        ORDER BY rt.content_created_at
    ''')
    
    texts = cur.fetchall()
    total = len(texts)
    print(f"Found {total:,} texts to process")
    
    if total == 0:
        print("No texts to export!")
        return
    
    # Export in batches
    batch_num = 0
    batch = []
    
    for text_id, content, created_at, source_id in texts:
        batch.append({
            'id': str(text_id),
            'content': content[:5000],  # Truncate for processing
            'created_at': str(created_at),
            'source_id': source_id,
        })
        
        if len(batch) >= BATCH_SIZE:
            batch_file = OUTPUT_DIR / f'batch_{batch_num:04d}.json'
            with open(batch_file, 'w') as f:
                json.dump(batch, f)
            print(f"  Saved {batch_file} ({len(batch):,} texts)")
            batch_num += 1
            batch = []
    
    # Save remaining
    if batch:
        batch_file = OUTPUT_DIR / f'batch_{batch_num:04d}.json'
        with open(batch_file, 'w') as f:
            json.dump(batch, f)
        print(f"  Saved {batch_file} ({len(batch):,} texts)")
        batch_num += 1
    
    conn.close()
    
    print(f"\n{'=' * 60}")
    print(f"EXPORT COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total texts: {total:,}")
    print(f"Batch files: {batch_num}")
    print(f"Output dir: {OUTPUT_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Copy {OUTPUT_DIR}/ to ManeFrame")
    print(f"  2. Run: sbatch scripts/hpc/process_sentiment.slurm")
    print(f"  3. Import results with: python scripts/import_hpc_sentiment.py")


if __name__ == "__main__":
    export_for_hpc()
