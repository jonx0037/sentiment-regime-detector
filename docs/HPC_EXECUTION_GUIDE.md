# HPC Execution Guide: Complete Data Collection & Validation

**Goal:** Rebuild sentiment dataset from scratch with balanced, comprehensive coverage
**Timeline:** 5-7 days
**Platform:** SMU ManeFrame III

---

## 📋 Prerequisites

### 1. HPC Access

```bash
# SSH to ManeFrame III
ssh jarocha@m3.smu.edu

# Navigate to project
cd /work/$USER/sentiment-regime-detector
```

### 2. Environment Setup

```bash
# Create virtual environment (if not exists)
module load python/3.11
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install datasets transformers torch --extra-index-url https://download.pytorch.org/whl/cu121

# Create directories
mkdir -p /work/$USER/sentiment_regime_data/{raw_data,sentiment_results}
mkdir -p logs
```

### 3. Verify GPU Access

```bash
# Check A100 availability
sinfo -p gpu-a100

# Test GPU allocation
srun --partition=gpu-a100 --gres=gpu:1 --time=00:05:00 nvidia-smi
```

---

## 🚀 Execution Plan

### Phase 1: Data Collection (2-3 days)

**Submit array job for historical data collection:**

```bash
# Submit 72 parallel collection jobs (one per quarter, 2008-2026)
sbatch scripts/hpc/run_complete_collection.sh

# Monitor progress
watch -n 30 'squeue -u $USER'

# Check logs
tail -f logs/collect_*.out
```

**Expected Output:**

- 72 quarters collected in parallel
- ~250 GDELT articles + ~1000 Reddit posts per day
- Total: ~1.5M texts spanning 2008-2026
- Output: `/work/$USER/sentiment_regime_data/raw_data/`

**Validation Check:**

```bash
# After collection completes (2-3 days)
find /work/$USER/sentiment_regime_data/raw_data -name "*.parquet" | wc -l
# Should show 72+ files (one per quarter)

# Check a sample batch
python << 'EOF'
import pandas as pd
df = pd.read_parquet("/work/$USER/sentiment_regime_data/raw_data/combined_batch_0000.parquet")
print(f"Rows: {len(df):,}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
EOF
```

---

### Phase 2: Sentiment Processing (1-2 days)

**Submit array job for sentiment analysis:**

```bash
# Wait for collection to complete (check all 72 jobs finished)
squeue -u $USER

# Submit 72 parallel GPU jobs for sentiment processing
sbatch scripts/hpc/run_sentiment_processing.sh

# Monitor GPU usage
watch -n 60 'squeue -u $USER -p gpu-a100'

# Check processing logs
tail -f logs/process_*.out
```

**Expected Output:**

- FinBERT + VADER processing on A100 GPUs
- ~50-100 texts/sec per GPU
- Output: `/work/$USER/sentiment_regime_data/sentiment_results/`
  - `daily_batch_0000.csv` through `daily_batch_0071.csv`
  - Each contains daily aggregated sentiment for its quarter

**Validation Check:**

```bash
# After processing completes (1-2 days)
ls /work/$USER/sentiment_regime_data/sentiment_results/daily_batch_*.csv | wc -l
# Should show 72 files

# Check a sample
head -20 /work/$USER/sentiment_regime_data/sentiment_results/daily_batch_0000.csv
```

---

### Phase 3: Aggregation & Validation (1 hour)

**Combine all batches into final dataset:**

```bash
# Run aggregation script
python scripts/hpc/aggregate_all_sentiment.py \
    --sentiment-dir /work/$USER/sentiment_regime_data/sentiment_results \
    --output data/finbert_daily_sentiment_v2.csv

# This will:
# 1. Load all 72 daily batch files
# 2. Remove duplicates
# 3. Validate coverage (2008-2026)
# 4. Check crisis periods (2008, COVID-19, GameStop)
# 5. Save final consolidated dataset
```

**Expected Output:**

```
✅ AGGREGATION COMPLETE - READY FOR BACKTESTING
  Total days: 6,575
  Date range: 2008-01-01 to 2026-02-06
  Mean volume: 450 texts/day
  Coverage: 100%
```

**Validation Checks:**

