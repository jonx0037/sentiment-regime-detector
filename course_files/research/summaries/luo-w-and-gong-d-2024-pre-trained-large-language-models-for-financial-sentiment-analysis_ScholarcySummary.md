[[Luo_trainedLargeLanguageModelsFinancial_2024]]

# [Pre-trained Large Language Models for Financial Sentiment Analysis](https://arxiv.org/abs/2401.05215v1)

## [[Wei Luo]]; [[Dihong Gong]]

## Abstract

Financial sentiment analysis involves classifying financial text content into sentiment categories (e.g., positive, negative, and neutral). In this paper, we focus on the classification of financial news titles, a challenging task due to a lack of sufficient training samples. To overcome this difficulty, we propose adapting pretrained large language models (LLMs) [1, 2, 3] to address it. The LLMs, which are trained on large amounts of text corpora, have an advantage in text understanding and can be effectively adapted to domain-specific tasks with very few training samples. In particular, we adapt the open-source Llama2-7B model (2023) with the supervised fine-tuning (SFT) technique [4]. Experimental evaluation shows that even with the 7B model (which is relatively small for LLMs), our approach significantly outperforms the previous state-of-the-art algorithms.

## Key concepts

# fine_tuning; #finding/financial_news; #financial_news; #claim/large_language_models; #large_language_models; #text_corpora

## Quote
>
> This paper proposes the use of a pre-trained large language model, LLaMA2-7B, with supervised fine-tuning (SFT) to achieve state-of-the-art results in financial sentiment analysis, outperforming previous methods with limited training samples.

## Key points

- Financial sentiment analysis refers to classifying financial text contents into sentiment categories
- We investigate with different methods of using few-shot, further pretraining, and supervised fine-tuning (SFT) based on the Llama2-7B model
- The base method leverages the capability of pretrained large language models (LLMs), while the SFT method further improves this capability by fine-tuning the model using task-specific training data, and the ClassHead method models the problem as a classification problem by adding a classification head at the output layer
- We can see that the SFT version improves from the base version by a clear margin, which confirms that our SFT method is effective in improving the classification accuracy of the financial news titles
- We explored the potential of using LLMs for financial sentiment analysis
- Our SFT algorithm significantly improves over the baseline method and achieves a new state-of-the-art performance

## Summary

### Introduction

The paper discusses financial sentiment analysis, which involves classifying financial text into sentiment categories.
The authors propose using a pretrained large language model (LLM) to solve this problem, specifically the LLaMA2-7B model with supervised fine-tuning (SFT).
The LLMs have an advantage in text understanding and can be effectively adapted to domain-specific tasks with few training samples.

### Methodology

The authors investigate different methods for few-shot learning, further pretraining, and SFT based on the LLaMA2-7B model.
They achieve state-of-the-art results on the PhraseBank financial sentiment analysis benchmark.
The paper also discusses the use of the GPT model, which differs from BERT in its pre-training methodology and architectural design, and may offer a distinctive perspective and advantages in financial sentiment analysis.

### Results

The authors demonstrate LLMs' capability to solve the financial sentiment analysis problem, and their approach significantly outperforms previous state-of-the-art algorithms.
The study is based on the Financial PhraseBank dataset, and the authors provide data and code for their approach on GitHub.
The paper also discusses related work, including the use of BERT and FinBERT for financial sentiment analysis, and highlights the potential of LLMs for this task.
The results show that the SFT method improves classification accuracy, and the ClassHead method performs equally well as the SFT method but provides classification confidence scores.
The proposed method achieves a new state-of-the-art performance, achieving an accuracy of 0.9, outperforming the current state-of-the-art of 0.86.

### Model

The model used is LLaMA-7B version 2 without SFT, trained for 5 epochs with a learning rate starting at $3e^{-5}$ and decreasing to $3e^{-6}$ using a cosine annealing schedule.
The micro-batch size is set to $4$ with a max sequence length of $1024$.
The model is trained with a data-parallel paradigm with a world size of $4$, and each GPU has 80 GB of RAM.

### Dataset

The dataset used is the Financial PhraseBank, which contains 4845 English sentences randomly extracted from financial news.
The data is split into training, validation, and test sets, with $20\%$ held out for testing.
The performance of algorithms is measured with classification accuracy.

## Study subjects

### 1200 workers

- You are asked to choose the most suitable sentiment from ("positive", "negative", "neutral") with single-choice questions. Please follow these examples to answer the question. News Title: Most of the permanent layoffs will be in the plywood and sawn timber sectors of the Finnish company’s operations at several domestic mills, where earlier this year it temporarily laid off some 1,200 workers to save costs. Choices: A) positive

### 1200 workers

