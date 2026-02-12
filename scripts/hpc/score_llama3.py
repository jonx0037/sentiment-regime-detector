#!/usr/bin/env python3
"""
Add Llama 3 sentiment scores to existing scored parquet files.
Reads parquet output from score_sentiment.py, adds llama3_score column,
recalculates ensemble with 6-model weights, and overwrites the parquet.

Uses Llama-3.1-8B-Instruct with 4-bit quantization (bitsandbytes).
"""

import argparse
import os
import time

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm


# ── 6-model ensemble weights ────────────────────────────────
# Original 5-model weights (from score_sentiment.py):
#   FinBERT 31.25%, RoBERTa 25%, VADER 18.75%, TextBlob 12.5%, DistilBERT 12.5%
# With Llama 3 added, redistribute proportionally:
WEIGHTS_6 = {
    "finbert_score": 0.25,
    "roberta_score": 0.20,
    "vader_score": 0.15,
    "textblob_score": 0.10,
    "distilbert_score": 0.10,
    "llama3_score": 0.20,
}


def score_llama3(texts, batch_size=4, device="cuda"):
    """
    Score texts with Llama 3 8B Instruct (4-bit quantized).
    Uses generate() with a sentiment classification prompt.
    Returns array of scores: 1.0 (positive), -1.0 (negative), 0.0 (neutral).
    """
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

    model_name = "meta-llama/Llama-3.1-8B-Instruct"

    print(f"  Loading {model_name} (4-bit quantized)...")
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quantization_config,
        device_map="auto",
        dtype=torch.float16,
    )
    model.eval()
    print(f"  Model loaded. GPU Memory: {torch.cuda.memory_allocated() / 1e9:.1f} GB")

    all_scores = []

    for i in tqdm(
        range(0, len(texts), batch_size), desc="Llama3", unit="batch", mininterval=5
    ):
        batch_texts = texts[i : i + batch_size]

        for text in batch_texts:
            if not text or str(text) == "nan":
                all_scores.append(0.0)
                continue

            try:
                prompt = (
                    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
                    "You are a financial sentiment analyzer. Respond with exactly one word: "
                    "POSITIVE, NEGATIVE, or NEUTRAL.<|eot_id|>\n"
                    "<|start_header_id|>user<|end_header_id|>\n"
                    f"Text: {str(text)[:500]}\n"
                    "Sentiment:<|eot_id|>\n"
                    "<|start_header_id|>assistant<|end_header_id|>\n"
                )

                inputs = tokenizer(
                    prompt,
                    return_tensors="pt",
                    max_length=256,
                    truncation=True,
                )
                inputs = {k: v.to(model.device) for k, v in inputs.items()}

                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=5,
                        do_sample=False,
                        pad_token_id=tokenizer.pad_token_id,
                    )
                    response = (
                        tokenizer.decode(
                            outputs[0][inputs["input_ids"].shape[1] :],
                            skip_special_tokens=True,
                        )
                        .strip()
                        .lower()
                    )

                if "positive" in response:
                    all_scores.append(1.0)
                elif "negative" in response:
                    all_scores.append(-1.0)
                else:
                    all_scores.append(0.0)

            except Exception:
                all_scores.append(0.0)

        if device == "cuda":
            torch.cuda.empty_cache()

    del model, tokenizer
    torch.cuda.empty_cache()

    return np.array(all_scores, dtype=np.float32)


def main():
    parser = argparse.ArgumentParser(
        description="Add Llama 3 scores to existing parquet"
    )
    parser.add_argument(
        "--parquet-dir",
        required=True,
        help="Path to sentiment_processed output directory",
    )
    args = parser.parse_args()

    start_time = time.time()

    # Find all parquet files
    parquet_files = []
    for root, dirs, files in os.walk(args.parquet_dir):
        for f in files:
            if f.endswith(".parquet"):
                parquet_files.append(os.path.join(root, f))

    if not parquet_files:
        print("ERROR: No parquet files found!")
        return

    print(f"Found {len(parquet_files)} parquet files")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("ERROR: Llama 3 requires GPU")
        return

    print(f"GPU: {torch.cuda.get_device_name(0)}")

    # Process each parquet file
    total_rows = 0
    for pf in sorted(parquet_files):
        asset_dir = os.path.basename(os.path.dirname(pf))
        print(f"\n{'=' * 50}")
        print(f"Processing: {asset_dir}")

        df = pd.read_parquet(pf)
        total_rows += len(df)
        print(f"  Rows: {len(df):,}")

        texts = df["text_content"].tolist()

        t0 = time.time()
        df["llama3_score"] = score_llama3(texts, batch_size=1, device=device)
        print(f"  Llama3 done in {time.time() - t0:.1f}s")

        # Recalculate ensemble with 6-model weights
        df["ensemble_score"] = (
            WEIGHTS_6["finbert_score"] * df["finbert_score"]
            + WEIGHTS_6["roberta_score"] * df["roberta_score"]
            + WEIGHTS_6["vader_score"] * df["vader_score"]
            + WEIGHTS_6["textblob_score"] * df["textblob_score"]
            + WEIGHTS_6["distilbert_score"] * df["distilbert_score"]
            + WEIGHTS_6["llama3_score"] * df["llama3_score"]
        )

        # Overwrite parquet with new columns
        df.to_parquet(pf, index=False)
        print(f"  Saved: {pf}")

    total_time = time.time() - start_time
    print(f"\n{'=' * 50}")
    print(
        f"DONE — {total_rows:,} rows scored with Llama 3 in {total_time / 3600:.1f} hours"
    )
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
