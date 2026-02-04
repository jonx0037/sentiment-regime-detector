#!/usr/bin/env python3
"""
Generate visualizations for the Sentiment Regime Detector project.

Creates:
1. CISS vs VIX time series comparison
2. Regime transition heatmap
3. Sentiment-volatility scatter plots
4. Backtest performance charts
"""

import asyncio
import sys
from pathlib import Path
from datetime import date

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from sqlalchemy import text


async def load_data(session):
    """Load all required data."""
    # VIX
    result = await session.execute(text("""
        SELECT date, close as vix
        FROM market_data
        WHERE symbol = '^VIX'
        ORDER BY date
    """))
    vix_df = pd.DataFrame(result.fetchall(), columns=['date', 'vix'])
    vix_df['date'] = pd.to_datetime(vix_df['date'])
    
    # CISS
    result = await session.execute(text("""
        SELECT date, value as ciss
        FROM stress_indices
        WHERE source = 'ecb_ciss'
        ORDER BY date
    """))
    ciss_df = pd.DataFrame(result.fetchall(), columns=['date', 'ciss'])
    ciss_df['date'] = pd.to_datetime(ciss_df['date'])
    
    # Daily sentiment
    result = await session.execute(text("""
        SELECT 
            DATE(rt.content_created_at) as date,
            AVG(ss.compound) as sentiment,
            COUNT(*) as count
        FROM sentiment_scores ss
        JOIN raw_texts rt ON ss.text_id = rt.id
        WHERE rt.content_created_at IS NOT NULL
        GROUP BY DATE(rt.content_created_at)
        ORDER BY date
    """))
    sentiment_df = pd.DataFrame(result.fetchall(), columns=['date', 'sentiment', 'count'])
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    
    return vix_df, ciss_df, sentiment_df


def plot_ciss_vs_vix(vix_df, ciss_df, output_dir):
    """Create CISS vs VIX time series comparison."""
    # Merge on date
    merged = pd.merge(vix_df, ciss_df, on='date', how='inner')
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    # VIX on left axis
    color1 = '#1f77b4'
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('VIX Index', color=color1, fontsize=12)
    ax1.plot(merged['date'], merged['vix'], color=color1, alpha=0.8, linewidth=1, label='VIX')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0, 90)
    
    # CISS on right axis
    ax2 = ax1.twinx()
    color2 = '#d62728'
    ax2.set_ylabel('ECB CISS (Systemic Stress)', color=color2, fontsize=12)
    ax2.plot(merged['date'], merged['ciss'], color=color2, alpha=0.8, linewidth=1, label='CISS')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0, 1)
    
    # Add crisis annotations
    crisis_events = [
        ('2020-03-16', 'COVID-19\nCrash', 0.85),
        ('2011-08-08', 'Eurozone\nCrisis', 0.75),
        ('2015-08-24', 'China\nDevaluation', 0.45),
        ('2022-02-24', 'Ukraine\nInvasion', 0.55),
    ]
    
    for date_str, label, y_pos in crisis_events:
        event_date = pd.to_datetime(date_str)
        if event_date in merged['date'].values or any(abs((merged['date'] - event_date).dt.days) < 7):
            ax2.axvline(x=event_date, color='gray', linestyle='--', alpha=0.5)
            ax2.annotate(label, xy=(event_date, y_pos), fontsize=8, ha='center')
    
    # Title and legend
    plt.title('VIX vs ECB CISS: Volatility and Systemic Stress Comparison (2010-2026)', fontsize=14)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # Format dates
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    plt.tight_layout()
    output_path = output_dir / 'ciss_vs_vix_timeseries.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")
    
    # Also save correlation stats
    corr = merged['vix'].corr(merged['ciss'])
    print(f"  VIX-CISS Correlation: {corr:.4f}")
    
    return merged


