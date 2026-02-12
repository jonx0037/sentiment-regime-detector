#!/bin/bash
#SBATCH --job-name=sentiment_prod
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=fp-gpgpu-3
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --gres=gpu:v100:2
#SBATCH --mem=160G
#SBATCH --time=7-00:00:00
#SBATCH --output=results/slurm_sentiment_%j.out
#SBATCH --error=results/slurm_sentiment_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jarocha@smu.edu

# ============================================================
# Sentiment Regime Detector — Full Corpus Processing
# Dataset: ~33M text records (61.8M total - 28.7M OHLCV)
# Ensemble: FinBERT, RoBERTa, VADER, TextBlob, DistilBERT, Llama 3
# Target: fp-gpgpu-3 (2x V100, 40 CPUs, 332GB RAM)
# Account: jcheun_ds6210_1262_401_0001
# ============================================================

echo "=== Job started at $(date) ==="
echo "=== Node: $(hostname) ==="
echo "=== GPUs available ==="
nvidia-smi -L 2>/dev/null || echo "No GPU detected"

# Environment setup
module load python/3.11.7-qxgm323
module load cuda/11.8.0-vnha6cm

cd /lustre/scratch/client/users/jarocha/sentiment-detector

# Create venv if needed
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

# Install dependencies
pip install --quiet --upgrade pip
pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --quiet transformers accelerate bitsandbytes
pip install --quiet vaderSentiment textblob pandas pyarrow tqdm

# Model cache
export TRANSFORMERS_CACHE=/lustre/scratch/client/users/jarocha/.cache/huggingface
export HF_HOME=$TRANSFORMERS_CACHE
mkdir -p $TRANSFORMERS_CACHE

# Paths
INPUT_PATH="/lustre/scratch/client/users/jarocha/sentiment-detector/data/kaggle"
OUTPUT_PATH="/lustre/scratch/client/users/jarocha/sentiment-detector/data/processed/sentiment_scored"
CHECKPOINT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector/data/processed/checkpoints"
mkdir -p $OUTPUT_PATH $CHECKPOINT_DIR results

echo "=== Input path: $INPUT_PATH ==="
echo "=== Output path: $OUTPUT_PATH ==="

# Count input files
echo "=== Counting input files... ==="
CSV_COUNT=$(find $INPUT_PATH -name "*.csv" | wc -l)
JSON_COUNT=$(find $INPUT_PATH -name "*.json" | wc -l)
PARQUET_COUNT=$(find $INPUT_PATH -name "*.parquet" | wc -l)
echo "Found $CSV_COUNT CSV, $JSON_COUNT JSON, $PARQUET_COUNT Parquet files"

# Run pure Python sentiment scoring (no Spark)
echo "=== Starting sentiment processing ==="
python3 scripts/hpc/score_sentiment.py \
  --input_path $INPUT_PATH \
  --output_path $OUTPUT_PATH \
  --checkpoint_dir $CHECKPOINT_DIR \
  --batch_size 64 \
  --device cuda \
  2>&1

EXIT_CODE=$?
echo "=== Sentiment job finished with exit code: $EXIT_CODE ==="
echo "=== Job completed at $(date) ==="

# Post-processing: aggregate to daily
if [ $EXIT_CODE -eq 0 ]; then
  echo "=== Running daily aggregation... ==="
  python3 scripts/aggregate_daily.py \
    --input-dir $OUTPUT_PATH \
    --output-file data/daily_sentiment_full_corpus.csv
  echo "=== Aggregation complete ==="
fi

exit $EXIT_CODE
