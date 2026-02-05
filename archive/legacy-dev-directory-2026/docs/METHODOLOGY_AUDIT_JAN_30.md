# Methodology Audit: Draft-1 vs Implementation
**Date:** January 30, 2026  
**Updated:** January 31, 2026 (Responses & Decisions Added)  
**Purpose:** Comprehensive audit to ensure alignment between written methodology (Draft-1 Section 3) and actual implementation

---

## User Responses & Decisions (January 31, 2026)

**Selected Approach:** Option C (Hybrid) - Full methodology with phased implementation  
**Simplification Policy:** NO simplification of methodology sections for feasibility  
**Defense Timeline:** ~10+ weeks (Mid-April 2026) - Ahead of schedule  
**Draft-2 Status:** Not yet needed; continue documenting progress

### Data Status (check_db.py results)
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Raw Texts | **141,273** | 5-10M | ~97% remaining |
| Sentiment Scores | **137,743** | 5-10M | ~97% remaining |
| Kaggle Available | ~827K rows | - | Ready for import |

**Action:** Prioritize historical backfill (Kaggle) before real-time refinement.

### Key Decisions by Section

| Section | Decision |
|---------|----------|
| **3.2 Data Collection** | Twitter token configured; NewsAPI TBD; prioritize Kaggle backfill |
| **3.3 Text Preprocessing** | Explicit text cleaning required; define finance-aware stop words |
| **3.3 Asset Classification** | Multi-label classification required |
| **3.4.1 Time-Alignment** | **PRIORITY 1**; batch preprocessing approach |
| **3.4.2 Bot Detection** | ML-based approach (not rule-based) to avoid false positives |
| **3.5 Ensemble** | Implement voting NOW; learned weights; add Llama 3 (7B) in Phase 2 |
| **3.5 Source-Weighting** | OK - not contradictory to ensemble strategy |
| **3.6.2-3.6.3** | **PRIORITY 1** - Required for H2/H3 validation |
| **3.6 Libraries** | Granger: nitime; Transfer Entropy: PyInform (jpype fallback) |
| **3.6 Skeletons** | OK for now; implement fully if conflicts arise |
| **3.7 Model Choice** | Statistical Jump Model per Draft-1 (NOT HMM) |
| **3.7.1 GARCH-MIDAS** | Full implementation (not simplified GARCH); use `arch` library |
| **3.7 Layer Order** | Layer 1 (GARCH-MIDAS) first, then Layer 2 (Jump Model) |
| **3.8 Evaluation** | Build infrastructure ASAP |
| **3.8 VIX Data** | Need to gather historical VIX for ground truth |
| **3.8 Walk-Forward** | Deferred to Phase 2 |
| **3.9 Dashboard** | Develop features first, connect after testing; 30-sec polling OK |

### Related Documents Created
- **IMPLEMENTATION_ROADMAP.md** - Detailed phased development plan

---

## Executive Summary

This document compares the methodology described in `draft-1.md` (Section 3: Methods) against the current implementation in the workspace. The goal is to identify discrepancies, gaps, and areas requiring discussion before proceeding with development.

**Overall Assessment:** 🟡 **PARTIALLY ALIGNED** - Data collection and sentiment classification infrastructure is complete. Advanced methodological components (GARCH-MIDAS, Statistical Jump Model, Transfer Entropy) are not yet implemented.

---

## 1. Data Collection (Section 3.2)

### Written Methodology (Draft-1)

**Data Sources:**
1. Reddit (via Pushshift/PRAW API): r/wallstreetbets, r/investing, r/stocks, r/cryptocurrency, r/forex
2. Twitter (via Twitter Academic API/Apify): Ticker keywords, hashtags, influencer accounts
3. Financial News (via NewsAPI/scraping): Bloomberg, Reuters, FT, WSJ
4. Target: 5-10 million text samples (2016-present)
5. Supplementary: Price data (SPY, QQQ, BTC, ETH, EUR/USD, GLD, USO) + VIX

### Current Implementation

**Status:** 🟢 **FULLY IMPLEMENTED**

**Evidence:**
- ✅ `src/sentiment_detector/collectors/reddit.py` - Reddit collector exists
- ✅ `src/sentiment_detector/collectors/twitter.py` - X/Twitter collector using API v2 (Bearer Token)
- ✅ `src/sentiment_detector/collectors/news.py` - NewsAPI integration for Bloomberg, Reuters, WSJ, etc.
- ✅ `src/sentiment_detector/collectors/rss.py` - RSS feeds for real-time news (Yahoo Finance, MarketWatch, CoinDesk, etc.)
- ✅ `src/sentiment_detector/collectors/kaggle_loader.py` - Historical data loader for Kaggle datasets
- ✅ `src/sentiment_detector/collectors/market_data.py` - Market data collection
- ✅ `scripts/collect_multi_source.py` - Multi-source orchestration (Twitter, RSS, Kaggle, News)
- ✅ `data/kaggle/` - Multiple historical datasets (crypto-tweets, financial-news, stock_news, wsb, etc.)

**Collector Details:**
- **Twitter:** Full TwitterCollector class with asset-specific search queries, Bearer Token auth
- **News:** NewsAPI integration with FINANCIAL_SOURCES list (Bloomberg, Reuters, WSJ, FT, CNBC, etc.)
- **RSS:** 15+ financial RSS feeds organized by asset class (equity, crypto, forex, commodity)
- **Kaggle:** Loader supports CSV/JSON formats, subreddit-to-asset mapping

