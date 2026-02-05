# Scripts Directory

Utility scripts for data collection, processing, validation, analysis, and HPC operations.

## 📁 Directory Structure

### [admin/](admin/) (4 scripts)
System administration and setup scripts.

**Key Scripts:**
- `seed_data.py` - Seed database with initial data
- `start_dev.sh` - Start development environment
- `update_vix_extended.py` - Update VIX data
- `run_all_imports.py` - Bulk import orchestrator

**When to Use:** Initial setup, environment management, bulk operations

---

### [analysis/](analysis/) (6 scripts)
Data analysis, regime detection, and result evaluation.

**Key Scripts:**
- `analyze_2008_backtest.py` - Analyze 2008 financial crisis backtest results
- `analyze_regimes.py` - Regime pattern analysis
- `analyze_results.py` - General results analysis
- `analyze_texts.py` - Text data analysis
- `detect_regime.py` - Real-time regime detection
- `evaluate_sentiment.py` - Sentiment model evaluation

**When to Use:** Post-processing analysis, regime investigation, model evaluation

---

### [backtesting/](backtesting/) (11 scripts)
Historical backtesting and performance evaluation.

**Key Scripts:**
- `run_historical_backtests.py` - Main historical backtest runner
- `run_2008_crisis_backtest.py` - 2008 financial crisis specific
- `run_gamestop_backtest.py` - GameStop event (Jan 2021)
- `run_garch_midas_backtests.py` - GARCH-MIDAS model backtests
- `run_cross_asset_backtests.py` - Multi-asset class backtests
- `summarize_all_backtests.py` - Generate backtest summary report

**Variants:**
- `_conditional.py` - Conditional classifier model
- `_ensemble.py` - Ensemble model approach
- `_ml.py` - Machine learning classifier

**When to Use:** Performance evaluation, strategy validation, historical analysis

---

### [data_collection/](data_collection/) (8 scripts)
Collect data from external sources (APIs, Kaggle, market data).

**Key Scripts:**
- `collect_multi_source.py` - Multi-source collection (Twitter, Reddit, RSS)
- `collect_reddit_data.py` - Reddit-specific collection
- `collect_vix_data.py` - VIX data from CBOE
- `download_kaggle_data.py` - Download Kaggle datasets
- `download_cross_asset_data.py` - Multi-asset market data
- `cron_collect.sh` - Scheduled data collection

**When to Use:** Initial data gathering, scheduled updates, new data sources

---

### [data_import/](data_import/) (13 scripts)
Import collected data into PostgreSQL database.

**Key Scripts:**
- `import_to_postgres.py` - General PostgreSQL import
- `import_ecb_ciss.py` - ECB Composite Indicator of Systemic Stress
- `import_reddit_finance.py` - Reddit financial discussions
- `import_wsb_2022.py` - WallStreetBets 2022 data
- `import_wsb_historical.py` - Historical WSB data
- `import_prelabeled_sentiment.py` - Pre-labeled sentiment datasets
- `import_collected_data.py` - Import from collection scripts
- `import_hpc_sentiment.py` - Import HPC sentiment results
- `import_maneframe_results.py` - Import MANEFRAME outputs
- `import_phased_hpc_results.py` - Phased HPC batch results

**When to Use:** After data collection, database population, HPC result integration

---

### [hpc/](hpc/) (14 scripts)
High-Performance Computing (MANEFRAME III) batch processing.

**Key Scripts:**
- `package_for_hpc.sh` - Create HPC deployment package
- `export_for_hpc.py` - Export data for HPC processing
- `export_phase1_hpc.py` - Phase 1 batch export
- `export_phase2_hpc.py` - Phase 2 batch export
- `run_kaggle_sentiment.sh` - SLURM job for Kaggle data
- `batch_sentiment.py` - Batch sentiment processing
- `hpc_garch_midas.py` - GARCH-MIDAS on HPC

**When to Use:** Large-scale batch processing (millions of texts), GPU model training

---

### [ml_training/](ml_training/) (1 script)
Machine learning model training and fine-tuning.

**Key Scripts:**
- `train_regime_classifier.py` - Train regime classification model

**When to Use:** Model training, hyperparameter tuning, model updates

---

### [processing/](processing/) (8 scripts)
Data processing, transformation, and preparation.

**Key Scripts:**
- `process_batch.py` - Batch processing pipeline
- `process_kaggle_sentiment.py` - Process Kaggle sentiment data
- `prepare_kaggle_batch.py` - Prepare Kaggle data for processing
- `batch_sentiment_vader.py` - VADER sentiment batch processing
- `calculate_indices.py` - Calculate sentiment indices
- `fix_midas_alignment.py` - Fix MIDAS temporal alignment
- `export_garch_midas_data.py` - Export GARCH-MIDAS data

**When to Use:** Data transformation, feature engineering, data preparation

