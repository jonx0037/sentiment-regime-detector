# Cross-Asset Sentiment Regime Detector

**SMU MSDS Capstone Project | Spring 2026**  
**Author:** Jonathan Rocha (<jrocha@smu.edu>)  
**Advisor:** [To be determined]  
**Due Date:** March 20, 2026

---

## 🎯 Project Overview

An automated system for detecting market regime transitions (Risk-On/Risk-Off/Transition) through cross-asset sentiment analysis. Uses ensemble transformer models to analyze financial social media, news, and forum data across equities, crypto, forex, and commodities.

**Key Innovation:** First system to aggregate sentiment across multiple asset classes as a **leading indicator** for regime shifts, integrating the ECB Composite Indicator of Systemic Stress (CISS) for enhanced crisis detection.

---

## 📊 Project Status

**Current Phase:** Week 4 - GARCH-MIDAS & Backtesting Complete  
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
├── course_files/              # SMU templates, syllabus, guidelines
├── dev/
│   ├── code/                  # Source code (Python backend, React frontend)
│   ├── config/                # Configuration templates, requirements
│   ├── data/                  # Data collection scripts (raw data git-ignored)
│   ├── docs/                  # Technical documentation (Docker, K8s, etc.)
│   ├── research/              # Draft papers, literature notes
│   └── results/               # Model outputs, backtesting results, visualizations
├── .gitignore                 # Git ignore rules (data, secrets, models)
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

*[Literature review to be expanded with 5-8 additional papers this week]*

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python environment
conda create -n sentiment python=3.9
conda activate sentiment
pip install -r dev/config/requirements.md

# API Credentials (see dev/config/config-template.md)
export REDDIT_CLIENT_ID="your_id"
export REDDIT_CLIENT_SECRET="your_secret"
export TWITTER_BEARER_TOKEN="your_token"
export NEWSAPI_KEY="your_key"
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/[your-username]/sentiment-regime-detector.git
cd sentiment-regime-detector

# Set up environment
make setup  # (see dev/docs/makefile-commands.md)

# Run data collection pipeline
python dev/code/data-pipeline-orchestrator.py --start-date 2020-01-01 --end-date 2024-12-31

# Train sentiment model on MANEFRAME
sbatch dev/docs/slurm-job-template.sh
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
- **Dr. [Advisor Name]** - Research guidance
- **Hugging Face** - Pre-trained transformer models
