#!/usr/bin/env python3
"""
Generate Comparative Visualizations for All Backtest Approaches

Creates comprehensive visualizations comparing:
- Rule-Based
- ML-Only
- Ensemble
- Conditional Routing
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set style
plt.style.use("seaborn-v0_8-darkgrid")
COLORS = {
    "rule": "#FF6B6B",
    "ml": "#4ECDC4",
    "ensemble": "#95E1D3",
    "conditional": "#FFD93D",
}


def load_results():
    """Load all backtest results."""
    base_dir = Path("data/processed")

    # Load summaries
    results = {
        "rule": json.load(open(base_dir / "historical_backtests" / "all_events_summary.json")),
        "ml": json.load(open(base_dir / "historical_backtests_ml" / "all_events_ml_summary.json")),
        "ensemble": json.load(open(base_dir / "historical_backtests_ensemble" / "ensemble_summary.json")),
        "conditional": json.load(
            open(base_dir / "historical_backtests_conditional" / "conditional_routing_summary.json")
        ),
    }

    return results


def create_accuracy_comparison(results, output_dir):
    """Create accuracy comparison across all approaches."""
    events = ["COVID Market Crash", "FTX Collapse", "Silicon Valley Bank"]
    event_keys = ["covid", "ftx", "svb"]

    # Prepare data
    data = {
        "Rule-Based": [],
        "ML-Only": [],
        "Ensemble": [],
        "Conditional": [],
    }

    for event_key in event_keys:
        # Rule-based
        rule_event = next((e for e in results["rule"]["events"] if e["event_key"] == event_key), None)
        data["Rule-Based"].append(rule_event["metrics"]["accuracy"] * 100 if rule_event else 0)

        # ML
        ml_event = next((e for e in results["ml"]["events"] if e["event_key"] == event_key), None)
        data["ML-Only"].append(ml_event["metrics"]["accuracy"] * 100 if ml_event else 0)

        # Ensemble
        ens_event = next((e for e in results["ensemble"]["events"] if e["event_key"] == event_key), None)
        data["Ensemble"].append(ens_event["metrics"]["ensemble_accuracy"] * 100 if ens_event else 0)

        # Conditional
        cond_event = next((e for e in results["conditional"]["events"] if e["event_key"] == event_key), None)
        data["Conditional"].append(cond_event["metrics"]["accuracy"] * 100 if cond_event else 0)

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(events))
    width = 0.2

    bars1 = ax.bar(x - 1.5 * width, data["Rule-Based"], width, label="Rule-Based", color=COLORS["rule"])
    bars2 = ax.bar(x - 0.5 * width, data["ML-Only"], width, label="ML-Only", color=COLORS["ml"])
    bars3 = ax.bar(x + 0.5 * width, data["Ensemble"], width, label="Ensemble", color=COLORS["ensemble"])
    bars4 = ax.bar(x + 1.5 * width, data["Conditional"], width, label="Conditional", color=COLORS["conditional"])

    # Add value labels on bars
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

    ax.set_xlabel("Crisis Event", fontsize=12, fontweight="bold")
    ax.set_ylabel("Accuracy (%)", fontsize=12, fontweight="bold")
    ax.set_title("Regime Classification Accuracy Comparison\nAcross Historical Crisis Events", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(events)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(output_dir / "accuracy_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created accuracy comparison chart")


def create_overall_performance_table(results, output_dir):
    """Create overall performance summary table."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")

    # Prepare data
    approaches = ["Rule-Based", "ML-Only", "Ensemble", "Conditional"]
    covid = [4.9, 80.5, 80.5, 76.7]
    ftx = [23.8, 0.0, 0.0, 20.0]
    svb = [30.4, 47.8, 47.8, 64.5]
    average = [19.7, 42.8, 42.8, 53.7]

    table_data = []
    for i, approach in enumerate(approaches):
        table_data.append([approach, f"{covid[i]:.1f}%", f"{ftx[i]:.1f}%", f"{svb[i]:.1f}%", f"{average[i]:.1f}%"])

    table = ax.table(
        cellText=table_data,
        colLabels=["Approach", "COVID", "FTX", "SVB", "Average"],
        cellLoc="center",
        loc="center",
        colWidths=[0.25, 0.15, 0.15, 0.15, 0.15],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    # Style header
    for i in range(5):
        table[(0, i)].set_facecolor("#4ECDC4")
        table[(0, i)].set_text_props(weight="bold", color="white")

    # Highlight best values
    for i in range(4):
        # COVID (row 2 = ML/Ensemble)
        if i == 1 or i == 2:
            table[(i + 1, 1)].set_facecolor("#C8E6C9")
        # FTX (row 1 = Rule-Based)
        if i == 0:
            table[(i + 1, 2)].set_facecolor("#C8E6C9")
        # SVB (row 4 = Conditional)
        if i == 3:
            table[(i + 1, 3)].set_facecolor("#C8E6C9")
        # Average (row 4 = Conditional)
        if i == 3:
            table[(i + 1, 4)].set_facecolor("#FFD54F")
            table[(i + 1, 4)].set_text_props(weight="bold")

    plt.title("Overall Performance Summary\n(Highlighted = Best Performance)", fontsize=14, fontweight="bold", pad=20)
    plt.savefig(output_dir / "performance_table.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created performance summary table")


def create_routing_decision_chart(results, output_dir):
    """Create routing decision visualization."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Event characteristics
    events = ["COVID", "FTX", "SVB"]
    vix_max = [82.69, 26.09, 26.52]
    vix_spike = [24.86, 3.57, 5.69]
    divergence = [0.138, 0.162, 0.320]
    routing = ["ML", "Ensemble", "Ensemble"]

    # Chart 1: VIX characteristics
    x = np.arange(len(events))
    width = 0.35

    bars1 = ax1.bar(x - width / 2, vix_max, width, label="VIX Max", color="#FF6B6B")
    bars2 = ax1.bar(x + width / 2, vix_spike, width, label="VIX Spike (3d)", color="#4ECDC4")

    # Add routing labels
    for i, (bar1, bar2, route) in enumerate(zip(bars1, bars2, routing)):
        height = max(bar1.get_height(), bar2.get_height())
        ax1.text(
            x[i],
            height + 5,
            f"→ {route}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=COLORS[route.lower()], alpha=0.7),
        )

    ax1.axhline(y=30, color="red", linestyle="--", linewidth=2, label="VIX 30 (Extreme)", alpha=0.7)
    ax1.axhline(y=5, color="orange", linestyle="--", linewidth=2, label="Spike 5 (Rapid)", alpha=0.7)

    ax1.set_xlabel("Crisis Event", fontsize=12, fontweight="bold")
    ax1.set_ylabel("VIX Level / Change", fontsize=12, fontweight="bold")
    ax1.set_title("VIX Characteristics & Routing Decision", fontsize=13, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(events)
    ax1.legend(loc="upper right", fontsize=10)
    ax1.grid(axis="y", alpha=0.3)

    # Chart 2: Divergence and routing accuracy
    bars = ax2.bar(events, divergence, color=[COLORS[r.lower()] for r in routing], alpha=0.7, edgecolor="black")
    ax2.axhline(y=0.35, color="purple", linestyle="--", linewidth=2, label="High Divergence (0.35)", alpha=0.7)

    # Add accuracy labels
    accuracies = [76.7, 20.0, 64.5]
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{acc:.1f}%",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax2.set_xlabel("Crisis Event", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Cross-Asset Divergence", fontsize=12, fontweight="bold")
    ax2.set_title("Cross-Asset Divergence & Accuracy", fontsize=13, fontweight="bold")
    ax2.legend(loc="upper right", fontsize=10)
    ax2.grid(axis="y", alpha=0.3)
    ax2.set_ylim(0, 0.4)

    plt.tight_layout()
    plt.savefig(output_dir / "routing_decision_analysis.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created routing decision analysis chart")


def create_confidence_comparison(results, output_dir):
    """Create confidence comparison chart."""
    fig, ax = plt.subplots(figsize=(12, 7))

    events = ["COVID", "FTX", "SVB"]
    event_keys = ["covid", "ftx", "svb"]

    # Prepare data
    rule_conf = []
    ml_conf = []
    ensemble_conf = []
    cond_conf = []

    for event_key in event_keys:
        rule_event = next((e for e in results["rule"]["events"] if e["event_key"] == event_key), None)
        rule_conf.append(
            rule_event["metrics"].get("avg_confidence", 0.6) * 100 if rule_event else 0
        )  # Default 60% for rule-based

        ml_event = next((e for e in results["ml"]["events"] if e["event_key"] == event_key), None)
        ml_conf.append(ml_event["metrics"].get("avg_confidence", 0) * 100 if ml_event else 0)

        ens_event = next((e for e in results["ensemble"]["events"] if e["event_key"] == event_key), None)
        ensemble_conf.append(ens_event["metrics"].get("avg_confidence", 0) * 100 if ens_event else 0)

        cond_event = next((e for e in results["conditional"]["events"] if e["event_key"] == event_key), None)
        cond_conf.append(cond_event["metrics"].get("avg_confidence", 0) * 100 if cond_event else 0)

    x = np.arange(len(events))
    width = 0.2

    ax.bar(x - 1.5 * width, rule_conf, width, label="Rule-Based", color=COLORS["rule"])
    ax.bar(x - 0.5 * width, ml_conf, width, label="ML-Only", color=COLORS["ml"])
    ax.bar(x + 0.5 * width, ensemble_conf, width, label="Ensemble", color=COLORS["ensemble"])
    ax.bar(x + 1.5 * width, cond_conf, width, label="Conditional", color=COLORS["conditional"])

    ax.set_xlabel("Crisis Event", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Confidence (%)", fontsize=12, fontweight="bold")
    ax.set_title("Prediction Confidence Comparison\nAcross Approaches and Events", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(events)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(output_dir / "confidence_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created confidence comparison chart")


def create_early_warning_chart(results, output_dir):
    """Create early warning performance chart."""
    fig, ax = plt.subplots(figsize=(12, 7))

    events = ["COVID", "FTX", "SVB"]
    event_keys = ["covid", "ftx", "svb"]

    # Prepare data
    data = {"Rule-Based": [], "ML-Only": [], "Ensemble": [], "Conditional": []}

    for event_key in event_keys:
        rule_event = next((e for e in results["rule"]["events"] if e["event_key"] == event_key), None)
        data["Rule-Based"].append(
            rule_event["detection"]["early_warning_days"] if rule_event and rule_event["detection"]["peak_detected"] else 0
        )

        ml_event = next((e for e in results["ml"]["events"] if e["event_key"] == event_key), None)
        data["ML-Only"].append(
            ml_event["detection"]["early_warning_days"] if ml_event and ml_event["detection"]["peak_detected"] else 0
        )

        ens_event = next((e for e in results["ensemble"]["events"] if e["event_key"] == event_key), None)
        data["Ensemble"].append(
            ens_event["detection"]["early_warning_days"] if ens_event and ens_event["detection"]["peak_detected"] else 0
        )

        cond_event = next((e for e in results["conditional"]["events"] if e["event_key"] == event_key), None)
        data["Conditional"].append(
            cond_event["detection"]["early_warning_days"]
            if cond_event and cond_event["detection"]["peak_detected"]
            else 0
        )

    x = np.arange(len(events))
    width = 0.2

    bars1 = ax.bar(x - 1.5 * width, data["Rule-Based"], width, label="Rule-Based", color=COLORS["rule"])
    bars2 = ax.bar(x - 0.5 * width, data["ML-Only"], width, label="ML-Only", color=COLORS["ml"])
    bars3 = ax.bar(x + 0.5 * width, data["Ensemble"], width, label="Ensemble", color=COLORS["ensemble"])
    bars4 = ax.bar(x + 1.5 * width, data["Conditional"], width, label="Conditional", color=COLORS["conditional"])

    # Add value labels
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{int(height)}d",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                )

    ax.set_xlabel("Crisis Event", fontsize=12, fontweight="bold")
    ax.set_ylabel("Days Before Peak Detection", fontsize=12, fontweight="bold")
    ax.set_title("Early Warning Performance\n(Days Before Crisis Peak Detected)", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(events)
    ax.legend(loc="upper right", fontsize=11)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "early_warning_performance.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created early warning performance chart")


def create_methodology_flowchart(output_dir):
    """Create conditional routing methodology flowchart."""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # Title
    ax.text(5, 9.5, "Conditional Routing Methodology", ha="center", fontsize=16, fontweight="bold")

    # Event Analysis Box
    ax.add_patch(plt.Rectangle((2, 7.5), 6, 1.5, facecolor="#E3F2FD", edgecolor="black", linewidth=2))
    ax.text(5, 8.7, "Event Characteristic Analysis", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 8.3, "VIX Max, VIX Spike Rate, Cross-Asset Divergence", ha="center", fontsize=9)
    ax.text(5, 7.9, "Sentiment Momentum, Volatility Patterns", ha="center", fontsize=9)

    # Arrow down
    ax.arrow(5, 7.5, 0, -0.8, head_width=0.2, head_length=0.1, fc="black", ec="black")

    # Decision Box
    ax.add_patch(plt.Rectangle((2, 5.5), 6, 1.5, facecolor="#FFF9C4", edgecolor="black", linewidth=2))
    ax.text(5, 6.6, "Routing Decision Logic", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 6.2, "IF VIX > 30 AND Spike > 5: Extreme Systemic → ML", ha="center", fontsize=9)
    ax.text(5, 5.9, "ELIF VIX < 25 AND Divergence > 0.35: Sector-Specific → Rule", ha="center", fontsize=9)
    ax.text(5, 5.6, "ELSE: Mixed Characteristics → Ensemble", ha="center", fontsize=9)

    # Arrows to classifiers
    ax.arrow(3.5, 5.5, -1.5, -1.3, head_width=0.2, head_length=0.1, fc="black", ec="black")
    ax.arrow(5, 5.5, 0, -1.3, head_width=0.2, head_length=0.1, fc="black", ec="black")
    ax.arrow(6.5, 5.5, 1.5, -1.3, head_width=0.2, head_length=0.1, fc="black", ec="black")

    # Classifier boxes
    # ML Classifier
    ax.add_patch(plt.Rectangle((0.5, 2.5), 2.5, 1.5, facecolor=COLORS["ml"], edgecolor="black", linewidth=2, alpha=0.7))
    ax.text(1.75, 3.6, "ML Classifier", ha="center", fontsize=11, fontweight="bold")
    ax.text(1.75, 3.2, "Trained on CISS,", ha="center", fontsize=8)
    ax.text(1.75, 2.9, "VIX, Sentiment", ha="center", fontsize=8)
    ax.text(1.75, 2.6, "→ 99.45% train acc", ha="center", fontsize=8)

    # Rule-Based Classifier
    ax.add_patch(plt.Rectangle((3.75, 2.5), 2.5, 1.5, facecolor=COLORS["rule"], edgecolor="black", linewidth=2, alpha=0.7))
    ax.text(5, 3.6, "Rule-Based", ha="center", fontsize=11, fontweight="bold")
    ax.text(5, 3.2, "Volume spikes,", ha="center", fontsize=8)
    ax.text(5, 2.9, "Divergence,", ha="center", fontsize=8)
    ax.text(5, 2.6, "VIX thresholds", ha="center", fontsize=8)

    # Ensemble Classifier
    ax.add_patch(
        plt.Rectangle((7, 2.5), 2.5, 1.5, facecolor=COLORS["ensemble"], edgecolor="black", linewidth=2, alpha=0.7)
    )
    ax.text(8.25, 3.6, "Ensemble", ha="center", fontsize=11, fontweight="bold")
    ax.text(8.25, 3.2, "Weighted voting:", ha="center", fontsize=8)
    ax.text(8.25, 2.9, "60% ML + 40% Rule", ha="center", fontsize=8)
    ax.text(8.25, 2.6, "Dynamic adjust", ha="center", fontsize=8)

    # Arrows to final prediction
    ax.arrow(1.75, 2.5, 0.5, -0.8, head_width=0.2, head_length=0.1, fc="black", ec="black")
    ax.arrow(5, 2.5, 0, -0.8, head_width=0.2, head_length=0.1, fc="black", ec="black")
    ax.arrow(8.25, 2.5, -0.5, -0.8, head_width=0.2, head_length=0.1, fc="black", ec="black")

    # Final prediction box
    ax.add_patch(plt.Rectangle((3, 0.3), 4, 1.2, facecolor=COLORS["conditional"], edgecolor="black", linewidth=2))
    ax.text(5, 1.2, "Regime Classification", ha="center", fontsize=12, fontweight="bold")
    ax.text(5, 0.8, "Risk On / Transition / Risk Off", ha="center", fontsize=10)
    ax.text(5, 0.5, "+ Confidence Score", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / "methodology_flowchart.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Created methodology flowchart")


def main():
    """Generate all comparative visualizations."""
    print("\n" + "=" * 60)
    print("GENERATING COMPARATIVE VISUALIZATIONS")
    print("=" * 60 + "\n")

    # Create output directory
    output_dir = Path("data/processed/comparative_visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load results
    print("Loading backtest results...")
    results = load_results()

    # Generate visualizations
    print("\nGenerating visualizations...")
    create_accuracy_comparison(results, output_dir)
    create_overall_performance_table(results, output_dir)
    create_routing_decision_chart(results, output_dir)
    create_confidence_comparison(results, output_dir)
    create_early_warning_chart(results, output_dir)
    create_methodology_flowchart(output_dir)

    print(f"\n✅ All visualizations saved to: {output_dir}")
    print("\nGenerated files:")
    print("  1. accuracy_comparison.png")
    print("  2. performance_table.png")
    print("  3. routing_decision_analysis.png")
    print("  4. confidence_comparison.png")
    print("  5. early_warning_performance.png")
    print("  6. methodology_flowchart.png")


if __name__ == "__main__":
    main()
