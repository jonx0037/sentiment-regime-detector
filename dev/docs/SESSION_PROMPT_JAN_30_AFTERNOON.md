# Session Prompt - January 30, 2026 (Post-Lunch)

## Project Context

**Project:** Cross-Asset Sentiment Regime Detector  
**Course:** SMU MSDS 6210 Capstone (Spring 2026)  
**Due Date:** March 20, 2026  
**Student:** Jonathan Rocha (<jarocha@mail.smu.edu>)  
**Repository:** `jonx0037/sentiment-regime-detector`

### Project Goal

Build an automated system that detects market regime transitions (Risk-On/Risk-Off/Transition) 1-5 trading days **before** traditional indicators like VIX, by analyzing sentiment across Equities, Crypto, Forex, and Commodities using ensemble transformer models (FinBERT, Llama 3).

### Model Ensemble Strategy

- **FinBERT** - Domain-specific financial sentiment (tested ✅)
- **Llama 3 (7B)** - General LLM for nuanced context understanding (planned)
- V100 GPU (32GB VRAM) can handle both models

---

## Today's Session Summary (January 30, 2026 - Morning)

### ✅ MANEFRAME HPC Access - FULLY OPERATIONAL

Successfully tested SMU's MANEFRAME supercomputer:

| Component | Status | Details |
|-----------|--------|---------|
| SSH Access | ✅ Working | `jarocha@m3.smu.edu` |
| Account | ✅ Active | `jcheun_ds6210_1262_401_0001` |
| GPU | ✅ Tested | Tesla V100-SXM2-32GB (32GB VRAM) |
| PyTorch | ✅ 2.8.0+cu128 | CUDA enabled |
| Transformers | ✅ 5.0.0 | Ready for FinBERT |
| Virtual Env | ✅ Created | `/lustre/scratch/client/users/jarocha/sentiment-detector/venv` |

### MANEFRAME Allocation Details

- **CPU Hours:** 25,000
- **GPU Hours:** 5,000
- **Memory Hours:** 100,000
- **Active Until:** May 7, 2026

### Key MANEFRAME Paths

- **Scratch (main workspace):** `/lustre/scratch/client/users/jarocha/sentiment-detector/`
- **Home (limited, 10GB):** `/users/jarocha/`
- **Activation script:** `source /lustre/scratch/client/users/jarocha/sentiment-detector/activate_env.sh`

### Files Deployed to MANEFRAME

- `setup_environment.sh` - ✅ Ran successfully
- `test_sentiment.sh` - ✅ FinBERT tested on GPU
- `batch_sentiment.py` - Ready for production
- `run_sentiment_batch.sh` - Production batch job script
- `requirements_hpc.txt` - HPC-specific dependencies

### FinBERT Test Results (on GPU)

```text
Model loaded in 8.64 seconds
Inference: 2.2 texts/second
GPU Memory: 0.45 GB used (of 32 GB available)

Sample Results:
[positive] (0.946) The stock market surged today...
[negative] (0.934) Investors are worried about the economic downturn...
[neutral]  (0.874) The Federal Reserve announced it will maintain...
[negative] (0.973) Breaking: Major bank reports significant losses...
```

---

## Current Project State

### Backend (FastAPI) - LOCAL

- **Status:** ✅ Functional
- **Location:** `/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/src/sentiment_detector/`
- **Key Services:**
  - `sentiment_engine.py` - Multi-model sentiment analysis (DistilBERT/FinBERT/RoBERTa)
  - `regime_classifier.py` - Regime state classification
  - `sentiment_service.py` - API service layer
- **Database:** PostgreSQL with 18 analyzed texts
- **Start Command:** `PYTHONPATH=src uvicorn sentiment_detector.main:app --reload --port 8000`

### Frontend (Next.js) - LOCAL

- **Status:** ✅ Ready
- **Location:** `/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/frontend/`
- **Components:** SentimentCard, CrossAssetSummary, SentimentComparisonChart
- **Start Command:** `cd frontend && npm run dev`

### Data Collectors - LOCAL

- `reddit.py` - Reddit PRAW integration (ready, needs API keys)
- `market_data.py` - Yahoo Finance for VIX, prices, volatility
- `news.py` - NewsAPI integration (ready)

---

## Implementation Plan Phase Status

### Phase 1: Local Development (Jan 25 - Feb 15) - IN PROGRESS

- [x] Week 1 (Jan 25-31): Project setup, database, API skeleton
- [x] Sentiment engine with DistilBERT working locally
- [x] React dashboard with live data
- [x] Market data collector tested
- [ ] **NEXT:** Data collection pipeline (Reddit, News)

### Phase 2: MANEFRAME HPC (Feb 10-21)

- [x] HPC access obtained and tested ✅
- [x] Environment setup complete ✅
- [x] FinBERT tested on GPU ✅
- [ ] **NEXT:** Upload real data for batch processing
- [ ] Add Llama 3 (7B) to ensemble for enhanced context understanding
- [ ] Fine-tune models on financial corpus

---

## Recommended Next Steps (This Session)

### Option A: Data Collection Pipeline

1. Set up Reddit API credentials (.env file)
2. Collect sample Reddit data from r/wallstreetbets, r/stocks, r/cryptocurrency
3. Upload to MANEFRAME for batch sentiment analysis
4. Download results and integrate into local database

### Option B: Batch Processing Test

1. Create sample dataset locally (1000+ texts)
2. Upload to MANEFRAME `/lustre/scratch/client/users/jarocha/sentiment-detector/data/raw/`
3. Run `sbatch run_sentiment_batch.sh`
4. Analyze results

### Option C: Model Fine-Tuning Prep

1. Prepare financial corpus for fine-tuning
2. Create SLURM job for FinBERT fine-tuning on financial Reddit data
3. Set up experiment tracking

---

## Quick Start Commands

### Local Development

```bash
# Terminal 1: Start databases
cd ~/Documents/SMU/DS_6210_Capstone
docker-compose -f docker-compose.dev.yml up -d

# Terminal 2: Start backend
source .venv/bin/activate
PYTHONPATH=src uvicorn sentiment_detector.main:app --reload --port 8000

# Terminal 3: Start frontend
cd frontend && npm run dev
```

### MANEFRAME

```bash
# SSH to MANEFRAME
ssh jarocha@m3.smu.edu

# Navigate to project
cd /lustre/scratch/client/users/jarocha/sentiment-detector

# Activate environment
source activate_env.sh

# Submit a job
sbatch <script_name>.sh

# Monitor jobs
squeue -u jarocha

# Check output
cat <job_name>_*.out
```

### Upload files to MANEFRAME (from Mac)

```bash
cd ~/Documents/SMU/DS_6210_Capstone/scripts/hpc
scp <files> jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `src/sentiment_detector/services/sentiment_engine.py` | Core sentiment analysis |
| `src/sentiment_detector/collectors/reddit.py` | Reddit data collection |
| `scripts/hpc/batch_sentiment.py` | MANEFRAME batch processing |
| `scripts/hpc/run_sentiment_batch.sh` | Production SLURM job |
| `dev/docs/IMPLEMENTATION_PLAN.md` | Full project roadmap |
| `course_files/paper-drafts/draft-1.md` | Research paper draft |

---

## Session Goal Suggestion

**Recommended Focus:** Set up data collection pipeline to gather real Reddit/news data, then batch process it on MANEFRAME. This connects your working HPC environment to actual financial text data, completing the data → analysis pipeline.

---

*Generated: January 30, 2026, 1:30 PM CST*
