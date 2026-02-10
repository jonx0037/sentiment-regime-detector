[[Shao_et+al_RevisitingTimevaryingDynamicsStockMarket_2024]]

# [Revisiting time-varying dynamics in stock market forecasting: A multi-source sentiment analysis approach with large language model](https://doi.org/10.1016/j.dss.2024.114362)

## [[Zhen Shao]]; [[Xusheng Yao]]; [[Feng Chen]] et al

## Abstract

This paper presents the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM), an innovative framework for stock return prediction that combines cutting-edge sentiment analysis with dynamic financial modeling. The model integrates sentiment data from 2.5 million Twitter posts and various news sources, utilizing state-of-the-art sentiment analysis tools such as VADER, TextBlob, and RoBERTa. HD-SURDLM refines Gibbs sampling for enhanced numerical stability and efficiency while capturing cross-sectional dependencies across multiple assets, such as a portfolio. The model consistently outperforms traditional methods such as LSTM, Random Forest, and RNNs in forecasting accuracy. Empirical results show a 1.02% improvement in 1-day horizon forecasts, a 0.42% gain for 20-day predictions, and a 0.36% increase for 50-day forecasts. By effectively merging public sentiment with dynamic asset modeling, HD-SURDLM offers substantial improvements in short- and long-term prediction accuracy. Its capacity to capture both cross-sectional insights and temporal dynamics makes it an invaluable tool for investors, traders, and financial institutions navigating sentiment-driven markets. HD-SURDLM not only enhances predictive accuracy but also provides a robust decision-support system for financial stakeholders.

## Key concepts

# sentiment_analysis; #support_vector_regression; #recurrent_neural_networks; #finding/long_short_term_memory; #long_short_term_memory; #claim/RoBERTa; #RoBERTa

## Quote
>
> The study introduces the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM) framework for stock return prediction, which integrates advanced sentiment analysis and financial modeling techniques, demonstrating superior performance over traditional models.

## Key points

- In the rapidly evolving landscape of financial markets, accurately predicting stock returns across multiple assets has become increasingly crucial for investors, traders, and financial institutions
- The primary objectives of this research are (1) to explore the intricate relationship between sentiments expressed on social and news media platforms and stock returns and (2) to develop a robust model capable of capturing these complex, time-varying relationships in financial markets: To achieve these goals, we propose a novel approach: the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM)
- Interpretability: HD-SURDLM provides greater transparency compared to neural networks like Long Short-Term Memory (LSTM) [^2] and Recurrent Neural Networks (RNNs) [^3], offering clearer insights into the factors driving stock price predictions, which is crucial for financial forecasting
- Experiment setting We evaluated two HD-SURDLM models: HD-SURDLM-1 using Twitter sentiment VADER scores and news sentiment TB scores, which are based on our empirical simulation, and HD-SURDLM-2 employing RoBERTa for both Twitter and news sentiment analysis
- To illustrate with concrete numbers: assuming a baseline profit of $500, the improved model generates $597.65, representing an additional $97.65 per trade. This pattern of enhanced profitability extends across different forecast horizons, with profit improvements of $27.80 and $34.90 per trade for 20-day and 50-day horizons, respectively. These results demonstrate that the Mean Absolute Error (MAE) reductions achieved by HD-SURDLM translate into economically significant improvements in trading performance
- On AMZN, HD-SURDLM-2 achieves an MAE of 0.87, which is an 11% improvement over the traditional SUR-DLM and a 15% improvement over LSTM. This trend is consistent across other tickers like MSFT and FB, where HD-SURDLM-2 provides a significant accuracy boost of approximately 8% and 6%, respectively, compared to the best-performing baseline models
- This research underscores the importance of combining public sentiment with dynamic asset modeling to enhance predictive accuracy across various time horizons

## Summary

### Model

The Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HD-SURDLM) is a novel framework for stock return prediction that combines sentiment analysis with dynamic financial modeling.
The model integrates sentiment data from 2.5 million Twitter posts and various news sources, utilizing state-of-the-art sentiment analysis tools such as VADER, TextBlob, and RoBERTa.
HD-SURDLM refines Gibbs sampling for enhanced numerical stability and efficiency while capturing cross-sectional dependencies across multiple assets.

