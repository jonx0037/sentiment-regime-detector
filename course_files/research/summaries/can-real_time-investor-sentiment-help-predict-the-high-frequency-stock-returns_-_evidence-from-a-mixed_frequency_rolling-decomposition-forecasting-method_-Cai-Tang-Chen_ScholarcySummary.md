[[Cai_et+al_RealtimeInvestorSentimentHelpPredict_2024]]

# [Can real-time investor sentiment help predict the high-frequency stock returns? Evidence from a mixed-frequency-rolling decomposition forecasting method](https://doi.org/10.1016/j.najef.2024.102147)

## [[Yi Cai]]; [[Zhenpeng Tang]]; [[Ying Chen]]

## Abstract

This research examines the predictive effect of real-time investor sentiment on high-frequency stock returns. Utilizing text sentiment analysis, we extract investor sentiment with a half-hour frequency from the stock message board. The RR-MIDAS method is used to model half-hourly sentiment and three-minute stock returns. Economic analysis reveals that investor sentiment significantly affects stock returns across seven high-frequency periods, with this influence gradually weakening. Subsequently, we propose the “MF-EEMD-ML” prediction system, which introduces a rolling decomposition algorithm into the RR-MIDAS framework to predict high-frequency trend items, combined with real-time forum sentiment. The results, using rolling EMD decomposition for comparison, show that the “MF-EEMD-ML” system achieves a maximum reduction of 19.18 % in MAE, 19.08 % in RMSE, 11.71 % in SMAPE, and a maximum improvement of 16.66 % in DS. Additionally, the Diebold-Mariano (DM) tests show that the “MF-EEMD-ML” prediction system significantly outperforms both the “MF-EMD-ML” system and the LR model.

## Key concepts

# linear_regression; #mean_squared_error; #finding/symmetric_mean_absolute_percentage_error; #symmetric_mean_absolute_percentage_error; #finding/root_mean_square_error; #root_mean_square_error; #finding/empirical_mode_decomposition; #empirical_mode_decomposition; #finding/mean_absolute_percentage_error; #mean_absolute_percentage_error

## Quote

This study proposes a "Mixed-Frequency-Rolling Decomposition-Forecasting" framework that uses the EMD algorithm for decomposition and machine learning for forecasting stock returns and finds that the framework performs well across four error metrics but has limited success in passing the Diebold-Mariano tests.

## Key points

- The Efficient Market Hypothesis (EMH) holds that asset prices have incorporated all historical information in a weak-form efficient market, so predicting stock price trends solely based on historical data is unfeasible
- In the predictions for the second sub-series, the MF-Empirical Mode Decomposition (EMD)-Long Short-Term Memory (LSTM) model’s Symmetric Mean Absolute Percentage Error (SMAPE) indicator has decreased by 35.25 %, and the Directional precision of Statistics (DS) indicator for the MF-EMD-Support Vector Regression (SVR) model has improved by 41.13 %
- [^Lv_et+al_2022_a]) forecast stock trends in six markets, showing that the CEEMDAN-DAE-Recurrent Neural Network (RNN) model improves by 7.44 %, 6.25 %, and 19.66 % in Root Mean Square Error (RMSE), Mean Absolute Error (MAE), and NMSE indicators compared to the benchmark model
- This paper explores the significant influence of real-time investor sentiment from stock message boards on high-frequency stock returns
- Compared to the “MF-EMD-ML” prediction framework, the “MF-Ensemble Empirical Mode Decomposition (EEMD)-ML” system achieves a maximum reduction of 19.18 % in MAE, 19.08 % in RMSE, 11.71 % in SMAPE, and a maximum improvement of 16.66 % in DS
- DM test results show that the “MF-EEMD-ML” system passes the significance test compared to the linear regression (LR) model and against the “MF-EMDML” framework

## Summary

### Introduction To Research

The research examines the predictive effect of real-time investor sentiment on high-frequency stock returns, utilizing text sentiment analysis to extract investor sentiment from a stock message board.
The study aims to explore whether real-time sentiment from stock message boards can improve stock return prediction and develop a specialized model for heightened accuracy.

### Methodology And Results

