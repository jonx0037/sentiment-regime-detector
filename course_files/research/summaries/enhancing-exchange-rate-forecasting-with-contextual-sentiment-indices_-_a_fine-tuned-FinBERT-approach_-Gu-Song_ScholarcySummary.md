[[Gu_EnhancingExchangeRateForecastingWith_2026]]

# [Enhancing exchange rate forecasting with contextual sentiment indices: A fine-tuned FinBERT approach](https://doi.org/10.1016/j.asoc.2026.114556)

## [[Guoqin Gu]]; [[Yuping Song]]

## Abstract

The incorporation of sentiment as a predictor of exchange rate movements has long been of interest to the academic community. This paper argues that, because currency fluctuations are relative and interdependent, the sentiment in foreign exchange news cannot be effectively captured by current sentiment analysis tools. Instead, it requires models tailored to each currency pair's characteristics. To address this gap, we take the EUR/USD pair as an example, construct a manually annotated news dataset, and fine-tune the FinBERT model on an annual rolling basis to produce a series of specialized sentiment classifiers. Based on these models, we develop contextual sentiment indices and incorporate them as predictors of exchange rate changes. Our empirical findings offer several key insights. (1) The fine-tuned FinBERT models exhibit strong capability in identifying forex-specific sentiment, achieving an out-of-sample accuracy of 84.33 %, and outperforming traditional sentiment tools as well as four state-of-the-art large language models. (2) Using a doubly debiased machine learning framework, we show that the developed sentiment indices exert a statistically significant influence on exchange rate movements. (3) Compared with benchmark predictors—including technical indicators and macroeconomic variables—the inclusion of sentiment indices consistently enhances the forecasting performance of LSTM models, their variants, and a range of machine learning methods. Overall, this study contributes to both sentiment analysis and exchange rate forecasting by providing a currency-pair-specific modeling framework and demonstrating that fine-tuned language models can materially improve predictive accuracy in financial applications.

## Key concepts

#sentiment_analysis; #long_short_term_memory; #average_treatment_effects; #claim/index; #index; #finding/sentiment; #sentiment; #finding/large_language_models; #large_language_models; #foreign_exchange

## Quote
>
> This study proposes a novel sentiment analysis model, FXFinBERT, tailored for the EUR/USD currency pair, which outperforms traditional sentiment analysis tools and state-of-the-art large language models in capturing the nuanced sentiment of forex-related news, achieving an out-of-sample accuracy of 84.33%.

## Key points

- As globalization progresses and international trade intensifies, accurately forecasting exchange rate fluctuations has become increasingly significant [^1]
- These include Mean Absolute Error (MAE), Mean Squared Error (MSE), Mean Squared Logarithmic Error (MSLE), Mean Absolute Percentage Error (MAPE), and Logarithm of the Hyperbolic Cosine Loss (LogCosh), each defined by the following formulas: 1 ∑n
- This study contributes to the literature on exchange rate forecasting by proposing a novel sentiment analysis model, FXFinBERT, tailored for the EUR/USD currency pair
- Empirical results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models (LLMs) in capturing the nuanced sentiment of forex-related news, achieving an out-of-sample accuracy of 84.33 %
- Future work could explore the transferability of FXFinBERT models: applying the model fine-tuned on EUR/USD to other currency pairs may yield promising performance, facilitating broader cross-market sentiment analysis
- We propose FXFinBERT, a computationally efficient model, designed for prediction in highly volatile forex markets through a rolling training mechanism that continuously adapts to market semantics evolution

## Summary

### Introduction

The paper discusses the importance of accurately forecasting exchange rate fluctuations, which is crucial for corporations, investors, and government institutions.
The foreign exchange market is complex, influenced by various factors, and requires multivariate models to capture information from multiple sources.

### Sentiment Analysis

