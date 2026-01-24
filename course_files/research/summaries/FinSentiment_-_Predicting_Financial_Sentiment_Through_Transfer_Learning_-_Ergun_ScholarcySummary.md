[[Ergun_FinsentimentPredictingFinancialSentimentThrough_2025]]

# [FinSentiment: Predicting Financial Sentiment Through Transfer Learning](https://doi.org/10.1002/isaf.70015)

## [[Zehra Erva Ergun]]; [[Emre Sefer]]

## Abstract
ABSTRACT There is an increasing interest in financial text mining tasks. Significant progress has been made by using deep learning‐based models on a generic corpus, which also shows reasonable results on financial text mining tasks such as financial sentiment analysis. However, financial sentiment analysis remains demanding due to the scarcity of labeled data in the financial domain and the specialized language. General-purpose deep learning methods are not as effective, mainly because of the specialized language used in the financial context. In this study, we focus on improving the performance of financial text mining tasks by enhancing existing pretrained language models through NLP transfer learning. Pretrained language models require only a small number of labeled samples and can be further improved by training them on domain‐specific corpora. We propose an enhanced model, FinSentiment, that incorporates versions of several recently proposed pretrained models, such as BERT, XLNet, RoBERTa, GPT, Llama, and T5, and trains them on financial-domain corpora to better perform across NLP tasks in the financial domain. The corresponding finance‐specific models in FinSentiment are called Fin‐BERT, Fin‐XLNet, Fin‐RoBERTa, Fin‐GPT, Fin‐Llama, and Fin‐T5, respectively. We also propose variants of these models jointly trained over the financial domain and general corpora. Our finance‐specific FinSentiment models generally show the best performance across three financial sentiment analysis datasets, even when only a subset of these models is fine‐tuned on a smaller training set. Our results show improvements across all tested performance criteria relative to the existing results for these datasets. Extensive experimental results demonstrate the effectiveness and robustness of RoBERTa, especially when pretrained on financial corpora. Overall, we show that NLP transfer learning techniques are favorable solutions to financial sentiment analysis tasks. Our source code has been deposited at https://github.com/seferlab/finsentiment.

## Key concepts
#sentiment_analysis; #natural_language_processing; #claim/language_models; #language_models; #finding/xlnet; #xlnet; #finding/BERT; #BERT; #finding/RoBERTa; #RoBERTa

## Quote
The study proposes FinSentiment, a model for financial sentiment analysis that incorporates enhanced neural language models and evaluates its performance on three sentiment datasets, outperforming state-of-the-art methods.

## Key points
- Asset prices in an open economy mirror all the existing knowledge about these assets trading in a market ([^Malkiel_2003_a]; [^Gezici_2024_a]; [^Seyhan_2023_a]; [^Tuncer_et+al_2022_a])
- Our model FinSentiment in the table represents the best performance over Fin-­BERT, Fin-XLNet, and Fin-­RoBERTa finance-­specific models
- BERT, XLNet, and RoBERTa enhance the performance remarkably on all evaluation metrics, and the models do not perform significantly better in certain classes than in the remaining classes
- FinSentiment models better perform across sentiment analysis tasks in the financial domain by training these models on financial domain corpora
- We have evaluated the performance of FinSentiment models over three different sentiment datasets
- When compared with the baseline and non-finance specific models, our results indicate the success of pretrained language models (LMs) for a subsequent task, such as financial sentiment analysis, by using only a tiny labeled dataset


## Summary

### Introduction
The study focuses on financial sentiment analysis, a crucial task in the financial domain, which involves categorizing text as neutral, negative, or positive.
The financial domain poses unique challenges, including insufficient labeled data and specialized language.
To address these challenges, the study proposes FinSentiment, an enhanced model that incorporates pretrained language models, such as BERT, XLNet, RoBERTa, GPT, Llama, and T5, and is fine-tuned on financial-domain corpora.

### Methodology
The study utilizes NLP transfer learning techniques to improve the performance of financial sentiment analysis tasks.
The proposed FinSentiment models are trained on financial domain corpora and fine-tuned on smaller training sets.
The study also investigates the effects of training strategies, extra pretraining over a financial corpus, and fine-tuning a tiny subset of model layers solely to decrease training time without a significant performance decrease.

### Results
The FinSentiment models demonstrate state-of-the-art results on three financial sentiment analysis datasets, outperforming existing models.
The study finds that RoBERTa, pretrained on financial corpora, exhibits exceptional performance and robustness.
The results highlight the effectiveness of NLP transfer learning techniques for financial sentiment analysis, and the study makes the source code and pretrained models publicly available.

### Background
Financial sentiment analysis differs from general sentiment analysis in its aims and domain perspectives, focusing on predicting market reactions to textual information.
Traditional machine learning-based approaches have limitations in representing semantic knowledge, while deep learning-based approaches require large amounts of data.
Researchers have applied various deep learning models, including LSTM, CNN, and transformer-based models, to financial sentiment analysis.

### Pretrained Models
Pretrained language models, such as ELMo, ULMFit, BERT, XLNet, and RoBERTa, have achieved state-of-the-art results in various NLP tasks, including text classification.
These models can be fine-tuned for specific tasks, including financial sentiment analysis.
FinBERT, a domain-specific adaptation of BERT, has been proposed for financial text mining tasks.
Other models, such as GPT and T5, have also been applied to financial sentiment analysis.

### Methods
Unsupervised pretraining of language models on large text corpora has improved the performance of NLP tasks.
Domain-specific adaptations of BERT, XLNet, and RoBERTa, named Fin-BERT, Fin-XLNet, and Fin-RoBERTa, have been proposed for financial sentiment analysis.
These models combine the strengths of unsupervised pretraining with extensive financial data to improve financial applications.
LSTM and transformer-based models serve as the underlying neural network architectures, leveraging techniques such as contextualized embeddings and attention mechanisms.

### Models
Transformer models have advantages over recurrent neural network models, including the ability to be parallelized over GPUs.
BERT is a language model composed of multiple transformer encoders that uses a masked language modeling task to predict masked tokens.
BERT has two versions: BERT-base and BERT-large, with different numbers of encoder layers and trainable parameters.
Other models, such as XLNet, RoBERTa, and GPT, have been developed with various enhancements, including permutation-based objectives, dynamic masking, and reversible tokenization.
Several models are used for sentiment analysis, including LSTM classifiers with GLoVe and ELMo embeddings, BERT, XLNet, RoBERTa, GPT, Llama, and T5.
The Fin-­BERT, Fin-­XLNet, and Fin-­RoBERTa models are finance-domain-specific models that outperform general models.
The models are trained using 10-fold cross-validation and evaluated using cross-entropy loss, macro-average F1, and accuracy.

### Finetuning
Finetuning of pre-trained language models, such as BERT, can be performed for specific tasks, such as sentiment classification and regression.
Fin-BERT is a finetuned version of BERT for the financial domain and can be implemented by adding additional pretraining on financial-domain corpora.
Techniques like gradual unfreezing, discriminative fine-tuning, and slanted triangular learning rates can be used to prevent catastrophic forgetting.
Other models, such as Fin-XLNet, Fin-RoBERTa, Fin-GPT, Fin-Llama, and Fin-T5, can also be finetuned for the financial domain.

### Datasets
The datasets used for training and testing the models include corporate reports and filings, such as 10-K and 10-Q filings, as well as financial news articles, such as the Financial PhraseBank dataset.
These datasets provide a large amount of textual data for training and testing models and can be used to evaluate their performance on tasks such as sentiment analysis.
The Financial PhraseBank dataset consists of 4840 English sentences chosen randomly from a financial news database, labeled by people with a finance or economics background.
The FiQA dataset contains 1174 examples of news headlines and tweets, each with a sentence, a sentence snippet, aspects, and a sentiment score.
The AnalystTone dataset measures judgments and beliefs in analyst reports, consisting of 10,000 randomly selected sentences.

### Performance Evaluation
The finance-domain-specific FinSentiment models outperform general models across almost all evaluation criteria.
The results show that FinSentiment clearly outperforms all the existing methods across all metrics, including accuracy, F1 score, and cross-entropy loss.
The performance of the models increases with the number of samples in the training dataset, and FinSentiment begins to efficiently differentiate between labels with 250 samples.

