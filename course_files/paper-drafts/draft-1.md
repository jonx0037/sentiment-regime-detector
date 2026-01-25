# Cross-Asset Sentiment Regime Detector: Automating Market Psychology Analysis Through Multi-Source NLP

**Author:** Jonathan Rocha (<jrocha@smu.edu>)  
**Advisor:** [Searching - TBD]  
**Affiliation:** Master of Science in Data Science, Southern Methodist University, Dallas, TX 75275 USA  
**GitHub:** github.com/jonx0037/sentiment-regime-detector  
**Draft:** 1.0  
**Date:** January 25, 2026  
**Based on:** Draft-0 (January 12, 2026)

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

#### 2.1.1 From Lexicons to BERT

The evolution of financial sentiment analysis reflects a broader transition in natural language processing from rule-based systems to contextual deep learning models. Early approaches relied on domain-specific lexicons to identify sentiment-bearing words in financial texts. Loughran and McDonald (2011) demonstrated that general-purpose sentiment dictionaries perform poorly in financial contexts because words carry domain-specific meanings—for example, "liability" carries negative connotations in everyday English but represents a neutral accounting term in finance. Their finance-specific lexicon addressed this limitation and became a foundational resource for subsequent research.

The introduction of transformer-based architectures marked a paradigm shift in financial sentiment analysis. Araci (2019) introduced FinBERT, a BERT model fine-tuned on financial news and analyst reports, achieving a 15% accuracy improvement over previous state-of-the-art methods. Critically, FinBERT demonstrated effectiveness even with limited labeled data, outperforming baseline models when trained on as few as 500 examples. This finding established the viability of transfer learning for financial NLP tasks where labeled datasets are scarce.

Mishev et al. (2020) conducted over 100 experiments to systematically evaluate sentiment analysis approaches ranging from lexicons to transformers. Their comprehensive study compared BERT variants including RoBERTa, XLNet, ALBERT, and DistilBERT across multiple financial datasets. The results demonstrated that contextual embeddings achieve substantially greater efficiency than lexicons and fixed word encoders. BART and ALBERT-xxlarge achieved the highest performance with Matthews Correlation Coefficient scores of 0.895 and 0.881 respectively. Notably, distilled versions of transformers such as DistilBERT retained greater than 95% of BERT's accuracy while requiring 40% fewer parameters, making them suitable for production environments where computational resources are constrained.

#### 2.1.2 Large Language Models

The emergence of large language models has introduced new capabilities for financial sentiment analysis, particularly through zero-shot and few-shot learning paradigms. Fatouros et al. (2023) investigated ChatGPT 3.5 for sentiment analysis in the foreign exchange market, finding that the model achieved approximately 35% higher sentiment classification performance and 36% higher correlation with market returns compared to FinBERT. Their zero-shot prompting approach demonstrated that LLMs can interpret financial texts without domain-specific fine-tuning, though the study emphasized that prompt engineering significantly influences performance outcomes.

Konstantinidis et al. (2024) developed FinLlama, a fine-tuned version of Llama 2 7B designed specifically for financial sentiment classification. Their approach employed Low-Rank Adaptation (LoRA) to minimize computational requirements, reducing trainable parameters to just 0.0638% of the total model parameters while maintaining accuracy. In portfolio construction experiments, FinLlama achieved 44.7% higher cumulative returns than FinBERT-based portfolios, with a significantly higher Sharpe ratio and lower annualized volatility. Beyond binary classification, FinLlama quantifies sentiment strength, providing traders with nuanced insight into financial news articles.

Luo and Gong (2024) demonstrated that supervised fine-tuning of LLaMA-2 7B achieves state-of-the-art performance on the Financial PhraseBank benchmark, improving accuracy from 0.86 to 0.90. Their experiments compared few-shot learning, further pre-training, and supervised fine-tuning approaches, finding that further pre-training alone does not provide noticeable improvement over baseline performance. The supervised fine-tuning approach proved most effective, confirming that task-specific adaptation remains essential even for large pre-trained models.

Shen and Zhang (2024) compared FinBERT against GPT-3.5-turbo and GPT-4o for sentiment analysis on financial news articles and reports. Their findings indicated that FinBERT with domain-specific pre-training consistently outperformed general-purpose LLMs in accuracy, precision, recall, and F1-score. However, GPT-4o with few-shot examples of financial texts achieved competitive results, suggesting that effective prompt engineering can make general-purpose LLMs viable tools for financial sentiment analysis without extensive fine-tuning.

#### 2.1.3 Model Comparison and Selection Criteria

Systematic comparisons across model architectures have clarified the trade-offs between accuracy, computational cost, and deployment considerations. Nasiopoulos et al. (2025) conducted a comparative study of fine-tuned deep learning models including GPT-4o, GPT-4o-mini, BERT, and FinBERT, benchmarked against traditional machine learning classifiers. Using Bayesian optimization across 100 trials for hyperparameter tuning, they found that fine-tuned GPT-4o and GPT-4o-mini achieved 87.79% accuracy on combined FiQA and Financial PhraseBank datasets. Traditional approaches including Support Vector Machines, Random Forests, and Logistic Regression lagged substantially behind at 64.53% to 65.31% accuracy. Fine-tuned LLMs outperformed fine-tuned BERT models by approximately 9% in mean accuracy, though at the cost of increased computational time and inference expense.

Mahendran et al. (2025) reviewed advances in financial sentiment analysis using BERT, FinBERT, and large language models, highlighting practical considerations for deployment. Their analysis noted that DistilBERT retains 97% of BERT's capabilities while requiring only half the parameters, making it suitable for low-latency applications such as algorithmic trading and real-time market monitoring. The review identified persistent challenges including model bias, limited interpretability, high computational requirements, and ethical concerns around data privacy and market manipulation. Domain-specific adaptation remains essential because financial language contains jargon and subtle expressions that general-purpose models may misinterpret.

Ergun and Sefer (2025) proposed FinSentiment, a comprehensive transfer learning framework that creates finance-specific versions of multiple pretrained models including Fin-BERT, Fin-XLNet, Fin-RoBERTa, Fin-GPT, Fin-Llama, and Fin-T5. Their experiments across three financial sentiment datasets demonstrated that models pretrained on financial corpora consistently outperform their general-domain counterparts. RoBERTa pretrained on financial text exhibited exceptional performance and robustness, achieving state-of-the-art results even when fine-tuned on as few as 250 labeled samples. This finding suggests that transfer learning techniques provide favorable solutions to financial sentiment analysis tasks, particularly in data-scarce scenarios.

#### 2.1.4 Domain-Specific Fine-Tuning Approaches

Beyond architecture selection, recent research has investigated how pre-training corpus composition and feature engineering influence model performance. Delgadillo et al. (2024) developed FinSoSent, a domain-specific language model pretrained on 49 million words from the Thomas Reuters Corpus of financial news articles. Through over 860 experiments with varying learning rates, epochs, and batch sizes, they found that selecting the right hyperparameter configuration is as critical as domain-specific pre-training for achieving optimal performance. While FinSoSent outperformed baseline models including Amazon Comprehend, GPT-3.5-Turbo, IBM Watson, SentiStrength, and VADER, the performance differences were marginal, with accuracy in the 50-60% range across tested datasets. Ensemble methods using majority voting provided modest additional improvements, underscoring the difficulty of sentiment analysis even with domain-specific approaches.

