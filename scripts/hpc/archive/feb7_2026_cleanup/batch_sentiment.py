"""
Batch Sentiment Analysis Script for MANEFRAME HPC
Processes large datasets with GPU acceleration and checkpointing.
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import pandas as pd
import torch
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('batch_sentiment.log')
    ]
)
logger = logging.getLogger(__name__)


class BatchSentimentAnalyzer:
    """
    GPU-accelerated batch sentiment analysis with checkpointing.
    """
    
    MODEL_CONFIGS = {
        "finbert": "ProsusAI/finbert",
        "distilbert": "distilbert-base-uncased-finetuned-sst-2-english",
        "roberta": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    }
    
    def __init__(
        self,
        model_name: str = "finbert",
        batch_size: int = 64,
        device: Optional[int] = None,
        checkpoint_dir: Optional[str] = None,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.checkpoint_dir = Path(checkpoint_dir) if checkpoint_dir else None
        
        # Setup device
        if device is not None:
            self.device = device
        elif torch.cuda.is_available():
            self.device = 0
            logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = -1
            logger.info("Using CPU")
        
        # Load model
        model_path = self.MODEL_CONFIGS.get(model_name, model_name)
        logger.info(f"Loading model: {model_path}")
        
        self.classifier = pipeline(
            "sentiment-analysis",
            model=model_path,
            device=self.device,
            truncation=True,
            max_length=512,
        )
        
        if self.checkpoint_dir:
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def process_batch(self, texts: List[str]) -> List[Dict]:
        """Process a batch of texts."""
        results = self.classifier(texts, batch_size=self.batch_size)
        return results
    
    def load_checkpoint(self, job_id: str) -> Optional[int]:
        """Load processing checkpoint if exists."""
        if not self.checkpoint_dir:
            return None
        
        checkpoint_file = self.checkpoint_dir / f"{job_id}_checkpoint.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                data = json.load(f)
                logger.info(f"Resuming from checkpoint: row {data['last_processed']}")
                return data['last_processed']
        return None
    
    def save_checkpoint(self, job_id: str, last_processed: int):
        """Save processing checkpoint."""
        if not self.checkpoint_dir:
            return
        
        checkpoint_file = self.checkpoint_dir / f"{job_id}_checkpoint.json"
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'last_processed': last_processed,
                'timestamp': datetime.now().isoformat(),
            }, f)
    
    def process_file(
        self,
        input_file: Path,
        output_file: Path,
        text_column: str = "text",
        job_id: Optional[str] = None,
        checkpoint_frequency: int = 1000,
    ) -> pd.DataFrame:
        """
        Process a single file with sentiment analysis.
        
        Args:
            input_file: Path to input CSV/JSON file
            output_file: Path to save results
            text_column: Name of column containing text
            job_id: Unique job identifier for checkpointing
            checkpoint_frequency: Save checkpoint every N rows
        """
        # Load data
        logger.info(f"Loading data from {input_file}")
        if input_file.suffix == '.json':
            with open(input_file) as f:
                data = json.load(f)
            # Handle nested JSON format (items array)
            if isinstance(data, dict) and 'items' in data:
                logger.info("Detected nested JSON format with 'items' array")
                df = pd.DataFrame(data['items'])
            else:
                df = pd.DataFrame(data) if isinstance(data, list) else pd.read_json(input_file)
        else:
            df = pd.read_csv(input_file)
        
        total_rows = len(df)
        logger.info(f"Loaded {total_rows} rows")
        
        # Check for checkpoint
        start_idx = 0
        if job_id:
            checkpoint_idx = self.load_checkpoint(job_id)
            if checkpoint_idx:
                start_idx = checkpoint_idx
        
        # Initialize result columns if resuming
        if 'sentiment_label' not in df.columns:
            df['sentiment_label'] = None
            df['sentiment_score'] = None
        
        # Process in batches with progress bar
        logger.info(f"Processing rows {start_idx} to {total_rows}")
        
        batch_texts = []
        batch_indices = []
        
        for idx in tqdm(range(start_idx, total_rows), desc="Analyzing"):
            text = str(df.iloc[idx][text_column])
            batch_texts.append(text)
            batch_indices.append(idx)
            
            # Process when batch is full
            if len(batch_texts) >= self.batch_size:
                results = self.process_batch(batch_texts)
                
                for i, result in zip(batch_indices, results):
                    df.at[i, 'sentiment_label'] = result['label']
                    df.at[i, 'sentiment_score'] = result['score']
                
                batch_texts = []
                batch_indices = []
                
                # Checkpoint
                if job_id and idx % checkpoint_frequency == 0:
                    self.save_checkpoint(job_id, idx)
        
        # Process remaining
        if batch_texts:
            results = self.process_batch(batch_texts)
            for i, result in zip(batch_indices, results):
                df.at[i, 'sentiment_label'] = result['label']
                df.at[i, 'sentiment_score'] = result['score']
        
        # Save results
        logger.info(f"Saving results to {output_file}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if output_file.suffix == '.json':
            df.to_json(output_file, orient='records', indent=2)
        else:
            df.to_csv(output_file, index=False)
        
        # Clean up checkpoint
        if job_id and self.checkpoint_dir:
            checkpoint_file = self.checkpoint_dir / f"{job_id}_checkpoint.json"
            if checkpoint_file.exists():
                checkpoint_file.unlink()
        
        return df


def main():
    parser = argparse.ArgumentParser(description="Batch Sentiment Analysis for MANEFRAME")
    parser.add_argument("--input-dir", type=str, required=True, help="Input directory")
    parser.add_argument("--output-dir", type=str, required=True, help="Output directory")
    parser.add_argument("--model", type=str, default="finbert", help="Model name")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size")
    parser.add_argument("--checkpoint-dir", type=str, help="Checkpoint directory")
    parser.add_argument("--num-workers", type=int, default=4, help="Number of workers")
    parser.add_argument("--text-column", type=str, default="text", help="Text column name")
    
    args = parser.parse_args()
    
    # Get SLURM job ID if available
    job_id = os.environ.get('SLURM_JOB_ID', datetime.now().strftime('%Y%m%d_%H%M%S'))
    
    # Initialize analyzer
    analyzer = BatchSentimentAnalyzer(
        model_name=args.model,
        batch_size=args.batch_size,
        checkpoint_dir=args.checkpoint_dir,
    )
    
    # Find input files
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    input_files = list(input_dir.glob("*.csv")) + list(input_dir.glob("*.json"))
    
    if not input_files:
        logger.warning(f"No CSV or JSON files found in {input_dir}")
        # Create sample data for testing
        logger.info("Creating sample data for testing...")
        sample_data = pd.DataFrame({
            'text': [
                "Stock prices reached all-time highs today.",
                "Market crash fears grow as inflation rises.",
                "Federal Reserve maintains steady interest rates.",
                "Tech sector leads market recovery.",
                "Investors remain cautious amid uncertainty.",
            ] * 20,  # 100 samples
            'source': ['test'] * 100,
            'date': [datetime.now().isoformat()] * 100,
        })
        sample_file = input_dir / "sample_data.csv"
        input_dir.mkdir(parents=True, exist_ok=True)
        sample_data.to_csv(sample_file, index=False)
        input_files = [sample_file]
        logger.info(f"Created sample data at {sample_file}")
    
    logger.info(f"Found {len(input_files)} input files")
    
    # Process each file
    start_time = time.time()
    total_processed = 0
    
    for input_file in input_files:
        output_file = output_dir / f"{input_file.stem}_sentiment{input_file.suffix}"
        file_job_id = f"{job_id}_{input_file.stem}"
        
        try:
            df = analyzer.process_file(
                input_file=input_file,
                output_file=output_file,
                text_column=args.text_column,
                job_id=file_job_id,
            )
            total_processed += len(df)
            
            # Log summary stats
            if 'sentiment_label' in df.columns:
                label_counts = df['sentiment_label'].value_counts()
                logger.info(f"Results for {input_file.name}:")
                for label, count in label_counts.items():
                    logger.info(f"  {label}: {count} ({count/len(df)*100:.1f}%)")
                    
        except Exception as e:
            logger.error(f"Error processing {input_file}: {e}")
            raise
    
    elapsed = time.time() - start_time
    logger.info(f"\n{'='*50}")
    logger.info(f"Batch processing complete!")
    logger.info(f"Total processed: {total_processed} texts")
    logger.info(f"Total time: {elapsed:.1f} seconds")
    logger.info(f"Throughput: {total_processed/elapsed:.1f} texts/second")
    logger.info(f"{'='*50}")


if __name__ == "__main__":
    main()
