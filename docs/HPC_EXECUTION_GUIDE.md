# HPC Execution Guide: Complete Data Collection & Validation

**Goal:** Rebuild sentiment dataset from $scratch with balanced, comprehensive coverage
**Timeline:** 5-7 days
**Platform:** SMU ManeFrame III

---

## 📋 Prerequisites

### 1. HPC Access

```bash
# SSH to ManeFrame III
ssh jarocha@m3.smu.edu

# Navigate to project
cd /scratch/users/jarocha/sentiment-detector
```

### 2. Environment Setup

```bash
# Load Python with data science environment
# (includes numpy, pandas, scipy, and other scientific packages)
module load python/3.11.11/data_science/2025.08.21

# Remove old venv if it exists (from previous Python module)
rm -rf venv

# Create fresh virtual environment
python -m venv venv
source venv/bin/activate

# Install additional dependencies
pip install --upgrade pip setuptools wheel

# Install from requirements.txt if it exists
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  # Manual install of key packages if requirements.txt is missing
  pip install numpy pandas scipy scikit-learn
  pip install torch --index-url https://download.pytorch.org/whl/cu121
  pip install transformers datasets
  pip install pandas-datareader quandl yfinance
  pip install shap plotly
fi

# Create directories
mkdir -p /scratch/users/jarocha/sentiment_regime_data/{raw_data,sentiment_results}
mkdir -p logs
```

### 3. Verify GPU Access

```bash
# Check V100 availability (your course account has access to gpu-dev)
sinfo -p gpu-dev

# Test GPU allocation
srun --account=jcheun_ds6210_1262_401_0001 --partition=gpu-dev --gres=gpu:1 --mem=4G --time=00:05:00 nvidia-smi
```

**Note:** Your DS 6210 account has access to Tesla V100 GPUs on the `gpu-dev` partition. A100 GPUs are not currently accessible.

### 4. Module Discovery (If configs change)

If the Python modules are unavailable or you want to check alternatives:

```bash
# List available Python modules
module avail python

# Search for specific versions
module spider python

# Load a different variant if data_science isn't available
module load python/3.11.11/pytorch/2025.08.21  # PyTorch variant
# or
module load python/3.11.11/tensorflow/2025.08.21  # TensorFlow variant
```

---

## 🚀 Execution Plan

### Phase 1: Data Collection (2-3 days)

**Submit array job for historical data collection:**

```bash
# Submit 72 parallel collection jobs (one per quarter, 2008-2026)
sbatch scripts/hpc/collect_historical_array.sh

# Monitor progress
watch -n 30 'squeue -u $USER'

# Check logs
tail -f logs/collect_*.out
```

**Expected Output:**

- 72 quarters collected in parallel
- ~250 GDELT articles + ~1000 Reddit posts per day
- Total: ~1.5M texts spanning 2008-2026
- Output: `/scratch/users/jarocha/sentiment_regime_data/raw_data/`

**Validation Check:**

```bash
# After collection completes (2-3 days)
find /scratch/users/jarocha/sentiment_regime_data/raw_data -name "*.parquet" | wc -l
# Should show 72+ files (one per quarter)

# Check a sample batch
python << 'EOF'
import pandas as pd
df = pd.read_parquet("/scratch/users/jarocha/sentiment_regime_data/raw_data/combined_batch_0000.parquet")
print(f"Rows: {len(df):,}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
EOF
```

---

### Phase 2: Sentiment Processing (1-2 days)

**Submit array job for sentiment analysis:**

```bash
# Wait for collection to complete (check all 72 jobs finished)
squeue -u jarocha

# Submit 72 parallel GPU jobs for sentiment processing
sbatch scripts/hpc/run_sentiment_processing.sh

# Monitor GPU usage
watch -n 60 'squeue -u jarocha -p gpu-dev'

# Check processing logs
tail -f logs/process_*.out
```

**Expected Output:**

- Full 5-model sentiment ensemble on V100 GPUs:
  - FinBERT (financial domain BERT)
  - VADER (lexicon-based)
  - TextBlob (rule-based)
  - DistilBERT (general domain)
  - Llama 3 (LLM-based, nuanced understanding)
- ~30-50 texts/sec per GPU (V100 is slower than A100 but sufficient)
- Output: `/scratch/users/jarocha/sentiment_regime_data/sentiment_results/`
  - `daily_batch_0000.csv` through `daily_batch_0071.csv`
  - Each contains daily aggregated sentiment for its quarter

**Validation Check:**

```bash
# After processing completes (1-2 days)
ls /scratch/users/jarocha/sentiment_regime_data/sentiment_results/daily_batch_*.csv | wc -l
# Should show 72 files

# Check a sample
head -20 /scratch/users/jarocha/sentiment_regime_data/sentiment_results/daily_batch_0000.csv
```

---

### Phase 3: Aggregation & Validation (1 hour)

**Combine all batches into final dataset:**

```bash
# Run aggregation script
python scripts/hpc/aggregate_all_sentiment.py \
    --sentiment-dir /scratch/users/jarocha/sentiment_regime_data/sentiment_results \
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

### Phase 3.5: GARCH-MIDAS Volatility Forecasting (2 hours)

**Run GARCH-MIDAS model after sentiment aggregation:**

```bash
# Submit GARCH-MIDAS job
sbatch scripts/hpc/run_garch_midas.sh

# Monitor progress
watch -n 30 'squeue -u jarocha'

