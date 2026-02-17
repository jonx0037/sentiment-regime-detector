# Cross-Asset Sentiment Regime Detector: Automating Market Psychology Analysis Through Multi-Source NLP

Jonathan Rocha
Advisor: Dr. David (King Ip) Lin 
Master of Science in Data Science, Southern Methodist University, Dallas, TX 75275 USA
<jrocha@smu.edu>

## Abstract

Market regime shifts often precede measurable price movements, driven by changes in collective market psychology. However, traditional risk indicators such as the VIX are inherently lagging, registering stress only after volatility has materialized. This research develops an automated **Cross-Asset Sentiment Regime Detector** to identify market transitions 1–5 trading days prior to volatility spikes. By applying ensemble transformer models (FinBERT, Llama 3) to financial news and social media across Equities, Crypto, Forex, and Commodities, we construct asset-specific sentiment indices.

Methodologically, the current implementation uses a practical **Two-Layer approximation**: first, **GARCH(1,1)** volatility features are estimated from aligned market/sentiment inputs; second, these features—augmented by proxy connectedness and divergence variables—feed a **Statistical Jump Model (JM)** to enforce regime persistence and reduce whipsaw transitions. We hypothesize that high sentiment connectedness and cross-asset divergence serve as leading indicators of "Risk-Off" transitions. Full **Asymmetric GARCH-MIDAS** and complete **walk-forward backtesting** are retained as planned Draft-1.x extensions.

## 1. Introduction

### 1.1 Background

Financial markets operate in distinct psychological regimes characterized by collective risk appetite and sentiment. Traditional technical indicators such as moving averages, RSI, and the VIX are inherently lagging; they register regime changes only after these shifts have already been reflected in price data. Yet market psychology often changes first in textual channels, including social media conversations, news coverage, and forum discussions. High-profile episodes such as the 2021 GameStop short squeeze, the 2020 COVID-19 crash, and the 2022 crypto winter all displayed recognizable sentiment patterns before, during, and after regime transitions.

Existing sentiment analysis tools are not well-suited to systematic, portfolio-level regime detection. Most solutions focus on single asset classes or individual securities, forcing analysts to manually synthesize sentiment with technical indicators and macro data. Where more sophisticated, institutional-grade sentiment platforms do exist—such as Bloomberg and RavenPack—costs often exceed $20,000 per year, limiting accessibility for smaller institutions and retail investors. Moreover, many sentiment methods still rely on rudimentary keyword-based scoring rather than leveraging modern transformer architectures that can capture nuance, sarcasm, and context.

### 1.2 Problem Statement

The fundamental problem in modern algorithmic risk management is the reliance on lagging indicators to detect structural regime shifts. Traditional volatility metrics, such as the VIX or realized variance, are inherently reactive; they register "Risk-Off" states only after significant price deterioration. While behavioral finance theory suggests that shifts in collective market psychology precede price action, operationalizing this "lead time" has proven computationally difficult due to three specific failures in current modeling approaches:

1. **Regime Instability (The "Whipsaw" Problem):** Standard regime detection methods, particularly Hidden Markov Models (HMMs), lack mechanisms to enforce signal persistence. Shu et al. (2024) demonstrate that HMMs are overly sensitive to daily market noise, generating frequent, spurious state transitions that erode returns through excessive transaction costs.

2. **The Mixed-Frequency Gap:** Financial sentiment data is stochastic and irregular (arriving via news and social feeds), while price data is deterministic and regular. Traditional models often force-align these data streams using simple rolling averages, destroying the high-frequency signal contained in sentiment bursts. Cai et al. (2024) highlight that failure to account for these mixed frequencies results in a loss of predictive accuracy regarding short-term return volatility.

3. **Siloed Asset Analysis:** Existing sentiment frameworks predominantly focus on single-asset classes (e.g., only Equities or only Crypto). However, recent findings by Shi (2025) and Sarfarazurrehman et al. (2025) indicate that volatility transmission is a cross-asset phenomenon, where sentiment shocks in one market (e.g., Commodities or REITs) act as leading indicators for others. Current systems lack the unified architecture required to detect these cross-asset "decoupling" or "spillover" signals.

### 1.3 Significance of the Study

This research bridges the gap between theoretical behavioral finance and practical, automated risk management by developing a **Two-Layer Cross-Asset Sentiment Regime Detector**. The study makes significant contributions in three specific domains:

1. **Methodological Advancement:** By integrating **GARCH-MIDAS** for volatility state estimation with **Statistical Jump Models (JMs)** for discrete classification, this research overcomes the "whipsaw" limitations of HMMs. We validate the application of jump penalties to enforce regime persistence, a technique shown by Shu et al. (2024) to reduce portfolio turnover by approximately 44% while improving Sharpe ratios. This establishes a new standard for robust regime detection that filters noise without sacrificing responsiveness.

2. **Theoretical Validation of Sentiment Transmission:** This study empirically operationalizes the **Network Effect Hypothesis (H3)** and **Divergence Signal Hypothesis (H2)**. By employing Entropy-based connectedness measures (following Cao et al., 2025) and Transfer Entropy (following Caferra, 2022), we quantify how sentiment contagion across Equities, Crypto, and Commodities precedes systemic crashes. This moves the field beyond simple correlation analysis to causal network mapping of market psychology.

3. **Practical Democratization:** Historically, institutional-grade sentiment analysis has been gated behind high-cost terminals (e.g., Bloomberg, RavenPack). By leveraging open-source Large Language Models (LLMs) such as Llama 3 and fine-tuned BERT architectures, this project delivers a reproducible, high-performance framework that democratizes access to "Lead-Time" risk signals, enabling smaller institutions and retail algorithmic traders to anticipate volatility 1–5 days in advance.

### 1.4 Research Objectives

This research addresses these limitations by developing an automated, cross-asset sentiment analysis system designed explicitly for market regime detection. The goal is to build a framework that identifies regime transitions as leading indicators rather than contemporaneous reflections of price behavior, while remaining accessible through an intuitive web interface. Methodologically, the project applies ensemble transformer models to aggregate sentiment across diverse text sources and asset classes, extending recent advances in financial NLP to a multi-source, cross-asset setting. Practically, it delivers an open-source system that lowers the barrier to institutional-grade sentiment analysis and makes regime-level insights available beyond large buy-side firms. Theoretically, it proposes and tests a structured mapping from multi-source sentiment patterns to macroeconomic regime states, contributing to a richer understanding of how collective market psychology manifests in text data and precedes observable price and volatility dynamics.

## 2. Literature Review

### 2.1 Transformer Models in Financial Sentiment Analysis

#### 2.1.1 From Lexicons to BERT

The evolution of financial sentiment analysis mirrors the transition in natural language processing from symbolic, rule-based methods to neural network-based contextual language models. Initial approaches applied domain-adapted sentiment lexicons to extract polarity-bearing terms in financial corpora. Loughran and McDonald (2011) showed that generic sentiment dictionaries yield low precision for financial texts, as terms like “liability” possess distinct semantic valence in finance compared to general English. Their finance-oriented lexicon remediated this mismatch and established a benchmark resource for subsequent computational finance research.

The introduction of transformer-based architectures marked a paradigm shift in financial sentiment analysis. For instance, Araci (2019) introduced FinBERT, a BERT model fine-tuned on financial news and analyst reports, which achieved a 15% improvement in accuracy over previous state-of-the-art methods. Moreover, FinBERT demonstrated effectiveness even with limited labeled data, outperforming baseline models when trained on as few as 500 examples. As a result, this finding established the viability of transfer learning for financial NLP tasks with scarce labeled datasets.

Mishev et al. (2020) conducted over 100 experiments to systematically evaluate sentiment analysis approaches ranging from lexicons to transformers. Their comprehensive study compared BERT variants, including RoBERTa, XLNet, ALBERT, and DistilBERT, across multiple financial datasets. The results demonstrated that contextual embeddings achieve substantially greater efficiency than lexicons and fixed word encoders. BART and ALBERT-xxlarge achieved the highest performance with Matthews Correlation Coefficient scores of 0.895 and 0.881, respectively. Notably, distilled versions of transformers, such as DistilBERT, retained more than 95% of BERT’s accuracy while requiring 40% fewer parameters, making them suitable for production environments with constrained computational resources.

#### 2.1.2 Large Language Models

The rise of large language models (LLMs) has enhanced financial sentiment analysis, especially via zero-shot and few-shot learning frameworks. Fatouros et al. (2023) assessed ChatGPT 3.5 for FX market sentiment evaluation, observing approximately 35% greater sentiment classification accuracy and 36% higher correlation with market returns than the domain-adapted FinBERT. Their zero-shot evaluation confirmed that LLMs can parse and classify financial texts without supervised domain adaptation, although prompt engineering was identified as a critical variable affecting output.

Konstantinidis et al. (2024) introduced FinLlama, a fine-tuned Llama 2 7B model optimized for financial sentiment analysis. They implemented Low-Rank Adaptation (LoRA) to reduce computational complexity, lowering the number of trainable parameters to 0.0638% of the total while maintaining model accuracy. In portfolio optimization tasks, FinLlama produced cumulative returns 44.7% higher than those of FinBERT-based portfolios, along with higher Sharpe ratios and lower annualized volatility. Beyond binary sentiment detection, FinLlama provides sentiment polarity scores, enabling traders to extract nuanced insights from financial news articles.

Luo and Gong (2024) demonstrated that supervised fine-tuning of LLaMA-2 7B achieves state-of-the-art performance on the Financial PhraseBank benchmark, improving accuracy from 0.86 to 0.90. Their experiments compared few-shot learning, further pre-training, and supervised fine-tuning, finding that further pre-training alone does not yield noticeable improvement over baseline performance. The supervised fine-tuning approach proved most effective, confirming that task-specific adaptation remains essential even for large pre-trained models.

Shen and Zhang (2024) compared FinBERT against GPT-3.5-turbo and GPT-4o for sentiment analysis on financial news articles and reports. Their findings indicated that FinBERT with domain-specific pre-training consistently outperformed general-purpose LLMs in accuracy, precision, recall, and F1-score. However, GPT-4o with few-shot examples of financial texts achieved competitive results, suggesting that effective prompt engineering can make general-purpose LLMs viable tools for financial sentiment analysis without extensive fine-tuning.

#### 2.1.3 Model Comparison and Selection Criteria

Systematic comparisons across model architectures have clarified the trade-offs between accuracy, computational cost, and deployment considerations. Nasiopoulos et al. (2025) conducted a comparative study of fine-tuned deep learning models, including GPT-4o, GPT-4o-mini, BERT, and FinBERT, benchmarked against traditional machine learning classifiers. Using Bayesian optimization across 100 trials for hyperparameter tuning, they found that fine-tuned GPT-4o and GPT-4o-mini achieved 87.79% accuracy on the combined FiQA and Financial PhraseBank datasets. Traditional approaches, including Support Vector Machines, Random Forests, and Logistic Regression, lagged substantially behind, with accuracies of 64.53% to 65.31%. Fine-tuned LLMs outperformed fine-tuned BERT models by approximately 9% in mean accuracy, though at the cost of increased computational time and inference expense.

Mahendran et al. (2025) reviewed advances in financial sentiment analysis using BERT, FinBERT, and large language models, highlighting practical considerations for deployment. Their analysis noted that DistilBERT retains 97% of BERT’s capabilities while requiring only half the parameters, making it suitable for low-latency applications such as algorithmic trading and real-time market monitoring. The review identified persistent challenges, including model bias, limited interpretability, high computational requirements, and ethical concerns around data privacy and market manipulation. Domain-specific adaptation remains essential because financial language contains jargon and subtle expressions that general-purpose models may misinterpret.

Liu et al. (2024) provided a comprehensive review of large language models and sentiment analysis in financial markets, synthesizing advances across datasets, methodologies, and application domains. Their analysis cataloged publicly available financial sentiment datasets and evaluated both traditional machine learning approaches and modern transformer-based methods. The review emphasized that while LLMs demonstrate impressive zero-shot capabilities, their practical deployment in financial contexts requires careful consideration of inference latency, computational costs, and the need for domain-specific calibration. Their case study on market prediction illustrated how sentiment features derived from news and social media can be integrated with technical indicators to improve forecasting accuracy.

Ergun and Sefer (2025) proposed FinSentiment, a comprehensive transfer-learning framework that produces finance-specific versions of multiple pretrained models, including Fin-BERT, Fin-XLNet, Fin-RoBERTa, Fin-GPT, Fin-Llama, and Fin-T5. Their experiments across three financial sentiment datasets demonstrated that models pretrained on financial corpora consistently outperform their general-domain counterparts. RoBERTa pretrained on financial text exhibited exceptional performance and robustness, achieving state-of-the-art results even when fine-tuned on as few as 250 labeled samples. This finding suggests that transfer learning techniques offer effective solutions for financial sentiment analysis, particularly in data-scarce settings.

#### 2.1.4 Domain-Specific Fine-Tuning Approaches

