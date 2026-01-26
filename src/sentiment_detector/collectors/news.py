"""News data collector using NewsAPI."""

from datetime import datetime
from typing import Optional
import logging

import httpx

from .base import BaseCollector, CollectedItem, AssetClass, DataSource

logger = logging.getLogger(__name__)

# Query templates for each asset class
ASSET_QUERIES = {
    AssetClass.EQUITY: [
        "stock market",
        "S&P 500",
        "NASDAQ",
        "Wall Street",
        "equity markets",
    ],
    AssetClass.CRYPTO: [
        "cryptocurrency",
        "bitcoin",
        "ethereum",
        "crypto market",
        "blockchain",
    ],
    AssetClass.FOREX: [
        "forex",
        "currency exchange",
        "US dollar",
        "EUR USD",
        "foreign exchange",
    ],
    AssetClass.COMMODITY: [
        "gold price",
        "oil market",
        "commodities",
        "crude oil",
        "precious metals",
    ],
}

# Preferred news sources (financial)
FINANCIAL_SOURCES = [
    "bloomberg",
    "reuters",
    "the-wall-street-journal",
    "financial-times",
    "cnbc",
    "business-insider",
    "fortune",
    "the-economist",
]


class NewsCollector(BaseCollector):
    """
    Collector for news articles using NewsAPI.
    
    Free tier: 100 requests/day, 1 month historical
    Paid tier: More requests, 2+ years historical
    """
    
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize news collector.
        
        Args:
            api_key: NewsAPI API key
        """
        super().__init__(source=DataSource.NEWS)
        self.api_key = api_key
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={"X-Api-Key": self.api_key or ""},
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
        Collect news articles for a specific asset class.
        
        Args:
            asset_class: Asset class to collect for
            start_date: Start of date range
            end_date: End of date range
            limit: Maximum articles to collect
            
        Returns:
            List of CollectedItem objects
        """
        queries = ASSET_QUERIES.get(asset_class, [])
        if not queries:
            self.logger.warning(f"No queries configured for {asset_class}")
            return []
        
        items = []
        limit_per_query = (limit // len(queries)) if limit else 100
        
        for query in queries:
            try:
                query_items = await self._search(
                    query=query,
                    asset_class=asset_class,
                    start_date=start_date,
                    end_date=end_date,
                    limit=limit_per_query,
                )
                items.extend(query_items)
            except Exception as e:
                self.logger.error(f"Error searching for '{query}': {e}")
        
        # Remove duplicates by source_id
        seen = set()
        unique_items = []
        for item in items:
            if item.source_id not in seen:
                seen.add(item.source_id)
                unique_items.append(item)
        
        return unique_items[:limit] if limit else unique_items
    
    async def _search(
        self,
        query: str,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: int = 100,
    ) -> list[CollectedItem]:
        """Execute a single search query."""
        client = await self._get_client()
        
        params = {
            "q": query,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": min(limit, 100),  # NewsAPI max is 100
        }
        
        # Add source filter for financial sources
        if FINANCIAL_SOURCES:
            params["sources"] = ",".join(FINANCIAL_SOURCES[:10])  # API limit
        
        response = await client.get(f"{self.BASE_URL}/everything", params=params)
        
        if response.status_code != 200:
            error_data = response.json() if response.content else {}
            self.logger.error(f"NewsAPI error: {response.status_code} - {error_data}")
            return []
        
        data = response.json()
        articles = data.get("articles", [])
        
        items = []
        for article in articles:
            try:
                # Create unique ID from URL hash
                source_id = str(hash(article.get("url", "")))
                
                # Parse published date
                published = article.get("publishedAt", "")
                if published:
                    created_at = datetime.fromisoformat(published.replace("Z", "+00:00"))
                else:
                    created_at = datetime.utcnow()
                
                # Combine title and description
                content = article.get("title", "")
                if article.get("description"):
                    content = f"{content}\n\n{article['description']}"
                if article.get("content"):
                    # NewsAPI truncates content, but include what we have
                    content = f"{content}\n\n{article['content']}"
                
                item = CollectedItem(
                    source=DataSource.NEWS,
                    source_id=source_id,
                    asset_class=asset_class,
                    created_at=created_at,
                    title=article.get("title"),
                    content=content,
                    metadata={
                        "source_name": article.get("source", {}).get("name"),
                        "author": article.get("author"),
                        "url": article.get("url"),
                        "image_url": article.get("urlToImage"),
                        "query": query,
                    },
                )
                items.append(item)
            except Exception as e:
                self.logger.debug(f"Skipping invalid article: {e}")
        
        return items
    
    async def health_check(self) -> bool:
        """Check if NewsAPI is accessible."""
        try:
            client = await self._get_client()
            response = await client.get(
                f"{self.BASE_URL}/top-headlines",
                params={"country": "us", "pageSize": 1},
            )
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"NewsAPI health check failed: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