**Minor Gaps:**
1. ⚠️ **Historical Depth:** Need to verify if 2016-present data has been fully collected
2. ⚠️ **API Key Configuration:** Twitter/NewsAPI require keys in `.env` (may not be configured)

**Questions for Discussion:**
- What is our actual data volume to date? (Run `scripts/check_db.py`)
- Are the API keys (Twitter Bearer Token, NewsAPI) configured and tested?
- Should we prioritize real-time collection (RSS/Twitter) or historical backfill (Kaggle)?

**✅ RESOLVED (Jan 31):**
1. **Data volume:** 141,273 raw texts, 137,743 sentiment scores (97% short of target)
2. **API keys:** Twitter Bearer Token configured; NewsAPI TBD based on updated source strategy
3. **Priority:** Historical backfill (Kaggle) FIRST; real-time collection needs refinement only

---

## 2. Text Preprocessing Pipeline (Section 3.3)

### Written Methodology (Draft-1)

**Pipeline:**
1. Tokenization (spaCy/NLTK)
2. Lowercasing
3. URL/mention removal
4. Emoji handling (preserve sentiment-rich: 🚀📈 bullish, 📉💩 bearish)
5. Stop word removal (finance-aware: retain "bull", "bear", "crash")
6. Lemmatization

**Asset Class Labeling:**
- Keyword matching (ticker symbols, currency pairs, commodity names)
- NER models (spaCy financial NER or custom-trained)
- Multi-label classification

### Current Implementation

**Status:** � **IMPLEMENTED (Model-Integrated)**

**Evidence:**
- ✅ `src/sentiment_detector/services/sentiment_engine.py` - Supports DistilBERT, FinBERT, RoBERTa
- ✅ `src/sentiment_detector/collectors/base.py` - Asset classification keywords defined per collector
- ✅ **Emoji handling:** Transformers handle raw text including emojis natively
- ✅ **Asset Class Labeling:** Each collector (Twitter, Reddit, RSS, News, Kaggle) has ASSET_KEYWORDS dict
- ✅ **Model-based tokenization:** Uses HuggingFace AutoTokenizer with truncation/max_length

**How Preprocessing Works:**
- Preprocessing is **model-integrated**, not standalone - transformers handle tokenization, special chars, etc.
- Asset classification uses **keyword matching** in collectors (e.g., ASSET_KEYWORDS dict)
- URL/mention handling is done by the transformer tokenizer implicitly

**Minor Gaps:**
1. ⚠️ **Finance-Aware Stop Words:** Not explicitly defined (relies on model vocabulary)
2. ⚠️ **Multi-Label Classification:** Currently single-label asset assignment

**Questions for Discussion:**
- Is the current model-integrated preprocessing sufficient, or do we need explicit text cleaning?
- Do we need multi-label asset classification (text referencing multiple asset classes)?

**✅ RESOLVED (Jan 31):**
1. **Text cleaning:** Explicit text cleaning required; define finance-aware stop words list
2. **Asset classification:** Multi-label classification required (text may reference multiple assets)

---

## 3. Data Preprocessing Pipeline (Section 3.4)

### Written Methodology (Draft-1)

**Key Components:**

#### 3.4.1 Time-Alignment Algorithm (Dakalbab et al., 2025)
- **Timestamp Standardization:** UTC/EST with 4:30 PM EST cutoff
- **Alignment Logic:**
  - **Case 1 (Perfect Match):** News in [t-1, t] → map to p_t
  - **Case 2 (Sparse Data):** Forward-fill last sentiment (S_last)
  - **Case 3 (High Velocity):** Aggregate Interval Sentiment (AIS_t) for multiple articles

#### 3.4.2 Entity Filtering and Disambiguation (Kengmegni, 2024)
- **Dictionary-Based Filtering:** Ticker/cashtag extraction ($BTC, $SPY)
- **Contextual Disambiguation (Forex):** Handle Subject-Object ambiguity (e.g., "USD soars against JPY")
- **Bot/Spam Removal:** Remove duplicates and bot clusters (Trushkovskyi, 2025)

### Current Implementation

**Status:** 🔴 **NOT IMPLEMENTED**

**Evidence:**
- No `alignment.py`, `time_sync.py`, or similar module found
- No reference to forward-fill logic in codebase
- No entity disambiguation logic found

**Critical Gaps:**
1. ❌ **Time-Alignment Algorithm:** Core preprocessing requirement not implemented
2. ❌ **AIS_t (Aggregated Interval Sentiment):** No aggregation logic for high-velocity periods
3. ❌ **4:30 PM EST Cutoff:** No evidence of next-day attribution logic
4. ❌ **Forex Subject-Object Disambiguation:** Not implemented
5. ❌ **Bot/Spam Detection:** No duplicate or bot removal pipeline

**Questions for Discussion:**
- **CRITICAL:** Time-alignment is fundamental to GARCH-MIDAS (Layer 1). Should this be Priority 1?
- Should we implement time-alignment as a batch preprocessing step or real-time service?
- For bot detection, do we need an ML-based approach or rule-based (e.g., identical text + timestamps)?

**✅ RESOLVED (Jan 31):**
1. **Priority:** YES - Time-alignment is PRIORITY 1 (highest priority in this section)
2. **Implementation:** Batch preprocessing step (more prudent and feasible)
3. **Bot detection:** ML-based approach preferred (rule-based may incorrectly exclude outlier real accounts)

---

## 4. Sentiment Classification (Section 3.5)

### Written Methodology (Draft-1)

**Model Architecture:**
1. **FinBERT:** Finance-specific BERT variant (Araci, 2019) - Fine-tuned on Financial PhraseBank
2. **RoBERTa-base:** General-purpose, fine-tuned on Twitter Financial News Sentiment dataset