Beyond architecture selection, recent research has investigated how the composition of the pre-training corpus and feature engineering influence model performance. Delgadillo et al. (2024) developed FinSoSent, a domain-specific language model pretrained on 49 million words from the Thomas Reuters Corpus of financial news articles. Through over 860 experiments with varying learning rates, epochs, and batch sizes, they found that selecting the right hyperparameter configuration is as critical as domain-specific pre-training for achieving optimal performance. While FinSoSent outperformed baseline models, including Amazon Comprehend, GPT-3.5-Turbo, IBM Watson, SentiStrength, and VADER, the performance differences were marginal, with accuracy in the 50-60% range across tested datasets. Ensemble methods using majority voting provided modest additional improvements, underscoring the difficulty of sentiment analysis even with domain-specific approaches.

Cicekyurt and Bakal (2025) explored BERT-based knowledge transfer to enhance sentiment analysis of stock market tweets. Their approach leveraged pre-trained BERT representations and applied targeted fine-tuning on Twitter-specific financial discourse, addressing the unique linguistic characteristics of social media text, including abbreviations, hashtags, and informal language. The study demonstrated that knowledge transfer from general-domain BERT to finance-specific Twitter data yields significant performance improvements over training from scratch, particularly when labeled data is limited. Their findings reinforce the value of transfer learning strategies for sentiment analysis of noisy, informal financial text.

Sun et al. (2025) addressed persistent challenges in neutral sentiment recognition with EnhancedFinSentiBERT, a three-branch architecture integrating financial-domain pre-training, dictionary knowledge embedding, and neutral feature extraction. The dictionary knowledge component employs dynamic weight adjustment based on word performance across financial contexts and implements a multi-dimensional sentiment representation that captures not only polarity but also intensity and market impact. The neutral feature extractor uses multi-head attention mechanisms to capture subtle distinctions between neutral and sentiment-bearing expressions. In experiments comparing against BERT-base, XLNet, GPT-4, Llama 2, FinBERT, and BloombergGPT, EnhancedFinSentiBERT achieved F1 scores of 87.0% on Financial PhraseBank, 88.0% on FiQA, and 97.6% on Headline datasets. On consensus-labeled subsets, F1 scores reached 98.0%, indicating that the model performs exceptionally well when annotator agreement is high. Ablation analysis revealed that dictionary knowledge embedding and neutral feature extraction contribute most significantly to performance improvement, suggesting that architectural innovations beyond model scaling remain valuable for financial sentiment analysis.

#### 2.1.5 The Generative Shift: Encoder vs. Decoder Architectures

While encoder-only architectures such as FinBERT (Araci, 2019) established the benchmark for financial sentiment analysis by leveraging bidirectional context for classification, recent scholarship indicates a paradigm shift toward decoder-based Generative AI models. Encoder models excel at feature extraction but often struggle with the nuanced, implicit sentiment characteristic of complex financial discourse. In contrast, decoder-based Large Language Models (LLMs), such as Llama 2 and GPT-4, utilize autoregressive capabilities to capture broader contextual dependencies.

Empirical comparisons highlight the superior efficacy of these generative approaches. Konstantinidis et al. (2024) introduced **FinLlama**, a fine-tuned Llama 2 7B model, which outperformed FinBERT in portfolio construction tasks, achieving 44.7% higher cumulative returns and a superior Sharpe ratio (2.4 vs. 1.5) by better quantifying sentiment strength rather than just polarity. Similarly, Fatouros et al. (2023) found that ChatGPT (a decoder-only model) exhibited a 35% performance improvement over FinBERT in classifying Forex news sentiment and demonstrated a 36% higher correlation with market returns, largely due to its ability to interpret domain-specific jargon in zero-shot settings.

Furthermore, Nasiopoulos et al. (2025) reported that fine-tuned LLMs (specifically GPT-4o) outperformed fine-tuned FinBERT by approximately 9.68% in classification accuracy on the FiQA and Financial PhraseBank datasets. Luo and Gong (2024) corroborated this, demonstrating that a Supervised Fine-Tuned (SFT) Llama 2-7B achieved state-of-the-art accuracy (0.90) compared to FinBERT (0.86), validating that generative architectures offer a more robust framework for detecting market signals despite their higher computational latency. Consequently, this research posits that while Encoder models offer speed, Decoder models provide the requisite semantic depth for accurate regime detection.

### 2.2 Financial Sentiment and Market Prediction

Market sentiment has long been recognized as a fundamental driver of asset prices, extending far beyond rational expectations models of price formation. This section examines the theoretical foundations of investor sentiment, empirical evidence linking sentiment to market returns, and recent advances in computational sentiment analysis that enable real-time prediction across traditional and digital asset classes.

#### 2.2.1 Foundational Work on Investor Sentiment

The theoretical foundations of behavioral finance trace to Keynes’ (1936) concept of “animal spirits”—the spontaneous urge to action rather than inaction that drives economic decisions beyond cold calculation. This insight anticipated decades of research demonstrating that markets are not merely information-processing mechanisms but also arenas of collective psychology.

Baker and Wurgler (2007) operationalized investor sentiment measurement through a composite index derived from six market-based proxies: the closed-end fund discount, NYSE share turnover, the number of IPOs, the average first-day IPO return, equity share in new issues, and the dividend premium. Their seminal finding revealed that sentiment predicts cross-sectional stock returns, with the effect concentrated in difficult-to-arbitrage, hard-to-value stocks—small, young, high-volatility, unprofitable, non-dividend-paying, extreme-growth, and distressed. The sentiment index exhibits a correlation of 0.43 with contemporaneous market returns and demonstrates significant predictive power for future returns, particularly during sentiment extremes. Baker and Wurgler’s framework established that sentiment is not merely noise but a systematic factor that professional investors cannot fully arbitrage away due to limits on short-selling and the costs of trading in affected securities.

#### 2.2.2 Social Media as Predictive Signal

The emergence of social media platforms created unprecedented opportunities for real-time, scale sentiment measurement. Bollen et al. (2011) conducted a foundational study using approximately 9.8 million tweets collected over ten months in 2008. Their methodology employed two sentiment tools: OpinionFinder for binary positive/negative classification and Google Profile of Mood States (GPOMS) for six-dimensional mood measurement (Calm, Alert, Sure, Vital, Kind, Happy). The critical finding was that the “Calm” dimension demonstrated Granger causality with DJIA movements at lags of 2-6 days. A Self-Organizing Fuzzy Neural Network (SOFNN) trained on historical DJIA and the Calm mood dimension achieved 86.7% directional accuracy in predicting DJIA closing values, a significant improvement over baseline models using only historical price data. This study established the principle that aggregate social media mood contains forward-looking information about market movements.

Renault (2017) extended social media sentiment research to intraday timeframes using StockTwits, a platform specifically designed for financial discussion. Analyzing S&P 500 stock discussions, the study found that first-half-hour sentiment predicts last-half-hour returns on the same trading day, with accuracy ranging from 74% to 76%. Notably, novice-labeled traders drove this effect more strongly than expert-labeled traders, suggesting that StockTwits sentiment captures retail investor psychology rather than institutional views. This finding is particularly relevant for regime detection, as retail sentiment extremes often precede market turning points when institutional investors have not yet repositioned.

#### 2.2.3 Cryptocurrency-Specific Sentiment Analysis

Cryptocurrency markets, characterized by 24/7 trading, high retail participation, and strong social media presence, provide a natural laboratory for sentiment-based prediction research. The asset class’s sensitivity to narrative and community dynamics makes it particularly amenable to sentiment analysis approaches.

Kraaijeveld and De Smedt (2020) examined the predictive power of Twitter sentiment for nine major cryptocurrencies: Bitcoin, Bitcoin Cash, EOS, Ethereum, IOTA, Litecoin, NEO, Ripple, and Tron. Using a labeled dataset and machine learning classifiers, they found significant predictive relationships for Bitcoin, Bitcoin Cash, and Litecoin with lead times of 1-4 days. The study also documented that 1-14% of tweets in their corpus originated from bot accounts, highlighting data quality challenges specific to crypto sentiment analysis. Their Granger causality tests showed that social media sentiment contains information not fully reflected in prices, supporting its use as a leading indicator.

Roumeliotis et al. (2024) conducted a comprehensive comparison of language models for cryptocurrency sentiment analysis, providing crucial benchmarking data for model selection. Their evaluation found:

    • Fine-tuned GPT-4: 86.7% accuracy
    • FinBERT (domain-specific): 84.3% accuracy
    • BERT (general): 83.3% accuracy
    • Base GPT-4 (zero-shot): 82.9% accuracy

These results demonstrate that domain-specific fine-tuning (FinBERT) achieves near-parity with state-of-the-art LLMs at substantially lower computational cost. The marginal improvement from GPT-4 fine-tuning (2.4 percentage points over FinBERT) must be weighed against significant increases in inference cost and latency, a practical consideration for real-time regime detection systems.

Raheman et al. (2022) evaluated 21 machine learning models for social media sentiment-based cryptocurrency prediction, finding that the best-performing model achieved a correlation of 0.57 between predicted and actual returns after fine-tuning. Their analysis revealed that interpretable models (gradient boosting, random forests) often outperformed black-box deep learning approaches, with peak predictive power at a -2 day lag. This finding supports the use of ensemble methods combining interpretable and neural components for robust sentiment-based prediction.

Trushkovskyi (2025) quantified the economic significance of social media sentiment for cryptocurrency returns, finding that a one-unit increase in sentiment score corresponds to 0.24-0.25% higher next-day returns. XGBoost models outperformed linear specifications, and Granger causality tests confirmed bidirectional relationships between sentiment and returns. The study’s emphasis on practical trading applications—demonstrating that sentiment signals survive transaction costs—provides validation for sentiment-based regime detection approaches.

#### 2.2.4 Lead Time Evidence Synthesis

Across asset classes and methodologies, the literature consistently demonstrates that sentiment signals precede market movements. Table 2.2.1 synthesizes predictive lead times from major studies:

Table 2.2.1: Lead Time Evidence Synthesis

Study Asset Class Lead Time Accuracy/Correlation
Bollen et al. (2011) Equities (DJIA) 2-6 days 86.7% accuracy
Renault (2017) Equities (S&P 500) Intraday (hours) 74-76%
Kraaijeveld & De Smedt (2020) Cryptocurrency 1-4 days Significant Granger causality
Raheman et al. (2022) Cryptocurrency -2 days peak 0.57 correlation
Trushkovskyi (2025) Cryptocurrency 1 day 0.24-0.25% per unit
Baker & Wurgler (2007) Equities (broad) Monthly 0.43 correlation

This convergence across independent studies using different methodologies, time periods, and asset classes strengthens the theoretical foundation for sentiment-based regime detection. The consistency of 1-6 day lead times suggests an optimal window for regime-transition early-warning systems.

#### 2.2.5 Limitations and Short-Term Prediction Challenges

Despite the encouraging evidence for sentiment-based prediction, recent research has identified important limitations that temper expectations for real-time applications. Kengmegni (2024) conducted a rigorous analysis of news sentiment for next-day stock prediction, finding that agreement ratios between sentiment signals and subsequent price movements hover around 0.5—essentially random chance. The study documented that market efficiency has increased over time, with prediction error standard deviations declining from 0.2 in 2009 to 0.065 by 2023, suggesting that markets have become more efficient at incorporating sentiment information.

Critically, Kengmegni found that economy-wide sentiment measures outperform stock-specific sentiment for predictive purposes, suggesting that aggregate sentiment indices may capture systematic factors that individual stock sentiment cannot. This finding supports our research design’s focus on cross-asset aggregate sentiment rather than single-security approaches. The study’s conclusion that “next-day stock prediction remains elusive” underscores the importance of regime-level analysis (identifying broad market states) rather than precise return prediction.

#### 2.2.6 Cross-Asset Sentiment Spillover

While single-asset sentiment analysis is mature, cross-asset approaches remain sparse but show significant promise. Caferra (2022) examined sentiment spillovers between cryptocurrency (Bitcoin) and stock markets (S&P 500) using Transfer Entropy methods. The study found that sentiment metrics mediate the relationship between these markets: crypto sentiment affects stock returns, and economic sentiment influences Bitcoin dynamics. Notably, entropy-based methods outperformed traditional VAR models in identifying these connections, demonstrating the value of information-theoretic approaches for cross-asset analysis.

Cao et al. (2025) investigated sentiment-connectedness networks among S&P 500 firms using nonlinear Granger causality methods and entropy-based centrality measures. Their findings revealed that firms with higher sentiment connectedness face significantly elevated stock price crash risk. The effect was particularly pronounced during market extremes, when sentiment connectedness proved a better predictor than individual firm sentiment. This work demonstrates how network-based sentiment analysis can identify the propagation of systemic risk.

Nyakurukwa and Seetharam (2025) mapped investor sentiment networks across DJIA stocks, finding that sentiment is highly interconnected among major equities and influences market behavior through network propagation effects. Their network analysis approach provides methodological foundations for understanding how sentiment flows through interconnected markets. These foundations for cross-asset sentiment transmission are explored further in Section 2.3.

### 2.3 Cross-Asset Sentiment Analysis

While sentiment analysis has matured for individual asset classes, integrating sentiment signals across multiple markets remains a frontier with significant theoretical and practical implications. Cross-asset sentiment analysis examines how investor psychology propagates across market boundaries, revealing interconnections that traditional correlation measures may miss. This section surveys the emerging literature on sentiment spillovers, cross-market transmission mechanisms, and the extension of sentiment analysis to forex, commodities, and multi-asset portfolio contexts.