The incorporation of sentiment as a predictor of exchange rate movements has attracted the attention of the academic community.
The paper argues that current sentiment analysis tools are ineffective at capturing sentiment in foreign exchange news and that a model tailored to each currency pair's characteristics is required.
A fine-tuned FinBERT model is proposed, achieving an out-of-sample accuracy of 84.33% and outperforming traditional sentiment tools and state-of-the-art large language models.
The study used a fine-tuned version of FinBERT, called FXFinBERT, to classify news headlines from Investing.com as Positive, Negative, or Neutral.
The model was fine-tuned using a rolling approach: it was trained on 7 years of data and then used to classify news for the next year.
This process was repeated for each year from 2016 to 2023.
The sentiment indices derived from the classified news were then used as predictors in the exchange rate forecasting model.
Sentiment classification results were obtained for all years using the FXFinBERT models, and daily sentiment indices were constructed for further analysis.
The results reveal that the model effectively identifies sentences containing information about a bearish USD or a bullish EUR as "Positive," and, conversely, sentences indicating a bullish USD or a bearish EUR as "Negative." A dual-axis plot demonstrates that news sentiment has predictive power for changes in exchange rates.
The study proposes a novel sentiment analysis model, FXFinBERT, tailored specifically for the EUR/USD currency pair.
The results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models in capturing nuanced sentiment in forex-related news.
The constructed sentiment indices exhibit significant predictive power for exchange rate movements across multiple time horizons.

### Forecasting

The paper demonstrates that the developed sentiment indices exert a statistically significant influence on exchange rate movements and enhance the forecasting performance of LSTM models and other machine learning methods.
The inclusion of sentiment indices consistently improves predictive accuracy, providing novel empirical support for sentiment-driven theories in the foreign exchange market.

### Methodology

The study consists of three core modules: sentiment construction based on forex news, exchange rate forecasting using various machine learning methods, and performance evaluation and interpretation.
Sentiment construction uses the Term Frequency-Inverse Document Frequency (TF-IDF) model, FinBERT, and large language models (LLMs) such as GPT-4.
The TF-IDF model serves as a baseline for sentiment analysis, while FinBERT is fine-tuned on a custom dataset to develop a sentiment analysis model tailored to the foreign exchange market.
LLMs serve as a comparison against the fine-tuned FinBERT.

### Forecasting Models

The study employs various machine learning models for exchange rate forecasting, including Doubly Debiased Machine Learning (DDML), Long Short-Term Memory (LSTM) networks, and other baseline models such as Support Vector Regression (SVR), Random Forest (RFR), and Gradient Boosting (GBR).
The DDML method is used to evaluate the impact of sentiment indices on future exchange rate changes, while LSTM networks are used to model complex sequences with long-range temporal dependencies.

### Evaluation And Interpretation

The study uses five loss functions to evaluate each model's performance, including Mean Absolute Error (MAE), Mean Squared Error (MSE), Mean Squared Logarithmic Error (MSLE), Mean Absolute Percentage Error (MAPE), and Logarithm of the Hyperbolic Cosine Loss (LogCosh).
The Diebold-Mariano test is used to assess the statistical significance of differences in predictive accuracy between two forecasting models, while permutation feature importance is used to assess the importance of the sentiment index in the model.

### Macroeconomic Indicators

The study selected 20 commonly used macroeconomic indicators for exchange rate forecasting, including indicators from equity, commodity, and bond markets, as well as inflation dynamics.
The indicators from equity markets include the S&P 500 Index, the NASDAQ Composite Index, the Euronext 100 Index, and the EURO STOXX 50 Index.
The commodity markets indicators include gold, West Texas Intermediate crude oil futures, and Bitcoin.
The bond market indicators include the 13-week Treasury Bill Yield, 5-year Treasury Yield, and 30-year Treasury Yield.
The inflation dynamics indicators include the year-over-year and month-over-month changes in the U.S Consumer Price Index and the Eurozone CPI.

### Empirical Study

The empirical study consisted of three core components: training FXFinBERT, constructing sentiment indices, and conducting in-sample analysis and out-of-sample prediction.
The study used Doubly Debiased Machine Learning (DDML) for in-sample analysis and compared the predictive performance of various models, including FXFinBERT, TF-IDF, GPT-4, and others.
The results showed that incorporating sentiment indices improved the predictive performance of the models, and FXFinBERT outperformed other sentiment analysis methods.

