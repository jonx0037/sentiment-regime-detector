# Draft-1 Starting Prompt

## Use this prompt to start a new chat session for composing Draft-1

**Last Updated:** January 24, 2026  
**Research Library:** 55+ papers with PDFs, 40+ Scholarcy summaries

---

## Context Prompt

I'm working on my MSDS Capstone at SMU. I need help composing Draft-1 of my research paper: "Cross-Asset Sentiment Regime Detector: Automating Market Psychology Analysis Through Multi-Source NLP."

**Project Repository:** github.com/jonx0037/sentiment-regime-detector
**Workspace:** /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone

## Current State

Draft-0 (completed January 12, 2026) established:
- Abstract, Introduction, and Methods sections
- Literature review covering 22 papers
- Four research hypotheses (H1-H4)

For Draft-1, I need to SUBSTANTIALLY EXPAND the Literature Review (Section 2) by integrating 30+ additional papers that comprehensively address all previously identified gaps.

## Key Files to Read

1. \`course_files/paper-drafts/draft-0.md\` — Current draft (449 lines)
2. \`course_files/paper-drafts/literature-mapping.md\` — Maps papers to sections with action items
3. \`course_files/research/article-index.md\` — Catalog of all papers

## Research Library Resources

### Zotero Exports (Full Bibliography)
Located in: \`course_files/research/full-articles/zotero-exports/\`
- \`Capstone-zotero-export_1-23-26_A.csv\` — Primary bibliography (30+ papers)
- \`Capstone-zotero-export_1-23-26_B.csv\` — Extended bibliography (25+ papers)

### Full-Text PDFs (50+ papers)
Located in: \`course_files/research/full-articles/core-papers/\`

### Scholarcy Summaries (40+ structured summaries)
Located in: \`course_files/research/summaries/\`
Each summary contains: key concepts, quotable passages, methodology details, and structured findings.

## Literature Review Structure for Draft-1

2. Literature Review

   2.1 Transformer Models in Financial Sentiment Analysis
       2.1.1 From Lexicons to BERT (Loughran-McDonald → FinBERT)
       2.1.2 Large Language Models (GPT, LLaMA, ChatGPT, FinLlama)
       2.1.3 Model Comparison and Selection Criteria
       2.1.4 Domain-Specific Fine-Tuning Approaches [NEW]
   
   2.2 Financial Sentiment and Market Prediction
       2.2.1 Foundational Work (Baker-Wurgler, Animal Spirits)
       2.2.2 Social Media as Predictive Signal
       2.2.3 Cryptocurrency-Specific Sentiment Analysis
       2.2.4 Lead Time Evidence Synthesis
       2.2.5 Limitations and Short-Term Prediction Challenges [NEW]
   
   2.3 Cross-Asset Sentiment Analysis [MAJOR EXPANSION]
       2.3.1 Sentiment Spillover Mechanisms
       2.3.2 Transfer Entropy and Information Flow
       2.3.3 Network-Based Approaches & Sentiment Connectedness
       2.3.4 Forex and Currency Market Sentiment [NEW - 5 papers]
       2.3.5 Multi-Asset Portfolio Integration [NEW - 4 papers]
       2.3.6 Commodities (Gold, Oil) Sentiment [NEW]
   
   2.4 Market Regime Detection [MAJOR EXPANSION]
       2.4.1 Traditional Approaches (VIX, HMM)
       2.4.2 Machine Learning Methods (Clustering, Jump Models)
       2.4.3 Sentiment-Based Regime Detection
       2.4.4 Real-Time and High-Frequency Systems [NEW - 3 papers]
       2.4.5 Explainable AI for Regime Classification [NEW]
       2.4.6 Risk Management Integration [NEW]
   
   2.5 Research Gaps and Hypotheses
       2.5.1 Synthesis of Literature Gaps
       2.5.2 Updated Research Hypotheses (H1-H4)
       2.5.3 Novel Contribution Positioning

## Papers to Integrate by Theme (30+ New Papers)

### Theme 1: LLM & Transformer Advances (Section 2.1)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Fatouros et al. (2023) | ChatGPT 35% better than FinBERT for forex sentiment | \`transforming-sentiment-analysis-in-the-financial-domain-with-ChatGPT_*\` |
| Konstantinidis et al. (2024) | FinLlama for algorithmic trading, LoRA fine-tuning | \`finllama-financial-sentiment-classification-*\` |
| Delgadillo et al. (2024) | FinSoSent domain-specific LLM pre-training | \`finsosent-advancing-financial-market-*\` |
| Luo & Gong (2024) | LLaMA-2 fine-tuning for financial sentiment | \`luo-w-and-gong-d-2024-pre-trained-*\` |
| Nasiopoulos et al. (2025) | Comparative study: GPT-4o vs BERT vs FinBERT | \`Financial_Sentiment_Analysis_and_Classification-*\` |
| Ergun & Sefer (2025) | FinSentiment transfer learning framework | \`FinSentiment_-_Predicting_Financial_Sentiment-*\` |
| Mahendran et al. (2025) | BERT vs FinBERT vs LLM review | \`Comparative_Advances_in_Financial_Sentiment*\` |
| Sun et al. (2025) | Dictionary knowledge + neutral features in BERT | \`financial-sentiment-analysis-for-pre-trained-*\` |
| Shen & Zhang (2024) | GPT-4o vs FinBERT on news/reports | \`Financial_Sentiment_Analysis_on_News_and_Reports-*\` |

### Theme 2: Forex & Currency Market Sentiment (Section 2.3.4)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Dakalbab et al. (2025) | Multimodal forex prediction with cross-modal attention | \`advancing-forex-prediction-through-multimodal_*\` |
| Olaiyapo (2024) | Forex trading signals from news/social media sentiment | \`applying-news-and-media-sentiment-analysis-*\` |
| Gu & Song (2026) | Fine-tuned FinBERT for EUR/USD forecasting (84.33% accuracy) | \`enhancing-exchange-rate-forecasting-with-*\` |
| Sibande et al. (2023) | Twitter sentiment → currency market herding behavior | \`investor-sentiman-and-anti-herding-*\` |
| Fatouros et al. (2023) | ChatGPT for forex sentiment (36% higher correlation) | (same as above) |

### Theme 3: Cross-Asset & Multi-Market Analysis (Section 2.3.5)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Wang et al. (2024) | Cross-asset momentum transmission (China stocks/bonds) | N/A (use Zotero abstract) |
| Yang et al. (2025) | LLM framework for real-time cross-asset risk monitoring | N/A (use Zotero abstract) |
| Pankwaen et al. (2025) | Global cross-market optimization (39 stocks + BTC) | N/A (use Zotero abstract) |
| Sarfarazurrehman et al. (2025) | AI/ML for cross-asset risk (real estate + equities) | N/A (use Zotero abstract) |
| Caferra (2022) | Sentiment spillover crypto ↔ stocks via Transfer Entropy | \`caferra-2022-physica-a-crypto-equity-*\` |

### Theme 4: Sentiment Networks & Crash Risk (Section 2.3.3)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Cao et al. (2025) | Sentiment connectedness → crash risk (entropy methods) | \`cao-et-al-2025-entropy-sentiment-connectedness-*\` |
| Nyakurukwa & Seetharam (2025) | DJIA sentiment network mapping | \`nyakurukwa-and-seetharam-2025-financial-*\` |

### Theme 5: Regime Detection & ML Methods (Section 2.4)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Shu, Yu & Mulvey (2024) | Statistical Jump Models for regime switching | \`downside-risk-reduction-using-regime-switching-*\` |
| Zhang, Yi & Chen (2020) | Explainable ML for regime-based asset allocation | \`Explainable_Machine_Learning_for_Regime-Based-*\` |
| Suárez Cetrulo et al. (2024) | ML for financial prediction under regime change | \`machine-learning-for-financial-prediction-under-*\` |
| Kelly & Xiu (2023) | Financial Machine Learning methodology review | N/A (use Zotero abstract) |
| Micaletti (2019) | Relative sentiment for tactical asset allocation | N/A (use Zotero abstract) |

### Theme 6: Real-Time & High-Frequency Systems (Section 2.4.4)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Cai, Tang & Chen (2024) | Real-time sentiment → high-frequency returns (MF-EEMD-ML) | \`can-real_time-investor-sentiment-help-predict-*\` |
| Renault (2017) | Intraday StockTwits sentiment → S&P 500 returns | \`renault-2017-intraday-online-investor-sentiment-*\` |
| Various (2025) | Time-varying dynamics with LLM | \`revisiting-time-varying-dynamics-*\` |

### Theme 7: Cryptocurrency Sentiment (Section 2.2.3)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Roumeliotis et al. (2024) | LLM vs NLP for crypto sentiment (GPT-4, BERT, FinBERT) | \`LLMs_and_NLP_Models_in_Cryptocurrency-*\` |
| Kraaijeveld & De Smedt (2020) | Twitter sentiment → crypto prices (Granger causality) | \`kraaijeveld-de-smedt-2020-*\` |
| Raheman et al. | Social media sentiment → Bitcoin prediction | \`social-media-sentiment-analysis-for-cryptocurrency-*\` |
| Trushkovskyi (2024) | Crypto trading models from sentiment | \`application-of-social-media-sentiment-*\` |

### Theme 8: Commodities Sentiment (Section 2.3.6)

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Shi (2025) | Gold/Dollar sentiment with GARCH-MIDAS | \`Understanding_Gold_and_Dollar_Price_Movements-*\` |
| Ehsan et al. (2025) | NLP for gold, crude oil price prediction | \`financial-news-sentiment-analysis-using-nlp-*\` |

### Theme 9: Foundational & Survey Papers

| Paper | Key Contribution | Summary File |
| --- | --- | --- |
| Baker & Wurgler (2007) | Investor sentiment in stock markets (foundational) | \`baker-wurgler-2007-investor-sentiment-*\` |
| Bollen, Mao & Zeng (2011) | Twitter mood predicts DJIA (86.7% accuracy) | \`bollen-mao-zeng-2011-twitter-mood-*\` |
| Loughran & McDonald (2011) | Finance-specific lexicons | \`loughran-mcdonald-2011-when-is-a-liability-*\` |
| Mishev et al. (2020) | Lexicons to transformers evaluation | \`Evaluation_of_Sentiment_Analysis_in_Finance-*\` |
| Sathish & Jamalpur (2025) | ML + NLP integration survey | \`A_Comprehensive_Survey_on_Enhancing_Stock_Market-*\` |
| Ferrell & McInnes (2025) | RL + NLP for trading survey | \`A_Comprehensive_Survey_on_the_Integration_of_RL-*\` |
| Kengmegni (2025) | Limitations of short-term sentiment prediction | \`Limitations_of_News_Sentiment_Analysis-*\` |

## Gaps Now Comprehensively Addressed

- ✅ **Forex Sentiment Analysis** — 5 papers (Dakalbab, Olaiyapo, Gu & Song, Sibande, Fatouros)
- ✅ **Real-Time Systems** — 3 papers (Cai et al., Renault, time-varying dynamics)
- ✅ **Multi-Asset Integration** — 5 papers (Wang, Yang, Pankwaen, Sarfarazurrehman, Caferra)
- ✅ **LLM Comparative Analysis** — 9 papers (ChatGPT, FinLlama, FinSoSent, GPT-4 studies)
- ✅ **Regime Detection ML** — 4 papers (Jump Models, Explainable ML, Kelly & Xiu)
- ✅ **Sentiment Networks** — 3 papers (Cao crash risk, Nyakurukwa networks, entropy methods)
- ✅ **Cryptocurrency** — 4 papers (Roumeliotis, Kraaijeveld, Raheman, Trushkovskyi)
- ✅ **Commodities** — 2 papers (Shi gold/dollar, Ehsan commodities)
- ✅ **Limitations/Challenges** — 2 papers (Kengmegni short-term limits, neutral sentiment issues)

## Writing Guidelines

1. **Academic tone** — Third person, formal language
2. **Citation style** — Author (Year) in-text, APA format
3. **Integration approach** — SYNTHESIZE findings thematically, don't just summarize individual papers
4. **Connect to hypotheses** — Each section should build evidence for H1-H4
5. **Identify remaining gaps** — Position novel contribution clearly
6. **Use Scholarcy summaries** — Extract key quotes and methodology details
7. **Cross-reference Zotero** — Use CSVs for accurate citations and abstracts

## Expected Output for Draft-1

Revised Section 2 (Literature Review) approximately **5,000-7,000 words** that:

1. Integrates 30+ new papers naturally into an expanded thematic narrative
2. Adds new subsections: 2.1.4, 2.2.5, 2.3.4, 2.3.5, 2.3.6, 2.4.4, 2.4.5, 2.4.6
3. Provides a comprehensive gap analysis showing how this research addresses remaining gaps
4. Strengthens all four hypothesis justifications with extensive new evidence
5. Positions the novel contribution as addressing the cross-asset regime detection gap that NO existing paper fully covers

Please start by:
1. Reading \`course_files/paper-drafts/draft-0.md\` (current draft)
2. Scanning the Scholarcy summaries in \`course_files/research/summaries/\` for key themes
3. Proposing a detailed outline for the expanded literature review
4. Writing the expanded sections with proper citations

---

## Quick Copy Version (Condensed)

For a quick session start, copy this condensed prompt:

```markdown
I need help composing Draft-1 of my MSDS Capstone paper on Cross-Asset Sentiment Regime Detection.

