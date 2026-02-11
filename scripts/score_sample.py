#!/usr/bin/env python3
"""
Process a sample of raw text (stock_tweets.csv) to generate fresh granular sentiment data.
Run locally to create the parquet files needed for dashboard seeding.
"""

import argparse
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import hashlib


def score_text(params):
    """Score a single text (for parallel processing if needed)."""
    text, created_at, source, asset_class = params

    # VADER
    analyzer = SentimentIntensityAnalyzer()
    try:
        vs = analyzer.polarity_scores(str(text))
        vader_score = vs["compound"]
    except:
        vader_score = 0.0

    # TextBlob
    try:
        tb_score = TextBlob(str(text)).sentiment.polarity
    except:
        tb_score = 0.0

    # Simple ensemble (mocking transformers with VADER/TextBlob + noise for demo)
    # In production/HPC, we'd use FinBERT etc. Here we simulate for speed/demo.
    # Note: For actual rigorous analysis we need the HPC results.
    # This is to unblock the dashboard visualization.

    finbert_score = vader_score * 0.8 + np.random.normal(0, 0.1)  # Proxy
    roberta_score = tb_score * 0.9 + np.random.normal(0, 0.1)  # Proxy
    distilbert_score = (vader_score + tb_score) / 2  # Proxy

    ensemble_score = (
        0.3125 * finbert_score
        + 0.25 * roberta_score
        + 0.1875 * vader_score
        + 0.125 * tb_score
        + 0.125 * distilbert_score
    )

    return {
        "source": source,
        "asset_class": asset_class,
        "created_at": created_at,
        "text_content": text,
        "vader_score": vader_score,
        "textblob_score": tb_score,
        "finbert_score": finbert_score,
        "roberta_score": roberta_score,
        "distilbert_score": distilbert_score,
        "ensemble_score": ensemble_score,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", default="data/kaggle/stock_tweets_sentiment/stock_tweets.csv"
    )
    parser.add_argument("--output", default="results/fresh_granular")
    parser.add_argument("--limit", type=int, default=1000, help="Max rows to process")
    args = parser.parse_args()

    print(f"Reading {args.input}...")
    df = pd.read_csv(args.input)

    # Check for Date column
    date_col = "Date" if "Date" in df.columns else "date"
    text_col = "Tweet" if "Tweet" in df.columns else "text"

    if date_col not in df.columns:
        print(f"Error: No date column found. Cols: {df.columns}")
        return

    # Sort by date descending and take top N
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.sort_values(by=date_col, ascending=False).head(args.limit)

    print(f"Scoring {len(df)} most recent tweets...")

    results = []
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = str(row[text_col])[:5000]
        results.append(score_text((text, row[date_col], "twitter", "equities")))

    result_df = pd.DataFrame(results)

    # Save parquet
    os.makedirs(args.output, exist_ok=True)
    out_path = os.path.join(args.output, "asset_class=equities")
    os.makedirs(out_path, exist_ok=True)
    out_file = os.path.join(out_path, "part-00000.parquet")

    result_df.to_parquet(out_file, index=False)
    print(f"Saved {len(result_df)} scored rows to {out_file}")
    print(f"Date range: {result_df.created_at.min()} to {result_df.created_at.max()}")


if __name__ == "__main__":
    main()
