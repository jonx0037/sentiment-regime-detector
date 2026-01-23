# Literature Mapping: Draft-0 → Draft-1

**Cross-Asset Sentiment Regime Detector**  
Mapping Research Articles to Paper Sections  
Last Updated: January 22, 2026

---

## Purpose

This document maps each research article to specific sections of the capstone paper, supporting the development of Draft-1's expanded literature review. Use this to:

1. Identify which articles support each hypothesis
2. Find gaps where additional literature may be needed
3. Track which articles have been fully integrated vs. only cited
4. Plan the narrative flow of the literature review

---

## Section Mapping

### 2.1 Transformer Models in Financial Sentiment Analysis

**Current Status:** ✅ Well-covered in Draft-0

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|----------------|------------------|-------------------|
| Araci (2019) - FinBERT | ✅ Cited | 15% accuracy improvement, domain-specific pre-training | Core foundation - fully integrated |
| Mishev et al. (2020) | ✅ Cited | Comprehensive transformer comparison (BERT, RoBERTa, XLNet) | Detailed architecture comparison included |
| Liu et al. (2024) - LLM Review | ✅ Cited | LLM categorization (encoder-only, encoder-decoder, decoder-only) | Architectural framework integrated |
| Shen & Zhang (2024) | ✅ Cited | FinBERT vs GPT-4o comparison | Few-shot prompt engineering findings |
| Luo & Gong (2024) | ⚠️ In library | Pre-trained LLMs for financial sentiment | **Draft-1: Add for LLM depth** |
| FinLLaMA paper | ⚠️ In library | Algorithmic trading applications | **Draft-1: Add for trading applications** |
| FinSoSent paper | ⚠️ In library | Advanced LLM sentiment methods | **Draft-1: Add for methodology** |

**Draft-1 Action Items:**
- [ ] Expand LLM section with Luo & Gong (2024), FinLLaMA, FinSoSent
- [ ] Add performance benchmarks table comparing all transformer approaches
- [ ] Discuss computational trade-offs between model sizes

---

### 2.2 Financial Sentiment Analysis and NLP

**Current Status:** ✅ Well-covered in Draft-0

#### Foundational Work
| Article | Citation Status | Key Contribution | Integration Notes |
|---------|----------------|------------------|-------------------|
| Keynes (1973) | ✅ Cited | "Animal spirits" concept | Historical context |
| Loughran & McDonald (2011) | ✅ Cited | Finance-specific lexicon | Foundational methodology |
| Baker & Wurgler (2007) | ✅ Cited | Investor sentiment index | Foundational for H1 |

#### Social Media and Alternative Data
| Article | Citation Status | Key Contribution | Integration Notes |
|---------|----------------|------------------|-------------------|
| Bollen et al. (2011) | ✅ Cited | Twitter → DJIA (87.6% accuracy, 2-6 day lead) | Core evidence for H1 |
| Renault (2017) | ✅ Cited | Reddit → next-day volatility | Core evidence |
| Kraaijeveld & De Smedt (2020) | ✅ Cited | Twitter → crypto (1-3 day lead) | Core evidence for H1 |
| Cicekyurt & Bakal (2025) | ✅ Cited | BERT transfer on stock tweets (+20% F1) | Transfer learning evidence |
| Social media crypto prediction paper | ⚠️ In library | Social media → crypto | **Draft-1: Add for crypto section** |

**Draft-1 Action Items:**
- [ ] Add subsection on cryptocurrency-specific sentiment analysis
- [ ] Expand social media section with new 2024 papers
- [ ] Create table comparing lead times across asset classes

---

### 2.3 Cross-Asset and Sentiment Spillover (NEW SECTION FOR DRAFT-1)

**Current Status:** ⚠️ Partially covered - needs significant expansion

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|----------------|------------------|-------------------|
| Caferra (2022) | ✅ Cited | Transfer Entropy: crypto↔equity spillovers | Core for H2/H3 |
| Cao et al. (2025) | ✅ Cited | Sentiment connectedness → crash risk | Core for H3 |
| Nyakurukwa & Seetharam (2025) | ✅ Cited | DJIA sentiment network mapping | Core for H3 |

**Draft-1 Action Items:**
- [ ] Create dedicated subsection 2.3 for cross-asset analysis
- [ ] Synthesize Transfer Entropy methods from Caferra (2022)
- [ ] Discuss limitations of pairwise vs. multi-asset approaches
- [ ] Build case for portfolio-level sentiment aggregation

---

### 2.4 Market Regime Detection

**Current Status:** ✅ Well-covered in Draft-0

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|----------------|------------------|-------------------|
| Zhang et al. (2020) | ✅ Cited | Explainable ML, 22.53% annual returns, Sharpe 1.06 | Benchmark results |
| Shu et al. (2024) | ✅ Cited | Statistical jump model for regimes | Methodology reference |
| Suárez-Cetrulo et al. (2023) | ✅ Cited | Systematic review (140 studies) | Comprehensive background |

