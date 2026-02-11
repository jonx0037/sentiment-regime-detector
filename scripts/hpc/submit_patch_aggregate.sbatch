#!/bin/bash
#SBATCH --job-name=patch_agg
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=standard-s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=02:00:00
#SBATCH --output=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/patch_agg_%j.out
#SBATCH --error=/lustre/scratch/client/users/jarocha/sentiment-detector/logs/patch_agg_%j.err

source ~/.venv/auto_python_3.11.11_pytorch_2025.08.21/bin/activate

PROJECT_DIR=/lustre/scratch/client/users/jarocha/sentiment-detector
RAW_DATA=/lustre/scratch/client/users/jarocha/sentiment_regime_data
cd $PROJECT_DIR

echo "=== Step 1: Patch missing dates in scored parquet ==="
python3 scripts/hpc/patch_dates.py \
    --data-dir $RAW_DATA \
    --parquet-dir results/sentiment_processed

echo ""
echo "=== Step 2: Aggregate to daily CSV ==="
python3 scripts/hpc/aggregate_daily.py \
    --input-dir results/sentiment_processed \
    --output-file results/daily_sentiment.csv

echo ""
echo "=== DONE ==="
