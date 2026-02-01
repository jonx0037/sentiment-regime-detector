# Afternoon Session Processing Plan - February 1, 2026

## Overview

This document outlines the complete plan for processing and integrating all new datasets discovered during the morning research session. The goal is to have all scripts ready for HPC submission by end of afternoon, with actual processing deferred to the evening session.

---

## Dataset Inventory Summary

| Dataset | Location | Size | Format | Processing |
|---------|----------|------|--------|------------|
| ECB CISS | `data/kaggle/ecb-ciss/` | 12,030 rows | CSV | Local |
| COVID World Indices | `data/kaggle/covid-world-indices/` | 46 indices | CSV | Local |
| WSB Echo Chamber | `data/kaggle/wsb-echo-chamber/` | 6 tickers, ~7K+ files | JSON | **HPC** |
| Bitcoin Tweets (HF) | `data/kaggle/huggingface/bitcoin_tweets_sentiment/` | 9.5MB | Parquet | Local |
| Financial News 2025 | `data/kaggle/financial-news-nlp-2025/` | ~1MB | CSV | Local |
| Reddit Sentiment 2025 | `data/kaggle/reddit-sentiment-2025/` | ~1MB | CSV | Local |
| CryptoMarket Classifier | `data/reference-repos/CryptoMarket_Regime_Classifier/` | Reference | Python | N/A |

---

## Processing Phases

### Phase 1: Local Imports (Afternoon - Direct Execution)

These datasets are small enough to import directly without HPC resources.

#### 1.1 ECB CISS (Systemic Stress Index)
- **Script**: `scripts/import_ecb_ciss.py`
- **Purpose**: 
  - Ground truth for regime validation (stress events)
  - Feature for GARCH-MIDAS model (macroeconomic stress)
- **Fields**: date, CISS_ea, CISS_de, CISS_fr, etc.
- **Time Range**: 1980-2026 (daily data)
- **Integration**: 
  - Create `StressIndex` table for storing CISS values
  - Link to regime validation via date alignment

#### 1.2 COVID World Indices
- **Script**: `scripts/import_covid_indices.py`
- **Purpose**: Global market data for cross-market regime analysis
- **Fields**: Date, Open, High, Low, Close, Volume per index
- **Time Range**: 2018-2024 covering COVID period
- **Integration**:
  - Create `MarketData` table for multi-market storage
  - Key indices: SP500, DJIA, NASDAQ, DAX, FTSE, Nikkei, etc.

#### 1.3 Pre-labeled Sentiment Datasets
- **Script**: `scripts/import_prelabeled_sentiment.py`
- **Datasets**:
  - Bitcoin Tweets Sentiment (HuggingFace, with labels)
  - Financial News NLP 2025 (with event labels)
  - Reddit Sentiment 2025 (pre-processed scores)
- **Purpose**: Validation data for sentiment model accuracy
- **Integration**: Import to `RawText` + `SentimentScore` tables with `is_prelabeled=True` flag

---

### Phase 2: HPC Processing (Evening - Submit to ManeFrame)

#### 2.1 WSB Echo Chamber Dataset
- **Preparation Script**: `scripts/prepare_wsb_echo_chamber.py`
- **HPC Script**: `scripts/hpc/wsb_echo_chamber.slurm`
- **Tickers**: GME, AMC, TSLA, AAPL, MSFT, NOK
- **Format**: JSON files with Reddit posts (selftext, score, timestamps, etc.)
- **Processing**:
  1. Parse JSON files per ticker
  2. Extract text, timestamps, scores
  3. Convert to HPC batch format
  4. Run FinBERT + RoBERTa sentiment on V100 GPU
- **Expected Volume**: ~7,000+ posts across 6 tickers
- **Estimated HPC Time**: ~15-20 minutes (based on prior job performance)

---

## Database Model Updates

### New Models Required

```python
# models/stress_index.py
class StressIndex(Base, TimestampMixin):
    """ECB CISS and other systemic stress indicators"""
    id = Column(Integer, primary_key=True)
    source = Column(String(50))  # 'ecb_ciss', 'vix', etc.
    date = Column(Date, index=True)
    region = Column(String(10))  # 'ea', 'de', 'us', etc.
    value = Column(Float)
    # Composite index on (source, date, region)

# models/market_data.py
class MarketData(Base, TimestampMixin):
    """Multi-market price data"""
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume = Column(BigInteger)
    source = Column(String(50))  # 'covid_indices', 'yahoo', etc.
```

### Model Updates

