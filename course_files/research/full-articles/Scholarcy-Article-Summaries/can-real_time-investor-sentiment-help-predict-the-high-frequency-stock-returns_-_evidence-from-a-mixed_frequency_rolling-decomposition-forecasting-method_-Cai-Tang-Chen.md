[[Cai_et+al_RealtimeInvestorSentimentHelpPredict_2024]]

# [Can real-time investor sentiment help predict the high-frequency stock returns? Evidence from a mixed-frequency-rolling decomposition forecasting method](https://doi.org/10.1016/j.najef.2024.102147)

## [[Yi Cai]]; [[Zhenpeng Tang]]; [[Ying Chen]]

## Abstract
This research examines the predictive effect of real-time investor sentiment on high-frequency stock returns. Utilizing text sentiment analysis, we extract investor sentiment with a half-hour frequency from the stock message board. The RR-MIDAS method is used to model half-hourly sentiment and three-minute stock returns, and economic analysis reveals that investor sentiment significantly affects the stock returns during seven high-frequency periods, and the influence gradually weakens. Subsequently, we propose the “MF-EEMD-ML” prediction system, which introduces a rolling decomposition algorithm into the RR-MIDAS framework for predicting highfrequency trend items combined with real-time forum sentiment. The results, using rolling EMD decomposition for comparison, show that the “MF-EEMD-ML” system achieves a maximum reduction of 19.18 % in MAE, 19.08 % in RMSE, 11.71 % in SMAPE, and a maximum improvement of 16.66 % in DS. Additionally, the outcomes of the Diebold-Mariano (DM) tests also demonstrate that the “MF-EEMD-ML” prediction system significantly outperforms both the “MF-EMD-ML” system and the LR model.

## Key concepts
#linear_regression; #mean_squared_error; #finding/symmetric_mean_absolute_percentage_error; #symmetric_mean_absolute_percentage_error; #finding/root_mean_square_error; #root_mean_square_error; #finding/empirical_mode_decomposition; #empirical_mode_decomposition; #finding/mean_absolute_percentage_error; #mean_absolute_percentage_error

## Quote
> This study proposes a "Mixed-Frequency-Rolling Decomposition-Forecasting" framework that utilizes the EMD algorithm for decomposition and machine learning algorithms for forecasting stock returns, and finds that the framework performs well on four types of error metrics but has limited success in passing the Diebold-Mariano tests.

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
The "MF-EEMD-ML" prediction system is proposed, introducing a rolling decomposition algorithm into the RR-MIDAS framework for predicting high-frequency trend items combined with real-time forum sentiment.
The results show that the "MF-EEMD-ML" system achieves a maximum reduction of 19.18% in MAE, 19.08% in RMSE, 11.71% in SMAPE, and a maximum improvement of 16.66% in DS.

### Predictive Models And Sentiment Analysis
The study uses six machine learning algorithms—SVR, RF, XGBoost, LSTM, CNN, and ANN—to evaluate the effectiveness of the EEMD decomposition algorithm.
The results of the Diebold-Mariano tests demonstrate that the "MF-EEMD-ML" prediction system significantly outperforms both the "MF-EMD-ML" system and the LR model.
The study also discusses the dynamic changes in the impact of real-time social media sentiments on high-frequency stock returns, highlighting the importance of rolling decomposition and one-step-ahead prediction approach in predictive research.

### Methodology
The study utilizes data mining techniques to gather posts from stock message boards and obtain an investor sentiment indicator through manual labeling and automatic sentiment scoring using SnowNLP analysis.
The text-based sentiment index captures investor sentiments more effectively than survey-based and proxy variable methods.
The study focuses on the dynamic impact of intraday high-frequency investor sentiment on the stock market, extracting sentiment from message boards at half-hourly intervals.
The study employs a range of methodologies, including the RR-MIDAS model, EMD and EEMD algorithms, and machine learning algorithms such as LSTM, GRU, and SVR.
The study also uses a non-linear least squares estimation (NLS) approach and calculates fuzzy entropy and Pearson correlation coefficients.
The results are presented in various tables and figures, including Table 4, Fig. 5, and Fig. 11, which illustrate the coefficient variations, fuzzy entropy values, and predictive outcomes of the proposed framework.
The study introduces a "Mixed-Frequency-Rolling Decomposition-Forecasting" framework to improve the accuracy of high-frequency stock returns predictions.
The framework utilizes a reverse mixed-frequency data sampling approach, dividing the 3-minute frequency stock returns sequence into ten subsequences.
Each subsequence undergoes a "rolling decomposition - one-step-ahead prediction" process, and predictions are made by combining the high-frequency component with half-hourly sentiment from stock message boards.

### Modeling
The study uses the RR-MIDAS model to establish a relationship between half-hourly investor sentiment and 3-minute stock returns.
The RR-MIDAS results show a significant impact of half-hourly sentiment on 3-minute stock returns during seven high-frequency periods.
The study then constructs a forecasting model, integrating the rolling EEMD decomposition algorithm into the RR-MIDAS model to address the non-stationary and nonlinear nature of stock returns.

