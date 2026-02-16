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


def _build_h1_sentiment_series(
    feature_df: pd.DataFrame,
    transform: str,
) -> pd.Series:
    if "compound" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'compound' for H1 validation")

    compound = feature_df["compound"].astype(float)
    returns = feature_df["returns"].astype(float) if "returns" in feature_df.columns else None
    vix = feature_df["vix"].astype(float) if "vix" in feature_df.columns else None

    if transform == "compound":
        out = compound.copy()
    elif transform == "compound_delta_1":
        out = compound.diff(1)
    elif transform == "compound_delta_3":
        out = compound.diff(3)
    elif transform == "compound_ema_10":
        out = compound.ewm(span=10, adjust=False).mean()
    elif transform == "compound_deviation_ema_10":
        out = compound - compound.ewm(span=10, adjust=False).mean()
    elif transform == "compound_zscore_63":
        roll_mean = compound.rolling(63, min_periods=10).mean()
        roll_std = compound.rolling(63, min_periods=10).std()
        out = (compound - roll_mean) / (roll_std + 1e-9)
    elif transform == "compound_x_abs_returns":
        if returns is None:
            raise ValueError("H1 transform 'compound_x_abs_returns' requires 'returns' column")
        out = compound * returns.abs()
    elif transform == "compound_vol_scaled_delta_1":
        if vix is None:
            raise ValueError("H1 transform 'compound_vol_scaled_delta_1' requires 'vix' column")
        out = compound.diff(1) / (vix.rolling(5, min_periods=2).mean() + 1e-9)
    else:
        raise ValueError(f"Unsupported h1 sentiment transform: {transform}")

    return out.replace([np.inf, -np.inf], np.nan).ffill().bfill().fillna(0.0)


def _apply_garch_midas_ciss_features(
    features: pd.DataFrame,
    ciss_weight: float = 0.5,
    ciss_transform: str = "raw",
) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = features.copy()
    metadata: dict[str, Any] = {"mode": "baseline"}
    try:
        from sentiment_detector.models.garch_midas import GARCHMIDASWithCISS
    except Exception as exc:
        metadata.update({"mode": "baseline", "error": f"import_failed: {exc}"})
        return out, metadata

    if "returns" not in out.columns or "compound" not in out.columns:
        metadata.update({"mode": "baseline", "error": "missing_returns_or_compound"})
        return out, metadata

    try:
        model = GARCHMIDASWithCISS(ciss_weight=ciss_weight, distribution="t")
        result = model.fit_with_ciss(
            returns=out["returns"].astype(float),
            sentiment=out["compound"].astype(float),
            ciss=out["ciss"].astype(float) if "ciss" in out.columns else None,
            ciss_transform=ciss_transform,
        )

        out["garch_vol"] = result.conditional_volatility.reindex(out.index).ffill().bfill()
        out["long_run_vol"] = result.long_run_volatility.reindex(out.index).ffill().bfill()
        out["garch_midas_short_run_vol"] = result.short_run_volatility.reindex(out.index).ffill().bfill()

        metadata = {
            "mode": "garch_midas_ciss",
            "ciss_weight": ciss_weight,
            "ciss_transform": ciss_transform,
            "convergence": bool(result.convergence),
            "aic": float(result.aic) if result.aic is not None and not np.isnan(result.aic) else None,
            "bic": float(result.bic) if result.bic is not None and not np.isnan(result.bic) else None,
            "log_likelihood": float(result.log_likelihood)
            if result.log_likelihood is not None and not np.isnan(result.log_likelihood)
            else None,
            "sentiment_coefficient": result.sentiment_coefficient,
            "ciss_coefficient": getattr(result, "ciss_coefficient", None),
        }
        return out, metadata
    except Exception as exc:
        metadata = {"mode": "baseline", "error": f"fit_failed: {exc}"}
        return out, metadata


