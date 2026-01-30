#!/usr/bin/env python3
"""
Reddit Data Collection Script for Sentiment Regime Detector.

Collects posts from financial subreddits and saves to JSON for batch processing on MANEFRAME.

Usage:
    python scripts/collect_reddit_data.py --days 7 --limit 500 --output data/reddit_batch.json
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

# Load environment variables
load_dotenv()


def check_credentials():
    """Check if Reddit credentials are configured."""
    client_id = os.getenv("REDDIT_CLIENT_ID", "")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET", "")
    
    if client_id in ["your_reddit_client_id", ""] or client_secret in ["your_reddit_client_secret", ""]:
        print("=" * 60)
        print("❌ Reddit API credentials not configured!")
        print("=" * 60)
        print("\nTo set up Reddit API access:")
        print("1. Go to: https://www.reddit.com/prefs/apps")
        print("2. Click 'create another app...'")
        print("3. Select 'script' type")
        print("4. Name it: sentiment-regime-detector")
        print("5. Redirect URI: http://localhost:8080")
        print("6. Copy client_id and client_secret to .env file")
        print("\nEdit .env and update these lines:")
        print("  REDDIT_CLIENT_ID=your_actual_client_id")
        print("  REDDIT_CLIENT_SECRET=your_actual_client_secret")
        print("=" * 60)
        return False
    return True


async def collect_reddit_data(
    days: int = 7,
    limit_per_subreddit: int = 500,
    output_path: str = None,
):
    """
    Collect Reddit data from financial subreddits.
    
    Args:
        days: Number of days to look back
        limit_per_subreddit: Max posts per subreddit
        output_path: Path to save JSON output
    """
    from sentiment_detector.collectors.reddit import RedditCollector, SUBREDDIT_ASSETS
    from sentiment_detector.collectors.base import AssetClass
    
    # Initialize collector with credentials from .env
    collector = RedditCollector(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "sentiment-regime-detector:v1.0.0 (by /u/capstone_research)"),
    )
    
    # Date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    print(f"\n📊 Collecting Reddit data")
    print(f"   Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"   Limit per subreddit: {limit_per_subreddit}")
    print(f"   Subreddits: {list(SUBREDDIT_ASSETS.keys())}")
    print()
    
    # Health check
    print("🔍 Testing Reddit API connection...")
    try:
        is_healthy = await collector.health_check()
        if not is_healthy:
            print("❌ Reddit API health check failed!")
            return None
        print("✅ Reddit API connection successful!\n")
    except Exception as e:
        print(f"❌ Reddit API error: {e}")
        return None
    
    # Collect from all asset classes
    all_items = []
    stats = {
        "equity": 0,
        "crypto": 0,
        "forex": 0,
        "commodity": 0,
    }
    
    print("📥 Collecting posts...")
    results = await collector.collect_all_assets(
        start_date=start_date,
        end_date=end_date,
        limit_per_subreddit=limit_per_subreddit,
    )
    
    # Convert to JSON-serializable format
    for asset_class, items in results.items():
        asset_name = asset_class.value.lower()
        stats[asset_name] = len(items)
        
        for item in items:
            all_items.append({
                "id": item.source_id,
                "source": item.source.value,
                "asset_class": item.asset_class.value,
                "created_at": item.created_at.isoformat(),
                "title": item.title,
                "content": item.content,
                "metadata": item.metadata,
            })
    
    # Print collection stats
    print("\n" + "=" * 60)
    print("📈 Collection Summary")
    print("=" * 60)
    print(f"   Equity posts:    {stats['equity']:,}")
    print(f"   Crypto posts:    {stats['crypto']:,}")
    print(f"   Forex posts:     {stats['forex']:,}")
    print(f"   Commodity posts: {stats['commodity']:,}")
    print(f"   ─────────────────────────")
    print(f"   Total posts:     {len(all_items):,}")
    print("=" * 60)
    
    if not all_items:
        print("\n⚠️  No posts collected! Check your date range and subreddit access.")
        return None
    
    # Prepare output
    output_data = {
        "collection_timestamp": datetime.utcnow().isoformat(),
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
        },
        "stats": stats,
        "total_items": len(all_items),
        "items": all_items,
    }
    
    # Save to file
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        
        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"\n💾 Saved to: {output_file}")
        print(f"   File size: {file_size_mb:.2f} MB")
        
        # Print upload instructions
        print("\n" + "=" * 60)
        print("📤 Next Steps: Upload to MANEFRAME")
        print("=" * 60)
        print(f"\nRun this command to upload:")
        print(f"  scp {output_file} jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/data/raw/")
        print("\nThen on MANEFRAME:")
        print("  cd /lustre/scratch/client/users/jarocha/sentiment-detector")
        print("  source activate_env.sh")
        print("  sbatch run_sentiment_batch.sh")
        print("=" * 60)
    
    return output_data


def main():
    parser = argparse.ArgumentParser(
        description="Collect Reddit data for sentiment analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Collect last 7 days, 500 posts per subreddit
  python scripts/collect_reddit_data.py --days 7 --limit 500

  # Collect last 30 days for comprehensive analysis
  python scripts/collect_reddit_data.py --days 30 --limit 1000 --output data/reddit_30day.json
        """,
    )
    parser.add_argument(
        "--days", 
        type=int, 
        default=7,
        help="Number of days to look back (default: 7)"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=500,
        help="Max posts per subreddit (default: 500)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="data/raw/reddit_batch.json",
        help="Output JSON file path (default: data/raw/reddit_batch.json)"
    )
    
    args = parser.parse_args()
    
    # Check credentials first
    if not check_credentials():
        sys.exit(1)
    
    # Run collection
    try:
        asyncio.run(collect_reddit_data(
            days=args.days,
            limit_per_subreddit=args.limit,
            output_path=args.output,
        ))
    except KeyboardInterrupt:
        print("\n\n⚠️  Collection interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
