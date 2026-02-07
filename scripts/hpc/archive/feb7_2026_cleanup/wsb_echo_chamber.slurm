#!/bin/bash
#SBATCH --job-name=wsb_echo_sentiment
#SBATCH --output=logs/wsb_echo_chamber_%j.log
#SBATCH --error=logs/wsb_echo_chamber_%j.err
#SBATCH --partition=gpgpu-1
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --mail-user=$USER@smu.edu
#SBATCH --mail-type=ALL

# ============================================================================
# WSB Echo Chamber Sentiment Processing - SMU ManeFrame M3
# ============================================================================
#
# This SLURM script processes the WSB Echo Chamber Reddit data through
# FinBERT + RoBERTa sentiment ensemble on V100 GPU.
#
# Previous HPC Performance (Job #22738072):
#   - 218,702 items processed in 47 minutes
#   - Rate: ~77 items/second
#
# Expected Performance for WSB Echo Chamber:
#   - ~7,000 items across 6 tickers
#   - Estimated time: ~2-3 minutes processing + overhead
#
# Usage:
#   sbatch scripts/hpc/wsb_echo_chamber.slurm
#
# ============================================================================

echo "=============================================="
echo "WSB Echo Chamber Sentiment Processing"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Load modules
module purge
module load python/3.10
module load cuda/11.8
module load cudnn/8.6

# Set up environment
export CUDA_VISIBLE_DEVICES=0
export TRANSFORMERS_CACHE=$HOME/.cache/huggingface
export HF_HOME=$HOME/.cache/huggingface

# Navigate to project directory
cd $HOME/capstone

# Activate virtual environment
source venv/bin/activate

# Check GPU availability
echo ""
echo "GPU Check:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

# Set paths
BATCH_DIR="data/hpc_batches/wsb_echo_chamber"
OUTPUT_DIR="results/wsb_echo_chamber_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="logs/wsb_echo_chamber_$SLURM_JOB_ID.progress"

mkdir -p $OUTPUT_DIR
mkdir -p logs