**Ensemble Strategy:**
- Voting: Average logits from both models
- Weighted: Source-dependent weights (FinBERT for news, RoBERTa for social)

**Infrastructure:**
- MANEFRAME HPC (SMU cluster)
- GPUs: NVIDIA V100 or A100
- Framework: PyTorch + HuggingFace Transformers

**Output:** {Positive: [0-1], Neutral: [0-1], Negative: [0-1]}

### Current Implementation

**Status:** 🟢 **FULLY IMPLEMENTED**

**Evidence:**
- ✅ `src/sentiment_detector/services/sentiment_engine.py` - Multi-model engine supporting:
  - **DistilBERT:** CPU-friendly default for development
  - **FinBERT (ProsusAI/finbert):** Finance-specific, 3-class (positive/negative/neutral)
  - **RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest):** Twitter-optimized, 3-class
- ✅ `src/sentiment_detector/services/sentiment_service.py` - Orchestration layer for batch processing
- ✅ `scripts/process_batch.py` - Batch processing for HPC
- ✅ `scripts/hpc/` - MANEFRAME integration scripts
- ✅ Auto-device detection (CPU/CUDA/MPS for Apple Silicon)
- ✅ Batch inference with configurable batch_size

**Model Architecture (as implemented):**
```python
MODEL_CONFIGS = {
    "distilbert": {"name": "distilbert-base-uncased-finetuned-sst-2-english"},
    "finbert": {"name": "ProsusAI/finbert"},  # Finance-specific
    "roberta": {"name": "cardiffnlp/twitter-roberta-base-sentiment-latest"},  # Twitter-optimized
}
```

**Output:** SentimentScore dataclass with {label, positive, negative, neutral, compound, confidence}

**Minor Gaps:**
1. ⚠️ **Ensemble Strategy:** Models are switchable but not yet ensembled (averaging/weighting)
2. ⚠️ **Source-Dependent Weighting:** Could apply FinBERT to news, RoBERTa to social
3. ⚠️ **Fine-Tuning:** Using pre-trained weights; fine-tuning on Financial PhraseBank is Phase 2

**Questions for Discussion:**
- Should we implement ensemble voting now or defer to Phase 2?
- Is DistilBERT sufficient for development, or should we default to FinBERT?

**✅ RESOLVED (Jan 31):**
1. **Ensemble:** Implement ensemble voting NOW with learned weights (not simple averaging)
2. **Source-Dependent Weighting:** OK to implement - NOT contradictory to ensemble (weights vary by source type)
3. **Development Model:** DistilBERT sufficient for development
4. **Llama 3 (7B):** Add to ensemble per Abstract (Phase 2 on MANEFRAME)

**Clarification on Source-Dependent Weighting:**  
This is NOT contradictory to ensemble strategy. Source-dependent weighting adjusts the ensemble weight coefficients based on text source (e.g., RoBERTa weighted higher for Twitter, FinBERT for news). The final output still combines all models, but the combination weights vary by source type.

---

## 5. Sentiment Index Construction & Feature Engineering (Section 3.6)

### Written Methodology (Draft-1)

#### 3.6.1 Basic Aggregation Strategy
- **Formula:** SentimentIndex_{c,t} = Σ(P_i - N_i) · w_i / Σw_i
- **Weighting Schemes:** Equal, engagement-weighted, source-weighted, temporal decay (Cai et al., 2024)
- **Features:** Sentiment momentum (ΔSI), cross-asset divergence, volatility

#### 3.6.2 Sentiment Connectedness (Entropy-Based, Cao et al., 2025)
**CRITICAL COMPONENT FOR H3 VALIDATION**

**Methodology:**
1. Construct sentiment spillover network (nodes = asset classes, edges = nonlinear Granger causality)
2. Calculate 4 centrality measures: Degree, Closeness, Betweenness, Eigenvector
3. Use Entropy Weight Method to assign dynamic weights
4. Final feature: SC_{i,t} = Σω_j · C_{ij,t}

**Mathematical Specification:**
- Entropy: E_j = -(1/ln n) Σp_{ij} ln p_{ij}
- Weight: ω_j = (1 - E_j) / Σ(1 - E_k)

#### 3.6.3 Sentiment Divergence & Decoupling (Rényi Transfer Entropy, Caferra, 2022)
**CRITICAL COMPONENT FOR H2 VALIDATION**

**Methodology:**
1. Calculate Rényi Transfer Entropy (RTE) with weighting parameter q
2. Define Net Information Flow: NIF_{X,Y,t} = RTE_{X→Y,t}(q) - RTE_{Y→X,t}(q)
3. Sentiment Decoupling Indicator (SDI_t): Binary feature for total disconnection or anomalous flow

**Mathematical Specification:**
- RTE_{X→Y}(q) = (1/(1-q)) log [Σ_y φ_q(y_t)p_q(y_{t+1}|y_t) / Σ_{x,y} φ_q(x_t,y_t)p_q(y_{t+1}|y_t,x_t)]
- Escort distribution: φ_q(x) = p(x)^q / Σp(x)^q

### Current Implementation

**Status:** � **PARTIALLY IMPLEMENTED (Basic Aggregation Only)**

