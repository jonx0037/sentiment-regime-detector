[[Cicekyurt_EnhancingSentimentAnalysisStockMarket_2025]]

# [Enhancing Sentiment Analysis in Stock Market Tweets Through BERT-Based Knowledge Transfer](https://doi.org/10.1007/s10614-025-10901-8)

## [[Emre Cicekyurt]]; [[Gokhan Bakal]]

## Abstract

One of the widely studied text classification efforts is sentiment analysis. It is a specific examination that uses natural language processing and machine learning methods to infer semantic orientation from textual data. Working social media posts, such as tweets, for sentiment analysis, is quite common among researchers due to the speed of information dissemination. In this regard, forecasting stock market tweets is a widely studied research topic. Some studies have found a strong connection between sentiment and stock market performance, while others have not. The proposed work presents two distinct approaches to sentiment analysis of stock market tweets. The first approach employs traditional machine learning algorithms, including logistic regression, random forest, and XGBoost. The second approach constructs deep learning (as a subfield of machine learning) models using LSTM and CNN algorithms to classify test instances into positive, negative, or neutral classes across 10 randomly shuffled data splits. In this study, the labeled data size is gradually increased utilizing a pre-trained model, FinBERT. It is exclusively employed to label unlabeled data instances to integrate them into the experiments. The goal is to monitor the effect of the newly labeled examples on sentiment analysis performance. The experiments showed that the average F1-score improved by 20% for the deep learning models and 17% for the machine learning models. In the end, the paper reveals a strong positive correlation between the size of the training data and the classification performance of the experimental approaches.

## Key concepts

# finding/machine_learning; #machine_learning; #natural_language_processing; #finding/logistic_regression; #logistic_regression; #sentiment_analysis; #natural_language; #finding/stock_market; #stock_market; #deep_learning; #long_short_term_memory; #finding/random_forest; #random_forest

## Quote
>
> The study explores the use of BERT-based knowledge transfer to enhance sentiment analysis in stock market tweets, demonstrating a strong positive correlation between training data size and classification performance, with average F1-score improvements of 20% for deep learning models and 17% for machine learning models.

## Key points

- Text classification is an essential task since it enables the extraction of relevant information from vast amounts of text and can be applied to various domains for distinct purposes, including sentiment analysis, spam detection, and topic modeling
- The convolutional neural networks (CNNs) model outperformed the Long Short-Term Memory (LSTM) model; the CNN model did not achieve any better performance than the best-performing logistic regression and random forest models
- When we interpret the impact of the Deep learning (DL) experiments utilizing cumulatively more annotated instances, the LSTM model captured more discriminative contextual information than the CNN model when we introduced new samples
- Sentiment analysis stands as a pivotal research endeavor within the machine learning and data science fields, where it finds widespread applications across various domains, encompassing individual opinions on products or services to collective expressions in social media posts
- The optimal machine learning model, constructed using the random forest algorithm with unigram features and 40,000 new instances, achieved an F1 score of 69%, which outperforms the initial model’s F1 score of 54% in its best configuration. This noteworthy improvement of 15% in F1 score reaffirms the effectiveness of our approach, a result consistently observed across both traditional machine learning and deep learning model experiments
- Among the XGBoost classifier experiments, again, the model using the unigram feature space yielded the highest F1 score as opposed to the other feature space configurations
- One limitation lies in the reliance on labeled data, and the study’s focus on sentiment analysis may not capture the full spectrum of market dynamics

## Summary

### Introduction

The study focuses on sentiment analysis of stock market tweets, utilizing natural language processing and machine learning methods to understand semantic orientation from textual data.
The goal is to examine the effect of increasing the size of labeled data on the performance of sentiment analysis models.

### Methods

Two approaches are employed: traditional machine learning algorithms (logistic regression, random forests, and XGBoost) and deep learning models (LSTMs and CNNs).
A pre-trained model, FinBERT, is used to label unlabeled data instances, which are then incorporated into the experiments.
The results show that the average F1-score improved by 20% for deep learning models and by 17% for machine learning models.

