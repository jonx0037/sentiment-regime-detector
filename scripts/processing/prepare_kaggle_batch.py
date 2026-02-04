#!/usr/bin/env python3
"""
Prepare full Kaggle datasets for MANEFRAME batch processing.

This script:
1. Loads all Kaggle datasets (RedditNews, DJIA, Crypto, WSB)
2. Deduplicates and cleans the data
3. Exports to JSON format for MANEFRAME processing
4. Provides statistics and summary

Total estimated data:
- RedditNews: ~76K rows
- DJIA Combined News: ~4K rows  
- Crypto Tweets: ~36K rows
- WSB Posts: ~400K rows

Usage:
    python scripts/prepare_kaggle_batch.py [--limit N] [--output-dir DIR]
"""

import argparse
import json
import logging
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional
import hashlib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.collectors.kaggle_loader import KaggleDataLoader
from sentiment_detector.collectors.base import CollectedItem, AssetClass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def deduplicate_items(items: list[CollectedItem]) -> list[CollectedItem]:
    """Remove duplicate items based on content hash."""
    seen_hashes = set()
    unique_items = []
    
    for item in items:
        # Create hash of content
        content_hash = hashlib.md5(item.content.lower().encode()).hexdigest()
        
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_items.append(item)
    
    logger.info(f"Deduplicated: {len(items)} → {len(unique_items)} items ({len(items) - len(unique_items)} duplicates removed)")
    return unique_items


def export_for_maneframe(
    items: list[CollectedItem],
    output_path: Path,
    batch_size: int = 10000,
) -> list[Path]:
    """
    Export items to JSON files for MANEFRAME processing.
    
    Args:
        items: List of CollectedItem objects
        output_path: Directory to save batches
        batch_size: Items per batch file
        
    Returns:
        List of created batch file paths
    """
    output_path.mkdir(parents=True, exist_ok=True)
    
    batch_files = []
    num_batches = (len(items) + batch_size - 1) // batch_size
    
    for i in range(num_batches):
        start = i * batch_size
        end = min(start + batch_size, len(items))
        batch = items[start:end]
        
        # Convert to serializable format
        batch_data = []
        for item in batch:
            batch_data.append({
                "source_id": item.source_id,
                "source": item.source.value if hasattr(item.source, 'value') else str(item.source),
                "asset_class": item.asset_class.value if hasattr(item.asset_class, 'value') else str(item.asset_class),
                "content": item.content,
                "title": item.title,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "metadata": item.metadata,
            })
        
        batch_file = output_path / f"batch_{i+1:04d}_of_{num_batches:04d}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        batch_files.append(batch_file)
        logger.info(f"Created {batch_file.name}: {len(batch)} items")
    
    return batch_files


def print_statistics(items: list[CollectedItem], title: str = "Dataset Statistics"):
    """Print statistics about the collected items."""
    print(f"\n{'='*70}")
    print(f" {title}")
    print('='*70)
    
    # Count by asset class
    asset_counts = Counter(item.asset_class for item in items)
    print(f"\n📊 By Asset Class:")
    for asset, count in sorted(asset_counts.items(), key=lambda x: -x[1]):
        asset_name = asset.value if hasattr(asset, 'value') else str(asset)
        pct = count / len(items) * 100
        print(f"   {asset_name:12}: {count:>8,} ({pct:>5.1f}%)")
    
    # Count by source
    source_counts = Counter(item.source for item in items)
    print(f"\n📰 By Source:")
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        source_name = source.value if hasattr(source, 'value') else str(source)
        pct = count / len(items) * 100
        print(f"   {source_name:12}: {count:>8,} ({pct:>5.1f}%)")
    
    # Dataset breakdown from metadata
    dataset_counts = Counter(
        item.metadata.get('dataset', item.metadata.get('source_file', 'unknown'))
        for item in items
    )
    print(f"\n📁 By Dataset:")
    for dataset, count in sorted(dataset_counts.items(), key=lambda x: -x[1]):
        pct = count / len(items) * 100
        print(f"   {dataset:25}: {count:>8,} ({pct:>5.1f}%)")
    
    # Date range
    dates = [item.created_at for item in items if item.created_at]
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        print(f"\n📅 Date Range: {min_date.date()} to {max_date.date()}")
    
    # Content length stats
    lengths = [len(item.content) for item in items]
    avg_len = sum(lengths) / len(lengths) if lengths else 0
    print(f"\n📝 Content Length:")
    print(f"   Average: {avg_len:,.0f} characters")
    print(f"   Min: {min(lengths):,}, Max: {max(lengths):,}")
    
    print(f"\n{'='*70}")
    print(f" Total Items: {len(items):,}")
    print('='*70 + '\n')


