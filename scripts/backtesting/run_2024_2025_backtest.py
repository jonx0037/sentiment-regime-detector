#!/usr/bin/env python3
"""
2024-2026 Out-of-Sample Validation Backtest

Tests the regime classifier on recent, unseen data to demonstrate model robustness.
"""

import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.sentiment_detector.services.regime_classifier import (
    MLRegimeClassifier,
    SentimentFeatures,
)


# Period definitions
PERIODS = {
    "2024_full": {
        "name": "2024 Full Year",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "description": "Bitcoin ETF approval, AI boom",
    },
    "2025_recent": {
        "name": "2025-2026 Recent",
        "start_date": "2025-01-01",
        "end_date": "2026-02-05",
        "description": "Most recent period",
    },
    "full_period": {
        "name": "Full 2024-2026",
        "start_date": "2024-01-01",
        "end_date": "2026-02-05",
        "description": "Complete out-of-sample period",
    },
}


def load_sentiment_data(start_date, end_date):
    csv_path = Path("scripts/hpc/hpc_data/sentiment_daily_by_asset.csv")
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.rename(columns={"sentiment": "mean_compound", "count": "text_count"})
    if "std_compound" not in df.columns:
        df["std_compound"] = 0.1
    return df


def load_vix_data(start_date, end_date):
    csv_path = Path("scripts/hpc/hpc_data/vix_data.csv")
    if not csv_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_ciss_data(start_date, end_date):
    csv_path = Path("scripts/hpc/hpc_data/ciss_data.csv")
    if not csv_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def prepare_ml_features(sentiment_df, ciss_df, vix_df):
    sentiment_pivot = sentiment_df.pivot_table(
        index="date", columns="asset_class", values="mean_compound", aggfunc="mean"
    )
    features = pd.DataFrame(index=sentiment_pivot.index)
    
    for asset_class in ["equity", "crypto", "forex", "commodity"]:
        if asset_class in sentiment_pivot.columns:
            features[f"{asset_class}_sentiment"] = sentiment_pivot[asset_class]
        else:
            features[f"{asset_class}_sentiment"] = 0.0
    
    asset_cols = ["equity_sentiment", "crypto_sentiment", "forex_sentiment", "commodity_sentiment"]
    features["sentiment_mean"] = features[asset_cols].mean(axis=1)
    features["sentiment_std"] = features[asset_cols].std(axis=1)
    features["sentiment_momentum"] = features["sentiment_mean"].diff(7)
    features["sentiment_acceleration"] = features["sentiment_momentum"].diff(7)
    features["max_divergence"] = features[asset_cols].max(axis=1) - features[asset_cols].min(axis=1)
    
    if not vix_df.empty:
        features = features.join(vix_df[["close"]], how="left")
        features = features.rename(columns={"close": "vix_level"})
        features["vix_level"] = features["vix_level"].ffill()
    
    if not ciss_df.empty:
        features = features.join(ciss_df[["value"]], how="left")
        features = features.rename(columns={"value": "ciss_level"})
        features["ciss_level"] = features["ciss_level"].ffill()
    
    features = features.ffill().fillna(0)
    return features


def run_regime_detection(features_df, classifier):
    results = []
    for date, row in features_df.iterrows():
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
        classification = classifier.classify(sentiment_features)
        results.append({
            "date": date,
            "regime": classification.state.value,
            "confidence": classification.confidence,
            "prob_risk_on": classification.prob_risk_on,
            "prob_risk_off": classification.prob_risk_off,
            "prob_transition": classification.prob_transition,
            "crypto_sentiment": row["crypto_sentiment"],
            "equity_sentiment": row["equity_sentiment"],
            "vix_level": row.get("vix_level"),
        })
    return pd.DataFrame(results)