### Methodology

The study employs a comprehensive suite of sentiment analysis methods, including VADER, Bag-of-Words, TextBlob, and RoBERTa, to capture nuanced sentiments expressed in social media and news.
A sophisticated weighting mechanism for tweets is introduced based on user influence and tweet attributes, enhancing the relevance and impact of social media data in predictions.
The model leverages an unprecedented dataset comprising over 2.5 million Twitter posts and Reuters news headlines, spanning from 2014 to 2021.
The HD-SURDLM model utilizes a novel, stable Gibbs sampling approach to enhance performance and handle multiple assets.
The method involves sampling the intercept vector, non-time-varying coefficient matrix, and time-varying coefficient tensors.
An improved Filter Forward-Backward Sampling (FFBS) algorithm is used to process all stocks concurrently, thereby enhancing numerical stability.
The joint variance-covariance matrix is sampled to capture cross-stock error correlations.

### Results

The HD-SURDLM model consistently outperforms traditional methods such as LSTM, Random Forest, and RNN in forecasting accuracy, with 1.02% improvement at the 1-day horizon, 0.42% at 20 days, and 0.36% at 50 days.
The model provides a robust decision-support system for financial stakeholders, offering substantial improvements in short- and long-term prediction accuracy by effectively merging public sentiment with dynamic asset modeling.
The HD-SURDLM model is evaluated using a comprehensive comparison with baseline models, including LSTM, RNN, Lasso, MLP, Random Forest, and SVR.
The results show that HD-SURDLM-2 achieves the lowest MAE for 15 out of 20 tickers, outperforming the best baseline model by an average of 5%.
The model demonstrates clear advantages across all forecasting horizons, showing consistent improvements in prediction accuracy.
An ablation study reveals the performance improvements of different model configurations, highlighting the importance of integrating multi-source sentiment analysis with dynamic modeling capabilities.

### Model Description

The HD-SURDLM model is a high-dimensional framework that incorporates multidimensional time-varying features to improve model performance.
It comprises stock-specific intercepts, time-varying features with coefficients, and non-time-varying features with coefficients.
The model accounts for observation errors and system errors, which are independent across time and features.
The unknown parameters collectively capture stock-specific effects, time-varying relationships, and error structures.

### Model Performance

The study demonstrates that the HD-SURDLM models generally outperform baseline models in predicting stock returns, achieving lower Mean Absolute Errors (MAEs) for the majority of tickers.
The integration of LLMs results in the most significant reductions in MAE for WFC and WMT, with 39.63% for AAPL, 41.88% for WFC, and 29.33% for WMT.
The Diebold-Mariano test results indicate that the HD-SURDLM models demonstrate statistically significant improvements over baseline models in several instances.

### Computational Cost

The study highlights the importance of considering computational cost, particularly in financial decision-making, where timely analysis is essential.
The results show that HD-SURDLM1 is highly efficient, taking only 3 to 6 seconds, while HD-SURDLM2, which employs RoBERTa, requires up to 14 hours.
The trade-off between efficiency and complexity is evident, with HD-SURDLM1 providing a better balance of performance and feasibility for large-scale or frequent financial tasks.

### Implementation And Economic Relevance

The study underscores the importance of integrating public sentiment analysis with dynamic asset modeling to improve predictive accuracy across various time horizons.
The implications of this research extend to investors, traders, and financial institutions, offering more nuanced tools for risk assessment and strategy formulation.
The improved profit calculations demonstrate that the MAE reductions achieved by HD-SURDLM translate into economically significant improvements in trading performance, with a profit increase of $97.65 per trade on a baseline profit of $500.

## Data analysis

- #method/lstm_model
- #method/
- #method/diebold_mariano_test
- #method/covariance_matrix
- #method/hdsurdlm_model
- #method/roberta_model
- #method/random_forest_models
- #method/lasso_regression

## Findings

