#!/usr/bin/env python3
"""
2008 Financial Crisis Backtest

Run historical backtest against the 2008 financial crisis period.
Validates our sentiment-based regime detection against VIX ground truth.
"""

import json
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
DB_URL = 'postgresql://postgres:password@localhost:5432/sentiment_db'
VIX_FILE = Path('data/processed/vix_regimes_extended.json')
OUTPUT_DIR = Path('data/processed')

# Backtest period: Sep 1 - Nov 30, 2008 (peak crisis)
START_DATE = '2008-09-01'
END_DATE = '2008-11-30'


def load_vix_regimes():
    """Load extended VIX regime data."""
    with open(VIX_FILE) as f:
        vix_data = json.load(f)
    return {d['date']: d for d in vix_data['daily_data']}


def get_sentiment_data():
    """Get daily sentiment aggregates for the crisis period."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cur.execute('''
        SELECT 
            DATE(t.content_created_at) as day,
            COUNT(*) as text_count,
            AVG(ss.compound) as avg_sentiment,
            STDDEV(ss.compound) as std_sentiment,
            MIN(ss.compound) as min_sentiment,
            MAX(ss.compound) as max_sentiment,
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ss.compound) as q25,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ss.compound) as median,
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ss.compound) as q75
        FROM raw_texts t
        JOIN sentiment_scores ss ON t.id = ss.text_id
        WHERE t.content_created_at >= %s AND t.content_created_at <= %s
        GROUP BY DATE(t.content_created_at)
        ORDER BY day
    ''', (START_DATE, END_DATE))
    
    columns = ['date', 'text_count', 'avg_sentiment', 'std_sentiment', 
               'min_sentiment', 'max_sentiment', 'q25', 'median', 'q75']
    data = cur.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=columns)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df


def calculate_sentiment_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate rolling features for regime detection."""
    df = df.copy()
    
    # Rolling averages (3-day and 7-day)
    df['sentiment_ma3'] = df['avg_sentiment'].rolling(3, min_periods=1).mean()
    df['sentiment_ma7'] = df['avg_sentiment'].rolling(7, min_periods=1).mean()
    
    # Volatility (rolling std)
    df['sentiment_volatility'] = df['avg_sentiment'].rolling(5, min_periods=2).std()
    
    # Momentum (change from previous day)
    df['sentiment_momentum'] = df['avg_sentiment'].diff()
    
    # Z-score (how extreme is today vs recent history)
    rolling_mean = df['avg_sentiment'].rolling(14, min_periods=3).mean()
    rolling_std = df['avg_sentiment'].rolling(14, min_periods=3).std()
    df['sentiment_zscore'] = (df['avg_sentiment'] - rolling_mean) / rolling_std.replace(0, 0.01)
    
    # Fill NaN with neutral values
    df = df.fillna(0)
    
    return df


def predict_regime(row: pd.Series) -> str:
    """
    Predict regime based on sentiment features.
    
    Rules calibrated for 2008 crisis (more extreme than GameStop):
    - Very negative sentiment + high volatility -> high_volatility
    - Moderately negative sentiment -> elevated
    - Neutral to slightly negative -> normal
    - Positive sentiment -> low_volatility
    """
    avg_sent = row['avg_sentiment']
    volatility = row.get('sentiment_volatility', 0)
    zscore = row.get('sentiment_zscore', 0)
    momentum = row.get('sentiment_momentum', 0)
    
    # Scoring system
    crisis_score = 0
    
    # Sentiment level (primary signal)
    if avg_sent < -0.25:
        crisis_score += 3
    elif avg_sent < -0.15:
        crisis_score += 2
    elif avg_sent < -0.05:
        crisis_score += 1
    elif avg_sent > 0.1:
        crisis_score -= 1
    
    # Volatility (secondary signal)
    if volatility > 0.15:
        crisis_score += 2
    elif volatility > 0.10:
        crisis_score += 1
    
    # Z-score extremity
    if zscore < -1.5:
        crisis_score += 2
    elif zscore < -1.0:
        crisis_score += 1
    
    # Negative momentum (deteriorating sentiment)
    if momentum < -0.1:
        crisis_score += 1
    
    # Map score to regime
    if crisis_score >= 5:
        return 'high_volatility'
    elif crisis_score >= 3:
        return 'elevated'
    elif crisis_score >= 1:
        return 'normal'
    else:
        return 'low_volatility'