The study employs the RR-MIDAS method to model half-hourly sentiment and three-minute stock returns, revealing that investor sentiment significantly affects stock returns during seven high-frequency periods.
The "MF-EEMD-ML" prediction system is proposed, introducing a rolling decomposition algorithm into the RR-MIDAS framework to predict high-frequency trend items, combined with real-time forum sentiment.
The results show that the "MF-EEMD-ML" system achieves a maximum reduction of 19.18% in MAE, 19.08% in RMSE, 11.71% in SMAPE, and a maximum improvement of 16.66% in DS.

### Predictive Models And Sentiment Analysis

The study uses six machine learning algorithms—SVR, RF, XGBoost, LSTM, CNN, and ANN—to evaluate the effectiveness of the EEMD decomposition algorithm.
The results of the Diebold-Mariano tests demonstrate that the "MF-EEMD-ML" prediction system significantly outperforms both the "MF-EMD-ML" system and the LR model.
The study also discusses the dynamic changes in the impact of real-time social media sentiments on high-frequency stock returns, highlighting the importance of rolling decomposition and a one-step-ahead prediction approach in predictive research.

### Methodology

The study uses data mining techniques to gather posts from stock message boards and to obtain an investor sentiment indicator through manual labeling and automatic sentiment scoring with SnowNLP.
The text-based sentiment index captures investor sentiment more effectively than survey-based and proxy-variable methods.
The study focuses on the dynamic impact of intraday high-frequency investor sentiment on the stock market, extracting sentiment from message boards at half-hourly intervals.
The study employs a range of methodologies, including the RR-MIDAS model, EMD and EEMD algorithms, and machine learning algorithms such as LSTM, GRU, and SVR.
The study also uses a non-linear least-squares (NLS) approach and calculates fuzzy entropy and Pearson correlation coefficients.
The results are presented in various tables and figures, including Table 4, Fig. 5, and Fig. 11, which illustrate the coefficient variations, fuzzy entropy values, and predictive outcomes of the proposed framework.
The study introduces a "Mixed-Frequency-Rolling Decomposition-Forecasting" framework to improve the accuracy of high-frequency stock returns predictions.
The framework uses a reverse mixed-frequency data sampling approach, dividing the 3-minute frequency stock return sequence into 10 subsequences.
Each subsequence undergoes a "rolling decomposition - one-step-ahead prediction" process, and predictions are made by combining the high-frequency component with half-hourly sentiment from stock message boards.

### Modeling

The study uses the RR-MIDAS model to establish a relationship between half-hourly investor sentiment and 3-minute stock returns.
The RR-MIDAS results show a significant impact of half-hourly sentiment on 3-minute stock returns during seven high-frequency periods.
The study then constructs a forecasting model that integrates the rolling EEMD decomposition into the RR-MIDAS model to address the nonstationarity and nonlinearity of stock returns.

### Results

The study applies the "MF-EEMD-ML" technique to each subseries of 3-minute stock returns, combining high-frequency components with half-hourly investor sentiment for prediction using machine learning algorithms.
The study evaluates predictive performance using RMSE, MAE, SMAPE, and DS indicators, and performs the Diebold-Mariano test to assess the robustness of the findings.
The results show that the "MF-EEMD-ML" system achieves the maximum reductions of 19.18% in MAE, 19.08% in RMSE, and 11.71% in SMAPE, and a maximum improvement of 16.66% in DS compared to the "MF-EMD-ML" prediction framework.
The Diebold-Mariano (DM) tests conducted on these prediction outcomes meet the significance threshold, indicating that the proposed "MF-EEMD-ML" prediction system effectively enhances the accuracy of high-frequency stock returns predictions.

### Data Analysis

The study analyzes the dynamic impact of half-hourly frequency sentiment on subsequent 3-minute frequency stock returns using the RR-MIDAS model.
The results show that half-hourly sentiment significantly impacts future 3-minute stock returns in seven high-frequency periods.
The coefficient variations of αh indicate that even the lagged periods of the high-frequency returns series struggle to produce significant effects, except during the h = 8 period.
The study also uses the EEMD algorithm to decompose the original stock return sequence into distinct-frequency modal components.

### Forecasting Results

The study evaluates the predictive outcomes of the proposed "Mixed-Frequency-Rolling Decomposition-Forecasting" framework, which utilizes the EMD and EEMD algorithms for decomposition.
The results show that the "MF-EEMD-ML" system outperforms the "MF-EMD-ML" framework across most metrics.
The study also conducts Diebold-Mariano (DM) tests to validate the effectiveness of the proposed framework, and the results indicate significant improvements over the LR model in several instances.

