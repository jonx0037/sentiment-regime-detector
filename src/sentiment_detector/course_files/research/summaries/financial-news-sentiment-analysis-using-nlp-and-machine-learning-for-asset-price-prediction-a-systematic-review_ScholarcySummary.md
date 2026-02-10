[[Ehsan_et+al_FinancialNewsSentimentAnalysisUsing_2025]]

# [Financial News Sentiment Analysis Using NLP and Machine Learning for Asset Price Prediction: A Systematic Review](https://doi.org/10.21015/vtse.v13i3.2165)

## [[Aqsa Ehsan]]; [[Shaista Habib]]; [[Aamir Sohail]]

## Abstract

Forecasting market movements in stocks, gold, and crude oil requires a deep understanding of how financial news sentiment influences asset prices. Analyzing news sentiment is crucial for understanding market dynamics and forecasting price fluctuations. However, creating accurate financial news datasets, particularly in terms of proper labeling and sourcing, remains a significant challenge. This paper presents a comprehensive literature review on financial news sentiment analysis and its application in market trend prediction. By reviewing articles in reputable journals from 2018–2025, we consolidate key findings, including techniques for dataset creation, labeling, and sourcing, as well as the use of advanced methods such as Natural Language Processing (NLP) and deep learning models. This review contributes to the growing literature on sentiment analysis in the context of the relationship between stocks and commodities, especially gold and crude oil, and examines the role of global and market-specific news sentiment in determining asset prices. The study focuses on issues that concern researchers in this regard; it also compares the relative success of various prediction models and discusses the criteria for assessing their effectiveness. We propose solutions to current challenges and outline future research directions to improve sentiment analysis in financial markets.

## Key concepts

# machine_learning; #claim/deep_learning; #deep_learning; #claim/crude_oil; #crude_oil; #claim/natural_language_processing; #natural_language_processing; #financial_news; #sentiment_analysis; #stock_market; #claim/financial_market; #financial_market

## Quote

This paper presents a comprehensive literature review of financial news sentiment analysis and its application to market trend prediction, focusing on stocks, gold, and crude oil, and discussing the challenges and future research directions in this field.

## Key points

- This paper presents a comprehensive literature review on financial news sentiment analysis and its application in market trend prediction. By reviewing articles in reputable journals from 2018–2025, we consolidate key findings, including techniques for dataset creation, labeling, and sourcing, as well as the use of advanced methods such as Natural Language Processing (NLP) and deep learning models
- Financial markets are affected by various factors, one of which includes sentiment about financial news, a measure of tone, and implications attached to the news content. News sentiment influences investor behavior and market trends, and adds a predictive signal to price models
- Many existing models focus on sentiment classification, yet they often overlook the deeper causal mechanisms driving financial markets
- The future of financial news sentiment analysis lies in the development of adaptive, interpretable, and causality-driven models
- By embracing these advanced methodologies, researchers can enhance the predictive power of sentiment analysis tools and provide more valuable information to academics and practitioners in financial markets

## Summary

### Introduction

The paper presents a systematic review of financial news sentiment analysis and its application in market trend prediction.
It aims to consolidate key findings, including techniques for dataset creation, labeling, and sourcing, as well as the use of advanced methods such as Natural Language Processing (NLP) and deep learning models.
The review focuses on the relationship between stocks and commodities, particularly gold and crude oil, and on the role of global and market-specific news sentiment in determining asset prices.

### Sentiment Analysis

