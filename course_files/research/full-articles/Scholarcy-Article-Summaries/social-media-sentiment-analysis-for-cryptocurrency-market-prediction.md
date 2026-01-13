[[Raheman_et+al_SocialMediaSentimentAnalysisCryptocurrency_2022]]

# [Social Media Sentiment Analysis for Cryptocurrency Market Prediction](https://doi.org/10.48550/arxiv.2204.10185)

## [[Ali Raheman]]; [[Anton Kolonin]]; [[Igors Fridkins]] et al.

## Abstract
In this paper, we explore the usability of different natural language processing models for the sentiment analysis of social media applied to financial market prediction, using the cryptocurrency domain as a reference. ==We study how the different sentiment metrics are correlated with the price movements of Bitcoin==. ==For this purpose, we explore different methods to calculate the sentiment metrics from a text finding most of them not very accurate for this prediction task==. ==We find that one of the models outperforms more than 20 other public ones and makes it possible to fine-tune it efficiently given its interpretable nature==. Thus we confirm that interpretable artificial intelligence and natural language processing methods might be more valuable practically than non-explainable and non-interpretable ones. In the end, we analyse potential causal connections between the different sentiment metrics and the price movements.

## Key concepts
#cryptocurrency; #machine_learning; #claim/metrics; #metrics; #sentiment_analysis; #claim/natural_language_processing; #natural_language_processing; #interpretable_artificial_intelligence

## Quote
> The study evaluates 21 sentiment analysis models on a cryptocurrency dataset, fine-tunes the top-performing model, and explores the causal connection between social media sentiment and price movements, with results showing a potential connection between sentiment metrics and price changes.

## Key points
- We all are well aware of how much social media is connected to everyone's life and the impact it has on it
- Given a much clearer maximum at -1 day lag with correlation value as high as 0.55, compared with values corresponding to other lags, we can assume that selective inclusion and weighting of the news metrics and channels enables finding more causally connected time series, which builds up compound sentiment indicators that are potentially valuable for further feature engineering for the price prediction purposes
- We have shown how an “interpretable” sentiment analysis model could be significantly improved manually and without the huge costs for training the domain-specific corpus and creating and tagging this corpus for said purpose
- We are exploring how to automate this process of using the price movements being an implicit tagging of the sentiment-rich text data and learning the indicative n-grams from the temporally aligned market and news media data, with the option for manual review on the discovered patterns within the “interpretable” mode
- We are looking forward to improving the performance of the best model further
- Our future work in this area will be dedicated to exploring the predictive power of the connection to improve the reliability of the price prediction and business applications for decentralized finance relying on such predictions


## Summary

### Introduction
The paper explores the use of natural language processing models for sentiment analysis of social media to predict cryptocurrency market movements.
The study focuses on Bitcoin and uses data from Twitter and Reddit.
The goal is to determine if sentiment scores can be used for price prediction.

### Methodology
The study involves a literature survey of publicly available sentiment models, data collection from Twitter and Reddit, processing of the data using various models, and evaluation of their performance.
The best model, Aigents, is fine-tuned and re-evaluated, showing a significant increase in correlation between sentiment score and price movement.

### Results
The study evaluates 21 different sentiment models and finds that the Aigents model outperforms the others.
The model is based on "n-grams" and has an interpretable nature, allowing for fine-tuning and improvement of its performance.
The correlation between the improved Aigents model sentiment score and price movement increases from 0.33 to 0.57.
The study also explores possible causal connections between sentiment metrics and price movements, analyzing mutual Pearson correlation between daily Bitcoin price difference and sentiment metrics.
The evaluation of the 21 models was performed using the Pearson correlation coefficient, with the fine-tuned Aigents model achieving the highest correlation of 0.57.
The study also explored the potential causal connection between social media sentiment and price movements, finding a peak in correlation value at -2 days shift for overall sentiment and positive metrics.
The automated process of building compound sentiment indicators was employed to increase the power of such connections, with a maximum correlation value of 0.55 at -1 day lag.

### Models
The experiments used 15 BERT-based models trained on different datasets, including Distilbert-base-uncased, finiteautomata/bertweet-base-sentiment-analysis, and cardiffnlp/twitter-roberta-base-sentiment.
Other models used include ProsusAI/finBERT, moussaKam/barthez-sentiment-classification, and textattack/bert-base-uncased-imdb.
The base models used were BERT, RoBERTa, and DistilRoBERTa, and were fine-tuned on various datasets such as IMDB, Yelp polarity, and tweets_hate_speech_detection.