### Implications

The study contributes to the understanding of the timeliness and complexity of information structures in the stock market for investors and regulatory authorities.
The results suggest that investors should discern the authenticity of internet information and avoid being easily swayed by extreme sentiments on forums.
Regulatory authorities can incorporate various social media platforms into the scope of information supervision and use the proposed model to monitor real-time forum sentiment, mitigating the adverse effects of excessive market downturns.

## Study subjects

### 1068183 valid posts

- The main cleaning criteria involve: (1) removing posts with only images or advertisements; (2) deleting blank posts; (3) eliminating reposts from other financial forums; (4) excluding posts about news, institutional research reports, and company announcements. After cleaning, we obtain 1,068,183 valid posts, spanning from January 16, 2020, to November 18, 2022, within the trading hours of 9:30–11:30 and 13:00–15:00. In Section 2.4, during the “MF-EEMD-ML” predictive modeling process, we face the challenge of computational burden due to rolling window decomposition and machine learning techniques

### 5 research students

- The lower portion of Fig. 1 illustrates this sentiment classification process. We randomly select 20,000 posts for manual labeling by five research students experienced in the stock market. Posts are labeled as “1′′ for positive, ”0′′ for negative, and ambiguous posts are later labeled by the advisor

## Data analysis

- #method/emd_algorithm
- #method/reverse_unrestricted_mixed_data_sampling_model
- #method/eemd_algorithm
- #method/eemd_method
- #method/diebold_mariano_test
- #method/pearson_correlation_coefficients

## Findings