Sun et al. (2025) addressed persistent challenges in neutral sentiment recognition through EnhancedFinSentiBERT, a three-branch architecture integrating financial domain pre-training, dictionary knowledge embedding, and neutral feature extraction. The dictionary knowledge component employs dynamic weight adjustment based on word performance across financial contexts and implements multi-dimensional sentiment representation that captures not only polarity but also intensity and market impact. The neutral feature extractor uses multi-head attention mechanisms to capture subtle distinctions between neutral and sentiment-bearing expressions. In experiments comparing against BERT-base, XLNet, GPT-4, Llama 2, FinBERT, and BloombergGPT, EnhancedFinSentiBERT achieved F1 scores of 87.0% on Financial PhraseBank, 88.0% on FiQA, and 97.6% on Headline datasets. On consensus-labeled subsets, F1 scores reached 98.0%, indicating that the model performs exceptionally well when annotator agreement is high. Ablation analysis revealed that dictionary knowledge embedding and neutral feature extraction contribute most significantly to performance improvement, suggesting that architectural innovations beyond model scaling remain valuable for financial sentiment analysis.

### 2.2 Financial Sentiment and Market Prediction

Market sentiment has long been recognized as a fundamental driver of asset prices, extending far beyond rational expectations models of price formation. This section examines the theoretical foundations of investor sentiment, empirical evidence linking sentiment to market returns, and recent advances in computational sentiment analysis that enable real-time prediction across traditional and digital asset classes.

#### 2.2.1 Foundational Work on Investor Sentiment

The theoretical foundations of behavioral finance trace to Keynes' (1936) concept of "animal spirits"—the spontaneous urge to action rather than inaction that drives economic decisions beyond cold calculation. This insight anticipated decades of research demonstrating that markets are not merely information-processing mechanisms but also arenas of collective psychology.

Baker and Wurgler (2007) operationalized investor sentiment measurement through a composite index derived from six market-based proxies: closed-end fund discount, NYSE share turnover, number of IPOs, average first-day IPO return, equity share in new issues, and dividend premium. Their seminal finding revealed that sentiment predicts cross-sectional stock returns, with the effect concentrated in stocks that are difficult to arbitrage and hard to value—small stocks, young stocks, high volatility stocks, unprofitable stocks, non-dividend-paying stocks, extreme growth stocks, and distressed stocks. The sentiment index exhibits a correlation of 0.43 with contemporaneous market returns and demonstrates significant predictive power for future returns, particularly during sentiment extremes. Baker and Wurgler's framework established that sentiment is not merely noise but a systematic factor that professional investors cannot fully arbitrage away due to limits on short-selling and the costs of trading in affected securities.

#### 2.2.2 Social Media as Predictive Signal

The emergence of social media platforms created unprecedented opportunities for real-time sentiment measurement at scale. Bollen et al. (2011) conducted a foundational study using approximately 9.8 million tweets collected over ten months in 2008. Their methodology employed two sentiment tools: OpinionFinder for binary positive/negative classification and Google Profile of Mood States (GPOMS) for six-dimensional mood measurement (Calm, Alert, Sure, Vital, Kind, Happy). The critical finding was that the "Calm" dimension demonstrated Granger causality with DJIA movements at lags of 2-6 days. A Self-Organizing Fuzzy Neural Network (SOFNN) trained on historical DJIA and the Calm mood dimension achieved 86.7% directional accuracy in predicting DJIA closing values, a significant improvement over baseline models using only historical price data. This study established the principle that aggregate social media mood contains forward-looking information about market movements.

Renault (2017) extended social media sentiment research to intraday timeframes using StockTwits, a platform specifically designed for financial discussion. Analyzing S&P 500 stock discussions, the study found that first half-hour sentiment predicts last half-hour returns within the same trading day, with accuracy ranging from 74-76%. Notably, novice-labeled traders drove this effect more strongly than expert-labeled traders, suggesting that StockTwits sentiment captures retail investor psychology rather than institutional views. This finding is particularly relevant for regime detection, as retail sentiment extremes often precede market turning points when institutional investors have not yet repositioned.

#### 2.2.3 Cryptocurrency-Specific Sentiment Analysis

Cryptocurrency markets, characterized by 24/7 trading, high retail participation, and strong social media presence, provide a natural laboratory for sentiment-based prediction research. The asset class's sensitivity to narrative and community dynamics makes it particularly amenable to sentiment analysis approaches.

Kraaijeveld and De Smedt (2020) examined the predictive power of Twitter sentiment for nine major cryptocurrencies: Bitcoin, Bitcoin Cash, EOS, Ethereum, IOTA, Litecoin, NEO, Ripple, and Tron. Using a labeled dataset and machine learning classifiers, they found significant predictive relationships for Bitcoin, Bitcoin Cash, and Litecoin with lead times of 1-4 days. The study also documented that 1-14% of tweets in their corpus originated from bot accounts, highlighting data quality challenges specific to crypto sentiment analysis. Their Granger causality tests demonstrated that social media sentiment contains information not fully reflected in prices, supporting the use of sentiment as a leading indicator.

Roumeliotis et al. (2024) conducted a comprehensive comparison of language models for cryptocurrency sentiment analysis, providing crucial benchmarking data for model selection. Their evaluation found:

- Fine-tuned GPT-4: 86.7% accuracy
- FinBERT (domain-specific): 84.3% accuracy  
- BERT (general): 83.3% accuracy
- Base GPT-4 (zero-shot): 82.9% accuracy

These results demonstrate that domain-specific fine-tuning (FinBERT) achieves near-parity with state-of-the-art LLMs at substantially lower computational cost. The marginal improvement from GPT-4 fine-tuning (2.4 percentage points over FinBERT) must be weighed against significant increases in inference cost and latency, a practical consideration for real-time regime detection systems.

Raheman et al. (2022) evaluated 21 machine learning models for social media sentiment-based cryptocurrency prediction, finding that the best-performing model achieved a correlation of 0.57 between predicted and actual returns after fine-tuning. Their analysis revealed that interpretable models (gradient boosting, random forests) often outperformed black-box deep learning approaches, with peak predictive power at a -2 day lag. This finding supports the use of ensemble methods combining interpretable and neural components for robust sentiment-based prediction.

Trushkovskyi (2025) quantified the economic significance of social media sentiment for cryptocurrency returns, finding that a one-unit increase in sentiment score corresponds to 0.24-0.25% higher next-day returns. XGBoost models outperformed linear specifications, and Granger causality tests confirmed bidirectional relationships between sentiment and returns. The study's emphasis on practical trading applications—demonstrating that sentiment signals survive transaction costs—provides validation for sentiment-based regime detection approaches.

#### 2.2.4 Lead Time Evidence Synthesis

Across asset classes and methodologies, the literature consistently demonstrates that sentiment signals precede market movements. Table 2.2.1 synthesizes predictive lead times from major studies:

**Table 2.2.1: Lead Time Evidence Synthesis**

