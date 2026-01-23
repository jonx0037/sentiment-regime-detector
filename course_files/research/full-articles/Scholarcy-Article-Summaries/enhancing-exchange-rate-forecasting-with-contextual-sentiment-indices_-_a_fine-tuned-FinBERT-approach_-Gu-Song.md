[[Gu_EnhancingExchangeRateForecastingWith_2026]]

# [Enhancing exchange rate forecasting with contextual sentiment indices: A fine-tuned FinBERT approach](https://doi.org/10.1016/j.asoc.2026.114556)

## [[Guoqin Gu]]; [[Yuping Song]]

## Abstract
The incorporation of sentiment as a predictor of exchange rate movements has long been of interest to the academic community. ==This paper argues that, due to the relative and interdependent nature of currency fluctuations, the sentiment contained in foreign exchange news cannot be effectively captured through current sentiment analysis tools==. Instead, it requires models specifically adapted to the characteristics of each currency pair. To address this gap, we take EUR/USD pair as an example, construct a manually annotated news dataset and fine-tune the FinBERT model on an annual rolling basis to produce a series of specialized sentiment classifiers. ==Based on these models, we develop contextual sentiment indices and incorporate them as predictors of exchange rate changes==. ==Our empirical findings offer several key insights. (1) The fine-tuned FinBERT models exhibit strong capability in identifying forex-specific sentiment, achieving an out-of-sample accuracy of 84.33 %, and outperforming traditional sentiment tools as well as four state-of-the-art large language models. ==(2) Using a doubly debiased machine learning framework, we show that the developed sentiment indices exert a statistically significant influence on exchange rate movements==. (3) Compared with benchmark predictors—including technical indicators and macroeconomic variables—the inclusion of sentiment indices consistently enhances the forecasting performance of LSTM models, their variants, and a range of machine learning methods==. Overall, this study contributes to both sentiment analysis and exchange rate forecasting by providing a currency-pair-specific modeling framework and demonstrating that fine-tuned language models can materially improve predictive accuracy in financial applications.

## Key concepts
#sentiment_analysis; #long_short_term_memory; #average_treatment_effects; #claim/index; #index; #finding/sentiment; #sentiment; #finding/large_language_models; #large_language_models; #foreign_exchange

## Quote
> This study proposes a novel sentiment analysis model, FXFinBERT, tailored for the EUR/USD currency pair, which outperforms traditional sentiment analysis tools and state-of-the-art large language models in capturing nuanced sentiment of forex-related news, achieving an out-of-sample accuracy of 84.33%.

## Key points
- As globalization progresses and international trade intensifies, accurately forecasting exchange rate fluctuations has become increasingly significant [^1]
- These include Mean Absolute Error (MAE), Mean Squared Error (MSE), Mean Squared Logarithmic Error (MSLE), Mean Absolute Percentage Error (MAPE), and Logarithm of the Hyperbolic Cosine Loss (LogCosh), each defined by the following formulas: 1 ∑n
- This study contributes to the literature on exchange rate forecasting by proposing a novel sentiment analysis model, FXFinBERT, tailored for the EUR/USD currency pair
- Empirical results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models (LLMs) in capturing the nuanced sentiment of forex-related news, achieving an out-of-sample accuracy of 84.33 %
- Future work could explore the transferability of FXFinBERT models: applying the model fine-tuned on EUR/USD to other currency pairs may yield promising performance, facilitating broader cross-market sentiment analysis
- We propose FXFinBERT, a computationally efficient model, designed for prediction in highly volatile forex markets through an rolling training mechanism that continuously adapts to market semantics evolution


## Summary

### Introduction
The paper discusses the importance of accurately forecasting exchange rate fluctuations, which is crucial for corporations, investors, and government institutions.
The foreign exchange market is complex, influenced by various factors, and requires multivariate models to capture information from multiple sources.

### Sentiment Analysis
The incorporation of sentiment as a predictor of exchange rate movements has been of interest to the academic community.
The paper argues that current sentiment analysis tools are not effective in capturing the sentiment contained in foreign exchange news, and a model specifically adapted to the characteristics of each currency pair is required.
A fine-tuned FinBERT model is proposed, which achieves an out-of-sample accuracy of 84.33% and outperforms traditional sentiment tools and state-of-the-art large language models.
The study used a fine-tuned version of FinBERT, called FXFinBERT, to classify news headlines from Investing.com as Positive, Negative, or Neutral.
The model was fine-tuned using a rolling approach, where the model was trained on seven years of data and then used to classify news for the next year.
This process was repeated for each year from 2016 to 2023.
The sentiment indices derived from the classified news were then used as predictors in the exchange rate forecasting model.
Sentiment classification results were obtained for all years using the FXFinBERT models, and daily sentiment indices were constructed for further analysis.
The results reveal that the model effectively identifies sentences containing information about a bearish USD or bullish EUR as "Positive," and conversely, sentences indicating a bullish USD or bearish EUR as "Negative." A dual-axis plot demonstrates that news sentiment has predictive power for changes in exchange rates.
The study proposes a novel sentiment analysis model, FXFinBERT, tailored specifically for the EUR/USD currency pair.
The results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models in capturing nuanced sentiment in forex-related news.
The constructed sentiment indices exhibit significant predictive power for exchange rate movements across multiple time horizons.

### Forecasting
The paper demonstrates that the developed sentiment indices exert a statistically significant influence on exchange rate movements and enhance the forecasting performance of LSTM models and other machine learning methods.
The inclusion of sentiment indices consistently improves predictive accuracy, providing novel empirical support for sentiment-driven theories in the foreign exchange market.