- Please follow these examples to answer the question. News Title: Most of the permanent layoffs will be in the plywood and sawn timber sectors of the Finnish company’s operations at several domestic mills, where earlier this year it temporarily laid off some 1,200 workers to save costs. Choices: A) positive

## Data analysis

- #method/classhead_method

## Findings

- <mark class="claim">Experimental evaluation shows that even with the 7B model (which is relatively small for LLMs), our approach significantly outperforms the previous state-of-the-art algorithms</mark>
- <mark class="claim"><mark class="fact">We achieve the state-of-the-art on PhraseBank financial sentiment analysis benchmark</mark></mark>
- <mark class="fact">The base method leverages the capability of pretrained LLMs</mark>, <mark class="fact">while the SFT method further improves this capability by fune-tuning the model use task-specific training data</mark>, and finally <mark class="fact">the ClassHead method models the problem as classification problem by adding a classification head</mark> at the output layer. The results of these three methods are show in Table 1. <mark class="claim">According to these results, <mark class="fact">we can see that the SFT version improves from the base version</mark> by a clear margin, <mark class="fact">which confirms that our SFT method is effective in improving the classification accuracy</mark> of the financial news titles</mark>
- <mark class="claim"><mark class="fact">The results show that our method has improved the current state-of-the-art accuracy</mark> from 0.86 to 0.9, which is a big improvement</mark>
- <mark class="claim"><mark class="fact">Our SFT algorithm significantly improves over the baseline method</mark> and achieve a new state-of-the-art performance</mark>

## Differs from previous work

- Based on the papers of Yang et al (2023) and Kheiri et al (2023), the GPT model differs significantly from BERT in its pre-training methodology and architectural design, primarily emphasizing its generative modeling capabilities. In contrast to BERT’ s bidirectional encoding, the GPT model adopts a unidirectional architecture, focusing more on context generation and coherence [^16], [^17].

## Contributions

- In this paper, <mark class="claim"><mark class="fact"><mark class="fact">we explored the potential of using LLMs for financial sentiment analysis</mark></mark></mark>. We conducted a systematic empirical analysis and provided novel insights on how to efficiently leverage LLMs to improve classification accuracy. Specifically, the few-shot-only method can achieve relatively decent accuracy, <mark class="fact">while further pretraining doesn’t provide a noticeable improvement over its baseline</mark>. Finally, <mark class="claim"><mark class="fact"><mark class="fact">our SFT algorithm significantly improves over the baseline method</mark></mark> and achieve a new state-of-the-art performance</mark>. Future work includes using LLMs with more parameters (e.g., LLaMA2-70B).

## Limitations

- The limitations of this study include the use of a relatively small model (7B parameters) and the reliance on a specific dataset (Financial PhraseBank).
- The study does not explicitly mention limitations, but it notes that further pretraining does not provide a noticeable improvement over the baseline.

## Future work

- The future work includes exploring the use of larger models, investigating the use of other pre-trained models, and evaluating the model's performance on other datasets.
- The study suggests using LLMs with a larger number of parameters, such as LLaMA2-70B, for future work.

## References

[^16]: Binxia Yang, Xudong Luo, Kaili Sun, and Michael Y. Luo. Recent progress on text summarisation based on BERT and GPT. In Zhi Jin, Yuncheng Jiang, Robert Andrei Buchmann, Yaxin Bi, Ana-Maria Ghiran, and Wenjun Ma, editors, Knowledge Science, Engineering and Management, pages 225–241, Cham, 2023. Springer Nature Switzerland.  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20Binxia%20Luo%2C%20Xudong%20Sun%2C%20Kaili%20Luo%2C%20Michael%20Y.%20Recent%20progress%20on%20text%20summarisation%20based%20on%20bert%20and%20gpt%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Binxia%20Luo%2C%20Xudong%20Sun%2C%20Kaili%20Luo%2C%20Michael%20Y.%20Recent%20progress%20on%20text%20summarisation%20based%20on%20bert%20and%20gpt%202023)

[^17]: Kiana Kheiri and Hamid Karimi. SentimentGPT: Exploiting GPT for advanced sentiment analysis and its departure from current machine learning, 2023.  [OA](https://scholar.google.co.uk/scholar?q=Kheiri%2C%20Kiana%20Karimi%2C%20Hamid%20Sentimentgpt%3A%20Exploiting%20gpt%20for%20advanced%20sentiment%20analysis%20and%20its%20departure%20from%20current%20machine%20learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Kheiri%2C%20Kiana%20Karimi%2C%20Hamid%20Sentimentgpt%3A%20Exploiting%20gpt%20for%20advanced%20sentiment%20analysis%20and%20its%20departure%20from%20current%20machine%20learning%202023)