**Workspace:** /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
**Repo:** github.com/jonx0037/sentiment-regime-detector

## Research Library (Updated Jan 24, 2026)
- 55+ papers in \`course_files/research/full-articles/core-papers/\`
- 40+ Scholarcy summaries in \`course_files/research/summaries/\`
- Zotero exports in \`course_files/research/full-articles/zotero-exports/\`

## Please read these files first:
1. \`course_files/paper-drafts/draft-0.md\` — Current draft (449 lines)
2. \`course_files/paper-drafts/draft-1-starting-prompt.md\` — Full context with paper mappings
3. Scan Scholarcy summaries for key themes

## Task
Expand Section 2 (Literature Review) from ~2,000 to ~6,000 words by integrating 30+ new papers across these themes:
- LLM advances (FinLlama, ChatGPT, FinSoSent)
- Forex sentiment (Dakalbab, Gu & Song, Sibande)
- Cross-asset analysis (Wang, Yang, Caferra spillovers)
- Regime detection (Jump Models, Explainable ML)
- Real-time systems (Cai high-frequency, Renault intraday)
- Sentiment networks (Cao crash risk, Nyakurukwa)

Start by proposing an outline, then write the expanded sections with proper APA citations.
```

---

## Session Checklist

Before starting work, verify:

- [ ] Read \`course_files/paper-drafts/draft-0.md\` for current state
- [ ] Confirm access to \`course_files/research/summaries/\` (40+ files)
- [ ] Confirm access to Zotero CSVs for accurate citations
- [ ] Review literature structure in this prompt
- [ ] Understand the four hypotheses (H1-H4) to connect evidence

## Paper Count Summary

| Category | Papers | Status |
|----------|--------|--------|
| Transformer/LLM Models | 12 | ✅ Ready |
| Forex/Currency | 5 | ✅ Ready |
| Cross-Asset | 5 | ✅ Ready |
| Sentiment Networks | 3 | ✅ Ready |
| Regime Detection | 5 | ✅ Ready |
| Real-Time/HF | 3 | ✅ Ready |
| Cryptocurrency | 5 | ✅ Ready |
| Commodities | 2 | ✅ Ready |
| Foundational/Surveys | 8 | ✅ Ready |
| **TOTAL** | **48+** | ✅ |

---

## Key Citations Quick Reference

### Foundational Papers
- Baker & Wurgler (2007) - Investor sentiment theory
- Loughran & McDonald (2011) - Finance-specific lexicons
- Bollen, Mao & Zeng (2011) - Twitter predicts DJIA (86.7%)
- Araci (2019) - FinBERT introduction

### Transformer/LLM Models
- Mishev et al. (2020) - Lexicons to transformers evaluation
- Fatouros et al. (2023) - ChatGPT 35% better than FinBERT
- Konstantinidis et al. (2024) - FinLlama with LoRA
- Delgadillo et al. (2024) - FinSoSent
- Nasiopoulos et al. (2025) - GPT-4o vs FinBERT comparison

### Cross-Asset Analysis
- Caferra (2022) - Crypto-equity sentiment spillover
- Wang et al. (2024) - Cross-asset momentum
- Yang et al. (2025) - LLM cross-asset risk monitoring
- Cao et al. (2025) - Sentiment connectedness → crash risk

### Forex Sentiment
- Sibande et al. (2023) - Twitter → currency herding
- Olaiyapo (2024) - Forex trading signals
- Dakalbab et al. (2025) - Multimodal forex prediction
- Gu & Song (2026) - FinBERT for EUR/USD (84.33%)

### Regime Detection
- Zhang, Yi & Chen (2020) - Explainable ML for regimes
- Shu, Yu & Mulvey (2024) - Statistical Jump Models
- Suárez Cetrulo et al. (2024) - ML under regime change

### Real-Time Systems
- Renault (2017) - Intraday StockTwits → S&P 500
- Cai, Tang & Chen (2024) - High-frequency prediction

