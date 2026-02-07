#!/bin/bash
#SBATCH --job-name=regime_classification
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=standard-s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/regime_class_%j.out
#SBATCH --error=logs/regime_class_%j.err

# Regime Classification using Statistical Jump Model
# Run after GARCH-MIDAS completes (Phase 3.6)
# Single job (not array) - processes all aggregated data at once

# Load Python with data science environment
module load python/3.11.11/data_science/2025.08.21

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

echo "=================================================="
echo "Regime Classification - Statistical Jump Model"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "=================================================="

# Directories (using /scratch, not /work)
SCRATCH_DIR="/scratch/users/$USER/sentiment_regime_data"
VOLATILITY_FILE="$SCRATCH_DIR/volatility_forecasts.csv"
SENTIMENT_FILE="data/finbert_daily_sentiment_v2.csv"
OUTPUT_FILE="$SCRATCH_DIR/regime_predictions.csv"

# Run regime classification
python scripts/hpc/run_regime_classification.py \
    --volatility-file $VOLATILITY_FILE \
    --sentiment-file $SENTIMENT_FILE \
    --output-file $OUTPUT_FILE \
    --jump-penalty 10.0 \
    --n-regimes 3 \
    --tune-lambda

echo "=================================================="
echo "Regime classification complete"
echo "Results saved to: $OUTPUT_FILE"
echo "=================================================="
