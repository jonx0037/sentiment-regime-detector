# Morning Session - February 2, 2026

## Project: Cross-Asset Sentiment Regime Detector (DS 6210 Capstone)

### Current State

#### Database: PostgreSQL with 100% sentiment coverage achieved

| Table | Count | Notes |
|-------|-------|-------|
| RawTexts | 2,657,261 | All sources |
| SentimentScores | 2,657,260 | FinBERT + RoBERTa ensemble |
| StressIndices | 12,029 | ECB CISS 1980-2026 |
| MarketData | 108,483 | 46 global indices |

#### Sources with full coverage

- reddit: 2,147,948 texts
- wsb_echo_chamber: 226,860 (GME, AMC, TSLA, AAPL, MSFT, NOK)
- kaggle: 219,607
- reddit_sentiment: 42,987
- news: 14,924
- financial_news: 2,876
- twitter: 1,058
- rss: 1,001

#### Models implemented

- GARCH-MIDAS (Layer 1 volatility) - `src/sentiment_detector/models/garch_midas.py`
- Statistical Jump Model (Layer 2 regime detection) - `src/sentiment_detector/models/jump_model.py`
- Hypothesis validation framework (H1, H2, H3 all supported)
- Walk-forward backtesting infrastructure

#### Today's Goals

1. **ECB CISS Integration** - Connect stress indices to GARCH-MIDAS model
2. **Historical Backtests** - Run crisis scenarios:
   - 2008 Financial Crisis (CISS peak 0.9428)
   - 2020 COVID Crash (CISS peak 0.6825)
   - 2021 GameStop squeeze
   - Crypto Winter 2022
   - Gold Rise since COVID
3. **Regime Validation** - Compare detected regimes vs VIX ground truth
4. **Dashboard API** - Wire up regime endpoints to frontend

---

### Quick Start

```bash
cd ~/Documents/SMU/DS_6210_Capstone

# Verify database status
python scripts/check_processing_status.py

# Run backtests
python scripts/run_2008_crisis_backtest.py
python scripts/run_gamestop_backtest.py
python scripts/run_multi_event_backtest.py

# Test pipeline
python scripts/test_pipeline.py

# Analyze results
python scripts/summarize_all_backtests.py
```

---

### Key Files

| File | Purpose |
|------|---------|
| `src/sentiment_detector/models/garch_midas.py` | GARCH-MIDAS implementation |
| `src/sentiment_detector/models/jump_model.py` | Statistical Jump Model (regime classifier) |
| `src/sentiment_detector/models/stress_index.py` | StressIndex SQLAlchemy model |
| `src/sentiment_detector/models/market_data.py` | MarketData SQLAlchemy model |
| `src/sentiment_detector/pipeline/regime_detection_pipeline.py` | End-to-end pipeline |
| `src/sentiment_detector/validation/hypothesis_validator.py` | H1/H2/H3 tests |
| `src/sentiment_detector/validation/walk_forward_backtest.py` | Walk-forward backtesting |

### Backtest Scripts

| Script | Description |
|--------|-------------|
| `scripts/run_2008_crisis_backtest.py` | 2008 Financial Crisis scenario |
| `scripts/run_gamestop_backtest.py` | 2021 GameStop squeeze |
| `scripts/run_multi_event_backtest.py` | Multiple crisis events |
| `scripts/run_2016_2026_backtests.py` | Extended historical range |
| `scripts/summarize_all_backtests.py` | Aggregate results |

---

### ManeFrame Reference (if needed)

```bash
ssh jarocha@m3.smu.edu
# SCRATCH: /lustre/scratch/client/users/jarocha
# Partition: gpu-dev, GPU: gpu:v100:1
# Module: python/3.11.11/pytorch/2025.08.21
```