| Study | Asset Class | Lead Time | Accuracy/Correlation |
|-------|-------------|-----------|---------------------|
| Bollen et al. (2011) | Equities (DJIA) | 2-6 days | 86.7% accuracy |
| Renault (2017) | Equities (S&P 500) | Intraday (hours) | 74-76% |
| Kraaijeveld & De Smedt (2020) | Cryptocurrency | 1-4 days | Significant Granger causality |
| Raheman et al. (2022) | Cryptocurrency | -2 days peak | 0.57 correlation |
| Trushkovskyi (2025) | Cryptocurrency | 1 day | 0.24-0.25% per unit |
| Baker & Wurgler (2007) | Equities (broad) | Monthly | 0.43 correlation |

This convergence across independent studies using different methodologies, time periods, and asset classes strengthens the theoretical foundation for sentiment-based regime detection. The consistency of 1-6 day lead times suggests an optimal window for regime transition early warning systems.

#### 2.2.5 Limitations and Short-Term Prediction Challenges

Despite the encouraging evidence for sentiment-based prediction, recent research has identified important limitations that temper expectations for real-time applications. Kengmegni (2025) conducted a rigorous analysis of news sentiment for next-day stock prediction, finding that agreement ratios between sentiment signals and subsequent price movements hover around 0.5—essentially random chance. The study documented that market efficiency has increased over time, with prediction error standard deviations declining from 0.2 in 2009 to 0.065 by 2023, suggesting that markets have become more efficient at incorporating sentiment information.

Critically, Kengmegni found that economy-wide sentiment measures outperform stock-specific sentiment for prediction, implying that aggregate sentiment indices may capture systematic factors that individual stock sentiment cannot. This finding supports our research design's focus on cross-asset aggregate sentiment rather than single-security approaches. The study's conclusion that "next-day stock prediction remains elusive" underscores the importance of regime-level analysis (identifying broad market states) rather than precise return prediction.

#### 2.2.6 Cross-Asset Sentiment Spillover

While single-asset sentiment analysis is mature, cross-asset approaches remain sparse but show significant promise. Caferra (2022) examined sentiment spillovers between cryptocurrency (Bitcoin) and stock markets (S&P 500) using Transfer Entropy methods. The study found that sentiment metrics successfully mediate the relationship between these markets, with crypto sentiments affecting stock returns and economic sentiments influencing Bitcoin dynamics. Notably, entropy-based methods outperformed traditional VAR models in identifying these connections, demonstrating the value of information-theoretic approaches for cross-asset analysis.

Cao et al. (2025) investigated sentiment connectedness networks among S&P 500 firms using nonlinear Granger causality methods and entropy-based centrality measures. Their findings revealed that firms with higher sentiment connectedness face significantly elevated stock price crash risk. The effect was particularly pronounced during market extremes, when sentiment connectedness proved a better predictor than individual firm sentiment. This work demonstrates how network-based sentiment analysis can identify systemic risk propagation.

Nyakurukwa and Seetharam (2025) mapped investor sentiment networks across DJIA stocks, finding that sentiment is highly interconnected among major equities and influences market behavior through network propagation effects. Their network analysis approach provides methodological foundations for understanding how sentiment flows through interconnected markets. These foundations for cross-asset sentiment transmission are explored further in Section 2.3.

### 2.3 Cross-Asset Sentiment Analysis

While sentiment analysis has matured for individual asset classes, the integration of sentiment signals across multiple markets represents a frontier with significant theoretical and practical implications. Cross-asset sentiment analysis examines how investor psychology propagates across market boundaries, revealing interconnections that traditional correlation measures may miss. This section surveys the emerging literature on sentiment spillovers, cross-market transmission mechanisms, and the extension of sentiment analysis to forex, commodities, and multi-asset portfolio contexts.

#### 2.3.1 Sentiment Spillover Mechanisms

The theoretical foundation for cross-asset sentiment analysis rests on the observation that investor psychology does not respect asset class boundaries. Caferra (2022) provided seminal evidence of sentiment spillovers between cryptocurrency (Bitcoin) and equity markets (S&P 500) using Transfer Entropy methods—an information-theoretic approach that captures directional information flow beyond linear correlations. The study found that crypto sentiments affect stock returns while economic sentiments influence Bitcoin dynamics, demonstrating bidirectional sentiment transmission. Critically, entropy-based methods outperformed traditional VAR models in identifying these connections, suggesting that sentiment spillovers are fundamentally nonlinear phenomena requiring appropriate analytical tools.

Wang et al. (2024) extended cross-asset analysis to China's stock and bond markets, discovering asymmetric momentum transmission: stock market momentum negatively influences bond returns, while bond market momentum positively influences stock returns. Their analysis revealed that hybrid funds serve as intermediaries in this transmission mechanism, with more flexible asset allocation enabling stronger cross-market effects. For every 1% increase in hybrid fund returns, the CSI 300 Index increased by 0.73-0.86%. These findings demonstrate that institutional investment vehicles can amplify or dampen cross-asset sentiment propagation, a consideration relevant for understanding how sentiment signals may be transmitted—or distorted—across market boundaries.

#### 2.3.2 Network-Based Approaches and Sentiment Connectedness

Network analysis has emerged as a powerful framework for understanding sentiment dynamics across interconnected markets. Cao et al. (2025) investigated sentiment connectedness networks among S&P 500 firms using nonlinear Granger causality and entropy-based centrality measures, finding that firms with higher sentiment connectedness face significantly elevated stock price crash risk. The effect proved particularly pronounced during market extremes, when network-level sentiment measures outperformed individual firm sentiment for risk prediction.

Yang et al. (2025) introduced a Cross-Asset Risk Management framework leveraging large language models for real-time monitoring of equity, fixed-income, and currency markets simultaneously. Their approach synthesizes market signals across asset classes to identify potential risks and opportunities, achieving 82.1% accuracy in predicting market shifts—substantially outperforming traditional methods including blockchain-enhanced frameworks (74.0%) and conventional big data approaches (75.2%). The framework's integration of GPT-4 and Llama-3-30b for interpreting financial texts across asset classes demonstrates the practical feasibility of unified cross-asset sentiment monitoring systems.

#### 2.3.3 Forex and Currency Market Sentiment

Foreign exchange markets, characterized by 24-hour trading and sensitivity to macroeconomic narratives, present unique opportunities for sentiment-based analysis. Olaiyapo (2024) examined sentiment analysis for generating Forex trading signals, combining lexicon-based analysis with Naive Bayes classification on news articles and social media posts related to the US Dollar. The Naive Bayes model achieved 85% classification accuracy with precision of 0.87 and F1-score of 0.86. When combined with technical indicators (moving averages and RSI), the sentiment-based signals generated over 12% profit during the testing period, demonstrating the practical value of sentiment integration for currency trading.

Dakalbab et al. (2025) advanced forex prediction through a multimodal deep learning framework integrating technical and sentiment analysis via cross-modal attention mechanisms. Testing on EUR/USD, GBP/USD, and USD/JPY currency pairs, their hybrid attention model achieved accuracy of 82.9% and Matthews Correlation Coefficient of 0.744-0.776, consistently outperforming single-modality approaches. The study's key contribution was demonstrating that sentiment-technical fusion captures market dynamics that neither modality captures alone—a finding with direct implications for multi-source regime detection systems.

Sibande et al. (2021) established a direct link between herding behavior in currency markets and investor sentiment using a Twitter-based happiness index. Analyzing nine developed-market currencies, they found that forex markets exhibit strong anti-herding behavior, particularly during extreme sentiment states. The relationship between sentiment and anti-herding proved regime-specific: extreme bullish or bearish sentiment strengthened anti-herding, while average sentiment was associated with weaker effects. These findings suggest that real-time sentiment monitoring can identify periods of heightened speculative activity in currency markets—a capability directly relevant to regime detection.

