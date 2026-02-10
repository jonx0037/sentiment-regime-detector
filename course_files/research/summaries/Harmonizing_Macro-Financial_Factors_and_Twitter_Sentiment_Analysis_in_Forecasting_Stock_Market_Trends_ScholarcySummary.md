[[Amin_et+al_HarmonizingMacrofinancialFactorsTwitterSentiment_2024]]

# [Harmonizing Macro-Financial Factors and Twitter Sentiment Analysis in Forecasting Stock Market Trends](https://doi.org/10.32996/jcsts)

## [[Md Shahedul Amin]]; [[✉]]; [[Eftekhar Hossain Ayon]] et al

## Abstract

ABSTRACT: The surge in generative artificial intelligence technologies, exemplified by systems such as ChatGPT, has sparked widespread interest and discourse, prominently observed on social media platforms such as Twitter. This paper examines whether sentiment expressed in tweets discussing advancements in AI can forecast day-to-day fluctuations in the stock prices of associated companies. Our investigation involves analyzing tweets containing hashtags related to ChatGPT from December 2022 to March 2023. Leveraging natural language processing techniques, we extract features, including positive/negative sentiment scores, from the collected tweets. A range of machine learning classification models, including gradient boosting, decision trees, and random forests, are trained on tweet sentiments and associated features to predict stock price movements for key companies, such as Microsoft and OpenAI. These models undergo training and testing phases using an empirical dataset collected during the specified timeframe. Our preliminary findings reveal intriguing indications of a plausible correlation between public sentiment reflected in Twitter discussions surrounding ChatGPT and generative AI and the subsequent impact on market valuation and trading activities for pertinent companies, as gauged by stock prices. This study aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets. In conjunction with this Twitter-based sentiment analysis, we incorporate control variables including macroeconomic indicators, the Twitter uncertainty index, and stock market data for several prominent companies.

## Key concepts

# claim/ChatGPT; #ChatGPT; #consumer_price_index; #sentiment_analysis; #market_trend; #social_media; #claim/stock_price; #stock_price; #tweets; #claim/stock_market; #stock_market

## Quote
>
> The study evaluates the performance of various machine learning models, including Random Forest, Decision Tree, Extra Tree, Gradient Boosting, and Naive Bayes, in predicting stock market trends, with Random Forest demonstrating robust performance in identifying both Bearish and Bullish trends.

## Key points

- The sentiment analysis of tweets spanning December 2022 to March 2023 holds the potential to significantly impact the stock trends of various influential companies
- 1. Conclusion: The analysis of Twitter data in anticipation of stock market trends presents a compelling narrative when juxtaposed against macroeconomic indicators and company-specific stock data
- This multifaceted approach seeks to unravel the intricate interplay between sentiment analysis derived from social media, broader economic conditions, and the individual performance of companies in the stock market
- The integration of sentiment analysis from Twitter data alongside macroeconomic indicators offers a holistic view of market sentiment
- Incorporating company-specific stock data, including financial reports, revenue, and earnings, provides granular insights into individual stock performance. This holistic approach illuminates the intricate relationships between sentiment, economic conditions, and market dynamics. It unveils the potential synergy between social sentiment and economic indicators in predicting market trends, offering a more comprehensive understanding of market behavior
- In identifying Bullish trends, Random Forest again emerged with the highest accuracy of 100%, followed by Decision Tree (89%) and Gradient Boosting (93%)
- While sentiment analysis offers a window into public perception, its amalgamation with broader economic indicators and detailed company-specific data augments predictive models, fostering a nuanced comprehension of market behavior and trends

## Summary

### Introduction

The study examines the relationship between sentiment expressed in tweets about AI advancements and day-to-day fluctuations in the stock prices of associated companies.
The investigation involves analyzing tweets containing hashtags related to ChatGPT from December 2022 to March 2023.
The research aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets.

### Methodology

The study employs natural language processing techniques to extract features, including positive/negative sentiment scores, from the collected tweets.
A range of machine learning classification models, including gradient boosting, decision trees, and random forests, are used to train on tweet sentiments and associated features to predict stock price movements for key companies.
The features extracted from Twitter data are systematically linked to daily stock prices, and supervised learning models are trained on the amalgamated paired dataset.
The study employs sentiment analysis of the tweet dataset to forecast bullish or bearish stock market trends.
The analysis integrates Twitter-derived sentiment with control variables, including the Consumer Confidence Index, Unemployment Rate, and Consumer Price Index.
The study also incorporates company-specific stock market data, including the Stock Market Uncertainty Index and Volume.
Feature engineering involves computing sentiment scores, including positive, neutral, and negative sentiments, and introducing a small value to prevent potential issues arising from zero values.

### Literature Review

Prior research has utilized sentiment analysis of Twitter messages to construct a daily happiness index, offering insights into the influence of social media on financial markets.
Studies have also explored the influence of social media sentiment on stock market volatility, elucidating the effects of sentiments linked to significant global events on investor attitudes and transactional trading metrics.
The application of machine learning methodologies has been instrumental in developing predictive models that assess the relationship between tweet content and stock prices, underscoring the promise of machine learning for predicting future stock prices through sentiment analysis.

### Data