# Check logs
tail -f logs/garch_midas_*.out
```

**Expected Output:**

- GARCH(1,1) + MIDAS volatility estimates
- Long-run (sentiment/CISS-driven) and short-run (market-driven) components
- 22-day ahead volatility forecasts
- Output: `/scratch/users/jarocha/sentiment_regime_data/volatility_forecasts.csv`

**Validation Check:**

```bash
# Check volatility estimates
head -20 /scratch/users/jarocha/sentiment_regime_data/volatility_forecasts.csv

# Check model parameters in logs
grep "GARCH Parameters" logs/garch_midas_*.out
```

---

### Phase 3.6: Regime Classification (1 hour)

**Run Statistical Jump Model after GARCH-MIDAS:**

```bash
# Submit regime classification job
sbatch scripts/hpc/run_regime_classification.sh

# Monitor progress
watch -n 30 'squeue -u jarocha'

# Check logs
tail -f logs/regime_class_*.out
```

**Expected Output:**

- Regime classifications: Risk-On, Transition, Risk-Off
- Regime probabilities for each day
- Crisis indicators (risk-off periods)
- Feature importance (volatility, sentiment divergence, connectedness)
- Output: `/scratch/users/jarocha/sentiment_regime_data/regime_predictions.csv`

**Validation Check:**

```bash
# Check regime predictions
head -20 /scratch/users/jarocha/sentiment_regime_data/regime_predictions.csv

# Count regime distribution
python << 'EOF'
import pandas as pd
df = pd.read_csv("/scratch/users/jarocha/sentiment_regime_data/regime_predictions.csv")
print(df['regime_name'].value_counts())
print(f"\nCrisis days: {df['crisis_indicator'].sum()} ({df['crisis_indicator'].mean():.1%})")
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

## 🔍 Comprehensive Validation Frame$scratch

### Automated Validation Script

Create a validation script that runs after each phase to catch issues early:

```bash
# scripts/hpc/validate_pipeline_phase.py
```

**This script should check:**

#### Phase 1: Data Collection Quality Checks

```python
# After each quarter collection completes
import pandas as pd
from pathlib import Path

def validate_collection_batch(batch_file: Path):
    """Validate a single collected quarter"""
    df = pd.read_parquet(batch_file)

    issues = []

    # Volume checks
    min_daily_volume = TODO  # What's your minimum acceptable texts/day?
    daily_counts = df.groupby('date').size()
    low_volume_days = daily_counts[daily_counts < min_daily_volume]
    if len(low_volume_days) > 0:
        issues.append(f"⚠️  {len(low_volume_days)} days below {min_daily_volume} texts")

    # Date continuity
    date_range = pd.date_range(df['date'].min(), df['date'].max())
    missing_dates = set(date_range) - set(df['date'].unique())
    max_gap_days = TODO  # How many consecutive missing days are acceptable?
    if len(missing_dates) > max_gap_days:
        issues.append(f"⚠️  {len(missing_dates)} missing dates in quarter")

    # Content quality
    null_text_pct = df['text'].isna().mean()
    max_null_pct = TODO  # What % null text is acceptable? (suggest 0.01)
    if null_text_pct > max_null_pct:
        issues.append(f"⚠️  {null_text_pct:.1%} null text values")

    # Text length distribution
    df['text_length'] = df['text'].str.len()
    min_text_length = TODO  # Minimum characters for valid text?
    short_texts = (df['text_length'] < min_text_length).sum()
    if short_texts > len(df) * 0.05:  # >5% too short
        issues.append(f"⚠️  {short_texts:,} texts below {min_text_length} chars")

    # Source balance
    source_dist = df['source'].value_counts(normalize=True)
    # TODO: Define your expected source distribution (GDELT vs Reddit)
    # E.g., expect 20-30% GDELT, 70-80% Reddit

    return issues
```

#### Phase 2: Sentiment Processing Quality Checks

```python
def validate_sentiment_batch(batch_file: Path):
    """Validate daily sentiment aggregates"""
    df = pd.read_csv(batch_file)

    issues = []

    # Sentiment range checks (should be [-1, 1] for most models)
    for model in ['finbert', 'vader', 'textblob', 'distilbert', 'llama3']:
        col = f'{model}_sentiment'
        if col in df.columns:
            out_of_range = ((df[col] < -1) | (df[col] > 1)).sum()
            if out_of_range > 0:
                issues.append(f"⚠️  {model}: {out_of_range} values out of range")

    # Model agreement check
    sentiment_cols = [c for c in df.columns if '_sentiment' in c]
    df['sentiment_std'] = df[sentiment_cols].std(axis=1)
    high_disagreement_threshold = TODO  # When do models disagree too much? (suggest 0.5)
    high_disagreement = (df['sentiment_std'] > high_disagreement_threshold).sum()
    if high_disagreement > len(df) * 0.10:  # >10% with high disagreement
        issues.append(f"⚠️  {high_disagreement} days ({high_disagreement/len(df):.1%}) with high model disagreement (std > {high_disagreement_threshold})")

    # Volume consistency with raw data
    min_volume = TODO  # After processing, minimum texts/day
    low_volume = (df['volume'] < min_volume).sum()
    if low_volume > 0:
        issues.append(f"⚠️  {low_volume} days with volume < {min_volume}")

    return issues
```

#### Phase 3: Final Dataset Validation

