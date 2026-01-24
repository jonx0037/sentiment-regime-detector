# Cross-Asset Sentiment Regime Detector: Automating Market Psychology Analysis Through Multi-Source NLP

**Author:** Jonathan Rocha (<jrocha@smu.edu>)  
**Advisor:** [Searching - TBD]  
**Affiliation:** Master of Science in Data Science, Southern Methodist University, Dallas, TX 75275 USA  
**GitHub:** github.com/jonx0037/sentiment-regime-detector  
**Date:** January 12, 2026

---

Jonathan Rocha¹, [Advisor Name]¹
¹ Master of Science in Data Science, Southern Methodist University, Dallas, TX 75275 USA
<jrocha@smu.edu>

## Abstract

Market regime shifts often precede measurable price movements, driven by changes in collective market psychology. This research develops an automated system for detecting market regime transitions through cross-asset sentiment analysis. By applying ensemble transformer models (FinBERT, RoBERTa) to financial social media, news, and forum data across equities, crypto, forex, and commodities, we construct asset-class-specific sentiment indices. These indices feed a regime classification model that identifies Risk-On, Risk-Off, and Transition states. We hypothesize that sentiment-based regime detection will identify market transitions 1-5 trading days before traditional volatility-based indicators (VIX thresholds), providing a leading signal for portfolio risk management. The system is validated through backtesting against historical market events (COVID-19 crash, 2021 bull run, 2022 bear market) and deployed as a real-time dashboard with sentiment visualization, regime indicators, and cross-asset divergence alerts. This research democratizes institutional-grade sentiment analysis and establishes a framework for mapping multi-source sentiment patterns to macroeconomic regime states.

## 1. Introduction

### Motivation

Financial markets operate in distinct psychological regimes characterized by collective risk appetite and sentiment. Traditional technical indicators (moving averages, RSI, VIX) are lagging—they reflect regime changes after they've already occurred in price data. However, market psychology shifts often manifest first in textual data: social media sentiment, news tone, and forum discussions. The 2021 GameStop short squeeze, the 2020 COVID crash, and the 2022 crypto winter all exhibited distinct sentiment patterns before, during, and after regime transitions.

Current sentiment analysis tools either focus on single asset classes or provide only rudimentary keyword-based scoring. No existing system aggregates cross-asset sentiment to detect systematic regime shifts applicable to portfolio-level risk management.

### Problem Statement

This research addresses three key limitations in current market sentiment analysis:

1. **Single-Asset Focus:** Existing tools analyze individual securities rather than cross-asset market psychology
2. **Manual Integration:** Sentiment must be manually interpreted alongside technical indicators
3. **Limited Accessibility:** Institutional-grade sentiment tools (Bloomberg, RavenPack) cost $20K+/year

This research aims to develop an automated, cross-asset sentiment analysis system that identifies market regime transitions as a leading indicator, accessible through an intuitive web interface.

### Research Contributions

1. **Methodological:** Novel application of ensemble transformers to multi-source, cross-asset sentiment aggregation
2. **Practical:** Open-source system democratizing institutional-grade sentiment analysis
3. **Theoretical:** Framework for mapping sentiment patterns to macroeconomic regime states

### Paper Structure

Section 2 reviews related work in financial sentiment analysis, NLP for finance, and market regime detection. Section 3 details our data sources and collection methodology. Section 4 describes the sentiment extraction and regime classification models. Section 5 presents [will present] validation results and backtesting performance. Section 6 discusses implications, limitations, and future work.

## 2. Literature Review

### 2.1 Transformer Models in Financial Sentiment Analysis

The application of pre-trained language models has revolutionized financial sentiment analysis. Traditional lexicon-based approaches (Loughran & McDonald, 2011) identified finance-specific sentiment words but lacked contextual understanding. The introduction of BERT-based models addressed this limitation through transfer learning and contextual embeddings.

FinBERT (Araci, 2019) represents a breakthrough in domain-specific sentiment analysis, achieving state-of-the-art results with a 15% increase in accuracy over previous methods. Critically, FinBERT outperformed baseline models even when trained on only 500 examples, demonstrating the effectiveness of pre-trained language models with limited labeled data. The model was fine-tuned on financial news and analyst reports, learning finance-specific language nuances that general-purpose models miss.

