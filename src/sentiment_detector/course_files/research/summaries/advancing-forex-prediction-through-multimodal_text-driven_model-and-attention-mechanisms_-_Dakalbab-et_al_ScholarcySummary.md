[[Dakalbab_et+al_AdvancingForexPredictionThroughMultimodal_2025]]

# [Advancing Forex prediction through multimodal text-driven model and attention mechanisms](https://doi.org/10.1016/j.iswa.2025.200518)

## [[Fatima Dakalbab]]; [[Ayush Kumar]]; [[Manar Abu Talib]] et al

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

[^Farimani_et+al_2021_a]: Farimani, S. A., Jahan, M. V., Fard, A. M., &amp; Haffari, G. (2021). Leveraging latent economic concepts and sentiments in the news for market prediction. In Proceedings of the IEEE 8th International Conference on Data Science and Advanced Analytics (DSAA) (pp. 1–10).  [OA](https://scholar.google.co.uk/scholar?q=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Haffari%2C%20G.%20Leveraging%20latent%20economic%20concepts%20and%20sentiments%20in%20the%20news%20for%20market%20prediction%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Haffari%2C%20G.%20Leveraging%20latent%20economic%20concepts%20and%20sentiments%20in%20the%20news%20for%20market%20prediction%202021)

[^Farimani_et+al_2022_a]: Farimani, S. A., Vafaei Jahan, M., Milani Fard, A., &amp; Tabbakh, S. R. K. (2022). Investigating the informativeness of technical indicators and news sentiment in financial market price prediction. Knowledge-Based Systems, 247, Article 108742. <https://doi.org/10.1016/j.knosys.2022.108742>  [OA](https://doi.org/10.1016/j.knosys.2022.108742)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.knosys.2022.108742)

[^Golovanevsky_et+al_2022_a]: Golovanevsky, M., Eickhoff, C., &amp; Singh, R. (2022). Multimodal attention-based deep learning for Alzheimer’s disease diagnosis. Journal of the American Medical Informatics Association, 29(12), 2014–2022. <https://doi.org/10.1093/jamia/ocac168>  [OA](https://doi.org/10.1093/jamia/ocac168)  [Scite](/scite_tallies?query=https://doi.org/10.1093/jamia/ocac168)
