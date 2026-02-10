[[Araci_FinbertFinancialSentimentAnalysisWith_2019]]

# [FinBERT: Financial Sentiment Analysis with Pre-trained Language Models](https://arxiv.org/abs/1908.10063)

## [[Dogu Araci]]

## Abstract

Financial sentiment analysis is a challenging task due to the specialized language and lack of labeled data in that domain. General-purpose models are not effective enough due to the specialized language used in financial contexts. We hypothesize that pre-trained language models can help with this problem because they require fewer labeled examples, and they can be further trained on domain-specific corpora. We introduce FinBERT, a BERT-based language model, to tackle NLP tasks in the financial domain. Our results show improvements across all measured metrics relative to the current state of the art on two financial sentiment analysis datasets. We find that even with a smaller training set and fine-tuning only a part of the model, FinBERT outperforms state-of-the-art machine learning methods.

## Key concepts

# loughran; #claim/language_model; #language_model; #finding/BERT; #BERT; #natural_language_processing; #long_short_term_memory

## Quote

The paper presents FinBERT, a BERT implementation for the financial domain, and evaluates its performance on short-sentence classification and regression tasks, comparing it with other transfer learning methods such as ELMo and ULMFit.

## Key points

- Prices in an open market reflect all of the available information regarding assets exchanged in an economy ([^Malkiel_2003_a])
- We introduce FinBERT, which is a language model based on BERT for financial natural language processing (NLP) tasks
- This work is the first application of BERT for finance to the best of our knowledge, and one of the few that experimented with further pre-training on a domain-specific corpus
- ULMFit, further pre-trained on a financial corpus, beat the previous state-of-the-art for the classification task, only to a smaller degree than BERT. These results show the effectiveness of pre-trained language models for a downstream task such as sentiment analysis, especially with a small labeled dataset
- The complete dataset included more than 3000 examples, but FinBERT was able to surpass the previous state-of-the-art even with a training set as small as 500 examples
- On both of the datasets we used, we achieved state-of-the-art results by a significant margin
- FinBERT is good enough for extracting explicit sentiments, but modeling implicit information that is not necessarily apparent even to those who are writing the text should be a challenging task. Another possible extension can be using FinBERT for other natural language processing tasks, such as named entity recognition or question answering in the financial domain

## Summary

### Introduction

Financial sentiment analysis is challenging due to specialized language and a lack of labeled data in the financial domain.
General-purpose models are not effective enough because of the specialized language used in the financial context.
The goal of this thesis is to test the hypothesized advantages of using and fine-tuning pre-trained language models for the financial domain.

### Methodology

The thesis introduces FinBERT, a language model based on BERT, to tackle NLP tasks in the financial domain.
FinBERT is evaluated on two financial sentiment analysis datasets, and the results show improvements across all measured metrics compared to the current state of the art.
The thesis also implements two other pre-trained language models, ULMFit and ELMo, for financial sentiment analysis and compares these with FinBERT.
The paper implemented BERT for the financial domain by further pre-training it on a financial corpus and fine-tuning it for sentiment analysis, resulting in a model called FinBERT.
Other pre-training language models, such as ELMo and ULMFit, were also implemented for comparison.
The effects of further pre-training and several training strategies were investigated, including the impact of learning rate regimes and fine-tuning only the last 2 layers of BERT.

### Related Work

Previous research on sentiment analysis in finance has used machine learning methods with features extracted from text via "word counting," as well as deep learning methods, where text is represented as a sequence of embeddings.
The thesis also discusses text classification using pre-trained language models, including ELMo, ULMFit, and BERT, which have achieved state-of-the-art results in multiple NLP tasks.

### Models

The paper discusses several natural language processing models, including GLoVe, ELMo, ULMFit, and BERT.
GLoVe is a model for calculating word representations, while ELMo provides contextualized word representations.
ULMFit is a transfer learning model that uses language model pre-training, while BERT is a language model consisting of a set of Transformer encoders stacked on top of each other.

### BERT For Financial Domain