def create_visualization(results_df, period_info, output_dir):
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    results_df["date"] = pd.to_datetime(results_df["date"])
    
    # Plot 1: Cross-Asset Sentiment
    axes[0].plot(results_df["date"], results_df["crypto_sentiment"], label="Crypto", linewidth=2, color="#f7931a")
    axes[0].plot(results_df["date"], results_df["equity_sentiment"], label="Equity", linewidth=2, color="#627EEA")
    axes[0].axhline(y=0, color="black", linestyle="--", alpha=0.5)
    axes[0].set_ylabel("Sentiment", fontsize=11)
    axes[0].set_title(f"{period_info['name']}: Cross-Asset Sentiment", fontsize=13, fontweight="bold")
    axes[0].legend(loc="best")
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Regime Detection
    regime_colors = {"risk_on": "#2ecc71", "risk_off": "#e74c3c", "transition": "#f39c12"}
    for regime, color in regime_colors.items():
        mask = results_df["regime"] == regime
        axes[1].scatter(results_df.loc[mask, "date"], results_df.loc[mask, "confidence"], 
                       label=regime.replace("_", " ").title(), color=color, alpha=0.6, s=50)
    axes[1].set_ylabel("Confidence", fontsize=11)
    axes[1].set_title("Out-of-Sample Regime Detection", fontsize=12)
    axes[1].legend(loc="best")
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Regime Probabilities
    axes[2].fill_between(results_df["date"], 0, results_df["prob_risk_on"], label="Risk-On", color="#2ecc71", alpha=0.5)
    axes[2].fill_between(results_df["date"], results_df["prob_risk_on"], 
                        results_df["prob_risk_on"] + results_df["prob_transition"], 
                        label="Transition", color="#f39c12", alpha=0.5)
    axes[2].fill_between(results_df["date"], results_df["prob_risk_on"] + results_df["prob_transition"], 
                        1.0, label="Risk-Off", color="#e74c3c", alpha=0.5)
    axes[2].set_ylabel("Probability", fontsize=11)
    axes[2].set_ylim(0, 1)
    axes[2].set_title("Regime Probability Distribution", fontsize=12)
    axes[2].legend(loc="best")
    axes[2].grid(True, alpha=0.3, axis="x")
    
    # Plot 4: VIX
    if "vix_level" in results_df.columns and results_df["vix_level"].notna().any():
        axes[3].plot(results_df["date"], results_df["vix_level"], label="VIX", linewidth=2, color="#e74c3c")
        axes[3].axhline(y=20, color="orange", linestyle="--", alpha=0.5, label="VIX 20")
        axes[3].axhline(y=30, color="red", linestyle="--", alpha=0.5, label="VIX 30")
        axes[3].set_ylabel("VIX Level", fontsize=11)
        axes[3].set_title("Traditional Risk Indicator (VIX)", fontsize=12)
        axes[3].legend(loc="best")
        axes[3].grid(True, alpha=0.3)
    
    plt.xlabel("Date", fontsize=11)
    plt.tight_layout()
    
    output_file = output_dir / f"out_of_sample_{period_info['start_date'][:4]}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"✅ Saved visualization: {output_file}")
    plt.close()


def main():
    print("=" * 70)
    print("2024-2026 OUT-OF-SAMPLE VALIDATION BACKTEST")
    print("=" * 70)
    
    output_dir = Path("results/out_of_sample_2024_2026")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nLoading ML classifier...")
    classifier = MLRegimeClassifier(model_type="best")
    
    for period_key, period_info in PERIODS.items():
        print(f"\n{'='*70}")
        print(f"Analyzing: {period_info['name']}")
        print(f"Period: {period_info['start_date']} to {period_info['end_date']}")
        print(f"{'='*70}")
        
        sentiment_df = load_sentiment_data(period_info["start_date"], period_info["end_date"])
        vix_df = load_vix_data(period_info["start_date"], period_info["end_date"])
        ciss_df = load_ciss_data(period_info["start_date"], period_info["end_date"])
        
        print(f"Sentiment records: {len(sentiment_df)}")
        print(f"VIX records: {len(vix_df)}")
        
        features_df = prepare_ml_features(sentiment_df, ciss_df, vix_df)
        print(f"Feature matrix: {features_df.shape}")
        
        results_df = run_regime_detection(features_df, classifier)
        
        regime_counts = results_df["regime"].value_counts()
        total_days = len(results_df)
        print(f"\nRegime Distribution:")
        for regime, count in regime_counts.items():
            print(f"  {regime}: {count/total_days*100:.1f}% ({count} days)")
        print(f"Average Confidence: {results_df['confidence'].mean():.2f}")
        
        create_visualization(results_df, period_info, output_dir)
        
        csv_file = output_dir / f"{period_key}_daily_results.csv"
        results_df.to_csv(csv_file, index=False)
        print(f"✅ Saved: {csv_file}")
    
    print("\n" + "=" * 70)
    print("OUT-OF-SAMPLE VALIDATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
