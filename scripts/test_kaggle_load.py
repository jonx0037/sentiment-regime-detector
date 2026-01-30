#!/usr/bin/env python3
"""Test loading new Kaggle datasets."""

from sentiment_detector.collectors.kaggle_loader import KaggleDataLoader
from collections import Counter

loader = KaggleDataLoader('data/kaggle')

print('Testing new Kaggle datasets...')
print()

# Reddit News
items = loader.load_reddit_news('data/kaggle/stocknews/RedditNews.csv', limit=5)
print(f'📰 Reddit News: {len(items)} items')
if items:
    print(f'   Sample: {items[0].content[:80]}...')

# DJIA News  
items = loader.load_djia_news('data/kaggle/stocknews/Combined_News_DJIA.csv', limit=5)
print(f'📈 DJIA Combined News: {len(items)} items')
if items:
    print(f'   Sample: {items[0].content[:80]}...')

# Crypto Tweets
items = loader.load_crypto_tweets('data/kaggle/crypto-tweets/crypto_10k_tweets_(2021_2022Nov).csv', limit=5)
print(f'🪙 Crypto Tweets: {len(items)} items')
if items:
    print(f'   Sample: {items[0].content[:80]}...')

print()
print('Testing load_all with limit=1000...')
all_items = loader.load_all(limit=1000)
print(f'✅ Total loaded: {len(all_items)} items')

# Show distribution
sources = Counter(i.metadata.get('dataset', 'unknown') for i in all_items)
print('   By dataset:', dict(sources))