### Methodology
The study consists of three core modules: sentiment construction based on forex news, exchange rate forecasting using various machine learning methods, and performance evaluation and interpretation.
Sentiment construction utilizes the Term Frequency-Inverse Document Frequency (TF-IDF) model, FinBERT, and Large Language Models (LLMs) such as GPT-4.
The TF-IDF model is used as a baseline for sentiment analysis, while FinBERT is fine-tuned on a custom dataset to develop a sentiment analysis model specifically tailored for the foreign exchange market.
LLMs serve as a comparison against the fine-tuned FinBERT.

### Forecasting Models
The study employs various machine learning models for exchange rate forecasting, including Doubly Debiased Machine Learning (DDML), Long Short-Term Memory (LSTM) networks, and other baseline models such as Support Vector Regression (SVR), Random Forest (RFR), and Gradient Boosting (GBR).
The DDML method is used to evaluate the impact of sentiment indices on future exchange rate changes, while LSTM networks are used to model complex sequences with long-range temporal dependencies.

### Evaluation And Interpretation
The study uses five loss functions to evaluate the performance of each model, including Mean Absolute Error (MAE), Mean Squared Error (MSE), Mean Squared Logarithmic Error (MSLE), Mean Absolute Percentage Error (MAPE), and Logarithm of the Hyperbolic Cosine Loss (LogCosh).
The Diebold-Mariano test is used to evaluate the statistical significance of the difference in predictive accuracy between two forecasting models, while permutation feature importance is used to evaluate the importance of the sentiment index in the model.

### Macroeconomic Indicators
The study selected 20 commonly used macroeconomic indicators for exchange rate forecasting, including indicators from equity markets, commodity markets, bond markets, and inflation dynamics.
The indicators from equity markets include the S&amp;P 500 Index, NASDAQ Composite Index, Euronext 100 Index, and EURO STOXX 50 Index.
The commodity markets indicators include gold, West Texas Intermediate crude oil futures, and Bitcoin.
The bond markets indicators include the 13-week Treasury Bill Yield, 5-year Treasury Yield, and 30-year Treasury Yield.
The inflation dynamics indicators include the year-over-year and month-over-month changes in the U.S Consumer Price Index and the Eurozone CPI.

### Empirical Study
The empirical study consisted of three core components: training FXFinBERT and constructing sentiment indices, conducting in-sample analysis, and performing out-of-sample prediction.
The study used Doubly Debiased Machine Learning (DDML) for in-sample analysis and compared the predictive performance of various models, including FXFinBERT, TF-IDF, GPT-4, and others.
The results showed that incorporating sentiment indices improved the predictive performance of the models, and FXFinBERT outperformed other sentiment analysis methods.

### Model Performance
The best performance was observed with FXFinBERTEURUSD-2022, fine-tuned on data from 2015 to 2021, achieving an F1 score of 0.8981 in the fifth epoch.
Fine-tuning consistently improved model performance, surpassing that of proprietary large language models.
The "Positive" and "Negative" classes achieved classification accuracies of 80% and 81%, respectively.
Macro-averaged Accuracy, Recall, and F1 scores improved substantially, reaching 84.86%, 84.34%, and 84.60%, respectively.

### Predictive Power
The average treatment effects (ATE) of the untreated Daily Sentiment Scores on future exchange rate changes were calculated, and the results show that negative sentiment tends to trigger stronger and more prolonged reactions in financial markets.
The Adjusted Sentiment Scale (AdSSt) demonstrates particularly strong predictive effects, with ATEs reaching up to 100 basis points over shorter horizons.
The predictive power of sentiment indices is further evaluated using various models, including neural network, ensemble learning, and machine learning models, and the results show that the addition of sentiment indices improves predictive accuracy.

### Models
The study compares the performance of various machine learning models, including KNR, ENR, SVR, LGBR, RFR, GBR, and LSTM, in predicting exchange rate fluctuations.
The results show that the LSTM model with sentiment indices demonstrates good predictive ability at turning points of exchange rate fluctuations.
Ensemble learning models, such as LGBR, RFR, and GBR, show a high degree of overlap and tend to amplify the volatility of one-step predictions.

### Predictive Performance
The study evaluates the predictive performance of various models with and without sentiment indices.
The results show that incorporating sentiment indices improves the predictive performance of all models, with the LSTM model showing the most significant improvement.
The study also conducts robustness tests, including the DM test, feature importance rankings, and comparisons across sentiment analysis methods, to validate the findings.

### Market Indicators
The text tracks various market indicators, including S&amp;P 500 option price volatility, broad basket of commodities returns, and U.S Treasury yields.
It also captures Eurozone government bond yields, with specific focus on 2-year, 5-year, and 30-year yields.

### Inflation Rates
The text measures inflation rates in the U.S and Eurozone, with both annual and monthly rates based on CPI.
This includes the difference between the 3-Month LIBOR and the 3-Month Treasury Bill Secondary Market Rate.

### Data And Models
The text mentions various technical indicators and models, including Forex/FX, LLM, LSTM, DDML, RNNs, and others, with coefficient of variation (CV) values provided.
It also references data availability and a prompt for classifying sentiment related to the EUR/USD exchange rate.


## Study subjects

### 20 commonly used macroeconomic indicators
- Empirical Evidence for TheoryOut-of-sample PredictionLSTM vs. ML Methods With Senti-Index vs. Without DM Test Permutation Importance Analysis FXFinBERT Senti vs. Other Methods LSTM vs. its variants Interval Prediction3.2. ==Macroeconomic indicators as predictorsWe selected 20 commonly used macroeconomic indicators for exchange rate forecasting, taking into account the availability of daily data==. A detailed list of these indicators is presented in Table 11, and is briefly described below.The first set of predictors relates to the equity markets in the Eurozone and the United States