### Model Performance
FinSentiment outperforms LSTM classifiers and other existing models, including state-of-the-art models, in financial sentiment analysis tasks.
The results show that FinSentiment performs better with 250 samples than LSTM classifiers with all samples.
Fin-­BERT, Fin-­XLNet, and Fin-­RoBERTa, which are part of FinSentiment, outperform their general counterparts in terms of accuracy.
FinSentiment models outperform state-of-the-art methods in sentiment analysis tasks in the financial domain.
The models, including Fin-BERT, Fin-XLNet, and Fin-RoBERTa, achieve higher accuracy and F1 scores than baseline approaches.
Fine-tuning the models on financial-domain corpora improves their performance, with Fin-RoBERTa performing best.
The models can achieve good performance even with a small labeled dataset, such as 500 samples.

### Domain-Specific Training
Domain-specific training is crucial for financial sentiment analysis tasks.
Finance-specific models, such as Fin-­BERT, Fin-­XLNet, and Fin-­RoBERTa, outperform their general counterparts, even when trained on a different dataset.
The results show that finance-specific models outperform general models, even when the training and test datasets differ.

### Catastrophic Forgetting Prevention
Techniques such as slanted triangular learning rate, gradual unfreezing, and discriminative fine-tuning can help prevent catastrophic forgetting in finance-specific models.
The results show that using these techniques can improve the performance of Fin-­BERT and Fin-­RoBERTa models, with gradual unfreezing being the most effective strategy.

### Fine-Tuning And Evaluation
Fine-tuning the final k many encoder layers or the complete model solely can improve the performance of FinSentiment models.
However, fine-tuning the classification layer solely does not perform as well.
The models are evaluated using 10-fold cross-validation, and the results are similar when using fivefold cross-validation.
Bagging (Bootstrap Aggregation) can also improve model performance.

### Analysis And Future Work
The models are analyzed to identify where they fail to predict the true label, and it is found that they tend to predict neutral sentences as positive.
Future work includes improving classification models, expanding the model catalog, and using the trained finance-specific models on stock market price datasets to predict returns and volatility.
Additionally, the models can be used for financial text-mining tasks, such as question answering and named-entity recognition.


## Study subjects

### 3 financial sentiment analysis datasets
- We also propose variants of these models jointly trained over the financial domain and general corpora. Our finance-­specific FinSentiment models, in general, show the best performance across three financial sentiment analysis datasets, even when only a subpart of these models is fine-­tuned with a smaller training set. Our results exhibit enhancement for each of the tested performance criteria on the existing results for these datasets

### 3 financial sentiment analysis datasets
- We also propose variants of these models jointly trained over the financial domain and general corpora. Our finance‐specific FinSentiment models generally show the best performance across three financial sentiment analysis datasets, even when only a subset of these models is fine‐tuned on a smaller training set. Our results exhibit enhancement for each of the tested performance criteria on the existing results for these datasets

## Data analysis
- #method/llama_model
- #method/roberta_model
- #method/bert_model
- #method/gpt_model

## Findings
- (2) Then, we initialize the downstream models by using the parameters learned over the LM task. <mark class="claim">By following these two consecutive steps, we can achieve a significantly better performance</mark>
- <mark class="claim">BERT, XLNet, and RoBERTa enhance the performance remarkably on all evaluation metrics, and the models do not perform significantly better in certain classes than the remaining classes</mark>
- <mark class="claim">We observe similar results in terms of F1 score as well</mark>
- <mark class="claim">Table 9 shows the results, <mark class="fact">where we have evaluated the models with respect to macro average F1 score</mark>, accuracy, and loss over the test set</mark>
- <mark class="claim">On all of the used datasets, we have significantly outperformed the state-­of-­the-­art methods</mark>
- For sentiment classification tasks, FinSentiment has outperformed the existing generally trained versions and baselines by more than 10% in terms of accuracy and F1 scores

##  Builds on previous research
- Furthermore, solutions to domain-­specificity have been introduced in different research areas, such as defining a specialized language for biomedical studies. [^Lee_et+al_2020_a]) have implemented BioBERT for biological text mining tasks, achieving outstanding performance across a range of tasks, including biomedical question answering, biomedical relation extraction, and biomedical named-­entity recognition. [^Asgari_2015_a]) have presented an unsupervised, data-­driven approach to represent and extract features from biological sequences, which are then used in a number of machine learning applications. However, they are not trained on a variety of financial tasks as we did.
- All general models without finance-specific training again outperform LSTM models with different embeddings, similar to the Financial PhraseBank dataset. We use the reported results from state-of-the-art papers (S. [^Yang_et+al_2018_a]; [^Piao_2018_a]), which use the official FiQA Task 1 test set.

## Differs from previous work
- In other attempts, [^Yang_et+al_2023_a] and [^Todt_et+al_2023_a] have been proposed. However, they are not trained on a variety of financial tasks as we did.

##  Confirmation of earlier findings
- Lastly, Section 6 summarizes our findings and concludes the paper. Asset prices in an open economy mirror all the existing knowledge about these assets trading in a market ([^Malkiel_2003_a]; [^Gezici_2024_a]; [^Seyhan_2023_a]; [^Tuncer_et+al_2022_a]).

## Contributions
- In this research, we have come up with a FinSentiment model for financial tasks, which incorporates enhanced versions of a number of recently-­proposed neural LMs, such as BERT, XLNet, and RoBERTa. The corresponding finance-­specific models in FinSentiment are called Fin-­BERT, Fin-­XLNet, and Fin-RoBERTa, respectively. <mark class="fact">In general, FinSentiment models better perform across sentiment analysis tasks in the financial domain</mark> by training these models on financial domain corpora. To our best knowledge, this is the first study to investigate the performance of finetuning commonly used pretrained neural LMs in the financial domain and tasks. Additionally, it is one <mark class="fact">of the limited comprehensive studies that focus on additional pretraining over domain-­specific corpora</mark>. <mark class="claim"><mark class="fact">We have evaluated the performance of FinSentiment models over three different sentiment datasets</mark></mark>. <mark class="claim">On all of the used datasets, we have significantly outperformed the state-­of-­the-­art methods</mark>. For instance, for sentiment classification tasks, FinSentiment has outperformed the existing generally trained versions and baselines by more than 10% in terms of accuracy and F1 scores.

## Limitations
- The study has limitations, including the use of a small number of datasets and the potential for overfitting. The study also notes that FinSentiment model performance may vary across datasets and tasks.

## Future work
- The study suggests future work, including improving the finance-specific models for classification purposes and regression purposes. The study also suggests exploring the use of FinSentiment models for other NLP tasks in the financial domain.
- The future work suggested by the study includes improving the proposed finance-specific models and mechanisms for classification purposes in terms of aspect levels and regression purposes. The study also suggests using the trained finance-specific models with stock market price datasets to predict stock return volatility.


## References
[^Abadi_et+al_2015_a]: Abadi M., Agarwal A., Barham P. et al. 2015. TensorFlow: Large-­Scale Machine Learning on Heterogeneous Systems, Software Available From tensorflow.org https://www.tensorflow.org/.  [OA](https://www.tensorflow.org/)  

[^Agarwal_2016_a]: Agarwal, B., and N. Mittal. 2016. Machine Learning Approach for Sentiment Analysis, 21–45. Springer International Publishing. https://doi.org/10.1007/978-­3 -­3 19-­2 5343 -­5_3.  [OA](https://doi.org/10.1007/978-­3)  [Scite](/scite_tallies?query=https://doi.org/10.1007/978-­3)