### Results
The study applies the "MF-EEMD-ML" technique to each subseries of 3-minute stock returns, combining high-frequency components with half-hourly investor sentiment for prediction using machine learning algorithms.
The study evaluates the predictive performance using RMSE, MAE, SMAPE, and DS indicators and performs the Diebold-Mariano test to confirm the robustness of the findings.
The results show that the "MF-EEMD-ML" system achieves a maximum reduction of 19.18% in MAE, 19.08% in RMSE, 11.71% in SMAPE, and a maximum improvement of 16.66% in DS compared to the "MF-EMD-ML" prediction framework.
The Diebold-Mariano (DM) tests conducted on these prediction outcomes meet the significance threshold, indicating that the proposed "MF-EEMD-ML" prediction system effectively enhances the accuracy of high-frequency stock returns predictions.

### Data Analysis
The study analyzes the dynamic impact of half-hourly frequency sentiment on subsequent 3-minute frequency stock returns using the RR-MIDAS model.
The results show that half-hourly sentiment significantly impacts future 3-minute stock returns in seven high-frequency periods.
The coefficient variations of αh indicate that even the lagged periods of the high-frequency returns series struggle to produce significant effects, except during the h = 8 period.
The study also uses the EEMD algorithm to decompose the original stock returns sequence into various modal components of distinct frequencies.

### Forecasting Results
The study evaluates the predictive outcomes of the proposed "Mixed-Frequency-Rolling Decomposition-Forecasting" framework, which utilizes the EMD and EEMD algorithms for decomposition.
The results show that the "MF-EEMD-ML" system exhibits improvements over the "MF-EMD-ML" framework in most metrics.
The study also conducts Diebold-Mariano (DM) tests to validate the effectiveness of the proposed framework, and the results indicate that significant improvements over the LR model can be observed in several instances.

### Implications
The study contributes to the understanding of the timeliness and complexity of information structures in the stock market for investors and regulatory authorities.
The results suggest that investors should discern the authenticity of internet information and avoid being easily swayed by extreme sentiments on forums.
Regulatory authorities can incorporate various social media platforms into the scope of information supervision and use the proposed model to monitor forum sentiments in real-time, mitigating the adverse effects of excessive market downturns.


## Study subjects

### 1068183 valid posts
- The main cleaning criteria involve: (1) removing posts with only images or advertisements; (2) deleting blank posts; (3) eliminating reposts from other financial forums; (4) excluding posts about news, institutional research reports, and company announcements. ==After cleaning, we obtain 1,068,183 valid posts, spanning from January 16, 2020, to November 18, 2022, within the trading hours of 9:30–11:30 and 13:00–15:00==. In Section 2.4, during the “MF-EEMD-ML” predictive modeling process, we face the challenge of computational burden due to rolling window decomposition and machine learning techniques

### 5 research students
- The lower portion of Fig. 1 illustrates this sentiment classification process. ==We randomly select 20,000 posts for manual labeling by five research students experienced in the stock market==. Posts are labeled as “1′′ for positive, ”0′′ for negative, and ambiguous posts are later labeled by the advisor

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

##  Builds on previous research
- Experimental results demonstrate a significant enhancement in predictive accuracy with the introduction of the decomposition algorithm. ==In similar studies,== [^Lv_et+al_2022_a]) forecast stock trends in six markets, showing that the CEEMDAN-DAE-RNN model improves by 7.44 %, 6.25 %, and 19.66 % in RMSE, MAE, and NMSE indicators compared to the benchmark model. [^Park_et+al_2022_a]), when predicting returns for S&amp;P500, SSE Composite Index, and KOSPI200, observe that LSTM-Forest with multi-task (LFM) exhibits RMSE values 25.53 %, 22.75 %, and 16.29 % lower than the benchmark RF model.

##  Confirmation of earlier findings
- We experiment with three algorithms: (1) Text vectorization using Word2Vec and BiLSTM training; (2) Sentiment analysis using the SnowNLP Bayesian machine learning algorithm; (3) Sentiment analysis using BaiduNLP. Examination results of 1000 out-of-sample comments indicate that method (2) performs best, achieving an accuracy of 83 %. [^Shi_et+al_2019_a]) combine text vector representation and SVM algorithm to train manually labeled forum posts, achieving an accuracy of 76 %. [^Yin_et+al_2022_a]) supplement multiple sources of sentiment lexicons and use a model ==consistent with our study, achieving a classification accuracy of 86 %==.

## Contributions
- In summary, although we incorporated half-hourly investor sentiment from stock message boards in this section, the unsatisfactory predictive performance of the reverse mixed-frequency model was likely due to the inherent high noise and clustered volatility in the stock returns sequence. The predictive outcomes for the second to tenth subsequences of stock returns, which underwent mixedfrequency periodic treatment, showed patterns similar to the first subsequence, leading the six algorithms to underperform compared to the LR model. Therefore, Fig. 10 and Table 6 only display the predictive outcomes for the first sub-series of stock returns in the undecomposed framework, while the results for the remaining nine sub-series are available upon request.

