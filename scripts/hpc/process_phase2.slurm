#!/bin/bash
#SBATCH --job-name=phase2_sentiment
#SBATCH --output=logs/phase2_%A_%a.log
#SBATCH --error=logs/phase2_%A_%a.err
#SBATCH --partition=gpu-dev
#SBATCH --gres=gpu:v100:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --array=0-12

# ============================================================================
# PHASE 2: Reddit Backfill Sentiment Processing
# ============================================================================
# Contents: ~613,000 Reddit texts without sentiment scores
# Batches: 13 x 50,000 texts each
# Estimated GPU time per batch: ~11 minutes
# Total time with parallel: ~11 min if all 13 GPUs available
# Total time sequential: ~2.3 hours
# ============================================================================

echo "=============================================="
echo "Phase 2: Reddit Backfill - Batch $SLURM_ARRAY_TASK_ID"
echo "Job ID: $SLURM_JOB_ID"
echo "Array Task: $SLURM_ARRAY_TASK_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Load PyTorch module (includes transformers)
module purge
module load python/3.11.11/pytorch/2025.08.21

# Set cache directories
export TRANSFORMERS_CACHE=$SCRATCH/.cache/huggingface
export HF_HOME=$SCRATCH/.cache/huggingface
mkdir -p $TRANSFORMERS_CACHE

# Navigate to scratch directory
cd $SCRATCH

# Check GPU availability
echo ""
echo "GPU Check:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

# Set paths
BATCH_NUM=$(printf "%04d" $SLURM_ARRAY_TASK_ID)
INPUT_FILE="data/hpc_batches/phase2/phase2_batch_${BATCH_NUM}.json"
OUTPUT_DIR="results/phase2"
OUTPUT_FILE="$OUTPUT_DIR/phase2_results_${BATCH_NUM}.json"
LOG_FILE="logs/phase2_batch_${BATCH_NUM}.progress"

mkdir -p $OUTPUT_DIR
mkdir -p logs

# Check input exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input file not found: $INPUT_FILE"
    echo "This batch may not exist. Exiting gracefully."
    exit 0
fi

# Count items
ITEM_COUNT=$(python -c "import json; print(json.load(open('$INPUT_FILE'))['count'])")
echo "Processing $ITEM_COUNT items from batch $BATCH_NUM"
echo ""

# Run sentiment analysis
echo "Starting FinBERT + RoBERTa ensemble processing..."
python scripts/hpc/process_phase_batch.py \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --batch-size 128 \
    --device 0

RESULT=$?

echo ""
echo "=============================================="
echo "End: $(date)"
echo "Exit code: $RESULT"
echo "Output: $OUTPUT_FILE"
echo "=============================================="

exit $RESULT
