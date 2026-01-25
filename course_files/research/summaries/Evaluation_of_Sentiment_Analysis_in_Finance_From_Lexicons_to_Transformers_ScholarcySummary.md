[[Mishev_et+al_EvaluationSentimentAnalysisFinanceFrom_2020]]

# [Evaluation of Sentiment Analysis in Finance: From Lexicons to Transformers](https://doi.org/10.1109/access.2020.3009626)

## [[Kostadin Mishev]]; [[Ana Gjorgjevikj]]; [[Irena Vodenska]] et al.

## Abstract

Financial and economic news is continuously monitored by financial market participants. According to the efficient market hypothesis, all past information is reflected in stock prices, and new information is instantaneously incorporated into future stock prices. Hence, prompt extraction of positive or negative sentiments from news is very important for investment decision-making by traders, portfolio managers, and investors. Sentiment analysis models can provide an efficient way to extract actionable signals from the news. However, financial sentiment analysis is challenging due to domain-specific language and the unavailability of large labeled datasets. General sentiment analysis models are ineffective when applied to specific domains such as finance. To overcome these challenges, we design an evaluation platform to assess the effectiveness and performance of various sentiment analysis approaches, based on combinations of text representation methods and machine-learning classifiers. We perform more than 100 experiments using publicly available datasets labeled by financial experts. We start the evaluation with specific lexicons for sentiment analysis in finance and gradually build the study to include word and sentence encoders, up to the latest available NLP transformers. The results show that contextual embeddings achieve greater efficiency in sentiment analysis than lexicons and fixed-word and sentence encoders, even when large datasets are not available. Furthermore, distilled versions of NLP transformers produce results comparable to those of their larger teacher models, making them suitable for production environments.

## Key concepts

#efficient_market_hypothesis; #lexicon; #text_classification; #natural_language_processing; #deep_learning; #transformers; #claim/language_model; #language_model; #sentiment_analysis; #finding/BERT; #BERT; #machine_learning

## Quote

This paper presents a comprehensive study of natural language processing (NLP) methods for sentiment analysis in finance, evaluating the performance of various text representations and machine learning classifiers.

## Key points

- The latest advances in Natural Language Processing (NLP) have received significant attention due to their efficiency in language modeling
- The main contribution of this paper is the development of an evaluation platform, which we use to assess the performance of NLP methodologies for text feature extraction in finance
- We show that recent advances in deep-learning and transfer-learning methods in NLP increase the accuracy of sentiment analysis based on financial headlines
- The study begins with the lexicon-based approach, includes word and sentence encoders, and concludes with recent NLP transformers
- The main progress in sentiment analysis accuracy is driven by the text representation methods, which feed the semantic meaning of the words and sentences into the models
- This approach was constructed for sentiment analysis in the finance domain; it can be extended to other areas such as healthcare, legal, and business analytics

## Summary

### Sentiment Analysis

Sentiment analysis is a crucial tool for extracting actionable signals from financial news, allowing traders, portfolio managers, and investors to make informed decisions.
The efficient market hypothesis states that all past information is reflected in stock prices, and new information is instantaneously absorbed in determining future stock prices.
However, financial sentiment analysis is challenging due to domain-specific language and the unavailability of large labeled datasets.
General sentiment analysis models are ineffective when applied to specific domains such as finance.

### Text Representation

Text representation methods, including lexicon-based and statistical approaches, are used to extract features from financial texts.
Lexicon-based methods rely on domain-specific knowledge represented as a lexicon or dictionary, such as the Loughran-McDonald lexicon and the Harvard IV-4 dictionary.
Statistical methods, including Count Vectorizer (CV) and TF-IDF, convert text documents into matrices of token counts or weighted term frequencies.
However, these methods have limitations, such as the loss of ordering and contextual information.

### Deep Learning

Deep learning methods, including word and sentence encoders and NLP transformers, have significantly improved sentiment extraction from financial news and texts.
Recent advances in deep learning and transfer learning have increased the accuracy of sentiment analysis of financial headlines.
The use of distilled versions of NLP transformers, such as BERT and RoBERTa, has yielded results comparable to those of their larger teacher models, making them suitable for production environments.

### Word Encoders

