#!/bin/bash
#SBATCH --job-name=garch_midas
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=standard-m
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/garch_midas_%j.out
#SBATCH --error=logs/garch_midas_%j.err

# GARCH-MIDAS Volatility Forecasting
# Run after sentiment aggregation completes (Phase 3)
# Single job (not array) - processes all aggregated data at once

# Load Python with data science environment
module load python/3.11.11/data_science/2025.08.21

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

echo "=================================================="
echo "GARCH-MIDAS Volatility Forecasting"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "=================================================="

# Directories (using /scratch, not /work)
SCRATCH_DIR="/scratch/users/$USER/sentiment_regime_data"
SENTIMENT_FILE="data/finbert_daily_sentiment_v2.csv"
MARKET_DATA_DIR="data"
OUTPUT_FILE="$SCRATCH_DIR/volatility_forecasts.csv"

# Run GARCH-MIDAS
python scripts/hpc/run_garch_midas.py \
    --sentiment-file $SENTIMENT_FILE \
    --market-data-dir $MARKET_DATA_DIR \
    --output-file $OUTPUT_FILE \
    --midas-lags 22 \
    --ciss-weight 0.5 \
    --forecast-horizon 22

echo "=================================================="
echo "GARCH-MIDAS complete"
echo "Results saved to: $OUTPUT_FILE"
echo "=================================================="
