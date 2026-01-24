[[Dakalbab_et+al_AdvancingForexPredictionThroughMultimodal_2025]]

# [Advancing Forex prediction through multimodal text-driven model and attention mechanisms](https://doi.org/10.1016/j.iswa.2025.200518)

## [[Fatima Dakalbab]]; [[Ayush Kumar]]; [[Manar Abu Talib]] et al.

## Abstract
The Forex market, characterized by high volatility and complexity, poses a significant challenge for accurately predicting currency price movements. Traditional approaches often rely on either technical indicators or sentiment analysis, limiting their ability to capture the interplay between diverse data modalities. This research introduces a novel multimodal deep learning framework that integrates technical and sentiment analysis via a cross-modal attention mechanism, enabling a comprehensive understanding of market dynamics. The proposed model leverages innovative alignment techniques to synchronize sentiment from news articles with historical price trends, facilitating robust multiclass prediction of Forex price directions. To evaluate its effectiveness, the model was tested on three major currency pairs—EUR/USD, GBP/USD, and USD/JPY—using k-fold cross-validation. Multiple attention configurations, including no attention, self-attention, bi-cross attention, and a hybrid approach, were implemented to assess the impact of attention mechanisms on prediction performance. Experimental results highlight the superiority of the hybrid attention mechanism, which consistently outperformed single-modality models and other configurations across key metrics, such as Matthew's correlation coefficient, accuracy, directional accuracy, and F1-score. These findings underscore the importance of integrating sentiment and technical data for enhanced Forex prediction. This study contributes to the growing field of multimodal financial forecasting by laying a foundation for future research that incorporates advanced risk metrics, real-time trading systems, and broader market applications.

## Key concepts
#FOREX; #technical_analysis; #finding/technical_indicator; #technical_indicator; #sentiment_analysis; #finding/matthews_correlation_coefficient; #matthews_correlation_coefficient; #finding/attention_mechanism; #attention_mechanism; #finding/currency_pair; #currency_pair

## Quote
This research proposes a multimodal Forex prediction model that combines qualitative sentiment data with quantitative technical analysis, leveraging cross-modal attention mechanisms to enhance forecasting performance in the Forex market.

## Key points
- Financial markets can be classified as complex systems since they exhibit non-linear, non-stationary, and time-variant characteristics
- This research presents a comprehensive method for forecasting Forex price fluctuations by combining technical indicators with sentiment analysis derived from news, employing a multi-cross-modal deep learning model
- The findings indicated that our multimodal model, especially with the self-attention and Bi-Cross Attention module, markedly surpassed single-modality models depending exclusively on technical indicators or sentiment, validating the benefits of a comprehensive approach to Forex prediction
- This research primarily contributes a multimodal Forex prediction model that enhances directional accuracy by identifying latent interactions between market sentiment and price trends. This model architecture demonstrates the effectiveness of cross-modal attention in financial forecasting and offers a scalable solution adaptable to various currency pairs and market situations
- This study focuses on Forex markets; the proposed approach can be applied to other financial prediction domains, such as stocks and commodities, with minor changes
- Feature-specific scaling methods could be explored to ensure that technical indicators with different ranges, such as the Relative Strength Index (RSI) and Moving Average Convergence Divergence (MACD), are normalized in a way that preserves their unique interpretations


## Summary

### Introduction
The Forex market is characterized by high volatility and complexity, making accurate prediction of currency price movements a significant challenge.
Traditional approaches often rely on either technical indicators or sentiment analysis, limiting their ability to capture the interplay between diverse data modalities.
This research introduces a novel multimodal deep learning framework that integrates technical and sentiment analysis via a cross-modal attention mechanism.

### Methodology
The proposed model leverages innovative alignment techniques to synchronize sentiment from news articles with historical price trends, facilitating robust multiclass prediction of Forex price directions.
The model was tested on three major currency pairs—EUR/USD, GBP/USD, and USD/JPY—using k-fold cross-validation.
Multiple attention configurations, including no attention, self-attention, bi-cross attention, and a hybrid approach, were implemented to assess the impact of attention mechanisms on prediction performance.

### Results
Experimental results highlight the superiority of the hybrid attention mechanism, which consistently outperforms single-modality models and other configurations across key metrics, including Matthew’s correlation coefficient, accuracy, directional accuracy, and F1-score.
These findings underscore the importance of integrating sentiment and technical data for enhanced Forex prediction, contributing to the growing field of multimodal financial forecasting.

### Fusion Techniques
Multimodal learning models demonstrate superior performance compared to unimodal techniques, leveraging the depth of integrated data to achieve more precise predictions and comprehensive representations.
Several fusion strategies are commonly used in multimodal models, including operation-based, attention-based, tensor-based, subspace-based, and graph-based fusion.
Operation-based fusion integrates feature vectors from multiple modalities using basic mathematical operations, while attention-based fusion prioritizes features across modalities, enabling the model to focus on the most important data for a given task.

