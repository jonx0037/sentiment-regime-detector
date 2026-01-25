# Annotated Bibliography

**Cross-Asset Sentiment Regime Detector**  
Last Updated: January 25, 2026  
Total Entries: 48 papers

---

## Transformer Models & Financial NLP

Araci, D. (2019). FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. <https://doi.org/10.48550/arxiv.1908.10063>
  - This paper introduces FinBERT, a pre-trained language model specifically designed for financial sentiment analysis. The author fine-tunes BERT on financial texts to improve sentiment classification accuracy in the finance domain. This work is significant for enhancing NLP applications in finance.
  - Keywords: FinBERT, Financial Sentiment Analysis, Pre-trained Language Models, BERT, NLP in Finance
  - Research Methods: Fine-tuning of BERT on financial datasets and evaluation of sentiment classification performance.
  - Findings: FinBERT outperforms general-purpose sentiment analysis models on financial texts.
  - Relevance: Core foundation for our ensemble transformer approach.

Mishev, K., Gjorgjevikj, A., Vodenska, I., Chitkushev, L. T., & Trajanov, D. (2020). Evaluation of Sentiment Analysis in Finance: From Lexicons to Transformers. IEEE Access, 8, 1–1. <https://doi.org/10.1109/ACCESS.2020.3009626>
  - Comprehensive evaluation of sentiment analysis techniques from traditional lexicon-based methods to advanced transformer models. The authors compare performance across financial datasets.
  - Keywords: Sentiment Analysis, Finance, Lexicon-Based Methods, Transformer Models
  - Findings: Transformer models outperform traditional methods in accuracy and contextual understanding.
  - Relevance: Evidence supporting H4 (Ensemble Superiority Hypothesis).

Liu, C., Arulappan, A., Naha, R., Mahanti, A., Kamruzzaman, J., & Ra, I.-H. (2024). Large Language Models and Sentiment Analysis in Financial Markets: A Review, Datasets, and Case Study. IEEE Access, 12, 134041–134061. <https://doi.org/10.1109/ACCESS.2024.3445413>
  - Comprehensive review of LLM applications in financial sentiment analysis with case study on Bitcoin price correlation.
  - Keywords: Large Language Models, Sentiment Analysis, Financial Markets, Datasets
  - Findings: LLMs significantly enhance sentiment analysis capabilities; historical news patterns show substantial impact on Bitcoin prices.
  - Relevance: LLM methodology framework for multi-asset analysis.

Shen, Y., & Zhang, P. K. (2024). Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT. IEEE ICPICS, 717–721. <https://doi.org/10.1109/ICPICS62053.2024.10796670>
  - Comparison of LLMs and FinBERT for sentiment analysis on news and reports, with emphasis on prompt engineering.
  - Findings: GPT-4o with few-shot examples matches fine-tuned FinBERT performance.
  - Relevance: Prompt engineering methodology for our system.

Konstantinidis, T., Iacovides, G., Xu, M., Constantinides, T. G., & Mandic, D. (2024). FinLlama: Financial Sentiment Classification for Algorithmic Trading Applications. <https://doi.org/10.48550/arxiv.2403.12285>
  - Presents FinLlama, a Llama2-based model fine-tuned for algorithmic trading sentiment classification with LoRA optimization.
  - Findings: High accuracy in sentiment classification suitable for real-time trading applications.
  - Relevance: Parameter-efficient fine-tuning methodology.

Delgadillo, J., Kinyua, J., & Mutigwe, C. (2024). FinSoSent: Advancing Financial Market Sentiment Analysis through Pretrained Large Language Models. Big Data and Cognitive Computing, 8(8), 87. <https://doi.org/10.3390/bdcc8080087>
  - Introduces FinSoSent, a domain-specific LLM for financial sentiment pre-trained on financial news.
  - Findings: Outperforms state-of-the-art models based on 860+ experiments.
  - Relevance: Domain-specific pre-training approach.