Word encoders convert discrete words into high-dimensional vectors, providing semantic knowledge.
Popular word encoders include Word2Vec, GloVe, and FastText.
Word2Vec uses Continuous Bag-of-Words and Continuous Skip-gram Model architectures, while GloVe emphasizes co-occurrence probabilities between words.
FastText builds word embeddings at a deeper level by leveraging subwords and characters, enabling training on smaller datasets and generalizing to unseen words.

### Sentence Encoders

Sentence encoders learn fixed-length feature vectors that encode syntax and semantic properties of variable-length sentences.
Recent sentence encoders include Doc2Vec, Skip-Thought Vectors, InferSent, Universal Sentence Encoder (USE), and Language-Agnostic Sentence Representations (LASER).
Doc2Vec represents variable-length fragments of texts as fixed-size dense vectors, while Skip-Thought Vectors use an encoder-decoder architecture for sequence modeling.
InferSent learns sentence embeddings using natural language inference data, and USE converts variable-length sentences into 512-dimensional vectors using transfer-learning.

### Evaluation

The performance of these word and sentence encoders is evaluated in various NLP tasks, including sentiment analysis and text classification.
Pre-trained models, such as Word2Vec, GloVe, and FastText, are used to assess their performance on financial texts.
The evaluation of sentence encoders, including Doc2Vec, Skip-Thought Vectors, InferSent, USE, and LASER, is also conducted to assess their ability to extract important features in the sentence representation of financial headlines.
The study evaluates the models using various metrics, including the Matthews Correlation Coefficient (MCC), a widely used metric for assessing binary classification performance.
The results show that the NLP transformers outperform the other models, with BART achieving the best results in sentiment analysis tasks.
The study also highlights the importance of using domain-specific dictionaries for feature extraction in sentiment analysis tasks.

### NLP Models

The study evaluates LASER on English texts, but the same model can be used for sentiment analysis in 92 other languages supported by LASER.
NLP transformers, such as BERT, XLNet, and RoBERTa, have achieved state-of-the-art performance across a range of NLP tasks, including text classification and sentiment analysis.
These models use a transformer architecture, which transforms one sequence into another using an encoder-decoder architecture.

### Transformer Architecture

The transformer architecture is based on multi-headed self-attention mechanisms, which enable parallelization and the learning of long-range word dependencies in a sequence.
The architecture consists of encoder and decoder modules, with multi-head attention and feed-forward layers as the main building blocks.
The scaled dot-product attention mechanism computes attention weights that represent the influence of each word in the sequence on other words.

### Language Representation

Language representation models, such as BERT, XLNet, and XLM, use pre-training objectives to learn contextualized word embeddings.
These models overcome the limitations of traditional word embeddings, such as Word2Vec and GloVe, which use fixed embeddings for each word.
The pre-trained models can be fine-tuned for specific tasks, such as sentiment analysis, to achieve better results.
Other models, such as ALBERT, RoBERTa, and DistilBERT, offer optimized versions of BERT with fewer parameters, improved training methods, and better performance across various NLP tasks.

### Models

The study evaluates the performance of various models for sentiment analysis in finance, including lexicon-based models, word encoders, sentence encoders, and NLP transformers such as BERT, RoBERTa, XLM-RoBERTa, and BART.
The models are fine-tuned and compared using different machine-learning and deep-learning classifiers.

### Datasets

The study uses two publicly available datasets: the Financial Phrase-Bank and SemEval 2017 datasets.
The datasets are pre-processed and balanced to address the imbalance between positive and negative sentences.
The preprocessing steps include tokenization, stop-word removal, stemming, and named-entity recognition.

### Methods

The study evaluates various NLP-based methods for sentiment analysis in finance, including lexicon-based approaches, word and sentence encoders, and recent NLP transformers.
The methods are compared based on their performance, with the NLP transformers showing superior results.
The study also investigates the use of different word embeddings, such as GloVe and FastText, and the impact of attention layers and bidirectional context on the results.

### Results

The results show that the NLP transformers, particularly BART and ALBERT-xxlarge, achieve the best performance with MCC scores of 0.895 and 0.881, respectively.
The study also finds that contextualized embeddings, such as ELMo and BERT, outperform non-contextualized embeddings.
The results are presented in Tables 4-8, which provide a detailed comparison of the methods and their performance.

