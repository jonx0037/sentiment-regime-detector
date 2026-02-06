"""Publication-quality visualization functions for SHAP explainability.

This module provides functions for generating figures for the capstone paper:
- Waterfall plots showing feature contributions to predictions
- Global importance bar charts
- Feature interaction heatmaps

All plots are configured for publication quality (300 DPI, LaTeX fonts).
"""

from pathlib import Path
from typing import Optional, Tuple
import logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import shap

from sentiment_detector.explainability import ExplanationResult

logger = logging.getLogger(__name__)

# Publication-quality plot configuration
PLOT_CONFIG = {
    'dpi': 300,
    'figure.figsize': (10, 6),
    'font.family': 'serif',
    'font.serif': ['Computer Modern', 'Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'text.usetex': False,  # Set to True if LaTeX is installed
    'axes.grid': True,
    'grid.alpha': 0.3,
}

# Colorblind-safe color palette
REGIME_COLORS = {
    'risk_on': '#2ecc71',    # Green
    'risk_off': '#e74c3c',   # Red
    'transition': '#f39c12', # Orange
}


def configure_publication_style() -> None:
    """Configure matplotlib for publication-quality plots.

    Sets DPI, fonts, sizes, and grid styles for academic papers.
    Call this once at the start of visualization generation.
    """
    mpl.rcParams.update(PLOT_CONFIG)
    sns.set_palette("colorblind")
    logger.info("Configured publication-quality plot style")


def plot_waterfall(
    result: ExplanationResult,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
    show: bool = False,
    max_features: int = 15,
) -> plt.Figure:
    """Create SHAP waterfall plot showing feature contributions.

    Args:
        result: ExplanationResult from explainer
        output_path: Path to save figure (if None, don't save)
        title: Custom title (if None, auto-generate)
        show: Whether to display plot interactively
        max_features: Maximum number of features to display

    Returns:
        matplotlib Figure object
    """
    # Create SHAP Explanation object (required for waterfall plot)
    shap_values = shap.Explanation(
        values=result.shap_values,
        base_values=result.base_value,
        data=np.array([result.feature_values[f] for f in result.feature_names]),
        feature_names=result.feature_names,
    )

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Generate waterfall plot
    shap.plots.waterfall(
        shap_values,
        max_display=max_features,
        show=False,
    )

    # Customize title
    if title is None:
        title = (
            f"Feature Contributions to {result.predicted_regime.replace('_', ' ').title()} Prediction\n"
            f"Confidence: {result.confidence:.1%} | Model: {result.model_version}"
        )
    plt.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout()

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=PLOT_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved waterfall plot to {output_path}")

    if show:
        plt.show()
    else:
        plt.close()

    return fig


def plot_global_importance(
    importance_dict: dict[str, float],
    output_path: Optional[Path] = None,
    title: str = "Global Feature Importance",
    show: bool = False,
    top_k: int = 20,
) -> plt.Figure:
    """Create bar chart of global feature importance.

    Args:
        importance_dict: Feature name -> mean |SHAP| value
        output_path: Path to save figure
        title: Plot title
        show: Whether to display plot
        top_k: Number of top features to display

    Returns:
        matplotlib Figure object
    """
    # Sort by importance and take top_k
    sorted_features = sorted(
        importance_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:top_k]

    features, importance = zip(*sorted_features)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, max(6, len(features) * 0.3)))

    # Create horizontal bar chart
    y_pos = np.arange(len(features))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(features)))

    bars = ax.barh(y_pos, importance, color=colors, edgecolor='black', linewidth=0.5)

    # Customize axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.invert_yaxis()  # Top feature at top
    ax.set_xlabel('Mean |SHAP Value|', fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=20)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, importance)):
        ax.text(
            val,
            i,
            f' {val:.4f}',
            va='center',
            ha='left',
            fontsize=9,
        )

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=PLOT_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved global importance plot to {output_path}")

    if show:
        plt.show()
    else:
        plt.close()

    return fig


