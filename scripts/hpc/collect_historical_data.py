#!/usr/bin/env python3
"""Collect comprehensive historical financial text data for sentiment analysis.

This script coordinates distributed data collection across multiple sources:
1. GDELT financial news (2008-2026)
2. Reddit archives via Pushshift (2008-2026)
3. NewsAPI historical (if API key available)
4. Twitter/X financial archives (if accessible)

Designed to run on HPC with parallel collection across date ranges.

Usage:
    python collect_historical_data.py --start-date 2008-01-01 --end-date 2026-02-06 \
        --sources gdelt,reddit --output /work/$USER/historical_data
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import aiohttp
import pandas as pd
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class HistoricalDataCollector:
    """Collects historical financial text data from multiple sources."""

    def __init__(self, output_dir: Path):
        """Initialize collector.

        Args:
            output_dir: Directory to save collected data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def collect_gdelt_news(
        self,
        start_date: datetime,
        end_date: datetime,
        keywords: list[str]
    ) -> pd.DataFrame:
        """Collect financial news from GDELT project.

        GDELT provides free access to global news coverage.

        Args:
            start_date: Start date for collection
            end_date: End date for collection
            keywords: Financial keywords to filter

        Returns:
            DataFrame with collected news articles (English only)
        """
        print(f"\n📰 Collecting GDELT news: {start_date.date()} to {end_date.date()}")

        # GDELT DOC 2.0 API endpoint
        base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

        articles = []
        current_date = start_date
        english_count = 0
        total_fetched = 0

        # Collect day by day
        pbar = tqdm(total=(end_date - start_date).days, desc="GDELT collection")

        while current_date <= end_date:
            try:
                # Build query for financial news (English only)
                # Add sourcelang:english to filter for English articles
                query = f"sourcelang:english ({' OR '.join(keywords)})"
                date_str = current_date.strftime("%Y%m%d")

                params = {
                    "query": query,
                    "mode": "artlist",
                    "maxrecords": 250,  # Max per request
                    "format": "json",
                    "startdatetime": f"{date_str}000000",
                    "enddatetime": f"{date_str}235959"
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(base_url, params=params, timeout=30) as resp:
                        if resp.status == 200:
                            data = await resp.json()

                            if "articles" in data:
                                total_fetched += len(data["articles"])
                                for article in data["articles"]:
                                    # Double-check language is English
                                    lang = article.get("language", "").lower()
                                    if lang in ["english", "en"]:
                                        articles.append({
                                            "date": current_date,
                                            "source": "gdelt",
                                            "title": article.get("title", ""),
                                            "text": article.get("title", ""),  # Use title as text
                                            "url": article.get("url", ""),
                                            "domain": article.get("domain", ""),
                                            "language": lang
                                        })
                                        english_count += 1
                        else:
                            # Log non-200 responses
                            error_text = await resp.text()
                            print(f"  ⚠️ HTTP {resp.status} on {current_date.date()}: {error_text[:100]}")

                # Rate limiting
                await asyncio.sleep(1)

            except asyncio.TimeoutError:
                print(f"  ⏱️  Timeout on {current_date.date()} - API not responding")
            except aiohttp.ClientError as e:
                print(f"  🔌 Network error on {current_date.date()}: {e}")
            except Exception as e:
                print(f"  ❌ Error on {current_date.date()}: {type(e).__name__}: {e}")

            current_date += timedelta(days=1)
            pbar.update(1)

        pbar.close()

        df = pd.DataFrame(articles)
        print(f"  ✓ Collected {len(df):,} English GDELT articles (filtered from {total_fetched:,} total)")

        return df

    async def collect_reddit_pushshift(
        self,
        start_date: datetime,
        end_date: datetime,
        subreddits: list[str],
        max_posts_per_sub: int = 5000  # Target posts per subreddit
    ) -> pd.DataFrame:
        """Collect Reddit posts via Pushshift archives with pagination.

        Args:
            start_date: Start date for collection
            end_date: End date for collection
            subreddits: List of subreddits to collect from
            max_posts_per_sub: Maximum posts to collect per subreddit

        Returns:
            DataFrame with collected Reddit posts
        """
        print(f"\n🗨️  Collecting Reddit posts: {start_date.date()} to {end_date.date()}")

        # Pushshift API endpoint
        base_url = "https://api.pullpush.io/reddit/search/submission"

        posts = []

        for subreddit in subreddits:
            print(f"  Collecting r/{subreddit}...")
            sub_posts = 0
            max_attempts = 10  # Limit pagination attempts

            after = int(start_date.timestamp())
            before = int(end_date.timestamp())

            # Paginate through results
            for attempt in range(max_attempts):
                try:
                    params = {
                        "subreddit": subreddit,
                        "after": after,
                        "before": before,
                        "size": 1000,  # Max per request
                        "sort": "desc",
                        "sort_type": "created_utc"
                    }

                    async with aiohttp.ClientSession() as session:
                        async with session.get(base_url, params=params, timeout=60) as resp:
                            if resp.status == 200:
                                data = await resp.json()

                                if "data" in data and len(data["data"]) > 0:
                                    batch_count = 0
                                    for post in data["data"]:
                                        # Combine title + selftext
                                        text = f"{post.get('title', '')} {post.get('selftext', '')}"

                                        posts.append({
                                            "date": datetime.fromtimestamp(post.get("created_utc", 0)),
                                            "source": "reddit",
                                            "subreddit": subreddit,
                                            "title": post.get("title", ""),
                                            "text": text.strip(),
                                            "score": post.get("score", 0),
                                            "num_comments": post.get("num_comments", 0),
                                            "author": post.get("author", ""),
                                            "url": f"https://reddit.com{post.get('permalink', '')}"
                                        })
                                        batch_count += 1

                                    sub_posts += batch_count

                                    # Update 'before' for pagination (get older posts)
                                    if len(data["data"]) > 0:
                                        # Use the oldest post's timestamp for next request
                                        before = data["data"][-1].get("created_utc", before) - 1

                                    # Check if we've hit our target
                                    if sub_posts >= max_posts_per_sub:
                                        print(f"    Reached target of {max_posts_per_sub} posts")
                                        break

                                    # If we got fewer than requested, we've reached the end
                                    if len(data["data"]) < 1000:
                                        print(f"    No more posts available ({sub_posts} total)")
                                        break
                                else:
                                    # No more data available
                                    print(f"    No more posts available ({sub_posts} total)")
                                    break
                            elif resp.status == 429:
                                # Rate limited
                                print(f"    ⏱️  Rate limited, waiting 60s...")
                                await asyncio.sleep(60)
                                continue
                            else:
                                error_text = await resp.text()
                                print(f"    ⚠️ HTTP {resp.status}: {error_text[:100]}")
                                break

                    # Rate limiting between requests
                    await asyncio.sleep(2)

                except asyncio.TimeoutError:
                    print(f"    ⏱️  Timeout on attempt {attempt + 1}")
                    await asyncio.sleep(5)
                except aiohttp.ClientError as e:
                    print(f"    🔌 Network error: {e}")
                    break
                except Exception as e:
                    print(f"    ❌ Error: {type(e).__name__}: {e}")
                    break

            print(f"    Collected {sub_posts} posts from r/{subreddit}")

        df = pd.DataFrame(posts)
        print(f"  ✓ Collected {len(df):,} Reddit posts total")

        return df

    async def collect_newsapi(
        self,
        start_date: datetime,
        end_date: datetime,
        api_key: str
    ) -> pd.DataFrame:
        """Collect news via NewsAPI (requires paid plan for historical).

        Args:
            start_date: Start date for collection
            end_date: End date for collection
            api_key: NewsAPI key

        Returns:
            DataFrame with collected news
        """
        print(f"\n📰 Collecting NewsAPI articles: {start_date.date()} to {end_date.date()}")

        if not api_key:
            print("  ⚠️  No API key provided, skipping NewsAPI")
            return pd.DataFrame()

        base_url = "https://newsapi.org/v2/everything"

        articles = []
        current_date = start_date

        keywords = ["stock market", "financial crisis", "economy", "recession", "bitcoin", "crypto"]

        while current_date <= end_date:
            try:
                params = {
                    "q": " OR ".join(keywords),
                    "from": current_date.strftime("%Y-%m-%d"),
                    "to": current_date.strftime("%Y-%m-%d"),
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": 100,
                    "apiKey": api_key
                }

                async with aiohttp.ClientSession() as session:
                    async with session.get(base_url, params=params, timeout=30) as resp:
                        if resp.status == 200:
                            data = await resp.json()

                            if "articles" in data:
                                for article in data["articles"]:
                                    articles.append({
                                        "date": current_date,
                                        "source": "newsapi",
                                        "title": article.get("title", ""),
                                        "text": article.get("description", ""),
                                        "url": article.get("url", ""),
                                        "author": article.get("author", ""),
                                        "published_at": article.get("publishedAt", "")
                                    })
                        else:
                            error_text = await resp.text()
                            print(f"  ⚠️ HTTP {resp.status} on {current_date.date()}: {error_text[:100]}")

                # Rate limiting (NewsAPI has strict limits)
                await asyncio.sleep(1)

            except asyncio.TimeoutError:
                print(f"  ⏱️  Timeout on {current_date.date()}")
            except aiohttp.ClientError as e:
                print(f"  🔌 Network error on {current_date.date()}: {e}")
            except Exception as e:
                print(f"  ❌ Error on {current_date.date()}: {type(e).__name__}: {e}")

            current_date += timedelta(days=1)

        df = pd.DataFrame(articles)
        print(f"  ✓ Collected {len(df):,} NewsAPI articles")

        return df

    def save_batch(self, df: pd.DataFrame, source: str, batch_id: int):
        """Save collected data batch to disk.

        Args:
            df: DataFrame to save
            source: Data source name
            batch_id: Batch identifier
        """
        output_file = self.output_dir / f"{source}_batch_{batch_id:04d}.parquet"
        df.to_parquet(output_file, index=False)
        print(f"  💾 Saved to: {output_file}")


async def main():
    """Run historical data collection."""
    parser = argparse.ArgumentParser(
        description="Collect historical financial text data"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        required=True,
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        required=True,
        help="End date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--sources",
        type=str,
        default="gdelt,reddit",
        help="Comma-separated list of sources (gdelt,reddit,newsapi)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory for collected data"
    )
    parser.add_argument(
        "--newsapi-key",
        type=str,
        default=None,
        help="NewsAPI key (for newsapi source)"
    )
    parser.add_argument(
        "--batch-id",
        type=int,
        default=0,
        help="Batch ID for parallel processing"
    )

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    print("🔍 HISTORICAL DATA COLLECTION")
    print("=" * 60)
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print(f"Sources: {args.sources}")
    print(f"Output: {args.output}")
    print("=" * 60)

    collector = HistoricalDataCollector(Path(args.output))

    sources = args.sources.split(",")

    # Collect from each source
    all_data = []

    if "gdelt" in sources:
        gdelt_data = await collector.collect_gdelt_news(
            start_date,
            end_date,
            keywords=["stock market", "financial crisis", "recession", "economy"]
        )
        if not gdelt_data.empty:
            all_data.append(gdelt_data)
            collector.save_batch(gdelt_data, "gdelt", args.batch_id)

    if "reddit" in sources:
        reddit_data = await collector.collect_reddit_pushshift(
            start_date,
            end_date,
            subreddits=["wallstreetbets", "stocks", "investing", "economics", "bitcoin"]
        )
        if not reddit_data.empty:
            all_data.append(reddit_data)
            collector.save_batch(reddit_data, "reddit", args.batch_id)

    if "newsapi" in sources and args.newsapi_key:
        newsapi_data = await collector.collect_newsapi(
            start_date,
            end_date,
            args.newsapi_key
        )
        if not newsapi_data.empty:
            all_data.append(newsapi_data)
            collector.save_batch(newsapi_data, "newsapi", args.batch_id)

    # Combine and save
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        collector.save_batch(combined, "combined", args.batch_id)

        print("\n" + "=" * 60)
        print(f"✅ Collection complete: {len(combined):,} total texts")
        print("=" * 60)
    else:
        print("\n⚠️  No data collected")


if __name__ == "__main__":
    asyncio.run(main())
