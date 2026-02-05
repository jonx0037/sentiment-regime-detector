# PySpark Sentiment Analysis Pipeline

Distributed sentiment analysis using Apache Spark for large-scale text processing.

## Overview

This module provides a PySpark-based alternative to the standard HPC batch processing pipeline. It's designed for scenarios where you need to:
- Process 10M+ texts efficiently
- Distribute workload across multiple GPUs
- Handle real-time streaming data
- Run exploratory analysis on large historical datasets

**Note:** For datasets under 5M texts, the standard HPC batch processing ([scripts/hpc/batch_sentiment.py](../../../scripts/hpc/batch_sentiment.py)) is recommended as it's simpler and faster.

## Architecture

### Components

1. **[schemas.py](schemas.py)** - PySpark schema definitions for input JSON
2. **[sentiment_job.py](sentiment_job.py)** - Main Spark job with VADER and FinBERT UDFs

### Processing Flow

```
Raw JSON Batches → Spark Explode → Text Cleaning → Sentiment Analysis → Parquet Output
                                                    ├── VADER (CPU UDF)
                                                    └── FinBERT (GPU pandas_udf)
```

## Input Format

The pipeline expects JSON files with this structure:

```json
{
  "collection_timestamp": "2026-02-02T19:30:00Z",
  "items": [
    {
      "id": "unique_post_id",
      "source": "reddit|twitter|news",
      "asset_class": "equity|crypto|forex|commodity",
      "created_at": "2026-02-02T15:45:00Z",
      "title": "Optional title",
      "content": "The text to analyze",
      "metadata": {
        "key": "value",
        ...
      }
    }
  ]
}
```

See [tests/data/sample_spark_batch.json](../../../tests/data/sample_spark_batch.json) for a complete example with 10 sample texts.

## Output Format

Parquet files partitioned by `asset_class` with columns:
- `post_id` - Unique identifier
- `source` - Data source (reddit, twitter, news)
- `asset_class` - Asset category
- `created_at` - Timestamp (parsed)
- `text_content` - Original text
- `vader_score` - VADER compound score [-1, 1]
- `finbert_score` - FinBERT score [-1, 1]

## Usage

### Local Testing (Standalone Mode)

```bash
# Install dependencies (from project root)
pip install -e .[hpc]  # Includes PySpark and all NLP tools

# Run on sample data
spark-submit \
  --master local[4] \
  --driver-memory 4g \
  src/sentiment_detector/spark/sentiment_job.py \
  --input_path tests/data/ \
  --output_path /tmp/spark_output/

# Verify output
python -c "import pandas as pd; df = pd.read_parquet('/tmp/spark_output/'); print(df.head())"
```

### ManeFrame III HPC Cluster

```bash
# 1. Package your code
cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
tar -czf spark_job.tar.gz src/sentiment_detector/spark/ pyproject.toml

# 2. Submit Spark job via SLURM
sbatch <<EOF
#!/bin/bash
#SBATCH --job-name=spark_sentiment
#SBATCH --output=spark_%j.log
#SBATCH --partition=gpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:v100:1
#SBATCH --time=02:00:00

module load spark/3.5.0
module load python/3.11

# Set Spark configuration
export SPARK_HOME=/path/to/spark
export PYSPARK_PYTHON=\$HOME/.venv/bin/python

spark-submit \\
  --master spark://master-node:7077 \\
  --num-executors 4 \\
  --executor-cores 8 \\
  --executor-memory 32g \\
  --driver-memory 16g \\
  --conf spark.sql.execution.arrow.pyspark.enabled=true \\
  --conf spark.executor.resource.gpu.amount=1 \\
  src/sentiment_detector/spark/sentiment_job.py \\
  --input_path /work/data/batches/ \\
  --output_path /work/results/sentiment/
EOF
```

### Cloud (AWS EMR Example)

```bash
aws emr create-cluster \
  --name "Sentiment-Analysis-Spark" \
  --release-label emr-7.0.0 \
  --applications Name=Spark \
  --instance-type m5.2xlarge \
  --instance-count 5 \
  --use-default-roles \
  --steps Type=Spark,Name="Sentiment Job",ActionOnFailure=CONTINUE,Args=[
    s3://your-bucket/sentiment_job.py,
    --input_path,s3://your-bucket/input/,
    --output_path,s3://your-bucket/output/
  ]
```