### Applications

The study highlights the potential applications of the proposed approach in finance, including forecasting stock market trends and corporate earnings; decision-making in securities trading and portfolio management; brand reputation management; and fraud detection and regulation.
The findings also suggest that the approach can be extended to other areas, such as healthcare, legal, and business analytics, where sentiment analysis can provide valuable insights.

## Study subjects

### 1748 samples

- Additionally, we shuffle the datasets, and we set aside stratified 80% of all sentences as a training set and stratified 20% of the remaining sentences as a validation set. At the end, our balanced training set includes 1748 samples, and a balanced validation set consisting of 438 samples. C

## Data analysis

- #method/roberta_model
- #method/bert_algorithm
- #method/bigru_method
- #method/correlation_coefficient

## Findings

- Compared to other pre-trained versions of <a class="keyword" href="https://en.wikipedia.org/wiki/BERT_(language_model)" title="BERT">BERT</a>, FinBERT model has achieved a 15% improvement in accuracy in <a class="keyword" href="https://en.wikipedia.org/wiki/Text_classification" title="text classification">text classification</a> tasks specifically applied to financial texts
- <mark class="fact">DistilBERT retains more than 95% of the accuracy</mark> while having 40% fewer parameters

##  Builds on previous research

- The results of this study can be applied in areas such as finance, where decision-making is based on sentiment extraction from massive textual datasets. The findings imply that selected models can be successfully used for forecasting stock market trends and corporate earnings, for decision-making in securities trading and portfolio management, for brand reputation management, and for fraud detection and regulation [^87]–[^89].

## Differs from previous work

- If the model has not encountered a word before, it will be unable to interpret it or build a vector for it. Additionally, Word2Vec does not support shared representations at the sub-word level, meaning it creates two completely different vector representations for words that are morphologically similar, such as agree/agreement or worth/worthwhile [^29].
- Recent research studies have proposed methods that produce different embeddings for the same word, taking into consideration specific contexts [^3], [^55], [^58]. As an illustration of context importance, we analyze the following two sentences that contain the word ‘‘Apple’’: ‘‘Apple Inc performed well this year.’’ and ‘‘Apple fruits are exported to various countries.’’ In the first sentence, Apple refers to the technology company Apple, headquartered in the US, while in the second sentence, apple refers to the fruit, with a completely different meaning.

## Contributions

- This paper presents a comprehensive chronological study of NLP-based methods for sentiment analysis in finance. <mark class="fact">The study begins with the lexicon-based approach</mark>, includes word and sentence encoders, and concludes with recent NLP transformers. <mark class="fact">The NLP transformers show superior performances compared to the other evaluated approaches</mark>. <mark class="fact">The main progress in sentiment analysis accuracy is driven by the text representation methods</mark>, <mark class="fact">which feed the semantic meaning of the words and sentences into the models</mark>. <mark class="fact">The results achieved by the best models are comparable to expert</mark>’s opinion. The evaluations were performed on a relatively small dataset of approximately 2000 sentences. Even though the dataset is not large, we obtained good results, suggesting <mark class="fact">that this approach is appropriate for domains where large annotated data is</mark> not available.

## Limitations

- The study is limited by the relatively small dataset of approximately 2000 sentences. However, the study suggests that this approach is appropriate for domains where large amounts of annotated data are not available.

## Future work

- The study suggests that the approach can be extended to other areas such as healthcare, legal, and business analytics. The study also suggests that the results can be applied in areas such as finance, where decision-making is based on sentiment extraction from massive textual datasets.

## References

[^3]: J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, ‘‘BERT: Pre-training of deep bidirectional transformers for language understanding,’’ 2018, arXiv:1810.04805. [Online]. Available: <http://arxiv.org/abs/1810.04805>  [OA](http://arxiv.org/abs/1810.04805)  