**Evidence:**
- ✅ `scripts/calculate_indices.py` - Calculates aggregated sentiment indices by asset class
- ✅ `scripts/detect_regime.py` - Calculates momentum, acceleration, and basic divergence
- ✅ `src/sentiment_detector/services/regime_classifier.py` - Has SentimentFeatures dataclass:
  - ✅ cross_asset_mean, cross_asset_std
  - ✅ sentiment_momentum (7-day rolling rate of change)
  - ✅ sentiment_acceleration
  - ✅ max_divergence (simple max-min across assets)
  - ❌ Entropy-based Connectedness (SC_t) - **NOT IMPLEMENTED**
  - ❌ Transfer Entropy Divergence (RTE, NIF, SDI) - **NOT IMPLEMENTED**

**What IS Implemented:**
- Mean compound scores aggregated by asset class/source/time period
- Standard deviation of sentiment
- Positive/negative ratio calculation
- 7-day rolling momentum and acceleration
- Cross-asset mean and std

**Critical Gaps:**
1. ❌ **Entropy-Based Connectedness (3.6.2):** Not implemented - Required for H3 validation
2. ❌ **Transfer Entropy Divergence (3.6.3):** Not implemented - Required for H2 validation
3. ❌ **Network Construction:** No sentiment spillover network (Granger causality) found
4. ❌ **Centrality Measures:** No degree, closeness, betweenness, eigenvector calculations
5. ⚠️ **Temporal Decay Weighting:** Not confirmed if implemented in aggregation

**Questions for Discussion:**
- **CRITICAL:** Sections 3.6.2 and 3.6.3 are CORE to your hypotheses (H2 & H3). Should these be Priority 1?
- For Connectedness: Do we need to implement Granger causality tests first, or use correlation-based networks?
- For Transfer Entropy: This requires PyInform or similar library - should we explore alternatives (e.g., simplified divergence metrics)?
- Are these features intended for Phase 2 (HPC training) or should skeleton implementations exist now?

**✅ RESOLVED (Jan 31):**
1. **Priority:** YES - Sections 3.6.2 and 3.6.3 are PRIORITY 1 for this section
2. **Connectedness Order:** Implement Granger causality tests FIRST, then correlation-based networks
3. **Transfer Entropy Library:** PyInform is first option; explore alternatives only if not feasible
4. **Skeleton vs Full:** Skeleton implementations OK for Phase 1; implement fully if conflicts arise

**Libraries Selected:**
- Granger Causality: `nitime` (nonlinear methods)
- Transfer Entropy: `PyInform` (primary), `jpype`/JIDT (fallback)

---

## 6. Two-Layer Regime Detection Model (Section 3.7)

### Written Methodology (Draft-1)

**Architecture:** Sequential two-layer approach

#### 3.7.1 Layer 1: Sentiment-Adjusted Volatility (GARCH-MIDAS)

**Purpose:** Isolate long-term volatility component driven by sentiment using mixed-frequency data

**Mathematical Specification (Shi, 2025; Cai et al., 2024):**

1. **Return Decomposition:**
   - r_t = μ + √(τ_t · g_t) · ε_t, ε_t ~ N(0,1)

2. **Short-Term Component (GARCH(1,1)):**
   - g_t = (1 - α - β) + α(r_{t-1} - μ)²/τ_t + β·g_{t-1}

3. **Long-Term Component (MIDAS Regression on Sentiment):**
   - log(τ_t) = m + θ Σφ_k(ω_1, ω_2) S_{t-k}
   - θ: Sensitivity to sentiment shocks (Shi found negative sentiment 1.8× stronger)
   - φ_k: Beta weighting polynomial (recent sentiment weighted more)

#### 3.7.2 Layer 2: Regime Classification (Statistical Jump Model)

**Purpose:** Discrete state classification with jump penalty to prevent whipsaw (Shu et al., 2024)

**Mathematical Specification:**
- **Objective:** min_{Θ,s} Σℓ(x_t, θ_{s_t}) + λΣI(s_t ≠ s_{t-1})
- **Loss:** ℓ(x, θ) = (1/2)||x - θ||²
- **Jump Penalty:** λ (tuned via time-series CV to maximize Sharpe ratio)

**Input Features (x_t):**
- GARCH-MIDAS volatility estimate (τ_t)
- Cross-Asset Sentiment Divergence
- Sentiment Connectedness (SC_t)
- Sentiment momentum

#### 3.7.3 Regime Definitions

**States:**
1. **Risk-On:** VIX < 20, equities rising, crypto/commodities rallying
2. **Risk-Off:** VIX > 30, equities falling, flight to safety
3. **Transition:** VIX 20-30, mixed signals

**Labeling Strategy:**
- Manual labeling of major historical regimes
- Algorithmic labeling using VIX thresholds + price trends
- Target: ~1000-2000 labeled days (2016-present)

### Current Implementation

**Status:** 🔴 **CRITICAL GAP - NOT IMPLEMENTED**

**Evidence:**
- `src/sentiment_detector/services/regime_classifier.py` - **Rule-Based Only**
  - Current: Simple threshold-based classification
  - ✅ Defines RegimeState enum (RISK_ON, RISK_OFF, TRANSITION)
  - ✅ Thresholds: RISK_ON > 0.15, RISK_OFF < -0.15
  - ❌ **GARCH-MIDAS:** Not implemented
  - ❌ **Statistical Jump Model:** Not implemented
  - Comment states: "Phase 2 (MANEFRAME): Hidden Markov Model + Gradient Boosting"

