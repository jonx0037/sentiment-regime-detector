# Master Data Pipeline Orchestrator

```python
# data/data_pipeline.py
import pandas as pd
from datetime import datetime, timedelta
import json
from reddit_scraper import RedditScraper
from twitter_scraper import TwitterScraper
from news_scraper import NewsScraper

class DataPipeline:
    def __init__(self, config_file='config/api_keys.json'):
        """Initialize all scrapers with credentials."""
        with open(config_file, 'r') as f:
            creds = json.load(f)
        
        self.reddit = RedditScraper(
            client_id=creds['reddit']['client_id'],
            client_secret=creds['reddit']['client_secret'],
            user_agent=creds['reddit']['user_agent']
        )
        
        self.twitter = TwitterScraper(bearer_token=creds['twitter']['bearer_token'])
        self.news = NewsScraper(api_key=creds['newsapi']['api_key'])
    
    def collect_all_data(self, start_date, end_date):
        """
        Orchestrate data collection from all sources.
        
        Args:
            start_date: Start date (datetime object)
            end_date: End date (datetime object)
        """
        print(f"\n{'='*60}")
        print(f"DATA COLLECTION PIPELINE: {start_date} to {end_date}")
        print(f"{'='*60}\n")
        
        # 1. Collect Reddit data
        print("\n[1/3] Collecting Reddit data...")
        reddit_dfs = []
        subreddits = ['wallstreetbets', 'investing', 'stocks', 'cryptocurrency', 'forex']
        for sub in subreddits:
            df = self.reddit.scrape_subreddit(sub, start_date, end_date, limit=5000)
            df['source'] = f'reddit_{sub}'
            reddit_dfs.append(df)
        
        reddit_combined = pd.concat(reddit_dfs, ignore_index=True)
        reddit_combined.to_csv(f"data/raw/reddit_all_{start_date.year}_{end_date.year}.csv", index=False)
        print(f"✓ Reddit: {len(reddit_combined)} posts collected\n")
        
        # 2. Collect Twitter data
        print("[2/3] Collecting Twitter data...")
        twitter_queries = [
            '($SPY OR $QQQ OR #stocks OR #stockmarket) lang:en -is:retweet',
            '(#crypto OR #bitcoin OR #ethereum OR $BTC OR $ETH) lang:en -is:retweet',
            '(#forex OR #EUR OR #USD OR #GBP) lang:en -is:retweet',
            '(#gold OR #oil OR #commodities OR $GLD OR $USO) lang:en -is:retweet'
        ]
        
        twitter_dfs = []
        for query in twitter_queries:
            df = self.twitter.search_tweets(query, start_date, end_date, max_results=100)
            twitter_dfs.append(df)
        
        twitter_combined = pd.concat(twitter_dfs, ignore_index=True)
        twitter_combined.to_csv(f"data/raw/twitter_all_{start_date.year}_{end_date.year}.csv", index=False)
        print(f"✓ Twitter: {len(twitter_combined)} tweets collected\n")
        
        # 3. Collect news data
        print("[3/3] Collecting news data...")
        news_queries = [
            'stock market OR equities',
            'cryptocurrency OR bitcoin',
            'forex OR currency',
            'commodities OR oil OR gold'
        ]
        
        news_dfs = []
        for query in news_queries:
            df = self.news.search_news(
                query=query,
                from_date=start_date,
                to_date=end_date,
                sources='bloomberg,reuters,financial-times,the-wall-street-journal'
            )
            news_dfs.append(df)
        
        news_combined = pd.concat(news_dfs, ignore_index=True)
        news_combined.to_csv(f"data/raw/news_all_{start_date.year}_{end_date.year}.csv", index=False)
        print(f"✓ News: {len(news_combined)} articles collected\n")
        
        # 4. Summary
        print(f"\n{'='*60}")
        print("COLLECTION SUMMARY:")
        print(f"{'='*60}")
        print(f"Reddit:  {len(reddit_combined):,} posts")
        print(f"Twitter: {len(twitter_combined):,} tweets")
        print(f"News:    {len(news_combined):,} articles")
        print(f"TOTAL:   {len(reddit_combined) + len(twitter_combined) + len(news_combined):,} samples")
        print(f"{'='*60}\n")

# Example usage
if __name__ == "__main__":
    pipeline = DataPipeline()
    
    # Collect data for a date range (start small, then expand)
    pipeline.collect_all_data(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 31)
    )
```
