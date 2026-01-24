[[TRUSHKOVSKYI_ApplicationSocialMediaSentimentAnalysis_2025]]

# [Application of Social Media Sentiment Analysis for Developing Trading Models in the Cryptocurrency Market](https://doi.org/10.57017/jaes.v20.3(89).11)

## [[Andrii TRUSHKOVSKYI]]

## Abstract
This study examines the predictive value of social media sentiment for forecasting short-term Bitcoin price changes using econometric and machine-learning models. Based on Twitter and Reddit data (2020–2025), we construct a daily sentiment index and analyse its lagged effect on returns. OLS regression and advanced models (random forest, XGBoost) show that a one-unit increase in lagged sentiment predicts a statistically significant 0.24–0.25% rise in next-day returns. Controls include momentum, volatility, and trading volume, and Granger causality tests and VARs confirm sentiment’s leading role. While volume is insignificant, sentiment and momentum are strong predictors. Machine learning models outperform linear baselines, highlighting nonlinear interactions in sentiment-driven markets. Results validate sentiment as a meaningful input for forecasting, with applications to trading bots, real-time risk dashboards, and supervisory tools. The study contributes to applied economics by showing how quantified investor emotion can serve as a leading indicator in volatile cryptocurrency markets. Future research should consider multilingual sentiment, intraday horizons, and cross-asset extensions.Copyright© 2025 The Author(s). This article is distributed under the terms of the license CC-BY 4.0, which permits any further distribution in any medium, provided the original work is properly cited. Article’s history: Received 5th of August, 2025; Revised 9th of September, 2025; Accepted 16th of September, 2025; Available online: 30th of September, 2025. Published as an article in Volume XX, Fall, Issue 3(89), 2025.

## Key concepts
#claim/machine_learning; #machine_learning; #finding/ordinary_least_squares; #ordinary_least_squares; #finding/bitcoin; #bitcoin; #finding/social_media; #social_media; #finding/cryptocurrency; #cryptocurrency; #sentiment_analysis; #finding/twitter; #twitter

## Quote
> This study examines the predictive role of social media sentiment in forecasting short-term Bitcoin price changes using econometric and machine learning models, finding that a one-unit increase in lagged sentiment predicts a statistically significant 0.24–0.25% rise in next-day returns.

## Key points
- Cryptocurrency markets, characterized by their decentralized structure and high-frequency trading environments, have emerged as some of the most volatile financial arenas globally
- We present empirical findings from the econometric and machine learning models used to examine the predictive power of social media sentiment on Bitcoin price movements
- The daily price change is volatile, with an average of 0.17%. This shows how quickly the asset's price can change. These numbers show that trading in Bitcoin was busy and volatile in 2025, with significant price changes and changes in how people felt about the market
- The results show that delayed opinion from sites like Twitter and Reddit has a statistically and economically significant impact on Bitcoin returns on the day
- The fact that nonlinear models, especially XGBoost, work better than linear ones shows that the connection between price and sentiment is not just a straight line. These results show how critical alternative data and behavioural indicators are becoming in financial forecasts, especially in markets with a lot of volatility, like cryptocurrency
- ordinary least squares (OLS) regression and advanced models show that a one-unit increase in lagged sentiment predicts a statistically significant 0.24–0.25% rise in next-day returns
- These results enrich our understanding of cryptocurrency finance and provide practical advice for navigating one of the planet's most volatile and emotionally charged marketplaces


## Summary

### Key findings
The study found that delayed opinion from social media sites like Twitter and Reddit has a statistically and economically significant impact on Bitcoin returns the next day.
A one-unit rise in the sentiment index is linked to a 0.24% – 0.25% rise in returns.
The performance of models is much better when sentiment data is added than with baseline models that use only standard technical inputs.
Nonlinear models, especially XGBoost, perform better than linear ones, indicating that the relationship between price and sentiment is not a straight line.

### Introduction
The study examines the predictive value of social media sentiment for forecasting short-term Bitcoin price changes using econometric and machine-learning models.
It constructs a daily sentiment index from Twitter and Reddit data and analyzes its lagged effect on returns.
The research aims to determine if lagging sentiment indicators can effectively forecast near-term price movements and improve the predictive accuracy of cryptocurrency price models.

### Methodology
The study uses ordinary least squares regression with lagged variables and econometric diagnostics, including stationarity tests, multicollinearity analysis, and residual analysis.
It also employs machine learning models, such as random forest and XGBoost, to compare their performance with traditional linear baselines.
The research integrates sentiment data with conventional market factors, such as volume and lagged returns, within an open, testable framework.
The study uses a sentiment index to capture a user's level of optimism or pessimism, with values less than or equal to -0.05 considered harmful and values in the middle considered neutral.
The daily sentiment index is one period behind to guarantee temporal precedence.
The study also uses an econometric model to assess how well social media sentiment can forecast short-term movements in Bitcoin prices.
The model is a multiple linear regression equation with the dependent variable being the daily price change and the independent variables being the lagged sentiment index, lagged volume, and lagged price change.