```bash
# Verify final dataset
python << 'EOF'
import pandas as pd

df = pd.read_csv("data/finbert_daily_sentiment_v2.csv", parse_dates=['date'])

print("=" * 60)
print("FINAL DATASET VALIDATION")
print("=" * 60)
print(f"Total days: {len(df):,}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Mean volume: {df['volume'].mean():.0f} texts/day")
print(f"Median volume: {df['volume'].median():.0f}")

# Check crisis periods
crisis = {
    "2008 Crisis": ("2008-09-15", "2009-03-09"),
    "COVID-19": ("2020-02-24", "2020-04-15"),
    "GameStop": ("2021-01-13", "2021-02-05")
}

print("\nCrisis Period Coverage:")
for name, (start, end) in crisis.items():
    mask = (df['date'] >= start) & (df['date'] <= end)
    period_data = df[mask]
    print(f"  {name}: {len(period_data)} days, avg {period_data['volume'].mean():.0f} texts/day")

print("=" * 60)
EOF
```

---

### Phase 4: Backtest Validation (2 days)

**Re-run all historical backtests with new data:**

```bash
# Update BACKTEST_VALIDATION_PLAN.md to use new dataset
# Then run comprehensive validation

# Phase 3.1: 2008 Financial Crisis
python scripts/backtesting/run_2008_crisis_backtest.py \
    --data data/finbert_daily_sentiment_v2.csv \
    --verbose

# Phase 3.2: COVID-19 Pandemic
python scripts/backtesting/run_covid19_backtest.py \
    --data data/finbert_daily_sentiment_v2.csv \
    --verbose

# Phase 3.3: GameStop Squeeze
python scripts/backtesting/run_gamestop_backtest.py \
    --data data/finbert_daily_sentiment_v2.csv \
    --verbose

# Full suite
python scripts/backtesting/run_historical_backtests_ml.py \
    --data data/finbert_daily_sentiment_v2.csv \
    --output results/validation/backtests_$(date +%Y%m%d).json \
    --verbose
```

---

## 📊 Cost Estimation

### Compute Hours

- **Collection:** 72 jobs × 24h × 8 CPU = 13,824 CPU-hours
- **Processing:** 72 jobs × 12h × (1 A100 + 8 CPU) = ~864 GPU-hours
- **Total:** ~14,700 CPU-hours + 864 GPU-hours

### Estimated Time

- **Wall time (parallel):** 5-7 days
- **Sequential (if needed):** ~30-45 days

---

## 🚨 Troubleshooting

### Collection Jobs Failing

```bash
# Check specific job log
cat logs/collect_JOBID_TASKID.err

# Common issues:
# 1. API rate limits - Already handled with delays
# 2. Network timeouts - Retry failed batches manually
# 3. Disk space - Check: df -h /work/$USER
```

### GPU Jobs Not Starting

```bash
# Check A100 partition queue
squeue -p gpu-a100

# If long wait, try gpu-a100-2 partition
# Edit scripts/hpc/run_sentiment_processing.sh:
#SBATCH --partition=gpu-a100-2
```

### Out of Memory

```bash
# Reduce batch size in processing script
# Edit scripts/hpc/process_sentiment_batch.py:
# Change --batch-size from 64 to 32
```

---

## ✅ Success Criteria

**Data Collection:**

- ✓ 72/72 quarters collected
- ✓ All parquet files created
- ✓ No major date gaps

**Sentiment Processing:**

- ✓ 72/72 daily aggregates generated
- ✓ Mean volume >100 texts/day
- ✓ All crisis periods covered

**Final Dataset:**

- ✓ 6,000+ days of data
- ✓ 2008-2026 coverage
- ✓ Crisis periods validated
- ✓ Ready for backtesting

---

## 📞 Support

**HPC Issues:**

- SMU HPC Help Desk: <hpc@smu.edu>
- Documentation: <https://www.smu.edu/OIT/research>

**Project Issues:**

- Contact: Jonathan Rocha (<jrocha@smu.edu>)
- Advisor: Dr. David (King Ip) Lin (<kdlin@smu.edu>)

---

**Last Updated:** February 6, 2026
**Status:** Ready for execution
