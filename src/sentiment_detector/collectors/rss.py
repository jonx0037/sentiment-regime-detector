"""RSS Feed collector for financial news."""

import asyncio
from datetime import datetime
from typing import Optional
import logging
import hashlib
import httpx
import xml.etree.ElementTree as ET
from html import unescape
import re

from .base import BaseCollector, CollectedItem, AssetClass, DataSource

logger = logging.getLogger(__name__)

# RSS feeds by category
RSS_FEEDS = {
    "general": [
        ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
        ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/"),
        ("Reuters Business", "https://feeds.reuters.com/reuters/businessNews"),
        ("CNBC", "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"),
    ],
    "equity": [
        ("Seeking Alpha", "https://seekingalpha.com/feed.xml"),
        ("Nasdaq News", "https://www.nasdaq.com/feed/rssoutbound?category=Markets"),
    ],
    "crypto": [
        ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
        ("Cointelegraph", "https://cointelegraph.com/rss"),
        ("Bitcoin Magazine", "https://bitcoinmagazine.com/feed"),
    ],
    "forex": [
        ("Forex Factory", "https://www.forexfactory.com/feed.php"),
        ("DailyFX", "https://www.dailyfx.com/feeds/market-news"),
    ],
    "commodity": [
        ("Kitco Gold", "https://www.kitco.com/rss/gold.xml"),
        ("OilPrice.com", "https://oilprice.com/rss/main"),
    ],
}

# Asset classification keywords
ASSET_KEYWORDS = {
    AssetClass.EQUITY: [
        "stock", "stocks", "shares", "equity", "s&p", "nasdaq", "dow jones",
        "nyse", "earnings", "dividend", "ipo", "market cap", "pe ratio",
        "bull market", "bear market", "trading", "investor",
    ],
    AssetClass.CRYPTO: [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
        "blockchain", "defi", "nft", "altcoin", "token", "mining",
        "wallet", "exchange", "binance", "coinbase",
    ],
    AssetClass.FOREX: [
        "forex", "fx", "currency", "exchange rate", "dollar", "euro", "yen",
        "pound", "fed", "federal reserve", "interest rate", "central bank",
        "monetary policy", "inflation",
    ],
    AssetClass.COMMODITY: [
        "gold", "silver", "oil", "crude", "natural gas", "copper",
        "platinum", "palladium", "wheat", "corn", "soybean", "commodity",
        "precious metal", "opec", "futures",
    ],
}