#### 2.3.1 Sentiment Spillover Mechanisms

The theoretical foundation for cross-asset sentiment analysis rests on the observation that investor psychology does not respect asset class boundaries. Caferra (2022) provided seminal evidence of sentiment spillovers between cryptocurrency (Bitcoin) and equity markets (S&P 500) using Transfer Entropy methods—an information-theoretic approach that captures directional information flow beyond linear correlations. The study found that crypto sentiment affects stock returns, while economic sentiment influences Bitcoin dynamics, demonstrating bidirectional sentiment transmission. Critically, entropy-based methods outperformed traditional VAR models in identifying these connections, suggesting that sentiment spillovers are fundamentally nonlinear phenomena requiring appropriate analytical tools.

Wang et al. (2024) extended cross-asset analysis to China’s stock and bond markets, discovering asymmetric momentum transmission: stock market momentum negatively influences bond returns, while bond market momentum positively influences stock returns. Their analysis revealed that hybrid funds serve as intermediaries in this transmission mechanism, with more flexible asset allocation enabling stronger cross-market effects. For every 1% increase in hybrid fund returns, the CSI 300 Index increased by 0.73-0.86%. These findings demonstrate that institutional investment vehicles can amplify or dampen cross-asset sentiment propagation, a consideration relevant for understanding how sentiment signals may be transmitted—or distorted—across market boundaries.

#### 2.3.2 Network-Based Approaches and Sentiment Connectedness

Network analysis has emerged as a powerful framework for understanding sentiment dynamics across interconnected markets. Cao et al. (2025) investigated sentiment-connectedness networks among S&P 500 firms using nonlinear Granger causality and entropy-based centrality measures, finding that firms with higher sentiment connectedness face significantly elevated stock price crash risk. The effect was particularly pronounced during market extremes, when network-level sentiment measures outperformed individual-firm sentiment for risk prediction.

Yang et al. (2025) introduced a Cross-Asset Risk Management framework that leverages large language models for real-time monitoring of equity, fixed-income, and currency markets. Their approach synthesizes market signals across asset classes to identify potential risks and opportunities, achieving 82.1% accuracy in predicting market shifts—substantially outperforming traditional methods, including blockchain-enhanced frameworks (74.0%) and conventional big data approaches (75.2%). The framework’s integration of GPT-4 and Llama-3-30b for interpreting financial texts across asset classes demonstrates the practical feasibility of unified, cross-asset sentiment-monitoring systems.

#### 2.3.3 Forex and Currency Market Sentiment

Foreign exchange markets, characterized by 24-hour trading and sensitivity to macroeconomic narratives, present unique opportunities for sentiment-based analysis. Olaiyapo (2024) examined sentiment analysis for generating Forex trading signals, combining lexicon-based analysis with Naive Bayes classification on news articles and social media posts related to the US Dollar. The Naive Bayes model achieved 85% classification accuracy with a precision of 0.87 and an F1-score of 0.86. When combined with technical indicators (moving averages and RSI), the sentiment-based signals generated over 12% profit during the testing period, demonstrating the practical value of sentiment integration for currency trading.

Dakalbab et al. (2025) advanced forex prediction by integrating technical and sentiment analysis via cross-modal attention mechanisms within a multimodal deep learning framework. Testing on EUR/USD, GBP/USD, and USD/JPY currency pairs, their hybrid attention model achieved an accuracy of 82.9% and a Matthews Correlation Coefficient of 0.744-0.776, consistently outperforming single-modality approaches. The study’s key contribution was demonstrating that sentiment-technical fusion captures market dynamics that neither modality alone captures—a finding with direct implications for multi-source regime-detection systems.

Sibande et al. (2021) established a direct link between herding behavior in currency markets and investor sentiment using a Twitter-based happiness index. Analyzing nine developed-market currencies, they found that forex markets exhibit strong anti-herding behavior, particularly during extreme sentiment states. The relationship between sentiment and anti-herding proved regime-specific: extreme bullish or bearish sentiment strengthened anti-herding, while average sentiment was associated with weaker effects. These findings suggest that real-time sentiment monitoring can identify periods of heightened speculative activity in currency markets—a capability directly relevant to regime detection.

#### 2.3.4 Multi-Asset Portfolio Integration

The integration of sentiment analysis into multi-asset portfolio management represents a natural extension of cross-asset research with significant practical applications. Sarfarazurrehman et al. (2025) explored AI and machine learning models for cross-asset investment risk analysis spanning real estate and equities markets. Their Deep Reinforcement Learning (DRL) and LSTM-based approaches achieved cumulative returns of 29.52% with a Sharpe ratio of 0.98, significantly outperforming traditional Mean-Variance Optimization. The study also documented that real estate investment trusts (REITs) are pervasive transmitters of long-term volatility, with shocks lasting longer than those in equities, commodities, and bonds—underscoring the importance of understanding cross-asset risk propagation.

Pankwaen et al. (2025) developed an Iterative Model Combining Algorithm (IMCA) for global cross-market trading optimization across 39 stocks from multiple regions plus Bitcoin. Their framework dynamically recalibrates model weights in response to real-time market conditions, achieving cumulative returns of 29.52% and a Sharpe ratio of 0.829. Critically, the study evaluated performance during major market disruptions, including COVID-19, the SVB crisis, and the 2022 crypto crash, demonstrating that adaptive multi-asset frameworks maintain effectiveness across regime transitions. The IMCA framework’s success in volatile conditions suggests that dynamic, sentiment-aware approaches may be essential for robust cross-asset regime detection.

#### 2.3.5 Commodities and Safe-Haven Asset Sentiment

Commodities, particularly gold as a traditional safe-haven asset, exhibit unique sentiment dynamics that complement equity and currency analysis. Shi (2025) developed a sentiment-based GARCH-MIDAS hybrid model to explain the unusual 2020-2022 period when gold prices rose 40% despite a 12% increase in the US Dollar Index—violating their typical inverse relationship. Using FinBERT-scored sentiment from financial media, the augmented model reduced out-of-sample prediction errors by 18.7% compared to traditional volatility models (23.6% reduction in MSE versus standard GARCH).

The study identified sentiment-driven herding effects, amplified by pandemic uncertainties and geopolitical tensions, as critical drivers of the shift in the gold-DXY correlation. Notably, negative sentiment exhibited 1.8 times stronger marginal impact on volatility than positive sentiment—an asymmetric effect consistent with loss aversion theory in behavioral finance (see also the negativity bias findings in Nyakurukwa and Seetharam 2025, discussed in Section 2.2.5). Sentiment factors accounted for approximately 15% of previously unobserved heteroskedasticity in long-term volatility components, establishing a new paradigm for incorporating behavioral factors into commodity pricing models.

The cross-asset evidence reviewed in this section—spanning crypto-equity spillovers, currency market herding, multi-asset portfolio optimization, and commodity safe-haven dynamics—demonstrates both the feasibility and value of unified sentiment analysis frameworks. These findings motivate our research design, which synthesizes sentiment signals across all four asset classes for regime-level detection rather than single-asset prediction.

### 2.4 Market Regime Detection

Having established in Sections 2.1-2.3 that transformer-based sentiment analysis achieves strong classification performance, and that sentiment signals demonstrate predictive power across individual and cross-asset contexts, we now turn to the challenge of integrating these insights for market regime detection. The identification of market regimes—distinct periods characterized by different return distributions, volatility patterns, and investor behavior—represents a critical challenge in financial modeling. Accurate regime detection enables portfolio managers to dynamically adjust allocations, hedge against downside risk, and capitalize on regime-specific opportunities. This section reviews traditional approaches, machine learning innovations, and the emerging role of sentiment signals in regime identification.

#### 2.4.1 Traditional Approaches

Classical regime detection relies on threshold-based indicators and statistical models that identify regimes from observable market data:

    • **Volatility thresholds:** VIX levels above 30 conventionally signal Risk-Off conditions, while sustained levels below 15 indicate a complacent Risk-On environment.
    • **Moving average crossovers:** Technical signals such as the Death Cross (50-day moving average crossing below the 200-day) have historically coincided with bear-market initiations.
    • **Economic indicators:** Yield curve inversions, rising unemployment claims, and declining PMI readings serve as macroeconomic regime markers.
    • **Hidden Markov Models (HMMs):** Traditional HMMs assume that observed market data emerges from a hidden state process, with regime transitions governed by fixed transition probabilities.

The fundamental limitation of these approaches is their lag—they identify regimes after transitions have already progressed substantially. Baker and Wurgler (2007) demonstrated that investor sentiment indices predict broad market returns, suggesting that behavioral signals may provide earlier regime indicators than price-based methods. However, their sentiment proxies relied on indirect measures (closed-end fund discounts, IPO volume, equity issuance share) rather than direct textual sentiment extraction.

#### 2.4.2 Machine Learning Methods

Modern machine learning approaches have substantially advanced regime detection by learning complex patterns from multiple signal sources.

##### 2.4.2.1 Statistical Jump Models vs. Hidden Markov Models

While Hidden Markov Models (HMMs) have traditionally served as the standard for regime detection, recent scholarship highlights significant limitations in their ability to handle signal instability. Shu et al. (2024) demonstrate that HMMs are highly sensitive to daily market noise, often identifying "short-lived regimes that are unintuitive and difficult to trade". This sensitivity results in "whipsaw" signals—frequent, spurious state flips that degrade performance through excessive transaction costs.

To address the lack of persistence in HMMs, **Statistical Jump Models (JMs)** offer a superior alternative by incorporating a discrete "jump penalty" ($\lambda$) directly into the objective function. Unlike HMMs, which rely solely on transition probabilities, this penalty mathematically enforces regime persistence, requiring substantial evidence of a structural shift before triggering a state change. Empirically, JMs have been shown to reduce annualized portfolio turnover by approximately two-thirds compared to HMMs (44% vs. 141% for the S&P 500) while simultaneously improving risk-adjusted returns and reducing maximum drawdown. Consequently, JMs provide a more robust framework for risk management applications where regime stability is paramount.

##### 2.4.2.2 Explainable and Ensemble Approaches

Zhang et al. (2020) developed an explainable machine learning framework for regime-based asset allocation using hierarchical clustering. Their model integrated macroeconomic indicators with market technical signals to divide economic conditions into four distinct regimes, then applied the Black-Litterman model for portfolio optimization. Backtesting from August 2010 to May 2020 achieved 22.53% annualized returns with a Sharpe ratio of 1.06, significantly outperforming both equal-weighted benchmarks and traditional Black-Litterman implementations. Critically, their approach captured both major market upswings and successfully withdrew capital before market crashes, demonstrating the practical value of regime-aware allocation strategies.

Shu et al. (2024) proposed a statistical jump model (JM) approach that enhances traditional Markov-switching models by imposing jump penalties at each state transition. This penalty mechanism promotes regime persistence, reducing spurious switching signals that plague traditional HMMs. Evaluating the approach across U.S., German, and Japanese equity indices from 1990 to 2023, they found that the JM-guided strategy consistently reduced volatility and maximum drawdown while improving Sharpe ratios relative to both the buy-and-hold and HMM-guided strategies. The JM approach enhanced compound annual growth rates by 1-4% across regions while limiting turnover to approximately 44% annually.

Suárez-Cetrulo et al. (2023) conducted a systematic review of 140 studies on machine learning for financial prediction under regime change. Their analysis identified four primary algorithmic categories showing promise: evolving systems (32.1% of studies), ensemble-based methods, traditional systems adapted to concept change, and neural networks with online learning capabilities. A critical finding was that most conventional machine learning techniques struggle with abrupt structural changes—the exact characteristic that distinguishes regime transitions from normal market fluctuations. They emphasized that the literature on online learning (concept drift) and regime switching has developed largely independently, despite addressing fundamentally similar challenges.

Table 2.4.1: Regime Detection Performance Comparison

Approach Method Annual Return Sharpe Ratio Key Advantage Citation
Hierarchical Clustering Black-Litterman integration 22.53% 1.06 Explainability Zhang et al. (2020)
Statistical Jump Model Jump penalty regime switching +1-4% vs. benchmark Higher vs. HMM Reduced turnover Shu et al. (2024)
Relative Sentiment Sentix + ML ensemble +400-700 bps Improved Cross-regional validity Micaletti (2022)
Mixed-Frequency MF-EEMD-ML — — 19.18% MAE reduction Cai et al. (2024)
Intraday Sentiment Field-specific lexicon 4.55% (strategy) 1.496 Leading indicator Renault (2017)

#### 2.4.3 Sentiment-Based Regime Detection

The application of sentiment analysis to regime detection remains an emerging frontier with substantial untapped potential. Foundational work has established that sentiment signals possess predictive power for market movements:

Bollen et al. (2011) demonstrated that Twitter mood states predicted DJIA movements 2-6 days ahead with 86.7% accuracy (87.6% direction accuracy in validation), establishing sentiment as a potentially leading indicator for market direction. Their analysis identified specific emotional dimensions (calm and anxiety) that correlated with subsequent market movements, suggesting that shifts in investor psychology precede price adjustments.