## Limitations
- The study notes that the adoption of the rolling decomposition algorithm is currently limited in the field of predictive research, and that the study's results may be affected by the quality of the sentiment analysis and the selection of the stock message board.
- The study acknowledges the limitations of using message board sentiment, including the potential for noise and bias in the data, and the need for further research to improve the accuracy of sentiment analysis.
- The limitations of the study are that the proposed framework has limited success in passing the Diebold-Mariano tests, and that the study only evaluates the effectiveness of the framework using a limited number of machine learning algorithms and decomposition techniques.
- The study has several limitations, including not considering the economic impact and predictive effects of overnight sentiment on stock returns. The study also notes that the posts issued after the market closes at 15:00 until the opening at 9:30 the next day are considered night posts, with a larger time span, and these posts are more dispersed and cannot be concentrated.

## Future work
- The study suggests that future research could explore the application of the "MF-EEMD-ML" prediction system to other financial markets and assets, and that further research is needed to improve the accuracy and robustness of the system.
- The future work of the study includes further validation of the proposed framework using additional machine learning algorithms and decomposition techniques, and evaluation of the framework's performance in different market conditions.
- The study suggests that future research can extend the modeling in this paper to explore the predictive effects of overnight sentiment on stock returns for the next day, as well as the predictive effects of midday sentiment on afternoon stock returns.


## References
[^Agoraki_et+al_2022_a]: Agoraki, M. E. K., Aslanidis, N., &amp; Kouretas, G. P. (2022). US banks’ lending, financial stability, and text-based sentiment analysis. Journal of Economic Behavior &amp; Organization, 197, 73–90. https://doi.org/10.1016/j.jebo.2022.02.025  [OA](https://doi.org/10.1016/j.jebo.2022.02.025)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jebo.2022.02.025)

[^Allen_et+al_2019_a]: Allen, D. E., McAleer, M., &amp; Singh, A. K. (2019). Daily market news sentiment and stock prices. Applied Economics, 51(30), 3212–3235. https://doi.org/10.1080/00036846.2018.1564115  [OA](https://doi.org/10.1080/00036846.2018.1564115)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2018.1564115)

[^Antoniou_et+al_2016_a]: Antoniou, C., Doukas, J. A., &amp; Subrahmanyam, A. (2016). Investor sentiment, beta, and the cost of equity capital. Management Science, 62(2), 347–367. https://doi.org/10.1287/mnsc.2014.2101  [OA](https://doi.org/10.1287/mnsc.2014.2101)  [Scite](/scite_tallies?query=https://doi.org/10.1287/mnsc.2014.2101)

[^Ashtiani_2023_a]: Ashtiani, M. N., &amp; Raahmei, B. (2023). News-based intelligent prediction of financial markets using text mining and machine learning: A systematic literature review. Expert Systems with Applications., Article 119509. https://doi.org/10.1016/j.eswa.2023.119509  [OA](https://doi.org/10.1016/j.eswa.2023.119509)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2023.119509)

[^Baker_2006_a]: Baker, M., &amp; Wurgler, J. (2006). Investor sentiment and the cross-section of stock returns. The Journal of Finance, 61(4), 1645–1680. https://doi.org/10.1111/j.15406261.2006.00885.x  [OA](https://doi.org/10.1111/j.15406261.2006.00885.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2006.00885.x)

[^Bartov_et+al_2018_a]: Bartov, E., Faurel, L., &amp; Mohanram, P. S. (2018). Can twitter help predict firm-level earnings and stock returns? The Accounting Review, 93(3), 25–57. https://doi.org/10.2308/accr-51865  [OA](https://doi.org/10.2308/accr-51865)  [Scite](/scite_tallies?query=https://doi.org/10.2308/accr-51865)

[^Broadstock_2019_a]: Broadstock, D. C., &amp; Zhang, D. (2019). Social-media and intraday stock returns: The pricing power of sentiment. Finance Research Letters, 30, 116–123. https://doi.org/10.1016/j.frl.2019.03.030  [OA](https://doi.org/10.1016/j.frl.2019.03.030)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.frl.2019.03.030)

[^Cevik_et+al_2022_a]: Cevik, E., Altinkeski, B., Cevik, E. I., &amp; Dibooglu, S. (2022). Investor sentiments and stock markets during the COVID-19 pandemic. Financial Innovation, 8(01), 69. https://doi.org/10.1186/s40854-022-00375-0  [OA](https://doi.org/10.1186/s40854-022-00375-0)  [Scite](/scite_tallies?query=https://doi.org/10.1186/s40854-022-00375-0)

[^Chang_et+al_2022_a]: Chang, Y. C., Shao, R., &amp; Wang, N. (2022). Can stock message board sentiment predict future returns? Local versus nonlocal posts. Journal of Behavioral and Experimental Finance, 34, Article 100625. https://doi.org/10.1016/j.jbef.2022.100625  [OA](https://doi.org/10.1016/j.jbef.2022.100625)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbef.2022.100625)

[^Chen_et+al_2021_a]: Chen, R. D., Wu, L., Jin, C. L., &amp; Wang, S. N. (2021). Unintended investor sentiment on bank financial products: Evidence from China. Emerging Markets Review. https://doi.org/10.1016/j.ememar.2020.100760  [OA](https://doi.org/10.1016/j.ememar.2020.100760)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ememar.2020.100760)

[^Chen_et+al_2022_a]: Chen, P., Vivian, A., &amp; Ye, C. (2022). Forecasting carbon futures price: A hybrid method incorporating fuzzy entropy and extreme learning machine. Annals of Operations Research, 313(1), 559–601. https://doi.org/10.1007/s10479-021-04406-4  [OA](https://doi.org/10.1007/s10479-021-04406-4)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10479-021-04406-4)