### Results
The study finds that a one-unit increase in lagged sentiment predicts a statistically significant 0.24-0.25% rise in next-day returns.
The results validate sentiment as a meaningful input for forecasting, with applications to trading bots, real-time risk dashboards, and supervisory tools.
The research highlights the importance of incorporating sentiment analysis into cryptocurrency markets, particularly for developing trading models and risk management systems.
The study found that the average Sentiment Index of 50.2 with a standard deviation of 9.6 indicates moderate variability in market sentiment.
The average price of Bitcoin is $103,500, with a daily trade volume of $55.1 billion.
The daily price change is volatile, averaging 0.17%.
The correlation matrix shows a strong positive association between the Sentiment Index and Price Change, supporting the econometric finding that investor sentiment is a good predictor of short-term returns.
The study also found that lagged sentiment has a statistically significant, positive effect on next-day Bitcoin returns, with a coefficient of 0.1439 (p < 0.01).

### Sentiment Analysis
Sentiment analysis models often use feature extraction techniques such as bag-of-words, TF-IDF, or word embeddings, and can learn to use language specific to a topic.
Deep learning models, such as Recurrent Neural Networks (RNNs), Long Short-Term Memory (LSTM) networks, and transformer-based BERT, can understand complex expressions by capturing syntactic structures and semantic relationships within text.
Lexicon-based methods, like VADER, are faster and require less training, making them suitable for real-time systems.
Social media sentiment is directly related to cryptocurrency price dynamics, with a substantial and statistically significant correlation between the lagged Sentiment Index and changes in Bitcoin price.
Sentiment indicators improve the predictive accuracy of the OLS regression model, and the results validate earlier work on the predictive power of sentiment derived from social media data.

### Econometric Models
Econometric models, such as Ordinary Least Squares (OLS), Vector Autoregression (VAR), and Generalized Autoregressive Conditional Heteroskedasticity (GARCH), are used to analyze cryptocurrency markets.
These models can describe volatility, especially when data are collected hourly or at other frequent intervals.
However, many studies do not use opinion data from sites like Twitter and Reddit and do not perform essential checks, such as ADF tests for stationarity and residual normality.

### Research Methodology
The study employs a quantitative empirical research design grounded in econometric modelling, using the ARIMAX structure to estimate the relationship between sentiment analysis of social media and short-term fluctuations in Bitcoin prices.
The data set used in the study combines daily Bitcoin market data and real-time social media sentiment data, collected via official, well-documented APIs.
The VADER tool is used to determine the sentiment of the text, and a sentiment index is created by averaging the sentiment scores of all gathered messages.

### Conclusion
The study provides strong statistical evidence for the impact of key behavioural and technical variables on short-term Bitcoin price changes.
The results show that lagged sentiment is the most relevant variable for explaining price changes, followed by lagged price change (momentum) and volatility.
The study concludes that including sentiment analysis and other behavioural factors in econometric models is important for understanding and predicting cryptocurrency price changes.
The results also suggest that market participants react significantly during periods of uncertainty and that the addition of volume negatively affects price changes.

### Sentiment
The Sentiment Index shows a strong positive linear relationship with Bitcoin's price, suggesting that investor sentiment is a leading indicator in crypto markets.
A 1-unit increase in the lagged Sentiment Index leads to a statistically significant +0.2489% increase in Bitcoin returns.
The Granger causality test confirms that sentiment "Granger-causes" Bitcoin price movements, with an F-statistic of 4.76 and a p-value of 0.009.

### Volume
The relationship between trading volume and price is counterintuitive: higher trading activity does not always reinforce price momentum.
Instead, volume can act as a contrarian indicator when divorced from sentiment dynamics.
The Granger causality test finds no statistically significant relationship between volume and price, suggesting that volume is not a reliable predictor of price.

### Market Dynamics
The cryptocurrency market is highly speculative and volatile, with dramatic highs and lows.
The market is influenced by investor emotions, including greed, fear, and confidence, which can lead to herd behavior and reckless decision-making.
The Impulse Response Function study shows that changes in sentiment cause short-lived but significant price changes, highlighting the practical utility of integrating real-time sentiment data into high-frequency trading models.
The cryptocurrency market is nonlinear, processing sentiment-driven signals over short time horizons.
Momentum effects persist even after controlling for sentiment and volatility, with the lagged price change variable remaining highly statistically significant.
Market volatility significantly amplifies the effect, and high volume may indicate market saturation or temporary exhaustion.

### Regulatory Implications
The study's findings underscore the need to integrate behavioural signals into supervisory frameworks for cryptocurrency markets.
Monitoring the joint behaviour of sentiment and trading volume allows regulators to identify destabilizing market conditions more accurately.
Regulatory authorities could use sentiment indices to fine-tune circuit breaker mechanisms, adjust risk-based margin and collateral requirements, and develop evidence-based regulatory interventions that address both structural and psychological risk factors.

### Limitations
The study acknowledges that sentiment data can be easily manipulated, and coordinated schemes can alter sentiment scores.
Future research should investigate transformer-based sentiment models to improve textual accuracy.
Real-time execution is also complex due to API rate limits, processing delays, and cloud infrastructure limits.
The use of lagged variables and Granger causality tests makes the case for predictive causation stronger, but does not prove structural causality.

