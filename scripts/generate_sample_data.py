#!/usr/bin/env python3
"""
Generate synthetic financial text data for pipeline testing.

Creates realistic-looking Reddit-style posts across all asset classes
with varied sentiment to test the MANEFRAME batch processing pipeline.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import uuid

# Sentiment templates by asset class
TEMPLATES = {
    "equity": {
        "positive": [
            "SPY is looking incredibly strong today. Breaking through resistance levels with massive volume. This bull run has legs! 🚀",
            "NVDA earnings crushed expectations. AI demand is insane. Added more to my position.",
            "Finally, the Fed signaled rate cuts. Market is going to love this. Time to load up on growth stocks.",
            "Tesla deliveries beat estimates by 15%. Bears are in shambles. $TSLA to the moon!",
            "Apple just announced record services revenue. The ecosystem moat is real. Long and strong.",
            "QQQ breaking all-time highs. Tech is back baby! Portfolio up 30% this quarter.",
            "Magnificent 7 carrying the market again. Can't fight the trend, stay long.",
            "Bank earnings came in hot. JPM and GS crushing it. Financial sector rotation incoming.",
            "Retail sales data strong. Consumer is resilient. Buy the dip mentality working.",
            "Options flow is extremely bullish. Big money loading calls on SPY for next month.",
        ],
        "negative": [
            "Market is way overextended. RSI screaming overbought. Taking profits here.",
            "Recession indicators flashing red. Yield curve still inverted. Be careful out there.",
            "AAPL missing estimates. iPhone demand slowing in China. Not good for the market.",
            "Layoffs accelerating across tech. This is just the beginning of the pain.",
            "Commercial real estate is a ticking time bomb. Regional banks exposure is scary.",
            "VIX spiking hard. Something is breaking. Moving to cash.",
            "Insider selling at record levels. Smart money heading for the exits.",
            "Credit spreads widening. High yield bonds selling off. Risk-off mode engaged.",
            "Earnings revisions turning negative. Analysts cutting estimates across the board.",
            "Market breadth terrible. Only handful of stocks holding up the indices. Not sustainable.",
        ],
        "neutral": [
            "Waiting for CPI data tomorrow. Could go either way. Staying flat for now.",
            "Fed meeting next week. Market in wait-and-see mode. Low volume expected.",
            "Mixed signals from the economic data. Hard to make a directional bet here.",
            "Earnings season starting. Will let the numbers guide my positioning.",
            "Technical levels are converging. Big move coming but direction unclear.",
            "Rotation from growth to value continuing. Staying diversified across sectors.",
            "Options expiration Friday. Expect some volatility but nothing directional.",
            "Market consolidating after the recent run. Normal healthy pullback.",
        ],
    },
    "crypto": {
        "positive": [
            "BTC breaking $100k was just the beginning. Institutional adoption accelerating. HODL! 💎🙌",
            "ETH ETF approval imminent. This will be bigger than the BTC ETF launch.",
            "Solana network hitting new TPS records. SOL ecosystem is thriving.",
            "BlackRock adding more Bitcoin to their holdings. Wall Street can't get enough.",
            "Halving effect kicking in. Supply shock is real. $200k BTC this cycle.",
            "DeFi TVL exploding. Yields are back. Crypto summer is here!",
            "Major bank announcing crypto custody services. Mass adoption incoming.",
            "Bitcoin dominance dropping. Altseason is officially here. Load up your bags!",
            "Crypto regulation clarity finally coming. This removes so much uncertainty.",
            "Whale wallets accumulating heavily. On-chain data extremely bullish.",
        ],
        "negative": [
            "Another exchange hack. $500M stolen. This space never learns. Staying in cold storage.",
            "SEC going after another major project. Regulatory crackdown intensifying.",
            "Bitcoin mining difficulty at ATH. Smaller miners getting squeezed out.",
            "Stablecoin redemptions spiking. Liquidity leaving the ecosystem.",
            "Major crypto fund liquidating positions. Contagion risk is real.",
            "Network fees through the roof. ETH unusable for small transactions.",
            "Memecoin mania is a sign of a top. Too much speculation, not enough building.",
            "Binance volume dropping. Trust in centralized exchanges at all-time low.",
            "Whale dumping on retail again. Same pattern every cycle.",
            "Mt Gox distributions starting. Billions in sell pressure coming.",
        ],
        "neutral": [
            "BTC ranging between support and resistance. Waiting for a breakout.",
            "Layer 2 adoption growing but still early. Monitoring the space.",
            "Mixed signals from on-chain metrics. Accumulation and distribution both happening.",
            "Waiting for more regulatory clarity before increasing position.",
            "Crypto funding rates neutral. No extreme positioning either way.",
            "DeFi yields normalizing. The easy money phase is over.",
        ],
    },
    "forex": {
        "positive": [
            "Dollar weakness continuing. EUR/USD breaking key resistance. Long euro here.",
            "BOJ finally raising rates. JPY strengthening as expected. USD/JPY shorts paying off.",
            "GBP rallying on strong UK economic data. Cable looking bullish.",
            "Risk-on environment favoring AUD and NZD. Commodity currencies outperforming.",
            "Carry trade unwinding complete. EM currencies stabilizing and recovering.",
            "Fed pivot confirmed. Dollar index breaking down. Long gold and short DXY.",
        ],
        "negative": [
            "Dollar wrecking ball mode activated. EM currencies getting destroyed.",
            "EUR/USD breaking below parity again. Eurozone economy in shambles.",
            "GBP flash crash. Brexit uncertainty never ends. Avoid sterling.",
            "Yen intervention failing. BOJ losing control. USD/JPY to 200?",
            "Currency wars heating up. Race to the bottom for export competitiveness.",
            "Swiss franc safe haven flows overwhelming. Risk-off across the board.",
        ],
        "neutral": [
            "Major pairs ranging. Waiting for central bank guidance.",
            "FX volatility at multi-year lows. Hard to find good setups.",
            "Mixed economic data keeping currencies in check. No strong trends.",
            "Central bank policy convergence reducing currency divergence.",
            "G7 meeting this week. Potential for coordinated currency statements.",
        ],
    },
    "commodity": {
        "positive": [
            "Gold breaking $3000. Central banks buying record amounts. The run is just starting.",
            "Oil rallying on OPEC+ cuts. Supply discipline finally working. Long crude.",
            "Silver outperforming gold. Industrial demand from solar panels exploding.",
            "Copper hitting new highs. Green energy transition driving demand. Super cycle is real.",
            "Natural gas bottoming. Winter demand picking up. Great risk/reward here.",
            "Agricultural commodities rallying. Weather disruptions and supply concerns. Long grains.",
            "Uranium breaking out. Nuclear renaissance underway. CCJ and URA looking great.",
            "Lithium demand outpacing supply. EV adoption accelerating. Battery metals hot.",
        ],
        "negative": [
            "Oil crashing on demand destruction fears. Global recession concerns mounting.",
            "Gold giving up gains. Real yields rising. Opportunity cost too high.",
            "Copper selling off on China slowdown fears. Property crisis weighing on metals.",
            "Natural gas oversupplied. Warm winter crushing prices. Storage at capacity.",
            "Agricultural commodities dumping. Bumper harvests expected. Supply glut incoming.",
            "Precious metals failing to hold support. Dollar strength too much to overcome.",
            "Commodity super cycle thesis dying. Demand destruction across the board.",
        ],
        "neutral": [
            "Oil in a range. OPEC meeting outcome uncertain. Staying on sidelines.",
            "Gold consolidating around key levels. Waiting for inflation data.",
            "Base metals mixed. China stimulus hopes vs economic reality.",
            "Agricultural commodities dependent on weather. Too binary to trade.",
            "Commodity ETF flows neutral. No strong conviction either direction.",
        ],
    },
}

# Subreddit simulation
SUBREDDITS = {
    "equity": ["wallstreetbets", "stocks", "investing", "options", "stockmarket"],
    "crypto": ["cryptocurrency", "bitcoin", "ethereum", "cryptomarkets"],
    "forex": ["forex", "forextrading"],
    "commodity": ["commodities", "gold", "silverbugs"],
}


def generate_post(asset_class: str, sentiment: str, base_time: datetime) -> dict:
    """Generate a single synthetic post."""
    templates = TEMPLATES[asset_class][sentiment]
    content = random.choice(templates)
    subreddit = random.choice(SUBREDDITS[asset_class])
    
    # Random time offset within 24 hours
    time_offset = timedelta(
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    created_at = base_time - time_offset
    
    # Simulate engagement metrics
    score = random.randint(1, 5000) if random.random() > 0.7 else random.randint(1, 100)
    num_comments = int(score * random.uniform(0.1, 0.5))
    
    return {
        "id": str(uuid.uuid4())[:8],
        "source": "reddit",
        "asset_class": asset_class,
        "created_at": created_at.isoformat(),
        "title": content[:100] + "..." if len(content) > 100 else content,
        "content": content,
        "metadata": {
            "subreddit": subreddit,
            "score": score,
            "num_comments": num_comments,
            "upvote_ratio": round(random.uniform(0.5, 0.99), 2),
            "synthetic": True,  # Flag for identification
        },
    }


def generate_dataset(
    num_posts: int = 1000,
    days_back: int = 7,
    output_path: str = "data/raw/sample_batch.json",
):
    """Generate a full synthetic dataset."""
    
    print(f"\n🔧 Generating {num_posts} synthetic financial posts...")
    print(f"   Date range: Last {days_back} days")
    
    items = []
    stats = {asset: {"positive": 0, "negative": 0, "neutral": 0} for asset in TEMPLATES.keys()}
    
    # Distribution: 25% each asset class
    posts_per_asset = num_posts // 4
    
    # Sentiment distribution: 35% positive, 35% negative, 30% neutral
    sentiment_weights = ["positive"] * 35 + ["negative"] * 35 + ["neutral"] * 30
    
    end_date = datetime.utcnow()
    
    for asset_class in TEMPLATES.keys():
        for _ in range(posts_per_asset):
            # Pick random day
            days_offset = random.randint(0, days_back - 1)
            base_time = end_date - timedelta(days=days_offset)
            
            # Pick sentiment
            sentiment = random.choice(sentiment_weights)
            
            # Generate post
            post = generate_post(asset_class, sentiment, base_time)
            items.append(post)
            stats[asset_class][sentiment] += 1
    
    # Shuffle to mix asset classes
    random.shuffle(items)
    
    # Build output
    output_data = {
        "collection_timestamp": datetime.utcnow().isoformat(),
        "date_range": {
            "start": (end_date - timedelta(days=days_back)).isoformat(),
            "end": end_date.isoformat(),
        },
        "stats": {
            "equity": sum(stats["equity"].values()),
            "crypto": sum(stats["crypto"].values()),
            "forex": sum(stats["forex"].values()),
            "commodity": sum(stats["commodity"].values()),
        },
        "sentiment_distribution": stats,
        "total_items": len(items),
        "synthetic": True,
        "items": items,
    }
    
    # Save to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    
    file_size_kb = output_file.stat().st_size / 1024
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Dataset Generated")
    print("=" * 60)
    print(f"\n📈 Posts by Asset Class:")
    for asset, count in output_data["stats"].items():
        print(f"   {asset.capitalize():12} {count:,} posts")
    print(f"   {'─' * 25}")
    print(f"   {'Total':12} {len(items):,} posts")
    
    print(f"\n😊 Sentiment Distribution:")
    for asset, sentiments in stats.items():
        print(f"   {asset.capitalize():12} +{sentiments['positive']} / -{sentiments['negative']} / ○{sentiments['neutral']}")
    
    print(f"\n💾 Output: {output_file}")
    print(f"   Size: {file_size_kb:.1f} KB")
    
    print("\n" + "=" * 60)
    print("📤 Upload to MANEFRAME")
    print("=" * 60)
    print(f"\nscp {output_file} jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/data/raw/")
    print("\nThen on MANEFRAME:")
    print("  ssh jarocha@m3.smu.edu")
    print("  cd /lustre/scratch/client/users/jarocha/sentiment-detector")
    print("  source activate_env.sh")
    print("  sbatch run_sentiment_batch.sh")
    print("=" * 60)
    
    return output_file


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate synthetic financial text data")
    parser.add_argument("--posts", type=int, default=1000, help="Number of posts to generate")
    parser.add_argument("--days", type=int, default=7, help="Days of data to simulate")
    parser.add_argument("--output", type=str, default="data/raw/sample_batch.json", help="Output file path")
    
    args = parser.parse_args()
    
    generate_dataset(
        num_posts=args.posts,
        days_back=args.days,
        output_path=args.output,
    )
