[[TRUSHKOVSKYI_ApplicationSocialMediaSentimentAnalysis_2025]]

# [Application of Social Media Sentiment Analysis for Developing Trading Models in the Cryptocurrency Market](https://doi.org/10.57017/jaes.v20.3(89).11)

## [[Andrii TRUSHKOVSKYI]]

## Abstract

This study examines the predictive value of social media sentiment for forecasting short-term Bitcoin price changes using econometric and machine-learning models. Based on Twitter and Reddit data (2020–2025), we construct a daily sentiment index and analyse its lagged effect on returns. OLS regression and advanced models (random forest, XGBoost) show that a one-unit increase in lagged sentiment predicts a statistically significant 0.24–0.25% rise in next-day returns. Controls include momentum, volatility, and trading volume, and Granger causality tests and VARs confirm sentiment’s leading role. While volume is insignificant, sentiment and momentum are strong predictors. Machine learning models outperform linear baselines, highlighting nonlinear interactions in sentiment-driven markets. Results validate sentiment as a meaningful input for forecasting, with applications to trading bots, real-time risk dashboards, and supervisory tools. The study contributes to applied economics by showing how quantified investor emotion can serve as a leading indicator in volatile cryptocurrency markets. Future research should consider multilingual sentiment, intraday horizons, and cross-asset extensions.Copyright© 2025 The Author(s). This article is distributed under the terms of the license CC-BY 4.0, which permits any further distribution in any medium, provided the original work is properly cited. Article’s history: Received 5th of August, 2025; Revised 9th of September, 2025; Accepted 16th of September, 2025; Available online: 30th of September, 2025. Published as an article in Volume XX, Fall, Issue 3(89), 2025.

## Key concepts

# claim/machine_learning; #machine_learning; #finding/ordinary_least_squares; #ordinary_least_squares; #finding/bitcoin; #bitcoin; #finding/social_media; #social_media; #finding/cryptocurrency; #cryptocurrency; #sentiment_analysis; #finding/twitter; #twitter

## Quote
>
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

The study examines the predictive power of social media sentiment for forecasting short-term Bitcoin price changes using econometric and machine-learning models.
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
The use of lagged variables and Granger causality tests strengthens the case for predictive causation, but does not prove structural causality.

### Future Directions

Future research directions include adding sentiment data across multiple languages, investigating real-time applications, and assessing the stability of the results across different cryptocurrencies and time periods.
The study also suggests comparing studies conducted during bear and bull market periods to learn how sentiment changes.
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
- The regression results (Table 4) show that lagged sentiment has a statistically significant and positive effect on next-day <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> returns, with a coefficient of +0.1439 (p &lt; 0.01)
- There are strong momentum effects indicated by the significant lagged price change variable (coefficient +0.014, p &lt; 0.01)
- Given the extreme volatility of the <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="bitcoin">bitcoin</a> market, the model adequately accounts for over 20.9% of the variance in price fluctuations (R2 = 0.209)
- The price effect builds up slowly, reaching its highest point around Day 2 with an overall rise of about 0.48 percent
- <mark class="fact">The final regression model confirms that a 1-unit increase in the lagged Sentiment Index leads to a</mark> statistically significant +0.2489% increase in <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> returns (p &lt; 0.01)
- Momentum effects, in which subsequent returns reflect past price movements, continue even after sentiment and volatility are considered, as seen by the substantial statistical significance of the lagged price change variable (β = +0.2120, p &lt; 0.01)
- The fact that market volatility (β = +0.1524, p &lt; 0.01) significantly amplified the effect confirms that highly volatile, <mark class="fact">emotionally charged circumstances typically come before more severe price swings</mark> and should be included as vital elements in predicting models
- The effect size of trading volume was negligible and negative (β = -0.00005), <mark class="fact">even though it was statistically significant in the extended regression</mark> (p &lt; 0.01)
- It is confirmed that <a class="keyword" href="https://en.wikipedia.org/wiki/social_media" title="social media">social media</a> sentiment is directly related to the dynamics of <a class="keyword" href="https://en.wikipedia.org/wiki/cryptocurrency" title="cryptocurrency">cryptocurrency</a> prices by the substantial and statistically significant correlation between the lagged Sentiment Index and changes in <a class="keyword" href="https://en.wikipedia.org/wiki/bitcoin" title="Bitcoin">Bitcoin</a> price (correlation coefficient = 0.92, p &lt; 0.01)
- <mark class="claim">Using a Granger causality test, <mark class="fact">we show that opinion Granger causes price changes with strong statistical evidence</mark> (F-statistics = 4.76, p = 0.009)</mark>
- When considering other technical measures like volume, momentum, and volatility, <mark class="fact">a one-unit rise in the sentiment index is linked to a 0.24%</mark> – 0.25% rise in returns

## Builds on previous research

