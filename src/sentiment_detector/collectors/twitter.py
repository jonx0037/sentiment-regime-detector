"""X/Twitter data collector using Twitter API v2."""

import asyncio
from datetime import datetime, timedelta
from typing import Optional
import logging
import httpx

from .base import BaseCollector, CollectedItem, AssetClass, DataSource

logger = logging.getLogger(__name__)

# Financial search queries by asset class
SEARCH_QUERIES = {
    AssetClass.EQUITY: [
        "$SPY OR $QQQ OR $AAPL OR $MSFT OR $NVDA",
        "#stocks OR #stockmarket OR #trading",
        "stock market OR earnings OR S&P500",
    ],
    AssetClass.CRYPTO: [
        "$BTC OR $ETH OR #Bitcoin OR #Ethereum",
        "#crypto OR cryptocurrency OR blockchain",
        "bitcoin OR ethereum OR altcoin",
    ],
    AssetClass.FOREX: [
        "forex OR #forex OR currency trading",
        "EURUSD OR GBPUSD OR dollar index",
        "Fed rate OR interest rate OR central bank",
    ],
    AssetClass.COMMODITY: [
        "gold price OR silver price OR $GLD",
        "oil price OR crude OR #oil",
        "#commodities OR wheat OR copper",
    ],
}

# Keywords for asset classification
ASSET_KEYWORDS = {
    AssetClass.EQUITY: [
        "spy", "qqq", "stocks", "stock", "shares", "equity", "s&p", "nasdaq",
        "dow", "nyse", "earnings", "dividend", "aapl", "msft", "googl", "amzn",
        "tsla", "nvda", "meta", "options", "calls", "puts",
    ],
    AssetClass.CRYPTO: [
        "btc", "eth", "bitcoin", "ethereum", "crypto", "blockchain", "defi",
        "nft", "altcoin", "binance", "coinbase", "solana", "cardano", "xrp",
    ],
    AssetClass.FOREX: [
        "forex", "fx", "eur", "usd", "gbp", "jpy", "currency", "dollar",
        "euro", "pound", "yen", "pip", "fed rate",
    ],
    AssetClass.COMMODITY: [
        "gold", "silver", "oil", "crude", "wti", "brent", "natural gas",
        "copper", "platinum", "wheat", "corn", "commodity", "gld", "slv",
    ],
}


class TwitterCollector(BaseCollector):
    """
    Collector for X/Twitter data using API v2.
    
    Requires Bearer Token from X Developer Portal.
    Free tier: 1,500 tweets/month read access.
    """
    
    BASE_URL = "https://api.twitter.com/2"
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize Twitter collector.
        
        Args:
            bearer_token: Twitter API v2 Bearer Token
        """
        super().__init__(source=DataSource.TWITTER)
        self.bearer_token = bearer_token
        self._client = None
    
    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            if not self.bearer_token:
                raise ValueError("Twitter Bearer Token is required")
            
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self.bearer_token}",
                    "User-Agent": "sentiment-regime-detector/1.0",
                },
                timeout=30.0,
            )
        return self._client
    
    async def collect(
        self,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """
        Collect tweets for a specific asset class.
        
        Args:
            asset_class: Asset class to collect for
            start_date: Start of date range (Twitter free tier: last 7 days only)
            end_date: End of date range
            limit: Maximum tweets to collect
            
        Returns:
            List of CollectedItem objects
        """
        queries = SEARCH_QUERIES.get(asset_class, [])
        if not queries:
            self.logger.warning(f"No search queries for {asset_class}")
            return []
        
        items = []
        max_results = min(limit or 100, 100)  # Twitter max per request is 100
        
        for query in queries:
            if limit and len(items) >= limit:
                break
                
            try:
                query_items = await self._search_tweets(
                    query=query,
                    asset_class=asset_class,
                    max_results=max_results,
                )
                items.extend(query_items)
                self.logger.info(f"Collected {len(query_items)} tweets for query: {query[:30]}...")
                
                # Rate limiting - be nice to the API
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error searching tweets: {e}")
        
        return items[:limit] if limit else items
    
    async def _search_tweets(
        self,
        query: str,
        asset_class: AssetClass,
        max_results: int = 100,
    ) -> list[CollectedItem]:
        """Search for tweets matching query."""
        client = self._get_client()
        
        # Build search params
        params = {
            "query": f"{query} -is:retweet lang:en",
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,author_id,public_metrics,context_annotations",
            "expansions": "author_id",
            "user.fields": "username,verified",
        }
        
        try:
            response = await client.get(
                f"{self.BASE_URL}/tweets/search/recent",
                params=params,
            )
            
            if response.status_code == 429:
                self.logger.warning("Twitter rate limit reached")
                return []
            
            response.raise_for_status()
            data = response.json()
            
        except httpx.HTTPStatusError as e:
            self.logger.error(f"Twitter API error: {e.response.status_code} - {e.response.text}")
            return []
        
        tweets = data.get("data", [])
        users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
        
        items = []
        for tweet in tweets:
            try:
                author = users.get(tweet.get("author_id"), {})
                created_at = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
                
                metrics = tweet.get("public_metrics", {})
                
                item = CollectedItem(
                    source=DataSource.TWITTER,
                    source_id=tweet["id"],
                    asset_class=asset_class,
                    created_at=created_at,
                    title=None,
                    content=tweet["text"],
                    metadata={
                        "author_id": tweet.get("author_id"),
                        "username": author.get("username"),
                        "verified": author.get("verified", False),
                        "retweet_count": metrics.get("retweet_count", 0),
                        "like_count": metrics.get("like_count", 0),
                        "reply_count": metrics.get("reply_count", 0),
                        "query": query,
                    },
                )
                items.append(item)
                
            except (KeyError, ValueError) as e:
                self.logger.debug(f"Skipping invalid tweet: {e}")
        
        return items
    
    async def health_check(self) -> bool:
        """Check if Twitter API is accessible."""
        try:
            client = self._get_client()
            response = await client.get(f"{self.BASE_URL}/users/me")
            # Free tier may not have this endpoint, so 401/403 is also "working"
            return response.status_code in [200, 401, 403]
        except Exception as e:
            self.logger.error(f"Twitter health check failed: {e}")
            return False
    
    async def collect_all_assets(
        self,
        limit_per_asset: int = 50,
    ) -> dict[AssetClass, list[CollectedItem]]:
        """
        Collect tweets for all asset classes.
        
        Args:
            limit_per_asset: Max tweets per asset class
            
        Returns:
            Dict mapping asset classes to collected items
        """
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        
        results = {}
        for asset_class in AssetClass:
            items = await self.collect(
                asset_class=asset_class,
                start_date=week_ago,
                end_date=now,
                limit=limit_per_asset,
            )
            results[asset_class] = items
            
        return results
    
    async def close(self):
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