#### 2.3.4 Multi-Asset Portfolio Integration

The integration of sentiment analysis into multi-asset portfolio management represents a natural extension of cross-asset research with significant practical applications. Sarfarazurrehman et al. (2025) explored AI and machine learning models for cross-asset investment risk analysis spanning real estate and equities markets. Their Deep Reinforcement Learning (DRL) and LSTM-based approaches achieved cumulative returns of 29.52% with a Sharpe ratio of 0.98, significantly outperforming traditional Mean-Variance Optimization. The study also documented that real estate investment trusts (REITs) are pervasive transmitters of long-term volatility, with shocks lasting longer than those in equities, commodities, and bonds—underscoring the importance of understanding cross-asset risk propagation.

Pankwaen et al. (2025) developed an Iterative Model Combining Algorithm (IMCA) for global cross-market trading optimization across 39 stocks from multiple regions plus Bitcoin. Their framework dynamically recalibrates model weights in response to real-time market conditions, achieving 29.52% cumulative returns and a Sharpe ratio of 0.829. Critically, the study evaluated performance during major market disruptions including COVID-19, the SVB crisis, and the 2022 crypto crash, demonstrating that adaptive multi-asset frameworks maintain effectiveness across regime transitions. The IMCA framework's success in volatile conditions suggests that dynamic, sentiment-aware approaches may be essential for robust cross-asset regime detection.

#### 2.3.5 Commodities and Safe-Haven Asset Sentiment

Commodities, particularly gold as a traditional safe-haven asset, exhibit unique sentiment dynamics that complement equity and currency analysis. Shi (2025) developed a sentiment-based GARCH-MIDAS hybrid model to explain the unusual 2020-2022 period when gold prices rose 40% despite a 12% increase in the US Dollar Index—violating their typical inverse relationship. Using FinBERT-scored sentiment from financial media, the augmented model reduced out-of-sample prediction errors by 18.7% compared to traditional volatility models (23.6% reduction in MSE versus standard GARCH).

The study identified sentiment-driven herding effects, amplified by pandemic uncertainties and geopolitical tensions, as critical channels driving the gold-DXY correlation shift. Notably, negative sentiment exhibited 1.8 times stronger marginal impact on volatility than positive sentiment—an asymmetric effect consistent with loss aversion theory in behavioral finance (see also the negativity bias findings in Nyakurukwa and Seetharam 2025, discussed in Section 2.2.5). Sentiment factors accounted for approximately 15% of previously unobserved heteroskedasticity in long-term volatility components, establishing a new paradigm for incorporating behavioral factors into commodity pricing models.

The cross-asset evidence reviewed in this section—spanning crypto-equity spillovers, currency market herding, multi-asset portfolio optimization, and commodity safe-haven dynamics—demonstrates both the feasibility and value of unified sentiment analysis frameworks. These findings motivate our research design, which synthesizes sentiment signals across all four asset classes for regime-level detection rather than single-asset prediction.

### 2.4 Market Regime Detection

Having established in Sections 2.1-2.3 that transformer-based sentiment analysis achieves strong classification performance and that sentiment signals demonstrate predictive power across individual and cross-asset contexts, we now turn to the challenge of integrating these insights for market regime detection. The identification of market regimes—distinct periods characterized by different return distributions, volatility patterns, and investor behavior—represents a critical challenge in financial modeling. Accurate regime detection enables portfolio managers to adjust allocations dynamically, hedge against downside risk, and capitalize on regime-specific opportunities. This section reviews traditional approaches, machine learning innovations, and the emerging role of sentiment signals in regime identification.

#### 2.4.1 Traditional Approaches

Classical regime detection relies on threshold-based indicators and statistical models that identify regimes from observable market data:

- **Volatility thresholds:** VIX levels exceeding 30 conventionally signal Risk-Off conditions, while sustained levels below 15 indicate complacent Risk-On environments.
- **Moving average crossovers:** Technical signals such as the Death Cross (50-day moving average crossing below 200-day) have historically coincided with bear market initiations.
- **Economic indicators:** Yield curve inversions, rising unemployment claims, and declining PMI readings serve as macroeconomic regime markers.
- **Hidden Markov Models (HMMs):** Traditional HMMs assume that observed market data emerges from a hidden state process, with regime transitions governed by fixed transition probabilities.

The fundamental limitation of these approaches is their lagging nature—they identify regimes after transitions have substantially progressed. Baker and Wurgler (2007) demonstrated that investor sentiment indices predict broad market returns, suggesting that behavioral signals may provide earlier regime indicators than price-based methods. However, their sentiment proxies relied on indirect measures (closed-end fund discounts, IPO volume, equity issuance share) rather than direct textual sentiment extraction.

#### 2.4.2 Machine Learning Methods

Modern machine learning approaches have substantially advanced regime detection by learning complex patterns from multiple signal sources:

Zhang et al. (2020) developed an explainable machine learning framework for regime-based asset allocation using hierarchical clustering. Their model integrated macroeconomic indicators with market technical signals to divide economic conditions into four distinct regimes, then applied the Black-Litterman model for portfolio optimization. Backtesting from August 2010 to May 2020 achieved 22.53% annualized returns with a Sharpe ratio of 1.06, significantly outperforming both equal-weighted benchmarks and traditional Black-Litterman implementations. Critically, their approach captured both major market upswings and successfully withdrew capital before market crashes, demonstrating the practical value of regime-aware allocation strategies.

Shu et al. (2024) proposed a statistical jump model (JM) approach that enhances traditional Markov-switching models by imposing jump penalties at each state transition. This penalty mechanism promotes regime persistence, reducing spurious switching signals that plague traditional HMMs. Evaluating the approach across U.S., German, and Japanese equity indices from 1990 to 2023, they found the JM-guided strategy consistently reduced volatility and maximum drawdown while improving Sharpe ratios compared to both buy-and-hold and HMM-guided strategies. The JM approach enhanced compound annual growth rates by 1-4% across regions while limiting turnover to approximately 44% annually.

Suárez-Cetrulo et al. (2023) conducted a systematic review of 140 studies on machine learning for financial prediction under regime change. Their analysis identified four primary algorithmic categories showing promise: evolving systems (32.1% of studies), ensemble-based methods, traditional systems adapted to concept change, and neural networks with online learning capabilities. A critical finding was that most conventional machine learning techniques struggle with abrupt structural changes—the exact characteristic that distinguishes regime transitions from normal market fluctuations. They emphasized that the literatures on online learning (concept drift) and regime switching have developed largely independently, despite addressing fundamentally similar challenges.

**Table 2.4.1: Regime Detection Performance Comparison**

| Approach | Method | Annual Return | Sharpe Ratio | Key Advantage | Citation |
|----------|--------|---------------|--------------|---------------|----------|
| Hierarchical Clustering | Black-Litterman integration | 22.53% | 1.06 | Explainability | Zhang et al. (2020) |
| Statistical Jump Model | Jump penalty regime switching | +1-4% vs. benchmark | Higher vs. HMM | Reduced turnover | Shu et al. (2024) |
| Relative Sentiment | Sentix + ML ensemble | +400-700 bps | Improved | Cross-regional validity | Micaletti (2022) |
| Mixed-Frequency | MF-EEMD-ML | — | — | 19.18% MAE reduction | Cai et al. (2024) |
| Intraday Sentiment | Field-specific lexicon | 4.55% (strategy) | 1.496 | Leading indicator | Renault (2017) |

