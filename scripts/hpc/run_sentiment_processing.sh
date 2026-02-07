#!/bin/bash
#SBATCH --job-name=process_sentiment
#SBATCH --partition=gpu-a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:a100:1
#SBATCH --time=24:00:00
#SBATCH --array=0-71  # Match collection array
#SBATCH --output=logs/process_%A_%a.out
#SBATCH --error=logs/process_%A_%a.err

# Process collected data with sentiment models
# Uses A100 GPU for FinBERT processing
# Produces daily sentiment aggregates

module load python/3.11
module load cuda/12.1

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

BATCH_ID=$SLURM_ARRAY_TASK_ID
YEAR=$((2008 + BATCH_ID / 4))
QUARTER=$((BATCH_ID % 4 + 1))

echo "=================================================="
echo "Sentiment Processing: Q${QUARTER} ${YEAR}"
echo "Batch: $BATCH_ID of 72"
echo "GPU: $CUDA_VISIBLE_DEVICES"
echo "=================================================="

# Directories
WORK_DIR="/work/$USER/sentiment_regime_data"
INPUT_DIR="$WORK_DIR/raw_data"
OUTPUT_DIR="$WORK_DIR/sentiment_results"

mkdir -p $OUTPUT_DIR

# Process with FinBERT + VADER ensemble
python scripts/hpc/process_sentiment_batch.py \
    --input-dir $INPUT_DIR \
    --batch-id $BATCH_ID \
    --output-dir $OUTPUT_DIR \
    --models finbert,vader \
    --batch-size 64

echo "=================================================="
echo "Processing complete for Q${QUARTER} ${YEAR}"
echo "Results saved to: $OUTPUT_DIR"
echo "=================================================="
