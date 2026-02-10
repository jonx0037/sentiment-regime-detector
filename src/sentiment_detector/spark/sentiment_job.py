import argparse
import pandas as pd
from typing import Iterator
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    pandas_udf,
    udf,
    explode,
    to_timestamp,
    concat_ws,
    when,
    lit,
    from_unixtime,
)
from pyspark.sql.types import FloatType, ArrayType

from sentiment_detector.spark.schemas import RAW_BATCH_SCHEMA


# ---------------------------------------------------------
# 1. SETUP
# ---------------------------------------------------------
def create_spark_session(app_name="Capstone_Sentiment_Analysis"):
    """Create Spark session optimized for multi-GPU processing."""
    import os

    # Use 4 cores for 4 GPUs - each task gets one GPU
    num_gpus = int(os.environ.get("SLURM_GPUS_ON_NODE", "4"))
    num_cores = str(num_gpus)  # One core per GPU

    return (
        SparkSession.builder.appName(app_name)
        .master(f"local[{num_cores}]")
        .config("spark.driver.memory", "96g")
        .config("spark.executor.memory", "96g")
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.driver.maxResultSize", "8g")
        .config("spark.sql.shuffle.partitions", str(num_gpus * 2))
        .config("spark.default.parallelism", str(num_gpus * 2))
        .config("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY")
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
        .getOrCreate()
    )


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
        return float(scores["compound"])
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
    # CRITICAL: Set CUDA_VISIBLE_DEVICES BEFORE importing torch
    import os
    import logging
    import sys
    from pyspark import TaskContext

    # Assign GPU based on partition ID BEFORE any CUDA initialization
    ctx = TaskContext.get()
    partition_id = 0
    gpu_id = 0
    if ctx:
        partition_id = ctx.partitionId()
        # We have 2 GPUs - distribute partitions across them
        gpu_id = partition_id % 2
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # NOW import torch - it will only see the assigned GPU
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F

    # Set up logging for this UDF
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    model_name = "ProsusAI/finbert"

    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    gpu_info = f"GPU {gpu_id}" if ctx and torch.cuda.is_available() else device
    logger.info(
        f"FinBERT UDF initializing on device: {gpu_info} (partition {partition_id if ctx else 'unknown'})"
    )

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
    BATCH_SIZE = 32  # Process 32 texts at a time to avoid GPU OOM

    for series in iterator:
        # 1. Clean inputs
        texts = [str(t) if t else "" for t in series]

        # 2. Process in sub-batches to avoid GPU memory exhaustion
        all_scores = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i : i + BATCH_SIZE]

            # Tokenize sub-batch
            inputs = tokenizer(
                batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=128
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}

            # Inference on sub-batch
            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                scores = probs[:, 0] - probs[:, 1]  # Positive - Negative
                all_scores.extend(scores.cpu().numpy())

            # Clear GPU cache after each sub-batch
            if device == "cuda":
                torch.cuda.empty_cache()

        yield pd.Series(all_scores)


# TextBlob UDF (CPU-fast)
def get_textblob_score(text: str) -> float:
    """Compute TextBlob polarity score for text."""
    if not text:
        return 0.0
    try:
        from textblob import TextBlob

        return float(TextBlob(str(text)).sentiment.polarity)
    except Exception:
        return 0.0


textblob_udf = udf(get_textblob_score, FloatType())