- Empirical results show a 1.02% improvement in 1-day horizon forecasts, a 0.42% gain for 20-day predictions, and a 0.36% increase for 50-day forecasts
- HD-SURDLM-2 shows a 6% reduction in <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> compared to <a class="keyword" href="https://en.wikipedia.org/wiki/Long_Short-Term_Memory" title="Long Short-Term Memory">LSTM</a> for tickers like AMZN and BAC, where short-term market sentiment plays a crucial role
- The overall improvement in prediction accuracy is particularly notable for highly volatile stocks such as TSLA, where HD-SURDLM-2 achieves a 4.5% lower <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> compared to the next best model, underscoring its strength in short-term prediction
- As the forecasting horizon extends to 20 days, the results, as shown in Table 4, reveal that HD-SURDLM-2 continues to outperform the baseline models, with an average <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> reduction of 7% across all tickers
- The <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> for HD-SURDLM-2 on GOOG is 1.08, representing a 12% improvement over the traditional SUR-DLM model
- The enhanced ability of HD-SURDLM-2 to capture medium-term trends is further evidenced by its performance on NFLX, where it achieves a 9% lower <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> compared to the <a class="keyword" href="https://en.wikipedia.org/wiki/Long_Short-Term_Memory" title="Long Short-Term Memory">LSTM</a> model
- This highlights HD-SURDLM’s effectiveness in adapting to market conditions over a medium-term horizon, making it more reliable than conventional methods like Random Forest, which shows a 20% higher error rate on average
- On average, HD-SURDLM-2 reduces the <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> by 10% compared to the best baseline model
- On AMZN, HD-SURDLM-2 achieves an <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> of 0.87, which is an 11% improvement over the traditional SUR-DLM and a 15% improvement over <a class="keyword" href="https://en.wikipedia.org/wiki/Long_Short-Term_Memory" title="Long Short-Term Memory">LSTM</a>
- For example, on AMZN, HD-SURDLM-2 achieves an <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> of 0.87, which is an 11% improvement over the traditional SUR-DLM and a 15% improvement over <a class="keyword" href="https://en.wikipedia.org/wiki/Long_Short-Term_Memory" title="Long Short-Term Memory">LSTM</a>. This trend is consistent across other tickers like MSFT and FB, where HD-SURDLM-2 provides a significant accuracy boost of approximately 8% and 6%, respectively, compared to the best-performing baseline models
- For the 1-day horizon, HD-SURDLM-2 provides up to a 6% reduction in <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> over the best baseline models
- For the 20-day horizon, it offers an average 7% reduction in <a class="keyword" href="#" title="Mean Absolute Error">MAE</a>, and for the 50-day horizon, it provides up to a 10% improvement
- The integration of LLM results in the most significant reduction in <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> for WFC and WMT, with WFC experiencing a reducing the <a class="keyword" href="#" title="Mean Absolute Error">MAE</a> by 39.63% for AAPL, 41.88% for WFC, and 29.33% for WMT, highlighting the effectiveness of combining HD-SURDLM with the proposed stable Gibbs sampling and LLM in financial forecasting
- <mark class="claim">The DM statistics, alongside their corresponding p-values, indicate <mark class="fact">whether the HD-SURDLM models significantly outperform the baselines over a 1day forecast horizon</mark></mark>
- With MAEbaseline = 0.215 and MAEimproved = 0.173, we observe a 19.53% improvement in prediction accuracy

## Builds on previous research

- In this study, we compare the performance of our proposed HDSURDLM model with several baseline models commonly used in financial forecasting. These baselines include Long Short-Term Memory (LSTM) networks [^2], Recurrent Neural Networks (RNNs) [^3], Lasso Regression [^4], Multi-Layer Perceptron (MLP) [^5], Random Forest models, Support Vector Regression (SVR), and the traditional SUR-DLM model.

## Differs from previous work

- ∑ Ψ = utuTt. Unlike Ho et al [^19], we do not incorporate vt (the difference between consecutive βt) in the sampling process.

## Contributions

- In conclusion, <mark class="claim">our research introduces the Heterogeneous Dynamic Seemingly Unrelated Regression with Dynamic Linear Models (HDSURDLM) as an innovative framework for stock return prediction</mark>. This model uniquely integrates advanced sentiment analysis from social media and news sources with sophisticated financial modeling techniques. Key innovations include (1) an improved Gibbs sampling technique with enhanced numerical stability, (2) A novel approach to modeling

## Limitations

