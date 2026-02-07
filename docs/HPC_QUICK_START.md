# HPC Pipeline - Quick Start (CORRECTED)

**Status:** ✅ All scripts updated and ready to run
**Date:** February 6, 2026

---

## 🔧 Critical Corrections Applied

All execution scripts have been updated for your ManeFrame environment:

| Issue | Status |
|-------|--------|
| Wrong script name in guide | ✅ Fixed - use `collect_historical_array.sh` |
| Missing SLURM account | ✅ Fixed - added `jcheun_ds6210_1262_401_0001` |
| Wrong GPU partition (A100) | ✅ Fixed - changed to `gpu-dev` (V100) |
| Deprecated `/work` paths | ✅ Fixed - changed to `/scratch/users/$USER` |
| Old Python module | ✅ Fixed - using `data_science/2025.08.21` |
| Missing checkpoint support | ✅ Fixed - auto-resume enabled |
| Time limit exceeds partition max | ✅ Fixed - reduced to 24h (standard-s limit) |

---

## 🚀 Ready to Run

### Prerequisites

```bash
# On ManeFrame III
cd /scratch/users/jarocha/sentiment-detector

# Activate environment
module load python/3.11.11/data_science/2025.08.21
source venv/bin/activate

# Create directories
mkdir -p /scratch/users/jarocha/sentiment_regime_data/{raw_data,sentiment_results}
mkdir -p logs
```

### Phase 1: Data Collection (2-3 days)

```bash
# Submit 72 parallel collection jobs (max 36 concurrent)
sbatch scripts/hpc/collect_historical_array.sh

# Monitor in real-time
watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'

# Or check status manually
squeue -u $USER
```

**What's running:**
- 72 array jobs, one per quarter (2008-Q1 through 2026-Q4)
- Max 36 concurrent to avoid API rate limits
- Auto-checkpointing every quarter for resume capability
- Output: `/scratch/users/jarocha/sentiment_regime_data/raw_data/`

### Phase 2: Sentiment Processing (1-2 days)

```bash
# Wait for collection to complete first!
# Check: all 72 parquet files should exist

# Submit GPU jobs (V100, max 36 concurrent)
sbatch scripts/hpc/run_sentiment_processing.sh

# Monitor
watch -n 60 'bash scripts/hpc/monitor_progress.sh sentiment'
```

**What's running:**
- 72 GPU jobs using V100 (16GB VRAM)
- 5-model ensemble: FinBERT, VADER, TextBlob, DistilBERT, Llama 3
- Adaptive batch sizing for V100 memory constraints
- Output: `/scratch/users/jarocha/sentiment_regime_data/sentiment_results/`

### Phase 3: Aggregation (1 hour)

```bash
# Combine all 72 sentiment batches into one dataset
python scripts/hpc/aggregate_all_sentiment.py \
    --sentiment-dir /scratch/users/jarocha/sentiment_regime_data/sentiment_results \
    --output data/finbert_daily_sentiment_v2.csv
```

### Phase 3.5: GARCH-MIDAS (2 hours)

```bash
# Run volatility forecasting
sbatch scripts/hpc/run_garch_midas.sh

# Monitor
squeue -u $USER
```

### Phase 3.6: Regime Classification (1 hour)

```bash
# Run statistical jump model
sbatch scripts/hpc/run_regime_classification.sh

# Monitor
squeue -u $USER
```

---

## 🔍 Monitoring Commands

```bash
# Real-time dashboard (recommended)
watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'

# Check job status
squeue -u $USER

# Count completed files
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l
# Should be 72 when collection is done

# Check for errors
grep -i "error\|fail" logs/*.err | tail -20

# Detect failed jobs and get retry commands
bash scripts/hpc/detect_failures.sh collection

# Check disk space
df -h /scratch/users/$USER
```

---

## ⚠️ If Jobs Fail

### Automatic Recovery

Jobs have built-in checkpointing - they'll resume from where they left off if restarted.

### Manual Recovery

```bash
# 1. Detect what failed
bash scripts/hpc/detect_failures.sh collection  # or sentiment, garch, regime

# 2. The script will show failed batch IDs and suggest retry command
# 3. Copy and run the suggested command, e.g.:
sbatch --array=5,12,23 scripts/hpc/collect_historical_array.sh
```

### Common Issues

**API Rate Limits (HTTP 429):**
```bash
# Reduce parallelism
sbatch --array=0-71%10 scripts/hpc/collect_historical_array.sh
```

**GPU Out of Memory:**
```bash
# Already handled automatically with dynamic batch sizing
# If still occurs, edit scripts/hpc/process_sentiment_batch.py
# and reduce initial BATCH_SIZE from 64 to 32
```

**Disk Space:**
```bash
# Check space
df -h /scratch/users/$USER

# Clean up old logs if needed
tar -czf logs_backup.tar.gz logs/*.out logs/*.err
rm logs/*.out logs/*.err
```

---

## ✅ Validation

After each phase:

```bash
# Validate collection
python scripts/hpc/validate_pipeline_phase.py \
  --phase collection \
  --path /scratch/users/jarocha/sentiment_regime_data/raw_data

# Validate sentiment
python scripts/hpc/validate_pipeline_phase.py \
  --phase sentiment \
  --path /scratch/users/jarocha/sentiment_regime_data/sentiment_results

# Validate final dataset
python scripts/hpc/validate_pipeline_phase.py \
  --phase final \
  --path data/finbert_daily_sentiment_v2.csv
```

---

## 📊 Your ManeFrame Configuration

```bash
# Account (required for all jobs)
--account=jcheun_ds6210_1262_401_0001

# CPU Partitions
--partition=standard-s    # Standard memory (collection, regime)
--partition=standard-m    # Medium memory (GARCH-MIDAS)

# GPU Partition
--partition=gpu-dev       # V100 GPUs (16GB VRAM)

# Storage
/scratch/users/jarocha    # Use this, NOT /work

# Python Module
module load python/3.11.11/data_science/2025.08.21
```

---

## 🎯 Success Criteria

**Collection Complete:**
- [ ] 72 parquet files in `/scratch/users/jarocha/sentiment_regime_data/raw_data/`
- [ ] No major errors in logs
- [ ] Validation script passes

**Sentiment Processing Complete:**
- [ ] 72 CSV files in `/scratch/users/jarocha/sentiment_regime_data/sentiment_results/`
- [ ] All models completed successfully
- [ ] Validation script passes

**Pipeline Complete:**
- [ ] `data/finbert_daily_sentiment_v2.csv` created
- [ ] `volatility_forecasts.csv` created
- [ ] `regime_predictions.csv` created
- [ ] Ready for backtesting!

---

**Next Steps After Pipeline Completes:**

1. Run comprehensive validation
2. Start backtesting (Phase 4)
3. Document any issues encountered
4. Update resource estimates for future runs

---

**Last Updated:** February 6, 2026, 11:45 PM
**All scripts tested and ready for execution**