Sentiment analysis is crucial for understanding market dynamics and forecasting price fluctuations.
Advanced machine-learning models, such as CNN-LSTM, support this improvement.
Domain-specific NLP models, like FinBERT, capture rapid news-driven moves.
Trading strategies that incorporate sentiment analysis have been shown to outperform traditional approaches in various market conditions.
Sentiment analysis improves the ability to understand differences between related activities and the fundamental causes of market trends.
Sentiment analysis is a powerful tool for navigating today’s financial markets, as it analyzes the emotional tone in news articles and other textual sources to understand how investor sentiment may currently impact markets.
The sentiment of news reports is often correlated with stock price fluctuations, and investors react to the most recent company updates or economic information.
In the oil market, sentiment derived from news stories has been shown to improve forecasting accuracy, with traditional media offering more insightful information than social media.
Similarly, in the gold market, understanding sentiment helps predict price changes, which are driven by a combination of financial news and macroeconomic factors.
The integration of sentiment analysis with Graph Neural Networks (GNNs) enables models to leverage both direct news sentiment and broader industry context to more accurately predict stock prices.
The Multi-source Aggregated Classification (MAC) method improves prediction by combining sentiment data from human-generated news with technical indicators and transaction data.
Techniques such as Natural Language Processing (NLP) and Sentiment Analysis, Generative Adversarial Networks (GANs), and Attention Mechanisms are used for sentiment analysis.

### Research Gaps

Despite the increasing use of sentiment analysis in financial markets, there is no unified synthesis of techniques applied across multiple asset classes.
Existing studies focus on isolated aspects, either evaluating the impact of sentiment on a single asset class or applying limited methodologies that fail to capture the interdependencies between global and market-specific news.
The lack of a unified synthesis across diverse asset classes and market conditions limits the broader applicability of sentiment analysis.
The review aims to bridge these gaps by providing an integrated context for sentiment analysis across multiple financial assets.

### Research Objectives

The research aims to predict stock and commodity price movements from financial news, examine the role of global and market-specific news sentiment in influencing price volatility, and investigate spillover effects and interdependencies among different asset classes.
The study also seeks to understand the challenges and restrictions of sentiment analysis techniques and analyze the use of causal inference techniques to differentiate between correlations and causal relationships.

### Methodology

The systematic literature review involved formulating structured research questions, developing a comprehensive search strategy, and applying strict inclusion and exclusion criteria to identify high-quality research on sentiment analysis in financial markets.
The search strategy included exploring publicly recognized academic databases such as ScienceDirect, SpringerLink, IEEE Xplore, and Web of Science, and using keywords like "financial news OR sentiment analysis" combined with "stock price prediction OR commodity price prediction OR gold price." A total of 10,655 records were collected, and after removing duplicates and applying the inclusion and exclusion criteria, 109 studies were included.

### Literature Review

The literature review focuses on previous research on stocks, crude oil, and gold, analyzing how sentiment analysis is used to predict price changes and understand market behavior.
The review highlights the connection between sentiment and price volatility, discusses the challenges and research gaps, and lays the groundwork for deeper research in this space.
The leading publication sources include IEEE Xplore, Resources Policy, Energy Economics, and International Review of Financial Analysis, with Asia emerging as the leading region in terms of publication output, followed by notable contributions from Europe, Oceania, and other regions.

### Data Preprocessing

Data preprocessing is a critical step in creating a financial news dataset for market prediction models.
This involves cleaning the text to remove unnecessary symbols, numbers, punctuation, and stopwords, then tokenizing it into words or phrases for sentiment analysis.
Normalization is then applied, usually by converting text to lowercase, and lemmatization is used to reduce words to their base forms.
Stopwords that do not provide significant sentiment value are removed to reduce noise, and missing data is handled through interpolation or imputation.

### Analysis Methods

Various methodologies have been devised to capture the relationship between sentiment and behavior in the market, including Natural Language Processing (NLP) and sentiment analysis, deep learning models, Generative Adversarial Networks (GANs) and attention mechanisms, investor sentiment indices and econometric models, hybrid and real-time sentiment analysis models, and Graph Neural Networks (GNNs) and Multi-Source Aggregated Classification (MAC).
These approaches combine econometrics, machine learning algorithms, and NLP to analyze sentiment data and selectively predict price movements.

### Market Dynamics

Geopolitical risks, such as conflicts and regional instability, influence commodity prices, particularly oil.
International trade policies, economic crises, and US monetary policy decisions also impact market dynamics.
The Ukraine war, for example, disrupted global energy supply chains, causing large price fluctuations in commodities such as oil and gas, and stocks.
Economic reports and corporate earnings also drive price volatility and market sentiment.