[^Chiong_et+al_2022_a]: Chiong, R., Fan, Z., Hu, Z., &amp; Dhakal, S. (2022). A novel ensemble learning approach for stock market prediction based on sentiment analysis and the sliding window method. IEEE Transactions on Computational Social Systems. https://doi.org/10.1109/TCSS.2022.3182375  [OA](https://doi.org/10.1109/TCSS.2022.3182375)  [Scite](/scite_tallies?query=https://doi.org/10.1109/TCSS.2022.3182375)

[^Choi_2019_a]: Choi, S., &amp; Choi, W. Y. (2019). Effects of limited attention on investors’ trading behavior: Evidence from online ranking data. Pacific-Basin Finance Journal, 56, 273–289. https://doi.org/10.1016/j.pacfin.2019.06.007  [OA](https://doi.org/10.1016/j.pacfin.2019.06.007)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.pacfin.2019.06.007)

[^Chung_et+al_2012_a]: Chung, S. L., Hung, C. H., &amp; Yeh, C. Y. (2012). When does investor sentiment predict stock returns? Journal of Empirical Finance, 19(2), 217–240. https://doi.org/10.1016/j.jempfin.2012.01.002  [OA](https://doi.org/10.1016/j.jempfin.2012.01.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jempfin.2012.01.002)

[^Ciner_2014_a]: Ciner, C. (2014). The time varying relation between consumer confidence and equities. Journal of Behavioral Finance, 15(4), 312–317. https://doi.org/10.1080/15427560.2014.968716  [OA](https://doi.org/10.1080/15427560.2014.968716)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2014.968716)

[^Costola_et+al_2023_a]: Costola, M., Hinz, O., Nofer, M., &amp; Pelizzon, L. (2023). Machine learning sentiment analysis, COVID-19 news and stock market reactions. Research in International Business and Finance, 64, Article 101881. https://doi.org/10.1016/j.ribaf.2023.101881  [OA](https://doi.org/10.1016/j.ribaf.2023.101881)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ribaf.2023.101881)

[^Deng_et+al_2023_a]: Deng, S., Huang, X., Zhu, Y., Su, Z., Fu, Z., &amp; Shimada, T. (2023). Stock index direction forecasting using an explainable eXtreme gradient boosting and investor sentiments. The North American Journal of Economics and Finance, 64, Article 101848. https://doi.org/10.1016/j.najef.2022.101848  [OA](https://doi.org/10.1016/j.najef.2022.101848)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2022.101848)

[^Deng_et+al_2023_b]: Deng, S., Xiao, C., Zhu, Y., Peng, J., Li, J., &amp; Liu, Z. H. (2023). High-frequency direction forecasting and simulation trading of the crude oil futures using Ichimoku KinkoHyo and fuzzy rough set[J]. Expert Systems with Applications, 215, Article 119326. https://doi.org/10.1016/j.eswa.2022.119326  [OA](https://doi.org/10.1016/j.eswa.2022.119326)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2022.119326)

[^Deng_et+al_2024_a]: Deng, S., Zhu, Y., Yu, Y., &amp; Huang, X. (2024). An integrated approach of ensemble learning methods for stock index prediction using investor sentiments[J]. Expert Systems with Applications, 238, Article 121710. https://doi.org/10.1016/j.eswa.2023.121710  [OA](https://doi.org/10.1016/j.eswa.2023.121710)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2023.121710)

[^Dimpfl_2016_a]: Dimpfl, T., &amp; Jank, S. (2016). Can internet search queries help to predict stock market volatility? European Financial Management, 22(2), 171–192. https://doi.org/10.1111/eufm.12058  [OA](https://doi.org/10.1111/eufm.12058)  [Scite](/scite_tallies?query=https://doi.org/10.1111/eufm.12058)

[^Ding_2015_a]: Ding, R., &amp; Hou, W. (2015). Retail investor attention and stock liquidity. Journal of International Financial Markets, Institutions and Money, 37, 12–26. https://doi.org/10.1016/j.intfin.2015.04.001  [OA](https://doi.org/10.1016/j.intfin.2015.04.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.intfin.2015.04.001)

[^Eslamieh_et+al_2023_a]: Eslamieh, P., Shajari, M., &amp; Nickabadi, A. (2023). User2Vec: A novel representation for the information of the social networks for stock market prediction using convolutional and recurrent neural networks. Mathematics, 11(13), 2950. https://doi.org/10.3390/math11132950  [OA](https://doi.org/10.3390/math11132950)  [Scite](/scite_tallies?query=https://doi.org/10.3390/math11132950)

[^Fazlija_2022_a]: Fazlija, B., &amp; Harder, P. (2022). Using financial news sentiment for stock price direction prediction. Mathematics, 10(13), 2156. https://doi.org/10.3390/math10132156  [OA](https://doi.org/10.3390/math10132156)  [Scite](/scite_tallies?query=https://doi.org/10.3390/math10132156)