### Multimodal Learning
The integration of various trading analysis methodologies, including technical analysis, fundamental factors, and sentiment analysis, is emerging as a novel strategy for Forex prediction.
Numerous studies have sought to clarify this interaction by integrating sentiment data with traditional price patterns and technical indicators.
For instance, Farimani et al. have made significant contributions to this field through several notable studies that investigate diverse methodologies for integrating sentiment and technical indicators to improve forecasting.

### Forex Prediction
In the field of deep learning, several studies have utilized advanced models that leverage BERT embeddings to analyze essential data, including FFD, GDP, DAX, PPI, CPI, and technical indicators.
The Windsor and Cao investigate multimodal learning using a fusion-based LSTM model that analyzes sentiment from social media platforms, including Twitter and Sina microblogs, in combination with technical indicators such as EMA and MACD.
However, several research has prioritized sentiment analysis while neglecting the importance of effective data alignment or fusion, which is essential for a comprehensive understanding of multimodal forecasting.

### Model Development
The research introduces a novel method for integrating and evaluating market data and news events to improve trading decisions.
A multimodal model is developed that combines sentiment analysis and technical analysis via a cross-attention mechanism for fusion.
The model analyzes historical price data and news sentiment to predict Forex prices.
The cross-attention mechanism effectively captures the dynamic relationship between sentiment and technical indicators, thereby improving the model's ability to accurately predict the direction of price movement.

### Data Preprocessing
The research preprocesses the dataset by importing and examining the data, correcting missing or incorrect values, and incorporating technical indicators.
The dataset is then normalized using Z-scale normalization to ensure that each feature contributes equally to the model's performance.
The preprocessing phase also involves tokenizing the text data, summarizing articles using the FinBERT model, and classifying sentiment using a sophisticated sentiment analysis framework.

### Evaluation And Comparison
The research compares the multimodal approach with singular-module approaches and evaluates the model's performance using directional accuracy.
The results demonstrate the superiority of the multimodal method.
The research also examines the correlation between labeling strategies and their impact on model performance, providing insights into their relationships and facilitating the selection of complementary labeling strategies for robust model training.

### Sentiment Analysis
The Twitter-RoBERTa model is used for sentiment classification, allowing the detection of nuanced emotional cues during crises.
Sentiment categories are mapped into three main categories: Positive, Neutral, and Negative.
The strategy minimizes the risk of sentiment bias from media sources by aggregating articles across multiple sources.
TF-IDF analysis is applied to the summarized articles to assess the significance of a word in a document relative to its appearance in the entire dataset.

### Data Alignment
The alignment process involves pairing each news article with the most relevant price data point.
The algorithm pairs each news story with the most recent price data prior to publication to model short-term market reactions.
The sentiment analysis findings are matched to price movement data across various scenarios, ensuring consistency between the datasets while preserving the nuances of the news sentiment data.

### Multimodal Architecture
The multimodal framework integrates sentiment analysis and technical indicators.
The model employs neural networks for each modality, using fully connected layers to process sentiment and technical features.
Various attention mechanisms are evaluated, including self-attention, bi-directional cross-modal attention, and combined self-attention and bi-cross attention.
The bi-directional cross-modal attention technique enables mutual interaction between modalities, capturing complicated interactions between sentiment and technical data.

### Metrics
The study uses various metrics to evaluate model performance, including Directional Accuracy (DA), Matthews Correlation Coefficient (MCC), accuracy, precision, recall, and F1-score.
DA evaluates the model's ability to predict directional price movements, while MCC provides a robust measure of classification accuracy that accounts for imbalanced datasets.

### Model Performance
The technical analysis and sentiment analysis models are evaluated individually across three currency pairs (EUR/USD, GBP/USD, JPY/USD).
The results show that the technical analysis model performs better than the sentiment analysis model, but both models have limitations in predicting trend shifts.
The multimodal approach, which combines technical indicators and sentiment analysis, outperforms the individual models.
The Self-Attention with Bi-directional Cross-Attention Mode (SA_BA) demonstrates the most exceptional performance among the tested modes, with high accuracy and directional accuracy across currency pairs, including EUR/USD, GBP/USD, and JPY/USD.
The model achieves accuracies of 0.829 and 0.834, and MCCs of 0.744 and 0.752 for EUR/USD, and 0.852 and 0.776 for JPY/USD.

### Multimodal Approach
The multimodal approach is evaluated in different modes, including No Attention, Self-Attention, and Bi-Directional Cross-Attention.
The results show that the Self-Attention and Bi-Directional Cross-Attention modes outperform the No Attention mode, with the latter achieving the best performance.
The multimodal approach is shown to capture the complex interdependencies between market sentiment and historical trends, thereby improving predictive performance.
The Multimodal Approach, which combines technical and sentiment data, exhibits a distinct performance advantage over the Singular Approach, which relies solely on technical analysis or sentiment analysis.
The SA_BA model in the Multimodal Approach demonstrates superior performance, with higher accuracy, MCC, and directional accuracy compared to the Singular Approach models.

