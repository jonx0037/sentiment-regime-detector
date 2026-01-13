[[Araci_FinbertFinancialSentimentAnalysisWith_2019]]

# [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063)

## [[Dogu Araci]]

## Abstract
Financial sentiment analysis is a challenging task due to the specialized language and lack of labeled data in that domain. General-purpose models are not effective enough because of the specialized language used in a financial context. We hypothesize that pre-trained language models can help with this problem because they require fewer labeled examples and they can be further trained on domain-specific corpora. ==We introduce FinBERT, a language model based on BERT, to tackle NLP tasks in the financial domain==. ==Our results show improvement in every measured metric on current state-of-the-art results for two financial sentiment analysis datasets==. ==We find that even with a smaller training set and fine-tuning only a part of the model, FinBERT outperforms state-of-the-art machine learning methods==.

## Key concepts
#loughran; #claim/language_model; #language_model; #finding/BERT; #BERT; #natural_language_processing; #long_short_term_memory

## Quote
> The paper presents FinBERT, a BERT implementation for the financial domain, and evaluates its performance on short sentence classification and regression tasks, comparing it to other transfer learning methods like ELMo and ULMFit.

## Key points
- Prices in an open market reflects all of the available information regarding assets exchanged in an economy ([^Malkiel_2003_a])
- We introduce FinBERT, which is a language model based on BERT for financial natural language processing (NLP) tasks
- This work is the first application of BERT for finance to the best of our knowledge and one of the few that experimented with further pre-training on a domain-specific corpus
- ULMFit, further pre-trained on a financial corpus, beat the previous state-of-the art for the classification task, only to a smaller degree than BERT. These results show the effectiveness of pre-trained language models for a down-stream task such as sentiment analysis especially with a small labeled dataset
- The complete dataset included more than 3000 examples, but FinBERT was able to surpass the previous state-of-the art even with a training set as small as 500 examples
- On both of the datasets we used, we achieved state-of-the-art results by a significant margin
- FinBERT is good enough for extracting explicit sentiments, but modeling implicit information that is not necessarily apparent even to those who are writing the text should be a challenging task. Another possible extension can be using FinBERT for other natural language processing tasks such as named entity recognition or question answering in financial domain


## Summary

### Introduction
Financial sentiment analysis is a challenging task due to the specialized language and lack of labeled data in the financial domain.
General-purpose models are not effective enough because of the specialized language used in the financial context.
The goal of this thesis is to test the hypothesized advantages of using and fine-tuning pre-trained language models for the financial domain.

### Methodology
The thesis introduces FinBERT, a language model based on BERT, to tackle NLP tasks in the financial domain.
FinBERT is evaluated on two financial sentiment analysis datasets, and the results show improvement in every measured metric on current state-of-the-art results.
The thesis also implements two other pre-trained language models, ULMFit and ELMo, for financial sentiment analysis and compares these with FinBERT.
The paper implemented BERT for the financial domain by further pre-training it on a financial corpus and fine-tuning it for sentiment analysis, resulting in a model called FinBERT.
Other pre-training language models like ELMo and ULMFit were also implemented for comparison purposes.
The effects of further pre-training and several training strategies were investigated, including the impact of learning rate regimes and fine-tuning only the last 2 layers of BERT.

### Related Work
Previous research on sentiment analysis in finance has used machine learning methods with features extracted from text with "word counting" and deep learning methods, where text is represented by a sequence of embeddings.
The thesis also discusses text classification using pre-trained language models, including ELMo, ULMFit, and BERT, which have achieved state-of-the-art results in multiple NLP tasks.

### Models
The paper discusses several models for natural language processing, including GLoVe, ELMo, ULMFit, and BERT.
GLoVe is a model for calculating word representations, while ELMo provides contextualized word representations.
ULMFit is a transfer learning model that uses language model pre-training, and BERT is a language model that consists of a set of Transformer encoders stacked on top of each other.

### BERT For Financial Domain
The paper implements BERT for the financial domain, including further pre-training on a financial corpus and fine-tuning for classification and regression tasks.
The authors use two approaches for further pre-training: pre-training on a large financial corpus and pre-training on sentences from the training classification dataset.

