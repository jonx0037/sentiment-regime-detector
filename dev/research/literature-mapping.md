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

**Current status:** ✅ Well-covered in Draft-0

| Article | Citation Status | Key Contribution | Integration Notes |
| --- | --- | --- | --- |
| Araci (2019) - FinBERT | ✅ Cited | 15% accuracy improvement, domain-specific pre-training | Core foundation - fully integrated |
| Mishev et al. (2020) | ✅ Cited | Comprehensive transformer comparison (BERT, RoBERTa, XLNet) | Detailed architecture comparison included |
| Liu et al. (2024) - LLM Review | ✅ Cited | LLM categorization (encoder-only, encoder-decoder, decoder-only) | Architectural framework integrated |
| Shen & Zhang (2024) | ✅ Cited | FinBERT vs GPT-4o comparison | Few-shot prompt engineering findings |
| Luo & Gong (2024) | ⚠️ In library | Pre-trained LLMs for financial sentiment | **Draft-1: Add for LLM depth** |
| FinLLaMA paper | ⚠️ In library | Algorithmic trading applications | **Draft-1: Add for trading applications** |
| FinSoSent paper | ⚠️ In library | Advanced LLM sentiment methods | **Draft-1: Add for methodology** |

#### Draft-1 Action Items: Transformer Models

- [ ] Expand LLM section with Luo & Gong (2024), FinLLaMA, FinSoSent
- [ ] Add performance benchmarks table comparing all transformer approaches
- [ ] Discuss computational trade-offs between model sizes

---

### 2.2 Financial Sentiment Analysis and NLP

**Current status:** ✅ Well-covered in Draft-0

#### Foundational Work

| Article | Citation Status | Key Contribution | Integration Notes |
| --- | --- | --- | --- |
| Keynes (1973) | ✅ Cited | "Animal spirits" concept | Historical context |
| Loughran & McDonald (2011) | ✅ Cited | Finance-specific lexicon | Foundational methodology |
| Baker & Wurgler (2007) | ✅ Cited | Investor sentiment index | Foundational for H1 |

#### Social Media and Alternative Data

| Article | Citation Status | Key Contribution | Integration Notes |
| --- | --- | --- | --- |
| Bollen et al. (2011) | ✅ Cited | Twitter → DJIA (87.6% accuracy, 2-6 day lead) | Core evidence for H1 |
| Renault (2017) | ✅ Cited | Reddit → next-day volatility | Core evidence |
| Kraaijeveld & De Smedt (2020) | ✅ Cited | Twitter → crypto (1-3 day lead) | Core evidence for H1 |
| Cicekyurt & Bakal (2025) | ✅ Cited | BERT transfer on stock tweets (+20% F1) | Transfer learning evidence |
| Social media crypto prediction paper | ⚠️ In library | Social media → crypto | **Draft-1: Add for crypto section** |

#### Draft-1 Action Items: Sentiment and NLP

- [ ] Add subsection on cryptocurrency-specific sentiment analysis
- [ ] Expand social media section with new 2024 papers
- [ ] Create table comparing lead times across asset classes

---

### 2.3 Cross-Asset and Sentiment Spillover (NEW SECTION FOR DRAFT-1)

**Current status:** ✅ Significantly expanded with new papers

| Article | Citation Status | Key Contribution | Integration Notes |
| --- | --- | --- | --- |
| Caferra (2022) | ✅ Cited | Transfer Entropy: crypto↔equity spillovers | Core for H2/H3 |
| Cao et al. (2025) | ✅ Cited | Sentiment connectedness → crash risk | Core for H3 |
| Nyakurukwa & Seetharam (2025) | ✅ Cited | DJIA sentiment network mapping | Core for H3 |
| Wang et al. (2024) | ⚠️ In library | Cross-asset momentum transmission in China | **Draft-1: Add for H2 evidence** |
| Yang et al. (2025) | ⚠️ In library | LLMs for cross-asset risk monitoring | **Draft-1: Add for methodology** |
| Sarfarazurrehman et al. (2025) | ⚠️ In library | AI/ML for cross-asset risk analysis | **Draft-1: Add for case study** |
| Pankwaen et al. (2025) | ⚠️ In library | Multi-asset global trading optimization | **Draft-1: Add for multi-asset** |

#### Draft-1 Action Items: Cross-Asset Analysis

- [ ] Create dedicated subsection 2.3 for cross-asset analysis
- [ ] Synthesize Transfer Entropy methods from Caferra (2022)
- [ ] Integrate Wang et al. (2024) for momentum transmission evidence
- [ ] Add Yang et al. (2025) for LLM-based cross-asset monitoring
- [ ] Build case for portfolio-level sentiment aggregation using Pankwaen et al. (2025)

---

### 2.4 Market Regime Detection

**Current status:** ✅ Well-covered in Draft-0

| Article | Citation Status | Key Contribution | Integration Notes |
| --- | --- | --- | --- |
| Zhang et al. (2020) | ✅ Cited | Explainable ML, 22.53% annual returns, Sharpe 1.06 | Benchmark results |
| Shu et al. (2024) | ✅ Cited | Statistical jump model for regimes | Methodology reference |
| Suárez-Cetrulo et al. (2023) | ✅ Cited | Systematic review (140 studies) | Comprehensive background |

