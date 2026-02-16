#!/usr/bin/env python3
"""Execute locked H1 confirmation analysis under a fixed pre-registered protocol."""

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
    return df.dropna(subset=[idx_col]).set_index(idx_col).sort_index()


def _build_h1_sentiment_series(feature_df: pd.DataFrame) -> pd.Series:
    if "compound" not in feature_df.columns or "returns" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'compound' and 'returns'")
    out = feature_df["compound"].astype(float) * feature_df["returns"].astype(float).abs()
    return out.replace([np.inf, -np.inf], np.nan).ffill().bfill().fillna(0.0)


def _bh_fdr(p_values: list[float]) -> list[float]:
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
    parser = argparse.ArgumentParser(description="Run locked H1 confirmation analysis")
    parser.add_argument("--feature-matrix", default="results/pipeline_output/feature_matrix.csv")
    parser.add_argument("--regime-labels", default="results/pipeline_output/regime_labels.csv")
    parser.add_argument(
        "--output-dir",
        default="results/validation/h1_confirmation/locked_protocol",
    )
    args = parser.parse_args()

    # Locked protocol constants.
    alpha = 0.05
    max_lag_days = 10
    vix_threshold = 25.0
    pre_event_days = 180
    post_event_days = 90
    min_event_observations = 80
    max_fpr_event = 0.25

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("h1_locked_confirmation_%Y%m%d_%H%M%S")

    feature_df = _load_time_indexed_csv(Path(args.feature_matrix))
    labels_df = _load_time_indexed_csv(Path(args.regime_labels))
    if "regime" not in labels_df.columns:
        raise ValueError("regime_labels CSV must include 'regime' column")
    if "vix" not in feature_df.columns:
        raise ValueError("feature_matrix.csv must include 'vix' column")

    common_idx = feature_df.index.intersection(labels_df.index)
    feature_df = feature_df.loc[common_idx].sort_index()
    regime = labels_df.loc[common_idx, "regime"].astype(str)
    vix = feature_df["vix"].astype(float)
    h1_sentiment = _build_h1_sentiment_series(feature_df)

    validator = HypothesisValidator(significance_level=alpha, max_lag_days=max_lag_days)
    global_h1 = validator.validate_h1(
        sentiment_series=h1_sentiment,
        vix_series=vix,
        regime_series=regime,
        vix_spike_threshold=vix_threshold,
    )

    event_rows: list[dict[str, Any]] = []
    for event in KEY_MARKET_EVENTS:
        start = event.start_date - pd.Timedelta(days=pre_event_days)
        end = event.end_date + pd.Timedelta(days=post_event_days)
        idx = vix.index[(vix.index >= start) & (vix.index <= end)]
        if len(idx) < min_event_observations:
            continue
        h1 = validator.validate_h1(
            sentiment_series=h1_sentiment.loc[idx],
            vix_series=vix.loc[idx],
            regime_series=regime.loc[idx],
            vix_spike_threshold=vix_threshold,
        )
        event_rows.append(
            {
                "event": event.name,
                "window_start": start.date().isoformat(),
                "window_end": end.date().isoformat(),
                "n_observations": int(len(idx)),
                "h1_result": h1.result.value,
                "optimal_lag": h1.lead_lag.optimal_lag if h1.lead_lag else None,
                "granger_p_value": h1.granger.p_value if h1.granger else None,
                "hit_rate": h1.hit_rate,
                "false_positive_rate": h1.false_positive_rate,
                "avg_lead_days": h1.avg_lead_days,
            }
        )

    ps = [r["granger_p_value"] for r in event_rows if r["granger_p_value"] is not None]
    q_values = _bh_fdr(ps)
    q_iter = iter(q_values)
    bonf_alpha = alpha / max(len(ps), 1)
    for row in event_rows:
        if row["granger_p_value"] is None:
            row["granger_q_value_bh"] = None
            row["granger_sig_bonferroni"] = False
            row["granger_sig_bh_fdr"] = False
            continue
        qv = float(next(q_iter))
        row["granger_q_value_bh"] = qv
        row["granger_sig_bonferroni"] = bool(row["granger_p_value"] < bonf_alpha)
        row["granger_sig_bh_fdr"] = bool(qv < alpha)

    primary_global_ok = bool(
        global_h1.result.value == "supported"
        and global_h1.lead_lag is not None
        and 1 <= int(global_h1.lead_lag.optimal_lag) <= 5
    )

    event_support_count = 0
    for row in event_rows:
        event_ok = bool(
            row["h1_result"] == "supported"
            and row["optimal_lag"] is not None
            and 1 <= int(row["optimal_lag"]) <= 5
            and row["granger_sig_bonferroni"]
            and row["granger_sig_bh_fdr"]
            and row["false_positive_rate"] is not None
            and float(row["false_positive_rate"]) <= max_fpr_event
        )
        row["event_confirm_eligible"] = event_ok
        if event_ok:
            event_support_count += 1

    confirmed = bool(primary_global_ok or event_support_count >= 2)
    if confirmed:
        outcome = "confirmed"
    else:
        outcome = "not_confirmed"

    payload = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": {
            "id": "H1_LOCKED_CONFIRMATION_PROTOCOL_V1",
            "alpha": alpha,
            "max_lag_days": max_lag_days,
            "vix_threshold": vix_threshold,
            "h1_sentiment_transform": "compound_x_abs_returns",
            "event_window_pre_days": pre_event_days,
            "event_window_post_days": post_event_days,
            "min_event_observations": min_event_observations,
            "event_max_false_positive_rate": max_fpr_event,
            "multiple_testing": {
                "bonferroni_alpha": bonf_alpha,
                "bh_fdr_alpha": alpha,
                "m_tests": len(ps),
            },
            "decision_rule": {
                "primary_global_required": "H1 supported AND optimal_lag in [1,5]",
                "secondary_event_required": (
                    "At least 2 events with H1 supported, lag in [1,5], Bonferroni+BH significance, and FPR <= 0.25"
                ),
            },
        },
        "global_h1": {
            "result": global_h1.result.value,
            "optimal_lag": global_h1.lead_lag.optimal_lag if global_h1.lead_lag else None,
            "max_correlation": global_h1.lead_lag.max_correlation if global_h1.lead_lag else None,
            "lead_lag_p_value": global_h1.lead_lag.p_value if global_h1.lead_lag else None,
            "granger_p_value": global_h1.granger.p_value if global_h1.granger else None,
            "hit_rate": global_h1.hit_rate,
            "false_positive_rate": global_h1.false_positive_rate,
            "avg_lead_days": global_h1.avg_lead_days,
        },
        "event_h1": event_rows,
        "decision": {
            "primary_global_ok": primary_global_ok,
            "event_support_count": event_support_count,
            "confirmed": confirmed,
            "outcome": outcome,
        },
    }

    json_path = out_dir / f"{run_id}.json"
    md_path = out_dir / f"{run_id}.md"
    json_path.write_text(json.dumps(payload, indent=2))

    lines = [
        "# H1 Locked Confirmation Analysis",
        "",
        f"- Run ID: `{run_id}`",
        f"- Protocol ID: `{payload['protocol']['id']}`",
        f"- Outcome: `{outcome}`",
        "",
        "## Global H1",
        "",
        f"- Result: `{payload['global_h1']['result']}`",
        f"- Optimal lag: `{payload['global_h1']['optimal_lag']}`",
        f"- Granger p-value: `{payload['global_h1']['granger_p_value']}`",
        f"- Hit rate: `{payload['global_h1']['hit_rate']}`",
        f"- FPR: `{payload['global_h1']['false_positive_rate']}`",
        "",
        "## Event-Conditioned H1",
        "",
        "| Event | H1 | Lag | Granger p | Granger q (BH) | Bonferroni Sig | FDR Sig | FPR | Confirm Eligible |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in event_rows:
        lines.append(
            "| {event} | {h1_result} | {optimal_lag} | {granger_p_value:.4g} | {granger_q_value_bh:.4g} | {granger_sig_bonferroni} | {granger_sig_bh_fdr} | {false_positive_rate:.4f} | {event_confirm_eligible} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Decision Summary",
            "",
            f"- Primary global criterion met: `{primary_global_ok}`",
            f"- Event confirmations: `{event_support_count}`",
            f"- Final confirmation: `{confirmed}`",
        ]
    )
    md_path.write_text("\n".join(lines) + "\n")

    print(f"Wrote JSON: {json_path}")
    print(f"Wrote Markdown: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