**Critical Gaps:**
1. ❌ **GARCH-MIDAS (Layer 1):** Completely missing - Core methodological contribution
2. ❌ **Statistical Jump Model (Layer 2):** Not implemented - Replaces HMM to avoid whipsaw
3. ❌ **Mixed-Frequency Handling:** No MIDAS regression on sentiment
4. ❌ **Jump Penalty Optimization:** No λ tuning via CV
5. ❌ **Historical Regime Labeling:** No evidence of VIX-based labeling pipeline
6. ⚠️ **Model Discrepancy:** Draft mentions "Hidden Markov Model" in comparison, but code comment suggests HMM as Phase 2 approach (contradicts Statistical Jump Model methodology)

**Questions for Discussion:**
- **CRITICAL DISCREPANCY:** Draft-1 states you are using **Statistical Jump Models** to avoid HMM limitations, but code comments suggest "HMM + Gradient Boosting" for Phase 2. Which is correct?
- Is GARCH-MIDAS intended as a research contribution or are we simplifying to standard GARCH for implementation?
- For Statistical Jump Model: Do we need custom implementation or can we use existing libraries (e.g., statsmodels, arch)?
- Should Layer 1 (GARCH-MIDAS) be implemented first before Layer 2, or can we use simple volatility proxies initially?

**✅ RESOLVED (Jan 31):**
1. **Model Choice:** **Statistical Jump Model (Shu et al., 2024)** per Draft-1 is CORRECT. Code comments about "HMM + Gradient Boosting" are outdated/incorrect.
2. **GARCH-MIDAS:** Full implementation intended (NOT simplified GARCH). Use `arch` (Python) library.
3. **Jump Model Implementation:** Use existing libraries if sufficient; custom implementation if needed.
4. **Layer Order:** Implement Layer 1 (GARCH-MIDAS) FIRST before Layer 2. NO simple volatility proxies at any stage.

**Note:** Draft-1 HTML version is slightly more up-to-date than markdown (due to post-.docx manual edits shared with advisor)

---

## 7. Evaluation Strategy (Section 3.8)

### Written Methodology (Draft-1)

**Metrics:**

#### 3.8.1 Directional Accuracy (DA)
- Evaluates capacity to predict *transition* between regimes (not static state)
- DA = (1/N) Σ I[sign(R_{actual,t} - R_{actual,t-1}) = sign(R_{pred,t} - R_{pred,t-1})]

#### 3.8.2 Matthews Correlation Coefficient (MCC)
- Primary metric for imbalanced classes (Risk-Off rare)
- MCC = (TP·TN - FP·FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)]

#### 3.8.3 Lead-Time Analysis (LTA)
- **Critical for H1 validation:** Does sentiment lead VIX?
- Δ_lead = t_start(VIX_threshold) - t_start(Model_pred)
- Target: Mean Δ_lead ∈ [1, 5] trading days

#### 3.8.4 Additional Metrics
- Accuracy, Precision, Recall, F1 per regime class
- Confusion matrix
- Sharpe ratio of regime-based trading strategy

**Training/Validation Split:**
- Training: 2016-2021 (5 years)
- Validation: 2022-2023 (2 years)
- Test: 2024-present (out-of-sample)

### Current Implementation

**Status:** 🔴 **NOT IMPLEMENTED**

**Evidence:**
- No `evaluation/` module found
- No `backtest_service.py` implementation (API route exists as placeholder)
- `scripts/analyze_results.py` - Exists but unclear if implements above metrics

**Critical Gaps:**
1. ❌ **Directional Accuracy (DA):** Not implemented
2. ❌ **Matthews Correlation Coefficient (MCC):** Not implemented
3. ❌ **Lead-Time Analysis (LTA):** Not implemented - Required for H1 validation
4. ❌ **Walk-Forward Backtesting:** No evidence of time-series CV
5. ❌ **Sharpe Ratio Calculation:** Not found
6. ❌ **Historical Labeling:** No VIX-based ground truth labels

**Questions for Discussion:**
- Should evaluation infrastructure be built now or after model implementation?
- For Lead-Time Analysis: Do we have VIX data ingested to create ground truth labels?
- Walk-forward backtesting requires significant infrastructure - is this Phase 2 or Phase 1 priority?

**✅ RESOLVED (Jan 31):**
1. **Timing:** Build evaluation infrastructure ASAP (not after model implementation)
2. **VIX Data:** Need to gather historical VIX data for ground truth labels
3. **Walk-Forward Backtesting:** Deferred to Phase 2

---

## 8. Dashboard Development (Section 3.9)

### Written Methodology (Draft-1)

**Backend (FastAPI):**
- `/sentiment/{asset_class}` - Sentiment index time series
- `/regime/current` - Current regime prediction + confidence
- `/alerts/divergence` - Cross-asset divergence alerts

**Frontend (React + Vite):**
- Real-time sentiment gauge per asset class
- Historical sentiment trends (line charts)
- Regime indicator (Risk-On/Off/Transition)
- Divergence alerts

**Deployment:** Not specified in Section 3.9

### Current Implementation

**Status:** 🟢 **IMPLEMENTED**

**Evidence:**
- ✅ **Backend:** `src/sentiment_detector/api/routes/` - All routes exist
- ✅ **Frontend:** `frontend/` with React + Next.js + TypeScript
- ✅ **Components:** CrossAssetSummary, RegimeIndicator, SentimentGauge
- ✅ **Docker:** docker-compose.yml, Dockerfile.dev
- ⚠️ **Divergence API:** `/regime/divergence` exists but marked as TODO

**Gaps Identified:**
1. ⚠️ **Divergence API Logic:** Placeholder only - requires Transfer Entropy implementation
2. ⚠️ **Real-Time Updates:** Unclear if WebSocket or polling implemented
3. ⚠️ **Historical Backtest Visualization:** Not evident in frontend

