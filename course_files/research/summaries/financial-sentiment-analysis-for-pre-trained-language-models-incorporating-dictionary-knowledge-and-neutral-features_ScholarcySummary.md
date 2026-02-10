[[Sun_et+al_FinancialSentimentAnalysistrainedLanguage_2025]]

# [Financial sentiment analysis for pre-trained language models incorporating dictionary knowledge and neutral features](https://doi.org/10.1016/j.nlp.2025.100148)

## [[Yongyong Sun]]; [[He Yuan]]; [[Fei Xu]]

## Abstract

As financial markets become increasingly complex, accurate sentiment analysis of financial texts has become crucial. Traditional methods often misinterpret financial terminology and show high error rates in neutral sentiment recognition. This study aims to improve the accuracy of financial sentiment analysis by developing EnhancedFinSentiBERT, a model that incorporates financial-domain pre-training, dictionary knowledge embedding, and neutral feature extraction. Experiments on the FinancialPhraseBank, FiQA, and Headline datasets demonstrate the model’s superior performance compared to mainstream methods, particularly in neutral sentiment recognition. Ablation analysis reveals that dictionary knowledge embedding and neutral feature extraction contribute most significantly to model improvement.

## Key concepts

# finding/BERT; #BERT; #claim/language_model; #language_model

## Quote
>
> The EnhancedFinSentiBERT model, which integrates financial domain pre-training, lexical knowledge embedding, and neutral feature extraction, demonstrates good generalization capability and outperforms baseline models in financial sentiment analysis, especially in neutral sentiment identification.

## Key points

- At the heart of financial markets lies the transmission and feedback of information
- This study proposes the EnhancedFinSentiBERT model to address challenges in financial text sentiment analysis through three key components: financial domain pre-training, dictionary knowledge integration, and neutral feature extraction
- The approach is based on the BERT model, which is used to improve the performance of the model on financial text analysis tasks through financial domain pretraining, financial lexicon knowledge incorporation, and neutral feature extraction techniques
- The EnhancedFinSentiBERT model integrates financial domain pretraining, lexical knowledge incorporation, and neutral feature extraction components in order to improve the accuracy of financial text sentiment analysis
- Compared to existing financial lexicon integration methods, this research’s implementation adopts several different approaches: First, it introduces a dynamic weight adjustment mechanism that adjusts influence weights based on word performance in different financial contexts, rather than using static weights; second, it adopts multidimensional sentiment representation, considering the positive and negative polarity of words and quantifying their intensity and degree of market impact; it implements a context-sensitive fusion strategy, enabling lexicon knowledge to dynamically interact with BERT’s contextual representations through a multi-head attention mechanism, thereby enhancing the model’s ability to capture subtle sentiment expressions in financial texts
- EnhancedFinSentiBERT’s F1 score on the consensus subset is 11 percentage points higher than on the complete dataset, increasing from 87.0% to 98.0%
- This paper considered three categories of baseline models: general pre-trained models BERT-base and XLNeT; general large language models GPT-4 and Llama 2; and finance domain-specific models FinBERT and BloombergGPT

## Summary

### Introduction To Financial Sentiment Analysis

Financial sentiment analysis is crucial for understanding market dynamics and investor decision-making.
Traditional methods often misinterpret financial terminology and struggle to recognize neutral sentiment.
The EnhancedFinSentiBERT model aims to improve the accuracy of financial sentiment analysis by incorporating financial-domain pre-training, dictionary knowledge embedding, and neutral feature extraction.

### Model Architecture And Components

The EnhancedFinSentiBERT model consists of three branches: financial pre-training, lexical feature enhancement, and neutral feature processing.
The model uses a three-branch fusion architecture that combines deep semantic representations, domain-specific feature representations, and neutral semantic information.
The financial pre-training branch employs NLTK for sentence disambiguation and a BERT feature extractor to obtain deep semantic representations.
The lexical feature enhancement branch refines word features via an initial embedding layer, an MLP feature-mapping layer, and a multi-head attention mechanism.
The neutral feature processing branch uses a feature extractor, a two-layer ReLU-activated fully connected network, and a multi-head attention mechanism to capture neutral semantic information.

### Key Contributions And Innovations

The study proposes several innovations, including pre-training the BERT model on a financial corpus, incorporating financial domain dictionary knowledge, and introducing a neutral feature extractor.
The model achieves significant performance improvements on benchmark datasets, demonstrating its effectiveness and applicability in financial text analysis.
The study addresses the limitations of existing methods, including the lack of domain-specific knowledge and the neglect of neutral expressions, and provides new ideas and tools for sentiment analysis in the financial sector.

### Model Architecture

The model employs a BERT-base architecture with 110M parameters, pre-trained on a large-scale unlabelled text corpus using masked language modelling and next-sentence prediction tasks.
The input representation combines token, positional, and segmental embeddings, with special [CLS] and [SEP] tokens for handling various NLP tasks.
A lexical embedding module is integrated in parallel with the pre-trained language model to incorporate domain knowledge from a financial lexicon.

### Financial Domain Adaptation