Mishev et al. (2020) provided a comprehensive evaluation of sentiment analysis techniques in finance, comparing lexicon-based methods to transformer models. Their systematic review demonstrated that transformer models significantly outperform traditional approaches in both accuracy and contextual understanding, particularly for complex financial discourse containing sarcasm, conditional statements, and domain-specific terminology.

Recent advances have expanded beyond FinBERT to larger language models. Liu et al. (2024) reviewed the application of large language models (LLMs) to financial sentiment analysis, demonstrating that LLMs enhance sentiment extraction capabilities while providing better generalization across different financial text types (news, social media, earnings calls). Their work highlighted datasets and methodologies for leveraging LLMs in financial contexts, showing consistent improvements over traditional methods.

### 2.2 Financial Sentiment Analysis and NLP

**Foundational Work:**
Market sentiment has long been recognized as a driver of asset prices, dating back to Keynes' (1973) concept of "animal spirits", first introduced circa 1936. Modern computational approaches began with simple lexicon-based methods (Loughran & McDonald, 2011), which identified finance-specific sentiment words that differ from general English (e.g., "liability" is negative in finance, neutral otherwise).

**Deep Learning Approaches:**
The advent of transformer models revolutionized financial NLP. Araci (2019) introduced FinBERT, a finance-specific BERT variant fine-tuned on financial news and analyst reports, achieving state-of-the-art performance on financial sentiment classification with 15% accuracy improvement over previous methods. The paper also evaluated comparable transfer learning approaches including ELMo (providing contextualized word representations) and ULMFit (using language model pre-training), demonstrating that domain-specific pre-training substantially improves performance even with limited labeled data (≤500 examples).

Mishev et al. (2020) conducted a comprehensive evaluation of transformer architectures for financial sentiment analysis, comparing:

- **BERT variants:** BERT, RoBERTa, XLNet, ALBERT, and DistilBERT (a distilled version retaining >95% of BERT's accuracy with 40% fewer parameters)
- **Attention mechanisms:** Multi-headed self-attention architectures enabling parallel processing of financial texts
- **Performance findings:** NLP transformers significantly outperformed traditional lexicon-based and word embedding approaches, with BART and ALBERT-xxlarge achieving the highest performance (Matthews Correlation Coefficient scores of 0.895 and 0.881 respectively)

Recent advances in Large Language Models (LLMs) extend transformer capabilities further. Liu et al. (2024) categorized LLMs into three architectural types:

1. **Encoder-only models** (e.g., BERT variants): Process input text into hidden representations for classification tasks
2. **Encoder-decoder models** (e.g., FINMEM): Integrate encoder and decoder components for text generation and financial analysis
3. **Decoder-only models** (e.g., GPT series): Generate output text directly, with applications in financial forecasting and sentiment synthesis

Shen & Zhang (2024) compared FinBERT against contemporary LLMs (GPT-3.5-turbo, GPT-4o) for financial sentiment analysis on news articles and reports, finding that FinBERT's domain-specific pre-training consistently achieved superior performance, though GPT-4o with few-shot prompt engineering showed competitive results.

**Social Media and Alternative Data:**
Recent research has validated social media as a predictive signal:

- Bollen et al. (2011) found Twitter sentiment predicted DJIA movements 2-6 days ahead with 87.6% accuracy
- Renault (2017) showed Reddit sentiment correlated with next-day volatility
- Kraaijeveld & De Smedt (2020) demonstrated cryptocurrency sentiment on Twitter preceded price movements by 1-3 days
- Cicekyurt & Bakal (2025) demonstrated that BERT-based knowledge transfer on stock market tweets improved F1-scores by 20% for deep learning models, showing the effectiveness of transfer learning on social media financial discourse

**Cross-Asset and Sentiment Spillover:**
While single-asset sentiment analysis is mature, cross-asset approaches remain sparse but show significant promise:

- Caferra (2022) examined sentiment spillovers between cryptocurrency (Bitcoin) and stock markets (S&P 500) using Transfer Entropy methods. The study found that sentiment metrics successfully mediate the relationship between these markets, with crypto sentiments affecting stock returns and economic sentiments influencing Bitcoin dynamics. Notably, entropy-based methods outperformed traditional VAR models in identifying these connections, demonstrating the value of information-theoretic approaches for cross-asset analysis.

- Cao et al. (2025) investigated sentiment connectedness networks among S&P 500 firms using nonlinear Granger causality methods and entropy-based centrality measures. Their findings revealed that firms with higher sentiment connectedness face significantly elevated stock price crash risk. The effect was particularly pronounced during market extremes, when sentiment connectedness proved a better predictor than individual firm sentiment. This work demonstrates how network-based sentiment analysis can identify systemic risk propagation.

- Nyakurukwa & Seetharam (2025) mapped investor sentiment networks across DJIA stocks, finding that sentiment is highly interconnected among major equities and influences market behavior through network propagation effects. Their network analysis approach provides methodological foundations for understanding how sentiment flows through interconnected markets.

**Gap in Literature:**
Despite these advances in sentiment networks and spillover effects, no existing research aggregates sentiment across multiple distinct asset classes (equities, crypto, forex, commodities) to detect systematic regime shifts applicable to portfolio-level risk management. Current work focuses on within-asset-class networks or pairwise market relationships, leaving the multi-asset regime detection problem unaddressed.

### 2.3 Market Regime Detection

**Traditional Approaches:**
Classical regime detection uses Hidden Markov Models (HMMs) or threshold-based indicators:

- VIX levels (VIX > 30 = Risk-Off)
- Moving average crossovers (Death Cross = regime shift)
- Economic indicators (yield curve inversion, unemployment)

These methods are lagging—they identify regimes after transition has occurred.

**Machine Learning Methods:**
Modern approaches apply ML to identify regimes from multiple signals:

- Zhang et al. (2020) developed an explainable machine learning framework for regime-based asset allocation using hierarchical clustering. Their model divided economic regimes into four categories based on macroeconomic indicators and market technical signals, then applied the Black-Litterman model for portfolio optimization. Backtesting from 2010-2020 achieved 22.53% annual returns with a Sharpe ratio of 1.06, significantly outperforming benchmark portfolios. The model successfully captured major market upswings and withdrew before crashes, demonstrating the practical value of regime-aware strategies.

- Shu et al. (2024) proposed a statistical jump model approach for regime-switching signals aimed at downside risk reduction. Their methodology incorporated jump processes to better capture abrupt market regime transitions, improving risk management effectiveness across different market conditions.

- Suárez-Cetrulo et al. (2023) conducted a systematic review of machine learning for financial prediction under regime change, analyzing 140 studies. Their review found that evolving systems, ensemble-based methods, and online incremental algorithms show particular promise for adapting to non-stationary financial dynamics. They emphasized that most machine learning techniques struggle with abrupt structural changes, highlighting the need for adaptive approaches that can detect and respond to regime shifts in real-time.

**Sentiment-Based Regime Detection:**
Limited work exists on sentiment-driven regime identification:

- Baker & Wurgler (2007): Investor sentiment index predicts broad market returns
- Bollen et al. (2011): Twitter sentiment predicted DJIA movements 2-6 days ahead with 87.6% accuracy, suggesting sentiment as a leading indicator
- Renault (2017): Reddit r/wallstreetbets sentiment correlated with next-day volatility

**Research Gap:**
No research has systematically integrated multi-source, cross-asset sentiment as a **leading indicator** for regime transitions. While sentiment analysis and regime detection have evolved independently, their integration remains unexplored despite evidence that sentiment shifts precede price-based regime changes. Existing sentiment research focuses on directional price prediction rather than regime-level market psychology, and regime detection methods rely primarily on lagging technical indicators rather than forward-looking behavioral signals.

### 2.4 Data Quality and Preprocessing Considerations

Financial text data from social media and news sources presents unique preprocessing challenges that impact sentiment analysis accuracy. Unlike formal financial documents, social media content contains noise, sarcasm, slang, and bot-generated content that can distort sentiment signals.

**Entity Recognition and Asset Classification:**
Accurately linking sentiment to specific asset classes requires robust entity recognition. Financial NER differs from general NER due to domain-specific entities (ticker symbols, ISIN codes, currency pairs), ambiguity (e.g., AAPL refers to Apple stock, not the fruit), and context-dependency where the same entity may carry different sentiment implications across asset classes.

**Multi-Source Data Integration:**
Integrating sentiment from heterogeneous sources (Reddit, Twitter, financial news) requires careful consideration of source reliability, temporal resolution, and weighting schemes. Mishev et al. (2020) noted that sentiment model performance varies significantly across data sources, with models trained on news performing differently than those trained on social media. This suggests the need for source-specific model ensembles or adaptive weighting mechanisms.

**Temporal Aggregation:**
Sentiment must be aggregated over appropriate time windows to construct meaningful indices. Daily or weekly aggregation smooths noise while preserving signal, but optimal window size may vary by asset class based on trading volume and information velocity. High-frequency crypto markets may require shorter windows than traditional equity markets.

### 2.5 Research Hypotheses

Based on the literature review, we hypothesize:

**H1 (Leading Indicator Hypothesis):** Cross-asset sentiment aggregation provides a leading indicator for market regime shifts, preceding VIX-based regime detection by 1-5 trading days. This is grounded in findings from Bollen et al. (2011) showing 2-6 day predictive lead time and Caferra (2022) demonstrating sentiment-mediated market connections.

**H2 (Divergence Signal Hypothesis):** Sentiment divergence between asset classes (e.g., equities bullish while crypto bearish) signals impending transitions between Risk-On and Risk-Off regimes. Caferra (2022) found that sentiment connectedness successfully identifies market linkages, suggesting that disconnection or divergence may indicate regime instability.

**H3 (Network Effect Hypothesis):** Sentiment connectedness intensity (measured via network centrality metrics similar to Cao et al. 2025) will correlate with regime transition probability, with high connectedness during stable regimes and rapid disconnection preceding transitions.

**H4 (Ensemble Superiority Hypothesis):** Ensemble transformer models (FinBERT + RoBERTa) will outperform single-model approaches for sentiment classification across heterogeneous data sources, based on Mishev et al. (2020) findings that different models excel on different source types.

## 3. Methods

### 3.1 Data Collection

**Data Sources:**
We collect historical text data (2016-present) from three primary sources:

1. **Reddit** (via Pushshift/PRAW API):
   - Subreddits: r/wallstreetbets, r/investing, r/stocks, r/cryptocurrency, r/forex
   - Timeframe: 2016-01-01 to present
   - Fields: Post/comment text, timestamps, scores, author

2. **Twitter** (via Twitter Academic API or Apify):
   - Keywords: $[ticker], #stocks, #crypto, #forex, #commodities, #trading
   - Influencer accounts: @DeItaone, @Fxhedgers, @zerohedge, @sentimentrader
   - Timeframe: 2016-01-01 to present
   - Fields: Tweet text, timestamps, engagement metrics

3. **Financial News** (via NewsAPI or scraping):
   - Sources: Bloomberg, Reuters, Financial Times, WSJ
   - Categories: Markets, Economy, Commodities, Crypto
   - Timeframe: 2016-01-01 to present

**Target Dataset Size:** ~5-10 million text samples across all sources

**Supplementary Data:**

- **Price Data:** Historical OHLCV for major indices (SPY, QQQ), crypto (BTC, ETH), forex (EUR/USD), commodities (GLD, USO) via yfinance or Alpha Vantage
- **VIX Data:** Volatility index for validation/labeling

### 3.2 Data Preprocessing Pipeline

**Text Cleaning:**

1. Tokenization (spaCy or NLTK)
2. Lowercasing
3. URL/mention removal
4. Emoji handling (preserve sentiment-rich emojis: 🚀📈 = bullish, 📉💩 = bearish)
5. Stop word removal (finance-aware: retain "bull", "bear", "crash")
6. Lemmatization

**Asset Class Labeling:**
Classify each text sample by asset class (Equities, Crypto, Forex, Commodities) using:

- **Keyword matching:** Ticker symbols, currency pairs, commodity names
- **NER models:** spaCy financial NER or custom-trained NER
- **Multi-label classification:** Some texts reference multiple asset classes

### 3.3 Sentiment Classification

**Model Architecture:**
Ensemble of two transformer models:

1. **FinBERT:** Finance-specific BERT variant (Araci, 2019)
   - Pretrained on financial news + analyst reports
   - Fine-tuned on Financial PhraseBank dataset
2. **RoBERTa-base:** General-purpose robustly optimized BERT
   - Broader linguistic understanding
   - Fine-tuned on Twitter Financial News Sentiment dataset

**Ensemble Strategy:**

- **Voting:** Average logits from both models
- **Weighted:** If one model shows higher validation accuracy on specific sources (e.g., FinBERT better on news, RoBERTa better on social media), apply source-dependent weights

**Training Infrastructure:**

- MANEFRAME HPC (SMU's cluster)
- GPUs: NVIDIA V100 or A100
- Framework: PyTorch + HuggingFace Transformers

**Output:**
Sentiment score per text sample: {Positive: [0-1], Neutral: [0-1], Negative: [0-1]}

### 3.4 Sentiment Index Construction

**Aggregation Strategy:**
For each asset class *c* (Equities, Crypto, Forex, Commodities) and time window *t* (daily or weekly):

$$
\text{SentimentIndex}_{c,t} = \frac{\sum_{i \in D_{c,t}} (P_i - N_i) \cdot w_i}{\sum_{i \in D_{c,t}} w_i}
$$

Where:

- $D_{c,t}$ = all documents for asset class *c* in time window *t*
- $P_i$ = positive sentiment score for document *i*
- $N_i$ = negative sentiment score for document *i*
- $w_i$ = weight (e.g., engagement score, source credibility)

**Weighting Schemes:**

- **Equal weight:** All texts contribute equally
- **Engagement-weighted:** Reddit/Twitter posts weighted by upvotes/retweets
- **Source-weighted:** News articles weighted higher than anonymous social media

**Feature Engineering:**

- **Sentiment momentum:** $\Delta \text{SentimentIndex}_{c,t} = \text{SI}_{c,t} - \text{SI}_{c,t-1}$
- **Cross-asset divergence:** $\text{Divergence}_{t} = \max(\text{SI}_{c,t}) - \min(\text{SI}_{c,t})$
- **Volatility:** Rolling standard deviation of sentiment index

### 3.5 Market Regime Classification

**Regime Definitions:**
Based on VIX and price action, historical periods labeled as:

1. **Risk-On:** VIX < 20, equities rising, crypto/commodities rallying
2. **Risk-Off:** VIX > 30, equities falling, flight to safety (bonds, gold, USD)
3. **Transition:** VIX 20-30, mixed signals, choppy price action

**Labeling Strategy:**

- Manual labeling of major historical regimes (COVID crash, 2021 bull run, 2022 bear market)
- Algorithmic labeling using VIX thresholds + price trends
- ~1000-2000 labeled days (2016-present)

**Model Selection:**
We compare:

1. **Random Forest:** Ensemble tree-based classifier
2. **XGBoost:** Gradient boosting (handles non-linear relationships well)
3. **LSTM:** Recurrent neural network (captures temporal dependencies in sentiment time series)

**Features (per time window):**

- Sentiment indices for all 4 asset classes (4 features)
- Sentiment momentum (4 features)
- Cross-asset divergence (1 feature)
- Historical VIX (1 feature)
- Rolling correlations between sentiment indices (6 features)
- **Total:** ~16 features

**Training/Validation Split:**

- Training: 2016-2021 (5 years)
- Validation: 2022-2023 (2 years)
- Test: 2024-present (out-of-sample)

**Evaluation Metrics:**

- Accuracy, Precision, Recall, F1-score per regime class
- Confusion matrix analysis
- Lead time analysis: How many days before VIX-based regime label does sentiment-based model predict transition?

### 3.6 Dashboard Development

**Backend:**

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (time-series data)
- **APIs:**
  - `/sentiment/{asset_class}`: Returns sentiment index time series
  - `/regime/current`: Returns current regime prediction + confidence
  - `/alerts/divergence`: Returns cross-asset divergence alerts

**Frontend:**

- **Framework:** React (Vite build tool)
- **Visualization:** Recharts or D3.js for interactive time-series charts
- **Components:**
  - Real-time sentiment gauge (per asset class)
  - Historical sentiment trends (line charts)
  - Regime indicator (Risk-On/Off/Transition)
  - Divergence alerts (when sentiment contradicts price or cross-asset sentiment diverges)

**Deployment:**

- **Backend:** Cloud hosting (AWS EC2, Google Cloud Run, or Heroku)
- **Frontend:** Vercel or Netlify
- **CI/CD:** GitHub Actions

## 4. Expected Results

### 4.1 Sentiment Model Performance Targets

Based on benchmark performance from FinBERT (Araci, 2019) and ensemble approaches:

- **Classification Accuracy:** 85-90% on financial text sentiment (positive/neutral/negative)
- **F1-Score:** >0.80 across all sentiment classes
- **Source-Specific Performance:** Higher accuracy on news (>90%) vs. social media (>80%)

### 4.2 Regime Classification Performance Targets

- **Overall Accuracy:** 75-85% for three-class regime prediction (Risk-On/Risk-Off/Transition)
- **Lead Time:** Sentiment-based signals detect regime transitions 1-5 trading days before VIX-based indicators
- **Transition Detection:** F1-score >0.70 for identifying Transition regimes (most challenging class)
- **Cross-validation:** Time-series split validation (2016-2021 train, 2022-2023 validation, 2024+ test)

### 4.3 Backtesting Validation Events

The system will be validated on major historical market events:

- **COVID-19 Crash (Feb-Mar 2020):** Did sentiment signals predict Risk-Off transition before VIX spike?
- **2021 Crypto Bull Run (Jan-Nov 2021):** Was cross-asset divergence visible before crypto correction?
- **2022 Bear Market (Jan-Oct 2022):** Could sentiment indices forecast Fed tightening impact?
- **2023 AI Rally (Jan-Jul 2023):** Did equity sentiment decouple from broader market psychology?

## 5. Discussion

### 5.1 Expected Interpretations

This research will establish whether cross-asset sentiment aggregation serves as a leading indicator for market regime transitions. If validated, results will demonstrate that collective market psychology (as expressed in text data) shifts before observable price-based regime changes, supporting the behavioral finance perspective that sentiment drives prices rather than merely reflecting them.

The sentiment divergence hypothesis—that cross-asset sentiment disconnection signals regime instability—builds on Caferra's (2022) finding that sentiment mediates cross-market relationships. Validation would suggest that portfolio-level risk management should monitor not just individual asset sentiment but the coherence of sentiment across asset classes.

### 5.2 Practical Implications

**For Portfolio Managers:**

- Early warning system for regime shifts enables proactive rebalancing before volatility spikes
- Sentiment divergence alerts identify periods of elevated transition risk
- Cross-asset sentiment indices complement traditional technical indicators

**For Risk Managers:**

- Leading indicator provides 1-5 day advance notice for risk mitigation actions
- Sentiment connectedness metrics (similar to Cao et al. 2025) identify systemic risk propagation
- Real-time dashboard enables continuous monitoring vs. periodic review

**For Retail Investors:**

- Democratizes institutional-grade sentiment analysis (previously $20K+/year tools)
- Intuitive visualization makes complex sentiment data accessible
- Educational resource for understanding market psychology dynamics

### 5.3 Limitations

- **Data quality:** Social media data is noisy, contains sarcasm, bots
- **Survivorship bias:** Only analyzing publicly available text (not institutional sentiment)
- **Causality vs. correlation:** Sentiment may reflect rather than predict regime shifts
- **Computational cost:** Real-time transformer inference expensive

### 5.4 Ethical Considerations

- **Market manipulation:** Could system be gamed if widely adopted?
- **Retail vs. institutional:** Does democratizing sentiment analysis level playing field or create new risks?
- **Data privacy:** Reddit/Twitter users may not consent to sentiment analysis

### 5.5 Future Work

- Incorporate alternative data (options flow, institutional positioning)
- Expand to more asset classes (bonds, real estate)
- Multi-language sentiment analysis (non-English financial discourse)
- Causal analysis (does sentiment drive prices or vice versa?)

## 6. Conclusion

This research addresses a critical gap in financial sentiment analysis by developing the first system to aggregate multi-source, cross-asset sentiment for market regime detection. By applying ensemble transformer models to heterogeneous data sources (social media, news, forums) across four major asset classes, we construct sentiment indices that capture collective market psychology. The integration of these indices with machine learning regime classification creates a leading indicator system that identifies Risk-On, Risk-Off, and Transition states before traditional volatility-based methods.

The contributions are threefold: methodologically, we establish a framework for cross-asset sentiment aggregation and regime mapping; practically, we democratize institutional-grade sentiment analysis through an open-source system; theoretically, we advance understanding of how distributed market psychology manifests in textual data and precedes observable price dynamics. Successful validation would demonstrate that behavioral signals embedded in financial discourse provide predictive information beyond technical indicators, supporting the integration of NLP-based sentiment analysis into quantitative portfolio management frameworks. The real-time dashboard deployment ensures accessibility for retail investors, traders, and risk managers, potentially leveling the information asymmetry that currently favors institutional players with expensive sentiment analysis tools.

## Acknowledgments

[Advisor name], PhD - Capstone Advisor
SMU MANEFRAME team - HPC support

## References

1. Araci, D. (2019). FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. <https://doi.org/10.48550/arxiv.1908.10063>

2. Baker, M., & Wurgler, J. (2007). Investor Sentiment in the Stock Market. The Journal of Economic Perspectives, 21(2), 129–151. <https://doi.org/10.1257/jep.21.2.129>

3. Bollen, J., Mao, H., & Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1–8. <https://doi.org/10.1016/j.jocs.2010.12.007>

4. Caferra, R. (2022). Sentiment spillover and price dynamics: Information flow in the cryptocurrency and stock market. *Physica A: Statistical Mechanics and its Applications*, 593, 126983. <https://doi.org/10.1016/j.physa.2022.126983>

5. Cao, J., He, G., & Jiao, Y. (2025). Too Sensitive to Fail: The Impact of Sentiment Connectedness on Stock Price Crash Risk. *Entropy*, 27(4), 345. <https://doi.org/10.3390/e27040345>

6. Keynes, J. M., & Royal Economic Society (Great Britain). (1973). The general theory of employment, interest and money. Cambridge University Press for the Royal Economic Society.

7. Kraaijeveld, O., & De Smedt, J. (2020). The predictive power of public Twitter sentiment for forecasting cryptocurrency prices. Journal of International Financial Markets, Institutions & Money, 65, Article 101188. <https://doi.org/10.1016/j.intfin.2020.101188>
.

8. Liu, C., Arulappan, A., Naha, R., Mahanti, A., Kamruzzaman, J., & Ra, I.-H. (2024). Large Language Models and Sentiment Analysis in Financial Markets: A Review, Datasets, and Case Study. *IEEE Access*, 12, 134041-134061. <https://doi.org/10.1109/ACCESS.2024.3445413>

9. LOUGHRAN, T., & MCDONALD, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. The Journal of Finance (New York), 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>

10. Cicekyurt, E., & Bakal, G. (2025). Enhancing Sentiment Analysis in Stock Market Tweets Through BERT-Based Knowledge Transfer. *Computational Economics*. <https://doi.org/10.1007/s10614-025-10901-8>

11. Mishev, K., Gjorgjevikj, A., Vodenska, I., Chitkushev, L. T., & Trajanov, D. (2020). Evaluation of Sentiment Analysis in Finance: From Lexicons to Transformers. *IEEE Access*, 8, 131662-131682. <https://doi.org/10.1109/ACCESS.2020.3009626>

12. Nyakurukwa, K., & Seetharam, Y. (2025). Investor sentiment networks: mapping connectedness in DJIA stocks. *Financial Innovation*, 11(1), 4. <https://doi.org/10.1186/s40854-024-00675-7>

13. Renault, T. (2017). Intraday online investor sentiment and return patterns in the U.S. stock market. Journal of Banking & Finance, 84, 25–40. <https://doi.org/10.1016/j.jbankfin.2017.07.002>

14. Shen, Y., & Zhang, P. K. (2024). Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT. *IEEE International Conference on Power, Intelligent Computing and Systems (Online)*, 717–721. <https://doi.org/10.1109/ICPICS62053.2024.10796670>

15. Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. *Journal of Asset Management*, 25(5), 493-507. <https://doi.org/10.1057/s41260-024-00376-x>

16. Suárez-Cetrulo, A. L., Quintana, D., & Cervantes, A. (2023). Machine Learning for Financial Prediction Under Regime Change Using Technical Analysis: A Systematic Review. *International Journal of Interactive Multimedia and Artificial Intelligence*, 8(2), 117-138. <https://doi.org/10.9781/ijimai.2023.06.003>

17. Zhang, R., Yi, C., & Chen, Y. (2020). Explainable Machine Learning for Regime-Based Asset Allocation. *2020 IEEE International Conference on Big Data (Big Data)*, 5480-5485. <https://doi.org/10.1109/BigData50022.2020.9378332>
