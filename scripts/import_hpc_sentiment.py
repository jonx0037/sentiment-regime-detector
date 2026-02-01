#!/usr/bin/env python3
"""
Import HPC Sentiment Results to PostgreSQL.

Imports pre-computed sentiment analysis results from the HPC cluster.
This script handles the output from process_kaggle_sentiment.py and
imports both raw texts and their sentiment scores.

Usage:
    # Download results first
    scp jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector-hpc-*/data/processed/kaggle_sentiment_full.json ./data/processed/

    # Then import
    python scripts/import_hpc_sentiment.py --input data/processed/kaggle_sentiment_full.json
    
    # With validation (re-runs hypothesis tests with real data)
    python scripts/import_hpc_sentiment.py --input data/processed/kaggle_sentiment_full.json --validate
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def import_hpc_results(input_path: Path, run_validation: bool = False) -> dict:
    """
    Import HPC sentiment results to the database.
    
    The HPC output format:
    {
        "generated_at": "2026-01-31T...",
        "stats": {...},
        "items": [
            {
                "id": "...",
                "content": "...",
                "cleaned_content": "...",
                "created_at": "...",
                "source": "kaggle",
                "asset_class": "crypto|equity|mixed",
                "sentiment": {
                    "label": "POSITIVE|NEGATIVE|NEUTRAL",
                    "value": 1|0|-1,
                    "confidence": 0.85,
                    "probabilities": {"negative": 0.1, "neutral": 0.2, "positive": 0.7},
                    "agreement": 0.9,
                    "uncertainty": 0.05
                },
                "dataset": "crypto-tweets|financial-news|..."
            },
            ...
        ]
    }
    """
    from sqlalchemy import select, text
    from sentiment_detector.core.database import get_session_context
    from sentiment_detector.models import RawText, SentimentScore
    
    logger.info(f"Loading HPC results from: {input_path}")
    
    with open(input_path) as f:
        data = json.load(f)
    
    # Extract metadata
    generated_at = data.get("generated_at", "unknown")
    stats = data.get("stats", {})
    items = data.get("items", [])
    
    logger.info(f"HPC run completed at: {generated_at}")
    logger.info(f"Total items processed: {stats.get('processed', len(items)):,}")
    logger.info(f"Items to import: {len(items):,}")
    
    if stats.get("by_sentiment"):
        logger.info(f"Sentiment distribution: {dict(stats['by_sentiment'])}")
    
    if not items:
        logger.warning("No items found in HPC results!")
        return {"texts_created": 0, "scores_created": 0, "skipped": 0}
    
    # Track statistics
    texts_created = 0
    scores_created = 0
    skipped = 0
    errors = 0
    seen_ids = set()
    
    # Batch processing for efficiency
    batch_size = 500
    
    async with get_session_context() as session:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                try:
                    # Generate unique source_id
                    source_id = str(item.get("id", hash(item.get("content", "")[:100])))
                    source = "kaggle"
                    
                    # Skip duplicates within this import
                    batch_key = (source, source_id)
                    if batch_key in seen_ids:
                        skipped += 1
                        continue
                    seen_ids.add(batch_key)
                    
                    # Check if already exists in database
                    existing = await session.execute(
                        select(RawText).where(
                            RawText.source == source,
                            RawText.source_id == source_id,
                        )
                    )
                    existing_text = existing.scalar_one_or_none()
                    
                    if existing_text:
                        # Text exists - check if it has a sentiment score
                        score_check = await session.execute(
                            select(SentimentScore).where(
                                SentimentScore.text_id == existing_text.id
                            )
                        )
                        if score_check.scalar_one_or_none():
                            skipped += 1
                            continue
                        # Text exists but no score - add the score
                        raw_text_id = existing_text.id
                    else:
                        # Create new RawText
                        raw_text_id = uuid4()
                        
                        # Parse created_at
                        created_at = None
                        if item.get("created_at"):
                            try:
                                created_at = datetime.fromisoformat(
                                    item["created_at"].replace("Z", "+00:00")
                                )
                            except (ValueError, AttributeError):
                                created_at = datetime.now(timezone.utc)
                        
                        # Determine asset class
                        asset_class_map = {
                            "crypto": "crypto",
                            "equity": "equity", 
                            "forex": "forex",
                            "commodity": "commodity",
                            "mixed": "equity",  # Default mixed to equity
                        }
                        asset_class = asset_class_map.get(
                            item.get("asset_class", "mixed").lower(), 
                            "equity"
                        )
                        
                        raw_text = RawText(
                            id=raw_text_id,
                            source=source,
                            source_id=source_id,
                            asset_class=asset_class,
                            content=item.get("content", "")[:10000],
                            content_created_at=created_at,
                            collected_at=datetime.now(timezone.utc),
                            metadata_={
                                "dataset": item.get("dataset"),
                                "cleaned_content": item.get("cleaned_content", "")[:500],
                                "hpc_import": True,
                                "hpc_run": generated_at,
                            },
                        )
                        session.add(raw_text)
                        texts_created += 1
                    
                    # Create SentimentScore
                    sentiment = item.get("sentiment", {})
                    probabilities = sentiment.get("probabilities", {})
                    
                    # Extract probabilities
                    pos = probabilities.get("positive", 0.33)
                    neg = probabilities.get("negative", 0.33)
                    neu = probabilities.get("neutral", 0.34)
                    
                    # Compute compound score from probabilities
                    # positive - negative (ranges from -1 to 1)
                    compound = pos - neg
                    
                    sentiment_score = SentimentScore(
                        id=uuid4(),
                        text_id=raw_text_id,
                        model_name="ensemble_finbert_roberta",
                        model_version="1.0.0",
                        positive=pos,
                        negative=neg,
                        neutral=neu,
                        compound=compound,
                        confidence=sentiment.get("confidence", 0.5),
                        processed_at=datetime.now(timezone.utc),
                    )
                    session.add(sentiment_score)
                    scores_created += 1
                    
                except Exception as e:
                    errors += 1
                    if errors <= 10:
                        logger.warning(f"Error processing item: {e}")
            
            # Commit batch
            await session.commit()
            
            # Progress update
            progress = min(100, (i + batch_size) / len(items) * 100)
            logger.info(
                f"Progress: {progress:.1f}% - "
                f"Texts: {texts_created:,}, Scores: {scores_created:,}, "
                f"Skipped: {skipped:,}"
            )
        
        # Final commit
        await session.commit()
    
    logger.info(f"\n{'='*60}")
    logger.info("Import complete!")
    logger.info(f"  Texts created:  {texts_created:,}")
    logger.info(f"  Scores created: {scores_created:,}")
    logger.info(f"  Skipped:        {skipped:,}")
    logger.info(f"  Errors:         {errors:,}")
    logger.info(f"{'='*60}")
    
    result = {
        "texts_created": texts_created,
        "scores_created": scores_created,
        "skipped": skipped,
        "errors": errors,
    }
    
    # Run validation if requested
    if run_validation and scores_created > 0:
        await run_hypothesis_validation()
    
    return result


async def run_hypothesis_validation():
    """Re-run hypothesis validation with real imported data."""
    logger.info("\n" + "="*60)
    logger.info("Running Hypothesis Validation with REAL Data")
    logger.info("="*60)
    
    try:
        from sentiment_detector.validation.hypothesis_validator import HypothesisValidator
        from sentiment_detector.core.database import get_session_context
        from sqlalchemy import select, func
        from sentiment_detector.models import SentimentScore, RawText
        
        # Get date range of imported data
        async with get_session_context() as session:
            result = await session.execute(
                select(
                    func.count(SentimentScore.id),
                    func.min(RawText.content_created_at),
                    func.max(RawText.content_created_at),
                ).join(RawText)
            )
            count, min_date, max_date = result.one()
            
            logger.info(f"Data available: {count:,} sentiment scores")
            logger.info(f"Date range: {min_date} to {max_date}")
        
        # Initialize validator and run tests
        validator = HypothesisValidator()
        
        logger.info("\nValidating H1: Sentiment-Volatility Correlation...")
        h1_result = await validator.validate_h1_correlation()
        logger.info(f"  Result: {'SUPPORTED' if h1_result.supported else 'NOT SUPPORTED'}")
        logger.info(f"  Correlation: {h1_result.test_statistic:.3f}")
        logger.info(f"  p-value: {h1_result.p_value:.4f}")
        
        logger.info("\nValidating H2: Divergence Predictability...")
        h2_result = await validator.validate_h2_divergence()
        logger.info(f"  Result: {'SUPPORTED' if h2_result.supported else 'NOT SUPPORTED'}")
        logger.info(f"  Predictive ratio: {h2_result.test_statistic:.2f}x")
        
        logger.info("\nValidating H3: Regime Specificity...")
        h3_result = await validator.validate_h3_regime()
        logger.info(f"  Result: {'SUPPORTED' if h3_result.supported else 'NOT SUPPORTED'}")
        logger.info(f"  F-statistic: {h3_result.test_statistic:.2f}")
        
        # Save results
        results_path = Path("data/processed/hypothesis_validation_real_data.json")
        results_path.parent.mkdir(parents=True, exist_ok=True)
        
        validation_results = {
            "validated_at": datetime.now(timezone.utc).isoformat(),
            "data_source": "hpc_kaggle_import",
            "data_count": count,
            "date_range": {
                "start": min_date.isoformat() if min_date else None,
                "end": max_date.isoformat() if max_date else None,
            },
            "hypotheses": {
                "H1": {
                    "supported": h1_result.supported,
                    "correlation": h1_result.test_statistic,
                    "p_value": h1_result.p_value,
                    "description": h1_result.description,
                },
                "H2": {
                    "supported": h2_result.supported,
                    "predictive_ratio": h2_result.test_statistic,
                    "p_value": h2_result.p_value,
                    "description": h2_result.description,
                },
                "H3": {
                    "supported": h3_result.supported,
                    "f_statistic": h3_result.test_statistic,
                    "p_value": h3_result.p_value,
                    "description": h3_result.description,
                },
            },
        }
        
        with open(results_path, "w") as f:
            json.dump(validation_results, f, indent=2, default=str)
        
        logger.info(f"\nValidation results saved to: {results_path}")
        
    except ImportError as e:
        logger.warning(f"Hypothesis validator not available: {e}")
    except Exception as e:
        logger.error(f"Error during validation: {e}")
        import traceback
        traceback.print_exc()


def print_summary_stats(input_path: Path):
    """Print summary statistics from HPC results without importing."""
    logger.info(f"Loading summary from: {input_path}")
    
    with open(input_path) as f:
        data = json.load(f)
    
    stats = data.get("stats", {})
    items = data.get("items", [])
    
    print("\n" + "="*60)
    print("HPC SENTIMENT RESULTS SUMMARY")
    print("="*60)
    print(f"Generated at: {data.get('generated_at', 'unknown')}")
    print(f"Total processed: {stats.get('processed', len(items)):,}")
    print(f"Errors: {stats.get('errors', 0):,}")
    
    if stats.get("by_sentiment"):
        print("\nBy Sentiment:")
        for label, count in sorted(stats["by_sentiment"].items()):
            pct = count / stats.get("processed", 1) * 100
            print(f"  {label}: {count:,} ({pct:.1f}%)")
    
    if stats.get("by_asset"):
        print("\nBy Asset Class:")
        for asset, count in sorted(stats["by_asset"].items()):
            pct = count / stats.get("processed", 1) * 100
            print(f"  {asset}: {count:,} ({pct:.1f}%)")
    
    if stats.get("by_dataset"):
        print("\nBy Dataset:")
        for dataset, count in sorted(stats["by_dataset"].items()):
            pct = count / stats.get("processed", 1) * 100
            print(f"  {dataset}: {count:,} ({pct:.1f}%)")
    
    # Sample some items
    if items:
        print("\nSample Items:")
        for item in items[:3]:
            sentiment = item.get("sentiment", {})
            print(f"  - [{sentiment.get('label', '?')}] "
                  f"(conf: {sentiment.get('confidence', 0):.2f}) "
                  f"{item.get('content', '')[:60]}...")
    
    print("="*60 + "\n")


async def main():
    parser = argparse.ArgumentParser(
        description="Import HPC sentiment results to PostgreSQL",
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to HPC results JSON file",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run hypothesis validation after import",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print summary, don't import",
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    if args.summary_only:
        print_summary_stats(input_path)
        return
    
    result = await import_hpc_results(input_path, run_validation=args.validate)
    
    print(f"\n✅ Import complete!")
    print(f"   Texts created:  {result['texts_created']:,}")
    print(f"   Scores created: {result['scores_created']:,}")
    print(f"   Skipped:        {result['skipped']:,}")
    print(f"   Errors:         {result['errors']:,}")


if __name__ == "__main__":
    asyncio.run(main())
