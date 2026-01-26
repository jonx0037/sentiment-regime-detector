# Cross-Asset Sentiment Regime Detector: Implementation Plan

**Created:** January 25, 2026  
**Status:** Phase 1 - Pre-HPC Development  
**Repository:** `jonx0037/sentiment-regime-detector`

---

## Executive Summary

This document outlines a two-phase implementation plan for the Cross-Asset Sentiment Regime Detector. Phase 1 focuses on building the complete application infrastructure locally, while Phase 2 leverages MANEFRAME HPC for model training and validation.

---

## System Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    React Dashboard (Next.js)                         │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │    │
│  │  │ Regime   │ │ Sentiment│ │ Cross-   │ │ Alerts   │ │ Historical│  │    │
│  │  │ Indicator│ │ Heatmap  │ │ Asset    │ │ Panel    │ │ Backtest  │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API LAYER (FastAPI)                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │
│  │ /sentiment  │ │ /regime     │ │ /alerts     │ │ /backtest           │    │
│  │ - current   │ │ - current   │ │ - subscribe │ │ - run               │    │
│  │ - history   │ │ - history   │ │ - history   │ │ - results           │    │
│  │ - by_asset  │ │ - transition│ │ - config    │ │ - compare           │    │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROCESSING LAYER                                   │
│  ┌─────────────────────────┐    ┌─────────────────────────────────────┐     │
│  │   Sentiment Engine      │    │      Regime Classifier               │     │
│  │  ┌─────────────────┐    │    │  ┌─────────────────────────────┐    │     │
│  │  │ FinBERT         │    │    │  │ Hidden Markov Model         │    │     │
│  │  │ (fine-tuned)    │────┼────┼─▶│ States: Risk-On, Risk-Off,  │    │     │
│  │  ├─────────────────┤    │    │  │         Transition          │    │     │
│  │  │ RoBERTa         │    │    │  └─────────────────────────────┘    │     │
│  │  │ (ensemble)      │    │    │  ┌─────────────────────────────┐    │     │
│  │  ├─────────────────┤    │    │  │ Gradient Boosting           │    │     │
│  │  │ DistilBERT      │    │    │  │ (regime features)           │    │     │
│  │  │ (fallback/dev)  │    │    │  └─────────────────────────────┘    │     │
│  │  └─────────────────┘    │    └─────────────────────────────────────┘     │
│  └─────────────────────────┘                                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             DATA LAYER                                       │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────────┐    │
│  │   Data Collectors │  │   PostgreSQL      │  │   Redis Cache         │    │
│  │  ┌─────────────┐  │  │  ┌─────────────┐  │  │  ┌─────────────────┐  │    │
│  │  │ Reddit API  │  │  │  │ raw_texts   │  │  │  │ current_regime  │  │    │
│  │  ├─────────────┤  │  │  ├─────────────┤  │  │  ├─────────────────┤  │    │
│  │  │ Twitter API │  │  │  │ sentiment   │  │  │  │ sentiment_cache │  │    │
│  │  ├─────────────┤  │  │  ├─────────────┤  │  │  ├─────────────────┤  │    │
│  │  │ News API    │  │  │  │ regimes     │  │  │  │ rate_limits     │  │    │
│  │  ├─────────────┤  │  │  ├─────────────┤  │  │  └─────────────────┘  │    │
│  │  │ Yahoo Fin   │  │  │  │ alerts      │  │  │                       │    │
│  │  └─────────────┘  │  │  └─────────────┘  │  │                       │    │
│  └───────────────────┘  └───────────────────┘  └───────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Local Development (Pre-HPC)

**Timeline:** January 25 - February 15, 2026 (3 weeks)  
**Goal:** Complete application skeleton with local inference capability

### Week 1: Foundation (Jan 25 - Jan 31)

#### 1.1 Project Structure Setup

