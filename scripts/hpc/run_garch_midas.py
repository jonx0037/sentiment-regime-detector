#!/usr/bin/env python3
"""GARCH-MIDAS Volatility Forecasting on HPC.

This script:
1. Loads daily sentiment aggregates and market data
2. Fits GARCH-MIDAS model with sentiment + CISS
3. Generates volatility forecasts
4. Saves results for regime classification

Part of Phase 2: After sentiment processing completes.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sentiment_detector.models.garch_midas import (
    GARCHMIDASWithCISS,
    compute_sentiment_index
)


def load_sentiment_data(sentiment_file: Path) -> pd.DataFrame:
    """Load aggregated daily sentiment data.

    Args:
        sentiment_file: Path to finbert_daily_sentiment_v2.csv

    Returns:
        DataFrame with daily sentiment
    """
    print("\n📊 Loading sentiment data...")

    df = pd.read_csv(sentiment_file, parse_dates=['date'])

    print(f"  ✓ Loaded {len(df):,} days")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")

    return df


def load_market_data(data_dir: Path) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Load market data (returns, VIX, CISS).

    Args:
        data_dir: Directory containing market data CSVs

    Returns:
        Tuple of (returns, vix, ciss) series
    """
    print("\n📊 Loading market data...")

    # Load VIX
    vix_file = data_dir / "vix_data.csv"
    if vix_file.exists():
        vix_df = pd.read_csv(vix_file, parse_dates=['date'])
        vix = vix_df.set_index('date')['close']
        print(f"  ✓ VIX: {len(vix):,} records")
    else:
        print("  ⚠️  VIX data not found, will skip")
        vix = None

    # Load CISS
    ciss_file = data_dir / "ciss_data.csv"
    if ciss_file.exists():
        ciss_df = pd.read_csv(ciss_file, parse_dates=['date'])
        ciss = ciss_df.set_index('date')['ciss']
        print(f"  ✓ CISS: {len(ciss):,} records")
    else:
        print("  ⚠️  CISS data not found, will use VIX only")
        ciss = None

    # Compute returns from VIX if available
    if vix is not None:
        returns = vix.pct_change().dropna()
        print(f"  ✓ Returns: {len(returns):,} records")
    else:
        returns = None

    return returns, vix, ciss


