# HPC Processing Plan - February 1, 2026

## Overview

**Strategy:** Option B - Prioritized Processing  
**Total Texts Needing Processing:** ~855K (revised after export)  
**HPC Platform:** SMU ManeFrame M3 (Tesla V100-SXM2-32GB)  
**Estimated Throughput:** ~4,650 items/minute (based on job #22738072)

### ManeFrame M3 Configuration (Verified Working)

```bash
SCRATCH=/lustre/scratch/client/users/$USER
PARTITION=gpu-dev
GPU_RESOURCE=gpu:v100:1
MODULE=python/3.11.11/pytorch/2025.08.21  # includes transformers 5.0, torch 2.8
```

---

## Phase 1: High-Priority New Data (~242K texts) 🚀 RUNNING

### Job Status

| Field | Value |
|-------|-------|
| Job ID | 22739605 |
| Node | va003 |
| GPU | Tesla V100-SXM2-32GB (32GB VRAM) |
| Started | Feb 1, 2026 9:13 PM CST |
| Expected Completion | ~10:05 PM CST |

### Actual Export Results (Feb 1 Evening)

```
News texts:         14,924
WSB Echo Chamber:  226,860  (much larger than initial estimate!)
Total:             241,784
File size:         362.3 MB (compressed to 7.5 MB)
```

### 1A. News Data (14,924 texts)

- **Source:** Already in database, 0% sentiment coverage
- **Status:** ✅ Exported to phase1_batch.json

### 1B. WSB Echo Chamber Data (226,860 posts)

- **Source:** New dataset from morning research (6 tickers)
- **Status:** ✅ Exported to phase1_batch.json
- **Breakdown by ticker:**
  - GME: 75,095 posts
  - AMC: 63,357 posts
  - TSLA: 26,706 posts
  - AAPL: 55,853 posts
  - MSFT: 4,599 posts
  - NOK: 1,250 posts

### Phase 1 Processing Estimate

- **Combined texts:** 241,784
- **Estimated GPU time:** ~52 minutes
- **Priority:** HIGH - New data critical for WSB/meme stock analysis

---

## Phase 2: Reddit Backfill (~613K texts)

### Reddit Data Gap Analysis

- **Total Reddit texts:** 2,147,948
- **Already scored:** 1,534,628 (71.4%)
- **Needing scores:** 613,320
- **Estimated GPU time:** ~132 minutes (~2.2 hours)

**Status:** 🔄 To be exported after Phase 1 submission

### Phase 2 Batching Strategy

- Batch size: 50,000 texts per batch file
- Number of batches: ~13 batches
- SLURM array job for parallel processing

---

## Pre-Flight Checklist

Before transferring to ManeFrame:

### Local Preparation

- [x] Verify database connection works
- [x] Confirm all export scripts run without errors  
- [x] Phase 1 batch exported (241,784 texts)
- [ ] Package Phase 1 for transfer

### ManeFrame Preparation

- [ ] SSH access verified
- [ ] Conda environment with transformers/torch ready
- [ ] Scratch space available for batch processing
- [ ] SLURM script templates uploaded

---

## Implementation Order

### Tonight (Feb 1 Evening)

1. ✅ **Export Phase 1 data locally** (DONE)
   - News: 14,924 texts
   - WSB Echo Chamber: 226,860 posts
2. **Package for HPC transfer**
   ```bash
   tar -czvf hpc_phase1.tar.gz data/hpc_batches/phase1/ scripts/hpc/
   ```
3. **Transfer to ManeFrame**
   ```bash
   scp hpc_phase1.tar.gz jarocha@m3.smu.edu:/lustre/scratch/users/jarocha/
   ```
4. **Submit Phase 1 job**

### Tomorrow (Feb 2)

1. **Check Phase 1 job status**
2. **Import Phase 1 results**
3. **Export Phase 2 data (reddit backfill)**
4. **Submit Phase 2 jobs**

### Feb 3-4

1. **Monitor Phase 2 jobs**
2. **Import Phase 2 results**
3. **Validate complete sentiment coverage**

---

## Scripts Needed

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/export_phase1_hpc.py` | Export News + WSB Echo Chamber | ✅ Created |
| `scripts/export_phase2_hpc.py` | Export Reddit backfill (613K) | ✅ Created |
| `scripts/hpc/process_phase1.slurm` | SLURM job for Phase 1 | ✅ Created |
| `scripts/hpc/process_phase2.slurm` | SLURM job for Phase 2 (array) | ✅ Created |
| `scripts/hpc/process_phase_batch.py` | GPU processor with ensemble | ✅ Created |
| `scripts/import_hpc_sentiment.py` | Import results to DB | Exists |

---

## Risk Mitigation

1. **Job Timeout:** Phase 1 uses 1-hour walltime, Phase 2 uses 4-hour walltime
2. **Memory Issues:** Limit GPU batch sizes to 128 for V100
3. **Network Transfer:** Compress batches before scp (362MB → ~80MB compressed)
4. **Result Integrity:** Validate row counts match after import
5. **Phase 1 Larger Than Expected:** 242K texts will take ~52 min instead of 5 min

---

## Revised Time Estimates

| Phase | Texts | GPU Time | Notes |
|-------|-------|----------|-------|
| Phase 1 | 241,784 | ~52 min | News + WSB Echo Chamber |
| Phase 2 | 613,320 | ~132 min | Reddit backfill (13 batches) |
| **Total** | **855,104** | **~3.1 hours** | Sequential; less if parallel |

---

## Success Criteria

- [ ] 100% sentiment coverage for news source (14,924 → 14,924 scored)
- [ ] WSB Echo Chamber fully processed (226,860 posts)
- [ ] Reddit coverage improved from 71.4% to 100%
- [ ] All backtests can run with complete sentiment data

---

## Notes

- HPC jobs run on `gpgpu-1` partition for V100 GPUs
- FinBERT + Twitter-RoBERTa ensemble provides sentiment + confidence scores
- Results stored as JSON, imported via `import_hpc_sentiment.py`
- Phase 1 export completed: `data/hpc_batches/phase1/phase1_batch.json`