```text
sentiment-regime-detector/
├── README.md
├── pyproject.toml                 # Modern Python packaging
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.dev.yml
├── Makefile                       # Common commands
│
├── src/
│   └── sentiment_detector/
│       ├── __init__.py
│       ├── main.py                # FastAPI application entry
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── routes/
│       │   │   ├── sentiment.py   # /api/v1/sentiment/*
│       │   │   ├── regime.py      # /api/v1/regime/*
│       │   │   ├── alerts.py      # /api/v1/alerts/*
│       │   │   └── backtest.py    # /api/v1/backtest/*
│       │   ├── schemas/           # Pydantic models
│       │   │   ├── sentiment.py
│       │   │   ├── regime.py
│       │   │   └── common.py
│       │   └── dependencies.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py          # Settings management
│       │   ├── database.py        # Database connection
│       │   └── security.py        # Auth utilities
│       │
│       ├── models/                # SQLAlchemy ORM models
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── text_record.py
│       │   ├── sentiment.py
│       │   └── regime.py
│       │
│       ├── services/              # Business logic
│       │   ├── __init__.py
│       │   ├── sentiment_engine.py
│       │   ├── regime_classifier.py
│       │   ├── alert_service.py
│       │   └── backtest_service.py
│       │
│       └── collectors/            # Data collection
│           ├── __init__.py
│           ├── base.py
│           ├── reddit.py
│           ├── twitter.py
│           ├── news.py
│           └── market_data.py
│
├── frontend/                      # React/Next.js dashboard
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── Dockerfile
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_sentiment_analysis.ipynb
│   └── 03_regime_detection.ipynb
│
├── tests/
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_collectors/
│
├── scripts/
│   ├── seed_db.py
│   ├── collect_historical.py
│   └── run_backtest.py
│
├── hpc/                           # MANEFRAME-specific files
│   ├── slurm/
│   │   ├── train_finbert.slurm
│       │   ├── train_regime.slurm
│       │   └── backtest.slurm
│   └── configs/
│       └── training_config.yaml
│
└── docs/
    ├── api.md
    ├── deployment.md
    └── architecture.md
```

#### 1.2 Database Schema

```sql
-- Core tables for sentiment regime detector

-- Raw text data from all sources
CREATE TABLE raw_texts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL,           -- 'reddit', 'twitter', 'news'
    source_id VARCHAR(100),                -- Original ID from source
    asset_class VARCHAR(20) NOT NULL,      -- 'equity', 'crypto', 'forex', 'commodity'
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    title TEXT,
    content TEXT NOT NULL,
    metadata JSONB,                         -- Source-specific fields
    
    UNIQUE(source, source_id)
);

-- Sentiment scores per text
CREATE TABLE sentiment_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text_id UUID REFERENCES raw_texts(id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL,        -- 'finbert', 'roberta', 'distilbert'
    model_version VARCHAR(20),
    positive FLOAT NOT NULL,
    negative FLOAT NOT NULL,
    neutral FLOAT NOT NULL,
    compound FLOAT NOT NULL,                -- Aggregated score [-1, 1]
    confidence FLOAT,
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(text_id, model_name)
);

-- Aggregated sentiment indices (hourly/daily)
CREATE TABLE sentiment_indices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_class VARCHAR(20) NOT NULL,
    source VARCHAR(50),                     -- NULL = all sources aggregated
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    granularity VARCHAR(10) NOT NULL,       -- 'hourly', 'daily'
    
    -- Aggregated metrics
    mean_compound FLOAT NOT NULL,
    std_compound FLOAT,
    sample_count INTEGER NOT NULL,
    positive_ratio FLOAT,                   -- % positive texts
    negative_ratio FLOAT,
    
    -- Momentum indicators
    sentiment_momentum FLOAT,               -- Rate of change
    sentiment_acceleration FLOAT,
    
    UNIQUE(asset_class, source, period_start, granularity)
);

-- Regime classifications
CREATE TABLE regime_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    regime VARCHAR(20) NOT NULL,            -- 'risk_on', 'risk_off', 'transition'
    confidence FLOAT NOT NULL,
    model_version VARCHAR(20),
    
    -- Probabilities for each state
    prob_risk_on FLOAT,
    prob_risk_off FLOAT,
    prob_transition FLOAT,
    
    -- Supporting features
    features JSONB,                         -- Input features used
    
    UNIQUE(timestamp)
);

-- Regime transitions (for analysis)
CREATE TABLE regime_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_regime VARCHAR(20) NOT NULL,
    to_regime VARCHAR(20) NOT NULL,
    transition_start TIMESTAMP WITH TIME ZONE NOT NULL,
    transition_end TIMESTAMP WITH TIME ZONE,
    duration_hours INTEGER,
    trigger_features JSONB,                 -- What drove the transition
    validated BOOLEAN DEFAULT FALSE,        -- Confirmed by price action
    
    UNIQUE(transition_start)
);

-- Alert configurations
CREATE TABLE alert_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,                           -- For future multi-user support
    alert_type VARCHAR(50) NOT NULL,        -- 'regime_change', 'divergence', etc.
    conditions JSONB NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alert history
CREATE TABLE alert_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_id UUID REFERENCES alert_configs(id),
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20),                   -- 'info', 'warning', 'critical'
    message TEXT NOT NULL,
    data JSONB,
    acknowledged BOOLEAN DEFAULT FALSE
);

-- Backtest results
CREATE TABLE backtest_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    config JSONB NOT NULL,                  -- Parameters used
    
    -- Date range
    backtest_start DATE NOT NULL,
    backtest_end DATE NOT NULL,
    
    -- Results summary
    total_trades INTEGER,
    win_rate FLOAT,
    sharpe_ratio FLOAT,
    max_drawdown FLOAT,
    cumulative_return FLOAT,
    
    -- Detailed results stored as JSONB
    daily_results JSONB,
    regime_accuracy JSONB,
    
    status VARCHAR(20) DEFAULT 'pending'    -- 'pending', 'running', 'completed', 'failed'
);

-- Market data cache (for validation)
CREATE TABLE market_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol VARCHAR(20) NOT NULL,
    asset_class VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT NOT NULL,
    volume BIGINT,
    
    UNIQUE(symbol, timestamp)
);

-- Indexes for performance
CREATE INDEX idx_raw_texts_created ON raw_texts(created_at);
CREATE INDEX idx_raw_texts_asset ON raw_texts(asset_class);
CREATE INDEX idx_sentiment_processed ON sentiment_scores(processed_at);
CREATE INDEX idx_indices_period ON sentiment_indices(period_start, asset_class);
CREATE INDEX idx_regime_timestamp ON regime_states(timestamp);
CREATE INDEX idx_market_data_lookup ON market_data(symbol, timestamp);
```