**Questions for Discussion:**
- Dashboard is well-developed - should we prioritize connecting it to advanced features (Connectedness, Transfer Entropy)?
- Is real-time sentiment streaming a priority or can we use polling (e.g., 30-second refresh)?

**✅ RESOLVED (Jan 31):**
1. **Feature Connection:** Develop and test advanced features FIRST, then connect to dashboard
2. **Streaming vs Polling:** 30-second polling preferred (cost-efficient, maintains "real-time" feel)

---

## 9. Model Comparison (Draft-1 Methodology Section)

### Written Methodology (Draft-1)

**Models to Compare:**
1. Random Forest - Ensemble tree-based classifier
2. XGBoost - Gradient boosting (handles non-linear relationships)
3. LSTM - Recurrent neural network (captures temporal dependencies)
4. **Statistical Jump Model** - Markov-switching with jump penalties (Shu et al., 2024)

**Features (~20 total):**
- Sentiment indices (4 asset classes)
- Sentiment momentum (4 features)
- Cross-asset divergence (1 feature)
- Historical VIX (1 feature)
- Rolling correlations (6 features)
- **Sentiment connectedness metrics** (4 features: degree, betweenness, etc.)

### Current Implementation

**Status:** 🔴 **NOT IMPLEMENTED**

**Evidence:**
- Only rule-based classifier exists
- No model comparison framework
- No training scripts for RF, XGBoost, LSTM, or Statistical Jump Model

**Critical Gaps:**
1. ❌ **Model Training Pipeline:** No HPC training scripts operational
2. ❌ **Baseline Models:** RF, XGBoost, LSTM not implemented
3. ❌ **Statistical Jump Model:** Not implemented (despite being core methodology)
4. ❌ **Feature Vector Construction:** Missing connectedness metrics (4 features)
5. ❌ **Model Evaluation Framework:** No comparison infrastructure

---

## 10. Summary of Critical Gaps

### 🔴 **Priority 1: Core Methodological Contributions (MUST Address)**

These are the novel components that distinguish your research:

1. **GARCH-MIDAS (Section 3.7.1):** Sentiment-adjusted volatility modeling - **NOT IMPLEMENTED**
   - *Why Critical:* Core Layer 1 of Two-Layer Model; handles mixed-frequency data
   - *Dependency:* Requires Time-Alignment Algorithm (3.4.1) to be implemented first

2. **Statistical Jump Model (Section 3.7.2):** Discrete regime classification with jump penalty - **NOT IMPLEMENTED**
   - *Why Critical:* Core Layer 2; avoids HMM whipsaw problem (44% turnover reduction)
   - *Discrepancy:* Draft specifies JM, but code comments mention "HMM + Gradient Boosting"

3. **Entropy-Based Sentiment Connectedness (Section 3.6.2):** Network centrality with entropy weighting - **NOT IMPLEMENTED**
   - *Why Critical:* Required to validate H3 (Network Effect Hypothesis)
   - *Components Missing:* Granger causality network, centrality measures, entropy weighting

4. **Transfer Entropy Divergence (Section 3.6.3):** Rényi Transfer Entropy for decoupling detection - **NOT IMPLEMENTED**
   - *Why Critical:* Required to validate H2 (Divergence Signal Hypothesis)
   - *Note:* Complex mathematical specification, may require PyInform or similar library

5. **Time-Alignment Algorithm (Section 3.4.1):** Forward-fill with aggregation for mixed-frequency data - **NOT IMPLEMENTED**
   - *Why Critical:* Prerequisite for GARCH-MIDAS; handles stochastic sentiment + deterministic prices
   - *Note:* 4:30 PM EST cutoff, Aggregated Interval Sentiment (AIS_t) not implemented

6. **Lead-Time Analysis (Section 3.8.3):** Measuring sentiment→VIX lag - **NOT IMPLEMENTED**
   - *Why Critical:* Required to validate H1 (Leading Indicator Hypothesis)
   - *Note:* Need VIX data ingestion and ground truth labeling

### 🟡 **Priority 2: Supporting Infrastructure (Should Address Soon)**

7. **Entity Disambiguation (Section 3.4.2):** Forex Subject-Object handling, bot removal
8. **Historical Regime Labeling (Section 3.7.3):** VIX-based ground truth for 2016-present
9. **Model Comparison Framework (Section 3.7):** RF, XGBoost, LSTM baselines
10. **Ensemble Strategy (Section 3.5):** Combine FinBERT + RoBERTa outputs
11. **Walk-Forward Backtesting (Section 3.8):** Time-series cross-validation infrastructure

### 🟢 **Strengths: What IS Aligned**

1. ✅ **Data Collection Pipeline:** All sources implemented (Reddit, Twitter, News, RSS, Kaggle)
2. ✅ **Multi-Source Orchestration:** `collect_multi_source.py` handles all collectors
3. ✅ **Sentiment Models:** FinBERT, RoBERTa, DistilBERT all available and switchable
4. ✅ **Database Schema:** Well-designed for multi-source, multi-asset sentiment storage
5. ✅ **Basic Feature Engineering:** Mean, std, momentum, acceleration, simple divergence
6. ✅ **Sentiment Aggregation:** Daily/hourly indices by asset class implemented
7. ✅ **Dashboard:** Frontend + backend API infrastructure complete
8. ✅ **HPC Integration:** MANEFRAME scripts and batch processing ready

---

## 11. Key Questions for Discussion

### **Philosophical/Strategic Questions: ✅ ALL RESOLVED (Jan 31)**