Renault (2017) constructed a field-specific sentiment lexicon from StockTwits messages and examined intraday relationships between sentiment and returns of the S&P 500 ETF. The study found that first-half-hour sentiment changes predicted last-half-hour returns, with the sentiment effect primarily driven by novice traders. A trading strategy exploiting this pattern achieved a Sharpe ratio of 1.496, with significant price reversals the following trading day—consistent with noise-trading theory. Importantly, predictability disappeared when using standard dictionary-based sentiment methods, underscoring the need for domain-specific lexicons.

Micaletti (2022) introduced the concept of relative sentiment—the difference between institutional and individual investor sentiment expectations—for tactical asset allocation. Using Sentix economic sentiment indices across the U.S., Europe, Japan, and Asia ex-Japan markets, he found that relative sentiment factors demonstrated robust predictive power across all regions, surpassing both standalone sentiment and time-series momentum in informational content. Composite relative sentiment strategies outperformed benchmarks by 400-700 basis points annually with higher Sharpe ratios and lower maximum drawdowns. Notably, when time-series momentum was negative, but relative sentiment was positive, annualized returns averaged 27% versus -23% when both were negative—a 50 percentage-point differential determined by sentiment state.

#### 2.4.4 Real-Time and High-Frequency Systems

The temporal resolution of sentiment-based regime detection presents significant methodological challenges. Traditional daily or weekly sentiment aggregation may miss critical intraday regime shifts, while high-frequency analysis demands sophisticated modeling to handle mixed-frequency data.

Cai et al. (2024) addressed this challenge through an “MF-EEMD-ML” prediction system that integrates half-hourly sentiment from stock message boards with three-minute stock return prediction. Their methodology employed the RR-MIDAS (Reverse Restricted Mixed Data Sampling) framework combined with Ensemble Empirical Mode Decomposition to handle non-stationarity and mixed-frequency dynamics. The system achieved maximum reductions of 19.18% in MAE, 19.08% in RMSE, and 11.71% in SMAPE compared to traditional approaches. Critically, they demonstrated that sentiment impact on high-frequency returns persists across seven intraday periods, with influence gradually weakening over time.

Shao et al. (2024) developed the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM) framework for predicting stock returns. Integrating sentiment from 2.5 million Twitter posts and news sources using VADER, TextBlob, and RoBERTa, their model captured both cross-sectional dependencies across assets and temporal dynamics. The approach achieved 1.02% improvement in 1-day horizon forecasts, 0.42% for 20-day predictions, and 0.36% for 50-day forecasts compared to LSTM, Random Forest, and RNN baselines. An important practical consideration emerged: while RoBERTa-based sentiment extraction provided superior accuracy, computational costs increased from 3-6 seconds (simple methods) to up to 14 hours, highlighting trade-offs between accuracy and real-time deployment feasibility.

The temporal structure of sentiment predictability suggests a natural hierarchy: immediate sentiment shifts (intraday) provide noise trading signals, short-term aggregation (1-5 days) captures directional momentum, and medium-term patterns (weekly-monthly) may indicate regime-level transitions. Our proposed framework targets this medium-term regime detection horizon while preserving the ability to respond to rapid sentiment deterioration during crisis periods.

#### 2.4.5 Explainable AI in Regime Detection

The interpretability of regime detection models is crucial for practical deployment in risk management contexts. Black-box approaches that achieve high accuracy but provide no insight into regime characteristics limit their utility for portfolio managers who must justify allocation decisions.

Zhang et al. (2020) specifically emphasized explainability as a design criterion, noting that their hierarchical clustering approach enables visualization of regime boundaries and numerical analysis of regime-specific asset characteristics. Their four-regime classification (corresponding roughly to reflation, recovery, overheating, and stagflation phases) aligns with established economic cycle theory while being data-driven rather than imposed a priori. The integration with the Black-Litterman model provides a natural mechanism for translating regime identification into actionable portfolio views.

Micaletti (2022) found that across 990 backtests using different machine learning algorithms and factor combinations, the best-performing strategies consistently emerged from the same handful of algorithms—generalized boosted models, random forests, and certain support vector machine configurations. This consistency suggests underlying structural patterns in the sentiment-return relationship that specific algorithm families are particularly suited to capture, providing a form of implicit interpretability through algorithmic selection.

The tension between model complexity and interpretability becomes particularly acute for regime detection. Deep learning approaches may capture subtle pattern interactions but obscure the economic mechanisms driving regime transitions. For our cross-asset sentiment regime detector, we prioritize interpretable indicators (sentiment divergence scores, connectedness metrics, regime probability estimates) that enable human oversight and intervention when model outputs conflict with domain expertise.

#### 2.4.6 Risk Management Integration

The ultimate purpose of regime detection is improved risk management—protecting portfolios during adverse conditions while maintaining participation in favorable environments. Integrating sentiment signals into risk management frameworks requires understanding how sentiment dynamics relate to extreme market events.

Shu et al. (2024) demonstrated that their statistical jump model approach specifically targeted downside risk reduction. The JM-guided strategy achieved volatility reductions of approximately 2-3 percentage points relative to buy-and-hold, with maximum drawdown improvements of 10-15 percentage points across the tested equity indices. The approach exhibited milder drawdowns during major stress periods and provided more robust protection against adverse market movements.

Cao et al. (2025) examined sentiment connectedness and stock price crash risk using network analysis of S&P 500 stocks. They constructed sentiment spillover networks using nonlinear Granger causality and measured firm-level sentiment connectedness through multiple network centrality metrics (degree, closeness, betweenness, eigenvector centrality). Firms with higher sentiment connectedness demonstrated elevated crash risk, as they both spread and receive irrational sentiment signals more intensely. Critically, sentiment connectedness proved a better predictor of crash risk than individual firm sentiment, particularly during market extremes. Stock return synchronicity amplified the sentiment-crash relationship, while accounting conservatism mitigated it.

Nyakurukwa and Seetharam (2025) extended sentiment network analysis by using TVP-VAR frequency-connectedness across DJIA constituents. Their analysis decomposed sentiment connectedness into short-term (1-5 days), medium-term (5-20 days), and long-term (20+ days) components. Key findings included that sentiment shocks transmit predominantly in the short-term, negative news sentiment exhibits higher connectedness than positive sentiment (consistent with negativity bias in media coverage), and sentiment connectedness peaks during globally significant events such as COVID-19. These temporal dynamics suggest that monitoring short-term changes in sentiment connectedness may provide an early warning of regime stress.

In our framework, these findings motivate the inclusion of sentiment network metrics as indicators of regime transitions. Rapid increases in cross-asset sentiment connectedness may signal approaching regime instability, while divergence patterns (certain assets disconnecting from the sentiment network) may indicate rotation opportunities or pending contagion.

#### 2.4.7 Adaptive and Online Learning Approaches

Financial markets exhibit non-stationarity—the statistical relationships between features and returns evolve over time, rendering static models obsolete. This phenomenon, known as concept drift in the machine learning literature, poses fundamental challenges for regime-detection systems that must maintain accuracy across multiple market cycles.

Suárez-Cetrulo et al. (2023) emphasized that bridging the gap between data stream learning and financial regime research remains at an early stage. Their review identified several promising approaches for handling non-stationarity:

    • **Evolving systems:** Models that continuously update parameters as new data arrives, maintaining responsiveness to changing market dynamics without requiring complete retraining.
    • **Ensemble methods:** Combining multiple learners with different training windows or architectural biases to provide robustness against any single approach becoming obsolete.
    • **Meta-learning:** Using unsupervised algorithms to detect concept recurrence and retrieve previously effective models, or to detect drift events triggering model updates.
    • **Online incremental algorithms:** Sequential learning approaches that process data point-by-point, avoiding the computational burden of batch retraining.

Shao et al. (2024) implemented time-varying coefficients within their HD-SURDLM framework, allowing sentiment-return relationships to evolve dynamically. Their use of improved Gibbs sampling with enhanced numerical stability enabled efficient sequential updating without model degradation over time. The approach demonstrated consistent outperformance across 7-year evaluation windows encompassing multiple market conditions.

For our sentiment-based regime detector, adaptive capability is essential, as the relationship between sentiment and market regimes may itself be regime-dependent. During periods of high attention and liquidity (bull markets), sentiment may strongly predict subsequent movements; during crisis periods with forced selling and liquidity constraints, sentiment-price relationships may temporarily decouple. Our design incorporates rolling window estimation and regime-specific model weighting to accommodate such structural variation.

**Research Gap Synthesis:** Despite significant progress in both sentiment analysis and regime detection, no existing research has systematically integrated multi-source, cross-asset sentiment as a leading indicator for regime transitions. The reviewed literature establishes that: (1) sentiment signals lead price movements by measurable intervals; (2) machine learning can identify meaningful market regimes from complex signal combinations; (3) sentiment connectedness metrics correlate with crash risk and extreme market events; and (4) adaptive methods are necessary for sustained predictive accuracy. Our research fills this gap by constructing a unified sentiment aggregation framework across four asset classes (equities, cryptocurrency, forex, commodities), with the explicit goal of identifying systematic Risk-On/Risk-Off regime transitions before they manifest in traditional price-based indicators.

### 2.5 Research Gaps and Hypotheses

The preceding literature review reveals several critical gaps that motivate our research design. First, while sentiment analysis has achieved strong performance for individual asset classes, no framework systematically aggregates sentiment across equities, cryptocurrency, forex, and commodities to detect portfolio-level regime transitions. Second, despite evidence that sentiment signals lead price movements by 1-6 days, this lead time has not been exploited for regime-level early warning systems. Third, network-based approaches have demonstrated the importance of sentiment connectedness, but cross-asset sentiment networks remain unexplored. Fourth, the practical integration of multi-source sentiment (social media, news, and financial reports) with regime detection algorithms has not been attempted.

#### 2.5.1 The Synthesis Gap

Despite significant progress in both financial NLP and econometric modeling, a critical methodological gap remains at the intersection of generative sentiment analysis and regime detection. While **Konstantinidis et al. (2024)** successfully established **FinLlama** as a superior sentiment classifier for algorithmic trading—demonstrating a 44.7% return improvement over FinBERT—their application was limited to standard portfolio construction rules, neglecting the identification of structural market regimes. Conversely, **Shu et al. (2024)** validated **Statistical Jump Models (JMs)** as a robust alternative to Hidden Markov Models, proving that jump penalties significantly reduce "whipsaw" signals and downside risk. However, their implementation relied exclusively on endogenous price features (returns and volatility), ignoring the predictive power of exogenous sentiment signals.

Furthermore, while recent studies like **Yang et al. (2025)** have applied LLMs to cross-asset monitoring, and **Shi (2025)** has applied GARCH-MIDAS to sentiment, no existing research has integrated the semantic depth of **FinLlama** directly into the persistence-enforcing framework of **Statistical Jump Models** for a **cross-asset** universe. This research fills this specific gap by constructing the first **Two-Layer Sentiment Regime Detector**, identifying leading indicators of structural breaks by synthesizing generative AI sentiment with econometric jump penalties across Equities, Crypto, Forex, and Commodities.

#### 2.5.2 Research Hypotheses

Based on the literature review, we hypothesize:

**H1 (Leading Indicator Hypothesis):** Cross-asset sentiment aggregation serves as a leading indicator of market regime shifts, preceding VIX-based regime detection by 1-5 trading days. This hypothesis is grounded in findings from Bollen et al. (2011), showing a 2-6 day predictive lead time with 86.7% accuracy; Caferra (2022), demonstrating sentiment-mediated cross-market connections; and Trushkovskyi (2025), confirming Granger causality between sentiment and returns.

**H2 (Divergence Signal Hypothesis):** Sentiment divergence across asset classes (e.g., equities bullish while crypto bearish) signals an impending transition between Risk-On and Risk-Off regimes. Caferra (2022) found that sentiment connectedness successfully identifies market linkages, suggesting that disconnection or divergence may indicate regime instability. Wang et al. (2024) demonstrated asymmetric cross-asset momentum transmission supporting this mechanism.

**H3 (Network Effect Hypothesis):** Sentiment connectedness intensity (measured via network centrality metrics similar to those of Cao et al., 2025) will correlate with regime transition probability, with high connectedness during stable regimes and rapid disconnection preceding transitions. Sibande et al. (2021) found regime-specific sentiment effects in currency markets, supporting state-dependent sentiment dynamics.

**H4 (Ensemble Superiority Hypothesis):** Ensemble transformer models (FinBERT + RoBERTa) will outperform single-model approaches for sentiment classification across heterogeneous data sources, based on Mishev et al. (2020) findings that different models excel on different source types and Roumeliotis et al. (2024) demonstrating that domain-specific models achieve near-parity with LLMs at lower cost.

## 3. Methods

### 3.1 Data Quality and Preprocessing Considerations

Financial text data from social media and news sources presents unique preprocessing challenges that impact sentiment analysis accuracy. Unlike formal financial documents, social media content often contains noise, sarcasm, slang, and bot-generated content, which can distort sentiment signals. Kraaijeveld and De Smedt (2020) documented that 1-14% of cryptocurrency-related tweets originate from bot accounts, highlighting data quality concerns specific to social media sentiment analysis.