### Experimental Setup
The paper describes the experimental setup, including the research questions, datasets, and baseline methods.
The authors use three datasets: TRC2-financial, Financial PhraseBank, and FiQA Sentiment.
The baseline methods include LSTM classifiers with GLoVe and ELMo embeddings, and ULMFit.
The authors evaluate the models using accuracy, cross-entropy loss, and other metrics.

### Model Performance
The FinBERT model outperforms other methods, including LSTM, ULMFit, LPS, HSC, and FinSSLX, in terms of accuracy, macro F1 average, and other metrics.
The model achieves the best results on both the whole dataset and a subset with 100% annotator agreement.
The use of language model pre-training and effective training strategies enables the model to overcome the small data problem.

### Training Strategies
The effectiveness of language model pre-training is demonstrated by the superior performance of ULMFit and FinBERT compared to LSTM classifiers.
The use of discriminative fine-tuning, gradual unfreezing, and slanted triangular learning rates helps to prevent catastrophic forgetting and improves the model's performance.
Fine-tuning only a subset of the layers can achieve a fair trade-off between performance and training time.

### Error Analysis
The model's failures are mostly due to its inability to distinguish between positive and neutral labels, which is consistent with inter-annotator agreement numbers and common sense.
The model struggles to identify the polarity of statements about companies, especially when the statements are neutral or lack indicative words.
The confusion matrix shows that 73% of the failures occur between positive and neutral labels, while only 5% occur between negative and positive labels.

### Results
The results showed that FinBERT achieved state-of-the-art results by a significant margin on both datasets used, increasing the state-of-the-art by 15% in accuracy for the classification task.
ULMFit, further pre-trained on a financial corpus, also beat the previous state-of-the-art, but to a smaller degree than BERT.
The results demonstrated the effectiveness of pre-trained language models for sentiment analysis, even with a small labeled dataset.

### Future Work
The paper suggests potential extensions of the work, including using FinBERT directly with stock market return data to support financial decisions, and applying FinBERT to other natural language processing tasks such as named entity recognition or question answering in the financial domain.
Additionally, modeling implicit information that is not necessarily apparent in the text is identified as a challenging task that could be explored in future research.


## Study subjects

### 46143 documents with more than 29M words and nearly 400K sentences
- We filter for some financial keywords in order to make corpus more relevant and in limits with the compute power available. ==The resulting corpus, TRC2-financial, includes 46,143 documents with more than 29M words and nearly 400K sentences==. 4.2.2

### 16 people with background in finance and business
- Financial Phrasebank consists of 4845 english sentences selected randomly from financial news found on LexisNexis database. ==These sentences then were annotated by 16 people with background in finance and business==. The annotators were asked to give labels according to how they think the information in the sentence might affect the mentioned company stock price

## Data analysis
- #method/lstm_model
- #method/

## Findings
- <mark class="claim"><mark class="fact">We achieve the state-of-the-art on FiQA sentiment scoring</mark> and Financial PhraseBank</mark>
- Once the training size becomes 250, ULMFit and FinBERT starts to successfully differentiate between labels, with an accuracy as high as 80% for FinBERT
- <mark class="claim">Our model outperforms state-of-the-art models for both MSE and</mark> $R^{2}$
- <mark class="claim"><mark class="fact">The model achieves the best performance on validation set after the first epoch</mark> and then starts to overfit</mark>
- With 97% accuracy on the subset of Financial PhraseBank with 100% annotator agreement, we think it might be an interesting exercise to examine cases where the model failed to predict the true label
- <mark class="fact">This work is the first application of BERT for finance</mark> to the best of our knowledge and one of the few <mark class="fact">that experimented with further pre-training on a domain-specific corpus</mark>. <mark class="claim">On both of the datasets we used, we achieved state-of-the-art results by a significant margin</mark>

##  Builds on previous research
- They also introduced further pre-training of the language model on a domain-specific corpus, assuming target task data comes from a different distribution than the general corpus the initial model was trained on. ==ULMFit’s main idea of efficiently fine-tuning a pre-trained a language model for down-stream tasks was brought to another level with Bidirectional Encoder Representations from Transformers (BERT) ([^Devlin_et+al_2018_a]), which is also the main focus of this paper==.

