# Literature Mapping: Draft-0 → Draft-1

**Cross-Asset Sentiment Regime Detector**  
Mapping Research Articles to Paper Sections  
Last Updated: January 25, 2026

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

**Current status:** ✅ Comprehensive coverage with new LLM comparison papers

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Araci (2019) - FinBERT | ✅ Cited | 15% accuracy improvement, domain-specific pre-training | Core foundation - fully integrated |
| Mishev et al. (2020) | ✅ Cited | Comprehensive transformer comparison (BERT, RoBERTa, XLNet) | Detailed architecture comparison included |
| Liu et al. (2024) - LLM Review | ✅ Cited | LLM categorization (encoder-only, encoder-decoder, decoder-only) | Architectural framework integrated |
| Shen & Zhang (2024) | ✅ Cited | FinBERT vs GPT-4o comparison | Few-shot prompt engineering findings |
| Luo & Gong (2024) | ✅ In library | Pre-trained LLMs for financial sentiment | **Draft-1: Add for LLM depth** |
| Konstantinidis et al. (2024) - FinLLaMA | ✅ In library | Algorithmic trading applications | **Draft-1: Add for trading applications** |
| Delgadillo et al. (2024) - FinSoSent | ✅ In library | Advanced LLM sentiment methods | **Draft-1: Add for methodology** |
| Sun et al. (2025) | ✅ NEW | Dictionary + neural hybrid approach | **Draft-1: Hybrid methods section** |
| Ergun & Sefer (2025) - FinSentiment | ✅ NEW | Multi-model comparison (BERT, XLNet, RoBERTa, GPT, Llama, T5) | **Draft-1: Key for H4 ensemble evidence** |
| Nasiopoulos et al. (2025) | ✅ NEW | Fine-tuned GPT-4o, GPT-4o-mini, BERT, FinBERT | **Draft-1: Latest LLM benchmarks** |
| Mahendran et al. (2025) | ✅ NEW | BERT vs FinBERT vs LLMs review | **Draft-1: Model selection guidance** |
| Baghavathi Priya et al. (2025) | ✅ NEW | FinBERT sentiment dynamics, 89.6% accuracy | **Draft-1: Performance benchmarks** |

#### Draft-1 Action Items: Transformer Models

- [x] Expand LLM section with new 2025 comparison papers
- [x] Add performance benchmarks table comparing all transformer approaches
- [ ] Discuss computational trade-offs between model sizes
- [ ] Add subsection on fine-tuning strategies (FinSentiment methodology)

---

### 2.2 Financial Sentiment Analysis and NLP

**Current status:** ✅ Well-covered with new social media and crypto papers

#### Foundational Work

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Keynes (1973) | ✅ Cited | "Animal spirits" concept | Historical context |
| Loughran & McDonald (2011) | ✅ Cited | Finance-specific lexicon | Foundational methodology |
| Baker & Wurgler (2007) | ✅ Cited | Investor sentiment index | Foundational for H1 |

#### Social Media and Alternative Data

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Bollen et al. (2011) | ✅ Cited | Twitter → DJIA (87.6% accuracy, 2-6 day lead) | Core evidence for H1 |
| Renault (2017) | ✅ Cited | Reddit → next-day volatility | Core evidence |
| Kraaijeveld & De Smedt (2020) | ✅ Cited | Twitter → crypto (1-3 day lead) | Core evidence for H1 |
| Cicekyurt & Bakal (2025) | ✅ Cited | BERT transfer on stock tweets (+20% F1) | Transfer learning evidence |
| Raheman et al. (2022) | ✅ In library | Social media → crypto | **Draft-1: Add for crypto section** |
| Amin et al. (2024) | ✅ NEW | Twitter + macro factors for stock prediction | **Draft-1: Multi-factor sentiment** |

#### Cryptocurrency-Specific Sentiment (NEW SUBSECTION)

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Roumeliotis et al. (2024) | ✅ NEW | GPT-4, BERT, FinBERT comparison for crypto | **Draft-1: Crypto NLP benchmarks** |
| Trushkovskyi (2024) | ✅ NEW | Crypto trading models from social sentiment | **Draft-1: Trading applications** |

#### Draft-1 Action Items: Sentiment and NLP

- [x] Add subsection on cryptocurrency-specific sentiment analysis
- [x] Expand social media section with new 2024-2025 papers
- [ ] Create table comparing lead times across asset classes
- [ ] Integrate Amin et al. (2024) for multi-factor framework