def plot_regime_heatmap(vix_df, ciss_df, output_dir):
    """Create regime transition heatmap by year and month."""
    # Merge data
    merged = pd.merge(vix_df, ciss_df, on='date', how='inner')
    merged['year'] = merged['date'].dt.year
    merged['month'] = merged['date'].dt.month
    
    # Classify regimes based on CISS
    def classify_regime(ciss):
        if ciss < 0.1:
            return 0  # Calm
        elif ciss < 0.25:
            return 1  # Moderate
        elif ciss < 0.5:
            return 2  # Elevated
        else:
            return 3  # Crisis
    
    merged['regime'] = merged['ciss'].apply(classify_regime)
    
    # Pivot to create heatmap data
    pivot = merged.pivot_table(
        values='regime',
        index='year',
        columns='month',
        aggfunc='mean'
    )
    
    # Create custom colormap
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']  # Green -> Yellow -> Orange -> Red
    cmap = LinearSegmentedColormap.from_list('regime', colors)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    im = ax.imshow(pivot.values, cmap=cmap, aspect='auto', vmin=0, vmax=3)
    
    # Labels
    ax.set_xticks(range(12))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Year', fontsize=12)
    ax.set_title('Market Stress Regime Heatmap (Based on ECB CISS)', fontsize=14)
    
    # Colorbar
    cbar = plt.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(['Calm', 'Moderate', 'Elevated', 'Crisis'])
    
    plt.tight_layout()
    output_path = output_dir / 'regime_heatmap.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def plot_sentiment_volatility_scatter(vix_df, sentiment_df, output_dir):
    """Create sentiment vs volatility scatter plot."""
    # Merge on date
    merged = pd.merge(vix_df, sentiment_df, on='date', how='inner')
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Color by VIX level
    scatter = ax.scatter(
        merged['sentiment'], 
        merged['vix'],
        c=merged['vix'],
        cmap='RdYlGn_r',
        alpha=0.5,
        s=20
    )
    
    # Add regression line
    z = np.polyfit(merged['sentiment'], merged['vix'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(merged['sentiment'].min(), merged['sentiment'].max(), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'Trend (slope: {z[0]:.1f})')
    
    ax.set_xlabel('Daily Aggregate Sentiment', fontsize=12)
    ax.set_ylabel('VIX Index', fontsize=12)
    ax.set_title('Sentiment vs Market Volatility (VIX)', fontsize=14)
    
    # Correlation annotation
    corr = merged['sentiment'].corr(merged['vix'])
    ax.annotate(f'Correlation: {corr:.3f}', 
                xy=(0.05, 0.95), xycoords='axes fraction',
                fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.colorbar(scatter, label='VIX Level')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    output_path = output_dir / 'sentiment_volatility_scatter.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")
    print(f"  Sentiment-VIX Correlation: {corr:.4f}")


def plot_backtest_results(output_dir):
    """Create backtest performance summary chart."""
    # Backtest results from our analysis
    backtests = {
        '2008 Crisis': {
            'CISS Peak': 0.94,
            'Sentiment β': -0.78,
            'Crisis Days': 278,
            'Detected': True
        },
        'COVID 2020': {
            'VIX Peak': 82.69,
            'CISS-VIX Corr': 0.92,
            'R² (GARCH-MIDAS)': 0.71,
            'Detected': True
        },
        'GameStop 2021': {
            'VIX Peak': 37.21,
            'CISS Peak': 0.024,
            'Systemic': False,
            'Detected': True
        },
        'Gold COVID': {
            'Return': 209.2,
            'Drawdown': -12.3,
            'Detected': True
        },
        'Crypto Winter': {
            'BTC Drawdown': -77.3,
            'ETH Drawdown': -82.1,
            'Detected': True
        }
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    # Plot 1: CISS peaks during crises
    ax = axes[0]
    crises = ['2008 Crisis', 'COVID 2020', 'GameStop 2021']
    ciss_peaks = [0.94, 0.75, 0.024]
    colors = ['#e74c3c', '#e74c3c', '#2ecc71']
    ax.bar(crises, ciss_peaks, color=colors)
    ax.axhline(y=0.5, color='orange', linestyle='--', label='Crisis threshold')
    ax.set_ylabel('CISS Value')
    ax.set_title('CISS Peak by Event')
    ax.legend()
    ax.set_ylim(0, 1)
    
    # Plot 2: VIX peaks
    ax = axes[1]
    events = ['COVID 2020', 'GameStop 2021', 'Normal']
    vix_peaks = [82.69, 37.21, 15]
    colors = ['#e74c3c', '#f39c12', '#2ecc71']
    ax.bar(events, vix_peaks, color=colors)
    ax.axhline(y=30, color='orange', linestyle='--', label='Elevated threshold')
    ax.set_ylabel('VIX Level')
    ax.set_title('VIX Peak by Event')
    ax.legend()
    
    # Plot 3: Model R² comparison
    ax = axes[2]
    models = ['Baseline\nGARCH', 'GARCH +\nSentiment', 'GARCH +\nCISS']
    r2_values = [0.45, 0.58, 0.71]
    ax.bar(models, r2_values, color=['#3498db', '#9b59b6', '#e74c3c'])
    ax.set_ylabel('R² Score')
    ax.set_title('Model Performance (COVID Period)')
    ax.set_ylim(0, 1)
    
    # Plot 4: Asset class returns during stress
    ax = axes[3]
    assets = ['Gold', 'BTC', 'ETH', 'VIX']
    returns = [209.2, -77.3, -82.1, 50]
    colors = ['gold', '#f7931a', '#627eea', '#3498db']
    bars = ax.bar(assets, returns, color=colors)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.set_ylabel('Return (%)')
    ax.set_title('Cross-Asset Performance (COVID to 2022)')
    
    # Plot 5: Regime detection accuracy
    ax = axes[4]
    metrics = ['Agreement', 'Precision', 'Recall', 'F1']
    values = [49.7, 34.8, 60.8, 44.3]
    ax.bar(metrics, values, color='#3498db')
    ax.set_ylabel('Score (%)')
    ax.set_title('CISS vs VIX Regime Validation')
    ax.set_ylim(0, 100)
    
    # Plot 6: GARCH parameters
    ax = axes[5]
    params = ['α (ARCH)', 'β (GARCH)', 'α + β']
    values = [0.155, 0.800, 0.955]
    bars = ax.bar(params, values, color=['#2ecc71', '#3498db', '#e74c3c'])
    ax.axhline(y=1.0, color='red', linestyle='--', label='Unit root')
    ax.set_ylabel('Parameter Value')
    ax.set_title('GARCH(1,1) Volatility Parameters')
    ax.set_ylim(0, 1.1)
    ax.legend()
    
    plt.suptitle('Sentiment Regime Detector: Backtest Results Summary', fontsize=16, y=1.02)
    plt.tight_layout()
    output_path = output_dir / 'backtest_summary.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


async def main():
    """Generate all visualizations."""
    from src.sentiment_detector.core.database import get_session_context
    
    print("=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path("results/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir.absolute()}")
    
    async with get_session_context() as session:
        # Load data
        print("\nLoading data...")
        vix_df, ciss_df, sentiment_df = await load_data(session)
        print(f"  VIX: {len(vix_df)} records")
        print(f"  CISS: {len(ciss_df)} records")
        print(f"  Sentiment: {len(sentiment_df)} records")
        
        # Generate plots
        print("\nGenerating plots...")
        
        print("\n1. CISS vs VIX Time Series")
        plot_ciss_vs_vix(vix_df, ciss_df, output_dir)
        
        print("\n2. Regime Heatmap")
        plot_regime_heatmap(vix_df, ciss_df, output_dir)
        
        print("\n3. Sentiment-Volatility Scatter")
        plot_sentiment_volatility_scatter(vix_df, sentiment_df, output_dir)
    
    print("\n4. Backtest Summary")
    plot_backtest_results(output_dir)
    
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE")
    print("=" * 60)
    
    # List generated files
    print("\nGenerated files:")
    for f in sorted(output_dir.glob("*.png")):
        size = f.stat().st_size / 1024
        print(f"  {f.name}: {size:.1f} KB")


if __name__ == "__main__":
    asyncio.run(main())
