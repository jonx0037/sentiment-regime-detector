#!/usr/bin/env python3
"""
Seed database with sample financial texts for testing.

This script populates the raw_texts table with diverse financial content
across all asset classes (equity, crypto, forex, commodity) with varying
sentiment (positive, negative, neutral).

Usage:
    python scripts/seed_data.py
"""

import asyncio
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sentiment_detector.core.config import get_settings
from sentiment_detector.models.text_record import RawText

# Sample financial texts with known sentiment tendencies
SAMPLE_TEXTS = [
    # EQUITY - Positive
    {
        "source": "reddit",
        "source_id": "reddit_eq_pos_1",
        "asset_class": "equity",
        "title": "Tech stocks rally on strong earnings",
        "content": "Major tech companies exceeded expectations this quarter, driving the NASDAQ to new highs. "
                   "Investors are optimistic about AI integration boosting productivity and margins. "
                   "Strong guidance from industry leaders signals sustained growth momentum.",
        "hours_ago": 2,
        "metadata": {"subreddit": "wallstreetbets", "score": 1247, "num_comments": 83},
    },
    {
        "source": "news",
        "source_id": "news_eq_pos_1",
        "asset_class": "equity",
        "title": "S&P 500 reaches record high amid economic optimism",
        "content": "The S&P 500 climbed to a new all-time high today as investors welcomed better-than-expected "
                   "economic data. Job growth remained robust, and inflation showed signs of moderating. "
                   "Analysts are revising their year-end targets upward.",
        "hours_ago": 5,
        "metadata": {"publisher": "Bloomberg", "author": "Market Reporter"},
    },
    
    # EQUITY - Negative
    {
        "source": "reddit",
        "source_id": "reddit_eq_neg_1",
        "asset_class": "equity",
        "title": "Market correction incoming?",
        "content": "The recent volatility is concerning. Overvalued tech stocks are showing cracks, and "
                   "institutional selling has accelerated. Historical P/E ratios suggest we're due for "
                   "a significant pullback. Risk management is crucial here.",
        "hours_ago": 3,
        "metadata": {"subreddit": "investing", "score": 892, "num_comments": 156},
    },
    {
        "source": "news",
        "source_id": "news_eq_neg_1",
        "asset_class": "equity",
        "title": "Dow plunges 500 points on recession fears",
        "content": "Stocks tumbled today as disappointing manufacturing data fueled recession concerns. "
                   "The Dow Jones Industrial Average dropped 500 points, and the VIX spiked above 30. "
                   "Investors are fleeing to safe-haven assets amid heightened uncertainty.",
        "hours_ago": 1,
        "metadata": {"publisher": "Reuters", "author": "Financial News Team"},
    },
    
    # EQUITY - Neutral
    {
        "source": "news",
        "source_id": "news_eq_neu_1",
        "asset_class": "equity",
        "title": "Markets end mixed as investors digest Fed minutes",
        "content": "Major indices finished relatively flat today as traders analyzed the latest Federal Reserve "
                   "meeting minutes. The S&P 500 edged up 0.1% while the Nasdaq closed unchanged. "
                   "Volume was below average ahead of tomorrow's economic reports.",
        "hours_ago": 4,
        "metadata": {"publisher": "CNBC", "author": "Markets Desk"},
    },
    
    # CRYPTO - Positive
    {
        "source": "reddit",
        "source_id": "reddit_crypto_pos_1",
        "asset_class": "crypto",
        "title": "Bitcoin surges past $70K!",
        "content": "BTC just broke through the $70,000 resistance level on massive volume! "
                   "ETF inflows are accelerating and institutional adoption continues to grow. "
                   "The halving cycle dynamics are playing out perfectly. Bullish momentum is strong!",
        "hours_ago": 1,
        "metadata": {"subreddit": "cryptocurrency", "score": 3421, "num_comments": 789},
    },
    {
        "source": "news",
        "source_id": "news_crypto_pos_1",
        "asset_class": "crypto",
        "title": "Ethereum upgrade successful, network performance improved",
        "content": "The latest Ethereum network upgrade has been successfully deployed, resulting in "
                   "faster transaction speeds and lower gas fees. Developers are enthusiastic about "
                   "the enhanced scalability, which could drive wider adoption of DeFi applications.",
        "hours_ago": 6,
        "metadata": {"publisher": "CoinDesk", "author": "Crypto Reporter"},
    },
    
    # CRYPTO - Negative
    {
        "source": "reddit",
        "source_id": "reddit_crypto_neg_1",
        "asset_class": "crypto",
        "title": "Crypto winter continues",
        "content": "Another exchange just halted withdrawals. The regulatory crackdown is intensifying, "
                   "and institutional investors are pulling back. Liquidations are cascading across "
                   "the market. This bear market could last longer than many expect.",
        "hours_ago": 2,
        "metadata": {"subreddit": "bitcoin", "score": 2156, "num_comments": 412},
    },
    {
        "source": "news",
        "source_id": "news_crypto_neg_1",
        "asset_class": "crypto",
        "title": "SEC announces new crypto enforcement actions",
        "content": "The Securities and Exchange Commission filed charges against multiple crypto platforms "
                   "for alleged securities violations. The announcement triggered a sharp selloff across "
                   "the crypto market, with Bitcoin down 8% and altcoins declining even more sharply.",
        "hours_ago": 3,
        "metadata": {"publisher": "Wall Street Journal", "author": "Regulatory Affairs"},
    },
    
    # CRYPTO - Neutral
    {
        "source": "news",
        "source_id": "news_crypto_neu_1",
        "asset_class": "crypto",
        "title": "Bitcoin trades sideways as market awaits direction",
        "content": "Bitcoin continues to consolidate in a narrow range between $65,000 and $67,000. "
                   "Trading volume has decreased as the market digests recent gains. "
                   "Analysts note that a breakout in either direction could come in the next few days.",
        "hours_ago": 5,
        "metadata": {"publisher": "CoinTelegraph", "author": "Market Analysis"},
    },
    
    # FOREX - Positive
    {
        "source": "news",
        "source_id": "news_forex_pos_1",
        "asset_class": "forex",
        "title": "Dollar strengthens on robust economic data",
        "content": "The U.S. dollar rallied against major currencies following stronger-than-expected "
                   "GDP growth and employment figures. The DXY index climbed to its highest level "
                   "in three months, reflecting renewed confidence in the American economy.",
        "hours_ago": 4,
        "metadata": {"publisher": "Forex.com", "author": "FX Strategist"},
    },
    {
        "source": "reddit",
        "source_id": "reddit_forex_pos_1",
        "asset_class": "forex",
        "title": "EUR/USD technical breakout",
        "content": "Clean breakout above the 1.12 resistance on EUR/USD! The chart is looking very bullish "
                   "with strong momentum and increasing volume. ECB's hawkish stance is supporting the euro. "
                   "Targeting 1.15 in the next few weeks.",
        "hours_ago": 7,
        "metadata": {"subreddit": "forex", "score": 234, "num_comments": 45},
    },
    
    # FOREX - Negative
    {
        "source": "news",
        "source_id": "news_forex_neg_1",
        "asset_class": "forex",
        "title": "Emerging market currencies under pressure",
        "content": "Currencies from emerging markets tumbled as investors fled to safer assets. "
                   "The Turkish lira and Argentine peso hit new record lows amid political instability "
                   "and inflation concerns. Capital outflows are accelerating.",
        "hours_ago": 2,
        "metadata": {"publisher": "Financial Times", "author": "EM Markets"},
    },
    
    # FOREX - Neutral
    {
        "source": "news",
        "source_id": "news_forex_neu_1",
        "asset_class": "forex",
        "title": "GBP/USD remains range-bound ahead of BoE decision",
        "content": "The British pound traded in a tight range against the dollar as traders awaited "
                   "the Bank of England's policy announcement. The pair oscillated between 1.27 and 1.28 "
                   "with no clear directional bias. Market participants are split on the rate decision.",
        "hours_ago": 6,
        "metadata": {"publisher": "DailyFX", "author": "Sterling Desk"},
    },
    
    # COMMODITY - Positive
    {
        "source": "news",
        "source_id": "news_comm_pos_1",
        "asset_class": "commodity",
        "title": "Gold hits new high on safe-haven demand",
        "content": "Gold prices surged to a new all-time high above $2,400 per ounce as geopolitical "
                   "tensions escalated and investors sought safety. Central bank buying remains robust, "
                   "and ETF inflows have accelerated. The precious metal's outlook is increasingly bullish.",
        "hours_ago": 3,
        "metadata": {"publisher": "Kitco News", "author": "Precious Metals"},
    },
    {
        "source": "reddit",
        "source_id": "reddit_comm_pos_1",
        "asset_class": "commodity",
        "title": "Oil supply concerns push prices higher",
        "content": "Crude oil jumped 5% today on reports of production disruptions in key regions. "
                   "OPEC+ supply cuts are tightening the market, and demand forecasts are being revised upward. "
                   "The fundamentals look very supportive for higher energy prices.",
        "hours_ago": 1,
        "metadata": {"subreddit": "commodities", "score": 567, "num_comments": 92},
    },
    
    # COMMODITY - Negative
    {
        "source": "news",
        "source_id": "news_comm_neg_1",
        "asset_class": "commodity",
        "title": "Copper prices slump on China demand worries",
        "content": "Copper futures fell sharply as weak Chinese manufacturing data raised concerns about "
                   "industrial demand. The bellwether metal declined 4%, its largest single-day drop "
                   "in months. Analysts are cutting price forecasts amid deteriorating economic indicators.",
        "hours_ago": 2,
        "metadata": {"publisher": "Mining.com", "author": "Base Metals Team"},
    },
    
    # COMMODITY - Neutral
    {
        "source": "news",
        "source_id": "news_comm_neu_1",
        "asset_class": "commodity",
        "title": "Agricultural commodities trade mixed",
        "content": "Grain futures showed no clear trend today, with wheat up slightly, corn unchanged, "
                   "and soybeans down marginally. Weather patterns remain favorable for now, "
                   "but traders are monitoring upcoming planting season conditions.",
        "hours_ago": 4,
        "metadata": {"publisher": "AgWeb", "author": "Grain Markets"},
    },
]


