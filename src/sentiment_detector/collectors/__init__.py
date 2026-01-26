"""Data collectors for various sources."""

from .base import BaseCollector, CollectedItem
from .reddit import RedditCollector
from .news import NewsCollector
from .market_data import MarketDataCollector

__all__ = [
    "BaseCollector",
    "CollectedItem", 
    "RedditCollector",
    "NewsCollector",
    "MarketDataCollector",
]
