"""Kaggle dataset loader for historical Reddit financial data."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
import logging
import csv

from .base import CollectedItem, AssetClass, DataSource

logger = logging.getLogger(__name__)

# Asset classification keywords
ASSET_KEYWORDS = {
    AssetClass.EQUITY: [
        "spy", "qqq", "stocks", "stock", "shares", "equity", "s&p", "nasdaq",
        "dow", "nyse", "earnings", "dividend", "aapl", "msft", "googl", "amzn",
        "tsla", "nvda", "meta", "options", "calls", "puts", "short", "long",
        "bull", "bear", "wsb", "yolo", "tendies", "diamond hands",
    ],
    AssetClass.CRYPTO: [
        "btc", "eth", "bitcoin", "ethereum", "crypto", "blockchain", "defi",
        "nft", "altcoin", "binance", "coinbase", "solana", "cardano", "xrp",
        "doge", "shib", "hodl", "moon", "wallet", "mining",
    ],
    AssetClass.FOREX: [
        "forex", "fx", "eur", "usd", "gbp", "jpy", "chf", "aud", "cad",
        "currency", "dollar", "euro", "pound", "yen", "pip",
    ],
    AssetClass.COMMODITY: [
        "gold", "silver", "oil", "crude", "wti", "brent", "natural gas",
        "copper", "platinum", "wheat", "corn", "commodity", "gld", "slv",
    ],
}

# Subreddit to asset class mapping
SUBREDDIT_ASSETS = {
    "wallstreetbets": AssetClass.EQUITY,
    "stocks": AssetClass.EQUITY,
    "investing": AssetClass.EQUITY,
    "options": AssetClass.EQUITY,
    "stockmarket": AssetClass.EQUITY,
    "cryptocurrency": AssetClass.CRYPTO,
    "bitcoin": AssetClass.CRYPTO,
    "ethereum": AssetClass.CRYPTO,
    "cryptomarkets": AssetClass.CRYPTO,
    "forex": AssetClass.FOREX,
    "commodities": AssetClass.COMMODITY,
    "gold": AssetClass.COMMODITY,
    "silverbugs": AssetClass.COMMODITY,
}


class KaggleDataLoader:
    """
    Loader for Kaggle financial Reddit datasets.
    
    Supports common Kaggle dataset formats:
    - WallStreetBets posts (CSV with title, body, score, etc.)
    - Reddit dumps (JSON/CSV with various schemas)
    
    Download datasets from:
    - https://www.kaggle.com/datasets/gpreda/reddit-wallstreetsbets-posts
    - https://www.kaggle.com/datasets/unanimad/reddit-rwallstreetbets
    """
    
    def __init__(self, data_dir: Union[str, Path] = "data/kaggle"):
        """
        Initialize Kaggle loader.
        
        Args:
            data_dir: Directory containing downloaded Kaggle datasets
        """
        self.data_dir = Path(data_dir)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def load_csv(
        self,
        filepath: Union[str, Path],
        title_col: str = "title",
        body_col: str = "body",
        date_col: str = "timestamp",
        score_col: str = "score",
        subreddit_col: Optional[str] = "subreddit",
        limit: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[CollectedItem]:
        """
        Load data from a CSV file.
        
        Args:
            filepath: Path to CSV file
            title_col: Column name for post title
            body_col: Column name for post body/content
            date_col: Column name for timestamp
            score_col: Column name for score/upvotes
            subreddit_col: Column name for subreddit
            limit: Maximum rows to load
            start_date: Filter by start date
            end_date: Filter by end date
            
        Returns:
            List of CollectedItem objects
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        items = []
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader):
                if limit and len(items) >= limit:
                    break
                
                try:
                    item = self._parse_csv_row(
                        row=row,
                        title_col=title_col,
                        body_col=body_col,
                        date_col=date_col,
                        score_col=score_col,
                        subreddit_col=subreddit_col,
                        row_num=i,
                    )
                    
                    if item:
                        # Date filtering
                        if start_date and item.created_at < start_date:
                            continue
                        if end_date and item.created_at > end_date:
                            continue
                        
                        items.append(item)
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing row {i}: {e}")
        
        self.logger.info(f"Loaded {len(items)} items from {filepath.name}")
        return items
    
    def _parse_csv_row(
        self,
        row: dict,
        title_col: str,
        body_col: str,
        date_col: str,
        score_col: str,
        subreddit_col: Optional[str],
        row_num: int,
    ) -> Optional[CollectedItem]:
        """Parse a single CSV row into CollectedItem."""
        # Get content
        title = row.get(title_col, "") or ""
        body = row.get(body_col, "") or ""
        content = f"{title}\n\n{body}".strip() if body else title
        
        if not content or len(content) < 10:
            return None
        
        # Get date
        date_str = row.get(date_col, "")
        created_at = self._parse_date(date_str) or datetime.utcnow()
        
        # Get subreddit and classify asset
        subreddit = row.get(subreddit_col, "").lower() if subreddit_col else ""
        asset_class = SUBREDDIT_ASSETS.get(subreddit)
        
        if not asset_class:
            asset_class = self._classify_asset(content)
        
        # Get score
        try:
            score = int(row.get(score_col, 0) or 0)
        except (ValueError, TypeError):
            score = 0
        
        # Generate ID
        source_id = row.get("id", f"kaggle_{row_num}")
        
        return CollectedItem(
            source=DataSource.KAGGLE,
            source_id=str(source_id),
            asset_class=asset_class,
            created_at=created_at,
            title=title[:500] if title else None,
            content=content[:10000],
            metadata={
                "subreddit": subreddit,
                "score": score,
                "source_file": "kaggle_csv",
            },
        )
    
    def load_json(
        self,
        filepath: Union[str, Path],
        limit: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[CollectedItem]:
        """
        Load data from a JSON file.
        
        Args:
            filepath: Path to JSON file
            limit: Maximum items to load
            start_date: Filter by start date
            end_date: Filter by end date
            
        Returns:
            List of CollectedItem objects
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"JSON file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, dict):
            if 'items' in data:
                records = data['items']
            elif 'data' in data:
                records = data['data']
            else:
                records = [data]
        else:
            records = data
        
        items = []
        for i, record in enumerate(records):
            if limit and len(items) >= limit:
                break
            
            try:
                item = self._parse_json_record(record, i)
                if item:
                    if start_date and item.created_at < start_date:
                        continue
                    if end_date and item.created_at > end_date:
                        continue
                    items.append(item)
            except Exception as e:
                self.logger.debug(f"Error parsing record {i}: {e}")
        
        self.logger.info(f"Loaded {len(items)} items from {filepath.name}")
        return items
    
    def _parse_json_record(self, record: dict, index: int) -> Optional[CollectedItem]:
        """Parse a single JSON record."""
        # Try common field names
        title = record.get("title", "") or ""
        body = record.get("body") or record.get("selftext") or record.get("content") or ""
        content = f"{title}\n\n{body}".strip() if body else title
        
        if not content or len(content) < 10:
            return None
        
        # Date
        date_str = (
            record.get("created_at") or 
            record.get("timestamp") or 
            record.get("created_utc") or
            record.get("date")
        )
        if isinstance(date_str, (int, float)):
            created_at = datetime.utcfromtimestamp(date_str)
        else:
            created_at = self._parse_date(str(date_str)) or datetime.utcnow()
        
        # Subreddit
        subreddit = (record.get("subreddit", "") or "").lower()
        asset_class = SUBREDDIT_ASSETS.get(subreddit) or self._classify_asset(content)
        
        # Score
        try:
            score = int(record.get("score", 0) or 0)
        except (ValueError, TypeError):
            score = 0
        
        source_id = str(record.get("id", f"kaggle_{index}"))
        
        return CollectedItem(
            source=DataSource.KAGGLE,
            source_id=source_id,
            asset_class=asset_class,
            created_at=created_at,
            title=title[:500] if title else None,
            content=content[:10000],
            metadata={
                "subreddit": subreddit,
                "score": score,
                "num_comments": record.get("num_comments", 0),
            },
        )
    
    def _classify_asset(self, text: str) -> AssetClass:
        """Classify text into asset class based on keywords."""
        text_lower = text.lower()
        scores = {asset: 0 for asset in AssetClass}
        
        for asset_class, keywords in ASSET_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[asset_class] += 1
        
        max_score = max(scores.values())
        if max_score == 0:
            return AssetClass.EQUITY  # Default
        
        return max(scores, key=scores.get)
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats."""
        if not date_str:
            return None
        
        # Handle Unix timestamp
        try:
            ts = float(date_str)
            if ts > 1e10:  # Milliseconds
                ts /= 1000
            return datetime.utcfromtimestamp(ts)
        except (ValueError, TypeError):
            pass
        
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=None)
            except ValueError:
                continue
        
        return None
    
    def load_reddit_news(
        self,
        filepath: Union[str, Path],
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """Load Reddit News dataset (aaron7sun/stocknews)."""
        filepath = Path(filepath)
        items = []
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and len(items) >= limit:
                    break
                
                content = row.get("News", "").strip()
                if not content or len(content) < 20:
                    continue
                
                date_str = row.get("Date", "")
                created_at = self._parse_date(date_str) or datetime.utcnow()
                
                items.append(CollectedItem(
                    source=DataSource.KAGGLE,
                    source_id=f"reddit_news_{i}",
                    asset_class=AssetClass.EQUITY,  # This dataset is stock-focused
                    created_at=created_at,
                    title=content[:100],
                    content=content[:10000],
                    metadata={"dataset": "reddit_news", "source_file": filepath.name},
                ))
        
        self.logger.info(f"Loaded {len(items)} items from Reddit News")
        return items
    
    def load_djia_news(
        self,
        filepath: Union[str, Path],
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """Load Combined News DJIA dataset (aaron7sun/stocknews)."""
        filepath = Path(filepath)
        items = []
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and len(items) >= limit:
                    break
                
                # Combine all Top1-Top25 news columns
                news_items = []
                for j in range(1, 26):
                    col = f"Top{j}"
                    if col in row and row[col]:
                        # Clean b'...' format
                        text = row[col].strip()
                        if text.startswith("b'") or text.startswith('b"'):
                            text = text[2:-1]
                        news_items.append(text)
                
                if not news_items:
                    continue
                
                content = " | ".join(news_items[:5])  # First 5 headlines
                date_str = row.get("Date", "")
                created_at = self._parse_date(date_str) or datetime.utcnow()
                label = row.get("Label", "")  # 1 = market up, 0 = market down
                
                items.append(CollectedItem(
                    source=DataSource.KAGGLE,
                    source_id=f"djia_news_{i}",
                    asset_class=AssetClass.EQUITY,
                    created_at=created_at,
                    title=news_items[0][:100] if news_items else None,
                    content=content[:10000],
                    metadata={
                        "dataset": "djia_combined_news",
                        "market_label": label,
                        "num_headlines": len(news_items),
                    },
                ))
        
        self.logger.info(f"Loaded {len(items)} items from DJIA News")
        return items
    
    def load_crypto_tweets(
        self,
        filepath: Union[str, Path],
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """Load Crypto Tweets dataset (leoth9/crypto-tweets)."""
        filepath = Path(filepath)
        items = []
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and len(items) >= limit:
                    break
                
                content = row.get("Content") or ""
                content = content.strip() if content else ""
                if not content or len(content) < 10:
                    continue
                
                date_str = row.get("Date") or ""
                created_at = self._parse_date(date_str) or datetime.utcnow()
                username = row.get("Username") or ""
                
                items.append(CollectedItem(
                    source=DataSource.KAGGLE,
                    source_id=f"crypto_tweet_{i}",
                    asset_class=AssetClass.CRYPTO,
                    created_at=created_at,
                    title=None,
                    content=content[:10000],
                    metadata={
                        "dataset": "crypto_tweets",
                        "username": username,
                        "hashtags": row.get("Hashtags") or "",
                    },
                ))
        
        self.logger.info(f"Loaded {len(items)} items from Crypto Tweets")
        return items
    
    def load_stock_tweets(
        self,
        filepath: Union[str, Path],
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """Load Stock Tweets dataset (omer2040/stock-tweets-for-sentiment-analysis)."""
        filepath = Path(filepath)
        items = []
        
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and len(items) >= limit:
                    break
                
                content = row.get("Tweet") or ""
                content = content.strip() if content else ""
                if not content or len(content) < 10:
                    continue
                
                date_str = row.get("Date") or ""
                created_at = self._parse_date(date_str) or datetime.utcnow()
                stock_name = row.get("Stock Name") or ""
                company_name = row.get("Company Name") or ""
                
                # Classify asset based on content
                asset_class = self._classify_asset(content)
                
                items.append(CollectedItem(
                    source=DataSource.KAGGLE,
                    source_id=f"stock_tweet_{i}",
                    asset_class=asset_class,
                    created_at=created_at,
                    title=None,
                    content=content[:10000],
                    metadata={
                        "dataset": "stock_tweets",
                        "stock_name": stock_name,
                        "company_name": company_name,
                    },
                ))
        
        self.logger.info(f"Loaded {len(items)} items from Stock Tweets")
        return items
    
    def load_all(
        self,
        limit: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[CollectedItem]:
        """
        Load all datasets from the data directory.
        
        Returns:
            Combined list of CollectedItem objects
        """
        if not self.data_dir.exists():
            self.logger.warning(f"Data directory does not exist: {self.data_dir}")
            return []
        
        all_items = []
        per_dataset_limit = limit // 5 if limit else None  # Split across datasets
        
        # Load specific known datasets with their custom loaders
        
        # 1. Reddit News (aaron7sun/stocknews)
        reddit_news = self.data_dir / "stocknews" / "RedditNews.csv"
        if reddit_news.exists():
            try:
                items = self.load_reddit_news(reddit_news, limit=per_dataset_limit)
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading RedditNews: {e}")
        
        # 2. DJIA Combined News
        djia_news = self.data_dir / "stocknews" / "Combined_News_DJIA.csv"
        if djia_news.exists():
            try:
                items = self.load_djia_news(djia_news, limit=per_dataset_limit)
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading DJIA News: {e}")
        
        # 3. Crypto Tweets
        crypto_tweets = self.data_dir / "crypto-tweets"
        for csv_file in crypto_tweets.glob("*.csv"):
            try:
                items = self.load_crypto_tweets(csv_file, limit=per_dataset_limit)
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading crypto tweets: {e}")
        
        # 4. WSB posts (original dataset) - use generic loader
        wsb_dir = self.data_dir / "wsb"
        for csv_file in wsb_dir.glob("*.csv"):
            try:
                items = self.load_csv(csv_file, limit=per_dataset_limit)
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading WSB data: {e}")
        
        # 5. Financial news
        financial_news = self.data_dir / "financial-news"
        for csv_file in financial_news.glob("*.csv"):
            try:
                items = self.load_csv(
                    csv_file, 
                    title_col="title",
                    body_col="description",
                    date_col="date",
                    limit=per_dataset_limit,
                )
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading financial news: {e}")
        
        # 6. Stock Tweets (omer2040/stock-tweets-for-sentiment-analysis)
        stock_tweets = self.data_dir / "stock_tweets"
        for csv_file in stock_tweets.glob("*.csv"):
            if "yfinance" in csv_file.name:
                continue  # Skip market data file
            try:
                items = self.load_stock_tweets(csv_file, limit=per_dataset_limit)
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading stock tweets: {e}")
        
        # Also try loading any JSON files
        for json_file in self.data_dir.glob("**/*.json"):
            try:
                items = self.load_json(
                    json_file,
                    limit=per_dataset_limit,
                    start_date=start_date,
                    end_date=end_date,
                )
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading {json_file}: {e}")
        
        # Load JSON files
        for json_file in self.data_dir.glob("**/*.json"):
            try:
                items = self.load_json(
                    json_file,
                    limit=limit,
                    start_date=start_date,
                    end_date=end_date,
                )
                all_items.extend(items)
            except Exception as e:
                self.logger.error(f"Error loading {json_file}: {e}")
        
        self.logger.info(f"Loaded {len(all_items)} total items from Kaggle data")
        return all_items


def download_instructions():
    """Print instructions for downloading Kaggle datasets."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     Kaggle Dataset Download Instructions                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║  1. Install Kaggle CLI (if not already):                                       ║
║     pip install kaggle                                                         ║
║                                                                                ║
║  2. Set up Kaggle credentials:                                                 ║
║     - Go to kaggle.com → Account → Create New Token                            ║
║     - Save kaggle.json to ~/.kaggle/                                           ║
║     - chmod 600 ~/.kaggle/kaggle.json                                          ║
║                                                                                ║
║  3. Download recommended datasets:                                             ║
║                                                                                ║
║     # WallStreetBets posts (2021-2023)                                         ║
║     kaggle datasets download -d gpreda/reddit-wallstreetbets-posts \\           ║
║         -p data/kaggle/wsb --unzip                                             ║
║                                                                                ║
║     # Reddit stock discussions                                                 ║
║     kaggle datasets download -d unanimad/reddit-rwallstreetbets \\              ║
║         -p data/kaggle/reddit --unzip                                          ║
║                                                                                ║
║     # Crypto sentiment data                                                    ║
║     kaggle datasets download -d kaushiksuresh147/cryptocurrency-sentiment \\    ║
║         -p data/kaggle/crypto --unzip                                          ║
║                                                                                ║
║  4. Load data in Python:                                                       ║
║     from sentiment_detector.collectors.kaggle_loader import KaggleDataLoader   ║
║     loader = KaggleDataLoader("data/kaggle")                                   ║
║     items = loader.load_all()                                                  ║
║                                                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    download_instructions()
