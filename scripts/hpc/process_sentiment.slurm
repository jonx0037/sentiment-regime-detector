#!/bin/bash
#SBATCH --job-name=sentiment_batch
#SBATCH --output=sentiment_%A_%a.out
#SBATCH --error=sentiment_%A_%a.err
#SBATCH --partition=gpgpu-1
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --array=0-29

# SMU ManeFrame III Sentiment Analysis Job
# Processes batch files in parallel using GPU

echo "Starting job $SLURM_ARRAY_TASK_ID on $(hostname)"
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"

# Load modules
module load python/3.10
module load cuda/12.0

# Activate virtual environment
source ~/sentiment_env/bin/activate

# Set batch file
BATCH_NUM=$(printf "%04d" $SLURM_ARRAY_TASK_ID)
INPUT_FILE="data/hpc_batches/batch_${BATCH_NUM}.json"
OUTPUT_FILE="data/hpc_results/results_${BATCH_NUM}.json"

# Check if input exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Input file not found: $INPUT_FILE"
    exit 1
fi

# Create output directory
mkdir -p data/hpc_results

# Run sentiment analysis
echo "Processing $INPUT_FILE..."
python scripts/hpc/batch_sentiment.py \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE" \
    --model finbert \
    --batch-size 128 \
    --device 0

echo "Completed batch $SLURM_ARRAY_TASK_ID"
echo "Output: $OUTPUT_FILE"