---

### [validation/](validation/) (21 scripts)
Data validation, database checks, and integration testing.

**Key Scripts:**
- `check_db.py` / `check_db_status.py` - Database status checks
- `check_dates.py` / `check_text_dates.py` - Temporal coverage validation
- `check_2008_data.py` - Verify 2008 crisis data completeness
- `check_2016_2026_coverage.py` - Verify date range coverage
- `verify_ciss_data.py` - CISS data validation
- `test_pipeline.py` - End-to-end pipeline test
- `test_garch_midas.py` - GARCH-MIDAS model test
- `test_api.py` - API endpoint tests
- `test_maneframe.sh` / `test_maneframe_gpu.sh` - HPC environment tests

**When to Use:** Data quality checks, integration testing, pre-deployment validation

---

### [visualization/](visualization/) (3 scripts)
Generate charts, plots, and visual analysis.

**Key Scripts:**
- `generate_visualizations.py` - Main visualization generator
- `generate_comparative_visualizations.py` - Comparative analysis plots
- `generate_sample_data.py` - Generate synthetic test data

**When to Use:** Result visualization, report generation, exploratory data analysis

---

## 🚀 Common Workflows

### Initial Setup
```bash
# 1. Start infrastructure
docker compose up -d

# 2. Run database migrations
alembic upgrade head

# 3. Seed initial data
python scripts/admin/seed_data.py

# 4. Import core datasets
python scripts/data_import/import_ecb_ciss.py
python scripts/data_import/import_reddit_finance.py
```

### Data Collection & Import
```bash
# Collect from multiple sources
python scripts/data_collection/collect_multi_source.py --sources twitter,rss,reddit

# Download Kaggle datasets
python scripts/data_collection/download_kaggle_data.py

# Import to database
python scripts/data_import/import_to_postgres.py
```

### Analysis & Backtesting
```bash
# Run historical backtests
python scripts/backtesting/run_historical_backtests.py

# Analyze specific event
python scripts/backtesting/run_2008_crisis_backtest.py

# Generate summary
python scripts/backtesting/summarize_all_backtests.py

# Create visualizations
python scripts/visualization/generate_comparative_visualizations.py
```

### HPC Processing
```bash
# Package for MANEFRAME
./scripts/hpc/package_for_hpc.sh

# Transfer to HPC
scp sentiment-detector-hpc-*.tar.gz username@m3.smu.edu:/path/

# On MANEFRAME: Submit job
sbatch scripts/hpc/run_kaggle_sentiment.sh

# After completion: Import results
python scripts/data_import/import_maneframe_results.py
```

### Validation
```bash
# Check database status
python scripts/validation/check_db_status.py

# Verify date coverage
python scripts/validation/check_2016_2026_coverage.py

# Test full pipeline
python scripts/validation/test_pipeline.py
```

## 📝 Script Naming Conventions

| Prefix | Purpose | Example |
|--------|---------|---------|
| `collect_*` | Data collection | `collect_multi_source.py` |
| `download_*` | Data downloads | `download_kaggle_data.py` |
| `import_*` | Database import | `import_ecb_ciss.py` |
| `process_*` | Data processing | `process_batch.py` |
| `analyze_*` | Analysis | `analyze_regimes.py` |
| `run_*` | Execute tasks | `run_historical_backtests.py` |
| `check_*` | Validation | `check_db_status.py` |
| `test_*` | Testing | `test_pipeline.py` |
| `generate_*` | Generation | `generate_visualizations.py` |
| `export_*` | Data export | `export_for_hpc.py` |
| `train_*` | ML training | `train_regime_classifier.py` |

## 🔧 Environment Requirements

Most scripts require:
- Python 3.11+ with project dependencies: `pip install -e .`
- PostgreSQL database running: `docker compose up -d`
- Environment variables configured: `.env` file (see [.env.example](../.env.example))

HPC scripts additionally require:
- MANEFRAME III access
- SLURM job scheduler
- CUDA-enabled GPUs (for Spark/FinBERT processing)

## 📚 Additional Documentation

- [Docker Guide](../DOCKER_GUIDE.md) - Infrastructure setup
- [HPC Spark README](../src/sentiment_detector/spark/README.md) - Distributed processing
- [Main README](../README.md) - Project overview

---

## 🔄 Migration Notes

**February 2026 Reorganization:**
- Consolidated 80+ scripts from flat structure into 10 functional directories
- Added this README for navigation and discovery
- All scripts retained in git history with `git mv` (no data loss)
- Maintained original filenames for easy grep/search

**Finding Old Script Locations:**
```bash
# Search git history for a script
git log --all --follow -- scripts/**/*script_name.py

# Find current location
find scripts -name "script_name.py"
```

---

*Last Updated: February 2026 | Workspace Audit & Cleanup*
