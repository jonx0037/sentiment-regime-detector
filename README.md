# Cross-Asset Sentiment Regime Detector

**SMU MSDS Capstone Project | Spring 2026**
**Author:** Jonathan Rocha (<jrocha@smu.edu>)
**Advisor:** David (King Ip) Lin, Ph.D. (<kdlin@smu.edu>)
**Due Date:** March 20, 2026

---

## 🎯 Project Overview

An automated system for detecting market regime transitions (Risk-On/Risk-Off/Transition) through cross-asset sentiment analysis. Uses ensemble transformer models to analyze financial social media, news, and forum data across equities, crypto, forex, and commodities.

**Key Innovation:** First system to aggregate sentiment across multiple asset classes as a **leading indicator** for regime shifts, integrating the ECB Composite Indicator of Systemic Stress (CISS) for enhanced crisis detection.

---

## 📊 Project Status

**Current Phase:** Week 4 - GARCH-MIDAS & Backtesting Complete
**Deployment:** Production deployment active on Railway (backend) + Vercel (frontend)  
**Last Updated:** February 2, 2026

### Key Results

| Metric | Value |
|--------|-------|
| **Texts Processed** | 2.66 million |
| **Date Coverage** | 2002-2026 |
| **CISS Records** | 12,029 |
| **Market Data** | 135,000+ |
| **VIX-CISS Correlation** | 0.63 |

### GARCH(1,1) Volatility Model

| Parameter | Value | Interpretation |
|-----------|-------|----------------|
| α (ARCH) | 0.155 | Shock impact |
| β (GARCH) | 0.800 | Volatility persistence |
| α + β | 0.955 | High persistence |
| AIC | 7027.28 | Model fit |

---

## 📈 Backtest Results

### 2008 Financial Crisis

- **CISS Peak:** 0.9428 (Nov 20, 2008)
- **Sentiment β:** -0.776 (p=0.0044)
- **Crisis Days:** 278 (34.6% of period)

### COVID-19 March 2020

- **VIX Peak:** 82.69 (March 16, 2020)
- **VIX-CISS Correlation:** 0.922
- **GARCH-MIDAS R²:** 0.7124

### GameStop January 2021

- **VIX Spike:** 37.21 (elevated)
- **CISS Max:** 0.024 (calm)
- **Systemic Event?** ❌ Correctly identified as retail-only

### Cross-Asset Performance

- **Gold (COVID to 2024):** +209.2%
- **Crypto Winter 2022:** BTC -77.3%, ETH -82.1%

---

## 🖼️ Visualizations

| Plot | Description |
|------|-------------|
| [CISS vs VIX](results/figures/ciss_vs_vix_timeseries.png) | Time series comparison of systemic stress |
| [Regime Heatmap](results/figures/regime_heatmap.png) | Monthly stress levels 2010-2026 |
| [Sentiment-Volatility](results/figures/sentiment_volatility_scatter.png) | Scatter plot with correlation |
| [Backtest Summary](results/figures/backtest_summary.png) | All backtest results |

---

## 🏗️ Repository Structure

```text
DS_6210_Capstone/
├── src/                       # Core application code
│   └── sentiment_detector/    # Main Python package
│       ├── api/               # FastAPI REST endpoints
│       ├── collectors/        # Data collection (Reddit, Twitter, RSS)
│       ├── core/              # Core models and database
│       ├── features/          # Feature engineering
│       ├── models/            # ML models (GARCH, classifiers)
│       ├── pipeline/          # Data processing pipeline
│       ├── preprocessing/     # Text preprocessing
│       ├── services/          # Business logic services
│       ├── spark/             # PySpark distributed processing
│       └── validation/        # Data validation
├── frontend/                  # React/Next.js dashboard
│   ├── src/                   # Frontend source code
│   └── public/                # Static assets
├── tests/                     # Test suite
├── scripts/                   # Utility scripts (data import, HPC, analysis)
├── data/                      # Data storage (gitignored)
│   ├── kaggle/                # Kaggle datasets
│   ├── processed/             # Processed results
│   └── raw/                   # Raw collected data
├── alembic/                   # Database migrations
├── archive/                   # Historical documentation
├── course_files/              # SMU academic materials
├── docs/                      # Project documentation
├── models/                    # Trained model artifacts
├── results/                   # Analysis results and figures
├── pyproject.toml             # Project dependencies and config
├── docker-compose.yml         # Docker infrastructure
└── README.md                  # This file
```

---

## 🔬 Research Objectives

1. **Sentiment Classification:** Fine-tune FinBERT + RoBERTa ensemble on multi-source financial text ✅
2. **Sentiment Indices:** Construct daily/weekly asset-class-specific indices ✅
3. **Stress Integration:** Integrate ECB CISS for systemic stress detection ✅
4. **GARCH-MIDAS:** Volatility modeling with sentiment/CISS as exogenous variables ✅
5. **Regime Detection:** Build ML classifier for Risk-On/Off/Transition states ⏳
6. **Real-time Dashboard:** Deploy React app with live sentiment visualization 🔜