# Count batches
NUM_BATCHES=$(ls -1 $BATCH_DIR/*.json 2>/dev/null | wc -l)
echo "Found $NUM_BATCHES batch files"
echo ""

# Process batches
echo "Starting sentiment processing..."
echo "Output: $OUTPUT_DIR"
echo ""

python3 << 'PYTHON_SCRIPT'
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    pipeline
)

# Configuration
BATCH_DIR = Path(os.environ.get("BATCH_DIR", "data/hpc_batches/wsb_echo_chamber"))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "results/wsb_echo_chamber"))
MAX_LENGTH = 512

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
print()

# Load models
print("Loading FinBERT model...")
finbert_tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
finbert_model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
finbert_model = finbert_model.to("cuda" if torch.cuda.is_available() else "cpu")
finbert_model.eval()

print("Loading RoBERTa model...")
roberta_tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
roberta_model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
roberta_model = roberta_model.to("cuda" if torch.cuda.is_available() else "cpu")
roberta_model.eval()

print("Models loaded successfully!\n")

def process_text_finbert(text):
    """Process text through FinBERT."""
    inputs = finbert_tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        max_length=MAX_LENGTH,
        padding=True
    )
    inputs = {k: v.to(finbert_model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = finbert_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0].cpu().numpy()
    
    # FinBERT: positive, negative, neutral
    return {
        "positive": float(probs[0]),
        "negative": float(probs[1]),
        "neutral": float(probs[2]),
    }

def process_text_roberta(text):
    """Process text through RoBERTa."""
    inputs = roberta_tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        max_length=MAX_LENGTH,
        padding=True
    )
    inputs = {k: v.to(roberta_model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = roberta_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0].cpu().numpy()
    
    # RoBERTa: negative, neutral, positive
    return {
        "negative": float(probs[0]),
        "neutral": float(probs[1]),
        "positive": float(probs[2]),
    }

def compute_ensemble(finbert_scores, roberta_scores):
    """Compute weighted ensemble of FinBERT and RoBERTa scores."""
    # Weights: FinBERT 60%, RoBERTa 40% (FinBERT trained on financial text)
    weights = {"finbert": 0.6, "roberta": 0.4}
    
    ensemble = {
        "positive": weights["finbert"] * finbert_scores["positive"] + 
                   weights["roberta"] * roberta_scores["positive"],
        "negative": weights["finbert"] * finbert_scores["negative"] + 
                   weights["roberta"] * roberta_scores["negative"],
        "neutral": weights["finbert"] * finbert_scores["neutral"] + 
                   weights["roberta"] * roberta_scores["neutral"],
    }
    
    # Compute compound score (-1 to 1)
    ensemble["compound"] = ensemble["positive"] - ensemble["negative"]
    
    # Confidence is max probability
    ensemble["confidence"] = max(ensemble["positive"], ensemble["negative"], ensemble["neutral"])
    
    return ensemble

# Process all batches
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
batch_files = sorted(BATCH_DIR.glob("*.json"))
batch_files = [f for f in batch_files if f.name != "manifest.json"]

print(f"Processing {len(batch_files)} batch files...")

total_processed = 0
start_time = time.time()

for batch_file in batch_files:
    print(f"\nProcessing {batch_file.name}...")
    batch_start = time.time()
    
    with open(batch_file) as f:
        batch_data = json.load(f)
    
    items = batch_data.get("items", [])
    results = []
    
    for item in items:
        text = item.get("text", "")
        if not text or len(text) < 10:
            continue
        
        try:
            finbert_scores = process_text_finbert(text)
            roberta_scores = process_text_roberta(text)
            ensemble = compute_ensemble(finbert_scores, roberta_scores)
            
            result = {
                "id": item.get("id"),
                "ticker": item.get("ticker"),
                "timestamp": item.get("timestamp"),
                "text_preview": text[:100],
                "finbert": finbert_scores,
                "roberta": roberta_scores,
                "ensemble": ensemble,
                "processed_at": datetime.now().isoformat(),
            }
            results.append(result)
            
        except Exception as e:
            print(f"  Error processing item: {e}")
            continue
    
    # Save results
    output_file = OUTPUT_DIR / f"results_{batch_file.stem}.json"
    with open(output_file, "w") as f:
        json.dump({
            "batch_id": batch_data.get("batch_id"),
            "source": "wsb_echo_chamber",
            "num_items": len(results),
            "processed_at": datetime.now().isoformat(),
            "items": results,
        }, f, indent=2)
    
    batch_time = time.time() - batch_start
    total_processed += len(results)
    
    print(f"  Processed {len(results)} items in {batch_time:.1f}s ({len(results)/batch_time:.1f} items/s)")

# Summary
total_time = time.time() - start_time
print(f"\n{'='*60}")
print(f"Processing Complete!")
print(f"{'='*60}")
print(f"Total items: {total_processed}")
print(f"Total time: {total_time:.1f}s ({total_time/60:.1f} min)")
print(f"Average rate: {total_processed/total_time:.1f} items/s")
print(f"Output directory: {OUTPUT_DIR}")

# Create summary manifest
summary = {
    "job_id": os.environ.get("SLURM_JOB_ID"),
    "completed_at": datetime.now().isoformat(),
    "total_items": total_processed,
    "total_time_seconds": total_time,
    "items_per_second": total_processed / total_time if total_time > 0 else 0,
    "output_directory": str(OUTPUT_DIR),
    "batch_files_processed": len(batch_files),
}

with open(OUTPUT_DIR / "processing_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nSummary saved to: {OUTPUT_DIR}/processing_summary.json")

PYTHON_SCRIPT

# Check exit status
PYTHON_EXIT=$?

echo ""
echo "=============================================="
echo "Job Complete"
echo "Exit Status: $PYTHON_EXIT"
echo "End: $(date)"
echo "=============================================="

# Notify if successful
if [ $PYTHON_EXIT -eq 0 ]; then
    echo "SUCCESS: WSB Echo Chamber processing complete"
    echo "Results in: $OUTPUT_DIR"
else
    echo "ERROR: Processing failed with exit code $PYTHON_EXIT"
fi

exit $PYTHON_EXIT
