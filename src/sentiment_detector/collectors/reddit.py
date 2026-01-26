"""Reddit data collector using PRAW."""

import asyncio
from datetime import datetime
from typing import Optional
import logging

from .base import BaseCollector, CollectedItem, AssetClass, DataSource

logger = logging.getLogger(__name__)

# Asset classification keywords
ASSET_KEYWORDS = {
    AssetClass.EQUITY: [
        "spy", "qqq", "stocks", "stock", "shares", "equity", "s&p", "nasdaq",
        "dow", "nyse", "earnings", "dividend", "aapl", "msft", "googl", "amzn",
        "tsla", "nvda", "meta", "options", "calls", "puts", "short", "long",
    ],
    AssetClass.CRYPTO: [
        "btc", "eth", "bitcoin", "ethereum", "crypto", "blockchain", "defi",
        "nft", "altcoin", "binance", "coinbase", "solana", "cardano", "xrp",
        "doge", "shib", "hodl", "wallet", "mining", "staking",
    ],
    AssetClass.FOREX: [
        "forex", "fx", "eur", "usd", "gbp", "jpy", "chf", "aud", "cad",
        "currency", "exchange rate", "dollar", "euro", "pound", "yen",
        "pip", "leverage", "carry trade",
    ],
    AssetClass.COMMODITY: [
        "gold", "silver", "oil", "crude", "wti", "brent", "natural gas",
        "copper", "platinum", "wheat", "corn", "soybean", "commodity",
        "futures", "gld", "slv", "uso", "metals",
    ],
}

# Subreddit to asset class mapping
SUBREDDIT_ASSETS = {
    # Equity-focused
    "wallstreetbets": AssetClass.EQUITY,
    "stocks": AssetClass.EQUITY,
    "investing": AssetClass.EQUITY,
    "options": AssetClass.EQUITY,
    "stockmarket": AssetClass.EQUITY,
    
    # Crypto-focused
    "cryptocurrency": AssetClass.CRYPTO,
    "bitcoin": AssetClass.CRYPTO,
    "ethereum": AssetClass.CRYPTO,
    "cryptomarkets": AssetClass.CRYPTO,
    
    # Forex-focused
    "forex": AssetClass.FOREX,
    "forextrading": AssetClass.FOREX,
    
    # Commodity-focused
    "commodities": AssetClass.COMMODITY,
    "gold": AssetClass.COMMODITY,
    "silverbugs": AssetClass.COMMODITY,
}


class RedditCollector(BaseCollector):
    """
    Collector for Reddit posts and comments.
    
    Uses PRAW (Python Reddit API Wrapper) for data collection.
    Requires Reddit API credentials in environment variables.
    """
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: str = "sentiment-regime-detector:v1.0.0",
    ):
        """
        Initialize Reddit collector.
        
        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string for API requests
        """
        super().__init__(source=DataSource.REDDIT)
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self._reddit = None
    
    def _get_client(self):
        """Lazily initialize Reddit client."""
        if self._reddit is None:
            try:
                import praw
                
                self._reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent=self.user_agent,
                )
                self.logger.info("Reddit client initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize Reddit client: {e}")
                raise
        
        return self._reddit
    
    async def collect(
        self,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """
        Collect Reddit posts for a specific asset class.
        
        Args:
            asset_class: Asset class to collect for
            start_date: Start of date range
            end_date: End of date range
            limit: Maximum posts to collect (per subreddit)
            
        Returns:
            List of CollectedItem objects
        """
        # Get subreddits for this asset class
        subreddits = [
            name for name, asset in SUBREDDIT_ASSETS.items()
            if asset == asset_class
        ]
        
        if not subreddits:
            self.logger.warning(f"No subreddits configured for {asset_class}")
            return []
        
        items = []
        
        for subreddit_name in subreddits:
            try:
                subreddit_items = await self._collect_subreddit(
                    subreddit_name=subreddit_name,
                    asset_class=asset_class,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit,
                )
                items.extend(subreddit_items)
                self.logger.info(f"Collected {len(subreddit_items)} posts from r/{subreddit_name}")
            except Exception as e:
                self.logger.error(f"Error collecting from r/{subreddit_name}: {e}")
        
        return items
    
    async def _collect_subreddit(
        self,
        subreddit_name: str,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """Collect posts from a single subreddit."""
        # Run PRAW in executor since it's synchronous
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._collect_subreddit_sync,
            subreddit_name,
            asset_class,
            start_date,
            end_date,
            limit,
        )
    
    def _collect_subreddit_sync(
        self,
        subreddit_name: str,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int],
    ) -> list[CollectedItem]:
        """Synchronous subreddit collection (run in executor)."""
        reddit = self._get_client()
        subreddit = reddit.subreddit(subreddit_name)
        
        items = []
        post_limit = limit or 1000
        
        for submission in subreddit.new(limit=post_limit):
            created = datetime.utcfromtimestamp(submission.created_utc)
            
            # Check date range
            if created < start_date:
                break  # Posts are sorted by new, so we can stop
            if created > end_date:
                continue
            
            # Combine title and body
            content = submission.title
            if submission.selftext:
                content = f"{submission.title}\n\n{submission.selftext}"
            
            try:
                item = CollectedItem(
                    source=DataSource.REDDIT,
                    source_id=submission.id,
                    asset_class=asset_class,
                    created_at=created,
                    title=submission.title,
                    content=content,
                    metadata={
                        "subreddit": subreddit_name,
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "author": str(submission.author),
                        "url": submission.url,
                        "upvote_ratio": submission.upvote_ratio,
                    },
                )
                items.append(item)
            except ValueError as e:
                self.logger.debug(f"Skipping invalid post {submission.id}: {e}")
        
        return items
    
    async def health_check(self) -> bool:
        """Check if Reddit API is accessible."""
        try:
            reddit = self._get_client()
            # Simple check - try to access a known subreddit
            _ = reddit.subreddit("test").id
            return True
        except Exception as e:
            self.logger.error(f"Reddit health check failed: {e}")
            return False
    
    async def collect_all_assets(
        self,
        start_date: datetime,
        end_date: datetime,
        limit_per_subreddit: Optional[int] = None,
    ) -> dict[AssetClass, list[CollectedItem]]:
        """
        Collect from all configured subreddits, grouped by asset class.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            limit_per_subreddit: Maximum posts per subreddit
            
        Returns:
            Dict mapping asset classes to collected items
        """
        results = {asset: [] for asset in AssetClass}
        
        for asset_class in AssetClass:
            items = await self.collect(
                asset_class=asset_class,
                start_date=start_date,
                end_date=end_date,
                limit=limit_per_subreddit,
            )
            results[asset_class] = items
        
        return results
