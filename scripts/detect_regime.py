#!/usr/bin/env python3
"""
Run market regime detection on current sentiment indices.

Uses the RegimeClassifier to determine current market state based on
aggregated sentiment features across asset classes.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.services.regime_classifier import (
    RegimeClassifier,
    SentimentFeatures,
    RegimeState,
)

load_dotenv()


def get_db_url() -> str:
    """Get database URL from environment."""
    url = os.getenv("DATABASE_URL", "")
    return url.replace("postgresql+asyncpg://", "postgresql://")


async def get_latest_sentiment_features() -> SentimentFeatures:
    """
    Fetch latest aggregated sentiment data from the database.
    
    Returns:
        SentimentFeatures object with current market sentiment
    """
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        # Get latest sentiment by asset class (using aggregated source=NULL)
        rows = await conn.fetch("""
            SELECT DISTINCT ON (asset_class)
                asset_class,
                mean_compound,
                std_compound,
                sentiment_momentum
            FROM sentiment_indices
            WHERE source IS NULL
            ORDER BY asset_class, period_start DESC
        """)
        
        # Map asset classes to features
        sentiments = {}
        momentums = []
        for row in rows:
            asset = row['asset_class']
            sentiments[asset] = row['mean_compound'] or 0.0
            if row['sentiment_momentum']:
                momentums.append(row['sentiment_momentum'])
        
        # Get historical data for momentum/acceleration calculation
        historical = await conn.fetch("""
            SELECT 
                period_start,
                AVG(mean_compound) as mean_sentiment
            FROM sentiment_indices
            WHERE source IS NULL
            GROUP BY period_start
            ORDER BY period_start DESC
            LIMIT 14
        """)
        
        # Calculate 7-day momentum (if we have enough data)
        momentum = 0.0
        acceleration = 0.0
        if len(historical) >= 7:
            recent_avg = sum(h['mean_sentiment'] or 0 for h in historical[:7]) / 7
            older_avg = sum(h['mean_sentiment'] or 0 for h in historical[7:14]) / max(len(historical[7:14]), 1)
            momentum = recent_avg - older_avg
            
            if len(historical) >= 14:
                prev_momentum = (
                    sum(h['mean_sentiment'] or 0 for h in historical[1:8]) / 7 -
                    sum(h['mean_sentiment'] or 0 for h in historical[8:15]) / max(len(historical[8:15]), 1)
                )
                acceleration = momentum - prev_momentum
        
        # Calculate cross-asset metrics
        values = list(sentiments.values())
        cross_mean = sum(values) / len(values) if values else 0.0
        cross_std = (sum((v - cross_mean) ** 2 for v in values) / len(values)) ** 0.5 if len(values) > 1 else 0.0
        
        # Calculate max divergence
        max_divergence = max(values) - min(values) if values else 0.0
        
        return SentimentFeatures(
            equity_sentiment=sentiments.get('equity', 0.0),
            crypto_sentiment=sentiments.get('crypto', 0.0),
            forex_sentiment=sentiments.get('forex', 0.0),
            commodity_sentiment=sentiments.get('commodity', 0.0),
            cross_asset_mean=cross_mean,
            cross_asset_std=cross_std,
            sentiment_momentum=momentum,
            sentiment_acceleration=acceleration,
            max_divergence=max_divergence,
            vix_level=None,  # Could integrate VIX data later
        )
        
    finally:
        await conn.close()


async def get_historical_regimes(days: int = 30) -> list[dict]:
    """Get historical regime classifications for analysis."""
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        # Calculate regime for each day in history
        rows = await conn.fetch("""
            SELECT 
                period_start::date as date,
                AVG(mean_compound) FILTER (WHERE asset_class = 'equity') as equity,
                AVG(mean_compound) FILTER (WHERE asset_class = 'crypto') as crypto,
                AVG(mean_compound) FILTER (WHERE asset_class = 'forex') as forex,
                AVG(mean_compound) FILTER (WHERE asset_class = 'commodity') as commodity,
                AVG(mean_compound) as overall
            FROM sentiment_indices
            WHERE source IS NULL
            AND period_start >= NOW() - $1 * INTERVAL '1 day'
            GROUP BY period_start::date
            ORDER BY period_start::date
        """, days)
        
        classifier = RegimeClassifier()
        regimes = []
        
        for row in rows:
            # Build features for this day
            values = [
                row['equity'] or 0,
                row['crypto'] or 0,
                row['forex'] or 0,
                row['commodity'] or 0,
            ]
            cross_mean = sum(values) / len(values)
            cross_std = (sum((v - cross_mean) ** 2 for v in values) / len(values)) ** 0.5
            
            features = SentimentFeatures(
                equity_sentiment=row['equity'] or 0,
                crypto_sentiment=row['crypto'] or 0,
                forex_sentiment=row['forex'] or 0,
                commodity_sentiment=row['commodity'] or 0,
                cross_asset_mean=cross_mean,
                cross_asset_std=cross_std,
                sentiment_momentum=0,  # Simplified for historical
                sentiment_acceleration=0,
                max_divergence=max(values) - min(values),
            )
            
            classification = classifier.classify(features)
            regimes.append({
                'date': row['date'],
                'overall_sentiment': row['overall'] or 0,
                'regime': classification.state.value,
                'confidence': classification.confidence,
                'prob_risk_on': classification.prob_risk_on,
                'prob_risk_off': classification.prob_risk_off,
            })
        
        return regimes
        
    finally:
        await conn.close()


def print_regime_report(features: SentimentFeatures, classification):
    """Print a formatted regime detection report."""
    
    # Regime color/icon
    regime_display = {
        RegimeState.RISK_ON: ("🟢", "RISK-ON", "Bullish sentiment across assets"),
        RegimeState.RISK_OFF: ("🔴", "RISK-OFF", "Defensive positioning recommended"),
        RegimeState.TRANSITION: ("🟡", "TRANSITION", "Market regime uncertain"),
    }
    
    icon, label, description = regime_display[classification.state]
    
    print("\n" + "=" * 70)
    print("🎯 MARKET REGIME DETECTION REPORT")
    print("=" * 70)
    print(f"\nTimestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Model: {classification.model_version}")
    
    print("\n" + "-" * 70)
    print("📊 CURRENT SENTIMENT BY ASSET CLASS")
    print("-" * 70)
    
    def sentiment_bar(value, width=20):
        """Create a visual bar for sentiment."""
        normalized = (value + 1) / 2  # -1 to 1 → 0 to 1
        filled = int(normalized * width)
        bar = "█" * filled + "░" * (width - filled)
        return bar
    
    print(f"\n  Equity:    {features.equity_sentiment:+.4f}  {sentiment_bar(features.equity_sentiment)}")
    print(f"  Crypto:    {features.crypto_sentiment:+.4f}  {sentiment_bar(features.crypto_sentiment)}")
    print(f"  Forex:     {features.forex_sentiment:+.4f}  {sentiment_bar(features.forex_sentiment)}")
    print(f"  Commodity: {features.commodity_sentiment:+.4f}  {sentiment_bar(features.commodity_sentiment)}")
    
    print("\n" + "-" * 70)
    print("📈 AGGREGATE METRICS")
    print("-" * 70)
    
    print(f"\n  Cross-Asset Mean:    {features.cross_asset_mean:+.4f}")
    print(f"  Cross-Asset StdDev:   {features.cross_asset_std:.4f}")
    print(f"  Max Divergence:       {features.max_divergence:.4f}")
    print(f"  7-Day Momentum:      {features.sentiment_momentum:+.4f}")
    print(f"  Acceleration:        {features.sentiment_acceleration:+.4f}")
    
    print("\n" + "-" * 70)
    print("🎯 REGIME CLASSIFICATION")
    print("-" * 70)
    
    print(f"\n  {icon}  Current Regime: {label}")
    print(f"      {description}")
    print(f"\n  Confidence: {classification.confidence:.1%}")
    
    print("\n  Probability Distribution:")
    print(f"      Risk-On:     {classification.prob_risk_on:6.1%}  {'█' * int(classification.prob_risk_on * 30)}")
    print(f"      Risk-Off:    {classification.prob_risk_off:6.1%}  {'█' * int(classification.prob_risk_off * 30)}")
    print(f"      Transition:  {classification.prob_transition:6.1%}  {'█' * int(classification.prob_transition * 30)}")
    
    print("\n" + "=" * 70)


async def print_historical_summary(days: int = 30):
    """Print historical regime summary."""
    regimes = await get_historical_regimes(days)
    
    if not regimes:
        print("\n⚠️  No historical data available")
        return
    
    print(f"\n📅 HISTORICAL REGIME ANALYSIS (Last {days} days)")
    print("-" * 70)
    
    # Count regimes
    counts = {'risk_on': 0, 'risk_off': 0, 'transition': 0}
    for r in regimes:
        counts[r['regime']] += 1
    
    total = len(regimes)
    print(f"\n  Risk-On days:     {counts['risk_on']:3d} ({counts['risk_on']/total:.1%})")
    print(f"  Risk-Off days:    {counts['risk_off']:3d} ({counts['risk_off']/total:.1%})")
    print(f"  Transition days:  {counts['transition']:3d} ({counts['transition']/total:.1%})")
    
    # Show recent history
    print(f"\n  Recent Regimes:")
    regime_icons = {'risk_on': '🟢', 'risk_off': '🔴', 'transition': '🟡'}
    
    for r in regimes[-10:]:
        icon = regime_icons[r['regime']]
        print(f"      {r['date']}: {icon} {r['regime']:10s} (conf: {r['confidence']:.0%}, sentiment: {r['overall_sentiment']:+.3f})")


async def main():
    """Main entry point for regime detection."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run market regime detection")
    parser.add_argument("--history", type=int, default=30, help="Days of history to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Get current features
    print("\n🔄 Fetching latest sentiment data...")
    features = await get_latest_sentiment_features()
    
    # Run classification
    classifier = RegimeClassifier()
    classification = classifier.classify(features)
    
    if args.json:
        import json
        output = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "regime": classification.state.value,
            "confidence": classification.confidence,
            "probabilities": {
                "risk_on": classification.prob_risk_on,
                "risk_off": classification.prob_risk_off,
                "transition": classification.prob_transition,
            },
            "features": features.to_dict(),
            "model_version": classification.model_version,
        }
        print(json.dumps(output, indent=2))
    else:
        # Print formatted report
        print_regime_report(features, classification)
        
        # Print historical summary
        await print_historical_summary(args.history)
    
    print("\n✅ Regime detection complete!\n")


if __name__ == "__main__":
    asyncio.run(main())