```python
def validate_final_dataset(csv_path: Path):
    """Comprehensive validation of aggregated dataset"""
    df = pd.read_csv(csv_path, parse_dates=['date'])

    print("="*70)
    print("COMPREHENSIVE DATASET VALIDATION")
    print("="*70)

    # 1. Coverage validation
    expected_start = "2008-01-01"
    expected_end = "2026-02-06"
    date_range = pd.date_range(expected_start, expected_end)
    coverage_pct = len(df) / len(date_range)
    min_coverage = TODO  # What % coverage is acceptable? (suggest 0.95 = 95%)

    print(f"\n📅 Date Coverage:")
    print(f"   Expected: {len(date_range):,} days ({expected_start} to {expected_end})")
    print(f"   Actual: {len(df):,} days")
    print(f"   Coverage: {coverage_pct:.1%}")
    if coverage_pct < min_coverage:
        print(f"   ❌ FAIL: Coverage below {min_coverage:.0%}")
    else:
        print(f"   ✅ PASS")

    # 2. Crisis period validation
    crisis_periods = {
        "2008 Financial Crisis": ("2008-09-15", "2009-03-09"),
        "COVID-19 Pandemic": ("2020-02-24", "2020-04-15"),
        "GameStop Squeeze": ("2021-01-13", "2021-02-05")
    }

    print(f"\n🚨 Crisis Period Coverage:")
    for name, (start, end) in crisis_periods.items():
        period_df = df[(df['date'] >= start) & (df['date'] <= end)]
        expected_days = len(pd.date_range(start, end))
        crisis_coverage = len(period_df) / expected_days
        avg_volume = period_df['volume'].mean()

        min_crisis_volume = TODO  # Minimum texts/day during crisis (suggest higher, e.g., 200)

        print(f"   {name}:")
        print(f"      Days: {len(period_df)}/{expected_days} ({crisis_coverage:.1%})")
        print(f"      Avg volume: {avg_volume:.0f} texts/day")
        if crisis_coverage < 0.90 or avg_volume < min_crisis_volume:
            print(f"      ❌ FAIL: Insufficient crisis coverage or volume")
        else:
            print(f"      ✅ PASS")

    # 3. Statistical distribution checks
    print(f"\n📊 Statistical Properties:")

    # Sentiment distribution
    sentiment_cols = [c for c in df.columns if '_sentiment' in c and c != 'ensemble_sentiment']
    for col in sentiment_cols:
        mean_sent = df[col].mean()
        std_sent = df[col].std()
        # TODO: Define expected ranges for each model
        # FinBERT on financial text is often slightly negative (-0.1 to 0.0)
        # VADER tends to be slightly positive (0.0 to 0.1)
        print(f"   {col}: μ={mean_sent:.3f}, σ={std_sent:.3f}")

    # Volume distribution
    print(f"\n   Volume statistics:")
    print(f"      Mean: {df['volume'].mean():.0f}")
    print(f"      Median: {df['volume'].median():.0f}")
    print(f"      Std: {df['volume'].std():.0f}")
    print(f"      Min: {df['volume'].min():.0f}")
    print(f"      Max: {df['volume'].max():.0f}")

    # 4. Outlier detection
    # TODO: Define outlier thresholds for your domain
    # Z-score method for sentiment
    from scipy import stats
    for col in sentiment_cols:
        z_scores = np.abs(stats.zscore(df[col]))
        outlier_threshold = TODO  # Z-score threshold (suggest 3.0)
        outliers = (z_scores > outlier_threshold).sum()
        print(f"\n   {col} outliers (|z| > {outlier_threshold}): {outliers} ({outliers/len(df):.2%})")

    print("="*70)

    return df
```

### Validation Checklist

**After Phase 1 (Collection):**

- [ ] All 72 quarter files created
- [ ] Each quarter has minimum viable volume
- [ ] No major date gaps within quarters
- [ ] Text quality checks pass
- [ ] Source distribution is balanced

**After Phase 2 (Sentiment Processing):**

- [ ] All 72 daily batch files created
- [ ] Sentiment values in valid ranges
- [ ] Model agreement within acceptable bounds
- [ ] Volume matches raw data collection
- [ ] No systematic processing failures

**After Phase 3 (Aggregation):**

- [ ] Overall coverage meets minimum threshold
- [ ] All crisis periods well-covered
- [ ] Statistical distributions look reasonable
- [ ] No major outliers requiring investigation
- [ ] Ready for GARCH-MIDAS and regime classification

**After Phase 3.5 (GARCH-MIDAS):**

- [ ] Volatility forecasts generated for all dates
- [ ] GARCH parameters converged successfully
- [ ] Long-run and short-run components separated
- [ ] Forecasts align with known volatile periods

**After Phase 3.6 (Regime Classification):**

- [ ] Regime predictions for all dates
- [ ] Regime distribution looks reasonable (not all one class)
- [ ] Crisis indicators align with known crises
- [ ] Feature importance makes economic sense

---

## ⚙️ Resource Optimization

### Philosophy: Balance Speed, Cost, and Reliability

Resource allocation is a three-way trade-off:
- **More resources** → Faster completion BUT higher cost
- **Aggressive settings** → Better throughput BUT risk of failures (OOM, timeouts)
- **Conservative settings** → High reliability BUT longer runtime

### Optimization Guidelines by Phase

#### Phase 1: Collection (CPU-Bound)

**Current Configuration:**
```bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=48:00:00
```

**Tuning Considerations:**

| Parameter | Conservative | Balanced (Current) | Aggressive | Trade-off |
|-----------|-------------|-------------------|-----------|-----------|
| CPUs | 4 | 8 | 16 | More CPUs = faster API calls, but diminishing returns due to rate limits |
| Memory | 8G | 16G | 32G | API collection is memory-light; 16G is plenty |
| Time Limit | 72h | 48h | 24h | Shorter limits fail if collection is slow; checkpoints enable resume |
| Array Throttle | %10 | %36 | %72 | Lower % reduces API rate limit issues but takes longer |

**Recommended Adjustments:**

