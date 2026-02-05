# Scripts Reference

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

---

## 📋 Overview

The `/scripts/` directory contains **89 utility scripts** organized into **10 functional categories**.

---

## 📁 Primary Documentation

**For complete scripts reference, see:**

📄 **[/scripts/README.md](../scripts/README.md)**
- Complete catalog of all 89 scripts
- Organized by functional category
- Usage examples for each script
- Input/output specifications
- Common workflows

---

## 🗂️ Script Categories

### 1. Data Collection (7 scripts)

Collect data from external APIs and sources.

**Key Scripts:**

```bash
# Reddit data collection
python scripts/data_collection/collect_reddit_data.py --limit 1000

# Multi-source collection
python scripts/data_collection/collect_multi_source.py --sources reddit,twitter,rss

# VIX data download
python scripts/data_collection/collect_vix_data.py
```

**Location:** [/scripts/data_collection/](../scripts/data_collection/)

---

### 2. Data Import (14 scripts)

Import data from various sources into PostgreSQL.

**Key Scripts:**

```bash
# Import Reddit finance data
python scripts/data_import/import_reddit_finance.py

# Import WallStreetBets historical
python scripts/data_import/import_wsb_historical.py
python scripts/data_import/import_wsb_2022.py

# Import market data
python scripts/data_import/import_ecb_ciss.py
python scripts/data_import/import_covid_indices.py

# Import HPC results
python scripts/data_import/import_phased_hpc_results.py --phase 1

# Run ALL imports
python scripts/admin/run_all_imports.py
```

**Location:** [/scripts/data_import/](../scripts/data_import/)

---

### 3. HPC Processing (4 scripts)

Export data for HPC processing and package for transfer.

**Key Scripts:**

```bash
# Export for phase 1 processing
python scripts/hpc/export_phase1_hpc.py --batch-size 50000

# Export for phase 2 (refinement)
python scripts/hpc/export_phase2_hpc.py

# Export MIDAS-aligned data
python scripts/hpc/export_aligned_midas_for_hpc.py

# Package for ManeFrame transfer
bash scripts/hpc/package_for_hpc.sh
```

**Location:** [/scripts/hpc/](../scripts/hpc/)

---

### 4. Processing (8 scripts)

Process and transform data.

**Key Scripts:**

```bash
# Batch sentiment analysis (VADER)
python scripts/processing/batch_sentiment_vader.py

# Calculate market indices
python scripts/processing/calculate_indices.py

# Fix MIDAS alignment
python scripts/processing/fix_midas_alignment.py

# Export GARCH-MIDAS data
python scripts/processing/export_garch_midas_data.py

# Process Kaggle sentiment
python scripts/processing/process_kaggle_sentiment.py
```

**Location:** [/scripts/processing/](../scripts/processing/)

---

### 5. Backtesting (9 scripts)

Run historical backtests and evaluate models.

**Key Scripts:**

```bash
# Historical backtests (multiple periods)
python scripts/backtesting/run_historical_backtests.py
python scripts/backtesting/run_historical_backtests_ml.py
python scripts/backtesting/run_historical_backtests_conditional.py

# Crisis event backtests
python scripts/backtesting/run_2008_crisis_backtest.py
python scripts/backtesting/run_gamestop_backtest.py

# GARCH-MIDAS backtests
python scripts/backtesting/run_garch_midas_backtests.py

# Summarize all results
python scripts/backtesting/summarize_all_backtests.py
```

**Location:** [/scripts/backtesting/](../scripts/backtesting/)

---

### 6. Analysis (6 scripts)

Analyze results and generate insights.

**Key Scripts:**

```bash
# Analyze regime transitions
python scripts/analysis/analyze_regimes.py

# Analyze backtest results
python scripts/analysis/analyze_results.py

# Analyze 2008 crisis
python scripts/analysis/analyze_2008_backtest.py

# Detect current regime
python scripts/analysis/detect_regime.py

# Evaluate sentiment accuracy
python scripts/analysis/evaluate_sentiment.py
```

**Location:** [/scripts/analysis/](../scripts/analysis/)

---

### 7. Validation (17 scripts)

Verify data quality and system status.

**Key Scripts:**

```bash
# Check database status
python scripts/validation/check_db_status.py

# Check processing status
python scripts/validation/check_processing_status.py

# Verify date coverage
python scripts/validation/check_text_dates.py
python scripts/validation/check_2016_2026_coverage.py

# Check event coverage
python scripts/validation/check_event_coverage.py

# Test API endpoints
python scripts/validation/test_api.py

# Test GARCH-MIDAS
python scripts/validation/test_garch_midas.py
```