- The study acknowledges that current approaches to stock market prediction, while diverse, face several limitations, including a lack of interpretability, dynamic adaptation, and cross-sectional insights. The study also notes that deep learning models, such as LSTMs and RNNs, have shown considerable potential for capturing complex patterns in market data but often lack interpretability.
- The study does not explicitly discuss the limitations of the proposed model, but it can be inferred that the model may be sensitive to the choice of hyperparameters and the quality of the sentiment analysis data.
- The study notes that certain exceptions were observed, particularly with WFC and T, where the model’s performance was less robust, especially in long-term forecasts.

## Future work

- The study suggests that future research could explore the application of HD-SURDLM to other financial markets and assets, such as commodities and currencies. The study also notes that the development of more advanced sentiment analysis techniques and the integration of additional data sources could further enhance the accuracy and robustness of the HD-SURDLM model.
- The study suggests that future work could involve exploring the application of the HD-SURDLM model to other financial markets and assets, and investigating the use of alternative sentiment analysis methods.

## References

[^2]: A. Sherstinsky, Fundamentals of recurrent neural network (RNN) and long short-term memory (LSTM) network, Physica D 404 (2020) 132306.  [OA](https://engine.scholarcy.com/oa_version?query=Sherstinsky%2C%20A.%20Fundamentals%20of%20recurrent%20neural%20network%20%28RNN%29%20and%20long%20short-term%20memory%20%28LSTM%29%20network%202020&author=Sherstinsky&title=Fundamentals%20of%20recurrent%20neural%20network%20%28RNN%29%20and%20long%20short-term%20memory%20%28LSTM%29%20network&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Sherstinsky%2C%20A.%20Fundamentals%20of%20recurrent%20neural%20network%20%28RNN%29%20and%20long%20short-term%20memory%20%28LSTM%29%20network%202020) [Scite](/scite_tallies?query=author%3ASherstinsky%2Ctitle%3AFundamentals%20of%20recurrent%20neural%20network%20%28RNN%29%20and%20long%20short-term%20memory%20%28LSTM%29%20network%2Cyear%3A2020)

[^3]: L. Medsker, L.C. Jain, Recurrent Neural Networks: Design and Applications, CRC Press, 1999.  [OA](https://scholar.google.co.uk/scholar?q=Medsker%2C%20L.%20Jain%2C%20L.C.%20Recurrent%20Neural%20Networks%3A%20Design%20and%20Applications%201999) [GScholar](https://scholar.google.co.uk/scholar?q=Medsker%2C%20L.%20Jain%2C%20L.C.%20Recurrent%20Neural%20Networks%3A%20Design%20and%20Applications%201999)

[^4]: R. Tibshirani, Regression shrinkage and selection via the lasso, J. R. Stat. Soc. Ser. B Stat. Methodol. 58 (1) (1996) 267–288.  [OA](https://engine.scholarcy.com/oa_version?query=R%20Tibshirani%20Regression%20shrinkage%20and%20selection%20via%20the%20lasso%20J%20R%20Stat%20Soc%20Ser%20B%20Stat%20Methodol%2058%201%201996%20267288&author=Tibshirani&title=&year=1996) [GScholar](https://scholar.google.co.uk/scholar?q=R%20Tibshirani%20Regression%20shrinkage%20and%20selection%20via%20the%20lasso%20J%20R%20Stat%20Soc%20Ser%20B%20Stat%20Methodol%2058%201%201996%20267288) [Scite](/scite_tallies?query=%5B4%5D%20R.%20Tibshirani%2C%20Regression%20shrinkage%20and%20selection%20via%20the%20lasso%2C%20J.%20R.%20Stat.%20Soc.%20Ser.%20B%20Stat.%20Methodol.%2058%20%281%29%20%281996%29%20267%E2%80%93288.)

[^5]: H. Taud, J.-F. Mas, Multilayer perceptron (MLP), Geomat. Approaches Model. Land Chang. Scen. (2018) 451–455.  [OA](https://engine.scholarcy.com/oa_version?query=Taud%2C%20H.%20Mas%2C%20J.-F.%20Multilayer%20perceptron%20%28MLP%202018&author=Taud&title=Multilayer%20perceptron%20%28MLP&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Taud%2C%20H.%20Mas%2C%20J.-F.%20Multilayer%20perceptron%20%28MLP%202018) [Scite](/scite_tallies?query=author%3ATaud%2Ctitle%3AMultilayer%20perceptron%20%28MLP%2Cyear%3A2018)

[^19]: C.-S. Ho, P. Damien, B. Gu, P. Konana, The time-varying nature of social media sentiments in modeling stock returns, Decis. Support Syst. (2017).  [OA](https://scholar.google.co.uk/scholar?q=Ho%2C%20C.-S.%20Damien%2C%20P.%20Gu%2C%20B.%20Konana%2C%20P.%20The%20time-varying%20nature%20of%20social%20media%20sentiments%20in%20modeling%20stock%20returns%2C%20Decis%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Ho%2C%20C.-S.%20Damien%2C%20P.%20Gu%2C%20B.%20Konana%2C%20P.%20The%20time-varying%20nature%20of%20social%20media%20sentiments%20in%20modeling%20stock%20returns%2C%20Decis%202017)

[^26] Junbin Gao graduated from Huazhong University of Science and Technology (HUST), China, in 1982 with a B.Sc. in Computational Mathematics and obtained his Ph.D. from Dalian University of Technology, China, in 1991. He is a Professor of Big Data Analytics at the University of Sydney Business School and was a Professor in Computer Science at the School of Computing and Mathematics at Charles Sturt University, Australia. He was a senior lecturer and lecturer in Computer Science at the University of New England, Australia, from 2001 to 2005. From 1982 to 2001, he was an associate lecturer, lecturer, associate professor, and professor in the Department of Mathematics at HUST. His main research interests include machine learning, data analytics, Bayesian learning and inference, and image analysis.  [OA](https://scholar.google.co.uk/scholar?q=Junbin%20Gao%20graduated%20from%20Huazhong%20University%20of%20Science%20and%20Technology%20HUST%20China%20in%201982%20with%20a%20BSc%20in%20Computational%20Mathematics%20and%20obtained%20his%20PhD%20from%20Dalian%20University%20of%20Technology%20China%20in%201991%20He%20is%20Professor%20of%20Big%20Data%20Analytics%20in%20the%20University%20of%20Sydney%20Business%20School%20at%20the%20University%20of%20Sydney%20and%20was%20a%20Professor%20in%20Computer%20Science%20in%20the%20School%20of%20Computing%20and%20Mathematics%20at%20Charles%20Sturt%20University%20Australia%20He%20was%20a%20senior%20lecturer%20a%20lecturer%20in%20Computer%20Science%20from%202001%20to%202005%20at%20the%20University%20of%20New%20England%20Australia%20From%201982%20to%202001%20he%20was%20an%20associate%20lecturer%20lecturer%20associate%20professor%20and%20professor%20in%20Department%20of%20Mathematics%20at%20HUST%20His%20main%20research%20interests%20include%20machine%20learning%20data%20analytics%20Bayesian%20learning%20and%20inference%20and%20image%20analysis) [GScholar](https://scholar.google.co.uk/scholar?q=Junbin%20Gao%20graduated%20from%20Huazhong%20University%20of%20Science%20and%20Technology%20HUST%20China%20in%201982%20with%20a%20BSc%20in%20Computational%20Mathematics%20and%20obtained%20his%20PhD%20from%20Dalian%20University%20of%20Technology%20China%20in%201991%20He%20is%20Professor%20of%20Big%20Data%20Analytics%20in%20the%20University%20of%20Sydney%20Business%20School%20at%20the%20University%20of%20Sydney%20and%20was%20a%20Professor%20in%20Computer%20Science%20in%20the%20School%20of%20Computing%20and%20Mathematics%20at%20Charles%20Sturt%20University%20Australia%20He%20was%20a%20senior%20lecturer%20a%20lecturer%20in%20Computer%20Science%20from%202001%20to%202005%20at%20the%20University%20of%20New%20England%20Australia%20From%201982%20to%202001%20he%20was%20an%20associate%20lecturer%20lecturer%20associate%20professor%20and%20professor%20in%20Department%20of%20Mathematics%20at%20HUST%20His%20main%20research%20interests%20include%20machine%20learning%20data%20analytics%20Bayesian%20learning%20and%20inference%20and%20image%20analysis)