1. **Phased Implementation vs. Full Methodology:**
   - ~~Are Sections 3.6.2 (Connectedness), 3.6.3 (Transfer Entropy), and 3.7 (GARCH-MIDAS + JM) intended for Phase 2 (post-HPC training)?~~
   - ~~Or should skeleton implementations exist now to guide development?~~
   - **ANSWER:** Skeleton implementations OK for Phase 1; implement fully if conflicts arise. No simplification of methodology.

2. **Model Choice Discrepancy:**
   - ~~Draft-1 specifies **Statistical Jump Model** (Shu et al., 2024) to avoid HMM limitations~~
   - ~~Code comments suggest "**HMM + Gradient Boosting**" for Phase 2~~
   - **ANSWER:** Statistical Jump Model (Draft-1) is CORRECT. Code comments are outdated.

3. **Hypothesis Validation Priority:**
   - ~~H1 (Leading Indicator), H2 (Divergence), H3 (Connectedness) require specific features/metrics~~
   - ~~Should we prioritize hypothesis-critical features (Sections 3.6.2, 3.6.3, 3.8.3) over baseline model training?~~
   - **ANSWER:** If we must prioritize baseline training over hypothesis features, so be it, but not expected to be necessary.

4. **Simplification vs. Innovation:**
   - ~~GARCH-MIDAS and Transfer Entropy are complex. Are we:~~
     - ~~A) Implementing them as written (research contribution)~~
     - ~~B) Using simpler proxies initially (e.g., rolling volatility, correlation divergence)~~
     - ~~C) Deferring to Phase 2?~~
   - **ANSWER:** (A) Full implementation as written. Defer complex components to Phase 2, but NO simpler proxies at any stage unless absolutely necessary.

### **Technical Implementation Questions: ✅ ALL RESOLVED (Jan 31)**

5. **Time-Alignment (Section 3.4.1):**
   - ~~Should this be implemented as: Batch preprocessing / Real-time service / Both?~~
   - **ANSWER:** Both, but batch preprocessing first (more prudent and feasible for the app)

6. **Library Selection:**
   - **GARCH-MIDAS:** `arch` (Python) ✅
   - **Transfer Entropy:** `PyInform` (primary), `jpype`/JIDT (fallback) ✅
   - **Granger Causality (for Connectedness):** `nitime` (nonlinear methods) ✅

7. **Sentiment Model Ensemble:**
   - ~~Current status: FinBERT only or FinBERT + RoBERTa?~~
   - ~~If ensemble: Static weights or learned weights?~~
   - ~~Should we add Llama 3 as mentioned in Abstract?~~
   - **ANSWER:** FinBERT + RoBERTa available now; learned weights; YES add Llama 3 (7B) in Phase 2

8. **Data Volume Reality Check:**
   - Target: 5-10 million samples (2016-present)
   - **Current:** 141,273 raw texts (check_db.py results Jan 31)
   - **ANSWER:** Accelerate collection via Kaggle backfill (~827K rows available)

### **Documentation & Workflow Questions: ✅ ALL RESOLVED (Jan 31)**

9. **Methodological Evolution:**
   - ~~Create a separate `IMPLEMENTATION_ROADMAP.md`?~~
   - ~~Update Draft-1 to reflect "as-implemented" methodology?~~
   - ~~Maintain both?~~
   - **ANSWER:** Create IMPLEMENTATION_ROADMAP.md ✅ (created Jan 31). Create Draft-1.1 for as-implemented methodology. Maintain both.

10. **Testing Strategy:**
    - ~~Unit tests vs. end-to-end integration tests?~~
    - **ANSWER:** Unit tests for each methodological component preferred.

---

## 12. Proposed Action Plan (For Discussion)

**✅ SELECTED: Option C (Hybrid Approach)** - See IMPLEMENTATION_ROADMAP.md for full details
6. Add rolling volatility as GARCH-MIDAS proxy
7. Train baseline models (RF, XGBoost)

**Phase 3 (Weeks 6-9):**
8. Implement full GARCH-MIDAS
9. Implement Statistical Jump Model
10. Implement Entropy Connectedness + Transfer Entropy
11. Re-run full evaluation with Draft-1 metrics

**Pros:** Faster to working product; validates data pipeline first  
**Cons:** Risk of "technical debt" if simplifications become permanent

---

### **Option C: Hybrid Approach (Recommended)**

**Philosophy:** Build critical infrastructure now; defer complex modeling to HPC phase

**Phase 1 (Weeks 1-3) - Foundation + Key Features:**
1. ✅ Keep current dashboard/API (already strong)
2. 🔧 Implement Time-Alignment Algorithm (Section 3.4.1) - **CRITICAL for GARCH-MIDAS**
3. 🔧 Implement Historical Regime Labeling (VIX-based)
4. 🔧 Implement simplified Connectedness (correlation-based network, defer Granger causality)
5. 🔧 Implement simplified Divergence (rolling correlation divergence, defer Transfer Entropy)
6. 🔧 Implement Lead-Time Analysis framework (Section 3.8.3)

**Phase 2 (Weeks 4-6) - Model Training on MANEFRAME:**
7. Train baseline models (RF, XGBoost, LSTM) with current + simplified features
8. Implement GARCH-MIDAS in `arch` (Python)
9. Implement Statistical Jump Model (resolve HMM discrepancy first)
10. Run walk-forward backtesting

**Phase 3 (Weeks 7-8) - Advanced Features:**
11. Implement full Entropy-Based Connectedness (Section 3.6.2)
12. Implement Rényi Transfer Entropy (Section 3.6.3)
13. Re-train models with advanced features
14. Final evaluation with all Draft-1 metrics