# RoBERTa UDF (GPU)
@pandas_udf(FloatType())
def roberta_score_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    """Batch sentiment scoring using RoBERTa model."""
    # Set GPU BEFORE importing torch
    import os
    from pyspark import TaskContext

    ctx = TaskContext.get()
    if ctx:
        partition_id = ctx.partitionId()
        gpu_id = partition_id % 2  # Distribute across 2 GPUs
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # Now import torch
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F

    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.to(device)
        model.eval()
    except Exception:
        for series in iterator:
            yield pd.Series([0.0] * len(series))
        return

    BATCH_SIZE = 32  # Process 32 texts at a time to avoid GPU OOM

    for series in iterator:
        texts = [str(t) if t else "" for t in series]
        all_scores = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i : i + BATCH_SIZE]
            inputs = tokenizer(
                batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=128
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                scores = probs[:, 2] - probs[:, 0]  # positive - negative
                all_scores.extend(scores.cpu().numpy())

            if device == "cuda":
                torch.cuda.empty_cache()

        yield pd.Series(all_scores)


# DistilBERT UDF (GPU)
@pandas_udf(FloatType())
def distilbert_score_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    """Batch sentiment scoring using DistilBERT model."""
    # Set GPU BEFORE importing torch
    import os
    from pyspark import TaskContext

    ctx = TaskContext.get()
    if ctx:
        partition_id = ctx.partitionId()
        gpu_id = partition_id % 2  # Distribute across 2 GPUs
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # Now import torch
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F

    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.to(device)
        model.eval()
    except Exception:
        for series in iterator:
            yield pd.Series([0.0] * len(series))
        return

    BATCH_SIZE = 32  # Process 32 texts at a time to avoid GPU OOM

    for series in iterator:
        texts = [str(t) if t else "" for t in series]
        all_scores = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch_texts = texts[i : i + BATCH_SIZE]
            inputs = tokenizer(
                batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=128
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                scores = probs[:, 1] - probs[:, 0]  # positive - negative
                all_scores.extend(scores.cpu().numpy())

            if device == "cuda":
                torch.cuda.empty_cache()

        yield pd.Series(all_scores)


# Llama 3 UDF (GPU with quantization)
@pandas_udf(FloatType())
def llama3_score_udf(iterator: Iterator[pd.Series]) -> Iterator[pd.Series]:
    """
    Batch sentiment scoring using Llama 3 8B with 4-bit quantization.
    This is computationally expensive - use smaller batches.
    """
    # Set GPU BEFORE importing torch
    import os
    import re
    from pyspark import TaskContext

    ctx = TaskContext.get()
    if ctx:
        partition_id = ctx.partitionId()
        gpu_id = partition_id % 2  # Distribute across 2 GPUs
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    # Now import torch
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # If no CUDA, return zeros (Llama 3 8B requires GPU)
    if device == "cpu":
        for series in iterator:
            yield pd.Series([0.0] * len(series))
        return

    try:
        # 4-bit quantization for memory efficiency
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
        )

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        model.eval()
    except Exception:
        # Fallback to zero scores if model fails to load
        for series in iterator:
            yield pd.Series([0.0] * len(series))
        return

    for series in iterator:
        texts = [str(t) if t else "" for t in series]
        scores = []

        for text in texts:
            if not text:
                scores.append(0.0)
                continue

            try:
                # Prompt for sentiment classification
                prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a financial sentiment analyzer. Classify the sentiment as POSITIVE, NEGATIVE, or NEUTRAL.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
Text: {text[:500]}
Sentiment:<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

                inputs = tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)
                inputs = {k: v.to(device) for k, v in inputs.items()}

                with torch.no_grad():
                    outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False)
                    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

                # Extract sentiment from response
                response_lower = response.lower()
                if "positive" in response_lower:
                    scores.append(1.0)
                elif "negative" in response_lower:
                    scores.append(-1.0)
                else:
                    scores.append(0.0)
            except Exception:
                scores.append(0.0)

        yield pd.Series(scores)