### 100 largest companies
- For the U.S stock market, we use the S&amp;P 500 Index (GSPC) and the NASDAQ Composite Index (IXIC). ==For the European stock market, we include the Euronext 100 Index (N100), which reflects the performance of the 100 largest companies listed on the Euronext exchange, and the EURO STOXX 50 Index (STOXX50E), a blue-chip index tracking the 50 largest companies in the Eurozone==. Macro P.a)    Macro R.b)    Macro F.c)    Balanced Acc.d)NoFT-FinBERT TF-IDF GPT-4 Claude-sonnet Qwen-plus GLM-4-plusNote: a) The macro-averaged Precision: The average precision score calculated across all classes.b) The macro-averaged Recall: The average recall score calculated across all classes. c) The macro-averaged F-score: The harmonic mean of macro-averaged precision and macro-averaged recall.d) Balanced Accuracy: The average of recall for each class, providing a measure that accounts for class imbalance.4

## Data analysis
- #method/adjusted_sentiment_scale
- #method/linear_models
- #method/svm_model
- #method/composite_index
- #method/garch_model
- #method/pearson_correlation
- #method/finbert_model
- #method/arima_model
- #method/boruta_algorithm

## Findings
- <mark class="claim">Our empirical findings offer several key insights. (1) The fine-tuned FinBERT models exhibit strong capability in identifying forex-specific <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a>, achieving an out-of-sample accuracy of 84.33 %, and outperforming traditional <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> tools as well as four state-of-the-art <a class="keyword" href="https://en.wikipedia.org/wiki/Large_Language_Models" title="large language models">large language models</a>. <mark class="claim">(2) Using a doubly debiased machine learning framework, <mark class="fact">we show that the developed sentiment indices exert a</mark> statistically significant influence on exchange rate movements</mark>. (3) Compared with benchmark predictors—including technical indicators and macroeconomic variables—the inclusion of sentiment indices consistently enhances the forecasting performance of LSTM models, their variants, and a range of machine learning methods</mark>
- (1) The fine-tuned FinBERT models exhibit strong capability in identifying forex-specific <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a>, achieving an out-of-sample accuracy of 84.33 %, and outperforming traditional <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> tools as well as four state-of-the-art <a class="keyword" href="https://en.wikipedia.org/wiki/Large_Language_Models" title="large language models">large language models</a>
- Compared to existing approaches—including zero-shot FinBERT, <a class="keyword" href="#" title="Term Frequency-Inverse Document Frequency">TF-IDF</a>, and proprietary <a class="keyword" href="https://en.wikipedia.org/wiki/Large_Language_Models" title="Large Language Models">LLMs</a> such as GPT-4, Claude-3.5-sonnet, Qwen-plus, and GLM4—FXFinBERT achieves SOTA accuracy (84.33 %) and macro F1-score (84.60 %). 3
- <mark class="claim"><mark class="fact">Subsection 4.4 begins with a comparison showing that incorporating our constructed sentiment indices improves the predictive performance of various models</mark> (detailed in Section 4.4.1)</mark>
- The "Positive" and "Negative" classes achieved classification accuracies of 80 % and 81 %, respectively
- Ensemble learning models all show an improvement of around 10 % after incorporating <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> indices (taking <a class="keyword" href="#" title="Mean Squared Error">MSE</a> as an example)
- <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="Sentiment">Sentiment</a> indices followed in importance, and once <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> score indices or <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> change&amp;continuity indices were permuted, the model's error increased by an average of 8 % or 10 %
- <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="Sentiment">Sentiment</a> features showed substantial impact ablating change&amp;continuity indices increased <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> by 11.2 % (p &lt; 0.001), while score indices removal led to 7.3 % performance drop (p &lt; 0.001)
- <mark class="fact">Empirical results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models</mark> (<a class="keyword" href="https://en.wikipedia.org/wiki/Large_Language_Models" title="Large Language Models">LLMs</a>) in capturing the nuanced <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> of forex-related news, achieving an out-of-sample accuracy of 84.33 %
- When <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> indices are permuted during the prediction phase or removed during the training phase, <mark class="fact">the model's MAE increases by 10 %</mark> and 11 %, respectively

##  Builds on previous research
- For traditional machine learning, we employ Support Vector (SVR), Random Forest (RFR), Gradient Boosting (GBR), LightGBM (LGBM), Elastic Net (ENR), and K-Nearest Neighbors (KNR). ==For LSTM variants, we consider CNN-LSTM== [^11], Bidirectional LSTM (BiLSTM) [^41], and Gated Recurrent Units (GRU) [^42].

##  Confirmation of earlier findings
- This result reinforces the theoretical argument that refined sentiment measures—capturing nuanced information through advanced processing methods—are critical for modeling sentiment-driven exchange rate movements [^22],[^64],[^65],[^66]. Section 4.3.1 ==align with and provide empirical validation for the theoretical mechanisms proposed in prior literature regarding the influence of news sentiment on exchange rates== [^24],[^59],[^60].
- Economic theory suggests that negative sentiment tends to trigger stronger and more prolonged reactions in financial markets due to risk aversion and flight-to-safety behaviors [^59],[^61],[^62],[^63]. ==Our results, as shown in Table 5, confirm this phenomenon==: the Average Treatment Effects (ATEs) of negative sentiment scores (St,negative) are consistently larger and more persistent across longer forecast horizons compared to positive sentiment scores (St,positive).

## Contributions
- In conclusion, <mark class="claim"><mark class="fact">we developed a robust framework for annually updating FXFinBERT to handle the unique</mark> and dynamic challenges of forex-related sentiment analysis</mark>. This framework also establishes a solid foundation for future research in similar fields.

## Limitations
- The study notes that several limitations remain, offering opportunities for future research. Future work could explore the transferability of FXFinBERT models to other currency pairs.

