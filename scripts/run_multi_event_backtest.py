#!/usr/bin/env python3
"""
Multi-Event Historical Backtest

Run backtests across multiple historical volatility events to validate
sentiment-based regime detection against VIX ground truth.
"""

import json
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from scipy import stats

# Configuration
DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
VIX_FILE = Path('data/processed/vix_regimes_extended.json')
OUTPUT_DIR = Path('data/processed')

# Define events to backtest
EVENTS = [
    {
        'name': 'Flash Crash',
        'start': '2010-05-01',
        'end': '2010-05-31',
        'description': 'May 6, 2010 Flash Crash - Dow dropped 1000 points in minutes'
    },
    {
        'name': '2011 Debt Ceiling',
        'start': '2011-07-15',
        'end': '2011-08-31',
        'description': 'US Debt Ceiling Crisis - S&P downgrade'
    },
    {
        'name': '2015 China Devaluation',
        'start': '2015-08-01',
        'end': '2015-09-15',
        'description': 'Chinese Yuan devaluation sparked global selloff'
    },
    {
        'name': 'Brexit',
        'start': '2016-06-01',
        'end': '2016-07-15',
        'description': 'UK Brexit referendum on June 23, 2016'
    },
]


def load_vix_regimes():
    """Load extended VIX regime data."""
    with open(VIX_FILE) as f:
        vix_data = json.load(f)
    return {d['date']: d for d in vix_data['daily_data']}


def get_sentiment_data(start_date: str, end_date: str):
    """Get daily sentiment aggregates for a period."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute('''
        SELECT 
            DATE(t.content_created_at) as day,
            COUNT(*) as text_count,
            AVG(ss.compound) as avg_sentiment,
            STDDEV(ss.compound) as std_sentiment,
            MIN(ss.compound) as min_sentiment,
            MAX(ss.compound) as max_sentiment
        FROM raw_texts t
        JOIN sentiment_scores ss ON t.id = ss.text_id
        WHERE t.content_created_at >= %s AND t.content_created_at <= %s
        GROUP BY DATE(t.content_created_at)
        ORDER BY day
    ''', (start_date, end_date))
    
    columns = ['date', 'text_count', 'avg_sentiment', 'std_sentiment', 
               'min_sentiment', 'max_sentiment']
    data = cur.fetchall()
    conn.close()
    
    if not data:
        return pd.DataFrame(columns=columns)
    
    df = pd.DataFrame(data, columns=columns)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df


def calculate_sentiment_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate rolling features for regime detection."""
    if len(df) == 0:
        return df
        
    df = df.copy()
    
    # Rolling averages
    df['sentiment_ma3'] = df['avg_sentiment'].rolling(3, min_periods=1).mean()
    df['sentiment_ma7'] = df['avg_sentiment'].rolling(7, min_periods=1).mean()
    
    # Volatility
    df['sentiment_volatility'] = df['avg_sentiment'].rolling(5, min_periods=2).std()
    
    # Momentum
    df['sentiment_momentum'] = df['avg_sentiment'].diff()
    
    # Z-score
    rolling_mean = df['avg_sentiment'].rolling(14, min_periods=3).mean()
    rolling_std = df['avg_sentiment'].rolling(14, min_periods=3).std()
    df['sentiment_zscore'] = (df['avg_sentiment'] - rolling_mean) / rolling_std.replace(0, 0.01)
    
    df = df.fillna(0)
    return df