### Results

The study reveals a strong positive correlation between the size of the training data and the classification performance of the experimental approaches.
The experiments demonstrate that using a pre-trained model to label unlabeled data can significantly boost classification performance, even in the absence of human annotators.
The findings suggest that sentiment analysis of stock market tweets can provide valuable insights into market trends and investor sentiment.

### NLP Techniques

Natural language processing (NLP) techniques are employed to extract meaningful features from raw text data.
Data preprocessing is crucial in NLP to improve model accuracy by cleaning the data before analysis.
Preprocessing steps include tokenization, lemmatization, and stop-word removal.
The dataset used in this study consists of 1,300 tweets and requires additional cleaning operations to remove unnecessary information.

### Machine Learning

Machine learning algorithms, including logistic regression, random forest, and XGBoost, are used to build traditional machine learning models that predict tweet sentiment labels.
A TF-IDF vectorizer converts textual data into a numerical matrix for model training.
N-gram representations are also used to analyze the statistical properties of the text and understand the conveyed meaning.

### Deep Learning

Deep learning models, including convolutional neural networks (CNNs) and long short-term memory (LSTM) models, are used to capture complex nonlinear relationships and abstract patterns in the data.
CNNs are effective in capturing local patterns and features in text, while LSTMs are designed to overcome vanishing and exploding gradient problems in traditional RNNs.
Nonlinear activation functions, such as ReLU, introduce nonlinearity into the model's decision boundaries, allowing the model to learn hierarchical representations of the data.

### Models

The study uses various machine learning models, including logistic regression, random forests, XGBoost, CNNs, and LSTMs, to classify financial tweets based on their contextual sentiment.
The models are evaluated based on their performance, with the random forest model using unigram features achieving the highest F1 score.
The study also explores the use of pre-trained models, such as Fin-BERT, to improve model performance.

### Performance

The performance of the models is evaluated using various metrics, including precision, recall, and F1 score.
The results show that increasing the number of new examples boosts the models' classification performance, with the random forest model achieving an F1 score of 69% using 40,000 new instances.
The study also finds that traditional machine learning models perform better than deep learning models, likely because the tweet examples are short.

### Limitations

The study has several limitations, including its reliance on labeled data and its focus on sentiment analysis, which may not capture the full spectrum of market dynamics.
The effectiveness of the proposed approaches may vary across different market conditions, and external factors influencing sentiment expression may affect the models' generalizability.
Additionally, the original data collection method may no longer function due to changes to Twitter's APIs.

### Future Work

The success of the proposed Bert-based approach can be confirmed by performing additional operations in the future.
Another potential future direction is exploring ensemble models or hybrid approaches that combine traditional machine learning algorithms with deep learning techniques, which might offer synergistic advantages.

### Data And Funding

The dataset used is available at <https://ieee-dataport.org/open-access/stock-market-tweets-data>.
Open access funding was provided by the Scientific and Technological Research Council of Türkiye (TÜBİTAK).

### Publication Details

The article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution, and reproduction in any medium or format, as long as appropriate credit is given to the original authors and the source.
The article was written by E.
Cicekyurt and G.
Bakal, with G.
Bakal is supervising the project and conceiving the original idea.

## Study subjects

### 45 companies

- Plus, they revealed that the sentiment of tweets was a significant predictor of stock price movements (Bacco et al, 2024; Gandhudi et al, 2024). Yet another relevant effort employed by [^Antweiler_2004_a] examined the influence of Internet stock message boards on market movements, explicitly focusing on the 45 companies in the Dow Jones Industrial Average and the Dow Jones Internet Index. They analyzed over 1.5 million messages posted on Yahoo! Finance and Raging Bull, using computational linguistics methods to measure the bullishness level

### 943672 tweets

- 3 Dataset &amp; Data Preprocessing. Between April 9th and July 16th, 2020, 943,672 tweets were obtained using hashtags such as #SPX500, references to the top 25 companies in the S&P 500 index, and #stocks by Taborda et al (2021). Among these tweets, 1300 were annotated by manual efforts and labeled as positive (529), neutral (349), or negative (422)

