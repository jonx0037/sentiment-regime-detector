#!/bin/bash
#SBATCH --job-name=sentiment_prod
#SBATCH --partition=gpu-a100
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=48:00:00
#SBATCH --output=results/slurm_sentiment_%j.out
#SBATCH --error=results/slurm_sentiment_%j.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jarocha@smu.edu

# ============================================================
# Sentiment Regime Detector — Full Corpus Processing
# Dataset: ~33M text records (61.8M total - 28.7M OHLCV)
# Ensemble: FinBERT, RoBERTa, VADER, TextBlob, DistilBERT, Llama 3
# Expected runtime: ~18-24 hours on 20x A100 GPUs
# ============================================================

echo "=== Job started at $(date) ==="
echo "=== Node: $(hostname) ==="
echo "=== GPUs: $(nvidia-smi -L 2>/dev/null | wc -l) ==="

# Environment setup
module load python/3.11 cuda/12.1 spark/3.5.0
cd /lustre/scratch/client/users/jarocha/sentiment-detector
source .venv/bin/activate

# Ensure models are cached
export TRANSFORMERS_CACHE=/lustre/scratch/client/users/jarocha/.cache/huggingface
export HF_HOME=$TRANSFORMERS_CACHE
mkdir -p $TRANSFORMERS_CACHE

# Set paths
INPUT_PATH="/lustre/scratch/client/users/jarocha/sentiment-detector/data/kaggle"
OUTPUT_PATH="/lustre/scratch/client/users/jarocha/sentiment-detector/data/processed/sentiment_scored"
CHECKPOINT_PATH="/lustre/scratch/client/users/jarocha/sentiment-detector/data/processed/checkpoints"
mkdir -p $OUTPUT_PATH $CHECKPOINT_PATH

echo "=== Input path: $INPUT_PATH ==="
echo "=== Output path: $OUTPUT_PATH ==="

# Count input records
echo "=== Counting input records... ==="
find $INPUT_PATH -name "*.csv" -o -name "*.json" | wc -l

# Submit PySpark job
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 20 \
  --executor-cores 8 \
  --executor-memory 32g \
  --driver-memory 16g \
  --conf spark.sql.execution.arrow.pyspark.enabled=true \
  --conf spark.sql.shuffle.partitions=400 \
  --conf spark.default.parallelism=400 \
  --conf spark.driver.maxResultSize=4g \
  --conf spark.executor.resource.gpu.amount=1 \
  --conf spark.task.resource.gpu.amount=0.25 \
  --py-files src/sentiment_detector.zip \
  src/sentiment_detector/spark/sentiment_job.py \
  --input_path $INPUT_PATH \
  --output_path $OUTPUT_PATH

EXIT_CODE=$?
echo "=== Spark job finished with exit code: $EXIT_CODE ==="
echo "=== Job completed at $(date) ==="

# Post-processing: aggregate to daily
if [ $EXIT_CODE -eq 0 ]; then
  echo "=== Running daily aggregation... ==="
  python scripts/aggregate_daily.py \
    --input-dir $OUTPUT_PATH \
    --output-file data/daily_sentiment_full_corpus.csv
  echo "=== Aggregation complete ==="
fi

exit $EXIT_CODE