The study combines tweet data related to ChatGPT with historical stock prices of five technology giants - Google, Amazon, Meta, Nvidia, and Microsoft - from December 2022 to March 2023.
The dataset includes over 500,000 tweets and 90 trading days of historical price data.
The fusion of these datasets enables correlating daily Twitter sentiment and engagement metrics with end-of-day stock price movements.

### Results

The study evaluates the performance of various classification models, including Random Forest, Decision Tree, Extra Trees Classifier, and Naive Bias Classifier, in predicting stock market trends.
The models are trained on a subset of the dataset and validated on an independent section.
The evaluation metrics include accuracy, F1, and recall scores.
The results show that Random Forest performs strongly, achieving high accuracy and recall in identifying bearish and bullish trends.

### Models

Random Forest achieved high accuracy, recall, and F1 scores in identifying both Bearish and Bullish trends, demonstrating its potential as an effective model for financial market trend prediction.
Decision Tree and Extra Tree also exhibited commendable performance, while Gradient Boosting and Naive Bayes showed relatively lower predictive performance.
However, Gradient Boosting achieved the highest accuracy score for both bullish and bearish predictions in certain scenarios, followed by Random Forest and Decision Tree.

### Predictions

The analysis of Twitter data to anticipate stock market trends presents a compelling narrative when juxtaposed with macroeconomic indicators and company-specific stock data.
The integration of sentiment analysis from Twitter data alongside macroeconomic indicators offers a holistic view of market sentiment.
The quantitative assessment of sentiment provides valuable insights, with models such as Random Forests achieving high accuracy, recall, and F1 scores.

### Trends

The convergence of sentiment analysis with macroeconomic indicators and company-specific data further enriches the predictive landscape.
While sentiment analysis captures public perception and emotions, macroeconomic indicators offer a broader economic context.
Incorporating company-specific stock data provides granular insights into individual stock performance, illuminating the intricate relationships between sentiment, economic conditions, and market dynamics.
This holistic approach unveils the potential synergy between social sentiment and economic indicators in predicting market trends.

## Study subjects

### 500000 tweets

- Our preliminary findings reveal intriguing indications suggesting a plausible correlation between public sentiment reflected in Twitter discussions surrounding ChatGPT and generative AI and the subsequent impact on market valuation and trading activities concerning pertinent companies, gauged through stock prices. This study aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets. In conjunction with this sentiment analysis derived from Twitter, we incorporate control variables encompassing macroeconomic indicators, Twitter uncertainty index, and stock market data for several prominent companies

### 500000 tweets

- This research embarks on an exploration leveraging two prominent datasets recently published, both offering distinct yet complementary dimensions to the study. Firstly, the 500k ChatGPT-related Tweets dataset, sourced from Kaggle and meticulously curated by users, comprises over 500,000 tweets spanning December 2022 to March 2023. This rich dataset encompasses diverse attributes, including tweet text, temporal information, engagement metrics such as likes and retweets, user follower counts, and sentiment evaluations, all intricately associated with the ChatGPT conversational AI system

## Data analysis

- #method/consumer_price_index
- #method/twitter_uncertainty_index
- #method/gradient_boosting_classifier_model
- #method/consumer_confidence_index

## Findings

- For the identification of Bearish trends, Random Forest emerged as a prominent performer, showcasing a notable accuracy score of 82%, closely followed by Decision Tree at 81% and Extra Tree at 76%
- Gradient Boosting and Naive Bayes exhibited comparatively lower accuracies of 74% and 68%, respectively
- Extra Tree and Decision Tree followed with accuracies of 89% and 85%, respectively, while Gradient Boosting and Naive Bayes exhibited lower accuracy rates of 95% and 73%
- In Table 3, identifying Google Stock Bearish trends, Random Forest exhibited the highest accuracy at 96%, followed by Gradient Boosting (98%) and Extra Trees (90%)
- In identifying Bullish trends, Random Forest again emerged with the highest accuracy of 100%, followed by Decision Tree (89%) and Gradient Boosting (93%)

## Contributions

- In summary, the application of machine learning classifiers such as gradient boosting, decision tree, random forest, naive Bayes, and <mark class="fact">extra tree classifiers has been extensively explored in predicting stock market trends and prices</mark>. These models have been applied across diverse contexts and optimized for improved performance, demonstrating the significance of machine learning in stock market prediction.

## Limitations

- The study does not explicitly state its limitations, but it can be inferred that the study is limited to the analysis of tweets containing hashtags related to ChatGPT and the stock prices of key companies such as Microsoft and OpenAI. The study also relies on the accuracy of the natural language processing techniques and machine learning models used to extract features and predict stock price movements.
- The study does not discuss any limitations of the research, but potential limitations could include the limited scope of the study to five major tech companies and the potential for bias in the Twitter sentiment data.
- The limitations of the study include the potential overfitting or insufficient feature importance considerations of certain models, such as Decision Tree, and the limited suitability of models like Naive Bayes and Extra Tree for this task.

## Future work

- The study suggests that future research can focus on exploring the application of machine learning methodologies in constructing predictive models that assess the interconnection between tweet content and stock values. The study also suggests that future research can investigate the influence of social media rumors on stock market volatility.
- The study suggests that future work could involve exploring the use of other social media platforms and machine learning models to predict stock market trends.

## References