## Data analysis

- #method/lstm_model
- #method/bert_model
- #method/logistic_regression
- #method/natural_language_toolkit
- #method/cnn_model
- #method/maximum_likelihood_estimation
- #method/dow_jones_internet_index

## Findings

- <mark class="fact">The experiments showed that the average F1-score improved by</mark> 20% for the <a class="keyword" href="https://en.wikipedia.org/wiki/Deep_learning" title="deep learning">deep learning</a> models and 17% for the <a class="keyword" href="https://en.wikipedia.org/wiki/machine_learning" title="machine learning">machine learning</a> models
- <mark class="fact">The study performed by Bollen et al</mark> (2011); Khafaga et al (2023) disclosed that Twitter posts could be used to understand the encoded sentiment and to predict <a class="keyword" href="https://en.wikipedia.org/wiki/stock_market" title="stock market">stock market</a> changes with an accuracy of 86%, where the dataset used consisted of over 2 million tweets and a subset of Dow Jones Industrial Average (<a class="keyword" href="#" title="Dow Jones Industrial Average">DJIA</a>) stocks
- The authors used a tweet dataset and stock prices from 2012 to 2013 and found no significant correlation between the sentiment of tweets and stock prices
- The authors used a dataset containing nine-month stock tweets and daily stock data and identified that their model could predict stock price movements with an accuracy range between 75% and 85%
- <mark class="claim">Among the xgboost classifier experiments, again, the model using the unigram feature space yielded the highest F1 score as opposed to the other feature space configurations</mark>
- <mark class="claim">When the most successful models are considered, regardless of the classifier type, in each configuration where additional instances are cumulatively included, we achieved at least a 1% F1 score improvement</mark>
- <mark class="claim">Contrary to the best model, the lowest model achieved an F1 score of 45%</mark>
- Specifically, the optimal <a class="keyword" href="https://en.wikipedia.org/wiki/machine_learning" title="machine learning">machine learning</a> model, constructed using the <a class="keyword" href="https://en.wikipedia.org/wiki/random_forest" title="random forest">random forest</a> algorithm with unigram features and 40,000 new instances, achieved an F1 score of 69%, which outperforms the initial model’s F1 score of 54% in its best configuration (a <a class="keyword" href="https://en.wikipedia.org/wiki/logistic_regression" title="logistic regression">logistic regression</a> model employing unigram features). <mark class="fact">This noteworthy improvement of 15% in F1 score reaffirms the effectiveness of our approach</mark>, <mark class="fact">a result consistently observed across both traditional machine learning</mark> and <a class="keyword" href="https://en.wikipedia.org/wiki/Deep_learning" title="deep learning">deep learning</a> model experiments

## Builds on previous research

- They found that commonly used negative word lists developed for other disciplines, such as the Harvard Dictionary, often misclassify common words in financial contexts. A more recent study by [^Gupta_2020_a] conducted a sentiment analysis experiment combining machine learning techniques and Term Frequency-Inverse Document Frequency (TF-IDF) to predict periodic changes in stock market prices.

## Differs from previous work

- However, sentiment analysis of tweets can provide additional information about the market directions that can help investors make more concrete decisions ([^Tumasjan_et+al_2010_a]). Furthermore, the major obstacle to working with social media datasets for sentiment analysis is the need for labeled instances to build supervised learning models ([^Aroyehun_2018_a]).

## Contributions

- <mark class="fact">Sentiment analysis stands as a pivotal research endeavor within the machine learning and data science fields</mark>, where it finds widespread applications across various domains, encompassing individual opinions on products or services to collective expressions in social media posts. <mark class="fact">The conclusive findings presented in Section 5 </mark>. 5 <mark class="fact">unequivocally validate our hypothesis that the incremental inclusion of new samples significantly enhances the performance of the models</mark>. Specifically, the optimal machine learning model, constructed using the random forest algorithm with unigram features and 40,000 new instances, achieved an F1 score of 69%, which outperforms the initial model’s best configuration (a logistic regression model employing unigram features) by 15%. <mark class="fact">This noteworthy improvement of 15% in F1 score reaffirms the effectiveness of our approach</mark>, <mark class="fact">a result consistently observed across both traditional machine learning</mark> and deep learning model experiments.