```bash
# For faster collection (if no rate limit issues):
#SBATCH --cpus-per-task=8       # Keep at 8 (sweet spot)
#SBATCH --mem=16G                # Keep at 16G (sufficient)
#SBATCH --time=48:00:00          # Keep at 48h (safe buffer)
#SBATCH --array=0-71%36          # 50% parallelism (balance speed/rate limits)

# For maximum reliability (if hitting rate limits):
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=72:00:00          # Extra time buffer
#SBATCH --array=0-71%15          # Lower parallelism (fewer API conflicts)
```

#### Phase 2: Sentiment Processing (GPU-Bound)

**Current Configuration:**
```bash
#SBATCH --partition=a100
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=12:00:00
```

**Critical Parameter: Batch Size**

Batch size is the single most important performance knob for GPU workloads:

| Batch Size | Throughput (texts/sec) | Memory Usage | Failure Risk | Use Case |
|------------|----------------------|--------------|--------------|----------|
| 16 | ~30 | ~12 GB | Very Low | Maximum reliability, very long texts |
| 32 | ~60 | ~20 GB | Low | Conservative, safe default |
| 64 | ~100 | ~35 GB | Medium | **Current setting** - good balance |
| 128 | ~150 | ~60 GB | High | Aggressive, short texts only |
| 256 | ~180 | OOM | Very High | Will likely fail |

**Memory Calculation:**
```
GPU Memory = Model Size + (Batch Size × Text Length × Hidden Dim)

FinBERT-base: ~500 MB model
Per-batch overhead: ~400 MB per text (max length 512 tokens)

Safe batch size = (GPU Memory - Model Size - 5GB buffer) / (400 MB × avg_text_length_ratio)

For A100 (40GB):
  Batch 64: ~28 GB (safe)
  Batch 128: ~55 GB (risky)
```

**Tuning Strategy:**

```python
# In scripts/hpc/process_sentiment_batch.py

# Option 1: Fixed conservative batch size
BATCH_SIZE = 32  # Safe for all text lengths

# Option 2: Dynamic batch sizing (RECOMMENDED)
def get_optimal_batch_size(texts, gpu_memory_gb=40):
    """Calculate safe batch size based on text lengths"""
    avg_length = np.mean([len(t.split()) for t in texts[:100]])  # Sample

    if avg_length < 100:
        return 128  # Short texts
    elif avg_length < 200:
        return 64   # Medium texts (most financial content)
    else:
        return 32   # Long texts

# Option 3: Adaptive batch size with OOM recovery
def process_with_adaptive_batch(texts, initial_batch_size=64):
    """Try batch_size, halve on OOM, retry"""
    batch_size = initial_batch_size

    while batch_size >= 8:
        try:
            return model.predict(texts, batch_size=batch_size)
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                torch.cuda.empty_cache()
                batch_size //= 2
                print(f"OOM detected, reducing to batch_size={batch_size}")
            else:
                raise

    raise RuntimeError("Cannot process even with batch_size=8")
```

**Hardware Selection:**

| GPU Type | Memory | Speed | Cost Multiplier | Best For |
|----------|--------|-------|----------------|----------|
| V100 | 16 GB | 1.0x | 1.0x | Small batches, budget-constrained |
| A100 | 40 GB | 2.5x | 2.0x | **Recommended** - large batches, fast |
| A100-80GB | 80 GB | 2.5x | 3.0x | Very large batches, overkill for this task |

**Recommendation:** Stick with A100 40GB - best price/performance for this workload.

#### Phase 3.5: GARCH-MIDAS (CPU-Bound, Memory-Intensive)

**Current Configuration:**
```bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=02:00:00
```

**Tuning Considerations:**

GARCH-MIDAS is single-threaded for optimization but multi-threaded for matrix operations:

| CPUs | Memory | Time | Notes |
|------|--------|------|-------|
| 8 | 16G | 3h | Might struggle with large datasets |
| 16 | 32G | 2h | **Current** - good balance |
| 32 | 64G | 1.5h | Diminishing returns, more isn't always better |

**Memory Usage:**
- Base model: ~2 GB
- Per date of data: ~50 MB
- 6,575 days × 50 MB = ~330 MB data
- Matrix operations: ~5-10 GB peak
- **Recommendation: 32 GB is comfortable**

#### Phase 3.6: Regime Classification (CPU-Bound)

**Current Configuration:**
```bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=01:00:00
```

This is well-configured. Statistical jump model is fast and memory-light.

### Parallelism Tuning

**Array Job Throttling:**

Control how many jobs run simultaneously with `--array=START-END%LIMIT`:

```bash
# Examples:
--array=0-71%5    # Max 5 concurrent (slowest, safest for API rate limits)
--array=0-71%10   # Max 10 concurrent (conservative)
--array=0-71%20   # Max 20 concurrent (moderate)
--array=0-71%36   # Max 36 concurrent (half capacity, good balance)
--array=0-71      # All 72 at once (fastest, highest risk of rate limits)
```

**Decision Matrix:**

| Scenario | Parallelism | Reasoning |
|----------|-------------|-----------|
| First run, testing | %5 | Validate configuration before full run |
| Production, stable APIs | %36 | Balance speed and reliability |
| Retry after failures | %10 | Conservative to avoid repeating issues |
| Crisis (deadline approaching) | %72 | Maximum speed, accept some failures |

### Cost Optimization

**Scenario: Reduce cost by 30% with minimal time increase**

