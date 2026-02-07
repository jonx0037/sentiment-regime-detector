#!/bin/bash
#SBATCH --job-name=collect_historical
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=standard-s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --array=0-71%36  # 72 quarters, max 36 concurrent (avoid API rate limits)
#SBATCH --output=logs/collect_%A_%a.out
#SBATCH --error=logs/collect_%A_%a.err

# Historical data collection array job
# Each array task collects data for one 3-month period (quarter)
# 72 quarters total: 2008-Q1 through 2026-Q4

# Load Python with data science packages (includes numpy, pandas, scipy)
module load python/3.11.11/data_science/2025.08.21

# Activate virtual environment
source venv/bin/activate

# Calculate date range for this array task
# Array 0 = 2008-Q1, Array 1 = 2008-Q2, etc.
YEAR=$((2008 + SLURM_ARRAY_TASK_ID / 4))
QUARTER=$((SLURM_ARRAY_TASK_ID % 4 + 1))

# Calculate start and end dates
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

echo "=================================================="
echo "Historical Data Collection - Array Task $SLURM_ARRAY_TASK_ID"
echo "Period: $START_DATE to $END_DATE"
echo "=================================================="

# Create output directory (using /scratch, not /work which is being deprecated)
OUTPUT_DIR="/scratch/users/$USER/sentiment_regime_data/raw_data"
mkdir -p $OUTPUT_DIR

# Run collection (checkpoint support not yet implemented in Python script)
python scripts/hpc/collect_historical_data.py \
    --start-date $START_DATE \
    --end-date $END_DATE \
    --sources gdelt,reddit \
    --output $OUTPUT_DIR \
    --batch-id $SLURM_ARRAY_TASK_ID

echo "=================================================="
echo "Collection complete for $START_DATE to $END_DATE"
echo "=================================================="
