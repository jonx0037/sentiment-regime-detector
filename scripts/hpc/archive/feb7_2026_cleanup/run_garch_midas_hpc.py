#!/usr/bin/env python3
"""
GARCH-MIDAS Full Estimation for HPC (ManeFrame III).

This script runs the complete GARCH-MIDAS model with the arch library,
which requires proper installation on HPC (causes segfaults on macOS).

Usage on ManeFrame:
    module load python/3.11.11
    pip install --user arch
    python run_garch_midas_hpc.py

Outputs:
    - garch_midas_results_YYYYMMDD.json
    - volatility_decomposition.csv
"""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

# Check for arch library
try:
    from arch import arch_model
    from arch.univariate import GARCH, ConstantMean
    ARCH_AVAILABLE = True
except ImportError:
    ARCH_AVAILABLE = False
    print("WARNING: arch library not available. Using fallback estimation.")


def load_data_from_csv(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """Load exported CSV data for HPC processing."""
    data = {}
    
    # Load VIX
    vix_file = data_dir / "vix_data.csv"
    if vix_file.exists():
        data['vix'] = pd.read_csv(vix_file, parse_dates=['date'], index_col='date')
        print(f"Loaded VIX: {len(data['vix'])} records")
    
    # Load CISS
    ciss_file = data_dir / "ciss_data.csv"
    if ciss_file.exists():
        data['ciss'] = pd.read_csv(ciss_file, parse_dates=['date'], index_col='date')
        print(f"Loaded CISS: {len(data['ciss'])} records")
    
    # Load sentiment
    sentiment_file = data_dir / "sentiment_daily.csv"
    if sentiment_file.exists():
        data['sentiment'] = pd.read_csv(sentiment_file, parse_dates=['date'], index_col='date')
        print(f"Loaded Sentiment: {len(data['sentiment'])} records")
    
    # Load market returns
    returns_file = data_dir / "market_returns.csv"
    if returns_file.exists():
        data['returns'] = pd.read_csv(returns_file, parse_dates=['date'], index_col='date')
        print(f"Loaded Returns: {len(data['returns'])} records")
    
    return data


def fit_garch_model(
    returns: np.ndarray,
    p: int = 1,
    q: int = 1,
) -> Dict:
    """Fit standard GARCH(p,q) model."""
    if not ARCH_AVAILABLE:
        return {"error": "arch library not available"}
    
    # Scale returns (arch expects percentage returns)
    returns_pct = returns * 100
    
    # Fit GARCH model
    model = arch_model(
        returns_pct,
        mean='Constant',
        vol='GARCH',
        p=p,
        q=q,
        dist='normal'
    )
    
    result = model.fit(disp='off', show_warning=False)
    
    return {
        "params": dict(result.params),
        "aic": result.aic,
        "bic": result.bic,
        "loglikelihood": result.loglikelihood,
        "conditional_volatility": result.conditional_volatility.tolist(),
    }


def fit_garch_midas_with_sentiment(
    returns: pd.Series,
    sentiment: pd.Series,
    ciss: Optional[pd.Series] = None,
    midas_lags: int = 22,
) -> Dict:
    """
    Fit GARCH-MIDAS model with sentiment as exogenous variable.
    
    The GARCH-MIDAS decomposes volatility into:
    - Short-run (GARCH) component: g_t
    - Long-run (MIDAS) component: τ_t based on sentiment
    
    σ²_t = g_t × τ_t
    
    τ_t = exp(m + θ × sentiment_aggregated)
    """
    if not ARCH_AVAILABLE:
        # Fallback OLS-based estimation
        return _fit_garch_midas_fallback(returns, sentiment, ciss, midas_lags)
    
    # Align data
    common_idx = returns.index.intersection(sentiment.index)
    if ciss is not None:
        common_idx = common_idx.intersection(ciss.index)
    
    if len(common_idx) < 100:
        return {"error": f"Insufficient data: {len(common_idx)} observations"}
    
    returns_aligned = returns.loc[common_idx].dropna()
    sentiment_aligned = sentiment.loc[common_idx]
    
    # Create weekly aggregated sentiment (MIDAS weighting)
    weekly_sentiment = sentiment_aligned.resample('W').mean()
    
    # Exponential Almon lag weights for MIDAS
    def almon_weights(K, theta1=1.0, theta2=5.0):
        """Exponential Almon lag polynomial weights."""
        k = np.arange(1, K + 1)
        weights = np.exp(theta1 * k + theta2 * k**2)
        return weights / weights.sum()
    
    weights = almon_weights(midas_lags)
    
    # Calculate weighted sentiment component
    sentiment_midas = []
    for i in range(len(returns_aligned)):
        dt = returns_aligned.index[i]
        # Get past midas_lags weeks of sentiment
        past_weeks = weekly_sentiment.loc[:dt].tail(midas_lags)
        if len(past_weeks) >= midas_lags:
            weighted_sent = np.sum(past_weeks.values[-midas_lags:] * weights)
            sentiment_midas.append(weighted_sent)
        else:
            sentiment_midas.append(np.nan)
    
    sentiment_midas = pd.Series(sentiment_midas, index=returns_aligned.index)
    
    # Drop NaNs from MIDAS calculation
    valid_idx = ~sentiment_midas.isna()
    returns_valid = returns_aligned[valid_idx]
    sentiment_midas_valid = sentiment_midas[valid_idx]
    
    if len(returns_valid) < 100:
        return {"error": f"Insufficient valid data after MIDAS: {len(returns_valid)}"}
    
    # Step 1: Estimate long-run component via regression
    realized_var = returns_valid ** 2
    log_realized_var = np.log(realized_var.replace(0, 1e-10))
    
    # τ_t = exp(m + θ × X)
    X = sentiment_midas_valid.values
    y = log_realized_var.values
    
    # Add CISS if available
    if ciss is not None:
        ciss_aligned = ciss.loc[returns_valid.index]
        ciss_midas = ciss_aligned.resample('W').mean().reindex(
            returns_valid.index, method='ffill'
        )
        X = np.column_stack([X, ciss_midas.values])
    
    # OLS for long-run component
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    X_with_const = np.column_stack([np.ones(len(X)), X])
    
    coeffs, residuals, rank, s = np.linalg.lstsq(X_with_const, y, rcond=None)
    
    # Long-run component τ_t
    tau_t = np.exp(X_with_const @ coeffs)
    
    # Step 2: Standardize returns by long-run component
    returns_standardized = returns_valid / np.sqrt(tau_t)
    
    # Step 3: Fit GARCH on standardized returns
    returns_pct = returns_standardized.values * 100
    
    garch_model = arch_model(
        returns_pct,
        mean='Constant',
        vol='GARCH',
        p=1,
        q=1,
        dist='normal'
    )
    
    garch_result = garch_model.fit(disp='off', show_warning=False)
    
    # Short-run component g_t
    g_t = (garch_result.conditional_volatility / 100) ** 2
    
    # Total volatility σ_t = sqrt(g_t × τ_t)
    sigma_t = np.sqrt(g_t * tau_t)
    
    # Calculate decomposition stats
    var_total = np.var(np.log(sigma_t ** 2))
    var_longrun = np.var(np.log(tau_t))
    var_shortrun = np.var(np.log(g_t))
    
    result = {
        "n_observations": len(returns_valid),
        "midas_lags": midas_lags,
        "long_run_coefficients": {
            "constant": float(coeffs[0]),
            "sentiment": float(coeffs[1]),
        },
        "garch_params": dict(garch_result.params),
        "garch_aic": float(garch_result.aic),
        "garch_bic": float(garch_result.bic),
        "volatility_decomposition": {
            "long_run_variance_share": float(var_longrun / var_total) if var_total > 0 else 0,
            "short_run_variance_share": float(var_shortrun / var_total) if var_total > 0 else 0,
            "mean_long_run_vol": float(np.sqrt(tau_t).mean() * np.sqrt(252)),
            "mean_short_run_vol": float(np.sqrt(g_t).mean()),
            "mean_total_vol": float(sigma_t.mean() * np.sqrt(252)),
        },
        "conditional_volatility": sigma_t.tolist(),
        "long_run_component": tau_t.tolist(),
        "short_run_component": g_t.tolist(),
        "dates": returns_valid.index.strftime('%Y-%m-%d').tolist(),
    }
    
    if ciss is not None and len(coeffs) > 2:
        result["long_run_coefficients"]["ciss"] = float(coeffs[2])
    
    return result


def _fit_garch_midas_fallback(
    returns: pd.Series,
    sentiment: pd.Series,
    ciss: Optional[pd.Series] = None,
    midas_lags: int = 22,
) -> Dict:
    """Fallback estimation when arch is not available."""
    # Simple OLS-based approximation
    common_idx = returns.index.intersection(sentiment.index)
    if ciss is not None:
        common_idx = common_idx.intersection(ciss.index)
    
    returns_aligned = returns.loc[common_idx].dropna()
    sentiment_aligned = sentiment.loc[common_idx]
    
    # Calculate realized variance
    realized_var = returns_aligned ** 2
    
    # Weekly sentiment
    weekly_sentiment = sentiment_aligned.resample('W').mean().ffill()
    sentiment_weekly = weekly_sentiment.reindex(returns_aligned.index, method='ffill')
    
    # Regression
    X = sentiment_weekly.values
    y = realized_var.values
    
    mask = ~(np.isnan(X) | np.isnan(y))
    X_clean = X[mask]
    y_clean = y[mask]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_clean, y_clean)
    
    result = {
        "method": "fallback_ols",
        "n_observations": len(X_clean),
        "sentiment_coefficient": float(slope),
        "intercept": float(intercept),
        "r_squared": float(r_value ** 2),
        "p_value": float(p_value),
        "mean_volatility": float(np.sqrt(y_clean.mean()) * np.sqrt(252)),
    }
    
    if ciss is not None:
        ciss_aligned = ciss.loc[common_idx]
        ciss_clean = ciss_aligned.values[mask]
        
        X_multi = np.column_stack([np.ones(len(X_clean)), X_clean, ciss_clean])
        coeffs, residuals, rank, s = np.linalg.lstsq(X_multi, y_clean, rcond=None)
        
        y_pred = X_multi @ coeffs
        ss_res = np.sum((y_clean - y_pred) ** 2)
        ss_tot = np.sum((y_clean - np.mean(y_clean)) ** 2)
        
        result["ciss_coefficient"] = float(coeffs[2])
        result["sentiment_coefficient_with_ciss"] = float(coeffs[1])
        result["r_squared_with_ciss"] = float(1 - ss_res / ss_tot)
    
    return result


