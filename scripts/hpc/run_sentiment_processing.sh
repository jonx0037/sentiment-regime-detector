#!/bin/bash
#SBATCH --job-name=process_sentiment
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=gpu-dev
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=18:00:00
#SBATCH --array=0-71%36  # 72 batches, max 36 concurrent
#SBATCH --output=logs/process_%A_%a.out
#SBATCH --error=logs/process_%A_%a.err

# Process collected data with full sentiment ensemble
# Uses V100 GPU for all transformer models (gpu-dev partition)
# Models: FinBERT, VADER, TextBlob, DistilBERT, Llama 3
# Produces daily sentiment aggregates with 5-model ensemble averaging

# Load Python with data science environment and CUDA
module load python/3.11.11/data_science/2025.08.21
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
echo "Node: $(hostname)"
echo "=================================================="

# Directories (using /scratch, not /work)
SCRATCH_DIR="/scratch/users/$USER/sentiment_regime_data"
INPUT_DIR="$SCRATCH_DIR/raw_data"
OUTPUT_DIR="$SCRATCH_DIR/sentiment_results"

mkdir -p $OUTPUT_DIR

# Process with full sentiment ensemble (5 models)
# FinBERT + VADER + TextBlob + DistilBERT + Llama 3
# Using adaptive batch sizing for V100's 16GB memory
python scripts/hpc/process_sentiment_batch.py \
    --input-dir $INPUT_DIR \
    --batch-id $BATCH_ID \
    --output-dir $OUTPUT_DIR \
    --models finbert,vader,textblob,distilbert,llama3 \
    --batch-size 64

echo "=================================================="
echo "Processing complete for Q${QUARTER} ${YEAR}"
echo "Results saved to: $OUTPUT_DIR"
echo "=================================================="