Ergun, Z. E., & Sefer, E. (2025). FinSentiment: Predicting Financial Sentiment Through Transfer Learning. Intelligent Systems in Accounting, Finance and Management, 32(3), e70015. <https://doi.org/10.1002/isaf.70015>
  - Comprehensive comparison of BERT, XLNet, RoBERTa, GPT, Llama, and T5 for financial sentiment, with finance-specific variants (Fin-BERT, Fin-XLNet, etc.).
  - Findings: RoBERTa pretrained on financial corpora shows best performance.
  - Relevance: Key evidence for H4 - multi-model ensemble approach.

Nasiopoulos, D. K., Roumeliotis, K. I., Sakas, D. P., Toudas, K., & Reklitis, P. (2025). Financial Sentiment Analysis and Classification: A Comparative Study of Fine-Tuned Deep Learning Models. IJFS, 13(2), 75. <https://doi.org/10.3390/ijfs13020075>
  - Comparison of fine-tuned GPT-4o, GPT-4o-mini, BERT, and FinBERT with Bayesian optimization.
  - Findings: GPT-4o-mini shows strong efficiency and performance; fine-tuning substantially improves accuracy.
  - Relevance: Latest benchmarks for model selection.

Mahendran, M. B., Gokul, A. K., Lakshmi, P., & Pavithra, S. (2025). Comparative Advances in Financial Sentiment Analysis: A Review of BERT, FinBert, and Large Language Models. IEEE IDCIoT, 39–45. <https://doi.org/10.1109/IDCIOT64235.2025.10914764>
  - Review of BERT, FinBERT, and LLMs with focus on zero-shot, few-shot, and fine-tuning approaches.
  - Findings: FinBERT exhibits high accuracy and robustness across financial datasets.
  - Relevance: Model selection guidance for our ensemble.

Baghavathi Priya, S., Kumar, M., Prakash J D, N., & Krithika, N. (2025). Advanced Financial Sentiment Analysis Using FinBERT to Explore Sentiment Dynamics. IEEE IDCIoT, 889–897. <https://doi.org/10.1109/IDCIOT64235.2025.10915080>
  - Comparison of FinBERT, DistilBERT, and BERT with custom preprocessing framework.
  - Findings: FinBERT achieves 89.6% average accuracy across 3 sentiment classes.
  - Relevance: Performance benchmark for our FinBERT implementation.

---

## Social Media & Alternative Data

Bollen, J., Mao, H., & Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1-8. <https://doi.org/10.1016/j.jocs.2010.12.007>
  - Seminal work analyzing Twitter mood dimensions (Calm, Alert, Sure, Vital, Kind, Happy) and their correlation with DJIA.
  - Findings: 86.7% accuracy in predicting daily DJIA movements; 2-6 day lead time.
  - Relevance: Core evidence for H1 (Leading Indicator Hypothesis).

Renault, T. (2017). Intraday online investor sentiment and return patterns in the U.S. stock market. Journal of Banking & Finance, 84, 25–40. <https://doi.org/10.1016/j.jbankfin.2017.07.002>
  - Analysis of StockTwits sentiment at half-hour intervals and intraday return patterns.
  - Findings: First half-hour sentiment predicts last half-hour S&P 500 returns; novice traders drive effect.
  - Relevance: Intraday sentiment methodology.

Kraaijeveld, O., & De Smedt, J. (2020). The predictive power of public Twitter sentiment for forecasting cryptocurrency prices. Journal of International Financial Markets, Institutions & Money, 65, 101188. <https://doi.org/10.1016/j.intfin.2020.101188>
  - Twitter sentiment analysis for 9 cryptocurrencies using crypto-specific lexicon.
  - Findings: 1-3 day predictive power for Bitcoin, Bitcoin Cash, Litecoin; 1-14% tweets from bots.
  - Relevance: Crypto-specific sentiment methodology and H1 evidence.

Cicekyurt, E., & Bakal, G. (2025). Enhancing Sentiment Analysis in Stock Market Tweets Through BERT-Based Knowledge Transfer. Computational Economics. <https://doi.org/10.1007/s10614-025-10901-8>
  - BERT-based knowledge transfer for stock market tweet sentiment with FinBERT labeling of unlabeled data.
  - Findings: +20% F1-score improvement for deep learning models; +17% for ML models.
  - Relevance: Transfer learning methodology for social media data.