##  Confirmation of earlier findings
- $R^{2}$. ==Bold face indicated best result in corresponding metric==. [^Yang_et+al_2018_a]) ([^Yang_et+al_2018_a]) and [^Piao_2018_a]) ([^Piao_2018_a]) report results on the official test set.

## Counterpoint to earlier claims
- Since we don’t have access to that we report the results on 10-Fold cross validation. There is no indication on ([^Maia_et+al_2018_b]) that the train and test sets they publish come from ==different distributions and our model can be interpreted to be at disadvantage since we need to set aside a subset of training set as test set, while state-of-the-art papers can use the complete training set==.

## Contributions
- In this paper, we implemented BERT for the financial domain by further pre-training it on a financial corpus and fine-tuning it for sentiment analysis (FinBERT). <mark class="fact">This work is the first application of BERT for finance</mark> to the best of our knowledge and one of the few <mark class="fact">that experimented with further pre-training on a domain-specific corpus</mark>. <mark class="claim">On both of the datasets we used, we achieved state-of-the-art results by a significant margin</mark>. For the classification task, <mark class="fact">we increased the state-of-the art by 15% in accuracy</mark>.

## Limitations
- The study notes that one of the limitations of the study is the lack of large labeled financial datasets, which makes it difficult to utilize neural networks to their full potential for sentiment analysis.
- The study has several limitations, including the use of a limited number of baseline methods and the lack of thorough experimentation with these methods. The study also notes that the results should not be interpreted as definitive conclusions of one method being better.
- The limitations of the study include: the use of a limited dataset.
- The limitations of the study include the fact that further pre-training on a domain-specific corpus did not significantly improve the performance of BERT, and that modeling implicit information that is not necessarily apparent even to those who are writing the text is a challenging task.


## References
[^Agarwal_2016_a]: Agarwal and Mittal (2016) Basant Agarwal and Namita Mittal. 2016. Machine Learning Approach for Sentiment Analysis. Springer International Publishing, Cham, 21–45. https://doi.org/10.1007/978-3-319-25343-5_3  [OA](https://doi.org/10.1007/978-3-319-25343-5_3)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-3-319-25343-5_3)

[^Araque_et+al_2017_a]: Araque et al. (2017) Oscar Araque, Ignacio Corcuera-Platas, J. Fernando Sánchez-Rada, and Carlos A. Iglesias. 2017. Enhancing deep learning sentiment analysis with ensemble techniques in social applications. Expert Systems with Applications 77 (jul 2017), 236–246. https://doi.org/10.1016/j.eswa.2017.02.002  [OA](https://doi.org/10.1016/j.eswa.2017.02.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2017.02.002)

[^Devlin_et+al_2018_a]: Devlin et al. (2018) Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. (2018). https://doi.org/arXiv:1811.03600v2 arXiv:1810.04805  [OA](https://doi.org/arXiv:1811.03600v2)  

[^Guo_et+al_2016_a]: Guo et al. (2016) Li Guo, Feng Shi, and Jun Tu. 2016. Textual analysis and machine leaning: Crack unstructured data in finance and accounting. The Journal of Finance and Data Science 2, 3 (sep 2016), 153–170. https://doi.org/10.1016/J.JFDS.2017.02.001  [OA](https://doi.org/10.1016/J.JFDS.2017.02.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/J.JFDS.2017.02.001)

[^Howard_2018_a]: Howard and Ruder (2018) Jeremy Howard and Sebastian Ruder. 2018. Universal Language Model Fine-tuning for Text Classification. (jan 2018). arXiv:1801.06146 http://arxiv.org/abs/1801.06146  [OA](http://arxiv.org/abs/1801.06146)  

[^Kant_et+al_2018_a]: Kant et al. (2018) Neel Kant, Raul Puri, Nikolai Yakovenko, and Bryan Catanzaro. 2018. Practical Text Classification With Large Pre-Trained Language Models. (2018). arXiv:1812.01207 http://arxiv.org/abs/1812.01207  [OA](http://arxiv.org/abs/1812.01207)  