## Future work
- Future work could explore the transferability of FXFinBERT models to other currency pairs. The study also suggests that future work could examine the extent to which sentiment indicators can improve existing forecasting methods on a marginal basis.
- The study suggests that future work could explore the transferability of FXFinBERT models to other currency pairs. The study also suggests that future work could leverage advanced large language model techniques to enhance classification performance.


## References
[^1]: I.D. Raheem, Global financial cycles and exchange rate forecast: a factor analysis, Borsa Istanb. Rev. 20 (2020) S81–S92, https://doi.org/10.1016/j.bir.2020.06.002.  [OA](https://doi.org/10.1016/j.bir.2020.06.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.bir.2020.06.002)

[^2]: C. Engel, K.D. West, Exchange rates and fundamentals, J. Polit. Econ. 113 (2005) 485–517, https://doi.org/10.1086/429137.  [OA](https://doi.org/10.1086/429137)  [Scite](/scite_tallies?query=https://doi.org/10.1086/429137)

[^3]: C. Evans, K. Pappas, F. Xhafa, Utilizing artificial neural networks and genetic algorithms to build an algo-trading model for intra-day foreign exchange speculation, Math. Comput. Model 58 (2013) 1249–1266, https://doi.org/10.1016/j.mcm.2013.02.002.  [OA](https://doi.org/10.1016/j.mcm.2013.02.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.mcm.2013.02.002)

[^4]: B. Rossi, Exchange rate predictability, J. Econ. Lit. 51 (2013) 1063–1119, https://doi.org/10.1257/jel.51.4.1063.  [OA](https://doi.org/10.1257/jel.51.4.1063)  [Scite](/scite_tallies?query=https://doi.org/10.1257/jel.51.4.1063)

[^5]: C. Alexander, E. Lazar, Normal mixture GARCH(1,1): applications to exchange rate modelling, J. Appl. Econ. 21 (2006) 307–336, https://doi.org/10.1002/jae.849.  [OA](https://doi.org/10.1002/jae.849)  [Scite](/scite_tallies?query=https://doi.org/10.1002/jae.849)

[^6]: J.F. Torres, D. Hadjout, A. Sebaa, F. Martínez-Alvarez, A. Troncoso, Deep Learning for time series forecasting: a survey, Big Data 9 (2021) 3–21, https://doi.org/10.1089/big.2020.0159.  [OA](https://doi.org/10.1089/big.2020.0159)  [Scite](/scite_tallies?query=https://doi.org/10.1089/big.2020.0159)

[^7]: J. Henríquez, W. Kristjanpoller, A combined independent component analysis–neural network model for forecasting exchange rate variation, Appl. Soft Comput. 83 (2019) 105654, https://doi.org/10.1016/j.asoc.2019.105654.  [OA](https://doi.org/10.1016/j.asoc.2019.105654)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asoc.2019.105654)

[^8]: Y. Lu, B. Sheng, G. Fu, R. Luo, G. Chen, Y. Huang, Prophet-EEMD-LSTM based method for predicting energy consumption in the paint workshop, Appl. Soft Comput. 143 (2023) 110447, https://doi.org/10.1016/j.asoc.2023.110447.  [OA](https://doi.org/10.1016/j.asoc.2023.110447)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asoc.2023.110447)

[^9]: S. Ray, A. Lama, P. Mishra, T. Biswas, S. Sankar Das, B. Gurung, An ARIMA-LSTM model for predicting volatile agricultural price series with random forest technique, Appl. Soft Comput. 149 (2023) 110939, https://doi.org/10.1016/j.asoc.2023.110939.  [OA](https://doi.org/10.1016/j.asoc.2023.110939)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asoc.2023.110939)

[^10]: J. Wang, X. Wang, J. Li, H. Wang, A prediction model of CNN-TLSTM for USD/CNY exchange rate prediction, IEEE Access 9 (2021) 73346–73354, https://doi.org/10.1109/ACCESS.2021.3080459.  [OA](https://doi.org/10.1109/ACCESS.2021.3080459)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2021.3080459)

[^11]: P. Liu, Z. Wang, D. Liu, J. Wang, T. Wang, A CNN-STLSTM-AM model for forecasting USD/RMB exchange rate, J. Eng. Res. 11 (2023) 100079, https://doi.org/10.1016/j.jer.2023.100079.  [OA](https://doi.org/10.1016/j.jer.2023.100079)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jer.2023.100079)

[^12]: P.-H. Hsu, M.P. Taylor, Z. Wang, Technical trading: Is it still beating the foreign exchange market? J. Int. Econ. 102 (2016) 188–208, https://doi.org/10.1016/j.jinteco.2016.03.012.  [OA](https://doi.org/10.1016/j.jinteco.2016.03.012)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jinteco.2016.03.012)

[^13]: N. Zarrabi, S. Snaith, J. Coakley, FX technical trading rules can be profitable sometimes!, Int. Rev. Financ. Anal. 49 (2017) 113–127, https://doi.org/10.1016/j.irfa.2016.12.010.  [OA](https://doi.org/10.1016/j.irfa.2016.12.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.irfa.2016.12.010)

[^14]: E. Panopoulou, I. Souropanis, The role of technical indicators in exchange rate forecasting, J. Empir. Financ. 53 (2019) 197–221, https://doi.org/10.1016/j.jempfin.2019.07.004.  [OA](https://doi.org/10.1016/j.jempfin.2019.07.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jempfin.2019.07.004)

[^15]: S. Alonso-Monsalve, A.L. Suarez-Cetrulo, A. Cervantes, D. Quintana, Convolution on neural networks for high-frequency trend prediction of cryptocurrency exchange rates using technical indicators, Expert Syst. Appl. 149 (2020) 113250, https://doi.org/10.1016/j.eswa.2020.113250.  [OA](https://doi.org/10.1016/j.eswa.2020.113250)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2020.113250)