def main():
    parser = argparse.ArgumentParser(description="Prepare Kaggle data for MANEFRAME")
    parser.add_argument("--limit", type=int, default=None, help="Limit total items (for testing)")
    parser.add_argument("--output-dir", type=str, default="data/processed/maneframe_batches", help="Output directory")
    parser.add_argument("--batch-size", type=int, default=10000, help="Items per batch file")
    parser.add_argument("--dataset", type=str, default="all", 
                        choices=["all", "reddit_news", "djia", "crypto", "wsb"],
                        help="Which dataset to process")
    args = parser.parse_args()
    
    # Initialize loader
    data_dir = Path(__file__).parent.parent / "data" / "kaggle"
    loader = KaggleDataLoader(data_dir)
    
    all_items = []
    
    print("\n🚀 Loading Kaggle Datasets...")
    print("=" * 70)
    
    # Load specific datasets
    if args.dataset in ["all", "reddit_news"]:
        reddit_news_path = data_dir / "stocknews" / "RedditNews.csv"
        if reddit_news_path.exists():
            print(f"\n📰 Loading Reddit News ({reddit_news_path.name})...")
            items = loader.load_reddit_news(reddit_news_path, limit=args.limit)
            print(f"   Loaded {len(items):,} items")
            all_items.extend(items)
        else:
            print(f"   ⚠️  Not found: {reddit_news_path}")
    
    if args.dataset in ["all", "djia"]:
        djia_path = data_dir / "stocknews" / "Combined_News_DJIA.csv"
        if djia_path.exists():
            print(f"\n📈 Loading DJIA Combined News ({djia_path.name})...")
            items = loader.load_djia_news(djia_path, limit=args.limit)
            print(f"   Loaded {len(items):,} items")
            all_items.extend(items)
        else:
            print(f"   ⚠️  Not found: {djia_path}")
    
    if args.dataset in ["all", "crypto"]:
        crypto_dir = data_dir / "crypto-tweets"
        if crypto_dir.exists():
            for csv_file in crypto_dir.glob("*.csv"):
                print(f"\n🪙 Loading Crypto Tweets ({csv_file.name})...")
                items = loader.load_crypto_tweets(csv_file, limit=args.limit)
                print(f"   Loaded {len(items):,} items")
                all_items.extend(items)
    
    if args.dataset in ["all", "wsb"]:
        wsb_path = data_dir / "wsb" / "reddit_wsb.csv"
        if wsb_path.exists():
            print(f"\n🎰 Loading WSB Posts ({wsb_path.name})...")
            # WSB is large, load with custom loader
            items = loader.load_csv(
                wsb_path,
                title_col="title",
                body_col="body",
                date_col="timestamp",
                score_col="score",
                limit=args.limit,
            )
            print(f"   Loaded {len(items):,} items")
            all_items.extend(items)
        else:
            print(f"   ⚠️  Not found: {wsb_path}")
    
    if not all_items:
        print("\n❌ No items loaded. Check that Kaggle data exists in data/kaggle/")
        return 1
    
    # Deduplicate
    print(f"\n🔄 Deduplicating {len(all_items):,} items...")
    all_items = deduplicate_items(all_items)
    
    # Print statistics
    print_statistics(all_items, "Full Kaggle Dataset Statistics")
    
    # Export for MANEFRAME
    output_dir = Path(args.output_dir)
    print(f"\n📦 Exporting to {output_dir}...")
    batch_files = export_for_maneframe(all_items, output_dir, args.batch_size)
    
    # Summary
    print(f"\n✅ Export Complete!")
    print(f"   Created {len(batch_files)} batch files in {output_dir}")
    print(f"   Total items: {len(all_items):,}")
    
    # Print rsync command for MANEFRAME
    print(f"\n📤 To upload to MANEFRAME, run:")
    print(f"   rsync -avz {output_dir}/ jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/data/batches/")
    
    # Estimate processing time
    texts_per_sec = 346.9  # From your V100 benchmark
    estimated_time = len(all_items) / texts_per_sec
    print(f"\n⏱️  Estimated MANEFRAME processing time: {estimated_time/60:.1f} minutes ({estimated_time:.0f} seconds)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