### Model Performance

The best performance was observed with FXFinBERTEURUSD-2022, fine-tuned on data from 2015 to 2021, achieving an F1 score of 0.8981 in the fifth epoch.
Fine-tuning consistently improved model performance, surpassing that of proprietary large language models.
The "Positive" and "Negative" classes achieved classification accuracies of 80% and 81%, respectively.
Macro-averaged Accuracy, Recall, and F1 scores improved substantially, reaching 84.86%, 84.34%, and 84.60%, respectively.

### Predictive Power

The average treatment effects (ATE) of the untreated Daily Sentiment Scores on future exchange rate changes were estimated, and the results indicate that negative sentiment tends to trigger stronger, more prolonged reactions in financial markets.
The Adjusted Sentiment Scale (AdSSt) demonstrates particularly strong predictive effects, with ATEs reaching up to 100 basis points over shorter horizons.
The predictive power of sentiment indices is further evaluated using neural networks, ensemble learning, and other machine learning methods, and the results show that their inclusion improves predictive accuracy.

### Models

The study compares the performance of various machine learning models, including KNR, ENR, SVR, LGBR, RFR, GBR, and LSTM, in predicting exchange rate fluctuations.
The results show that the LSTM model with sentiment indices demonstrates good predictive ability at turning points of exchange rate fluctuations.
Ensemble learning models, such as LGBR, RFR, and GBR, exhibit significant overlap and tend to amplify the volatility of one-step predictions.

### Predictive Performance

The study evaluates the predictive performance of various models with and without sentiment indices.
The results show that incorporating sentiment indices improves the predictive performance of all models, with the LSTM model showing the most significant improvement.
The study also conducts robustness tests, including the DM test, feature importance rankings, and comparisons across sentiment analysis methods, to validate the findings.

### Market Indicators

The text tracks various market indicators, including S&P 500 option price volatility, a broad basket of commodity returns, and U.S. Treasury yields.
It also captures Eurozone government bond yields, with a specific focus on 2-year, 5-year, and 30-year yields.

### Inflation Rates

The text measures inflation rates in the U.S and the Eurozone, with both annual and monthly rates based on CPI.
This includes the difference between the 3-Month LIBOR and the 3-Month Treasury Bill Secondary Market Rate.

### Data And Models

The text mentions various technical indicators and models, including Forex/FX, LLM, LSTM, DDML, RNNs, and others, and provides coefficient of variation (CV) values.
It also references data availability and a prompt for classifying sentiment related to the EUR/USD exchange rate.

## Study subjects

### 20 commonly used macroeconomic indicators

- Empirical Evidence for Theory: Out-of-sample Prediction, LSTM vs. ML Methods With Senti-Index vs. Without DM Test Permutation Importance Analysis, FXFinBERT Senti vs. Other Methods, LSTM vs. its variants, Interval Prediction3.2. Macroeconomic indicators as predictors. We selected 20 commonly used macroeconomic indicators for exchange rate forecasting, with daily data availability in mind. A detailed list of these indicators is presented in Table 11 and is briefly described below. The first set of predictors relates to the equity markets in the Eurozone and the United States

### 100 largest companies

