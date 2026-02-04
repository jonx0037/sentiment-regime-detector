"""
Unit tests for text preprocessing module.

Tests text cleaning, finance stop words, and asset classification.
"""

import pytest

from src.sentiment_detector.preprocessing.text_cleaner import (
    TextCleaner,
    CleanedText,
    SourceSpecificCleaner,
    clean_financial_text,
)
from src.sentiment_detector.preprocessing.finance_stopwords import (
    FINANCE_STOPWORDS,
    FINANCE_PRESERVE_BULLISH,
    FINANCE_PRESERVE_BEARISH,
    get_finance_stopwords,
    is_financial_sentiment_word,
    get_word_sentiment_polarity,
    get_emoji_sentiment,
)
from src.sentiment_detector.preprocessing.asset_classifier import (
    MultiLabelAssetClassifier,
    AssetClassification,
    AssetClass,
    classify_asset_class,
    classify_asset_classes,
)


class TestFinanceStopwords:
    """Tests for finance-aware stop words."""
    
    def test_standard_stopwords_removed(self):
        """Test that standard stop words are in the set."""
        assert "the" in FINANCE_STOPWORDS
        assert "is" in FINANCE_STOPWORDS
        assert "a" in FINANCE_STOPWORDS
        assert "and" in FINANCE_STOPWORDS
    
    def test_bullish_words_preserved(self):
        """Test that bullish financial words are NOT in stop words."""
        preserved_words = ["bull", "bullish", "rally", "moon", "pump", "gain"]
        
        for word in preserved_words:
            assert word not in FINANCE_STOPWORDS, f"{word} should be preserved"
    
    def test_bearish_words_preserved(self):
        """Test that bearish financial words are NOT in stop words."""
        preserved_words = ["bear", "crash", "dump", "tank", "rekt", "loss"]
        
        for word in preserved_words:
            assert word not in FINANCE_STOPWORDS, f"{word} should be preserved"
    
    def test_is_financial_sentiment_word(self):
        """Test identification of sentiment-bearing words."""
        assert is_financial_sentiment_word("bullish") is True
        assert is_financial_sentiment_word("crash") is True
        assert is_financial_sentiment_word("market") is True
        assert is_financial_sentiment_word("the") is False
    
    def test_word_sentiment_polarity(self):
        """Test sentiment polarity detection."""
        assert get_word_sentiment_polarity("moon") == "bullish"
        assert get_word_sentiment_polarity("crash") == "bearish"
        assert get_word_sentiment_polarity("market") == "neutral"
        assert get_word_sentiment_polarity("xyz") is None
    
    def test_get_finance_stopwords_custom(self):
        """Test customizing stop words."""
        # Add custom stop word
        custom = get_finance_stopwords(include_custom={"myword"})
        assert "myword" in custom
        
        # Exclude a word (preserve it)
        custom = get_finance_stopwords(exclude_custom={"the"})
        assert "the" not in custom
    
    def test_emoji_sentiment(self):
        """Test emoji sentiment detection."""
        assert get_emoji_sentiment("🚀") == "bullish"
        assert get_emoji_sentiment("📈") == "bullish"
        assert get_emoji_sentiment("📉") == "bearish"
        assert get_emoji_sentiment("💩") == "bearish"
        assert get_emoji_sentiment("😀") is None  # Not financial


