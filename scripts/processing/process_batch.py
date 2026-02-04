#!/usr/bin/env python3
"""
Process a batch of texts through FinBERT on MANEFRAME GPU.

This script is designed to run on MANEFRAME III with V100 GPU.
It loads a JSON batch file, processes through FinBERT, and saves results.

Usage:
    python process_batch.py --input batch.json --output results.json
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
from transformers import AutoModelForSequenceClassification, AutoTokenizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class FinBERTAnalyzer:
    """FinBERT sentiment analyzer optimized for GPU batch processing."""
    
    def __init__(
        self,
        model_name: str = "ProsusAI/finbert",
        device: str = "cuda",
        batch_size: int = 64,
    ):
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        
        logger.info(f"Loading model: {model_name}")
        logger.info(f"Device: {device}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(device)
        self.model.eval()
        
        # FinBERT labels
        self.labels = ["positive", "negative", "neutral"]
        
        logger.info("Model loaded successfully")
    
    def analyze_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """
        Analyze a batch of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of sentiment results
        """
        results = []
        
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            batch_results = self._process_batch(batch_texts)
            results.extend(batch_results)
            
            if (i // self.batch_size + 1) % 10 == 0:
                logger.info(f"Processed {min(i + self.batch_size, len(texts))}/{len(texts)} texts")
        
        return results
    
    def _process_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """Process a single batch through the model."""
        # Truncate long texts
        texts = [t[:512] if len(t) > 512 else t for t in texts]
        
        # Tokenize
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        ).to(self.device)
        
        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
        
        # Convert to results
        results = []
        for i, text in enumerate(texts):
            prob_values = probs[i].cpu().tolist()
            
            # Create score dict
            scores = {
                label: prob_values[j] 
                for j, label in enumerate(self.labels)
            }
            
            # Calculate compound score (-1 to 1)
            compound = scores["positive"] - scores["negative"]
            
            # Determine label
            label_idx = prob_values.index(max(prob_values))
            label = self.labels[label_idx]
            
            results.append({
                "label": label,
                "compound": compound,
                "positive": scores["positive"],
                "negative": scores["negative"],
                "neutral": scores["neutral"],
            })
        
        return results


def process_batch_file(
    input_path: Path,
    output_path: Path,
    model_name: str = "ProsusAI/finbert",
    device: str = "cuda",
    batch_size: int = 64,
) -> int:
    """
    Process a batch file through FinBERT.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path to output JSON file
        model_name: Model name
        device: Device (cuda/cpu)
        batch_size: Batch size
        
    Returns:
        Number of items processed
    """
    logger.info(f"Loading batch: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    
    logger.info(f"Loaded {len(items)} items")
    
    # Extract texts
    texts = [item.get("content", "") or "" for item in items]
    
    # Initialize analyzer
    analyzer = FinBERTAnalyzer(
        model_name=model_name,
        device=device,
        batch_size=batch_size,
    )
    
    # Process
    start_time = time.time()
    sentiment_results = analyzer.analyze_batch(texts)
    elapsed = time.time() - start_time
    
    rate = len(texts) / elapsed if elapsed > 0 else 0
    logger.info(f"Processed {len(texts)} texts in {elapsed:.1f}s ({rate:.1f} texts/sec)")
    
    # Merge results with original data
    output_items = []
    for item, sentiment in zip(items, sentiment_results):
        output_items.append({
            "source_id": item.get("source_id"),
            "source": item.get("source"),
            "asset_class": item.get("asset_class"),
            "content": item.get("content"),
            "title": item.get("title"),
            "created_at": item.get("created_at"),
            "metadata": item.get("metadata"),
            "sentiment": sentiment,
            "processed_at": datetime.utcnow().isoformat(),
            "model": model_name,
        })
    
    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_items, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved results to: {output_path}")
    
    return len(output_items)


def main():
    parser = argparse.ArgumentParser(description="Process batch through FinBERT")
    parser.add_argument("--input", type=str, required=True, help="Input JSON batch file")
    parser.add_argument("--output", type=str, required=True, help="Output JSON file")
    parser.add_argument("--model", type=str, default="ProsusAI/finbert", help="Model name")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"], help="Device")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    args = parser.parse_args()
    
    # Check GPU
    if args.device == "cuda" and not torch.cuda.is_available():
        logger.warning("CUDA not available, falling back to CPU")
        args.device = "cpu"
    
    if args.device == "cuda":
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Process
    count = process_batch_file(
        input_path=Path(args.input),
        output_path=Path(args.output),
        model_name=args.model,
        device=args.device,
        batch_size=args.batch_size,
    )
    
    logger.info(f"Successfully processed {count} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