### Challenges
The experiments encountered several challenges, including sarcasm, idioms, and negations, which can make it difficult for sentiment models to understand the true context of texts.
Non-text data, such as images and videos, can also contain strong indications of price change that may be missed by sentiment models.
These challenges can lead to misclassification and lower model accuracy.


## Study subjects

### 490 tweets
- The data collection process has been based on official Reddit and Twitter APIs and was performed exclusively on public posts in public feeds. ==For the purpose of the algorithm quality assessment, we have used 490 tweets/posts from 5 randomly selected Twitter public feeds==. The tweets/ posts have been manually classified for both positive and negative sentiment in the range [-1.0,0.0] and [0.0,+1.0] respectively by two independent reviewers and made the “ground truth” sentiment assessment as the average of the two assessments for positive and negative metrics

### 10 independent people
- It is a lexicon and rule-based sentiment model specially created for texts in social media. ==It has over 9,000 words, and every word was marked by ten independent people from -4 (extremely negative) to 4 (extremely positive) and after that, the final score is the average of all 10 scores [^2]==. TextBlob

## Data analysis
- #method/pearson_correlation
- #method/aigents_model
- #method/pearson_correlation_coefficient

## Findings
- <mark class="claim">We are looking forward to improving the performance of the best model further</mark>

##  Builds on previous research
- 8 following the concepts of causal analysis on time series discussed in [^15], as shown in Figure 2. ==We can see that the plots corresponding to overall sentiment and positive metrics are presenting the peaks in the correlation value at -2 days shift==.

## Contributions
- In this paper, <mark class="claim">we have found the most reliable model for social media sentiment analysis in the cryptocurrency domain</mark>. <mark class="claim"><mark class="fact">We have shown how an “interpretable” sentiment analysis model could be significantly improved</mark> manually and without the huge costs for training the domain-specific corpus and creating and tagging this corpus for said purpose</mark>. In our further work, <mark class="fact">we are exploring how to automate this process of using the price movements being an implicit tagging of the sentiment-rich text data</mark> and learning the indicative n-grams from the temporally aligned market and news media data, with the option for manual review on the discovered patterns within the “interpretable” mode. <mark class="claim">We are looking forward to improving the performance of the best model further</mark>.

## Limitations
- The study has several limitations, including the use of a limited dataset and the reliance on manual classification of tweets/posts. The study also notes that the models used are not perfect and may have biases.
- The limitations of the study include the challenges of sentiment analysis, such as sarcasm, idioms, and negations, which can affect the accuracy of the models. The study also notes that the correlation values between social media sentiment and price movements are not high, which may limit the predictive power of the models.

## Future work
- The study suggests that future work could involve exploring other natural language processing models and techniques. The study also suggests that future work could involve using larger datasets and more advanced models.
- The future work of the study includes exploring how to automate the process of using price movements as implicit tagging of sentiment-rich text data, and learning indicative n-grams from temporally aligned market and news media data. The study also aims to improve the performance of the best model further, and to explore the predictive power of the connection between social media sentiment and price movements.