[^16]: A. Almeida, C. Goodhart, R. Payne, The effects of macroeconomic news on high frequency exchange rate behavior, J. Financ. Quant. Anal. 33 (1998) 383–408, https://doi.org/10.2307/2331101.  [OA](https://doi.org/10.2307/2331101)  [Scite](/scite_tallies?query=https://doi.org/10.2307/2331101)

[^17]: D. Rime, L. Sarno, E. Sojli, Exchange rate forecasting, order flow and macroeconomic information, J. Int. Econ. 80 (2010) 72–88, https://doi.org/10.1016/j.jinteco.2009.03.005.  [OA](https://doi.org/10.1016/j.jinteco.2009.03.005)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jinteco.2009.03.005)

[^18]: A.K. Alexandridis, E. Panopoulou, I. Souropanis, Forecasting exchange rate volatility: an amalgamation approach, J. Int. Financ. Mark. Inst. Money 97 (2024) 102067, https://doi.org/10.1016/j.intfin.2024.102067.  [OA](https://doi.org/10.1016/j.intfin.2024.102067)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.intfin.2024.102067)

[^19]: L. Liu, S. Tan, Y. Wang, Can commodity prices forecast exchange rates? Energy Econ. 87 (2020) 104719 https://doi.org/10.1016/j.eneco.2020.104719.  [OA](https://doi.org/10.1016/j.eneco.2020.104719)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eneco.2020.104719)

[^20]: B.N. Iyke, D.H.B. Phan, P.K. Narayan, Exchange rate return predictability in times of geopolitical risk, Int. Rev. Financ. Anal. 81 (2022) 102099, https://doi.org/10.1016/j.irfa.2022.102099.  [OA](https://doi.org/10.1016/j.irfa.2022.102099)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.irfa.2022.102099)

[^21]: J. Kearns, P. Manners, The impact of monetary policy on the exchange rate: a study using intraday data, Int. J. Cent. Bank 2 (2006). 〈https://ideas.repec.org//a/ijc/ijcj ou/y2006q4a6.html〉 (accessed December 18, 2024).  [OA](https://ideas.repec.org//a/ijc/ijcj)  [Scite](/scite_tallies?query=author%3AKearns%2Ctitle%3AThe%20impact%20of%20monetary%20policy%20on%20the%20exchange%20rate%3A%20a%20study%20using%20intraday%20data%2Cyear%3A2006)

[^22]: A. Khadjeh Nassirtoussi, S. Aghabozorgi, T. Ying Wah, D.C.L. Ngo, Text mining of news-headlines for FOREX market prediction: a multi-layer dimension reduction algorithm with semantics and sentiment, Expert Syst. Appl. 42 (2015) 306–324, https://doi.org/10.1016/j.eswa.2014.08.004.  [OA](https://doi.org/10.1016/j.eswa.2014.08.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2014.08.004)

[^23]: M. Mussa, Empirical regularities in the behavior of exchange rates and theories of the foreign exchange market, Carne Rochester Conf. Ser. Public Policy 11 (1979) 9–57, https://doi.org/10.1016/0167-2231(79)90034-4.  [OA](https://doi.org/10.1016/0167-2231(79)90034-4)  [Scite](/scite_tallies?query=https://doi.org/10.1016/0167-2231(79)90034-4)

[^24]: J.A. Frenkel, Flexible exchange rates, prices, and the role of “news”: lessons from the 1970s, J. Polit. Econ. 89 (1981) 665–705, https://doi.org/10.1086/260998.  [OA](https://doi.org/10.1086/260998)  [Scite](/scite_tallies?query=https://doi.org/10.1086/260998)

[^25]: S. Heiden, C. Klein, B. Zwergel, Beyond fundamentals: investor sentiment and exchange rate forecasting, Eur. Financ. Manag 19 (2013) 558–578, https://doi.org/10.1111/j.1468-036X.2010.00593.x.  [OA](https://doi.org/10.1111/j.1468-036X.2010.00593.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1468-036X.2010.00593.x)

[^26]: V. Plakandaras, T. Papadimitriou, P. Gogas, K. Diamantaras, Market sentiment and exchange rate directional forecasting, Algorithm Financ. 4 (2015) 69–79, https://doi.org/10.3233/AF-150044.  [OA](https://doi.org/10.3233/AF-150044)  [Scite](/scite_tallies?query=https://doi.org/10.3233/AF-150044)

[^27]: T. Skrinjaric, Z.L. Golubic, Z. Orlovic, Empirical analysis of dynamic spillovers between exchange rate return, return volatility and investor sentiment, Stud. Econ. Financ. 38 (2020) 86–113, https://doi.org/10.1108/SEF-07-2020-0247.  [OA](https://doi.org/10.1108/SEF-07-2020-0247)  [Scite](/scite_tallies?query=https://doi.org/10.1108/SEF-07-2020-0247)

[^28]: H. Naderi Semiromi, S. Lessmann, W. Peters, News will tell: forecasting foreign exchange rates based on news story events in the economy calendar, North Am. J. Econ. Financ. 52 (2020) 101181, https://doi.org/10.1016/j.najef.2020.101181.  [OA](https://doi.org/10.1016/j.najef.2020.101181)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2020.101181)

[^29]: Y. Li, H. Bu, J. Li, J. Wu, The role of text-extracted investor sentiment in Chinese stock price prediction with the enhancement of deep learning, Int. J. Forecast 36 (2020) 1541–1562, https://doi.org/10.1016/j.ijforecast.2020.05.001.  [OA](https://doi.org/10.1016/j.ijforecast.2020.05.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ijforecast.2020.05.001)