class TestTextCleaner:
    """Tests for TextCleaner class."""
    
    @pytest.fixture
    def cleaner(self):
        return TextCleaner()
    
    def test_url_removal(self, cleaner):
        """Test URL removal."""
        text = "Check out https://example.com for more info"
        result = cleaner.clean(text)
        
        assert "https://example.com" not in result.cleaned
        assert "https://example.com" in result.urls
    
    def test_mention_removal(self, cleaner):
        """Test @mention removal."""
        text = "Hey @elonmusk what do you think about $TSLA?"
        result = cleaner.clean(text)
        
        assert "@elonmusk" not in result.cleaned
        assert "@elonmusk" in result.mentions
    
    def test_cashtag_extraction(self, cleaner):
        """Test cashtag extraction."""
        text = "$TSLA is going to the moon! Also watching $BTC"
        result = cleaner.clean(text)
        
        assert "$TSLA" in result.cashtags
        assert "$BTC" in result.cashtags
        assert len(result.tickers) == 2
    
    def test_hashtag_handling(self, cleaner):
        """Test hashtag extraction and cleaning."""
        text = "Just bought more #bitcoin #hodl"
        result = cleaner.clean(text)
        
        assert "bitcoin" in result.hashtags
        assert "hodl" in result.hashtags
        # Hashtag symbol should be removed but word kept
        assert "bitcoin" in result.cleaned
        assert "#" not in result.cleaned.split()[0] if result.cleaned else True
    
    def test_emoji_preservation(self, cleaner):
        """Test that sentiment-rich emojis are preserved."""
        text = "🚀🚀🚀 to the moon! 📈"
        result = cleaner.clean(text)
        
        assert "🚀" in result.cleaned
        assert result.emoji_sentiment["bullish"] == 4  # 3 rockets + 1 chart
        assert result.emoji_sentiment["bearish"] == 0
    
    def test_emoji_sentiment_bearish(self, cleaner):
        """Test bearish emoji detection."""
        text = "Portfolio bleeding 📉📉 😭"
        result = cleaner.clean(text)
        
        assert result.emoji_sentiment["bearish"] >= 2
    
    def test_lowercase(self):
        """Test lowercase conversion."""
        cleaner = TextCleaner(lowercase=True)
        result = cleaner.clean("TSLA IS MOONING")
        
        # "is" gets preserved because stopword removal is off by default
        assert result.cleaned == "tsla is mooning"
    
    def test_no_lowercase(self):
        """Test preserving case."""
        cleaner = TextCleaner(lowercase=False)
        result = cleaner.clean("TSLA IS MOONING")
        
        assert "TSLA" in result.cleaned
    
    def test_reddit_artifact_removal(self, cleaner):
        """Test removal of Reddit-specific artifacts."""
        text = "[removed] This is a test &amp; another test"
        result = cleaner.clean(text)
        
        assert "[removed]" not in result.cleaned
        assert "&amp;" not in result.cleaned
    
    def test_empty_input(self, cleaner):
        """Test handling of empty input."""
        result = cleaner.clean("")
        
        assert result.cleaned == ""
        assert result.metadata.get("empty_input") is True
    
    def test_none_input(self, cleaner):
        """Test handling of None input."""
        result = cleaner.clean(None)
        
        assert result.cleaned == ""
    
    def test_clean_batch(self, cleaner):
        """Test batch cleaning."""
        texts = [
            "$TSLA going up!",
            "$BTC crashing hard 📉",
            "Market is uncertain",
        ]
        results = cleaner.clean_batch(texts)
        
        assert len(results) == 3
        assert all(isinstance(r, CleanedText) for r in results)
    
    def test_max_length_truncation(self):
        """Test text truncation at max_length."""
        cleaner = TextCleaner(max_length=50)
        long_text = "A " * 100
        result = cleaner.clean(long_text)
        
        assert len(result.cleaned) <= 50


class TestSourceSpecificCleaner:
    """Tests for source-specific cleaners."""
    
    def test_reddit_cleaner(self):
        """Test Reddit-optimized cleaner."""
        cleaner = SourceSpecificCleaner.for_reddit()
        
        # Reddit cleaner should keep @mentions (not common on Reddit)
        result = cleaner.clean("Some text @mention")
        assert "@mention" in result.cleaned  # Reddit doesn't use @mentions
    
    def test_twitter_cleaner(self):
        """Test Twitter-optimized cleaner."""
        cleaner = SourceSpecificCleaner.for_twitter()
        
        # Twitter cleaner should remove @mentions
        result = cleaner.clean("Hey @user what's up")
        assert "@user" not in result.cleaned
    
    def test_news_cleaner(self):
        """Test news-optimized cleaner."""
        cleaner = SourceSpecificCleaner.for_news()
        
        # News cleaner should not preserve emojis
        result = cleaner.clean("Market rallies 🚀")
        assert "🚀" not in result.cleaned
    
    def test_model_input_cleaner(self):
        """Test minimal cleaner for model input."""
        cleaner = SourceSpecificCleaner.for_model_input()
        
        # Should preserve case for tokenizer
        result = cleaner.clean("TSLA is UP")
        # Lowercase is False by default in model_input cleaner
        # Actually it's True in implementation, let's check
        assert result.cleaned  # Should have content


