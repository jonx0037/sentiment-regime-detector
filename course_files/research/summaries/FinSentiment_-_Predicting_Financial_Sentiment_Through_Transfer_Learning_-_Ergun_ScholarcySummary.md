[[Ergun_FinsentimentPredictingFinancialSentimentThrough_2025]]

# [FinSentiment: Predicting Financial Sentiment Through Transfer Learning](https://doi.org/10.1002/isaf.70015)

## [[Zehra Erva Ergun]]; [[Emre Sefer]]

## Abstract

ABSTRACT There is an increasing interest in financial text mining tasks. Significant progress has been made by using deep learning‐based models on a generic corpus, which also shows reasonable results on financial text mining tasks such as financial sentiment analysis. However, financial sentiment analysis remains demanding due to the scarcity of labeled data in the financial domain and the specialized language. General-purpose deep learning methods are not as effective, mainly because of the specialized language used in the financial context. In this study, we focus on improving the performance of financial text mining tasks by enhancing existing pretrained language models through NLP transfer learning. Pretrained language models require only a small number of labeled samples and can be further improved by training them on domain‐specific corpora. We propose an enhanced model, FinSentiment, that incorporates versions of several recently proposed pretrained models, such as BERT, XLNet, RoBERTa, GPT, Llama, and T5, and trains them on financial-domain corpora to better perform across NLP tasks in the financial domain. The corresponding finance‐specific models in FinSentiment are called Fin‐BERT, Fin‐XLNet, Fin‐RoBERTa, Fin‐GPT, Fin‐Llama, and Fin‐T5, respectively. We also propose variants of these models jointly trained over the financial domain and general corpora. Our finance‐specific FinSentiment models generally show the best performance across three financial sentiment analysis datasets, even when only a subset of these models is fine‐tuned on a smaller training set. Our results show improvements across all tested performance criteria relative to the existing results for these datasets. Extensive experimental results demonstrate the effectiveness and robustness of RoBERTa, especially when pretrained on financial corpora. Overall, we show that NLP transfer learning techniques are favorable solutions to financial sentiment analysis tasks. Our source code has been deposited at <https://github.com/seferlab/finsentiment>.

## Key concepts

# sentiment_analysis; #natural_language_processing; #claim/language_models; #language_models; #finding/xlnet; #xlnet; #finding/BERT; #BERT; #finding/RoBERTa; #RoBERTa

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

## Builds on previous research

- Furthermore, solutions to domain-­specificity have been introduced in different research areas, such as defining a specialized language for biomedical studies. [^Lee_et+al_2020_a]) have implemented BioBERT for biological text mining tasks, achieving outstanding performance across a range of tasks, including biomedical question answering, biomedical relation extraction, and biomedical named-­entity recognition. [^Asgari_2015_a]) have presented an unsupervised, data-­driven approach to represent and extract features from biological sequences, which are then used in a number of machine learning applications. However, they are not trained on a variety of financial tasks as we did.
- All general models without finance-specific training again outperform LSTM models with different embeddings, similar to the Financial PhraseBank dataset. We use the reported results from state-of-the-art papers (S. [^Yang_et+al_2018_a]; [^Piao_2018_a]), which use the official FiQA Task 1 test set.

## Differs from previous work

- In other attempts, [^Yang_et+al_2023_a] and [^Todt_et+al_2023_a] have been proposed. However, they are not trained on a variety of financial tasks as we did.

## Confirmation of earlier findings

- Lastly, Section 6 summarizes our findings and concludes the paper. Asset prices in an open economy mirror all the existing knowledge about these assets trading in a market ([^Malkiel_2003_a]; [^Gezici_2024_a]; [^Seyhan_2023_a]; [^Tuncer_et+al_2022_a]).

## Contributions