```python
# Add to models/sentiment.py - SentimentScore class
is_prelabeled = Column(Boolean, default=False)  # For validation datasets
prelabeled_source = Column(String(100))  # e.g., 'bitcoin_tweets_hf'
```

---

## Script Dependencies

### Required Packages
All packages should be available in the existing environment:
- `pandas`, `polars` - Data processing
- `sqlalchemy` - Database ORM
- `pyarrow` - Parquet file reading
- `transformers` - HuggingFace models (HPC only)
- `torch` - GPU processing (HPC only)

---

## Execution Order

### Afternoon Session (Local Machine)

```bash
# 1. Update database models (run Alembic migration)
alembic revision --autogenerate -m "Add StressIndex and MarketData models"
alembic upgrade head

# 2. Import local datasets
python scripts/import_ecb_ciss.py
python scripts/import_covid_indices.py
python scripts/import_prelabeled_sentiment.py

# 3. Prepare HPC batch
python scripts/prepare_wsb_echo_chamber.py

# 4. Package for HPC transfer
./scripts/package_for_hpc.sh
```

### Evening Session (ManeFrame M3)

```bash
# 1. Transfer HPC package to M3
scp hpc_package_*.tar.gz m3.smu.edu:~/capstone/

# 2. SSH to M3 and extract
ssh m3.smu.edu
cd ~/capstone && tar -xzf hpc_package_*.tar.gz

# 3. Submit SLURM job
sbatch scripts/hpc/wsb_echo_chamber.slurm

# 4. Monitor job
squeue -u $USER
tail -f logs/wsb_echo_chamber_*.log

# 5. After completion, transfer results back
scp m3.smu.edu:~/capstone/results/*.json ./data/hpc_results/

# 6. Import HPC results locally
python scripts/import_hpc_sentiment.py --input data/hpc_results/
```

---

## Validation Checkpoints

### After Phase 1 (Local Imports)
- [ ] ECB CISS: 12,030 rows in `stress_index` table
- [ ] COVID Indices: ~15,000+ rows in `market_data` table
- [ ] Pre-labeled: Verify sample sentiment scores match labels

### After Phase 2 (HPC Processing)
- [ ] WSB Echo Chamber: All 6 tickers processed
- [ ] Sentiment scores for ~7,000+ posts
- [ ] Cross-validate against pre-labeled datasets

---

## Integration with Existing Pipeline

### GARCH-MIDAS Layer
```python
# ECB CISS becomes a low-frequency exogenous variable
garch_midas_model.add_feature(
    'ecb_ciss',
    frequency='daily',
    transformation='log_diff',
    lags=[1, 5, 22]  # 1 day, 1 week, 1 month
)
```

### Regime Detection Layer
```python
# Use ECB CISS as ground truth for regime validation
regime_validator.set_ground_truth(
    source='ecb_ciss',
    high_stress_threshold=0.35,  # ECB standard threshold
    crisis_periods=['2008-09', '2011-11', '2020-03']
)
```

---

## Scripts to Create

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/import_ecb_ciss.py` | Import ECB CISS data | Pending |
| `scripts/import_covid_indices.py` | Import COVID indices | Pending |
| `scripts/import_prelabeled_sentiment.py` | Import pre-labeled sentiment | Pending |
| `scripts/prepare_wsb_echo_chamber.py` | Prepare WSB data for HPC | Pending |
| `scripts/hpc/wsb_echo_chamber.slurm` | HPC SLURM job script | Pending |
| `scripts/run_all_imports.py` | Master orchestrator | Pending |

---

## Timeline

| Time | Task |
|------|------|
| 2:00 PM | Create processing plan (this document) ✓ |
| 2:15 PM | Create database model updates |
| 2:30 PM | Create ECB CISS import script |
| 2:45 PM | Create COVID indices import script |
| 3:00 PM | Create pre-labeled sentiment import script |
| 3:15 PM | Create WSB Echo Chamber HPC prep script |
| 3:30 PM | Create SLURM job script |
| 3:45 PM | Create master orchestrator |
| 4:00 PM | Test local imports |
| 4:30 PM | Package for HPC |
| 5:00 PM | Break before evening session |

---

## Notes

- ECB CISS serves dual purpose: ground truth AND GARCH-MIDAS feature
- Process ALL WSB Echo Chamber tickers (GME, AMC, TSLA, AAPL, MSFT, NOK)
- Maximize HPC utilization for sentiment processing
- Pre-labeled datasets enable sentiment model validation

---

*Created: February 1, 2026 - Afternoon Session*
*Author: Capstone Project - Sentiment Regime Detector*
