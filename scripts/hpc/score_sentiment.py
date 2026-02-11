#!/usr/bin/env python3
"""
Sentiment scoring without PySpark — uses pandas + PyTorch directly.
Same 5 models, same ensemble weights as the Spark version.
"""

import argparse
import glob
import hashlib
import os
import sys
import time

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm


# ── Ensemble weights (same as Spark job) ─────────────────────
WEIGHTS = {
    "finbert_score": 0.3125,
    "roberta_score": 0.25,
    "vader_score": 0.1875,
    "textblob_score": 0.125,
    "distilbert_score": 0.125,
}

# ── Text column detection (same logic as Spark job) ──────────
TEXT_COL_NAMES = [
    "body",
    "text",
    "title",
    "comment",
    "content",
    "headline",
    "selftext",
    "description",
    "message",
    "text_content",
    "sentence",
    "review",
    "summary",
]

DATE_COL_NAMES = [
    "created_at",
    "date",
    "timestamp",
    "created_utc",
    "created",
    "post_date",
    "published",
    "published_at",
    "datetime",
    "time",
    "published_utc",
    "publishedat",
    "article_url",
]


def find_text_col(cols):
    """Find the best text column from available columns."""
    cols_lower = {c.lower(): c for c in cols}
    for name in TEXT_COL_NAMES:
        if name in cols_lower:
            return cols_lower[name]
    return None


def find_date_col(cols):
    """Find the best date column from available columns."""
    cols_lower = {c.lower(): c for c in cols}
    for name in DATE_COL_NAMES:
        if name in cols_lower:
            return cols_lower[name]
    return None


def infer_asset_class(name):
    """Infer asset class from dataset directory name."""
    name_l = name.lower()
    if any(k in name_l for k in ["crypto", "bitcoin", "btc", "eth"]):
        return "crypto"
    if any(k in name_l for k in ["forex", "fx", "currency", "dollar"]):
        return "forex"
    if any(k in name_l for k in ["gold", "silver", "oil", "commodit"]):
        return "commodities"
    if any(k in name_l for k in ["reddit", "wsb", "wallstreetbet"]):
        return "social"
    if any(
        k in name_l for k in ["stock", "equity", "spy", "market", "analyst", "earning"]
    ):
        return "equities"
    if any(k in name_l for k in ["news", "financial_news", "ticker"]):
        return "news"
    return "cross-asset"