- In this research, we have come up with a FinSentiment model for financial tasks, which incorporates enhanced versions of a number of recently-­proposed neural LMs, such as BERT, XLNet, and RoBERTa. The corresponding finance-­specific models in FinSentiment are called Fin-­BERT, Fin-­XLNet, and Fin-RoBERTa, respectively. <mark class="fact">In general, FinSentiment models better perform across sentiment analysis tasks in the financial domain</mark> by training these models on financial domain corpora. To our best knowledge, this is the first study to investigate the performance of finetuning commonly used pretrained neural LMs in the financial domain and tasks. Additionally, it is one <mark class="fact">of the limited comprehensive studies that focus on additional pretraining over domain-­specific corpora</mark>. <mark class="claim"><mark class="fact">We have evaluated the performance of FinSentiment models over three different sentiment datasets</mark></mark>. <mark class="claim">On all of the used datasets, we have significantly outperformed the state-­of-­the-­art methods</mark>. For instance, for sentiment classification tasks, FinSentiment has outperformed the existing generally trained versions and baselines by more than 10% in terms of accuracy and F1 scores.

## Limitations

- The study has limitations, including the use of a small number of datasets and the potential for overfitting. The study also notes that FinSentiment model performance may vary across datasets and tasks.

## Future work

- The study suggests future work, including improving the finance-specific models for classification purposes and regression purposes. The study also suggests exploring the use of FinSentiment models for other NLP tasks in the financial domain.
- The future work suggested by the study includes improving the proposed finance-specific models and mechanisms for classification purposes in terms of aspect levels and regression purposes. The study also suggests using the trained finance-specific models with stock market price datasets to predict stock return volatility.

## References

