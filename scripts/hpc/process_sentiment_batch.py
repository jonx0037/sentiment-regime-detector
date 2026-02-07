#!/usr/bin/env python3
"""Process collected historical data with sentiment models on HPC.

This script:
1. Loads collected data batches
2. Runs sentiment analysis (FinBERT, VADER, TextBlob, optionally Llama 3)
3. Aggregates to daily sentiment scores
4. Saves results for backtest validation

Designed for HPC with GPU acceleration.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import torch
from tqdm import tqdm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def load_data_batch(input_dir: Path, batch_id: int) -> pd.DataFrame:
    """Load collected data batch.

    Args:
        input_dir: Directory containing collected data
        batch_id: Batch ID to load

    Returns:
        DataFrame with text data
    """
    # Try different file patterns
    patterns = [
        f"combined_batch_{batch_id:04d}.parquet",
        f"gdelt_batch_{batch_id:04d}.parquet",
        f"reddit_batch_{batch_id:04d}.parquet"
    ]

    for pattern in patterns:
        file_path = input_dir / pattern
        if file_path.exists():
            print(f"✓ Loading: {file_path}")
            df = pd.read_parquet(file_path)
            return df

    raise FileNotFoundError(f"No data batch found for ID {batch_id}")


def process_with_finbert(texts: list[str], batch_size: int = 32) -> list[dict]:
    """Process texts with FinBERT sentiment model.

    Args:
        texts: List of texts to process
        batch_size: Batch size for processing

    Returns:
        List of sentiment results
    """
    print(f"\n📊 Processing {len(texts):,} texts with FinBERT...")

    # Check GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Device: {device}")

    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        import numpy as np

        # Load FinBERT
        model_name = "ProsusAI/finbert"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model = model.to(device)
        model = model.train(False)  # Set to evaluation mode

        print(f"  ✓ FinBERT loaded on {device}")

        results = []

        # Process in batches
        for i in tqdm(range(0, len(texts), batch_size), desc="FinBERT"):
            batch_texts = texts[i:i+batch_size]

            # Tokenize
            inputs = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt"
            ).to(device)

            # Inference
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Extract results
            for j, text in enumerate(batch_texts):
                prob_positive = probs[j][2].item()
                prob_negative = probs[j][0].item()
                prob_neutral = probs[j][1].item()

                # Compute compound score
                compound = prob_positive - prob_negative

                # Determine label
                if prob_positive > max(prob_negative, prob_neutral):
                    label = "positive"
                elif prob_negative > max(prob_positive, prob_neutral):
                    label = "negative"
                else:
                    label = "neutral"

                results.append({
                    "text": text,
                    "label": label,
                    "compound": compound,
                    "positive": prob_positive,
                    "negative": prob_negative,
                    "neutral": prob_neutral,
                    "model": "finbert"
                })

        print(f"  ✓ Processed {len(results):,} texts")

        return results

    except Exception as e:
        print(f"  ✗ FinBERT processing failed: {e}")
        raise


def process_with_vader(texts: list[str]) -> list[dict]:
    """Process texts with VADER sentiment.

    Args:
        texts: List of texts to process

    Returns:
        List of sentiment results
    """
    print(f"\n📊 Processing {len(texts):,} texts with VADER...")

    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        analyzer = SentimentIntensityAnalyzer()

        results = []

        for text in tqdm(texts, desc="VADER"):
            scores = analyzer.polarity_scores(text)

            results.append({
                "text": text,
                "label": "positive" if scores["compound"] > 0.05 else "negative" if scores["compound"] < -0.05 else "neutral",
                "compound": scores["compound"],
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "model": "vader"
            })

        print(f"  ✓ Processed {len(results):,} texts")

        return results

    except Exception as e:
        print(f"  ✗ VADER processing failed: {e}")
        raise


def aggregate_to_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment results to daily scores.

    Args:
        df: DataFrame with sentiment results

    Returns:
        DataFrame with daily aggregated sentiment
    """
    print("\n📊 Aggregating to daily sentiment...")

    # Ensure date column
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Group by date and aggregate
    daily = df.groupby('date').agg({
        'compound': ['mean', 'std', 'median', 'min', 'max'],
        'positive': 'mean',
        'negative': 'mean',
        'neutral': 'mean',
        'text': 'count'
    }).reset_index()

    # Flatten column names
    daily.columns = [
        'date',
        'compound_mean', 'compound_std', 'compound_median', 'compound_min', 'compound_max',
        'positive_mean', 'negative_mean', 'neutral_mean',
        'volume'
    ]

    # Calculate percentages
    label_counts = df.groupby(['date', 'label']).size().unstack(fill_value=0)
    label_pcts = label_counts.div(label_counts.sum(axis=1), axis=0)

    daily['pct_positive'] = label_pcts.get('positive', 0).values
    daily['pct_negative'] = label_pcts.get('negative', 0).values
    daily['pct_neutral'] = label_pcts.get('neutral', 0).values

    # Assign reliability based on volume
    def assign_reliability(volume):
        if volume >= 1000:
            return "high"
        elif volume >= 100:
            return "medium"
        elif volume >= 10:
            return "low"
        else:
            return "very_low"

    daily['reliability'] = daily['volume'].apply(assign_reliability)

    print(f"  ✓ Aggregated to {len(daily)} days")
    print(f"  ✓ Volume range: {daily['volume'].min():.0f} to {daily['volume'].max():.0f}")

    return daily