```bash
# Phase 1: Collection
# Original: 72 jobs × 48h = 3,456 node-hours
# Optimized: Reduce parallelism, let it run longer
--array=0-71%20  # Instead of %36
# Time: 3-4 days instead of 2-3 days
# Cost: ~30% reduction (fewer concurrent nodes)

# Phase 2: Sentiment
# Original: A100 GPUs for 12h × 72 jobs
# Optimized: Use V100 instead
#SBATCH --partition=gpu-v100
#SBATCH --gres=gpu:1
BATCH_SIZE=32  # Smaller due to less memory
# Time: ~18h instead of 12h per job
# Cost: 50% cheaper, +50% time (net savings)
```

**Scenario: Reduce time by 30% accepting higher cost**

```bash
# Phase 2: Sentiment
# Use larger batches and more parallelism
BATCH_SIZE=128  # Aggressive
--array=0-71     # All at once (no throttling)
# Time: ~8h instead of 12h per job
# Cost: ~30% higher (more GPU hours, more failures to retry)
```

### Performance Monitoring

Track resource utilization to optimize future runs:

```bash
# During job execution, monitor GPU usage
srun --account=jcheun_ds6210_1262_401_0001 --partition=gpu-dev --gres=gpu:1 --jobid=JOBID nvidia-smi

# After job completes, check efficiency
sacct -j JOBID --format=JobID,JobName,Partition,AllocCPUS,ReqMem,MaxRSS,Elapsed,State

# GPU utilization in job output
grep "GPU Utilization" logs/process_*.out
```

**Red Flags:**
- GPU utilization < 60% → Batch size too small, CPU bottleneck
- Memory usage > 90% → Risk of OOM, reduce batch size
- CPU utilization < 50% → Over-allocated CPUs

### Recommended Configuration Summary

**For balanced speed/cost/reliability (most users):**

```bash
# Collection (Phase 1)
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=48:00:00
#SBATCH --array=0-71%36

# Sentiment (Phase 2)
#SBATCH --account=jcheun_ds6210_1262_401_0001
#SBATCH --partition=gpu-dev
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=18:00:00
#SBATCH --array=0-71%36
# BATCH_SIZE=64 (dynamic adjustment in code)

# GARCH-MIDAS (Phase 3.5)
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --time=02:00:00

# Regime Classification (Phase 3.6)
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=01:00:00
```

---

## 📊 Cost Estimation

### Compute Hours

- **Collection:** 72 jobs × 24h × 8 CPU = 13,824 CPU-hours
- **Sentiment Processing:** 72 jobs × 12h × (1 A100 + 8 CPU) = ~864 GPU-hours
- **GARCH-MIDAS:** 1 job × 2h × 16 CPU = 32 CPU-hours
- **Regime Classification:** 1 job × 1h × 16 CPU = 16 CPU-hours
- **Total:** ~13,872 CPU-hours + 864 GPU-hours

### Estimated Time

- **Wall time (parallel):** 5-7 days total
  - Phase 1 (Collection): 2-3 days
  - Phase 2 (Sentiment): 1-2 days (parallel with collection tail-end)
  - Phase 3 (Aggregation): 1 hour
  - Phase 3.5 (GARCH-MIDAS): 2 hours
  - Phase 3.6 (Regime Classification): 1 hour
  - Phase 4 (Backtests): 2 days
- **Sequential (if needed):** ~30-45 days

---

## 📊 Monitoring & Observability

### Real-Time Job Monitoring

#### Quick Status Check

```bash
# Check running jobs
squeue -u jarocha

# Detailed view with resource usage
squeue -u jarocha --format="%.18i %.9P %.30j %.8T %.10M %.6D %.4C %.8m"
# Shows: JobID, Partition, Name, State, Time, Nodes, CPUs, Memory

# Watch status (auto-refresh every 30 seconds)
watch -n 30 'squeue -u jarocha'

# Count jobs by state
squeue -u jarocha -h -o "%T" | sort | uniq -c
```

#### Progress Dashboard Script

Create a monitoring dashboard that shows overall progress:

```bash
# scripts/hpc/monitor_progress.sh
#!/bin/bash

PHASE=$1  # collection, sentiment, garch, regime

clear
echo "========================================"
echo "HPC Pipeline Progress Dashboard"
echo "Phase: $PHASE"
echo "Timestamp: $(date)"
echo "========================================"
echo ""

# Job status
echo "📊 Job Status:"
squeue -u jarocha -h -o "%T" | sort | uniq -c | while read count state; do
  case $state in
    RUNNING)   echo "  🟢 Running:    $count" ;;
    PENDING)   echo "  🟡 Pending:    $count" ;;
    COMPLETED) echo "  ✅ Completed:  $count" ;;
    FAILED)    echo "  ❌ Failed:     $count" ;;
    TIMEOUT)   echo "  ⏱️  Timeout:    $count" ;;
    *)         echo "  ⚪ $state:     $count" ;;
  esac
done

total_jobs=$(squeue -u jarocha -h | wc -l)
echo "  📈 Total active: $total_jobs"
echo ""

# File output progress
case $PHASE in
  collection)
    output_dir="/scratch/users/jarocha/sentiment_regime_data/raw_data"
    expected_files=72
    pattern="*.parquet"
    ;;
  sentiment)
    output_dir="/scratch/users/jarocha/sentiment_regime_data/sentiment_results"
    expected_files=72
    pattern="daily_batch_*.csv"
    ;;
  garch)
    output_dir="/scratch/users/jarocha/sentiment_regime_data"
    expected_files=1
    pattern="volatility_forecasts.csv"
    ;;
  regime)
    output_dir="/scratch/users/jarocha/sentiment_regime_data"
    expected_files=1
    pattern="regime_predictions.csv"
    ;;
esac

if [ -d "$output_dir" ]; then
  completed_files=$(find "$output_dir" -name "$pattern" 2>/dev/null | wc -l)
  percent=$((completed_files * 100 / expected_files))

  echo "📁 Output Files:"
  echo "  Completed: $completed_files / $expected_files ($percent%)"

  # Progress bar
  bar_length=40
  filled=$((completed_files * bar_length / expected_files))
  empty=$((bar_length - filled))
  bar=$(printf "%${filled}s" | tr ' ' '█')
  bar+=$(printf "%${empty}s" | tr ' ' '░')
  echo "  [$bar] $percent%"
fi

echo ""

# Disk usage
echo "💾 Disk Usage:"
du -sh "$output_dir" 2>/dev/null | awk '{print "  Data: " $1}'
du -sh logs 2>/dev/null | awk '{print "  Logs: " $1}'
df -h /scratch/users/jarocha | tail -1 | awk '{print "  Free: " $4 " (" $5 " used)"}'

echo ""

# Recent errors (last 5)
echo "⚠️  Recent Errors:"
recent_errors=$(grep -i "error\|fail" logs/*.err 2>/dev/null | tail -5)
if [ -n "$recent_errors" ]; then
  echo "$recent_errors" | while read line; do
    echo "  ${line:0:80}"
  done
else
  echo "  None in recent logs"
fi

echo ""
echo "========================================"
echo "Commands:"
echo "  Detailed errors: bash scripts/hpc/detect_failures.sh $PHASE"
echo "  Check logs:      tail -f logs/${PHASE}_*.out"
echo "  GPU status:      srun --account=jcheun_ds6210_1262_401_0001 --partition=gpu-dev --gres=gpu:1 --mem=4G nvidia-smi"
echo "========================================"
```

