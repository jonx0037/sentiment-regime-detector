# HPC Data Collection - Simple Start Guide

**Date:** February 7, 2026
**Goal:** Collect comprehensive historical financial text data for sentiment analysis
**Timeline:** 2-3 days for collection, then 1-2 days for processing

---

## 🎯 What This Does

Collects 18 years of financial text data (2008-2026) from:
- **GDELT**: Global news articles (English only, financial keywords)
- **Reddit**: Posts from financial subreddits (wallstreetbets, stocks, investing)

**Output:** ~50,000-100,000 texts per quarter = ~3-7 million total texts

---

## ✅ Prerequisites Checklist

Run these commands on ManeFrame to verify you're ready:

```bash
# SSH to ManeFrame III
ssh jarocha@m3.smu.edu

# Navigate to project
cd /scratch/users/jarocha/sentiment-detector

# Check Python module
module load python/3.11.11/data_science/2025.08.21
python --version  # Should show 3.11.11

# Activate virtual environment
source venv/bin/activate

# Verify key packages
python -c "import pandas, aiohttp, tqdm; print('✅ Dependencies OK')"

# Create data directories
mkdir -p /scratch/users/jarocha/sentiment_regime_data/{raw_data,sentiment_results}
mkdir -p logs

# Check disk space (need ~50GB free)
df -h /scratch/users/jarocha
```

**If any step fails, stop and fix before continuing.**

---

## 🚀 Phase 1: Test Single Batch First

**Before submitting 72 jobs, test one batch to verify everything works:**

```bash
# Get interactive session
srun --account=jcheun_ds6210_1262_401_0001 \
     --partition=standard-s \
     --cpus-per-task=8 \
     --mem=16G \
     --time=02:00:00 \
     --pty bash

# Load environment
module load python/3.11.11/data_science/2025.08.21
source venv/bin/activate

# Test collection for 2008-Q1 (3 months)
python scripts/hpc/collect_historical_data.py \
    --start-date 2008-01-01 \
    --end-date 2008-03-31 \
    --sources gdelt,reddit \
    --output /scratch/users/jarocha/test_collection \
    --batch-id 999

# Check results
ls -lh /scratch/users/jarocha/test_collection/
# Should see:
#   reddit_batch_0999.parquet (should be 1-10 MB)
#   combined_batch_0999.parquet (should be 5-20 MB)

# Verify data quality
python << 'EOF'
import pandas as pd
df = pd.read_parquet("/scratch/users/jarocha/test_collection/combined_batch_0999.parquet")
print(f"✅ Collected {len(df):,} texts")
print(f"✅ Date range: {df['date'].min()} to {df['date'].max()}")
print(f"✅ Sources: {df['source'].value_counts().to_dict()}")
EOF

# Exit interactive session
exit
```

**✅ Success Criteria:**
- Script completed without errors
- 2 parquet files created
- Files are 5-20 MB (not KB)
- DataFrame shows thousands of texts
- Both GDELT and Reddit data present

**❌ If test fails, do NOT proceed to full submission. Debug first.**

---

## 🚀 Phase 2: Full Collection (72 Quarters)

**Only proceed if test batch succeeded.**

```bash
# Clean up test data
rm -rf /scratch/users/jarocha/test_collection

# Submit array job (72 quarters, max 36 concurrent)
sbatch scripts/hpc/collect_historical_array.sh

# Note the job ID from output
# Example: "Submitted batch job 123456"
```

**Monitor progress:**

```bash
# Real-time dashboard (updates every 60 seconds)
watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'

# Or check manually
squeue -u jarocha

# Check log files
tail -f logs/collect_*.out
tail -f logs/collect_*.err

# Count completed files
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l
# Target: 144 files (72 reddit + 72 combined)
```

**Expected Timeline:**
- First 36 jobs start immediately
- Remaining 36 jobs wait in queue
- Each job takes 2-12 hours (depends on API response times)
- **Total: 2-3 days** for all 72 quarters

---

## 🔍 During Collection: What to Check

**Every few hours:**

```bash
# Quick status
squeue -u jarocha
# Look for: RUNNING, PENDING, or COMPLETED

# Check for errors
grep -i "error" logs/collect_*.err | tail -20

# Disk space
df -h /scratch/users/jarocha

# Count completions
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l
```

**If you see issues:**

```bash
# API rate limits (HTTP 429)
# → Normal, built-in retry handles this

# Timeout errors
# → Some API calls are slow, retry handles this

# Disk full
# → Clean up old logs: tar -czf logs_backup.tar.gz logs/*.{out,err} && rm logs/*.{out,err}

# Jobs failing
bash scripts/hpc/detect_failures.sh collection
# Will show which batches failed and suggest retry command
```