# ── Data loading ─────────────────────────────────────────────
def load_all_datasets(input_path):
    """Load all CSV datasets into a single DataFrame with standardized columns."""
    subdirs = sorted(
        [
            d
            for d in os.listdir(input_path)
            if os.path.isdir(os.path.join(input_path, d))
        ]
    )
    print(f"Found {len(subdirs)} dataset subdirectories")

    all_dfs = []
    skipped = []

    for subdir in subdirs:
        subdir_path = os.path.join(input_path, subdir)

        # Find CSVs — top-level first, then recursive
        csv_files = glob.glob(os.path.join(subdir_path, "*.csv"))
        if not csv_files:
            csv_files = glob.glob(
                os.path.join(subdir_path, "**", "*.csv"), recursive=True
            )
        if not csv_files:
            skipped.append((subdir, "no CSV files"))
            continue

        # Read each CSV and find text column
        dataset_dfs = []
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file, low_memory=False, nrows=0)  # headers only
                text_col = find_text_col(df.columns)
                if text_col is None:
                    # Check for stocknews Top1-Top25 pattern
                    top_cols = [
                        c
                        for c in df.columns
                        if c.lower().startswith("top") and c[3:].isdigit()
                    ]
                    if len(top_cols) >= 5:
                        df_full = pd.read_csv(csv_file, low_memory=False)
                        date_col = find_date_col(df_full.columns)
                        # Melt top columns into rows
                        rows = []
                        for _, row in df_full.iterrows():
                            for tc in top_cols:
                                text = str(row.get(tc, ""))
                                if text and text != "nan":
                                    rows.append(
                                        {
                                            "source": subdir,
                                            "asset_class": infer_asset_class(subdir),
                                            "created_at": str(row[date_col])
                                            if date_col
                                            else None,
                                            "text_content": text[:5000],
                                        }
                                    )
                        if rows:
                            dataset_dfs.append(pd.DataFrame(rows))
                        continue
                    continue

                # Read full CSV with text column
                date_col = find_date_col(
                    pd.read_csv(csv_file, low_memory=False, nrows=0).columns
                )
                cols_to_read = [text_col]
                if date_col:
                    cols_to_read.append(date_col)

                df_full = pd.read_csv(csv_file, low_memory=False)

                # Build result DataFrame from dict (scalar + Series in one shot)
                text_series = df_full[text_col].astype(str).str[:5000]
                date_series = (
                    df_full[date_col].astype(str)
                    if date_col and date_col in df_full.columns
                    else pd.Series([None] * len(df_full))
                )

                result = pd.DataFrame(
                    {
                        "source": subdir,
                        "asset_class": infer_asset_class(subdir),
                        "text_content": text_series.values,
                        "created_at": date_series.values,
                    }
                )

                # Filter empty/deleted text
                result = result[
                    result["text_content"].notna()
                    & (result["text_content"] != "")
                    & (result["text_content"] != "nan")
                    & (result["text_content"] != "[removed]")
                    & (result["text_content"] != "[deleted]")
                ]

                if len(result) > 0:
                    dataset_dfs.append(result)

            except Exception as e:
                print(f"  WARN: Error reading {csv_file}: {e}")
                continue

        if dataset_dfs:
            combined = pd.concat(dataset_dfs, ignore_index=True)
            print(f"  [{subdir}] {len(combined):,} rows ({infer_asset_class(subdir)})")
            all_dfs.append(combined)
        else:
            skipped.append((subdir, "no text columns found"))

    print(f"\nDatasets loaded: {len(all_dfs)}")
    print(f"Datasets skipped: {len(skipped)}")
    for name, reason in skipped:
        print(f"  - {name}: {reason}")

    if not all_dfs:
        print("ERROR: No datasets had text columns!")
        sys.exit(1)

    df = pd.concat(all_dfs, ignore_index=True)
    print(
        f"\nTotal rows: {len(df):,} (no deduplication — cross-asset overlap preserved)"
    )

    return df


# ── CPU scorers ──────────────────────────────────────────────
def score_vader(texts):
    """Score texts with VADER (CPU)."""
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    analyzer = SentimentIntensityAnalyzer()
    scores = []
    for text in tqdm(texts, desc="VADER", unit="text", mininterval=5):
        try:
            scores.append(analyzer.polarity_scores(str(text))["compound"])
        except Exception:
            scores.append(0.0)
    return np.array(scores, dtype=np.float32)


def score_textblob(texts):
    """Score texts with TextBlob (CPU)."""
    from textblob import TextBlob

    scores = []
    for text in tqdm(texts, desc="TextBlob", unit="text", mininterval=5):
        try:
            scores.append(TextBlob(str(text)).sentiment.polarity)
        except Exception:
            scores.append(0.0)
    return np.array(scores, dtype=np.float32)