[^Kraus_2017_a]: Kraus and Feuerriegel (2017) Mathias Kraus and Stefan Feuerriegel. 2017. Decision support from financial disclosures with deep neural networks and transfer learning. Decision Support Systems 104 (2017), 38–48. https://doi.org/10.1016/j.dss.2017.10.001 arXiv:1710.03954  [OA](https://arxiv.org/abs/1710.03954)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2017.10.001)

[^Krishnamoorthy_2018_a]: Krishnamoorthy (2018) Srikumar Krishnamoorthy. 2018. Sentiment analysis of financial news articles using performance indicators. Knowledge and Information Systems 56, 2 (aug 2018), 373–394. https://doi.org/10.1007/s10115-017-1134-1  [OA](https://doi.org/10.1007/s10115-017-1134-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10115-017-1134-1)

[^Li_et+al_2014_a]: Li et al. (2014) Xiaodong Li, Haoran Xie, Li Chen, Jianping Wang, and Xiaotie Deng. 2014. News impact on stock price return via sentiment analysis. Knowledge-Based Systems 69 (oct 2014), 14–23. https://doi.org/10.1016/j.knosys.2014.04.022  [OA](https://doi.org/10.1016/j.knosys.2014.04.022)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.knosys.2014.04.022)

[^Liu_2012_a]: Liu (2012) Bing Liu. 2012. Sentiment Analysis and Opinion Mining. Synthesis Lectures on Human Language Technologies 5, 1 (may 2012), 1–167. https://doi.org/10.2200/s00416ed1v01y201204hlt016  [OA](https://doi.org/10.2200/s00416ed1v01y201204hlt016)  [Scite](/scite_tallies?query=https://doi.org/10.2200/s00416ed1v01y201204hlt016)

[^Loughran_2011_a]: Loughran and Mcdonald (2011) Tim Loughran and Bill Mcdonald. 2011. When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks. Journal of Finance 66, 1 (feb 2011), 35–65. https://doi.org/10.1111/j.1540-6261.2010.01625.x  [OA](https://doi.org/10.1111/j.1540-6261.2010.01625.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2010.01625.x)

[^Loughran_2016_a]: Loughran and Mcdonald (2016) Tim Loughran and Bill Mcdonald. 2016. Textual Analysis in Accounting and Finance: A Survey. Journal of Accounting Research 54, 4 (2016), 1187–1230. https://doi.org/10.1111/1475-679X.12123  [OA](https://doi.org/10.1111/1475-679X.12123)  [Scite](/scite_tallies?query=https://doi.org/10.1111/1475-679X.12123)

[^Lutz_et+al_2018_a]: Lutz et al. (2018) Bernhard Lutz, Nicolas Pröllochs, and Dirk Neumann. 2018. Sentence-Level Sentiment Analysis of Financial News Using Distributed Text Representations and Multi-Instance Learning. Technical Report. arXiv:1901.00400 http://arxiv.org/abs/1901.00400  [OA](http://arxiv.org/abs/1901.00400)  

[^Maia_et+al_2018_a]: Maia et al. (2018a) Macedo Maia, Andr Freitas, and Siegfried Handschuh. 2018a. FinSSLx: A Sentiment Analysis Model for the Financial Domain Using Text Simplification. In 2018 IEEE 12th International Conference on Semantic Computing (ICSC). IEEE, 318–319. https://doi.org/10.1109/ICSC.2018.00065  [OA](https://doi.org/10.1109/ICSC.2018.00065)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ICSC.2018.00065)

[^Maia_et+al_2018_b]: Maia et al. (2018b) Macedo Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross Mcdermott, Manel Zarrouk, Alexandra Balahur, and Ross Mc-Dermott. 2018b. Companion of the The Web Conference 2018 on The Web Conference 2018, {WWW} 2018, Lyon, France, April 23-27, 2018. ACM. https://doi.org/10.1145/3184558  [OA](https://doi.org/10.1145/3184558)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3184558)

