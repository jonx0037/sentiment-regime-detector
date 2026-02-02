#!/usr/bin/env python3
"""
Full GARCH-MIDAS Backtest with CISS Integration.

Runs historical backtests for:
1. 2008 Financial Crisis
2. COVID-19 March 2020
3. GameStop January 2021

Tests the complete pipeline:
- Load market returns
- Load sentiment data
- Load CISS stress data
- Fit GARCH-MIDAS model
- Compare regimes to VIX ground truth
"""

import asyncio
import sys
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))
os.chdir(project_root)

from sqlalchemy import text


async def load_market_returns(
    session,
    symbol: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load market data and calculate returns."""
    result = await session.execute(text("""
        SELECT date, close, adj_close
        FROM market_data
        WHERE symbol = :symbol
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"symbol": symbol, "start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'close', 'adj_close'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    # Calculate log returns
    df['returns'] = np.log(df['adj_close'] / df['adj_close'].shift(1))
    df = df.dropna()
    
    return df


async def load_ciss(
    session,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load CISS stress index."""
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


async def load_vix(
    session,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load VIX as ground truth."""
    result = await session.execute(text("""
        SELECT date, close as vix
        FROM market_data
        WHERE symbol = '^VIX'
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'vix'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


async def load_aggregated_sentiment(
    session,
    start_date: date,
    end_date: date,
    asset_class: str = 'equity',
) -> pd.DataFrame:
    """Load daily aggregated sentiment scores."""
    result = await session.execute(text("""
        SELECT 
            DATE(rt.content_created_at) as date,
            AVG(ss.compound) as sentiment,
            COUNT(*) as count
        FROM sentiment_scores ss
        JOIN raw_texts rt ON ss.text_id = rt.id
        WHERE rt.content_created_at BETWEEN :start AND :end
        AND rt.asset_class = :asset_class
        GROUP BY DATE(rt.content_created_at)
        ORDER BY date
    """), {"start": start_date, "end": end_date, "asset_class": asset_class})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'sentiment', 'count'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


def assign_vix_regime(vix: float) -> str:
    """Assign regime based on VIX level."""
    if vix < 15:
        return 'calm'
    elif vix < 25:
        return 'moderate'
    elif vix < 35:
        return 'elevated'
    else:
        return 'crisis'


def assign_ciss_regime(ciss: float) -> str:
    """Assign regime based on CISS level."""
    if ciss < 0.15:
        return 'calm'
    elif ciss < 0.35:
        return 'moderate'
    elif ciss < 0.50:
        return 'elevated'
    else:
        return 'crisis'


def calculate_realized_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    """Calculate rolling realized volatility (annualized)."""
    return returns.rolling(window=window).std() * np.sqrt(252)


def fit_simple_garch_midas(
    returns: pd.Series,
    sentiment: pd.Series,
    ciss: Optional[pd.Series] = None,
) -> Dict:
    """
    Simplified GARCH-MIDAS estimation without arch library.
    
    Uses OLS-based approximation for demonstration.
    For production, use arch library on HPC.
    """
    # Align data
    common_idx = returns.index.intersection(sentiment.index)
    if ciss is not None:
        common_idx = common_idx.intersection(ciss.index)
    
    if len(common_idx) < 50:
        return {"error": "Insufficient overlapping data"}
    
    returns_aligned = returns.loc[common_idx]
    sentiment_aligned = sentiment.loc[common_idx]
    
    # Calculate weekly sentiment aggregation (MIDAS)
    weekly_sentiment = sentiment_aligned.resample('W').mean().ffill()
    sentiment_weekly_aligned = weekly_sentiment.reindex(common_idx, method='ffill')
    
    # Calculate realized variance
    realized_var = returns_aligned ** 2
    
    # Simple regression: RV ~ sentiment
    from scipy import stats
    
    # Prepare data
    X = sentiment_weekly_aligned.values
    y = realized_var.values
    
    # Remove NaNs
    mask = ~(np.isnan(X) | np.isnan(y))
    X_clean = X[mask]
    y_clean = y[mask]
    
    if len(X_clean) < 30:
        return {"error": "Insufficient clean data"}
    
    # OLS regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_clean, y_clean)
    
    result = {
        "n_observations": len(X_clean),
        "sentiment_coefficient": slope,
        "intercept": intercept,
        "r_squared": r_value ** 2,
        "p_value": p_value,
        "mean_volatility": np.sqrt(y_clean.mean()) * np.sqrt(252),
    }
    
    # Add CISS effect if provided
    if ciss is not None:
        ciss_aligned = ciss.loc[common_idx]
        ciss_clean = ciss_aligned.values[mask]
        
        # Multiple regression with both sentiment and CISS
        from scipy.linalg import lstsq
        
        X_multi = np.column_stack([np.ones(len(X_clean)), X_clean, ciss_clean])
        coeffs, residuals, rank, s = lstsq(X_multi, y_clean)
        
        result["ciss_coefficient"] = coeffs[2]
        result["sentiment_coefficient_with_ciss"] = coeffs[1]
        
        # Calculate R-squared for multiple regression
        y_pred = X_multi @ coeffs
        ss_res = np.sum((y_clean - y_pred) ** 2)
        ss_tot = np.sum((y_clean - np.mean(y_clean)) ** 2)
        result["r_squared_with_ciss"] = 1 - (ss_res / ss_tot)
    
    return result


async def run_backtest_2008(session) -> Dict:
    """2008 Financial Crisis backtest."""
    print("\n" + "=" * 70)
    print("BACKTEST: 2008 FINANCIAL CRISIS")
    print("=" * 70)
    
    start = date(2007, 6, 1)
    end = date(2010, 6, 30)
    
    # Load data
    ciss = await load_ciss(session, start, end)
    sentiment = await load_aggregated_sentiment(session, start, end, 'equity')
    
    print(f"\n📊 Data Loaded:")
    print(f"   CISS: {len(ciss)} observations")
    print(f"   Sentiment: {len(sentiment)} days with {sentiment['count'].sum():,} texts")
    
    if len(ciss) == 0:
        print("   ⚠️ No CISS data")
        return {}
    
    # CISS regime analysis
    ciss['regime'] = ciss['ciss'].apply(assign_ciss_regime)
    regime_counts = ciss['regime'].value_counts()
    
    print(f"\n🎯 CISS Regime Distribution:")
    for regime in ['calm', 'moderate', 'elevated', 'crisis']:
        count = regime_counts.get(regime, 0)
        pct = count / len(ciss) * 100
        print(f"   {regime.capitalize()}: {count} days ({pct:.1f}%)")
    
    # Key crisis dates
    print(f"\n📅 Key CISS Readings:")
    
    # Lehman (Sep 15, 2008)
    lehman = ciss.loc['2008-09-12':'2008-09-19']
    if len(lehman) > 0:
        print(f"   Lehman Week: avg={lehman['ciss'].mean():.3f}, max={lehman['ciss'].max():.3f}")
    
    # Peak crisis
    peak_date = ciss['ciss'].idxmax()
    peak_val = ciss['ciss'].max()
    print(f"   Peak: {peak_val:.4f} on {peak_date.date()}")
    
    # Sentiment during crisis
    if len(sentiment) > 0:
        crisis_sentiment = sentiment.loc['2008-09':'2008-11']
        if len(crisis_sentiment) > 0:
            print(f"\n📝 Sentiment During Crisis (Sep-Nov 2008):")
            print(f"   Mean sentiment: {crisis_sentiment['sentiment'].mean():.4f}")
            print(f"   Daily texts: {crisis_sentiment['count'].mean():.0f}")
    
    # Fit simplified GARCH-MIDAS
    if len(sentiment) > 50:
        print(f"\n📈 GARCH-MIDAS Estimation:")
        garch_result = fit_simple_garch_midas(
            ciss['ciss'],  # Using CISS as proxy for volatility
            sentiment['sentiment'],
        )
        
        if 'error' not in garch_result:
            print(f"   Observations: {garch_result['n_observations']}")
            print(f"   Sentiment β: {garch_result['sentiment_coefficient']:.6f}")
            print(f"   R²: {garch_result['r_squared']:.4f}")
            print(f"   p-value: {garch_result['p_value']:.4f}")
    
    return {
        "period": f"{start} to {end}",
        "ciss_peak": peak_val,
        "crisis_days": regime_counts.get('crisis', 0),
    }


async def run_backtest_covid(session) -> Dict:
    """COVID-19 March 2020 backtest."""
    print("\n" + "=" * 70)
    print("BACKTEST: COVID-19 MARCH 2020")
    print("=" * 70)
    
    start = date(2019, 10, 1)
    end = date(2020, 6, 30)
    
    # Load data
    vix = await load_vix(session, start, end)
    ciss = await load_ciss(session, start, end)
    sentiment = await load_aggregated_sentiment(session, start, end, 'equity')
    
    print(f"\n📊 Data Loaded:")
    print(f"   VIX: {len(vix)} observations")
    print(f"   CISS: {len(ciss)} observations")
    print(f"   Sentiment: {len(sentiment)} days with {sentiment['count'].sum():,} texts")
    
    if len(vix) == 0:
        print("   ⚠️ No VIX data")
        return {}
    
    # VIX regime analysis
    vix['regime'] = vix['vix'].apply(assign_vix_regime)
    
    # March 2020 spike
    march_2020 = vix.loc['2020-03']
    if len(march_2020) > 0:
        print(f"\n🔴 March 2020 VIX Spike:")
        print(f"   Max VIX: {march_2020['vix'].max():.2f}")
        print(f"   Mean VIX: {march_2020['vix'].mean():.2f}")
        max_date = march_2020['vix'].idxmax()
        print(f"   Peak Date: {max_date.date()}")
        
        crisis_days = (march_2020['regime'] == 'crisis').sum()
        print(f"   Crisis Days: {crisis_days}/{len(march_2020)}")
    
    # Compare VIX and CISS
    if len(ciss) > 0:
        march_ciss = ciss.loc['2020-03']
        if len(march_ciss) > 0:
            print(f"\n📊 CISS vs VIX Comparison (March 2020):")
            print(f"   CISS Max: {march_ciss['ciss'].max():.3f}")
            print(f"   VIX Max: {march_2020['vix'].max():.2f}")
            
            # Correlation
            common = vix.index.intersection(ciss.index)
            if len(common) > 20:
                corr = vix.loc[common, 'vix'].corr(ciss.loc[common, 'ciss'])
                print(f"   VIX-CISS Correlation: {corr:.3f}")
    
    # Sentiment during crisis
    if len(sentiment) > 0:
        march_sent = sentiment.loc['2020-03']
        if len(march_sent) > 0:
            print(f"\n📝 Sentiment (March 2020):")
            print(f"   Mean: {march_sent['sentiment'].mean():.4f}")
            print(f"   Min: {march_sent['sentiment'].min():.4f}")
            print(f"   Daily texts: {march_sent['count'].mean():.0f}")
    
    # Fit GARCH-MIDAS with CISS
    if len(sentiment) > 50 and len(ciss) > 50:
        print(f"\n📈 GARCH-MIDAS with CISS:")
        
        # Use VIX as volatility proxy, sentiment and CISS as regressors
        garch_result = fit_simple_garch_midas(
            vix['vix'] / 100,  # Normalize VIX
            sentiment['sentiment'],
            ciss['ciss'],
        )
        
        if 'error' not in garch_result:
            print(f"   Observations: {garch_result['n_observations']}")
            print(f"   Sentiment β: {garch_result['sentiment_coefficient_with_ciss']:.4f}")
            print(f"   CISS β: {garch_result['ciss_coefficient']:.4f}")
            print(f"   R² (with CISS): {garch_result['r_squared_with_ciss']:.4f}")
    
    return {
        "period": f"{start} to {end}",
        "vix_peak": march_2020['vix'].max() if len(march_2020) > 0 else None,
    }


async def run_backtest_gamestop(session) -> Dict:
    """GameStop January 2021 backtest."""
    print("\n" + "=" * 70)
    print("BACKTEST: GAMESTOP JANUARY 2021")
    print("=" * 70)
    
    start = date(2020, 12, 1)
    end = date(2021, 3, 31)
    
    # Load data
    vix = await load_vix(session, start, end)
    ciss = await load_ciss(session, start, end)
    sentiment = await load_aggregated_sentiment(session, start, end, 'equity')
    
    print(f"\n📊 Data Loaded:")
    print(f"   VIX: {len(vix)} observations")
    print(f"   CISS: {len(ciss)} observations")
    print(f"   Sentiment: {len(sentiment)} days with {sentiment['count'].sum():,} texts")
    
    # January 2021 focus
    jan_2021 = vix.loc['2021-01'] if len(vix) > 0 else pd.DataFrame()
    
    if len(jan_2021) > 0:
        print(f"\n🎮 GameStop Week (Jan 25-29, 2021):")
        gme_week = vix.loc['2021-01-25':'2021-01-29']
        if len(gme_week) > 0:
            print(f"   VIX Range: {gme_week['vix'].min():.2f} - {gme_week['vix'].max():.2f}")
            print(f"   VIX Spike: {gme_week['vix'].max():.2f}")
    
    # Sentiment analysis
    if len(sentiment) > 0:
        jan_sent = sentiment.loc['2021-01']
        if len(jan_sent) > 0:
            print(f"\n📝 Sentiment (January 2021):")
            print(f"   Mean: {jan_sent['sentiment'].mean():.4f}")
            print(f"   Std: {jan_sent['sentiment'].std():.4f}")
            print(f"   Daily texts: {jan_sent['count'].mean():.0f}")
            
            # GameStop week sentiment
            gme_sent = sentiment.loc['2021-01-25':'2021-01-29']
            if len(gme_sent) > 0:
                print(f"\n   GME Week Sentiment:")
                print(f"   Mean: {gme_sent['sentiment'].mean():.4f}")
                print(f"   Texts: {gme_sent['count'].sum():,}")
    
    # CISS during GME (should be low - retail event, not systemic)
    if len(ciss) > 0:
        jan_ciss = ciss.loc['2021-01']
        if len(jan_ciss) > 0:
            print(f"\n📊 CISS (January 2021):")
            print(f"   Mean: {jan_ciss['ciss'].mean():.4f}")
            print(f"   Max: {jan_ciss['ciss'].max():.4f}")
            print(f"   Interpretation: {'Elevated systemic stress' if jan_ciss['ciss'].max() > 0.35 else 'Low systemic stress (retail event)'}")
    
    return {
        "period": f"{start} to {end}",
        "was_systemic": ciss.loc['2021-01']['ciss'].max() > 0.35 if len(ciss) > 0 else None,
    }


async def run_regime_validation(session) -> Dict:
    """Validate regime predictions against VIX ground truth."""
    print("\n" + "=" * 70)
    print("REGIME VALIDATION: CISS vs VIX")
    print("=" * 70)
    
    start = date(2010, 1, 1)
    end = date(2026, 1, 31)
    
    # Load VIX and CISS
    vix = await load_vix(session, start, end)
    ciss = await load_ciss(session, start, end)
    
    print(f"\n📊 Full Period Analysis ({start} to {end})")
    print(f"   VIX: {len(vix)} observations")
    print(f"   CISS: {len(ciss)} observations")
    
    if len(vix) == 0 or len(ciss) == 0:
        return {}
    
    # Align data
    common = vix.index.intersection(ciss.index)
    print(f"   Overlapping: {len(common)} days")
    
    if len(common) < 100:
        return {"error": "Insufficient overlap"}
    
    vix_aligned = vix.loc[common, 'vix']
    ciss_aligned = ciss.loc[common, 'ciss']
    
    # Assign regimes
    vix_regimes = vix_aligned.apply(assign_vix_regime)
    ciss_regimes = ciss_aligned.apply(assign_ciss_regime)
    
    # Calculate agreement
    agreement = (vix_regimes == ciss_regimes).mean()
    print(f"\n🎯 Regime Agreement: {agreement * 100:.1f}%")
    
    # Confusion matrix
    regime_order = ['calm', 'moderate', 'elevated', 'crisis']
    print(f"\n   Confusion Matrix (CISS predicted vs VIX actual):")
    print(f"   {'':12} | " + " | ".join(f"{r:>8}" for r in regime_order))
    print(f"   {'-' * 60}")
    
    for ciss_r in regime_order:
        row = []
        for vix_r in regime_order:
            count = ((ciss_regimes == ciss_r) & (vix_regimes == vix_r)).sum()
            row.append(count)
        print(f"   {ciss_r:12} | " + " | ".join(f"{c:>8}" for c in row))
    
    # Correlation
    corr = vix_aligned.corr(ciss_aligned)
    print(f"\n📈 VIX-CISS Correlation: {corr:.4f}")
    
    # Crisis detection accuracy
    vix_crisis = vix_regimes == 'crisis'
    ciss_crisis = ciss_regimes == 'crisis'
    
    tp = (vix_crisis & ciss_crisis).sum()
    fp = (~vix_crisis & ciss_crisis).sum()
    fn = (vix_crisis & ~ciss_crisis).sum()
    tn = (~vix_crisis & ~ciss_crisis).sum()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\n🔴 Crisis Detection Metrics:")
    print(f"   Precision: {precision * 100:.1f}%")
    print(f"   Recall: {recall * 100:.1f}%")
    print(f"   F1 Score: {f1 * 100:.1f}%")
    
    return {
        "agreement": agreement,
        "correlation": corr,
        "crisis_precision": precision,
        "crisis_recall": recall,
        "crisis_f1": f1,
    }


async def main():
    """Run all backtests."""
    from src.sentiment_detector.core.database import get_session_context
    
    print("\n" + "=" * 70)
    print("GARCH-MIDAS HISTORICAL BACKTESTS")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = {}
    
    async with get_session_context() as session:
        results['2008_crisis'] = await run_backtest_2008(session)
        results['covid_2020'] = await run_backtest_covid(session)
        results['gamestop_2021'] = await run_backtest_gamestop(session)
        results['regime_validation'] = await run_regime_validation(session)
    
    # Final summary
    print("\n" + "=" * 70)
    print("BACKTEST SUMMARY")
    print("=" * 70)
    
    if results.get('2008_crisis'):
        r = results['2008_crisis']
        print(f"\n📉 2008 Financial Crisis:")
        print(f"   CISS Peak: {r.get('ciss_peak', 'N/A'):.4f}")
        print(f"   Crisis Days: {r.get('crisis_days', 'N/A')}")
    
    if results.get('covid_2020'):
        r = results['covid_2020']
        print(f"\n🦠 COVID-19 March 2020:")
        print(f"   VIX Peak: {r.get('vix_peak', 'N/A'):.2f}")
    
    if results.get('gamestop_2021'):
        r = results['gamestop_2021']
        print(f"\n🎮 GameStop 2021:")
        print(f"   Systemic Event: {'Yes' if r.get('was_systemic') else 'No (retail event)'}")
    
    if results.get('regime_validation'):
        r = results['regime_validation']
        print(f"\n🎯 Regime Validation:")
        print(f"   CISS-VIX Agreement: {r.get('agreement', 0) * 100:.1f}%")
        print(f"   Crisis F1 Score: {r.get('crisis_f1', 0) * 100:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ ALL BACKTESTS COMPLETE")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = asyncio.run(main())