def predict_regime(row: pd.Series) -> str:
    """Predict regime based on sentiment features."""
    avg_sent = row['avg_sentiment']
    volatility = row.get('sentiment_volatility', 0)
    zscore = row.get('sentiment_zscore', 0)
    momentum = row.get('sentiment_momentum', 0)
    
    crisis_score = 0
    
    # Sentiment level
    if avg_sent < -0.25:
        crisis_score += 3
    elif avg_sent < -0.15:
        crisis_score += 2
    elif avg_sent < -0.05:
        crisis_score += 1
    elif avg_sent > 0.1:
        crisis_score -= 1
    
    # Volatility
    if volatility > 0.15:
        crisis_score += 2
    elif volatility > 0.10:
        crisis_score += 1
    
    # Z-score
    if zscore < -1.5:
        crisis_score += 2
    elif zscore < -1.0:
        crisis_score += 1
    
    # Momentum
    if momentum < -0.1:
        crisis_score += 1
    
    # Map to regime
    if crisis_score >= 5:
        return 'high_volatility'
    elif crisis_score >= 3:
        return 'elevated'
    elif crisis_score >= 1:
        return 'normal'
    else:
        return 'low_volatility'


def run_single_backtest(event: dict, vix_regimes: dict) -> dict:
    """Run backtest for a single event."""
    print(f"\n{'='*60}")
    print(f"EVENT: {event['name']}")
    print(f"{'='*60}")
    print(f"Period: {event['start']} to {event['end']}")
    print(f"Description: {event['description']}")
    
    # Get sentiment data
    sentiment_df = get_sentiment_data(event['start'], event['end'])
    
    if len(sentiment_df) == 0:
        print("  No data available for this period!")
        return None
    
    print(f"  Data: {len(sentiment_df)} days, {sentiment_df['text_count'].sum():,} texts")
    
    # Calculate features
    features_df = calculate_sentiment_features(sentiment_df)
    
    # Generate predictions
    predictions = []
    for _, row in features_df.iterrows():
        date = row['date']
        predicted_regime = predict_regime(row)
        
        vix_info = vix_regimes.get(date, {})
        vix_regime = vix_info.get('regime', 'unknown')
        vix_value = vix_info.get('close', None)
        
        predictions.append({
            'date': date,
            'avg_sentiment': row['avg_sentiment'],
            'text_count': row['text_count'],
            'predicted_regime': predicted_regime,
            'vix_regime': vix_regime,
            'vix_value': vix_value,
            'correct': predicted_regime == vix_regime
        })
    
    results_df = pd.DataFrame(predictions)
    valid_results = results_df[results_df['vix_regime'] != 'unknown']
    
    if len(valid_results) == 0:
        print("  No VIX data available for this period!")
        return None
    
    # Calculate metrics
    correct = valid_results['correct'].sum()
    total = len(valid_results)
    accuracy = correct / total * 100 if total > 0 else 0
    
    print(f"\n  Classification Accuracy: {accuracy:.1f}% ({correct}/{total} days)")
    
    # Correlation
    if len(valid_results) > 3:
        corr, p_val = stats.pearsonr(valid_results['avg_sentiment'], valid_results['vix_value'])
        print(f"  Sentiment-VIX Correlation: r = {corr:.3f} (p = {p_val:.4f})")
    else:
        corr, p_val = np.nan, np.nan
    
    # Binary crisis detection
    valid_results = valid_results.copy()
    valid_results['vix_crisis'] = valid_results['vix_regime'].isin(['high_volatility', 'elevated'])
    valid_results['predicted_crisis'] = valid_results['predicted_regime'].isin(['high_volatility', 'elevated'])
    binary_correct = (valid_results['vix_crisis'] == valid_results['predicted_crisis']).sum()
    binary_accuracy = binary_correct / len(valid_results) * 100
    print(f"  Binary Crisis Detection: {binary_accuracy:.1f}%")
    
    # VIX stats
    max_vix = valid_results['vix_value'].max()
    avg_vix = valid_results['vix_value'].mean()
    print(f"  VIX Range: {valid_results['vix_value'].min():.1f} - {max_vix:.1f} (avg: {avg_vix:.1f})")
    
    # Peak day detection
    peak_day = valid_results.loc[valid_results['vix_value'].idxmax()]
    peak_match = "✓" if peak_day['correct'] else "✗"
    print(f"  Peak VIX Day: {peak_day['date']} (VIX={peak_day['vix_value']:.1f}) - {peak_match}")
    
    return {
        'event': event['name'],
        'period': {'start': event['start'], 'end': event['end']},
        'data_stats': {
            'total_days': len(sentiment_df),
            'total_texts': int(sentiment_df['text_count'].sum()),
        },
        'classification_accuracy': accuracy,
        'binary_crisis_accuracy': binary_accuracy,
        'correlation': float(corr) if not np.isnan(corr) else None,
        'correlation_pvalue': float(p_val) if not np.isnan(p_val) else None,
        'vix_stats': {
            'max': float(max_vix),
            'avg': float(avg_vix),
        },
        'peak_day_correct': peak_day['correct'],
        'predictions': predictions,
    }


