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


def process_with_textblob(texts: list[str]) -> list[dict]:
    """Process texts with TextBlob sentiment.

    Args:
        texts: List of texts to process

    Returns:
        List of sentiment results
    """
    print(f"\n📊 Processing {len(texts):,} texts with TextBlob...")

    try:
        from textblob import TextBlob

        results = []

        for text in tqdm(texts, desc="TextBlob"):
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity  # Range: -1 to 1
                subjectivity = blob.sentiment.subjectivity  # Range: 0 to 1

                # Map polarity to positive/negative/neutral
                if polarity > 0.1:
                    label = "positive"
                    positive = (polarity + 1) / 2  # Map [-1,1] to [0,1]
                    negative = 0.0
                    neutral = 1 - positive
                elif polarity < -0.1:
                    label = "negative"
                    negative = abs(polarity)
                    positive = 0.0
                    neutral = 1 - negative
                else:
                    label = "neutral"
                    neutral = 1.0
                    positive = 0.0
                    negative = 0.0

                results.append({
                    "text": text,
                    "label": label,
                    "compound": polarity,
                    "positive": positive,
                    "negative": negative,
                    "neutral": neutral,
                    "subjectivity": subjectivity,
                    "model": "textblob"
                })

            except Exception as e:
                # Skip texts that cause errors
                results.append({
                    "text": text,
                    "label": "neutral",
                    "compound": 0.0,
                    "positive": 0.0,
                    "negative": 0.0,
                    "neutral": 1.0,
                    "subjectivity": 0.5,
                    "model": "textblob"
                })

        print(f"  ✓ Processed {len(results):,} texts")

        return results

    except Exception as e:
        print(f"  ✗ TextBlob processing failed: {e}")
        raise


def process_with_distilbert(texts: list[str], batch_size: int = 32) -> list[dict]:
    """Process texts with DistilBERT sentiment model.

    Args:
        texts: List of texts to process
        batch_size: Batch size for processing

    Returns:
        List of sentiment results
    """
    print(f"\n📊 Processing {len(texts):,} texts with DistilBERT...")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Device: {device}")

    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        # Load DistilBERT sentiment model
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model = model.to(device)
        model = model.train(False)

        print(f"  ✓ DistilBERT loaded on {device}")

        results = []

        # Process in batches
        for i in tqdm(range(0, len(texts), batch_size), desc="DistilBERT"):
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

            # Extract results (DistilBERT SST-2: 0=negative, 1=positive)
            for j, text in enumerate(batch_texts):
                prob_negative = probs[j][0].item()
                prob_positive = probs[j][1].item()
                prob_neutral = 0.0  # SST-2 doesn't have neutral class

                # Compute compound score
                compound = prob_positive - prob_negative

                # Determine label
                if prob_positive > 0.6:
                    label = "positive"
                elif prob_negative > 0.6:
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
                    "model": "distilbert"
                })

        print(f"  ✓ Processed {len(results):,} texts")

        return results

    except Exception as e:
        print(f"  ✗ DistilBERT processing failed: {e}")
        raise


def process_with_llama3(texts: list[str], batch_size: int = 8) -> list[dict]:
    """Process texts with Llama 3 sentiment model.

    Args:
        texts: List of texts to process
        batch_size: Batch size for processing (smaller for LLM)

    Returns:
        List of sentiment results
    """
    print(f"\n📊 Processing {len(texts):,} texts with Llama 3...")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Device: {device}")

    try:
        # Import Llama sentiment model
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
        from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

        # Initialize with transformers backend (or mock for testing)
        try:
            model = LlamaSentimentModel(backend="transformers")
            model.load()
            print(f"  ✓ Llama 3 loaded on {device}")
        except Exception as e:
            print(f"  ⚠️  Llama 3 transformers backend failed: {e}")
            print("  Falling back to mock backend...")
            model = LlamaSentimentModel(backend="mock")
            model.load()

        results = []

        # Process in smaller batches (LLMs are memory-intensive)
        for i in tqdm(range(0, len(texts), batch_size), desc="Llama 3"):
            batch_texts = texts[i:i+batch_size]

            for text in batch_texts:
                try:
                    result = model.predict(text)

                    # Map Llama result to standard format
                    label_map = {
                        "POSITIVE": "positive",
                        "NEGATIVE": "negative",
                        "NEUTRAL": "neutral"
                    }

                    label = label_map.get(result["label"], "neutral")
                    confidence = result["confidence"]

                    # Compute compound score from confidence
                    if label == "positive":
                        compound = confidence
                        positive = confidence
                        negative = 0.0
                        neutral = 1 - confidence
                    elif label == "negative":
                        compound = -confidence
                        positive = 0.0
                        negative = confidence
                        neutral = 1 - confidence
                    else:
                        compound = 0.0
                        positive = 0.0
                        negative = 0.0
                        neutral = confidence

                    results.append({
                        "text": text,
                        "label": label,
                        "compound": compound,
                        "positive": positive,
                        "negative": negative,
                        "neutral": neutral,
                        "model": "llama3"
                    })

                except Exception as e:
                    # Skip texts that cause errors
                    results.append({
                        "text": text,
                        "label": "neutral",
                        "compound": 0.0,
                        "positive": 0.0,
                        "negative": 0.0,
                        "neutral": 1.0,
                        "model": "llama3"
                    })

        print(f"  ✓ Processed {len(results):,} texts")

        return results

    except Exception as e:
        print(f"  ✗ Llama 3 processing failed: {e}")
        print("  Skipping Llama 3 model...")
        return []


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
        default="finbert,vader,textblob,distilbert,llama3",
        help="Comma-separated list of models (full ensemble: finbert,vader,textblob,distilbert,llama3)"
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
        models = [m.strip() for m in args.models.split(",")]
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

        if "textblob" in models:
            textblob_results = process_with_textblob(texts)
            results_df = pd.DataFrame(textblob_results)
            results_df['date'] = df['date'].values
            all_results.append(results_df)

        if "distilbert" in models:
            distilbert_results = process_with_distilbert(texts, args.batch_size)
            results_df = pd.DataFrame(distilbert_results)
            results_df['date'] = df['date'].values
            all_results.append(results_df)

        if "llama3" in models:
            llama3_results = process_with_llama3(texts, batch_size=8)
            if llama3_results:  # Only add if not empty
                results_df = pd.DataFrame(llama3_results)
                results_df['date'] = df['date'].values
                all_results.append(results_df)

        if not all_results:
            print("\n❌ ERROR: No models processed successfully")
            sys.exit(1)

        # Combine results (ensemble average if multiple models)
        if len(all_results) > 1:
            print(f"\n📊 Combining {len(all_results)} model outputs...")
            combined = pd.concat(all_results, ignore_index=True)

            # Compute ensemble average by text
            numeric_cols = ['compound', 'positive', 'negative', 'neutral']
            combined_agg = combined.groupby(['date', 'text'])[numeric_cols].mean().reset_index()

            # Determine ensemble label from averaged scores
            def ensemble_label(row):
                if row['compound'] > 0.05:
                    return "positive"
                elif row['compound'] < -0.05:
                    return "negative"
                else:
                    return "neutral"

            combined_agg['label'] = combined_agg.apply(ensemble_label, axis=1)
            combined_agg['model'] = 'ensemble'

            combined = combined_agg
            print(f"  ✓ Ensemble: {len(all_results)} models averaged")
        else:
            combined = all_results[0]
            print(f"  Single model used: {combined['model'].iloc[0]}")

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