- The results, using rolling <a class="keyword" href="https://en.wikipedia.org/wiki/Empirical_mode_decomposition" title="Empirical Mode Decomposition">EMD</a> decomposition for comparison, show that the “MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-ML” <mark class="fact">system achieves a maximum reduction of 19.18 % in MAE</mark>, 19.08 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a>, 11.71 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Symmetric_Mean_Absolute_Percentage_Error" title="Symmetric Mean Absolute Percentage Error">SMAPE</a>, and a maximum improvement of 16.66 % in <a class="keyword" href="#" title="Directional precision of Statistics">DS</a>
- Examination results of 1000 out-of-sample comments indicate that method (2) performs best, achieving an accuracy of 83 %
- [^Shi_et+al_2019_a]) combine text vector representation and SVM algorithm to train manually labeled forum posts, achieving an accuracy of 76 %
- [^Yin_et+al_2022_a]) supplement multiple sources of sentiment lexicons and use a model consistent with our study, achieving a classification accuracy of 86 %
- Significant enhancements are seen in the tenth sub-series predictions: the <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> indicator for the MF-<a class="keyword" href="https://en.wikipedia.org/wiki/Empirical_mode_decomposition" title="Empirical Mode Decomposition">EMD</a>-<a class="keyword" href="#" title="Convolutional Neural Network">CNN</a> model has been reduced by 17.21 %, and the <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a> indicator for the MF-<a class="keyword" href="https://en.wikipedia.org/wiki/Empirical_mode_decomposition" title="Empirical Mode Decomposition">EMD</a>-<a class="keyword" href="#" title="Gated Recurrent Unit">GRU</a> model has decreased by 22.52 %
- <mark class="claim">In the predictions for the second sub-series, <mark class="fact">the MF-EMD-LSTM model’s SMAPE indicator has decreased by 35.25 %</mark>, and <mark class="fact">the DS indicator for the MF-EMD-SVR model has improved by 41.13 %</mark></mark>
- <mark class="claim">In the first prediction task, the MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-<a class="keyword" href="#" title="Convolutional Neural Network">CNN</a> model achieves a 27.80 % improvement in <a class="keyword" href="#" title="Mean Absolute Error">MAE</a>, a 23.68 % improvement in <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a>, a 14.33 % improvement in <a class="keyword" href="https://en.wikipedia.org/wiki/Symmetric_Mean_Absolute_Percentage_Error" title="Symmetric Mean Absolute Percentage Error">SMAPE</a>, and <mark class="fact">a 13.12 % enhancement in DS compared to the MF-EMD-XGB model</mark></mark>
- Statistical analysis reveals the most notable improvements as follows: In the prediction of the first stock return subsequence, MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-<a class="keyword" href="#" title="Gated Recurrent Unit">GRU</a> achieves a 19.18 % reduction in the <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> metric, and MF-EEMDXGB sees an 11.71 % decrease in the <a class="keyword" href="https://en.wikipedia.org/wiki/Symmetric_Mean_Absolute_Percentage_Error" title="Symmetric Mean Absolute Percentage Error">SMAPE</a> metric
- For the seventh subsequence, MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-<a class="keyword" href="#" title="Gated Recurrent Unit">GRU</a> demonstrates a 19.08 % reduction in the <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a> metric
- In the ninth prediction task, MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-<a class="keyword" href="#" title="Long Short-Term Memory">LSTM</a> shows a 16.66 % increase in the <a class="keyword" href="#" title="Directional precision of Statistics">DS</a> metric
- In similar studies, [^Lv_et+al_2022_a]) forecast stock trends in six markets, showing <mark class="fact">that the CEEMDAN-DAE-RNN model improves by 7.44 %</mark>, 6.25 %, and 19.66 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a>, <a class="keyword" href="#" title="Mean Absolute Error">MAE</a>, and <mark class="fact">NMSE indicators compared to the benchmark model</mark>
- [^Park_et+al_2022_a]), when predicting returns for S&amp;P500, SSE Composite Index, and KOSPI200, observe that <a class="keyword" href="#" title="Long Short-Term Memory">LSTM</a>-Forest with multi-task (<a class="keyword" href="#" title="LSTM-Forest with multi-task">LFM</a>) exhibits <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a> values 25.53 %, 22.75 %, and 16.29 % lower than the benchmark <a class="keyword" href="#" title="Random Forest">RF</a> model
- In our research, the “MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-ML” system surpasses the “MF-<a class="keyword" href="https://en.wikipedia.org/wiki/Empirical_mode_decomposition" title="Empirical Mode Decomposition">EMD</a>-ML” system, with the maximum improvement reaching 19.08 %, 19.18 %, and 11.71 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a>, <a class="keyword" href="#" title="Mean Absolute Error">MAE</a>, and <a class="keyword" href="https://en.wikipedia.org/wiki/Symmetric_Mean_Absolute_Percentage_Error" title="Symmetric Mean Absolute Percentage Error">SMAPE</a> indicators
- Compared to the “MF-<a class="keyword" href="https://en.wikipedia.org/wiki/Empirical_mode_decomposition" title="Empirical Mode Decomposition">EMD</a>-ML” prediction framework, the “MF-<a class="keyword" href="#" title="Ensemble Empirical Mode Decomposition">EEMD</a>-ML” <mark class="fact">system achieves a maximum reduction of 19.18 % in MAE</mark>, 19.08 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Root_mean_square_error" title="Root Mean Square Error">RMSE</a>, 11.71 % in <a class="keyword" href="https://en.wikipedia.org/wiki/Symmetric_Mean_Absolute_Percentage_Error" title="Symmetric Mean Absolute Percentage Error">SMAPE</a>, and a maximum improvement of 16.66 % in <a class="keyword" href="#" title="Directional precision of Statistics">DS</a>

## Builds on previous research

- Experimental results demonstrate a significant enhancement in predictive accuracy with the introduction of the decomposition algorithm. In similar studies ([^Lv_et+al_2022_a]), forecast stock trends in six markets, showing that the CEEMDAN-DAE-RNN model improves RMSE, MAE, and NMSE by 7.44 %, 6.25 %, and 19.66 %, respectively, compared to the benchmark model. [^Park_et+al_2022_a]), when predicting returns for S&P 500, SSE Composite Index, and KOSPI200, observe that LSTM-Forest with multi-task (LFM) exhibits RMSE values 25.53 %, 22.75 %, and 16.29 % lower than the benchmark RF model.

## Confirmation of earlier findings

- We experiment with three algorithms: (1) Text vectorization using Word2Vec and BiLSTM training; (2) Sentiment analysis using the SnowNLP Bayesian machine learning algorithm; (3) Sentiment analysis using BaiduNLP. Examination results of 1000 out-of-sample comments indicate that method (2) performs best, achieving an accuracy of 83 %. [^Shi_et+al_2019_a]) combine text vector representation and SVM algorithm to train manually labeled forum posts, achieving an accuracy of 76 %. [^Yin_et+al_2022_a]) supplement multiple sentiment lexicons and use a model consistent with our study, achieving a classification accuracy of 86%.