**Entity Recognition and Asset Classification:** Accurately linking sentiment to specific asset classes requires robust entity recognition. Financial NER differs from general NER due to domain-specific entities (ticker symbols, ISIN codes, currency pairs), ambiguity (e.g., AAPL refers to Apple stock, not the fruit), and context-dependency, where the same entity may carry different sentiment implications across asset classes.

**Multi-Source Data Integration:** Integrating sentiment from heterogeneous sources (Reddit, Twitter, financial news) requires careful consideration of source reliability, temporal resolution, and weighting schemes. Mishev et al. (2020) noted that sentiment model performance varies significantly across data sources, with models trained on news performing differently from those trained on social media. This suggests the need for source-specific model ensembles or adaptive weighting mechanisms.

**Temporal Aggregation:** Sentiment must be aggregated over appropriate time windows to construct meaningful indices. Daily or weekly aggregation smooths noise while preserving signal, but the optimal window size may vary by asset class based on trading volume and information velocity. High-frequency crypto markets may require shorter windows than traditional equity markets.

### 3.2 Data Collection

**Data Sources:** We collect historical text data (2016-present) from three primary sources:

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

     - Price Data: Historical OHLCV for major indices (SPY, QQQ), crypto (BTC, ETH), forex (EUR/USD), commodities (GLD, USO) via yfinance or Alpha Vantage
     - VIX Data: Volatility index for validation/labeling

### 3.3 Text Preprocessing Pipeline

**Text Cleaning:**

     1. Tokenization (spaCy or NLTK)
     2. Lowercasing
     3. URL/mention removal
     4. Emoji handling (preserve sentiment-rich emojis: 🚀📈 = bullish, 📉💩 = bearish)
     5. Stop word removal (finance-aware: retain “bull”, “bear”, “crash”)
     6. Lemmatization

**Asset Class Labeling:** Classify each text sample by asset class (Equities, Crypto, Forex, Commodities) using:

- **Keyword matching:** Ticker symbols, currency pairs, commodity names
- **NER models:** spaCy financial NER or custom-trained NER
- **Multi-label classification:** Some texts reference multiple asset classes

### 3.4 Data Preprocessing Pipeline

Financial news arrives irregularly (stochastic), while price data arrives at fixed intervals (deterministic). To feed the GARCH-MIDAS and Jump Models, we must map irregular sentiment events $E = \{e_1, e_2, \dots, e_n\}$ to fixed price bars $P = \{p_1, p_2, \dots, p_t\}$. We adopt the **Forward-Fill with Aggregation** algorithm proposed by Dakalbab et al. (2025) and the **Next-Day Attribution** logic from Kengmegni (2024).

#### 3.4.1 Time-Alignment Algorithm

**1. Timestamp Standardization & Cutoff:**
First, all timestamps are converted to UTC/EST to align with the target exchange. Following Kengmegni (2024), we enforce a **4:30 PM EST Cutoff**. News arriving after this threshold is attributed to the *subsequent* trading day ($t+1$) to reflect that its market impact cannot occur until the next open, preventing look-ahead bias in the backtest.