#### 2.4.3 Sentiment-Based Regime Detection

The application of sentiment analysis to regime detection remains an emerging frontier with substantial untapped potential. Foundational work has established that sentiment signals possess predictive power for market movements:

Bollen et al. (2011) demonstrated that Twitter mood states predicted DJIA movements 2-6 days ahead with 86.7% accuracy (87.6% direction accuracy in validation), establishing sentiment as a potentially leading indicator for market direction. Their analysis identified specific emotional dimensions (calm, anxiety) that correlated with subsequent market movements, suggesting that investor psychology shifts precede price adjustments.

Renault (2017) constructed a field-specific sentiment lexicon from StockTwits messages and examined intraday relationships between sentiment and S&P 500 ETF returns. The study found that first half-hour sentiment changes predicted last half-hour returns, with the sentiment effect primarily driven by novice traders. A trading strategy exploiting this pattern achieved a Sharpe ratio of 1.496, with significant price reversal occurring the following trading day—consistent with noise trading theory. Importantly, predictability disappeared when using standard dictionary-based sentiment methods, highlighting the importance of domain-specific lexicons.

Micaletti (2022) introduced the concept of relative sentiment—the difference between institutional and individual investor sentiment expectations—for tactical asset allocation. Using Sentix economic sentiment indices across U.S., Europe, Japan, and Asia ex-Japan markets, he found that relative sentiment factors demonstrated robust predictive power across all regions, surpassing both standalone sentiment and time-series momentum in informational content. Composite relative sentiment strategies outperformed benchmarks by 400-700 basis points annually with higher Sharpe ratios and lower maximum drawdowns. Notably, when time-series momentum was negative but relative sentiment was positive, annualized returns averaged 27% versus -23% when both were negative—a 50 percentage point differential determined by sentiment state.

#### 2.4.4 Real-Time and High-Frequency Systems

The temporal resolution of sentiment-based regime detection presents significant methodological challenges. Traditional daily or weekly sentiment aggregation may miss critical intraday regime shifts, while high-frequency analysis demands sophisticated modeling to handle mixed-frequency data.

Cai et al. (2024) addressed this challenge through a "MF-EEMD-ML" prediction system that integrates half-hourly sentiment from stock message boards with three-minute stock return prediction. Their methodology employed the RR-MIDAS (Reverse Restricted Mixed Data Sampling) framework combined with Ensemble Empirical Mode Decomposition to handle non-stationarity and mixed-frequency dynamics. The system achieved maximum reductions of 19.18% in MAE, 19.08% in RMSE, and 11.71% in SMAPE compared to traditional approaches. Critically, they demonstrated that sentiment impact on high-frequency returns persists across seven intraday periods, with influence gradually weakening over time.

Shao et al. (2024) developed the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM) framework for stock return prediction. Integrating sentiment from 2.5 million Twitter posts and news sources using VADER, TextBlob, and RoBERTa, their model captured both cross-sectional dependencies across assets and temporal dynamics. The approach achieved 1.02% improvement in 1-day horizon forecasts, 0.42% for 20-day predictions, and 0.36% for 50-day forecasts compared to LSTM, Random Forest, and RNN baselines. An important practical consideration emerged: while RoBERTa-based sentiment extraction provided superior accuracy, computational costs increased from 3-6 seconds (simple methods) to up to 14 hours, highlighting trade-offs between accuracy and real-time deployment feasibility.

The temporal structure of sentiment predictability suggests a natural hierarchy: immediate sentiment shifts (intraday) provide noise trading signals, short-term aggregation (1-5 days) captures directional momentum, and medium-term patterns (weekly-monthly) may indicate regime-level transitions. Our proposed framework targets this medium-term regime detection horizon while preserving the ability to respond to rapid sentiment deterioration during crisis periods.

#### 2.4.5 Explainable AI in Regime Detection

The interpretability of regime detection models is crucial for practical deployment in risk management contexts. Black-box approaches that achieve high accuracy but provide no insight into regime characteristics limit their utility for portfolio managers who must justify allocation decisions.

Zhang et al. (2020) specifically emphasized explainability as a design criterion, noting that their hierarchical clustering approach enables visualization of regime boundaries and numerical analysis of regime-specific asset characteristics. Their four-regime classification (corresponding roughly to reflation, recovery, overheating, and stagflation phases) aligns with established economic cycle theory while being data-driven rather than imposed a priori. The integration with the Black-Litterman model provides a natural mechanism for translating regime identification into actionable portfolio views.

Micaletti (2022) found that across 990 backtests using different machine learning algorithms and factor combinations, the best-performing strategies consistently emerged from the same handful of algorithms—generalized boosted models, random forests, and certain support vector machine configurations. This consistency suggests underlying structural patterns in the sentiment-return relationship that specific algorithm families are particularly suited to capture, providing a form of implicit interpretability through algorithmic selection.

The tension between model complexity and interpretability becomes particularly acute for regime detection. Deep learning approaches may capture subtle pattern interactions but obscure the economic mechanisms driving regime transitions. For our cross-asset sentiment regime detector, we prioritize interpretable indicators (sentiment divergence scores, connectedness metrics, regime probability estimates) that enable human oversight and intervention when model outputs conflict with domain expertise.

#### 2.4.6 Risk Management Integration

The ultimate purpose of regime detection is improved risk management—protecting portfolios during adverse conditions while maintaining participation in favorable environments. Integrating sentiment signals into risk management frameworks requires understanding how sentiment dynamics relate to extreme market events.

Shu et al. (2024) demonstrated that their statistical jump model approach specifically targeted downside risk reduction. The JM-guided strategy achieved volatility reductions of approximately 2-3 percentage points versus buy-and-hold, with maximum drawdown improvements of 10-15 percentage points across tested equity indices. The approach exhibited milder drawdowns during major stress periods and provided more robust protection against adverse market movements.

Cao et al. (2025) examined sentiment connectedness and stock price crash risk using network analysis of S&P 500 stocks. They constructed sentiment spillover networks using nonlinear Granger causality and measured firm-level sentiment connectedness through multiple network centrality metrics (degree, closeness, betweenness, eigenvector centrality). Firms with higher sentiment connectedness demonstrated elevated crash risk, as they both spread and receive irrational sentiment signals more intensely. Critically, sentiment connectedness proved a better predictor of crash risk than individual firm sentiment, particularly during market extremes. Stock return synchronicity amplified the sentiment-crash relationship, while accounting conservatism provided a mitigating effect.

Nyakurukwa and Seetharam (2025) extended sentiment network analysis using TVP-VAR frequency connectedness across DJIA constituents. Their analysis decomposed sentiment connectedness into short-term (1-5 days), medium-term (5-20 days), and long-term (20+ days) components. Key findings included that sentiment shocks transmit predominantly in the short-term, negative news sentiment exhibits higher connectedness than positive sentiment (consistent with negativity bias in media coverage), and sentiment connectedness peaks during globally significant events such as COVID-19. These temporal dynamics suggest that monitoring short-term sentiment connectedness changes may provide early warning of regime stress.

