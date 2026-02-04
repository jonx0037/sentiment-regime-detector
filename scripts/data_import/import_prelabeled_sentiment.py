#!/usr/bin/env python3
"""
Import pre-labeled sentiment datasets for model validation.

This script imports datasets that have ground-truth sentiment labels,
useful for validating our FinBERT + RoBERTa ensemble accuracy.

Datasets:
1. Bitcoin Tweets Sentiment (HuggingFace) - Parquet format with sentiment labels
2. Financial News NLP 2025 - CSV with event labels and sentiment
3. Reddit Sentiment 2025 - CSV with pre-computed sentiment scores

These are used for validation, not training.
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.models import Base, RawText, SentimentScore
from sentiment_detector.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default data paths
DATA_BASE = Path(__file__).parent.parent / "data" / "kaggle"
BITCOIN_TWEETS_PATH = DATA_BASE / "huggingface" / "bitcoin_tweets_sentiment"
FINANCIAL_NEWS_PATH = DATA_BASE / "financial-news-nlp-2025"
REDDIT_SENTIMENT_PATH = DATA_BASE / "reddit-sentiment-2025"


def load_bitcoin_tweets(data_path: Path) -> pd.DataFrame:
    """
    Load Bitcoin tweets sentiment dataset from HuggingFace parquet files.
    
    Args:
        data_path: Path to bitcoin_tweets_sentiment directory
        
    Returns:
        DataFrame with text and sentiment labels
    """
    logger.info(f"Loading Bitcoin tweets from {data_path}")
    
    dfs = []
    for parquet_file in data_path.glob("*.parquet"):
        logger.info(f"  Reading {parquet_file.name}")
        df = pd.read_parquet(parquet_file)
        df["split"] = parquet_file.stem  # train, test, eval
        dfs.append(df)
    
    if not dfs:
        raise FileNotFoundError(f"No parquet files found in {data_path}")
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Standardize columns
    combined["source"] = "bitcoin_tweets_hf"
    combined["source_type"] = "twitter"
    combined["asset"] = "BTC"
    
    # Map sentiment labels to standard format if needed
    # The dataset should have columns like 'text' and 'label' or 'sentiment'
    if "label" in combined.columns:
        combined["sentiment_label"] = combined["label"]
    elif "sentiment" in combined.columns:
        combined["sentiment_label"] = combined["sentiment"]
    
    logger.info(f"Loaded {len(combined)} Bitcoin tweets")
    logger.info(f"Splits: {combined['split'].value_counts().to_dict()}")
    
    return combined


def load_financial_news(data_path: Path) -> pd.DataFrame:
    """
    Load Financial News NLP 2025 dataset.
    
    Args:
        data_path: Path to financial-news-nlp-2025 directory
        
    Returns:
        DataFrame with news headlines and sentiment labels
    """
    logger.info(f"Loading Financial News from {data_path}")
    
    csv_files = list(data_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    
    dfs = []
    for csv_file in csv_files:
        logger.info(f"  Reading {csv_file.name}")
        df = pd.read_csv(csv_file)
        df["source_file"] = csv_file.stem
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Standardize columns
    col_mapping = {
        "Headline": "text",
        "headline": "text",
        "Date": "date",
        "date": "date",
        "Sentiment": "sentiment_label",
        "sentiment": "sentiment_label",
        "Source": "news_source",
        "source": "news_source",
        "Market_Event": "event_type",
        "market_event": "event_type",
        "Market_Index": "market_index",
        "market_index": "market_index",
    }
    
    combined = combined.rename(columns={k: v for k, v in col_mapping.items() if k in combined.columns})
    
    combined["source"] = "financial_news_2025"
    combined["source_type"] = "news"
    
    # Parse date if present
    if "date" in combined.columns:
        combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
    
    logger.info(f"Loaded {len(combined)} financial news items")
    if "sentiment_label" in combined.columns:
        logger.info(f"Sentiment distribution: {combined['sentiment_label'].value_counts().to_dict()}")
    
    return combined


def load_reddit_sentiment(data_path: Path) -> pd.DataFrame:
    """
    Load Reddit Sentiment 2025 dataset.
    
    Args:
        data_path: Path to reddit-sentiment-2025 directory
        
    Returns:
        DataFrame with Reddit posts/comments and sentiment scores
    """
    logger.info(f"Loading Reddit Sentiment from {data_path}")
    
    # Load comments with sentiment
    dfs = []
    
    # Comments file has pre-computed sentiment
    comments_file = data_path / "comments.csv"
    if comments_file.exists():
        logger.info("  Reading comments.csv")
        comments_df = pd.read_csv(comments_file)
        comments_df["text"] = comments_df.get("Body", comments_df.get("body", ""))
        comments_df["content_type"] = "comment"
        dfs.append(comments_df)
    
    # User posts with sentiment
    user_posts_file = data_path / "user_posts.csv"
    if user_posts_file.exists():
        logger.info("  Reading user_posts.csv")
        posts_df = pd.read_csv(user_posts_file)
        posts_df["text"] = posts_df.get("Title", posts_df.get("title", ""))
        posts_df["content_type"] = "post"
        dfs.append(posts_df)
    
    if not dfs:
        raise FileNotFoundError(f"No suitable files found in {data_path}")
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Standardize columns
    col_mapping = {
        "Sentiment": "sentiment_label",
        "sentiment": "sentiment_label",
        "Confidence": "confidence",
        "confidence": "confidence",
        "Sentiment_Score": "sentiment_score",
        "sentiment_score": "sentiment_score",
        "Post_ID": "post_id",
        "post_id": "post_id",
        "Score": "reddit_score",
        "score": "reddit_score",
    }
    
    combined = combined.rename(columns={k: v for k, v in col_mapping.items() if k in combined.columns})
    
    combined["source"] = "reddit_sentiment_2025"
    combined["source_type"] = "reddit"
    
    logger.info(f"Loaded {len(combined)} Reddit items")
    if "sentiment_label" in combined.columns:
        logger.info(f"Sentiment distribution: {combined['sentiment_label'].value_counts().to_dict()}")
    
    return combined


def standardize_sentiment_label(label: Any) -> dict:
    """
    Convert various sentiment label formats to standard scores.
    
    Returns:
        Dict with positive, negative, neutral, compound scores
    """
    if pd.isna(label):
        return {"positive": 0.33, "negative": 0.33, "neutral": 0.34, "compound": 0.0}
    
    label_str = str(label).lower().strip()
    
    # Handle string labels
    if label_str in ["positive", "pos", "1", "bullish"]:
        return {"positive": 0.9, "negative": 0.05, "neutral": 0.05, "compound": 0.8}
    elif label_str in ["negative", "neg", "-1", "bearish"]:
        return {"positive": 0.05, "negative": 0.9, "neutral": 0.05, "compound": -0.8}
    elif label_str in ["neutral", "neu", "0"]:
        return {"positive": 0.1, "negative": 0.1, "neutral": 0.8, "compound": 0.0}
    
    # Handle numeric scores
    try:
        score = float(label)
        if score > 0.3:
            return {"positive": score, "negative": 1-score, "neutral": 0.0, "compound": score}
        elif score < -0.3:
            return {"positive": 1+score, "negative": abs(score), "neutral": 0.0, "compound": score}
        else:
            return {"positive": 0.1, "negative": 0.1, "neutral": 0.8, "compound": score}
    except (ValueError, TypeError):
        return {"positive": 0.33, "negative": 0.33, "neutral": 0.34, "compound": 0.0}


def import_to_database(
    dfs: Dict[str, pd.DataFrame],
    db_url: str,
    batch_size: int = 500,
    dry_run: bool = False,
) -> int:
    """
    Import pre-labeled sentiment data to database.
    
    Args:
        dfs: Dictionary of DataFrames by source name
        db_url: Database connection URL
        batch_size: Number of records per batch
        dry_run: If True, don't actually insert data
        
    Returns:
        Total number of records imported
    """
    if dry_run:
        logger.info("DRY RUN - No data will be imported")
        return 0
    
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    
    total_imported = 0
    
    for source_name, df in dfs.items():
        logger.info(f"\nImporting {source_name}...")
        
        if df is None or len(df) == 0:
            logger.warning(f"No data for {source_name}")
            continue
        
        with Session(engine) as session:
            # Check for text column
            text_col = None
            for col in ["text", "Text", "body", "Body", "headline", "Headline"]:
                if col in df.columns:
                    text_col = col
                    break
            
            if not text_col:
                logger.warning(f"No text column found in {source_name}")
                continue
            
            imported = 0
            for _, row in df.iterrows():
                text_content = str(row.get(text_col, ""))
                
                if not text_content or len(text_content.strip()) < 5:
                    continue
                
                # Parse timestamp
                ts = row.get("date", datetime.now())
                if pd.notna(ts):
                    if isinstance(ts, str):
                        try:
                            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        except:
                            ts = datetime.now()
                else:
                    ts = datetime.now()
                
                # Create RawText record
                raw_text = RawText(
                    content=text_content[:10000],  # Limit text length
                    source=source_name,
                    asset_class=row.get("asset", "equity"),  # Default to equity
                    content_created_at=ts,
                    collected_at=datetime.now(),
                    metadata_={
                        "prelabeled": True,
                        "original_source": row.get("news_source", row.get("source", source_name)),
                    },
                )
                session.add(raw_text)
                session.flush()  # Get the ID
                
                # Create SentimentScore with ground truth label
                sentiment_label = row.get("sentiment_label")
                scores = standardize_sentiment_label(sentiment_label)
                
                sentiment_score = SentimentScore(
                    text_id=raw_text.id,
                    model_name="ground_truth",
                    model_version="prelabeled",
                    positive=scores["positive"],
                    negative=scores["negative"],
                    neutral=scores["neutral"],
                    compound=scores["compound"],
                    confidence=row.get("confidence", 1.0) if pd.notna(row.get("confidence")) else 1.0,
                    processed_at=datetime.now(),
                )
                session.add(sentiment_score)
                
                imported += 1
                
                if imported % batch_size == 0:
                    session.commit()
                    logger.info(f"  Imported {imported} records...")
            
            session.commit()
            logger.info(f"  Completed: {imported} records from {source_name}")
            total_imported += imported
    
    logger.info(f"\nTotal imported: {total_imported} pre-labeled records")
    return total_imported


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import pre-labeled sentiment datasets for validation"
    )
    parser.add_argument(
        "--bitcoin-path",
        type=Path,
        default=BITCOIN_TWEETS_PATH,
        help="Path to Bitcoin tweets data",
    )
    parser.add_argument(
        "--news-path",
        type=Path,
        default=FINANCIAL_NEWS_PATH,
        help="Path to Financial News data",
    )
    parser.add_argument(
        "--reddit-path",
        type=Path,
        default=REDDIT_SENTIMENT_PATH,
        help="Path to Reddit Sentiment data",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=None,
        help="Database URL (defaults to settings)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze data without importing",
    )
    parser.add_argument(
        "--sources",
        type=str,
        nargs="+",
        choices=["bitcoin", "news", "reddit"],
        default=["bitcoin", "news", "reddit"],
        help="Which sources to import",
    )
    
    args = parser.parse_args()
    
    # Load datasets
    datasets = {}
    
    if "bitcoin" in args.sources:
        try:
            datasets["bitcoin_tweets"] = load_bitcoin_tweets(args.bitcoin_path)
        except Exception as e:
            logger.error(f"Failed to load Bitcoin tweets: {e}")
    
    if "news" in args.sources:
        try:
            datasets["financial_news"] = load_financial_news(args.news_path)
        except Exception as e:
            logger.error(f"Failed to load Financial News: {e}")
    
    if "reddit" in args.sources:
        try:
            datasets["reddit_sentiment"] = load_reddit_sentiment(args.reddit_path)
        except Exception as e:
            logger.error(f"Failed to load Reddit Sentiment: {e}")
    
    if not datasets:
        logger.error("No datasets could be loaded")
        return
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Pre-labeled Dataset Summary")
    logger.info("=" * 60)
    
    total_records = 0
    for name, df in datasets.items():
        if df is not None:
            total_records += len(df)
            logger.info(f"{name}: {len(df):,} records")
    
    logger.info(f"\nTotal: {total_records:,} pre-labeled records")
    
    if args.dry_run:
        logger.info("\nDry run complete - no data imported")
        return
    
    # Import to database
    db_url = args.db_url
    if not db_url:
        try:
            settings = get_settings()
            # Convert to string and use sync driver
            db_url = str(settings.database_url).replace("+asyncpg", "+psycopg2")
        except Exception as e:
            logger.error(f"Could not get database URL from settings: {e}")
            logger.info("Use --db-url to specify database connection")
            return
    
    import_to_database(datasets, db_url, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