---

## ✅ Phase 3: Validation

**After collection completes (all 72 jobs done):**

```bash
# Count files
file_count=$(ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l)
echo "Collected $file_count / 144 files"

# Run validation
python scripts/hpc/validate_pipeline_phase.py \
    --phase collection \
    --path /scratch/users/jarocha/sentiment_regime_data/raw_data

# Check a sample batch
python << 'EOF'
import pandas as pd
import glob

files = sorted(glob.glob("/scratch/users/jarocha/sentiment_regime_data/raw_data/combined_batch_*.parquet"))

print(f"Total files: {len(files)}")
print("\nSample of first 3 batches:")

for f in files[:3]:
    df = pd.read_parquet(f)
    print(f"  {f.split('/')[-1]}: {len(df):,} texts, {df['date'].min()} to {df['date'].max()}")

# Check total volume
total_texts = sum(len(pd.read_parquet(f)) for f in files)
print(f"\n✅ Total texts collected: {total_texts:,}")
print(f"✅ Average per batch: {total_texts / len(files):,.0f}")
EOF
```

**✅ Success Criteria:**
- 144 files present (or 72 if reddit batches failed)
- Files are MB range, not KB
- Total texts > 1 million
- Validation script passes all checks

---

## 🚨 Common Issues & Fixes

### Issue: Jobs complete instantly (seconds) with ExitCode 0

**Cause:** Python script error not caught by SLURM

**Fix:**
```bash
# Check error log
cat logs/collect_*.err | head -50
# Look for: "unrecognized arguments", "ImportError", etc.

# Common causes:
# 1. Missing dependency → pip install <package>
# 2. Python path issue → check sys.path in script
# 3. Module not loaded → module load python/3.11.11/data_science/2025.08.21
```

### Issue: File sizes are tiny (KB instead of MB)

**Cause:** API returning empty results or wrong language

**Check:**
```bash
# Test GDELT API manually
curl "https://api.gdeltproject.org/api/v2/doc/doc?query=sourcelang:english%20(stock%20market)&mode=artlist&maxrecords=10&format=json&startdatetime=20190101000000&enddatetime=20190101235959"

# Should see English articles in response
```

### Issue: Many HTTP 429 (rate limit) errors

**Fix:**
```bash
# Reduce parallelism
scancel -u jarocha  # Cancel current jobs
sbatch --array=0-71%10 scripts/hpc/collect_historical_array.sh  # Only 10 concurrent
```

### Issue: Jobs timeout after 24 hours

**Expected:** Some quarters may have lots of data

**Fix:**
```bash
# Detect which batches timed out
bash scripts/hpc/detect_failures.sh collection

# Resubmit just those batches
# Script will suggest command like:
sbatch --array=5,12,23,45 scripts/hpc/collect_historical_array.sh
```

---

## 📊 Next Steps After Collection Success

Once you have validated data collection:

1. **Archive raw data** (optional but recommended):
   ```bash
   cd /scratch/users/jarocha/sentiment_regime_data
   tar -czf raw_data_backup_$(date +%Y%m%d).tar.gz raw_data/
   ```

2. **Proceed to sentiment processing** (Phase 2):
   ```bash
   sbatch scripts/hpc/run_sentiment_processing.sh
   ```

3. **Monitor sentiment processing**:
   ```bash
   watch -n 60 'bash scripts/hpc/monitor_progress.sh sentiment'
   ```

---

## 🛟 Help & Support

**If stuck:**

1. Check error logs: `tail -100 logs/collect_*.err`
2. Verify environment: `module list`, `which python`
3. Test manually: Run Python script in interactive session
4. Check HPC status: <https://www.smu.edu/oit/research/hpc-status>

**ManeFrame Issues:**
- HPC Help Desk: <hpc@smu.edu>

**Project Issues:**
- Jonathan Rocha: <jrocha@smu.edu>

---

## 📋 Quick Reference Card

```bash
# Check job status
squeue -u jarocha

# Cancel all jobs
scancel -u jarocha

# Monitor progress
bash scripts/hpc/monitor_progress.sh collection

# Check errors
grep -i error logs/*.err | tail -20

# Count files
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l

# Disk space
df -h /scratch/users/jarocha

# Detect failures
bash scripts/hpc/detect_failures.sh collection

# Validate
python scripts/hpc/validate_pipeline_phase.py --phase collection --path /scratch/users/jarocha/sentiment_regime_data/raw_data
```

---

**Last Updated:** February 7, 2026
**Status:** Simplified, ready to use
**Expected Success Rate:** >90% with proper testing
