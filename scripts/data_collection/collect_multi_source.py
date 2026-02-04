#!/usr/bin/env python3
"""
Multi-Source Data Collection Pipeline for Sentiment Regime Detector.

Collects financial text data from multiple sources:
- X/Twitter (real-time, requires Bearer Token)
- RSS Feeds (real-time, no API key needed)
- Kaggle datasets (historical Reddit data)
- NewsAPI (if configured)

Usage:
    python scripts/collect_multi_source.py --sources twitter,rss,kaggle --output data/raw/multi_source.json
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
load_dotenv()


async def collect_twitter(
    limit_per_asset: int = 50,
) -> list[dict]:
    """Collect tweets from X/Twitter."""
    from sentiment_detector.collectors.twitter import TwitterCollector
    
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token or bearer_token == "your_twitter_bearer_token":
        print("⚠️  X/Twitter: Bearer token not configured (skipping)")
        print("   Set TWITTER_BEARER_TOKEN in .env to enable")
        return []
    
    print("\n🐦 Collecting from X/Twitter...")
    collector = TwitterCollector(bearer_token=bearer_token)
    
    try:
        results = await collector.collect_all_assets(limit_per_asset=limit_per_asset)
        
        items = []
        for asset_class, collected in results.items():
            for item in collected:
                items.append({
                    "id": item.source_id,
                    "source": "twitter",
                    "asset_class": item.asset_class.value,
                    "created_at": item.created_at.isoformat(),
                    "title": item.title,
                    "content": item.content,
                    "metadata": item.metadata,
                })
        
        print(f"   ✅ Collected {len(items)} tweets")
        return items
        
    except Exception as e:
        print(f"   ❌ Twitter error: {e}")
        return []
    finally:
        await collector.close()


async def collect_rss(
    limit_per_asset: int = 50,
) -> list[dict]:
    """Collect from RSS feeds."""
    from sentiment_detector.collectors.rss import RSSCollector
    
    print("\n📰 Collecting from RSS feeds...")
    collector = RSSCollector()
    
    try:
        results = await collector.collect_all_assets(limit_per_asset=limit_per_asset)
        
        items = []
        for asset_class, collected in results.items():
            for item in collected:
                items.append({
                    "id": item.source_id,
                    "source": "rss",
                    "asset_class": item.asset_class.value,
                    "created_at": item.created_at.isoformat(),
                    "title": item.title,
                    "content": item.content,
                    "metadata": item.metadata,
                })
        
        print(f"   ✅ Collected {len(items)} RSS items")
        return items
        
    except Exception as e:
        print(f"   ❌ RSS error: {e}")
        return []
    finally:
        await collector.close()


def collect_kaggle(
    data_dir: str = "data/kaggle",
    limit: int = 1000,
) -> list[dict]:
    """Load data from Kaggle datasets."""
    from sentiment_detector.collectors.kaggle_loader import KaggleDataLoader
    
    print(f"\n📊 Loading Kaggle data from {data_dir}...")
    
    data_path = Path(data_dir)
    if not data_path.exists() or not any(data_path.glob("**/*.csv")) and not any(data_path.glob("**/*.json")):
        print("   ⚠️  No Kaggle data found")
        print("   📥 To download Kaggle datasets, run:")
        print("      python -m sentiment_detector.collectors.kaggle_loader")
        return []
    
    loader = KaggleDataLoader(data_dir)
    
    try:
        collected = loader.load_all(limit=limit)
        
        items = []
        for item in collected:
            items.append({
                "id": item.source_id,
                "source": "kaggle",
                "asset_class": item.asset_class.value,
                "created_at": item.created_at.isoformat(),
                "title": item.title,
                "content": item.content,
                "metadata": item.metadata,
            })
        
        print(f"   ✅ Loaded {len(items)} Kaggle items")
        return items
        
    except Exception as e:
        print(f"   ❌ Kaggle error: {e}")
        return []


async def collect_news(
    days: int = 7,
    limit_per_asset: int = 50,
) -> list[dict]:
    """Collect from NewsAPI."""
    # Check if NewsAPI collector exists and key is configured
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key or api_key == "your_newsapi_key":
        print("\n📰 NewsAPI: API key not configured (skipping)")
        print("   Get a free key at https://newsapi.org/")
        return []
    
    print("\n📰 Collecting from NewsAPI...")
    
    try:
        from sentiment_detector.collectors.news import NewsCollector
        collector = NewsCollector(api_key=api_key)
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        from sentiment_detector.collectors.base import AssetClass
        
        items = []
        for asset_class in AssetClass:
            try:
                collected = await collector.collect(
                    asset_class=asset_class,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit_per_asset,
                )
                for item in collected:
                    items.append({
                        "id": item.source_id,
                        "source": "news",
                        "asset_class": item.asset_class.value,
                        "created_at": item.created_at.isoformat(),
                        "title": item.title,
                        "content": item.content,
                        "metadata": item.metadata,
                    })
            except Exception as e:
                print(f"   ⚠️  Error collecting {asset_class}: {e}")
        
        print(f"   ✅ Collected {len(items)} news articles")
        return items
        
    except ImportError:
        print("   ⚠️  NewsAPI collector not available")
        return []
    except Exception as e:
        print(f"   ❌ NewsAPI error: {e}")
        return []


async def main():
    parser = argparse.ArgumentParser(
        description="Multi-source financial data collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect from all sources
  python scripts/collect_multi_source.py --sources all
  
  # Collect from specific sources
  python scripts/collect_multi_source.py --sources twitter,rss
  
  # Collect with custom limits
  python scripts/collect_multi_source.py --sources rss --limit 100
        """,
    )
    parser.add_argument(
        "--sources",
        type=str,
        default="all",
        help="Comma-separated list of sources: twitter,rss,kaggle,news,all (default: all)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Items per source/asset (default: 100)"
    )
    parser.add_argument(
        "--kaggle-dir",
        type=str,
        default="data/kaggle",
        help="Directory containing Kaggle datasets"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/multi_source.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Days of data to collect for real-time sources"
    )
    
    args = parser.parse_args()
    
    # Parse sources
    if args.sources == "all":
        sources = ["twitter", "rss", "kaggle", "news"]
    else:
        sources = [s.strip().lower() for s in args.sources.split(",")]
    
    print("=" * 60)
    print("🚀 Multi-Source Data Collection Pipeline")
    print("=" * 60)
    print(f"   Sources: {', '.join(sources)}")
    print(f"   Limit per source: {args.limit}")
    print(f"   Output: {args.output}")
    
    all_items = []
    source_stats = {}
    
    # Collect from each source
    if "twitter" in sources:
        items = await collect_twitter(limit_per_asset=args.limit // 4)
        all_items.extend(items)
        source_stats["twitter"] = len(items)
    
    if "rss" in sources:
        items = await collect_rss(limit_per_asset=args.limit // 4)
        all_items.extend(items)
        source_stats["rss"] = len(items)
    
    if "kaggle" in sources:
        items = collect_kaggle(data_dir=args.kaggle_dir, limit=args.limit)
        all_items.extend(items)
        source_stats["kaggle"] = len(items)
    
    if "news" in sources:
        items = await collect_news(days=args.days, limit_per_asset=args.limit // 4)
        all_items.extend(items)
        source_stats["news"] = len(items)
    
    # Compute asset class distribution
    asset_stats = {}
    for item in all_items:
        asset = item.get("asset_class", "unknown")
        asset_stats[asset] = asset_stats.get(asset, 0) + 1
    
    # Prepare output
    output_data = {
        "collection_timestamp": datetime.utcnow().isoformat(),
        "sources_collected": list(source_stats.keys()),
        "source_stats": source_stats,
        "asset_stats": asset_stats,
        "total_items": len(all_items),
        "items": all_items,
    }
    
    # Save to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, default=str)
    
    file_size_mb = output_path.stat().st_size / (1024 * 1024)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Collection Summary")
    print("=" * 60)
    
    print("\n📡 By Source:")
    for source, count in source_stats.items():
        print(f"   {source:12} {count:,} items")
    
    print("\n📈 By Asset Class:")
    for asset, count in sorted(asset_stats.items()):
        print(f"   {asset:12} {count:,} items")
    
    print(f"\n💾 Output: {output_path}")
    print(f"   Size: {file_size_mb:.2f} MB")
    print(f"   Total: {len(all_items):,} items")
    
    if len(all_items) > 0:
        print("\n" + "=" * 60)
        print("📤 Next: Upload to MANEFRAME for batch processing")
        print("=" * 60)
        print(f"\nscp {output_path} jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/data/raw/")
    
    print("\n✅ Collection complete!")
    
    return output_data


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Collection interrupted")
        sys.exit(1)