#### 1.3 API Contract (OpenAPI Specification)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/sentiment/current` | GET | Current sentiment by asset class |
| `/api/v1/sentiment/history` | GET | Historical sentiment (date range) |
| `/api/v1/sentiment/by-source` | GET | Breakdown by data source |
| `/api/v1/regime/current` | GET | Current regime state + confidence |
| `/api/v1/regime/history` | GET | Regime history with transitions |
| `/api/v1/regime/transitions` | GET | List of regime transitions |
| `/api/v1/alerts/subscribe` | POST | Configure alert notifications |
| `/api/v1/alerts/history` | GET | Past alerts |
| `/api/v1/backtest/run` | POST | Start a backtest |
| `/api/v1/backtest/{id}/status` | GET | Check backtest status |
| `/api/v1/backtest/{id}/results` | GET | Get backtest results |
| `/api/v1/health` | GET | Health check |

#### 1.4 Week 1 Deliverables

- [ ] Initialize Git repository with proper structure
- [ ] Set up `pyproject.toml` with dependencies
- [ ] Create Docker Compose development environment
- [ ] Implement database models (SQLAlchemy)
- [ ] Create Alembic migrations
- [ ] Basic FastAPI skeleton with health endpoint
- [ ] Pydantic schemas for API contracts

---

### Week 2: Data Pipeline & Local Inference (Feb 1 - Feb 7)

#### 2.1 Data Collectors Implementation

| Collector | API | Rate Limits | Priority |
|-----------|-----|-------------|----------|
| Reddit | PRAW | 60 req/min | High |
| Twitter | v2 API | 300 req/15min | Medium |
| News | NewsAPI | 100 req/day (free) | Medium |
| Market Data | yfinance | Unlimited | High |

#### 2.2 Sentiment Engine (Local Development)

For Phase 1, use **DistilBERT** as a lightweight stand-in:

```python
# Inference approach for local development
class SentimentEngine:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Phase 1: Use DistilBERT for fast CPU inference
        Phase 2: Swap to fine-tuned FinBERT from MANEFRAME
        """
        self.pipeline = transformers.pipeline(
            "sentiment-analysis",
            model=model_name,
            device=-1  # CPU
        )
    
    def analyze(self, texts: list[str]) -> list[SentimentScore]:
        # Batch processing for efficiency
        results = self.pipeline(texts, batch_size=32, truncation=True)
        return [self._convert_to_score(r) for r in results]
```

#### 2.3 Week 2 Deliverables

- [ ] Implement Reddit collector with PRAW
- [ ] Implement News collector with NewsAPI
- [ ] Implement Market Data collector with yfinance
- [ ] Create SentimentEngine service with DistilBERT
- [ ] Build sentiment aggregation pipeline
- [ ] Add sentiment API endpoints
- [ ] Write unit tests for collectors

---

### Week 3: Regime Detection & Dashboard (Feb 8 - Feb 15)

#### 3.1 Regime Classifier (Placeholder)

```python
class RegimeClassifier:
    """
    Phase 1: Rule-based regime detection
    Phase 2: Replace with trained HMM + Gradient Boosting
    """
    
    def classify(self, sentiment_features: dict) -> RegimeState:
        # Simple threshold-based logic for development
        mean_sentiment = sentiment_features["cross_asset_mean"]
        sentiment_std = sentiment_features["cross_asset_std"]
        
        if mean_sentiment > 0.2 and sentiment_std < 0.3:
            return RegimeState.RISK_ON
        elif mean_sentiment < -0.2 and sentiment_std < 0.3:
            return RegimeState.RISK_OFF
        else:
            return RegimeState.TRANSITION
```

#### 3.2 Dashboard Components

| Component | Library | Description |
|-----------|---------|-------------|
| Regime Gauge | Custom SVG | Current regime indicator |
| Sentiment Heatmap | Recharts | 4x4 asset class × source grid |
| Time Series | Recharts | Historical sentiment + regime overlay |
| Cross-Asset Divergence | Custom | Highlight when assets diverge |
| Alert Panel | shadcn/ui | Real-time alert notifications |

#### 3.3 Week 3 Deliverables

- [ ] Implement RegimeClassifier service (rule-based)
- [ ] Add regime API endpoints
- [ ] Create Next.js project structure
- [ ] Build dashboard layout and navigation
- [ ] Implement Regime Gauge component
- [ ] Implement Sentiment Heatmap
- [ ] Implement Time Series chart
- [ ] Connect frontend to backend API
- [ ] End-to-end local testing

---

## Phase 2: HPC Training & Validation (With MANEFRAME)

**Timeline:** February 15 - March 15, 2026 (4 weeks)  
**Prerequisites:** MANEFRAME access approved, GPU allocation confirmed

### Week 4-5: Model Training (Feb 15 - Feb 28)

#### 2.1 FinBERT Fine-Tuning

**Training Data:**

- Financial PhraseBank (4,840 sentences)
- FiQA Sentiment Dataset (1,174 samples)  
- Custom collected data from Phase 1 (target: 10,000+ samples)

**SLURM Job Configuration:**

```bash
#SBATCH --job-name=finbert_finetune
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=8:00:00
#SBATCH --output=logs/finbert_%j.out
```

**Training Parameters:**

| Parameter | Value |
|-----------|-------|
| Base Model | `ProsusAI/finbert` |
| Learning Rate | 2e-5 |
| Batch Size | 16 |
| Epochs | 5 |
| Max Length | 512 |
| Warmup Steps | 500 |

#### 2.2 Ensemble Architecture

```python
class EnsembleSentimentModel:
    """
    Weighted ensemble of fine-tuned models
    """
    def __init__(self):
        self.models = {
            "finbert": (FinBERTModel(), 0.5),    # Primary weight
            "roberta": (RoBERTaModel(), 0.3),    # Secondary
            "distilbert": (DistilBERTModel(), 0.2)  # Fast fallback
        }
    
    def predict(self, text: str) -> SentimentScore:
        weighted_scores = []
        for name, (model, weight) in self.models.items():
            score = model.predict(text)
            weighted_scores.append(score * weight)
        return sum(weighted_scores)
```

#### 2.3 Regime Classification Model

**Approach:** Hidden Markov Model + Gradient Boosting hybrid

**Features for HMM:**

