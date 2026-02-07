#!/bin/bash
#SBATCH --job-name=collect_all_historical
#SBATCH --partition=standard-mem-s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --array=0-71  # 72 quarters (2008 Q1 to 2026 Q1)
#SBATCH --output=logs/collect_%A_%a.out
#SBATCH --error=logs/collect_%A_%a.err

# Complete historical data collection
# Collects from GDELT (news) + Reddit archives
# Ensures balanced coverage across all asset classes

module load python/3.11

# Activate virtual environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

# Calculate date range for this quarter
YEAR=$((2008 + SLURM_ARRAY_TASK_ID / 4))
QUARTER=$((SLURM_ARRAY_TASK_ID % 4 + 1))

case $QUARTER in
    1) START_DATE="$YEAR-01-01"; END_DATE="$YEAR-03-31" ;;
    2) START_DATE="$YEAR-04-01"; END_DATE="$YEAR-06-30" ;;
    3) START_DATE="$YEAR-07-01"; END_DATE="$YEAR-09-30" ;;
    4) START_DATE="$YEAR-10-01"; END_DATE="$YEAR-12-31" ;;
esac

echo "=================================================="
echo "Historical Collection: Q${QUARTER} ${YEAR}"
echo "Period: $START_DATE to $END_DATE"
echo "Task: $SLURM_ARRAY_TASK_ID of 72"
echo "=================================================="

# Create work directory
WORK_DIR="/work/$USER/sentiment_regime_data"
mkdir -p $WORK_DIR

# Run collection
python scripts/hpc/collect_historical_data.py \
    --start-date $START_DATE \
    --end-date $END_DATE \
    --sources gdelt,reddit \
    --output $WORK_DIR/raw_data \
    --batch-id $SLURM_ARRAY_TASK_ID

echo "=================================================="
echo "Collection complete for Q${QUARTER} ${YEAR}"
echo "Next: Process with sentiment models"
echo "=================================================="
