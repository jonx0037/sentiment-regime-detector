#!/usr/bin/env python3
"""Fix multiline CSVs by stripping newlines from text fields.
Spark's CSV reader treats each line as a row, so embedded newlines corrupt data."""

import csv
import sys
import os

csv.field_size_limit(100 * 1024 * 1024)  # 100MB max field
MAX_TEXT_LEN = 5000  # Transformers only use ~512 tokens


def fix_csv(input_path):
    output_path = input_path + ".fixed"
    with (
        open(input_path, "r", encoding="utf-8") as fin,
        open(output_path, "w", newline="", encoding="utf-8") as fout,
    ):
        reader = csv.reader(fin)
        writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
        header = next(reader)
        writer.writerow(header)
        count = 0
        for row in reader:
            # Strip newlines and truncate extreme text
            cleaned = [
                field.replace("\n", " ").replace("\r", " ")[:MAX_TEXT_LEN]
                for field in row
            ]
            writer.writerow(cleaned)
            count += 1
            if count % 50000 == 0:
                print(f"  {count} rows...")
    os.replace(output_path, input_path)
    print(f"  Done: {count} rows, newlines stripped")
    return count


data_dir = sys.argv[1] if len(sys.argv) > 1 else "data/kaggle"
for name, fname in [
    ("us_financial_news_comprehensive", "aggregated_news.csv"),
    ("wsb-echo-chamber", "aggregated_wsb_posts.csv"),
    ("ticker_sentiment_news", "aggregated_ticker_news.csv"),
]:
    path = os.path.join(data_dir, name, fname)
    if os.path.exists(path):
        print(f"Fixing {path}...")
        fix_csv(path)
    else:
        print(f"SKIP: {path}")
