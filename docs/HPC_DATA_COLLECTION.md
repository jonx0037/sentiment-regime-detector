# HPC Comprehensive Data Collection

**Last Updated:** February 7, 2026
**Status:** Fixed - Now uses ALL API keys and collectors

---

## What This Collects

Uses your complete collector infrastructure with ALL configured API keys:

1. **Twitter/X** - Financial tweets across all asset classes (Bearer Token)
2. **Reddit** - Posts from financial subreddits (Client credentials)
3. **RSS Feeds** - News from financial RSS sources (No auth needed)
4. **NewsAPI** - News articles with financial keywords (API key)
5. **Market Data** - Price/volume data from Finhub, Tiingo, CoinAPI (optional)

**Coverage:** 2008-2026, 72 quarters, comprehensive multi-source data

---

## Run on ManeFrame

```bash
# Prerequisites
ssh jarocha@m3.smu.edu
cd /scratch/users/jarocha/sentiment-detector

# Copy .env file to cluster (contains your API keys)
scp .env jarocha@m3.smu.edu:/scratch/users/jarocha/sentiment-detector/

# Load environment
module load python/3.11.11/data_science/2025.08.21
source venv/bin/activate

# Create output directory
mkdir -p /scratch/users/jarocha/sentiment_regime_data/comprehensive_data
mkdir -p logs

# Submit collection
sbatch scripts/hpc/collect_comprehensive_array.sh
```

---

## Monitor

```bash
# Check job status
squeue -u jarocha

# Watch logs
tail -f logs/collect_*.out

# Count completed batches
ls /scratch/users/jarocha/sentiment_regime_data/comprehensive_data/*.parquet | wc -l
```

---

## What Changed

**Old approach (broken):**
- Used simplified reimplementation
- Only collected GDELT + Reddit Pushshift
- Ignored all your API keys
- Didn't use your collector infrastructure

**New approach (fixed):**
- Uses `src/sentiment_detector/collectors/` infrastructure
- Collects from ALL sources with ALL API keys
- Leverages your 2 weeks of API key setup
- Comprehensive multi-source coverage