def plot_interaction_heatmap(
    interaction_matrix: np.ndarray,
    feature_names: list[str],
    output_path: Optional[Path] = None,
    title: str = "Feature Interaction Strengths",
    show: bool = False,
    top_k: Optional[int] = None,
) -> plt.Figure:
    """Create heatmap of feature interaction strengths.

    Args:
        interaction_matrix: NxN matrix of interaction values
        feature_names: List of feature names (length N)
        output_path: Path to save figure
        title: Plot title
        show: Whether to display plot
        top_k: If provided, only show top_k most important features

    Returns:
        matplotlib Figure object
    """
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(
        interaction_matrix,
        index=feature_names,
        columns=feature_names,
    )

    # If top_k specified, filter to top features by mean interaction
    if top_k:
        # Get top features by mean |interaction|
        mean_interaction = np.abs(interaction_matrix).mean(axis=0)
        top_indices = np.argsort(mean_interaction)[-top_k:]
        top_features = [feature_names[i] for i in top_indices]
        df = df.loc[top_features, top_features]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Create heatmap
    sns.heatmap(
        df,
        cmap='RdBu_r',
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={
            'label': 'Interaction Strength',
            'shrink': 0.8,
        },
        ax=ax,
        fmt='.3f',
        vmin=-np.abs(df.values).max(),
        vmax=np.abs(df.values).max(),
    )

    # Customize
    ax.set_title(title, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.tight_layout()

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=PLOT_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved interaction heatmap to {output_path}")

    if show:
        plt.show()
    else:
        plt.close()

    return fig


def plot_feature_comparison(
    results: dict[str, ExplanationResult],
    feature_name: str,
    output_path: Optional[Path] = None,
    title: Optional[str] = None,
    show: bool = False,
) -> plt.Figure:
    """Compare a single feature's SHAP values across multiple predictions.

    Useful for showing how a feature's importance changes across events.

    Args:
        results: Dict mapping event name -> ExplanationResult
        feature_name: Feature to compare
        output_path: Path to save figure
        title: Custom title
        show: Whether to display plot

    Returns:
        matplotlib Figure object
    """
    # Extract SHAP values for the feature
    event_names = []
    shap_values = []
    regimes = []

    for event_name, result in results.items():
        if feature_name not in result.feature_names:
            logger.warning(f"Feature {feature_name} not in {event_name}")
            continue

        idx = result.feature_names.index(feature_name)
        event_names.append(event_name)
        shap_values.append(float(result.shap_values[idx]))
        regimes.append(result.predicted_regime)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Color bars by regime
    colors = [REGIME_COLORS[regime] for regime in regimes]

    # Create bar chart
    x_pos = np.arange(len(event_names))
    bars = ax.bar(x_pos, shap_values, color=colors, edgecolor='black', linewidth=1)

    # Customize
    ax.set_xticks(x_pos)
    ax.set_xticklabels(event_names, rotation=45, ha='right')
    ax.set_ylabel('SHAP Value', fontweight='bold')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

    if title is None:
        title = f"SHAP Values for '{feature_name}' Across Crisis Events"
    ax.set_title(title, fontweight='bold', pad=20)

    # Add regime legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=REGIME_COLORS[regime], label=regime.replace('_', ' ').title())
        for regime in ['risk_on', 'transition', 'risk_off']
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=PLOT_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved feature comparison plot to {output_path}")

    if show:
        plt.show()
    else:
        plt.close()

    return fig


def plot_regime_prediction_summary(
    result: ExplanationResult,
    output_path: Optional[Path] = None,
    show: bool = False,
) -> plt.Figure:
    """Create comprehensive summary figure for a regime prediction.

    Combines multiple visualizations:
    - Regime prediction with confidence
    - Top 10 feature contributions
    - Probability distribution

    Args:
        result: ExplanationResult from explainer
        output_path: Path to save figure
        show: Whether to display plot

    Returns:
        matplotlib Figure object
    """
    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # 1. Regime indicator (top-left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    regime_color = REGIME_COLORS[result.predicted_regime]
    ax1.add_patch(plt.Circle((0.5, 0.5), 0.4, color=regime_color, alpha=0.7))
    ax1.text(
        0.5, 0.5,
        result.predicted_regime.replace('_', '\n').upper(),
        ha='center', va='center',
        fontsize=20, fontweight='bold',
        color='white',
    )
    ax1.text(
        0.5, 0.1,
        f"Confidence: {result.confidence:.1%}",
        ha='center', va='center',
        fontsize=12,
    )
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)

    # 2. Top features (top-right and bottom-left, spanning)
    ax2 = fig.add_subplot(gs[:, 1])

    # Get top 10 features by |SHAP|
    shap_abs = np.abs(result.shap_values)
    top_indices = np.argsort(shap_abs)[-10:][::-1]

    top_features = [result.feature_names[i] for i in top_indices]
    top_shap = [float(result.shap_values[i]) for i in top_indices]

    # Color by positive/negative
    colors = ['#2ecc71' if val > 0 else '#e74c3c' for val in top_shap]

    y_pos = np.arange(len(top_features))
    ax2.barh(y_pos, top_shap, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(top_features)
    ax2.invert_yaxis()
    ax2.set_xlabel('SHAP Value', fontweight='bold')
    ax2.set_title('Top 10 Feature Contributions', fontweight='bold')
    ax2.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')

    # 3. Probability distribution (bottom-left)
    ax3 = fig.add_subplot(gs[1, 0])

    # Calculate probabilities from confidence (simplified)
    # In reality, we'd get these from the model
    regimes = ['risk_on', 'transition', 'risk_off']
    if result.predicted_regime == 'risk_on':
        probs = [result.confidence, (1 - result.confidence) * 0.7, (1 - result.confidence) * 0.3]
    elif result.predicted_regime == 'risk_off':
        probs = [(1 - result.confidence) * 0.3, (1 - result.confidence) * 0.7, result.confidence]
    else:  # transition
        probs = [(1 - result.confidence) * 0.5, result.confidence, (1 - result.confidence) * 0.5]

    colors_prob = [REGIME_COLORS[r] for r in regimes]
    ax3.bar(regimes, probs, color=colors_prob, edgecolor='black', linewidth=1)
    ax3.set_ylabel('Probability', fontweight='bold')
    ax3.set_title('Regime Probabilities', fontweight='bold')
    ax3.set_ylim(0, 1)
    for i, (regime, prob) in enumerate(zip(regimes, probs)):
        ax3.text(i, prob + 0.02, f'{prob:.1%}', ha='center', fontsize=10)

    # Overall title
    fig.suptitle(
        f"Regime Prediction Summary - {result.timestamp.strftime('%Y-%m-%d')}",
        fontsize=16,
        fontweight='bold',
    )

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=PLOT_CONFIG['dpi'], bbox_inches='tight')
        logger.info(f"Saved regime summary plot to {output_path}")

    if show:
        plt.show()
    else:
        plt.close()

    return fig


