#!/bin/bash
#SBATCH -J sentiment_batch        # Job name
#SBATCH -o logs/sentiment_batch_%j.out  # Output file
#SBATCH -e logs/sentiment_batch_%j.err  # Error file
#SBATCH -p fp-gpgpu-3             # Production GPU partition (7 day limit)
#SBATCH -N 1                      # 1 node
#SBATCH -n 8                      # 8 CPU cores
#SBATCH --gres=gpu:1              # 1 GPU
#SBATCH --mem=32G                 # Memory
#SBATCH -t 12:00:00               # 12 hour limit
#SBATCH -A jcheun_ds6210_1262_401_0001
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jarocha@mail.smu.edu

# ============================================================
# Production Sentiment Analysis Batch Job
# Processes full dataset with checkpointing
# ============================================================

echo "=============================================="
echo "Sentiment Analysis Batch Processing"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Setup
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
source $PROJECT_DIR/activate_env.sh

# Create logs directory if not exists
mkdir -p $PROJECT_DIR/logs

# Show resources
echo -e "\n1. Resources allocated:"
echo "CPUs: $SLURM_CPUS_ON_NODE"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# Run the batch processing script
echo -e "\n2. Starting batch processing..."
python $PROJECT_DIR/batch_sentiment.py \
    --input-dir $PROJECT_DIR/data/raw \
    --output-dir $PROJECT_DIR/data/processed \
    --model finbert \
    --batch-size 64 \
    --checkpoint-dir $PROJECT_DIR/checkpoints \
    --text-column content \
    --num-workers 4

echo -e "\n=============================================="
echo "Batch Processing Completed"
echo "End: $(date)"
echo "=============================================="
