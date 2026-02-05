# Datasets Reference

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

---

## 📊 Overview

This project processes **2.66 million texts** spanning **24 years (2002-2026)** across 21 Kaggle datasets and live API collections.

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

### Social Media & Forums (1.8 GB)

- **wsb-echo-chamber/** (1.5 GB) - Stock-specific meme analysis
- **reddit-finance/** (1.2 GB) - Multi-subreddit coverage (2010-2024)
- **wsb-2022/** (211 MB) - 2.1M rows from 2022
- **wsb/** (42 MB) - GameStop era (2020-2021)
- **reddit-sentiment-2025/** (11 MB) - Recent preprocessed data

### Cryptocurrency (475 MB)

- **crypto-reddit/** (445 MB) - r/cryptocurrency, r/bitcoin, r/ethereum
- **crypto/** (425 MB) - Market data by coin
- **crypto-tweets/** (3.1 MB) - 10k tweets from crypto winter

### Financial News (17 MB)

- **financial-news/** (2.6 MB) - FinancialPhraseBank labeled sentences
- **stocknews/** (14 MB) - DJIA news correlation (2008-2016)
- **financial-news-nlp-2025/** (2.0 MB) - Recent event-based news

### Market Data (12 MB)

- **covid-world-indices/** (5.8 MB) - 46 global indices during COVID
- **forex/** (4.1 MB) - Currency sentiment
- **commodity-gold/** (1.9 MB) - Gold prices (2000-2024)
- **ecb-ciss/** (424 KB) ⭐ - ECB systemic stress indicator

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

### Coverage

- **Total Texts:** 2.66 million
- **Date Range:** 2002-2026 (24 years)
- **CISS Records:** 12,029 (daily from 2000)
- **Market Data:** 135,000+ records

### Asset Class Distribution

| Asset Class | Datasets | Est. Texts |
|-------------|----------|------------|
| Equities | 8 | ~1.2M |
| Crypto | 4 | ~900K |
| Reddit (Mixed) | 5 | ~1.8M |
| Forex | 1 | ~50K |
| Commodities | 1 | ~30K |
| News | 4 | ~200K |

---

## 🔗 Related Documentation

- **Data Directory Overview:** [/data/README.md](../data/README.md)
- **Complete Dataset Catalog:** [/data/kaggle/README.md](../data/kaggle/README.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **Scripts Reference:** [SCRIPTS.md](SCRIPTS.md)

---

**For dataset questions, contact:** Jonathan Rocha (<jrocha@smu.edu>)