## Contributions

- In summary, although we incorporated half-hourly investor sentiment from stock message boards in this section, the unsatisfactory predictive performance of the reverse mixed-frequency model was likely due to the inherent high noise and clustered volatility in the stock returns sequence. The predictive outcomes for the second to tenth subsequences of stock returns, which underwent mixed-frequency periodic treatment, showed patterns similar to those of the first subsequence, leading the six algorithms to underperform the LR model. Therefore, Fig. 10 and Table 6 only display the predictive outcomes for the first sub-series of stock returns in the undecomposed framework, while the results for the remaining nine sub-series are available upon request.

## Limitations

- The study notes that the adoption of the rolling decomposition algorithm is currently limited in the field of predictive research, and that the study's results may be affected by the quality of the sentiment analysis and the selection of the stock message board.
- The study acknowledges the limitations of using message board sentiment, including the potential for noise and bias in the data, and the need for further research to improve the accuracy of sentiment analysis.
- The limitations of the study are that the proposed framework has limited success in passing the Diebold-Mariano tests and that the study only evaluates the effectiveness of the framework using a limited number of machine learning algorithms and decomposition techniques.
- The study has several limitations, including not considering the economic impact and predictive effects of overnight sentiment on stock returns. The study also notes that posts issued after the market closes at 15:00 and until the opening at 9:30 the next day are considered night posts, with a larger time span and more dispersed, and cannot be concentrated.

## Future work

- The study suggests that future research could explore the application of the "MF-EEMD-ML" prediction system to other financial markets and assets, and that further research is needed to improve the accuracy and robustness of the system.
- The future work of the study includes further validation of the proposed framework using additional machine learning algorithms and decomposition techniques, and evaluation of the framework's performance in different market conditions.
- The study suggests that future research can extend the modeling in this paper to explore the predictive effects of overnight sentiment on stock returns for the next day, as well as the predictive effects of midday sentiment on afternoon stock returns.

## References

[^Lv_et+al_2022_a]: Lv, P., Shu, Y., Xu, J., &amp; Wu, Q. (2022). Modal decomposition-based hybrid model for stock index prediction[J]. Expert Systems with Applications, 202, Article 117252. <https://doi.org/10.1016/j.eswa.2022.117252>  [OA](https://doi.org/10.1016/j.eswa.2022.117252)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2022.117252)

[^Park_et+al_2022_a]: Park, H. J., Kim, Y., &; Kim, H. Y. (2022). Stock market forecasting using a multi-task approach integrating long short-term memory and the random forest framework  [OA](https://scholar.google.co.uk/scholar?q=Park%2C%20H.J.%20Kim%2C%20Y.%20Kim%2C%20H.Y.%20Stock%20market%20forecasting%20using%20a%20multi-task%20approach%20integrating%20long%20short-term%20memory%20and%20the%20random%20forest%20framework%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Park%2C%20H.J.%20Kim%2C%20Y.%20Kim%2C%20H.Y.%20Stock%20market%20forecasting%20using%20a%20multi-task%20approach%20integrating%20long%20short-term%20memory%20and%20the%20random%20forest%20framework%202022)

[^Shi_et+al_2019_a]: Shi, Y., Tang, Y., &; Long, W. (2019). Sentiment contagion analysis of interacting investors: evidence from China’s stock forum[J]. Physica A: Statistical Mechanics and its Applications, 523, 246–259. <https://doi.org/10.1016/j.physa.2019.02.025>  [OA](https://doi.org/10.1016/j.physa.2019.02.025)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.physa.2019.02.025)

[^Yin_et+al_2022_a]: Yin, H., Wu, X., &amp; Kong, S. X. (2022). Daily investor sentiment, order flow imbalance, and stock liquidity: evidence from the Chinese stock market[J]. International Journal of Finance &amp; Economics, 2022, 27(4): 4816-4836. <https://doi.org/10.1002/ijfe.2402>.  [OA](https://doi.org/10.1002/ijfe.2402)  [Scite](/scite_tallies?query=https://doi.org/10.1002/ijfe.2402)
