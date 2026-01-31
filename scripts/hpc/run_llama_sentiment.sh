#!/bin/bash
#SBATCH -J llama_sentiment        # Job name
#SBATCH -o logs/llama_sentiment_%j.out  # Output file
#SBATCH -e logs/llama_sentiment_%j.err  # Error file
#SBATCH -p fp-gpgpu-3             # Production GPU partition (7 day limit)
#SBATCH -N 1                      # 1 node
#SBATCH -n 8                      # 8 CPU cores
#SBATCH --gres=gpu:1              # 1 GPU (A100 or V100)
#SBATCH --mem=64G                 # Memory (Llama 7B needs ~14GB VRAM, buffer for batching)
#SBATCH -t 48:00:00               # 48 hour limit for full dataset
#SBATCH -A jcheun_ds6210_1262_401_0001
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jarocha@mail.smu.edu

# ============================================================
# Llama 3 (7B) Sentiment Processing
# Processes Kaggle items through Llama 3 for ensemble integration
# Per Draft-1 Abstract: "ensemble transformer models (FinBERT, Llama 3)"
# ============================================================

echo "=============================================="
echo "Llama 3 (7B) Sentiment Processing"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Setup
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector-hpc-20260131"
cd $PROJECT_DIR

# Load modules - using the pytorch environment which has CUDA
module load python/3.11.11/pytorch

# Add local bin to PATH for user-installed packages
export PATH="$HOME/.local/bin:$PATH"
export HF_HOME="$PROJECT_DIR/.cache/huggingface"
export TRANSFORMERS_CACHE="$PROJECT_DIR/.cache/huggingface"

# Create output directories
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/data/processed
mkdir -p $PROJECT_DIR/.cache/huggingface

# Show resources
echo -e "\n1. Resources allocated:"
echo "CPUs: $SLURM_CPUS_ON_NODE"
echo "Memory: ${SLURM_MEM_PER_NODE:-64G}"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader

# Check Python environment
echo -e "\n2. Python environment:"
python3 --version
python3 -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"
python3 -c "import torch; print(f'CUDA device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Check if Llama model needs to be downloaded
echo -e "\n3. Checking Llama model access..."
# Note: Llama 3 requires HuggingFace login - ensure token is set
if [ -z "$HF_TOKEN" ]; then
    echo "Warning: HF_TOKEN not set. You may need to login with: huggingface-cli login"
fi

# Run Llama sentiment processing
echo -e "\n4. Starting Llama 3 sentiment processing..."
echo "Processing Kaggle items through Llama 3 (7B)"

# Use the llama_sentiment.py module
python3 << 'PYTHON_SCRIPT'
import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import torch
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Llama 3 sentiment processing...")
    
    # Check CUDA
    if not torch.cuda.is_available():
        logger.error("CUDA not available! Exiting.")
        sys.exit(1)
    
    logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
    logger.info(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    
    # Import our modules
    try:
        from sentiment_detector.models.llama_sentiment import (
            LlamaSentimentModel, 
            LlamaConfig, 
            LlamaBackend
        )
        logger.info("Successfully imported LlamaSentimentModel")
    except ImportError as e:
        logger.error(f"Failed to import: {e}")
        logger.info("Falling back to direct transformers usage...")
        
        # Fallback: Use transformers directly
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        model_name = "meta-llama/Llama-3.2-3B-Instruct"  # Smaller model for testing
        logger.info(f"Loading {model_name}...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        logger.info("Model loaded successfully!")
        
        # Test inference
        test_text = "The stock market is crashing and investors are panicking."
        prompt = f"""Analyze the sentiment of this financial text. Respond with only one word: positive, negative, or neutral.

Text: {test_text}

Sentiment:"""
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=10,
                temperature=0.1,
                do_sample=False
            )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Test inference result: {response}")
        return
    
    # Use our LlamaSentimentModel
    config = LlamaConfig(
        model_name="meta-llama/Meta-Llama-3-8B-Instruct",
        backend=LlamaBackend.TRANSFORMERS,
        device="cuda",
        max_length=512,
        temperature=0.1,
    )
    
    logger.info(f"Initializing Llama model: {config.model_name}")
    model = LlamaSentimentModel(config)
    
    # Load Kaggle data
    kaggle_dir = Path("data/kaggle")
    output_file = Path("data/processed/llama_sentiment.json")
    
    # Find CSV files
    csv_files = list(kaggle_dir.glob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files in {kaggle_dir}")
    
    # Process sample first to verify
    import pandas as pd
    results = []
    
    for csv_file in csv_files[:1]:  # Start with first file
        logger.info(f"Processing {csv_file.name}...")
        df = pd.read_csv(csv_file, nrows=100)  # Sample
        
        # Find text column
        text_col = None
        for col in ['text', 'Text', 'body', 'content', 'title', 'headline']:
            if col in df.columns:
                text_col = col
                break
        
        if text_col is None:
            logger.warning(f"No text column found in {csv_file.name}")
            continue
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc=csv_file.name):
            text = str(row[text_col])[:512]  # Truncate
            
            try:
                result = model.predict(text)
                results.append({
                    'file': csv_file.name,
                    'index': idx,
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'sentiment': result.label,
                    'confidence': result.confidence,
                    'scores': result.scores
                })
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"Saved {len(results)} results to {output_file}")

if __name__ == '__main__':
    main()
PYTHON_SCRIPT

# Check output
echo -e "\n5. Output summary:"
if [ -f data/processed/llama_sentiment.json ]; then
    echo "Output file created successfully"
    ls -lh data/processed/llama_sentiment.json
    echo "Sample results:"
    head -50 data/processed/llama_sentiment.json
else
    echo "Check logs for errors"
fi

echo -e "\n=============================================="
echo "Llama 3 Sentiment Processing Completed"
echo "End: $(date)"
echo "=============================================="