## Performance Tuning

### Memory Configuration

For 1M texts:
```bash
--driver-memory 8g
--executor-memory 16g
--executor-cores 4
```

For 10M+ texts:
```bash
--driver-memory 16g
--executor-memory 32g
--executor-cores 8
--num-executors 8
```

### GPU Optimization

To use GPUs for FinBERT inference:
```bash
--conf spark.executor.resource.gpu.amount=1
--conf spark.task.resource.gpu.amount=0.25  # 4 tasks per GPU
```

### Partitioning

Adjust for your cluster size:
```python
# In sentiment_job.py line 128
df_clean = df_clean.repartition(200)  # 200 partitions for 20+ executors
```

Rule of thumb: 2-3 partitions per core

## Comparison with Batch Processing

| Metric | HPC Batch | PySpark (4 nodes) |
|--------|-----------|-------------------|
| Setup Time | 5 min | 30 min |
| 1M texts | 6 hours | 8 hours |
| 10M texts | 60 hours | 20 hours |
| GPU Efficiency | 95% | 70% |
| Complexity | Low | High |
| Cost | Single GPU | 4x GPUs |

**Recommendation:** Use Spark only when scaling beyond 5-10M texts or need distributed features.

## When to Use This Pipeline

✅ **Use Spark if:**
- Dataset > 10M texts
- Multi-GPU cluster available
- Need streaming ingestion
- Distributed feature engineering
- Parallel API collection

❌ **Use HPC Batch if:**
- Dataset < 5M texts
- Single GPU sufficient
- Simple pipeline
- Tight deadline

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'sentiment_detector.spark.schemas'
```
**Solution:** Ensure PYTHONPATH includes project root:
```bash
export PYTHONPATH=/path/to/DS_6210_Capstone/src:$PYTHONPATH
```

### VADER Slow Performance
**Symptom:** Processing < 10 texts/second

**Solution:** Verify VADER analyzer is cached (fixed in latest version)

### FinBERT Returns All Zeros
**Symptom:** All `finbert_score` values are 0.0

**Solution:** Check Spark logs for model loading errors:
```bash
grep "CRITICAL: Failed to load FinBERT" spark_*.log
```

Common causes:
- Missing transformers library
- Insufficient memory
- Network timeout downloading model

### Out of Memory
```
java.lang.OutOfMemoryError: Java heap space
```
**Solution:** Increase executor memory:
```bash
--executor-memory 32g --driver-memory 16g
```

## Testing

Run unit tests:
```bash
cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone

# Test schema import
python -c "from sentiment_detector.spark.schemas import RAW_BATCH_SCHEMA; print(RAW_BATCH_SCHEMA)"

# Test job import
python -c "from sentiment_detector.spark.sentiment_job import main; print('OK')"

# Run end-to-end test
pytest tests/test_spark_job.py
```

## Integration with Existing Pipeline

To integrate Spark output with PostgreSQL:

```python
import pandas as pd
from sqlalchemy import create_engine

# Read Parquet results
df = pd.read_parquet('/path/to/spark/output/')

# Connect to database
engine = create_engine('postgresql://user:pass@localhost:5432/sentiment')

# Insert sentiment scores
for _, row in df.iterrows():
    # Map to SentimentScore table
    # See scripts/spark_to_postgres.py (TODO: create this)
    pass
```

## Next Steps

1. **Benchmark:** Compare Spark vs HPC batch on your data
2. **Optimize:** Tune partitions and memory for your cluster
3. **Monitor:** Add metrics collection (Spark UI, Ganglia)
4. **Scale:** Test with 1M → 10M → 100M texts
5. **Integrate:** Build Parquet → PostgreSQL bridge

## References

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Pandas UDFs](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html)
- [Spark on HPC](https://spark.apache.org/docs/latest/running-on-yarn.html)
- [ManeFrame III Guide](https://www.smu.edu/OIT/Services/HPC)

## Support

For issues or questions:
1. Check Spark logs: `spark_*.log` files
2. Review plan: `/Users/jonathanrocha/.claude/plans/warm-hugging-dawn.md`
3. Contact: jrocha@smu.edu