# ── GPU scorers ──────────────────────────────────────────────
def score_transformer(texts, model_name, score_fn, batch_size=64, device="cuda"):
    """Generic transformer scoring — loads model, batches through GPU."""
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F

    print(f"\n  Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.to(device)
    model.eval()

    all_scores = []
    for i in tqdm(
        range(0, len(texts), batch_size),
        desc=model_name.split("/")[-1],
        unit="batch",
        mininterval=5,
    ):
        batch = [str(t)[:512] for t in texts[i : i + batch_size]]
        inputs = tokenizer(
            batch, return_tensors="pt", padding=True, truncation=True, max_length=128
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            scores = score_fn(probs)
            all_scores.extend(scores.cpu().numpy())

        if device == "cuda":
            torch.cuda.empty_cache()

    # Free GPU memory
    del model, tokenizer
    torch.cuda.empty_cache()

    return np.array(all_scores, dtype=np.float32)


def main():
    parser = argparse.ArgumentParser(description="Sentiment scoring (no Spark)")
    parser.add_argument("--input-path", required=True, help="Path to dataset directory")
    parser.add_argument("--output-path", required=True, help="Path for output parquet")
    args = parser.parse_args()

    start_time = time.time()

    # 1. Load data
    print("=" * 60)
    print("LOADING DATASETS")
    print("=" * 60)
    df = load_all_datasets(args.input_path)
    texts = df["text_content"].tolist()
    print(f"\nData loaded in {time.time() - start_time:.1f}s")

    # 2. Device check
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(
            f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB"
        )
    else:
        print("WARNING: No GPU available, using CPU (will be very slow)")

    # 3. Score with each model
    print("\n" + "=" * 60)
    print(f"SCORING {len(texts):,} TEXTS WITH 5 MODELS")
    print("=" * 60)

    # CPU models first (can run while GPU loads)
    print("\n--- CPU Models ---")
    t0 = time.time()
    df["vader_score"] = score_vader(texts)
    print(f"  VADER done in {time.time() - t0:.1f}s")

    t0 = time.time()
    df["textblob_score"] = score_textblob(texts)
    print(f"  TextBlob done in {time.time() - t0:.1f}s")

    # GPU models sequentially (to avoid OOM)
    print("\n--- GPU Models ---")

    t0 = time.time()
    df["finbert_score"] = score_transformer(
        texts,
        "ProsusAI/finbert",
        lambda probs: probs[:, 0] - probs[:, 1],  # positive - negative
        batch_size=64,
        device=device,
    )
    print(f"  FinBERT done in {time.time() - t0:.1f}s")

    t0 = time.time()
    df["roberta_score"] = score_transformer(
        texts,
        "cardiffnlp/twitter-roberta-base-sentiment-latest",
        lambda probs: probs[:, 2] - probs[:, 0],  # positive - negative
        batch_size=64,
        device=device,
    )
    print(f"  RoBERTa done in {time.time() - t0:.1f}s")

    t0 = time.time()
    df["distilbert_score"] = score_transformer(
        texts,
        "distilbert-base-uncased-finetuned-sst-2-english",
        lambda probs: probs[:, 1] - probs[:, 0],  # positive - negative
        batch_size=64,
        device=device,
    )
    print(f"  DistilBERT done in {time.time() - t0:.1f}s")

    # 4. Ensemble score
    print("\n--- Ensemble ---")
    df["ensemble_score"] = (
        WEIGHTS["finbert_score"] * df["finbert_score"]
        + WEIGHTS["roberta_score"] * df["roberta_score"]
        + WEIGHTS["vader_score"] * df["vader_score"]
        + WEIGHTS["textblob_score"] * df["textblob_score"]
        + WEIGHTS["distilbert_score"] * df["distilbert_score"]
    )

    # 5. Write output
    print(f"\n{'=' * 60}")
    print(f"WRITING RESULTS")
    print(f"{'=' * 60}")

    output_cols = [
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
    ]

    os.makedirs(args.output_path, exist_ok=True)

    # Write one parquet per asset class (same as Spark job)
    for asset_class, group in df.groupby("asset_class"):
        safe_name = asset_class.replace("/", "_").replace(" ", "_")
        out_file = os.path.join(
            args.output_path, f"asset_class={safe_name}", "part-00000.parquet"
        )
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        group[output_cols].to_parquet(out_file, index=False)
        print(f"  {asset_class}: {len(group):,} rows → {out_file}")

    total_time = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"DONE — {len(df):,} rows scored in {total_time / 3600:.1f} hours")
    print(f"{'=' * 60}")

    # Summary stats
    print(f"\nEnsemble score stats:")
    print(f"  Mean:   {df['ensemble_score'].mean():.4f}")
    print(f"  Median: {df['ensemble_score'].median():.4f}")
    print(f"  Std:    {df['ensemble_score'].std():.4f}")
    print(f"  Min:    {df['ensemble_score'].min():.4f}")
    print(f"  Max:    {df['ensemble_score'].max():.4f}")


if __name__ == "__main__":
    main()
