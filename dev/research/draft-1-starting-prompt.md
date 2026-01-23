# Draft-1 Starting Prompt

**Use this prompt to start a new chat session for composing Draft-1**

---

## Context Prompt

```
I'm working on my MSDS Capstone at SMU. I need help composing Draft-1 of my research paper: "Cross-Asset Sentiment Regime Detector: Automating Market Psychology Analysis Through Multi-Source NLP."

**Project Repository:** github.com/jonx0037/sentiment-regime-detector
**Workspace:** /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone

## Current State

Draft-0 (completed January 12, 2026) established:
- Abstract, Introduction, and Methods sections
- Literature review covering 22 papers
- Four research hypotheses (H1-H4)

For Draft-1, I need to EXPAND the Literature Review (Section 2) by integrating 12 additional papers that address previously identified gaps.

## Key Files to Read

1. `dev/research/draft-0.md` — Current draft (449 lines)
2. `dev/research/literature-mapping.md` — Maps papers to sections with action items
3. `course_files/research/article-index.md` — Catalog of all 34 papers

## Literature Review Structure for Draft-1

```
2. Literature Review

   2.1 Transformer Models in Financial Sentiment Analysis
       2.1.1 From Lexicons to BERT (Loughran-McDonald → FinBERT)
       2.1.2 Large Language Models (GPT, LLaMA, ChatGPT)
       2.1.3 Model Comparison and Selection Criteria
   
   2.2 Financial Sentiment and Market Prediction
       2.2.1 Foundational Work (Baker-Wurgler, Animal Spirits)
       2.2.2 Social Media as Predictive Signal
       2.2.3 Cryptocurrency-Specific Sentiment Analysis
       2.2.4 Lead Time Evidence Synthesis
   
   2.3 Cross-Asset Sentiment Analysis [EXPANDED]
       2.3.1 Sentiment Spillover Mechanisms
       2.3.2 Transfer Entropy and Information Flow
       2.3.3 Network-Based Approaches
       2.3.4 Forex and Currency Market Sentiment [NEW]
   
   2.4 Market Regime Detection
       2.4.1 Traditional Approaches (VIX, HMM)
       2.4.2 Machine Learning Methods
       2.4.3 Sentiment-Based Regime Detection
       2.4.4 Real-Time and High-Frequency Systems [NEW]
   
   2.5 Research Hypotheses
       (Updated based on expanded review)
```

## 12 Papers to Integrate

### High Priority (Core additions)
| Paper | Section | Key Contribution |
|-------|---------|------------------|
| Wang et al. (2024) | 2.3 | Cross-asset momentum transmission |
| Yang et al. (2025) | 2.3 | LLM cross-asset risk monitoring |
| Dakalbab et al. (2024) | 2.3.4 | Multimodal forex prediction |
| Olaiyapo (2024) | 2.3.4 | Forex trading signals from sentiment |
| Gu & Song (2024) | 2.3.4 / 2.1 | FinBERT for exchange rate forecasting |
| Cai, Tang & Chen (2024) | 2.4.4 | Real-time high-frequency prediction |
| Fatouros et al. (2024) | 2.1.2 | ChatGPT financial sentiment |
| Kelly & Xiu (2023) | 2.4 | Financial ML methodology review |

### Medium Priority (Supporting evidence)
| Paper | Section | Key Contribution |
|-------|---------|------------------|
| Pankwaen et al. (2025) | 2.3 | Multi-asset global optimization |
| Sarfarazurrehman et al. (2025) | 2.3 | AI/ML cross-asset risk analysis |
| Sibande et al. (2024) | 2.3.4 | Twitter currency market herding |
| Micaletti (2019) | 2.2 | Tactical allocation with sentiment |

## Gaps Now Addressed

- ✅ **Forex Sentiment Analysis** — 4 papers (Dakalbab, Olaiyapo, Gu & Song, Sibande)
- ✅ **Real-Time Systems** — 2 papers (Cai et al., Fatouros et al.)
- ✅ **Multi-Asset Integration** — 4 papers (Wang, Yang, Pankwaen, Sarfarazurrehman)
- ⚠️ **Commodities** — Still limited (lower priority)

## Scholarcy Summaries Available

All 12 new papers have Scholarcy summaries in:
`course_files/research/full-articles/Scholarcy-Article-Summaries/`

These contain key findings, methodology, and quotable passages for integration.

## Writing Guidelines

1. **Academic tone** — Third person, formal language
2. **Citation style** — Author (Year) in-text, APA format
3. **Integration approach** — Synthesize findings, don't just summarize
4. **Connect to hypotheses** — Each paper should strengthen H1-H4 evidence
5. **Identify remaining gaps** — Position novel contribution clearly

## Expected Output

Revised Section 2 (Literature Review) approximately 3,000-4,000 words that:
1. Integrates all 12 new papers naturally into existing narrative
2. Adds new subsections 2.3.4 (Forex) and 2.4.4 (Real-Time)
3. Updates gap analysis to reflect addressed gaps
4. Strengthens hypothesis justifications with new evidence

Please start by reading the key files, then propose an outline for the expanded literature review before writing.
```

---

## Quick Copy Version

For quick start, copy this condensed prompt:

```
I need help composing Draft-1 of my MSDS Capstone paper on Cross-Asset Sentiment Regime Detection.

Workspace: /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
Repo: github.com/jonx0037/sentiment-regime-detector

Please read these files first:
1. dev/research/draft-0.md (current draft)
2. dev/research/literature-mapping.md (paper-to-section mapping)
3. course_files/research/article-index.md (34-paper catalog)

Task: Expand Section 2 (Literature Review) by integrating 12 new papers that address forex sentiment, real-time systems, and cross-asset integration gaps. The Scholarcy summaries in course_files/research/full-articles/Scholarcy-Article-Summaries/ contain key findings.

Start by proposing an outline, then write the expanded sections.
```
