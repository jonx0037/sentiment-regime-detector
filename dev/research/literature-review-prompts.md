# Literature Review Research Prompts

**Purpose:** Guide systematic literature search for MSDS 6210 Capstone Research Outline  
**Target:** 5-8 high-quality papers (peer-reviewed, 2015+) across 4 themes  
**Deadline:** January 15, 2026 (for Draft 0 bibliography)  
**Student:** Jonathan Rocha (<jrocha@smu.edu>)  
**GitHub:** github.com/jonx0037/sentiment-regime-detector  
**Project:** Cross-Asset Sentiment Regime Detector

Use these prompts with Google Scholar, Semantic Scholar, Connected Papers, or AI research assistants (Claude, Perplexity, Elicit).

---

## 🎯 Search Strategy Overview

**Goal:** Find 5-8 high-quality papers (peer-reviewed, 2015+) across 4 themes  
**Timeline:** Complete by Wednesday, January 15, 2026  
**Quality Criteria:**

- Published in reputable venues (IEEE, ACL, NeurIPS, Finance journals)
- Cited 20+ times (for papers >2 years old)
- Methodologically relevant (uses similar data/models)
- Addresses specific gap in your research

---

## Theme 1: Cross-Asset Sentiment & Spillover Effects (2-3 papers needed)

### Primary Search Query

```text
"cross-asset sentiment" OR "multi-asset sentiment" OR "sentiment spillover" OR "cross-market sentiment"
AND ("machine learning" OR "NLP" OR "transformer")
AND (stocks OR equity OR crypto OR cryptocurrency OR forex OR commodities)
```

### Targeted Prompts for AI Tools

**Prompt 1 (Perplexity/Elicit):**
> "Find academic papers published after 2015 on cross-asset sentiment analysis in financial markets. I'm specifically interested in research that analyzes sentiment across multiple asset classes (equities, crypto, forex, commodities) simultaneously, not just single-asset sentiment. Focus on papers using modern NLP or machine learning methods."

**Prompt 2 (Connected Papers):**
> Start with: **Ranco et al. (2015) - "The Effects of Twitter Sentiment on Stock Price Returns"**  
> Explore forward citations looking for papers that extend single-asset sentiment to multi-asset analysis

**Prompt 3 (Claude/ChatGPT):**
> "What are the most cited papers on sentiment contagion or sentiment spillover between different financial markets (e.g., equity markets affecting crypto markets)? I need papers that go beyond correlation studies and actually use sentiment as a predictive feature."

### Key Questions to Answer (Theme 1)

- Has anyone built a unified sentiment index across multiple asset classes?
- What methods exist for detecting sentiment spillover between markets?
- How do researchers handle asset-class-specific language differences?

---

## Theme 2: Transformer Models in Financial NLP (2-3 papers needed)

### Search Query for Transformer Models

```text
("FinBERT" OR "financial BERT" OR "financial transformers" OR "StockBERT" OR "CryptoBERT")
AND ("sentiment analysis" OR "sentiment classification")
AND (fine-tuning OR "transfer learning")
```

### Targeted Prompts for Transformer Models

**Prompt 1 (Google Scholar):**
> "Domain-specific transformer models for financial sentiment analysis"  
> Filters: Since 2019, sort by relevance

**Prompt 2 (Semantic Scholar):**
> "Compare the performance of FinBERT vs. general-purpose transformers (BERT, RoBERTa, GPT) on financial text classification tasks. Find papers that benchmark multiple models."

**Prompt 3 (Literature Review AI):**
> "I'm using an ensemble of FinBERT and RoBERTa for financial sentiment analysis. Find papers that:
>
> 1. Compare FinBERT to other financial NLP models
> 2. Use ensemble methods for sentiment classification
> 3. Fine-tune transformers on social media financial text (Reddit/Twitter)
>
> Prioritize papers with publicly available code or pre-trained models."

### Key Questions to Answer (Theme 2)

- What's the state-of-the-art architecture for financial sentiment on social media?
- How do ensemble methods compare to single-model approaches?
- What training data do top-performing models use?