- Many use the Ordinary Least Squares (OLS) analysis to determine what happened. It is often used to see how cryptocurrency prices are related to factors that help explain them, such as trade volume, macroeconomic indicators, and, more recently, social media sentiment. [^Ciaian_et+al_2016_a]) used OLS models to study how things like speculative interest, demand, and supply affect the value of Bitcoin.

## Confirmation of earlier findings

- Based on these findings, researchers, traders, and fintech developers can act, which shows that sentiment integration into forecasting frameworks significantly improves accuracy and explanatory power. The results validate earlier work by [^Bollen_et+al_2011_a]), who found that sentiment derived from Twitter data could predict shifts in major equity indices.
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

[^Agrawal_et+al_2024_a]: Agrawal, S., Kumar, N., Rathee, G., Kerrache, C. A., Calafate, C. T., &amp; Bilal, M. (2024). Improving stock market prediction accuracy using sentiment and technical analysis. Electronic Commerce Research. <https://doi.org/10.1007/s10660-02409874-x>  [OA](https://doi.org/10.1007/s10660-02409874-x)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10660-02409874-x)

[^Bollen_et+al_2011_a]: Bollen, J., Mao, H., &amp; Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1–8. <https://doi.org/10.1016/j.jocs.2010.12.007>  [OA](https://doi.org/10.1016/j.jocs.2010.12.007)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jocs.2010.12.007)

[^Ciaian_et+al_2016_a]: Ciaian, P., Rajcaniova, M., &amp; Kancs, D. A. (2016). The economics of Bitcoin price formation. Applied Economics, 48(19), 1799– 1815. <https://doi.org/10.1080/00036846.2015.1109038>  [OA](https://doi.org/10.1080/00036846.2015.1109038)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2015.1109038)

[^Khan_et+al_2022_a]: Khan, W., Ghazanfar, M. A., Azam, M. A., Karami, A., Alyoubi, K. H., &amp; Alfakeeh, A. S. (2022). Stock market prediction using machine learning classifiers and social media, news. Journal of Ambient Intelligence and Humanized Computing, 13, 3433–3456. <https://doi.org/10.1007/s12652-020-01839-w>  [OA](https://doi.org/10.1007/s12652-020-01839-w)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s12652-020-01839-w)

[^Marchuk_et+al_2023_a]: Marchuk, H., Plekhanova, T., &amp; Marukhovskа-Kartunova, O. (2023). Using social media to engage the public in sustainable development initiatives. Law, Business and Sustainability Herald, 3(2), 4–14. <https://lbsherald.org/index.php/journal/article/view/51>  [OA](https://lbsherald.org/index.php/journal/article/view/51)  [Scite](/scite_tallies?query=author%3AMarchuk%2Ctitle%3AUsing%20social%20media%20to%20engage%20the%20public%20in%20sustainable%20development%20initiatives%2Cyear%3A2023)

[^Orazbayev_et+al_2017_a]: Orazbayev, B., Ospanov, E., Kissikova, N., Mukataev, N., &amp; Orazbayeva, K. (2017). Decision-making in the fuzzy environment on the basis of various compromise schemes. Procedia Computer Science, 120, 945–952. <https://doi.org/10.1016/j.procs.2017.11.330>  [OA](https://doi.org/10.1016/j.procs.2017.11.330)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.procs.2017.11.330)

[^Potwora_et+al_2024_a]: Potwora, M., Vdovichena, O., Semchuk, D., Lipych, L., &amp; Saienko, V. (2024). The use of artificial intelligence in marketing strategies: Automation, personalization and forecasting. Journal of Management World, 2, 41–49. <https://doi.org/10.53935/jomw.v2024i2.275>  [OA](https://doi.org/10.53935/jomw.v2024i2.275)  [Scite](/scite_tallies?query=https://doi.org/10.53935/jomw.v2024i2.275)

[^Potwora_et+al_2023_a]: Potwora, M., Zakryzhevska, I., Mostova, A., Kyrkovskyi, V., &amp; Saienko, V. (2023). Marketing strategies in e-commerce: Personalised content, recommendations, and increased customer trust. Financial and Credit Activity: Problems of Theory and Practice, 5(52), 562–573. <https://doi.org/10.55643/fcaptp.5.52.2023.4190>  [OA](https://doi.org/10.55643/fcaptp.5.52.2023.4190)  [Scite](/scite_tallies?query=https://doi.org/10.55643/fcaptp.5.52.2023.4190)

[^Smailov_et+al_2025_a]: Smailov, N., Uralova, F., Kadyrova, R., Magazov, R., &amp; Sabibolda, A. (2025). Optimization of machine learning methods for de-anonymization in social networks. Informatyka, Automatyka, Pomiary w Gospodarce i Ochronie Środowiska, 15(1), 101–104. <https://doi.org/10.35784/iapgos.7098>  [OA](https://doi.org/10.35784/iapgos.7098)  [Scite](/scite_tallies?query=https://doi.org/10.35784/iapgos.7098)
