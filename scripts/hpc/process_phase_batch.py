#!/usr/bin/env python3
"""
Process Phase Batch Files through FinBERT + RoBERTa Ensemble.

This script is designed to run on ManeFrame M3 with V100 GPU.
It processes batch files from the phased HPC export and saves results.

Usage:
    python process_phase_batch.py --input batch.json --output results.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class SentimentEnsemble:
    """FinBERT + RoBERTa sentiment ensemble for financial text."""
    
    def __init__(
        self,
        device: str = "cuda",
        batch_size: int = 64,
    ):
        self.device = device
        self.batch_size = batch_size
        
        # Load FinBERT
        logger.info("Loading FinBERT...")
        self.finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.finbert_model.to(device)
        self.finbert_model.eval()
        self.finbert_labels = ["positive", "negative", "neutral"]
        
        # Load Twitter RoBERTa (good for social media)
        logger.info("Loading Twitter-RoBERTa...")
        self.roberta_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.roberta_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
        self.roberta_model.to(device)
        self.roberta_model.eval()
        self.roberta_labels = ["negative", "neutral", "positive"]
        
        logger.info(f"Models loaded on {device}")
    
    def analyze(self, texts: list[str]) -> list[dict[str, Any]]:
        """
        Analyze texts through both models and ensemble results.
        """
        results = []
        total = len(texts)
        
        for i in range(0, total, self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            
            # Get predictions from both models
            finbert_preds = self._predict_finbert(batch_texts)
            roberta_preds = self._predict_roberta(batch_texts)
            
            # Ensemble
            for j, (fb, rb) in enumerate(zip(finbert_preds, roberta_preds)):
                # Average probabilities
                pos = (fb["positive"] + rb["positive"]) / 2
                neg = (fb["negative"] + rb["negative"]) / 2
                neu = (fb["neutral"] + rb["neutral"]) / 2
                
                # Compound score
                compound = pos - neg
                
                # Agreement score (how much models agree)
                agreement = 1 - abs(fb["positive"] - rb["positive"]) - abs(fb["negative"] - rb["negative"])
                agreement = max(0, agreement)
                
                # Ensemble label
                probs = {"positive": pos, "negative": neg, "neutral": neu}
                label = max(probs, key=probs.get)
                
                results.append({
                    "label": label.upper(),
                    "value": 1 if label == "positive" else (-1 if label == "negative" else 0),
                    "compound": round(compound, 4),
                    "confidence": round(max(pos, neg, neu), 4),
                    "probabilities": {
                        "positive": round(pos, 4),
                        "negative": round(neg, 4),
                        "neutral": round(neu, 4),
                    },
                    "agreement": round(agreement, 4),
                    "finbert": {
                        "label": fb["label"],
                        "positive": round(fb["positive"], 4),
                        "negative": round(fb["negative"], 4),
                        "neutral": round(fb["neutral"], 4),
                    },
                    "roberta": {
                        "label": rb["label"],
                        "positive": round(rb["positive"], 4),
                        "negative": round(rb["negative"], 4),
                        "neutral": round(rb["neutral"], 4),
                    },
                })
            
            # Progress
            processed = min(i + self.batch_size, total)
            if (processed // self.batch_size) % 10 == 0:
                pct = processed / total * 100
                logger.info(f"Progress: {processed:,}/{total:,} ({pct:.1f}%)")
        
        return results
    
    def _predict_finbert(self, texts: list[str]) -> list[dict]:
        """Get FinBERT predictions."""
        texts = [t[:512] if t else "" for t in texts]
        
        inputs = self.finbert_tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.finbert_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
        
        results = []
        for i in range(len(texts)):
            prob_values = probs[i].cpu().tolist()
            label_idx = prob_values.index(max(prob_values))
            results.append({
                "label": self.finbert_labels[label_idx],
                "positive": prob_values[0],
                "negative": prob_values[1],
                "neutral": prob_values[2],
            })
        
        return results
    
    def _predict_roberta(self, texts: list[str]) -> list[dict]:
        """Get RoBERTa predictions."""
        texts = [t[:512] if t else "" for t in texts]
        
        inputs = self.roberta_tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.roberta_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
        
        results = []
        for i in range(len(texts)):
            prob_values = probs[i].cpu().tolist()
            label_idx = prob_values.index(max(prob_values))
            results.append({
                "label": self.roberta_labels[label_idx],
                "negative": prob_values[0],
                "neutral": prob_values[1],
                "positive": prob_values[2],
            })
        
        return results


def process_batch(
    input_path: Path,
    output_path: Path,
    batch_size: int = 64,
    device: int = 0,
) -> dict:
    """
    Process a batch file and save results.
    
    Args:
        input_path: Path to input JSON batch file
        output_path: Path to output results file
        batch_size: GPU batch size
        device: GPU device index
        
    Returns:
        Statistics dict
    """
    start_time = time.time()
    
    logger.info(f"Loading batch: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both direct list and wrapped format
    if isinstance(data, list):
        items = data
    else:
        items = data.get("items", [])
    
    logger.info(f"Loaded {len(items):,} items")
    
    if not items:
        logger.warning("No items to process!")
        return {"processed": 0, "elapsed": 0}
    
    # Extract texts
    texts = [item.get("content", "") for item in items]
    
    # Initialize ensemble
    device_str = f"cuda:{device}" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device_str}")
    
    ensemble = SentimentEnsemble(device=device_str, batch_size=batch_size)
    
    # Process
    logger.info("Starting sentiment analysis...")
    sentiments = ensemble.analyze(texts)
    
    # Combine with original items
    results = []
    for item, sentiment in zip(items, sentiments):
        result = {
            "id": item.get("id"),
            "source": item.get("source"),
            "phase": item.get("phase"),
            "created_at": item.get("created_at"),
            "content": item.get("content", "")[:500],  # Truncate for output
            "sentiment": sentiment,
        }
        if "ticker" in item:
            result["ticker"] = item["ticker"]
        results.append(result)
    
    # Calculate stats
    elapsed = time.time() - start_time
    rate = len(items) / elapsed if elapsed > 0 else 0
    
    by_sentiment = {}
    for r in results:
        label = r["sentiment"]["label"]
        by_sentiment[label] = by_sentiment.get(label, 0) + 1
    
    stats = {
        "processed": len(items),
        "elapsed_seconds": round(elapsed, 2),
        "items_per_second": round(rate, 2),
        "by_sentiment": by_sentiment,
    }
    
    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "input_file": str(input_path),
        "stats": stats,
        "items": results,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, default=str)
    
    logger.info(f"Saved results to: {output_path}")
    logger.info(f"Processed {len(items):,} items in {elapsed:.1f}s ({rate:.1f} items/sec)")
    logger.info(f"Sentiment distribution: {by_sentiment}")
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Process sentiment batch on GPU")
    parser.add_argument("--input", required=True, help="Input JSON batch file")
    parser.add_argument("--output", required=True, help="Output results file")
    parser.add_argument("--batch-size", type=int, default=128, help="GPU batch size")
    parser.add_argument("--device", type=int, default=0, help="GPU device index")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    stats = process_batch(
        input_path=input_path,
        output_path=output_path,
        batch_size=args.batch_size,
        device=args.device,
    )
    
    logger.info("Processing complete!")
    logger.info(f"Stats: {json.dumps(stats)}")


if __name__ == "__main__":
    main()