The model is adapted to the financial domain through pre-training on a self-constructed corpus of financial articles from news outlets and analyst reports from 2010 to September 2024.
The pre-training process involves masked language modelling and next-sentence prediction tasks, with adjustments to training parameters and strategies to accommodate the larger dataset.
The results show that the model adapts to financial text features, learning jargon and industry-specific expressions, and to contexts and expressions specific to the financial domain.

### Sentiment Analysis

The model uses a dynamic weight adjustment mechanism to adjust influence weights based on word performance across different financial contexts, and adopts a multidimensional sentiment representation that considers not only the positive and negative polarity of words but also their intensity and market impact.
A context-sensitive fusion strategy is implemented, enabling lexicon knowledge to dynamically interact with BERT's contextual representations through a multi-head attention mechanism.
The importance of each lexicon feature in the model is evaluated, with sentiment intensity scoring highest, followed by word frequency and its derivative indicators.

### Model Limitations

The model has limitations in distinguishing between neutral and non-neutral emotions, especially when dealing with subtle emotional expressions.
The model's main misjudgements are concentrated between neutral emotions and other emotion categories.
For example, positive statements are sometimes misjudged as neutral, while neutral statements are misjudged as positive.

### Neutral Feature Extractor

To address the model's limitations, a neutral feature extractor is designed to enhance the understanding of neutral expressions.
The extractor uses a lightweight neural network architecture comprising an input layer, two fully connected layers, a ReLU activation function, a multi-head attention layer, and an average pooling layer.
The extractor leverages BERT's contextual representations and employs multi-attention mechanisms to capture neutral features at multiple scales.

### Experimental Results

The EnhancedFinSentiBERT model performs optimally on the Financial PhraseBank, FiQA Task 1, and Headline datasets, achieving F1 scores of 87.0%, 88.0%, and 97.6%, respectively.
The model outperforms baseline models, including BERT-base, XLNet, GPT-4, Llama 2, FinBERT, and BloombergGPT.
The results indicate that the model maintains stable performance when processing both formal and informal financial texts, and that its architecture and task-specific optimization are more important than relying solely on large-scale pre-training.

### Model Performance

The EnhancedFinSentiBERT model achieved an F1 score of 94.2%, outperforming other models such as XLNeT, FinBERT, BERT-base, and GPT-4.
The model demonstrated good generalization capability across three datasets.
Ablation experiments showed that integrating dictionary knowledge with the neutral feature extractor significantly improved the model's performance, especially in identifying neutral sentiments.

### Ablation Experiments

The ablation experiments revealed that the neutral feature extractor contributed most significantly to the model's performance improvement, especially when processing financial texts with numerous neutral expressions.
Dictionary knowledge integration provided stable performance gains, particularly in understanding professional financial terminology.
Financial domain pre-training had limited effects on its own but produced significant synergistic improvements when combined with other components.

### Limitations And Future Directions

The model has limitations, including poor performance on cross-domain content and the potential for introducing noise when integrating financial dictionaries.
Future research directions could focus on expanding and optimizing the financial pre-training corpus, improving methods for incorporating lexical knowledge, and further optimizing the neutral feature extractor to better identify and process subtle sentiment expressions in complex financial contexts.

## Study subjects

### 2264 samples with expert consensus

- This dataset presents a natural imbalanced distribution, with neutral samples dominating, which reflects the characteristics of typical financial news. The evaluation used both the complete dataset and a high-consistency subset (2,264 samples with expert consensus). The FiQA Task 1 dataset includes 1,174 finance-related social media posts and news headlines, with continuous sentiment scores ranging from −1 to 1 ([^Maia_et+al_2018_a]). These texts have an average length of 18.3 words, longer and more colloquial than Financial PhraseBank, and have a balanced distribution of positive, neutral, and negative sentiment

### 148 positive samples

- As can be seen from the figure, the main misjudgements of the model are concentrated between neutral emotions and other emotion categories. Of the 148 positive samples, 27.7% were misclassified as neutral; of the 561 neutral samples, 7.3% were misclassified as positive; and of the 261 negative samples, 3.8% were misclassified as neutral. These three types of errors totalled 92 samples, representing 9.5% of the total sample size of 970, but 79.3% of the 116 total misclassifications

## Data analysis

- #method/bert_model
- #method/enhancedfinsentibert_model
- #method/masked_language_model

## Findings

- [^Choe_et+al_2023_a]) introduced FiLM, a financial pre-trained model using a diverse corpus, achieving superior performance on various financial tasks while reducing energy consumption by 82% ([^Choe_et+al_2023_a])
- By the end of training, around 140,000 steps, the loss reduces to approximately 1.3510, representing an overall reduction of over 50 percent
- <mark class="claim">On the complete dataset with 50% annotation agreement, the model achieved an F1 score of 87.0%, higher than all baseline models</mark>
- EnhancedFinSentiBERT’s F1 score on the consensus subset is 11 percentage points higher than on the complete dataset, increasing from 87.0% to 98.0%
- <mark class="claim">Headline dataset: In the financial news headline classification task, the proposed model also stands out with an F1 score of 97.6%, surpassing all other baseline models</mark>
- Confidence in the neutral classification increased from 44.27% to 59.24%, a 15-percentage-point improvement, demonstrating the effectiveness of this study’s approach

