"""
Multi-Label Asset Classification for Financial Text.

Per Draft-1 Section 3.3, this module provides multi-label asset classification
because "Some texts reference multiple asset classes."

This extends the single-label classification in collectors/base.py to support
texts that mention multiple asset classes (e.g., "BTC and SPY both dropping").
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union
import re
import logging

logger = logging.getLogger(__name__)


class AssetClass(str, Enum):
    """Asset class categories matching collectors/base.py."""
    EQUITY = "equity"
    CRYPTO = "crypto"
    FOREX = "forex"
    COMMODITY = "commodity"


@dataclass
class AssetClassification:
    """
    Result of multi-label asset classification.
    
    Attributes:
        primary: Most likely asset class
        labels: All detected asset classes
        scores: Confidence scores per asset class
        matched_keywords: Keywords that matched per asset class
        confidence: Overall classification confidence
    """
    primary: AssetClass
    labels: list[AssetClass]
    scores: dict[AssetClass, float]
    matched_keywords: dict[AssetClass, list[str]]
    confidence: float
    
    @property
    def is_multi_label(self) -> bool:
        """Check if text references multiple asset classes."""
        return len(self.labels) > 1
    
    @property
    def label_count(self) -> int:
        """Number of asset classes detected."""
        return len(self.labels)


# Comprehensive keyword dictionaries per asset class
# Organized by specificity (more specific keywords = higher weight)

EQUITY_KEYWORDS: dict[str, float] = {
    # Major indices
    "spy": 1.5, "qqq": 1.5, "dia": 1.5, "iwm": 1.5, "voo": 1.5,
    "s&p": 1.3, "s&p500": 1.5, "sp500": 1.5, "nasdaq": 1.3, "dow": 1.2,
    "russell": 1.2, "nyse": 1.3, "djia": 1.5,
    # Sector ETFs
    "xlf": 1.3, "xle": 1.3, "xlk": 1.3, "xlv": 1.3, "xlu": 1.3,
    "arkk": 1.3, "arkw": 1.3, "arkf": 1.3,
    # Tech megacaps
    "aapl": 1.5, "apple": 1.2, "msft": 1.5, "microsoft": 1.2,
    "googl": 1.5, "goog": 1.5, "google": 1.2, "alphabet": 1.2,
    "amzn": 1.5, "amazon": 1.2, "meta": 1.3, "facebook": 1.2,
    "tsla": 1.5, "tesla": 1.2, "nvda": 1.5, "nvidia": 1.2,
    "amd": 1.5, "intc": 1.5, "intel": 1.2,
    # Finance
    "jpm": 1.5, "jpmorgan": 1.2, "bac": 1.5, "gs": 1.5, "goldman": 1.2,
    "wfc": 1.5, "wells fargo": 1.2, "ms": 1.3, "morgan stanley": 1.2,
    "v": 1.2, "visa": 1.2, "ma": 1.2, "mastercard": 1.2,
    # Meme stocks
    "gme": 1.5, "gamestop": 1.3, "amc": 1.5, "bb": 1.2, "blackberry": 1.2,
    "pltr": 1.5, "palantir": 1.3, "nok": 1.2, "nokia": 1.2,
    # General equity terms
    "stock": 0.8, "stocks": 0.8, "equity": 0.9, "equities": 0.9,
    "share": 0.7, "shares": 0.7, "market": 0.5, "markets": 0.5,
    "earnings": 0.8, "eps": 0.9, "revenue": 0.7, "dividend": 0.8,
    "ipo": 0.9, "buyback": 0.8, "split": 0.7,
    # Broker/exchange
    "robinhood": 0.8, "schwab": 0.8, "fidelity": 0.8, "vanguard": 0.8,
}

CRYPTO_KEYWORDS: dict[str, float] = {
    # Major coins
    "btc": 1.5, "bitcoin": 1.5, "eth": 1.5, "ethereum": 1.5,
    "sol": 1.3, "solana": 1.5, "ada": 1.3, "cardano": 1.5,
    "xrp": 1.5, "ripple": 1.5, "doge": 1.5, "dogecoin": 1.5,
    "bnb": 1.5, "ltc": 1.5, "litecoin": 1.5,
    "dot": 1.3, "polkadot": 1.5, "avax": 1.3, "avalanche": 1.5,
    "matic": 1.5, "polygon": 1.5, "link": 1.2, "chainlink": 1.5,
    "shib": 1.5, "shibainu": 1.5, "shiba": 1.3,
    # DeFi
    "uni": 1.3, "uniswap": 1.5, "aave": 1.5, "sushi": 1.3,
    "comp": 1.3, "compound": 1.3, "mkr": 1.3, "maker": 1.3,
    "crv": 1.3, "curve": 1.2,
    # Layer 2
    "arb": 1.3, "arbitrum": 1.5, "op": 1.2, "optimism": 1.5,
    # Stablecoins
    "usdt": 1.3, "tether": 1.3, "usdc": 1.3, "dai": 1.3, "busd": 1.3,
    # Exchanges
    "binance": 1.2, "coinbase": 1.2, "kraken": 1.2, "ftx": 1.2,
    "bybit": 1.2, "kucoin": 1.2,
    # General crypto terms
    "crypto": 1.0, "cryptocurrency": 1.0, "cryptocurrencies": 1.0,
    "blockchain": 0.9, "defi": 1.0, "nft": 0.9, "nfts": 0.9,
    "altcoin": 1.0, "altcoins": 1.0, "token": 0.8, "tokens": 0.8,
    "wallet": 0.7, "mining": 0.8, "staking": 0.9, "yield": 0.6,
    "hodl": 1.0, "satoshi": 1.0, "sats": 1.0, "gwei": 1.0,
    "moon": 0.7, "mooning": 0.8, "rekt": 0.9, "wagmi": 0.9, "ngmi": 0.9,
    "web3": 0.9, "metaverse": 0.8,
}

FOREX_KEYWORDS: dict[str, float] = {
    # Major pairs
    "eurusd": 1.5, "eur/usd": 1.5, "gbpusd": 1.5, "gbp/usd": 1.5,
    "usdjpy": 1.5, "usd/jpy": 1.5, "usdchf": 1.5, "usd/chf": 1.5,
    "audusd": 1.5, "aud/usd": 1.5, "usdcad": 1.5, "usd/cad": 1.5,
    "nzdusd": 1.5, "nzd/usd": 1.5,
    # Cross pairs
    "eurgbp": 1.5, "eur/gbp": 1.5, "eurjpy": 1.5, "eur/jpy": 1.5,
    "gbpjpy": 1.5, "gbp/jpy": 1.5,
    # Individual currencies (context dependent)
    "dollar": 0.9, "usd": 0.8, "euro": 0.9, "eur": 0.8,
    "pound": 0.9, "sterling": 0.9, "gbp": 0.8,
    "yen": 0.9, "jpy": 0.8,
    "franc": 0.8, "chf": 0.8,
    "aussie": 0.8, "aud": 0.8, "kiwi": 0.7, "nzd": 0.8,
    "loonie": 0.8, "cad": 0.8,
    # General forex terms
    "forex": 1.0, "fx": 0.9, "currency": 0.8, "currencies": 0.8,
    "exchange rate": 0.9, "pip": 0.9, "pips": 0.9,
    # Central banks
    "fed": 0.8, "fomc": 0.9, "ecb": 0.9, "boe": 0.9, "boj": 0.9,
    "rba": 0.9, "snb": 0.9, "rbnz": 0.9,
    "rate hike": 0.8, "rate cut": 0.8, "hawkish": 0.7, "dovish": 0.7,
}

COMMODITY_KEYWORDS: dict[str, float] = {
    # Precious metals
    "gold": 1.2, "xauusd": 1.5, "xau": 1.3, "gld": 1.3,
    "silver": 1.2, "xagusd": 1.5, "xag": 1.3, "slv": 1.3,
    "platinum": 1.2, "palladium": 1.2,
    # Energy
    "oil": 1.0, "crude": 1.2, "wti": 1.3, "brent": 1.3,
    "uso": 1.3, "uco": 1.3, "xle": 1.0,
    "gas": 0.8, "natural gas": 1.2, "natgas": 1.3, "ung": 1.3,
    # Agriculture
    "wheat": 1.2, "weat": 1.3, "corn": 1.0, "corn futures": 1.3,
    "soybean": 1.2, "soybeans": 1.2, "coffee": 1.0, "sugar": 0.9,
    "cotton": 1.0, "cocoa": 1.0,
    # General commodity terms
    "commodity": 1.0, "commodities": 1.0, "futures": 0.8,
    "opec": 1.0, "inventory": 0.6, "inventories": 0.6,
    "supply": 0.5, "demand": 0.5,
}

# Compile all keywords into a master dictionary
ALL_KEYWORDS: dict[AssetClass, dict[str, float]] = {
    AssetClass.EQUITY: EQUITY_KEYWORDS,
    AssetClass.CRYPTO: CRYPTO_KEYWORDS,
    AssetClass.FOREX: FOREX_KEYWORDS,
    AssetClass.COMMODITY: COMMODITY_KEYWORDS,
}


class MultiLabelAssetClassifier:
    """
    Multi-label asset classification for financial text.
    
    Supports classifying text into one or more asset classes based on
    keyword matching with weighted scores.
    
    Example:
        >>> classifier = MultiLabelAssetClassifier()
        >>> result = classifier.classify("Bitcoin and S&P 500 both crashing today!")
        >>> print(result.labels)
        [AssetClass.CRYPTO, AssetClass.EQUITY]
        >>> print(result.primary)
        AssetClass.CRYPTO  # Higher score due to more specific keyword
    """
    
    def __init__(
        self,
        min_score_threshold: float = 0.5,
        multi_label_threshold: float = 0.7,
        default_class: AssetClass = AssetClass.EQUITY,
        custom_keywords: Optional[dict[AssetClass, dict[str, float]]] = None
    ):
        """
        Initialize classifier.
        
        Args:
            min_score_threshold: Minimum score to assign any label
            multi_label_threshold: Ratio of secondary/primary score needed
                                   for multi-label assignment
            default_class: Default asset class when no keywords match
            custom_keywords: Optional custom keyword dictionary to merge
        """
        self.min_score_threshold = min_score_threshold
        self.multi_label_threshold = multi_label_threshold
        self.default_class = default_class
        
        # Build keyword dictionary
        self.keywords = {ac: dict(kw) for ac, kw in ALL_KEYWORDS.items()}
        
        if custom_keywords:
            for asset_class, kw_dict in custom_keywords.items():
                if asset_class in self.keywords:
                    self.keywords[asset_class].update(kw_dict)
                else:
                    self.keywords[asset_class] = kw_dict
        
        # Build regex patterns for efficient matching
        self._build_patterns()
    
    def _build_patterns(self):
        """Build compiled regex patterns for keyword matching."""
        self.patterns: dict[AssetClass, list[tuple[re.Pattern, str, float]]] = {}
        
        for asset_class, kw_dict in self.keywords.items():
            patterns = []
            for keyword, weight in kw_dict.items():
                # Create word-boundary pattern
                # Handle special characters in keywords
                escaped = re.escape(keyword)
                # Allow for $ prefix (cashtags)
                pattern = re.compile(
                    r'(?:^|\s|\$)' + escaped + r'(?:\s|$|[.,!?;:])',
                    re.IGNORECASE
                )
                patterns.append((pattern, keyword, weight))
            self.patterns[asset_class] = patterns
    
    def classify(self, text: str) -> AssetClassification:
        """
        Classify text into asset class(es).
        
        Args:
            text: Text to classify
            
        Returns:
            AssetClassification with all detected labels
        """
        if not text or not isinstance(text, str):
            return AssetClassification(
                primary=self.default_class,
                labels=[self.default_class],
                scores={self.default_class: 0.0},
                matched_keywords={},
                confidence=0.0
            )
        
        text_lower = text.lower()
        
        # Calculate scores for each asset class
        scores: dict[AssetClass, float] = {}
        matched: dict[AssetClass, list[str]] = {}
        
        for asset_class, patterns in self.patterns.items():
            score = 0.0
            matches = []
            
            for pattern, keyword, weight in patterns:
                if pattern.search(text_lower):
                    score += weight
                    matches.append(keyword)
            
            scores[asset_class] = score
            matched[asset_class] = matches
        
        # Determine labels
        max_score = max(scores.values())
        
        if max_score < self.min_score_threshold:
            # No strong signal - return default
            return AssetClassification(
                primary=self.default_class,
                labels=[self.default_class],
                scores=scores,
                matched_keywords=matched,
                confidence=0.0
            )
        
        # Find primary class
        primary = max(scores, key=scores.get)
        
        # Find additional labels (multi-label)
        labels = [primary]
        for asset_class, score in scores.items():
            if asset_class != primary and score >= max_score * self.multi_label_threshold:
                labels.append(asset_class)
        
        # Calculate confidence
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return AssetClassification(
            primary=primary,
            labels=labels,
            scores=scores,
            matched_keywords={ac: kw for ac, kw in matched.items() if kw},
            confidence=confidence
        )
    
    def classify_batch(
        self,
        texts: list[str]
    ) -> list[AssetClassification]:
        """
        Classify a batch of texts.
        
        Args:
            texts: List of texts to classify
            
        Returns:
            List of AssetClassification results
        """
        return [self.classify(text) for text in texts]
    
    def get_primary_label(self, text: str) -> AssetClass:
        """
        Get just the primary asset class label.
        
        Convenience method for simple use cases.
        
        Args:
            text: Text to classify
            
        Returns:
            Primary AssetClass
        """
        return self.classify(text).primary
    
    def get_all_labels(self, text: str) -> list[AssetClass]:
        """
        Get all detected asset class labels.
        
        Args:
            text: Text to classify
            
        Returns:
            List of detected AssetClass values
        """
        return self.classify(text).labels


# Convenience instance
_default_classifier: Optional[MultiLabelAssetClassifier] = None


def get_classifier() -> MultiLabelAssetClassifier:
    """Get the default classifier instance (singleton)."""
    global _default_classifier
    if _default_classifier is None:
        _default_classifier = MultiLabelAssetClassifier()
    return _default_classifier


def classify_asset_class(text: str) -> AssetClass:
    """
    Convenience function to classify text to primary asset class.
    
    Args:
        text: Text to classify
        
    Returns:
        Primary AssetClass
    """
    return get_classifier().get_primary_label(text)


def classify_asset_classes(text: str) -> list[AssetClass]:
    """
    Convenience function to get all asset classes from text.
    
    Args:
        text: Text to classify
        
    Returns:
        List of detected AssetClass values
    """
    return get_classifier().get_all_labels(text)