### Future Directions
Future research directions include adding sentiment data across multiple languages, investigating real-time applications, and evaluating the stability of the results across different cryptocurrencies and time periods.
The study also suggests comparing studies conducted during bear and bull market periods to learn how sentiment affects outcomes.
Additionally, researchers can use natural experiments, instrumental variables, or causal reasoning frameworks to better understand how behavioural finance works.


## Study subjects

### 1000 daily observations
- We use forward-filling to deal with missing values, and standard Z-score approaches to check for outliers in all our variables. With perfectly synchronized market and sentiment indicators, the final dataset comprises about 1,000 daily observations. The study methodology revolves around the sentiment analysis procedure

## Data analysis
- #method/ols_model
- #method/ols_regression
- #method/
- #method/akaike_information_criterion
- #method/time_series_analysis
- #method/sentiment_index
- #method/nonlinear_models

## Findings
- <a class="keyword" href="https://en.wikipedia.org/wiki/ordinary_least_squares" title="ordinary least squares">OLS</a> regression and advanced models (random forest, XGBoost) show that a one-unit increase in lagged sentiment predicts a statistically significant 0.24–0.25% rise in next-day returns
- <mark class="fact">A critical study looked into Twitter sentiment patterns</mark> and discovered that public sentiment states might predict the Dow Jones Industrial Average with an accuracy rate of more than 85% ([^Agrawal_et+al_2024_a]; [^Khan_et+al_2022_a])
- The regression results (Table 4) show that lagged sentiment has a statistically significant and positive effect on next-day <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> returns, with a coefficient of +0.1439 (p < 0.01)
- There are strong momentum effects indicated by the significant lagged price change variable (coefficient +0.014, p < 0.01)
- Given the extreme volatility of the <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="bitcoin">bitcoin</a> market, the model adequately accounts for over 20.9% of the variance in price fluctuations (R2 = 0.209)
- The price effect builds up slowly, reaching its highest point around Day 2 with an overall rise of about 0.48 percent
- <mark class="fact">The final regression model confirms that a 1-unit increase in the lagged Sentiment Index leads to a</mark> statistically significant +0.2489% increase in <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> returns (p < 0.01)
- Momentum effects, in which subsequent returns reflect past price movements, continue even after sentiment and volatility are considered, as seen by the substantial statistical significance of the lagged price change variable (β = +0.2120, p < 0.01)
- The fact that market volatility (β = +0.1524, p < 0.01) significantly amplified the effect confirms that highly volatile, <mark class="fact">emotionally charged circumstances typically come before more severe price swings</mark> and should be included as vital elements in predicting models
- The effect size of trading volume was negligible and negative (β = -0.00005), <mark class="fact">even though it was statistically significant in the extended regression</mark> (p < 0.01)
- It is confirmed that <a class="keyword" href="https://en.wikipedia.org/wiki/social_media" title="social media">social media</a> sentiment is directly related to the dynamics of <a class="keyword" href="https://en.wikipedia.org/wiki/cryptocurrency" title="cryptocurrency">cryptocurrency</a> prices by the substantial and statistically significant correlation between the lagged Sentiment Index and changes in <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> price (correlation coefficient = 0.92, p < 0.01)
- <mark class="claim">Using a Granger causality test, <mark class="fact">we show that opinion Granger causes price changes with strong statistical evidence</mark> (F-statistics = 4.76, p = 0.009)</mark>
- When considering other technical measures like volume, momentum, and volatility, <mark class="fact">a one-unit rise in the sentiment index is linked to a 0.24%</mark> – 0.25% rise in returns

##  Builds on previous research
- Many use the Ordinary Least Squares (OLS) analysis to determine what happened. It is often used to see how cryptocurrency prices are related to factors that help explain them, such as trade volume, macroeconomic indicators, and, more recently, social media sentiment. [^Ciaian_et+al_2016_a]) used OLS models to study how things like speculative interest, demand, and supply affect the value of Bitcoin.

##  Confirmation of earlier findings
- Based on these findings, researchers, traders, and fintech developers can act, which shows that sentiment integration into forecasting frameworks significantly improves accuracy and explanatory power. The results validate earlier work by [^Bollen_et+al_2011_a], who found that sentiment derived from Twitter data could predict shifts in major equity indices.
- It also shows that sentiment is still a good predictor even when considering technical measures like volume and volatility. [^Smailov_et+al_2025_a]) align with our research by demonstrating the value of machine learning in extracting behavioural signals, such as user identity, from anonymized social network data.
- While their focus is on deanonymization, our work similarly leverages sentiment and user-generated content to predict market behaviour, highlighting the shared utility of optimized ML frameworks in social data analysis. [^Potwora_et+al_2024_a] complements our findings by emphasizing AI's predictive and personalization capabilities in market analysis.
- [^Potwora_et+al_2024_a] complements our findings by emphasizing AI's predictive and personalization capabilities in market analysis. Just as AI transforms marketing by forecasting consumer behaviour, our study demonstrates how AI-enhanced sentiment models can anticipate cryptocurrency price movements, reflecting the broader trend of data-driven, ethically aware decision-making in digital environments. [^Marchuk_et+al_2023_a]) reinforces the role of social media as a behavioural signal, aligning with our findings that sentiment data from platforms like Twitter and Reddit not only shape financial decision-making but also reflect broader socio-economic dynamics.
- We use lagged sentiment to ensure predictions are based on real-time data, making them more useful for algorithmic trading. [^Potwora_et+al_2023_a]) reinforces the strategic importance of digital marketing, particularly in its ability to personalize user experiences and anticipate market demand concepts that closely align with our research.
- The study by [^Orazbayev_et+al_2017_a] demonstrates how fuzzy multi-criteria programming can guide decision-making in complex, uncertain environments. Just as personalized content builds trust and improves product-market fit in e-commerce, our findings show that sentiment-driven models in cryptocurrency forecasting enhance the responsiveness and precision of trading strategies, validating the broader effectiveness of behaviourally informed, data-driven approaches in dynamic digital markets.