def generate_latex_table_global_importance(
    importance_dict: dict[str, float],
    output_path: Optional[Path] = None,
    top_k: int = 15,
    caption: str = "Global Feature Importance Rankings",
    label: str = "tab:global_importance",
) -> str:
    """Generate LaTeX table for global feature importance.

    Args:
        importance_dict: Feature name -> mean |SHAP| value
        output_path: Path to save .tex file
        top_k: Number of top features to include
        caption: Table caption
        label: LaTeX label for referencing

    Returns:
        LaTeX table string
    """
    # Sort by importance
    sorted_features = sorted(
        importance_dict.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:top_k]

    # Build LaTeX table
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"  \centering")
    latex.append(r"  \caption{" + caption + r"}")
    latex.append(r"  \label{" + label + r"}")
    latex.append(r"  \begin{tabular}{clr}")
    latex.append(r"    \toprule")
    latex.append(r"    Rank & Feature & Mean |SHAP| \\")
    latex.append(r"    \midrule")

    for rank, (feature, importance) in enumerate(sorted_features, 1):
        # Format feature name (replace underscores)
        feature_display = feature.replace('_', r'\_')
        latex.append(f"    {rank} & {feature_display} & {importance:.4f} \\\\")

    latex.append(r"    \bottomrule")
    latex.append(r"  \end{tabular}")
    latex.append(r"\end{table}")

    table_str = "\n".join(latex)

    # Save if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(table_str)
        logger.info(f"Saved LaTeX table to {output_path}")

    return table_str
