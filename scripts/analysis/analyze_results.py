#!/usr/bin/env python3
"""Analyze sentiment results from MANEFRAME."""

import json
import sys
from collections import defaultdict
from pathlib import Path

def analyze_file(filepath):
    """Analyze a single results file."""
    with open(filepath) as f:
        data = json.load(f)

    print(f'\n📊 Sentiment Analysis Results: {Path(filepath).name}')
    print('=' * 70)

    # By source
    source_sentiment = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
    for item in data:
        source = item.get('source', 'unknown')
        label = item.get('sentiment_label', 'neutral').lower()
        source_sentiment[source][label] += 1

    print('\n📡 Sentiment by Source:')
    for source, counts in sorted(source_sentiment.items()):
        total = sum(counts.values())
        pos_pct = counts["positive"]/total*100
        neg_pct = counts["negative"]/total*100
        neu_pct = counts["neutral"]/total*100
        print(f'  {source:10} | +{counts["positive"]:3} ({pos_pct:4.1f}%) | -{counts["negative"]:3} ({neg_pct:4.1f}%) | o{counts["neutral"]:3} ({neu_pct:4.1f}%) | n={total}')

    # By asset class
    asset_sentiment = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
    for item in data:
        asset = item.get('asset_class', 'unknown')
        label = item.get('sentiment_label', 'neutral').lower()
        asset_sentiment[asset][label] += 1

    print('\n📈 Sentiment by Asset Class:')
    for asset, counts in sorted(asset_sentiment.items()):
        total = sum(counts.values())
        pos_pct = counts["positive"]/total*100
        neg_pct = counts["negative"]/total*100
        neu_pct = counts["neutral"]/total*100
        print(f'  {asset:10} | +{counts["positive"]:3} ({pos_pct:4.1f}%) | -{counts["negative"]:3} ({neg_pct:4.1f}%) | o{counts["neutral"]:3} ({neu_pct:4.1f}%) | n={total}')

    # Sample high-confidence predictions
    print('\n📝 Sample High-Confidence Predictions:')
    high_conf = [i for i in data if i.get('sentiment_score', 0) > 0.95][:6]
    for item in high_conf:
        content = (item.get('content', '') or '')[:55] + '...'
        label = item.get('sentiment_label', 'unknown')
        score = item.get('sentiment_score', 0)
        print(f'  [{label:8}] ({score:.3f}) {content}')

    print(f'\nTotal records: {len(data)}')


if __name__ == '__main__':
    # Default to the real data results
    default_file = 'data/processed/kaggle_rss_combined_sentiment.json'
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    elif Path(default_file).exists():
        filepath = default_file
    elif Path('data/processed/sample_batch_sentiment.json').exists():
        filepath = 'data/processed/sample_batch_sentiment.json'
    else:
        print("Usage: python scripts/analyze_results.py <results_file>")
        sys.exit(1)
    
    analyze_file(filepath)
