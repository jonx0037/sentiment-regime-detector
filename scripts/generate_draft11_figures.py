#!/usr/bin/env python3
"""Generate Draft-1.1 figure pack from locked validation artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


sns.set_theme(style="whitegrid")


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def figure_h1_summary(validation: dict, locked_h1: dict, outpath: Path) -> None:
    h1 = validation["hypotheses"]["H1"]

    corr_by_lag = h1["lead_lag"]["correlations_by_lag"]
    lags = np.array(sorted(int(k) for k in corr_by_lag.keys()))
    corrs = np.array([corr_by_lag[str(k)] for k in lags])

    events = pd.DataFrame(locked_h1["event_h1"]).copy()
    events = events[["event", "optimal_lag", "h1_result", "false_positive_rate", "event_confirm_eligible"]]
    events = events.sort_values(["optimal_lag", "event"], ascending=[False, True]).reset_index(drop=True)

    result_colors = {
        "supported": "#2E8B57",
        "inconclusive": "#E6A700",
        "not_supported": "#D9534F",
    }

    fig, axes = plt.subplots(2, 1, figsize=(11, 12), gridspec_kw={"height_ratios": [1.0, 1.35]})

    ax0 = axes[0]
    ax0.plot(lags, corrs, marker="o", color="#1f77b4", linewidth=2.2, markersize=8)
    ax0.axvspan(1, 7, color="#d3e5ff", alpha=0.35, label="Locked confirmation lag range (1-7)")
    ax0.axvline(h1["lead_lag"]["optimal_lag"], color="#d62728", linestyle="--", linewidth=2.0)
    ax0.set_title("Global H1 Lead-Lag Profile (Locked Reporting Run)", fontsize=17)
    ax0.set_xlabel("Lag (days, positive = sentiment leads)", fontsize=14)
    ax0.set_ylabel("Correlation", fontsize=14)
    ax0.tick_params(labelsize=12)
    ax0.legend(loc="lower left", fontsize=12)

    ax1 = axes[1]
    events = events.copy()
    events["event_label"] = events.apply(
        lambda row: f"{row['event']} | FPR={row['false_positive_rate']:.2f}" + (" *" if bool(row["event_confirm_eligible"]) else ""),
        axis=1,
    )

    y = np.arange(len(events))
    colors = [result_colors.get(v, "#666666") for v in events["h1_result"]]
    ax1.hlines(y, xmin=0.0, xmax=events["optimal_lag"], color="#9aa0a6", linewidth=1.2, alpha=0.8)
    ax1.scatter(events["optimal_lag"], y, c=colors, s=170, edgecolor="black", linewidth=0.9)

    ax1.axvspan(1, 7, color="#d3e5ff", alpha=0.25)
    ax1.set_yticks(y)
    ax1.set_yticklabels(events["event_label"], fontsize=11)
    ax1.invert_yaxis()
    ax1.set_xlim(-0.25, max(7.5, float(events["optimal_lag"].max()) + 1.0))
    ax1.set_xlabel("Optimal lag by event window (days)", fontsize=14)
    ax1.set_title("Event-Conditioned H1 Outcomes (Locked Protocol V3)", fontsize=17)
    ax1.tick_params(axis="x", labelsize=12)
    ax1.grid(axis="y", alpha=0.15)

    outcome = locked_h1["decision"]["outcome"]
    support_count = locked_h1["decision"]["event_support_count"]
    required = locked_h1["protocol"]["required_event_confirmations"]
    global_lag = locked_h1["global_h1"]["optimal_lag"]
    fig.suptitle(
        f"H1 Summary: global={locked_h1['global_h1']['result']} (lag={global_lag}), "
        f"event confirmations={support_count}/{required}, decision={outcome}",
        fontsize=16,
        y=0.995,
    )

    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=result_colors["supported"], label="supported", markersize=8),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=result_colors["inconclusive"], label="inconclusive", markersize=8),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=result_colors["not_supported"], label="not_supported", markersize=9),
        Line2D([0], [0], color="w", marker=None, label="* = event_confirm_eligible"),
    ]
    ax1.legend(handles=legend, loc="lower right", fontsize=11)

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(outpath, dpi=240, bbox_inches="tight")
    plt.close(fig)


def _contiguous_segments(df: pd.DataFrame, regime_col: str = "regime"):
    start_idx = 0
    regimes = df[regime_col].tolist()
    dates = df.index.tolist()
    for i in range(1, len(df)):
        if regimes[i] != regimes[i - 1]:
            yield dates[start_idx], dates[i - 1], regimes[i - 1]
            start_idx = i
    if len(df):
        yield dates[start_idx], dates[-1], regimes[-1]


def figure_regime_vix_timeline(feature_matrix: pd.DataFrame, outpath: Path) -> None:
    fm = feature_matrix.copy()
    fm = fm.loc[(fm.index >= "2019-11-01") & (fm.index <= "2020-06-30")]

    regime_colors = {
        "low_volatility": "#2ca02c",
        "normal": "#1f77b4",
        "elevated": "#ff7f0e",
        "high_volatility": "#d62728",
    }

    fig, ax = plt.subplots(figsize=(11, 6.5))

    for start, end, regime in _contiguous_segments(fm, regime_col="regime"):
        color = regime_colors.get(str(regime), "#bbbbbb")
        ax.axvspan(start, end, color=color, alpha=0.18)

    ax.plot(fm.index, fm["vix"], color="black", linewidth=2.2, label="VIX")
    ax.axhline(30.0, color="#8b0000", linestyle="--", linewidth=1.8, label="VIX=30 threshold")
    ax.set_title("COVID Window: VIX vs Regime Labels (Canonical Pipeline Output)", fontsize=16)
    ax.set_ylabel("VIX", fontsize=14)
    ax.set_xlabel("Date", fontsize=14)
    ax.tick_params(labelsize=12)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")

    patches = [Patch(facecolor=c, edgecolor="none", alpha=0.25, label=k) for k, c in regime_colors.items()]
    ax.legend(
        handles=[
            Line2D([0], [0], color="black", lw=2.2, label="VIX"),
            Line2D([0], [0], color="#8b0000", lw=1.8, ls="--", label="VIX=30 threshold"),
        ]
        + patches,
        loc="upper left",
        ncol=2,
        fontsize=11,
    )

    fig.tight_layout()
    fig.savefig(outpath, dpi=240, bbox_inches="tight")
    plt.close(fig)


def figure_confusion_matrix(validation: dict, outpath: Path) -> None:
    c = validation["classification"]
    labels = c["labels"]
    cm = np.array(c["confusion_matrix"])

    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Locked Run Confusion Matrix (validation_20260216_013107)")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    txt = (
        f"Accuracy={c['accuracy']:.4f} | F1w={c['f1_weighted']:.4f} | "
        f"MCC={c['mcc']:.4f} | Transition Acc={c['transition_accuracy']:.4f}"
    )
    fig.text(0.5, 0.01, txt, ha="center", fontsize=9)

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(outpath, dpi=220, bbox_inches="tight")
    plt.close(fig)


def _h2_distributions(feature_matrix: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    sent_cols = [c for c in feature_matrix.columns if c.startswith("sent_")]
    regimes = feature_matrix["regime"]
    divergence = feature_matrix[sent_cols].std(axis=1)

    regime_changes = regimes != regimes.shift(1)
    transition_points = regime_changes[regime_changes].index

    pre_transition_divs = []
    for tp in transition_points:
        start = tp - pd.Timedelta(days=5)
        pre_window = divergence[(divergence.index >= start) & (divergence.index < tp)]
        if len(pre_window) > 0:
            pre_transition_divs.extend(pre_window.values.tolist())

    stable_divs = divergence[~regime_changes].values
    return np.asarray(pre_transition_divs), np.asarray(stable_divs)


def figure_h2_divergence(feature_matrix: pd.DataFrame, validation: dict, outpath: Path) -> None:
    pre_divs, stable_divs = _h2_distributions(feature_matrix)

    df = pd.DataFrame(
        {
            "value": np.concatenate([pre_divs, stable_divs]),
            "group": ["Pre-transition"] * len(pre_divs) + ["Stable"] * len(stable_divs),
        }
    )

    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.violinplot(
        data=df,
        x="group",
        y="value",
        hue="group",
        inner="quartile",
        cut=0,
        palette=["#ff7f0e", "#1f77b4"],
        legend=False,
        ax=ax,
    )
    ax.set_title("H2 Divergence Distribution: Pre-transition vs Stable")
    ax.set_xlabel("")
    ax.set_ylabel("Cross-asset divergence (std over sent_* columns)")

    h2 = validation["hypotheses"]["H2"]
    annotation = (
        f"Locked run summary: ratio={h2['divergence_ratio']:.2f}x, "
        f"t={h2['t_statistic']:.2f}, p={h2['p_value']:.2e}, d={h2['effect_size']:.2f}"
    )
    fig.text(0.5, 0.01, annotation, ha="center", fontsize=9)

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(outpath, dpi=220, bbox_inches="tight")
    plt.close(fig)


def figure_h3_connectedness(validation: dict, outpath: Path) -> None:
    h3 = validation["hypotheses"]["H3"]

    x = ["Stable regimes", "Transition regimes"]
    y = [h3["stable_regime_tci"], h3["transition_tci"]]

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(x, y, color=["#1f77b4", "#ff7f0e"], width=0.6)
    for b, v in zip(bars, y):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.003, f"{v:.3f}", ha="center", va="bottom", fontsize=10)

    ax.set_ylim(0, max(y) * 1.2)
    ax.set_ylabel("TCI")
    ax.set_title("H3 Connectedness Comparison (full_granger_te mode)")

    txt = (
        f"ANOVA F={h3['anova_f']:.2f}, p={h3['anova_p']:.2e}; "
        f"pre-crash TCI change={h3['pre_crash_tci_change']:.4f}"
    )
    fig.text(0.5, 0.01, txt, ha="center", fontsize=9)

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(outpath, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Draft-1.1 figures from locked artifacts.")
    parser.add_argument(
        "--validation-json",
        default="results/validation/methodology_ab_backend/network_tuning_pyinform/cfg_default/validation_20260216_013107.json",
    )
    parser.add_argument(
        "--locked-h1-json",
        default="results/validation/h1_confirmation/locked_protocol/h1_locked_confirmation_20260216_022558.json",
    )
    parser.add_argument(
        "--feature-matrix",
        default="results/pipeline_output/feature_matrix.csv",
    )
    parser.add_argument(
        "--output-dir",
        default="course_files/images/draft-1.1",
    )
    args = parser.parse_args()

    validation = _load_json(Path(args.validation_json))
    locked_h1 = _load_json(Path(args.locked_h1_json))

    fm = pd.read_csv(args.feature_matrix)
    idx_col = fm.columns[0]
    fm[idx_col] = pd.to_datetime(fm[idx_col])
    fm = fm.rename(columns={idx_col: "date"}).set_index("date").sort_index()

    outdir = Path(args.output_dir)
    _ensure_dir(outdir)

    figure_h1_summary(validation, locked_h1, outdir / "fig_5_5_h1_lead_time_summary_v2.png")
    figure_regime_vix_timeline(fm, outdir / "fig_5_5_regime_vs_vix_covid_v2.png")
    figure_confusion_matrix(validation, outdir / "fig_5_5_transition_confusion_matrix.png")
    figure_h2_divergence(fm, validation, outdir / "fig_5_6_h2_divergence_distribution.png")
    figure_h3_connectedness(validation, outdir / "fig_5_6_h3_connectedness_comparison.png")

    print(f"Generated 5 figures in {outdir}")


if __name__ == "__main__":
    main()
