#!/bin/bash
#SBATCH --job-name=sentiment_pytorch
#SBATCH --output=logs/sentiment_%j.out
#SBATCH --error=logs/sentiment_%j.err
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=fp-gpgpu-3
#SBATCH --gres=gpu:v100:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jarocha@smu.edu

echo "Job started: $(date)"
echo "Job ID: $SLURM_JOB_ID"
echo "Running on nodes: $SLURM_NODELIST"

# Activate PyTorch virtual environment (same as Spark job)
source ~/.venv/auto_python_3.11.11_pytorch_2025.08.21/bin/activate

# GPU memory management
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Project paths
PROJECT_DIR=/lustre/scratch/client/users/jarocha/sentiment-detector
INPUT_PATH=/lustre/scratch/client/users/jarocha/sentiment_regime_data
OUTPUT_PATH=${PROJECT_DIR}/results/sentiment_processed

echo "Python: $(which python) ($(python --version))"
echo "GPU available: $(python -c 'import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))' 2>&1)"
echo "Input: $INPUT_PATH"
echo "Output: $OUTPUT_PATH"

# Run PyTorch sentiment scorer (no Spark)
cd $PROJECT_DIR
python scripts/hpc/score_sentiment.py \
    --input-path $INPUT_PATH \
    --output-path $OUTPUT_PATH

echo "Job completed: $(date)"