## References

[^Antweiler_2004_a]: Antweiler, W., & Frank, M. Z. (2004). Is all that talk just noise? The information content of internet stock message boards. The Journal of Finance,59(3), 1259–1294.  [OA](https://engine.scholarcy.com/oa_version?query=Antweiler%20W%20amp%20Frank%20M%20Z%202004%20Is%20all%20that%20talk%20just%20noise%20The%20information%20content%20of%20internet%20stock%20message%20boards%20The%20Journal%20of%20finance593%2012591294&author=Antweiler&title=Is%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20internet%20stock%20message%20boards&year=2004) [GScholar](https://scholar.google.co.uk/scholar?q=Antweiler%20W%20amp%20Frank%20M%20Z%202004%20Is%20all%20that%20talk%20just%20noise%20The%20information%20content%20of%20internet%20stock%20message%20boards%20The%20Journal%20of%20finance593%2012591294) [Scite](/scite_tallies?query=author%3AAntweiler%2Ctitle%3AIs%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20internet%20stock%20message%20boards%2Cyear%3A2004)

[^Aroyehun_2018_a]: Aroyehun, S. T., Gelbukh, A. (2018). Aggression detection in social media: Using deep neural networks, data augmentation, and pseudo labeling. In: Proceedings of the first workshop on trolling, aggression and cyberbullying (TRAC-2018), pp. 90–97.  [OA](https://scholar.google.co.uk/scholar?q=Aroyehun%2C%20S.T.%20Gelbukh%2C%20A.%20Aggression%20detection%20in%20social%20media%3A%20Using%20deep%20neural%20networks%2C%20data%20augmentation%2C%20and%20pseudo%20labeling%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Aroyehun%2C%20S.T.%20Gelbukh%2C%20A.%20Aggression%20detection%20in%20social%20media%3A%20Using%20deep%20neural%20networks%2C%20data%20augmentation%2C%20and%20pseudo%20labeling%202018)

[^Gupta_2020_a]: Gupta, R., & Chen, M. (2020). Sentiment analysis for stock price prediction. In: 2020 IEEE conference on multimedia information processing and retrieval (MIPR), IEEE, pp. 213–218.  [OA](https://scholar.google.co.uk/scholar?q=Gupta%20R%20amp%20Chen%20M%202020%20Sentiment%20analysis%20for%20stock%20price%20prediction%20In%202020%20IEEE%20conference%20on%20multimedia%20information%20processing%20and%20retrieval%20MIPR%20IEEE%20pp%20213218) [GScholar](https://scholar.google.co.uk/scholar?q=Gupta%20R%20amp%20Chen%20M%202020%20Sentiment%20analysis%20for%20stock%20price%20prediction%20In%202020%20IEEE%20conference%20on%20multimedia%20information%20processing%20and%20retrieval%20MIPR%20IEEE%20pp%20213218)

[^Tumasjan_et+al_2010_a]: Tumasjan, A., Sprenger, T., Sandner, P., et al. (2010). Predicting elections with Twitter: What 140 characters reveal about political sentiment. In: Proceedings of the international AAAI conference on web and social media, pp. 178–185.  [OA](https://scholar.google.co.uk/scholar?q=Tumasjan%2C%20A.%20Sprenger%2C%20T.%20Sandner%2C%20P.%20Predicting%20elections%20with%20twitter%3A%20What%20140%20characters%20reveal%20about%20political%20sentiment%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Tumasjan%2C%20A.%20Sprenger%2C%20T.%20Sandner%2C%20P.%20Predicting%20elections%20with%20twitter%3A%20What%20140%20characters%20reveal%20about%20political%20sentiment%202010)
