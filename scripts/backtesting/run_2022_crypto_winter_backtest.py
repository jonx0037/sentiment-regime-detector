#!/usr/bin/env python3
"""
2022 Crypto Winter Backtest - Multi-Phase Crisis Analysis

This script analyzes the 2022 cryptocurrency market collapse, which consisted
of multiple interconnected failures demonstrating systemic contagion:

Phase 1: Luna/Terra Collapse (May 7-13, 2022)
- Terra USD (UST) stablecoin loses peg
- Luna token hyperinflates from $80 to $0.0001
- ~$40 billion in market cap destroyed
- VIX: Moderate elevation (~30), sector-specific crisis

Phase 2: Celsius/3AC Contagion (June 12-27, 2022)
- Celsius Network halts withdrawals (June 12)
- Three Arrows Capital (3AC) liquidations begin
- Cascading liquidations across DeFi protocols
- VIX: Still moderate, but crypto fear index (CFI) spikes

Phase 3: Broader Impact (June-July 2022)
- Bitcoin drops from $40k to $17.6k (-56%)
- Ethereum drops from $3k to $880 (-70%)
- Traditional markets show limited contagion
- Tests model's ability to detect sector-specific vs systemic risk

This event is particularly valuable because:
1. It was largely isolated to crypto (sector-specific)
2. It showed clear contagion patterns within the sector
3. Traditional risk indicators (VIX, CISS) were only moderately elevated
4. It tests if sentiment-based detection outperforms VIX for crypto crises
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.sentiment_detector.services.regime_classifier import (
    MLRegimeClassifier,
    RegimeClassification,
    SentimentFeatures,
)


# ==================== EVENT DEFINITIONS ====================
PHASES = {
    "luna_terra": {
        "name": "Luna/Terra Collapse",
        "start_date": "2022-05-07",
        "end_date": "2022-05-15",
        "peak_date": "2022-05-12",  # Peak panic
        "description": "UST depeg and Luna hyperinflation - $40B destroyed",
    },
    "celsius_3ac": {
        "name": "Celsius/3AC Contagion",
        "start_date": "2022-06-12",
        "end_date": "2022-06-27",
        "peak_date": "2022-06-18",  # Peak liquidations
        "description": "Major crypto lenders collapse, DeFi liquidation cascade",
    },
    "full_crisis": {
        "name": "Full 2022 Crypto Winter",
        "start_date": "2022-05-01",
        "end_date": "2022-07-31",
        "peak_date": "2022-06-18",  # Overall crisis peak
        "description": "Multi-phase crypto market collapse and contagion",
    },
}


# ==================== DATA LOADING ====================
def load_sentiment_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load sentiment data for the specified period."""
    csv_path = Path("scripts/hpc/hpc_data/sentiment_daily_by_asset.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"Sentiment data not found: {csv_path}")

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Rename columns
    df = df.rename(
        columns={
            "sentiment": "mean_compound",
            "count": "text_count",
        }
    )

    # Add std_compound if not present
    if "std_compound" not in df.columns:
        df["std_compound"] = 0.1

    return df


def load_vix_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load VIX data."""
    csv_path = Path("scripts/hpc/hpc_data/vix_data.csv")

    if not csv_path.exists():
        print(f"⚠️  VIX data not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_ciss_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load CISS data."""
    csv_path = Path("scripts/hpc/hpc_data/ciss_data.csv")

    if not csv_path.exists():
        print(f"⚠️  CISS data not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_crypto_prices(start_date: str, end_date: str) -> pd.DataFrame:
    """Load crypto price data for BTC and ETH."""
    csv_path = Path("scripts/hpc/hpc_data/cross_asset_prices.csv")

    if not csv_path.exists():
        print(f"⚠️  Price data not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Filter for crypto assets
    crypto_df = df[df["symbol"].isin(["BTC-USD", "ETH-USD"])]
    return crypto_df


# ==================== FEATURE ENGINEERING ====================
def prepare_ml_features(sentiment_df, ciss_df, vix_df) -> pd.DataFrame:
    """Prepare features for ML classifier."""
    # Pivot sentiment data by asset class
    sentiment_pivot = sentiment_df.pivot_table(
        index="date", columns="asset_class", values="mean_compound", aggfunc="mean"
    )

    # Create feature dataframe
    features = pd.DataFrame(index=sentiment_pivot.index)

    # Add per-asset sentiment
    for asset_class in ["equity", "crypto", "forex", "commodity"]:
        if asset_class in sentiment_pivot.columns:
            features[f"{asset_class}_sentiment"] = sentiment_pivot[asset_class]
        else:
            features[f"{asset_class}_sentiment"] = 0.0

    # Calculate aggregate sentiment
    asset_cols = [
        "equity_sentiment",
        "crypto_sentiment",
        "forex_sentiment",
        "commodity_sentiment",
    ]
    features["sentiment_mean"] = features[asset_cols].mean(axis=1)
    features["sentiment_std"] = features[asset_cols].std(axis=1)

    # Calculate momentum (7-day rolling)
    features["sentiment_momentum"] = features["sentiment_mean"].diff(7)
    features["sentiment_acceleration"] = features["sentiment_momentum"].diff(7)

    # Calculate divergence
    features["max_divergence"] = features[asset_cols].max(axis=1) - features[
        asset_cols
    ].min(axis=1)

    # Add VIX and CISS if available
    if not vix_df.empty:
        features = features.join(vix_df[["close"]], how="left")
        features = features.rename(columns={"close": "vix_level"})
        features["vix_level"] = features["vix_level"].ffill()

    if not ciss_df.empty:
        features = features.join(ciss_df[["value"]], how="left")
        features = features.rename(columns={"value": "ciss_level"})
        features["ciss_level"] = features["ciss_level"].ffill()

    # Forward fill missing values
    features = features.ffill().fillna(0)

    return features


# ==================== REGIME DETECTION ====================
def run_regime_detection(features_df: pd.DataFrame, classifier) -> pd.DataFrame:
    """Run regime detection for each day."""
    results = []

    for date, row in features_df.iterrows():
        # Create SentimentFeatures object
        sentiment_features = SentimentFeatures(
            equity_sentiment=row["equity_sentiment"],
            crypto_sentiment=row["crypto_sentiment"],
            forex_sentiment=row["forex_sentiment"],
            commodity_sentiment=row["commodity_sentiment"],
            cross_asset_mean=row["sentiment_mean"],
            cross_asset_std=row["sentiment_std"],
            sentiment_momentum=row["sentiment_momentum"],
            sentiment_acceleration=row["sentiment_acceleration"],
            max_divergence=row["max_divergence"],
            vix_level=row.get("vix_level"),
            ciss_level=row.get("ciss_level"),
        )

        # Classify regime
        classification = classifier.classify(sentiment_features)

        results.append(
            {
                "date": date,
                "regime": classification.state.value,
                "confidence": classification.confidence,
                "prob_risk_on": classification.prob_risk_on,
                "prob_risk_off": classification.prob_risk_off,
                "prob_transition": classification.prob_transition,
                "crypto_sentiment": row["crypto_sentiment"],
                "equity_sentiment": row["equity_sentiment"],
                "vix_level": row.get("vix_level"),
                "ciss_level": row.get("ciss_level"),
            }
        )

    return pd.DataFrame(results)


# ==================== ANALYSIS ====================
def analyze_contagion_patterns(sentiment_df: pd.DataFrame) -> Dict:
    """Analyze cross-asset contagion patterns."""
    # Pivot by asset class
    pivot = sentiment_df.pivot_table(
        index="date", columns="asset_class", values="mean_compound"
    )

    # Calculate correlations
    correlations = pivot.corr()

    # Calculate rolling correlations with crypto
    if "crypto" in pivot.columns:
        rolling_corrs = {}
        for asset in ["equity", "forex", "commodity"]:
            if asset in pivot.columns:
                rolling_corrs[asset] = (
                    pivot["crypto"].rolling(7).corr(pivot[asset])
                )

        return {
            "correlations": correlations.to_dict(),
            "rolling_correlations": {
                k: v.to_dict() for k, v in rolling_corrs.items()
            },
        }

    return {"correlations": correlations.to_dict()}


def calculate_sentiment_vs_vix_lead_lag(results_df: pd.DataFrame) -> Dict:
    """
    Calculate lead-lag relationship between sentiment and VIX.
    Tests if sentiment leads VIX during sector-specific crises.
    """
    if "vix_level" not in results_df.columns:
        return {}

    # Calculate changes
    results_df["crypto_sentiment_change"] = results_df["crypto_sentiment"].diff()
    results_df["vix_change"] = results_df["vix_level"].diff()

    # Test various lags
    lag_correlations = {}
    for lag in range(-5, 6):  # -5 to +5 days
        if lag < 0:
            # Negative lag: sentiment leads VIX
            corr = results_df["crypto_sentiment_change"].corr(
                results_df["vix_change"].shift(-lag)
            )
        else:
            # Positive lag: VIX leads sentiment
            corr = results_df["crypto_sentiment_change"].shift(lag).corr(
                results_df["vix_change"]
            )

        lag_correlations[lag] = corr

    return {"lead_lag_correlations": lag_correlations}


def evaluate_detection_accuracy(
    results_df: pd.DataFrame, phase_info: Dict
) -> Dict:
    """
    Evaluate how well the model detected the crisis.
    For crypto crises, we expect:
    1. High crypto sentiment divergence from other assets
    2. Risk-off detection before VIX spikes
    3. Sustained risk-off during crisis peak
    """
    peak_date = pd.to_datetime(phase_info["peak_date"])
    start_date = pd.to_datetime(phase_info["start_date"])

    # Get peak period (±3 days around peak)
    peak_window = results_df[
        (results_df["date"] >= peak_date - pd.Timedelta(days=3))
        & (results_df["date"] <= peak_date + pd.Timedelta(days=3))
    ]

    # Calculate metrics
    risk_off_pct = (
        (results_df["regime"] == "risk_off").sum() / len(results_df) * 100
    )
    peak_risk_off_pct = (
        (peak_window["regime"] == "risk_off").sum() / len(peak_window) * 100
        if len(peak_window) > 0
        else 0
    )

    # Early warning: did we detect risk-off before the peak?
    pre_peak = results_df[results_df["date"] < peak_date]
    early_warning = (pre_peak["regime"] == "risk_off").any()
    if early_warning:
        first_warning = pre_peak[pre_peak["regime"] == "risk_off"][
            "date"
        ].iloc[0]
        days_before_peak = (peak_date - first_warning).days
    else:
        days_before_peak = 0

    # Crypto sentiment divergence
    crypto_equity_divergence = abs(
        results_df["crypto_sentiment"].mean()
        - results_df["equity_sentiment"].mean()
    )

    return {
        "risk_off_pct": risk_off_pct,
        "peak_risk_off_pct": peak_risk_off_pct,
        "early_warning": early_warning,
        "days_before_peak": days_before_peak,
        "crypto_equity_divergence": crypto_equity_divergence,
        "avg_confidence": results_df["confidence"].mean(),
        "avg_crypto_sentiment": results_df["crypto_sentiment"].mean(),
        "avg_vix": results_df["vix_level"].mean() if "vix_level" in results_df.columns else None,
    }


# ==================== VISUALIZATION ====================
def create_crypto_winter_visualization(
    results_df: pd.DataFrame, crypto_prices: pd.DataFrame, phase_info: Dict, output_dir: Path
):
    """Create comprehensive visualization of the 2022 Crypto Winter."""
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    # Ensure date columns are datetime
    results_df["date"] = pd.to_datetime(results_df["date"])
    if not crypto_prices.empty:
        crypto_prices["date"] = pd.to_datetime(crypto_prices["date"])

    # Plot 1: Crypto Prices (BTC and ETH)
    if not crypto_prices.empty:
        for symbol in ["BTC-USD", "ETH-USD"]:
            symbol_data = crypto_prices[crypto_prices["symbol"] == symbol]
            if not symbol_data.empty:
                # Normalize to percentage of first value
                first_price = symbol_data["close"].iloc[0]
                pct_change = ((symbol_data["close"] / first_price) - 1) * 100
                axes[0].plot(
                    symbol_data["date"],
                    pct_change,
                    label=symbol.replace("-USD", ""),
                    linewidth=2,
                )

        axes[0].set_ylabel("Price Change (%)", fontsize=11)
        axes[0].set_title(
            f"{phase_info['name']}: Crypto Price Collapse",
            fontsize=13,
            fontweight="bold",
        )
        axes[0].legend(loc="best")
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(y=0, color="black", linestyle="--", alpha=0.5)

    # Plot 2: Cross-Asset Sentiment
    axes[1].plot(
        results_df["date"],
        results_df["crypto_sentiment"],
        label="Crypto",
        linewidth=2,
        color="#f7931a",
    )
    axes[1].plot(
        results_df["date"],
        results_df["equity_sentiment"],
        label="Equity",
        linewidth=2,
        color="#627EEA",
    )
    axes[1].axhline(y=0, color="black", linestyle="--", alpha=0.5)
    axes[1].set_ylabel("Sentiment", fontsize=11)
    axes[1].set_title("Cross-Asset Sentiment Divergence", fontsize=12)
    axes[1].legend(loc="best")
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Regime Detection
    regime_colors = {"risk_on": "#2ecc71", "risk_off": "#e74c3c", "transition": "#f39c12"}
    for regime, color in regime_colors.items():
        mask = results_df["regime"] == regime
        axes[2].scatter(
            results_df.loc[mask, "date"],
            results_df.loc[mask, "confidence"],
            label=regime.replace("_", " ").title(),
            color=color,
            alpha=0.6,
            s=50,
        )
    axes[2].set_ylabel("Confidence", fontsize=11)
    axes[2].set_title("Regime Detection Results", fontsize=12)
    axes[2].legend(loc="best")
    axes[2].grid(True, alpha=0.3)

    # Plot 4: VIX (if available)
    if "vix_level" in results_df.columns and results_df["vix_level"].notna().any():
        axes[3].plot(
            results_df["date"],
            results_df["vix_level"],
            label="VIX",
            linewidth=2,
            color="#e74c3c",
        )
        axes[3].axhline(y=20, color="orange", linestyle="--", alpha=0.5, label="VIX 20")
        axes[3].axhline(y=30, color="red", linestyle="--", alpha=0.5, label="VIX 30")
        axes[3].set_ylabel("VIX Level", fontsize=11)
        axes[3].set_title("Traditional Risk Indicator (VIX)", fontsize=12)
        axes[3].legend(loc="best")
        axes[3].grid(True, alpha=0.3)

    # Mark peak date on all plots
    peak_date = pd.to_datetime(phase_info["peak_date"])
    for ax in axes:
        ax.axvline(x=peak_date, color="red", linestyle="--", alpha=0.7, linewidth=2)
        ax.text(
            peak_date,
            ax.get_ylim()[1] * 0.95,
            "Peak",
            rotation=90,
            verticalalignment="top",
            fontsize=9,
        )

    plt.xlabel("Date", fontsize=11)
    plt.tight_layout()

    # Save figure
    output_file = output_dir / f"crypto_winter_{phase_info['start_date'][:7]}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"✅ Saved visualization: {output_file}")
    plt.close()


# ==================== MAIN ====================
def main():
    """Run 2022 Crypto Winter backtest analysis."""
    print("=" * 70)
    print("2022 CRYPTO WINTER BACKTEST")
    print("Multi-Phase Crisis Analysis: Luna/Terra + Celsius/3AC")
    print("=" * 70)

    # Create output directory
    output_dir = Path("results/crypto_winter_2022")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load ML classifier
    print("\n📊 Loading ML classifier...")
    classifier = MLRegimeClassifier(model_type="best")

    # Analyze each phase
    all_results = {}

    for phase_key, phase_info in PHASES.items():
        print(f"\n{'='*70}")
        print(f"Analyzing: {phase_info['name']}")
        print(f"Period: {phase_info['start_date']} to {phase_info['end_date']}")
        print(f"{'='*70}")

        # Load data
        print("Loading data...")
        sentiment_df = load_sentiment_data(
            phase_info["start_date"], phase_info["end_date"]
        )
        vix_df = load_vix_data(phase_info["start_date"], phase_info["end_date"])
        ciss_df = load_ciss_data(phase_info["start_date"], phase_info["end_date"])
        crypto_prices = load_crypto_prices(
            phase_info["start_date"], phase_info["end_date"]
        )

        print(f"  Sentiment records: {len(sentiment_df)}")
        print(f"  VIX records: {len(vix_df)}")
        print(f"  Crypto price records: {len(crypto_prices)}")

        # Prepare features
        print("Preparing features...")
        features_df = prepare_ml_features(sentiment_df, ciss_df, vix_df)
        print(f"  Feature matrix: {features_df.shape}")

        # Run regime detection
        print("Running regime detection...")
        results_df = run_regime_detection(features_df, classifier)

        # Calculate metrics
        print("Calculating metrics...")
        metrics = evaluate_detection_accuracy(results_df, phase_info)
        contagion = analyze_contagion_patterns(sentiment_df)
        lead_lag = calculate_sentiment_vs_vix_lead_lag(results_df)

        # Print summary
        print(f"\n📈 Results Summary:")
        print(f"  Risk-Off Detection: {metrics['risk_off_pct']:.1f}% of period")
        print(f"  Peak Risk-Off: {metrics['peak_risk_off_pct']:.1f}% around peak")
        print(f"  Early Warning: {metrics['early_warning']} ({metrics['days_before_peak']} days before peak)")
        print(f"  Crypto-Equity Divergence: {metrics['crypto_equity_divergence']:.3f}")
        print(f"  Average Confidence: {metrics['avg_confidence']:.2f}")
        print(f"  Average Crypto Sentiment: {metrics['avg_crypto_sentiment']:.3f}")
        if metrics['avg_vix']:
            print(f"  Average VIX: {metrics['avg_vix']:.1f}")

        # Create visualization
        print("Creating visualization...")
        create_crypto_winter_visualization(
            results_df, crypto_prices, phase_info, output_dir
        )

        # Store results
        all_results[phase_key] = {
            "phase_info": phase_info,
            "metrics": metrics,
            "contagion_analysis": contagion,
            "lead_lag_analysis": lead_lag,
            "results_df": results_df.to_dict("records"),
        }

    # Save comprehensive results
    output_file = output_dir / "crypto_winter_backtest_results.json"

    # Use simple JSON string conversion
    print("\n💾 Saving results...")
    for phase_key, phase_data in all_results.items():
        phase_output = output_dir / f"{phase_key}_results.json"
        simple_results = {
            "phase_info": phase_data["phase_info"],
            "metrics": {
                k: (float(v) if isinstance(v, (np.floating, float)) else
                    int(v) if isinstance(v, (np.integer, int)) else
                    bool(v) if isinstance(v, (np.bool_, bool)) else
                    str(v))
                for k, v in phase_data["metrics"].items()
            },
            "results_summary": {
                "total_days": len(phase_data["results_df"]),
                "regime_distribution": {
                    k: int(v) for k, v in pd.DataFrame(phase_data["results_df"])["regime"].value_counts().to_dict().items()
                },
            }
        }
        with open(phase_output, "w") as f:
            json.dump(simple_results, f, indent=2)
        print(f"  ✅ Saved: {phase_output}")

    # Save individual CSV files for detailed results
    for phase_key, phase_data in all_results.items():
        csv_output = output_dir / f"{phase_key}_daily_results.csv"
        pd.DataFrame(phase_data["results_df"]).to_csv(csv_output, index=False)
        print(f"  ✅ Saved: {csv_output}")

    print(f"\n✅ Saved results: {output_file}")
    print("\n" + "=" * 70)
    print("2022 CRYPTO WINTER BACKTEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