def _apply_full_network_features(
    features: pd.DataFrame,
    sent_cols: list[str],
    window_days: int = 126,
    step_days: int = 21,
    te_history_length: int = 3,
    te_permutations: int = 10,
    granger_max_lag: int = 3,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = features.copy()
    metadata: dict[str, Any] = {"mode": "proxy"}
    if len(sent_cols) < 2:
        metadata.update({"mode": "proxy", "error": "insufficient_sent_cols"})
        return out, metadata

    try:
        from sentiment_detector.features.transfer_entropy import TransferEntropyAnalyzer
        from sentiment_detector.features.connectedness import ConnectednessAnalyzer
    except Exception as exc:
        metadata.update({"mode": "proxy", "error": f"import_failed: {exc}"})
        return out, metadata

    tci_series = pd.Series(np.nan, index=out.index, dtype=float)
    te_netflow = pd.Series(np.nan, index=out.index, dtype=float)

    # Prefer equities/crypto pair for directional divergence if available.
    pair_a = "sent_equities" if "sent_equities" in sent_cols else sent_cols[0]
    pair_b = "sent_crypto" if "sent_crypto" in sent_cols else sent_cols[1]

    conn = ConnectednessAnalyzer(var_lag=granger_max_lag, forecast_horizon=10, generalized=True)
    te = TransferEntropyAnalyzer(
        history_length=te_history_length,
        n_permutations=te_permutations,
        significance_level=0.05,
    )

    n = len(out)
    anchors = 0
    for i in range(window_days, n, step_days):
        window = out[sent_cols].iloc[i - window_days : i].copy()
        window = window.replace([np.inf, -np.inf], np.nan).dropna()
        if len(window) < max(50, granger_max_lag * 6):
            continue
        date = out.index[i]
        anchors += 1
        try:
            c_res = conn.from_data(window, columns=sent_cols, method="granger")
            # ConnectednessAnalyzer returns percentage-like values; normalize to 0..1 scale.
            tci_series.loc[date] = float(c_res.total_connectedness) / 100.0
        except Exception:
            pass

        try:
            te_ab = te.calculate_te(
                source=window[pair_a].values,
                target=window[pair_b].values,
                source_name=pair_a,
                target_name=pair_b,
            )
            te_ba = te.calculate_te(
                source=window[pair_b].values,
                target=window[pair_a].values,
                source_name=pair_b,
                target_name=pair_a,
            )
            te_netflow.loc[date] = float(te_ab.effective_te - te_ba.effective_te)
        except Exception:
            pass

    tci_series = tci_series.ffill().bfill().fillna(0.0)
    te_netflow = te_netflow.ffill().bfill().fillna(0.0)

    out["tci_full_granger"] = tci_series
    out["te_netflow_full"] = te_netflow
    # Maintain backward-compatible proxy column name while swapping in full feature.
    out["te_proxy"] = te_netflow.abs()

    metadata = {
        "mode": "full_granger_te",
        "window_days": int(window_days),
        "step_days": int(step_days),
        "anchors_computed": int(anchors),
        "te_history_length": int(te_history_length),
        "te_permutations": int(te_permutations),
        "granger_max_lag": int(granger_max_lag),
        "netflow_pair": [pair_a, pair_b],
    }
    return out, metadata


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
        "--volatility-feature-mode",
        choices=["baseline", "garch_midas_ciss"],
        default="baseline",
        help="How to construct volatility features before walk-forward modeling",
    )
    parser.add_argument("--ciss-weight", type=float, default=0.5)
    parser.add_argument(
        "--ciss-transform",
        choices=["raw", "log", "zscore", "rank"],
        default="raw",
    )
    parser.add_argument(
        "--network-feature-mode",
        choices=["proxy", "full_granger_te"],
        default="proxy",
        help="Use existing proxy network features or coarse full granger/TE network features",
    )
    parser.add_argument("--network-window-days", type=int, default=126)
    parser.add_argument("--network-step-days", type=int, default=21)
    parser.add_argument("--network-te-history-length", type=int, default=3)
    parser.add_argument("--network-te-permutations", type=int, default=10)
    parser.add_argument("--network-granger-max-lag", type=int, default=3)
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
    parser.add_argument(
        "--h1-sentiment-transform",
        choices=[
            "compound",
            "compound_delta_1",
            "compound_delta_3",
            "compound_ema_10",
            "compound_deviation_ema_10",
            "compound_zscore_63",
            "compound_x_abs_returns",
            "compound_vol_scaled_delta_1",
        ],
        default="compound",
        help="Sentiment series transform used for H1 validation only",
    )
    parser.add_argument(
        "--h1-max-lag-days",
        type=int,
        default=10,
        help="Maximum lag tested in H1 lead-lag analysis",
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

    # Optional methodology upgrades before model feature selection.
    vol_feature_metadata: dict[str, Any] = {"mode": "baseline"}
    if args.volatility_feature_mode == "garch_midas_ciss":
        feature_df, vol_feature_metadata = _apply_garch_midas_ciss_features(
            feature_df,
            ciss_weight=args.ciss_weight,
            ciss_transform=args.ciss_transform,
        )

    sent_cols = [c for c in feature_df.columns if c.startswith("sent_")]
    network_feature_metadata: dict[str, Any] = {"mode": "proxy"}
    if args.network_feature_mode == "full_granger_te":
        feature_df, network_feature_metadata = _apply_full_network_features(
            feature_df,
            sent_cols=sent_cols,
            window_days=args.network_window_days,
            step_days=args.network_step_days,
            te_history_length=args.network_te_history_length,
            te_permutations=args.network_te_permutations,
            granger_max_lag=args.network_granger_max_lag,
        )
        sent_cols = [c for c in feature_df.columns if c.startswith("sent_")]

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

    if not sent_cols:
        raise ValueError("feature_matrix.csv must include sent_* columns for H2 validation")
    if "vix" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'vix' for H1 validation")
    if "compound" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'compound' for H1 validation")

    if args.network_feature_mode == "full_granger_te" and "tci_full_granger" in feature_df.columns:
        tci_col = "tci_full_granger"
    else:
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

    h1_sentiment = _build_h1_sentiment_series(feature_df, args.h1_sentiment_transform)
    hyp_input = feature_df[[c for c in ["compound", "vix", tci_col] + sent_cols if c in feature_df.columns]].copy()
    hyp_input["h1_sentiment_series"] = h1_sentiment
    hyp_input = _sanitize_features(hyp_input)

    validator = HypothesisValidator(significance_level=0.05, max_lag_days=args.h1_max_lag_days)
    h1_result = validator.validate_h1(
        sentiment_series=hyp_input["h1_sentiment_series"],
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
            sentiment_series=hyp_input["h1_sentiment_series"],
            vix_series=hyp_input["vix"],
            regime_series=regime,
            vix_spike_threshold=threshold,
        )
        h1_sensitivity[str(int(threshold) if threshold.is_integer() else threshold)] = {
            "summary": _result_to_dict(h1_thr),
            "warning_day_distribution": _warning_day_distribution(
                hyp_input["h1_sentiment_series"],
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
            "volatility_feature_mode": args.volatility_feature_mode,
            "volatility_feature_metadata": vol_feature_metadata,
            "network_feature_mode": args.network_feature_mode,
            "network_feature_metadata": network_feature_metadata,
            "tci_series_used_for_h3": tci_col,
            "h1_primary_vix_threshold": float(primary_h1_threshold),
            "h1_vix_thresholds_evaluated": h1_thresholds,
            "h1_lead_window_days": int(args.h1_lead_window_days),
            "h1_sentiment_transform": args.h1_sentiment_transform,
            "h1_max_lag_days": int(args.h1_max_lag_days),
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
        f"- Volatility feature mode: `{args.volatility_feature_mode}`",
        f"- Network feature mode: `{args.network_feature_mode}`",
        f"- Primary H1 VIX threshold: `{primary_h1_threshold}`",
        f"- H1 thresholds evaluated: `{', '.join(str(t) for t in h1_thresholds)}`",
        f"- H1 sentiment transform: `{args.h1_sentiment_transform}`",
        f"- H1 max lag days: `{args.h1_max_lag_days}`",
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
