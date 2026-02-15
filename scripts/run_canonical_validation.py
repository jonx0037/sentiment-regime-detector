#!/usr/bin/env python3
"""Run canonical walk-forward + hypothesis validation and export report artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
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

    def model_fn(x_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
        model = RandomForestClassifier(
            n_estimators=args.rf_estimators,
            random_state=42,
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

    hyp_input = feature_df[[c for c in ["compound", "vix", tci_col] + sent_cols if c in feature_df.columns]].copy()
    hyp_input = _sanitize_features(hyp_input)

    validator = HypothesisValidator(significance_level=0.05, max_lag_days=10)
    hyp_results = validator.validate_all(
        sentiment_series=hyp_input["compound"],
        sentiment_by_asset=hyp_input[sent_cols],
        vix_series=hyp_input["vix"],
        tci_series=hyp_input[tci_col],
        regime_series=regime,
        crash_dates=crash_dates,
    )
    hypothesis_report_text = generate_hypothesis_report(hyp_results)

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
