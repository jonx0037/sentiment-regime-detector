# Implementation Roadmap: Cross-Asset Sentiment Regime Detector

**Created:** January 31, 2026  
**Status:** Active Development  
**Defense Date:** ~10+ weeks (Mid-April 2026)  
**Approach:** Hybrid (Option C) - Full methodology with phased implementation

---

## Executive Summary

This roadmap maps each methodology section from Draft-1 (Section 3) to specific development phases. It reflects decisions made on January 31, 2026 based on the comprehensive methodology audit.

### Current Data Status
| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Raw Texts (Kaggle) | 218,702 | 5-10M | ~96% remaining |
| Sentiment Scored | 5,000 (test) | 218K+ | Batch ready |
| VIX Regime Days | 2,535 | - | ✅ Complete |

**Progress (Jan 31, 2026):**
- ✅ KaggleDataLoader enhanced (loads 218K items)
- ✅ Sentiment processing pipeline working (0 errors on 5K test)
- ✅ VIX data collected (10 years, 2015-2025)
- ✅ Evaluation metrics implemented (DA, MCC, F1, Calibration)
- 🔄 Full sentiment processing ready for MANEFRAME

**Priority:** Complete sentiment scoring on HPC, then GARCH-MIDAS.

---

## Phase 1: Foundation (Current - February 10, 2026)

### Priority 1: Time-Alignment Algorithm (Section 3.4.1)
**Status:** � IMPLEMENTED (Jan 31, 2026)  
**Criticality:** HIGHEST - Foundational for GARCH-MIDAS (Layer 1)

**Implementation Approach:** Batch preprocessing step

**Tasks:**
- [x] Implement Dakalbab et al. (2024) time-alignment algorithm
- [x] Create preprocessing pipeline for irregular → regular intervals
- [x] Handle timezone normalization across sources
- [x] Build validation tests for alignment accuracy (61 tests passing)

**Files Created:**
```
src/sentiment_detector/preprocessing/
├── __init__.py            # Module exports
├── time_alignment.py      # Core algorithm (TimeAligner, AlignmentCase, AlignmentResult)
├── timezone_handler.py    # Timezone normalization (4:30 PM EST cutoff)
├── finance_stopwords.py   # Finance-aware stop words (preserves bull, bear, crash, etc.)
├── text_cleaner.py        # Explicit text preprocessing pipeline
├── asset_classifier.py    # Multi-label asset classification
└── tests/
    ├── __init__.py
    ├── test_time_alignment.py
    └── test_preprocessing.py
```

---

### Priority 1: Feature Engineering Core (Section 3.6.2 & 3.6.3)
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Criticality:** HIGHEST - Required for H2 and H3 validation

#### 3.6.2 Entropy-Based Connectedness (Cao et al., 2025)
**Library:** `nitime` (for nonlinear Granger causality)

**Tasks:**
- [x] Implement Granger causality tests FIRST
- [x] Then implement correlation-based networks
- [x] Build entropy-based connectedness measure
- [ ] Create visualization for cross-asset network (deferred to dashboard phase)

#### 3.6.3 Transfer Entropy Divergence (Caferra, 2022)
**Library:** Manual implementation (PyInform has ARM compatibility issues)

**Tasks:**
- [x] Install and test PyInform (note: x86 only, manual fallback for ARM)
- [x] Implement Transfer Entropy calculation
- [x] Build divergence metric between asset classes
- [x] Rényi Transfer Entropy support added

**Files Created:**
```
src/sentiment_detector/features/
├── __init__.py            # Module exports
├── granger_causality.py   # GrangerCausalityAnalyzer, CausalityNetwork (12 tests)
├── transfer_entropy.py    # TransferEntropyAnalyzer, Rényi TE (10 tests)
├── connectedness.py       # ConnectednessAnalyzer, DynamicConnectedness (14 tests)
└── tests/
    └── test_features.py   # 36 tests total, all passing
```

**Key Components:**
- `GrangerCausalityAnalyzer`: Pairwise tests with BIC lag selection
- `TransferEntropyAnalyzer`: Shannon and Rényi TE with permutation significance
- `ConnectednessAnalyzer`: Diebold-Yilmaz framework, TCI, net spillovers
- `DynamicConnectedness`: Rolling window analysis
- Centrality measures: in-degree, out-degree, eigenvector

---

### Priority 2: Text Preprocessing Enhancement (Section 3.3)
**Status:** � IMPLEMENTED (Jan 31, 2026)  
**Decision:** Explicit text cleaning required

**Tasks:**
- [x] Define finance-aware stop words list (preserves: bull, bear, crash, moon, etc.)
- [x] Implement multi-label asset classification
- [x] Create explicit preprocessing pipeline (not just model-integrated)

**Files Created:** See Time-Alignment section above (same module)