---

### 2.3 Cross-Asset and Sentiment Spillover

**Current status:** ✅ Significantly expanded - now comprehensive

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Caferra (2022) | ✅ Cited | Transfer Entropy: crypto↔equity spillovers | Core for H2/H3 |
| Cao et al. (2025) | ✅ Cited | Sentiment connectedness → crash risk | Core for H3 |
| Nyakurukwa & Seetharam (2025) | ✅ Cited | DJIA sentiment network mapping | Core for H3 |
| Wang et al. (2024) | ✅ In library | Cross-asset momentum transmission in China | **Draft-1: Add for H2 evidence** |
| Yang et al. (2025) | ✅ In library | LLMs for cross-asset risk monitoring | **Draft-1: Add for methodology** |
| Sarfarazurrehman et al. (2025) | ✅ In library | AI/ML for cross-asset risk analysis (29.52% returns, Sharpe 0.98) | **Draft-1: Add for case study** |
| Pankwaen et al. (2025) | ✅ In library | Multi-asset global trading (29.52% returns, Sharpe 0.829) | **Draft-1: Add for multi-asset** |

#### Forex and Currency Market Sentiment (NEW SUBSECTION 2.3.4)

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Dakalbab et al. (2025) | ✅ NEW | Multimodal forex prediction with attention | **Draft-1: Attention mechanisms** |
| Olaiyapo (2024) | ✅ NEW | News/media sentiment → forex trading signals | **Draft-1: Forex trading signals** |
| Gu & Song (2026) | ✅ NEW | Fine-tuned FinBERT for EUR/USD (84.33% accuracy) | **Draft-1: Currency-pair specific models** |
| Sibande et al. (2023) | ✅ NEW | Twitter sentiment → currency herding | **Draft-1: Behavioral forex** |
| Fatouros et al. (2023) | ✅ NEW | ChatGPT forex sentiment (35% better than FinBERT) | **Draft-1: LLM forex applications** |

#### Commodities Sentiment (NEW SUBSECTION 2.3.5)

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Shi (2025) | ✅ NEW | Gold/USD GARCH-MIDAS (18.7% error reduction) | **Draft-1: Commodity sentiment** |

#### Draft-1 Action Items: Cross-Asset Analysis

- [x] Create dedicated subsection 2.3 for cross-asset analysis
- [x] Add forex and currency sentiment subsection (2.3.4)
- [x] Add commodities sentiment subsection (2.3.5)
- [ ] Synthesize Transfer Entropy methods from Caferra (2022)
- [ ] Integrate Wang et al. (2024) for momentum transmission evidence
- [ ] Build case for portfolio-level sentiment aggregation

---

### 2.4 Market Regime Detection

**Current status:** ✅ Well-covered with real-time systems added

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Zhang et al. (2020) | ✅ Cited | Explainable ML, 22.53% annual returns, Sharpe 1.06 | Benchmark results |
| Shu et al. (2024) | ✅ Cited | Statistical jump model for regimes | Methodology reference |
| Suárez-Cetrulo et al. (2023) | ✅ Cited | Systematic review (140 studies) | Comprehensive background |

#### Real-Time and High-Frequency Systems (NEW SUBSECTION 2.4.4)

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Cai, Tang & Chen (2024) | ✅ NEW | Real-time sentiment → high-frequency returns (MF-EEMD-ML) | **Draft-1: Real-time methodology** |

#### Draft-1 Action Items: Regime Detection

- [ ] Expand on limitations of traditional regime detection
- [ ] Create comparison table: VIX-based vs. sentiment-based detection
- [ ] Add real-time systems subsection with Cai et al. (2024)

---

### 2.5 Literature Reviews and Surveys (NEW SECTION)

**Purpose:** Contextualize contribution within existing survey landscape

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Ehsan et al. (2025) | ✅ NEW | Systematic review: NLP for price prediction | **Draft-1: Literature context** |
| Sathish & Jamalpur (2025) | ✅ NEW | ML + NLP-based sentiment integration survey | **Draft-1: Integration frameworks** |
| Ferrell & McInnes (2025) | ✅ NEW | RL + NLP integration for trading (22 papers) | **Draft-1: RL connections** |
| Kengmegni (2025) | ✅ NEW | Multi-level sentiment, limitations analysis | **Draft-1: Addressing limitations** |
| Todd, Bowden & Moshfeghi (2024) | ✅ NEW | Text-based sentiment synthesis, multimodal methods | **Draft-1: Future directions** |
| Shao et al. (2025) | ✅ NEW | HD-SURDLM framework, multi-source sentiment | **Draft-1: Dynamic modeling methods** |