### Future Research
Future research directions include experimenting with alternative preprocessing approaches, such as subword-level tokenization and pre-trained contextual embeddings, and exploring feature-specific scaling methods to normalize technical indicators.
Additionally, dynamic window adaptation for rolling standard deviation-based labeling and the development of a front-end system for online, real-time testing and assessment are potential areas of investigation.


## Study subjects

### 3 major currency pairs
- The proposed model leverages innovative alignment techniques to synchronize sentiment from news articles with historical price trends, facilitating robust multiclass prediction of Forex price directions. To evaluate its effectiveness, the model was tested on three major currency pairs—EUR/USD, GBP/USD, and USD/JPY—using k-fold cross-validation. Multiple attention configurations, including no attention, self-attention, bi-cross attention, and a hybrid approach, were implemented to assess the impact of attention mechanisms on prediction performance

### 3 notable studies
- Numerous studies have sought to clarify this interaction by integrating sentiment data with traditional price patterns and technical indicators. For instance, [^Farimani_et+al_2021_a], [^Farimani_et+al_2022_a], 2024) have made significant contributions to this field through three notable studies. These studies investigate diverse methodologies for integrating sentiment and technical indicators to improve forecasting abilities, highlighting the increasing recognition of sentiment’s role as a complement to traditional trading metrics

## Data analysis
- #method/adjusted_standard_deviation_method
- #method/directional_method
- #method/price_change_direction_method
- #method/linear_regression
- #method/relative_strength_index
- #method/lstm_model
- #method/adjusted_threshold_method
- #method/singular_model
- #method/singular_approach_models
- #method/direction_method_show_weaker_correlations
- #method/finbert_model

## Findings
- The hybrid <a class="keyword" href="#" title="Long Short-Term Memory">LSTM</a> model, integrated with a rule-based decision framework, attains a notable profit accuracy of 73.09 % on <a class="keyword" href="https://en.wikipedia.org/wiki/currency_pair" title="currency pairs">currency pairs</a> such as EUR/USD, illustrating the capability of <a class="keyword" href="#" title="Long Short-Term Memory">LSTMs</a> to effectively capture both technical patterns and economic fluctuations in a dynamic market
- <mark class="claim">• EUR/USD: The model achieved an accuracy of 0.741, along with an MCC of 0.497, signifying a degree of predictive capability</mark>
- <mark class="fact">The module demonstrated a directional accuracy of approximately 76.5 %</mark>, indicating a reasonable level of reliability in identifying trend directions
- The self-<a class="keyword" href="https://en.wikipedia.org/wiki/attention_mechanism" title="attention mechanism">attention mechanism</a> emphasizes critical data points, enhancing the model’s understanding of trend behaviors with a directional accuracy of 80.1 %
- Its capacity to consistently identify directional trends is underscored by its directional accuracy of 80.9 %
- 0.752 0.834 0.819 0.844 0.832 0.836 would otherwise remain <mark class="fact">latent is indicated by robust F1-scores</mark> and directional accuracy of 83.4 %
- • EUR/USD: This mode reveals exceptional predictive accuracy, obtaining a directional accuracy of 82.2 %, with an accuracy of 0.829 and an <a class="keyword" href="https://en.wikipedia.org/wiki/Matthews_Correlation_Coefficient" title="Matthews Correlation Coefficient">MCC</a> of 0.744
- The model demonstrates a strong comprehension of the trend directions for JPY/USD, with a directional accuracy of 84.6 %
- The <a class="keyword" href="#" title="Self-Attention with Bi-directional Cross-Attention Mode">SA_BA</a> model achieved a directional accuracy of 81.9 %, which is higher than the Technical and Sentiment models’ accuracy of 66 % and 38.1 %, respectively
- Accuracy 85.2 % <a class="keyword" href="https://en.wikipedia.org/wiki/Matthews_Correlation_Coefficient" title="Matthews Correlation Coefficient">MCC</a>: 0.776 Directional Accuracy: 84.6 % AUC 0.955 integration of self-attention and bi-cross <a class="keyword" href="https://en.wikipedia.org/wiki/attention_mechanism" title="attention mechanisms">attention mechanisms</a>, enabling the model to capture interdependencies between news sentiment and <a class="keyword" href="https://en.wikipedia.org/wiki/technical_indicator" title="technical indicators">technical indicators</a> effectively

##  Builds on previous research
- However, none of these studies have focused on the Forex market. Therefore, we explore the field of Forex analysis by integrating multimodal attention mechanisms that have been previously effective outside of finance, such as in Alzheimer’s disease, using an attention-based deep learning framework that leverages several forms of data ([^Golovanevsky_et+al_2022_a]).

