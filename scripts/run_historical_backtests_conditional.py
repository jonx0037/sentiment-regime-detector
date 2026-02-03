#!/usr/bin/env python3
"""
Historical Backtest Script - Conditional Routing Approach

This script implements a conditional routing strategy that selects the best
classifier (ML, rule-based, or ensemble) based on event characteristics:
- Extreme systemic events (high VIX spike) → ML classifier
- Sector-specific events (low VIX, high divergence) → Rule-based classifier
- Mixed events → Ensemble classifier

Events tested:
1. COVID Market Crash (Feb-Mar 2020)
2. FTX Collapse (Nov 2022)
3. Silicon Valley Bank (Mar 2023)
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
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.sentiment_detector.services.regime_classifier import (
    MLRegimeClassifier,
    RegimeClassification,
    SentimentFeatures,
)


# ==================== EVENT DEFINITIONS ====================
EVENTS = {
    "covid": {
        "name": "COVID Market Crash",
        "start_date": "2020-02-01",
        "end_date": "2020-03-31",
        "peak_date": "2020-03-16",  # VIX reached 82.69
        "description": "Global pandemic triggers massive market selloff",
    },
    "ftx": {
        "name": "FTX Collapse",
        "start_date": "2022-11-01",
        "end_date": "2022-11-30",
        "peak_date": "2022-11-11",  # FTX bankruptcy filing
        "description": "Major crypto exchange collapse and contagion",
    },
    "svb": {
        "name": "Silicon Valley Bank",
        "start_date": "2023-03-01",
        "end_date": "2023-03-31",
        "peak_date": "2023-03-10",  # SVB collapse
        "description": "Regional bank failure sparks banking sector stress",
    },
}


# ==================== DATA LOADING ====================
def load_sentiment_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load sentiment data from CSV file for the specified period."""
    csv_path = Path("scripts/hpc/hpc_data/sentiment_daily_by_asset.csv")

    if not csv_path.exists():
        print(f"⚠️  Sentiment data file not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Rename columns to match expected format
    df = df.rename(
        columns={
            "sentiment": "mean_compound",
            "count": "text_count",
            "positive": "positive_count",
            "negative": "negative_count",
        }
    )

    # Add std_compound if not present
    if "std_compound" not in df.columns:
        df["std_compound"] = 0.1

    # Convert positive/negative from proportions to counts if needed
    if "positive_count" in df.columns and df["positive_count"].max() <= 1.0:
        df["positive_count"] = (df["positive_count"] * df["text_count"]).fillna(0).astype(int)
        df["negative_count"] = (df["negative_count"] * df["text_count"]).fillna(0).astype(int)

    return df


def load_ciss_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load CISS data from CSV file."""
    csv_path = Path("scripts/hpc/hpc_data/ciss_data.csv")

    if not csv_path.exists():
        print(f"⚠️  CISS data file not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


def load_vix_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Load VIX data from CSV file."""
    csv_path = Path("scripts/hpc/hpc_data/vix_data.csv")

    if not csv_path.exists():
        print(f"⚠️  VIX data file not found: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df = df.set_index("date")
    return df


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
    asset_cols = ["equity_sentiment", "crypto_sentiment", "forex_sentiment", "commodity_sentiment"]
    features["sentiment_mean"] = features[asset_cols].mean(axis=1)

    # Calculate momentum features
    features["sentiment_momentum"] = features["sentiment_mean"].diff(3)
    features["sentiment_acceleration"] = features["sentiment_momentum"].diff()

    # Calculate divergence
    features["max_divergence"] = features[asset_cols].max(axis=1) - features[asset_cols].min(axis=1)

    # Add CISS if available
    if len(ciss_df) > 0:
        ciss_col = "value" if "value" in ciss_df.columns else "ciss"
        features = features.join(ciss_df[[ciss_col]], how="left")
        features = features.rename(columns={ciss_col: "ciss"})
        features["ciss"] = features["ciss"].ffill()
    else:
        features["ciss"] = np.nan

    # Add VIX if available
    if len(vix_df) > 0:
        vix_col = "close" if "close" in vix_df.columns else "vix"
        features = features.join(vix_df[[vix_col]], how="left")
        features = features.rename(columns={vix_col: "vix"})
        features["vix"] = features["vix"].ffill()
    else:
        features["vix"] = np.nan

    # Fill any remaining NaNs
    features = features.fillna(0)

    return features


# ==================== CLASSIFIERS ====================
class RuleBasedRegimeClassifier:
    """Rule-based classifier using volume spikes and divergence."""

    def __init__(self):
        self.thresholds = {"high_volatility": 3.0, "elevated_volatility": 2.0, "high_divergence": 0.3}

    def classify(self, features: SentimentFeatures) -> Dict:
        """Classify regime based on rules."""
        # Use VIX if available, otherwise use divergence
        vix = features.vix_level if features.vix_level is not None else 20.0

        # Use divergence as primary signal
        divergence = features.max_divergence

        # Calculate momentum magnitude
        momentum_magnitude = abs(features.sentiment_momentum) if features.sentiment_momentum else 0.0

        # Decision logic combining VIX, divergence, and momentum
        if vix > 30 or momentum_magnitude > 0.15:
            state = "risk_off"
            confidence = 0.7
        elif vix > 20 or divergence > self.thresholds["high_divergence"]:
            state = "transition"
            confidence = 0.6
        elif divergence > 0.2:
            state = "transition"
            confidence = 0.55
        else:
            state = "risk_on"
            confidence = 0.5

        return {
            "state": state,
            "confidence": confidence,
            "probabilities": {
                "risk_on": 1.0 - confidence if state == "risk_on" else 0.2,
                "risk_off": confidence if state == "risk_off" else 0.2,
                "transition": confidence if state == "transition" else 0.2,
            },
            "vix": vix,
            "divergence": divergence,
            "momentum": momentum_magnitude,
        }


class EnsembleRegimeClassifier:
    """Ensemble classifier combining ML and rule-based."""

    def __init__(self, ml_classifier, rule_classifier, ml_weight=0.6, rule_weight=0.4):
        self.ml_classifier = ml_classifier
        self.rule_classifier = rule_classifier

        # Normalize weights
        total = ml_weight + rule_weight
        self.ml_weight = ml_weight / total
        self.rule_weight = rule_weight / total

    def classify(self, features: SentimentFeatures) -> Dict:
        """Classify using ensemble voting."""
        ml_result_raw = self.ml_classifier.classify(features)
        rule_result = self.rule_classifier.classify(features)

        # Normalize ML result (RegimeClassification -> dict)
        ml_result = ConditionalRoutingClassifier._normalize_result(ml_result_raw)

        # Check if models agree
        agreement = ml_result["state"] == rule_result["state"]

        if agreement:
            # Both agree - return the one with higher confidence
            if ml_result["confidence"] > rule_result["confidence"]:
                return {**ml_result, "agreement": True, "method": "ml"}
            else:
                return {**rule_result, "agreement": True, "method": "rule"}

        # Models disagree - use confidence-weighted voting
        ml_probs = ml_result.get("probabilities", {})
        rule_probs = rule_result.get("probabilities", {})

        # Adjust weights based on confidence ratio
        conf_ratio = ml_result["confidence"] / (rule_result["confidence"] + 0.01)

        if conf_ratio > 2.0:  # ML much more confident
            adjusted_ml_weight = 0.75
            adjusted_rule_weight = 0.25
        elif conf_ratio < 0.5:  # Rule more confident
            adjusted_ml_weight = 0.25
            adjusted_rule_weight = 0.75
        else:
            adjusted_ml_weight = self.ml_weight
            adjusted_rule_weight = self.rule_weight

        # Combine probabilities
        ensemble_probs = {}
        for state in ["risk_on", "risk_off", "transition"]:
            ml_prob = ml_probs.get(state, 0.33)
            rule_prob = rule_probs.get(state, 0.33)
            ensemble_probs[state] = adjusted_ml_weight * ml_prob + adjusted_rule_weight * rule_prob

        # Select state with highest probability
        final_state = max(ensemble_probs.items(), key=lambda x: x[1])[0]
        final_confidence = ensemble_probs[final_state]

        return {
            "state": final_state,
            "confidence": final_confidence,
            "probabilities": ensemble_probs,
            "agreement": False,
            "method": "ensemble",
            "ml_state": ml_result["state"],
            "rule_state": rule_result["state"],
        }


class ConditionalRoutingClassifier:
    """
    Conditional routing classifier that selects the best classifier
    based on event characteristics.
    """

    def __init__(self, ml_classifier, rule_classifier, ensemble_classifier):
        self.ml_classifier = ml_classifier
        self.rule_classifier = rule_classifier
        self.ensemble_classifier = ensemble_classifier

        # Routing thresholds
        self.EXTREME_VIX_THRESHOLD = 30.0  # VIX > 30 = extreme stress
        self.RAPID_VIX_SPIKE_THRESHOLD = 5.0  # VIX change > 5 points in 3 days
        self.HIGH_DIVERGENCE_THRESHOLD = 0.35  # High cross-asset divergence
        self.LOW_VIX_THRESHOLD = 25.0  # VIX < 25 = normal to moderate stress

    @staticmethod
    def _normalize_result(result) -> Dict:
        """Normalize result from ML (RegimeClassification) or rule-based (dict)."""
        if isinstance(result, RegimeClassification):
            # ML classifier returns RegimeClassification object
            return {
                "state": result.state.value,  # Convert enum to string
                "confidence": result.confidence,
                "probabilities": {
                    "risk_on": result.prob_risk_on,
                    "risk_off": result.prob_risk_off,
                    "transition": result.prob_transition,
                },
            }
        else:
            # Rule-based classifier returns dict
            return result

    def _analyze_event_characteristics(self, features_df: pd.DataFrame) -> Dict:
        """Analyze event characteristics to determine routing."""
        # Calculate VIX statistics
        vix_max = features_df["vix"].max()
        vix_mean = features_df["vix"].mean()
        vix_std = features_df["vix"].std()

        # Calculate VIX rate of change (3-day window)
        vix_change = features_df["vix"].diff(3).abs().max()

        # Calculate divergence statistics
        divergence_max = features_df["max_divergence"].max()
        divergence_mean = features_df["max_divergence"].mean()

        # Calculate sentiment volatility
        sentiment_std = features_df["sentiment_mean"].std()

        return {
            "vix_max": vix_max,
            "vix_mean": vix_mean,
            "vix_std": vix_std,
            "vix_change": vix_change,
            "divergence_max": divergence_max,
            "divergence_mean": divergence_mean,
            "sentiment_std": sentiment_std,
        }

    def _route_classifier(self, characteristics: Dict) -> str:
        """
        Determine which classifier to use based on event characteristics.

        Returns:
            "ml", "rule", or "ensemble"
        """
        vix_max = characteristics["vix_max"]
        vix_change = characteristics["vix_change"]
        divergence_max = characteristics["divergence_max"]

        # Route 1: Extreme systemic event → Use ML
        if vix_max > self.EXTREME_VIX_THRESHOLD and vix_change > self.RAPID_VIX_SPIKE_THRESHOLD:
            return "ml"

        # Route 2: Sector-specific event → Use rule-based
        if vix_max < self.LOW_VIX_THRESHOLD and divergence_max > self.HIGH_DIVERGENCE_THRESHOLD:
            return "rule"

        # Route 3: Mixed event → Use ensemble
        return "ensemble"

    def classify_event(self, features_df: pd.DataFrame) -> Tuple[str, Dict, List[Dict]]:
        """
        Classify entire event period using conditional routing.

        Returns:
            (routing_decision, characteristics, predictions_list)
        """
        # Analyze event characteristics
        characteristics = self._analyze_event_characteristics(features_df)

        # Determine routing
        routing_decision = self._route_classifier(characteristics)

        # Select classifier
        if routing_decision == "ml":
            classifier = self.ml_classifier
        elif routing_decision == "rule":
            classifier = self.rule_classifier
        else:
            classifier = self.ensemble_classifier

        # Make predictions for each day
        predictions = []
        for date, row in features_df.iterrows():
            # Calculate cross-asset std for this row
            asset_values = [
                row["equity_sentiment"],
                row["crypto_sentiment"],
                row["forex_sentiment"],
                row["commodity_sentiment"],
            ]
            cross_asset_std = np.std(asset_values)

            features = SentimentFeatures(
                equity_sentiment=row["equity_sentiment"],
                crypto_sentiment=row["crypto_sentiment"],
                forex_sentiment=row["forex_sentiment"],
                commodity_sentiment=row["commodity_sentiment"],
                cross_asset_mean=row["sentiment_mean"],
                cross_asset_std=cross_asset_std,
                sentiment_momentum=row.get("sentiment_momentum", 0.0),
                sentiment_acceleration=row.get("sentiment_acceleration", 0.0),
                max_divergence=row["max_divergence"],
                vix_level=row.get("vix", None),
                ciss_level=row.get("ciss", None),
            )

            result = classifier.classify(features)
            normalized_result = self._normalize_result(result)
            predictions.append(
                {
                    "date": date,
                    "predicted_state": normalized_result["state"],
                    "confidence": normalized_result["confidence"],
                    "vix": row.get("vix", np.nan),
                    "routing": routing_decision,
                }
            )

        return routing_decision, characteristics, predictions


# ==================== GROUND TRUTH GENERATION ====================
def generate_ground_truth(vix_series: pd.Series) -> pd.Series:
    """Generate ground truth labels from VIX levels."""
    labels = pd.Series(index=vix_series.index, dtype=str)

    for date, vix_value in vix_series.items():
        if vix_value < 20:
            labels[date] = "risk_on"
        elif vix_value < 30:
            labels[date] = "transition"
        else:
            labels[date] = "risk_off"

    return labels


# ==================== EVALUATION ====================
def evaluate_predictions(predictions_df: pd.DataFrame, peak_date: str) -> Dict:
    """Evaluate prediction accuracy and early warning."""
    # Calculate accuracy
    correct = (predictions_df["predicted_state"] == predictions_df["ground_truth"]).sum()
    total = len(predictions_df)
    accuracy = correct / total if total > 0 else 0.0

    # Check early warning
    peak_date_dt = pd.to_datetime(peak_date)
    risk_off_dates = predictions_df[predictions_df["predicted_state"] == "risk_off"].index

    peak_detected = False
    early_warning_days = 0

    if len(risk_off_dates) > 0:
        first_risk_off = risk_off_dates[0]
        if first_risk_off <= peak_date_dt:
            peak_detected = True
            early_warning_days = (peak_date_dt - first_risk_off).days

    # Calculate average confidence
    avg_confidence = predictions_df["confidence"].mean()

    return {
        "accuracy": accuracy,
        "correct_predictions": int(correct),
        "total_days": total,
        "peak_detected": peak_detected,
        "early_warning_days": int(early_warning_days),
        "avg_confidence": avg_confidence,
    }


# ==================== VISUALIZATION ====================
def create_visualization(results_df: pd.DataFrame, event_name: str, output_dir: Path, routing: str):
    """Create visualization of predictions vs ground truth."""
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Color mapping
    colors = {"risk_on": "green", "transition": "yellow", "risk_off": "red"}

    # Plot 1: Predictions vs Ground Truth
    ax1 = axes[0]
    for state in ["risk_on", "transition", "risk_off"]:
        pred_mask = results_df["predicted_state"] == state
        gt_mask = results_df["ground_truth"] == state

        ax1.scatter(
            results_df[pred_mask].index,
            [1] * pred_mask.sum(),
            c=colors[state],
            marker="o",
            s=100,
            label=f"Predicted {state}",
            alpha=0.7,
        )

        ax1.scatter(
            results_df[gt_mask].index,
            [0] * gt_mask.sum(),
            c=colors[state],
            marker="s",
            s=100,
            label=f"Actual {state}",
            alpha=0.7,
        )

    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(["Actual", "Predicted"])
    ax1.set_title(f"{event_name} - Regime Classification\n(Routing: {routing.upper()})")
    ax1.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    ax1.grid(True, alpha=0.3)

    # Plot 2: VIX
    ax2 = axes[1]
    ax2.plot(results_df.index, results_df["vix"], label="VIX", color="darkblue", linewidth=2)
    ax2.axhline(y=20, color="green", linestyle="--", label="VIX 20 (Risk On threshold)")
    ax2.axhline(y=30, color="red", linestyle="--", label="VIX 30 (Risk Off threshold)")
    ax2.set_ylabel("VIX Level")
    ax2.set_title("VIX Volatility Index")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Plot 3: Confidence
    ax3 = axes[2]
    ax3.plot(
        results_df.index,
        results_df["confidence"],
        label="Prediction Confidence",
        color="purple",
        linewidth=2,
    )
    ax3.set_ylabel("Confidence")
    ax3.set_xlabel("Date")
    ax3.set_title("Prediction Confidence Over Time")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / f"{event_name.lower().replace(' ', '_')}_conditional.png", dpi=300)
    plt.close()


# ==================== MAIN EXECUTION ====================
def run_backtest(event_key: str) -> Dict:
    """Run backtest for a single event using conditional routing."""
    event = EVENTS[event_key]
    print(f"\n{'='*60}")
    print(f"Testing: {event['name']}")
    print(f"Period: {event['start_date']} to {event['end_date']}")
    print(f"{'='*60}")

    # Load data
    print("Loading data...")
    sentiment_df = load_sentiment_data(event["start_date"], event["end_date"])
    ciss_df = load_ciss_data(event["start_date"], event["end_date"])
    vix_df = load_vix_data(event["start_date"], event["end_date"])

    if sentiment_df.empty:
        print("❌ No sentiment data available")
        return None

    # Prepare features
    print("Preparing features...")
    features_df = prepare_ml_features(sentiment_df, ciss_df, vix_df)

    # Generate ground truth
    ground_truth = generate_ground_truth(features_df["vix"])

    # Initialize classifiers
    print("Initializing classifiers...")
    ml_classifier = MLRegimeClassifier()
    rule_classifier = RuleBasedRegimeClassifier()
    ensemble_classifier = EnsembleRegimeClassifier(ml_classifier, rule_classifier)
    conditional_classifier = ConditionalRoutingClassifier(
        ml_classifier, rule_classifier, ensemble_classifier
    )

    # Classify event
    print("Running conditional routing...")
    routing_decision, characteristics, predictions = conditional_classifier.classify_event(features_df)

    print(f"\n📊 Event Characteristics:")
    print(f"   VIX Max: {characteristics['vix_max']:.2f}")
    print(f"   VIX Mean: {characteristics['vix_mean']:.2f}")
    print(f"   VIX Max Change (3d): {characteristics['vix_change']:.2f}")
    print(f"   Divergence Max: {characteristics['divergence_max']:.3f}")
    print(f"   Divergence Mean: {characteristics['divergence_mean']:.3f}")
    print(f"\n🎯 Routing Decision: {routing_decision.upper()}")

    # Create results dataframe
    results_df = pd.DataFrame(predictions)
    results_df = results_df.set_index("date")
    results_df["ground_truth"] = ground_truth

    # Evaluate
    metrics = evaluate_predictions(results_df, event["peak_date"])

    print(f"\n✅ Results:")
    print(f"   Accuracy: {metrics['accuracy']:.1%}")
    print(f"   Correct: {metrics['correct_predictions']}/{metrics['total_days']} days")
    print(f"   Peak Detected: {'Yes' if metrics['peak_detected'] else 'No'}")
    if metrics["peak_detected"]:
        print(f"   Early Warning: {metrics['early_warning_days']} days before peak")
    print(f"   Avg Confidence: {metrics['avg_confidence']:.1%}")

    # Save results
    output_dir = Path("data/processed/historical_backtests_conditional")
    output_dir.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(output_dir / f"{event_key}_conditional_results.csv")

    # Create visualization
    viz_dir = output_dir / "visualizations_conditional"
    viz_dir.mkdir(exist_ok=True)
    create_visualization(results_df, event["name"], viz_dir, routing_decision)

    return {
        "event": event["name"],
        "event_key": event_key,
        "routing_decision": routing_decision,
        "characteristics": characteristics,
        "metrics": metrics,
    }


def main():
    """Run all backtests and generate summary."""
    print("\n" + "=" * 60)
    print("HISTORICAL BACKTESTS - CONDITIONAL ROUTING APPROACH")
    print("=" * 60)

    results = []
    for event_key in ["covid", "ftx", "svb"]:
        result = run_backtest(event_key)
        if result:
            results.append(result)

    # Generate summary
    print("\n" + "=" * 60)
    print("SUMMARY - CONDITIONAL ROUTING")
    print("=" * 60)

    for result in results:
        print(f"\n{result['event']}:")
        print(f"  Routing: {result['routing_decision'].upper()}")
        print(f"  Accuracy: {result['metrics']['accuracy']:.1%}")
        print(f"  Peak Detected: {'Yes' if result['metrics']['peak_detected'] else 'No'}")
        if result["metrics"]["peak_detected"]:
            print(f"  Early Warning: {result['metrics']['early_warning_days']} days")

    # Calculate overall statistics
    accuracies = [r["metrics"]["accuracy"] for r in results]
    avg_accuracy = np.mean(accuracies)

    print(f"\nOverall Average Accuracy: {avg_accuracy:.1%}")

    # Save summary
    output_dir = Path("data/processed/historical_backtests_conditional")
    summary = {
        "generated_at": datetime.now().isoformat(),
        "method": "conditional_routing",
        "events": [
            {
                "event": r["event"],
                "event_key": r["event_key"],
                "routing_decision": r["routing_decision"],
                "characteristics": {k: float(v) for k, v in r["characteristics"].items()},
                "metrics": {
                    "accuracy": r["metrics"]["accuracy"],
                    "exact_match_days": r["metrics"]["correct_predictions"],
                    "total_days": r["metrics"]["total_days"],
                    "avg_confidence": r["metrics"]["avg_confidence"],
                },
                "detection": {
                    "peak_detected": r["metrics"]["peak_detected"],
                    "early_warning_days": r["metrics"]["early_warning_days"],
                },
            }
            for r in results
        ],
        "overall_stats": {"avg_accuracy": avg_accuracy, "routing_breakdown": {}},
    }

    # Calculate routing breakdown
    routing_counts = {}
    for r in results:
        routing = r["routing_decision"]
        routing_counts[routing] = routing_counts.get(routing, 0) + 1
    summary["overall_stats"]["routing_breakdown"] = routing_counts

    with open(output_dir / "conditional_routing_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ Results saved to: {output_dir}")
    print("\nRouting Breakdown:")
    for routing, count in routing_counts.items():
        print(f"  {routing.upper()}: {count} event(s)")


if __name__ == "__main__":
    main()
