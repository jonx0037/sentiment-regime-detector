# Cross-Asset Sentiment Regime Detector

**SMU MSDS Capstone Project | Spring 2026**  
**Author:** Jonathan Rocha (<jrocha@smu.edu>)  
**Advisor:** [To be determined]  
**Due Date:** March 20, 2026

---

## 🎯 Project Overview

An automated system for detecting market regime transitions (Risk-On/Risk-Off/Transition) through cross-asset sentiment analysis. Uses ensemble transformer models to analyze financial social media, news, and forum data across equities, crypto, forex, and commodities.

**Key Innovation:** First system to aggregate sentiment across multiple asset classes as a **leading indicator** for regime shifts, preceding traditional price-based detection by 1-5 trading days.

---

## 📊 Project Status

**Current Phase:** Week 1 - Draft 0 & Setup  
**Last Updated:** January 10, 2026

### Milestones

- [ ] **Week 1 (Jan 10-17):** Draft 0 completion + workspace setup
- [ ] **Weeks 2-3 (Jan 20-31):** Data collection pipeline
- [ ] **Week 4 (Feb 3-7):** EDA & preprocessing
- [ ] **Weeks 5-6 (Feb 10-21):** Sentiment model training on MANEFRAME
- [ ] **Week 7 (Feb 24-28):** Feature engineering
- [ ] **Weeks 8-9 (Mar 3-14):** Regime classification & backtesting
- [ ] **Week 10 (Mar 17-20):** Dashboard deployment & final paper

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

1. **Sentiment Classification:** Fine-tune FinBERT + RoBERTa ensemble on multi-source financial text
2. **Sentiment Indices:** Construct daily/weekly asset-class-specific indices
3. **Regime Detection:** Build ML classifier (RF/XGBoost/LSTM) for Risk-On/Off/Transition states
4. **Real-time Dashboard:** Deploy React app with live sentiment visualization & regime alerts

---

## 🛠️ Technical Stack

| Component        | Technology                                        |
| ---------------- | ------------------------------------------------- |
| **Backend**      | Python 3.9+, FastAPI, Transformers (Hugging Face) |
| **Models**       | FinBERT, RoBERTa, XGBoost/Random Forest           |
| **Data Sources** | Reddit (PRAW), Twitter/X (Academic API), NewsAPI  |
| **Database**     | PostgreSQL (time-series data)                     |
| **Frontend**     | React, Recharts/D3.js                             |
| **HPC Training** | MANEFRAME (SMU), SLURM job scheduler              |
| **Deployment**   | GitHub Pages (frontend), Docker (backend)         |

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

## 📝 Weekly Progress Log

### Week 1 (Jan 10-17, 2026)

**Goals:**

- [x] Workspace structure setup
- [x] .gitignore configuration
- [x] Todoist automation script
- [ ] Literature review expansion (5-8 papers)
- [ ] Draft 0 completion (abstract, intro, methods)
- [ ] MANEFRAME access request
- [ ] Advisor finalization

**Blockers:** Waiting on HPC access approval, advisor assignment

---

### Week 2-3 (Jan 20-31, 2026)

*[To be updated]*

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