## Contributions
- In conclusion, the SA_BA Mode is superior to previous models, resulting in a level of predictive complexity that exceeds them. The advantages of a multi-attention framework for Forex market predictions are underscored by the comprehensive, sophisticated interaction among data streams facilitated by the integration of SA with bidirectional cross-attention. The significance of sophisticated attention mechanisms in improving the interpretability and accuracy of multimodal forecasting frameworks is underscored by the success of this model.

## Limitations
- The study focuses on short-term forecasting and does not incorporate fundamental analysis, which may be important for long-term forecasts. The model requires additional resources, such as organized datasets and processing overhead, to incorporate fundamental analysis.
- The study does not investigate cross-domain validation to analyze performance and the necessary modifications across different financial markets, which could be a limitation.

## Future work
- The study suggests that feature-specific scaling methods could be explored to ensure that technical indicators with different ranges are normalized in a way that preserves their unique interpretations. The research also proposes dynamic window adaptation for rolling standard deviation-based labeling, adjusting the window size according to changing market conditions.
- Future research could involve experimenting with alternative preprocessing approaches to enhance model robustness and performance, such as subword-level tokenization and pre-trained contextual embeddings.


## References
[^Anon_2022_a]: Anon. (2022). MMDL: A novel multi-modal deep learning model for stock market prediction. In Proceedings of the IEEE 9th International Conference on Data Science and Advanced Analytics (DSAA) (pp. 1–2). https://doi.org/10.1109/ DSAA54385.2022.10032436  [OA](https://doi.org/10.1109/DSAA54385.2022.10032436)  

