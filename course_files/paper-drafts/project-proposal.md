# Cross-Asset Sentiment Regime Detector

**Capstone Project Proposal**  
**Student:** Jonathan Rocha (<jrocha@smu.edu>)  
**Advisor:** [Searching - TBD]  
**Institution:** SMU MSDS (Spring 2026 Capstone)  
**GitHub:** github.com/jonx0037/sentiment-regime-detector  
**Updated:** January 11, 2026

## Problem Statement

Financial market participants lack tools to predict regime shifts (Risk-On/Risk-Off/Transition) across multiple asset classes using cross-asset sentiment analysis. Existing sentiment analysis tools focus on single assets and fail to capture the interconnected nature of modern financial markets. This research addresses this gap by developing an ensemble transformer-based system that analyzes sentiment across equities, crypto, forex, and commodities to predict market regime shifts 2-4 weeks in advance, specifically benefiting risk analysts and portfolio managers who need cross-asset perspective for portfolio allocation decisions.

## Research Objectives

1. Develop an automated sentiment classification system for multi-source financial text data
2. Construct asset-class-specific sentiment indices
3. Build a regime classification model to detect market state transitions
4. Create a real-time dashboard for sentiment visualization and regime indicators

## Methodology

**Data Collection (2016-Present):**

- Reddit (r/wallstreetbets, r/investing, r/cryptocurrency, r/forex)
- Twitter (financial hashtags, key influencer accounts)
- Financial news (Bloomberg, Reuters, Financial Times via APIs)

**Sentiment Analysis:**

- Ensemble transformer models: FinBERT (finance-specific) + RoBERTa (general NLP)
- Training on MANEFRAME HPC cluster
- Asset-class-specific sentiment indices (daily/weekly aggregation)

- Feature engineering: Sentiment momentum, cross-asset divergence, volatility metrics
- ML classification: Random Forest, XGBoost, or LSTM for regime detection
- Validation: Backtesting against known market events (COVID-19 crash, 2022 bear market, etc.)- Validation: Backtesting against known market events (COVID-19 crash, 2022 bear market, etc.)

## Technical Architecture

- **Backend:** Python (FastAPI), sentiment models, data pipeline
- **Frontend:** React dashboard with real-time charts (Recharts/D3.js)
- **Infrastructure:** MANEFRAME for training, cloud hosting for deployment
- **Data Storage:** PostgreSQL for time-series data

## Expected Deliverables

1. Research paper (15+ pages) following SMU MSDS Review Journal format
2. Production-ready web application with:
   - Real-time sentiment visualization across asset classes
   - Market regime indicator (Risk-On/Risk-Off/Transition)
   - Historical backtesting performance metrics
   - Divergence alerts (when sentiment contradicts price action)
3. GitHub repository with documented code
4. Conference presentation (poster/lightning talk format)

## Timeline (Capstone A)

- Weeks 1-2: Literature review, advisor finalization
- Weeks 3-5: Data collection pipeline, initial EDA
- Weeks 6-8: Sentiment model training and validation
- Weeks 9-11: Regime classification model development
- Weeks 12-15: Dashboard development, Draft 1 completion

## Advisor Requirements

Seeking an advisor with expertise in:

- NLP/Transformer models (primary need)
- Financial machine learning (secondary)
- Time-series analysis (beneficial)

**Status:** Actively searching for faculty advisor  
**Contact:** <jrocha@smu.edu>  
**GitHub:** github.com/jonx0037/sentiment-regime-detector