**Key Components:**
- `TextCleaner`: URL/mention removal, emoji preservation, cashtag extraction
- `FINANCE_STOPWORDS`: Curated list preserving ~200 financial sentiment words
- `MultiLabelAssetClassifier`: Weighted keyword matching across 4 asset classes

---

### Priority 2: Sentiment Ensemble Implementation (Section 3.5)
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Decision:** Implement ensemble voting NOW

**Current Models:**
- ✅ FinBERT (ProsusAI/finbert)
- ✅ RoBERTa (cardiffnlp/twitter-roberta-base-sentiment-latest)
- ✅ DistilBERT (development)
- 🔴 Llama 3 (7B) - To be added in Phase 2

**Ensemble Strategy:** Weighted voting with asset-class specific adjustments

**Tasks:**
- [x] Implement weighted ensemble voting mechanism
- [x] Create weight learning infrastructure (calibrate method)
- [x] Add model confidence calibration
- [x] Asset-class specific weight adjustments
- [ ] Prepare Llama 3 integration interface (Phase 2)

**Note on Source-Dependent Weighting:**  
*This is NOT contradictory to ensemble strategy. Source-dependent weighting adjusts the ensemble weights based on the text source (e.g., RoBERTa weighted higher for Twitter/crypto, FinBERT for news/equity). The final ensemble still combines all models, but the weight coefficients vary by source type.*

**Files Created:**
```
src/sentiment_detector/models/
├── sentiment_ensemble.py      # SentimentEnsemble, weighted voting (25 tests)
└── tests/
    └── test_sentiment_ensemble.py
```

**Key Components:**
- `SentimentEnsemble`: Weighted voting across multiple models
- `ModelPrediction`: Individual model predictions with entropy
- `EnsemblePrediction`: Combined result with agreement/uncertainty
- Asset-class weights: equity (FinBERT 60%), crypto (RoBERTa 55%)
- Confidence-weighted soft voting
- Mock predictions for testing without GPU

---

### Priority 3: Data Pipeline - Historical Backfill
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Decision:** Prioritize Kaggle ingestion

**Current Kaggle Datasets (~218K loaded, ~827K available):**
| Dataset | Rows Loaded | Status |
|---------|------|--------|
| stock_tweets.csv | 80,787 | ✅ Loaded |
| reddit_news.csv | 73,533 | ✅ Loaded |
| reddit_wsb.csv | 52,398 | ✅ Loaded |
| crypto_tweets | 9,995 | ✅ Loaded |
| djia_combined_news | 1,989 | ✅ Loaded |
| **Total** | **218,702** | **Ready** |

**Tasks:**
- [x] Enhance KaggleDataLoader with stock_tweets format
- [x] Run full Kaggle import for all datasets  
- [x] Add text truncation (512 tokens) to SentimentEnsemble
- [x] Create process_kaggle_sentiment.py batch script
- [x] Test processing pipeline (5K items: 0 errors)
- [ ] Run full processing on all 218K items (ready for MANEFRAME)

**Files Created/Modified:**
```
scripts/process_kaggle_sentiment.py       # Batch processing with progress
src/sentiment_detector/collectors/kaggle_loader.py  # Enhanced loader
```

---

### Priority 3: VIX Data Collection
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Decision:** Collect 10 years of VIX for regime ground truth

**VIX Regime Distribution (2015-2025):**
| Regime | Days | Percentage |
|--------|------|------------|
| low_volatility (VIX < 15) | 1,011 | 39.9% |
| normal (15-25) | 1,167 | 46.0% |
| elevated (25-35) | 299 | 11.8% |
| high_volatility (≥35) | 58 | 2.3% |
| **Total** | **2,535** | **100%** |

**Files Created:**
```
scripts/collect_vix_data.py               # VIX collection script
data/processed/vix_regimes.json           # 10 years of VIX regime data
```

---

### Priority 3: Bot Detection (Section 3.3.4)
**Status:** 🔴 NOT IMPLEMENTED  
**Decision:** ML-based approach (not rule-based)

**Rationale:** Rule-based may incorrectly exclude legitimate outlier accounts

**Tasks:**
- [ ] Research ML-based bot detection methods
- [ ] Implement bot detection classifier
- [ ] Create training data from known bot patterns
- [ ] Add confidence scoring for bot classification

---

### Priority 4: Evaluation Infrastructure (Section 3.8)
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Decision:** Build ASAP (but after model priorities)

**Implemented Metrics:**
- ✅ Directional Accuracy (DA) - per-class precision + transition accuracy
- ✅ Matthews Correlation Coefficient (MCC) - multi-class implementation
- ✅ F1 Score (macro, weighted, per-class)
- ✅ Calibration metrics (ECE, MCE, Brier Score)
- ✅ Confusion matrix