- For the U.S stock market, we use the S&P 500 Index (GSPC) and the NASDAQ Composite Index (IXIC). For the European stock market, we include the Euronext 100 Index (N100), which tracks the performance of the 100 largest companies listed on the Euronext exchange, and the EURO STOXX 50 Index (STOXX50E), a blue-chip index that tracks the 50 largest companies in the Eurozone. Macro P.a)    Macro R.b)    Macro F.c)    Balanced Acc.d)NoFT-FinBERT TF-IDF GPT-4 Claude-sonnet Qwen-plus GLM-4-plusNote: a) The macro-averaged Precision: The average precision score calculated across all classes.b) The macro-averaged Recall: The average recall score calculated across all classes. c) The macro-averaged F-score: The harmonic mean of macro-averaged precision and macro-averaged recall.d) Balanced Accuracy: The average of recall for each class, providing a measure that accounts for class imbalance.4

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
- <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="Sentiment">Sentiment</a> indices followed in importance, and once <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> score indices or <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> change&amp; continuity indices were permuted, the model's error increased by an average of 8 % or 10 %
- <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="Sentiment">Sentiment</a> features showed substantial impact ablating change&amp; continuity indices increased <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> by 11.2 % (p &lt; 0.001), while score indices removal led to 7.3 % performance drop (p &lt; 0.001)
- <mark class="fact">Empirical results demonstrate that FXFinBERT outperforms traditional sentiment analysis tools and state-of-the-art large language models</mark> (<a class="keyword" href="https://en.wikipedia.org/wiki/Large_Language_Models" title="Large Language Models">LLMs</a>) in capturing the nuanced <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> of forex-related news, achieving an out-of-sample accuracy of 84.33 %
- When <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment" title="sentiment">sentiment</a> indices are permuted during the prediction phase or removed during the training phase, <mark class="fact">the model's MAE increases by 10 %</mark> and 11 %, respectively

##  Builds on previous research

- For traditional machine learning, we employ Support Vector (SVR), Random Forest (RFR), Gradient Boosting (GBR), LightGBM (LGBM), Elastic Net (ENR), and K-Nearest Neighbors (KNR). For LSTM variants, we consider CNN-LSTM [^11], Bidirectional LSTM (BiLSTM) [^41], and Gated Recurrent Units (GRU) [^42].

##  Confirmation of earlier findings

- This result reinforces the theoretical argument that refined sentiment measures—capturing nuanced information through advanced processing methods—are critical for modeling sentiment-driven exchange rate movements [^22],[^64],[^65],[^66]. Section 4.3.1 aligns with and provides empirical validation for the theoretical mechanisms proposed in prior literature regarding the influence of news sentiment on exchange rates [^24],[^59],[^60].
- Economic theory suggests that negative sentiment tends to trigger stronger and more prolonged reactions in financial markets due to risk aversion and flight-to-safety behaviors [^59],[^61],[^62],[^63]. Our results, as shown in Table 5, confirm this phenomenon: the Average Treatment Effects (ATEs) of negative sentiment scores (St, negative) are consistently larger and more persistent across longer forecast horizons than those of positive sentiment scores (St, positive).

## Contributions

- In conclusion, <mark class="claim"><mark class="fact">we developed a robust framework for annually updating FXFinBERT to handle the unique</mark> and dynamic challenges of forex-related sentiment analysis</mark>. This framework also establishes a solid foundation for future research in similar fields.

## Limitations

- The study notes that several limitations remain, offering opportunities for future research. Future work could explore the transferability of FXFinBERT models to other currency pairs.

## Future work

- Future work could explore the transferability of FXFinBERT models to other currency pairs. The study also suggests that future work could examine the extent to which sentiment indicators can improve existing forecasting methods incrementally.
- The study suggests that future work could explore the transferability of FXFinBERT models to other currency pairs. The study also suggests that future work could leverage advanced large-language model techniques to improve classification performance.

## References

[^1]: I.D. Raheem, Global financial cycles and exchange rate forecast: a factor analysis, Borsa Istanbul. Rev. 20 (2020) S81–S92, <https://doi.org/10.1016/j.bir.2020.06.002>.  [OA](https://doi.org/10.1016/j.bir.2020.06.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.bir.2020.06.002)

[^11]: P. Liu, Z. Wang, D. Liu, J. Wang, T. Wang, A CNN-STLSTM-AM model for forecasting USD/RMB exchange rate, J. Eng. Res. 11 (2023) 100079, <https://doi.org/10.1016/j.jer.2023.100079>.  [OA](https://doi.org/10.1016/j.jer.2023.100079)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jer.2023.100079)

