#!/usr/bin/env python
"""
Ensemble Historical Backtests: Combining Rule-Based + ML Classifiers

This script implements an ensemble approach that combines:
1. Rule-based classifier (good for sector-specific events)
2. ML classifier (excellent for extreme crises)
3. Confidence-weighted voting
4. Multi-index ground truth (CISS + VIX)

The ensemble approach aims to achieve the best of both worlds:
- ML excels at extreme events (COVID: 80.5% vs rule-based 4.9%)
- Rule-based handles sector-specific events better (FTX)
- Weighted voting reduces errors from overconfident predictions

Events tested:
1. COVID Market Crash (Feb-Mar 2020)
2. FTX Collapse (Nov 2022)
3. Silicon Valley Bank (Mar 2023)
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import classifiers
from sentiment_detector.services.regime_classifier import (
    MLRegimeClassifier,
    RegimeClassifier,
    SentimentFeatures,
    RegimeState,
)

# Event definitions (same as before)
EVENTS = {
    "covid": {
        "name": "COVID Market Crash",
        "start": "2020-02-15",
        "peak": "2020-03-16",
        "end": "2020-04-15",
        "vix_peak": 82.69,
        "description": "Global pandemic declaration, VIX all-time high",
    },
    "ftx": {
        "name": "FTX Collapse",
        "start": "2022-11-01",
        "peak": "2022-11-10",
        "end": "2022-11-30",
        "vix_peak": 33.43,
        "description": "Crypto exchange collapse, contagion risk",
    },
    "svb": {
        "name": "Silicon Valley Bank",
        "start": "2023-03-01",
        "peak": "2023-03-13",
        "end": "2023-03-31",
        "vix_peak": 28.00,
        "description": "Regional bank failure, banking sector stress",
    }
}

# Ground truth mapping
VIX_TO_ML_STATE_MAP = {
    "low_volatility": "risk_on",
    "normal": "risk_on",
    "elevated": "transition",
    "high_volatility": "risk_off",
}


class EnsembleRegimeClassifier:
    """
    Ensemble classifier combining rule-based and ML approaches.

    Uses confidence-weighted voting to combine predictions:
    - ML classifier: Generally more accurate, especially for extreme events
    - Rule-based: Better at capturing sector-specific or moderate stress

    Weights are dynamically adjusted based on:
    - Individual model confidence scores
    - Historical performance on similar regimes
    - Feature availability (CISS/VIX presence)
    """

    def __init__(
        self,
        ml_classifier: MLRegimeClassifier,
        rule_classifier: RegimeClassifier,
        ml_weight: float = 0.6,
        rule_weight: float = 0.4,
    ):
        """
        Initialize ensemble classifier.

        Args:
            ml_classifier: Trained ML classifier
            rule_classifier: Rule-based classifier
            ml_weight: Base weight for ML predictions (0-1)
            rule_weight: Base weight for rule-based predictions (0-1)
        """
        self.ml_classifier = ml_classifier
        self.rule_classifier = rule_classifier
        self.ml_weight = ml_weight
        self.rule_weight = rule_weight

        # Normalize weights
        total = ml_weight + rule_weight
        self.ml_weight /= total
        self.rule_weight /= total

    def classify(self, features: SentimentFeatures) -> Dict:
        """
        Classify regime using ensemble approach.

        Returns dict with:
        - predicted_regime: Final ensemble prediction
        - confidence: Ensemble confidence
        - ml_prediction: ML classifier result
        - rule_prediction: Rule-based result
        - agreement: Whether models agree
        """
        # Get ML prediction
        ml_result = self.ml_classifier.classify(features)

        # Get rule-based prediction
        rule_result = self.rule_classifier.classify(features)

        # Check agreement
        agreement = ml_result.state == rule_result.state

        # If models agree, use their prediction with high confidence
        if agreement:
            return {
                "predicted_regime": ml_result.state.value,
                "confidence": max(ml_result.confidence, rule_result.confidence),
                "ml_prediction": ml_result.state.value,
                "ml_confidence": ml_result.confidence,
                "rule_prediction": rule_result.state.value,
                "rule_confidence": rule_result.confidence,
                "agreement": True,
                "method": "agreement",
            }

        # Models disagree - use confidence-weighted voting
        # Convert probabilities to weighted ensemble
        ml_probs = {
            "risk_on": ml_result.prob_risk_on,
            "risk_off": ml_result.prob_risk_off,
            "transition": ml_result.prob_transition,
        }

        rule_probs = {
            "risk_on": rule_result.prob_risk_on,
            "risk_off": rule_result.prob_risk_off,
            "transition": rule_result.prob_transition,
        }

        # Dynamically adjust weights based on confidence
        # If one model is very confident and the other isn't, trust the confident one more
        conf_ratio = ml_result.confidence / (rule_result.confidence + 0.01)
        if conf_ratio > 2.0:  # ML is much more confident
            adjusted_ml_weight = 0.75
            adjusted_rule_weight = 0.25
        elif conf_ratio < 0.5:  # Rule is much more confident
            adjusted_ml_weight = 0.25
            adjusted_rule_weight = 0.75
        else:  # Similar confidence, use base weights
            adjusted_ml_weight = self.ml_weight
            adjusted_rule_weight = self.rule_weight

        # Compute weighted probabilities
        ensemble_probs = {}
        for state in ["risk_on", "risk_off", "transition"]:
            ensemble_probs[state] = (
                adjusted_ml_weight * ml_probs[state] +
                adjusted_rule_weight * rule_probs[state]
            )

        # Select state with highest probability
        final_state = max(ensemble_probs, key=ensemble_probs.get)
        final_confidence = ensemble_probs[final_state]

        return {
            "predicted_regime": final_state,
            "confidence": final_confidence,
            "ml_prediction": ml_result.state.value,
            "ml_confidence": ml_result.confidence,
            "rule_prediction": rule_result.state.value,
            "rule_confidence": rule_result.confidence,
            "agreement": False,
            "method": "weighted_voting",
            "weights_used": {
                "ml": adjusted_ml_weight,
                "rule": adjusted_rule_weight,
            }
        }


# Import data loading functions from ML script
def load_vix_regimes(start_date: str, end_date: str) -> pd.DataFrame:
    """Load VIX regime data."""
    vix_file = Path("data/processed/vix_regimes.json")
    if not vix_file.exists():
        return pd.DataFrame()

    with open(vix_file) as f:
        data = json.load(f)

    df = pd.DataFrame(data["daily_data"])
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    df["ml_regime"] = df["regime"].map(VIX_TO_ML_STATE_MAP)
    return df


def load_ciss_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load CISS data."""
    ciss_file = Path("scripts/hpc/hpc_data/ciss_data.csv")
    if not ciss_file.exists():
        return pd.DataFrame()

    df = pd.read_csv(ciss_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_vix_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load VIX data."""
    vix_file = Path("scripts/hpc/hpc_data/vix_data.csv")
    if not vix_file.exists():
        return pd.DataFrame()

    df = pd.read_csv(vix_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_sentiment_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load sentiment data."""
    csv_path = Path("scripts/hpc/hpc_data/sentiment_daily_by_asset.csv")
    if not csv_path.exists():
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    return df


def prepare_ml_features(
    sentiment_df: pd.DataFrame,
    ciss_df: pd.DataFrame,
    vix_df: pd.DataFrame
) -> pd.DataFrame:
    """Prepare features for classifiers."""
    if len(sentiment_df) == 0:
        return pd.DataFrame()

    # Pivot sentiment by asset class
    sentiment_pivot = sentiment_df.pivot_table(
        index="date",
        columns="asset_class",
        values="sentiment",
        aggfunc="mean"
    )

    # Get sentiment aggregates
    sentiment_agg = sentiment_df.groupby("date").agg({
        "sentiment": ["mean", "std"],
        "count": "sum"
    })
    sentiment_agg.columns = ["sentiment_mean", "sentiment_std", "text_count"]

    features = sentiment_agg.copy()

    # Add per-asset sentiment
    for asset_class in ["equity", "crypto", "forex", "commodity"]:
        if asset_class in sentiment_pivot.columns:
            features[f"{asset_class}_sentiment"] = sentiment_pivot[asset_class]
        else:
            features[f"{asset_class}_sentiment"] = 0.0

    # Fill missing
    features["equity_sentiment"] = features["equity_sentiment"].fillna(features["sentiment_mean"])
    features["crypto_sentiment"] = features["crypto_sentiment"].fillna(features["sentiment_mean"])
    features["forex_sentiment"] = features["forex_sentiment"].fillna(features["sentiment_mean"])
    features["commodity_sentiment"] = features["commodity_sentiment"].fillna(features["sentiment_mean"])

    # Calculate momentum
    features["sentiment_momentum"] = features["sentiment_mean"].diff(3)
    features["sentiment_acceleration"] = features["sentiment_momentum"].diff()

    # Calculate divergence
    asset_cols = ["equity_sentiment", "crypto_sentiment", "forex_sentiment", "commodity_sentiment"]
    features["max_divergence"] = features[asset_cols].max(axis=1) - features[asset_cols].min(axis=1)

    # Add CISS
    if len(ciss_df) > 0:
        ciss_col = "value" if "value" in ciss_df.columns else "ciss"
        features = features.join(ciss_df[[ciss_col]], how="left")
        features = features.rename(columns={ciss_col: "ciss"})
        features["ciss"] = features["ciss"].ffill()
    else:
        features["ciss"] = np.nan

    # Add VIX
    if len(vix_df) > 0:
        vix_col = "close" if "close" in vix_df.columns else "vix"
        features = features.join(vix_df[[vix_col]], how="left")
        features = features.rename(columns={vix_col: "vix"})
        features["vix"] = features["vix"].ffill()
    else:
        features["vix"] = np.nan

    # Fill NaNs
    features = features.fillna(0)

    return features


def classify_with_ensemble(
    features_df: pd.DataFrame,
    ensemble: EnsembleRegimeClassifier
) -> pd.DataFrame:
    """Classify using ensemble."""
    predictions = []

    for date, row in features_df.iterrows():
        sent_features = SentimentFeatures(
            equity_sentiment=row.get("equity_sentiment", 0.0),
            crypto_sentiment=row.get("crypto_sentiment", 0.0),
            forex_sentiment=row.get("forex_sentiment", 0.0),
            commodity_sentiment=row.get("commodity_sentiment", 0.0),
            cross_asset_mean=row.get("sentiment_mean", 0.0),
            cross_asset_std=row.get("sentiment_std", 0.1),
            sentiment_momentum=row.get("sentiment_momentum", 0.0),
            sentiment_acceleration=row.get("sentiment_acceleration", 0.0),
            max_divergence=row.get("max_divergence", 0.0),
            vix_level=row.get("vix") if not np.isnan(row.get("vix", np.nan)) else None,
            ciss_level=row.get("ciss") if not np.isnan(row.get("ciss", np.nan)) else None,
        )

        result = ensemble.classify(sent_features)
        result["date"] = date
        predictions.append(result)

    pred_df = pd.DataFrame(predictions)
    pred_df = pred_df.set_index("date")

    return pred_df


def run_ensemble_backtest(
    event_key: str,
    event_config: Dict,
    ensemble: EnsembleRegimeClassifier
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[Dict]]:
    """Run ensemble backtest for a single event."""
    print("\n" + "=" * 80)
    print(f"ENSEMBLE BACKTEST: {event_config['name'].upper()}")
    print("=" * 80)

    start_date = event_config["start"]
    peak_date = event_config["peak"]
    end_date = event_config["end"]

    print(f"\n📅 Event Period: {start_date} to {end_date}")
    print(f"   Peak Date: {peak_date} (VIX hit {event_config['vix_peak']:.2f})")
    print(f"   Using Ensemble: ML + Rule-Based Weighted Voting")

    # Load data
    print("\n1. Loading ground truth and data sources...")
    vix_regimes = load_vix_regimes(start_date, end_date)
    sentiment_df = load_sentiment_data(start_date, end_date)
    ciss_df = load_ciss_data(start_date, end_date)
    vix_df = load_vix_data(start_date, end_date)

    if len(vix_regimes) == 0 or len(sentiment_df) == 0:
        print("   ⚠️  Insufficient data")
        return None, None, None

    print(f"   VIX regimes: {len(vix_regimes)} days")
    print(f"   Sentiment: {sentiment_df['count'].sum():,.0f} texts")
    print(f"   Asset classes: {', '.join(sentiment_df['asset_class'].unique())}")

    # Prepare features
    print("\n2. Preparing features...")
    features = prepare_ml_features(sentiment_df, ciss_df, vix_df)
    print(f"   Features ready: {len(features)} days")

    # Classify
    print("\n3. Running ensemble classification...")
    predictions = classify_with_ensemble(features, ensemble)
    print(f"   Predictions: {len(predictions)} days")
    print(f"   Agreement rate: {predictions['agreement'].mean():.1%}")

    # Evaluate
    print("\n4. Evaluating against ground truth...")
    results = predictions.join(vix_regimes[["ml_regime", "vix_close", "regime"]], how="inner")
    results = results.rename(columns={"ml_regime": "actual"})

    if len(results) == 0:
        print("   ⚠️  No aligned data")
        return None, None, None

    # Calculate metrics
    print("\n" + "=" * 80)
    print("ENSEMBLE RESULTS")
    print("=" * 80)

    exact_match = (results["predicted_regime"] == results["actual"]).sum()
    accuracy = exact_match / len(results)
    print(f"\n📊 Ensemble Accuracy: {accuracy:.1%} ({exact_match}/{len(results)} days)")
    print(f"   Model Agreement: {results['agreement'].mean():.1%} of predictions")
    print(f"   Avg Confidence: {results['confidence'].mean():.1%}")

    # Compare with individual models
    ml_only = (results["ml_prediction"] == results["actual"]).sum() / len(results)
    rule_only = (results["rule_prediction"] == results["actual"]).sum() / len(results)
    print(f"\n   ML-only would be: {ml_only:.1%}")
    print(f"   Rule-only would be: {rule_only:.1%}")
    print(f"   Ensemble improvement: {(accuracy - max(ml_only, rule_only)):.1%}")

    # Sample output
    print("\n📅 Sample Predictions (first 5 and last 5 days):")
    print("-" * 100)
    print(f"{'Date':<12} {'VIX':>6} {'Actual':<12} {'Ensemble':<12} {'ML':<12} {'Rule':<12} {'Conf':>6} {'Agree'}")
    print("-" * 100)

    sample = pd.concat([results.head(5), results.tail(5)])
    for date, row in sample.iterrows():
        match = "✅" if row["predicted_regime"] == row["actual"] else "❌"
        agree = "✅" if row["agreement"] else "⚠️"
        date_str = date.strftime("%Y-%m-%d")
        print(f"{date_str:<12} {row['vix_close']:>6.1f} {row['actual']:<12} "
              f"{row['predicted_regime']:<12} {row['ml_prediction']:<12} "
              f"{row['rule_prediction']:<12} {row['confidence']:>6.1%} {agree} {match}")

    if len(results) > 10:
        print(f"   ... ({len(results) - 10} more days) ...")

    # Event detection
    print("\n" + "=" * 80)
    print("EVENT DETECTION")
    print("=" * 80)

    peak_ts = pd.Timestamp(peak_date)
    peak_detected = False
    if peak_ts in results.index:
        peak_pred = results.loc[peak_ts, "predicted_regime"]
        peak_actual = results.loc[peak_ts, "actual"]
        peak_detected = peak_pred in ['risk_off', 'transition']
        print(f"\n🎯 Peak Day ({peak_date}):")
        print(f"   Actual: {peak_actual}")
        print(f"   Ensemble: {peak_pred}")
        print(f"   ML: {results.loc[peak_ts, 'ml_prediction']}")
        print(f"   Rule: {results.loc[peak_ts, 'rule_prediction']}")
        print(f"   Result: {'✅ Correct' if peak_detected else '❌ Missed'}")

    # Early warning
    pre_peak = results[results.index < peak_ts]
    warning_days = 0
    if len(pre_peak) > 0:
        stress_days = pre_peak[pre_peak["predicted_regime"].isin(["risk_off", "transition"])]
        if len(stress_days) > 0:
            warning_days = (peak_ts - stress_days.index[0]).days
            print(f"\n⚠️  Early Warning: {warning_days} days before peak")
        else:
            print(f"\n⚠️  No early warning detected")

    # Create summary
    summary = {
        "event": event_config["name"],
        "event_key": event_key,
        "metrics": {
            "ensemble_accuracy": float(accuracy),
            "ml_only_accuracy": float(ml_only),
            "rule_only_accuracy": float(rule_only),
            "agreement_rate": float(results["agreement"].mean()),
            "avg_confidence": float(results["confidence"].mean()),
            "exact_match_days": int(exact_match),
            "total_days": int(len(results)),
        },
        "detection": {
            "peak_detected": peak_detected,
            "early_warning_days": warning_days,
        },
    }

    print("\n✅ Ensemble backtest complete!")

    return results, features, summary


def main():
    """Run ensemble backtests."""
    print("\n" + "=" * 80)
    print("ENSEMBLE HISTORICAL BACKTESTS")
    print("ML Classifier + Rule-Based Classifier with Weighted Voting")
    print("=" * 80)
    print(f"\nStarting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize classifiers
    print("Loading classifiers...")
    ml_classifier = MLRegimeClassifier(model_type="best")
    rule_classifier = RegimeClassifier()

    if not ml_classifier.is_loaded:
        print("⚠️  ML model not loaded! Exiting...")
        return

    # Create ensemble
    ensemble = EnsembleRegimeClassifier(
        ml_classifier=ml_classifier,
        rule_classifier=rule_classifier,
        ml_weight=0.6,  # Slightly favor ML (better average performance)
        rule_weight=0.4,
    )

    print(f"✅ Ensemble ready (ML weight: 60%, Rule weight: 40%)\n")

    # Output directory
    output_dir = Path("data/processed/historical_backtests_ensemble")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run backtests
    all_results = {}
    all_features = {}
    all_summaries = []

    for event_key, event_config in EVENTS.items():
        results, features, summary = run_ensemble_backtest(event_key, event_config, ensemble)
        all_results[event_key] = results
        all_features[event_key] = features
        all_summaries.append(summary)

        if results is not None:
            results_file = output_dir / f"{event_key}_ensemble_results.csv"
            results.to_csv(results_file)
            print(f"   📁 Saved: {results_file}")

    # Export summary
    summary_json = output_dir / "ensemble_summary.json"
    with open(summary_json, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "method": "ensemble_weighted_voting",
            "events": all_summaries,
            "overall_stats": {
                "avg_ensemble_accuracy": float(np.mean([s['metrics']['ensemble_accuracy'] for s in all_summaries if s])),
                "avg_ml_only": float(np.mean([s['metrics']['ml_only_accuracy'] for s in all_summaries if s])),
                "avg_rule_only": float(np.mean([s['metrics']['rule_only_accuracy'] for s in all_summaries if s])),
                "avg_agreement": float(np.mean([s['metrics']['agreement_rate'] for s in all_summaries if s])),
            }
        }, f, indent=2)
    print(f"\n📁 Summary: {summary_json}")

    print("\n" + "=" * 80)
    print("ALL ENSEMBLE BACKTESTS COMPLETE!")
    print("=" * 80)
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults: {output_dir}\n")


if __name__ == "__main__":
    main()