**VIX Data Collection:**
- ✅ Historical VIX collector: `collect_vix_data.py`
- ✅ 10 years of VIX data collected (2015-2025)
- ✅ Regime labels defined: low_volatility, normal, elevated, high_volatility

**Files Created:**
```
src/sentiment_detector/core/metrics.py    # EvaluationMetrics class
scripts/collect_vix_data.py               # VIX collection
scripts/evaluate_sentiment.py             # Evaluation harness
data/processed/vix_regimes.json           # VIX regime ground truth
data/processed/evaluation_5k.json         # Initial evaluation results
```

**Initial Evaluation (5K sample):**
| Metric | Value |
|--------|-------|
| Accuracy | 0.233 |
| Macro F1 | 0.161 |
| MCC | -0.067 |
| ECE | 0.495 |

*Note: Low metrics expected due to limited date overlap (30 days). Full evaluation pending complete data processing.*

**Walk-forward backtesting:** Deferred to Phase 2

---

## Phase 2: MANEFRAME HPC (February 10 - February 21, 2026)

### Layer 1: GARCH-MIDAS (Section 3.7.1)
**Status:** ✅ IMPLEMENTED (Jan 31, 2026)  
**Library:** `arch` (Python)  
**Criticality:** Required before Layer 2

**Decision:** Full GARCH-MIDAS implementation (not simplified GARCH)

**Tasks:**
- [x] Install and test arch library (v8.0.0)
- [x] Implement GARCH-MIDAS with sentiment as exogenous variable
- [x] MIDAS weighting with Beta polynomial
- [x] Volatility regime classification (low/normal/high)
- [x] Forecasting capability
- [ ] Validate against benchmark (standard GARCH) - Phase 3

**Files Created:**
```
src/sentiment_detector/models/garch_midas.py   # GARCHMIDASModel, MIDASWeights
scripts/test_garch_midas.py                    # Unit tests
```

**Key Components:**
- `MIDASWeights`: Beta polynomial weighting for low-frequency variables
- `GARCHMIDASModel`: Combined short-run (GARCH) + long-run (MIDAS) volatility
- `get_volatility_regimes()`: Quantile-based regime classification
- `compute_sentiment_index()`: Aggregate daily sentiments

---

### Layer 2: Statistical Jump Model (Section 3.7.2)
**Status:** 🔴 NOT IMPLEMENTED  
**Reference:** Shu et al. (2024)  
**Criticality:** Core regime detector

**CRITICAL CLARIFICATION:** Draft-1 specifies Statistical Jump Model, NOT HMM. Code comments mentioning "HMM + Gradient Boosting" are outdated.

**Tasks:**
- [ ] Research existing Jump Model implementations
- [ ] If insufficient: Implement custom JM with jump penalty
- [ ] Integrate GARCH-MIDAS volatility estimates
- [ ] Add Connectedness and Transfer Entropy features
- [ ] Tune jump penalty hyperparameter (λ)

**Libraries to Explore:**
- `statsmodels` (check for jump model support)
- `arch` (check for regime-switching models)
- Custom implementation if needed

---

### Llama 3 (7B) Integration
**Status:** ✅ INTERFACE READY (Jan 31, 2026)  
**Decision:** Add to ensemble per Abstract

**Tasks:**
- [x] Create Llama sentiment model interface
- [x] Multiple backends: transformers, llama.cpp, API
- [x] Mock mode for testing
- [x] Ensemble integration function
- [ ] Set up Llama 3 (7B) on MANEFRAME
- [ ] Fine-tune on financial corpus (if time permits)

**Files Created:**
```
src/sentiment_detector/models/llama_sentiment.py   # LlamaSentimentModel
```

**Key Components:**
- `LlamaSentimentModel`: Multi-backend Llama inference
- `LlamaBackend`: Enum for transformers/llama_cpp/api/mock
- `create_llama_for_ensemble()`: Factory for ensemble integration
- Prompt templates for zero-shot sentiment

---

### Batch Processing at Scale
**Status:** ✅ READY FOR HPC  
**Tasks:**
- [x] Create SLURM batch scripts for Kaggle processing
- [x] Create HPC packaging script
- [ ] Upload full dataset to MANEFRAME
- [ ] Run batch sentiment processing with all models
- [ ] Process Connectedness and Transfer Entropy at scale
- [ ] Train Jump Model on full historical data

**Files Created:**
```
scripts/hpc/run_kaggle_sentiment.sh   # SLURM job for 218K items
scripts/package_for_hpc.sh            # Packaging script for transfer
```

---

## Phase 3: Validation & Integration (February 21 - March, 2026)

### Hypothesis Validation
| Hypothesis | Feature Required | Status |
|------------|------------------|--------|
| H1 (Leading Indicator) | Lead-Time Analysis | 🔴 |
| H2 (Divergence Signal) | Transfer Entropy | 🔴 |
| H3 (Network Effect) | Entropy Connectedness | 🔴 |