## References
[^1]: Nielsen, F.: Evaluation of a word list for sentiment analysis in microblogs. arXiv 2011. arXiv preprint arXiv:1103.2903 (2011).  [OA](https://arxiv.org/abs/1103.2903)  

[^2]: Hutto, C., Gilbert, E.: Vader: A parsimonious rule-based model for sentiment analysis of so - cial media text. In Proceedings of the International AAAI Conference on Web and Social  [OA](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20Gilbert%2C%20E.%20Vader%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20so%20-%20cial%20media%20text) [GScholar](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20Gilbert%2C%20E.%20Vader%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20so%20-%20cial%20media%20text) 

[^3]: Media (Vol. 8, No. 1) (2014).  [OA](https://scholar.google.co.uk/scholar?q=Media%20Vol%208%20No%201%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Media%20Vol%208%20No%201%202014) 

[^3]: Kolonin, A.: High-performance automatic categorization and attribution of inventory cata - logs. Proceedings of All-Russia conference Knowledge Ontology Theories (KONT-2013), Novosibirsk, Russia (2013).  [OA](https://scholar.google.co.uk/scholar?q=Kolonin%2C%20A.%20High-performance%20automatic%20categorization%20and%20attribution%20of%20inventory%20cata%20-%20logs%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Kolonin%2C%20A.%20High-performance%20automatic%20categorization%20and%20attribution%20of%20inventory%20cata%20-%20logs%202013) 

[^4]: Sanh, V., Debut, L., Chaumond, J., Wolf, T.: DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108 (2019).  [OA](https://arxiv.org/abs/1910.01108)  

[^5]: Pérez, J. M., Giudici, J. C., Luque, F.: pysentimiento: A Python Toolkit for Sentiment Analysis and SocialNLP tasks. arXiv preprint arXiv:2106.09462 (2021).  [OA](https://arxiv.org/abs/2106.09462)  

[^6]: Barbieri, F., Camacho-Collados, J., Neves, L., &amp; Espinosa-Anke, L.: Tweeteval: Unified benchmark and comparative evaluation for tweet classification. arXiv preprint arXiv:2010.12421 (2020).  [OA](https://arxiv.org/abs/2010.12421)  

[^7]: Araci, D.: Finbert: Financial sentiment analysis with pre-trained language models. arXiv preprint arXiv:1908.10063 (2019).  [OA](https://arxiv.org/abs/1908.10063)  

[^8]: Eddine, M.K., Tixier, A.J., Vazirgiannis, M.: BARThez: a Skilled Pretrained French Sequence-to-Sequence Model. EMNLP (2021).  [OA](https://scholar.google.co.uk/scholar?q=Eddine%2C%20M.K.%20Tixier%2C%20A.J.%20Vazirgiannis%2C%20M.%20BARThez%3A%20a%20Skilled%20Pretrained%20French%20Sequence-to-Sequence%20Model%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Eddine%2C%20M.K.%20Tixier%2C%20A.J.%20Vazirgiannis%2C%20M.%20BARThez%3A%20a%20Skilled%20Pretrained%20French%20Sequence-to-Sequence%20Model%202021) 

[^9]: Morris, J. X., Lifland, E., Yoo, J. Y., Grigsby, J., Jin, D., Qi, Y.: Textattack: A framework for adversarial attacks, data augmentation, and adversarial training in nlp. arXiv preprint arXiv:2005.05909 (2020).  [OA](https://arxiv.org/abs/2005.05909)  

[^10]: Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Stoyanov, V.: Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692 (2019).  [OA](https://arxiv.org/abs/1907.11692)  

[^11]: Heitmann, M., Siebert, C., Hartmann, J., Schamp, C.: More than a feeling: Benchmarks for sentiment analysis accuracy. Available at SSRN 3489963 (2020).  [OA](https://engine.scholarcy.com/oa_version?query=Heitmann%2C%20M.%20Siebert%2C%20C.%20Hartmann%2C%20J.%20Schamp%2C%20C.%20More%20than%20a%20feeling%3A%20Benchmarks%20for%20sentiment%20analysis%20accuracy%202020&author=Heitmann&title=More%20than%20a%20feeling%3A%20Benchmarks%20for%20sentiment%20analysis%20accuracy&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Heitmann%2C%20M.%20Siebert%2C%20C.%20Hartmann%2C%20J.%20Schamp%2C%20C.%20More%20than%20a%20feeling%3A%20Benchmarks%20for%20sentiment%20analysis%20accuracy%202020) [Scite](/scite_tallies?query=author%3AHeitmann%2Ctitle%3AMore%20than%20a%20feeling%3A%20Benchmarks%20for%20sentiment%20analysis%20accuracy%2Cyear%3A2020)

[^12]: Aguilar, G., Kar, S., Solorio, T.: LinCE: A centralized benchmark for linguistic codeswitching evaluation. ArXiv preprint arXiv:2005.04322 (2020).  [OA](https://arxiv.org/abs/2005.04322)  

[^13]: Khanuja, S., Dandapat, S., Srini vasan, A., Sitaram, S., Choudhury, M.: GLUECoS: An evaluation benchmark for code-switched NLP. arXiv preprint arXiv:2004.12376 (2020).  [OA](https://arxiv.org/abs/2004.12376)  

[^14]: Canete, J., Chaperon, G., Fuentes, R., Ho, J. H., Kang, H., Pérez, J.: Spanish pretrained bert model and evaluation data. Workshop paper at PML4DC at ICLR (2020).  [OA](https://scholar.google.co.uk/scholar?q=Canete%2C%20J.%20Chaperon%2C%20G.%20Fuentes%2C%20R.%20Ho%2C%20J.H.%20Spanish%20pretrained%20bert%20model%20and%20evaluation%20data%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Canete%2C%20J.%20Chaperon%2C%20G.%20Fuentes%2C%20R.%20Ho%2C%20J.H.%20Spanish%20pretrained%20bert%20model%20and%20evaluation%20data%202020) 

[^15]: Mastakouri, A., Schölkopf, B., Janzing D.: Necessary and sufficient conditions for causal feature selection in time series with latent common causes. arXiv preprint arXiv:2005.08543 (2020).   [OA](https://arxiv.org/abs/2005.08543)  