- Cross-asset sentiment mean (4 asset classes)
- Sentiment momentum (7-day rolling)
- Sentiment volatility
- Cross-asset correlation
- VIX level (external validation)

**States:**

1. **Risk-On:** High positive sentiment, low volatility, positive momentum
2. **Risk-Off:** Negative sentiment, rising volatility, negative momentum  
3. **Transition:** Mixed signals, high uncertainty

---

### Week 6-7: Backtesting & Validation (Mar 1 - Mar 15)

#### 2.4 Backtesting Framework

**Historical Events to Validate:**

| Event | Date Range | Expected Regime Pattern |
|-------|------------|-------------------------|
| COVID-19 Crash | Feb-Mar 2020 | Risk-On → Transition → Risk-Off |
| 2021 Bull Run | Jan-Nov 2021 | Sustained Risk-On |
| 2022 Bear Market | Jan-Oct 2022 | Risk-Off with brief transitions |
| 2023 AI Rally | Jan-Jul 2023 | Transition → Risk-On |

**Validation Metrics:**

- Regime transition lead time vs. VIX spikes
- Classification accuracy (manual labels)
- Portfolio performance (long/short based on regime)
- Sharpe ratio improvement over buy-and-hold

#### 2.5 Deliverables

- [ ] Fine-tuned FinBERT model checkpoint
- [ ] Fine-tuned RoBERTa model checkpoint
- [ ] Trained HMM regime classifier
- [ ] Backtesting results across all events
- [ ] Performance comparison tables
- [ ] Model cards with metrics

---

## Technical Decisions

### Backend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | FastAPI | Async, OpenAPI auto-docs |
| ORM | SQLAlchemy 2.0 | Type hints, async support |
| Database | PostgreSQL 15 | JSONB, time-series extensions |
| Cache | Redis 7 | Fast in-memory caching |
| Task Queue | Celery + Redis | Background jobs (data collection) |
| ML Serving | Direct inference | Simple for MVP; consider TorchServe later |

### Frontend Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Framework | Next.js 14 | App Router, SSR |
| Styling | Tailwind CSS | Utility-first, fast iteration |
| Components | shadcn/ui | Accessible, customizable |
| Charts | Recharts | React-native, composable |
| State | TanStack Query | Server state management |

### DevOps

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Containerization | Docker | Reproducible environments |
| CI/CD | GitHub Actions | Native integration |
| Deployment | Railway / Render | Simple for MVP |
| Monitoring | Sentry | Error tracking |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Twitter API costs too high | Prioritize Reddit + News; Twitter optional |
| MANEFRAME access delayed | Full app works with DistilBERT locally |
| Rate limiting from data sources | Implement caching, respect limits, use historical data |
| Model performance insufficient | Ensemble approach provides fallbacks |
| Scope creep | Strict adherence to MVP features |

---

## Success Criteria

### Phase 1 (Pre-HPC)

- [ ] API serves sentiment data for 4 asset classes
- [ ] Dashboard displays real-time regime indicator
- [ ] Rule-based regime detection functional
- [ ] Docker Compose enables one-command local setup
- [ ] 80%+ test coverage on core services

### Phase 2 (With MANEFRAME)

- [ ] Fine-tuned FinBERT achieves >85% accuracy on test set
- [ ] Regime classifier identifies transitions 1-5 days before VIX
- [ ] Backtesting shows positive Sharpe ratio improvement
- [ ] Production deployment accessible via public URL

---

## Next Steps

**Immediate (Today):**

1. Initialize the repository structure
2. Set up `pyproject.toml` and dependencies
3. Create Docker Compose development environment
4. Implement database models

**This Week:**

1. Complete Week 1 deliverables
2. Request MANEFRAME access (parallel track)
3. Obtain API keys (Reddit, NewsAPI)

---

## Appendix: Environment Variables

```bash
# .env.example

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sentiment_db

# Redis
REDIS_URL=redis://localhost:6379

# API Keys
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=sentiment-detector:v1.0.0

TWITTER_BEARER_TOKEN=your_twitter_token

NEWS_API_KEY=your_newsapi_key

# Model Configuration
MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
MODEL_DEVICE=cpu  # or cuda

# Application
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

---

*Document maintained by: Jonathan Rocha*  
*Last updated: January 25, 2026*