The paper implements BERT for the financial domain, including further pre-training on a financial corpus and fine-tuning for classification and regression tasks.
The authors use two approaches for further pre-training: pre-training on a large financial corpus and pre-training on sentences from the training classification dataset.

### Experimental Setup

The paper describes the experimental setup, including the research questions, datasets, and baseline methods.
The authors use three datasets: TRC2-financial, Financial PhraseBank, and FiQA Sentiment.
The baseline methods include LSTM classifiers with GLoVe and ELMo embeddings, as well as ULMFit.
The authors evaluate the models using accuracy, cross-entropy loss, and other metrics.

### Model Performance

The FinBERT model outperforms other methods, including LSTM, ULMFit, LPS, HSC, and FinSSLX, across accuracy, macro F1 average, and other metrics.
The model achieves the best results on both the whole dataset and a subset with 100% annotator agreement.
The use of language model pre-training and effective training strategies enables the model to overcome the small data problem.

### Training Strategies

The effectiveness of language model pre-training is demonstrated by the superior performance of ULMFit and FinBERT compared to LSTM classifiers.
The use of discriminative fine-tuning, gradual unfreezing, and slanted triangular learning rates helps to prevent catastrophic forgetting and improve the model's performance.
Fine-tuning only a subset of the layers can achieve a fair trade-off between performance and training time.

### Error Analysis

The model's failures are mostly due to its inability to distinguish between positive and neutral labels, consistent with inter-annotator agreement and common sense.
The model struggles to identify the polarity of statements about companies, especially when the statements are neutral or lack indicative words.
The confusion matrix shows that 73% of the failures occur between positive and neutral labels, while only 5% occur between negative and positive labels.

### Results

The results showed that FinBERT achieved state-of-the-art performance by a significant margin on both datasets, increasing the state of the art by 15% in classification accuracy.
ULMFit, further pre-trained on a financial corpus, also beat the previous state-of-the-art, but to a smaller degree than BERT.
The results demonstrated the effectiveness of pre-trained language models for sentiment analysis, even with a small labeled dataset.

### Future Work

The paper suggests potential extensions of the work, including using FinBERT directly with stock market return data to support financial decisions, and applying FinBERT to other natural language processing tasks such as named entity recognition or question answering in the financial domain.
Additionally, modeling implicit information that is not necessarily apparent in the text is identified as a challenging task that could be explored in future research.

## Study subjects

### 46143 documents with more than 29M words and nearly 400K sentences

- We filter for some financial keywords in order to make the corpus more relevant and within the limits of the computing power available. The resulting corpus, TRC2-financial, includes 46,143 documents with more than 29M words and nearly 400K sentences. 4.2.2

### 16 people with a background in finance and business

- Financial Phrasebank consists of 4845 english sentences selected randomly from financial news found on the LexisNexis database. These sentences were then annotated by 16 individuals with backgrounds in finance and business. The annotators were asked to give labels according to how they think the information in the sentence might affect the mentioned company's stock price

## Data analysis

- #method/lstm_model
- #method/

## Findings

- <mark class="claim"><mark class="fact">We achieve the state-of-the-art on FiQA sentiment scoring</mark> and Financial PhraseBank</mark>
- Once the training size becomes 250, ULMFit and FinBERT start to successfully differentiate between labels, with an accuracy as high as 80% for FinBERT
- <mark class="claim">Our model outperforms state-of-the-art models for both MSE and</mark> $R^{2}$
- <mark class="claim"><mark class="fact">The model achieves the best performance on the validation set after the first epoch</mark> and then starts to overfit</mark>
- With 97% accuracy on the subset of Financial PhraseBank with 100% annotator agreement, we think it might be an interesting exercise to examine cases where the model failed to predict the true label
- <mark class="fact">This work is the first application of BERT for finance</mark> to the best of our knowledge and one of the few <mark class="fact">that experimented with further pre-training on a domain-specific corpus</mark>. <mark class="claim">On both of the datasets we used, we achieved state-of-the-art results by a significant margin</mark>

## Builds on previous research