Amin, M. S., et al. (2024). Harmonizing Macro-Financial Factors and Twitter Sentiment Analysis in Forecasting Stock Market Trends. JCSTS, 6(1), 58-67. <https://doi.org/10.32996/jcsts.2024.6.1.7>
  - Integration of Twitter sentiment with macroeconomic indicators (500,000 tweets analyzed).
  - Findings: Correlation between ChatGPT-related sentiment and Microsoft/OpenAI stock movements.
  - Relevance: Multi-factor sentiment integration framework.

---

## Cryptocurrency Sentiment Analysis

Roumeliotis, K. I., Tselikas, N. D., & Nasiopoulos, D. K. (2024). LLMs and NLP Models in Cryptocurrency Sentiment Analysis: A Comparative Classification Study. BDCC, 8(6), 63. <https://doi.org/10.3390/bdcc8060063>
  - Fine-tuning GPT-4, BERT, and FinBERT for cryptocurrency news sentiment.
  - Findings: Fine-tuned models significantly improve crypto sentiment classification.
  - Relevance: Crypto-specific NLP benchmarks.

Raheman, A., Kolonin, A., Fridkins, I., Ansari, I., & Vishwas, M. (2022). Social Media Sentiment Analysis for Cryptocurrency Market Prediction. <https://doi.org/10.48550/arxiv.2204.10185>
  - NLP models for social media sentiment analysis applied to Bitcoin prediction.
  - Findings: Interpretable models outperform non-explainable ones for sentiment-price correlation.
  - Relevance: Explainable AI approach for crypto sentiment.

---

## Cross-Asset & Sentiment Spillover

Caferra, R. (2022). Sentiment spillover and price dynamics: Information flow in the cryptocurrency and stock market. Physica A, 593, 126983. <https://doi.org/10.1016/j.physa.2022.126983>
  - Examines sentiment–returns relationship in S&P500 and Bitcoin using Transfer Entropy.
  - Findings: Sentiment mediates cross-market relationships; Transfer Entropy outperforms VAR estimates.
  - Relevance: Core methodology for H2/H3 - sentiment spillover measurement.

Cao, J., He, G., & Jiao, Y. (2025). Too Sensitive to Fail: The Impact of Sentiment Connectedness on Stock Price Crash Risk. Entropy, 27(4), 345. <https://doi.org/10.3390/e27040345>
  - S&P 500 sentiment spillover network analysis and crash risk assessment.
  - Findings: Higher sentiment connectedness → increased crash risk; network effects dominate individual sentiment.
  - Relevance: Core evidence for H3 (Network Effect Hypothesis).

Nyakurukwa, K., & Seetharam, Y. (2025). Investor sentiment networks: mapping connectedness in DJIA stocks. Financial Innovation, 11(1), 4. <https://doi.org/10.1186/s40854-024-00675-7>
  - DJIA sentiment connectedness at frequency and asymmetric levels.
  - Findings: News and social media sentiment show consistent connectedness; negative news has higher connectedness.
  - Relevance: Sentiment network mapping methodology.

Wang, X., Wang, R., & Zhang, Y. (2024). Cross-asset momentum and the hybrid fund transmission mechanism in China's stock and bond markets. PLOS ONE, 19(3), e0300781. <https://doi.org/10.1371/journal.pone.0300781>
  - Cross-asset momentum between Chinese stock and bond markets (2006-2022).
  - Findings: Stock momentum negatively influences bonds; bond momentum positively influences stocks; hybrid funds mediate transmission.
  - Relevance: Evidence for H2 - cross-asset divergence signals.

Yang, J., Tang, Y., Li, Y., Zhang, L., & Zhang, H. (2025). Cross-Asset Risk Management: Integrating LLMs for Real-Time Monitoring of Equity, Fixed Income, and Currency Markets. <https://doi.org/10.48550/arXiv.2504.04292>
  - LLM framework for real-time cross-asset risk monitoring.
  - Findings: Increased accuracy in predicting market shifts vs. conventional methods.
  - Relevance: LLM methodology for cross-asset monitoring.