[^Foroni_et+al_2018_a]: Foroni, C., Guerin, P., &amp; Marcellino, M. (2018). Using low frequency information for predicting high frequency variables. International Journal of Forecasting, 34(4), 774–787. https://doi.org/10.1016/j.ijforecast.2018.06.004  [OA](https://doi.org/10.1016/j.ijforecast.2018.06.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ijforecast.2018.06.004)

[^Fraiberger_et+al_2021_a]: Fraiberger, S. P., Lee, D., Puy, D., &amp; Ranciere, R. (2021). Media sentiment and international asset prices. Journal of International Economics, 133, Article 103526. https://doi.org/10.1016/j.jinteco.2021.103526  [OA](https://doi.org/10.1016/j.jinteco.2021.103526)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jinteco.2021.103526)

[^Frazzini_2008_a]: Frazzini, A., &amp; Lamont, O. A. (2008). Dumb money: Mutual fund flows and the cross-section of stock returns. Journal of Financial Economics, 88(2), 299–322. https://doi.org/10.1016/j.jfineco.2007.07.001  [OA](https://doi.org/10.1016/j.jfineco.2007.07.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfineco.2007.07.001)

[^Gao_2023_a]: Gao, Z., &amp; Zhang, J. (2023). The fluctuation correlation between investor sentiment and stock index using VMD-LSTM: Evidence from China stock market. The North American Journal of Economics and Finance, 66, Article 101915. https://doi.org/10.1016/j.najef.2023.101915  [OA](https://doi.org/10.1016/j.najef.2023.101915)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2023.101915)

[^Gao_et+al_2019_a]: Gao, Y., Xiong, X., Feng, X., Li, Y., &amp; Vigne, S. (2019). A new attention proxy and order imbalance: Evidence from China. Finance Research Letters, 29, 411–417. https://doi.org/10.1016/j.frl.2018.11.009  [OA](https://doi.org/10.1016/j.frl.2018.11.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.frl.2018.11.009)

[^Greenwood_2014_a]: Greenwood, R., &amp; Shleifer, A. (2014). Expectations of returns and expected returns. The Review of Financial Studies, 27(3), 714–746. https://doi.org/10.1093/rfs/hht082  [OA](https://doi.org/10.1093/rfs/hht082)  [Scite](/scite_tallies?query=https://doi.org/10.1093/rfs/hht082)

[^Gu_2020_a]: Gu, C., &amp; Kurov, A. (2020). Informational role of social media: Evidence from twitter sentiment. Journal of Banking &amp; Finance, 121, Article 105969. https://doi.org/10.1016/j.jbankfin.2020.105969  [OA](https://doi.org/10.1016/j.jbankfin.2020.105969)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2020.105969)

[^Gupta_et+al_2023_a]: Gupta, R., Nel, J., &amp; Pierdzioch, C. (2023). Investor confidence and forecastability of US stock market realized volatility: Evidence from machine learning. Journal of Behavioral Finance, 24(1), 111–122. https://doi.org/10.1080/15427560.2021.1949719  [OA](https://doi.org/10.1080/15427560.2021.1949719)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2021.1949719)

[^Han_et+al_2018_a]: Han, L., Li, Z., &amp; Yin, L. (2018). Investor attention and stock returns: International evidence. Emerging Markets Finance and Trade, 54(14), 3168–3188. https://doi.org/10.1080/1540496X.2017.1413980  [OA](https://doi.org/10.1080/1540496X.2017.1413980)  [Scite](/scite_tallies?query=https://doi.org/10.1080/1540496X.2017.1413980)

[^Hao_et+al_2023_a]: Hao, J., Yuan, J., Wu, D., Xu, W., &amp; Li, J. (2023). A dynamic ensemble approach for multi-step price prediction: Empirical evidence from crude oil and shipping market [J]. Expert Systems with Applications, 2023(234), Article 121117. https://doi.org/10.1016/j.eswa.2023.121117  [OA](https://doi.org/10.1016/j.eswa.2023.121117)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2023.121117)

[^Hoekstra_2022_a]: Hoekstra, J., &amp; Guler, D. (2022). The mediating effect of trading volume on the relationship between investor sentiment and the return of tech companies. Journal of Behavioral Finance. https://doi.org/10.1080/15427560.2022.2138394  [OA](https://doi.org/10.1080/15427560.2022.2138394)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2022.2138394)

[^Huang_et+al_2022_a]: Huang, C., Wen, S., Yang, X., Cao, J., &amp; Yang, X. (2022). Measurement of individual investor sentiment and its application: Evidence from Chinese stock message board. Emerging Markets Finance and Trade, 58(3), 681–691. https://doi.org/10.1080/1540496X.2020.1835637  [OA](https://doi.org/10.1080/1540496X.2020.1835637)  [Scite](/scite_tallies?query=https://doi.org/10.1080/1540496X.2020.1835637)

[^Jiang_et+al_2022_a]: Jiang, H., Hu, W., Xiao, L., &amp; Dong, Y. (2022). A decomposition ensemble based deep learning approach for crude oil price forecasting. Resources Policy, 78, Article 102855. https://doi.org/10.1016/j.resourpol.2022.102855  [OA](https://doi.org/10.1016/j.resourpol.2022.102855)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.resourpol.2022.102855)

