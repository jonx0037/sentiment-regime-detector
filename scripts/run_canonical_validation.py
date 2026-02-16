#!/usr/bin/env python3
"""Run canonical walk-forward + hypothesis validation and export report artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
)

from sentiment_detector.validation.hypothesis_validator import (
    HypothesisValidator,
    generate_hypothesis_report,
)
from sentiment_detector.validation.walk_forward_backtest import (
    WalkForwardBacktester,
    KEY_MARKET_EVENTS,
)


def _load_time_indexed_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" in df.columns:
        idx_col = "date"
    elif "Unnamed: 0" in df.columns:
        idx_col = "Unnamed: 0"
    else:
        idx_col = df.columns[0]
    df[idx_col] = pd.to_datetime(df[idx_col], errors="coerce")
    df = df.dropna(subset=[idx_col]).set_index(idx_col).sort_index()
    return df


def _sanitize_features(features: pd.DataFrame) -> pd.DataFrame:
    out = features.copy()
    out = out.replace([np.inf, -np.inf], np.nan)
    out = out.ffill().bfill().fillna(0)
    return out


def _aggregate_predictions(window_results: list[Any]) -> tuple[pd.Series, pd.Series]:
    if not window_results:
        return pd.Series(dtype="object"), pd.Series(dtype="object")
    pred_chunks = []
    true_chunks = []
    for wr in window_results:
        common = wr.predictions.index.intersection(wr.true_labels.index)
        pred_chunks.append(wr.predictions.loc[common])
        true_chunks.append(wr.true_labels.loc[common])
    y_pred = pd.concat(pred_chunks).sort_index()
    y_true = pd.concat(true_chunks).sort_index()
    common = y_true.index.intersection(y_pred.index)
    return y_true.loc[common], y_pred.loc[common]


def _transition_accuracy(y_true: pd.Series, y_pred: pd.Series) -> float:
    if len(y_true) < 2:
        return 0.0
    transitions = 0
    correct = 0
    true_vals = y_true.tolist()
    pred_vals = y_pred.tolist()
    for i in range(1, len(true_vals)):
        if true_vals[i] != true_vals[i - 1]:
            transitions += 1
            if pred_vals[i] == true_vals[i]:
                correct += 1
    return float(correct / transitions) if transitions > 0 else 0.0


def _add_compound_lags(features: pd.DataFrame, max_lag_days: int) -> tuple[pd.DataFrame, list[str]]:
    if max_lag_days <= 0 or "compound" not in features.columns:
        return features, []
    out = features.copy()
    added = []
    for lag in range(1, max_lag_days + 1):
        col = f"compound_lag_{lag}"
        out[col] = out["compound"].shift(lag)
        added.append(col)
    out = _sanitize_features(out)
    return out, added


def _warning_day_distribution(
    sentiment_series: pd.Series,
    vix_series: pd.Series,
    threshold: float,
    lead_window_days: int = 5,
) -> dict[str, Any]:
    sentiment, vix = sentiment_series.align(vix_series, join="inner")
    if len(sentiment) == 0:
        return {
            "threshold": threshold,
            "lead_window_days": lead_window_days,
            "total_spikes": 0,
            "matched_spikes": 0,
            "unmatched_spikes": 0,
            "warning_distribution": {},
            "avg_warning_days": 0.0,
        }

    spike_dates = set(vix[vix > threshold].index)
    total_spikes = len(spike_dates)
    if total_spikes == 0:
        return {
            "threshold": threshold,
            "lead_window_days": lead_window_days,
            "total_spikes": 0,
            "matched_spikes": 0,
            "unmatched_spikes": 0,
            "warning_distribution": {},
            "avg_warning_days": 0.0,
        }

    sentiment_drop = sentiment.diff() < -sentiment.std()
    lead_times: list[int] = []
    for drop_date in sentiment.index[sentiment_drop.fillna(False)]:
        for i in range(1, lead_window_days + 1):
            candidate = drop_date + timedelta(days=i)
            if candidate in spike_dates:
                lead_times.append(i)
                spike_dates.remove(candidate)
                break

    dist: dict[str, int] = {}
    for lt in lead_times:
        key = str(lt)
        dist[key] = dist.get(key, 0) + 1

    return {
        "threshold": threshold,
        "lead_window_days": lead_window_days,
        "total_spikes": total_spikes,
        "matched_spikes": len(lead_times),
        "unmatched_spikes": len(spike_dates),
        "warning_distribution": dist,
        "avg_warning_days": float(np.mean(lead_times)) if lead_times else 0.0,
    }


def _result_to_dict(obj: Any) -> dict[str, Any]:
    return _json_safe(asdict(obj))


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "value") and not isinstance(value, (str, bytes)):
        # Enum-like objects.
        try:
            return value.value
        except Exception:
            pass
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run canonical validation artifacts")
    parser.add_argument(
        "--feature-matrix",
        default="results/pipeline_output/feature_matrix.csv",
        help="Path to canonical feature matrix CSV",
    )
    parser.add_argument(
        "--regime-labels",
        default="results/pipeline_output/regime_labels.csv",
        help="Path to canonical regime labels CSV",
    )
    parser.add_argument(
        "--output-dir",
        default="results/validation",
        help="Output directory for validation artifacts",
    )
    parser.add_argument("--train-window-days", type=int, default=756)
    parser.add_argument("--test-window-days", type=int, default=63)
    parser.add_argument("--step-days", type=int, default=63)
    parser.add_argument("--purge-days", type=int, default=5)
    parser.add_argument("--rf-estimators", type=int, default=300)
    parser.add_argument(
        "--rf-random-state",
        type=int,
        default=42,
        help="Random seed for RandomForest walk-forward model",
    )
    parser.add_argument(
        "--compound-lag-days",
        type=int,
        default=0,
        help="Add lagged compound sentiment features from 1..N days to model inputs",
    )
    parser.add_argument(
        "--h1-vix-thresholds",
        default="20,25,30",
        help="Comma-separated VIX thresholds for H1 sensitivity checks",
    )
    parser.add_argument(
        "--h1-lead-window-days",
        type=int,
        default=5,
        help="Lead-window days used for H1 warning distribution analysis",
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("validation_%Y%m%d_%H%M%S")

    feature_df = _load_time_indexed_csv(Path(args.feature_matrix))
    labels_df = _load_time_indexed_csv(Path(args.regime_labels))
    if "regime" not in labels_df.columns:
        raise ValueError("regime_labels CSV must include 'regime' column")

    common_idx = feature_df.index.intersection(labels_df.index)
    feature_df = feature_df.loc[common_idx].sort_index()
    regime = labels_df.loc[common_idx, "regime"].astype(str)

    model_features = feature_df.drop(columns=[c for c in ["regime", "regime_id"] if c in feature_df.columns])
    model_features = _sanitize_features(model_features)
    model_features, lag_cols = _add_compound_lags(model_features, args.compound_lag_days)

    def model_fn(x_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
        model = RandomForestClassifier(
            n_estimators=args.rf_estimators,
            random_state=args.rf_random_state,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )
        model.fit(x_train, y_train)
        return model

    def predict_fn(model: RandomForestClassifier, x_test: pd.DataFrame) -> np.ndarray:
        return model.predict(x_test)

    backtester = WalkForwardBacktester(
        train_window_days=args.train_window_days,
        test_window_days=args.test_window_days,
        step_days=args.step_days,
        purge_days=args.purge_days,
        embargo_days=0,
        events=KEY_MARKET_EVENTS,
    )
    wf = backtester.run(model_features, regime, model_fn, predict_fn)

    y_true, y_pred = _aggregate_predictions(wf.window_results)
    labels_seen = sorted(set(y_true.tolist()) | set(y_pred.tolist()))
    cm = confusion_matrix(y_true, y_pred, labels=labels_seen)

    classification_metrics = {
        "n_observations": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)) if len(y_true) else 0.0,
        "precision_weighted": float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
        if len(y_true)
        else 0.0,
        "recall_weighted": float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
        if len(y_true)
        else 0.0,
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
        if len(y_true)
        else 0.0,
        "mcc": float(matthews_corrcoef(y_true, y_pred)) if len(y_true) else 0.0,
        "directional_accuracy": float(accuracy_score(y_true, y_pred)) if len(y_true) else 0.0,
        "transition_accuracy": _transition_accuracy(y_true, y_pred),
        "labels": labels_seen,
        "confusion_matrix": cm.tolist(),
    }

    sent_cols = [c for c in feature_df.columns if c.startswith("sent_")]
    if not sent_cols:
        raise ValueError("feature_matrix.csv must include sent_* columns for H2 validation")
    if "vix" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'vix' for H1 validation")

    tci_col = "te_proxy" if "te_proxy" in feature_df.columns else "cross_asset_std"
    crash_dates = [ev.start_date for ev in KEY_MARKET_EVENTS]
    h1_thresholds = [
        float(x.strip())
        for x in args.h1_vix_thresholds.split(",")
        if x.strip()
    ]
    if not h1_thresholds:
        h1_thresholds = [25.0]
    primary_h1_threshold = 25.0 if 25.0 in h1_thresholds else h1_thresholds[0]

    hyp_input = feature_df[[c for c in ["compound", "vix", tci_col] + sent_cols if c in feature_df.columns]].copy()
    hyp_input = _sanitize_features(hyp_input)

    validator = HypothesisValidator(significance_level=0.05, max_lag_days=10)
    h1_result = validator.validate_h1(
        sentiment_series=hyp_input["compound"],
        vix_series=hyp_input["vix"],
        regime_series=regime,
        vix_spike_threshold=primary_h1_threshold,
    )
    h2_result = validator.validate_h2(
        sentiment_by_asset=hyp_input[sent_cols],
        regime_series=regime,
    )
    h3_result = validator.validate_h3(
        tci_series=hyp_input[tci_col],
        regime_series=regime,
        crash_dates=crash_dates,
    )
    hyp_results = {"H1": h1_result, "H2": h2_result, "H3": h3_result}
    hypothesis_report_text = generate_hypothesis_report(hyp_results)

    h1_sensitivity = {}
    for threshold in h1_thresholds:
        h1_thr = validator.validate_h1(
            sentiment_series=hyp_input["compound"],
            vix_series=hyp_input["vix"],
            regime_series=regime,
            vix_spike_threshold=threshold,
        )
        h1_sensitivity[str(int(threshold) if threshold.is_integer() else threshold)] = {
            "summary": _result_to_dict(h1_thr),
            "warning_day_distribution": _warning_day_distribution(
                hyp_input["compound"],
                hyp_input["vix"],
                threshold=threshold,
                lead_window_days=args.h1_lead_window_days,
            ),
        }

    wf_summary = {
        "overall_accuracy": float(wf.overall_accuracy),
        "overall_precision": float(wf.overall_precision),
        "overall_recall": float(wf.overall_recall),
        "overall_f1": float(wf.overall_f1),
        "avg_window_accuracy": float(wf.avg_window_accuracy),
        "std_window_accuracy": float(wf.std_window_accuracy),
        "min_window_accuracy": float(wf.min_window_accuracy),
        "max_window_accuracy": float(wf.max_window_accuracy),
        "n_windows_generated": int(wf.n_windows),
        "n_windows_scored": int(len(wf.window_results)),
        "train_window_days": int(wf.train_window_days),
        "test_window_days": int(wf.test_window_days),
        "step_days": int(wf.step_days),
    }

    window_metrics = []
    for wr in wf.window_results:
        window_metrics.append(
            {
                "window_id": int(wr.window.window_id),
                "train_start": wr.window.train_start.isoformat(),
                "train_end": wr.window.train_end.isoformat(),
                "test_start": wr.window.test_start.isoformat(),
                "test_end": wr.window.test_end.isoformat(),
                "accuracy": float(wr.accuracy),
                "precision": float(wr.precision),
                "recall": float(wr.recall),
                "f1": float(wr.f1),
                "n_test_obs": int(len(wr.true_labels)),
            }
        )

    event_metrics = {
        k: {
            "detected_pre_event": bool(v.detected_pre_event),
            "warning_days": int(v.warning_days),
            "regime_during_event": v.regime_during_event,
            "regime_accuracy": float(v.regime_accuracy),
            "precision": float(v.precision),
            "recall": float(v.recall),
            "f1": float(v.f1),
            "transition_date": v.transition_date.isoformat() if v.transition_date else None,
            "evidence": v.evidence,
        }
        for k, v in wf.event_results.items()
    }

    hypothesis_json = {k: _result_to_dict(v) for k, v in hyp_results.items()}
    hypothesis_json["report_text"] = hypothesis_report_text

    payload = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "feature_matrix": str(Path(args.feature_matrix)),
            "regime_labels": str(Path(args.regime_labels)),
        },
        "methodology_experiments": {
            "compound_lag_days": int(args.compound_lag_days),
            "added_compound_lag_features": lag_cols,
            "rf_random_state": int(args.rf_random_state),
            "h1_primary_vix_threshold": float(primary_h1_threshold),
            "h1_vix_thresholds_evaluated": h1_thresholds,
            "h1_lead_window_days": int(args.h1_lead_window_days),
            "h1_threshold_sensitivity": h1_sensitivity,
        },
        "walk_forward": wf_summary,
        "classification": classification_metrics,
        "window_metrics": window_metrics,
        "event_metrics": event_metrics,
        "hypotheses": hypothesis_json,
    }

    json_path = out_dir / f"{run_id}.json"
    md_path = out_dir / f"{run_id}.md"
    txt_path = out_dir / f"{run_id}_hypothesis_report.txt"

    json_path.write_text(json.dumps(_json_safe(payload), indent=2))
    txt_path.write_text(hypothesis_report_text)

    md_lines = [
        "# Canonical Validation Report",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated UTC: `{payload['generated_at_utc']}`",
        f"- Inputs: `{payload['inputs']['feature_matrix']}`, `{payload['inputs']['regime_labels']}`",
        "",
        "## Walk-Forward Summary",
        "",
        f"- Windows generated/scored: {wf_summary['n_windows_generated']}/{wf_summary['n_windows_scored']}",
        f"- Accuracy: {wf_summary['overall_accuracy']:.4f}",
        f"- Precision (weighted): {wf_summary['overall_precision']:.4f}",
        f"- Recall (weighted): {wf_summary['overall_recall']:.4f}",
        f"- F1 (weighted): {wf_summary['overall_f1']:.4f}",
        "",
        "## Methodology Experiments",
        "",
        f"- Added lagged compound features: `{len(lag_cols)}`",
        f"- Random seed: `{args.rf_random_state}`",
        f"- Primary H1 VIX threshold: `{primary_h1_threshold}`",
        f"- H1 thresholds evaluated: `{', '.join(str(t) for t in h1_thresholds)}`",
        "",
        "## Classification Metrics",
        "",
        f"- MCC: {classification_metrics['mcc']:.4f}",
        f"- Directional Accuracy: {classification_metrics['directional_accuracy']:.4f}",
        f"- Transition Accuracy: {classification_metrics['transition_accuracy']:.4f}",
        "",
        "## Hypothesis Verdicts",
        "",
        f"- H1: `{hyp_results['H1'].result.value}`",
        f"- H2: `{hyp_results['H2'].result.value}`",
        f"- H3: `{hyp_results['H3'].result.value}`",
        "",
        "See the full hypothesis report in:",
        f"- `{txt_path}`",
    ]
    md_path.write_text("\n".join(md_lines) + "\n")

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote Markdown: {md_path}")
    print(f"Wrote text report: {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