**Location:** [/scripts/validation/](../scripts/validation/)

---

### 8. Visualization (3 scripts)

Generate charts and visualizations.

**Key Scripts:**

```bash
# Generate comparative visualizations
python scripts/visualization/generate_comparative_visualizations.py

# Generate general visualizations
python scripts/visualization/generate_visualizations.py

# Generate sample data
python scripts/visualization/generate_sample_data.py
```

**Location:** [/scripts/visualization/](../scripts/visualization/)

---

### 9. ML Training (1 script)

Train machine learning models.

**Key Scripts:**

```bash
# Train regime classifier
python scripts/ml_training/train_regime_classifier.py
```

**Location:** [/scripts/ml_training/](../scripts/ml_training/)

---

### 10. Admin (4 scripts)

Administrative and maintenance tasks.

**Key Scripts:**

```bash
# Run all imports
python scripts/admin/run_all_imports.py

# Seed database with sample data
python scripts/admin/seed_data.py

# Start development environment
bash scripts/admin/start_dev.sh

# Update VIX extended data
python scripts/admin/update_vix_extended.py
```

**Location:** [/scripts/admin/](../scripts/admin/)

---

## 🔄 Common Workflows

### Complete Data Pipeline

```bash
# 1. Collect data
python scripts/data_collection/collect_multi_source.py

# 2. Import to database
python scripts/data_import/import_collected_data.py --input data/raw/latest.json

# 3. Export for HPC
python scripts/hpc/export_phase1_hpc.py

# 4. [Process on HPC - see DEPLOYMENT.md]

# 5. Import HPC results
python scripts/data_import/import_phased_hpc_results.py --phase 1

# 6. Run backtests
python scripts/backtesting/run_historical_backtests_ml.py

# 7. Generate visualizations
python scripts/visualization/generate_comparative_visualizations.py

# 8. Validate results
python scripts/validation/check_processing_status.py
```

### Quick Data Import

```bash
# Import all Kaggle datasets
python scripts/admin/run_all_imports.py

# Verify import
python scripts/validation/check_db_status.py
python scripts/validation/check_text_dates.py
```

### HPC Workflow

```bash
# Local: Export batches
python scripts/hpc/export_phase1_hpc.py
bash scripts/hpc/package_for_hpc.sh

# Transfer to ManeFrame
scp sentiment-hpc.tar.gz jarocha@m3.smu.edu:~/

# ManeFrame: Submit jobs
sbatch scripts/hpc/slurm_job_array.sh

# Local: Import results
python scripts/data_import/import_phased_hpc_results.py --phase 1
```

### Validation Workflow

```bash
# Check system status
python scripts/validation/check_db_status.py
python scripts/validation/check_processing_status.py

# Verify data quality
python scripts/validation/check_text_dates.py
python scripts/validation/check_event_coverage.py

# Test components
python scripts/validation/test_api.py
python scripts/validation/test_garch_midas.py
python scripts/validation/test_hypothesis_validator.py
```

---

## 📊 Script Statistics

### By Category

| Category | Scripts | Purpose |
|----------|---------|---------|
| Validation | 17 | Data quality & testing |
| Data Import | 14 | Loading external data |
| Backtesting | 9 | Model evaluation |
| Processing | 8 | Data transformation |
| Data Collection | 7 | API data gathering |
| Analysis | 6 | Results analysis |
| Admin | 4 | Maintenance tasks |
| HPC | 4 | Cluster processing |
| Visualization | 3 | Chart generation |
| ML Training | 1 | Model training |

**Total:** 89 scripts across 10 categories

---

## 🔧 Common Patterns

### Standard Argument Structure

Most scripts follow this pattern:

```bash
python script_name.py \
  --input <input_file> \
  --output <output_file> \
  --config <config_file> \
  [options]
```

### Help Documentation

All scripts include help:

```bash
python script_name.py --help
```

### Logging

Scripts log to console and optionally to files:

```bash
# Enable verbose logging
python script_name.py --log-level DEBUG

# Save logs to file
python script_name.py --log-file logs/script.log
```

---

## 🔗 Related Documentation

- **Scripts Directory:** [/scripts/README.md](../scripts/README.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **Development Guide:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **HPC Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md#hpc-deployment-maneframe-iii)

---

**For script questions, contact:** Jonathan Rocha (<jrocha@smu.edu>)