class RSSCollector(BaseCollector):
    """
    Collector for RSS feeds from financial news sources.
    
    No API key required - uses public RSS feeds.
    """
    
    def __init__(self, timeout: float = 30.0):
        """
        Initialize RSS collector.
        
        Args:
            timeout: Request timeout in seconds
        """
        super().__init__(source=DataSource.RSS)
        self.timeout = timeout
        self._client = None
    
    def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; SentimentBot/1.0)",
                    "Accept": "application/rss+xml, application/xml, text/xml, */*",
                },
                follow_redirects=True,
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
        Collect RSS feed items for a specific asset class.
        
        Args:
            asset_class: Asset class to collect for
            start_date: Start of date range
            end_date: End of date range
            limit: Maximum items to collect
            
        Returns:
            List of CollectedItem objects
        """
        # Get relevant feeds
        feeds = RSS_FEEDS.get("general", []).copy()
        
        asset_key = asset_class.value.lower()
        if asset_key in RSS_FEEDS:
            feeds.extend(RSS_FEEDS[asset_key])
        
        items = []
        
        for feed_name, feed_url in feeds:
            if limit and len(items) >= limit:
                break
                
            try:
                feed_items = await self._fetch_feed(
                    feed_name=feed_name,
                    feed_url=feed_url,
                    target_asset=asset_class,
                    start_date=start_date,
                    end_date=end_date,
                )
                items.extend(feed_items)
                self.logger.info(f"Collected {len(feed_items)} items from {feed_name}")
                
            except Exception as e:
                self.logger.warning(f"Failed to fetch {feed_name}: {e}")
        
        # Sort by date and limit
        items.sort(key=lambda x: x.created_at, reverse=True)
        return items[:limit] if limit else items
    
    async def _fetch_feed(
        self,
        feed_name: str,
        feed_url: str,
        target_asset: AssetClass,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CollectedItem]:
        """Fetch and parse a single RSS feed."""
        client = self._get_client()
        
        try:
            response = await client.get(feed_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            self.logger.warning(f"HTTP error fetching {feed_url}: {e}")
            return []
        
        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            self.logger.warning(f"XML parse error for {feed_url}: {e}")
            return []
        
        items = []
        
        # Handle both RSS 2.0 and Atom formats
        for item in root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            try:
                parsed = self._parse_item(item, feed_name, target_asset)
                if parsed and start_date <= parsed.created_at <= end_date:
                    items.append(parsed)
            except Exception as e:
                self.logger.debug(f"Failed to parse item: {e}")
        
        return items
    
    def _parse_item(
        self,
        item: ET.Element,
        feed_name: str,
        default_asset: AssetClass,
    ) -> Optional[CollectedItem]:
        """Parse a single RSS item."""
        # Try different tag names for compatibility
        title = self._get_text(item, ["title", "{http://www.w3.org/2005/Atom}title"])
        
        # Get content/description
        content = self._get_text(item, [
            "description",
            "content:encoded",
            "{http://www.w3.org/2005/Atom}content",
            "{http://www.w3.org/2005/Atom}summary",
        ])
        
        # Get link
        link = self._get_text(item, ["link", "guid"])
        if not link:
            link_elem = item.find("{http://www.w3.org/2005/Atom}link")
            if link_elem is not None:
                link = link_elem.get("href", "")
        
        # Get publication date
        pub_date_str = self._get_text(item, [
            "pubDate",
            "{http://www.w3.org/2005/Atom}published",
            "{http://www.w3.org/2005/Atom}updated",
        ])
        
        if not content and not title:
            return None
        
        # Clean HTML from content
        content = self._clean_html(content or title or "")
        title = self._clean_html(title or "")
        
        # Combine for better analysis
        full_text = f"{title} {content}"
        
        # Classify asset
        asset_class = self._classify_asset(full_text, ASSET_KEYWORDS) or default_asset
        
        # Parse date
        created_at = self._parse_date(pub_date_str) or datetime.utcnow()
        
        # Generate unique ID
        source_id = hashlib.md5(f"{feed_name}:{link or title}".encode()).hexdigest()[:16]
        
        return CollectedItem(
            source=DataSource.RSS,
            source_id=source_id,
            asset_class=asset_class,
            created_at=created_at,
            title=title[:500] if title else None,
            content=full_text[:5000],
            metadata={
                "feed_name": feed_name,
                "link": link,
            },
        )
    
    def _get_text(self, elem: ET.Element, tags: list[str]) -> Optional[str]:
        """Get text content from first matching tag."""
        for tag in tags:
            child = elem.find(tag)
            if child is not None and child.text:
                return child.text.strip()
        return None
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean text."""
        # Unescape HTML entities
        text = unescape(text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Clean whitespace
        text = ' '.join(text.split())
        return text
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse various date formats."""
        if not date_str:
            return None
        
        formats = [
            "%a, %d %b %Y %H:%M:%S %z",  # RFC 822
            "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                # Remove timezone info for consistency
                return dt.replace(tzinfo=None)
            except ValueError:
                continue
        
        return None
    
    async def health_check(self) -> bool:
        """Check if RSS feeds are accessible."""
        try:
            client = self._get_client()
            # Try to fetch Yahoo Finance as a basic check
            response = await client.get(RSS_FEEDS["general"][0][1])
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"RSS health check failed: {e}")
            return False
    
    async def collect_all_assets(
        self,
        limit_per_asset: int = 50,
    ) -> dict[AssetClass, list[CollectedItem]]:
        """
        Collect from all RSS feeds, grouped by asset class.
        
        Args:
            limit_per_asset: Max items per asset class
            
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


# Missing import
from datetime import timedelta
