#!/usr/bin/env python3
"""
Import Kaggle data and generate sentiment scores.

This script:
1. Loads all Kaggle datasets
2. Applies text preprocessing
3. Runs ensemble sentiment analysis
4. Saves results to JSON for database import

Usage:
    python scripts/process_kaggle_sentiment.py
    python scripts/process_kaggle_sentiment.py --limit 1000 --output results.json
"""

import argparse
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.collectors.kaggle_loader import KaggleDataLoader
from sentiment_detector.preprocessing import TextCleaner
from sentiment_detector.models.sentiment_ensemble import SentimentEnsemble, SentimentLabel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def process_kaggle_data(
    data_dir: str = "data/kaggle",
    output_path: str = "data/processed/kaggle_sentiment.json",
    limit: int | None = None,
    batch_size: int = 100,
) -> dict:
    """
    Process Kaggle data with sentiment analysis.
    
    Args:
        data_dir: Directory containing Kaggle datasets
        output_path: Path to save processed results
        limit: Maximum items to process
        batch_size: Batch size for processing
        
    Returns:
        Summary statistics
    """
    # Initialize components
    logger.info("Initializing components...")
    loader = KaggleDataLoader(data_dir)
    cleaner = TextCleaner()
    ensemble = SentimentEnsemble()
    
    # Load data
    logger.info(f"Loading data from {data_dir}...")
    items = loader.load_all(limit=limit)
    logger.info(f"Loaded {len(items):,} items")
    
    if not items:
        logger.warning("No items loaded!")
        return {"error": "no_items"}
    
    # Process items
    results = []
    stats = {
        "total_loaded": len(items),
        "processed": 0,
        "errors": 0,
        "by_sentiment": Counter(),
        "by_asset": Counter(),
        "by_dataset": Counter(),
    }
    
    logger.info(f"Processing {len(items):,} items in batches of {batch_size}...")
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        for item in batch:
            try:
                # Clean text
                cleaned = cleaner.clean(item.content)
                
                # Get asset class for weight adjustment
                asset_class = str(item.asset_class).split(".")[-1].lower()
                
                # Get sentiment prediction
                prediction = ensemble.predict(
                    cleaned.cleaned,  # Use .cleaned attribute
                    asset_class=asset_class
                )
                
                # Build result
                result = {
                    "id": item.source_id,
                    "content": item.content[:1000],  # Truncate for storage
                    "cleaned_content": cleaned.cleaned[:1000],  # Use .cleaned
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "source": str(item.source),
                    "asset_class": asset_class,
                    "sentiment": {
                        "label": prediction.label.name,
                        "value": prediction.label.value,
                        "confidence": prediction.confidence,
                        "probabilities": {
                            "negative": prediction.probabilities[0],
                            "neutral": prediction.probabilities[1],
                            "positive": prediction.probabilities[2],
                        },
                        "agreement": prediction.agreement,
                        "uncertainty": prediction.uncertainty,
                    },
                    "metadata": {
                        "dataset": item.metadata.get("dataset", "unknown"),
                        "cashtags": cleaned.cashtags,
                        "hashtags": cleaned.hashtags,
                    }
                }
                
                results.append(result)
                stats["processed"] += 1
                stats["by_sentiment"][prediction.label.name] += 1
                stats["by_asset"][asset_class] += 1
                stats["by_dataset"][item.metadata.get("dataset", "unknown")] += 1
                
            except Exception as e:
                logger.debug(f"Error processing item {item.source_id}: {e}")
                stats["errors"] += 1
        
        # Progress logging
        if (i + batch_size) % 1000 == 0 or (i + batch_size) >= len(items):
            pct = min(100, (i + batch_size) / len(items) * 100)
            logger.info(f"Progress: {pct:.1f}% ({stats['processed']:,} processed)")
    
    # Save results
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "generated_at": datetime.utcnow().isoformat(),
        "stats": {
            "total_loaded": stats["total_loaded"],
            "processed": stats["processed"],
            "errors": stats["errors"],
            "by_sentiment": dict(stats["by_sentiment"]),
            "by_asset": dict(stats["by_asset"]),
            "by_dataset": dict(stats["by_dataset"]),
        },
        "items": results,
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, default=str)
    
    logger.info(f"Results saved to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total loaded:  {stats['total_loaded']:,}")
    print(f"Processed:     {stats['processed']:,}")
    print(f"Errors:        {stats['errors']:,}")
    print()
    print("By Sentiment:")
    for label, count in sorted(stats["by_sentiment"].items()):
        pct = count / stats["processed"] * 100 if stats["processed"] else 0
        print(f"  {label:10s}: {count:>8,} ({pct:5.1f}%)")
    print()
    print("By Asset Class:")
    for asset, count in sorted(stats["by_asset"].items(), key=lambda x: -x[1]):
        pct = count / stats["processed"] * 100 if stats["processed"] else 0
        print(f"  {asset:10s}: {count:>8,} ({pct:5.1f}%)")
    print()
    print("By Dataset:")
    for ds, count in sorted(stats["by_dataset"].items(), key=lambda x: -x[1]):
        pct = count / stats["processed"] * 100 if stats["processed"] else 0
        print(f"  {ds:25s}: {count:>8,} ({pct:5.1f}%)")
    print("=" * 60)
    
    return output_data["stats"]


def main():
    parser = argparse.ArgumentParser(
        description="Process Kaggle data with sentiment analysis"
    )
    parser.add_argument(
        "--data-dir",
        default="data/kaggle",
        help="Directory containing Kaggle datasets"
    )
    parser.add_argument(
        "--output",
        default="data/processed/kaggle_sentiment.json",
        help="Output file path"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum items to process"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing"
    )
    
    args = parser.parse_args()
    
    process_kaggle_data(
        data_dir=args.data_dir,
        output_path=args.output,
        limit=args.limit,
        batch_size=args.batch_size,
    )


if __name__ == "__main__":
    main()