[^30]: X. Li, W. Shang, S. Wang, Text-based crude oil price forecasting: a deep learning approach, Int. J. Forecast 35 (2019) 1548–1560, https://doi.org/10.1016/j.ijforecast.2018.07.006.  [OA](https://doi.org/10.1016/j.ijforecast.2018.07.006)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ijforecast.2018.07.006)

[^31]: S. Sohangir, D. Wang, A. Pomeranets, T.M. Khoshgoftaar, Big data: deep learning for financial sentiment analysis, J. Big Data 5 (2018) 3, https://doi.org/10.1186/s40537-017-0111-6.  [OA](https://doi.org/10.1186/s40537-017-0111-6)  [Scite](/scite_tallies?query=https://doi.org/10.1186/s40537-017-0111-6)

[^32]: M.G. Sousa, K. Sakiyama, L. de, S. Rodrigues, P.H. Moraes, E.R. Fernandes, E. T. Matsubara, BERT for stock market sentiment analysis, IEEE 31st Int. Conf. Tools Artif. Intell. ICTAI 2019 (2019) 1597–1601, https://doi.org/10.1109/ ICTAI.2019.00231.  [OA](https://doi.org/10.1109/ICTAI.2019.00231)  [Scite](/scite_tallies?query=author%3ASousa%2Ctitle%3ABERT%20for%20stock%20market%20sentiment%20analysis%2Cyear%3A2019)

