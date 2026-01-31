#!/bin/bash
#SBATCH --job-name=finbert_batch
#SBATCH --output=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/finbert_batch_%j.out
#SBATCH --error=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/finbert_batch_%j.err
#SBATCH --partition=gpgpu-1
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4

# =============================================================================
# MANEFRAME III - FinBERT Batch Processing Script
# =============================================================================
# This script processes all Kaggle dataset batches through FinBERT on the V100 GPU
# Expected throughput: ~347 texts/second
# =============================================================================

echo "=============================================="
echo "FinBERT Batch Processing on MANEFRAME III"
echo "=============================================="
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start time: $(date)"
echo ""

# Load required modules
module purge
module load python/3.10
module load cuda/11.8

# Set paths
WORK_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
BATCH_DIR="$WORK_DIR/data/batches"
OUTPUT_DIR="$WORK_DIR/data/processed"
VENV_DIR="$WORK_DIR/venv"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Verify GPU
echo "GPU Information:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

# Check Python environment
echo "Python: $(which python)"
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"
mkdir -p "$WORK_DIR/logs"

# Count batches
NUM_BATCHES=$(ls -1 "$BATCH_DIR"/*.json 2>/dev/null | wc -l)
echo "Found $NUM_BATCHES batch files to process"
echo ""

# Process each batch
TOTAL_PROCESSED=0
START_TIME=$(date +%s)

for BATCH_FILE in "$BATCH_DIR"/*.json; do
    if [ -f "$BATCH_FILE" ]; then
        BATCH_NAME=$(basename "$BATCH_FILE" .json)
        OUTPUT_FILE="$OUTPUT_DIR/${BATCH_NAME}_sentiment.json"
        
        # Skip if already processed
        if [ -f "$OUTPUT_FILE" ]; then
            echo "⏭️  Skipping $BATCH_NAME (already processed)"
            continue
        fi
        
        echo "🔄 Processing: $BATCH_NAME"
        
        python "$WORK_DIR/scripts/process_batch.py" \
            --input "$BATCH_FILE" \
            --output "$OUTPUT_FILE" \
            --model "ProsusAI/finbert" \
            --device "cuda" \
            --batch-size 64
        
        if [ $? -eq 0 ]; then
            echo "✅ Completed: $BATCH_NAME"
            ITEMS=$(python -c "import json; print(len(json.load(open('$OUTPUT_FILE'))))")
            TOTAL_PROCESSED=$((TOTAL_PROCESSED + ITEMS))
        else
            echo "❌ Failed: $BATCH_NAME"
        fi
        echo ""
    fi
done

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo "=============================================="
echo "Processing Complete!"
echo "=============================================="
echo "Total items processed: $TOTAL_PROCESSED"
echo "Total time: $ELAPSED seconds"
if [ $ELAPSED -gt 0 ]; then
    RATE=$(echo "scale=1; $TOTAL_PROCESSED / $ELAPSED" | bc)
    echo "Processing rate: $RATE texts/second"
fi
echo "Output directory: $OUTPUT_DIR"
echo "End time: $(date)"
