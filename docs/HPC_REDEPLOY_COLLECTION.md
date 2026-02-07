# HPC Data Collection - Redeployment Guide

**Date:** February 7, 2026
**Status:** Error #10 Fixed - Ready to redeploy with improved collection

---

## 🔍 What Was Fixed

**Error #9 & #10 Resolution:**

- ✅ Removed unsupported `--checkpoint` parameter
- ✅ Added English language filtering to GDELT
- ✅ Implemented Reddit pagination for more posts
- ✅ Enhanced error logging for debugging

**Expected Results:**

- GDELT: 50-250 English articles/day (was: 0)
- Reddit: 5,000-25,000 posts/quarter (was: ~100)
- File sizes: 5-20 MB per quarter (was: 15-98 KB)

---

## 📋 Deployment Steps

### Step 1: Sync Updated Collection Script

You have two options:

**Option A: Push from local (recommended if you have working git)**

```bash
# On your local machine in project directory
cd ~/Documents/SMU/DS_6210_Capstone

# Stage the updated Python script
git add scripts/hpc/collect_historical_data.py

# Commit the fix
git commit -m "fix: enhance data collection with English filtering and pagination

- Add sourcelang:english filter to GDELT queries
- Implement Reddit pagination to collect 5000+ posts per subreddit
- Add detailed error logging (timeout, network, HTTP status)
- Expected improvement: 50,000-100,000 texts per quarter vs 100 before"

# Push to remote
git push origin main

# SSH to cluster and pull
ssh jarocha@m3.smu.edu
cd /scratch/users/jarocha/sentiment-detector
git pull origin main
```

