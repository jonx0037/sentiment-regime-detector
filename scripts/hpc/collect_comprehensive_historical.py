#!/usr/bin/env python3
"""
Comprehensive historical data collection using ALL configured collectors and API keys.

Uses the existing collector infrastructure from src/sentiment_detector/collectors/
to collect from all available sources:
- Twitter/X (with Bearer Token)
- Reddit (with client credentials)
- RSS Feeds (no auth needed)
- NewsAPI (with API key)
- Market data (Finhub, Tiingo, CoinAPI)
"""

import argparse
import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Load environment variables
load_dotenv()


async def collect_all_sources(start_date: datetime, end_date: datetime, output_dir: Path, batch_id: int):
    """Collect from all configured sources for the given date range."""

    print("=" * 80)
    print(f"COMPREHENSIVE DATA COLLECTION - Batch {batch_id}")
    print("=" * 80)
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print(f"Output: {output_dir}")
    print("=" * 80)

    all_data = []

    # 1. Twitter/X Collection
    twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
    if twitter_token and twitter_token != "your_twitter_bearer_token":
        try:
            from sentiment_detector.collectors.twitter import TwitterCollector
            print("\n🐦 Collecting from Twitter/X...")

            collector = TwitterCollector(bearer_token=twitter_token)
            # Collect for each asset class
            results = await collector.collect_all_assets(
                start_date=start_date,
                end_date=end_date,
                limit=1000  # per asset class
            )

            for asset_class, items in results.items():
                for item in items:
                    all_data.append({
                        'date': item.created_at,
                        'source': 'twitter',
                        'asset_class': asset_class.value,
                        'text': item.content,
                        'title': item.title,
                        'metadata': item.metadata
                    })

            await collector.close()
            print(f"  ✅ Collected {len([d for d in all_data if d['source'] == 'twitter'])} tweets")
        except Exception as e:
            print(f"  ❌ Twitter error: {e}")
    else:
        print("\n⚠️  Twitter/X: Bearer token not configured, skipping")

    # 2. Reddit Collection (using your reddit.py collector, not Pushshift)
    reddit_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if reddit_id and reddit_id != "your_reddit_client_id":
        try:
            from sentiment_detector.collectors.reddit import RedditCollector
            print("\n🔴 Collecting from Reddit...")

            collector = RedditCollector(
                client_id=reddit_id,
                client_secret=reddit_secret,
                user_agent="sentiment-regime-detector:v1.0"
            )

            results = await collector.collect_all_assets(
                start_date=start_date,
                end_date=end_date,
                limit=1000  # per asset class
            )

            for asset_class, items in results.items():
                for item in items:
                    all_data.append({
                        'date': item.created_at,
                        'source': 'reddit',
                        'asset_class': asset_class.value,
                        'text': item.content,
                        'title': item.title,
                        'metadata': item.metadata
                    })

            await collector.close()
            print(f"  ✅ Collected {len([d for d in all_data if d['source'] == 'reddit'])} posts")
        except Exception as e:
            print(f"  ❌ Reddit error: {e}")
    else:
        print("\n⚠️  Reddit: Client credentials not configured, skipping")

    # 3. RSS Feeds
    try:
        from sentiment_detector.collectors.rss import RSSCollector
        print("\n📰 Collecting from RSS feeds...")

        collector = RSSCollector()
        results = await collector.collect_all_assets(
            start_date=start_date,
            end_date=end_date,
            limit=500
        )

        for asset_class, items in results.items():
            for item in items:
                all_data.append({
                    'date': item.created_at,
                    'source': 'rss',
                    'asset_class': asset_class.value,
                    'text': item.content,
                    'title': item.title,
                    'metadata': item.metadata
                })

        await collector.close()
        print(f"  ✅ Collected {len([d for d in all_data if d['source'] == 'rss'])} articles")
    except Exception as e:
        print(f"  ❌ RSS error: {e}")

    # 4. NewsAPI
    newsapi_key = os.getenv("NEWS_API_KEY")
    if newsapi_key and newsapi_key != "your_newsapi_key":
        try:
            from sentiment_detector.collectors.news import NewsCollector
            print("\n📡 Collecting from NewsAPI...")

            collector = NewsCollector(api_key=newsapi_key)
            results = await collector.collect_all_assets(
                start_date=start_date,
                end_date=end_date,
                limit=500
            )

            for asset_class, items in results.items():
                for item in items:
                    all_data.append({
                        'date': item.created_at,
                        'source': 'newsapi',
                        'asset_class': asset_class.value,
                        'text': item.content,
                        'title': item.title,
                        'metadata': item.metadata
                    })

            await collector.close()
            print(f"  ✅ Collected {len([d for d in all_data if d['source'] == 'newsapi'])} articles")
        except Exception as e:
            print(f"  ❌ NewsAPI error: {e}")
    else:
        print("\n⚠️  NewsAPI: Key not configured, skipping")

    # 5. Market Data (Finhub, Tiingo, CoinAPI)
    # Note: These are typically for price/volume data, not text sentiment
    # Add if needed for your analysis

    # Save results
    if all_data:
        df = pd.DataFrame(all_data)
        output_file = output_dir / f"comprehensive_batch_{batch_id:04d}.parquet"
        df.to_parquet(output_file, index=False)

        print("\n" + "=" * 80)
        print(f"✅ COLLECTION COMPLETE")
        print(f"   Total texts: {len(df):,}")
        print(f"   Sources: {df['source'].value_counts().to_dict()}")
        print(f"   Saved to: {output_file}")
        print("=" * 80)
    else:
        print("\n⚠️  No data collected from any source!")


async def main():
    parser = argparse.ArgumentParser(description="Comprehensive historical data collection")
    parser.add_argument("--start-date", type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    parser.add_argument("--batch-id", type=int, required=True, help="Batch ID")

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    await collect_all_sources(start_date, end_date, output_dir, args.batch_id)


if __name__ == "__main__":
    asyncio.run(main())
