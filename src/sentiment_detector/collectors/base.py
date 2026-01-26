"""Base collector interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class AssetClass(str, Enum):
    """Asset class categories."""
    EQUITY = "equity"
    CRYPTO = "crypto"
    FOREX = "forex"
    COMMODITY = "commodity"


class DataSource(str, Enum):
    """Data source identifiers."""
    REDDIT = "reddit"
    TWITTER = "twitter"
    NEWS = "news"
    YAHOO_FINANCE = "yahoo_finance"


@dataclass
class CollectedItem:
    """A single collected data item."""
    source: DataSource
    source_id: str
    asset_class: AssetClass
    created_at: datetime
    title: Optional[str]
    content: str
    metadata: dict = field(default_factory=dict)
    collected_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate fields after initialization."""
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty")
        if not self.source_id:
            raise ValueError("source_id is required")


class BaseCollector(ABC):
    """
    Abstract base class for data collectors.
    
    All collectors should inherit from this class and implement
    the collect() method.
    """
    
    def __init__(self, source: DataSource):
        """
        Initialize collector.
        
        Args:
            source: The data source this collector handles
        """
        self.source = source
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def collect(
        self,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        limit: Optional[int] = None,
    ) -> list[CollectedItem]:
        """
        Collect data for a specific asset class and date range.
        
        Args:
            asset_class: The asset class to collect data for
            start_date: Start of date range
            end_date: End of date range
            limit: Maximum number of items to collect
            
        Returns:
            List of CollectedItem objects
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the collector is operational.
        
        Returns:
            True if healthy, False otherwise
        """
        pass
    
    def _classify_asset(self, text: str, keywords: dict[AssetClass, list[str]]) -> AssetClass:
        """
        Classify text into an asset class based on keywords.
        
        Args:
            text: Text to classify
            keywords: Dict mapping asset classes to keyword lists
            
        Returns:
            Most likely asset class
        """
        text_lower = text.lower()
        scores = {asset: 0 for asset in AssetClass}
        
        for asset_class, words in keywords.items():
            for word in words:
                if word.lower() in text_lower:
                    scores[asset_class] += 1
        
        # Return highest scoring, default to equity
        max_score = max(scores.values())
        if max_score == 0:
            return AssetClass.EQUITY
        
        return max(scores, key=scores.get)