def main():
    """Run GARCH-MIDAS volatility forecasting."""
    parser = argparse.ArgumentParser(
        description="GARCH-MIDAS volatility forecasting with sentiment"
    )
    parser.add_argument(
        "--sentiment-file",
        type=str,
        required=True,
        help="Path to aggregated sentiment CSV (finbert_daily_sentiment_v2.csv)"
    )
    parser.add_argument(
        "--market-data-dir",
        type=str,
        required=True,
        help="Directory containing market data (VIX, CISS)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Output file for volatility forecasts"
    )
    parser.add_argument(
        "--midas-lags",
        type=int,
        default=22,
        help="MIDAS lag window (default: 22 days)"
    )
    parser.add_argument(
        "--ciss-weight",
        type=float,
        default=0.5,
        help="Weight for CISS vs sentiment (0=sentiment only, 1=CISS only)"
    )
    parser.add_argument(
        "--forecast-horizon",
        type=int,
        default=22,
        help="Forecast horizon in days"
    )

    args = parser.parse_args()

    print("🔍 GARCH-MIDAS VOLATILITY FORECASTING")
    print("=" * 60)
    print(f"Sentiment: {args.sentiment_file}")
    print(f"Market Data: {args.market_data_dir}")
    print(f"Output: {args.output_file}")
    print(f"MIDAS Lags: {args.midas_lags}")
    print(f"CISS Weight: {args.ciss_weight}")
    print("=" * 60)

    try:
        # Load data
        sentiment_df = load_sentiment_data(Path(args.sentiment_file))
        returns, vix, ciss = load_market_data(Path(args.market_data_dir))

        if returns is None:
            print("\n❌ ERROR: No market data available for modeling")
            sys.exit(1)

        # Create sentiment index
        print("\n📊 Computing sentiment index...")
        sentiment_index = sentiment_df.set_index('date')['compound_mean']
        print(f"  ✓ Sentiment index: {len(sentiment_index):,} days")

        # Initialize GARCH-MIDAS model
        print("\n📊 Initializing GARCH-MIDAS model...")
        model = GARCHMIDASWithCISS(
            p=1,
            q=1,
            midas_lags=args.midas_lags,
            midas_omega1=1.0,
            midas_omega2=1.0,
            distribution='t',  # Student-t for fat tails
            ciss_weight=args.ciss_weight
        )

        # Fit model
        print("\n📊 Fitting GARCH-MIDAS...")
        print("  This may take several minutes...")

        result = model.fit_with_ciss(
            returns=returns,
            sentiment=sentiment_index,
            ciss=ciss,
            ciss_transform='zscore'  # Standardize CISS
        )

        # Print results
        print("\n" + "=" * 60)
        print("GARCH-MIDAS Results")
        print("=" * 60)
        print(f"\nGARCH Parameters:")
        print(f"  ω (omega):  {result.params['omega']:.6f}")
        print(f"  α (alpha):  {result.params['alpha']:.6f}")
        print(f"  β (beta):   {result.params['beta']:.6f}")

        print(f"\nExogenous Coefficients:")
        print(f"  Sentiment:  {result.sentiment_coefficient:.6f}" if result.sentiment_coefficient else "  Sentiment:  N/A")
        print(f"  CISS:       {result.ciss_coefficient:.6f}" if result.ciss_coefficient else "  CISS:       N/A")

        print(f"\nModel Fit:")
        print(f"  Log-Likelihood: {result.log_likelihood:.2f}")
        print(f"  AIC: {result.aic:.2f}")
        print(f"  BIC: {result.bic:.2f}")
        print(f"  Converged: {result.convergence}")

        print(f"\nVolatility Statistics:")
        vol_mean = result.conditional_volatility.mean()
        vol_std = result.conditional_volatility.std()
        vol_max = result.conditional_volatility.max()
        print(f"  Mean: {vol_mean:.4f}")
        print(f"  Std:  {vol_std:.4f}")
        print(f"  Max:  {vol_max:.4f}")

        # Generate forecasts
        print(f"\n📊 Generating {args.forecast_horizon}-day forecast...")
        forecast = model.forecast(steps=args.forecast_horizon)

        # Compile output
        output_df = pd.DataFrame({
            'date': result.conditional_volatility.index,
            'conditional_volatility': result.conditional_volatility.values,
            'long_run_volatility': result.long_run_volatility.values,
            'short_run_volatility': result.short_run_volatility.values,
        })

        # Add regime classification (simple thresholds)
        vol_q25 = output_df['conditional_volatility'].quantile(0.25)
        vol_q75 = output_df['conditional_volatility'].quantile(0.75)

        output_df['volatility_regime'] = 'normal'
        output_df.loc[output_df['conditional_volatility'] <= vol_q25, 'volatility_regime'] = 'low'
        output_df.loc[output_df['conditional_volatility'] >= vol_q75, 'volatility_regime'] = 'high'

        # Save results
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_df.to_csv(output_path, index=False)

        print(f"\n💾 Saved volatility estimates: {output_path}")
        print(f"   Total days: {len(output_df):,}")
        print(f"   Low volatility: {(output_df['volatility_regime']=='low').sum()} days")
        print(f"   Normal: {(output_df['volatility_regime']=='normal').sum()} days")
        print(f"   High volatility: {(output_df['volatility_regime']=='high').sum()} days")

        # Save forecast
        forecast_path = output_path.parent / f"{output_path.stem}_forecast.csv"
        forecast.to_csv(forecast_path, index=True)
        print(f"💾 Saved forecast: {forecast_path}")

        print("\n" + "=" * 60)
        print("✅ GARCH-MIDAS COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