**Usage:**
```bash
# Run once
bash scripts/hpc/monitor_progress.sh collection

# Auto-refresh every 60 seconds
watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'
```

### Performance Metrics

#### Track Processing Speed

```bash
# For sentiment processing, track texts/second
# Add to scripts/hpc/process_sentiment_batch.py:

import time
from datetime import datetime

start_time = time.time()
texts_processed = 0

for batch in batches:
    results = model.predict(batch)
    texts_processed += len(batch)

    # Log progress every 100 batches
    if texts_processed % (100 * BATCH_SIZE) == 0:
        elapsed = time.time() - start_time
        rate = texts_processed / elapsed
        eta_seconds = (total_texts - texts_processed) / rate
        eta_hours = eta_seconds / 3600

        print(f"Progress: {texts_processed}/{total_texts} texts")
        print(f"Rate: {rate:.1f} texts/sec")
        print(f"ETA: {eta_hours:.1f} hours")
```

#### GPU Utilization Monitoring

```bash
# Check GPU usage on running job
squeue -u jarocha -p gpu-dev -h -o "%A" | while read jobid; do
  echo "Job $jobid GPU stats:"
  srun --account=jcheun_ds6210_1262_401_0001 --jobid=$jobid nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total --format=csv
done

# Or monitor specific GPU node
ssh gpu-nodeXX  # Replace XX with node number
nvidia-smi -l 5  # Refresh every 5 seconds
```

### Alerting & Notifications

#### Email Alerts for Critical Events

```python
# Add to scripts/hpc/utils/notify.py (already created in error handling section)

# Example usage in job scripts:
from scripts.hpc.utils.notify import send_alert

# Alert on job start
send_alert(
    subject=f"Batch {batch_id} started",
    body=f"Processing quarter {quarter} on {hostname}",
    severity="INFO"
)

# Alert on completion
send_alert(
    subject=f"Batch {batch_id} completed",
    body=f"Processed {num_texts} texts in {elapsed:.1f} hours",
    severity="INFO"
)

# Alert on failure (automatic via error handling)
try:
    process_batch(batch_id)
except Exception as e:
    send_alert(
        subject=f"URGENT: Batch {batch_id} failed",
        body=f"Error: {e}\n\nCheck logs/process_{batch_id}.err",
        severity="CRITICAL"
    )
    raise
```

#### Slack/Discord Webhooks (Optional)

```python
# scripts/hpc/utils/webhook_notify.py
import requests
import os

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # Set in environment

def send_webhook(message, level="info"):
    """Send notification to Slack/Discord"""
    if not WEBHOOK_URL:
        return

    colors = {
        "info": "#36a64f",     # Green
        "warning": "#ff9900",  # Orange
        "error": "#ff0000"     # Red
    }

    payload = {
        "text": message,
        "color": colors.get(level, "#808080")
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Webhook notification failed: {e}")

# Usage:
send_webhook("🚀 Collection phase started - 72 jobs queued", "info")
send_webhook("⚠️ 5 batches failed, retrying...", "warning")
send_webhook("✅ All 72 batches completed successfully!", "info")
```

### Log Management

#### Centralized Log Viewing

```bash
# View all outputs in real-time (dangerous with many jobs!)
tail -f logs/*.out

# View errors only
tail -f logs/*.err

# Search for specific patterns across all logs
grep -i "error" logs/*.err | grep -v "No error"
grep -i "complete" logs/*.out | wc -l  # Count completions

# Find slowest jobs (by runtime)
for log in logs/collect_*.out; do
  runtime=$(grep "Elapsed" $log | tail -1 | awk '{print $2}')
  echo "$log: $runtime"
done | sort -k2 -rh | head -10
```

#### Log Rotation and Archiving

```bash
# Archive old logs before new run
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p logs/archive
tar -czf logs/archive/logs_${timestamp}.tar.gz logs/*.out logs/*.err
rm logs/*.out logs/*.err

# Or use SLURM's automatic log management
#SBATCH --output=logs/run_%x_%A_%a.out  # %x=job name, %A=array job ID, %a=task ID
#SBATCH --error=logs/run_%x_%A_%a.err
```

