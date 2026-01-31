"""
Finance-Aware Stop Words for Sentiment Analysis.

This module provides a curated list of stop words that:
1. Removes standard English stop words (the, a, an, is, etc.)
2. PRESERVES finance-specific sentiment indicators (bull, bear, crash, rally, etc.)

Based on Loughran and McDonald (2011) financial sentiment lexicon principles
and adapted for social media financial discourse.
"""

from typing import Optional, Set


# Standard English stop words to REMOVE
# (These carry little sentiment meaning in financial context)
STANDARD_STOP_WORDS: Set[str] = {
    # Articles
    "a", "an", "the",
    # Pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those",
    # Verbs (common, low-sentiment)
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing",
    # Prepositions
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then",
    "once",
    # Conjunctions
    "and", "but", "if", "or", "because", "as", "until", "while", "of", "so",
    "than", "too", "very", "just",
    # Modal verbs (often neutral in financial context)
    "can", "will", "would", "could", "should", "may", "might", "must", "shall",
    # Other common words
    "here", "there", "when", "where", "why", "how", "all", "each", "few",
    "more", "most", "other", "some", "such", "only", "own", "same", "also",
    "any", "both", "no", "nor", "not", "now",
    # Numbers (as words)
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    # Social media artifacts
    "rt", "via", "lol", "lmao", "omg", "btw", "imo", "imho", "tbh", "ngl",
    # Common but low-info
    "get", "got", "getting", "go", "going", "gone", "went", "come", "coming",
    "came", "see", "saw", "seen", "seeing", "look", "looking", "looked",
    "like", "think", "thought", "know", "knew", "known", "say", "said",
    "want", "wanted", "need", "needed", "make", "made", "making",
}


# Finance-specific words to PRESERVE (these carry sentiment)
# Organized by sentiment polarity
FINANCE_PRESERVE_BULLISH: Set[str] = {
    # General bullish terms
    "bull", "bullish", "bulls", "buy", "buying", "bought", "long", "longs",
    "rally", "rallies", "rallying", "rallied", "surge", "surging", "surged",
    "soar", "soaring", "soared", "spike", "spiking", "spiked",
    "moon", "mooning", "mooned", "rocket", "rocketship", "takeoff",
    "breakout", "breakouts", "breakthrough",
    "pump", "pumping", "pumped", "rip", "ripping", "ripped",
    "gain", "gains", "gaining", "gainz",
    "profit", "profits", "profitable", "profiting",
    "win", "winning", "winner", "winners",
    "green", "greens",
    "up", "higher", "high", "highs", "ath",  # all-time high
    "growth", "growing", "grow",
    "strong", "stronger", "strength",
    "beat", "beats", "beating",
    "outperform", "outperforming", "outperformed",
    "upgrade", "upgrades", "upgraded",
    "accumulate", "accumulating", "accumulation",
    "undervalued", "cheap", "discount", "discounted",
    "opportunity", "opportunities",
    "recovery", "recovering", "recovered", "rebound", "rebounding",
    "positive", "optimistic", "optimism",
    "confidence", "confident",
    # Crypto-specific bullish
    "hodl", "hodling", "hodler", "hodlers",
    "diamond", "hands", "diamondhands",
    "wagmi",  # we're all gonna make it
    "gm",  # good morning (crypto culture)
    "bullrun", "supercycle",
    "fomo",  # fear of missing out (can drive buying)
    # Options bullish
    "calls", "call",
    "tendies",  # WSB term for profits
    "yolo",  # sometimes bullish sentiment
}


FINANCE_PRESERVE_BEARISH: Set[str] = {
    # General bearish terms
    "bear", "bearish", "bears", "sell", "selling", "sold", "short", "shorts",
    "crash", "crashing", "crashed", "crashes",
    "dump", "dumping", "dumped", "dumps",
    "tank", "tanking", "tanked", "tanks",
    "plunge", "plunging", "plunged",
    "collapse", "collapsing", "collapsed",
    "drop", "dropping", "dropped", "drops",
    "fall", "falling", "fell", "falls",
    "decline", "declining", "declined", "declines",
    "sink", "sinking", "sunk",
    "slide", "sliding", "slid",
    "tumble", "tumbling", "tumbled",
    "pullback", "pullbacks", "correction", "corrections",
    "loss", "losses", "losing", "lost",
    "red", "reds", "blood", "bloody", "bloodbath",
    "down", "lower", "low", "lows",
    "weak", "weaker", "weakness",
    "miss", "missed", "misses", "missing",
    "underperform", "underperforming", "underperformed",
    "downgrade", "downgrades", "downgraded",
    "overvalued", "expensive", "bubble",
    "recession", "recessionary",
    "fear", "fears", "fearful", "panic", "panicking", "panicked",
    "negative", "pessimistic", "pessimism",
    "risk", "risks", "risky",
    "warning", "warnings", "warn", "warned",
    "trouble", "troubled", "troubles",
    "concern", "concerns", "concerning", "concerned",
    "crisis", "crises",
    "default", "defaults", "defaulting", "defaulted",
    "bankruptcy", "bankrupt",
    "fraud", "fraudulent", "scam", "scams",
    # Crypto-specific bearish
    "rekt", "wrecked",
    "paperhands", "paper",
    "ngmi",  # not gonna make it
    "rug", "rugged", "rugpull",
    "ponzi",
    "fud",  # fear, uncertainty, doubt
    # Options bearish
    "puts", "put",
    # Volatility-related
    "volatile", "volatility", "vix",
}