#### Multi-Source Sentiment & Trading Applications (NEW SUBSECTION)

| Article | Citation Status | Key Contribution | Integration Notes |
|---------|-----------------|------------------|-------------------|
| Trushkovskyi (2025) | ✅ NEW | Twitter/Reddit → crypto trading (Granger causality) | **Draft-1: H1 evidence, trading bots** |
| Shao et al. (2025) | ✅ NEW | HD-SURDLM: 1.02% improvement in 1-day forecasts | **Draft-1: Gibbs sampling methodology** |
| Todd et al. (2024) | ✅ NEW | Multimodal (text-audio) for earnings calls | **Draft-1: Multimodal opportunities** |

---

## Hypothesis Support Matrix

### H1: Leading Indicator Hypothesis

**Hypothesis:** *Cross-asset sentiment provides a leading indicator for market regime shifts, preceding VIX-based detection by 1-5 trading days.*

| Evidence Source | Lead Time | Asset Class | Strength |
|-----------------|-----------|-------------|----------|
| Bollen et al. (2011) | 2-6 days | Equities (DJIA) | Strong |
| Kraaijeveld & De Smedt (2020) | 1-3 days | Crypto | Strong |
| Renault (2017) | Next-day | Equities | Moderate |
| Caferra (2022) | Not specified | Crypto↔Equity | Moderate |
| Olaiyapo (2024) | Trading signals | Forex | Strong |
| Gu & Song (2026) | Forecasting | Forex (EUR/USD) | Strong |
| Sibande et al. (2023) | Not specified | Currency markets | Moderate |
| Cai, Tang & Chen (2024) | Real-time | High-frequency equities | Strong |
| Amin et al. (2024) | Daily | Equities + macro | Strong |
| Trushkovskyi (2025) | Daily | Crypto (Bitcoin) | Strong |

**Gap Analysis:** ✅ FULLY ADDRESSED - All major asset classes covered

---

### H2: Divergence Signal Hypothesis

**Hypothesis:** *Sentiment divergence between asset classes signals impending regime transitions.*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Caferra (2022) | Sentiment mediates cross-market relationships | Moderate |
| Wang et al. (2024) | Cross-asset momentum transmission mechanisms | Strong |
| Pankwaen et al. (2025) | Multi-asset optimization (29.52% returns) | Strong |
| Shi (2025) | Gold/USD divergence patterns | Moderate |
| Shao et al. (2025) | HD-SURDLM multi-source sentiment dynamics | Strong |

**Gap Analysis:** ✅ Significantly improved with cross-asset and multi-source papers

---

### H3: Network Effect Hypothesis

**Hypothesis:** *Sentiment connectedness intensity correlates with regime transition probability.*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Cao et al. (2025) | High connectedness → crash risk | Strong |
| Nyakurukwa & Seetharam (2025) | DJIA sentiment highly interconnected | Moderate |
| Yang et al. (2025) | LLM-based cross-asset monitoring | Moderate |
| Sarfarazurrehman et al. (2025) | AI/ML for cross-asset risk (Sharpe 0.98) | Strong |
| Sibande et al. (2023) | Herding behavior in currency markets | Moderate |

**Gap Analysis:** ✅ Well-supported with network and herding behavior evidence

---

### H4: Ensemble Superiority Hypothesis

**Hypothesis:** *Ensemble transformers outperform single-model approaches across data sources.*

| Evidence Source | Finding | Strength |
|-----------------|---------|----------|
| Mishev et al. (2020) | Different models excel on different sources | Strong |
| Shen & Zhang (2024) | FinBERT beats general LLMs on financial text | Moderate |
| Kelly & Xiu (2023) | Comprehensive financial ML methodology | Strong |
| Micaletti (2019) | Relative sentiment for tactical allocation | Moderate |
| Fatouros et al. (2023) | ChatGPT 35% better than FinBERT on forex | Strong |
| Gu & Song (2026) | Fine-tuned FinBERT 84.33% accuracy | Strong |
| Ergun & Sefer (2025) | FinSentiment multi-model comparison | Strong |
| Nasiopoulos et al. (2025) | GPT-4o fine-tuning outperforms baselines | Strong |
| Baghavathi Priya et al. (2025) | FinBERT 89.6% accuracy | Strong |
| Todd et al. (2024) | Multimodal (text-audio) opportunities | Strong |