## Contributions
- This study sets out to empirically examine the predictive power of social media sentiment on short-term Bitcoin price changes, using a combination of econometric and machine learning techniques. <mark class="claim"><mark class="fact">The results show that delayed opinion from sites</mark> like Twitter and Reddit has a statistically and economically significant impact on Bitcoin returns the next day</mark>. When considering other technical measures like volume, momentum, and volatility, <mark class="fact">a one-unit rise in the sentiment index is linked to a 0.24%</mark> – 0.25% rise in returns. This conclusion was supported by the Granger causality analysis and impulse response functions from a VAR model, both of which show that sentiment spikes precede and affect short-term price changes. <mark class="fact">The performance of models is much better when sentiment data is added compared to baseline models</mark> that only use standard technical inputs. Volume and volatility can help explain some things but cannot show <mark class="fact">how people act like investor opinion does</mark>. Also, the fact that nonlinear models, especially XGBoost, perform <mark class="fact">better than linear ones shows that the relationship between price and sentiment is</mark> not a straight line. <mark class="claim"><mark class="fact">These results show how critical alternative data</mark> and <mark class="fact">behavioural indicators are becoming in financial forecasts</mark>, especially in markets with a lot of volatility like cryptocurrency</mark>.

## Future work
- The study suggests several avenues for future research, including the use of multilingual sentiment analysis, intraday horizons, and cross-asset extensions. The study also notes that the use of alternative data and behavioral indicators is becoming increasingly important for financial forecasts, especially in volatile markets such as cryptocurrency.
- The study suggests that future research could explore the use of alternative data sources, such as social media platforms or online forums, to analyze sentiment and its impact on cryptocurrency prices. The study also suggests that future research could investigate the use of machine learning and deep learning models to improve forecasting accuracy and explanatory power.
- The study suggests several areas for future research, including the use of transformer-based sentiment models or ensemble lexicon-ML hybrids to improve textual accuracy. The study also suggests investigating sentiment asymmetry and its impact on debt, funding rates, or options skew. Additionally, the study suggests using natural experiments, instrumental variables, or causal reasoning frameworks like Bayesian networks or structural VAR (SVAR) models to investigate the relationship between sentiment and price changes.
- The study suggests several directions for future research, including adding sentiment data in multiple languages, investigating the application of sentiment analysis in real-time, and comparing studies done during bear and bull market periods.


## References
[^Abdullah_2022_a]: Abdullah, T., &amp; Ahmet, A. (2022). Deep learning in sentiment analysis: Recent architectures. ACM Computing Surveys, 55(8), 1–37. https://doi.org/10.1145/3548772  [OA](https://doi.org/10.1145/3548772)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3548772)

[^Agrawal_et+al_2024_a]: Agrawal, S., Kumar, N., Rathee, G., Kerrache, C. A., Calafate, C. T., &amp; Bilal, M. (2024). Improving stock market prediction accuracy using sentiment and technical analysis. Electronic Commerce Research. https://doi.org/10.1007/s10660-02409874-x  [OA](https://doi.org/10.1007/s10660-02409874-x)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10660-02409874-x)

[^Alternativeme_2024_a]: Alternative.me. (2024). Crypto Fear & Greed Index. https://alternative.me/crypto/fear-and-greed-index  [OA](https://alternative.me/crypto/fear-and-greed-index)  

[^Andreev_et+al_2022_a]: Andreev, B., Sermpinis, G., &; Stasinakis, C. (2022). Modeling financial markets during extreme volatility: Evidence from the GameStop short squeeze. Forecasting, 4(3), 654–673. https://doi.org/10.3390/forecast4030035  [OA](https://doi.org/10.3390/forecast4030035)  [Scite](/scite_tallies?query=https://doi.org/10.3390/forecast4030035)

[^Aren_2023_a]: Aren, S., &amp; Nayman Hamamci, H. (2023). Evaluation of investment preference with fantasy, emotional intelligence, confidence, trust, financial literacy, and risk preference. Kybernetes, 52(12), 6203–6231. https://doi.org/10.1108/K-012022-0014  [OA](https://doi.org/10.1108/K-012022-0014)  [Scite](/scite_tallies?query=https://doi.org/10.1108/K-012022-0014)

[^Augmento_XXXX_a]: Augmento. (n.d.). Bitcoin sentiment – Bull &amp; bear index. https://www.augmento.ai/bitcoin-sentiment  [OA](https://www.augmento.ai/bitcoin-sentiment)  