[^33]: D. Araci, 2019, FinBERT: Financial Sentiment Analysis with Pre-trained Language Models. 10.48550/arXiv.1908.10063.  [OA](https://doi.org/10.48550/arXiv.1908.10063)  [Scite](/scite_tallies?query=https://doi.org/10.48550/arXiv.1908.10063)

[^34]: A.H. Huang, H. Wang, Y. Yang, FinBERT: a large language model for extracting information from financial text, Contemp. Account. Res. 40 (2023) 806–841, https://doi.org/10.1111/1911-3846.12832.  [OA](https://doi.org/10.1111/1911-3846.12832)  [Scite](/scite_tallies?query=https://doi.org/10.1111/1911-3846.12832)

[^35]: J. Li, H.-J. Ahn, Sensitivity of Chinese stock markets to individual investor sentiment: an analysis of Sina Weibo mood related to COVID-19, J. Behav. Exp. Financ. 41 (2024) 100860, https://doi.org/10.1016/j.jbef.2023.100860.  [OA](https://doi.org/10.1016/j.jbef.2023.100860)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbef.2023.100860)

[^36]: H. Liang, J. Wu, H. Zhang, J. Yang, Two-stage short-term power load forecasting based on RFECV feature selection algorithm and a TCN–ECA–LSTM neural network, Energies 16 (2023) 1925, https://doi.org/10.3390/en16041925.  [OA](https://doi.org/10.3390/en16041925)  [Scite](/scite_tallies?query=https://doi.org/10.3390/en16041925)

[^37]: C. Wang, Z. Xiao, J. Wu, Functional connectivity-based classification of autism and control using SVM-RFECV on rs-fMRI data, Phys. Med. 65 (2019) 99–105, https://doi.org/10.1016/j.ejmp.2019.08.010.  [OA](https://doi.org/10.1016/j.ejmp.2019.08.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ejmp.2019.08.010)

[^38]: M.B. Kursa, A. Jankowski, W.R. Rudnicki, Boruta A system for feature selection, Fundam. Inform. 101 (2010) 271–285, https://doi.org/10.3233/FI-2010-288.  [OA](https://doi.org/10.3233/FI-2010-288)  [Scite](/scite_tallies?query=https://doi.org/10.3233/FI-2010-288)

[^39]: Y. Bengio, P. Simard, P. Frasconi, Learning long-term dependencies with gradient descent is difficult, IEEE Trans. Neural Netw. 5 (1994) 157–166, https://doi.org/10.1109/72.279181.  [OA](https://doi.org/10.1109/72.279181)  [Scite](/scite_tallies?query=https://doi.org/10.1109/72.279181)

[^40]: S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Comput. 9 (1997) 1735–1780, https://doi.org/10.1162/neco.1997.9.8.1735.  [OA](https://doi.org/10.1162/neco.1997.9.8.1735)  [Scite](/scite_tallies?query=https://doi.org/10.1162/neco.1997.9.8.1735)

[^41]: S. Liu, Q. Huang, M. Li, Y. Wei, A new LASSO-BiLSTM-based ensemble learning approach for exchange rate forecasting, Eng. Appl. Artif. Intell. 127 (2024) 107305, https://doi.org/10.1016/j.engappai.2023.107305.  [OA](https://doi.org/10.1016/j.engappai.2023.107305)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.engappai.2023.107305)

[^42]: M.S. Islam, E. Hossain, Foreign exchange currency rate prediction using a GRULSTM hybrid network, Soft Comput. Lett. 3 (2021) 100009, https://doi.org/10.1016/j.socl.2020.100009.  [OA](https://doi.org/10.1016/j.socl.2020.100009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.socl.2020.100009)

[^43]: F.X. Diebold, R.S. Mariano, Comparing predictive accuracy, J. Bus. Econ. Stat. 20 (2002) 134–144, https://doi.org/10.1198/073500102753410444.  [OA](https://doi.org/10.1198/073500102753410444)  [Scite](/scite_tallies?query=https://doi.org/10.1198/073500102753410444)

[^44]: L. Breiman, Random forests, Mach. Learn 45 (2001) 5–32, https://doi.org/10.1023/A:1010933404324.  [OA](https://doi.org/10.1023/A:1010933404324)  [Scite](/scite_tallies?query=https://doi.org/10.1023/A:1010933404324)

[^45]: A. Fisher, C. Rudin, F. Dominici, All models are wrong, but many are useful: learning a variable’s importance by studying an entire class of prediction models simultaneously, J. Mach. Learn. Res. 20 (2019) 1–81.  [OA](https://engine.scholarcy.com/oa_version?query=Fisher%2C%20A.%20Rudin%2C%20C.%20Dominici%2C%20F.%20All%20models%20are%20wrong%2C%20but%20many%20are%20useful%3A%20learning%20a%20variable%E2%80%99s%20importance%20by%20studying%20an%20entire%20class%20of%20prediction%20models%20simultaneously%202019&author=Fisher&title=All%20models%20are%20wrong%2C%20but%20many%20are%20useful%3A%20learning%20a%20variable%E2%80%99s%20importance%20by%20studying%20an%20entire%20class%20of%20prediction%20models%20simultaneously&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Fisher%2C%20A.%20Rudin%2C%20C.%20Dominici%2C%20F.%20All%20models%20are%20wrong%2C%20but%20many%20are%20useful%3A%20learning%20a%20variable%E2%80%99s%20importance%20by%20studying%20an%20entire%20class%20of%20prediction%20models%20simultaneously%202019) [Scite](/scite_tallies?query=author%3AFisher%2Ctitle%3AAll%20models%20are%20wrong%2C%20but%20many%20are%20useful%3A%20learning%20a%20variable%E2%80%99s%20importance%20by%20studying%20an%20entire%20class%20of%20prediction%20models%20simultaneously%2Cyear%3A2019)

[^46]: H. Qian, B. Wang, M. Yuan, S. Gao, Y. Song, Financial distress prediction using a corrected feature selection measure and gradient boosted decision tree, Expert Syst. Appl. 190 (2022) 116202, https://doi.org/10.1016/j.eswa.2021.116202.  [OA](https://doi.org/10.1016/j.eswa.2021.116202)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2021.116202)

[^47]: AssistProfDr.R. Nabi, S. Saeed, A. Abdi, Feature Eng. Stock Price Predict. 29 (2020) 2486–2496.  [OA](https://scholar.google.co.uk/scholar?q=AssistProfDrR%20Nabi%20S%20Saeed%20A%20Abdi%20Feature%20Eng%20Stock%20Price%20Predict%2029%202020%2024862496) [GScholar](https://scholar.google.co.uk/scholar?q=AssistProfDrR%20Nabi%20S%20Saeed%20A%20Abdi%20Feature%20Eng%20Stock%20Price%20Predict%2029%202020%2024862496) 

[^48]: A. Ntakaris, G. Mirone, J. Kanniainen, M. Gabbouj, A. Iosifidis, Feature engineering for mid-price prediction with deep learning, IEEE Access 7 (2019) 82390–82412, https://doi.org/10.1109/ACCESS.2019.2924353.  [OA](https://doi.org/10.1109/ACCESS.2019.2924353)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2019.2924353)

[^49]: J. Faust, J.H. Rogers, S.-Y.B. Wang, J.H. Wright, The high-frequency response of exchange rates and interest rates to macroeconomic announcements, J. Monet. Econ. 54 (2007) 1051–1068, https://doi.org/10.1016/j.jmoneco.2006.05.015.  [OA](https://doi.org/10.1016/j.jmoneco.2006.05.015)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jmoneco.2006.05.015)

[^50]: W. Wang, Z. Lin, B. Hu, Macro news effects on exchange rates: difference between carry trade target and safe-haven currencies, Financ. Res. Lett. 53 (2023) 103679, https://doi.org/10.1016/j.frl.2023.103679.  [OA](https://doi.org/10.1016/j.frl.2023.103679)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.frl.2023.103679)

[^51]: M. Agrawal, A. Khan, P. Shukla, Stock indices price prediction based on technical indicators using deep learning model, Int. J. Emerg. Technol. 10 (2019).  [OA](https://engine.scholarcy.com/oa_version?query=Agrawal%2C%20M.%20Khan%2C%20A.%20Shukla%2C%20P.%20Stock%20indices%20price%20prediction%20based%20on%20technical%20indicators%20using%20deep%20learning%20model%202019&author=Agrawal&title=Stock%20indices%20price%20prediction%20based%20on%20technical%20indicators%20using%20deep%20learning%20model&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Agrawal%2C%20M.%20Khan%2C%20A.%20Shukla%2C%20P.%20Stock%20indices%20price%20prediction%20based%20on%20technical%20indicators%20using%20deep%20learning%20model%202019) [Scite](/scite_tallies?query=author%3AAgrawal%2Ctitle%3AStock%20indices%20price%20prediction%20based%20on%20technical%20indicators%20using%20deep%20learning%20model%2Cyear%3A2019)

[^52]: Y. Gu, D. Yan, S. Yan, Z. Jiang, Price forecast with high-frequency finance data: an autoregressive recurrent neural network model with technical indicators. Proc. 29th ACM Int. Conf. Inf. Knowl. Manag, Association for Computing Machinery, New York, NY, USA, 2020, pp. 2485–2492, https://doi.org/10.1145/3340531.3412738.  [OA](https://doi.org/10.1145/3340531.3412738)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3340531.3412738)

[^53]: E. Andreou, M. Matsi, A. Savvides, Stock and foreign exchange market linkages in emerging economies, J. Int. Financ. Mark. Inst. Money 27 (2013) 248–268, https://doi.org/10.1016/j.intfin.2013.09.003.  [OA](https://doi.org/10.1016/j.intfin.2013.09.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.intfin.2013.09.003)

[^54]: G.-J. Wang, L. Wan, Y. Feng, C. Xie, G.S. Uddin, Y. Zhu, Interconnected multilayer networks: quantifying connectedness among global stock and foreign exchange markets, Int. Rev. Financ. Anal. 86 (2023) 102518, https://doi.org/10.1016/j.irfa.2023.102518.  [OA](https://doi.org/10.1016/j.irfa.2023.102518)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.irfa.2023.102518)

[^55]: Z. Liu, J. Hu, S. Zhang, Z. He, Risk spillovers among oil, gold, stock, and foreign exchange markets: evidence from G20 economies, North Am. J. Econ. Financ. 74 (2024) 102249, https://doi.org/10.1016/j.najef.2024.102249.  [OA](https://doi.org/10.1016/j.najef.2024.102249)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2024.102249)

[^56]: T.G. Andersen, T. Bollerslev, F.X. Diebold, P. Labys, Modeling and forecasting realized volatility, Econometrica 71 (2003) 579–625, https://doi.org/10.1111/1468-0262.00418.  [OA](https://doi.org/10.1111/1468-0262.00418)  [Scite](/scite_tallies?query=https://doi.org/10.1111/1468-0262.00418)

[^57]: D. Buncic, G.D. Piras, Heterogeneous agents, the financial crisis and exchange rate predictability, J. Int. Money Financ. 60 (2016) 313–359, https://doi.org/10.1016/j.jimonfin.2015.09.006.  [OA](https://doi.org/10.1016/j.jimonfin.2015.09.006)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jimonfin.2015.09.006)

[^58]: I. Tenney, J. Wexler, J. Bastings, T. Bolukbasi, A. Coenen, S. Gehrmann, E. Jiang, M. Pushkarna, C. Radebaugh, E. Reif, A. Yuan, 2020, The Language Interpretability Tool: Extensible, Interactive Visualizations and Analysis for NLP Models. 10.48550/arXiv.2008.05122.  [OA](https://doi.org/10.48550/arXiv.2008.05122)  [Scite](/scite_tallies?query=https://doi.org/10.48550/arXiv.2008.05122)

[^59]: T.G. Andersen, T. Bollerslev, F.X. Diebold, C. Vega, Micro effects of macro announcements: real-time price discovery in foreign exchange, Am. Econ. Rev. 93 (2003) 38–62, https://doi.org/10.1257/000282803321455151.  [OA](https://doi.org/10.1257/000282803321455151)  [Scite](/scite_tallies?query=https://doi.org/10.1257/000282803321455151)

[^60]: Y. Liu, I. Shaliastovich, Government policy approval and exchange rates, J. Financ. Econ. 143 (2022) 303–331, https://doi.org/10.1016/j.jfineco.2021.06.031.  [OA](https://doi.org/10.1016/j.jfineco.2021.06.031)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfineco.2021.06.031)

[^61]: S. Consoli, L.T. Pezzoli, E. Tosetti, Emotions in macroeconomic news and their impact on the European bond market, J. Int. Money Financ. 118 (2021) 102472, https://doi.org/10.1016/j.jimonfin.2021.102472.  [OA](https://doi.org/10.1016/j.jimonfin.2021.102472)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jimonfin.2021.102472)

[^62]: M. Baker, J. Wurgler, Investor sentiment and the cross-section of stock returns, J. Financ. 61 (2006) 1645–1680, https://doi.org/10.1111/j.15406261.2006.00885.x.  [OA](https://doi.org/10.1111/j.15406261.2006.00885.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2006.00885.x)

[^64]: P.C. Tetlock, Giving content to investor sentiment: the role of media in the stock market, J. Financ. 62 (2007) 1139–1168, https://doi.org/10.1111/j.15406261.2007.01232.x.  [OA](https://doi.org/10.1111/j.15406261.2007.01232.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2007.01232.x)

[^65]: L. Xueling, X. Xiong, S. Yucong, Exchange rate market trend prediction based on sentiment analysis, Comput. Electr. Eng. 111 (2023) 108901, https://doi.org/10.1016/j.compeleceng.2023.108901.  [OA](https://doi.org/10.1016/j.compeleceng.2023.108901)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.compeleceng.2023.108901)

[^66]: C.-I. Lee, C.-H. Chang, F.-N. Hwang, Currency exchange rate prediction with long short-term memory networks based on attention and news sentiment analysis, in: 2019 Int. Conf. Technol. Appl. Artificial Intell, TAAI, 2019, pp. 1–6, https://doi.org/10.1109/TAAI48200.2019.8959884.  [OA](https://doi.org/10.1109/TAAI48200.2019.8959884)  [Scite](/scite_tallies?query=https://doi.org/10.1109/TAAI48200.2019.8959884)

[^67]: H. Zhao, Z. Liu, Z. Wu, Y. Li, T. Yang, P. Shu, S. Xu, H. Dai, L. Zhao, H. Jiang, Y. Pan, J. Chen, Y. Zhou, G. Mai, N. Liu, T. Liu, 2024, Revolutionizing Finance with LLMs: An Overview of Applications and Insights. 10.48550/arXiv.2401.11641.  [OA](https://doi.org/10.48550/arXiv.2401.11641)  [Scite](/scite_tallies?query=https://doi.org/10.48550/arXiv.2401.11641)

[^68]: S. Duz Tan, O. Tas, Social media sentiment in international stock returns and trading activity, J. Behav. Financ. 22 (2021) 221–234, https://doi.org/10.1080/15427560.2020.1772261.  [OA](https://doi.org/10.1080/15427560.2020.1772261)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2020.1772261)

[^69]: X. Wan, J. Yang, S. Marinov, J.-P. Calliess, S. Zohren, X. Dong, Sentiment correlation in financial news networks and associated market movements, Sci. Rep. 11 (2021) 3062, https://doi.org/10.1038/s41598-021-82338-6.   [OA](https://doi.org/10.1038/s41598-021-82338-6)  [Scite](/scite_tallies?query=https://doi.org/10.1038/s41598-021-82338-6)