**Gap Analysis:** ✅ EXCELLENT - Multiple papers support ensemble/fine-tuned approach

---

## Literature Gap Analysis

### Previously Identified Gaps - Status Update

| Gap | Status | Resolution |
|-----|--------|------------|
| Forex Sentiment Analysis | ✅ ADDRESSED | 5 papers: Dakalbab, Olaiyapo, Gu & Song, Sibande, Fatouros |
| Commodities Sentiment | ✅ ADDRESSED | Shi (2025) - Gold/USD with GARCH-MIDAS |
| Multi-Asset Regime Detection | ✅ ADDRESSED | Wang, Yang, Pankwaen, Sarfarazurrehman |
| Real-Time Systems | ✅ ADDRESSED | Cai, Tang & Chen (2024) - MF-EEMD-ML |
| LLM Comparisons | ✅ ADDRESSED | 4 new papers: Ergun, Nasiopoulos, Mahendran, Baghavathi Priya |
| Crypto-Specific NLP | ✅ ADDRESSED | Roumeliotis et al. (2024), Trushkovskyi (2025) |

### Remaining Minor Gaps

1. **Fixed Income Sentiment** - Limited coverage (only through Yang et al. 2025 cross-asset paper)
2. **Real Estate Sentiment** - Only Sarfarazurrehman et al. (2025) case study
3. **Emerging Markets** - Limited to China (Wang et al. 2024) and Thailand (Pankwaen et al. 2025)

---

## Draft-1 Literature Review Outline

```markdown
2. Literature Review (Target: 5,000-7,000 words)

   2.1 Transformer Models in Financial Sentiment Analysis
       2.1.1 From Lexicons to BERT (Loughran-McDonald → FinBERT)
       2.1.2 Large Language Models (GPT, LLaMA, ChatGPT)
       2.1.3 Model Comparison and Selection Criteria
       2.1.4 Fine-Tuning Strategies and Domain Adaptation [NEW]
   
   2.2 Financial Sentiment and Market Prediction
       2.2.1 Foundational Work (Baker-Wurgler, Animal Spirits)
       2.2.2 Social Media as Predictive Signal
       2.2.3 Lead Time Evidence Synthesis
       2.2.4 Multi-Factor Sentiment Integration [NEW]
       2.2.5 Cryptocurrency-Specific Sentiment Analysis [NEW]
   
   2.3 Cross-Asset Sentiment Analysis [EXPANDED]
       2.3.1 Sentiment Spillover Mechanisms
       2.3.2 Transfer Entropy and Information Flow
       2.3.3 Network-Based Approaches
       2.3.4 Forex and Currency Market Sentiment [NEW]
       2.3.5 Commodities Sentiment [NEW]
       2.3.6 Multi-Asset Portfolio Applications [NEW]
   
   2.4 Market Regime Detection
       2.4.1 Traditional Approaches (VIX, HMM)
       2.4.2 Machine Learning Methods
       2.4.3 Sentiment-Based Regime Detection
       2.4.4 Real-Time and High-Frequency Systems [NEW]
       2.4.5 Limitations and Challenges [NEW]
       2.4.6 Explainable AI in Regime Detection [NEW]
   
   2.5 Research Hypotheses
       (Updated based on expanded review)
```

---

## Progress Tracker

| Section | Draft-0 Status | Draft-1 Target | Papers Integrated | Papers Added |
|---------|----------------|----------------|-------------------|--------------|
| 2.1 Transformers | 80% | 98% | 4 | +8 |
| 2.2 Sentiment/NLP | 75% | 95% | 8 | +4 |
| 2.3 Cross-Asset | 40% | 98% | 3 | +11 |
| 2.4 Regime Detection | 70% | 95% | 4 | +1 |
| Foundational | 70% | 95% | 3 | +2 |
| Surveys | 0% | 95% | 0 | +6 |
| **TOTAL** | **56%** | **96%** | **22** | **+32** |

---

## Key Metrics Summary

| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Total Papers | 48 | 51 | +3 |
| Scholarcy Summaries | 43 | 46 | +3 |
| Hypothesis Coverage | 96% | 98% | +2% |
| Asset Class Coverage | 6 | 6 | - |
| 2024-2025 Papers | 26 | 29 | +3 |