---

## 🛠️ Technical Stack

| Component        | Technology                                        |
| ---------------- | ------------------------------------------------- |
| **Backend**      | Python 3.11+, FastAPI, async SQLAlchemy           |
| **Models**       | FinBERT, VADER, GARCH-MIDAS (arch library)        |
| **Data Sources** | Reddit, Twitter/X, ECB CISS, Yahoo Finance        |
| **Database**     | PostgreSQL (asyncpg driver)                       |
| **Frontend**     | Next.js, Tailwind CSS                             |
| **HPC Training** | ManeFrame III (SMU), SLURM job scheduler          |
| **Deployment**   | Docker, GitHub Pages                              |

---

## 📚 Key References

### Core Papers (To be expanded in Week 1)

- **Araci (2019):** FinBERT - Financial sentiment analysis with pre-trained transformers
- **Bollen et al. (2011):** Twitter sentiment predicts stock market movements
- **Loughran & McDonald (2011):** Finance-specific sentiment lexicons
- **Renault (2017):** Reddit sentiment correlates with volatility
- **Nystrup et al. (2018):** Regime-switching models for market state detection

**Current Literature Base:** 53 academic papers analyzed (see `course_files/research/summaries/`)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12 (3.13 compatible)
- Docker and Docker Compose (for infrastructure)
- PostgreSQL 15+ and Redis 7+ (via Docker or local)
- Node.js 18+ (for frontend development)

### Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/[your-username]/sentiment-regime-detector.git
cd sentiment-regime-detector

# 2. Create Python virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -e .[dev]  # Install with development tools

# 4. Configure API credentials
cp .env.example .env
# Edit .env with your API keys (see .env.example for required keys)

# 5. Start infrastructure (PostgreSQL + Redis)
docker compose up -d
```

### Quick Start

```bash
# Run database migrations
alembic upgrade head

# Start the API server
uvicorn sentiment_detector.main:app --reload

# In another terminal, start the frontend (optional)
cd frontend
npm install
npm run dev

# Access the application
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Frontend: http://localhost:3000
```

### Data Collection

```bash
# Collect multi-source data
python scripts/collect_multi_source.py --sources twitter,rss,reddit

# Import Kaggle datasets
python scripts/import_kaggle_datasets.py

# Process historical backtests
python scripts/run_historical_backtests.py
```

### HPC Deployment (MANEFRAME III)

```bash
# Package for HPC
./scripts/package_for_hpc.sh

# Transfer to MANEFRAME
scp sentiment-detector-hpc-*.tar.gz username@m3.smu.edu:/path/

# On MANEFRAME: extract and setup
tar -xzf sentiment-detector-hpc-*.tar.gz
cd sentiment-detector-hpc-*
./setup_hpc.sh

# Submit Spark job
sbatch scripts/hpc/run_kaggle_sentiment.sh
```

---

## 📝 Progress Log

### Week 4 (Feb 1-2, 2026) - GARCH-MIDAS & Backtesting

**Completed:**

- ✅ ECB CISS integration (12,029 records)
- ✅ Cross-asset data download (VIX, Gold, Silver, BTC, ETH)
- ✅ GARCH-MIDAS backtests (2008, COVID, GameStop)
- ✅ VIX regime validation (50% agreement, 44% F1)
- ✅ HPC GARCH(1,1) estimation with arch library
- ✅ Visualization generation

### Week 3 (Jan 27-31, 2026) - Sentiment Processing

**Completed:**

- ✅ 2.66M texts processed with VADER on HPC
- ✅ Phased batch processing (Phase 1: 850K, Phase 2: 1.8M)
- ✅ Sentiment import to PostgreSQL
- ✅ WSB 2022 data integration

### Week 2 (Jan 20-26, 2026) - Data Collection

**Completed:**

- ✅ Reddit data collection pipeline
- ✅ Kaggle dataset integration
- ✅ Database schema design
- ✅ HPC job submission system

### Week 1 (Jan 10-17, 2026) - Setup

**Completed:**

- ✅ Workspace structure
- ✅ Git configuration
- ✅ ManeFrame access

---

## 🤝 Contributing

This is a solo capstone project, but feedback is welcome! Feel free to open issues or reach out via email.

---

## 📄 License

This project is for academic purposes as part of the SMU MSDS program. Code will be open-sourced under MIT license upon completion.

---

## 📞 Contact

**Jonathan Rocha**  
Master of Science in Data Science  
Southern Methodist University  
Email: <jrocha@smu.edu>  
GitHub: [your-github-username]

---

## 🙏 Acknowledgments

- **SMU Lyle School of Engineering** - MSDS program support
- **MANEFRAME HPC Team** - GPU compute resources
- **Dr. David (King Ip) Lin** - Research guidance and academic oversight
- **Hugging Face** - Pre-trained transformer models
