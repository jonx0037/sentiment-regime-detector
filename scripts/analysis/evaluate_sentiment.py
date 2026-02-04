#!/usr/bin/env python3
"""
Evaluate sentiment predictions against VIX-derived regime ground truth.

This script:
1. Loads processed sentiment data
2. Loads VIX regime data
3. Aligns by date
4. Computes evaluation metrics

Per Dakalbab et al. (2024), evaluation uses:
- Directional Accuracy (DA)
- Matthews Correlation Coefficient (MCC)
- F1 Score
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.core.metrics import EvaluationMetrics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def vix_regime_to_sentiment(regime: str) -> str:
    """
    Map VIX regime to expected sentiment direction.
    
    Low volatility -> Positive/Bullish (calm markets)
    Normal -> Neutral
    Elevated/High -> Negative/Bearish (fear)
    """
    mapping = {
        "low_volatility": "POSITIVE",
        "normal": "NEUTRAL",
        "elevated": "NEGATIVE",
        "high_volatility": "NEGATIVE"
    }
    return mapping.get(regime, "NEUTRAL")


def aggregate_daily_sentiment(
    sentiment_results: list[dict]
) -> dict[str, dict]:
    """
    Aggregate sentiment predictions by date.
    
    Returns:
        Dict mapping date -> {label, confidence, count}
    """
    daily = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0, "confidences": []})
    
    for item in sentiment_results:
        # Parse date - look for created_at or date field
        date_str = item.get("created_at", item.get("date", ""))
        if not date_str:
            continue
        
        # Normalize date to YYYY-MM-DD
        try:
            if "T" in date_str:
                date_str = date_str.split("T")[0]
            date_key = date_str[:10]  # First 10 chars YYYY-MM-DD
        except:
            continue
        
        # Get sentiment - handle nested structure
        sentiment = item.get("sentiment", {})
        if isinstance(sentiment, dict):
            label = sentiment.get("label", "NEUTRAL").upper()
            confidence = sentiment.get("confidence", 0.5)
        else:
            label = "NEUTRAL"
            confidence = 0.5
        
        if "POSITIVE" in label:
            daily[date_key]["positive"] += 1
        elif "NEGATIVE" in label:
            daily[date_key]["negative"] += 1
        else:
            daily[date_key]["neutral"] += 1
        
        daily[date_key]["confidences"].append(confidence)
    
    # Determine majority label per day
    result = {}
    for date_key, counts in daily.items():
        total = counts["positive"] + counts["neutral"] + counts["negative"]
        if total == 0:
            continue
        
        # Majority voting
        if counts["positive"] > counts["negative"] and counts["positive"] > counts["neutral"]:
            label = "POSITIVE"
        elif counts["negative"] > counts["positive"] and counts["negative"] > counts["neutral"]:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        
        avg_conf = sum(counts["confidences"]) / len(counts["confidences"]) if counts["confidences"] else 0.5
        
        result[date_key] = {
            "label": label,
            "confidence": avg_conf,
            "count": total,
            "distribution": {
                "positive": counts["positive"],
                "neutral": counts["neutral"],
                "negative": counts["negative"]
            }
        }
    
    return result


def evaluate_sentiment_vs_vix(
    sentiment_path: Path,
    vix_path: Path,
    output_path: Path
) -> None:
    """
    Evaluate sentiment predictions against VIX regime ground truth.
    """
    logger.info(f"Loading sentiment data from {sentiment_path}")
    with open(sentiment_path) as f:
        sentiment_data = json.load(f)
    
    logger.info(f"Loading VIX data from {vix_path}")
    with open(vix_path) as f:
        vix_data = json.load(f)
    
    # Get daily VIX regimes
    vix_daily = {
        item["date"]: item["regime"]
        for item in vix_data.get("daily_data", [])
    }
    
    # Aggregate sentiment by day
    # Handle both 'results' and 'items' keys
    results = sentiment_data.get("results", sentiment_data.get("items", []))
    logger.info(f"Processing {len(results)} sentiment predictions")
    
    sentiment_daily = aggregate_daily_sentiment(results)
    logger.info(f"Aggregated to {len(sentiment_daily)} unique dates")
    
    # Find overlapping dates
    overlapping_dates = sorted(set(sentiment_daily.keys()) & set(vix_daily.keys()))
    logger.info(f"Found {len(overlapping_dates)} overlapping dates")
    
    if not overlapping_dates:
        logger.error("No overlapping dates found between sentiment and VIX data")
        return
    
    # Build aligned predictions and labels
    y_true = []  # VIX-derived expected sentiment
    y_pred = []  # Actual sentiment predictions
    confidences = []
    
    for date in overlapping_dates:
        vix_regime = vix_daily[date]
        expected_sentiment = vix_regime_to_sentiment(vix_regime)
        actual_sentiment = sentiment_daily[date]["label"]
        confidence = sentiment_daily[date]["confidence"]
        
        y_true.append(expected_sentiment)
        y_pred.append(actual_sentiment)
        confidences.append(confidence)
    
    # Calculate metrics
    logger.info("Calculating evaluation metrics...")
    
    metrics = EvaluationMetrics.evaluate_sentiment_model(
        y_true=y_true,
        y_pred=y_pred,
        confidences=confidences,
        label_names=["NEGATIVE", "NEUTRAL", "POSITIVE"]
    )
    
    # Add date range info
    metrics["evaluation_info"] = {
        "start_date": min(overlapping_dates),
        "end_date": max(overlapping_dates),
        "total_days": len(overlapping_dates),
        "sentiment_records": len(results),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    logger.info(f"Saved evaluation results to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SENTIMENT vs VIX REGIME EVALUATION")
    print("=" * 60)
    print(f"Date Range: {min(overlapping_dates)} to {max(overlapping_dates)}")
    print(f"Total Days Evaluated: {len(overlapping_dates)}")
    print(f"Sentiment Records: {len(results)}")
    
    print("\nClassification Metrics:")
    print(f"  Accuracy:     {metrics['classification']['accuracy']:.3f}")
    print(f"  Macro F1:     {metrics['classification']['macro_f1']:.3f}")
    print(f"  Weighted F1:  {metrics['classification']['weighted_f1']:.3f}")
    print(f"  MCC:          {metrics['classification']['mcc']:.3f}")
    
    print("\nDirectional Metrics:")
    print(f"  Directional Accuracy: {metrics['directional']['accuracy']:.3f}")
    print(f"  Up (Bullish) Precision:   {metrics['directional']['up_precision']:.3f}")
    print(f"  Down (Bearish) Precision: {metrics['directional']['down_precision']:.3f}")
    print(f"  Transition Accuracy:      {metrics['directional']['transition_accuracy']:.3f}")
    
    if "calibration" in metrics:
        print("\nCalibration Metrics:")
        print(f"  ECE:         {metrics['calibration']['ece']:.3f}")
        print(f"  MCE:         {metrics['calibration']['mce']:.3f}")
        print(f"  Brier Score: {metrics['calibration']['brier_score']:.3f}")
    
    print("\nPer-Class F1 Scores:")
    for label, f1 in metrics["classification"]["f1_score"].items():
        print(f"  {label}: {f1:.3f}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate sentiment predictions against VIX regimes"
    )
    parser.add_argument(
        "--sentiment",
        type=str,
        default="data/processed/kaggle_sentiment_full.json",
        help="Path to processed sentiment data"
    )
    parser.add_argument(
        "--vix",
        type=str,
        default="data/processed/vix_regimes.json",
        help="Path to VIX regime data"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/evaluation_results.json",
        help="Output path for evaluation results"
    )
    
    args = parser.parse_args()
    
    evaluate_sentiment_vs_vix(
        sentiment_path=Path(args.sentiment),
        vix_path=Path(args.vix),
        output_path=Path(args.output)
    )


if __name__ == "__main__":
    main()