[^Ballis_2022_a]: Ballis, A., &amp; Verousis, T. (2022). Behavioural finance and cryptocurrencies. Review of Behavioural Finance, 14(4), 545–562. https://doi.org/10.1108/RBF-11-2021-0256  [OA](https://doi.org/10.1108/RBF-11-2021-0256)  [Scite](/scite_tallies?query=https://doi.org/10.1108/RBF-11-2021-0256)

[^Bashiri_2024_a]: Bashiri, H., &amp; Naderi, H. (2024). Comprehensive review and comparative analysis of transformer models in sentiment analysis. Knowledge and Information Systems, 66(12), 7305–7361. https://doi.org/10.1007/s10115-024-02214-3  [OA](https://doi.org/10.1007/s10115-024-02214-3)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10115-024-02214-3)

[^Bloomberg_2024_a]: Bloomberg. (2024). Strong performance despite macro headwinds. PAT, 16(18.3), 21–23. https://images.assettype.com/bloom bergquint/2024-02/4952a7b0-2fb3-4d68-a0ae-f59a5e871665/Motilal_Oswal__PI_Industries_Q3FY24_Results_Revi ew.pdf  [OA](https://images.assettype.com/bloom)  [Scite](/scite_tallies?query=author%3ABloomberg%2Ctitle%3AStrong%20performance%20despite%20macro%20headwinds%2Cyear%3A2024)

[^Bollen_et+al_2011_a]: Bollen, J., Mao, H., &amp; Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1–8. https://doi.org/10.1016/j.jocs.2010.12.007  [OA](https://doi.org/10.1016/j.jocs.2010.12.007)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jocs.2010.12.007)

[^Bouri_et+al_2019_a]: Bouri, E., Jalkh, N., &; Roubaud, D. (2019). Commodity volatility shocks and BRIC sovereign risk: A GARCH-quantile approach. Resources Policy, 61, 385–392. https://doi.org/10.1016/j.resourpol.2018.03.013  [OA](https://doi.org/10.1016/j.resourpol.2018.03.013)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.resourpol.2018.03.013)

[^Ciaian_et+al_2016_a]: Ciaian, P., Rajcaniova, M., &amp; Kancs, D. A. (2016). The economics of Bitcoin price formation. Applied Economics, 48(19), 1799– 1815. https://doi.org/10.1080/00036846.2015.1109038  [OA](https://doi.org/10.1080/00036846.2015.1109038)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2015.1109038)

[^Coincodex_2024_a]: CoinCodex. (2024). Crypto market sentiment score. https://coincodex.com/sentiment  [OA](https://coincodex.com/sentiment)  

[^Compass_XXXX_a]: Compass Financial Technologies. (n.d.). https://www.compassft.com/indice/cscsi20  [OA](https://www.compassft.com/indice/cscsi20)  

[^Das_2023_a]: Das, R., & Singh, T. D. (2023). Multimodal sentiment analysis: A survey of methods, trends, and challenges. ACM Computing Surveys, 55(13s), 1–38. https://doi.org/10.1145/3586075  [OA](https://doi.org/10.1145/3586075)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3586075)

[^Best_2025_a]: de Best, R. (2025, May 6). Price comparison and price change of the top 100 cryptos as of May 6, 2025. Statista. https://www.statista.com/statistics/1269013/biggest-crypto-per-category-worldwide/  [OA](https://www.statista.com/statistics/1269013/biggest-crypto-per-category-worldwide/)  

[^Delfabbro_et+al_2021_a]: Delfabbro, P., King, D., Williams, J., &; Georgiou, N. (2021). Cryptocurrency trading, gambling, and problem gambling. Addictive Behaviors, 122, Article 107021. https://doi.org/10.1016/j.addbeh.2021.107021  [OA](https://doi.org/10.1016/j.addbeh.2021.107021)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.addbeh.2021.107021)

[^Govindan_2022_a]: Govindan, V., &amp; Balakrishnan, V. (2022). A machine learning approach in analysing the effect of hyperboles using negative sentiment tweets for sarcasm detection. Journal of King Saud University - Computer and Information Sciences, 34(8), 5110–5120. https://doi.org/10.1016/j.jksuci.2022.01.008  [OA](https://doi.org/10.1016/j.jksuci.2022.01.008)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jksuci.2022.01.008)

[^Han_et+al_2022_a]: Han, B., Hirshleifer, D., &amp; Walden, J. (2022). Social transmission bias and investor behaviour. Journal of Financial and Quantitative Analysis, 57(1), 390–412. https://doi.org/10.1017/S0022109021000077  [OA](https://doi.org/10.1017/S0022109021000077)  [Scite](/scite_tallies?query=https://doi.org/10.1017/S0022109021000077)

[^Hassan_et+al_2022_a]: Hassan, M. K., Hudaefi, F. A., &amp; Caraka, R. E. (2022). Mining netizens’ opinion on cryptocurrency: Sentiment analysis of Twitter data. Studies in Economics and Finance, 39(3), 365–385. https://doi.org/10.1108/SEF-06-2021-0237  [OA](https://doi.org/10.1108/SEF-06-2021-0237)  [Scite](/scite_tallies?query=https://doi.org/10.1108/SEF-06-2021-0237)