[^Araci_2019_a]: Araci, D. 2019. “Finbert: Financial Sentiment Analysis With Pre-Trained Language Models.” CoRR: abs/1908.10063 arXiv:1908.10063.  [OA](https://arxiv.org/abs/1908.10063)  

[^Araque_et+al_2017_a]: Araque, O., I. Corcuera-Platas, J. F. Sánchez-Rada, and C. A. Iglesias. 2017. “Enhancing Deep Learning Sentiment Analysis With Ensemble Techniques in Social Applications.” Expert Systems With Applications 77: 236–246.  [OA](https://engine.scholarcy.com/oa_version?query=Araque%2C%20O.%20Corcuera-%C2%ADPlatas%2C%20I.%20S%C3%A1nchez-%C2%ADRada%2C%20J.F.%20Iglesias%2C%20C.A.%20Enhancing%20Deep%20Learning%20Sentiment%20Analysis%20With%20Ensemble%20Techniques%20in%20Social%20Applications%202017&author=Araque&title=Enhancing%20Deep%20Learning%20Sentiment%20Analysis%20With%20Ensemble%20Techniques%20in%20Social%20Applications&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Araque%2C%20O.%20Corcuera-%C2%ADPlatas%2C%20I.%20S%C3%A1nchez-%C2%ADRada%2C%20J.F.%20Iglesias%2C%20C.A.%20Enhancing%20Deep%20Learning%20Sentiment%20Analysis%20With%20Ensemble%20Techniques%20in%20Social%20Applications%202017) [Scite](/scite_tallies?query=author%3AAraque%2Ctitle%3AEnhancing%20Deep%20Learning%20Sentiment%20Analysis%20With%20Ensemble%20Techniques%20in%20Social%20Applications%2Cyear%3A2017)

[^Asgari_2015_a]: Asgari, E., and M. R. Mofrad. 2015. “Continuous Distributed Representation of Bi-­Ological Sequences for Deep Proteomics and Genomics.” PLoS ONE 10, no. 11: e0141287.  [OA](https://engine.scholarcy.com/oa_version?query=Asgari%2C%20E.%20R%2C%20M.%20Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%202015&author=Asgari&title=Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Asgari%2C%20E.%20R%2C%20M.%20Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%202015) [Scite](/scite_tallies?query=author%3AAsgari%2Ctitle%3AContinuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%2Cyear%3A2015)

[^Black_et+al_2021_a]: Black, S., G. Leo, P. Wang, C. Leahy, and S. Biderman. 2021. “GPT-Neo: Large Scale Autoregressive Language Modeling With Mesh-Tensorflow.” Zenodo. https://doi.org/10.5281/zenodo.5297715.  [OA](https://doi.org/10.5281/zenodo.5297715)  [Scite](/scite_tallies?query=https://doi.org/10.5281/zenodo.5297715)

[^Breiman_1996_a]: Breiman, L. 1996. “Bagging Predictors.” Machine Learning 24, no. 2: 123–140. https://doi.org/10.1007/BF000 58655.  [OA](https://doi.org/10.1007/BF000)  [Scite](/scite_tallies?query=https://doi.org/10.1007/BF000)

[^Brown_et+al_2020_a]: Brown, T. B., B. Mann, N. Ryder, et al. 2020. “Language Models Are Few-Shot Learners.” arXiv 2005: 14165. https://arxiv.org/abs/2005.14165.  [OA](https://arxiv.org/abs/2005.14165)  

[^Child_et+al_2019_a]: Child, R., S. Gray, A. Radford, and I. Sutskever. 2019. “Generating Long Sequences With Sparse Transformers.” arXiv: 1904.10509. https://arxiv.org/abs/1904.10509.  [OA](https://arxiv.org/abs/1904.10509)  

[^Chowdhery_et+al_2022_a]: Chowdhery, A., S. Narang, J. Devlin, et al. 2022. “Palm: Scaling Language Modeling With Pathways.” arXiv: 2204.02311. https://arxiv.org/abs/2204.02311.  [OA](https://arxiv.org/abs/2204.02311)  

[^Desola_et+al_2019_a]: Desola, V., K. Hanna, and P. Nonis. 2019. Finbert: Pre-­Trained Model on Sec Filings for Financial Natural Language Tasks, Tech. Rep.  [OA](https://scholar.google.co.uk/scholar?q=Desola%2C%20V.%20Hanna%2C%20K.%20Nonis%2C%20P.%20Finbert%3A%20Pre-%C2%ADTrained%20Model%20on%20Sec%20Filings%20for%20Financial%20Natural%20Language%20Tasks%2C%20Tech%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Desola%2C%20V.%20Hanna%2C%20K.%20Nonis%2C%20P.%20Finbert%3A%20Pre-%C2%ADTrained%20Model%20on%20Sec%20Filings%20for%20Financial%20Natural%20Language%20Tasks%2C%20Tech%202019) 

[^Devlin_et+al_2019_a]: Devlin, J., M.-­W. Chang, K. Lee, and K. Toutanova. 2019. “BERT: Pre-­Training of Deep Bidirectional Transformers for Language Understanding.” In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), 4171–4186.  [OA](https://scholar.google.co.uk/scholar?q=Devlin%2C%20J.%20Chang%2C%20M.-%C2%ADW.%20Lee%2C%20K.%20Toutanova%2C%20K.%20BERT%3A%20Pre-%C2%ADTraining%20of%20Deep%20Bidirectional%20Transformers%20for%20Language%20Understanding%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Devlin%2C%20J.%20Chang%2C%20M.-%C2%ADW.%20Lee%2C%20K.%20Toutanova%2C%20K.%20BERT%3A%20Pre-%C2%ADTraining%20of%20Deep%20Bidirectional%20Transformers%20for%20Language%20Understanding%202019) 

[^Minneapolis_0000_a]: Minneapolis, Minnesota: Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Minneapolis%20Minnesota%20Association%20for%20Computational%20Linguistics) [GScholar](https://scholar.google.co.uk/scholar?q=Minneapolis%20Minnesota%20Association%20for%20Computational%20Linguistics) 

[^Gezici_2024_a]: Gezici, A. H. B., and E. Sefer. 2024. “Deep Transformer-­Based Asset Price and Direction Prediction.” IEEE Access 12: 24164–24178. https://doi.org/10.1109/ACCESS.2024.3358452.  [OA](https://doi.org/10.1109/ACCESS.2024.3358452)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2024.3358452)

[^González-­Sánchez_2021_a]: González-Sánchez, M., and M. E. Morales Vega. 2021. “Influence of Bloomberg&#39;s Investor Sentiment Index: Evidence From European Union Financial Sector.” Mathematics 9, no. 4: 297.  [OA](https://engine.scholarcy.com/oa_version?query=Gonz%C3%A1lez-%C2%ADS%C3%A1nchez%2C%20M.%20Vega%2C%20M.E.Morales%20Influence%20of%20Bloomberg%27s%20Investor%20Sentiment%20Index%3A%20Evidence%20From%20European%20Union%20Financial%20Sector%202021&author=Gonz%C3%A1lez-%C2%ADS%C3%A1nchez&title=Influence%20of%20Bloomberg%27s%20Investor%20Sentiment%20Index%3A%20Evidence%20From%20European%20Union%20Financial%20Sector&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Gonz%C3%A1lez-%C2%ADS%C3%A1nchez%2C%20M.%20Vega%2C%20M.E.Morales%20Influence%20of%20Bloomberg%27s%20Investor%20Sentiment%20Index%3A%20Evidence%20From%20European%20Union%20Financial%20Sector%202021) [Scite](/scite_tallies?query=author%3AGonz%C3%A1lez-%C2%ADS%C3%A1nchez%2Ctitle%3AInfluence%20of%20Bloomberg%27s%20Investor%20Sentiment%20Index%3A%20Evidence%20From%20European%20Union%20Financial%20Sector%2Cyear%3A2021)

[^Hochreiter_1997_a]: Hochreiter, S., and J. Schmidhuber. 1997. “Long Short-­Term Memory.” Neural Computation 9, no. 8: 1735–1780.  [OA](https://engine.scholarcy.com/oa_version?query=Hochreiter%2C%20S.%20Schmidhuber%2C%20J.%20Long%20Short-%C2%ADTerm%20Memory%201997&author=Hochreiter&title=Long%20Short-%C2%ADTerm%20Memory&year=1997) [GScholar](https://scholar.google.co.uk/scholar?q=Hochreiter%2C%20S.%20Schmidhuber%2C%20J.%20Long%20Short-%C2%ADTerm%20Memory%201997) [Scite](/scite_tallies?query=author%3AHochreiter%2Ctitle%3ALong%20Short-%C2%ADTerm%20Memory%2Cyear%3A1997)

[^Howard_2018_a]: Howard, J., and S. Ruder. 2018. “Universal Language Model Fine-Tuning for Text Classification.” In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 328–339.  [OA](https://scholar.google.co.uk/scholar?q=Howard%2C%20J.%20Ruder%2C%20S.%20Universal%20Language%20Model%20Fine-Tuning%20for%20Text%20Classification%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Howard%2C%20J.%20Ruder%2C%20S.%20Universal%20Language%20Model%20Fine-Tuning%20for%20Text%20Classification%202018) 

[^Melbourne_0000_b]: Melbourne, Australia: Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Melbourne%20Australia%20Association%20for%20Computational%20Linguistics) [GScholar](https://scholar.google.co.uk/scholar?q=Melbourne%20Australia%20Association%20for%20Computational%20Linguistics) 

[^Hu_et+al_2021_a]: Hu, E. J., Y. Shen, P. Wallis, et al. 2021. “Lora: Low-­Rank Adaptation of Large Language Models.” arXiv:2106.09685. https://arxiv.org/abs/2106.09685.  [OA](https://arxiv.org/abs/2106.09685)  

[^Huang_et+al_2014_a]: Huang, A. H., A. Y. Zang, and R. Zheng. 2014. “Evidence on the Information Content of Text in Analyst Reports.” Accounting Review 89, no. 6: 2151–2180.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20A.H.%20Zang%2C%20A.Y.%20Zheng%2C%20R.%20Evidence%20on%20the%20Information%20Content%20of%20Text%20in%20Analyst%20Reports%202014&author=Huang&title=Evidence%20on%20the%20Information%20Content%20of%20Text%20in%20Analyst%20Reports&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20A.H.%20Zang%2C%20A.Y.%20Zheng%2C%20R.%20Evidence%20on%20the%20Information%20Content%20of%20Text%20in%20Analyst%20Reports%202014) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AEvidence%20on%20the%20Information%20Content%20of%20Text%20in%20Analyst%20Reports%2Cyear%3A2014)

[^Kant_et+al_2018_a]: Kant, N., R. Puri, N. Yakovenko, and B. Catanzaro. 2018. “Practical Text Classification With Large Pre-­Trained Language Models.” ArXiv abs/1812.01207.  [OA](https://arxiv.org/abs/1812.01207)  

[^Kingma_2017_a]: Kingma, D. P., and J. Ba. 2017. “Adam: A Method for Stochastic Optimization.” arXiv: 1412.6980. https://arxiv.org/abs/1412.6980.  [OA](https://arxiv.org/abs/1412.6980)  

[^Kraus_2017_a]: Kraus, M., and S. Feuerriegel. 2017. “Decision Support From Financial Disclosures With Deep Neural Networks and Transfer Learning.” Decision Support Systems 104: 10.  [OA](https://engine.scholarcy.com/oa_version?query=Kraus%2C%20M.%20Feuerriegel%2C%20S.%20Decision%20Support%20From%20Financial%20Disclosures%20With%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%202017&author=Kraus&title=Decision%20Support%20From%20Financial%20Disclosures%20With%20Deep%20Neural%20Networks%20and%20Transfer%20Learning&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Kraus%2C%20M.%20Feuerriegel%2C%20S.%20Decision%20Support%20From%20Financial%20Disclosures%20With%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%202017) [Scite](/scite_tallies?query=author%3AKraus%2Ctitle%3ADecision%20Support%20From%20Financial%20Disclosures%20With%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%2Cyear%3A2017)

[^Lee_et+al_2020_a]: Lee, J., W. Yoon, S. Kim, et al. 2020. “Biobert: A Pre-­Trained Biomedical Language Representation Model for Biomedical Text Mining.” Bioinformatics 36, no. 4: 1234–1240.  [OA](https://engine.scholarcy.com/oa_version?query=Lee%2C%20J.%20Yoon%2C%20W.%20Kim%2C%20S.%20Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%202020&author=Lee&title=Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Lee%2C%20J.%20Yoon%2C%20W.%20Kim%2C%20S.%20Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%202020) [Scite](/scite_tallies?query=author%3ALee%2Ctitle%3ABiobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%2Cyear%3A2020)

[^Li_et+al_2014_a]: Li, X., H. Xie, L. Chen, J. Wang, and X. Deng. 2014. “News Impact on Stock Price Return via Sentiment Analysis.” Knowledge-­Based Systems 69: 14–23.  [OA](https://engine.scholarcy.com/oa_version?query=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20News%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%202014&author=Li&title=News%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20News%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%202014) [Scite](/scite_tallies?query=author%3ALi%2Ctitle%3ANews%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%2Cyear%3A2014)

[^Liu_2012_a]: Liu, B. 2012. Sentiment Analysis and Opinion Mining. Morgan &amp; Claypool Publishers.  [OA](https://scholar.google.co.uk/scholar?q=Liu%2C%20B.%20Sentiment%20Analysis%20and%20Opinion%20Mining%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20B.%20Sentiment%20Analysis%20and%20Opinion%20Mining%202012) 

[^Liu_et+al_2019_a]: Liu, Y., M. Ott, N. Goyal, et al. 2019. “Roberta: A Robustly Optimized BERT Pre-­Training Approach.” arXiv preprint arXiv:1907.11692.  [OA](https://arxiv.org/abs/1907.11692)  

[^Liu_et+al_2020_a]: Liu, Z., D. Huang, K. Huang, Z. Li, and J. Zhao. 2020. “Finbert: A Pre-­Trained Financial Language Representation Model for Financial Text Mining.” In Proceedings of the Twenty-­Ninth International Joint Conference on Artificial Intelligence, IJCAI-­20, edited by C. Bessiere, 4513–4519. International Joint Conferences on Artificial Intelligence Organization Special Track on AI in FinTech.  [OA](https://scholar.google.co.uk/scholar?q=Liu%2C%20Z.%20Huang%2C%20D.%20Huang%2C%20K.%20Li%2C%20Z.%20Finbert%3A%20A%20Pre-%C2%ADTrained%20Financial%20Language%20Representation%20Model%20for%20Financial%20Text%20Mining%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Z.%20Huang%2C%20D.%20Huang%2C%20K.%20Li%2C%20Z.%20Finbert%3A%20A%20Pre-%C2%ADTrained%20Financial%20Language%20Representation%20Model%20for%20Financial%20Text%20Mining%202020) 

[^Loughran_2011_a]: Loughran, T., and B. McDonald. 2011. “When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-­Ks.” Journal of Finance 66, no. 1: 35–65.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20Mcdonald%2C%20B.%20When%20Is%20a%20Liability%20Not%20a%20Liability%3F%20Textual%20Analysis%2C%20Dictionaries%2C%20and%2010-%C2%ADKs%202011&author=Loughran&title=When%20Is%20a%20Liability%20Not%20a%20Liability%3F%20Textual%20Analysis%2C%20Dictionaries%2C%20and%2010-%C2%ADKs&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20Mcdonald%2C%20B.%20When%20Is%20a%20Liability%20Not%20a%20Liability%3F%20Textual%20Analysis%2C%20Dictionaries%2C%20and%2010-%C2%ADKs%202011) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3AWhen%20Is%20a%20Liability%20Not%20a%20Liability%3F%20Textual%20Analysis%2C%20Dictionaries%2C%20and%2010-%C2%ADKs%2Cyear%3A2011)

[^Loughran_2016_a]: Loughran, T., and B. McDonald. 2016. “Textual Analysis in Accounting and Finance: A Survey.” Journal of Accounting Research 54, no. 4: 1187–1230.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20McDonald%2C%20B.%20Textual%20Analysis%20in%20Accounting%20and%20Finance%3A%20A%20Survey%202016&author=Loughran&title=Textual%20Analysis%20in%20Accounting%20and%20Finance%3A%20A%20Survey&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20McDonald%2C%20B.%20Textual%20Analysis%20in%20Accounting%20and%20Finance%3A%20A%20Survey%202016) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3ATextual%20Analysis%20in%20Accounting%20and%20Finance%3A%20A%20Survey%2Cyear%3A2016)

[^Lutz_et+al_2019_a]: Lutz, B., N. Pröllochs, and D. Neumann. 2019. “Sentence-­Level Sentiment Analysis of Financial News Using Distributed Text Representations and Multi-­Instance Learning.” ArXiv: abs/1901.00400.  [OA](https://arxiv.org/abs/1901.00400)  

[^Maia_et+al_2018_a]: Maia, M., A. Freitas, and S. Handschuh. 2018. “Finsslx: A Sentiment Analysis Model for the Financial Domain Using Text Simplification.” In 2018, IEEE 12th International Conference on Semantic Computing (ICSC), 318–319. Los Alamitos, CA, USA: IEEE Computer Society.  [OA](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Freitas%2C%20A.%20Handschuh%2C%20S.%20Finsslx%3A%20A%20Sentiment%20Analysis%20Model%20for%20the%20Financial%20Domain%20Using%20Text%20Simplification%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Freitas%2C%20A.%20Handschuh%2C%20S.%20Finsslx%3A%20A%20Sentiment%20Analysis%20Model%20for%20the%20Financial%20Domain%20Using%20Text%20Simplification%202018) 

[^Maia_et+al_2018_b]: Maia, M., S. Handschuh, A. Freitas, et al. 2018. “WWW′18 Open Challenge: Financial Opinion Mining and Question Answering.” In  [OA](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20WWW%E2%80%B218%20Open%20Challenge%3A%20Financial%20Opinion%20Mining%20and%20Question%20Answering%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20WWW%E2%80%B218%20Open%20Challenge%3A%20Financial%20Opinion%20Mining%20and%20Question%20Answering%202018) 

[^Companion_1942_a]: Companion Proceedings of the the Web Conference 2018, WWW&#39;18, 1941– 1942. Republic and Canton of Geneva, CHE: International World Wide Web Conferences Steering Committee.  [OA](https://scholar.google.co.uk/scholar?q=Companion%20Proceedings%20of%20the%20the%20Web%20Conference%202018%20WWW18%201941%201942%20Republic%20and%20Canton%20of%20Geneva%20CHE%20International%20World%20Wide%20Web%20Conferences%20Steering%20Committee) [GScholar](https://scholar.google.co.uk/scholar?q=Companion%20Proceedings%20of%20the%20the%20Web%20Conference%202018%20WWW18%201941%201942%20Republic%20and%20Canton%20of%20Geneva%20CHE%20International%20World%20Wide%20Web%20Conferences%20Steering%20Committee) 

[^Maks_2010_a]: Maks, I., and P. Vossen. 2010. Annotation Scheme and Gold Standard for Dutch Subjective Adjectives. LREC.  [OA](https://scholar.google.co.uk/scholar?q=Maks%2C%20I.%20Vossen%2C%20P.%20Annotation%20Scheme%20and%20Gold%20Standard%20for%20Dutch%20Subjective%20Adjectives%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Maks%2C%20I.%20Vossen%2C%20P.%20Annotation%20Scheme%20and%20Gold%20Standard%20for%20Dutch%20Subjective%20Adjectives%202010) 

[^Malkiel_2003_a]: Malkiel, B. G. 2003. “The Efficient Market Hypothesis and Its Critics.” Journal of Economic Perspectives 17, no. 1: 59–82.  [OA](https://engine.scholarcy.com/oa_version?query=Malkiel%2C%20B.G.%20The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%202003&author=Malkiel&title=The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Malkiel%2C%20B.G.%20The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%202003) [Scite](/scite_tallies?query=author%3AMalkiel%2Ctitle%3AThe%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%2Cyear%3A2003)

[^Malo_et+al_2014_a]: Malo, P., A. Sinha, P. Korhonen, J. Wallenius, and P. Takala. 2014. “Good Debt or Bad Debt: Detecting Semantic Orientations in Economic Texts.” Journal of the Association for Information Science and Technology 65, no. 4: 782–796.  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20Debt%20or%20Bad%20Debt%3A%20Detecting%20Semantic%20Orientations%20in%20Economic%20Texts%202014&author=Malo&title=Good%20Debt%20or%20Bad%20Debt%3A%20Detecting%20Semantic%20Orientations%20in%20Economic%20Texts&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20Debt%20or%20Bad%20Debt%3A%20Detecting%20Semantic%20Orientations%20in%20Economic%20Texts%202014) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20Debt%20or%20Bad%20Debt%3A%20Detecting%20Semantic%20Orientations%20in%20Economic%20Texts%2Cyear%3A2014)

[^Malo_et+al_2013_a]: Malo, P., A. Sinha, P. Takala, P. Korhonen, and J. Wallenius. 2013. Financialphrasebank-v­ 1.0 (07 2013).  [OA](https://engine.scholarcy.com/oa_version?query=Malo%20P%20A%20Sinha%20P%20Takala%20P%20Korhonen%20and%20J%20Wallenius%202013%20Financialphrasebankv%2010%2007%202013&author=Malo&title=&year=2013) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%20P%20A%20Sinha%20P%20Takala%20P%20Korhonen%20and%20J%20Wallenius%202013%20Financialphrasebankv%2010%2007%202013) [Scite](/scite_tallies?query=Malo%2C%20P.%2C%20A.%20Sinha%2C%20P.%20Takala%2C%20P.%20Korhonen%2C%20and%20J.%20Wallenius.%202013.%20Financialphrasebank-v%C2%AD%201.0%20%2807%202013%29.)

[^Martineau_2009_a]: Martineau, J., and T. Finin. 2009. “Delta TFIDF: An Improved Feature Space for Sentiment Analysis.” Proceedings of the International AAAI Conference on Web and Social Media 3, no. 1: 258–261. https://ojs.aaai.org/index.php/ICWSM/article/view/13979.  [OA](https://ojs.aaai.org/index.php/ICWSM/article/view/13979)  

[^Mccloskey_1989_a]: McCloskey, M., and N. J. Cohen. 1989. “Catastrophic Interference in Connectionist Networks: The Sequential Learning Problem.” Psychology of Learning and Motivation 24: 104–169.  [OA](https://engine.scholarcy.com/oa_version?query=Mccloskey%2C%20M.%20Cohen%2C%20N.J.%20Catastrophic%20Interference%20in%20Connectionist%20Networks%3A%20The%20Sequential%20Learning%20Problem%201989&author=Mccloskey&title=Catastrophic%20Interference%20in%20Connectionist%20Networks%3A%20The%20Sequential%20Learning%20Problem&year=1989) [GScholar](https://scholar.google.co.uk/scholar?q=Mccloskey%2C%20M.%20Cohen%2C%20N.J.%20Catastrophic%20Interference%20in%20Connectionist%20Networks%3A%20The%20Sequential%20Learning%20Problem%201989) [Scite](/scite_tallies?query=author%3AMccloskey%2Ctitle%3ACatastrophic%20Interference%20in%20Connectionist%20Networks%3A%20The%20Sequential%20Learning%20Problem%2Cyear%3A1989)

[^Mikolov_et+al_2013_a]: Mikolov, T., I. Sutskever, K. Chen, G. Corrado, and J. Dean. 2013. “Distributed Representations of Words and Phrases and Their Compositionality.” In Proceedings of the 26th International Conference on Neural Information Processing Systems-­Volume 2, NIPS &#39;13, 3111– 3119. Red Hook, NY, USA: Curran Associates Inc.  [OA](https://scholar.google.co.uk/scholar?q=Mikolov%2C%20T.%20Sutskever%2C%20I.%20Chen%2C%20K.%20Corrado%2C%20G.%20Distributed%20Representations%20of%20Words%20and%20Phrases%20and%20Their%20Compositionality%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Mikolov%2C%20T.%20Sutskever%2C%20I.%20Chen%2C%20K.%20Corrado%2C%20G.%20Distributed%20Representations%20of%20Words%20and%20Phrases%20and%20Their%20Compositionality%202013) 

[^Min_et+al_2021_a]: Min, B., H. Ross, E. Sulem, et al. 2021. “Recent Advances in Natural Language Processing via Large Pre-­Trained Language Models: A Survey.” arXiv preprint arXiv:2111.01243.  [OA](https://arxiv.org/abs/2111.01243)  

[^Pagolu_et+al_2016_a]: Pagolu, S., K. Reddy, G. Panda, and B. Majhi. 2016. Sentiment Analysis of Twitter Data for Predicting Stock Market Movements, 1345–1350. IEEE. https://doi.org/10.1109/SCOPES.2016.7955659.  [OA](https://doi.org/10.1109/SCOPES.2016.7955659)  [Scite](/scite_tallies?query=https://doi.org/10.1109/SCOPES.2016.7955659)

[^Patro_et+al_2012_a]: Patro, R., G. Duggal, E. Sefer, H. Wang, D. Filippova, and C. Kingsford. 2012. “The Missing Models: A Data-­Driven Approach for Learning How Networks Grow.” In Proceedings of the 18th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD &#39 12, 42–50. New York, NY, USA: Association for Computing Machinery. https://doi.org/10.1145/23395 30.2339541.  [OA](https://doi.org/10.1145/23395)  [Scite](/scite_tallies?query=https://doi.org/10.1145/23395)

[^Patro_et+al_2011_a]: Patro, R., E. Sefer, J. Malin, G. Marçais, S. Navlakha, and C. Kingsford. 2011. “Parsimonious Reconstruction of Network Evolution.” In Algorithms in Bioinformatics, edited by T. M. Przytycka and M.-­F. Sagot, 237–249. Springer Berlin Heidelberg.  [OA](https://scholar.google.co.uk/scholar?q=Patro%2C%20R.%20Sefer%2C%20E.%20Malin%2C%20J.%20Mar%C3%A7ais%2C%20G.%20Parsimonious%20Reconstruction%20of%20Network%20Evolution%202011) [GScholar](https://scholar.google.co.uk/scholar?q=Patro%2C%20R.%20Sefer%2C%20E.%20Malin%2C%20J.%20Mar%C3%A7ais%2C%20G.%20Parsimonious%20Reconstruction%20of%20Network%20Evolution%202011) 

[^Pennington_et+al_2014_a]: Pennington, J., R. Socher, and C. Manning. 2014. “GloVe: Global Vectors for Word Representation.” In Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP), 1532– 1543.  [OA](https://scholar.google.co.uk/scholar?q=Pennington%2C%20J.%20Socher%2C%20R.%20Manning%2C%20C.%20GloVe%3A%20Global%20Vectors%20for%20Word%20Representation%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Pennington%2C%20J.%20Socher%2C%20R.%20Manning%2C%20C.%20GloVe%3A%20Global%20Vectors%20for%20Word%20Representation%202014) 

[^Doha_0000_c]: Doha, Qatar: Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Doha%20Qatar%20Association%20for%20Computational%20Linguistics) [GScholar](https://scholar.google.co.uk/scholar?q=Doha%20Qatar%20Association%20for%20Computational%20Linguistics) 

[^Peters_et+al_2018_a]: Peters, M. E., M. Neumann, M. Iyyer, et al. 2018. “Deep Contextualized Word Representations.” In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), 2227–2237. New Orleans, Louisiana: Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Peters%2C%20M.E.%20Neumann%2C%20M.%20Iyyer%2C%20M.%20Deep%20Contextualized%20Word%20Representations%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Peters%2C%20M.E.%20Neumann%2C%20M.%20Iyyer%2C%20M.%20Deep%20Contextualized%20Word%20Representations%202018) 

[^Piao_2018_a]: Piao, G., and J. G. Breslin. 2018. “Financial Aspect and Sentiment Predictions With Deep Neural Networks: An Ensemble Approach.” In Companion Proceedings of the The Web Conference 2018, WWW&#39;18, 1973–1977. Republic and Canton of Geneva, CHE: International World Wide Web Conferences Steering Committee.  [OA](https://scholar.google.co.uk/scholar?q=Piao%2C%20G.%20Breslin%2C%20J.G.%20Financial%20Aspect%20and%20Sentiment%20Predictions%20With%20Deep%20Neural%20Networks%3A%20An%20Ensemble%20Approach%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Piao%2C%20G.%20Breslin%2C%20J.G.%20Financial%20Aspect%20and%20Sentiment%20Predictions%20With%20Deep%20Neural%20Networks%3A%20An%20Ensemble%20Approach%202018) 

[^Qiu_et+al_2020_a]: Qiu, X., T. Sun, Y. Xu, Y. Shao, N. Dai, and X. Huang. 2020. “Pre-­Trained Models for Natural Language Processing: A Survey.” Science China Technological Sciences 63, no. 10: 1872–1897.  [OA](https://engine.scholarcy.com/oa_version?query=Qiu%2C%20X.%20Sun%2C%20T.%20Xu%2C%20Y.%20Shao%2C%20Y.%20Pre-%C2%ADTrained%20Models%20for%20Natural%20Language%20Processing%3A%20A%20Survey%202020&author=Qiu&title=Pre-%C2%ADTrained%20Models%20for%20Natural%20Language%20Processing%3A%20A%20Survey&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Qiu%2C%20X.%20Sun%2C%20T.%20Xu%2C%20Y.%20Shao%2C%20Y.%20Pre-%C2%ADTrained%20Models%20for%20Natural%20Language%20Processing%3A%20A%20Survey%202020) [Scite](/scite_tallies?query=author%3AQiu%2Ctitle%3APre-%C2%ADTrained%20Models%20for%20Natural%20Language%20Processing%3A%20A%20Survey%2Cyear%3A2020)

[^Radford_et+al_2019_a]: Radford, A., J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever. 2019. “Language Models Are Unsupervised Multitask Learners.” OpenAI blog 1, no. 8: 9.  [OA](https://engine.scholarcy.com/oa_version?query=Radford%2C%20A.%20Wu%2C%20J.%20Child%2C%20R.%20Luan%2C%20D.%20Language%20Models%20Are%20Unsupervised%20Multitask%20Learners%202019&author=Radford&title=Language%20Models%20Are%20Unsupervised%20Multitask%20Learners&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Radford%2C%20A.%20Wu%2C%20J.%20Child%2C%20R.%20Luan%2C%20D.%20Language%20Models%20Are%20Unsupervised%20Multitask%20Learners%202019) [Scite](/scite_tallies?query=author%3ARadford%2Ctitle%3ALanguage%20Models%20Are%20Unsupervised%20Multitask%20Learners%2Cyear%3A2019)

[^Raffel_et+al_2020_a]: Raffel, C., N. Shazeer, A. Roberts, et al. 2020. “Exploring the Limits of Transfer Learning With a Unified Text-­to-­Text Transformer.” Journal of Machine Learning Research 21, no. 140: 1–67. http://jmlr.org/papers/v21/20-­074.html.  [OA](http://jmlr.org/papers/v21/20-­074.html)  [Scite](/scite_tallies?query=author%3ARaffel%2Ctitle%3AExploring%20the%20Limits%20of%20Transfer%20Learning%20With%20a%20Unified%20Text-%C2%ADto-%C2%ADText%20Transformer%2Cyear%3A2020)

[^Schmidhuber_2015_a]: Schmidhuber, J. 2015. “Deep Learning in Neural Networks: An Overview.” Neural Networks 61: 85–117.  [OA](https://engine.scholarcy.com/oa_version?query=Schmidhuber%2C%20J.%20Deep%20Learning%20in%20Neural%20Networks%3A%20An%20Overview%202015&author=Schmidhuber&title=Deep%20Learning%20in%20Neural%20Networks%3A%20An%20Overview&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Schmidhuber%2C%20J.%20Deep%20Learning%20in%20Neural%20Networks%3A%20An%20Overview%202015) [Scite](/scite_tallies?query=author%3ASchmidhuber%2Ctitle%3ADeep%20Learning%20in%20Neural%20Networks%3A%20An%20Overview%2Cyear%3A2015)

[^Sefer_2021_a]: Sefer, E. 2021. “Hi–C Interaction Graph Analysis Reveals the Impact of Histone Modifications in Chromatin Shape.” Applied Network Science 6, no. 1: 54.  [OA](https://engine.scholarcy.com/oa_version?query=Sefer%2C%20E.%20Hi%E2%80%93C%20Interaction%20Graph%20Analysis%20Reveals%20the%20Impact%20of%20Histone%20Modifications%20in%20Chromatin%20Shape%202021&author=Sefer&title=Hi%E2%80%93C%20Interaction%20Graph%20Analysis%20Reveals%20the%20Impact%20of%20Histone%20Modifications%20in%20Chromatin%20Shape&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Sefer%2C%20E.%20Hi%E2%80%93C%20Interaction%20Graph%20Analysis%20Reveals%20the%20Impact%20of%20Histone%20Modifications%20in%20Chromatin%20Shape%202021) [Scite](/scite_tallies?query=author%3ASefer%2Ctitle%3AHi%E2%80%93C%20Interaction%20Graph%20Analysis%20Reveals%20the%20Impact%20of%20Histone%20Modifications%20in%20Chromatin%20Shape%2Cyear%3A2021)

[^Sefer_2022_a]: Sefer, E. 2022a. “Biocode: A Data-­Driven Procedure to Learn the Growth of Biological Networks.” IEEE/ACM Transactions on Computational Biology and Bioinformatics 19, no. 6: 3103–3113.  [OA](https://engine.scholarcy.com/oa_version?query=Sefer%2C%20E.%20Biocode%3A%20A%20Data-%C2%ADDriven%20Procedure%20to%20Learn%20the%20Growth%20of%20Biological%20Networks%202022&author=Sefer&title=Biocode%3A%20A%20Data-%C2%ADDriven%20Procedure%20to%20Learn%20the%20Growth%20of%20Biological%20Networks&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Sefer%2C%20E.%20Biocode%3A%20A%20Data-%C2%ADDriven%20Procedure%20to%20Learn%20the%20Growth%20of%20Biological%20Networks%202022) [Scite](/scite_tallies?query=author%3ASefer%2Ctitle%3ABiocode%3A%20A%20Data-%C2%ADDriven%20Procedure%20to%20Learn%20the%20Growth%20of%20Biological%20Networks%2Cyear%3A2022)

[^Sefer_2022_b]: Sefer, E. 2022b. “Probc: Joint Modeling of Epigenome and Transcriptome Effects in 3D Genome.” BMC Genomics 23, no. 1: 287.  [OA](https://engine.scholarcy.com/oa_version?query=Sefer%2C%20E.%20Probc%3A%20Joint%20Modeling%20of%20Epigenome%20and%20Transcriptome%20Effects%20in%203D%20Genome%202022&author=Sefer&title=Probc%3A%20Joint%20Modeling%20of%20Epigenome%20and%20Transcriptome%20Effects%20in%203D%20Genome&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Sefer%2C%20E.%20Probc%3A%20Joint%20Modeling%20of%20Epigenome%20and%20Transcriptome%20Effects%20in%203D%20Genome%202022) [Scite](/scite_tallies?query=author%3ASefer%2Ctitle%3AProbc%3A%20Joint%20Modeling%20of%20Epigenome%20and%20Transcriptome%20Effects%20in%203D%20Genome%2Cyear%3A2022)

[^Sefer_2011_a]: Sefer, E., and C. Kingsford. 2011. “Metric Labeling and Semimetric Embedding for Protein Annotation Prediction.” In Research in Computational Molecular Biology, edited by V. Bafna and S. C. Sahinalp, 392–407. Springer Berlin Heidelberg.  [OA](https://scholar.google.co.uk/scholar?q=Sefer%2C%20E.%20Kingsford%2C%20C.%20Metric%20Labeling%20and%20Semimetric%20Embedding%20for%20Protein%20Annotation%20Prediction%202011) [GScholar](https://scholar.google.co.uk/scholar?q=Sefer%2C%20E.%20Kingsford%2C%20C.%20Metric%20Labeling%20and%20Semimetric%20Embedding%20for%20Protein%20Annotation%20Prediction%202011) 

[^Sefer_2021_b]: Sefer, E., and C. Kingsford. 2021. “Metric Labeling and Semimetric Embedding for Protein Annotation Prediction.” Journal of Computational Biology 28, no. 5: 514–525. https://doi.org/10.1089/cmb.2020.0425 33370163.  [OA](https://doi.org/10.1089/cmb.2020.0425)  [Scite](/scite_tallies?query=https://doi.org/10.1089/cmb.2020.0425)

[^Severyn_2015_a]: Severyn, A., and A. Moschitti. 2015. “Twitter Sentiment Analysis With Deep Convolutional Neural Networks.” In Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR &#39;15, 959–962. New York, NY, USA: Association for Computing Machinery. https://doi.org/10.1145/27664 62.2767830.  [OA](https://doi.org/10.1145/27664)  [Scite](/scite_tallies?query=https://doi.org/10.1145/27664)

[^Seyhan_2023_a]: Seyhan, B., and E. Sefer. 2023. “NFT Primary Sale Price and Secondary Sale Prediction via Deep Learning.” Proceedings of the Fourth ACM International Conference on AI in Finance: 116–123.  [OA](https://scholar.google.co.uk/scholar?q=Seyhan%2C%20B.%20Sefer%2C%20E.%20NFT%20Primary%20Sale%20Price%20and%20Secondary%20Sale%20Prediction%20via%20Deep%20Learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Seyhan%2C%20B.%20Sefer%2C%20E.%20NFT%20Primary%20Sale%20Price%20and%20Secondary%20Sale%20Prediction%20via%20Deep%20Learning%202023) 

[^Sohangir_et+al_2018_a]: Sohangir, S., D. Wang, A. Pomeranets, and T. M. Khoshgoftaar. 2018. “Big Data: Deep Learning for Financial Sentiment Analysis.” Journal of Big Data 5, no. 1: 1–25.  [OA](https://engine.scholarcy.com/oa_version?query=Sohangir%2C%20S.%20Wang%2C%20D.%20Pomeranets%2C%20A.%20Khoshgoftaar%2C%20T.M.%20Big%20Data%3A%20Deep%20Learning%20for%20Financial%20Sentiment%20Analysis%202018&author=Sohangir&title=Big%20Data%3A%20Deep%20Learning%20for%20Financial%20Sentiment%20Analysis&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Sohangir%2C%20S.%20Wang%2C%20D.%20Pomeranets%2C%20A.%20Khoshgoftaar%2C%20T.M.%20Big%20Data%3A%20Deep%20Learning%20for%20Financial%20Sentiment%20Analysis%202018) [Scite](/scite_tallies?query=author%3ASohangir%2Ctitle%3ABig%20Data%3A%20Deep%20Learning%20for%20Financial%20Sentiment%20Analysis%2Cyear%3A2018)

[^Soylu_2024_a]: Soylu, N. N., and E. Sefer. 2024. “Deepptm: Protein Post-­Translational Modification Prediction From Protein Sequences by Combining Deep Protein Language Model With Vision Transformers.” Current Bioinformatics 19, no. 9: 810–824.  [OA](https://engine.scholarcy.com/oa_version?query=Soylu%2C%20N.N.%20Sefer%2C%20E.%20Deepptm%3A%20Protein%20Post-%C2%ADTranslational%20Modification%20Prediction%20From%20Protein%20Sequences%20by%20Combining%20Deep%20Protein%20Language%20Model%20With%20Vision%20Transformers%202024&author=Soylu&title=Deepptm%3A%20Protein%20Post-%C2%ADTranslational%20Modification%20Prediction%20From%20Protein%20Sequences%20by%20Combining%20Deep%20Protein%20Language%20Model%20With%20Vision%20Transformers&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Soylu%2C%20N.N.%20Sefer%2C%20E.%20Deepptm%3A%20Protein%20Post-%C2%ADTranslational%20Modification%20Prediction%20From%20Protein%20Sequences%20by%20Combining%20Deep%20Protein%20Language%20Model%20With%20Vision%20Transformers%202024) [Scite](/scite_tallies?query=author%3ASoylu%2Ctitle%3ADeepptm%3A%20Protein%20Post-%C2%ADTranslational%20Modification%20Prediction%20From%20Protein%20Sequences%20by%20Combining%20Deep%20Protein%20Language%20Model%20With%20Vision%20Transformers%2Cyear%3A2024)

[^Su_et+al_2023_a]: Su, J., Y. Lu, S. Pan, A. Murtadha, B. Wen, and Y. Liu. 2023. “Roformer: Enhanced Transformer With Rotary Position Embedding.” arXiv: 2104.09864. https://arxiv.org/abs/2104.09864.  [OA](https://arxiv.org/abs/2104.09864)  

[^Sun_et+al_2019_a]: Sun, C., X. Qiu, Y. Xu, and X. Huang. 2019. “How to Fine-­Tune BERT for Text Classification?” In Chinese Computational Linguistics, edited by M. Sun, X. Huang, H. Ji, Z. Liu, and Y. Liu, 194–206. Springer International Publishing.  [OA](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20Fine-%C2%ADTune%20BERT%20for%20Text%20Classification%3F%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20Fine-%C2%ADTune%20BERT%20for%20Text%20Classification%3F%202019) 

[^Tetlock_et+al_2008_a]: Tetlock, P. C., M. Saar-­Tsechansky, and S. Macskassy. 2008. “More Than Words: Quantifying Language to Measure Firms&#39; Fundamentals.” Journal of Finance 63, no. 3: 1437–1467.  [OA](https://engine.scholarcy.com/oa_version?query=Tetlock%2C%20P.C.%20Saar-%C2%ADTsechansky%2C%20M.%20Macskassy%2C%20S.%20More%20Than%20Words%3A%20Quantifying%20Language%20to%20Measure%20Firms%27%20Fundamentals%202008&author=Tetlock&title=More%20Than%20Words%3A%20Quantifying%20Language%20to%20Measure%20Firms%27%20Fundamentals&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Tetlock%2C%20P.C.%20Saar-%C2%ADTsechansky%2C%20M.%20Macskassy%2C%20S.%20More%20Than%20Words%3A%20Quantifying%20Language%20to%20Measure%20Firms%27%20Fundamentals%202008) [Scite](/scite_tallies?query=author%3ATetlock%2Ctitle%3AMore%20Than%20Words%3A%20Quantifying%20Language%20to%20Measure%20Firms%27%20Fundamentals%2Cyear%3A2008)

[^Todt_et+al_2023_a]: Todt, P. B., R. Babaei, and P. Babaei 2023. FIN-­LLAMA: Efficient Finetuning of Quantized LLMS for Finance. https://github.com/Bavest/fin-llama.  [OA](https://github.com/Bavest/fin-llama)  

[^Touvron_et+al_2023_a]: Touvron, H., T. Lavril, G. Izacard, et al. 2023. “LLAMA: Open and Efficient Foundation Language Models.” arXiv: 2302.13971. https://arxiv.org/abs/2302.13971.  [OA](https://arxiv.org/abs/2302.13971)  

[^Tripathy_et+al_2016_a]: Tripathy, A., A. Agrawal, and S. K. Rath. 2016. “Classification of Sentiment Reviews Using N-­Gram Machine Learning Approach.” Expert Systems with Applications 57: 117–126.  [OA](https://engine.scholarcy.com/oa_version?query=Tripathy%2C%20A.%20Agrawal%2C%20A.%20K%2C%20S.%20Classification%20of%20Sentiment%20Reviews%20Using%20N-%C2%ADGram%20Machine%20Learning%20Approach%202016&author=Tripathy&title=Classification%20of%20Sentiment%20Reviews%20Using%20N-%C2%ADGram%20Machine%20Learning%20Approach&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Tripathy%2C%20A.%20Agrawal%2C%20A.%20K%2C%20S.%20Classification%20of%20Sentiment%20Reviews%20Using%20N-%C2%ADGram%20Machine%20Learning%20Approach%202016) [Scite](/scite_tallies?query=author%3ATripathy%2Ctitle%3AClassification%20of%20Sentiment%20Reviews%20Using%20N-%C2%ADGram%20Machine%20Learning%20Approach%2Cyear%3A2016)

[^Tuncer_et+al_2022_a]: Tuncer, T., U. Kaya, E. Sefer, O. Alacam, and T. Hoser. 2022. “Asset Price and Direction Prediction via Deep 2D Transformer and Convolutional Neural Networks.” Proceedings of the Third ACM International Conference on AI in Finance: 79–86.  [OA](https://scholar.google.co.uk/scholar?q=Tuncer%2C%20T.%20Kaya%2C%20U.%20Sefer%2C%20E.%20Alacam%2C%20O.%20Asset%20Price%20and%20Direction%20Prediction%20via%20Deep%202D%20Transformer%20and%20Convolutional%20Neural%20Networks%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Tuncer%2C%20T.%20Kaya%2C%20U.%20Sefer%2C%20E.%20Alacam%2C%20O.%20Asset%20Price%20and%20Direction%20Prediction%20via%20Deep%202D%20Transformer%20and%20Convolutional%20Neural%20Networks%202022) 

[^Vaswani_et+al_2017_a]: Vaswani, A., N. Shazeer, N. Parmar, et al. 2017. “Attention Is All You Need.” Advances in Neural Information Processing Systems, 5998–6008.  [OA](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Attention%20Is%20All%20You%20Need%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Attention%20Is%20All%20You%20Need%202017) 

[^Whitelaw_et+al_2005_a]: Whitelaw, C., N. Garg, and S. Argamon. 2005. “Using Appraisal Groups for Sentiment Analysis.” In Proceedings of the 14th ACM International Conference on Information and Knowledge Management, CIKM&#39;05, 625– 631. New York, NY, USA: Association for Computing Machinery.  [OA](https://scholar.google.co.uk/scholar?q=Whitelaw%2C%20C.%20Garg%2C%20N.%20Argamon%2C%20S.%20Using%20Appraisal%20Groups%20for%20Sentiment%20Analysis%202005) [GScholar](https://scholar.google.co.uk/scholar?q=Whitelaw%2C%20C.%20Garg%2C%20N.%20Argamon%2C%20S.%20Using%20Appraisal%20Groups%20for%20Sentiment%20Analysis%202005) 

[^Wolf_et+al_2019_a]: Wolf, T., L. Debut, V. Sanh, et al. 2019. “Huggingface&#39;s Transformers: State-­of-­the-­Art Natural Language Processing.” ArXiv abs/1910.03771.  [OA](https://arxiv.org/abs/1910.03771)  

[^Yang_et+al_2023_a]: Yang, H., X.-­Y. Liu, and C. D. Wang. 2023. “Fingpt: Open-­Source Financial Large Language Models.” arXiv: 2306.06031. https://arxiv.org/abs/2306.06031. Yang, P. K. Y., K. Z. Zhang, M. C. S. Uy, and A. Huang.2020.“Finbert: A Pretrained Language Model for Financial Communications.” ArXiv:abs/2006.08097.  [OA](https://arxiv.org/abs/2306.06031)  

[^Yang_et+al_2020_a]: Yang, Q., Y. Zhang, W. Dai, and S. J. Pan. 2020. Transfer Learning. Cambridge University Press.  [OA](https://engine.scholarcy.com/oa_version?query=Yang%2C%20Q.%20Zhang%2C%20Y.%20Dai%2C%20W.%20J%2C%20S.%20Transfer%20Learning%202020&author=Yang&title=Transfer%20Learning&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Q.%20Zhang%2C%20Y.%20Dai%2C%20W.%20J%2C%20S.%20Transfer%20Learning%202020) [Scite](/scite_tallies?query=author%3AYang%2Ctitle%3ATransfer%20Learning%2Cyear%3A2020)

[^Yang_et+al_2018_a]: Yang, S., J. Rosenfeld, and J. Makutonin. 2018. “Financial Aspect-­Based Sentiment Analysis Using Deep Representations.” arXiv: 1808.07931.  [OA](https://arxiv.org/abs/1808.07931)  

[^Yang_et+al_2019_a]: Yang, Z., Z. Dai, Y. Yang, J. Carbonell, R. R. Salakhutdinov, and Q. V. Le. 2019. “XLNET: Generalized Autoregressive Pretraining for Language Understanding.” In Advances in Neural Information Processing Systems, edited by H. Wallach, H. Larochelle, A. Beygelzimer, F. d&#39; Alché-­Buc, E. Fox, and R. Garnett, vol. 32, 5753–5763. Curran Associates, Inc. Zaib, M., Q. Z. Sheng, and W. E. Zhang. 2020. “A Short Survey of Pre-Trained Language Models for Conversational AI-­A New Age in NLP.” In Proceedings of the Australasian Computer Science Week Multiconference, 1–4.  [OA](https://engine.scholarcy.com/oa_version?query=Yang%2C%20Z.%20Dai%2C%20Z.%20Yang%2C%20Y.%20Carbonell%2C%20J.%20XLNET%3A%20Generalized%20Autoregressive%20Pretraining%20for%20Language%20Understanding%202019&author=Yang&title=XLNET%3A%20Generalized%20Autoregressive%20Pretraining%20for%20Language%20Understanding&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Z.%20Dai%2C%20Z.%20Yang%2C%20Y.%20Carbonell%2C%20J.%20XLNET%3A%20Generalized%20Autoregressive%20Pretraining%20for%20Language%20Understanding%202019) [Scite](/scite_tallies?query=author%3AYang%2Ctitle%3AXLNET%3A%20Generalized%20Autoregressive%20Pretraining%20for%20Language%20Understanding%2Cyear%3A2019)

[^Zhang_et+al_2019_a]: Zhang, B., and R. Sennrich. 2019. “Root Mean Square Layer Normalization.” arXiv: 1910.07467. https://arxiv.org/abs/1910.07467. Zhang, L., S. Wang, and B. Liu.2018.“Deep Learning for Sentiment Analysis: A Survey.” Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery 8, no.4:e1253.  [OA](https://arxiv.org/abs/1910.07467)  

