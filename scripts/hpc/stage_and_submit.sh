#!/bin/bash
# ============================================================
# Quick-start script for HPC sentiment processing
# Run this LOCALLY after SSH'ing into MANEFRAME III
#
# Usage:
#   ssh jarocha@m3.smu.edu
#   # (authenticate with Duo)
#   bash /lustre/scratch/client/users/jarocha/sentiment-detector/scripts/hpc/stage_and_submit.sh
# ============================================================

set -e

PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
cd $PROJECT_DIR

echo "============================================"
echo "  Sentiment Regime Detector — HPC Setup"
echo "============================================"

# 1. Check data is present
echo ""
echo "=== Step 1: Checking data ==="
TOTAL_FILES=$(find data/kaggle -name "*.csv" -o -name "*.json" 2>/dev/null | wc -l)
echo "Found $TOTAL_FILES data files in data/kaggle/"

if [ "$TOTAL_FILES" -lt 10 ]; then
  echo "ERROR: Data not staged. Run this from your LOCAL machine first:"
  echo "  rsync -avz --progress data/kaggle/ jarocha@m3.smu.edu:$PROJECT_DIR/data/kaggle/"
  exit 1
fi

# 2. Check virtual environment
echo ""
echo "=== Step 2: Checking Python environment ==="
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
  echo "Virtual environment activated"
  python --version
else
  echo "Creating virtual environment..."
  module load python/3.11
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
fi

# 3. Check GPU availability
echo ""
echo "=== Step 3: Checking GPU access ==="
module load cuda/12.1 2>/dev/null || echo "CUDA module not available on login node (OK)"

# 4. Zip the source package for spark-submit
echo ""
echo "=== Step 4: Packaging source code ==="
if [ -d "src/sentiment_detector" ]; then
  cd src
  zip -r sentiment_detector.zip sentiment_detector/ -x "*.pyc" "*__pycache__*"
  cd ..
  echo "Created src/sentiment_detector.zip"
fi

# 5. Pre-download models (do this on login node to avoid GPU job delays)
echo ""
echo "=== Step 5: Pre-downloading transformer models ==="
export TRANSFORMERS_CACHE="$PROJECT_DIR/.cache/huggingface"
mkdir -p $TRANSFORMERS_CACHE
python -c "
from transformers import AutoTokenizer, AutoModelForSequenceClassification
print('Downloading FinBERT...')
AutoTokenizer.from_pretrained('ProsusAI/finbert', cache_dir='$TRANSFORMERS_CACHE')
AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert', cache_dir='$TRANSFORMERS_CACHE')
print('Downloading RoBERTa...')
AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest', cache_dir='$TRANSFORMERS_CACHE')
AutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest', cache_dir='$TRANSFORMERS_CACHE')
print('Downloading DistilBERT...')
AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english', cache_dir='$TRANSFORMERS_CACHE')
AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english', cache_dir='$TRANSFORMERS_CACHE')
print('All models downloaded.')
" 2>&1 || echo "WARNING: Model pre-download failed. Models will download during job."

# 6. Submit the job
echo ""
echo "=== Step 6: Submitting SLURM job ==="
module load spark/3.5.0 2>/dev/null || echo "Spark module loaded"
mkdir -p results
JOB_ID=$(sbatch scripts/hpc/submit_sentiment_job.sbatch | awk '{print $4}')
echo "Submitted job: $JOB_ID"
echo ""
echo "============================================"
echo "  MONITORING COMMANDS:"
echo "  squeue -u jarocha           # Check job status"
echo "  tail -f results/slurm_sentiment_${JOB_ID}.out  # Watch output"
echo "  scancel $JOB_ID             # Cancel if needed"
echo "============================================"
echo ""
echo "Expected runtime: 18-24 hours for ~33M texts"
echo "You will receive an email at jarocha@smu.edu when it completes."