def run_backtests(data: Dict[str, pd.DataFrame]) -> Dict:
    """Run all historical backtests."""
    results = {}
    
    # Get required data
    returns = data.get('returns', pd.DataFrame())
    sentiment = data.get('sentiment', pd.DataFrame())
    ciss = data.get('ciss', pd.DataFrame())
    vix = data.get('vix', pd.DataFrame())
    
    if len(returns) == 0:
        return {"error": "No returns data"}
    
    # Extract series
    if 'returns' in returns.columns:
        returns_series = returns['returns']
    else:
        returns_series = returns.iloc[:, 0]
    
    if len(sentiment) > 0:
        if 'sentiment' in sentiment.columns:
            sentiment_series = sentiment['sentiment']
        else:
            sentiment_series = sentiment.iloc[:, 0]
    else:
        sentiment_series = None
    
    if len(ciss) > 0:
        if 'ciss' in ciss.columns:
            ciss_series = ciss['ciss']
        elif 'value' in ciss.columns:
            ciss_series = ciss['value']
        else:
            ciss_series = ciss.iloc[:, 0]
    else:
        ciss_series = None
    
    # 1. Full period GARCH-MIDAS
    print("\n" + "=" * 60)
    print("FULL PERIOD GARCH-MIDAS ESTIMATION")
    print("=" * 60)
    
    if sentiment_series is not None:
        results['full_period'] = fit_garch_midas_with_sentiment(
            returns_series,
            sentiment_series,
            ciss_series,
            midas_lags=22
        )
        
        if 'error' not in results['full_period']:
            print(f"Observations: {results['full_period']['n_observations']}")
            print(f"Sentiment β: {results['full_period']['long_run_coefficients']['sentiment']:.6f}")
            if 'ciss' in results['full_period']['long_run_coefficients']:
                print(f"CISS β: {results['full_period']['long_run_coefficients']['ciss']:.6f}")
            print(f"Long-run vol share: {results['full_period']['volatility_decomposition']['long_run_variance_share']:.2%}")
    
    # 2. 2008 Financial Crisis
    print("\n" + "=" * 60)
    print("2008 FINANCIAL CRISIS")
    print("=" * 60)
    
    crisis_start = pd.Timestamp('2007-06-01')
    crisis_end = pd.Timestamp('2010-06-30')
    
    mask = (returns_series.index >= crisis_start) & (returns_series.index <= crisis_end)
    if mask.sum() > 100 and sentiment_series is not None:
        results['crisis_2008'] = fit_garch_midas_with_sentiment(
            returns_series[mask],
            sentiment_series,
            ciss_series,
            midas_lags=22
        )
        
        if 'error' not in results['crisis_2008']:
            print(f"Observations: {results['crisis_2008']['n_observations']}")
            print(f"Mean annualized vol: {results['crisis_2008']['volatility_decomposition']['mean_total_vol']:.2%}")
    
    # 3. COVID-19
    print("\n" + "=" * 60)
    print("COVID-19 MARCH 2020")
    print("=" * 60)
    
    covid_start = pd.Timestamp('2019-10-01')
    covid_end = pd.Timestamp('2020-06-30')
    
    mask = (returns_series.index >= covid_start) & (returns_series.index <= covid_end)
    if mask.sum() > 50 and sentiment_series is not None:
        results['covid_2020'] = fit_garch_midas_with_sentiment(
            returns_series[mask],
            sentiment_series,
            ciss_series,
            midas_lags=12  # Shorter period
        )
        
        if 'error' not in results['covid_2020']:
            print(f"Observations: {results['covid_2020']['n_observations']}")
    
    # 4. Simple GARCH for comparison
    print("\n" + "=" * 60)
    print("BASELINE GARCH(1,1)")
    print("=" * 60)
    
    results['baseline_garch'] = fit_garch_model(returns_series.dropna().values)
    
    if 'error' not in results['baseline_garch']:
        print(f"GARCH params: {results['baseline_garch']['params']}")
        print(f"AIC: {results['baseline_garch']['aic']:.2f}")
    
    return results