[^Jin_et+al_2020_a]: Jin, Z., Guo, K., Sun, Y., Lai, L., &amp; Liao, Z. (2020). The industrial asymmetry of the stock price prediction with investor sentiment: Based on the comparison of predictive effects with SVR. Journal of Forecasting, 39(7), 1166–1178. https://doi.org/10.1002/for.2681  [OA](https://doi.org/10.1002/for.2681)  [Scite](/scite_tallies?query=https://doi.org/10.1002/for.2681)

[^Leung_2015_a]: Leung, H., &amp; Ton, T. (2015). The impact of internet stock message boards on cross-sectional returns of small-capitalization stocks. Journal of Banking &amp; Finance, 55, 37–55. https://doi.org/10.1016/j.jbankfin.2015.01.009  [OA](https://doi.org/10.1016/j.jbankfin.2015.01.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2015.01.009)

[^Li_et+al_2020_a]: Li, Y., Bu, H., Li, J., &amp; Wu, J. (2020). The role of text-extracted investor sentiment in Chinese stock price prediction with the enhancement of deep learning. International Journal of Forecasting, 36(4), 1541–1562. https://doi.org/10.1016/j.ijforecast.2020.05.001  [OA](https://doi.org/10.1016/j.ijforecast.2020.05.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ijforecast.2020.05.001)

[^Li_et+al_2023_a]: Li, T., Chen, H., Liu, W., Yu, G., &amp; Yu, Y. (2023). Understanding the role of social media sentiment in identifying irrational herding behavior in the stock market. International Review of Economics &amp; Finance, 87, 163–179. https://doi.org/10.1016/j.iref.2023.04.016  [OA](https://doi.org/10.1016/j.iref.2023.04.016)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.iref.2023.04.016)

[^Liu_et+al_2022_a]: Liu, W., Zhang, C., Qiao, G., &amp; Xu, L. (2022). Impact of network investor sentiment and news arrival on jumps. The North American Journal of Economics and Finance, 62, Article 101780. https://doi.org/10.1016/j.najef.2022.101780  [OA](https://doi.org/10.1016/j.najef.2022.101780)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2022.101780)

[^Long_et+al_2019_a]: Long, W., Lu, Z., &amp; Cui, L. (2019). Deep learning-based feature engineering for stock price movement prediction. Knowledge-Based Systems, 164, 163–173. https://doi.org/10.1016/j.knosys.2018.10.034  [OA](https://doi.org/10.1016/j.knosys.2018.10.034)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.knosys.2018.10.034)

[^Lu_et+al_2021_a]: Lu, S., Liu, C., &amp; Chen, Z. (2021). Predicting stock market crisis via market indicators and mixed frequency investor sentiments. Expert Systems with Applications, 186, Article 115844. https://doi.org/10.1016/j.eswa.2021.115844  [OA](https://doi.org/10.1016/j.eswa.2021.115844)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2021.115844)

[^Lv_et+al_2022_a]: Lv, P., Shu, Y., Xu, J., &amp; Wu, Q. (2022). Modal decomposition-based hybrid model for stock index prediction[J]. Expert Systems with Applications, 202, Article 117252. https://doi.org/10.1016/j.eswa.2022.117252  [OA](https://doi.org/10.1016/j.eswa.2022.117252)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2022.117252)

[^Ma_2022_a]: Ma, C., &amp; Yan, S. (2022). Deep learning in the Chinese stock market: The role of technical indicators. Finance Research Letters, 49, Article 103025. https://doi.org/10.1016/j.frl.2022.103025  [OA](https://doi.org/10.1016/j.frl.2022.103025)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.frl.2022.103025)

[^Miwa_2023_a]: Miwa, K. (2023). Divergent opinions on social media. International Review of Economics &amp; Finance, 86, 182–196. https://doi.org/10.1016/j.iref.2023.03.004  [OA](https://doi.org/10.1016/j.iref.2023.03.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.iref.2023.03.004)

