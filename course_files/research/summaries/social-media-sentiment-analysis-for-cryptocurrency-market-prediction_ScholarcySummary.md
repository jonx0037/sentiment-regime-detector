[[Raheman_et+al_SocialMediaSentimentAnalysisCryptocurrency_2022]]

# [Social Media Sentiment Analysis for Cryptocurrency Market Prediction](https://doi.org/10.48550/arxiv.2204.10185)

## [[Ali Raheman]]; [[Anton Kolonin]]; [[Igors Fridkins]] et al

## Abstract

In this paper, we explore the usability of various natural language processing models for sentiment analysis of social media content applied to financial market prediction, using the cryptocurrency domain as a reference. We examine how different sentiment metrics correlate with Bitcoin's price movements. For this purpose, we explore different methods for calculating sentiment metrics from text, finding that most are not very accurate for this prediction task. We find that one of the models outperforms more than 20 other public models and allows efficient fine-tuning, given its interpretable nature. Thus, we confirm that interpretable artificial intelligence and natural language processing methods might be more valuable in practice than non-explainable, non-interpretable ones. In the end, we analyse potential causal connections between the different sentiment metrics and the price movements.

## Key concepts

# cryptocurrency; #machine_learning; #claim/metrics; #metrics; #sentiment_analysis; #claim/natural_language_processing; #natural_language_processing; #interpretable_artificial_intelligence

## Quote

The study evaluates 21 sentiment analysis models on a cryptocurrency dataset, fine-tunes the top-performing model, and explores the causal relationship between social media sentiment and price movements, with results indicating a potential link between sentiment metrics and price changes.

## Key points

- We are well aware of how much social media is connected to everyone's life and the impact it has on it
- Given a much clearer maximum at -1 day lag with a correlation value as high as 0.55, compared with values corresponding to other lags, we can assume that selective inclusion and weighting of the news metrics and channels enable finding more causally connected time series, which builds up compound sentiment indicators that are potentially valuable for further feature engineering for the price prediction purposes
- We have shown how an “interpretable” sentiment analysis model could be significantly improved manually and without the huge costs for training the domain-specific corpus and creating and tagging this corpus for said purpose
- We are exploring how to automate this process of using the price movements as an implicit tagging of the sentiment-rich text data and learning the indicative n-grams from the temporally aligned market and news media data, with the option for manual review on the discovered patterns within the “interpretable” mode
- We are looking forward to improving the performance of the best model further
- Our future work in this area will be dedicated to exploring the predictive power of the connection to improve the reliability of the price prediction and business applications for decentralized finance relying on such predictions

## Summary

### Introduction

The paper explores the use of natural language processing models for sentiment analysis of social media to predict cryptocurrency market movements.
The study focuses on Bitcoin and uses data from Twitter and Reddit.
The goal is to determine if sentiment scores can be used for price prediction.

### Methodology

The study involves a literature survey of publicly available sentiment models, data collection from Twitter and Reddit, data processing using various models, and performance evaluation.
The best model, AI agents, is fine-tuned and re-evaluated, resulting in a significant increase in the correlation between sentiment score and price movement.

### Results

The study evaluates 21 different sentiment models and finds that the AI agents model outperforms the others.
The model is based on "n-grams" and is interpretable, allowing fine-tuning and improving its performance.
The correlation between the improved AI agents model sentiment score and price movement increases from 0.33 to 0.57.
The study also explores possible causal links between sentiment metrics and price movements, analyzing the mutual Pearson correlation between daily Bitcoin price changes and sentiment metrics.
The evaluation of the 21 models was performed using the Pearson correlation coefficient, with the fine-tuned AI agents model achieving the highest correlation of 0.57.
The study also explored the potential causal connection between social media sentiment and price movements, finding a peak in correlation at a-2-day shift for overall sentiment and positive metrics.
The automated process of building compound sentiment indicators was employed to increase the power of such connections, with a maximum correlation value of 0.55 at a -1 day lag.

### Models