For our framework, these findings motivate the inclusion of sentiment network metrics as regime transition indicators. Rapid increases in cross-asset sentiment connectedness may signal approaching regime instability, while divergence patterns (certain assets disconnecting from the sentiment network) may indicate rotation opportunities or pending contagion.

#### 2.4.7 Adaptive and Online Learning Approaches

Financial markets exhibit non-stationarity—the statistical relationships between features and returns evolve over time, rendering static models obsolete. This phenomenon, termed concept drift in the machine learning literature, presents fundamental challenges for regime detection systems that must maintain accuracy across multiple market cycles.

Suárez-Cetrulo et al. (2023) emphasized that bridging the gap between data stream learning and financial regime research remains at an early stage. Their review identified several promising approaches for handling non-stationarity:

- **Evolving systems:** Models that continuously update parameters as new data arrives, maintaining responsiveness to changing market dynamics without requiring complete retraining.
- **Ensemble methods:** Combining multiple learners with different training windows or architectural biases to provide robustness against any single approach becoming obsolete.
- **Meta-learning:** Using unsupervised algorithms to detect concept recurrence and retrieve previously effective models, or to detect drift events triggering model updates.
- **Online incremental algorithms:** Sequential learning approaches that process data point-by-point, avoiding the computational burden of batch retraining.

Shao et al. (2024) implemented time-varying coefficients within their HD-SURDLM framework, allowing sentiment-return relationships to evolve dynamically. Their use of improved Gibbs sampling with enhanced numerical stability enabled efficient sequential updating without model degradation over time. The approach demonstrated consistent outperformance across 7-year evaluation windows encompassing multiple market conditions.

For our sentiment-based regime detector, adaptive capability is essential given that the relationship between sentiment and market regimes may itself be regime-dependent. During periods of high attention and liquidity (bull markets), sentiment may strongly predict subsequent movements; during crisis periods with forced selling and liquidity constraints, sentiment-price relationships may temporarily decouple. Our design incorporates rolling window estimation and regime-specific model weighting to accommodate such structural variation.

**Research Gap Synthesis:**
Despite significant progress in both sentiment analysis and regime detection, no existing research has systematically integrated multi-source, cross-asset sentiment as a leading indicator for regime transitions. The reviewed literature establishes that: (1) sentiment signals lead price movements by measurable intervals; (2) machine learning can identify meaningful market regimes from complex signal combinations; (3) sentiment connectedness metrics correlate with crash risk and extreme market events; and (4) adaptive methods are necessary for sustained predictive accuracy. Our research fills this gap by constructing a unified sentiment aggregation framework across four asset classes (equities, cryptocurrency, forex, commodities), with the explicit goal of identifying systematic Risk-On/Risk-Off regime transitions before they manifest in traditional price-based indicators.

### 2.5 Research Gaps and Hypotheses

The preceding literature review reveals several critical gaps that motivate our research design. First, while sentiment analysis has achieved strong performance for individual asset classes, no framework systematically aggregates sentiment across equities, cryptocurrency, forex, and commodities to detect portfolio-level regime transitions. Second, despite evidence that sentiment signals lead price movements by 1-6 days, this lead time has not been exploited for regime-level early warning systems. Third, network-based approaches have demonstrated the importance of sentiment connectedness, but cross-asset sentiment networks remain unexplored. Fourth, the practical integration of multi-source sentiment (social media, news, financial reports) with regime detection algorithms has not been attempted.

Based on the literature review, we hypothesize:

**H1 (Leading Indicator Hypothesis):** Cross-asset sentiment aggregation provides a leading indicator for market regime shifts, preceding VIX-based regime detection by 1-5 trading days. This hypothesis is grounded in findings from Bollen et al. (2011) showing 2-6 day predictive lead time with 86.7% accuracy, Caferra (2022) demonstrating sentiment-mediated cross-market connections, and Trushkovskyi (2025) confirming Granger causality between sentiment and returns.

**H2 (Divergence Signal Hypothesis):** Sentiment divergence between asset classes (e.g., equities bullish while crypto bearish) signals impending transitions between Risk-On and Risk-Off regimes. Caferra (2022) found that sentiment connectedness successfully identifies market linkages, suggesting that disconnection or divergence may indicate regime instability. Wang et al. (2024) demonstrated asymmetric cross-asset momentum transmission supporting this mechanism.

**H3 (Network Effect Hypothesis):** Sentiment connectedness intensity (measured via network centrality metrics similar to Cao et al. 2025) will correlate with regime transition probability, with high connectedness during stable regimes and rapid disconnection preceding transitions. Sibande et al. (2021) found regime-specific sentiment effects in currency markets, supporting state-dependent sentiment dynamics.

**H4 (Ensemble Superiority Hypothesis):** Ensemble transformer models (FinBERT + RoBERTa) will outperform single-model approaches for sentiment classification across heterogeneous data sources, based on Mishev et al. (2020) findings that different models excel on different source types and Roumeliotis et al. (2024) demonstrating that domain-specific models achieve near-parity with LLMs at lower cost.

## 3. Methods

### 3.1 Data Quality and Preprocessing Considerations

Financial text data from social media and news sources presents unique preprocessing challenges that impact sentiment analysis accuracy. Unlike formal financial documents, social media content contains noise, sarcasm, slang, and bot-generated content that can distort sentiment signals. Kraaijeveld and De Smedt (2020) documented that 1-14% of cryptocurrency-related tweets originate from bot accounts, highlighting data quality concerns specific to social media sentiment analysis.

**Entity Recognition and Asset Classification:**
Accurately linking sentiment to specific asset classes requires robust entity recognition. Financial NER differs from general NER due to domain-specific entities (ticker symbols, ISIN codes, currency pairs), ambiguity (e.g., AAPL refers to Apple stock, not the fruit), and context-dependency where the same entity may carry different sentiment implications across asset classes.

**Multi-Source Data Integration:**
Integrating sentiment from heterogeneous sources (Reddit, Twitter, financial news) requires careful consideration of source reliability, temporal resolution, and weighting schemes. Mishev et al. (2020) noted that sentiment model performance varies significantly across data sources, with models trained on news performing differently than those trained on social media. This suggests the need for source-specific model ensembles or adaptive weighting mechanisms.

**Temporal Aggregation:**
Sentiment must be aggregated over appropriate time windows to construct meaningful indices. Daily or weekly aggregation smooths noise while preserving signal, but optimal window size may vary by asset class based on trading volume and information velocity. High-frequency crypto markets may require shorter windows than traditional equity markets.

### 3.2 Data Collection

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

### 3.3 Text Preprocessing Pipeline

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

### 3.4 Sentiment Classification

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

### 3.5 Sentiment Index Construction

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

### 3.6 Market Regime Classification

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

### 3.7 Dashboard Development

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

5. Cai, Y., Tang, Z., & Chen, Y. (2024). Can real-time investor sentiment help predict the high-frequency stock returns? Evidence from a mixed-frequency-rolling decomposition forecasting method. *North American Journal of Economics and Finance*, 70, 102147. <https://doi.org/10.1016/j.najef.2024.102147>

6. Cao, J., He, G., & Jiao, Y. (2025). Too Sensitive to Fail: The Impact of Sentiment Connectedness on Stock Price Crash Risk. *Entropy*, 27(4), 345. <https://doi.org/10.3390/e27040345>

