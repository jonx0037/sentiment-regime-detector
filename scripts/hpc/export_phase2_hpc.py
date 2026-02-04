#!/usr/bin/env python3
"""
Export Phase 2 texts for HPC processing: Reddit Backfill.

Phase 2 handles the ~613K Reddit texts lacking sentiment scores.
These are batched into 50K chunks for efficient GPU processing.

Estimated HPC time: ~2.2 hours
"""

import json
import sys
from pathlib import Path
from datetime import datetime

import psycopg2

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.core.config import get_settings

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "hpc_batches" / "phase2"
BATCH_SIZE = 50000  # 50K texts per batch


def export_reddit_backfill():
    """Export all Reddit texts lacking sentiment scores."""
    settings = get_settings()
    # Convert SQLAlchemy URL to standard PostgreSQL format for psycopg2
    db_url = str(settings.database_url)
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    db_url = db_url.replace("postgresql+psycopg2://", "postgresql://")
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    print("Counting Reddit texts without sentiment scores...")
    
    # Count first
    # Note: 'source' is a column in raw_texts, not a separate table
    cur.execute("""
        SELECT COUNT(*)
        FROM raw_texts rt
        LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id
        WHERE rt.source = 'reddit'
          AND ss.id IS NULL
    """)
    total_count = cur.fetchone()[0]
    print(f"  Found {total_count:,} Reddit texts to export")
    
    if total_count == 0:
        print("No texts to export!")
        return
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Export in batches using cursor pagination
    print(f"\nExporting in batches of {BATCH_SIZE:,}...")
    
    batch_num = 0
    offset = 0
    total_exported = 0
    
    while offset < total_count:
        cur.execute("""
            SELECT rt.id, rt.content, rt.content_created_at, rt.source
            FROM raw_texts rt
            LEFT JOIN sentiment_scores ss ON rt.id = ss.text_id
            WHERE rt.source = 'reddit'
              AND ss.id IS NULL
            ORDER BY rt.content_created_at
            LIMIT %s OFFSET %s
        """, (BATCH_SIZE, offset))
        
        rows = cur.fetchall()
        if not rows:
            break
        
        items = []
        for text_id, content, created_at, source in rows:
            items.append({
                "id": str(text_id),
                "content": content[:5000] if content else "",
                "created_at": str(created_at) if created_at else None,
                "source_id": None,
                "source": "reddit",
                "phase": "2_reddit_backfill"
            })
        
        # Save batch
        batch_file = OUTPUT_DIR / f"phase2_batch_{batch_num:04d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump({
                "exported_at": datetime.now().isoformat(),
                "phase": 2,
                "batch_number": batch_num,
                "count": len(items),
                "items": items
            }, f, default=str)
        
        total_exported += len(items)
        print(f"  Batch {batch_num:04d}: {len(items):,} texts ({total_exported:,}/{total_count:,})")
        
        batch_num += 1
        offset += BATCH_SIZE
    
    conn.close()
    
    # Calculate totals
    total_size_mb = sum(f.stat().st_size for f in OUTPUT_DIR.glob("*.json")) / 1024 / 1024
    est_minutes = total_exported / 4650
    
    print()
    print("=" * 70)
    print("PHASE 2 EXPORT COMPLETE")
    print("=" * 70)
    print(f"Total texts exported: {total_exported:,}")
    print(f"Number of batches:    {batch_num}")
    print(f"Total size:           {total_size_mb:.1f} MB")
    print(f"Estimated GPU time:   {est_minutes:.0f} minutes (~{est_minutes/60:.1f} hours)")
    print()
    print("Output directory:", OUTPUT_DIR)
    
    # Create manifest
    manifest = {
        "exported_at": datetime.now().isoformat(),
        "phase": 2,
        "description": "Reddit backfill - texts without sentiment scores",
        "total_texts": total_exported,
        "num_batches": batch_num,
        "batch_size": BATCH_SIZE,
        "estimated_gpu_minutes": est_minutes,
        "batches": [f"phase2_batch_{i:04d}.json" for i in range(batch_num)]
    }
    
    manifest_file = OUTPUT_DIR / "manifest.json"
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"Manifest saved to: {manifest_file}")
    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Package for transfer:")
    print("   tar -czvf hpc_phase2.tar.gz data/hpc_batches/phase2/")
    print()
    print("2. Transfer to ManeFrame:")
    print("   scp hpc_phase2.tar.gz jarocha@m3.smu.edu:/lustre/scratch/users/jarocha/")
    print()
    print("3. Submit job on ManeFrame:")
    print("   sbatch scripts/hpc/process_phase2.slurm")


if __name__ == "__main__":
    print("=" * 70)
    print("PHASE 2 HPC EXPORT: Reddit Backfill (~613K texts)")
    print("=" * 70)
    print()
    export_reddit_backfill()