def main():
    print("=" * 60)
    print("MULTI-EVENT HISTORICAL BACKTEST")
    print("=" * 60)
    print(f"Running backtests for {len(EVENTS)} events")
    
    # Load VIX data
    print("\nLoading VIX regime data...")
    vix_regimes = load_vix_regimes()
    print(f"  Loaded {len(vix_regimes)} days of VIX data")
    
    # Run backtests
    all_results = []
    for event in EVENTS:
        result = run_single_backtest(event, vix_regimes)
        if result:
            all_results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY ACROSS ALL EVENTS")
    print("=" * 60)
    
    print(f"\n{'Event':25s} | {'Accuracy':>10s} | {'Binary':>10s} | {'Corr':>8s} | {'Peak':>6s}")
    print("-" * 70)
    
    for r in all_results:
        corr_str = f"{r['correlation']:.3f}" if r['correlation'] else "N/A"
        peak_str = "✓" if r['peak_day_correct'] else "✗"
        print(f"{r['event']:25s} | {r['classification_accuracy']:>9.1f}% | "
              f"{r['binary_crisis_accuracy']:>9.1f}% | {corr_str:>8s} | {peak_str:>6s}")
    
    # Overall statistics
    avg_accuracy = np.mean([r['classification_accuracy'] for r in all_results])
    avg_binary = np.mean([r['binary_crisis_accuracy'] for r in all_results])
    correlations = [r['correlation'] for r in all_results if r['correlation']]
    avg_corr = np.mean(correlations) if correlations else np.nan
    peak_correct = sum(1 for r in all_results if r['peak_day_correct'])
    
    print("-" * 70)
    print(f"{'AVERAGE':25s} | {avg_accuracy:>9.1f}% | {avg_binary:>9.1f}% | {avg_corr:>8.3f} | {peak_correct}/{len(all_results)}")
    
    # Export
    print("\n" + "=" * 60)
    print("EXPORTING RESULTS")
    print("=" * 60)
    
    # Save summary
    summary = {
        'events': [
            {k: (bool(v) if isinstance(v, np.bool_) else v) 
             for k, v in r.items() if k != 'predictions'}
            for r in all_results
        ],
        'overall': {
            'avg_classification_accuracy': float(avg_accuracy),
            'avg_binary_crisis_accuracy': float(avg_binary),
            'avg_correlation': float(avg_corr) if not np.isnan(avg_corr) else None,
            'peak_days_correct': f"{peak_correct}/{len(all_results)}",
        },
        'generated_at': datetime.now().isoformat()
    }
    
    summary_path = OUTPUT_DIR / 'multi_event_backtest_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {summary_path}")
    
    # Save detailed results as CSV
    all_predictions = []
    for r in all_results:
        for p in r['predictions']:
            p['event'] = r['event']
            all_predictions.append(p)
    
    predictions_df = pd.DataFrame(all_predictions)
    csv_path = OUTPUT_DIR / 'multi_event_backtest_predictions.csv'
    predictions_df.to_csv(csv_path, index=False)
    print(f"  Saved: {csv_path}")


if __name__ == "__main__":
    main()