def run_backtest():
    """Run the 2008 Financial Crisis backtest."""
    print("=" * 60)
    print("2008 FINANCIAL CRISIS BACKTEST")
    print("=" * 60)
    print(f"Period: {START_DATE} to {END_DATE}")
    print()
    
    # Load data
    print("Loading VIX regime data...")
    vix_regimes = load_vix_regimes()
    
    print("Loading sentiment data from database...")
    sentiment_df = get_sentiment_data()
    print(f"  Found {len(sentiment_df)} days with sentiment data")
    print(f"  Total texts: {sentiment_df['text_count'].sum():,}")
    
    # Calculate features
    print("\nCalculating sentiment features...")
    features_df = calculate_sentiment_features(sentiment_df)
    
    # Generate predictions
    print("Generating regime predictions...")
    predictions = []
    
    for _, row in features_df.iterrows():
        date = row['date']
        predicted_regime = predict_regime(row)
        
        # Get VIX ground truth
        vix_info = vix_regimes.get(date, {})
        vix_regime = vix_info.get('regime', 'unknown')
        vix_value = vix_info.get('close', None)  # VIX closing value
        
        predictions.append({
            'date': date,
            'avg_sentiment': row['avg_sentiment'],
            'text_count': row['text_count'],
            'sentiment_volatility': row['sentiment_volatility'],
            'sentiment_zscore': row['sentiment_zscore'],
            'predicted_regime': predicted_regime,
            'vix_regime': vix_regime,
            'vix_value': vix_value,
            'correct': predicted_regime == vix_regime
        })
    
    results_df = pd.DataFrame(predictions)
    
    # Calculate metrics
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    
    # Only count days where we have VIX data
    valid_results = results_df[results_df['vix_regime'] != 'unknown']
    
    correct = valid_results['correct'].sum()
    total = len(valid_results)
    accuracy = correct / total * 100 if total > 0 else 0
    
    print(f"\nOverall Accuracy: {accuracy:.1f}% ({correct}/{total} days)")
    
    # Per-regime breakdown
    print("\nPer-Regime Accuracy:")
    for regime in ['high_volatility', 'elevated', 'normal', 'low_volatility']:
        regime_days = valid_results[valid_results['vix_regime'] == regime]
        if len(regime_days) > 0:
            regime_correct = regime_days['correct'].sum()
            regime_acc = regime_correct / len(regime_days) * 100
            print(f"  {regime:16s}: {regime_acc:5.1f}% ({regime_correct}/{len(regime_days)} days)")
    
    # Confusion matrix
    print("\nConfusion Matrix (Predicted vs VIX Actual):")
    print(f"{'':16s} | {'high_vol':>10s} | {'elevated':>10s} | {'normal':>10s} | {'low_vol':>10s}")
    print("-" * 65)
    for pred_regime in ['high_volatility', 'elevated', 'normal', 'low_volatility']:
        pred_rows = valid_results[valid_results['predicted_regime'] == pred_regime]
        counts = []
        for actual_regime in ['high_volatility', 'elevated', 'normal', 'low_volatility']:
            count = len(pred_rows[pred_rows['vix_regime'] == actual_regime])
            counts.append(count)
        print(f"{pred_regime:16s} | {counts[0]:>10d} | {counts[1]:>10d} | {counts[2]:>10d} | {counts[3]:>10d}")
    
    # Key crisis days analysis
    print("\n" + "=" * 60)
    print("KEY CRISIS DAYS ANALYSIS")
    print("=" * 60)
    
    # Find VIX peak days
    crisis_days = valid_results.nlargest(10, 'vix_value')
    print("\nTop 10 Highest VIX Days:")
    for _, row in crisis_days.iterrows():
        match = "✓" if row['correct'] else "✗"
        print(f"  {row['date']}: VIX={row['vix_value']:.1f} "
              f"| Predicted: {row['predicted_regime']:16s} "
              f"| Actual: {row['vix_regime']:16s} {match}")
    
    # Most negative sentiment days
    print("\nMost Negative Sentiment Days:")
    neg_days = valid_results.nsmallest(10, 'avg_sentiment')
    for _, row in neg_days.iterrows():
        match = "✓" if row['correct'] else "✗"
        print(f"  {row['date']}: Sentiment={row['avg_sentiment']:.3f} "
              f"| Predicted: {row['predicted_regime']:16s} "
              f"| Actual: {row['vix_regime']:16s} {match}")
    
    # Export results
    print("\n" + "=" * 60)
    print("EXPORTING RESULTS")
    print("=" * 60)
    
    # Save CSV
    csv_path = OUTPUT_DIR / 'crisis_2008_backtest_results.csv'
    results_df.to_csv(csv_path, index=False)
    print(f"  Saved: {csv_path}")
    
    # Save features
    features_csv = OUTPUT_DIR / 'crisis_2008_sentiment_features.csv'
    features_df.to_csv(features_csv, index=False)
    print(f"  Saved: {features_csv}")
    
    # Save summary JSON
    summary = {
        'event': '2008 Financial Crisis',
        'period': {'start': START_DATE, 'end': END_DATE},
        'data_stats': {
            'total_days': len(sentiment_df),
            'total_texts': int(sentiment_df['text_count'].sum()),
            'avg_texts_per_day': float(sentiment_df['text_count'].mean()),
        },
        'results': {
            'accuracy': accuracy,
            'correct_predictions': int(correct),
            'total_predictions': int(total),
        },
        'regime_distribution': {
            'predicted': results_df['predicted_regime'].value_counts().to_dict(),
            'actual': results_df['vix_regime'].value_counts().to_dict(),
        },
        'vix_stats': {
            'max_vix': float(valid_results['vix_value'].max()),
            'avg_vix': float(valid_results['vix_value'].mean()),
            'min_vix': float(valid_results['vix_value'].min()),
        },
        'sentiment_stats': {
            'min_sentiment': float(results_df['avg_sentiment'].min()),
            'avg_sentiment': float(results_df['avg_sentiment'].mean()),
            'max_sentiment': float(results_df['avg_sentiment'].max()),
        },
        'generated_at': datetime.now().isoformat()
    }
    
    summary_path = OUTPUT_DIR / 'crisis_2008_backtest_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {summary_path}")
    
    return results_df, accuracy


if __name__ == "__main__":
    results, accuracy = run_backtest()
