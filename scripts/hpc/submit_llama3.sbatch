#!/bin/bash
#SBATCH --job-name=llama3_sentiment
#SBATCH --output=logs/llama3_%j.out
#SBATCH --error=logs/llama3_%j.err
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

# Activate PyTorch virtual environment
source ~/.venv/auto_python_3.11.11_pytorch_2025.08.21/bin/activate

# Hugging Face auth (set HF_TOKEN in your environment before submitting)
# e.g.: export HF_TOKEN=hf_xxx && sbatch submit_llama3.sbatch
# export HF_TOKEN=  # set before running

# GPU memory management
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

PROJECT_DIR=/lustre/scratch/client/users/jarocha/sentiment-detector
OUTPUT_PATH=${PROJECT_DIR}/results/sentiment_processed

echo "Python: $(which python) ($(python --version))"
echo "GPU: $(python -c 'import torch; print(torch.cuda.get_device_name(0))' 2>&1)"
echo "Parquet dir: $OUTPUT_PATH"

# Run Llama 3 add-on scorer
cd $PROJECT_DIR
python scripts/hpc/score_llama3.py --parquet-dir $OUTPUT_PATH

echo "Job completed: $(date)"