def main():
    """Process sentiment batch."""
    parser = argparse.ArgumentParser(
        description="Process sentiment for historical data batch"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Input directory with collected data"
    )
    parser.add_argument(
        "--batch-id",
        type=int,
        required=True,
        help="Batch ID to process"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Output directory for sentiment results"
    )
    parser.add_argument(
        "--models",
        type=str,
        default="finbert,vader",
        help="Comma-separated list of models (finbert,vader,textblob,llama3)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for model processing"
    )

    args = parser.parse_args()

    print("🔍 SENTIMENT PROCESSING")
    print("=" * 60)
    print(f"Batch ID: {args.batch_id}")
    print(f"Input: {args.input_dir}")
    print(f"Output: {args.output_dir}")
    print(f"Models: {args.models}")
    print("=" * 60)

    try:
        # Load data
        df = load_data_batch(Path(args.input_dir), args.batch_id)
        print(f"\n✓ Loaded {len(df):,} texts")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")

        # Extract texts
        texts = df['text'].tolist()

        # Process with requested models
        models = args.models.split(",")
        all_results = []

        if "finbert" in models:
            finbert_results = process_with_finbert(texts, args.batch_size)
            results_df = pd.DataFrame(finbert_results)
            results_df['date'] = df['date'].values
            all_results.append(results_df)

        if "vader" in models:
            vader_results = process_with_vader(texts)
            results_df = pd.DataFrame(vader_results)
            results_df['date'] = df['date'].values
            all_results.append(results_df)

        # Combine results (take average if multiple models)
        if len(all_results) > 1:
            combined = pd.concat(all_results, ignore_index=True)
            # Average by text
            combined = combined.groupby(['date', 'text']).mean(numeric_only=True).reset_index()
        else:
            combined = all_results[0]

        # Aggregate to daily
        daily = aggregate_to_daily(combined)

        # Save results
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save detailed results
        detail_file = output_dir / f"sentiment_batch_{args.batch_id:04d}.parquet"
        combined.to_parquet(detail_file, index=False)
        print(f"\n💾 Saved detailed results: {detail_file}")

        # Save daily aggregates
        daily_file = output_dir / f"daily_batch_{args.batch_id:04d}.csv"
        daily.to_csv(daily_file, index=False)
        print(f"💾 Saved daily aggregates: {daily_file}")

        # Print summary
        print("\n" + "=" * 60)
        print("✅ PROCESSING COMPLETE")
        print(f"  Texts processed: {len(combined):,}")
        print(f"  Days covered: {len(daily)}")
        print(f"  Mean sentiment: {daily['compound_mean'].mean():.4f}")
        print(f"  Mean volume: {daily['volume'].mean():.0f} texts/day")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