### Historical Performance Analysis

#### Post-Run Analysis Script

```python
# scripts/hpc/analyze_run_performance.py
import pandas as pd
import subprocess
import re
from pathlib import Path

def analyze_slurm_jobs(job_array_id):
    """Analyze performance of completed job array"""

    # Get job statistics from SLURM
    cmd = f"sacct -j {job_array_id} --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize,AveCPU -P"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)

    # Parse output
    lines = result.stdout.strip().split('\n')
    header = lines[0].split('|')

    data = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = line.split('|')
        data.append(dict(zip(header, values)))

    df = pd.DataFrame(data)

    # Analysis
    print("="*70)
    print("SLURM Job Array Performance Analysis")
    print("="*70)
    print(f"\nJob Array ID: {job_array_id}")
    print(f"Total tasks: {len(df)}")
    print(f"\nState breakdown:")
    print(df['State'].value_counts())

    # Convert elapsed time to seconds
    def parse_elapsed(elapsed_str):
        # Format: [DD-]HH:MM:SS
        parts = elapsed_str.split('-')
        if len(parts) == 2:
            days, time = parts
            days = int(days)
        else:
            days = 0
            time = parts[0]

        h, m, s = map(int, time.split(':'))
        return days * 86400 + h * 3600 + m * 60 + s

    df['elapsed_seconds'] = df['Elapsed'].apply(parse_elapsed)

    print(f"\nRuntime statistics:")
    print(f"  Mean: {df['elapsed_seconds'].mean() / 3600:.2f} hours")
    print(f"  Median: {df['elapsed_seconds'].median() / 3600:.2f} hours")
    print(f"  Min: {df['elapsed_seconds'].min() / 3600:.2f} hours")
    print(f"  Max: {df['elapsed_seconds'].max() / 3600:.2f} hours")

    # Identify outliers
    mean = df['elapsed_seconds'].mean()
    std = df['elapsed_seconds'].std()
    outliers = df[df['elapsed_seconds'] > mean + 2*std]

    if len(outliers) > 0:
        print(f"\n⚠️  Outliers (>2 std dev from mean):")
        for _, row in outliers.iterrows():
            print(f"  {row['JobID']}: {row['elapsed_seconds']/3600:.2f} hours")

    print("="*70)

    return df

# Usage:
# python scripts/hpc/analyze_run_performance.py --job-id 12345
```

### Monitoring Checklist

**Daily checks (5 minutes):**
- [ ] Run progress dashboard: `bash scripts/hpc/monitor_progress.sh <phase>`
- [ ] Check for new errors: `grep -i "error" logs/*.err | tail -20`
- [ ] Verify disk space: `df -h /scratch/users/jarocha`
- [ ] Check job queue: `squeue -u jarocha`

**Weekly checks (15 minutes):**
- [ ] Run failure detection: `bash scripts/hpc/detect_failures.sh <phase>`
- [ ] Archive old logs: `tar -czf logs_backup.tar.gz logs/`
- [ ] Check validation results: `python scripts/hpc/validate_pipeline_phase.py ...`
- [ ] Review performance metrics: `python scripts/hpc/analyze_run_performance.py`

**After each phase completion:**
- [ ] Run comprehensive validation
- [ ] Archive phase logs
- [ ] Document any issues and resolutions
- [ ] Update resource estimates for future runs

### Monitoring Tools Summary

| Tool | Purpose | When to Use | Update Frequency |
|------|---------|-------------|------------------|
| `squeue` | Job status | Check if jobs running/pending/complete | Real-time |
| `monitor_progress.sh` | Overall progress | Daily check on pipeline progress | Every 60s with `watch` |
| `detect_failures.sh` | Find failures | After jobs complete or on errors | After each batch |
| `validate_pipeline_phase.py` | Data quality | After phase completes | Once per phase |
| `analyze_run_performance.py` | Historical analysis | After phase completes | Once per phase |
| `nvidia-smi` | GPU utilization | Check GPU efficiency | Real-time |
| `df -h` | Disk space | Ensure enough space | Daily |
| Log files | Detailed debugging | When specific job fails | As needed |

---

## 🚨 Error Handling & Recovery

### Philosophy: Fail Fast, Recover Automatically, Preserve Progress

With 72 parallel jobs running for days, failures are inevitable. The key is:
1. **Checkpoint progress** - Never lose work
2. **Automatic retry** - Recover from transient failures
3. **Smart detection** - Know what failed and why
4. **Manual fallback** - Clear recovery steps when automation fails

### Quick Failure Detection

```bash
# Check which jobs are still running
squeue -u jarocha

# Detect failed batches automatically
bash scripts/hpc/detect_failures.sh collection  # or sentiment, garch, regime

# Check specific job log
cat logs/collect_JOBID_TASKID.err

# View all errors across logs
grep -i "error\|fail" logs/*.err | head -20
```

### Common Failure Modes & Solutions

#### 1. API Rate Limits (Collection Phase)

**Symptoms:** HTTP 429 errors, "rate limit exceeded"

**Why it happens:** GDELT/Reddit throttle requests when too many come too fast

**Automatic recovery:** Built-in exponential backoff retries

**Manual recovery if needed:**
```bash
# Check which batches hit rate limits
grep "429\|rate limit" logs/collect_*.err

# Reduce parallelism and retry (max 10 concurrent instead of 72)
sbatch --array=0-71%10 scripts/hpc/run_collection_retry.sh

# Or increase delays in collection script
nano scripts/hpc/collect_batch.py
# Increase: RATE_LIMIT_DELAY = 2.0  # seconds between requests
```