---

## Theme 3: Market Regime Detection (2-3 papers needed)

### Search Query for Regime Detection

```text
("market regime" OR "regime detection" OR "regime switching" OR "risk-on risk-off")
AND ("machine learning" OR "deep learning" OR "LSTM" OR "random forest" OR "HMM")
AND (sentiment OR "behavioral finance" OR psychology)
```

### Targeted Prompts for Market Regime Detection

**Prompt 1 (Perplexity):**
> "What are the best machine learning methods for detecting market regime changes (Bull/Bear, Risk-On/Risk-Off transitions)? I'm looking for papers published after 2016 that use sentiment or behavioral indicators, not just price/volume data."

**Prompt 2 (Connected Papers):**
> Start with: **Nystrup et al. (2018) - "Regime-Based Versus Static Asset Allocation"**  
> Look for papers that incorporate sentiment as a regime-detection feature

**Prompt 3 (Research Assistant):**
> "Find papers that predict market regime transitions using leading indicators (not lagging price-based signals). I'm particularly interested in:
>
> - Sentiment-based regime detection
> - Using Hidden Markov Models (HMMs) or LSTM networks
> - Regime detection across multiple markets simultaneously
> - Validation against historical crisis periods (2008, 2020, 2022)"

### Key Questions to Answer (Theme 3)

- What's the standard way to label regime states (Risk-On/Off/Transition)?
- How far in advance can regimes be predicted (lead time)?
- Which features are most predictive of regime shifts?

---

## Theme 4: Social Media as Predictive Signal (1-2 papers needed)

### Search Query for Social Media Signals

```text
("Reddit" OR "Twitter" OR "social media") AND (sentiment OR opinion)
AND (stock OR cryptocurrency OR "financial markets")
AND (prediction OR forecasting OR "lead-lag")
```

### Targeted Prompts for Social Media Research

**Prompt 1 (Google Scholar):**
> "Social media sentiment predicts stock market movements"  
> Filters: 2017-2024, exclude news articles

**Prompt 2 (Semantic Scholar):**
> "Does Reddit r/wallstreetbets sentiment have predictive power for stock volatility or returns? Find quantitative studies that measure lead-lag relationships, not just correlation."

**Prompt 3 (AI Research Assistant):**
> "I need evidence that social media sentiment is a **leading indicator** (not coincident or lagging) for financial market movements. Find papers that:
>
> 1. Measure the time lag between sentiment shifts and price changes
> 2. Control for confounding variables (news events, earnings releases)
> 3. Use Reddit, Twitter, or StockTwits data
> 4. Report prediction accuracy or profitability metrics"

### Key Questions to Answer (Theme 4)

- What's the typical lead time for social media sentiment (hours? days?)?
- How does signal quality vary by platform (Reddit vs. Twitter vs. forums)?
- What are common pitfalls (bot accounts, spam, survivorship bias)?

---

## 📋 Paper Evaluation Checklist

For each candidate paper, assess:

- [ ] **Relevance:** Directly addresses one of the 4 themes above
- [ ] **Quality:** Published in reputable venue (IEEE, ACL, Finance journals, arXiv if recent)
- [ ] **Recency:** Published 2015 or later (prefer 2019+ for transformer papers)
- [ ] **Citation Count:** 20+ citations (if >2 years old), or highly relevant if recent
- [ ] **Methodology:** Uses methods/data similar to your project (transformers, social media, ML)
- [ ] **Reproducibility:** Ideally has code/data available (GitHub repo)
- [ ] **Gap Identification:** Explicitly mentions limitations that your research addresses

**Target:** 5-8 papers total, distributed roughly:

- 2-3 papers on cross-asset sentiment (Theme 1)
- 2-3 papers on transformers in finance (Theme 2)
- 2 papers on regime detection (Theme 3)
- 1-2 papers on social media as signal (Theme 4)

---

## 🔍 Recommended Search Tools

1. **Google Scholar** - Broadest coverage, good for citation tracking
   - Use: `site:scholar.google.com [your query]`
   - Filter by date range: 2015-2024

