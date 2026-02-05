import argparse
import pandas as pd
from typing import Iterator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, pandas_udf, udf, explode, to_timestamp
from pyspark.sql.types import FloatType, ArrayType

from sentiment_detector.spark.schemas import RAW_BATCH_SCHEMA

# ---------------------------------------------------------
# 1. SETUP
# ---------------------------------------------------------
def create_spark_session(app_name="Capstone_Sentiment_Analysis"):
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.driver.memory", "8g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

# ---------------------------------------------------------
# 2. UDFs
# ---------------------------------------------------------

# Initialize VADER analyzer once (module-level caching)
# This is safe for Spark serialization since it's created on worker nodes
_vader_analyzer = None

def _get_vader_analyzer():
    """Lazy initialization of VADER analyzer (singleton pattern)."""
    global _vader_analyzer
    if _vader_analyzer is None:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        _vader_analyzer = SentimentIntensityAnalyzer()
    return _vader_analyzer

# Standard UDF for VADER (CPU-bound, fast)
def get_vader_score(text: str) -> float:
    """
    Compute VADER sentiment score for text.
    Uses cached analyzer instance for performance.
    """
    # Handle None/Empty
    if not text:
        return 0.0

    try:
        analyzer = _get_vader_analyzer()
        scores = analyzer.polarity_scores(str(text))
        return float(scores['compound'])
    except Exception:
        return 0.0

vader_udf = udf(get_vader_score, FloatType())

# Optimized Iterator UDF for FinBERT (GPU/Heavy Model)
# Input: Iterator of Series (Batches of text)
# Output: Iterator of Series (Batches of scores)
@pandas_udf(FloatType())
def finbert_score_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    """
    Batch sentiment scoring using FinBERT model.
    Initializes model once per partition for efficiency.
    """
    # --- Initialization Phase (Runs once per partition) ---
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F
    import logging
    import sys

    # Set up logging for this UDF
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    model_name = "ProsusAI/finbert"

    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"FinBERT UDF initializing on device: {device}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.to(device)
        model.eval()
        logger.info(f"FinBERT model loaded successfully on {device}")
    except Exception as e:
        # Log the error and return zeros as fallback
        logger.error(f"CRITICAL: Failed to load FinBERT model: {str(e)}", exc_info=True)
        logger.error("Returning zero scores for all texts in this partition")
        for series in iterator:
            yield pd.Series([0.0] * len(series))
        return

    # --- Processing Phase ---
    for series in iterator:
        # 1. Clean inputs
        texts = [str(t) if t else "" for t in series]
        
        # 2. Batch Tokenization
        # Max length 128 is usually sufficient for tweets/headlines
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=128)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # 3. Inference
        with torch.no_grad():
            outputs = model(**inputs)
            # FinBERT: [Positive, Negative, Neutral] (check specific config)
            # ProsusAI/finbert config: label2id: {'positive': 0, 'negative': 1, 'neutral': 2}
            probs = F.softmax(outputs.logits, dim=1)
            
            # Score = Prob(Pos) - Prob(Neg)
            # A score > 0 is positive, < 0 is negative
            scores = probs[:, 0] - probs[:, 1]
            
        yield pd.Series(scores.cpu().numpy())

# ---------------------------------------------------------
# 3. MAIN JOB
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Spark Sentiment Pipeline")
    parser.add_argument("--input_path", required=True, help="Path to raw JSON files")
    parser.add_argument("--output_path", required=True, help="Path to save processed Parquet")
    args = parser.parse_args()

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print(f"Reading data from: {args.input_path}")

    # A. Read Raw JSON (Handling Multiline/Nested Structure)
    # Using 'multiline=True' because your sample showed a single large JSON object per file
    df_raw = spark.read.option("multiline", "true").schema(RAW_BATCH_SCHEMA).json(args.input_path)

    # B. Flatten the Structure
    # Explode the 'items' array into individual rows
    df_flat = df_raw.select(explode(col("items")).alias("item")) \
        .select(
            col("item.id").alias("post_id"),
            col("item.source"),
            col("item.asset_class"),
            to_timestamp(col("item.created_at")).alias("created_at"),
            col("item.content").alias("text_content")
        )

    # Filter out empty text to save compute
    df_clean = df_flat.filter(col("text_content").isNotNull() & (col("text_content") != ""))

    print("--- Starting Sentiment Analysis ---")
    
    # C. Apply UDFs
    # Note: repartitioning can help balance work if input files are few but large
    # df_clean = df_clean.repartition(100) 
    
    df_scored = df_clean.withColumn("vader_score", vader_udf(col("text_content"))) \
                        .withColumn("finbert_score", finbert_score_udf(col("text_content")))

    # D. Write to Parquet
    print(f"Writing results to: {args.output_path}")
    
    # Partitioning by asset_class or source is usually good for downstream filtering
    df_scored.write.mode("append").partitionBy("asset_class").parquet(args.output_path)

    spark.stop()

if __name__ == "__main__":
    main()