**Draft-1 Action Items:**
- [ ] Expand on limitations of traditional regime detection
- [ ] Create comparison table: VIX-based vs. sentiment-based detection

---

## Hypothesis Support Matrix

### H1: Leading Indicator Hypothesis
*"Cross-asset sentiment provides a leading indicator for market regime shifts, preceding VIX-based detection by 1-5 trading days."*

| Evidence Source | Lead Time | Asset Class | Strength |
|-----------------|-----------|-------------|----------|
| Bollen et al. (2011) | 2-6 days | Equities (DJIA) | Strong |
| Kraaijeveld & De Smedt (2020) | 1-3 days | Crypto | Strong |
| Renault (2017) | Next-day | Equities | Moderate |
| Caferra (2022) | Not specified | Crypto↔Equity | Moderate |

**Gap Analysis:** ❌ No direct evidence for forex or commodities lead times

**Draft-1 Action:** Search for forex/commodities sentiment prediction papers

---

### H2: Divergence Signal Hypothesis
*"Sentiment divergence between asset classes signals impending regime transitions."*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Caferra (2022) | Sentiment mediates cross-market relationships | Moderate |

**Gap Analysis:** ⚠️ Limited direct evidence - mostly inferred

**Draft-1 Action:** 
- [ ] Review cross-asset papers for divergence evidence
- [ ] Consider proposing this as novel contribution if unsupported

---

### H3: Network Effect Hypothesis
*"Sentiment connectedness intensity correlates with regime transition probability."*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Cao et al. (2025) | High connectedness → crash risk | Strong |
| Nyakurukwa & Seetharam (2025) | DJIA sentiment highly interconnected | Moderate |

**Gap Analysis:** ✅ Well-supported for within-asset-class networks

**Draft-1 Action:** Extend to cross-asset network hypothesis (novel)

---

### H4: Ensemble Superiority Hypothesis
*"Ensemble transformers outperform single-model approaches across data sources."*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Mishev et al. (2020) | Different models excel on different sources | Strong |
| Shen & Zhang (2024) | FinBERT beats general LLMs on financial text | Moderate |

**Gap Analysis:** ✅ Well-supported theoretically, empirical validation needed

---

## Literature Gap Analysis

### Identified Gaps

1. **Forex Sentiment Analysis**
   - Current library has limited forex-specific papers
   - Action: Search for forex sentiment prediction literature

2. **Commodities Sentiment Analysis**
   - No dedicated papers on commodity sentiment
   - Action: Search for gold, oil sentiment analysis papers

3. **Multi-Asset Regime Detection**
   - Existing work focuses on single-asset or pairwise relationships
   - This is the core **novel contribution** of the research

4. **Real-Time System Implementations**
   - Most papers are retrospective analysis
   - Action: Search for deployed sentiment systems literature

---

## Draft-1 Literature Review Outline

```
2. Literature Review

   2.1 Transformer Models in Financial Sentiment Analysis
       2.1.1 From Lexicons to BERT (Loughran-McDonald → FinBERT)
       2.1.2 Large Language Models (GPT, LLaMA variants)
       2.1.3 Model Comparison and Selection Criteria
   
   2.2 Financial Sentiment and Market Prediction
       2.2.1 Foundational Work (Baker-Wurgler, Animal Spirits)
       2.2.2 Social Media as Predictive Signal
       2.2.3 Cryptocurrency-Specific Sentiment Analysis [NEW]
       2.2.4 Lead Time Evidence Synthesis [EXPANDED]
   
   2.3 Cross-Asset Sentiment Analysis [NEW SECTION]
       2.3.1 Sentiment Spillover Mechanisms
       2.3.2 Transfer Entropy and Information Flow
       2.3.3 Network-Based Approaches
       2.3.4 Gap: Multi-Asset Integration
   
   2.4 Market Regime Detection
       2.4.1 Traditional Approaches (VIX, HMM)
       2.4.2 Machine Learning Methods
       2.4.3 Sentiment-Based Regime Detection
       2.4.4 Gap: Sentiment as Leading Indicator
   
   2.5 Research Hypotheses
       (Updated based on expanded review)
```

---

## Progress Tracker

| Section | Draft-0 Status | Draft-1 Target | Papers Integrated | Papers Pending |
|---------|---------------|----------------|-------------------|----------------|
| 2.1 Transformers | 80% | 95% | 4 | 3 |
| 2.2 Sentiment/NLP | 75% | 90% | 8 | 1 |
| 2.3 Cross-Asset | 40% | 85% | 3 | 0 |
| 2.4 Regime Detection | 70% | 90% | 4 | 0 |
| **TOTAL** | **65%** | **90%** | **19** | **4** |