[^Hemmatian_2019_a]: Hemmatian, F., &amp; Sohrabi, M. K. (2019). A survey on classification techniques for opinion mining and sentiment analysis. Artificial Intelligence Review, 52(3), 1495–1545. https://doi.org/10.1007/s10462-017-9599-6  [OA](https://doi.org/10.1007/s10462-017-9599-6)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10462-017-9599-6)

[^Johnson_et+al_2023_a]: Johnson, B., Stjepanović, D., Leung, J., Sun, T., &amp; Chan, G. C. (2023). Cryptocurrency trading, mental health, and addiction: A qualitative analysis of Reddit discussions. Addiction Research &amp; Theory, 31(5), 345–351. https://doi.org/10.1080/16066359.2023.2174259  [OA](https://doi.org/10.1080/16066359.2023.2174259)  [Scite](/scite_tallies?query=https://doi.org/10.1080/16066359.2023.2174259)

[^Katsiampa_2017_a]: Katsiampa, P. (2017). Volatility estimation for Bitcoin: A comparison of GARCH models. Economics Letters, 158, 3–6. https://doi.org/10.1016/j.econlet.2017.06.023  [OA](https://doi.org/10.1016/j.econlet.2017.06.023)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.econlet.2017.06.023)

[^Khan_et+al_2022_a]: Khan, W., Ghazanfar, M. A., Azam, M. A., Karami, A., Alyoubi, K. H., &amp; Alfakeeh, A. S. (2022). Stock market prediction using machine learning classifiers and social media, news. Journal of Ambient Intelligence and Humanized Computing, 13, 3433–3456. https://doi.org/10.1007/s12652-020-01839-w  [OA](https://doi.org/10.1007/s12652-020-01839-w)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s12652-020-01839-w)

[^Knoppe_et+al_2025_a]: Knoppe, C., Okuneva, M., &amp; Zitti, M. (2025). Salmon stock returns around market news. Marine Resource Economics, 40(2), 107–140. https://doi.org/10.1086/734307  [OA](https://doi.org/10.1086/734307)  [Scite](/scite_tallies?query=https://doi.org/10.1086/734307)

[^Kokab_et+al_2022_a]: Kokab, S. T., Asghar, S., &amp; Naz, S. (2022). Transformer-based deep learning models for the sentiment analysis of social media data. Array, 14, Article 100157. https://doi.org/10.1016/j.array.2022.100157  [OA](https://doi.org/10.1016/j.array.2022.100157)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.array.2022.100157)

[^Korobtsova_et+al_2023_a]: Korobtsova, D., Fursa, V., &amp; Dobrovinskyi, A. (2023). Cryptocurrencies as a new form of money: Prospects for use and impact on the financial system in the future. Futurity Economics &amp; Law, 3(3), 49–66. https://doi.org/10.57125/FEL.2023.09.25.03  [OA](https://doi.org/10.57125/FEL.2023.09.25.03)  [Scite](/scite_tallies?query=https://doi.org/10.57125/FEL.2023.09.25.03)

[^Kotelnikova_et+al_2021_a]: Kotelnikova, A., Paschenko, D., Bochenina, K., &amp; Kotelnikov, E. (2021). Lexicon-based methods vs. BERT for text sentiment analysis. In I. Lytvynenko &amp; S. Lupenko (Eds.), International Conference on Analysis of Images, Social Networks and Texts (pp. 71–83). Springer International Publishing. https://doi.org/10.1007/978-3-031-16500-9_7  [OA](https://doi.org/10.1007/978-3-031-16500-9_7)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-031-16500-9_7)

[^Kristoufek_2013_a]: Kristoufek, L. (2013). Bitcoin meets Google Trends and Wikipedia: Quantifying the relationship between phenomena of the Internet era. Scientific Reports, 3(1), Article 3415. https://doi.org/10.1038/srep03415  [OA](https://doi.org/10.1038/srep03415)  [Scite](/scite_tallies?query=https://doi.org/10.1038/srep03415)

[^Marchuk_et+al_2023_a]: Marchuk, H., Plekhanova, T., &amp; Marukhovskа-Kartunova, O. (2023). Using social media to engage the public in sustainable development initiatives. Law, Business and Sustainability Herald, 3(2), 4–14. https://lbsherald.org/index.php/journal/article/view/51  [OA](https://lbsherald.org/index.php/journal/article/view/51)  [Scite](/scite_tallies?query=author%3AMarchuk%2Ctitle%3AUsing%20social%20media%20to%20engage%20the%20public%20in%20sustainable%20development%20initiatives%2Cyear%3A2023)

[^Marthinsen_2022_a]: Marthinsen, J. E., &amp; Gordon, S. R. (2022). The price and cost of Bitcoin. The Quarterly Review of Economics and Finance, 85, 280–288. https://doi.org/10.1016/j.qref.2022.04.003  [OA](https://doi.org/10.1016/j.qref.2022.04.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.qref.2022.04.003)

