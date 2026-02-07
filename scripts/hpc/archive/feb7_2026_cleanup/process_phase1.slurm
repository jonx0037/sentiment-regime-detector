#!/bin/bash
#SBATCH --job-name=phase1_sentiment
#SBATCH --output=logs/phase1_%j.log
#SBATCH --error=logs/phase1_%j.err
#SBATCH --partition=gpu-dev
#SBATCH --gres=gpu:v100:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00

echo "=============================================="
echo "Phase 1: News + WSB Echo Chamber Sentiment"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Load PyTorch module
module purge
module load python/3.11.11/pytorch/2025.08.21

# Set cache directories
export TRANSFORMERS_CACHE=$SCRATCH/.cache/huggingface
export HF_HOME=$SCRATCH/.cache/huggingface
mkdir -p $TRANSFORMERS_CACHE

# Navigate to scratch
cd $SCRATCH

# Check GPU
echo ""
echo "GPU Check:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv
echo ""

# Run sentiment analysis
echo "Processing Phase 1 batch..."
python scripts/hpc/process_phase_batch.py \
    --input data/hpc_batches/phase1/phase1_batch.json \
    --output results/phase1/phase1_results.json \
    --batch-size 128 \
    --device 0

echo ""
echo "=============================================="
echo "End: $(date)"
echo "=============================================="
