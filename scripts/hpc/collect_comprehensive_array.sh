#!/bin/bash
#SBATCH --job-name=collect_comprehensive
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=standard-s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --array=0-71%36
#SBATCH --output=logs/collect_%A_%a.out
#SBATCH --error=logs/collect_%A_%a.err

# Comprehensive historical data collection using ALL API keys and collectors
# Each array task collects one quarter (3 months)

# Load Python with data science packages
module load python/3.11.11/data_science/2025.08.21

# Activate virtual environment
source venv/bin/activate

# Load API keys from .env
export $(grep -v '^#' .env | xargs)

# Calculate date range for this quarter
YEAR=$((2008 + SLURM_ARRAY_TASK_ID / 4))
QUARTER=$((SLURM_ARRAY_TASK_ID % 4 + 1))

case $QUARTER in
    1)
        START_DATE="$YEAR-01-01"
        END_DATE="$YEAR-03-31"
        ;;
    2)
        START_DATE="$YEAR-04-01"
        END_DATE="$YEAR-06-30"
        ;;
    3)
        START_DATE="$YEAR-07-01"
        END_DATE="$YEAR-09-30"
        ;;
    4)
        START_DATE="$YEAR-10-01"
        END_DATE="$YEAR-12-31"
        ;;
esac

echo "=========================================="
echo "Comprehensive Data Collection - Batch $SLURM_ARRAY_TASK_ID"
echo "Period: $START_DATE to $END_DATE"
echo "Using ALL configured API keys:"
echo "  - Twitter/X: ${TWITTER_BEARER_TOKEN:0:20}..."
echo "  - NewsAPI: ${NEWS_API_KEY:0:20}..."
echo "  - Reddit: ${REDDIT_CLIENT_ID:0:20}..."
echo "  - Finhub: ${FINHUB_API_KEY:0:20}..."
echo "  - Tiingo: ${TIINGO_API_KEY:0:20}..."
echo "=========================================="

# Output directory
OUTPUT_DIR="/scratch/users/$USER/sentiment_regime_data/comprehensive_data"
mkdir -p $OUTPUT_DIR

# Run comprehensive collection
python scripts/hpc/collect_comprehensive_historical.py \
    --start-date $START_DATE \
    --end-date $END_DATE \
    --output $OUTPUT_DIR \
    --batch-id $SLURM_ARRAY_TASK_ID

echo "=========================================="
echo "Collection complete for $START_DATE to $END_DATE"
echo "=========================================="