## Builds on previous research

- For the Financial PhraseBank (FPB) dataset, two versions were used: one with 50% expert annotation agreement and another with 100% complete expert consensus. For FiQA Task 1, following BloombergGPT ([^Wu_et+al_2023_a]), this paper converted continuous sentiment values into a classification task for evaluation ([^Wu_et+al_2023_a]).

## Confirmation of earlier findings

- This model adopts innovative pre-training methods and optimized architecture design, showing excellent performance on general understanding tasks ([^Wang_et+al_2023_a]). Including Llama 2 in the baseline models for this paper helps comprehensively compare the performance differences of various types of large language models on financial sentiment analysis tasks and explore the capabilities of open-source and proprietary models.

## Contributions

- This research introduces EnhancedFinSentiBERT, a financial sentiment analysis model that combines financial domain pre-training, lexical knowledge embedding, and neutral feature extraction. Validated through Financial PhraseBank, FiQA Task 1, and Headline datasets, our model outperforms baseline models such as BERT, XLNet, GPT-4, Llama, BloombergGPT, and FinBERT, especially in neutral sentiment identification. The integration of financial vocabulary knowledge enhances the model’s ability to capture subtle sentiments, while the neutral feature extractor improves accuracy in handling prevalent neutral expressions. Ablation experiments indicate that although financial domain pre-training alone has limited effects, its combination with other components produces significant synergistic improvements.

## Limitations

- The study notes that existing approaches to financial sentiment analysis face significant technical challenges, including the lack of domain-specific knowledge and the ineffective handling of neutral expressions. The study also notes that the model requires a large financial corpus to pre-train BERT with domain adaptation.
- The study notes that the model may still have limitations in capturing subtle market signals and nuances in financial texts. The study also acknowledges that the pre-training dataset may not be exhaustive.
- The study notes that even large models specifically trained for the financial domain may face challenges in sentiment analysis tasks, and that model architecture and task-specific optimization may be more important than relying solely on large-scale pre-training.
- The limitations of the study include the potential introduction of noise when integrating financial dictionaries, the poor performance of the model on cross-domain content, and the limited effects of financial domain pre-training alone. The study also highlights the need for future research to address these limitations.

## Future work

- The study suggests that future work could focus on improving the model's ability to handle complex financial texts, including those with subtle sentiment expressions. The study also suggests that future work could explore the application of the EnhancedFinSentiBERT model to other financial tasks, such as investment decision support and market sentiment analysis.
- The future work directions include expanding and optimizing the financial pre-training corpus, improving lexical knowledge incorporation methods, and further optimizing the neutral feature extractor. The study also suggests exploring more flexible vocabulary integration strategies to better handle cross-domain content and reduce potential noise impacts.

## References

[^Choe_et+al_2023_a]: Choe, J., Noh, K., Kim, N., Ahn, S., Jung, W., 2023. Exploring the impact of corpus diversity on financial pretrained language models. In: Bouamor, H., Pino, J., Bali, K. (Eds.), Findings of EMNLP 2023 2101–2112. Association for Computational Linguistics, Singapore.  [OA](https://scholar.google.co.uk/scholar?q=Choe%2C%20J.%20Noh%2C%20K.%20Kim%2C%20N.%20Ahn%2C%20S.%20Exploring%20the%20impact%20of%20corpus%20diversity%20on%20financial%20pretrained%20language%20models%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Choe%2C%20J.%20Noh%2C%20K.%20Kim%2C%20N.%20Ahn%2C%20S.%20Exploring%20the%20impact%20of%20corpus%20diversity%20on%20financial%20pretrained%20language%20models%202023)

[^Maia_et+al_2018_a]: Maia, M., Handschuh, S., Freitas, A., Davis, B., McDermott, R., Zarrouk, M., Balahur, A., 2018. WWW’18 open challenge: Financial opinion mining and question answering. In: The Web Conference 2018 1941–1942. ACM.  [OA](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20Davis%2C%20B.%20WWW%E2%80%9918%20open%20challenge%3A%20Financial%20opinion%20mining%20and%20question%20answering%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20Davis%2C%20B.%20WWW%E2%80%9918%20open%20challenge%3A%20Financial%20opinion%20mining%20and%20question%20answering%202018)

[^Wang_et+al_2023_a]: Wang, N., Yang, H., Wang, C.D., 2023. Fingpt: Instruction tuning benchmark for open-source large language models in financial datasets. ArXiv preprint arXiv: 2310.04793.  [OA](https://arxiv.org/abs/2310.04793)  

[^Wu_et+al_2023_a]: Wu, S., Irsoy, O., Lu, S., Dabravolski, V., Dredze, M., Gehrmann, S., Kambadur, P., Rosenberg, D., Mann, G., 2023. BloombergGPT: A large language model for finance. ArXiv preprint arXiv:2303.17564.  [OA](https://arxiv.org/abs/2303.17564)  