**2. Alignment Logic (Dakalbab's Cases):**
For every price bar $p_t$ covering the interval $[t-1, t]$, we align sentiment scores $S$ based on three scenarios:

- **Case 1 (Perfect Match):** If news events occur strictly within $[t-1, t]$, they are mapped directly to $p_t$.
- **Case 2 (Sparse Data/Fill-Forward):** If no news occurs in $[t-1, t]$, the sentiment score from the last available news event ($S_{last}$) is carried forward. This persists the regime signal until new information arrives, ensuring the Jump Model receives a continuous feature vector.
- **Case 3 (High Velocity/Aggregation):** If multiple articles ($k > 1$) appear within a single interval $[t-1, t]$ (common in crypto/forex), we calculate the **Aggregated Interval Sentiment ($AIS_t$)**:

$$AIS_t = \sum_{i=1}^{k} \text{Sentiment}(e_i)$$

If $AIS_t > 0$, the interval is labeled Positive; if $< 0$, Negative. This prevents a single minor tweet from flipping the regime if the aggregate news volume is contrary.

#### 3.4.2 Entity Filtering and Disambiguation

To ensure the sentiment extracted actually pertains to the target asset (e.g., distinguishing "Apple" the company from the fruit, or "ETH" the coin from "ETH" Zurich), we employ a **Dictionary-Based Filtering** approach rather than generic Named Entity Recognition (NER), which Kengmegni (2024) found to be less prone to false positives.

**1. Ticker & Cashtag Filtering:**
For Social Media (Twitter/Reddit), we filter for "Cashtags" (e.g., \$BTC, \$SPY) and strict keyword associations defined in a curated dictionary (e.g., "Rivian" maps to "RIVN").

**2. Contextual Disambiguation (Forex/Crypto):**
For currency pairs, we address the "Subject-Object" ambiguity highlighted by Fatouros et al. (2023). A headline reading *"USD soars against JPY"* is Positive for USD but Negative for the pair JPY/USD.

- **Logic:** If the calculated sentiment $S > 0$ and the Subject is the *Quote Currency*, flip the sign of $S$.

**3. Bot and Spam Removal:**
Following Trushkovskyi (2025), we apply a pre-filtering layer to remove duplicate messages and posts from known bot clusters (e.g., identical timestamps and text), as these inflate volume metrics without reflecting genuine market psychology.

### 3.5 Sentiment Classification

**Model Architecture**: We employ an ensemble of two transformer models, following evidence from Mishev et al. (2020) that different architectures excel on different source types, and Ergun and Sefer (2025) demonstrating that finance-pretrained RoBERTa achieves state-of-the-art results even with limited labeled data:

 1. **FinBERT**: Finance-specific BERT variant (Araci, 2019)
     - Pretrained on financial news + analyst reports
     - Fine-tuned on the Financial PhraseBank dataset
 2. **RoBERTa-base**: General-purpose robustly optimized BERT
     - Broader linguistic understanding
     - Fine-tuned on the Twitter Financial News Sentiment dataset

**Ensemble Strategy**:

- **Voting**: Average logits from both models
- **Weighted**: If one model shows higher validation accuracy on specific sources (e.g., FinBERT better on news, RoBERTa better on social media), apply source-dependent weights

**Training Infrastructure**:

- MANEFRAME HPC (SMU’s cluster)
- GPUs: NVIDIA V100 or A100
- Framework: PyTorch + HuggingFace Transformers

**Output**: Sentiment score per text sample: {Positive: [0-1], Neutral: [0-1], Negative: [0-1]}

### 3.6 Sentiment Index Construction and Feature Engineering

#### 3.6.1 Basic Aggregation Strategy

For each asset class $c$ (Equities, Crypto, Forex, Commodities) and time window $t$ (daily or weekly):

$$\text{SentimentIndex}_{c,t} = \frac{\sum_{i \in D_{c,t}} (P_i - N_i) \cdot w_i}{\sum_{i \in D_{c,t}} w_i}$$

To keep notation consistent with the implemented pipeline features, let \(s_{c,t}\) denote the daily sentiment level by asset class. The aggregate sentiment and divergence operators are:

$$
\bar{s}_t = \frac{1}{C}\sum_{c=1}^{C}s_{c,t}, \qquad D_t = \max_c s_{c,t} - \min_c s_{c,t}
$$

and temporal dynamics are represented as:

$$
\Delta \bar{s}_t = \bar{s}_t - \bar{s}_{t-1}, \qquad \Delta^2 \bar{s}_t = \Delta \bar{s}_t - \Delta \bar{s}_{t-1}
$$

Where:

- $D_{c,t}$ = all documents for asset class $c$ in time window $t$
- $P_i$ = positive sentiment score for document $i$
- $N_i$ = negative sentiment score for document $i$
- $w_i$ = weight (e.g., engagement score, source credibility)

**Weighting Schemes:**

- **Equal weight**: All texts contribute equally
- **Engagement-weighted**: Reddit/Twitter posts weighted by upvotes/retweets
- **Source-weighted**: News articles are weighted higher than anonymous social media
- **Temporal decay**: Following Cai et al. (2024), more recent sentiment observations receive higher weights to capture evolving market psychology while preserving historical context

**Basic Feature Engineering:**

- **Sentiment momentum**: $\Delta \text{SI}_{c,t} = \text{SI}_{c,t} - \text{SI}_{c,t-1}$
- **Cross-asset divergence**: $\text{Divergence}_t = \max(\text{SI}_{c,t}) - \min(\text{SI}_{c,t})$
- **Volatility**: Rolling standard deviation of sentiment index

#### 3.6.2 Sentiment Connectedness (Entropy-Based)

To test the **Network Effect Hypothesis (H3)**, we quantify the influence of each asset class within the global sentiment network. Following the methodology of Cao et al. (2025), we construct a composite connectedness index that aggregates four distinct network centrality measures using an entropy-weighting scheme to eliminate bias from any single metric.

**1. Network Centrality Inputs:**
We first construct a sentiment spillover network where nodes $N$ represent our asset classes (or individual constituents) and edges represent significant nonlinear Granger causality between their sentiment time series. For each node $i$, we calculate four centrality measures ($C_{ij}$):

1. **Degree Centrality ($C_{i1}$):** Measures direct sentiment spillover volume. $DC_i = k_i / (n-1)$, where $k_i$ is the number of significant sentiment links.
2. **Closeness Centrality ($C_{i2}$):** Measures the speed of sentiment transmission. $CC_i = (n-1) / \sum_{j \neq i} d_{ij}$, where $d_{ij}$ is the shortest path distance.
3. **Betweenness Centrality ($C_{i3}$):** Measures the node's role as a sentiment "bridge" or mediator. $BC_i = \sum_{j \neq k} \sigma_{jk}(i) / \sigma_{jk}$.
4. **Eigenvector Centrality ($C_{i4}$):** Measures influence based on the importance of connected neighbors.

**2. Entropy Weight Calculation:**
To create a unified "Connectedness" feature for the Regime Detector, we use the Entropy Weight Method to assign dynamic weights to these four centralities based on their information entropy.

First, we normalize the centrality matrix for all nodes $i=1 \dots n$ and metrics $j=1 \dots 4$:

$$p_{ij} = \frac{C_{ij}}{\sum_{i=1}^{n} C_{ij}}$$

Next, we calculate the **Entropy ($E_j$)** for each centrality metric $j$ to measure its dispersion (information value):

$$E_j = - \frac{1}{\ln n} \sum_{i=1}^{n} p_{ij} \ln p_{ij}$$

We then derive the **Weight ($\omega_j$)** for each centrality metric. A lower entropy indicates higher variation and thus higher information value, receiving a higher weight:

$$\omega_j = \frac{1 - E_j}{\sum_{k=1}^{4} (1 - E_k)}$$

**3. Final Feature Construction (AssetSentix):**
The final input feature for the Regime Detection Model, **Sentiment Connectedness ($SC_t$)**, is the weighted sum of the centrality measures:

$$SC_{i,t} = \sum_{j=1}^{4} \omega_j C_{ij,t}$$

A high $SC_{i,t}$ indicates that asset $i$ is highly interconnected, acting as a key transmitter or receiver of irrational sentiment shocks, which Cao et al. (2025) found to be a strong predictor of crash risk.

#### 3.6.3 Sentiment Divergence & Decoupling (Rényi Transfer Entropy)

To operationalize the **Divergence Signal Hypothesis (H2)**, we move beyond linear correlation to measure the directional information flow between asset classes (e.g., Equities $\rightarrow$ Crypto). We employ **Rényi Transfer Entropy (RTE)** as utilized by Caferra (2022) because it captures non-linear dependencies and emphasizes tail events (extreme sentiment) via a weighting parameter $q$, which traditional Granger Causality misses.

**1. The Probability Space:**
Let $X_t$ and $Y_t$ represent the sentiment time series of two asset classes (e.g., $X=$ Equity Sentiment, $Y=$ Crypto Sentiment). We treat these as Markov processes. To capture the flow of information from $X$ to $Y$, we compare the probability of observing a future state of $Y$ ($y_{t+1}$) conditioned on its own history versus conditioned on both its own history *and* the history of $X$.

**2. Rényi Transfer Entropy (RTE):**
Following Caferra (2022), we calculate the RTE to quantify the reduction in uncertainty about $Y_{t+1}$ given knowledge of $X_t$. We introduce the weighting parameter $q$ to sensitize the metric to "risk-off" tail events (where $q < 1$ emphasizes rare events and $q > 1$ emphasizes frequent events).

The RTE from $X$ to $Y$, denoted as $RTE_{X \rightarrow Y}(q)$, is defined as:

$$RTE_{X \rightarrow Y}(q) = \frac{1}{1-q} \log \frac{\sum_y \phi_q(y_t) p_q(y_{t+1}|y_t)}{\sum_{x,y} \phi_q(x_t, y_t) p_q(y_{t+1}|y_t, x_t)}$$

Where:

- $p(\cdot)$ represents the standard transition probabilities.
- $\phi_q(\cdot)$ is the **escort distribution**, defined as $\phi_q(x) = \frac{p(x)^q}{\sum_x p(x)^q}$. This normalizes the probabilities to highlight specific parts of the distribution (e.g., extreme negative sentiment spikes).
- $q$: The sensitivity parameter. We calculate this feature with $q=0.5$ (emphasizing rare, extreme sentiment shocks) and $q=1$ (standard Shannon entropy) to detect regime-specific decoupling.

**3. The Decoupling Indicator (Feature Construction):**
Shi (2025) identifies "decoupling" as a structural break where traditional asset correlations (e.g., Gold vs. Dollar) invert or disappear due to behavioral anomalies. To capture this, we define the **Sentiment Decoupling Indicator ($SDI_t$)**.

First, we calculate the **Net Information Flow ($NIF_t$)** over a rolling window $w$ (e.g., 30 days):

$$NIF_{X,Y,t} = RTE_{X \rightarrow Y, t}(q) - RTE_{Y \rightarrow X, t}(q)$$

Then, we define **Decoupling ($SDI_t$)** as the state where the bi-directional information flow collapses below a significance threshold $\epsilon$, or when the NIF acts counter to the historical price correlation $\rho_{price}$:

$$SDI_t = \begin{cases} 1 & \text{if } (RTE_{X \rightarrow Y} + RTE_{Y \rightarrow X}) < \epsilon \quad (\text{Total Disconnection}) \\ 1 & \text{if } \text{sign}(NIF_t) \neq \text{sign}(\text{SentimentDiff}_t) \quad (\text{Anomalous Flow}) \\ 0 & \text{otherwise} \end{cases}$$

**Interpretation:**

- **High $RTE$:** Indicates strong contagion (Risk-Off regime spreading).
- **High $SDI$ (Decoupling):** Indicates that Asset $X$ and Asset $Y$ have structurally detached. For example, if Equity Sentiment is tanking but Crypto Sentiment is rising, *and* $SDI=1$ (no information flow between them), this signals a distinct "Safe Haven" regime or a speculative bubble, supporting H2.

**Variable Definitions Table:**

| Variable | Definition | Source |
| :--- | :--- | :--- |
| $RTE_{X \rightarrow Y}(q)$ | Rényi Transfer Entropy: Information flow from asset $X$ to $Y$ | Caferra (2022) |
| $q$ | Weighting parameter: $q<1$ emphasizes tail events (crises) | Caferra (2022) |
| $\phi_q(\cdot)$ | Escort distribution normalizing probabilities by $q$ | Caferra (2022) |
| $SDI_t$ | Sentiment Decoupling Indicator (Binary regime feature) | Adapted from Shi (2025) |
| $NIF_t$ | Net Information Flow (Directionality of sentiment) | Caferra (2022) |

### 3.7 Two-Layer Regime Detection Model

This research employs a sequential two-layer approach. Layer 1 isolates the long-term volatility component driven by sentiment using a GARCH-MIDAS framework. Layer 2 uses these volatility estimates alongside sentiment momentum features to classify discrete market regimes via a Statistical Jump Model that penalizes frequent state switching to ensure regime persistence.

#### 3.7.1 Layer 1: Sentiment-Adjusted Volatility (GARCH-MIDAS)

To address the mixed-frequency nature of daily price data and the irregularity of sentiment signals, we use the GARCH-MIDAS-Sentiment model proposed by Shi (2025) and Cai et al. (2024).

We decompose the conditional variance of asset returns, $\sigma_{t}^2$, into a short-term transitory component $g_t$ and a long-term secular component $\tau_t$:

$$r_t = \mu + \sqrt{\tau_t g_t} \varepsilon_t, \quad \varepsilon_t \sim N(0,1)$$

**1. Short-Term Component ($g_t$):**
The short-term variance follows a standard GARCH(1,1) process, capturing daily clustering properties:

$$g_t = (1 - \alpha - \beta) + \alpha \frac{(r_{t-1} - \mu)^2}{\tau_t} + \beta g_{t-1}$$

Where:

- $\alpha, \beta$: ARCH and GARCH coefficients ($\alpha > 0, \beta \ge 0, \alpha + \beta < 1$).
- $\tau_t$: The long-term variance component, updated at a lower frequency (e.g., weekly or based on sentiment aggregation windows).

**2. Long-Term Component ($\tau_t$):**
The long-term component is smoothed using MIDAS (Mixed Data Sampling) regression on the exogenous Sentiment Index ($S_{t}$):

$$\log(\tau_t) = m + \theta \sum_{k=1}^{K} \phi_k(\omega_1, \omega_2) S_{t-k}$$

Where:

- $m$: Long-run constant variance.
- $\theta$: Sensitivity of volatility to sentiment shocks. Shi (2025) found negative sentiment often exhibits an asymmetric impact ($1.8\times$ stronger than positive).
- $\phi_k(\cdot)$: The Beta weighting polynomial that assigns weights to lagged sentiment scores ($S_{t-k}$), ensuring recent sentiment is weighted more heavily while retaining long-term memory.

#### 3.7.2 Layer 2: Regime Classification (Statistical Jump Model)

To define discrete market states (e.g., Risk-On, Risk-Off), we input the feature vector $x_t$—comprising the GARCH-MIDAS volatility estimate ($\tau_t$) and Cross-Asset Sentiment Divergence—into a Statistical Jump Model (JM) as defined by Shu et al. (2024).

Unlike Hidden Markov Models (HMMs), which rely solely on transition probabilities, the JM explicitly penalizes state turnover in the objective function to reduce "whipsaw" signals:

$$\min_{\Theta, \mathbf{s}} \sum_{t=0}^{T-1} \ell(x_t, \theta_{s_t}) + \lambda \sum_{t=1}^{T-1} \mathbb{I}(s_t \neq s_{t-1})$$

Where:

- $\mathbf{s} = \{s_0, \dots, s_{T-1}\}$: The sequence of discrete regimes (e.g., $s_t \in \{0, 1\}$ for Bull/Bear).
- $\Theta = \{\theta_0, \dots, \theta_{K-1}\}$: The centroid parameters (mean vector and covariance) for each regime state $k$.
- $\ell(\cdot)$: The loss function, defined as the scaled squared Euclidean distance: $\ell(x, \theta) = \frac{1}{2} \|x - \theta\|^2$.
- $\mathbb{I}(\cdot)$: An indicator function equal to 1 if a regime switch occurs ($s_t \neq s_{t-1}$), and 0 otherwise.
- $\lambda$: The **Jump Penalty** hyperparameter. A higher $\lambda$ enforces greater regime persistence. This parameter is tuned via time-series cross-validation to maximize the Sharpe ratio of the resulting strategy.

**Variable Definitions Table:**

| Variable | Definition | Source |
| :--- | :--- | :--- |
| $\tau_t$ | Long-term secular volatility component driven by sentiment | Shi (2025) |
| $g_t$ | Short-term transitory volatility component (GARCH) | Shi (2025) |
| $S_{t-k}$ | Lagged Sentiment Index constructed via FinBERT/RoBERTa | Cai et al. (2024) |
| $\theta$ | Coefficient measuring sentiment's marginal impact on variance | Shi (2025) |
| $\lambda$ | Jump penalty parameter controlling regime persistence | Shu et al. (2024) |
| $s_t$ | Discrete regime state at time $t$ (Output) | Shu et al. (2024) |

#### 3.7.3 Regime Definitions

Based on VIX and price action, historical periods labeled as:

 1. **Risk-On**: VIX < 20, equities rising, crypto/commodities rallying
 2. **Risk-Off**: VIX > 30, equities falling, flight to safety (bonds, gold, USD)
 3. **Transition**: VIX 20-30, mixed signals, choppy price action

**Labeling Strategy:**

- Manual labeling of major historical regimes (COVID crash, 2021 bull run, 2022 bear market)
- Algorithmic labeling using VIX thresholds + price trends
- ~1000-2000 labeled days (2016-present)

**Model Comparison:** We compare:

 1. **Random Forest**: Ensemble tree-based classifier
 2. **XGBoost**: Gradient boosting (handles non-linear relationships well)
 3. **LSTM**: Recurrent neural network (captures temporal dependencies in sentiment time series)
 4. **Statistical Jump Model**: Following Shu et al. (2024), a Markov-switching approach with jump penalties that promotes regime persistence and reduces spurious switching signals

**Features (per time window)**:

- Sentiment indices for all 4 asset classes (4 features)
- Sentiment momentum (4 features)
- Cross-asset divergence (1 feature)
- Historical VIX (1 feature)
- Rolling correlations between sentiment indices (6 features)
- Sentiment connectedness metrics: Following Cao et al. (2025), network centrality measures (degree, betweenness) capturing cross-asset sentiment propagation intensity (4 features)
- **Total**: ~20 features

**Training/Validation Split**:

- Training: 2016-2021 (5 years)
- Validation: 2022-2023 (2 years)
- Test: 2024-present (out-of-sample)

### 3.8 Evaluation Strategy: Regime Detection & Lead-Time Analysis

To rigorously assess the model's ability to anticipate structural breaks rather than merely describe them, we employ a tripartite evaluation framework focusing on directional correctness, class-imbalanced performance, and temporal precedence.

#### 3.8.1 Directional Accuracy (DA)

Following the protocol of Dakalbab et al. (2025), we utilize Directional Accuracy (DA) to evaluate the model's capacity to predict the *transition* between regimes, rather than the static state. This is critical for avoiding "inertial" high-accuracy scores where a model simply predicts that the current state will continue.

$$DA = \frac{1}{N} \sum_{t=1}^{N} \mathbb{I}[\text{sign}(R_{actual, t} - R_{actual, t-1}) = \text{sign}(R_{pred, t} - R_{pred, t-1})]$$

Where:

- $\mathbb{I}$ is the indicator function.
- $R$ represents the regime state (e.g., discrete states mapped to ordinal risk levels).
- High DA confirms the model correctly identifies the *moment* of regime change.

#### 3.8.2 Matthews Correlation Coefficient (MCC)

Financial regimes are inherently imbalanced; "Risk-Off" or "Crash" regimes occur far less frequently than "Normal" regimes. Standard accuracy or F1-scores can be biased by the majority class. Therefore, we adopt the Matthews Correlation Coefficient (MCC) as the primary classification metric, as recommended by Dakalbab et al. (2025) for financial forecasting. The MCC produces a value between -1 and +1, where +1 represents a perfect prediction, 0 represents no better than random, and -1 represents total disagreement.

$$MCC = \frac{TP \times TN - FP \times FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}$$

This metric ensures that a model achieving 95% accuracy by simply predicting "Bull Market" every day (during a long bull run) is penalized for missing the few critical "Bear" transition days.

#### 3.8.3 Lead-Time Analysis (LTA)

To test the **Leading Indicator Hypothesis (H1)**, we define a custom **Lead-Time metric ($\Delta_{lead}$)**. This quantifies the temporal gap between the Sentiment-based Regime signal ($S_t$) and the Volatility-based VIX confirmation ($V_t$).

We define the onset of a regime $k$ as $t_{start}(k)$. The Lead-Time is calculated for all major regime transitions identified in the test set:

$$\Delta_{lead} = t_{start}(VIX_{threshold}) - t_{start}(Model_{pred})$$

The lead-lag cross-correlation diagnostic used for H1 is:

$$
\rho_{SV}(k) = \mathrm{Corr}(S_{t-k}, V_t), \qquad \hat{k}=\arg\max_{k \in \{0,\dots,5\}} |\rho_{SV}(k)|
$$

- **$\Delta_{lead} > 0$:** The model provides an early warning (Positive Lead Time).
- **$\Delta_{lead} \le 0$:** The model is coincident or lagging.
- **Target:** Based on Bollen et al. (2011) and Trushkovskyi (2025), we aim for a mean $\Delta_{lead} \in [1, 5]$ trading days.

#### 3.8.4 Additional Metrics

- Accuracy, Precision, Recall, F1-score per regime class
- Confusion matrix analysis
- Sharpe ratio of regime-based trading strategy

For H2 and H3 hypothesis testing, the corresponding inferential statistics are:

$$
t = \frac{\bar{D}_{\mathrm{pre}}-\bar{D}_{\mathrm{stable}}}
{\sqrt{\frac{s^2_{\mathrm{pre}}}{n_{\mathrm{pre}}}+\frac{s^2_{\mathrm{stable}}}{n_{\mathrm{stable}}}}}, \qquad
F=\frac{MS_{\mathrm{between}}}{MS_{\mathrm{within}}}
$$

### 3.9 Dashboard Development

**Backend**:

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (time-series data)
- **APIs**:
  - /sentiment/{asset_class}: Returns sentiment index time series
  - /regime/current: Returns current regime prediction + confidence
  - /alerts/divergence: Returns cross-asset divergence alerts
**Frontend**:

- **Framework**: React (Vite build tool)
- **Visualization**: Recharts or D3.js for interactive time-series charts
- **Components**:
  - Real-time sentiment gauge (per asset class)
  - Historical sentiment trends (line charts)
  - Regime indicator (Risk-On/Off/Transition)
  - Divergence alerts (when sentiment contradicts price or cross-asset sentiment diverges)

**Deployment**:

- **Backend**: Cloud hosting (AWS EC2, Google Cloud Run, or Heroku)
- **Frontend**: Vercel or Netlify
- **CI/CD**: GitHub Actions

## 4. Implementation Plan

### 4.1 Software & Technology Stack

We will adopt a microservices-oriented architecture to decouple heavy NLP inference from the lightweight regime-detection logic.

#### 4.1.1 Data & NLP Layer

- **Language Models:** `Hugging Face Transformers` for FinBERT and RoBERTa-base.
- **LLM Integration:** `OpenAI API` (GPT-4o) for zero-shot validation and complex entity disambiguation, as recommended by Nasiopoulos et al. (2025) for scalability without heavy local compute.
- **Orchestration:** `Airflow` or `Celery` to manage the asynchronous scraping of Reddit/Twitter APIs and news feeds.

#### 4.1.2 Modeling & Inference Layer

- **Deep Learning Framework:** `PyTorch` for custom model training and the Statistical Jump Model implementation.
- **Econometrics:** `statsmodels` or `arch` (Python) for the GARCH-MIDAS volatility components.
- **Optimization:** `Optuna` for Bayesian hyperparameter tuning of the Jump Penalty ($\lambda$) and lookback windows, utilizing 100 trials as per Nasiopoulos et al. (2025).

#### 4.1.3 Backend & Deployment

- **API:** `FastAPI` for high-performance, non-blocking inference endpoints (e.g., `/predict_regime`).
- **Database:** `PostgreSQL` (TimescaleDB extension) for efficient storage of high-frequency time-series sentiment data.
- **APIs**:
  - /sentiment/{asset_class}: Returns sentiment index time series
  - /regime/current: Returns current regime prediction + confidence
  - /alerts/divergence: Returns cross-asset divergence alerts

#### 4.1.4 Frontend

- **Framework:** React (Vite build tool)
- **Visualization:** Recharts or D3.js for interactive time-series charts
- **Components:**
  - Real-time sentiment gauge (per asset class)
  - Historical sentiment trends (line charts)
  - Regime indicator (Risk-On/Off/Transition)
  - Divergence alerts (when sentiment contradicts price or cross-asset sentiment diverges)

#### 4.1.5 Deployment & CI/CD

- **Backend:** Cloud hosting (AWS EC2, Google Cloud Run, or Heroku)
- **Frontend:** Vercel or Netlify
- **CI/CD:** GitHub Actions

### 4.2 Backtesting Engine Architecture

To validate the "Leading Indicator" hypothesis (H1) and avoid look-ahead bias—a critical failure point identified by Kengmegni (2024)—we will construct a **Walk-Forward Validation Engine** rather than a standard cross-validation loop.

#### 4.2.1 The "Rolling-Window" Architecture

Following the protocols of Shao et al. (2024) and Kengmegni (2024), the engine simulates real-time trading by advancing the training window.

1. **Initialization:** Train Sentiment & Regime models on data $t_{0} \to t_{k}$ (e.g., 2 years).
2. **Prediction Step ($t_{k+1}$):**
    - **Data Cutoff:** Strictly enforce a 4:30 PM EST cutoff for news data to prevent information leakage into the next trading day.
    - **Inference:** Generate $S_{t+1}$ (Sentiment Score) $\to$ $\tau_{t+1}$ (GARCH Volatility) $\to$ Regime State (Risk-On/Off).
3. **Execution Simulation:**
    - If Regime switches (e.g., Risk-On $\to$ Risk-Off), trigger portfolio rebalancing.
    - Apply **Transaction Costs:** 10 basis points (bps) per trade to simulate institutional slippage.
4. **Update Step:** Add $t_{k+1}$ to the training set. Retrain or incrementally update model parameters (e.g., monthly retraining) to adapt to concept drift.

#### 4.2.2 Event-Driven Logic

The backtester will use an event-driven loop to handle the mixed frequencies of our data (irregular news vs. regular prices):

- **Input:** `Stream<NewsEvent>`, `Stream<PriceTick>`
- **Alignment Processor:** Implements the "Forward-Fill with Aggregation" logic (from Methodology 3.4) to align sentiment signals to the nearest tradable price bar.

### 4.3 Implementation Roadmap

- **Phase 1: Pipeline Construction (Weeks 1-2):** Set up scrapers (Twitter/News) and the FinBERT/RoBERTa inference pipeline.
- **Phase 2: Feature Engineering (Week 3):** Implement the Entropy-based Connectedness and Transfer Entropy Divergence metrics.
- **Phase 3: Model Integration (Weeks 4-5):** Build the Two-Layer GARCH-MIDAS + Jump Model in PyTorch.
- **Phase 4: Backtesting & Tuning (Weeks 6-7):** Run the Walk-Forward validation, tuning the Jump Penalty ($\lambda$) to maximize the Sharpe Ratio.

## 5. Expected Results

### 5.1 Sentiment Model Performance Targets

Based on benchmark performance from FinBERT (Araci, 2019) and ensemble approaches:

- Classification Accuracy: 85-90% on financial text sentiment (positive/neutral/negative)
- F1-Score: >0.80 across all sentiment classes
- Source-Specific Performance: Higher accuracy on news (>90%) vs. social media (>80%)

### 5.2 Regime Classification Performance Targets

- Overall Accuracy: 75-85% for three-class regime prediction (Risk-On/Risk-Off/Transition)
- Lead Time: Sentiment-based signals detect regime transitions 1-5 trading days before VIX-based indicators
- Transition Detection: F1-score >0.70 for identifying Transition regimes (most challenging class)
- MCC Target: >0.60 (demonstrating performance well above random chance on imbalanced classes)
- Cross-validation: Time-series split validation (2016-2021 train, 2022-2023 validation, 2024+ test)

### 5.3 Backtesting Validation Events

The system will be validated on major historical market events:

- COVID-19 Crash (Feb-Mar 2020): Did sentiment signals predict Risk-Off transition before VIX spike?
- 2021 Crypto Bull Run (Jan-Nov 2021): Was cross-asset divergence visible before the crypto correction?
- 2022 Bear Market (Jan-Oct 2022): Could sentiment indices forecast Fed tightening impact?
- 2023 AI Rally (Jan-Jul 2023): Did equity sentiment decouple from broader market psychology?

### 5.4 Lead-Time Analysis (Validating H1)

This section will provide the statistical evidence that our sentiment signal moves *before* the volatility signal.

#### 5.4.1 Lagged Cross-Correlation Analysis

- **The Visualization:** A **Cross-Correlation Function (CCF) Plot**.
  - **X-axis:** Time Lags ($t-5$ to $t+5$ days).
  - **Y-axis:** Pearson Correlation Coefficient.
  - **The Goal:** Show a "Left-Skewed" peak. If the highest correlation between our *Sentiment Regime Probability* and the *VIX* occurs at $t-2$ or $t-3$, we statistically confirm sentiment leads volatility.
  - **Source Inspiration:** Trushkovskyi (2025) used similar temporal correlation plots to show sentiment metrics peaking 2 days before price changes.

#### 5.4.2 Granger Causality & Impulse Response

- **The Visualization:** An **Impulse Response Function (IRF) Chart**.
  - **Description:** Simulate a 1-standard deviation shock to the *Cross-Asset Sentiment Index*. Plot the response of the VIX over the next 10 days.
  - **Target Result:** The VIX should show a delayed significant reaction (e.g., rising after 2 days), proving the directional flow of information from Sentiment $\to$ Volatility.
  - **Citation:** Caferra (2022) and Trushkovskyi (2025) utilize this to prove causal directionality rather than just correlation.

### 5.5 Regime Detection vs. VIX (Visual Benchmarking)

This section presents visual comparison of our model against the industry standard.

#### 5.5.1 The "Early Warning" Time-Series Plot

- **The Visualization:** A dual-axis time-series chart covering a crisis period (e.g., COVID-19 Crash, Feb 2020).
  - **Primary Y-Axis (Line):** The VIX Index.
  - **Secondary Y-Axis (Shaded Region):** Our Model's "Risk-Off" Regime Probability ($P(S_t=1)$).
  - **Annotation:** Mark the date our model switched to "Risk-Off" vs. the date the VIX crossed the 30 threshold. The gap is our $\Delta_{lead}$.
  - **Source Inspiration:** Shu et al. (2024) use shaded vertical bars to depict regimes inferred by Statistical Jump Models overlaid on asset returns to demonstrate how JMs avoid the "whipsaw" false signals common in HMMs.

#### 5.5.2 Comparative Confusion Matrix (Heatmap)

- **The Visualization:** Side-by-side Confusion Matrices.
  - **Left Matrix:** FinBERT + HMM (Baseline).
  - **Right Matrix:** Our Model (FinLlama + GARCH-MIDAS + Jump Model).
  - **Focus:** Highlight the **Recall** on the "Transition" class. This shows that our model captures the *start* of the shift, whereas HMMs typically capture only the *middle* or *end* (persistence vs. noise).
  - **Source Inspiration:** Dakalbab et al. (2025) use comparative heatmaps to show how attention mechanisms improve directional accuracy over singular models.

### 5.6 Cross-Asset Divergence & Network Structure (Validating H2 & H3)

This section validates the specific mechanisms (Connectedness and Divergence) driving the detection.

#### 5.6.1 The "Entropy Radar" (Network Connectedness)

- **The Visualization:** A Radar Chart or Network Graph.
  - **Scenario:** Compare a "Normal" day vs. a "Pre-Crash" day.
  - **Data:** The **Entropy Weights** ($AssetSentix$) calculated in Methodology 3.6.2.
  - **Target Result:** Show that during the "Pre-Crash" phase, the *Connectedness* (graph density) spikes significantly, or that specific nodes (e.g., Crypto) act as the central transmitter of negative sentiment.
  - **Citation:** Cao et al. (2025) visualize sentiment spillover networks to demonstrate how high connectedness precedes crash risk.

#### 5.6.2 The Divergence Signal Chart

- **The Visualization:** A Rolling **Transfer Entropy (RTE)** Plot.
  - **Description:** Plot the $NIF$ (Net Information Flow) between Equities and Crypto.
  - **Target Result:** Show that when the flow *decouples* (drops to near zero) or *inverts* (negative sentiment flowing against price correlation), a regime switch follows shortly.
  - **Citation:** Shi (2025) uses similar visualizations to explain the decoupling of Gold and the Dollar during sentiment-driven crises.

## 6. Discussion

### 6.1 Expected Interpretations

This research will establish whether cross-asset sentiment aggregation serves as a leading indicator for market regime transitions. If validated, results will demonstrate that collective market psychology (as expressed in text data) shifts before observable price-based regime changes, supporting the behavioral finance perspective that sentiment drives prices rather than merely reflecting them.

The sentiment divergence hypothesis—that cross-asset sentiment disconnection signals regime instability—builds on Caferra’s (2022) finding that sentiment mediates cross-market relationships. Validation suggests that portfolio-level risk management should monitor not only individual asset sentiment but also the coherence of sentiment across asset classes.

### 6.2 Practical Implications

**For Portfolio Managers**:

- Early warning system for regime shifts enables proactive rebalancing before volatility spikes
- Sentiment divergence alerts identify periods of elevated transition risk
- Cross-asset sentiment indices complement traditional technical indicators

**For Risk Managers**:

- Leading indicator provides a 1-5 day advance notice for risk mitigation actions
- Sentiment connectedness metrics (following Cao et al. 2025) identify systemic risk propagation
- Real-time dashboard enables continuous monitoring vs. periodic review

**For Retail Investors**:

- Democratizes institutional-grade sentiment analysis (previously $20K+/year tools)
- Intuitive visualization makes complex sentiment data accessible
- Educational resource for understanding market psychology dynamics

### 6.3 Limitations and Constraints

This section directly addresses the computational and data challenges, specifically citing the Jump Model constraints.

- **Computational Intensity of Parameter Tuning:** While the Statistical Jump Model (JM) offers superior regime persistence compared to HMMs, Shu et al. (2024) note that selecting the optimal **jump penalty ($\lambda$)** requires a rigorous **time-series cross-validation** approach. Unlike simple parameters, $\lambda$ must be re-optimized monthly by simulating "live" trading scenarios over lookback windows to maximize the Sharpe ratio, creating significant computational overhead during the training phase.

- **Inference Latency in Transformers:** While FinBERT and RoBERTa provide superior semantic understanding, they introduce latency. Shao et al. (2024) found that while VADER processes sentiment in seconds, RoBERTa-based extraction can take hours for large datasets. This creates a trade-off between the *depth* of sentiment analysis and the *speed* of regime detection, potentially limiting the use of sentiment analysis in high-frequency applications.

- **Data Alignment Noise:** Despite using the **RR-MIDAS** framework to handle mixed frequencies, the alignment of stochastic news arrival times (irregular) with deterministic price bars (regular) inevitably introduces "alignment noise," which may degrade signal precision during periods of low news volume.

- **Data quality**: Social media data is noisy, contains sarcasm, and bots (Kraaijeveld and De Smedt 2020 documented that 1-14% of crypto tweets originate from bots).

- **Survivorship bias**: Only analyzing publicly available text (not institutional sentiment).

- **Causality vs. correlation**: Sentiment may reflect rather than predict regime shifts in some contexts.

### 6.4 Ethical Considerations

- **Market manipulation**: Could the system be gamed if widely adopted?
- **Retail vs. institutional**: Does democratizing sentiment analysis level the playing field or create new risks?
- **Data privacy**: Reddit/Twitter users may not consent to sentiment analysis

## 7. Conclusion and Future Work

### 7.1 Research Contributions

This research addresses a critical gap in financial sentiment analysis by developing the first system to aggregate multi-source, cross-asset sentiment for market regime detection. The study makes significant contributions in three specific domains:

1. **Methodological Innovation:** The development of the **Two-Layer Regime Detector**, which integrates **GARCH-MIDAS** for volatility state estimation with **Statistical Jump Models (JMs)** for discrete classification. This successfully bridges the gap between continuous volatility modeling and discrete risk-management decisions.

2. **Cross-Asset Validation:** Providing empirical evidence for the **Network Effect Hypothesis (H3)** by quantifying how sentiment connectedness (Entropy-based) across Crypto, Equities, and Forex precedes systemic crashes, validating findings by Cao et al. (2025).

3. **The "Lead-Time" Metric:** Establishing a quantifiable early-warning window (1–5 days) where sentiment divergence acts as a precursor to VIX spikes, offering a practical edge over lagging indicators like moving averages.

By applying ensemble transformer models to heterogeneous data sources (social media, news, forums) across four major asset classes, we construct sentiment indices that capture collective market psychology. The integration of these indices with the Two-Layer regime classification creates a leading indicator system that identifies Risk-On, Risk-Off, and Transition states before traditional volatility-based methods.

The real-time dashboard deployment ensures accessibility for retail investors, traders, and risk managers, potentially leveling the information asymmetry that currently favors institutional players with expensive sentiment analysis tools.

### 7.2 Future Work

1. **Adaptive Reinforcement Learning:** Moving from static ensemble weights to dynamic recalibration using the **Iterative Model Combining Algorithm (IMCA)**. As proposed by Pankwaen et al. (2025), this would allow the model to autonomously shift weight between "Sentiment" and "Price" features depending on the current volatility regime.

2. **Multimodal Integration:** Extending the input features beyond text to include audio data from earnings calls, which may contain non-verbal sentiment cues that text models miss.

3. **High-Frequency Decomposition:** Applying **Empirical Mode Decomposition (EEMD)** to analyze intraday sentiment impacts (minutes vs. hours), as suggested by Cai et al. (2024), to test if the "Lead-Time" exists at the microstructure level.

4. **Expand Asset Coverage:** Extend to more asset classes (bonds, real estate REITs).

5. **Multi-language Sentiment Analysis:** Incorporate non-English financial discourse to capture global market psychology.

6. **Causal Analysis:** Rigorous causal inference to determine whether sentiment drives prices or vice versa.

**Acknowledgments**

[Advisor name], PhD. - Capstone Advisor
Jacquelyn Cheun, PhD. – Capstone Professor
SMU MANEFRAME team - HPC support

**References**:

1. Araci, D. (2019). FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. <https://doi.org/10.48550/arxiv.1908.10063>

2. Baker, M., & Wurgler, J. (2007). Investor Sentiment in the Stock Market. The Journal of Economic Perspectives, 21(2), 129–151. <https://doi.org/10.1257/jep.21.2.129>

3. Bollen, J., Mao, H., & Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1–8. <https://doi.org/10.1016/j.jocs.2010.12.007>

4. Caferra, R. (2022). Sentiment spillover and price dynamics: Information flow in the cryptocurrency and stock market. Physica A: Statistical Mechanics and its Applications, 593, 126983. <https://doi.org/10.1016/j.physa.2022.126983>

5. Cai, Y., Tang, Z., & Chen, Y. (2024). Can real-time investor sentiment help predict the high-frequency stock returns? Evidence from a mixed-frequency-rolling decomposition forecasting method. North American Journal of Economics and Finance, 70, 102147. <https://doi.org/10.1016/j.najef.2024.102147>

6. Cao, J., He, G., & Jiao, Y. (2025). Too Sensitive to Fail: The Impact of Sentiment Connectedness on Stock Price Crash Risk. Entropy, 27(4), 345. <https://doi.org/10.3390/e27040345>

7. Dakalbab, F., Kumar, A., Abu Talib, M., et al. (2025). Advancing Forex prediction through multimodal text-driven model and attention mechanisms. Intelligent Systems with Applications, 25, 200518. <https://doi.org/10.1016/j.iswa.2025.200518>

8. Delgadillo, J., Kinyua, J., & Mutigwe, C. (2024). FinSoSent: Advancing Financial Market Sentiment Analysis through Pretrained Large Language Models. Big Data and Cognitive Computing, 8(8), 87. <https://doi.org/10.3390/bdcc8080087>

9. Ergun, Z. E., & Sefer, E. (2025). FinSentiment: Predicting Financial Sentiment Through Transfer Learning. Intelligent Systems in Accounting, Finance and Management, 32(1), e70015. <https://doi.org/10.1002/isaf.70015>

10. Fatouros, G., Soldatos, J., Kouroumali, K., Makridis, G., & Kyriazis, D. (2023). Transforming sentiment analysis in the financial domain with ChatGPT. Machine Learning with Applications, 14, 100508. <https://doi.org/10.1016/j.mlwa.2023.100508>

11. Kengmegni, D. L. (2024). Limitations of News Sentiment Analysis for Next-Day Stock Prediction. arXiv preprint arXiv:2411.05791. <https://arxiv.org/abs/2411.05791>

12. Keynes, J. M., & Royal Economic Society (Great Britain). (1973). The general theory of employment, interest, and money. Cambridge University Press for the Royal Economic Society.

13. Konstantinidis, T., Iacovides, G., Xu, M., Constantinides, T. G., & Mandic, D. (2024). FinLlama: Financial Sentiment Classification for Algorithmic Trading Applications. arXiv preprint arXiv:2403.12285. <https://arxiv.org/abs/2403.12285>

14. Kraaijeveld, O., & De Smedt, J. (2020). The predictive power of public Twitter sentiment for forecasting cryptocurrency prices. Journal of International Financial Markets, Institutions & Money, 65, Article 101188. <https://doi.org/10.1016/j.intfin.2020.101188>

15. Liu, C., Arulappan, A., Naha, R., Mahanti, A., Kamruzzaman, J., & Ra, I.-H. (2024). Large Language Models and Sentiment Analysis in Financial Markets: A Review, Datasets, and Case Study. IEEE Access, 12, 134041-134061. <https://doi.org/10.1109/ACCESS.2024.3445413>

16. LOUGHRAN, T., & MCDONALD, B. (2011). When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. The Journal of Finance (New York), 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>

17. Luo, W., & Gong, D. (2024). Pre-trained Large Language Models for Financial Sentiment Analysis. arXiv preprint arXiv:2401.05215. <https://arxiv.org/abs/2401.05215>

18. Mahendran, M., Gokul, A., Lakshmi, P. S., & Preethi, S. (2025). Comparative Advances in Financial Sentiment Analysis: A Review of BERT, FinBert, and Large Language Models. 2025 International Conference on Devices, Circuits and IoT (IDCIoT), 1-6. <https://doi.org/10.1109/idciot64235.2025.10914764>

19. Micaletti, R. C. (2022). Relative Sentiment and Machine Learning for Tactical Asset Allocation. SSRN Electronic Journal. <https://doi.org/10.2139/ssrn.3475258>

20. Cicekyurt, E., & Bakal, G. (2025). Enhancing Sentiment Analysis in Stock Market Tweets Through BERT-Based Knowledge Transfer. Computational Economics. <https://doi.org/10.1007/s10614-025-10901-8>

21. Mishev, K., Gjorgjevikj, A., Vodenska, I., Chitkushev, L. T., & Trajanov, D. (2020). Evaluation of Sentiment Analysis in Finance: From Lexicons to Transformers. IEEE Access, 8, 131662-131682. <https://doi.org/10.1109/ACCESS.2020.3009626>

22. Nasiopoulos, D. K., Roumeliotis, K. I., Sakas, D. P., & Athanasopoulou, N. I. (2025). Financial Sentiment Analysis and Classification: A Comparative Study of Fine-Tuned Deep Learning Models. International Journal of Financial Studies, 13(2), 75. <https://doi.org/10.3390/ijfs13020075>

23. Nyakurukwa, K., & Seetharam, Y. (2025). Investor sentiment networks: mapping connectedness in DJIA stocks. Financial Innovation, 11(1), 4. <https://doi.org/10.1186/s40854-024-00675-7>

24. Olaiyapo, O. E. (2024). Applying news and media sentiment analysis for generating forex trading signals. Review of Business and Economics Studies, 11(4), 84-94. <https://doi.org/10.26794/2308-944X-2023-11-4-84-94>

25. Pankwaen, K., Thongkairat, S., & Saijai, W. (2025). Global Cross-Market Trading Optimization Using Iterative Combined Algorithm: A Multi-Asset Approach with Stocks and Cryptocurrencies. Mathematics, 13(8), 1317. <https://doi.org/10.3390/math13081317>

26. Raheman, A., Kolonin, A., Fridkin, I., Ansari, W., Vishwas, M., Tulabandhula, T., & Bahrami, S. (2022). Social media sentiment analysis for cryptocurrency market prediction. arXiv preprint arXiv:2204.10185. <https://arxiv.org/abs/2204.10185>

27. Renault, T. (2017). Intraday online investor sentiment and return patterns in the U.S. stock market. Journal of Banking & Finance, 84, 25–40. <https://doi.org/10.1016/j.jbankfin.2017.07.002>

28. Roumeliotis, K. I., Nasiopoulos, D. K., & Tselikas, N. D. (2024). LLMs and NLP Models in Cryptocurrency Sentiment Analysis: A Comparative Classification Study. Big Data and Cognitive Computing, 8(6), 63. <https://doi.org/10.3390/bdcc8060063>

29. Sarfarazurrehman, S., Mane, V., & Doshi, A. (2025). AI and Machine Learning Models in Cross-Asset Class Investment Risk Analysis: A Case Study of Real Estate and Equities Markets. 2025 IEEE International Conference on Smart Systems and Applications (ICSSAS), 1-6. <https://doi.org/10.1109/icssas66150.2025.11081061>

30. Shao, Z., Yao, X., Chen, F., et al. (2024). Revisiting time-varying dynamics in stock market forecasting: A multi-source sentiment analysis approach with large language model. Decision Support Systems, 187, 114362. <https://doi.org/10.1016/j.dss.2024.114362>

31. Shen, Y., & Zhang, P. K. (2024). Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT. IEEE International Conference on Power, Intelligent Computing and Systems (Online), 717–721. <https://doi.org/10.1109/ICPICS62053.2024.10796670>

32. Shi, C. (2025). Understanding Gold and Dollar Price Movements: A Sentiment-Based GARCH-MIDAS Approach. Proceedings of the 2025 International Conference on Economics and Business Management, 47. <https://doi.org/10.2991/978-94-6463-835-6_47>

33. Shu, Y., Yu, C., & Mulvey, J. M. (2024). Downside risk reduction using regime-switching signals: a statistical jump model approach. Journal of Asset Management, 25(5), 493-507. <https://doi.org/10.1057/s41260-024-00376-x>

34. Sibande, X., Gupta, R., Demirer, R., & Bouri, E. (2021). Investor Sentiment and (Anti) Herding in the Currency Market: Evidence from Twitter Feed Data. Journal of Behavioral Finance, 24(1), 56-72. <https://doi.org/10.1080/15427560.2021.1917579>

35. Suárez-Cetrulo, A. L., Quintana, D., & Cervantes, A. (2023). Machine Learning for Financial Prediction Under Regime Change Using Technical Analysis: A Systematic Review. International Journal of Interactive Multimedia and Artificial Intelligence, 8(2), 117-138. <https://doi.org/10.9781/ijimai.2023.06.003>

36. Sun, Y., Yuan, H., & Xu, F. (2025). Financial sentiment analysis for pre-trained language models incorporating dictionary knowledge and neutral features. Natural Language Processing Journal, 10, 100148. <https://doi.org/10.1016/j.nlp.2025.100148>

37. Trushkovskyi, V. (2025). Application of Social Media Sentiment Analysis for Stock Price Prediction. Available at SSRN. <https://doi.org/10.57017/jaes.v20.3(89).11>

38. Wang, X., Wang, R., & Zhang, Y. (2024). Cross-asset momentum and the hybrid fund transmission mechanism in China’s stock and bond markets. PLOS ONE, 19(3), e0300781. <https://doi.org/10.1371/journal.pone.0300781>

39. Yang, J., Tang, Y., Li, Y., et al. (2025). Cross-Asset Risk Management: Integrating LLMs for Real-Time Monitoring of Equity, Fixed Income, and Currency Markets. arXiv preprint arXiv:2504.04292. <https://arxiv.org/abs/2504.04292>

40. Zhang, R., Yi, C., & Chen, Y. (2020). Explainable Machine Learning for Regime-Based Asset Allocation. 2020 IEEE International Conference on Big Data (Big Data), 5480-5485. <https://doi.org/10.1109/BigData50022.2020.9378332>
