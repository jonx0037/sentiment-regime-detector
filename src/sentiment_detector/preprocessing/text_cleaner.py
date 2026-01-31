"""
Text Cleaning and Preprocessing Pipeline for Financial Sentiment Analysis.

This module provides explicit text preprocessing that:
1. Cleans raw text from various sources (Reddit, Twitter, News)
2. Handles financial-specific patterns (tickers, cashtags, numbers)
3. Preserves sentiment-rich content (emojis, punctuation emphasis)
4. Prepares text for transformer model input

Based on Draft-1 Section 3.3 specifications.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Optional, Union
import logging

from .finance_stopwords import (
    get_finance_stopwords,
    BULLISH_EMOJIS,
    BEARISH_EMOJIS,
    get_emoji_sentiment
)

logger = logging.getLogger(__name__)


@dataclass
class CleanedText:
    """
    Result of text cleaning operation.
    
    Attributes:
        original: Original input text
        cleaned: Cleaned text ready for model input
        tickers: Extracted ticker symbols
        cashtags: Extracted cashtags ($BTC, $SPY, etc.)
        urls: Removed URLs
        mentions: Removed @mentions
        hashtags: Extracted hashtags (cleaned)
        emoji_sentiment: Detected emoji sentiment indicators
        metadata: Additional cleaning metadata
    """
    original: str
    cleaned: str
    tickers: list[str]
    cashtags: list[str]
    urls: list[str]
    mentions: list[str]
    hashtags: list[str]
    emoji_sentiment: dict[str, int]  # {"bullish": count, "bearish": count}
    metadata: dict


class TextCleaner:
    """
    Financial text cleaning pipeline.
    
    Implements the preprocessing steps from Draft-1 Section 3.3:
    1. Tokenization awareness (for transformer input)
    2. Lowercasing (configurable)
    3. URL/mention removal
    4. Emoji handling (preserve sentiment-rich emojis)
    5. Stop word removal (finance-aware)
    6. Lemmatization (optional, via spaCy)
    
    Example:
        >>> cleaner = TextCleaner()
        >>> result = cleaner.clean("$TSLA is 🚀🚀🚀 to the moon! Check https://t.co/xyz @elonmusk")
        >>> print(result.cleaned)
        "tsla is 🚀🚀🚀 to moon"
        >>> print(result.cashtags)
        ["$TSLA"]
        >>> print(result.emoji_sentiment)
        {"bullish": 3, "bearish": 0}
    """
    
    # Common ticker symbol patterns
    CASHTAG_PATTERN = re.compile(r'\$([A-Z]{1,5})\b', re.IGNORECASE)
    
    # URL patterns
    URL_PATTERN = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|'
        r'(?:www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?'
    )
    
    # @mention pattern
    MENTION_PATTERN = re.compile(r'@[\w]+')
    
    # Hashtag pattern
    HASHTAG_PATTERN = re.compile(r'#(\w+)')
    
    # Multiple spaces/newlines
    WHITESPACE_PATTERN = re.compile(r'\s+')
    
    # Reddit/forum artifacts
    REDDIT_ARTIFACTS = re.compile(
        r'\[removed\]|\[deleted\]|&amp;|&lt;|&gt;|'
        r'Edit:|EDIT:|Edit\s*\d*:|TL;DR:|TLDR:',
        re.IGNORECASE
    )
    
    # Common ticker symbols (expanded list for validation)
    VALID_TICKERS: set[str] = {
        # Major indices/ETFs
        "SPY", "QQQ", "IWM", "DIA", "VTI", "VOO", "VXX", "UVXY",
        # Tech
        "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA",
        "AMD", "INTC", "NFLX", "CRM", "ORCL", "ADBE", "PYPL",
        # Finance
        "JPM", "BAC", "WFC", "GS", "MS", "C", "V", "MA", "AXP",
        # Crypto
        "BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "DOT", "AVAX", "MATIC",
        "SHIB", "LINK", "UNI", "AAVE", "BNB", "LTC",
        # Forex
        "EUR", "USD", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD",
        # Commodities
        "GLD", "SLV", "USO", "UNG", "WEAT", "CORN",
        # Meme stocks
        "GME", "AMC", "BB", "BBBY", "NOK", "PLTR", "WISH", "CLOV",
        # Other popular
        "ARKK", "COIN", "HOOD", "RIVN", "LCID", "NIO", "F", "GM",
    }
    
    def __init__(
        self,
        lowercase: bool = True,
        remove_urls: bool = True,
        remove_mentions: bool = True,
        preserve_emojis: bool = True,
        remove_stopwords: bool = False,  # Usually False for transformer input
        lemmatize: bool = False,
        min_length: int = 2,
        max_length: Optional[int] = None
    ):
        """
        Initialize text cleaner.
        
        Args:
            lowercase: Convert text to lowercase
            remove_urls: Remove URLs from text
            remove_mentions: Remove @mentions
            preserve_emojis: Keep emojis (especially sentiment-rich ones)
            remove_stopwords: Apply finance-aware stop word removal
            lemmatize: Apply lemmatization (requires spaCy)
            min_length: Minimum word length to keep
            max_length: Maximum text length (truncate if longer)
        """
        self.lowercase = lowercase
        self.remove_urls = remove_urls
        self.remove_mentions = remove_mentions
        self.preserve_emojis = preserve_emojis
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.min_length = min_length
        self.max_length = max_length
        
        # Load stop words if needed
        self.stopwords = get_finance_stopwords() if remove_stopwords else set()
        
        # Lazy load spaCy for lemmatization
        self._nlp = None
        
    def _get_nlp(self):
        """Lazy load spaCy model for lemmatization."""
        if self._nlp is None and self.lemmatize:
            try:
                import spacy
                self._nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
            except ImportError:
                logger.warning("spaCy not installed. Lemmatization disabled.")
                self.lemmatize = False
            except OSError:
                logger.warning("spaCy model 'en_core_web_sm' not found. Lemmatization disabled.")
                self.lemmatize = False
        return self._nlp
    
    def clean(self, text: str) -> CleanedText:
        """
        Clean a single text string.
        
        Args:
            text: Raw input text
            
        Returns:
            CleanedText object with cleaned text and extracted metadata
        """
        if not text or not isinstance(text, str):
            return CleanedText(
                original=str(text) if text else "",
                cleaned="",
                tickers=[],
                cashtags=[],
                urls=[],
                mentions=[],
                hashtags=[],
                emoji_sentiment={"bullish": 0, "bearish": 0},
                metadata={"empty_input": True}
            )
        
        original = text
        
        # Extract components before cleaning
        urls = self.URL_PATTERN.findall(text)
        mentions = self.MENTION_PATTERN.findall(text)
        hashtags = self.HASHTAG_PATTERN.findall(text)
        cashtags = self.CASHTAG_PATTERN.findall(text)
        
        # Normalize cashtags to uppercase
        cashtags = [f"${c.upper()}" for c in cashtags]
        
        # Identify valid tickers
        tickers = [c[1:] for c in cashtags if c[1:].upper() in self.VALID_TICKERS]
        
        # Count emoji sentiment
        emoji_sentiment = self._count_emoji_sentiment(text)
        
        # Start cleaning
        cleaned = text
        
        # Remove Reddit artifacts
        cleaned = self.REDDIT_ARTIFACTS.sub(' ', cleaned)
        
        # Handle URLs
        if self.remove_urls:
            cleaned = self.URL_PATTERN.sub(' ', cleaned)
        
        # Handle mentions
        if self.remove_mentions:
            cleaned = self.MENTION_PATTERN.sub(' ', cleaned)
        
        # Handle cashtags - replace with just the ticker
        cleaned = self.CASHTAG_PATTERN.sub(r'\1', cleaned)
        
        # Handle hashtags - remove # but keep word
        cleaned = self.HASHTAG_PATTERN.sub(r'\1', cleaned)
        
        # Handle emojis
        if not self.preserve_emojis:
            cleaned = self._remove_emojis(cleaned)
        
        # Normalize unicode
        cleaned = unicodedata.normalize('NFKD', cleaned)
        
        # Lowercase
        if self.lowercase:
            cleaned = cleaned.lower()
        
        # Remove extra whitespace
        cleaned = self.WHITESPACE_PATTERN.sub(' ', cleaned).strip()
        
        # Stop word removal
        if self.remove_stopwords:
            words = cleaned.split()
            words = [w for w in words if w.lower() not in self.stopwords]
            cleaned = ' '.join(words)
        
        # Minimum word length filter
        if self.min_length > 1:
            words = cleaned.split()
            words = [w for w in words if len(w) >= self.min_length or w in BULLISH_EMOJIS | BEARISH_EMOJIS]
            cleaned = ' '.join(words)
        
        # Lemmatization
        if self.lemmatize:
            cleaned = self._lemmatize_text(cleaned)
        
        # Truncate if needed
        if self.max_length and len(cleaned) > self.max_length:
            cleaned = cleaned[:self.max_length].rsplit(' ', 1)[0]
        
        # Final whitespace cleanup
        cleaned = self.WHITESPACE_PATTERN.sub(' ', cleaned).strip()
        
        return CleanedText(
            original=original,
            cleaned=cleaned,
            tickers=tickers,
            cashtags=cashtags,
            urls=urls,
            mentions=mentions,
            hashtags=hashtags,
            emoji_sentiment=emoji_sentiment,
            metadata={
                "original_length": len(original),
                "cleaned_length": len(cleaned),
                "reduction_pct": 1 - (len(cleaned) / len(original)) if original else 0,
                "ticker_count": len(tickers),
                "cashtag_count": len(cashtags),
            }
        )
    
    def clean_batch(self, texts: list[str]) -> list[CleanedText]:
        """
        Clean a batch of texts.
        
        Args:
            texts: List of raw text strings
            
        Returns:
            List of CleanedText objects
        """
        return [self.clean(text) for text in texts]
    
    def clean_to_string(self, text: str) -> str:
        """
        Clean text and return just the cleaned string.
        
        Convenience method for simple use cases.
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text string
        """
        return self.clean(text).cleaned
    
    def _count_emoji_sentiment(self, text: str) -> dict[str, int]:
        """Count bullish and bearish emojis in text."""
        bullish = 0
        bearish = 0
        
        for char in text:
            if char in BULLISH_EMOJIS:
                bullish += 1
            elif char in BEARISH_EMOJIS:
                bearish += 1
        
        return {"bullish": bullish, "bearish": bearish}
    
    def _remove_emojis(self, text: str) -> str:
        """Remove all emojis from text."""
        # Unicode emoji pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub('', text)
    
    def _lemmatize_text(self, text: str) -> str:
        """Apply lemmatization using spaCy."""
        nlp = self._get_nlp()
        if nlp is None:
            return text
        
        doc = nlp(text)
        return ' '.join([token.lemma_ for token in doc])


class SourceSpecificCleaner:
    """
    Source-specific text cleaning with optimized settings.
    
    Different sources (Reddit, Twitter, News) have different characteristics
    and require slightly different preprocessing.
    """
    
    @staticmethod
    def for_reddit() -> TextCleaner:
        """Get cleaner optimized for Reddit content."""
        return TextCleaner(
            lowercase=True,
            remove_urls=True,
            remove_mentions=False,  # Reddit doesn't use @mentions much
            preserve_emojis=True,
            remove_stopwords=False,
            max_length=512  # Longer content typical on Reddit
        )
    
    @staticmethod
    def for_twitter() -> TextCleaner:
        """Get cleaner optimized for Twitter/X content."""
        return TextCleaner(
            lowercase=True,
            remove_urls=True,
            remove_mentions=True,  # Many @mentions on Twitter
            preserve_emojis=True,
            remove_stopwords=False,
            max_length=280  # Twitter character limit
        )
    
    @staticmethod
    def for_news() -> TextCleaner:
        """Get cleaner optimized for financial news."""
        return TextCleaner(
            lowercase=True,
            remove_urls=True,
            remove_mentions=True,
            preserve_emojis=False,  # News rarely has emojis
            remove_stopwords=False,
            max_length=1024  # News articles can be long
        )
    
    @staticmethod
    def for_model_input() -> TextCleaner:
        """Get minimal cleaner for direct transformer input."""
        return TextCleaner(
            lowercase=False,  # Let tokenizer handle casing
            remove_urls=True,
            remove_mentions=True,
            preserve_emojis=True,
            remove_stopwords=False,  # Transformers use full context
            lemmatize=False,  # Tokenizer handles this
            max_length=512  # Common transformer max length
        )


def clean_financial_text(
    text: str,
    source: Optional[str] = None
) -> str:
    """
    Convenience function to clean financial text.
    
    Args:
        text: Raw text to clean
        source: Optional source hint ('reddit', 'twitter', 'news')
        
    Returns:
        Cleaned text string
    """
    if source == "reddit":
        cleaner = SourceSpecificCleaner.for_reddit()
    elif source == "twitter":
        cleaner = SourceSpecificCleaner.for_twitter()
    elif source == "news":
        cleaner = SourceSpecificCleaner.for_news()
    else:
        cleaner = SourceSpecificCleaner.for_model_input()
    
    return cleaner.clean_to_string(text)