[^29]: P. Bojanowski, E. Grave, A. Joulin, and T. Mikolov, ‘‘Enriching word vectors with subword information,’’ Trans. Assoc. Comput. Linguistics, vol. 5, pp. 135–146, Dec. 2017.  [OA](https://engine.scholarcy.com/oa_version?query=Bojanowski%2C%20P.%20Grave%2C%20E.%20Joulin%2C%20A.%20Mikolov%2C%20T.%20%E2%80%98Enriching%20word%20vectors%20with%20subword%20information%2C%E2%80%99%202017-12&author=Bojanowski&title=%E2%80%98Enriching%20word%20vectors%20with%20subword%20information%2C%E2%80%99&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Bojanowski%2C%20P.%20Grave%2C%20E.%20Joulin%2C%20A.%20Mikolov%2C%20T.%20%E2%80%98Enriching%20word%20vectors%20with%20subword%20information%2C%E2%80%99%202017-12) [Scite](/scite_tallies?query=author%3ABojanowski%2Ctitle%3A%E2%80%98Enriching%20word%20vectors%20with%20subword%20information%2C%E2%80%99%2Cyear%3A2017)

[^55]: M. E. Peters, M. Neumann, M. Iyyer, M. Gardner, C. Clark, K. Lee, and L. Zettlemoyer, ‘‘Deep contextualized word representations,’’ 2018, arXiv:1802.05365. [Online]. Available: <http://arxiv.org/abs/1802.05365>  [OA](http://arxiv.org/abs/1802.05365)  

[^58]: A. Akbik, D. Blythe, and R. Vollgraf, ‘‘Contextual string embeddings for sequence labeling,’’ in Proc. 27th Int. Conf. Comput. Linguistics, 2018, pp. 1638–1649.  [OA](https://scholar.google.co.uk/scholar?q=Akbik%2C%20A.%20Blythe%2C%20D.%20Vollgraf%2C%20R.%20%E2%80%98Contextual%20string%20embeddings%20for%20sequence%20labeling%2C%E2%80%99%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Akbik%2C%20A.%20Blythe%2C%20D.%20Vollgraf%2C%20R.%20%E2%80%98Contextual%20string%20embeddings%20for%20sequence%20labeling%2C%E2%80%99%202018)

[^87]: T. Rao and S. Srivastava, ‘‘Analyzing stock market movements using Twitter sentiment analysis,’’ Tech. Rep., 2012.  [OA](https://engine.scholarcy.com/oa_version?query=Rao%2C%20T.%20Srivastava%2C%20S.%20%E2%80%98Analyzing%20stock%20market%20movements%20using%20twitter%20sentiment%20analysis%2C%E2%80%99%202012&author=Rao&title=%E2%80%98Analyzing%20stock%20market%20movements%20using%20twitter%20sentiment%20analysis%2C%E2%80%99&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Rao%2C%20T.%20Srivastava%2C%20S.%20%E2%80%98Analyzing%20stock%20market%20movements%20using%20twitter%20sentiment%20analysis%2C%E2%80%99%202012) [Scite](/scite_tallies?query=author%3ARao%2Ctitle%3A%E2%80%98Analyzing%20stock%20market%20movements%20using%20twitter%20sentiment%20analysis%2C%E2%80%99%2Cyear%3A2012)

[^89]: X. Li, H. Xie, L. Chen, J. Wang, and X. Deng, ‘‘News impact on stock price return via sentiment analysis,’’ Knowl.-Based Syst., vol. 69, pp. 14–23, Oct. 2014. KOSTADIN MISHEV received the bachelor’s degree in informatics and computer engineering and the master’s degree in computer networks and e-technologies from Saints Cyril and Methodius University, Skopje, in 2013 and 2016, respectively, where he is currently pursuing the Ph.D. degree. He is also a Teaching and Research Assistant with the Faculty of Computer Science and Engineering, Saints Cyril and Methodius University. His research interests include data science, natural language processing, semantic Web, enterprise application architectures, Web technologies, and computer networks.  [OA](https://engine.scholarcy.com/oa_version?query=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20%E2%80%98News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%2C%E2%80%99%202014-10&author=Li&title=%E2%80%98News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%2C%E2%80%99&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20%E2%80%98News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%2C%E2%80%99%202014-10) [Scite](/scite_tallies?query=author%3ALi%2Ctitle%3A%E2%80%98News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%2C%E2%80%99%2Cyear%3A2014)