[^22]: A. Khadjeh Nassirtoussi, S. Aghabozorgi, T. Ying Wah, D.C.L. Ngo, Text mining of news-headlines for FOREX market prediction: a multi-layer dimension reduction algorithm with semantics and sentiment, Expert Syst. Appl. 42 (2015) 306–324, <https://doi.org/10.1016/j.eswa.2014.08.004>.  [OA](https://doi.org/10.1016/j.eswa.2014.08.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2014.08.004)

[^24]: J.A. Frenkel, Flexible exchange rates, prices, and the role of “news”: lessons from the 1970s, J. Polit. Econ. 89 (1981) 665–705, <https://doi.org/10.1086/260998>.  [OA](https://doi.org/10.1086/260998)  [Scite](/scite_tallies?query=https://doi.org/10.1086/260998)

[^41]: S. Liu, Q. Huang, M. Li, Y. Wei, A new LASSO-BiLSTM-based ensemble learning approach for exchange rate forecasting, Eng. Appl. Artif. Intell. 127 (2024) 107305, <https://doi.org/10.1016/j.engappai.2023.107305>.  [OA](https://doi.org/10.1016/j.engappai.2023.107305)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.engappai.2023.107305)

[^42]: M.S. Islam, E. Hossain, Foreign exchange currency rate prediction using a GRULSTM hybrid network, Soft Comput. Lett. 3 (2021) 100009, <https://doi.org/10.1016/j.socl.2020.100009>.  [OA](https://doi.org/10.1016/j.socl.2020.100009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.socl.2020.100009)

[^59]: T.G. Andersen, T. Bollerslev, F.X. Diebold, C. Vega, Micro effects of macro announcements: real-time price discovery in foreign exchange, Am. Econ. Rev. 93 (2003) 38–62, <https://doi.org/10.1257/000282803321455151>.  [OA](https://doi.org/10.1257/000282803321455151)  [Scite](/scite_tallies?query=https://doi.org/10.1257/000282803321455151)

[^60]: Y. Liu, I. Shaliastovich, Government policy approval and exchange rates, J. Financ. Econ. 143 (2022) 303–331, <https://doi.org/10.1016/j.jfineco.2021.06.031>.  [OA](https://doi.org/10.1016/j.jfineco.2021.06.031)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfineco.2021.06.031)

[^61]: S. Consoli, L.T. Pezzoli, E. Tosetti, Emotions in macroeconomic news and their impact on the European bond market, J. Int. Money Financ. 118 (2021) 102472, <https://doi.org/10.1016/j.jimonfin.2021.102472>.  [OA](https://doi.org/10.1016/j.jimonfin.2021.102472)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jimonfin.2021.102472)

[^62]: M. Baker, J. Wurgler, Investor sentiment and the cross-section of stock returns, J. Financ. 61 (2006) 1645–1680, <https://doi.org/10.1111/j.15406261.2006.00885.x>.  [OA](https://doi.org/10.1111/j.15406261.2006.00885.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2006.00885.x)

[^64]: P.C. Tetlock, Giving content to investor sentiment: the role of media in the stock market, J. Financ. 62 (2007) 1139–1168, <https://doi.org/10.1111/j.15406261.2007.01232.x>.  [OA](https://doi.org/10.1111/j.15406261.2007.01232.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2007.01232.x)

[^65]: L. Xueling, X. Xiong, S. Yucong, Exchange rate market trend prediction based on sentiment analysis, Comput. Electr. Eng. 111 (2023) 108901, <https://doi.org/10.1016/j.compeleceng.2023.108901>.  [OA](https://doi.org/10.1016/j.compeleceng.2023.108901)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.compeleceng.2023.108901)

[^66]: C.-I. Lee, C.-H. Chang, F.-N. Hwang, Currency exchange rate prediction with long short-term memory networks based on attention and news sentiment analysis, in: 2019 Int. Conf. Technol. Appl. Artificial Intell, TAAI, 2019, pp. 1–6, <https://doi.org/10.1109/TAAI48200.2019.8959884>.  [OA](https://doi.org/10.1109/TAAI48200.2019.8959884)  [Scite](/scite_tallies?query=https://doi.org/10.1109/TAAI48200.2019.8959884)