Sarfarazurrehman, S., Mane, V., & Doshi, A. (2025). AI and Machine Learning Models in Cross-Asset Class Investment Risk Analysis. IEEE ICSSAS, 1170-1177. <https://doi.org/10.1109/ICSSAS66150.2025.11081061>
  - DRL and LSTM for cross-asset portfolio optimization (real estate and equities).
  - Findings: 29.52% cumulative returns; Sharpe ratio 0.98.
  - Relevance: AI/ML benchmarks for cross-asset systems.

Pankwaen, K., Thongkairat, S., & Saijai, W. (2025). Global Cross-Market Trading Optimization Using Iterative Combined Algorithm. Preprints. <https://doi.org/10.20944/preprints202503.1146.v1>
  - DRL with IMCA for 39 stocks across US, Australia, Europe, Thailand, and BTC.
  - Findings: 29.52% cumulative return; Sharpe 0.829; dynamic recalibration outperforms static ensembles.
  - Relevance: Multi-asset global optimization framework.

---

## Forex & Currency Sentiment

Dakalbab, F., Kumar, A., Talib, M. A., & Nasir, Q. (2025). Advancing Forex prediction through multimodal text-driven model and attention mechanisms. Intelligent Systems with Applications, 26, 200518. <https://doi.org/10.1016/j.iswa.2025.200518>
  - Multimodal framework integrating technical analysis and sentiment with cross-modal attention.
  - Findings: Hybrid attention mechanism outperforms single-modality models on EUR/USD, GBP/USD, USD/JPY.
  - Relevance: Attention mechanism methodology for forex.

Olaiyapo, O. F. (2024). Applying News and Media Sentiment Analysis for Generating Forex Trading Signals. RoBES, 11(4), 84-94. <https://doi.org/10.26794/2308-944X-2023-11-4-84-94>
  - Lexicon-based and Naive Bayes sentiment analysis for USD forex trading signals.
  - Findings: Sentiment analysis effectively forecasts market movements across conditions.
  - Relevance: Forex trading signal generation methodology.

Gu, G., & Song, Y. (2026). Enhancing exchange rate forecasting with contextual sentiment indices: A fine-tuned FinBERT approach. Applied Soft Computing, 189, 114556. <https://doi.org/10.1016/j.asoc.2026.114556>
  - Currency-pair-specific FinBERT fine-tuning on annual rolling basis for EUR/USD.
  - Findings: 84.33% out-of-sample accuracy; outperforms traditional sentiment tools and 4 SOTA LLMs.
  - Relevance: Currency-pair-specific modeling framework; H4 evidence.

Sibande, X., Gupta, R., Demirer, R., & Bouri, E. (2023). Investor Sentiment and (Anti) Herding in the Currency Market: Evidence from Twitter Feed Data. Journal of Behavioral Finance, 24(1), 56-72. <https://doi.org/10.1080/15427560.2021.1917579>
  - Twitter happiness index and currency market herding behavior for 9 developed market currencies.
  - Findings: Anti-herding prominent during extreme sentiment; stronger effect in bullish states.
  - Relevance: Behavioral forex analysis; H3 evidence.

Fatouros, G., Soldatos, J., Kouroumali, K., Makridis, G., & Kyriazis, D. (2023). Transforming sentiment analysis in the financial domain with ChatGPT. Machine Learning with Applications, 14, 100508. <https://doi.org/10.1016/j.mlwa.2023.100508>
  - ChatGPT 3.5 for forex sentiment analysis with zero-shot prompting.
  - Findings: 35% enhanced performance vs FinBERT; 36% higher correlation with market returns.
  - Relevance: ChatGPT forex methodology; prompt engineering approach.

---

## Real-Time & High-Frequency Systems