[^Antelmi_et+al_2019_a]: Antelmi, L., Ayache, N., Robert, P., &amp; Lorenzi, M. (2019). Sparse multi-channel variational autoencoder for the joint analysis of heterogeneous data. In Proceedings of the International Conference on machine learning (pp. 302–311).  [OA](https://scholar.google.co.uk/scholar?q=Antelmi%2C%20L.%20Ayache%2C%20N.%20Robert%2C%20P.%20Lorenzi%2C%20M.%20Sparse%20multi-channel%20variational%20autoencoder%20for%20the%20joint%20analysis%20of%20heterogeneous%20data%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Antelmi%2C%20L.%20Ayache%2C%20N.%20Robert%2C%20P.%20Lorenzi%2C%20M.%20Sparse%20multi-channel%20variational%20autoencoder%20for%20the%20joint%20analysis%20of%20heterogeneous%20data%202019) 

[^Baek_et+al_2020_a]: Baek, S., Glambosky, M., Oh, S. H., &amp; Lee, J. (2020). Machine learning and algorithmic pairs trading in futures markets. Sustainability (Switzerland), 12(17). https://doi.org/10.3390/SU12176791  [OA](https://doi.org/10.3390/SU12176791)  [Scite](/scite_tallies?query=https://doi.org/10.3390/SU12176791)

[^Barbieri_et+al_2020_a]: Barbieri, F., Camacho-Collados, J., Neves, L., &; Espinosa-Anke, L. (2020). TWEETEVAL: Unified benchmark and comparative evaluation for tweet classification. Findings of the Association for Computational Linguistics ACL: EMNLP 2020 (pp. 1644–1650). https://doi.org/10.18653/V1/2020.FINDINGS-EMNLP.148  [OA](https://doi.org/10.18653/V1/2020.FINDINGS-EMNLP.148)  [Scite](/scite_tallies?query=https://doi.org/10.18653/V1/2020.FINDINGS-EMNLP.148)

[^Bintsi_et+al_2023_a]: Bintsi, K.-M., Baltatzis, V., Potamias, R. A., Hammers, A., &; Rueckert, D. (2023). Multimodal brain age estimation using interpretable adaptive population-graph learning. In Proceedings of the International Conference on Medical Image Computing and Computer-Assisted Intervention (pp. 195–204).  [OA](https://scholar.google.co.uk/scholar?q=Bintsi%2C%20K.-M.%20Baltatzis%2C%20V.%20Potamias%2C%20R.A.%20Hammers%2C%20A.%20Multimodal%20brain%20age%20estimation%20using%20interpretable%20adaptive%20population-graph%20learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Bintsi%2C%20K.-M.%20Baltatzis%2C%20V.%20Potamias%2C%20R.A.%20Hammers%2C%20A.%20Multimodal%20brain%20age%20estimation%20using%20interpretable%20adaptive%20population-graph%20learning%202023) 

[^Chantarakasemchit_et+al_2020_a]: Chantarakasemchit, O., Nuchitprasitchai, S., & Nilsiam, Y. (2020). Forex rate prediction for EUR/USD using the simple moving average and financial factors. In Proceedings of the 17th international conference on electrical engineering/electronics, computer, telecommunications and information technology, ECTI-CON 2020 (pp. 771–774). Institute of Electrical and Electronics Engineers Inc.. https://doi.org/10.1109/ECTI-CON49241.2020.9157907  [OA](https://doi.org/10.1109/ECTI-CON49241.2020.9157907)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ECTI-CON49241.2020.9157907)

[^Chen_et+al_2023_a]: Chen, Q., Li, M., Chen, C., Zhou, P., Lv, X., & Chen, C. (2023). MDFNet: Application of multimodal fusion method based on skin image and clinical data to skin cancer classification. Journal of Cancer Research and Clinical Oncology, 149(7), 3287–3299. https://doi.org/10.1007/S00432-022-04180-1/METRICS  [OA](https://doi.org/10.1007/S00432-022-04180-1/METRICS)  [Scite](/scite_tallies?query=https://doi.org/10.1007/S00432-022-04180-1/METRICS)

[^Cui_et+al_2023_a]: Cui, C., et al. (2023). Deep multimodal fusion of image and non-image data in disease diagnosis and prognosis: A review. Progress in Biomedical Engineering, 5(2), Article 022001. https://doi.org/10.1088/2516-1091/ACC2FE  [OA](https://doi.org/10.1088/2516-1091/ACC2FE)  [Scite](/scite_tallies?query=https://doi.org/10.1088/2516-1091/ACC2FE)

[^Dakalbab_et+al_2023_a]: Dakalbab, F. M., Talib, M. A., &amp; Nasir, Q. (2023). Machine learning-based trading robot for foreign exchange (FOREX). Lecture Notes in Networks and Systems, 721, 196–210. https://doi.org/10.1007/978-3-031-35308-6_17/COVER  [OA](https://doi.org/10.1007/978-3-031-35308-6_17/COVER)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-031-35308-6_17/COVER)

[^Dammu_et+al_2023_a]: Dammu, H., Ren, T., &amp; Duong, T. Q. (2023). Deep learning prediction of pathological complete response, residual cancer burden, and progression-free survival in breast cancer patients. PLOS ONE, 18(1), Article e0280148. https://doi.org/10.1371/ JOURNAL.PONE.0280148  [OA](https://doi.org/10.1371/JOURNAL.PONE.0280148)  [Scite](/scite_tallies?query=author%3ADammu%2Ctitle%3ADeep%20learning%20prediction%20of%20pathological%20complete%20response%2C%20residual%20cancer%20burden%2C%20and%20progression-free%20survival%20in%20breast%20cancer%20patients%2Cyear%3A2023)

[^Dang_2019_a]: Dang, Q. V. (2019). Reinforcement learning in stock trading. Advances in Intelligent Systems and Computing, 1121, 311–322. https://doi.org/10.1007/978-3-030-383640_28  [OA](https://doi.org/10.1007/978-3-030-383640_28)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-030-383640_28)

[^Dautel_et+al_2020_a]: Dautel, A. J., Hardle, W. K., Lessmann, S., &amp; Seow, H.-V. (2020). Forex exchange rate forecasting using deep recurrent neural networks. Digital Finance, 2(1–2), 69–96. https://doi.org/10.1007/s42521-020-00019-x  [OA](https://doi.org/10.1007/s42521-020-00019-x)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s42521-020-00019-x)

[^Dymova_et+al_2016_a]: Dymova, L., Sevastjanov, P., &amp; Kaczmarek, K. (2016). A FOREX trading expert system based on a new approach to the rule-based evidential reasoning. Expert Systems with Applications, 51, 1–13. https://doi.org/10.1016/j.eswa.2015.12.028  [OA](https://doi.org/10.1016/j.eswa.2015.12.028)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2015.12.028)

[^Farimani_et+al_2021_a]: Farimani, S. A., Jahan, M. V., Fard, A. M., &amp; Haffari, G. (2021). Leveraging latent economic concepts and sentiments in the news for market prediction. In Proceedings of the IEEE 8th International Conference on Data Science and Advanced Analytics (DSAA) (pp. 1–10).  [OA](https://scholar.google.co.uk/scholar?q=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Haffari%2C%20G.%20Leveraging%20latent%20economic%20concepts%20and%20sentiments%20in%20the%20news%20for%20market%20prediction%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Haffari%2C%20G.%20Leveraging%20latent%20economic%20concepts%20and%20sentiments%20in%20the%20news%20for%20market%20prediction%202021) 

[^Farimani_et+al_2022_a]: Farimani, S. A., Vafaei Jahan, M., Milani Fard, A., &amp; Tabbakh, S. R. K. (2022). Investigating the informativeness of technical indicators and news sentiment in financial market price prediction. Knowledge-Based Systems, 247, Article 108742. https://doi.org/10.1016/j.knosys.2022.108742  [OA](https://doi.org/10.1016/j.knosys.2022.108742)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.knosys.2022.108742)

[^Farimani_et+al_2024_a]: Farimani, S. A., Jahan, M. V., &amp; Fard, A. M. (2024). An adaptive multimodal learning model for financial market price prediction. IEEE Access, 12, 121846–121863. https://doi.org/10.1109/ACCESS.2024.3441029  [OA](https://doi.org/10.1109/ACCESS.2024.3441029)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2024.3441029)

[^Fataliyev_2023_a]: Fataliyev, K., &amp; Liu, W. (2023). MCASP: Multi-modal cross attention network for stock market prediction. In Proceedings of the 21st annual workshop of the Australasian language technology association (pp. 67–77).  [OA](https://scholar.google.co.uk/scholar?q=Fataliyev%2C%20K.%20Liu%2C%20W.%20MCASP%3A%20Multi-modal%20cross%20attention%20network%20for%20stock%20market%20prediction%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Fataliyev%2C%20K.%20Liu%2C%20W.%20MCASP%3A%20Multi-modal%20cross%20attention%20network%20for%20stock%20market%20prediction%202023) 

[^Faulkner_2017_a]: Faulkner, A. E. (2017). Global financial data. Journal of Business &amp; Finance Librarianship, 22(1), 61–67. https://doi.org/10.1080/08963568.2017.1264051  [OA](https://doi.org/10.1080/08963568.2017.1264051)  [Scite](/scite_tallies?query=https://doi.org/10.1080/08963568.2017.1264051)

[^Ferreira_et+al_2021_a]: Ferreira, F. G. D. C., Gandomi, A. H., &amp; Cardoso, R. T. N. (2021). Artificial intelligence applied to stock market trading: A review. IEEE Access, 9, 30898–30917. https://doi.org/10.1109/ACCESS.2021.3058133  [OA](https://doi.org/10.1109/ACCESS.2021.3058133)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2021.3058133)

[^Gai_et+al_2018_a]: Gai, K., Qiu, M., &amp; Sun, X. (2018). A survey on FinTech. Journal of Network and Computer Applications, 103, 262–273. https://doi.org/10.1016/J.JNCA.2017.10.011  [OA](https://doi.org/10.1016/J.JNCA.2017.10.011)  [Scite](/scite_tallies?query=https://doi.org/10.1016/J.JNCA.2017.10.011)

[^Golovanevsky_et+al_2022_a]: Golovanevsky, M., Eickhoff, C., &amp; Singh, R. (2022). Multimodal attention-based deep learning for Alzheimer’s disease diagnosis. Journal of the American Medical Informatics Association, 29(12), 2014–2022. https://doi.org/10.1093/jamia/ocac168  [OA](https://doi.org/10.1093/jamia/ocac168)  [Scite](/scite_tallies?query=https://doi.org/10.1093/jamia/ocac168)

[^Gr_2024_a]: Grądzki, P., &amp; Wojcik, P. (2024). Is attention all you need for intraday FOREX trading? Expert Systems, 41(2). https://doi.org/10.1111/EXSY.13317  [OA](https://doi.org/10.1111/EXSY.13317)  [Scite](/scite_tallies?query=https://doi.org/10.1111/EXSY.13317)

[^Hajek_et+al_2022_a]: P. Hajek, J. Novotny, J. K., the 2022 6th I. C., and undefined 2022, “Predicting exchange rate with FinBERT-based sentiment analysis of online news,” dl.acm.org, pp. 133–138, Oct. 2022, doi:10.1145/3572647.3572667.  [OA](https://doi.org/10.1145/3572647.3572667)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3572647.3572667)

[^King_et+al_2012_a]: King, M. R., Osler, C., &; Rime, D. (2012). Foreign exchange market structure, players, and evolution. Handbook of exchange rates (pp. 2–44). John Wiley &amp; Sons, Ltd. https://doi.org/10.1002/9781118445785.ch1  [OA](https://doi.org/10.1002/9781118445785.ch1)  [Scite](/scite_tallies?query=https://doi.org/10.1002/9781118445785.ch1)

[^Leles_et+al_2019_a]: Leles, M. C. R., Sbruzzi, E. F., De Oliveira, J. M. P., &amp; Nascimento, C. L. (2019). Trading switching setup based on reinforcement learning applied to a multiagent system simulation of financial markets. In Proceedings of the SysCon 2019 - 13th annual IEEE international systems conference. Institute of Electrical and Electronics Engineers Inc.. https://doi.org/10.1109/SYSCON.2019.8836887  [OA](https://doi.org/10.1109/SYSCON.2019.8836887)  [Scite](/scite_tallies?query=https://doi.org/10.1109/SYSCON.2019.8836887)

[^Li_et+al_2015_a]: Li, W., Wong, M. C. S., &amp; Cenev, J. (2015). High frequency analysis of macro news releases on the foreign exchange market: A survey of literature. Big Data Research, 2 (1), 33–48. https://doi.org/10.1016/j.bdr.2015.02.003  [OA](https://doi.org/10.1016/j.bdr.2015.02.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.bdr.2015.02.003)

[^Li_et+al_2020_a]: Li, Y., Ni, P., &amp; Chang, V. (2020). Application of deep reinforcement learning in stock trading strategies and stock forecasting. Computing, 102(6), 1305–1322. https://doi.org/10.1007/s00607-019-00773-w  [OA](https://doi.org/10.1007/s00607-019-00773-w)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s00607-019-00773-w)

[^Li_et+al_2020_b]: Li, Q., Tan, J., Wang, J., &amp; Chen, H. (2020). A multimodal event-driven LSTM model for stock prediction using online news. IEEE Transactions on Knowledge and Data Engineering, 33(10), 3323–3337.  [OA](https://engine.scholarcy.com/oa_version?query=Li%2C%20Q.%20Tan%2C%20J.%20Wang%2C%20J.%20Chen%2C%20H.%20A%20multimodal%20event-driven%20LSTM%20model%20for%20stock%20prediction%20using%20online%20news%202020&author=Li&title=A%20multimodal%20event-driven%20LSTM%20model%20for%20stock%20prediction%20using%20online%20news&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Li%2C%20Q.%20Tan%2C%20J.%20Wang%2C%20J.%20Chen%2C%20H.%20A%20multimodal%20event-driven%20LSTM%20model%20for%20stock%20prediction%20using%20online%20news%202020) [Scite](/scite_tallies?query=author%3ALi%2Ctitle%3AA%20multimodal%20event-driven%20LSTM%20model%20for%20stock%20prediction%20using%20online%20news%2Cyear%3A2020)

[^Ma_et+al_2023_a]: Ma, N., et al. (2023). Comprehensive investigation of the MMR gene in hepatocellular carcinoma with chronic hepatitis B virus infection in the Han Chinese population. Frontiers in Oncology, 13. https://doi.org/10.3389/fonc.2023.1124459  [OA](https://doi.org/10.3389/fonc.2023.1124459)  [Scite](/scite_tallies?query=https://doi.org/10.3389/fonc.2023.1124459)

[^Munkhdalai_et+al_2019_a]: Munkhdalai, L., Munkhdalai, T., Park, K. H., Lee, H. G., Li, M., &amp; Ryu, K. H. (2019). Mixture of activation functions with extended min-max normalization for FOREX market prediction. IEEE Access, 7, 183680–183691. https://doi.org/10.1109/ ACCESS.2019.2959789  [OA](https://doi.org/10.1109/ACCESS.2019.2959789)  [Scite](/scite_tallies?query=author%3AMunkhdalai%2Ctitle%3AMixture%20of%20activation%20functions%20with%20extended%20min-max%20normalization%20for%20FOREX%20market%20prediction%2Cyear%3A2019)

[^Nassirtoussi_et+al_2015_a]: Nassirtoussi, A. K., Aghabozorgi, S., Wah, T. Y., &amp; Ngo, D. C. L. (2015). Text mining of news-headlines for FOREX market prediction: A multi-layer dimension reduction algorithm with semantics and sentiment. Expert Systems with Applications, 42(1), 306–324.  [OA](https://engine.scholarcy.com/oa_version?query=Nassirtoussi%2C%20A.K.%20Aghabozorgi%2C%20S.%20Wah%2C%20T.Y.%20Ngo%2C%20D.C.L.%20Text%20mining%20of%20news-headlines%20for%20FOREX%20market%20prediction%3A%20A%20multi-layer%20dimension%20reduction%20algorithm%20with%20semantics%20and%20sentiment%202015&author=Nassirtoussi&title=Text%20mining%20of%20news-headlines%20for%20FOREX%20market%20prediction%3A%20A%20multi-layer%20dimension%20reduction%20algorithm%20with%20semantics%20and%20sentiment&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Nassirtoussi%2C%20A.K.%20Aghabozorgi%2C%20S.%20Wah%2C%20T.Y.%20Ngo%2C%20D.C.L.%20Text%20mining%20of%20news-headlines%20for%20FOREX%20market%20prediction%3A%20A%20multi-layer%20dimension%20reduction%20algorithm%20with%20semantics%20and%20sentiment%202015) [Scite](/scite_tallies?query=author%3ANassirtoussi%2Ctitle%3AText%20mining%20of%20news-headlines%20for%20FOREX%20market%20prediction%3A%20A%20multi-layer%20dimension%20reduction%20algorithm%20with%20semantics%20and%20sentiment%2Cyear%3A2015)

[^Pornwattanavichai_et+al_2022_a]: Pornwattanavichai, A., Maneeroj, S., &amp; Boonsiri, S. (2022). BERTFOREX: Cascading model for FOREX market forecasting using fundamental and technical indicator data based on BERT. IEEE Access, 10, 23425–23437. https://doi.org/10.1109/ ACCESS.2022.3152152  [OA](https://doi.org/10.1109/ACCESS.2022.3152152)  [Scite](/scite_tallies?query=author%3APornwattanavichai%2Ctitle%3ABERTFOREX%3A%20Cascading%20model%20for%20FOREX%20market%20forecasting%20using%20fundamental%20and%20technical%20indicator%20data%20based%20on%20BERT%2Cyear%3A2022)

[^Ramachandram_2017_a]: Ramachandram, D., &amp; Taylor, G. W. (2017). Deep multimodal learning: A survey on recent advances and trends. IEEE Signal Processing Magazine, 34(6), 96–108. https://doi.org/10.1109/MSP.2017.2738401  [OA](https://doi.org/10.1109/MSP.2017.2738401)  [Scite](/scite_tallies?query=https://doi.org/10.1109/MSP.2017.2738401)

[^Semiromi_et+al_2020_a]: Semiromi, H. N, Lessmann, S., &amp; Peters, W. (2020). News will tell: Forecasting foreign exchange rates based on news story events in the economy calendar. North American Journal of Economics and Finance, 52, Article 101181. https://doi.org/10.1016/j.najef.2020.101181  [OA](https://doi.org/10.1016/j.najef.2020.101181)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.najef.2020.101181)

[^Townend_et+al_2024_a]: Townend, F., Roddy, P. J., &amp; Goebl, P. (2024). florencejt/fusilli: Fusilli v1.1.0 (v1.1.0). Zenodo. https://doi.org/10.5281/zenodo.10463697.  [OA](https://doi.org/10.5281/zenodo.10463697)  [Scite](/scite_tallies?query=https://doi.org/10.5281/zenodo.10463697)

[^Vaswani_et+al_2017_a]: Vaswani, A., Noam, S., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N.,... Polosukhin, I. (2017). Attention is all you need. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, &amp; R. Garnett (Eds.), 30. Advances in neural information processing systems. Curran Associates, Inc.  [OA](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Noam%2C%20S.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20is%20all%20you%20need%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Noam%2C%20S.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20is%20all%20you%20need%202017) 

[^Windsor_2022_a]: Windsor, E., &amp; Cao, W. (2022). Improving exchange rate forecasting via a new deep multimodal fusion model. Applied Intelligence, 52(14), 16701–16717.  [OA](https://engine.scholarcy.com/oa_version?query=Windsor%2C%20E.%20Cao%2C%20W.%20Improving%20exchange%20rate%20forecasting%20via%20a%20new%20deep%20multimodal%20fusion%20model%202022&author=Windsor&title=Improving%20exchange%20rate%20forecasting%20via%20a%20new%20deep%20multimodal%20fusion%20model&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Windsor%2C%20E.%20Cao%2C%20W.%20Improving%20exchange%20rate%20forecasting%20via%20a%20new%20deep%20multimodal%20fusion%20model%202022) [Scite](/scite_tallies?query=author%3AWindsor%2Ctitle%3AImproving%20exchange%20rate%20forecasting%20via%20a%20new%20deep%20multimodal%20fusion%20model%2Cyear%3A2022)

[^Yang_et+al_2018_a]: Yang, S. Y., Yu, Y., &amp; Almahdi, S. (2018). An investor sentiment reward-based trading system using a Gaussian inverse reinforcement learning algorithm. Expert Systems with Applications, 114, 388–401. https://doi.org/10.1016/J.ESWA.2018.07.056  [OA](https://doi.org/10.1016/J.ESWA.2018.07.056)  [Scite](/scite_tallies?query=https://doi.org/10.1016/J.ESWA.2018.07.056)

[^Yang_2023_a]: Yang, H. (2023). Multimodal stock price forecasting using an attention mechanism based on multi-task learning. In Proceedings of the Asia-Pacific Web (APWeb) and Web-Age Information Management (WAIM) Joint International Conference on Web and Big Data (pp. 454–468).  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20H.%20Multimodal%20stock%20price%20forecasting%20using%20attention%20mechanism%20based%20on%20multi-task%20learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20H.%20Multimodal%20stock%20price%20forecasting%20using%20attention%20mechanism%20based%20on%20multi-task%20learning%202023) 

[^Y_et+al_2021_a]: Yıldırım, D. C., Toroslu, I. H., &amp; Fiore, U. (2021). Forecasting directional movement of FOREX data using LSTM with technical and macroeconomic indicators. Financial Innovation, 7(1), 1–36. https://doi.org/10.1186/s40854-020-00220-2  [OA](https://doi.org/10.1186/s40854-020-00220-2)  [Scite](/scite_tallies?query=https://doi.org/10.1186/s40854-020-00220-2)

[^Zeng_2020_a]: Zeng, Z., &amp; Khushi, M. (2020). Wavelet denoising and an attention-based RNN-ARIMA model for predicting FOREX prices. In Proceedings of the international joint conference on neural networks. Institute of Electrical and Electronics Engineers Inc.. https://doi.org/10.1109/IJCNN48605.2020.9206832  [OA](https://doi.org/10.1109/IJCNN48605.2020.9206832)  [Scite](/scite_tallies?query=https://doi.org/10.1109/IJCNN48605.2020.9206832)