**Tasks:**
- [ ] Validate H1: Sentiment leads VIX by 1-5 days
- [ ] Validate H2: Transfer Entropy spikes precede crashes
- [ ] Validate H3: High Connectedness predicts Risk-Off
- [ ] Statistical significance testing for all hypotheses

---

### Walk-Forward Backtesting
**Status:** Deferred from Phase 1  
**Tasks:**
- [ ] Implement walk-forward validation framework
- [ ] Test against major market events:
  - COVID-19 crash (March 2020)
  - 2022 Crypto Winter
  - GameStop squeeze (Jan 2021)
- [ ] Calculate performance metrics per event

---

### Dashboard Integration
**Status:** Dashboard ready, features not connected  
**Decision:** Connect AFTER features are tested

**Tasks:**
- [ ] Connect Connectedness visualization
- [ ] Connect Transfer Entropy display
- [ ] Add regime probability display
- [ ] Implement 30-second polling (not real-time streaming)

---

## Testing Strategy

**Decision:** Unit tests for each methodological component

### Test Coverage Required
| Component | Test File | Priority |
|-----------|-----------|----------|
| Time-Alignment | test_time_alignment.py | P1 |
| Connectedness | test_connectedness.py | P1 |
| Transfer Entropy | test_transfer_entropy.py | P1 |
| Text Preprocessing | test_preprocessing.py | P2 |
| Ensemble Voting | test_ensemble.py | P2 |
| GARCH-MIDAS | test_garch_midas.py | P2 |
| Jump Model | test_jump_model.py | P2 |
| Evaluation Metrics | test_evaluation.py | P3 |

---

## Library Requirements

### To Install
```bash
# Feature Engineering
pip install nitime          # Granger causality
pip install pyinform        # Transfer entropy
pip install jpype1           # JIDT fallback

# Modeling
pip install arch            # GARCH-MIDAS

# Already Installed
# transformers, torch, pandas, numpy, scikit-learn
```

---

## Documentation Tracking

### Files to Maintain
| Document | Purpose | Status |
|----------|---------|--------|
| Draft-1.md / .html | Research methodology | Current |
| Draft-1.1.md | As-implemented methodology | To create |
| Draft-2.md | Final submission | Future |
| IMPLEMENTATION_ROADMAP.md | This file | Active |
| METHODOLOGY_AUDIT_JAN_30.md | Gap analysis | Reference |

**Note:** Draft-1 HTML is slightly more current than markdown (post-.docx edits)

---

## Decision Log

### January 31, 2026 Decisions

1. **Approach:** Hybrid (Option C) - Full methodology, phased implementation
2. **No simplification** of methodology for feasibility
3. **Time-alignment:** Priority 1, batch preprocessing
4. **Bot detection:** ML-based (not rule-based)
5. **Text preprocessing:** Explicit cleaning with finance-aware stop words
6. **Asset classification:** Multi-label required
7. **Ensemble:** Learned weights, source-dependent weighting OK
8. **Llama 3 (7B):** Add to ensemble per Abstract
9. **Features (3.6.2, 3.6.3):** Priority 1 (H2, H3 validation)
10. **Granger causality:** Implement before correlation networks
11. **Transfer Entropy:** PyInform first, alternatives if needed
12. **GARCH-MIDAS:** Full implementation (not simplified GARCH)
13. **Statistical Jump Model:** Per Draft-1 (not HMM)
14. **Layer order:** GARCH-MIDAS (L1) before Jump Model (L2)
15. **Evaluation:** Build infrastructure ASAP
16. **Walk-forward:** Deferred to Phase 2
17. **Dashboard:** Connect features after testing
18. **Polling:** 30-second refresh preferred

---

## Immediate Next Steps

### Today (January 31, 2026)
1. ✅ Data volume check: 141K texts (need 5-10M)
2. ✅ Time-alignment implementation (TimeAligner, TimezoneHandler, 4:30 PM cutoff)
3. ✅ Set up feature engineering module structure
4. ✅ Define finance-aware stop words (~200 preserved financial terms)
5. ✅ Implement text cleaner with explicit preprocessing
6. ✅ Implement multi-label asset classification
7. ✅ Create unit tests (61 tests passing)

### This Week (Feb 1-7)
1. [x] Complete time-alignment algorithm
2. [ ] Implement Granger causality tests (nitime)
3. [ ] Begin Transfer Entropy implementation (PyInform)
4. [ ] Accelerate Kaggle data import
5. [ ] Implement ensemble voting mechanism

### Pre-HPC (Feb 8-10)
1. [ ] Skeleton implementations for Connectedness & Transfer Entropy
2. [ ] Ensemble voting mechanism
3. [ ] Test all components locally

---

*Last Updated: January 31, 2026 (Session 2)*