[^Mu_2022_a]: Muñoz, S., &; Iglesias, C. A. (2022). A text classification approach to detect psychological stress, combining a lexicon-based feature framework with distributional representations. Information Processing &amp; Management, 59(5), Article 103011. https://doi.org/10.1016/j.ipm.2022.103011  [OA](https://doi.org/10.1016/j.ipm.2022.103011)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ipm.2022.103011)

[^Nariman_2024_a]: Nariman, D. (2024). Sentiment analysis of hotel reviews using lexicon-based methods: A comparative study of VADER and TextBlob. In International Conference on Broadband and Wireless Computing, Communication and Applications (pp. 263–274). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-76452-3_25  [OA](https://doi.org/10.1007/978-3-031-76452-3_25)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-031-76452-3_25)

[^Orazbayev_et+al_2017_a]: Orazbayev, B., Ospanov, E., Kissikova, N., Mukataev, N., &amp; Orazbayeva, K. (2017). Decision-making in the fuzzy environment on the basis of various compromise schemes. Procedia Computer Science, 120, 945–952. https://doi.org/10.1016/j.procs.2017.11.330  [OA](https://doi.org/10.1016/j.procs.2017.11.330)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.procs.2017.11.330)

[^Parekh_et+al_2022_a]: Parekh, R., Patel, N. P., Thakkar, N., Gupta, R., Tanwar, S., Sharma, G., &amp; Sharma, R. (2022). DL-GuesS: Deep learning and sentiment analysis-based cryptocurrency price prediction. IEEE Access, 10, 35398–35409. https://doi.org/10.1109/ACCESS.2022.3163817  [OA](https://doi.org/10.1109/ACCESS.2022.3163817)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2022.3163817)

[^Potwora_et+al_2024_a]: Potwora, M., Vdovichena, O., Semchuk, D., Lipych, L., &amp; Saienko, V. (2024). The use of artificial intelligence in marketing strategies: Automation, personalization, and forecasting. Journal of Management World, 2, 41–49. https://doi.org/10.53935/jomw.v2024i2.275  [OA](https://doi.org/10.53935/jomw.v2024i2.275)  [Scite](/scite_tallies?query=https://doi.org/10.53935/jomw.v2024i2.275)

[^Potwora_et+al_2023_a]: Potwora, M., Zakryzhevska, I., Mostova, A., Kyrkovskyi, V., &; Saienko, V. (2023). Marketing strategies in e-commerce: Personalised content, recommendations, and increased customer trust. Financial and Credit Activity: Problems of Theory and Practice, 5(52), 562–573. https://doi.org/10.55643/fcaptp.5.52.2023.4190  [OA](https://doi.org/10.55643/fcaptp.5.52.2023.4190)  [Scite](/scite_tallies?query=https://doi.org/10.55643/fcaptp.5.52.2023.4190)

[^Puertas_et+al_2023_a]: Puertas, A. M., Clara-Rahola, J., Sánchez-Granero, M. A., de las Nieves, F. J., & Trinidad-Segovia, J. E. (2023). A new look at financial markets' efficiency from linear response theory. Finance Research Letters, 51, Article 103455. https://doi.org/10.1016/j.frl.2022.103455  [OA](https://doi.org/10.1016/j.frl.2022.103455)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.frl.2022.103455)

[^Riabchykov_2024_a]: Riabchykov, M., &amp; Mytsa, V. (2024). Improvement of intelligent systems for creating personalized products. In I. Lytvynenko &amp; S. Lupenko (Eds.), Proceedings of the 4th International Workshop on Information Technologies: Theoretical and Applied Problems (ITTAP 2024) (Volume 3896, pp. 235–247). CEUR-WS. https://ceur-ws.org/Vol-3896/ITTAP  [OA](https://ceur-ws.org/Vol-3896/ITTAP)  

[^Riabchykov_et+al_2023_a]: Riabchykov, M., Mytsa, V., Tkachuk, O., Pakholiuk, O., &amp; Melnyk, D. (2023). Efficiency of protective textile smart systems using electronic Tags. In Conference on Integrated Computer Technologies in Mechanical Engineering–Synergetic Engineering (pp. 189-197). Cham: Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-61415-6_16  [OA](https://doi.org/10.1007/978-3-031-61415-6_16)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-031-61415-6_16)

[^Riabova_et+al_2022_a]: Riabova, T., Riabov, I., Vovchanska, O., Li, T., &amp; Saienko, V. (2022). Peculiarities of digital marketing in the era of globalization: An analysis of the challenges. Financial and Credit Activity: Problems of Theory and Practice, 6(47), 160–171. https://doi.org/10.55643/fcaptp.6.47.2022.3940  [OA](https://doi.org/10.55643/fcaptp.6.47.2022.3940)  [Scite](/scite_tallies?query=https://doi.org/10.55643/fcaptp.6.47.2022.3940)

[^Rogmann_2024_a]: Rogmann, J., & Schreiber, S. (2024). Carbon credit sentiments and green energy stocks. Applied Economics. https://doi.org/10.1080/00036846.2024.2393891  [OA](https://doi.org/10.1080/00036846.2024.2393891)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2024.2393891)

[^Said_et+al_2023_a]: Said, F. F., Somasuntharam, R. S., Yaakub, M. R., &amp; Sarmidi, T. (2023). Impact of Google searches and social media on the volatility of digital assets. Humanities and Social Sciences Communications, 10(1), 1–17. https://doi.org/10.1057/s41599-02302400-8  [OA](https://doi.org/10.1057/s41599-02302400-8)  [Scite](/scite_tallies?query=https://doi.org/10.1057/s41599-02302400-8)

[^Selvakumar_et+al_2025_a]: Selvakumar, P., Mishra, R. K., Budhiraja, A., Dahake, P. S., Chandel, P. S., &amp; Vats, C. (2025). Social media influence on market sentiment. In Unveiling investor biases that shape market dynamics (pp. 225–250). IGI Global Scientific Publishing. https://doi.org/10.4018/979-8-3693-3994-7.ch009  [OA](https://doi.org/10.4018/979-8-3693-3994-7.ch009)  [Scite](/scite_tallies?query=https://doi.org/10.4018/979-8-3693-3994-7.ch009)

[^Shah_2024_a]: Shah, S. S., &amp; Shah, S. A. H. (2024). Trust as a determinant of social welfare in the digital economy. Social Network Analysis and Mining, 14(1), Article 79. https://doi.org/10.1007/s13278-024-01238-5  [OA](https://doi.org/10.1007/s13278-024-01238-5)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s13278-024-01238-5)

[^Shah_et+al_2023_a]: Shah, S. S., Serna, R. J., &; Delgado, O. S. (2023). Modelling the influence of social learning on responsible consumption through directed graphs. Electronic Research Archive, 31(9), 5161–5206. https://doi.org/10.3934/era.2023263  [OA](https://doi.org/10.3934/era.2023263)  [Scite](/scite_tallies?query=https://doi.org/10.3934/era.2023263)

[^Smailov_et+al_2025_a]: Smailov, N., Uralova, F., Kadyrova, R., Magazov, R., &amp; Sabibolda, A. (2025). Optimization of machine learning methods for de-anonymization in social networks. Informatyka, Automatyka, Pomiary w Gospodarce i Ochronie Środowiska, 15(1), 101–104. https://doi.org/10.35784/iapgos.7098  [OA](https://doi.org/10.35784/iapgos.7098)  [Scite](/scite_tallies?query=https://doi.org/10.35784/iapgos.7098)

[^The_XXXX_b]: The Tie. (n.d.). Sentiment API documentation. https://www.thetie.io/solutions/sentiment-api  [OA](https://www.thetie.io/solutions/sentiment-api)  

[^Token_XXXX_c]: Token Metrics. (n.d.). Sentiment guide. https://developers.tokenmetrics.com/docs/sentiment-guide  [OA](https://developers.tokenmetrics.com/docs/sentiment-guide)  

[^Valle-Cruz_et+al_2022_a]: Valle-Cruz, D., Fernández-Cortez, V., López-Chau, A., & Sandoval-Almazán, R. (2022). Does Twitter affect stock market decisions? Financial sentiment analysis during pandemics: A comparative study of the H1N1 and the COVID-19 periods. Cognitive Computation, 14(1), 372–387. https://doi.org/10.1007/s12559-021-09819-8  [OA](https://doi.org/10.1007/s12559-021-09819-8)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s12559-021-09819-8)

[^Vlahavas_2024_a]: Vlahavas, G., &amp; Vakali, A. (2024). Dynamics between Bitcoin market trends and social media activity. FinTech, 3(3), 349–378. https://doi.org/10.3390/fintech3030020  [OA](https://doi.org/10.3390/fintech3030020)  [Scite](/scite_tallies?query=https://doi.org/10.3390/fintech3030020)

[^Wang_et+al_2019_a]: Wang, J., Xie, Z., Li, Q., Tan, J., Xing, R., Chen, Y., &amp; Wu, F. (2019). Effect of digitalized rumour clarification on stock markets. Emerging Markets Finance and Trade, 55(2), 450–474. https://doi.org/10.1080/1540496X.2018.1534683  [OA](https://doi.org/10.1080/1540496X.2018.1534683)  [Scite](/scite_tallies?query=https://doi.org/10.1080/1540496X.2018.1534683)

[^Wankhade_et+al_2022_a]: Wankhade, M., Rao, A. C. S., &amp; Kulkarni, C. (2022). A survey on sentiment analysis methods, applications, and challenges. Artificial Intelligence Review, 55(7), 5731–5780. https://doi.org/10.1007/s10462-022-10144-1  [OA](https://doi.org/10.1007/s10462-022-10144-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10462-022-10144-1)

[^Zeng_et+al_2022_a]: Zeng, H., Shao, B., Bian, G., Dai, H., &amp; Zhou, F. (2022). A hybrid deep learning approach by integrating extreme gradient boosting-long short-term memory with generalized autoregressive conditional heteroscedasticity family models for natural gas load volatility prediction. Energy Science &amp; Engineering, 10(7), 1998–2021. https://doi.org/10.1002/ese3.1122  [OA](https://doi.org/10.1002/ese3.1122)  [Scite](/scite_tallies?query=https://doi.org/10.1002/ese3.1122)