FINANCE_PRESERVE_NEUTRAL_IMPORTANT: Set[str] = {
    # Market structure terms (important context)
    "market", "markets", "stock", "stocks", "share", "shares",
    "trade", "trades", "trading", "traded", "trader", "traders",
    "invest", "investing", "investment", "investments", "investor", "investors",
    "portfolio", "portfolios", "position", "positions",
    "price", "prices", "priced", "pricing",
    "volume", "volumes",
    "liquidity", "liquid", "illiquid",
    "spread", "spreads",
    "bid", "ask", "bids", "asks",
    "support", "resistance",
    "trend", "trends", "trending",
    "momentum", "momemtum",  # common typo
    "sentiment", "sentiments",
    # Asset classes
    "equity", "equities", "bond", "bonds", "crypto", "cryptocurrency",
    "forex", "fx", "currency", "currencies", "commodity", "commodities",
    "gold", "silver", "oil", "gas", "wheat", "corn",
    "bitcoin", "btc", "ethereum", "eth", "solana", "sol",
    # Financial metrics
    "earnings", "revenue", "revenues", "eps", "pe", "ratio",
    "dividend", "dividends", "yield", "yields",
    "margin", "margins",
    "debt", "leverage", "leveraged",
    "cash", "cashflow",
    "valuation", "valuations",
    # Events
    "fed", "fomc", "rate", "rates", "hike", "hikes", "cut", "cuts",
    "inflation", "inflationary", "deflation", "deflationary",
    "gdp", "unemployment", "jobs", "payroll", "payrolls",
    "cpi", "ppi",
    "ipo", "merger", "acquisition",
    # Time references (important for regime detection)
    "today", "tomorrow", "yesterday", "week", "month", "year", "quarter",
    "morning", "afternoon", "evening", "overnight",
    "open", "close", "opening", "closing",
    # Magnitude words
    "huge", "massive", "significant", "major", "minor", "slight",
}


# Combined set of words to PRESERVE
FINANCE_PRESERVE_WORDS: Set[str] = (
    FINANCE_PRESERVE_BULLISH |
    FINANCE_PRESERVE_BEARISH |
    FINANCE_PRESERVE_NEUTRAL_IMPORTANT
)


# The actual stop words to use (standard minus preserved)
FINANCE_STOPWORDS: Set[str] = STANDARD_STOP_WORDS - FINANCE_PRESERVE_WORDS


def get_finance_stopwords(
    include_custom: Optional[Set[str]] = None,
    exclude_custom: Optional[Set[str]] = None
) -> Set[str]:
    """
    Get the set of finance-aware stop words.
    
    Args:
        include_custom: Additional stop words to include
        exclude_custom: Words to remove from stop words (preserve)
        
    Returns:
        Set of stop words customized for financial text
    """
    stopwords = FINANCE_STOPWORDS.copy()
    
    if include_custom:
        stopwords |= include_custom
    
    if exclude_custom:
        stopwords -= exclude_custom
    
    return stopwords


def is_financial_sentiment_word(word: str) -> bool:
    """
    Check if a word carries financial sentiment meaning.
    
    Args:
        word: Word to check (will be lowercased)
        
    Returns:
        True if word should be preserved for sentiment analysis
    """
    return word.lower() in FINANCE_PRESERVE_WORDS


def get_word_sentiment_polarity(word: str) -> Optional[str]:
    """
    Get the sentiment polarity of a financial word.
    
    Args:
        word: Word to check
        
    Returns:
        "bullish", "bearish", "neutral", or None if not a financial word
    """
    word_lower = word.lower()
    
    if word_lower in FINANCE_PRESERVE_BULLISH:
        return "bullish"
    elif word_lower in FINANCE_PRESERVE_BEARISH:
        return "bearish"
    elif word_lower in FINANCE_PRESERVE_NEUTRAL_IMPORTANT:
        return "neutral"
    else:
        return None


# Emoji sentiment mappings (per Draft-1 Section 3.3)
BULLISH_EMOJIS: Set[str] = {
    "🚀", "📈", "💰", "💵", "💎", "🙌", "💪", "🔥", "✅", "🎯",
    "🤑", "💸", "📊", "⬆️", "🟢", "🌕", "🌙", "👆", "🆙",
}

BEARISH_EMOJIS: Set[str] = {
    "📉", "💩", "🩸", "❌", "⬇️", "🔴", "😱", "😰", "💀", "☠️",
    "🤮", "📴", "👎", "🆘", "⚠️", "🚨", "😭", "🥺", "👇",
}


def get_emoji_sentiment(emoji: str) -> Optional[str]:
    """
    Get sentiment polarity for an emoji.
    
    Args:
        emoji: Emoji character to check
        
    Returns:
        "bullish", "bearish", or None
    """
    if emoji in BULLISH_EMOJIS:
        return "bullish"
    elif emoji in BEARISH_EMOJIS:
        return "bearish"
    return None
