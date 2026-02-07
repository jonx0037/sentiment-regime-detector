# Archived HPC Scripts - February 7, 2026

These files were archived during the cleanup to simplify the HPC pipeline.
They represent old versions, duplicates, or test scripts from the development process.

## Why Archived

- Multiple failed attempts created script sprawl
- Unclear which versions were correct
- Cleanup needed to restart with clear, working scripts

## What Was Archived

### Old SLURM Files (replaced by .sh versions)
- `*.slurm` files

### Duplicate Scripts
- `run_complete_collection.sh` (duplicate of collect_historical_array.sh)
- `batch_sentiment.py` (old version)
- `process_phase_batch.py` (old version)
- `run_sentiment_batch.sh` (old version)

### Test/Development Scripts
- `test_sentiment.sh`
- `run_kaggle_sentiment.sh`
- `run_llama_sentiment.sh`
- `run_finbert_batch.sh`

### One-Time Setup Scripts
- `deploy_finbert_hpc.sh`
- `setup_environment.sh`
- `package_for_hpc.sh`
- `requirements_hpc.txt`

### Old Export/Processing Scripts
- `export_*.py` files
- `run_garch_midas_hpc.py`

### Archive Files
- `*.tar.gz` files
- `hpc_data/` directory

## If Needed

These files can be restored if needed for reference, but the current
working scripts in `scripts/hpc/` are the canonical versions.

## Restoration

If you need any of these files:

```bash
cp scripts/hpc/archive/feb7_2026_cleanup/<filename> scripts/hpc/
```
