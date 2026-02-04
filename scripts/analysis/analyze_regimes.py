#!/usr/bin/env python3
"""
Comprehensive regime analysis across all historical data.
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

import asyncpg
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.services.regime_classifier import (
    RegimeClassifier,
    SentimentFeatures,
    RegimeState,
)

load_dotenv()


def get_db_url() -> str:
    url = os.getenv("DATABASE_URL", "")
    return url.replace("postgresql+asyncpg://", "postgresql://")


async def run_historical_analysis():
    """Run regime detection on all historical data."""
    
    db_url = get_db_url()
    conn = await asyncpg.connect(db_url)
    
    try:
        # Get all daily indices grouped by date
        rows = await conn.fetch("""
            SELECT 
                period_start::date as date,
                AVG(mean_compound) FILTER (WHERE asset_class = 'equity') as equity,
                AVG(mean_compound) FILTER (WHERE asset_class = 'crypto') as crypto,
                AVG(mean_compound) FILTER (WHERE asset_class = 'forex') as forex,
                AVG(mean_compound) FILTER (WHERE asset_class = 'commodity') as commodity,
                AVG(mean_compound) as overall,
                SUM(sample_count) as total_samples
            FROM sentiment_indices
            WHERE source IS NULL
            GROUP BY period_start::date
            ORDER BY period_start::date
        """)
        
        print(f"\n📊 Analyzing {len(rows)} days of sentiment data...")
        
        classifier = RegimeClassifier()
        regimes = []
        prev_sentiment = None
        
        for i, row in enumerate(rows):
            # Get available sentiment values
            equity = row['equity'] or 0
            crypto = row['crypto'] or 0
            forex = row['forex'] or 0
            commodity = row['commodity'] or 0
            
            # Calculate cross-asset metrics
            values = [v for v in [equity, crypto, forex, commodity] if v != 0]
            if not values:
                continue
                
            cross_mean = sum(values) / len(values)
            cross_std = (sum((v - cross_mean) ** 2 for v in values) / len(values)) ** 0.5
            max_div = max(values) - min(values)
            
            # Calculate momentum from previous period
            momentum = 0.0
            if prev_sentiment is not None:
                momentum = cross_mean - prev_sentiment
            prev_sentiment = cross_mean
            
            # Build features
            features = SentimentFeatures(
                equity_sentiment=equity,
                crypto_sentiment=crypto,
                forex_sentiment=forex,
                commodity_sentiment=commodity,
                cross_asset_mean=cross_mean,
                cross_asset_std=cross_std,
                sentiment_momentum=momentum,
                sentiment_acceleration=0,
                max_divergence=max_div,
            )
            
            # Classify
            classification = classifier.classify(features)
            
            regimes.append({
                'date': row['date'],
                'overall': row['overall'] or 0,
                'samples': row['total_samples'],
                'regime': classification.state.value,
                'confidence': classification.confidence,
                'momentum': momentum,
            })
        
        # Analyze regimes by year
        print("\n" + "=" * 70)
        print("📈 REGIME DISTRIBUTION BY YEAR")
        print("=" * 70)
        
        yearly_stats = {}
        for r in regimes:
            year = r['date'].year
            if year not in yearly_stats:
                yearly_stats[year] = {'risk_on': 0, 'risk_off': 0, 'transition': 0, 'avg_sentiment': [], 'samples': 0}
            yearly_stats[year][r['regime']] += 1
            yearly_stats[year]['avg_sentiment'].append(r['overall'])
            yearly_stats[year]['samples'] += r['samples']
        
        print(f"\n{'Year':<6} {'Days':<6} {'Risk-On':<10} {'Risk-Off':<10} {'Transition':<12} {'Avg Sent':<10} {'Samples':<10}")
        print("-" * 70)
        
        for year in sorted(yearly_stats.keys()):
            stats = yearly_stats[year]
            total = stats['risk_on'] + stats['risk_off'] + stats['transition']
            avg_sent = sum(stats['avg_sentiment']) / len(stats['avg_sentiment'])
            
            print(f"{year:<6} {total:<6} "
                  f"{stats['risk_on']:<4}({stats['risk_on']/total*100:4.0f}%) "
                  f"{stats['risk_off']:<4}({stats['risk_off']/total*100:4.0f}%) "
                  f"{stats['transition']:<4}({stats['transition']/total*100:4.0f}%) "
                  f"{avg_sent:+.4f}    {stats['samples']:,}")
        
        # Overall stats
        total_counts = Counter(r['regime'] for r in regimes)
        total_days = len(regimes)
        
        print("\n" + "=" * 70)
        print("📊 OVERALL REGIME SUMMARY")
        print("=" * 70)
        
        print(f"\n  Total days analyzed: {total_days}")
        print(f"\n  🟢 Risk-On:     {total_counts['risk_on']:4d} days ({total_counts['risk_on']/total_days*100:.1f}%)")
        print(f"  🔴 Risk-Off:    {total_counts['risk_off']:4d} days ({total_counts['risk_off']/total_days*100:.1f}%)")
        print(f"  🟡 Transition:  {total_counts['transition']:4d} days ({total_counts['transition']/total_days*100:.1f}%)")
        
        # Find regime transitions
        print("\n" + "=" * 70)
        print("🔄 MAJOR REGIME TRANSITIONS")
        print("=" * 70)
        
        transitions = []
        for i in range(1, len(regimes)):
            if regimes[i]['regime'] != regimes[i-1]['regime']:
                transitions.append({
                    'date': regimes[i]['date'],
                    'from': regimes[i-1]['regime'],
                    'to': regimes[i]['regime'],
                    'confidence': regimes[i]['confidence'],
                    'sentiment': regimes[i]['overall'],
                })
        
        print(f"\n  Found {len(transitions)} regime transitions\n")
        
        # Show last 15 transitions
        regime_icons = {'risk_on': '🟢', 'risk_off': '🔴', 'transition': '🟡'}
        for t in transitions[-15:]:
            from_icon = regime_icons[t['from']]
            to_icon = regime_icons[t['to']]
            print(f"  {t['date']}: {from_icon} {t['from']:10s} → {to_icon} {t['to']:10s} "
                  f"(conf: {t['confidence']:.0%}, sentiment: {t['sentiment']:+.3f})")
        
        # Extreme sentiment periods
        print("\n" + "=" * 70)
        print("⚡ EXTREME SENTIMENT PERIODS")
        print("=" * 70)
        
        sorted_by_sentiment = sorted(regimes, key=lambda x: x['overall'])
        
        print("\n  Most Bearish Days:")
        for r in sorted_by_sentiment[:5]:
            icon = regime_icons[r['regime']]
            print(f"    {r['date']}: {r['overall']:+.4f} {icon} {r['regime']}")
        
        print("\n  Most Bullish Days:")
        for r in sorted_by_sentiment[-5:][::-1]:
            icon = regime_icons[r['regime']]
            print(f"    {r['date']}: {r['overall']:+.4f} {icon} {r['regime']}")
        
        await conn.close()
        return regimes
        
    except Exception as e:
        await conn.close()
        raise e


async def main():
    print("\n🎯 COMPREHENSIVE MARKET REGIME ANALYSIS")
    print("=" * 70)
    
    regimes = await run_historical_analysis()
    
    print("\n" + "=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