### Causal Inference

Causal inference methods, such as Granger causality and transfer entropy, are used to differentiate between correlation and causation in the relationship between news sentiment and price movements.
Granger causality assesses whether future observations of one variable can be predicted from past values of another, while transfer entropy quantifies the flow of information between two time series, detecting both linear and nonlinear relationships.
These methods help determine whether price movements arise from changes in news sentiment or coexist due to other factors.

### Correlation Vs Causality

Correlation means that two variables move together, while causality means that one variable directly affects the other.
Asymmetric causality methods, such as nonlinear Granger Causality and Asymmetric Vector Autoregression (AVAR), are used to test whether negative news affects prices more strongly or for a longer period than positive news.
Causal inference methods, such as Granger causality and transfer entropy, are used to establish causality, i.e., whether news sentiment causes movements in asset prices.

### Evaluation Metrics

Several evaluation metrics are used to assess the performance of sentiment analysis models in predicting price movements in financial markets.
These include accuracy, precision, recall, F1-score, Mean Absolute Error (MAE), and Mean Squared Error (MSE).
The F1 score is a balanced evaluation metric that offers a more reliable measure of model performance than accuracy alone.
Time-series-specific metrics, such as cross-validation and out-of-sample prediction performance, are also important for assessing how a model would perform on unseen data.

### Limitations And Challenges

Current research on applying sentiment analysis techniques to financial news for predicting asset prices has several limitations, including manual data categorization, high computational requirements, limited model adaptability across industries and market conditions, and noisy data and subjective sentiment interpretation.
Future research directions include improving model efficiency, leveraging more sophisticated natural language processing (NLP) models, and incorporating additional data sources, such as social media and real-time news.

### Limitations

The model has an intricate architecture and requires significant processing time, which can be a challenge for real-time applications.
The prediction model may not be generalizable across different time periods or markets.
Media sentiment from Twitter and news may not always reflect true sentiment, and results may vary depending on the platform used.
The model’s ability to predict stock movements is limited by the accuracy of the sentiment analysis and the quality of the news data.

### Future Directions

Future research could focus on developing models that use lower processing resources while maintaining comparable levels of precision.
It is also recommended to incorporate larger datasets and additional geopolitical/macroeconomic factors to improve model accuracy.
Future research should incorporate a broader range of datasets and timeframes and integrate additional external economic indicators to improve performance.
Future work could explore advanced machine learning techniques and develop real-time prediction systems to improve accuracy.

### Challenges

Sentiment analysis applied to financial news to predict asset prices is hampered by several major obstacles, including the creation and availability of high-quality datasets.
News classification into appropriate categories and the ability of sentiment analysis tools to properly infer news sentiments are both tough tasks.
Research also struggles with the causal relationship between news sentiment and asset prices, and market volatility and misinformation make the predictive power of sentiment analysis even harder.

### Models

The future of financial news sentiment analysis lies in the development of adaptive, interpretable, and causality-driven models.
These models should not only predict but also be transparent, allowing stakeholders to trust the predictions and understand the underlying mechanisms.

### Research

The research was conducted independently, without any financial, commercial, or personal relationships that could influence the outcomes or interpretations presented.
The study is grounded on a systematic review of literature, which is publicly available and conforms to the ethical guidelines of secondary data analysis.

### Ethics

The authors declare no conflict of interest related to the content of this study.
The ethical principles of academic integrity are adhered to in this work, and the intellectual property rights of the original authors are respected.
No human or animal subjects, nor sensitive personal data, are involved in this study.

## Study subjects

### 109 papers

- Articles included in the systematic literature review (n=109). Final selected papers (n=109). only on research that is directly related to the area of sentiment analysis in financial markets

### 53 papers

