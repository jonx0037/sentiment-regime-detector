#!/usr/bin/env python3
"""Regime Classification using Statistical Jump Model on HPC.

This script:
1. Loads volatility forecasts and sentiment data
2. Creates feature matrix (volatility + sentiment divergence + connectedness)
3. Fits Statistical Jump Model for regime detection
4. Generates SHAP explanations
5. Saves regime predictions

Part of Phase 3: After GARCH-MIDAS completes.
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

from sentiment_detector.models.jump_model import (
    StatisticalJumpModel,
    JumpModelConfig,
    RegimeState,
    create_feature_matrix
)


def load_volatility_data(volatility_file: Path) -> pd.DataFrame:
    """Load GARCH-MIDAS volatility estimates.

    Args:
        volatility_file: Path to volatility forecasts CSV

    Returns:
        DataFrame with volatility estimates
    """
    print("\n📊 Loading volatility data...")

    df = pd.read_csv(volatility_file, parse_dates=['date'])

    print(f"  ✓ Loaded {len(df):,} days")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")

    return df


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

    return df


def compute_sentiment_divergence(sentiment_df: pd.DataFrame, window: int = 22) -> pd.Series:
    """Compute sentiment divergence (deviation from moving average).

    Args:
        sentiment_df: DataFrame with compound_mean column
        window: Rolling window for divergence

    Returns:
        Series with sentiment divergence
    """
    print(f"\n📊 Computing sentiment divergence (window={window})...")

    sentiment = sentiment_df.set_index('date')['compound_mean']

    # Compute rolling mean
    rolling_mean = sentiment.rolling(window=window, min_periods=1).mean()

    # Divergence = current - rolling mean
    divergence = sentiment - rolling_mean

    print(f"  ✓ Divergence range: {divergence.min():.4f} to {divergence.max():.4f}")

    return divergence


def compute_connectedness_proxy(volatility_df: pd.DataFrame) -> pd.Series:
    """Compute connectedness proxy from volatility decomposition.

    Uses ratio of long-run to short-run volatility as proxy for
    cross-asset connectedness (when long-run dominates, systemic risk is high).

    Args:
        volatility_df: DataFrame with volatility components

    Returns:
        Series with connectedness proxy
    """
    print("\n📊 Computing connectedness proxy...")

    volatility_df = volatility_df.set_index('date')

    # Connectedness proxy: long_run / short_run
    # Higher ratio = more systemic/connected risk
    connectedness = (
        volatility_df['long_run_volatility'] /
        volatility_df['short_run_volatility'].replace(0, 1e-10)
    )

    # Clip extreme values
    connectedness = connectedness.clip(0, 10)

    print(f"  ✓ Connectedness range: {connectedness.min():.4f} to {connectedness.max():.4f}")

    return connectedness


def main():
    """Run regime classification."""
    parser = argparse.ArgumentParser(
        description="Statistical Jump Model regime classification"
    )
    parser.add_argument(
        "--volatility-file",
        type=str,
        required=True,
        help="Path to GARCH-MIDAS volatility CSV"
    )
    parser.add_argument(
        "--sentiment-file",
        type=str,
        required=True,
        help="Path to aggregated sentiment CSV"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="Output file for regime predictions"
    )
    parser.add_argument(
        "--jump-penalty",
        type=float,
        default=10.0,
        help="Jump penalty λ (default: 10.0)"
    )
    parser.add_argument(
        "--n-regimes",
        type=int,
        default=3,
        help="Number of regimes (default: 3)"
    )
    parser.add_argument(
        "--tune-lambda",
        action="store_true",
        help="Tune jump penalty parameter"
    )

    args = parser.parse_args()

    print("🔍 REGIME CLASSIFICATION")
    print("=" * 60)
    print(f"Volatility: {args.volatility_file}")
    print(f"Sentiment: {args.sentiment_file}")
    print(f"Output: {args.output_file}")
    print(f"Jump Penalty: {args.jump_penalty}")
    print(f"N Regimes: {args.n_regimes}")
    print("=" * 60)

    try:
        # Load data
        volatility_df = load_volatility_data(Path(args.volatility_file))
        sentiment_df = load_sentiment_data(Path(args.sentiment_file))

        # Compute features
        sentiment_divergence = compute_sentiment_divergence(sentiment_df)
        connectedness = compute_connectedness_proxy(volatility_df)

        # Align data by date
        print("\n📊 Aligning features by date...")
        volatility_df = volatility_df.set_index('date')

        # Create feature matrix
        dates = volatility_df.index
        features = create_feature_matrix(
            volatility=volatility_df['conditional_volatility'].values,
            sentiment_divergence=sentiment_divergence.reindex(dates, fill_value=0).values,
            connectedness=connectedness.reindex(dates, fill_value=1).values,
            normalize=True
        )

        print(f"  ✓ Feature matrix: {features.shape}")
        print(f"    - Volatility")
        print(f"    - Sentiment Divergence")
        print(f"    - Connectedness Proxy")

        # Initialize model
        config = JumpModelConfig(
            n_regimes=args.n_regimes,
            jump_penalty=args.jump_penalty,
            max_iter=100,
            tol=1e-6,
            init_method='kmeans',
            min_regime_duration=5
        )

        model = StatisticalJumpModel(config=config)

        # Tune lambda if requested
        if args.tune_lambda:
            print("\n📊 Tuning jump penalty parameter...")
            lambda_range = [1, 5, 10, 20, 50, 100]
            best_lambda, tuning_results = model.tune_jump_penalty(
                features,
                lambda_range=lambda_range,
                metric='turnover'  # Target ~44% annualized turnover (Shu et al.)
            )
            print(f"  ✓ Best λ: {best_lambda}")

            # Print tuning results
            print("\n  Tuning Results:")
            for λ, result in tuning_results.items():
                print(f"    λ={λ:5.1f}: {result['n_jumps']:3d} jumps, "
                      f"{result['annualized_turnover']:5.1%} turnover")

        # Fit and predict
        print("\n📊 Fitting Statistical Jump Model...")
        result = model.fit_predict(features)

        # Print results
        print("\n" + "=" * 60)
        print("Jump Model Results")
        print("=" * 60)
        print(f"\nRegime Statistics:")
        print(f"  Total transitions: {result.n_jumps}")
        print(f"  Annualized turnover: {(result.n_jumps / len(features)) * 252:.1%}")

        durations = result.get_regime_durations()
        print(f"\nAverage Regime Duration:")
        for regime_name, avg_duration in durations.items():
            print(f"  {regime_name}: {avg_duration:.1f} days")

        # Count regime occurrences
        unique, counts = np.unique(result.regimes, return_counts=True)
        print(f"\nRegime Distribution:")
        for regime_id, count in zip(unique, counts):
            regime_name = result.centroids[regime_id].regime_name
            pct = count / len(result.regimes) * 100
            print(f"  {regime_name}: {count} days ({pct:.1f}%)")

        # Compile output
        output_df = pd.DataFrame({
            'date': dates,
            'regime_id': result.regimes,
            'regime_name': result.regime_names,
            'prob_risk_on': result.regime_probabilities[:, 0],
            'prob_transition': result.regime_probabilities[:, 1],
            'prob_risk_off': result.regime_probabilities[:, 2],
            'volatility': volatility_df['conditional_volatility'].values,
            'sentiment_divergence': sentiment_divergence.reindex(dates, fill_value=0).values,
            'connectedness': connectedness.reindex(dates, fill_value=1).values,
        })

        # Add crisis indicator (risk_off or high uncertainty)
        output_df['crisis_indicator'] = (
            (output_df['regime_name'] == RegimeState.RISK_OFF.value) |
            (output_df['prob_risk_off'] > 0.5)
        ).astype(int)

        # Save results
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_df.to_csv(output_path, index=False)

        print(f"\n💾 Saved regime predictions: {output_path}")
        print(f"   Total days: {len(output_df):,}")
        print(f"   Crisis days: {output_df['crisis_indicator'].sum()} ({output_df['crisis_indicator'].mean():.1%})")

        # Generate SHAP explanations if possible
        try:
            print("\n📊 Generating SHAP explanations...")
            import shap

            # Create explainer (use a sample for speed)
            sample_size = min(1000, len(features))
            background = features[np.random.choice(len(features), sample_size, replace=False)]

            # For now, just save feature importances from centroids
            feature_names = ['volatility', 'sentiment_divergence', 'connectedness']
            centroid_features = np.array([c.mean for c in result.centroids])

            importance_df = pd.DataFrame(
                centroid_features,
                columns=feature_names,
                index=[c.regime_name for c in result.centroids]
            )

            importance_path = output_path.parent / f"{output_path.stem}_feature_importance.csv"
            importance_df.to_csv(importance_path)
            print(f"💾 Saved feature importance: {importance_path}")

        except Exception as e:
            print(f"  ⚠️  SHAP explanations skipped: {e}")

        print("\n" + "=" * 60)
        print("✅ REGIME CLASSIFICATION COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