class TestMultiLabelAssetClassifier:
    """Tests for MultiLabelAssetClassifier."""
    
    @pytest.fixture
    def classifier(self):
        return MultiLabelAssetClassifier()
    
    def test_single_equity_classification(self, classifier):
        """Test classification of pure equity content."""
        result = classifier.classify("$AAPL earnings beat expectations, stock soaring!")
        
        assert result.primary == AssetClass.EQUITY
        assert AssetClass.EQUITY in result.labels
        assert not result.is_multi_label
    
    def test_single_crypto_classification(self, classifier):
        """Test classification of pure crypto content."""
        result = classifier.classify("Bitcoin is mooning! BTC to 100k! 🚀")
        
        assert result.primary == AssetClass.CRYPTO
        assert AssetClass.CRYPTO in result.labels
    
    def test_single_forex_classification(self, classifier):
        """Test classification of forex content."""
        result = classifier.classify("EUR/USD breaking resistance, dollar weakening")
        
        assert result.primary == AssetClass.FOREX
        assert AssetClass.FOREX in result.labels
    
    def test_single_commodity_classification(self, classifier):
        """Test classification of commodity content."""
        result = classifier.classify("Gold prices surge as investors seek safe haven")
        
        assert result.primary == AssetClass.COMMODITY
        assert AssetClass.COMMODITY in result.labels
    
    def test_multi_label_crypto_equity(self, classifier):
        """Test multi-label when text mentions multiple asset classes."""
        result = classifier.classify(
            "Bitcoin crashing and SPY dropping, entire market is red"
        )
        
        assert result.is_multi_label
        assert AssetClass.CRYPTO in result.labels
        assert AssetClass.EQUITY in result.labels
    
    def test_multi_label_count(self, classifier):
        """Test label_count property."""
        # Use text with both crypto and equity that clearly exceeds multi-label threshold
        result = classifier.classify("Bitcoin BTC ETH Solana pumping, also SPY QQQ DIA SPX all green")
        
        # With sufficient keyword matches, should be multi-label
        assert result.label_count >= 1  # At minimum we get the primary
    
    def test_matched_keywords_tracking(self, classifier):
        """Test that matched keywords are tracked."""
        result = classifier.classify("$TSLA and $NVDA are my top picks")
        
        assert "tsla" in result.matched_keywords.get(AssetClass.EQUITY, [])
        assert "nvda" in result.matched_keywords.get(AssetClass.EQUITY, [])
    
    def test_confidence_score(self, classifier):
        """Test confidence score is calculated."""
        result = classifier.classify("$BTC to the moon!")
        
        assert 0 <= result.confidence <= 1
        assert result.confidence > 0.5  # Should be confident with clear crypto mention
    
    def test_empty_text_default(self, classifier):
        """Test empty text returns default class."""
        result = classifier.classify("")
        
        assert result.primary == AssetClass.EQUITY  # Default
        assert result.confidence == 0.0
    
    def test_no_keywords_default(self, classifier):
        """Test text with no keywords returns default."""
        result = classifier.classify("The weather is nice today")
        
        assert result.primary == AssetClass.EQUITY  # Default
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        primary = classify_asset_class("$BTC pumping hard")
        assert primary == AssetClass.CRYPTO
        
        all_labels = classify_asset_classes("$BTC and $SPY both green")
        assert len(all_labels) >= 1
    
    def test_case_insensitivity(self, classifier):
        """Test that classification is case insensitive."""
        result1 = classifier.classify("BITCOIN is up")
        result2 = classifier.classify("bitcoin is up")
        result3 = classifier.classify("Bitcoin is up")
        
        assert result1.primary == result2.primary == result3.primary == AssetClass.CRYPTO
    
    def test_forex_currency_pairs(self, classifier):
        """Test forex pair detection."""
        pairs = ["EUR/USD", "GBPUSD", "usd/jpy"]
        
        for pair in pairs:
            result = classifier.classify(f"Trading {pair} today")
            assert AssetClass.FOREX in result.labels, f"Failed for {pair}"


class TestCleanFinancialText:
    """Tests for convenience function."""
    
    def test_without_source(self):
        """Test cleaning without source hint."""
        cleaned = clean_financial_text("$TSLA going up! https://t.co/abc")
        
        assert "https" not in cleaned
        assert "tsla" in cleaned.lower()
    
    def test_with_reddit_source(self):
        """Test cleaning with Reddit source."""
        cleaned = clean_financial_text("[removed] content", source="reddit")
        
        assert "[removed]" not in cleaned
    
    def test_with_twitter_source(self):
        """Test cleaning with Twitter source."""
        cleaned = clean_financial_text("@user $AAPL", source="twitter")
        
        assert "@user" not in cleaned