# ---------------------------------------------------------
# 3. MAIN JOB
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Spark Sentiment Pipeline")
    parser.add_argument("--input_path", required=True, help="Path to raw data files (CSV or JSON)")
    parser.add_argument("--output_path", required=True, help="Path to save processed Parquet")
    parser.add_argument(
        "--format", default="csv", choices=["csv", "json"], help="Input file format"
    )
    args = parser.parse_args()

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print(f"Reading data from: {args.input_path}")
    print(f"Format: {args.format}")

    if args.format == "json":
        # A. Read Raw JSON (Handling Multiline/Nested Structure)
        df_raw = (
            spark.read.option("multiline", "true").schema(RAW_BATCH_SCHEMA).json(args.input_path)
        )

        # B. Flatten the Structure
        df_flat = df_raw.select(explode(col("items")).alias("item")).select(
            col("item.id").alias("post_id"),
            col("item.source"),
            col("item.asset_class"),
            to_timestamp(col("item.created_at")).alias("created_at"),
            col("item.content").alias("text_content"),
        )
    else:
        # ══════════════════════════════════════════════════════════════
        # COMPREHENSIVE PER-DIRECTORY CSV READING
        # Handles: nested CSVs, multiple delimiters, no-header files,
        # stocknews Top1-Top25 unpivot, swapped columns, all column
        # naming conventions across 25+ datasets.
        # ══════════════════════════════════════════════════════════════
        print("Reading CSV files with comprehensive per-directory schema detection...")
        import os as _os
        import glob as _glob

        # ── Column name mappings ──────────────────────────────────────
        TEXT_COL_PRIORITY = [
            # (lowercase_name, combine_with_title?)
            ("selftext", True),  # Reddit
            ("self_text", True),  # Reddit variant
            ("content", False),  # Generic news
            ("text", False),  # Generic
            ("body", False),  # Reddit/forums
            ("fulltext", False),  # Elon tweets, some APIs
            ("full_text", False),  # Variant
            ("headline", False),  # News
            ("comment", False),  # Social media
            ("description", False),  # RSS
            ("message", False),  # Chat
            ("news", False),  # Financial news
            ("short description", False),  # Some datasets
            ("tweet", False),  # Twitter
            ("status", False),  # Social
            ("summary", False),  # Articles
            ("abstract", False),  # Academic
            ("post", False),  # Forums
            ("sentence", False),  # NLP datasets
            ("review", False),  # Review datasets
            ("judul", False),  # Indonesian: "title"
            ("title", False),  # Fallback: title only
        ]

        # Unix timestamp columns (need from_unixtime instead of to_timestamp)
        UNIX_TS_COLS = {"created", "created_utc", "created_at_utc", "retrieved"}

        # Date/timestamp columns priority order
        DATE_COL_PRIORITY = [
            "created_utc",
            "created",
            "created_at",
            "createdat",  # elon_tweets camelCase
            "date",
            "timestamp",
            "publish_date",
            "published_at",
            "published_date",
            "tanggal",  # Indonesian: "date"
            "time",
            "datetime",
            "post_date",
            "dates",
        ]

        def _find_col_ci(available_cols, target_lower):
            """Case-insensitive column lookup. Returns actual column name or None."""
            for c in available_cols:
                if c.lower().strip() == target_lower:
                    return c
            return None

        def _build_text_expr_for(available_cols):
            """Build text extraction expression for a dataset's columns."""
            for target_lower, combine_with_title in TEXT_COL_PRIORITY:
                actual_col = _find_col_ci(available_cols, target_lower)
                if actual_col is None:
                    continue

                if combine_with_title:
                    title_col = _find_col_ci(available_cols, "title")
                    if title_col:
                        return (
                            when(
                                (col(actual_col).isNotNull())
                                & (col(actual_col).cast("string") != ""),
                                concat_ws(
                                    " ",
                                    col(title_col).cast("string"),
                                    col(actual_col).cast("string"),
                                ),
                            )
                            .when(
                                (col(title_col).isNotNull())
                                & (col(title_col).cast("string") != ""),
                                col(title_col).cast("string"),
                            )
                            .otherwise(lit(None))
                        )
                    return when(
                        (col(actual_col).isNotNull()) & (col(actual_col).cast("string") != ""),
                        col(actual_col).cast("string"),
                    ).otherwise(lit(None))
                else:
                    return when(
                        (col(actual_col).isNotNull()) & (col(actual_col).cast("string") != ""),
                        col(actual_col).cast("string"),
                    ).otherwise(lit(None))

            return None

        def _build_date_expr_for(available_cols):
            """Build date extraction expression for a dataset's columns."""
            for target_lower in DATE_COL_PRIORITY:
                actual_col = _find_col_ci(available_cols, target_lower)
                if actual_col is None:
                    continue

                if target_lower in UNIX_TS_COLS:
                    return (
                        when(
                            (col(actual_col).isNotNull())
                            & (col(actual_col).cast("double") > 9999999999),
                            from_unixtime((col(actual_col).cast("double") / 1000).cast("long")),
                        )
                        .when(
                            (col(actual_col).isNotNull()) & (col(actual_col).cast("double") > 0),
                            from_unixtime(col(actual_col).cast("long")),
                        )
                        .otherwise(lit(None))
                    )
                else:
                    return when(
                        col(actual_col).isNotNull(),
                        to_timestamp(col(actual_col).cast("string")),
                    ).otherwise(lit(None))

            return None

        # ── ID and source helpers ─────────────────────────────────────
        from pyspark.sql.functions import (
            monotonically_increasing_id,
            concat as sql_concat,
            length,
            array,
            explode as sql_explode,
            md5,
            trim,
        )

        def _build_id_expr_for(available_cols, subdir_name):
            """Build post_id expression."""
            for id_name in ["submission", "id", "post_id", "comment_id"]:
                actual = _find_col_ci(available_cols, id_name)
                if actual:
                    return when(
                        col(actual).isNotNull(),
                        col(actual).cast("string"),
                    ).otherwise(
                        sql_concat(
                            lit(f"{subdir_name}_"), monotonically_increasing_id().cast("string")
                        )
                    )
            return sql_concat(lit(f"{subdir_name}_"), monotonically_increasing_id().cast("string"))

        def _build_source_expr_for(available_cols, subdir_name):
            """Build source expression."""
            for src_name in ["subreddit", "source", "publisher", "outlet", "channel"]:
                actual = _find_col_ci(available_cols, src_name)
                if actual:
                    return when(col(actual).isNotNull(), col(actual).cast("string")).otherwise(
                        lit(subdir_name)
                    )
            return lit(subdir_name)

        def _infer_asset_class(subdir_name):
            """Infer asset class from directory name."""
            name_lower = subdir_name.lower()
            if any(
                k in name_lower for k in ["bitcoin", "crypto", "btc", "eth", "defi", "telegram"]
            ):
                return "crypto"
            elif any(k in name_lower for k in ["forex", "currency", "fx", "exchange", "turkey"]):
                return "forex"
            elif any(k in name_lower for k in ["commodity", "gold", "oil", "wti", "crude"]):
                return "commodities"
            elif any(
                k in name_lower
                for k in ["stock", "equity", "wsb", "wallstreet", "sp500", "djia", "nasdaq", "elon"]
            ):
                return "equities"
            elif any(k in name_lower for k in ["vix", "ciss", "stress", "fear"]):
                return "market-stress"
            else:
                return "cross-asset"

        def _is_header_data(col_name):
            """Detect if a column name is actually a data value (no-header CSV)."""
            if len(col_name) > 50:
                return True
            if col_name.count(" ") > 5:
                return True
            return False

        def _get_csv_header(filepath):
            """Read the first line of a CSV to get column names (for schema grouping)."""
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    first_line = f.readline().strip()
                return first_line
            except Exception:
                return ""

        def _group_csvs_by_schema(csv_files):
            """Group CSV files by their header signature to avoid schema merge."""
            groups = {}
            for fpath in csv_files:
                header = _get_csv_header(fpath)
                groups.setdefault(header, []).append(fpath)
            return groups

        def _standard_filter(df):
            """Apply standard text quality filter."""
            return df.filter(
                (col("text_content").isNotNull())
                & (col("text_content") != "")
                & (col("text_content") != "[removed]")
                & (col("text_content") != "[deleted]")
                & (length(col("text_content")) > 10)
                & (col("text_content").rlike("[a-zA-Z]{3,}"))
            )

        def _process_csv_group(spark_sess, file_list, subdir_name, label_suffix=""):
            """Read a group of same-schema CSVs and return standardized DataFrame or None."""
            try:
                df_sub = (
                    spark_sess.read.option("header", "true")
                    .option("inferSchema", "true")
                    .option("escape", '"')
                    .option("multiLine", "true")
                    .csv(file_list)
                )
            except Exception as e:
                print(f"    Read error ({label_suffix}): {e}")
                return None

            available_cols = df_sub.columns

            # ── Handle no-header CSVs ─────────────────────────────
            if len(available_cols) <= 3 and any(_is_header_data(c) for c in available_cols):
                print(f"    No-header detected ({label_suffix}), re-reading...")
                try:
                    df_sub = (
                        spark_sess.read.option("header", "false")
                        .option("inferSchema", "true")
                        .option("escape", '"')
                        .option("multiLine", "true")
                        .csv(file_list)
                    )
                    available_cols = df_sub.columns
                    if len(available_cols) == 2:
                        df_mapped = df_sub.select(
                            sql_concat(
                                lit(f"{subdir_name}_"), monotonically_increasing_id().cast("string")
                            ).alias("post_id"),
                            lit(subdir_name).alias("source"),
                            lit(_infer_asset_class(subdir_name)).alias("asset_class"),
                            lit(None).cast("timestamp").alias("created_at"),
                            col("_c1").cast("string").alias("text_content"),
                        )
                        return _standard_filter(df_mapped)
                except Exception:
                    pass
                return None

            # ── Handle tab-delimited files ─────────────────────────
            if len(available_cols) <= 3:
                try:
                    df_tab = (
                        spark_sess.read.option("header", "true")
                        .option("inferSchema", "true")
                        .option("sep", "\t")
                        .csv(file_list)
                    )
                    if len(df_tab.columns) > len(available_cols):
                        print(f"    Tab-delimited ({label_suffix}): {len(df_tab.columns)} cols")
                        df_sub = df_tab
                        available_cols = df_tab.columns
                except Exception:
                    pass

            # ── Handle stocknews Top1-Top25 pattern ───────────────
            top_cols = [
                c for c in available_cols if c.lower().startswith("top") and c[3:].isdigit()
            ]
            if len(top_cols) >= 5:
                print(
                    f"    Stocknews pattern ({label_suffix}): {len(top_cols)} Top cols → unpivoting"
                )
                date_col = _find_col_ci(available_cols, "date")
                if date_col:
                    all_text_cols = top_cols[:]
                    label_col = _find_col_ci(available_cols, "label")
                    if label_col:
                        all_text_cols.append(label_col)
                    headline_array = array(
                        *[
                            when(
                                (col(c).isNotNull()) & (col(c).cast("string") != ""),
                                col(c).cast("string"),
                            ).otherwise(lit(None))
                            for c in all_text_cols
                        ]
                    )
                    df_unpivot = df_sub.select(
                        col(date_col).alias("_date"),
                        sql_explode(headline_array).alias("_headline"),
                    ).filter(col("_headline").isNotNull())
                    df_mapped = df_unpivot.select(
                        sql_concat(
                            lit(f"{subdir_name}_"), monotonically_increasing_id().cast("string")
                        ).alias("post_id"),
                        lit(subdir_name).alias("source"),
                        lit(_infer_asset_class(subdir_name)).alias("asset_class"),
                        to_timestamp(col("_date").cast("string")).alias("created_at"),
                        col("_headline").alias("text_content"),
                    )
                    return _standard_filter(df_mapped)

            # ── Standard column detection ─────────────────────────
            text_expr = _build_text_expr_for(available_cols)
            if text_expr is None:
                print(f"    No text col ({label_suffix}): {available_cols[:8]}")
                return None

            ts_expr = _build_date_expr_for(available_cols)
            if ts_expr is None:
                print(f"    No date col ({label_suffix}): using NULL timestamps")
                ts_expr = lit(None).cast("timestamp")

            id_expr = _build_id_expr_for(available_cols, subdir_name)
            source_expr = _build_source_expr_for(available_cols, subdir_name)

            df_mapped = df_sub.select(
                id_expr.alias("post_id"),
                source_expr.alias("source"),
                lit(_infer_asset_class(subdir_name)).alias("asset_class"),
                ts_expr.alias("created_at"),
                text_expr.alias("text_content"),
            )
            return _standard_filter(df_mapped)

        # ── Read each subdirectory ────────────────────────────────────
        input_path_str = str(args.input_path)
        subdirs = sorted(
            [
                d
                for d in _os.listdir(input_path_str)
                if _os.path.isdir(_os.path.join(input_path_str, d))
            ]
        )
        print(f"  Found {len(subdirs)} dataset subdirectories")

        all_dfs = []
        skipped_datasets = []
        good_datasets = []

        for subdir in subdirs:
            subdir_path = _os.path.join(input_path_str, subdir)

            # ── Find CSV files recursively ────────────────────────────
            csv_files = _glob.glob(_os.path.join(subdir_path, "**", "*.csv"), recursive=True)
            if not csv_files:
                # ── JSON fallback: look for JSON files ────────────────
                json_files = _glob.glob(_os.path.join(subdir_path, "**", "*.json"), recursive=True)
                if not json_files:
                    skipped_datasets.append((subdir, "no CSV or JSON files"))
                    continue

                print(f"\n  [{subdir}] {len(json_files)} JSON file(s) (no CSVs)...")

                # Batch JSON reads: Spark chokes on 300K+ individual files.
                # Read in batches of 1000, map each batch, then union.
                JSON_BATCH_SIZE = 1000
                json_batch_dfs = []
                try:
                    # Probe schema from first batch
                    probe = spark.read.option("multiLine", "true").json(
                        json_files[: min(50, len(json_files))]
                    )
                    json_cols = probe.columns
                    print(f"    JSON columns: {json_cols[:10]}")

                    # Find text column
                    text_expr = _build_text_expr_for(json_cols)
                    if text_expr is None:
                        for candidate in [
                            "text",
                            "title",
                            "description",
                            "content",
                            "body",
                            "selftext",
                        ]:
                            actual = _find_col_ci(json_cols, candidate)
                            if actual:
                                text_expr = col(actual).cast("string")
                                print(f"    Using JSON field: {actual}")
                                break

                    if text_expr is None:
                        skipped_datasets.append((subdir, f"no text field in JSON: {json_cols[:8]}"))
                        continue

                    ts_expr = _build_date_expr_for(json_cols)
                    if ts_expr is None:
                        pub_col = _find_col_ci(json_cols, "published")
                        if pub_col:
                            ts_expr = to_timestamp(col(pub_col).cast("string"))
                        else:
                            ts_expr = lit(None).cast("timestamp")

                    id_expr = _build_id_expr_for(json_cols, subdir)
                    schema = probe.schema  # reuse schema for consistent reads

                    n_batches = (len(json_files) + JSON_BATCH_SIZE - 1) // JSON_BATCH_SIZE
                    print(f"    Reading in {n_batches} batches of {JSON_BATCH_SIZE}...")

                    for batch_idx in range(0, len(json_files), JSON_BATCH_SIZE):
                        batch = json_files[batch_idx : batch_idx + JSON_BATCH_SIZE]
                        batch_num = batch_idx // JSON_BATCH_SIZE + 1
                        df_batch = spark.read.option("multiLine", "true").schema(schema).json(batch)
                        df_mapped = df_batch.select(
                            id_expr.alias("post_id"),
                            lit(subdir).alias("source"),
                            lit(_infer_asset_class(subdir)).alias("asset_class"),
                            ts_expr.alias("created_at"),
                            text_expr.alias("text_content"),
                        )
                        df_mapped = _standard_filter(df_mapped)
                        json_batch_dfs.append(df_mapped)
                        if batch_num % 50 == 0 or batch_num == n_batches:
                            print(f"      Batch {batch_num}/{n_batches} done")

                    if json_batch_dfs:
                        df_json_all = json_batch_dfs[0]
                        for extra in json_batch_dfs[1:]:
                            df_json_all = df_json_all.unionByName(extra)
                        all_dfs.append(df_json_all)
                        good_datasets.append(
                            f"{subdir} (JSON, {len(json_files)} files, {n_batches} batches)"
                        )
                    else:
                        skipped_datasets.append((subdir, "JSON batches produced no data"))
                except Exception as e:
                    skipped_datasets.append((subdir, f"JSON read error: {e}"))
                continue

            print(f"\n  [{subdir}] {len(csv_files)} CSV file(s)...")

            # ══════════════════════════════════════════════════════════
            # SPECIAL CASES (datasets with known quirks)
            # ══════════════════════════════════════════════════════════

            # ── twitter_stocks_2015_2020: relational 3-table dataset ──
            if subdir == "twitter_stocks_2015_2020":
                tweet_files = [f for f in csv_files if _os.path.basename(f).lower() == "tweet.csv"]
                if tweet_files:
                    print(f"    Reading Tweet.csv specifically ({len(tweet_files)} file(s))...")
                    try:
                        df_tweets = (
                            spark.read.option("header", "true")
                            .option("inferSchema", "true")
                            .option("escape", '"')
                            .csv(tweet_files)
                        )
                        df_mapped = df_tweets.select(
                            col("tweet_id").cast("string").alias("post_id"),
                            col("writer").cast("string").alias("source"),
                            lit("equities").alias("asset_class"),
                            from_unixtime(col("post_date").cast("long")).alias("created_at"),
                            col("body").cast("string").alias("text_content"),
                        )
                        df_mapped = _standard_filter(df_mapped)
                        all_dfs.append(df_mapped)
                        good_datasets.append(f"{subdir} (Tweet.csv)")
                    except Exception as e:
                        skipped_datasets.append((subdir, f"Tweet.csv error: {e}"))
                else:
                    skipped_datasets.append((subdir, "no Tweet.csv found"))
                continue

            # ── reddit-sentiment-2025: Body + Post_Title columns ──────
            if subdir == "reddit-sentiment-2025":
                try:
                    df_sub = (
                        spark.read.option("header", "true")
                        .option("inferSchema", "true")
                        .option("escape", '"')
                        .option("multiLine", "true")
                        .csv(csv_files)
                    )
                    body_col = _find_col_ci(df_sub.columns, "body")
                    title_col = _find_col_ci(df_sub.columns, "post_title")
                    text_col = body_col or title_col
                    if text_col:
                        print(f"    reddit-sentiment-2025: using {text_col} as text")
                        df_mapped = df_sub.select(
                            sql_concat(
                                lit(f"{subdir}_"), monotonically_increasing_id().cast("string")
                            ).alias("post_id"),
                            lit("reddit").alias("source"),
                            lit("cross-asset").alias("asset_class"),
                            lit(None).cast("timestamp").alias("created_at"),
                            col(text_col).cast("string").alias("text_content"),
                        )
                        df_mapped = _standard_filter(df_mapped)
                        all_dfs.append(df_mapped)
                        good_datasets.append(f"{subdir} ({text_col})")
                    else:
                        skipped_datasets.append(
                            (subdir, f"no Body/Post_Title col in {df_sub.columns[:8]}")
                        )
                except Exception as e:
                    skipped_datasets.append((subdir, f"read error: {e}"))
                continue

            # ══════════════════════════════════════════════════════════
            # PER-FILE SCHEMA DETECTION
            # Group files by their header line to prevent schema merge
            # ══════════════════════════════════════════════════════════

            schema_groups = _group_csvs_by_schema(csv_files)
            if len(schema_groups) > 1:
                print(f"    {len(schema_groups)} different schemas — processing per-group")

            dir_dfs = []
            for _schema_key, group_files in schema_groups.items():
                label = (
                    _os.path.basename(group_files[0])
                    if len(group_files) == 1
                    else f"{len(group_files)} files"
                )
                result = _process_csv_group(spark, group_files, subdir, label_suffix=label)
                if result is not None:
                    dir_dfs.append(result)

            if dir_dfs:
                dir_union = dir_dfs[0]
                for extra in dir_dfs[1:]:
                    dir_union = dir_union.unionByName(extra)
                all_dfs.append(dir_union)
                good_datasets.append(f"{subdir} ({len(schema_groups)} schema(s))")
            else:
                skipped_datasets.append((subdir, "no text columns in any schema group"))

        print(f"\n  Datasets with text: {len(all_dfs)}")
        print(f"  Datasets skipped: {len(skipped_datasets)}")
        for name, reason in skipped_datasets:
            print(f"    - {name}: {reason}")
        print(f"\n  Included datasets: {good_datasets}")

        if not all_dfs:
            print("ERROR: No datasets had text columns!")
            spark.stop()
            import sys

            sys.exit(1)

        # Union all datasets
        print(f"\n  Unioning {len(all_dfs)} datasets...")
        df_flat = all_dfs[0]
        for df_part in all_dfs[1:]:
            df_flat = df_flat.unionByName(df_part)

        # Deduplicate by text content (same article from different sources)
        df_flat = df_flat.withColumn("_text_hash", md5(trim(col("text_content"))))
        df_flat = df_flat.dropDuplicates(["_text_hash"]).drop("_text_hash")

        print("  Sample records after union + dedup:")
        df_flat.select("source", "asset_class", "created_at", "text_content").show(10, truncate=60)

    # Filter out empty text to save compute
    df_clean = (
        df_flat.filter(col("text_content").isNotNull() & (col("text_content") != ""))
        .filter(col("text_content") != "[removed]")
        .filter(col("text_content") != "[deleted]")
    )

    print(f"Cleaned rows ready for sentiment analysis: {df_clean.count()}")

    print("--- Starting Sentiment Analysis ---")

    # C. Apply UDFs
    # Note: repartitioning can help balance work if input files are few but large
    # df_clean = df_clean.repartition(100)

    # Apply 5 models (Llama3 disabled for now due to memory constraints)
    # Ensemble weights normalized without Llama3: FinBERT 31%, RoBERTa 25%, VADER 19%, TextBlob 12.5%, DistilBERT 12.5%
    df_scored = (
        df_clean.withColumn("vader_score", vader_udf(col("text_content")))
        .withColumn("textblob_score", textblob_udf(col("text_content")))
        .withColumn("finbert_score", finbert_score_udf(col("text_content")))
        .withColumn("roberta_score", roberta_score_udf(col("text_content")))
        .withColumn("distilbert_score", distilbert_score_udf(col("text_content")))
    )
    # .withColumn("llama3_score", llama3_score_udf(col("text_content")))  # DISABLED - high memory usage

    # Calculate weighted ensemble score (5 models, normalized to sum to 1.0)
    df_scored = df_scored.withColumn(
        "ensemble_score",
        (0.3125 * col("finbert_score"))
        + (0.25 * col("roberta_score"))
        + (0.1875 * col("vader_score"))
        + (0.125 * col("textblob_score"))
        + (0.125 * col("distilbert_score")),
    )

    # D. Write to Parquet
    print(f"Writing results to: {args.output_path}")

    # CRITICAL: Explicitly select columns to force Spark to compute them
    # Without this, Spark's optimizer skips the sentiment UDFs entirely
    final_df = df_scored.select(
        "post_id",
        "source",
        "asset_class",
        "created_at",
        "text_content",
        "vader_score",
        "textblob_score",
        "finbert_score",
        "roberta_score",
        "distilbert_score",
        "ensemble_score",
    )

    # Use overwrite mode to force computation (append can skip work)
    final_df.write.mode("overwrite").partitionBy("asset_class").parquet(args.output_path)

    spark.stop()


if __name__ == "__main__":
    main()
