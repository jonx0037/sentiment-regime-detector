#!/usr/bin/env python3
"""
Import Phased HPC Sentiment Results to PostgreSQL.

This script imports sentiment results from Phase 1 (News + WSB) and Phase 2 (Reddit backfill)
processed on ManeFrame M3 using FinBERT + RoBERTa ensemble.

Phase 1: News texts (existing in DB) + WSB Echo Chamber (new data)
Phase 2: Reddit texts (existing in DB, need scores)

Usage:
    python scripts/import_phased_hpc_results.py
    
    # Import only Phase 1
    python scripts/import_phased_hpc_results.py --phase 1
    
    # Import only Phase 2
    python scripts/import_phased_hpc_results.py --phase 2
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Paths
PHASE1_FILE = Path("data/processed/phase1_results.json")
PHASE2_DIR = Path("data/processed/phase2")


async def import_phase1_results():
    """Import Phase 1 results (News + WSB Echo Chamber)."""
    from sqlalchemy import select
    from sentiment_detector.core.database import get_session_context
    from sentiment_detector.models import RawText, SentimentScore
    
    if not PHASE1_FILE.exists():
        logger.error(f"Phase 1 results not found: {PHASE1_FILE}")
        return {"error": "File not found"}
    
    logger.info(f"Loading Phase 1 results from: {PHASE1_FILE}")
    with open(PHASE1_FILE) as f:
        data = json.load(f)
    
    stats = data.get("stats", {})
    items = data.get("items", [])
    
    logger.info(f"Phase 1 stats: {stats}")
    logger.info(f"Items to import: {len(items):,}")
    
    # Track statistics
    news_scores_created = 0
    wsb_texts_created = 0
    wsb_scores_created = 0
    skipped = 0
    errors = 0
    
    batch_size = 500
    
    async with get_session_context() as session:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                try:
                    item_id = item.get("id", "")
                    source = item.get("source", "")
                    phase = item.get("phase", "")
                    sentiment = item.get("sentiment", {})
                    
                    if phase == "1_news":
                        # News texts already exist in DB - just add sentiment score
                        try:
                            from uuid import UUID
                            text_uuid = UUID(item_id)
                        except (ValueError, TypeError):
                            errors += 1
                            continue
                        
                        # Check if text exists
                        result = await session.execute(
                            select(RawText).where(RawText.id == text_uuid)
                        )
                        existing_text = result.scalar_one_or_none()
                        
                        if not existing_text:
                            skipped += 1
                            continue
                        
                        # Check if score already exists
                        score_check = await session.execute(
                            select(SentimentScore).where(
                                SentimentScore.text_id == text_uuid,
                                SentimentScore.model_name == "ensemble_finbert_roberta"
                            )
                        )
                        if score_check.scalar_one_or_none():
                            skipped += 1
                            continue
                        
                        # Add sentiment score
                        probs = sentiment.get("probabilities", {})
                        score = SentimentScore(
                            id=uuid4(),
                            text_id=text_uuid,
                            model_name="ensemble_finbert_roberta",
                            model_version="1.0.0",
                            positive=probs.get("positive", 0.33),
                            negative=probs.get("negative", 0.33),
                            neutral=probs.get("neutral", 0.34),
                            compound=sentiment.get("compound", 0),
                            confidence=sentiment.get("confidence", 0.5),
                            processed_at=datetime.now(timezone.utc),
                        )
                        session.add(score)
                        news_scores_created += 1
                    
                    elif phase == "1_wsb":
                        # WSB Echo Chamber - new texts, need to create both
                        ticker = item.get("ticker", "")
                        content = item.get("content", "")
                        
                        if not content or content in ("[removed]", "[deleted]"):
                            skipped += 1
                            continue
                        
                        # Parse created_at
                        created_at = None
                        if item.get("created_at"):
                            try:
                                created_at = datetime.fromisoformat(
                                    str(item["created_at"]).replace("Z", "+00:00")
                                )
                            except (ValueError, AttributeError):
                                created_at = datetime.now(timezone.utc)
                        else:
                            created_at = datetime.now(timezone.utc)
                        
                        # Create RawText
                        raw_text_id = uuid4()
                        raw_text = RawText(
                            id=raw_text_id,
                            source="wsb_echo_chamber",
                            source_id=item_id,
                            asset_class="equity",
                            content=content[:10000],
                            content_created_at=created_at,
                            collected_at=datetime.now(timezone.utc),
                            metadata_={
                                "ticker": ticker,
                                "dataset": "wsb_echo_chamber",
                                "hpc_import": True,
                                "phase": "phase1",
                            },
                        )
                        session.add(raw_text)
                        wsb_texts_created += 1
                        
                        # Create SentimentScore
                        probs = sentiment.get("probabilities", {})
                        score = SentimentScore(
                            id=uuid4(),
                            text_id=raw_text_id,
                            model_name="ensemble_finbert_roberta",
                            model_version="1.0.0",
                            positive=probs.get("positive", 0.33),
                            negative=probs.get("negative", 0.33),
                            neutral=probs.get("neutral", 0.34),
                            compound=sentiment.get("compound", 0),
                            confidence=sentiment.get("confidence", 0.5),
                            processed_at=datetime.now(timezone.utc),
                        )
                        session.add(score)
                        wsb_scores_created += 1
                    
                except Exception as e:
                    errors += 1
                    if errors <= 10:
                        logger.warning(f"Error processing item: {e}")
            
            await session.commit()
            
            progress = min(100, (i + batch_size) / len(items) * 100)
            logger.info(
                f"Phase 1 Progress: {progress:.1f}% - "
                f"News scores: {news_scores_created:,}, "
                f"WSB texts: {wsb_texts_created:,}, WSB scores: {wsb_scores_created:,}"
            )
        
        await session.commit()
    
    logger.info("\n" + "=" * 60)
    logger.info("Phase 1 Import Complete!")
    logger.info(f"  News sentiment scores: {news_scores_created:,}")
    logger.info(f"  WSB texts created:     {wsb_texts_created:,}")
    logger.info(f"  WSB scores created:    {wsb_scores_created:,}")
    logger.info(f"  Skipped:               {skipped:,}")
    logger.info(f"  Errors:                {errors:,}")
    logger.info("=" * 60)
    
    return {
        "news_scores": news_scores_created,
        "wsb_texts": wsb_texts_created,
        "wsb_scores": wsb_scores_created,
        "skipped": skipped,
        "errors": errors,
    }


async def import_phase2_results():
    """Import Phase 2 results (Reddit backfill - existing texts, add scores)."""
    from sqlalchemy import select
    from sentiment_detector.core.database import get_session_context
    from sentiment_detector.models import RawText, SentimentScore
    
    if not PHASE2_DIR.exists():
        logger.error(f"Phase 2 results not found: {PHASE2_DIR}")
        return {"error": "Directory not found"}
    
    batch_files = sorted(PHASE2_DIR.glob("phase2_results_*.json"))
    logger.info(f"Found {len(batch_files)} Phase 2 batch files")
    
    # Track statistics
    scores_created = 0
    skipped = 0
    errors = 0
    
    async with get_session_context() as session:
        for batch_file in batch_files:
            logger.info(f"Processing: {batch_file.name}")
            
            with open(batch_file) as f:
                data = json.load(f)
            
            items = data.get("items", [])
            batch_size = 500
            
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                
                for item in batch:
                    try:
                        item_id = item.get("id", "")
                        sentiment = item.get("sentiment", {})
                        
                        # Reddit texts already exist - just add score
                        try:
                            from uuid import UUID
                            text_uuid = UUID(item_id)
                        except (ValueError, TypeError):
                            errors += 1
                            continue
                        
                        # Check if text exists
                        result = await session.execute(
                            select(RawText).where(RawText.id == text_uuid)
                        )
                        existing_text = result.scalar_one_or_none()
                        
                        if not existing_text:
                            skipped += 1
                            continue
                        
                        # Check if score already exists
                        score_check = await session.execute(
                            select(SentimentScore).where(
                                SentimentScore.text_id == text_uuid,
                                SentimentScore.model_name == "ensemble_finbert_roberta"
                            )
                        )
                        if score_check.scalar_one_or_none():
                            skipped += 1
                            continue
                        
                        # Add sentiment score
                        probs = sentiment.get("probabilities", {})
                        score = SentimentScore(
                            id=uuid4(),
                            text_id=text_uuid,
                            model_name="ensemble_finbert_roberta",
                            model_version="1.0.0",
                            positive=probs.get("positive", 0.33),
                            negative=probs.get("negative", 0.33),
                            neutral=probs.get("neutral", 0.34),
                            compound=sentiment.get("compound", 0),
                            confidence=sentiment.get("confidence", 0.5),
                            processed_at=datetime.now(timezone.utc),
                        )
                        session.add(score)
                        scores_created += 1
                        
                    except Exception as e:
                        errors += 1
                        if errors <= 10:
                            logger.warning(f"Error processing item: {e}")
                
                await session.commit()
            
            logger.info(f"  Completed {batch_file.name}: {scores_created:,} scores so far")
        
        await session.commit()
    
    logger.info("\n" + "=" * 60)
    logger.info("Phase 2 Import Complete!")
    logger.info(f"  Reddit scores created: {scores_created:,}")
    logger.info(f"  Skipped:               {skipped:,}")
    logger.info(f"  Errors:                {errors:,}")
    logger.info("=" * 60)
    
    return {
        "scores_created": scores_created,
        "skipped": skipped,
        "errors": errors,
    }


async def main():
    parser = argparse.ArgumentParser(description="Import phased HPC sentiment results")
    parser.add_argument("--phase", type=int, choices=[1, 2], help="Import only specified phase")
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("IMPORTING HPC SENTIMENT RESULTS")
    logger.info("=" * 60)
    
    results = {}
    
    if args.phase is None or args.phase == 1:
        logger.info("\n>>> Phase 1: News + WSB Echo Chamber")
        results["phase1"] = await import_phase1_results()
    
    if args.phase is None or args.phase == 2:
        logger.info("\n>>> Phase 2: Reddit Backfill")
        results["phase2"] = await import_phase2_results()
    
    logger.info("\n" + "=" * 60)
    logger.info("ALL IMPORTS COMPLETE")
    logger.info("=" * 60)
    
    # Print summary
    total_scores = 0
    total_texts = 0
    
    if "phase1" in results:
        p1 = results["phase1"]
        total_scores += p1.get("news_scores", 0) + p1.get("wsb_scores", 0)
        total_texts += p1.get("wsb_texts", 0)
    
    if "phase2" in results:
        p2 = results["phase2"]
        total_scores += p2.get("scores_created", 0)
    
    logger.info(f"Total new texts:  {total_texts:,}")
    logger.info(f"Total new scores: {total_scores:,}")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())