[^Asgari_2015_a]: Asgari, E., and M. R. Mofrad. 2015. “Continuous Distributed Representation of Bi-­Ological Sequences for Deep Proteomics and Genomics.” PLoS ONE 10, no. 11: e0141287.  [OA](https://engine.scholarcy.com/oa_version?query=Asgari%2C%20E.%20R%2C%20M.%20Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%202015&author=Asgari&title=Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Asgari%2C%20E.%20R%2C%20M.%20Continuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%202015) [Scite](/scite_tallies?query=author%3AAsgari%2Ctitle%3AContinuous%20Distributed%20Representation%20of%20Bi-%C2%ADOlogical%20Sequences%20for%20Deep%20Proteomics%20and%20Genomics%2Cyear%3A2015)

[^Gezici_2024_a]: Gezici, A. H. B., and E. Sefer. 2024. “Deep Transformer-­Based Asset Price and Direction Prediction.” IEEE Access 12: 24164–24178. <https://doi.org/10.1109/ACCESS.2024.3358452>.  [OA](https://doi.org/10.1109/ACCESS.2024.3358452)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2024.3358452)

[^Lee_et+al_2020_a]: Lee, J., W. Yoon, S. Kim, et al. 2020. “Biobert: A Pre-­Trained Biomedical Language Representation Model for Biomedical Text Mining.” Bioinformatics 36, no. 4: 1234–1240.  [OA](https://engine.scholarcy.com/oa_version?query=Lee%2C%20J.%20Yoon%2C%20W.%20Kim%2C%20S.%20Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%202020&author=Lee&title=Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Lee%2C%20J.%20Yoon%2C%20W.%20Kim%2C%20S.%20Biobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%202020) [Scite](/scite_tallies?query=author%3ALee%2Ctitle%3ABiobert%3A%20A%20Pre-%C2%ADTrained%20Biomedical%20Language%20Representation%20Model%20for%20Biomedical%20Text%20Mining%2Cyear%3A2020)

[^Malkiel_2003_a]: Malkiel, B. G. 2003. “The Efficient Market Hypothesis and Its Critics.” Journal of Economic Perspectives 17, no. 1: 59–82.  [OA](https://engine.scholarcy.com/oa_version?query=Malkiel%2C%20B.G.%20The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%202003&author=Malkiel&title=The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Malkiel%2C%20B.G.%20The%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%202003) [Scite](/scite_tallies?query=author%3AMalkiel%2Ctitle%3AThe%20Efficient%20Market%20Hypothesis%20and%20Its%20Critics%2Cyear%3A2003)

[^Piao_2018_a]: Piao, G., and J. G. Breslin. 2018. “Financial Aspect and Sentiment Predictions With Deep Neural Networks: An Ensemble Approach.” In Companion Proceedings of the The Web Conference 2018, WWW&#39;18, 1973–1977. Republic and Canton of Geneva, CHE: International World Wide Web Conferences Steering Committee.  [OA](https://scholar.google.co.uk/scholar?q=Piao%2C%20G.%20Breslin%2C%20J.G.%20Financial%20Aspect%20and%20Sentiment%20Predictions%20With%20Deep%20Neural%20Networks%3A%20An%20Ensemble%20Approach%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Piao%2C%20G.%20Breslin%2C%20J.G.%20Financial%20Aspect%20and%20Sentiment%20Predictions%20With%20Deep%20Neural%20Networks%3A%20An%20Ensemble%20Approach%202018)

[^Seyhan_2023_a]: Seyhan, B., and E. Sefer. 2023. “NFT Primary Sale Price and Secondary Sale Prediction via Deep Learning.” Proceedings of the Fourth ACM International Conference on AI in Finance: 116–123.  [OA](https://scholar.google.co.uk/scholar?q=Seyhan%2C%20B.%20Sefer%2C%20E.%20NFT%20Primary%20Sale%20Price%20and%20Secondary%20Sale%20Prediction%20via%20Deep%20Learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Seyhan%2C%20B.%20Sefer%2C%20E.%20NFT%20Primary%20Sale%20Price%20and%20Secondary%20Sale%20Prediction%20via%20Deep%20Learning%202023)

[^Todt_et+al_2023_a]: Todt, P. B., R. Babaei, and P. Babaei 2023. FIN-­LLAMA: Efficient Finetuning of Quantized LLMS for Finance. <https://github.com/Bavest/fin-llama>.  [OA](https://github.com/Bavest/fin-llama)  

[^Tuncer_et+al_2022_a]: Tuncer, T., U. Kaya, E. Sefer, O. Alacam, and T. Hoser. 2022. “Asset Price and Direction Prediction via Deep 2D Transformer and Convolutional Neural Networks.” Proceedings of the Third ACM International Conference on AI in Finance: 79–86.  [OA](https://scholar.google.co.uk/scholar?q=Tuncer%2C%20T.%20Kaya%2C%20U.%20Sefer%2C%20E.%20Alacam%2C%20O.%20Asset%20Price%20and%20Direction%20Prediction%20via%20Deep%202D%20Transformer%20and%20Convolutional%20Neural%20Networks%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Tuncer%2C%20T.%20Kaya%2C%20U.%20Sefer%2C%20E.%20Alacam%2C%20O.%20Asset%20Price%20and%20Direction%20Prediction%20via%20Deep%202D%20Transformer%20and%20Convolutional%20Neural%20Networks%202022)

[^Yang_et+al_2023_a]: Yang, H., X.-­Y. Liu, and C. D. Wang. 2023. “Fingpt: Open-­Source Financial Large Language Models.” arXiv: 2306.06031. <https://arxiv.org/abs/2306.06031>. Yang, P. K. Y., K. Z. Zhang, M. C. S. Uy, and A. Huang.2020.“Finbert: A Pretrained Language Model for Financial Communications.” ArXiv:abs/2006.08097.  [OA](https://arxiv.org/abs/2306.06031)  

[^Yang_et+al_2018_a]: Yang, S., J. Rosenfeld, and J. Makutonin. 2018. “Financial Aspect-­Based Sentiment Analysis Using Deep Representations.” arXiv: 1808.07931.  [OA](https://arxiv.org/abs/1808.07931)  
