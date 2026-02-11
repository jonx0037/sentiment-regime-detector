#!/bin/bash
#SBATCH --job-name=regime_analysis
#SBATCH --partition=standard-s
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --output=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/analysis_%j.out
#SBATCH --error=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/analysis_%j.err

echo "Job started: $(date)"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Running on nodes: ${SLURM_NODELIST}"

# Activate environment
source ~/.venv/auto_python_3.11.11_pytorch_2025.08.21/bin/activate
echo "Python: $(which python) ($(python --version 2>&1))"

cd /lustre/scratch/client/users/jarocha/sentiment-detector

# Create output directory
mkdir -p results/pipeline_output

# Run the analysis
python scripts/hpc/run_analysis.py \
    --sentiment results/daily_sentiment.csv \
    --vix data/vix_daily.csv \
    --ciss data/ecb_ciss_daily.csv \
    --market data/SPY.csv \
    --output-dir results/pipeline_output

echo "Job completed: $(date)"