- They also introduced further pre-training of the language model on a domain-specific corpus, assuming target task data comes from a different distribution than the general corpus the initial model was trained on. ULMFit’s main idea of efficiently fine-tuning a pre-trained language model for downstream tasks was brought to another level with Bidirectional Encoder Representations from Transformers (BERT) ([^Devlin_et+al_2018_a]), which is also the main focus of this paper.

## Confirmation of earlier findings

- $R^{2}$. Boldface indicated the best result in the corresponding metric. [^Yang_et+al_2018_a]) ([^Yang_et+al_2018_a]) and [^Piao_2018_a]) ([^Piao_2018_a]) report results on the official test set.

## Counterpoint to earlier claims

- Since we don’t have access to that, we report the results on 10-fold cross-validation. There is no indication on ([^Maia_et+al_2018_b]) that the train and test sets they publish come from different distributions, and our model can be interpreted to be at a disadvantage since we need to set aside a subset of the training set as the test set, while state-of-the-art papers can use the complete training set.

## Contributions

- In this paper, we implemented BERT for the financial domain by further pre-training it on a financial corpus and fine-tuning it for sentiment analysis (FinBERT). <mark class="fact">This work is the first application of BERT for finance</mark> to the best of our knowledge and one of the few <mark class="fact">that experimented with further pre-training on a domain-specific corpus</mark>. <mark class="claim">On both of the datasets we used, we achieved state-of-the-art results by a significant margin</mark>. For the classification task, <mark class="fact">we increased the state-of-the art by 15% in accuracy</mark>.

## Limitations

- The study notes that one of the limitations of the study is the lack of large labeled financial datasets, which makes it difficult to utilize neural networks to their full potential for sentiment analysis.
- The study has several limitations, including the use of a limited number of baseline methods and the lack of thorough experimentation with these methods. The study also notes that the results should not be interpreted as definitive conclusions of one method being better.
- The limitations of the study include: the use of a limited dataset.
- The limitations of the study include the fact that further pre-training on a domain-specific corpus did not significantly improve the performance of BERT, and that modeling implicit information that is not necessarily apparent even to those who are writing the text is a challenging task.

## References

[^Devlin_et+al_2018_a]: Devlin et al. (2018) Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. (2018). <https://doi.org/arXiv:1811.03600v2> arXiv:1810.04805  [OA](https://doi.org/arXiv:1811.03600v2)  

[^Maia_et+al_2018_b]: Maia et al. (2018b) Macedo Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross Mcdermott, Manel Zarrouk, Alexandra Balahur, and Ross McDermott. 2018b. Companion of the The Web Conference 2018 on The Web Conference 2018, {WWW} 2018, Lyon, France, April 23-27, 2018. ACM. <https://doi.org/10.1145/3184558>  [OA](https://doi.org/10.1145/3184558)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3184558)

[^Malkiel_2003_a]: Malkiel (2003) Burton G Malkiel. 2003. The Efficient Market Hypothesis and Its Critics. Journal of Economic Perspectives 17, 1 (feb 2003), 59–82. <https://doi.org/10.1257/089533003321164958>  [OA](https://doi.org/10.1257/089533003321164958)  [Scite](/scite_tallies?query=https://doi.org/10.1257/089533003321164958)

[^Piao_2018_a]: Piao and Breslin (2018) Guangyuan Piao and John G Breslin. 2018. Financial Aspect and Sentiment Predictions with Deep Neural Networks. 1973–1977. <https://doi.org/10.1145/3184558.3191829>  [OA](https://doi.org/10.1145/3184558.3191829)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3184558.3191829)

[^Yang_et+al_2018_a]: Yang et al. (2018) Steve Yang, Jason Rosenfeld, and Jacques Makutonin. 2018. Financial Aspect-Based Sentiment Analysis using Deep Representations. (2018). arXiv:1808.07931 <https://arxiv.org/pdf/1808.07931v1.pdfhttp://arxiv.org/abs/1808.07931>  [OA](https://arxiv.org/pdf/1808.07931v1.pdfhttp://arxiv.org/abs/1808.07931)  