[^Park_et+al_2022_a]: Park, H. J., Kim, Y., &amp; Kim, H. Y. (2022). Stock market forecasting using a multi-task approach integrating long short-term memory and the random forest framework  [OA](https://scholar.google.co.uk/scholar?q=Park%2C%20H.J.%20Kim%2C%20Y.%20Kim%2C%20H.Y.%20Stock%20market%20forecasting%20using%20a%20multi-task%20approach%20integrating%20long%20short-term%20memory%20and%20the%20random%20forest%20framework%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Park%2C%20H.J.%20Kim%2C%20Y.%20Kim%2C%20H.Y.%20Stock%20market%20forecasting%20using%20a%20multi-task%20approach%20integrating%20long%20short-term%20memory%20and%20the%20random%20forest%20framework%202022) 

[^J_0000_a]: [J]. Applied Soft Computing, 114, Article 108106. https://doi.org/10.1016/j.asoc.2021.108106  [OA](https://doi.org/10.1016/j.asoc.2021.108106)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asoc.2021.108106)

[^Rezaei_et+al_2021_a]: Rezaei, H., Faaljou, H., &amp; Mansourfar, G. (2021). Stock price prediction using deep learning and frequency decomposition. Expert Systems with Applications, 169, Article 114332. https://doi.org/10.1016/j.eswa.2020.114332  [OA](https://doi.org/10.1016/j.eswa.2020.114332)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2020.114332)

[^Schmeling_2009_a]: Schmeling, M. (2009). Investor sentiment and stock returns: Some international evidence. Journal of empirical finance, 16(3), 394–408. https://doi.org/10.1016/j.  [OA](https://doi.org/10.1016/j)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j)

[^Shen_et+al_2018_a]: jempfin.2009.01.002 Shen, D., Liu, L., &amp; Zhang, Y. (2018). Quantifying the cross-sectional relationship between online sentiment and the skewness of stock returns. Physica A: Statistical  [OA](https://scholar.google.co.uk/scholar?q=Shen%2C%20D.%20Liu%2C%20L.%20Zhang%2C%20Y.%20Quantifying%20the%20cross-sectional%20relationship%20between%20online%20sentiment%20and%20the%20skewness%20of%20stock%20returns%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Shen%2C%20D.%20Liu%2C%20L.%20Zhang%2C%20Y.%20Quantifying%20the%20cross-sectional%20relationship%20between%20online%20sentiment%20and%20the%20skewness%20of%20stock%20returns%202018) 

[^Mechanics_0000_a]: Mechanics and its Applications, 490, 928–934. https://doi.org/10.1016/j.physa.2017.08.036  [OA](https://doi.org/10.1016/j.physa.2017.08.036)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.physa.2017.08.036)

[^Shi_et+al_2019_a]: Shi, Y., Tang, Y., &amp; Long, W. (2019). Sentiment contagion analysis of interacting investors: evidence from China’s stock forum[J]. Physica A: Statistical Mechanics and its Applications, 523, 246–259. https://doi.org/10.1016/j.physa.2019.02.025  [OA](https://doi.org/10.1016/j.physa.2019.02.025)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.physa.2019.02.025)

[^Shiller_2003_a]: Shiller, R. J. (2003). From efficient markets theory to behavioral finance. Journal of Economic Perspectives, 17(1), 83–104. https://doi.org/10.1257/  [OA](https://doi.org/10.1257/)  [Scite](/scite_tallies?query=author%3AShiller%2Ctitle%3AFrom%20efficient%20markets%20theory%20to%20behavioral%20finance%2Cyear%3A2003)

[^Sun_et+al_2016_a]: Sun, L., Najand, M., &amp; Shen, J. (2016). Stock return predictability and investor sentiment: A high-frequency perspective[J]. Journal of Banking &amp; Finance, 73, 147–164.  [OA](https://engine.scholarcy.com/oa_version?query=Sun%2C%20L.%20Najand%2C%20M.%20Shen%2C%20J.%20Stock%20return%20predictability%20and%20investor%20sentiment%3A%20A%20high-frequency%20perspective%5BJ%202016&author=Sun&title=Stock%20return%20predictability%20and%20investor%20sentiment%3A%20A%20high-frequency%20perspective%5BJ&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Sun%2C%20L.%20Najand%2C%20M.%20Shen%2C%20J.%20Stock%20return%20predictability%20and%20investor%20sentiment%3A%20A%20high-frequency%20perspective%5BJ%202016) [Scite](/scite_tallies?query=author%3ASun%2Ctitle%3AStock%20return%20predictability%20and%20investor%20sentiment%3A%20A%20high-frequency%20perspective%5BJ%2Cyear%3A2016)

[^_0000_b]: https://doi.org/10.1016/j.jbankfin.2016.09.010  [OA](https://doi.org/10.1016/j.jbankfin.2016.09.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2016.09.010)

[^Sun_2018_a]: Sun, W., &amp; Zhang, C. (2018). Analysis and forecasting of the carbon price using multi—resolution singular value decomposition and extreme learning machine optimized by adaptive whale optimization algorithm. Applied Energy, 231, 1354–1371. https://doi.org/10.1016/j.apenergy.2018.09.118  [OA](https://doi.org/10.1016/j.apenergy.2018.09.118)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.apenergy.2018.09.118)

[^Swamy_2023_a]: Swamy, V., &amp; Lagesh, M. A. (2023). Does happy twitter forecast gold price? Resources Policy, 81, Article 103299. https://doi.org/10.1016/j.resourpol.2023.103299  [OA](https://doi.org/10.1016/j.resourpol.2023.103299)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.resourpol.2023.103299)

[^Uhl_2021_a]: Uhl, M. W., &amp; Novacek, M. (2021). When it pays to ignore: Focusing on top news and their sentiment. Journal of Behavioral Finance, 22(4), 461–479. https://doi.org/  [OA](https://doi.org/)  [Scite](/scite_tallies?query=author%3AUhl%2Ctitle%3AWhen%20it%20pays%20to%20ignore%3A%20Focusing%20on%20top%20news%20and%20their%20sentiment%2Cyear%3A2021)

[^Wang_2022_a]: 10.1080/15427560.2020.1821375 Wang, H., &amp; Hu, D. (2022). Heterogenous beliefs with sentiments and asset pricing. The North American Journal of Economics and Finance, 63, Article 101824. https://  [OA](https://doi.org/10.1080/15427560.2020.1821375)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2020.1821375)

[^_0000_c]: doi.org/10.1016/j.najef.2022.101824  [OA](https://doi.org/10.1016/j.najef.2022.101824)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2022.101824)

[^Wang_et+al_2005_a]: Wang, S., Yu, L., &amp; Lai, K. (2005). Crude oil price forecasting with TEI@I methodology. Journal of Systems Science and Complexity, 18(2), 145. https://doi.org/  [OA](https://doi.org/)  [Scite](/scite_tallies?query=author%3AWang%2Ctitle%3ACrude%20oil%20price%20forecasting%20with%20TEI%40I%20methodology%2Cyear%3A2005)

[^Wang_et+al_2017_a]: 10.1016/j.eneco.2008.05.003 Wang, D., Luo, H., Grunder, O., Lin, Y., &amp; Guo, H. (2017). Multi-step ahead electricity price forecasting using a hybrid model based on two-layer decomposition technique and BP neural network optimized by firefly algorithm. Applied Energy, 190, 390–407. https://doi.org/10.1016/j.apenergy.2016.12.134  [OA](https://doi.org/10.1016/j.apenergy.2016.12.134)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.apenergy.2016.12.134)

[^Wen_et+al_2019_a]: Wen, F., Xu, L., Ouyang, G., &amp; Kou, G. (2019). Retail investor attention and stock price crash risk: Evidence from China. International Review of Financial Analysis, 65, Article 101376. https://doi.org/10.1016/j.irfa.2019.101376  [OA](https://doi.org/10.1016/j.irfa.2019.101376)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.irfa.2019.101376)

[^Xu_et+al_2021_a]: Xu, Q. F., Zhuo, X. X., Jiang, C. X., Sun, F., &amp; Huang, X. (2021). Reverse restricted MIDAS model with application to US interest rate forecasts. Communications in  [OA](https://scholar.google.co.uk/scholar?q=Xu%2C%20Q.F.%20Zhuo%2C%20X.X.%20Jiang%2C%20C.X.%20Sun%2C%20F.%20Reverse%20restricted%20MIDAS%20model%20with%20application%20to%20US%20interest%20rate%20forecasts%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Xu%2C%20Q.F.%20Zhuo%2C%20X.X.%20Jiang%2C%20C.X.%20Sun%2C%20F.%20Reverse%20restricted%20MIDAS%20model%20with%20application%20to%20US%20interest%20rate%20forecasts%202021) 

[^Statistics-Simulation_0000_d]: Statistics-Simulation and Computation, 50(02), 462–482. https://doi.org/10.1080/03610918.2018.1563148  [OA](https://doi.org/10.1080/03610918.2018.1563148)  [Scite](/scite_tallies?query=https://doi.org/10.1080/03610918.2018.1563148)

[^Yang_et+al_2020_a]: Yang, W., Wang, J., Niu, T., &amp; Du, P. (2020). A novel system for multi-step electricity price forecasting for electricity market management. Applied Soft Computing, 88, Article 106029. https://doi.org/10.1016/j.asoc.2019.106029  [OA](https://doi.org/10.1016/j.asoc.2019.106029)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asoc.2019.106029)

[^Zhang_et+al_2021_a]: Zhang, T., Tang, Z., Wu, J., Du, X., &amp; Chen, K. (2021). Multi-step-ahead crude oil price forecasting based on two-layer decomposition technique and extreme learning machine optimized by the particle swarm optimization algorithm. Energy, 229, Article 120797. https://doi.org/10.1016/j.energy.2021.120797  [OA](https://doi.org/10.1016/j.energy.2021.120797)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.energy.2021.120797)

[^Zhao_2023_a]: Zhao, Y., &amp; Yang, G. (2023). Deep learning-based integrated framework for stock price movement prediction. Applied Soft Computing, 133, Article 109921. https://doi.  [OA](https://doi)  [Scite](/scite_tallies?query=author%3AZhao%2Ctitle%3ADeep%20learning-based%20integrated%20framework%20for%20stock%20price%20movement%20prediction%2Cyear%3A2023)

[^Zhou_2018_a]: org/10.1016/j.asoc.2022.109921 Zhou, G. (2018). Measuring investor sentiment. Annual Review of Financial Economics, 2018(10), 239–259. https://doi.org/10.1146/annurev-financial-110217-  [OA](https://doi.org/10.1146/annurev-financial-110217-)  [Scite](/scite_tallies?query=https://doi.org/10.1146/annurev-financial-110217-)

[^Zolfaghari_2021_a]: Zolfaghari, M., &amp; Gholami, S. (2021). A hybrid approach of adaptive wavelet transform, long short-term memory and ARIMA-GARCH family models for the stock index prediction. Expert Systems with Applications, 182, Article 115149. https://doi.org/10.1016/j.eswa.2021.115149  [OA](https://doi.org/10.1016/j.eswa.2021.115149)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2021.115149)

[^Yin_et+al_2022_a]: Yin, H., Wu, X., &amp; Kong, S. X. (2022). Daily investor sentiment, order flow imbalance and stock liquidity: evidence from the Chinese stock market[J]. International Journal of Finance &amp; Economics, 2022, 27(4): 4816-4836. https://doi.org/10.1002/ijfe.2402.  [OA](https://doi.org/10.1002/ijfe.2402)  [Scite](/scite_tallies?query=https://doi.org/10.1002/ijfe.2402)