**Option B: Direct edit on cluster (if git push doesn't work)**

```bash
# SSH to cluster
ssh jarocha@m3.smu.edu
cd /scratch/users/jarocha/sentiment-detector

# Backup current version
cp scripts/hpc/collect_historical_data.py scripts/hpc/collect_historical_data.py.backup

# Use scp to copy from local to cluster
# Run this in a NEW terminal on your LOCAL machine:
scp ~/Documents/SMU/DS_6210_Capstone/scripts/hpc/collect_historical_data.py \
    jarocha@m3.smu.edu:/scratch/users/jarocha/sentiment-detector/scripts/hpc/
```

### Step 2: Clean Up Old Broken Data

```bash
# On ManeFrame (jarocha@m3.smu.edu)
cd /scratch/users/jarocha/sentiment-detector

# Check current data directory
ls -lh /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | head -10

# Archive old broken files (don't delete - might need for debugging)
mkdir -p /scratch/users/jarocha/sentiment_regime_data/old_data_broken
mv /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet \
   /scratch/users/jarocha/sentiment_regime_data/old_data_broken/

# Verify directory is clean
ls /scratch/users/jarocha/sentiment_regime_data/raw_data/
# Should be empty

# Check disk space before starting
df -h /scratch/users/jarocha
```

### Step 3: Resubmit Collection Jobs

```bash
# Still on ManeFrame
cd /scratch/users/jarocha/sentiment-detector

# Archive old logs (optional but recommended)
mkdir -p logs/run_$(date +%Y%m%d_%H%M%S)
mv logs/collect_*.{out,err} logs/run_*/  2>/dev/null || true

# Submit corrected collection jobs
sbatch scripts/hpc/collect_historical_array.sh

# Get job ID (it will show: "Submitted batch job XXXXXX")
# Note this ID for monitoring

# Check job status immediately
squeue -u jarocha

# You should see 36 jobs RUNNING (max concurrent)
```

### Step 4: Monitor Collection Progress

```bash
# Real-time monitoring dashboard (updates every 60 seconds)
watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'

# Or check manually
bash scripts/hpc/monitor_progress.sh collection

# Check specific job log to verify English articles are being collected
# Replace JOBID with your actual job ID from sbatch output
tail -f logs/collect_JOBID_0.out
# Look for lines like:
#   ✓ Collected 150 English GDELT articles (filtered from 1250 total)
#   ✓ Collected 8500 Reddit posts total

# Check for errors
tail -f logs/collect_JOBID_0.err
# Should see progress bars, minimal errors

# Count completed files (updates as jobs finish)
watch -n 60 'ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet 2>/dev/null | wc -l'
# Target: 144 files (72 batches × 2 files: reddit_batch + combined_batch)
```

---

## ✅ Success Criteria

**After Collection Completes (2-3 days):**

1. **File Count:**

   ```bash
   ls /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | wc -l
   # Should show: 144 files (72 reddit + 72 combined)
   ```

2. **File Sizes:**

   ```bash
   ls -lh /scratch/users/jarocha/sentiment_regime_data/raw_data/*.parquet | head -10
   # Should show: Files ranging from 5-20 MB (not 15-98 KB)
   ```

3. **Sample Data Inspection:**

   ```bash
   python3 -c "import pandas as pd; df = pd.read_parquet('/scratch/users/jarocha/sentiment_regime_data/raw_data/combined_batch_0000.parquet'); print(f'Rows: {len(df):,}'); print(f'Columns: {df.columns.tolist()}'); print(df.head())"
   # Should show: 10,000+ rows for a 3-month batch
   ```

4. **No Critical Errors:**

   ```bash
   grep -i "error.*critical\|failed.*collect" logs/collect_*.err | wc -l
   # Should show: 0 or very few
   ```

5. **Validation:**

   ```bash
   python scripts/hpc/validate_pipeline_phase.py \
     --phase collection \
     --path /scratch/users/jarocha/sentiment_regime_data/raw_data
   # Should pass all checks
   ```

---

## 🚨 Troubleshooting

### If Jobs Fail Again

**1. Check error logs for patterns:**

```bash
# Find common errors across all batches
grep -h "Error\|Failed\|Exception" logs/collect_*.err | sort | uniq -c | sort -rn | head -10
```

**2. Test single batch manually:**

```bash
# Interactive test of batch 0 (2008-Q1)
srun --partition=standard-s --cpus-per-task=8 --mem=16G --time=1:00:00 --pty bash

# Activate environment
module load python/3.11.11/data_science/2025.08.21
source venv/bin/activate

# Run single batch
python scripts/hpc/collect_historical_data.py \
    --start-date 2008-01-01 \
    --end-date 2008-03-31 \
    --sources gdelt,reddit \
    --output /scratch/users/jarocha/sentiment_regime_data/test_run \
    --batch-id 999

# Check output
ls -lh /scratch/users/jarocha/sentiment_regime_data/test_run/
# Should see reddit_batch_0999.parquet and combined_batch_0999.parquet
```

**3. If GDELT still returns 0:**

```bash
# Test GDELT API directly
curl -s "https://api.gdeltproject.org/api/v2/doc/doc?query=sourcelang:english%20(stock%20market)&mode=artlist&maxrecords=10&format=json&startdatetime=20190701000000&enddatetime=20190701235959" | python3 -m json.tool | head -50
# Should see English articles
```

**4. If Reddit pagination fails:**

```bash
# Check Pushshift API status
curl -s "https://api.pullpush.io/reddit/search/submission?subreddit=wallstreetbets&after=1546300800&before=1554076799&size=100" | python3 -m json.tool | head -20
# Should see posts
```

### Common Issues

**API Rate Limiting:**

```bash
# If seeing many 429 errors, reduce parallelism
# Edit collect_historical_array.sh line 10:
#SBATCH --array=0-71%20  # Changed from %36 to %20
```

**Timeout Errors:**

```bash
# If seeing many timeouts, increase timeout in Python script
# Edit collect_historical_data.py:
async with session.get(base_url, params=params, timeout=90)  # Was 30 or 60
```

**Disk Space:**

```bash
# If running out of space
df -h /scratch/users/jarocha

# Clean up old broken data
rm -rf /scratch/users/jarocha/sentiment_regime_data/old_data_broken/

# Or compress it
tar -czf old_data_backup.tar.gz /scratch/users/jarocha/sentiment_regime_data/old_data_broken/
rm -rf /scratch/users/jarocha/sentiment_regime_data/old_data_broken/
```

---

## 📊 Expected Timeline

| Phase | Duration | What's Happening |
|-------|----------|------------------|
| Job submission | 1 minute | SLURM schedules 72 array jobs |
| Initial startup | 5-10 minutes | First 36 jobs start, load Python, activate env |
| Active collection | 2-3 days | Each batch collects 3 months of data |
| Completion | - | All 144 files present with good data |

**Realistic expectations:**

- Some jobs may timeout (24h limit) - that's OK, checkpoint-free restarts work
- API rate limits may slow things down - throttling helps
- Some quarters (early 2008, recent 2025-2026) may have less data

---

## 🎯 Next Steps After Success

Once all 72 batches complete successfully:

1. **Validate data quality:**

   ```bash
   python scripts/hpc/validate_pipeline_phase.py --phase collection --path /scratch/users/jarocha/sentiment_regime_data/raw_data
   ```

2. **Proceed to Phase 2: Sentiment Processing**

   ```bash
   sbatch scripts/hpc/run_sentiment_processing.sh
   ```

3. **Update documentation with actual results:**
   - Note actual file sizes
   - Document any recurring errors
   - Update time estimates based on real performance

---

**Deployment Owner:** Jonathan Rocha
**Last Updated:** February 7, 2026, 12:50 AM
**Ready to deploy:** ✅ All fixes applied and validated locally