[^Malkiel_2003_a]: Malkiel (2003) Burton G Malkiel. 2003. The Efficient Market Hypothesis and Its Critics. Journal of Economic Perspectives 17, 1 (feb 2003), 59–82. https://doi.org/10.1257/089533003321164958  [OA](https://doi.org/10.1257/089533003321164958)  [Scite](/scite_tallies?query=https://doi.org/10.1257/089533003321164958)

[^Malo_et+al_2014_a]: Malo et al. (2014) Pekka Malo, Ankur Sinha, Pekka Korhonen, Jyrki Wallenius, and Pyry Takala. 2014. Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology 65, 4 (2014), 782–796. https://doi.org/10.1002/asi.23062 arXiv:arXiv:1307.5336v2  [OA](https://arxiv.org/abs/1307.5336v2)  [Scite](/scite_tallies?query=https://doi.org/10.1002/asi.23062)

[^Marcus_2018_a]: Marcus (2018) G. Marcus. 2018. Deep Learning: A Critical Appraisal. arXiv e-prints (Jan. 2018). arXiv:cs.AI/1801.00631  [OA](https://engine.scholarcy.com/oa_version?query=Marcus%20G%202018&author=Marcus&title=G&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Marcus%20G%202018) [Scite](/scite_tallies?query=author%3AMarcus%2Ctitle%3AG%2Cyear%3A2018)

[^Martineau_2009_a]: Martineau and Finin (2009) Justin Martineau and Tim Finin. 2009. Delta TFIDF: An Improved Feature Space for Sentiment Analysis.. In ICWSM, Eytan Adar, Matthew Hurst, Tim Finin, Natalie S. Glance, Nicolas Nicolov, and Belle L. Tseng (Eds.). The AAAI Press. http://dblp.uni-trier.de/db/conf/icwsm/icwsm2009.html#MartineauF09  [OA](http://dblp.uni-trier.de/db/conf/icwsm/icwsm2009.html#MartineauF09)  

[^Mccann_et+al_2017_a]: McCann et al. (2017) Bryan McCann, James Bradbury, Caiming Xiong, and Richard Socher. 2017. Learned in Translation: Contextualized Word Vectors. Nips (2017), 1–12. arXiv:1708.00107 http://arxiv.org/abs/1708.00107  [OA](http://arxiv.org/abs/1708.00107)  

[^Merity_et+al_2017_a]: Merity et al. (2017) Stephen Merity, Nitish Shirish Keskar, and Richard Socher. 2017. Regularizing and Optimizing LSTM Language Models. CoRR abs/1708.02182 (2017). arXiv:1708.02182 http://arxiv.org/abs/1708.02182  [OA](http://arxiv.org/abs/1708.02182)  

[^Pennington_et+al_2014_a]: Pennington et al. (2014) Jeffrey Pennington, Richard Socher, and Christopher Manning. 2014. Glove: Global Vectors for Word Representation. In Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP). Association for Computational Linguistics, Doha, Qatar, 1532–1543. https://doi.org/10.3115/v1/D14-1162  [OA](https://doi.org/10.3115/v1/D14-1162)  [Scite](/scite_tallies?query=https://doi.org/10.3115/v1/D14-1162)

[^Peters_et+al_2018_a]: Peters et al. (2018) Matthew E Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and Luke Zettlemoyer. 2018. Deep contextualized word representations. (2018). https://doi.org/10.18653/v1/N18-1202 arXiv:1802.05365  [OA](https://arxiv.org/abs/1802.05365)  [Scite](/scite_tallies?query=https://doi.org/10.18653/v1/N18-1202)

[^Piao_2018_a]: Piao and Breslin (2018) Guangyuan Piao and John G Breslin. 2018. Financial Aspect and Sentiment Predictions with Deep Neural Networks. 1973–1977. https://doi.org/10.1145/3184558.3191829  [OA](https://doi.org/10.1145/3184558.3191829)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3184558.3191829)

[^Severyn_2015_a]: Severyn and Moschitti (2015) Aliaksei Severyn and Alessandro Moschitti. 2015. Twitter Sentiment Analysis with Deep Convolutional Neural Networks. In Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval - SIGIR &amp;#x27;15. ACM Press. https://doi.org/10.1145/2766462.2767830  [OA](https://doi.org/10.1145/2766462.2767830)  [Scite](/scite_tallies?query=https://doi.org/10.1145/2766462.2767830)

