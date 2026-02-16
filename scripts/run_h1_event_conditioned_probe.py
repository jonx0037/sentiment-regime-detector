#!/usr/bin/env python3
"""Run event-conditioned H1 diagnostics and export reproducible artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from sentiment_detector.validation.hypothesis_validator import HypothesisValidator
from sentiment_detector.validation.walk_forward_backtest import KEY_MARKET_EVENTS


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


def _build_h1_sentiment_series(feature_df: pd.DataFrame, transform: str) -> pd.Series:
    if "compound" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'compound'")
    compound = feature_df["compound"].astype(float)
    returns = feature_df["returns"].astype(float) if "returns" in feature_df.columns else None
    vix = feature_df["vix"].astype(float) if "vix" in feature_df.columns else None

    if transform == "compound":
        out = compound.copy()
    elif transform == "compound_delta_1":
        out = compound.diff(1)
    elif transform == "compound_delta_3":
        out = compound.diff(3)
    elif transform == "compound_zscore_63":
        roll_mean = compound.rolling(63, min_periods=10).mean()
        roll_std = compound.rolling(63, min_periods=10).std()
        out = (compound - roll_mean) / (roll_std + 1e-9)
    elif transform == "compound_x_abs_returns":
        if returns is None:
            raise ValueError("transform requires 'returns' column")
        out = compound * returns.abs()
    elif transform == "compound_vol_scaled_delta_1":
        if vix is None:
            raise ValueError("transform requires 'vix' column")
        out = compound.diff(1) / (vix.rolling(5, min_periods=2).mean() + 1e-9)
    else:
        raise ValueError(f"Unsupported transform: {transform}")

    return out.replace([np.inf, -np.inf], np.nan).ffill().bfill().fillna(0.0)


def _bh_fdr(p_values: list[float]) -> list[float]:
    """Benjamini-Hochberg adjusted q-values."""
    n = len(p_values)
    if n == 0:
        return []
    order = np.argsort(p_values)
    ranked = np.array(p_values)[order]
    q = np.empty(n, dtype=float)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        val = min(prev, ranked[i] * n / rank)
        q[i] = val
        prev = val
    out = np.empty(n, dtype=float)
    out[order] = q
    return out.tolist()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run event-conditioned H1 probe")
    parser.add_argument("--feature-matrix", default="results/pipeline_output/feature_matrix.csv")
    parser.add_argument("--regime-labels", default="results/pipeline_output/regime_labels.csv")
    parser.add_argument("--output-dir", default="results/validation/h1_remediation/event_conditioned_probe")
    parser.add_argument(
        "--h1-sentiment-transform",
        choices=[
            "compound",
            "compound_delta_1",
            "compound_delta_3",
            "compound_zscore_63",
            "compound_x_abs_returns",
            "compound_vol_scaled_delta_1",
        ],
        default="compound_x_abs_returns",
    )
    parser.add_argument("--pre-event-days", type=int, default=180)
    parser.add_argument("--post-event-days", type=int, default=90)
    parser.add_argument("--h1-max-lag-days", type=int, default=10)
    parser.add_argument("--h1-vix-threshold", type=float, default=25.0)
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("h1_event_probe_%Y%m%d_%H%M%S")

    feature_df = _load_time_indexed_csv(Path(args.feature_matrix))
    labels_df = _load_time_indexed_csv(Path(args.regime_labels))
    if "regime" not in labels_df.columns:
        raise ValueError("regime_labels CSV must include 'regime' column")

    common_idx = feature_df.index.intersection(labels_df.index)
    feature_df = feature_df.loc[common_idx].sort_index()
    regime = labels_df.loc[common_idx, "regime"].astype(str)
    if "vix" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'vix'")

    h1_sentiment = _build_h1_sentiment_series(feature_df, args.h1_sentiment_transform)
    vix = feature_df["vix"].astype(float)

    validator = HypothesisValidator(significance_level=0.05, max_lag_days=args.h1_max_lag_days)

    event_rows: list[dict[str, Any]] = []
    for event in KEY_MARKET_EVENTS:
        start = event.start_date - pd.Timedelta(days=args.pre_event_days)
        end = event.end_date + pd.Timedelta(days=args.post_event_days)
        idx = vix.index[(vix.index >= start) & (vix.index <= end)]
        if len(idx) < 80:
            continue
        h1 = validator.validate_h1(
            sentiment_series=h1_sentiment.loc[idx],
            vix_series=vix.loc[idx],
            regime_series=regime.loc[idx],
            vix_spike_threshold=args.h1_vix_threshold,
        )
        event_rows.append(
            {
                "event": event.name,
                "window_start": start.date().isoformat(),
                "window_end": end.date().isoformat(),
                "n_observations": int(len(idx)),
                "h1_result": h1.result.value,
                "optimal_lag": h1.lead_lag.optimal_lag if h1.lead_lag else None,
                "max_correlation": h1.lead_lag.max_correlation if h1.lead_lag else None,
                "granger_p_value": h1.granger.p_value if h1.granger else None,
                "hit_rate": h1.hit_rate,
                "false_positive_rate": h1.false_positive_rate,
                "avg_lead_days": h1.avg_lead_days,
            }
        )

    # Multiple-testing controls across event Granger p-values.
    granger_ps = [r["granger_p_value"] for r in event_rows if r["granger_p_value"] is not None]
    q_values = _bh_fdr(granger_ps)
    q_iter = iter(q_values)
    bonf_alpha = 0.05 / max(len(granger_ps), 1)
    for row in event_rows:
        if row["granger_p_value"] is None:
            row["granger_q_value_bh"] = None
            row["granger_sig_bonferroni"] = False
            row["granger_sig_bh_fdr"] = False
            continue
        qv = float(next(q_iter))
        row["granger_q_value_bh"] = qv
        row["granger_sig_bonferroni"] = bool(row["granger_p_value"] < bonf_alpha)
        row["granger_sig_bh_fdr"] = bool(qv < 0.05)

    payload = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "feature_matrix": str(Path(args.feature_matrix)),
            "regime_labels": str(Path(args.regime_labels)),
        },
        "configuration": {
            "h1_sentiment_transform": args.h1_sentiment_transform,
            "pre_event_days": int(args.pre_event_days),
            "post_event_days": int(args.post_event_days),
            "h1_max_lag_days": int(args.h1_max_lag_days),
            "h1_vix_threshold": float(args.h1_vix_threshold),
            "multiple_testing": {
                "method_bh_fdr": "Benjamini-Hochberg",
                "method_bonferroni": "familywise alpha=0.05/m",
                "m_tests": int(len(granger_ps)),
                "bonferroni_alpha": float(bonf_alpha),
            },
        },
        "event_results": event_rows,
    }

    json_path = out_dir / f"{run_id}.json"
    md_path = out_dir / f"{run_id}.md"
    json_path.write_text(json.dumps(payload, indent=2))

    lines = [
        "# H1 Event-Conditioned Probe",
        "",
        f"- Run ID: `{run_id}`",
        f"- Transform: `{args.h1_sentiment_transform}`",
        f"- Window: `[-{args.pre_event_days}, +{args.post_event_days}]` days around each event",
        f"- H1 max lag days: `{args.h1_max_lag_days}`",
        f"- H1 VIX threshold: `{args.h1_vix_threshold}`",
        "",
        "## Results",
        "",
        "| Event | H1 Result | Optimal Lag | Granger p | Granger q (BH) | Bonferroni Sig | FDR Sig | Hit Rate | FPR | Avg Lead | N Obs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in event_rows:
        lines.append(
            "| {event} | {h1_result} | {optimal_lag} | {granger_p_value:.4g} | {granger_q_value_bh:.4g} | {granger_sig_bonferroni} | {granger_sig_bh_fdr} | {hit_rate:.4f} | {false_positive_rate:.4f} | {avg_lead_days:.2f} | {n_observations} |".format(
                **row
            )
        )
    md_path.write_text("\n".join(lines) + "\n")

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote Markdown: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