7. Dakalbab, F., Kumar, A., Abu Talib, M., et al. (2025). Advancing Forex prediction through multimodal text-driven model and attention mechanisms. *Intelligent Systems with Applications*, 25, 200518. <https://doi.org/10.1016/j.iswa.2025.200518>

8. Delgadillo, J., Kinyua, J., & Mutigwe, C. (2024). FinSoSent: Advancing Financial Market Sentiment Analysis through Pretrained Large Language Models. *Big Data and Cognitive Computing*, 8(8), 87. <https://doi.org/10.3390/bdcc8080087>

9. Ergun, Z. E., & Sefer, E. (2025). FinSentiment: Predicting Financial Sentiment Through Transfer Learning. *Intelligent Systems in Accounting, Finance and Management*, 32(1), e70015. <https://doi.org/10.1002/isaf.70015>

10. Fatouros, G., Soldatos, J., Kouroumali, K., Makridis, G., & Kyriazis, D. (2023). Transforming sentiment analysis in the financial domain with ChatGPT. *Machine Learning with Applications*, 14, 100508. <https://doi.org/10.1016/j.mlwa.2023.100508>

11. Kengmegni, D. L. (2025). Limitations of News Sentiment Analysis for Next-Day Stock Prediction. arXiv preprint arXiv:2502.00139. <https://arxiv.org/abs/2502.00139>

12. Keynes, J. M., & Royal Economic Society (Great Britain). (1973). The general theory of employment, interest and money. Cambridge University Press for the Royal Economic Society.

13. Konstantinidis, T., Iacovides, G., Xu, M., Constantinides, T. G., & Mandic, D. (2024). FinLlama: Financial Sentiment Classification for Algorithmic Trading Applications. arXiv preprint arXiv:2403.12285. <https://arxiv.org/abs/2403.12285>

14. Kraaijeveld, O., & De Smedt, J. (2020). The predictive power of public Twitter sentiment for forecasting cryptocurrency prices. Journal of International Financial Markets, Institutions & Money, 65, Article 101188. <https://doi.org/10.1016/j.intfin.2020.101188>

15. Liu, C., Arulappan, A., Naha, R., Mahanti, A., Kamruzzaman, J., & Ra, I.-H. (2024). Large Language Models and Sentiment Analysis in Financial Markets: A Review, Datasets, and Case Study. *IEEE Access*, 12, 134041-134061. <https://doi.org/10.1109/ACCESS.2024.3445413>

16. LOUGHRAN, T., & MCDONALD, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. The Journal of Finance (New York), 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>

17. Luo, W., & Gong, D. (2024). Pre-trained Large Language Models for Financial Sentiment Analysis. arXiv preprint arXiv:2401.05215. <https://arxiv.org/abs/2401.05215>

18. Mahendran, M., Gokul, A., Lakshmi, P. S., & Preethi, S. (2025). Comparative Advances in Financial Sentiment Analysis: A Review of BERT, FinBert, and Large Language Models. *2025 International Conference on Devices, Circuits and IoT (IDCIoT)*, 1-6. <https://doi.org/10.1109/idciot64235.2025.10914764>

19. Micaletti, R. C. (2022). Relative Sentiment and Machine Learning for Tactical Asset Allocation. *SSRN Electronic Journal*. <https://dx.doi.org/10.2139/ssrn.3258071>

20. Cicekyurt, E., & Bakal, G. (2025). Enhancing Sentiment Analysis in Stock Market Tweets Through BERT-Based Knowledge Transfer. *Computational Economics*. <https://doi.org/10.1007/s10614-025-10901-8>

21. Mishev, K., Gjorgjevikj, A., Vodenska, I., Chitkushev, L. T., & Trajanov, D. (2020). Evaluation of Sentiment Analysis in Finance: From Lexicons to Transformers. *IEEE Access*, 8, 131662-131682. <https://doi.org/10.1109/ACCESS.2020.3009626>

22. Nasiopoulos, D. K., Roumeliotis, K. I., Sakas, D. P., & Athanasopoulou, N. I. (2025). Financial Sentiment Analysis and Classification: A Comparative Study of Fine-Tuned Deep Learning Models. *International Journal of Financial Studies*, 13(2), 75. <https://doi.org/10.3390/ijfs13020075>

23. Nyakurukwa, K., & Seetharam, Y. (2025). Investor sentiment networks: mapping connectedness in DJIA stocks. *Financial Innovation*, 11(1), 4. <https://doi.org/10.1186/s40854-024-00675-7>

24. Olaiyapo, O. E. (2024). Applying news and media sentiment analysis for generating forex trading signals. *Review of Business and Economics Studies*, 11(4), 84-94. <https://doi.org/10.26794/2308-944X-2023-11-4-84-94>

25. Pankwaen, K., Thongkairat, S., & Saijai, W. (2025). Global Cross-Market Trading Optimization Using Iterative Combined Algorithm: A Multi-Asset Approach with Stocks and Cryptocurrencies. *Mathematics*, 13(8), 1317. <https://doi.org/10.3390/math13081317>

26. Raheman, A., Kolonin, A., Fridkin, I., Ansari, W., Vishwas, M., Tulabandhula, T., & Bahrami, S. (2022). Social media sentiment analysis for cryptocurrency market prediction. arXiv preprint arXiv:2204.10185. <https://arxiv.org/abs/2204.10185>

27. Renault, T. (2017). Intraday online investor sentiment and return patterns in the U.S. stock market. Journal of Banking & Finance, 84, 25–40. <https://doi.org/10.1016/j.jbankfin.2017.07.002>

28. Roumeliotis, K. I., Nasiopoulos, D. K., & Tselikas, N. D. (2024). LLMs and NLP Models in Cryptocurrency Sentiment Analysis: A Comparative Classification Study. *Big Data and Cognitive Computing*, 8(6), 63. <https://doi.org/10.3390/bdcc8060063>

29. Sarfarazurrehman, S., Mane, V., & Doshi, A. (2025). AI and Machine Learning Models in Cross-Asset Class Investment Risk Analysis: A Case Study of Real Estate and Equities Markets. *2025 IEEE International Conference on Smart Systems and Applications (ICSSAS)*, 1-6. <https://doi.org/10.1109/icssas66150.2025.11081061>

30. Shao, Z., Yao, X., Chen, F., et al. (2024). Revisiting time-varying dynamics in stock market forecasting: A multi-source sentiment analysis approach with large language model. *Decision Support Systems*, 187, 114362. <https://doi.org/10.1016/j.dss.2024.114362>

31. Shen, Y., & Zhang, P. K. (2024). Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT. *IEEE International Conference on Power, Intelligent Computing and Systems (Online)*, 717–721. <https://doi.org/10.1109/ICPICS62053.2024.10796670>

32. Shi, C. (2025). Understanding Gold and Dollar Price Movements: A Sentiment-Based GARCH-MIDAS Approach. *Proceedings of the 2025 International Conference on Economics and Business Management*, 47. <https://doi.org/10.2991/978-94-6463-835-6_47>

33. Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. *Journal of Asset Management*, 25(5), 493-507. <https://doi.org/10.1057/s41260-024-00376-x>