[^Sohangir_et+al_2018_a]: Sohangir et al. (2018) Sahar Sohangir, Dingding Wang, Anna Pomeranets, and Taghi M Khoshgoftaar. 2018. Big Data: Deep Learning for financial sentiment analysis. Journal of Big Data 5, 1 (2018). https://doi.org/10.1186/s40537-017-0111-6  [OA](https://doi.org/10.1186/s40537-017-0111-6)  [Scite](/scite_tallies?query=https://doi.org/10.1186/s40537-017-0111-6)

[^Sun_et+al_2019_a]: Sun et al. (2019) Chi Sun, Xipeng Qiu, Yige Xu, and Xuanjing Huang. 2019. How to Fine-Tune BERT for Text Classification? (2019). arXiv:1905.05583 https://arxiv.org/pdf/1905.05583v1.pdfhttp://arxiv.org/abs/1905.05583  [OA](https://arxiv.org/pdf/1905.05583v1.pdfhttp://arxiv.org/abs/1905.05583)  

[^Tripathy_et+al_2016_a]: Tripathy et al. (2016) Abinash Tripathy, Ankit Agrawal, and Santanu Kumar Rath. 2016. Classification of sentiment reviews using n-gram machine learning approach. Expert Systems with Applications 57 (sep 2016), 117–126. https://doi.org/10.1016/j.eswa.2016.03.028  [OA](https://doi.org/10.1016/j.eswa.2016.03.028)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2016.03.028)

[^Vaswani_et+al_2017_a]: Vaswani et al. (2017) Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. 2017. Attention Is All You Need. Nips (2017). arXiv:1706.03762 http://arxiv.org/abs/1706.03762  [OA](http://arxiv.org/abs/1706.03762)  

[^Whitelaw_et+al_2005_a]: Whitelaw et al. (2005) Casey Whitelaw, Navendu Garg, and Shlomo Argamon. 2005. Using appraisal groups for sentiment analysis. In Proceedings of the 14th ACM international conference on Information and knowledge management - CIKM &amp;#x27;05. ACM Press. https://doi.org/10.1145/1099554.1099714  [OA](https://doi.org/10.1145/1099554.1099714)  [Scite](/scite_tallies?query=https://doi.org/10.1145/1099554.1099714)

[^Yang_et+al_2018_a]: Yang et al. (2018) Steve Yang, Jason Rosenfeld, and Jacques Makutonin. 2018. Financial Aspect-Based Sentiment Analysis using Deep Representations. (2018). arXiv:1808.07931 https://arxiv.org/pdf/1808.07931v1.pdfhttp://arxiv.org/abs/1808.07931  [OA](https://arxiv.org/pdf/1808.07931v1.pdfhttp://arxiv.org/abs/1808.07931)  

[^Zhang_et+al_2018_a]: Zhang et al. (2018) Lei Zhang, Shuai Wang, and Bing Liu. 2018. Deep learning for sentiment analysis: A survey. Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery 8, 4 (mar 2018), e1253. https://doi.org/10.1002/widm.1253  [OA](https://doi.org/10.1002/widm.1253)  [Scite](/scite_tallies?query=https://doi.org/10.1002/widm.1253)

[^Zhu_et+al_2015_a]: Zhu et al. (2015) Yukun Zhu, Ryan Kiros, Richard Zemel, Ruslan Salakhutdinov, Raquel Urtasun, Antonio Torralba, and Sanja Fidler. 2015. Aligning Books and Movies: Towards Story-like Visual Explanations by Watching Movies and Reading Books. (jun 2015). arXiv:1506.06724 http://arxiv.org/abs/1506.06724  [OA](http://arxiv.org/abs/1506.06724)  

[^Generated_2024_a]: Generated on Sat Mar 2 15:36:18 2024 by LaTeXML  [OA](https://scholar.google.co.uk/scholar?q=Generated%20on%20Sat%20Mar%202%20153618%202024%20by%20LaTeXML) [GScholar](https://scholar.google.co.uk/scholar?q=Generated%20on%20Sat%20Mar%202%20153618%202024%20by%20LaTeXML) 