The experiments used 15 BERT-based models trained on different datasets, including DistilBERT-base-uncased, finiteautomata/BERTweet-base-sentiment-analysis, and cardiffnlp/twitter-roBERTa-base-sentiment.
Other models used include ProsusAI/finBERT, moussaKam/barthez-sentiment-classification, and textattack/BERT-base-uncased-imdb.
The base models used were BERT, RoBERTa, and DistilRoBERTa, and were fine-tuned on various datasets such as IMDB, Yelp polarity, and tweets_hate_speech_detection.

### Challenges

The experiments encountered several challenges, including sarcasm, idioms, and negations, which can make it difficult for sentiment models to understand the true context of texts.
Non-text data, such as images and videos, can also contain strong indications of price change that may be missed by sentiment models.
These challenges can lead to misclassification and lower model accuracy.

## Study subjects

### 490 tweets

- The data collection process has been based on official Reddit and Twitter APIs and was performed exclusively on public posts in public feeds. For the purpose of the algorithm quality assessment, we have used 490 tweets/posts from 5 randomly selected Twitter public feeds. The tweets/ posts have been manually classified for both positive and negative sentiment in the range [-1.0,0.0] and [0.0,+1.0] respectively by two independent reviewers, and made the “ground truth” sentiment assessment as the average of the two assessments for positive and negative metrics

### 10 independent people

- It is a lexicon and rule-based sentiment model specially created for texts in social media. It has over 9,000 words, and each word was rated by 10 independent people on a scale from -4 (extremely negative) to 4 (extremely positive). The final score is the average of all 10 ratings [^2]. TextBlob

## Data analysis

- #method/pearson_correlation
- #method/AI agents_model
- #method/pearson_correlation_coefficient

## Findings

- <mark class="claim">We are looking forward to improving the performance of the best model further</mark>

## Builds on previous research

- 8 following the concepts of causal analysis on time series discussed in [^15], as shown in Figure 2. We can see that the plots corresponding to overall sentiment and positive metrics are presenting peaks in the correlation value at a -2-day shift.

## Contributions

- In this paper, <mark class="claim">we have found the most reliable model for social media sentiment analysis in the cryptocurrency domain</mark>. <mark class="claim"><mark class="fact">We have shown how an “interpretable” sentiment analysis model could be significantly improved</mark> manually and without the huge costs for training the domain-specific corpus and creating and tagging this corpus for said purpose</mark>. In our further work, <mark class="fact">we are exploring how to automate this process of using the price movements being an implicit tagging of the sentiment-rich text data</mark> and learning the indicative n-grams from the temporally aligned market and news media data, with the option for manual review on the discovered patterns within the “interpretable” mode. <mark class="claim">We are looking forward to improving the performance of the best model further</mark>.

## Limitations

- The study has several limitations, including the use of a limited dataset and the reliance on manual classification of tweets/posts. The study also notes that the models used are imperfect and may be biased.
- The limitations of the study include the challenges of sentiment analysis, such as sarcasm, idioms, and negations, which can affect the accuracy of the models. The study also notes that the correlation between social media sentiment and price movements is low, which may limit the predictive power of the models.

## Future work

- The study suggests that future work could involve exploring other natural language processing models and techniques. The study also suggests that future work could involve using larger datasets and more advanced models.
- The future work of the study includes exploring how to automate the process of using price movements as implicit tagging of sentiment-rich text data, and learning indicative n-grams from temporally aligned market and news media data. The study also aims to further improve the performance of the best model and to explore the predictive power of the relationship between social media sentiment and price movements.

## References

[^2]: Hutto, C., GilBERT, E.: Vader: A parsimonious rule-based model for sentiment analysis of social media text. In Proceedings of the International AAAI Conference on Web and Social  [OA](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20GilBERT%2C%20E.%20Vader%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20so%20-%20cial%20media%20text) [GScholar](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20GilBERT%2C%20E.%20Vader%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20so%20-%20cial%20media%20text)

[^15]: Mastakouri, A., Schölkopf, B., Janzing, D.: Necessary and sufficient conditions for causal feature selection in time series with latent common causes. arXiv preprint arXiv:2005.08543 (2020).   [OA](https://arxiv.org/abs/2005.08543)  