#### 2. GPU Out of Memory (Sentiment Phase)

**Symptoms:** "CUDA out of memory", job killed, batch incomplete

**Why it happens:** Batch size too large for GPU memory, or long texts exceed capacity

**Automatic recovery:** Dynamic batch size reduction built into processing script

**Manual recovery if needed:**
```bash
# Check for OOM errors
grep -i "out of memory\|OOM" logs/process_*.err

# Reduce batch size permanently
nano scripts/hpc/process_sentiment_batch.py
# Change: BATCH_SIZE = 32  # Was 64

# Clear GPU cache and retry
sbatch --array=FAILED_BATCH_IDS scripts/hpc/run_sentiment_retry.sh
```

#### 3. Disk Space Issues

**Symptoms:** "No space left on device", write failures

**Why it happens:** `/scratch` quota exceeded, temp files accumulating

**Check disk usage:**
```bash
# Check current usage and quota
df -h /scratch/users/jarocha
du -sh /scratch/users/jarocha/*

# Find large temporary files
find /scratch/users/jarocha -name "*.tmp" -exec ls -lh {} \; | sort -k 5 -hr | head -20
```

**Recovery:**
```bash
# Clean up temporary files (older than 1 day)
find /scratch/users/jarocha -name "*.tmp" -mtime +1 -delete
find /scratch/users/jarocha -name "*cache*" -mtime +7 -delete

# Archive old logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/*.out logs/*.err
rm logs/*.out logs/*.err

# Move processed data to long-term storage if needed
# (after validation passes)
```

#### 4. Network Timeouts

**Symptoms:** "Connection timeout", "Read timeout", incomplete downloads

**Why it happens:** Network congestion, API server issues, firewall problems

**Automatic recovery:** Built-in retry logic with backoff

**Manual recovery:**
```bash
# Test network connectivity
ping -c 3 api.gdelt.org
curl -I https://www.reddit.com/r/all.json

# Check for network issues in logs
grep -i "timeout\|connection" logs/collect_*.err

# Retry with increased timeout
sbatch --array=FAILED_BATCH_IDS \
  --export=TIMEOUT=60 \  # seconds (default 30)
  scripts/hpc/run_collection_retry.sh
```

#### 5. Job Time Limit Exceeded

**Symptoms:** SLURM "TIME LIMIT" in error log, job terminated early

**Why it happens:** Job took longer than allocated time (48h for collection, 12h for sentiment)

**Recovery:**
```bash
# Jobs will resume from checkpoint automatically
# Check checkpoint status
ls -lh logs/checkpoint_batch_*.json

# If needed, increase time limit
nano scripts/hpc/run_collection_retry.sh
# Change: #SBATCH --time=72:00:00  # Was 48:00:00

# Resubmit with longer time
sbatch --array=FAILED_BATCH_IDS scripts/hpc/run_collection_retry.sh
```

#### 6. Missing Dependencies / Import Errors

**Symptoms:** "ModuleNotFoundError", "ImportError"

**Why it happens:** Virtual environment not activated, packages not installed, wrong Python version

**Recovery:**
```bash
# Verify environment
module load python/3.11
source venv/bin/activate
python --version  # Should be 3.11.x

# Check installed packages
pip list | grep -E "transformers|torch|pandas"

# Reinstall if needed
pip install -r requirements.txt --force-reinstall
pip install datasets transformers torch --extra-index-url https://download.pytorch.org/whl/cu121
```

### Automated Recovery Workflow

**After each phase, validate and auto-retry:**

```bash
# Run this after collection completes
python scripts/hpc/validate_pipeline_phase.py \
  --phase collection \
  --path /scratch/users/jarocha/sentiment_regime_data/raw_data

# If validation fails, detect and retry automatically
if [ $? -ne 0 ]; then
  echo "Validation failed, detecting failures..."
  bash scripts/hpc/detect_failures.sh collection

  # Get failed batch IDs
  failed_batches=$(bash scripts/hpc/detect_failures.sh collection | \
    grep "Failed batch IDs:" | cut -d: -f2 | tr -d ' ')

  if [ -n "$failed_batches" ]; then
    echo "Retrying batches: $failed_batches"
    sbatch --array=$failed_batches scripts/hpc/run_collection_retry.sh
  fi
fi
```

### Troubleshooting Decision Tree

```
Job Failed?
│
├─ Check logs: cat logs/JOBNAME_*.err
│
├─ API Error (429, timeout)?
│  └─ Reduce parallelism, increase delays, retry
│
├─ GPU OOM?
│  └─ Reduce batch size, retry
│
├─ Disk full?
│  └─ Clean temp files, archive logs, retry
│
├─ Time limit?
│  └─ Checkpoint exists? Resume with longer time
│
├─ Import error?
│  └─ Check environment, reinstall packages
│
└─ Unknown error?
   └─ Check full logs, contact HPC support (hpc@smu.edu)
```

### Emergency: Cancel All Jobs

```bash
# Cancel all your running jobs
scancel -u jarocha

# Cancel specific job array
scancel JOBID

# Cancel only running jobs from specific batch
squeue -u jarocha -h -o "%A" | xargs -n 1 scancel
```

### Monitoring Job Health

```bash
# Check job status summary
squeue -u jarocha --format="%.18i %.9P %.30j %.8T %.10M %.6D"

# Watch job progress (refresh every 30 seconds)
watch -n 30 'squeue -u jarocha'

# Count successful completions
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l
# Should be 72 for collection phase

# Check average runtime
sacct -u jarocha --format=JobID,JobName,Elapsed,State | grep COMPLETED
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
