#!/usr/bin/env python3
"""
Export Phase 1 texts for HPC processing: News + WSB Echo Chamber.

Phase 1 focuses on high-priority new/unprocessed data:
- News source: 14,924 texts at 0% coverage
- WSB Echo Chamber: New dataset not yet in database

This creates a single batch file for quick GPU processing (~5 min).
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import psycopg2

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.core.config import get_settings

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "hpc_batches" / "phase1"


def export_news_texts() -> list:
    """Export all news texts that lack sentiment scores."""
    settings = get_settings()
    # Convert SQLAlchemy URL to standard PostgreSQL format for psycopg2
    db_url = str(settings.database_url)
    # Remove the driver specification
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    db_url = db_url.replace("postgresql+psycopg2://", "postgresql://")
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("Exporting news texts without sentiment scores...")
    
    # Get news texts without any sentiment scores
    # Note: 'source' is a column in raw_texts, not a separate table
    cur.execute("""
        SELECT rt.id, rt.content, rt.content_created_at, rt.source
        FROM raw_texts rt
        LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id
        WHERE rt.source = 'news'
          AND ss.id IS NULL
        ORDER BY rt.content_created_at
    """)
    
    texts = cur.fetchall()
    print(f"  Found {len(texts):,} news texts")
    
    items = []
    for text_id, content, created_at, source in texts:
        items.append({
            "id": str(text_id),
            "content": content[:5000] if content else "",
            "created_at": str(created_at) if created_at else None,
            "source_id": None,
            "source": "news",
            "phase": "1_news"
        })
    
    conn.close()
    return items


def export_wsb_echo_chamber() -> list:
    """
    Export WSB Echo Chamber data directly from JSON files.
    This data is not yet in the database.
    """
    WSB_BASE = Path(__file__).parent.parent / "data" / "kaggle" / "wsb-echo-chamber"
    TICKERS = ["GME", "AMC", "TSLA", "AAPL", "MSFT", "NOK"]
    
    print("Loading WSB Echo Chamber data...")
    
    items = []
    item_count = 0
    
    for ticker in TICKERS:
        ticker_dir = WSB_BASE / f"reddit_raw_{ticker}" / ticker
        
        if not ticker_dir.exists():
            print(f"  Warning: {ticker_dir} not found")
            continue
        
        for file_path in ticker_dir.iterdir():
            if not file_path.is_file():
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                
                if not content:
                    continue
                
                data = json.loads(content)
                
                if isinstance(data, dict):
                    # Data is structured as {field: {index: value}}
                    fields = list(data.keys())
                    if not fields:
                        continue
                    
                    first_field = data[fields[0]]
                    if isinstance(first_field, dict):
                        indices = list(first_field.keys())
                        
                        for idx in indices:
                            # Get selftext (main content) or title as fallback
                            text_content = ""
                            if "selftext" in data:
                                text_content = data["selftext"].get(idx, "")
                            if not text_content and "title" in data:
                                text_content = data["title"].get(idx, "")
                            
                            if not text_content or text_content in ("[removed]", "[deleted]"):
                                continue
                            
                            # Get creation time
                            created_utc = None
                            if "created_utc" in data:
                                try:
                                    ts = data["created_utc"].get(idx)
                                    if ts:
                                        created_utc = datetime.fromtimestamp(float(ts)).isoformat()
                                except (ValueError, TypeError):
                                    pass
                            
                            item_count += 1
                            items.append({
                                "id": f"wsb_{ticker}_{file_path.stem}_{idx}",
                                "content": text_content[:5000],
                                "created_at": created_utc,
                                "source_id": None,  # Not in DB yet
                                "source": "wsb_echo_chamber",
                                "ticker": ticker,
                                "phase": "1_wsb"
                            })
                    else:
                        # Single record format
                        text_content = data.get("selftext") or data.get("title") or ""
                        if text_content and text_content not in ("[removed]", "[deleted]"):
                            item_count += 1
                            items.append({
                                "id": f"wsb_{ticker}_{file_path.stem}",
                                "content": text_content[:5000],
                                "created_at": None,
                                "source_id": None,
                                "source": "wsb_echo_chamber",
                                "ticker": ticker,
                                "phase": "1_wsb"
                            })
            
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                # Skip malformed files
                continue
        
        print(f"  {ticker}: loaded {item_count - sum(1 for x in items if x.get('ticker') != ticker)} posts")
    
    print(f"  Total WSB Echo Chamber: {len(items):,} posts")
    return items


def main():
    print("=" * 70)
    print("PHASE 1 HPC EXPORT: News + WSB Echo Chamber")
    print("=" * 70)
    print()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Export news texts from database
    news_items = export_news_texts()
    
    # Export WSB Echo Chamber from files
    wsb_items = export_wsb_echo_chamber()
    
    # Combine for Phase 1
    all_items = news_items + wsb_items
    
    print()
    print("-" * 70)
    print(f"Phase 1 Summary:")
    print(f"  News texts:         {len(news_items):,}")
    print(f"  WSB Echo Chamber:   {len(wsb_items):,}")
    print(f"  Total:              {len(all_items):,}")
    print("-" * 70)
    
    if not all_items:
        print("No items to export!")
        return
    
    # Save to batch file
    batch_file = OUTPUT_DIR / "phase1_batch.json"
    with open(batch_file, "w", encoding="utf-8") as f:
        json.dump({
            "exported_at": datetime.now().isoformat(),
            "phase": 1,
            "description": "High-priority: News + WSB Echo Chamber",
            "count": len(all_items),
            "breakdown": {
                "news": len(news_items),
                "wsb_echo_chamber": len(wsb_items)
            },
            "items": all_items
        }, f, indent=2, default=str)
    
    print(f"\nSaved to: {batch_file}")
    print(f"File size: {batch_file.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Estimate processing time (based on 4,650 items/min)
    est_minutes = len(all_items) / 4650
    print(f"\nEstimated GPU processing time: {est_minutes:.1f} minutes")
    
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Package for transfer:")
    print("   tar -czvf hpc_phase1.tar.gz data/hpc_batches/phase1/")
    print()
    print("2. Transfer to ManeFrame:")
    print("   scp hpc_phase1.tar.gz jarocha@m3.smu.edu:/lustre/scratch/users/jarocha/")
    print()
    print("3. Submit job on ManeFrame:")
    print("   sbatch scripts/hpc/process_phase1.slurm")


if __name__ == "__main__":
    main()