#### Draft-1 Action Items: Regime Detection

- [ ] Expand on limitations of traditional regime detection
- [ ] Create comparison table: VIX-based vs. sentiment-based detection

---

## Hypothesis Support Matrix

### H1: Leading Indicator Hypothesis

**Hypothesis:** *Cross-asset sentiment provides a leading indicator for market regime shifts, preceding VIX-based detection by 1-5 trading days.*

| Evidence Source | Lead Time | Asset Class | Strength |
| --- | --- | --- | --- |
| Bollen et al. (2011) | 2-6 days | Equities (DJIA) | Strong |
| Kraaijeveld & De Smedt (2020) | 1-3 days | Crypto | Strong |
| Renault (2017) | Next-day | Equities | Moderate |
| Caferra (2022) | Not specified | Crypto↔Equity | Moderate |

**Gap Analysis:** ❌ No direct evidence for forex or commodities lead times

**Draft-1 Action:** Search for forex/commodities sentiment prediction papers

---

### H2: Divergence Signal Hypothesis

**Hypothesis:** *Sentiment divergence between asset classes signals impending regime transitions.*

| Evidence Source | Finding | Strength |
| --- | --- | --- |
| Caferra (2022) | Sentiment mediates cross-market relationships | Moderate |
| Wang et al. (2024) | Cross-asset momentum transmission mechanisms | Strong |
| Pankwaen et al. (2025) | Multi-asset optimization across markets | Moderate |

**Gap Analysis:** ✅ Significantly improved with new cross-asset papers

**Draft-1 Action:**

- [ ] Synthesize Wang et al. (2024) for momentum/divergence evidence
- [ ] Integrate Pankwaen et al. (2025) for multi-asset framework

---

### H3: Network Effect Hypothesis

**Hypothesis:** *Sentiment connectedness intensity correlates with regime transition probability.*

| Evidence Source | Finding | Strength |
| --- | --- | --- |
| Cao et al. (2025) | High connectedness → crash risk | Strong |
| Nyakurukwa & Seetharam (2025) | DJIA sentiment highly interconnected | Moderate |
| Yang et al. (2025) | LLM-based cross-asset monitoring | Moderate |
| Sarfarazurrehman et al. (2025) | AI/ML for cross-asset risk analysis | Moderate |

**Gap Analysis:** ✅ Well-supported with new AI/ML cross-asset papers

**Draft-1 Action:**

- [ ] Extend to cross-asset network hypothesis using Yang et al. (2025)
- [ ] Integrate Sarfarazurrehman et al. (2025) for risk analysis framework

---

### H4: Ensemble Superiority Hypothesis

**Hypothesis:** *Ensemble transformers outperform single-model approaches across data sources.*

| Evidence Source | Finding | Strength |
| --- | --- | --- |
| Mishev et al. (2020) | Different models excel on different sources | Strong |
| Shen & Zhang (2024) | FinBERT beats general LLMs on financial text | Moderate |
| Kelly & Xiu (2023) | Comprehensive financial ML methodology review | Strong |
| Micaletti (2019) | Relative sentiment for tactical asset allocation | Moderate |

**Gap Analysis:** ✅ Well-supported with foundational ML papers added

**Draft-1 Action:**

- [ ] Integrate Kelly & Xiu (2023) for ML methodology framework
- [ ] Add Micaletti (2019) for tactical allocation evidence

---

## Literature Gap Analysis

### Identified Gaps

1. **Forex Sentiment Analysis**
   - Current library has limited forex-specific papers
   - Action: Search for forex sentiment prediction literature

2. **Commodities Sentiment Analysis**
   - No dedicated papers on commodity sentiment
   - Action: Search for gold, oil sentiment analysis papers

3. **Multi-Asset Regime Detection** ✅ ADDRESSED
   - Previously a gap, now covered by:
     - Wang et al. (2024) - momentum transmission
     - Yang et al. (2025) - LLM cross-asset monitoring
     - Pankwaen et al. (2025) - multi-asset optimization
   - Core **novel contribution** remains: integrated sentiment-based detection

4. **Real-Time System Implementations**
   - Most papers are retrospective analysis
   - Action: Search for deployed sentiment systems literature

---

## Draft-1 Literature Review Outline

```markdown
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
| --- | --- | --- | --- | --- |
| 2.1 Transformers | 80% | 95% | 4 | 3 |
| 2.2 Sentiment/NLP | 75% | 90% | 8 | 1 |
| 2.3 Cross-Asset | 40% | 90% | 3 | 4 |
| 2.4 Regime Detection | 70% | 90% | 4 | 0 |
| Foundational | 70% | 95% | 3 | 2 |
| **TOTAL** | **65%** | **92%** | **22** | **6** |

### New Papers to Integrate for Draft-1

| Paper | Section | Priority |
| --- | --- | --- |
| Wang et al. (2024) - Cross-asset momentum | 2.3 | High |
| Yang et al. (2025) - LLM cross-asset risk | 2.3 | High |
| Pankwaen et al. (2025) - Multi-asset optimization | 2.3 | Medium |
| Sarfarazurrehman et al. (2025) - AI/ML risk analysis | 2.3 | Medium |
| Kelly & Xiu (2023) - Financial ML review | 2.4 / Methods | High |
| Micaletti (2019) - Tactical allocation | 2.2 | Medium |