- In ScienceDirect, for instance, we used keywords like "financial news OR sentiment analysis" combined with "stock price prediction OR commodity price prediction OR gold price." This search resulted in roughly 5,000 results. After carefully reviewing them, we identified 53 highly relevant papers. IEEE Xplore, with the same keyword strategy, returned about 2,500 articles

## Data analysis

- #method/large_language_models

## Differs from previous work

- Correlation, on the other hand, is reserved for monotonically quantifying the strength and direction of an association between two (or more) variables, while causality is reserved for the notion of such a relationship because it implies a directional change, that is, the change of values in one variable can (and indeed must) directly lead to the change of values in the other [^74]. This distinction is very important when we are working with financial markets, as news sentiment correlation between price movements does not necessarily imply that sentiment drives price changes.

## Confirmation of earlier findings

- For example, studies using causal inference techniques have shown that sentiment metrics can filter out background noise to isolate genuine market-moving news, thus improving financial modeling by capturing the interconnectedness of global markets [^2], [^50]. This paper shows that sentiment analysis improves the ability to understand differences between related activities and the fundamental causes of market trends.

## Contributions

- In conclusion, data preprocessing, extraction, and annotation techniques are essential to ensure that the data used in financial news sentiment analysis is clean, structured, and meaningful. Techniques such as web scraping, sentiment lexicons, and machine learning methods, such as SVM and LSTM, are commonly used to improve the accuracy of predictions of stock movements.

## Future work

- The future work in the field of financial news sentiment analysis will revolve around the integration of causal inference methods, the development of dynamic real-time datasets, and the use of advanced machine learning models. The study also highlights the need for researchers to develop more accurate and reliable financial news sentiment analysis by integrating real-time, dynamic datasets and multimodal data fusion from multiple sources.
- Future work includes developing models that use lower processing resources while maintaining comparable levels of precision. The study suggests incorporating more extensive datasets and additional geopolitical/macroeconomic factors to improve model accuracy.

## References

[^2]: K. Nam, N. Seong. & Financial news-based stock movement prediction using causality analysis of influence in the Korean stock market,&  in Decision Support Systems, vol. 117, pp. 100–112, 2019.  [OA](https://scholar.google.co.uk/scholar?q=Nam%2C%20K.%20Seong%2C%20N.%20Financial%20news-based%20stock%20movement%20prediction%20using%20causality%20analysis%20of%20influence%20in%20the%20Korean%20stock%20market%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Nam%2C%20K.%20Seong%2C%20N.%20Financial%20news-based%20stock%20movement%20prediction%20using%20causality%20analysis%20of%20influence%20in%20the%20Korean%20stock%20market%202019)

[^50]: S. Usmani, J. Shamsi, & News headlines categorization scheme for unlabelled data,&  in 2020 International Conference on Emerging Trends in Smart Technologies (ICETST), 2020, pp. 1–6.  [OA](https://scholar.google.co.uk/scholar?q=Usmani%2C%20S.%20Shamsi%2C%20J.%20News%20headlines%20categorization%20scheme%20for%20unlabelled%20data%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Usmani%2C%20S.%20Shamsi%2C%20J.%20News%20headlines%20categorization%20scheme%20for%20unlabelled%20data%202020)

[^74]: G. Anese et al., “Impact of public news sentiment on stock market index return and volatility,” Comput. Manag. Sci., vol. 20, no. 1, p. 20, 2023.  [OA](https://engine.scholarcy.com/oa_version?query=Anese%2C%20G.%20Impact%20of%20public%20news%20sentiment%20on%20stock%20market%20index%20return%20and%20volatility%202023&author=Anese&title=Impact%20of%20public%20news%20sentiment%20on%20stock%20market%20index%20return%20and%20volatility&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Anese%2C%20G.%20Impact%20of%20public%20news%20sentiment%20on%20stock%20market%20index%20return%20and%20volatility%202023) [Scite](/scite_tallies?query=author%3AAnese%2Ctitle%3AImpact%20of%20public%20news%20sentiment%20on%20stock%20market%20index%20return%20and%20volatility%2Cyear%3A2023)