Cai, Y., Tang, Z., & Chen, Y. (2024). Can real-time investor sentiment help predict the high-frequency stock returns? The North American Journal of Economics and Finance, 72, 102147. <https://doi.org/10.1016/j.najef.2024.102147>
  - Real-time sentiment at half-hour frequency using MF-EEMD-ML prediction system.
  - Findings: 19.18% MAE reduction, 19.08% RMSE reduction, 16.66% DS improvement.
  - Relevance: Real-time high-frequency methodology.

---

## Commodities Sentiment

Shi, C. (2025). Understanding Gold and Dollar Price Movements: A Sentiment-Based GARCH-MIDAS Approach. Atlantis Press, MIED 2025, 348, 449-456. <https://doi.org/10.2991/978-94-6463-835-6_47>
  - GARCH-MIDAS model with sentiment indices for gold and USD price prediction.
  - Findings: 18.7% out-of-sample prediction error reduction vs. traditional models; sentiment-driven herding effects identified.
  - Relevance: Commodity sentiment methodology; H2 evidence for gold/USD divergence.

---

## Market Regime Detection

Zhang, R., Yi, C., & Chen, Y. (2020). Explainable Machine Learning for Regime-Based Asset Allocation. IEEE Big Data, 5480–5485. <https://doi.org/10.1109/BigData50022.2020.9378332>
  - Hierarchical clustering for regime identification with Black-Litterman allocation.
  - Findings: 22.53% annual returns; Sharpe ratio 1.06; identifies abnormal market waves.
  - Relevance: Explainable AI benchmark for regime detection.

Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. Journal of Asset Management, 25(5), 493–507. <https://doi.org/10.1057/s41260-024-00376-x>
  - Statistical jump model for regime identification with time series cross-validation.
  - Findings: Outperforms HMM and buy-and-hold on US, Germany, Japan indices (1990-2023).
  - Relevance: Jump model methodology for regime detection.

Suárez Cetrulo, A. L., Quintana, D., & Cervantes, A. (2024). Machine Learning for Financial Prediction Under Regime Change Using Technical Analysis: A Systematic Review. IJIMAI, 9(1), 137–148. <https://doi.org/10.9781/ijimai.2023.06.003>
  - Systematic review of 140 studies on ML for financial prediction under regime change.
  - Findings: No single dominant technique; data stream learning and economic research communities converging.
  - Relevance: Comprehensive background on regime change literature.

---

## Foundational Works

Baker, M., & Wurgler, J. (2007). Investor Sentiment in the Stock Market. The Journal of Economic Perspectives, 21(2), 129–151. <https://doi.org/10.1257/jep.21.2.129>
  - Seminal paper on investor sentiment measures and their predictive power for stock returns.
  - Findings: Sentiment significantly affects stock prices, especially small-cap and growth stocks.
  - Relevance: Foundational for H1 - investor sentiment framework.

Loughran, T., & McDonald, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>
  - Development of finance-specific sentiment dictionary for 10-K analysis.
  - Findings: 75% of Harvard Dictionary "negative" words misclassified in financial context.
  - Relevance: Foundational lexicon methodology.

Kelly, B., & Xiu, D. (2023). Financial Machine Learning. Working Paper.
  - Comprehensive survey of machine learning in financial markets.
  - Findings: Best practices for ML applications in finance; promising research directions.
  - Relevance: Foundational ML methodology framework.

Micaletti, R. (2019). Relative Sentiment and Machine Learning for Tactical Asset Allocation. SSRN Electronic Journal. <https://doi.org/10.2139/ssrn.3475258>
  - Sentix sentiment indices for tactical allocation across US, Europe, Japan, Asia ex-Japan.
  - Findings: Relative sentiment (institutional vs. individual) has robust predictive power.
  - Relevance: Relative sentiment methodology for multi-region allocation.

Keynes, J. M. (1973). The General Theory of Employment, Interest and Money. Cambridge University Press.
  - Seminal work introducing "animal spirits" concept in market behavior.
  - Relevance: Historical/theoretical foundation for behavioral finance approach.

---

## Literature Reviews & Surveys

