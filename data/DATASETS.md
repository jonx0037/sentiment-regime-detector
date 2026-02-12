# Datasets Reference

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 12, 2026

---

## 📊 Overview

This project processes **~33 million text records** (61.8M total rows, ~28.7M OHLCV excluded) spanning **24 years (2002-2026)** across 40+ Kaggle datasets and live API collections.

---

## 📁 Dataset Locations

### Primary Documentation

**For complete dataset catalog, see:**

📄 **[/data/kaggle/README.md](../data/kaggle/README.md)**

- Comprehensive catalog of all 21 Kaggle datasets
- Redundancy analysis and recommendations
- Temporal coverage and overlap details
- Dataset-specific import scripts
- Use case recommendations

📄 **[/data/README.md](../data/README.md)**

- Data directory structure
- Data pipeline flow diagram
- Data retention policies
- Quick start commands

---

## 🗂️ Dataset Categories

### Social Media & Forums

- **stock_market_comprehensive/** - 28.2M rows (equities social + market data)
- **twitter_stocks_2015_2020/** - 8.1M rows (stock tweets)
- **reddit-finance/** (1.2 GB) - 4.5M rows, multi-subreddit (2010-2024)
- **wsb-echo-chamber/** (1.5 GB) - Stock-specific meme analysis
- **wsb-2022/** (211 MB) - 2.1M rows from 2022
- **wsb/** (42 MB) - 400K rows, GameStop era (2020-2021)
- **reddit-sentiment-2025/** - 105K rows, recent preprocessed data
- **elon_tweets_2010_2025/** - 106K rows
- **stock_tweets/** / **stock_tweets_sentiment/** - 306K rows each

### Cryptocurrency

- **crypto-reddit/** (445 MB) - 4.9M rows, r/cryptocurrency, r/bitcoin, r/ethereum
- **crypto/** (425 MB) - 4.7M rows, market data by coin
- **crypto_top200_daily_2025/** - 349K rows
- **crypto-tweets/** (3.1 MB) - 37K tweets from crypto winter
- **crypto_top500_2024_2025/** - 40K rows
- **crypto_top100_2025/** - 33K rows
- **crypto_telegram/** - 15K rows
- **bitcoin_sentiment_2021_2024/** - 11K rows
- **crypto_sentiment_2025/** - 2K rows
- **crypto_1000_realtime_2025/** - 1.1K rows

### Financial News

- **massive_stock_news_db/** - 4.65M rows (largest news dataset)
- **apple_news_historical/** - 915K rows
- **us_financial_news_comprehensive/** - 612K rows
- **news_sentiment_comprehensive/** - 431K rows
- **russian_financial_news/** - 274K rows
- **stocknews/** / **stocknews_2008_crisis/** - 83K rows each
- **finsen_sentiment/** - 51K rows
- **financial-news/** (2.6 MB) - 4.8K FinancialPhraseBank labeled sentences
- **financial-news-nlp-2025/** / **financial_news_2025_extended/** - 3K rows each
- **high_quality_financial_news/** - 24K rows
- **sp500_news_2008_2024/** - 19K rows
- **ticker_sentiment_news/** - 11K rows
- **cnn_indonesia_economy_news/** - 36K rows
- **news_cnbc_indonesia_2024_2025/** - 10K rows

### Market Data & Indices (OHLCV — excluded from text corpus)

- **covid-world-indices/** - 108K rows, 46 global indices during COVID
- **forex_turkey_central_bank/** - 144K rows
- **forex_9currencies_2014_2024/** - 36K rows
- **forex/** - 3K rows, currency sentiment
- **forex_euro_1999_2025/** - 6.8K rows
- **forex_usd_major_currencies/** - 6.7K rows
- **commodity-gold/** - 10.5K rows (2000-2024)
- **commodities_natural_resources/** - 14K rows
- **commodities_major_1997_2025/** - 7.1K rows
- **ecb-ciss/** - 12K rows ⭐ ECB systemic stress indicator
- **vix_index/** / **vix_daily_updated/** - 9K rows each
- **indices_financial_giants/** - 5.1K rows
- **indices_stock_portfolio/** - 39K rows
- **market_trends_external/** - 30K rows

### Pre-Labeled (2.0 GB)

- **huggingface/** (2.0 GB) ⭐ - Expert-labeled gold standard

---

## 🔍 Quick Reference

### By Use Case

| Use Case | Recommended Datasets |
|----------|---------------------|
| **Crisis Studies** | ecb-ciss, covid-world-indices, stocknews |
| **Model Training** | huggingface, financial-news |
| **Long-Term Backtesting** | reddit-finance (14 years), forex, gold, ecb-ciss (26 years) |
| **Crypto Analysis** | crypto-reddit (most comprehensive) |
| **Retail Behavior** | wsb-2022 (highest volume), wsb-echo-chamber |

### By Time Period

| Period | Datasets | Purpose |
|--------|----------|---------|
| **2000-2010** | gold, ecb-ciss | Long-term baseline |
| **2010-2020** | reddit-finance, forex, stocknews | Pre-pandemic |
| **2020-2022** | covid-world-indices, wsb, wsb-2022 | COVID era |
| **2022-2024** | crypto-tweets, wsb-2022 | Crypto winter |
| **2024-2026** | reddit-sentiment-2025, financial-news-nlp-2025 | Recent/validation |

---

## ⚠️ Known Issues

### Duplicates (Action Required)

1. **EXACT DUPLICATE:** `stock_news/` = `financial-news/`
   - **Action:** Delete `stock_news/` directory
   - **Space Saved:** 2.6 MB

2. **95% Overlap:** `crypto/` vs `crypto-reddit/`
   - **Action:** Consolidate or document difference
   - **Decision:** TBD

### Temporal Overlaps (Keep All)

Multiple datasets cover similar periods but from **different sources** - all provide value:

- WallStreetBets: 3 datasets with different granularity
- Reddit finance: 2 datasets with different communities
- Crypto: 3 sources (tweets, reddit, market data)

---

## 📥 Import Scripts

### Import All Datasets

```bash
# Run all imports at once
python scripts/admin/run_all_imports.py
```

### Individual Imports

```bash
# Social media
python scripts/data_import/import_reddit_finance.py
python scripts/data_import/import_wsb_historical.py
python scripts/data_import/import_wsb_2022.py

# Market data
python scripts/data_import/import_ecb_ciss.py
python scripts/data_import/import_covid_indices.py
python scripts/data_import/import_gold_forex.py

# Pre-labeled
python scripts/data_import/import_prelabeled_sentiment.py
```

---

## 📈 Dataset Statistics

### Coverage (Verified Feb 12, 2026)

- **Total Rows on Disk:** 61,845,921
- **OHLCV/Price Data (excluded):** ~28.7M rows
- **Text Records (for sentiment):** ~33M
- **Date Range:** 2002-2026 (24 years)
- **CISS Records:** 12,029 (daily from 2000)
- **Market Data:** 400K+ records

### Asset Class Distribution

| Asset Class | Datasets | Verified Rows |
|-------------|----------|---------------|
| Equities (social) | 10+ | ~36.5M |
| Crypto | 10 | ~10.1M |
| News | 15+ | ~7.1M |
| Forex | 5 | ~197K |
| Commodities | 3 | ~31K |
| Market Data (OHLCV) | 8+ | ~28.7M |

---

## 🔗 Related Documentation

- **Data Directory Overview:** [/data/README.md](../data/README.md)
- **Complete Dataset Catalog:** [/data/kaggle/README.md](../data/kaggle/README.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **Scripts Reference:** [SCRIPTS.md](SCRIPTS.md)

---

**For dataset questions, contact:** Jonathan Rocha (<jrocha@smu.edu>)