34. Sibande, X., Gupta, R., Demirer, R., & Bouri, E. (2021). Investor Sentiment and (Anti) Herding in the Currency Market: Evidence from Twitter Feed Data. *Journal of Behavioral Finance*, 24(1), 56-72. <https://doi.org/10.1080/15427560.2021.1917579>

35. Suárez-Cetrulo, A. L., Quintana, D., & Cervantes, A. (2023). Machine Learning for Financial Prediction Under Regime Change Using Technical Analysis: A Systematic Review. *International Journal of Interactive Multimedia and Artificial Intelligence*, 8(2), 117-138. <https://doi.org/10.9781/ijimai.2023.06.003>

36. Sun, Y., Yuan, H., & Xu, F. (2025). Financial sentiment analysis for pre-trained language models incorporating dictionary knowledge and neutral features. *Natural Language Processing Journal*, 10, 100148. <https://doi.org/10.1016/j.nlp.2025.100148>

37. Trushkovskyi, V. (2025). Application of Social Media Sentiment Analysis for Stock Price Prediction. Available at SSRN. <https://dx.doi.org/10.2139/ssrn.5086695>

38. Wang, X., Wang, R., & Zhang, Y. (2024). Cross-asset momentum and the hybrid fund transmission mechanism in China's stock and bond markets. *PLOS ONE*, 19(3), e0300781. <https://doi.org/10.1371/journal.pone.0300781>

39. Yang, J., Tang, Y., Li, Y., et al. (2025). Cross-Asset Risk Management: Integrating LLMs for Real-Time Monitoring of Equity, Fixed Income, and Currency Markets. arXiv preprint arXiv:2504.04292. <https://arxiv.org/abs/2504.04292>

40. Zhang, R., Yi, C., & Chen, Y. (2020). Explainable Machine Learning for Regime-Based Asset Allocation. *2020 IEEE International Conference on Big Data (Big Data)*, 5480-5485. <https://doi.org/10.1109/BigData50022.2020.9378332>

---

## Draft-1 Changelog

**Section 2.1 Transformer Models in Financial Sentiment Analysis** — Major Expansion

| Change | Description |
|--------|-------------|
| **Structure** | Reorganized into 4 subsections (2.1.1–2.1.4) |
| **New Subsection 2.1.4** | Domain-Specific Fine-Tuning Approaches |
| **Papers Added** | 9 new papers integrated |
| **Word Count** | Expanded from ~400 to ~1,370 words |

**New Citations Added:**
- Fatouros et al. (2023) — ChatGPT forex sentiment
- Konstantinidis et al. (2024) — FinLlama
- Luo & Gong (2024) — LLaMA-2 fine-tuning
- Nasiopoulos et al. (2025) — GPT-4o vs BERT comparison
- Mahendran et al. (2025) — BERT/FinBERT/LLM review
- Ergun & Sefer (2025) — FinSentiment framework
- Delgadillo et al. (2024) — FinSoSent
- Sun et al. (2025) — EnhancedFinSentiBERT

**Section 2.2 Financial Sentiment and Market Prediction** — Major Expansion

| Change | Description |
|--------|-------------|
| **Structure** | Reorganized into 6 subsections (2.2.1–2.2.6) |
| **New Subsection 2.2.5** | Limitations and Short-Term Prediction Challenges |
| **New Subsection 2.2.6** | Cross-Asset Sentiment Spillover |
| **Papers Added** | 5 new papers integrated |
| **Word Count** | Expanded from ~650 to ~1,600 words |
| **Table Added** | Lead Time Evidence Synthesis (6 studies) |

**New Citations Added (Section 2.2):**
- Kengmegni (2025) — Limitations of news sentiment prediction
- Roumeliotis et al. (2024) — LLM/NLP crypto sentiment comparison
- Raheman et al. (2022) — Social media crypto prediction
- Trushkovskyi (2025) — Crypto sentiment economic significance

**Section 2.3 Cross-Asset Sentiment Analysis** — NEW SECTION

| Change | Description |
|--------|-------------|
| **Structure** | New section with 5 subsections (2.3.1–2.3.5) |
| **New Subsection 2.3.3** | Forex and Currency Market Sentiment |
| **New Subsection 2.3.4** | Multi-Asset Portfolio Integration |
| **New Subsection 2.3.5** | Commodities and Safe-Haven Asset Sentiment |
| **Papers Added** | 8 new papers integrated |
| **Word Count** | ~1,800 words (entirely new content) |

**New Citations Added (Section 2.3):**
- Dakalbab et al. (2025) — Multimodal forex prediction (82.9% accuracy)
- Olaiyapo (2024) — Forex sentiment trading signals (85% accuracy, 12% profit)
- Pankwaen et al. (2025) — IMCA multi-asset trading (29.52% returns)
- Sarfarazurrehman et al. (2025) — AI/ML cross-asset risk (0.98 Sharpe)
- Shi (2025) — Gold/DXY sentiment GARCH-MIDAS (18.7% improvement)
- Sibande et al. (2021) — Currency market anti-herding
- Wang et al. (2024) — Cross-asset momentum China
- Yang et al. (2025) — Cross-asset LLM risk management (82.1% accuracy)

**Section 2.4 Market Regime Detection** — MAJOR EXPANSION

| Change | Description |
|--------|-------------|
| **Structure** | Reorganized into 7 subsections (2.4.1–2.4.7) |
| **New Subsection 2.4.4** | Real-Time and High-Frequency Systems |
| **New Subsection 2.4.5** | Explainable AI in Regime Detection |
| **New Subsection 2.4.6** | Risk Management Integration |
| **New Subsection 2.4.7** | Adaptive and Online Learning Approaches |
| **Papers Added** | 5 new papers integrated |
| **Word Count** | Expanded from ~550 to ~2,400 words |
| **Table Added** | Regime Detection Performance Comparison (5 methods) |

**New Citations Added (Section 2.4):**
- Cai et al. (2024) — Real-time mixed-frequency sentiment (19.18% MAE reduction)
- Micaletti (2022) — Relative sentiment tactical allocation (400-700 bps outperformance)
- Nyakurukwa and Seetharam (2025) — TVP-VAR sentiment frequency connectedness
- Shao et al. (2024) — HD-SURDLM time-varying dynamics (1.02% improvement)
- (Expanded coverage of Zhang et al. 2020, Shu et al. 2024, Suárez-Cetrulo et al. 2023, Renault 2017, Cao et al. 2025)

**Structural Changes:**
- Section 2.3 (old: Market Regime Detection) → Section 2.4
- Section 2.4 (old: Data Quality) → Moved to Section 3.1 (Methods)
- Section 2.5 (old: Research Hypotheses) → Section 2.5 Research Gaps and Hypotheses
- Methods sections renumbered: 3.1→3.2, 3.2→3.3→3.4, etc.

**Total Reference Count:** 40 (up from 37)

**Literature Review Progress:**
- ✅ Section 2.1 Transformer Models (~1,370 words, 12 papers)
- ✅ Section 2.2 Financial Sentiment (~1,600 words, 9 papers)
- ✅ Section 2.3 Cross-Asset Sentiment (~1,800 words, 10 papers)
- ✅ Section 2.4 Market Regime Detection (~2,400 words, 10 papers)
- ✅ Section 2.5 Research Gaps and Hypotheses (~350 words)

**Estimated Section 2 Total:** ~7,520 words (target: 5,000-7,000 words)