Ehsan, A., Habib, S., & Sohail, A. (2025). Financial News Sentiment Analysis Using NLP and Machine Learning for Asset Price Prediction: A Systematic Review. VFAST Trans. Software Engineering, 13(3), 279–308. <https://doi.org/10.21015/vtse.v13i3.2165>
  - Systematic review of NLP/ML for financial news sentiment (2018-2025).
  - Findings: Synthesis of effective methodologies for price prediction.
  - Relevance: Literature context for our contribution.

Sathish, N., & Jamalpur, B. (2025). A Comprehensive Survey on Enhancing Stock Market Predictions through Machine Learning and NLP-Based Sentiment Analysis Integration. IEEE ICSADL, 92-99. <https://doi.org/10.1109/ICSADL65848.2025.10933064>
  - Survey of ML + NLP sentiment integration for stock prediction.
  - Findings: Hybrid KNN-LR with sentiment outperforms individual algorithms.
  - Relevance: Integration framework guidance.

Ferrell, B., & McInnes, B. T. (2025). A Comprehensive Survey on the Integration of Reinforcement Learning and NLP for Stock Market Trading. SSRN. <https://doi.org/10.2139/ssrn.5135573>
  - Survey of 22 papers (2018-2024) on RL + NLP for stock trading.
  - Findings: Challenges include lack of standardized datasets; opportunities in LLMs.
  - Relevance: RL integration considerations.

Kengmegni, G. (2025). Limitations of News Sentiment Analysis in Short-term Stock Return Prediction: A Multi-Level Approach. SSRN. <https://doi.org/10.2139/ssrn.5086825>
  - Multi-level sentiment analysis (stock, industry, economy) for prediction.
  - Findings: Short-term prediction remains challenging despite advances.
  - Relevance: Limitations awareness; multi-level methodology.

Todd, A., Bowden, J., & Moshfeghi, Y. (2024). Text‐based sentiment analysis in finance: Synthesising the existing literature and exploring future directions. Intelligent Systems in Accounting, Finance and Management, 31(1), e1549. <https://doi.org/10.1002/isaf.1549>
  - Critical evaluation of sentiment analysis techniques in finance with focus on transformer architecture and multimodal analysis.
  - Keywords: Sentiment Analysis, Deep Learning, Transformer Architecture, Multimodal Analysis, Corporate Earnings
  - Findings: Transformer-based methods and multimodal classifiers (text-audio) represent underexplored opportunities in finance.
  - Relevance: Key literature synthesis for H4 (Ensemble Superiority); guidance on emerging multimodal approaches.

Shao, Z., Yao, X., Chen, F., Wang, Z., & Gao, J. (2025). Revisiting time-varying dynamics in stock market forecasting: A multi-source sentiment analysis approach with large language model. Decision Support Systems, 190, 114362. <https://doi.org/10.1016/j.dss.2024.114362>
  - Introduces HD-SURDLM framework combining Twitter sentiment (2.5M posts) with dynamic financial modeling using VADER, TextBlob, and RoBERTa.
  - Keywords: Multi-source Sentiment, LLM, Stock Forecasting, Gibbs Sampling, Dynamic Modeling
  - Findings: 1.02% improvement in 1-day forecasts; 0.42% for 20-day; 0.36% for 50-day; outperforms LSTM, Random Forest, RNN.
  - Relevance: Core evidence for H2 (cross-asset dynamics); multi-source sentiment aggregation methodology.

Trushkovskyi, A. (2025). Application of Social Media Sentiment Analysis for Developing Trading Models in the Cryptocurrency Market. Journal of Applied Economic Sciences (JAES), 20(3), 535. <https://doi.org/10.57017/jaes.v20.3(89).11>
  - Examines predictive role of Twitter/Reddit sentiment for Bitcoin price changes using OLS, Random Forest, and XGBoost.
  - Keywords: Cryptocurrency, Social Media Sentiment, Bitcoin, Trading Models, Granger Causality
  - Findings: 0.24-0.25% price increase predicted per unit sentiment increase; Granger causality confirms sentiment leads returns.
  - Relevance: Core evidence for H1 (Leading Indicator); crypto-specific sentiment methodology with trading bot applications.
