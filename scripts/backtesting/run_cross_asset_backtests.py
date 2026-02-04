#!/usr/bin/env python3
"""
Cross-Asset Backtest: Gold Rise Since COVID & Crypto Winter 2022.

This script runs backtests on:
1. Gold Rise Since COVID (2020-present): Gold went from ~$1,500 to $2,800+
2. Crypto Winter 2022: BTC from ~$69K to ~$16K (Nov 2021 - Late 2022)

Uses:
- ECB CISS for systemic stress context
- VIX for market fear
- GC=F, GLD for gold prices
- BTC-USD, ETH-USD for crypto prices
- GARCH-MIDAS with CISS integration
"""

import asyncio
import sys
import os
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from sqlalchemy import text


async def load_market_data(
    session,
    symbol: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load market data for a symbol."""
    result = await session.execute(text("""
        SELECT date, open, high, low, close, adj_close, volume
        FROM market_data
        WHERE symbol = :symbol
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"symbol": symbol, "start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


async def load_ciss_data(
    session,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load CISS stress index data."""
    result = await session.execute(text("""
        SELECT date, value
        FROM stress_indices
        WHERE source = 'ecb_ciss'
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'ciss'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


def calculate_returns(prices: pd.Series, log: bool = True) -> pd.Series:
    """Calculate returns from price series."""
    if log:
        return np.log(prices / prices.shift(1)).dropna()
    return prices.pct_change().dropna()


def calculate_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    """Calculate rolling volatility."""
    return returns.rolling(window=window).std() * np.sqrt(252)


def detect_regimes(ciss: pd.Series, vix: pd.Series) -> pd.DataFrame:
    """
    Detect market regimes based on CISS and VIX.
    
    Regimes:
    - Calm: CISS < 0.15, VIX < 15
    - Moderate: CISS 0.15-0.35 or VIX 15-25
    - Elevated: CISS 0.35-0.50 or VIX 25-35
    - Crisis: CISS >= 0.50 or VIX >= 35
    """
    # Align data
    data = pd.DataFrame({'ciss': ciss, 'vix': vix})
    data = data.dropna()
    
    regimes = []
    for idx, row in data.iterrows():
        ciss_val = row['ciss']
        vix_val = row['vix']
        
        if ciss_val >= 0.50 or vix_val >= 35:
            regime = 'crisis'
        elif ciss_val >= 0.35 or vix_val >= 25:
            regime = 'elevated'
        elif ciss_val >= 0.15 or vix_val >= 15:
            regime = 'moderate'
        else:
            regime = 'calm'
        
        regimes.append(regime)
    
    data['regime'] = regimes
    return data


async def run_gold_covid_backtest(session) -> Dict:
    """
    Backtest: Gold Rise Since COVID.
    
    Period: January 2020 - January 2026
    Key Events:
    - COVID crash: March 2020 (gold dropped briefly then rallied)
    - Post-COVID rally: 2020-2023
    - New all-time high: 2024-2026 ($2,800+)
    """
    print("\n" + "=" * 70)
    print("BACKTEST: GOLD RISE SINCE COVID (2020-2026)")
    print("=" * 70)
    
    start = date(2020, 1, 1)
    end = date(2026, 1, 31)
    
    # Load data
    gold = await load_market_data(session, "GC=F", start, end)
    gold_etf = await load_market_data(session, "GLD", start, end)
    vix = await load_market_data(session, "^VIX", start, end)
    ciss = await load_ciss_data(session, start, end)
    
    print(f"\n📊 Data Loaded:")
    print(f"   Gold Futures (GC=F): {len(gold)} trading days")
    print(f"   Gold ETF (GLD): {len(gold_etf)} trading days")
    print(f"   VIX: {len(vix)} trading days")
    print(f"   CISS: {len(ciss)} days")
    
    if len(gold) == 0:
        print("   ⚠️ No gold data available")
        return {}
    
    # Calculate returns
    gold_returns = calculate_returns(gold['close'])
    gold_volatility = calculate_volatility(gold_returns)
    
    # Key statistics
    print(f"\n📈 Gold Performance:")
    start_price = gold['close'].iloc[0]
    end_price = gold['close'].iloc[-1]
    total_return = (end_price / start_price - 1) * 100
    max_price = gold['close'].max()
    min_price = gold['close'].min()
    
    print(f"   Start Price: ${start_price:.2f}")
    print(f"   End Price: ${end_price:.2f}")
    print(f"   Max Price: ${max_price:.2f}")
    print(f"   Min Price: ${min_price:.2f}")
    print(f"   Total Return: {total_return:.1f}%")
    print(f"   Annualized Volatility: {gold_volatility.mean() * 100:.1f}%")
    
    # Regime analysis
    if len(vix) > 0 and len(ciss) > 0:
        regimes = detect_regimes(ciss['ciss'], vix['close'])
        regime_counts = regimes['regime'].value_counts()
        
        print(f"\n🎯 Regime Distribution:")
        for regime in ['calm', 'moderate', 'elevated', 'crisis']:
            count = regime_counts.get(regime, 0)
            pct = count / len(regimes) * 100 if len(regimes) > 0 else 0
            print(f"   {regime.capitalize()}: {count} days ({pct:.1f}%)")
        
        # Gold performance by regime
        if 'ciss' in regimes.columns:
            gold_aligned = gold['close'].reindex(regimes.index).dropna()
            gold_returns_aligned = calculate_returns(gold_aligned)
            regimes_aligned = regimes.loc[gold_returns_aligned.index]
            
            print(f"\n💰 Gold Returns by Regime:")
            for regime in ['calm', 'moderate', 'elevated', 'crisis']:
                mask = regimes_aligned['regime'] == regime
                if mask.sum() > 0:
                    regime_returns = gold_returns_aligned[mask]
                    avg_ret = regime_returns.mean() * 252 * 100  # Annualized
                    print(f"   {regime.capitalize()}: {avg_ret:.1f}% annualized")
    
    # Key dates
    print(f"\n📅 Key Observations:")
    covid_crash = gold.loc['2020-03':'2020-03']
    if len(covid_crash) > 0:
        crash_low = covid_crash['low'].min()
        print(f"   COVID Crash Low (March 2020): ${crash_low:.2f}")
    
    # 2024-2025 rally
    recent = gold.loc['2024-01':]
    if len(recent) > 0:
        recent_high = recent['high'].max()
        recent_high_date = recent['high'].idxmax()
        print(f"   Recent High: ${recent_high:.2f} on {recent_high_date.date()}")
    
    return {
        "period": f"{start} to {end}",
        "total_return": total_return,
        "start_price": start_price,
        "end_price": end_price,
        "max_price": max_price,
    }


async def run_crypto_winter_backtest(session) -> Dict:
    """
    Backtest: Crypto Winter 2022.
    
    Period: November 2021 - December 2022
    Key Events:
    - BTC All-time high: ~$69K (Nov 2021)
    - Steady decline through 2022
    - Terra/Luna collapse: May 2022
    - FTX collapse: November 2022
    - BTC Bottom: ~$16K (November 2022)
    """
    print("\n" + "=" * 70)
    print("BACKTEST: CRYPTO WINTER 2022")
    print("=" * 70)
    
    start = date(2021, 11, 1)
    end = date(2022, 12, 31)
    
    # Load data
    btc = await load_market_data(session, "BTC-USD", start, end)
    eth = await load_market_data(session, "ETH-USD", start, end)
    vix = await load_market_data(session, "^VIX", start, end)
    ciss = await load_ciss_data(session, start, end)
    
    print(f"\n📊 Data Loaded:")
    print(f"   Bitcoin (BTC-USD): {len(btc)} trading days")
    print(f"   Ethereum (ETH-USD): {len(eth)} trading days")
    print(f"   VIX: {len(vix)} trading days")
    print(f"   CISS: {len(ciss)} days")
    
    if len(btc) == 0:
        print("   ⚠️ No BTC data available")
        return {}
    
    # BTC Analysis
    print(f"\n₿ Bitcoin Performance:")
    btc_start = btc['close'].iloc[0]
    btc_end = btc['close'].iloc[-1]
    btc_high = btc['high'].max()
    btc_high_date = btc['high'].idxmax()
    btc_low = btc['low'].min()
    btc_low_date = btc['low'].idxmin()
    btc_drawdown = (btc_low / btc_high - 1) * 100
    
    print(f"   All-Time High: ${btc_high:,.0f} on {btc_high_date.date()}")
    print(f"   Period Low: ${btc_low:,.0f} on {btc_low_date.date()}")
    print(f"   Max Drawdown: {btc_drawdown:.1f}%")
    
    # ETH Analysis
    if len(eth) > 0:
        print(f"\nΞ Ethereum Performance:")
        eth_high = eth['high'].max()
        eth_low = eth['low'].min()
        eth_drawdown = (eth_low / eth_high - 1) * 100
        print(f"   Period High: ${eth_high:,.0f}")
        print(f"   Period Low: ${eth_low:,.0f}")
        print(f"   Max Drawdown: {eth_drawdown:.1f}%")
    
    # Volatility analysis
    btc_returns = calculate_returns(btc['close'])
    btc_volatility = calculate_volatility(btc_returns)
    
    print(f"\n📉 Volatility Analysis:")
    print(f"   Avg Daily Return: {btc_returns.mean() * 100:.3f}%")
    print(f"   Daily Return Std: {btc_returns.std() * 100:.2f}%")
    print(f"   Annualized Vol: {btc_volatility.mean() * 100:.1f}%")
    
    # Key crash events
    print(f"\n🔥 Major Crash Events:")
    
    # Terra/Luna (May 2022)
    luna = btc.loc['2022-05-01':'2022-05-15']
    if len(luna) > 0:
        luna_drop = (luna['close'].min() / luna['close'].max() - 1) * 100
        print(f"   Terra/Luna Crash (May 2022): {luna_drop:.1f}% in 2 weeks")
    
    # FTX (November 2022)
    ftx = btc.loc['2022-11-01':'2022-11-15']
    if len(ftx) > 0:
        ftx_drop = (ftx['close'].min() / ftx['close'].max() - 1) * 100
        print(f"   FTX Collapse (Nov 2022): {ftx_drop:.1f}% in 2 weeks")
    
    # Correlation with traditional markets
    if len(vix) > 0:
        # Align data
        common_idx = btc.index.intersection(vix.index)
        if len(common_idx) > 30:
            btc_aligned = btc.loc[common_idx, 'close']
            vix_aligned = vix.loc[common_idx, 'close']
            
            btc_ret = calculate_returns(btc_aligned)
            vix_ret = calculate_returns(vix_aligned)
            
            common_ret = btc_ret.index.intersection(vix_ret.index)
            if len(common_ret) > 20:
                corr = btc_ret.loc[common_ret].corr(vix_ret.loc[common_ret])
                print(f"\n📊 Correlation Analysis:")
                print(f"   BTC-VIX Correlation: {corr:.3f}")
    
    return {
        "period": f"{start} to {end}",
        "btc_high": btc_high,
        "btc_low": btc_low,
        "btc_drawdown": btc_drawdown,
    }


async def run_2008_financial_crisis_backtest(session) -> Dict:
    """
    Backtest: 2008 Financial Crisis.
    
    Tests CISS as leading/coincident indicator.
    """
    print("\n" + "=" * 70)
    print("BACKTEST: 2008 FINANCIAL CRISIS (CISS VALIDATION)")
    print("=" * 70)
    
    start = date(2007, 6, 1)
    end = date(2010, 6, 30)
    
    # Load CISS
    ciss = await load_ciss_data(session, start, end)
    
    if len(ciss) == 0:
        print("   ⚠️ No CISS data available")
        return {}
    
    print(f"\n📊 CISS Data: {len(ciss)} observations")
    
    # Key crisis dates
    print(f"\n📅 CISS During Key Events:")
    
    # August 2007 - BNP Paribas freezes funds (start of crisis)
    aug_2007 = ciss.loc['2007-08']
    if len(aug_2007) > 0:
        print(f"   Aug 2007 (BNP freeze): CISS avg={aug_2007['ciss'].mean():.3f}, max={aug_2007['ciss'].max():.3f}")
    
    # September 2008 - Lehman Brothers
    sep_2008 = ciss.loc['2008-09']
    if len(sep_2008) > 0:
        print(f"   Sep 2008 (Lehman): CISS avg={sep_2008['ciss'].mean():.3f}, max={sep_2008['ciss'].max():.3f}")
    
    # October-November 2008 - Peak crisis
    peak = ciss.loc['2008-10':'2008-11']
    if len(peak) > 0:
        print(f"   Oct-Nov 2008 (Peak): CISS avg={peak['ciss'].mean():.3f}, max={peak['ciss'].max():.3f}")
    
    # Crisis thresholds
    crisis_days = (ciss['ciss'] >= 0.50).sum()
    high_stress_days = ((ciss['ciss'] >= 0.35) & (ciss['ciss'] < 0.50)).sum()
    
    print(f"\n🔴 Stress Periods:")
    print(f"   Crisis (CISS >= 0.50): {crisis_days} days")
    print(f"   High Stress (0.35-0.50): {high_stress_days} days")
    print(f"   Total High/Crisis: {crisis_days + high_stress_days} days ({(crisis_days + high_stress_days) / len(ciss) * 100:.1f}%)")
    
    # Peak date
    peak_date = ciss['ciss'].idxmax()
    peak_val = ciss['ciss'].max()
    print(f"\n📈 CISS Peak: {peak_val:.4f} on {peak_date.date()}")
    
    return {
        "period": f"{start} to {end}",
        "ciss_peak": peak_val,
        "ciss_peak_date": peak_date,
        "crisis_days": crisis_days,
    }


async def main():
    """Run all backtests."""
    from src.sentiment_detector.core.database import get_session_context
    
    print("\n" + "=" * 70)
    print("CROSS-ASSET BACKTEST SUITE")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = {}
    
    async with get_session_context() as session:
        # Run backtests
        results['gold_covid'] = await run_gold_covid_backtest(session)
        results['crypto_winter'] = await run_crypto_winter_backtest(session)
        results['financial_crisis_2008'] = await run_2008_financial_crisis_backtest(session)
    
    # Summary
    print("\n" + "=" * 70)
    print("BACKTEST SUMMARY")
    print("=" * 70)
    
    if results.get('gold_covid'):
        r = results['gold_covid']
        print(f"\n🥇 Gold Since COVID: {r.get('total_return', 0):.1f}% total return")
    
    if results.get('crypto_winter'):
        r = results['crypto_winter']
        print(f"₿ Crypto Winter 2022: {r.get('btc_drawdown', 0):.1f}% max drawdown")
    
    if results.get('financial_crisis_2008'):
        r = results['financial_crisis_2008']
        print(f"📉 2008 Crisis CISS Peak: {r.get('ciss_peak', 0):.4f}")
    
    print("\n" + "=" * 70)
    print("✅ ALL BACKTESTS COMPLETE")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