async def create_sample_data(session: AsyncSession) -> None:
    """Create sample raw text records."""
    print("🌱 Seeding database with sample financial texts...")
    
    # Check if data already exists
    result = await session.execute(select(RawText).limit(1))
    if result.scalar_one_or_none():
        print("⚠️  Database already contains data. Clearing existing records...")
        await session.execute(select(RawText).delete())
        await session.commit()
    
    records_created = 0
    base_time = datetime.now(timezone.utc)
    
    for sample in SAMPLE_TEXTS:
        # Calculate timestamps
        collected_at = base_time
        content_created_at = base_time - timedelta(hours=sample["hours_ago"])
        
        record = RawText(
            id=uuid4(),
            source=sample["source"],
            source_id=sample["source_id"],
            asset_class=sample["asset_class"],
            title=sample.get("title"),
            content=sample["content"],
            content_created_at=content_created_at,
            collected_at=collected_at,
            metadata_=sample.get("metadata"),
        )
        
        session.add(record)
        records_created += 1
        
        print(f"  ✓ Added {sample['asset_class']:10} | {sample['source']:7} | {sample.get('title', 'No title')[:50]}")
    
    await session.commit()
    print(f"\n✅ Successfully created {records_created} sample records")
    print("\nRecords by asset class:")
    
    # Show summary by asset class
    for asset_class in ["equity", "crypto", "forex", "commodity"]:
        result = await session.execute(
            select(RawText).where(RawText.asset_class == asset_class)
        )
        count = len(result.scalars().all())
        print(f"  {asset_class.capitalize():12}: {count} records")


async def main() -> None:
    """Main execution function."""
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        str(settings.database_url),
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create session factory
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    try:
        async with async_session() as session:
            await create_sample_data(session)
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    print("=" * 70)
    print("SENTIMENT REGIME DETECTOR - Database Seeding Script")
    print("=" * 70)
    print()
    
    asyncio.run(main())
    
    print()
    print("=" * 70)
    print("Next steps:")
    print("  1. Run sentiment analysis: python scripts/analyze_texts.py")
    print("  2. Start API server: uvicorn sentiment_detector.main:app --reload")
    print("  3. View results: http://localhost:8000/api/v1/sentiment/current")
    print("=" * 70)