2. **Semantic Scholar** - AI-powered relevance ranking
   - Use: <https://www.semanticscholar.org>
   - Look for "Highly Influential Citations" badge

3. **Connected Papers** - Visual citation graphs
   - Use: <https://www.connectedpapers.com>
   - Start with a known paper (Bollen 2011, Araci 2019) and explore neighbors

4. **Perplexity AI** - Natural language search
   - Use the prompts above directly
   - Ask for DOIs or arxiv links

5. **Elicit** - AI research assistant
   - Use: <https://elicit.org>
   - Great for extracting key findings from multiple papers

6. **arXiv** - Preprints (for cutting-edge research)
   - Use: <https://arxiv.org/search/>
   - Categories: cs.CL (NLP), q-fin.CP (computational finance), stat.ML

---

## 📝 Note-Taking Template (Per Paper)

Create a file: `dev/research/literature-notes.md`

For each paper, record:

```markdown
### [Paper Title] (Author et al., Year)

**Citation:** [Full APA citation]
**DOI/Link:** [URL]
**Tags:** #cross-asset #transformers #regime-detection #social-media

**Key Findings:**
- [3-5 bullet points]

**Methodology:**
- Data sources: [e.g., Twitter, Reddit, news]
- Models/algorithms: [e.g., FinBERT, LSTM, Random Forest]
- Sample size: [e.g., 1M tweets, 2015-2020]

**Relevant to My Research:**
- [How does this relate to your cross-asset sentiment regime detector?]

**Gaps/Limitations:**
- [What doesn't this paper address that yours will?]

**Citation for Draft:**
> Author, A. B., & Author, C. D. (Year). Title of the paper. *Journal Name*, Volume(Issue), pages. https://doi.org/xxxxx
```

---

## 🚀 Action Plan

**Sunday (Jan 12):**

1. Run all 12 search queries above across 2-3 platforms
2. Download 10-15 candidate papers (PDFs)
3. Skim abstracts, create shortlist of 8-10 papers

**Monday (Jan 13):**

1. Read shortlisted papers in detail (30-45 min each)
2. Fill out note-taking template for each
3. Select final 5-8 papers for citation

**Tuesday (Jan 14):**

1. Begin drafting literature review section 2
2. Write 1-2 paragraphs per paper, grouped by theme
3. Identify gaps that lead to your research question

**Wednesday (Jan 15):**

1. Complete literature review draft
2. Add all APA citations to references section
3. Proofread and check citation format

---

## ⚡ Pro Tips

1. **Start with recent survey papers** - They cite dozens of relevant works
   - Search: "survey financial sentiment analysis" or "review market regime detection"

2. **Use "cited by" feature** - Find papers that cite your initial candidates
   - Google Scholar → click "Cited by XXX" under each result

3. **Check author's other work** - If you find one relevant paper, check what else that author published
   - Example: If you like a FinBERT paper, check Dogu Araci's other publications

4. **Look for code repositories** - Papers with GitHub repos are gold
   - Search: `[paper title] site:github.com`

5. **Use Zotero browser extension** - One-click paper saving with auto-filled metadata
   - Install: <https://www.zotero.org/download/>

6. **Don't over-perfect** - You can always add more citations in Draft 1
   - Draft 0 goal: 12-20 citations total (3-4 per subsection)
   - Draft 1 goal: 25-40 citations total

---

## 📚 Starter Bibliography (Already in Draft 0)

These are your baseline references—expand from here:

1. **Araci (2019)** - FinBERT
2. **Bollen et al. (2011)** - Twitter sentiment → DJIA
3. **Loughran & McDonald (2011)** - Finance sentiment lexicons
4. **Renault (2017)** - Reddit sentiment → volatility
5. **Nystrup et al. (2018)** - Regime-switching models

**Next steps:** Find 3-5 more papers that fill gaps in cross-asset sentiment and social media predictive power.

---

**Good luck! Remember: Done is better than perfect for Draft 0.**
