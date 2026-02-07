# HPC Scripts Cleanup Plan

**Date:** February 7, 2026
**Status:** Ready to execute cleanup and fresh start

---

## 🎯 Problem Summary

The HPC scripts directory has become cluttered with:
- **40 files** (should be ~12)
- Duplicate scripts with similar names
- Old versions from previous failed attempts
- Test scripts and archives
- Unclear which files are actually used

This complexity led to errors and confusion during execution.

---

## 🧹 Cleanup Strategy

### Keep These Core Files (The Good Ones)

**Data Collection (Phase 1):**
1. `collect_historical_array.sh` - SLURM array job wrapper ✅
2. `collect_historical_data.py` - Python collection logic ✅

**Sentiment Processing (Phase 2):**
3. `run_sentiment_processing.sh` - SLURM GPU job wrapper ✅
4. `process_sentiment_batch.py` - Python sentiment processing ✅

**GARCH-MIDAS (Phase 3.5):**
5. `run_garch_midas.sh` - SLURM wrapper ✅
6. `run_garch_midas.py` - Python GARCH-MIDAS logic ✅

**Regime Classification (Phase 3.6):**
7. `run_regime_classification.sh` - SLURM wrapper ✅
8. `run_regime_classification.py` - Python regime logic ✅

**Aggregation (Phase 3):**
9. `aggregate_all_sentiment.py` - Combine all batches ✅

**Utilities:**
10. `monitor_progress.sh` - Progress dashboard ✅
11. `detect_failures.sh` - Failure detection ✅
12. `validate_pipeline_phase.py` - Validation checks ✅
13. `utils/` directory (retry.py, checkpoint.py) ✅

**Total:** 13 files + 1 directory = exactly what we need

---

### Archive These Old/Duplicate Files

**Old SLURM files (replaced by .sh versions):**
- `garch_midas.slurm`
- `process_phase1.slurm`
- `process_phase2.slurm`
- `process_sentiment.slurm`
- `wsb_echo_chamber.slurm`

**Duplicate/Old collection scripts:**
- `run_complete_collection.sh` (duplicate of collect_historical_array.sh)

**Old processing scripts (replaced):**
- `batch_sentiment.py` (old version)
- `process_phase_batch.py` (old version)
- `run_sentiment_batch.sh` (old version)

**Test/Development scripts:**
- `test_sentiment.sh`
- `run_kaggle_sentiment.sh`
- `run_llama_sentiment.sh`
- `run_finbert_batch.sh`

**Deployment/Setup scripts (one-time use):**
- `deploy_finbert_hpc.sh`
- `setup_environment.sh`
- `package_for_hpc.sh`

**Old export scripts (from previous approach):**
- `export_for_hpc.py`
- `export_phase1_hpc.py`
- `export_phase2_hpc.py`
- `export_aligned_midas_for_hpc.py`

**Old GARCH-MIDAS version:**
- `run_garch_midas_hpc.py` (replaced by run_garch_midas.py)

**Archive files:**
- `hpc_garch_midas.tar.gz`
- `hpc_garch_midas_aligned.tar.gz`
- `hpc_data/` directory

**Total to archive:** 27 files

---

## 📂 Archive Process

```bash
# Create archive directory
mkdir -p scripts/hpc/archive/feb7_2026_cleanup

# Move old files to archive
mv scripts/hpc/*.slurm scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_complete_collection.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/batch_sentiment.py scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/process_phase_batch.py scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_sentiment_batch.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/test_sentiment.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_kaggle_sentiment.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_llama_sentiment.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_finbert_batch.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/deploy_finbert_hpc.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/setup_environment.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/package_for_hpc.sh scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/export_*.py scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/run_garch_midas_hpc.py scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/*.tar.gz scripts/hpc/archive/feb7_2026_cleanup/
mv scripts/hpc/hpc_data scripts/hpc/archive/feb7_2026_cleanup/

# Create archive README
cat > scripts/hpc/archive/feb7_2026_cleanup/README.md << 'EOF'
# Archived HPC Scripts - February 7, 2026

These files were archived during the cleanup to simplify the HPC pipeline.
They represent old versions, duplicates, or test scripts from the development process.

## Why Archived

- Multiple failed attempts created script sprawl
- Unclear which versions were correct
- Cleanup needed to restart with clear, working scripts

## If Needed

These files can be restored if needed for reference, but the current
working scripts in `scripts/hpc/` are the canonical versions.
EOF

echo "✅ Archive complete"
```

---

## 🔄 Fresh Start Verification

After cleanup, `scripts/hpc/` should contain EXACTLY:

```
scripts/hpc/
├── collect_historical_array.sh         # Phase 1 wrapper
├── collect_historical_data.py          # Phase 1 logic
├── run_sentiment_processing.sh         # Phase 2 wrapper
├── process_sentiment_batch.py          # Phase 2 logic
├── run_garch_midas.sh                  # Phase 3.5 wrapper
├── run_garch_midas.py                  # Phase 3.5 logic
├── run_regime_classification.sh        # Phase 3.6 wrapper
├── run_regime_classification.py        # Phase 3.6 logic
├── aggregate_all_sentiment.py          # Phase 3 logic
├── monitor_progress.sh                 # Utility
├── detect_failures.sh                  # Utility
├── validate_pipeline_phase.py          # Utility
├── utils/
│   ├── __init__.py
│   ├── retry.py
│   └── checkpoint.py
└── archive/
    └── feb7_2026_cleanup/              # Old files
```

**Verify:**
```bash
cd scripts/hpc
ls -1 | grep -v archive | wc -l
# Should output: 13 (12 files + 1 utils dir + 1 archive dir)
```

---

## ✅ Next Steps After Cleanup

1. **Verify core scripts have all fixes applied** (from HPC_CORRECTIONS_APPLIED.md)
2. **Create fresh HPC deployment checklist** (simpler than current docs)
3. **Test single batch manually** before full submission
4. **Submit with confidence** knowing exactly what's running

---

## 🚀 Simplified Execution Plan

Once cleanup is complete:

```bash
# On ManeFrame
cd /scratch/users/jarocha/sentiment-detector

# Pull latest clean scripts
git pull origin main

# Verify environment
module load python/3.11.11/data_science/2025.08.21
source venv/bin/activate

# Test single batch (2008-Q1)
srun --account=jcheun_ds6210_1262_401_0001 \
     --partition=standard-s \
     --cpus-per-task=8 \
     --mem=16G \
     --time=02:00:00 \
     --pty bash

python scripts/hpc/collect_historical_data.py \
    --start-date 2008-01-01 \
    --end-date 2008-03-31 \
    --sources gdelt,reddit \
    --output /scratch/users/jarocha/test_collection \
    --batch-id 999

# If successful, submit full array
sbatch scripts/hpc/collect_historical_array.sh
```

---

## 📊 Documentation Cleanup

**Keep:**
- HPC_QUICK_START.md (simplified guide)
- HPC_CORRECTIONS_APPLIED.md (error log for reference)

**Simplify/Merge:**
- HPC_EXECUTION_GUIDE.md (too long, fold into QUICK_START)
- HPC_REDEPLOY_COLLECTION.md (redundant with QUICK_START)

**Archive:**
- Old planning docs with outdated information

---

**Cleanup Owner:** Jonathan Rocha
**Ready to execute:** ✅ Clear plan, no ambiguity
**Estimated time:** 5 minutes to archive, 10 minutes to verify