def main():
    """Main entry point for HPC execution."""
    print("=" * 60)
    print("GARCH-MIDAS HPC ESTIMATION")
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"arch library available: {ARCH_AVAILABLE}")
    print("=" * 60)
    
    # Determine data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir / "hpc_data"
    
    if not data_dir.exists():
        # Try parent directory
        data_dir = script_dir.parent / "hpc_data"
    
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        print("Please run export_garch_midas_data.py first to create CSV files.")
        return 1
    
    print(f"\nLoading data from: {data_dir}")
    
    # Load data
    data = load_data_from_csv(data_dir)
    
    if not data:
        print("ERROR: No data loaded")
        return 1
    
    # Run backtests
    results = run_backtests(data)
    
    # Save results
    output_file = script_dir / f"garch_midas_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Convert numpy types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(v) for v in obj]
        return obj
    
    results_serializable = convert_types(results)
    
    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if 'full_period' in results and 'error' not in results['full_period']:
        r = results['full_period']
        print(f"\nFull Period GARCH-MIDAS:")
        print(f"  Observations: {r['n_observations']}")
        print(f"  Sentiment coefficient: {r['long_run_coefficients']['sentiment']:.6f}")
        if 'ciss' in r['long_run_coefficients']:
            print(f"  CISS coefficient: {r['long_run_coefficients']['ciss']:.6f}")
        print(f"  Long-run vol contribution: {r['volatility_decomposition']['long_run_variance_share']:.1%}")
        print(f"  Mean annualized vol: {r['volatility_decomposition']['mean_total_vol']:.1%}")
    
    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