**Pros:** Balances research rigor with progress; validates hypotheses incrementally  
**Cons:** Still requires significant time investment upfront

---

## 13. Immediate Next Steps (Pre-Meeting)

**✅ COMPLETED (Jan 31):**

1. **Data Inventory:** ✅
   - ✅ `scripts/check_db.py` run: 141,273 raw texts, 137,743 sentiment scores
   - ⏳ Date range verification pending
   - ⏳ Asset class distribution pending

2. **Sentiment Model Status:** ✅
   - ✅ Ensemble models available: FinBERT, RoBERTa, DistilBERT
   - ✅ Using pre-trained weights; fine-tuning deferred to Phase 2

3. **Model Choice Clarification:** ✅
   - ✅ CONFIRMED: Statistical Jump Model (Draft-1 is correct)
   - ✅ Code comments about "HMM" are outdated

4. **Priority Ranking:** ✅
   - ✅ NO simplification of methodology
   - ✅ All hypotheses important; no single priority over others

5. **Timeline Constraints:** ✅
   - ✅ Defense: ~10+ weeks (Mid-April 2026)
   - ✅ Draft-2: Not yet needed; ahead of schedule
   - ✅ Continue documenting progress until ready to compose

**NEW Next Steps (Post-Meeting):**
- See [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) for detailed phased plan

---

## 14. Appendices

### Appendix A: File Mapping (Draft-1 Section → Codebase)

| Draft-1 Section | Expected Implementation | Current Status | File/Module |
|----------------|------------------------|----------------|-------------|
| 3.2 Data Collection | Collectors for Reddit, Twitter, News | � Complete | `src/sentiment_detector/collectors/` (reddit.py, twitter.py, news.py, rss.py, kaggle_loader.py) |
| 3.3 Text Preprocessing | Preprocessing pipeline | 🟢 Model-Integrated | Handled by transformer tokenizers in `sentiment_engine.py` |
| 3.4.1 Time-Alignment | Forward-fill algorithm | ❌ Missing | N/A |
| 3.4.2 Entity Disambiguation | Ticker/cashtag filtering | 🟡 Basic | ASSET_KEYWORDS in each collector |
| 3.5 Sentiment Classification | FinBERT + RoBERTa ensemble | 🟢 Available | `services/sentiment_engine.py` (FinBERT, RoBERTa, DistilBERT) |
| 3.6.1 Basic Aggregation | Sentiment index construction | 🟢 Complete | `scripts/calculate_indices.py`, `scripts/detect_regime.py` |
| 3.6.2 Entropy Connectedness | Network centrality + entropy weights | ❌ Missing | N/A |
| 3.6.3 Transfer Entropy | Rényi TE, decoupling indicator | ❌ Missing | N/A |
| 3.7.1 GARCH-MIDAS | Sentiment-adjusted volatility | ❌ Missing | N/A |
| 3.7.2 Statistical Jump Model | Regime classification with jump penalty | ❌ Missing | `regime_classifier.py` is rule-based only |
| 3.7.3 Regime Labeling | VIX-based ground truth | ❌ Missing | N/A |
| 3.8.1 Directional Accuracy | DA metric | ❌ Missing | N/A |
| 3.8.2 MCC | Matthews Correlation Coefficient | ❌ Missing | N/A |
| 3.8.3 Lead-Time Analysis | Sentiment→VIX lag | ❌ Missing | N/A |
| 3.9 Dashboard | FastAPI + React interface | 🟢 Complete | `src/sentiment_detector/api/`, `frontend/` |

### Appendix B: Hypothesis-Feature Mapping

| Hypothesis | Required Feature/Metric | Draft-1 Section | Implementation Status |
|-----------|------------------------|----------------|----------------------|
| H1: Leading Indicator | Lead-Time Analysis (Δ_lead) | 3.8.3 | ❌ Missing |
| H2: Divergence Signal | Transfer Entropy (RTE, SDI) | 3.6.3 | ❌ Missing |
| H3: Network Effect | Entropy Connectedness (SC_t) | 3.6.2 | ❌ Missing |
| General Validation | GARCH-MIDAS volatility | 3.7.1 | ❌ Missing |
| General Validation | Statistical Jump Model | 3.7.2 | ❌ Missing |

### Appendix C: Libraries/Tools Required for Full Implementation

| Component | Draft-1 Methodology | Suggested Library/Tool | Status |
|----------|---------------------|----------------------|--------|
| GARCH-MIDAS | Shi (2025) | `arch` (Python) | ⚠️ Check if installed |
| Statistical Jump Model | Shu et al. (2024) | Custom implementation (based on Bemporad et al. 2018) | ❌ Not implemented |
| Transfer Entropy | Caferra (2022) | `PyInform` or `jpype` (JIDT) | ❌ Not installed |
| Granger Causality (for Connectedness) | Cao et al. (2025) | `statsmodels` or `nitime` | ⚠️ Check if installed |
| Network Analysis | Centrality measures | `networkx` | ⚠️ Check if installed |
| Sentiment Models | FinBERT, RoBERTa | `transformers`, `torch` | 🟢 Installed |
| Backtesting | Walk-forward CV | Custom or `backtrader` | ❌ Not installed |
| Data Collection | Multi-source | Custom collectors | 🟢 Implemented |
| API | FastAPI | `fastapi`, `uvicorn` | 🟢 Installed |
| Frontend | React + Next.js | Node.js ecosystem | 🟢 Installed |

---

**END OF AUDIT**

**Next Action:** Discuss discrepancies and prioritize implementation strategy.
