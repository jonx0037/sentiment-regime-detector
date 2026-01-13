[[Sun_et+al_FinancialSentimentAnalysistrainedLanguage_2025]]

# [Financial sentiment analysis for pre-trained language models incorporating dictionary knowledge and neutral features](https://doi.org/10.1016/j.nlp.2025.100148)

## [[Yongyong Sun]]; [[He Yuan]]; [[Fei Xu]]

## Abstract
With increasing financial market complexity, accurate sentiment analysis of financial texts has become crucial. Traditional methods often misinterpret financial terminology and show high error rates in neutral sentiment recognition. ==This study aims to improve financial sentiment analysis accuracy through developing EnhancedFinSentiBERT, a model incorporating financial domain pre-training, dictionary knowledge embedding, and neutral feature extraction==. Experiments on the FinancialPhraseBank, FiQA and Headline datasets demonstrate the model’s superior performance compared to mainstream methods, particularly in neutral sentiment recognition. Ablation analysis reveals that dictionary knowledge embedding and neutral feature extraction contribute most significantly to model improvement.

## Key concepts
#finding/BERT; #BERT; #claim/language_model; #language_model

## Quote
> The EnhancedFinSentiBERT model, which integrates financial domain pre-training, lexical knowledge embedding, and neutral feature extraction, demonstrates good generalization capability and outperforms baseline models in financial sentiment analysis, especially in neutral sentiment identification.

## Key points
- At the heart of financial markets lies the transmission and feedback of information
- This study proposes the EnhancedFinSentiBERT model to address challenges in financial text sentiment analysis through three key components: financial domain pre-training, dictionary knowledge integration, and neutral feature extraction
- The approach is based on the BERT model, which is used to improve the performance of the model on financial text analysis tasks through financial domain pretraining, financial lexicon knowledge incorporation, and neutral feature extraction techniques
- The EnhancedFinSentiBERT model integrates financial domain pretraining, lexical knowledge incorporation and neutral feature extraction components in order to improve the accuracy of financial text sentiment analysis
- Compared to existing financial lexicon integration methods, this research’s implementation adopts several different approaches: First, it introduces a dynamic weight adjustment mechanism that adjusts influence weights based on word performance in different financial contexts, rather than using static weights; second, it adopts multidimensional sentiment representation, considering the positive and negative polarity of words and quantifying their intensity and degree of market impact; it implements a context-sensitive fusion strategy, enabling lexicon knowledge to dynamically interact with BERT’s contextual representations through a multi-head attention mechanism, thereby enhancing the model’s ability to capture subtle sentiment expressions in financial texts
- EnhancedFinSentiBERT’s F1 score on the consensus subset is 11 percentage points higher than on the complete dataset, increasing from 87.0% to 98.0%
- This paper considered three categories of baseline models: general pre-trained models BERT-base and XLNeT; general large language models GPT-4 and Llama 2; and finance domainspecific models FinBERT and BloombergGPT


## Summary

### Introduction To Financial Sentiment Analysis
Financial sentiment analysis is crucial for understanding market dynamics and investor decision-making.
Traditional methods often misinterpret financial terminology and struggle with neutral sentiment recognition.
The EnhancedFinSentiBERT model aims to improve financial sentiment analysis accuracy by incorporating financial domain pre-training, dictionary knowledge embedding, and neutral feature extraction.

### Model Architecture And Components
The EnhancedFinSentiBERT model consists of three branches: financial pre-training, lexical feature enhancement, and neutral feature processing.
The model uses a three-branch fusion architecture, combining deep semantic representations, domain feature representations, and neutral semantic information.
The financial pre-training branch employs NLTK for sentence disambiguation and a BERT feature extractor to obtain deep semantic representations.
The lexical feature enhancement branch refines word features through an initial embedding layer, an MLP feature mapping layer, and a multi-head attention mechanism.
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
The model is adapted to the financial domain through pre-training on a self-constructed financial domain corpus, which includes articles from financial news outlets and analyst reports from 2010 to September 2024.
The pre-training process involves masked language modelling and next-sentence prediction tasks, with adjustments to training parameters and strategies to accommodate the larger dataset.
The results show that the model adapts to financial text features, learning jargon and industry-specific expressions, as well as adapting to contexts and expressions specific to the financial domain.

### Sentiment Analysis
The model uses a dynamic weight adjustment mechanism to adjust influence weights based on word performance in different financial contexts, and adopts a multidimensional sentiment representation, considering not only the positive and negative polarity of words but also quantifying their intensity and degree of market impact.
A context-sensitive fusion strategy is implemented, enabling lexicon knowledge to dynamically interact with BERT's contextual representations through a multi-head attention mechanism.
The importance of each lexicon feature in the model is evaluated, with sentiment intensity scoring highest, followed by word frequency and its derivative indicators.

### Model Limitations
The model has limitations in distinguishing between neutral and non-neutral emotions, especially when dealing with subtle emotional expressions.
The main misjudgements of the model are concentrated between neutral emotions and other emotion categories.
For example, positive statements are sometimes misjudged as neutral, while neutral statements are misjudged as positive.

### Neutral Feature Extractor
To address the model's limitations, a neutral feature extractor is designed to enhance the understanding of neutral expressions.
The extractor adopts a lightweight neural network structure, consisting of an input layer, two fully-connected layers, ReLU activation function, multi-head attention layer, and average pooling layer.
The extractor harnesses BERT's contextual representations and utilizes multi-attention mechanisms to capture neutral features at various scales.

### Experimental Results
The EnhancedFinSentiBERT model performs optimally on the Financial PhraseBank, FiQA Task 1, and Headline datasets, achieving F1 scores of 87.0%, 88.0%, and 97.6%, respectively.
The model outperforms baseline models, including BERT-base, XLNet, GPT-4, Llama 2, FinBERT, and BloombergGPT.
The results indicate that the model maintains stable performance when processing both formal and informal financial texts, and that its architecture and task-specific optimization are more important than relying solely on large-scale pre-training.

### Model Performance
The EnhancedFinSentiBERT model achieved an F1 score of 94.2%, outperforming other models such as XLNeT, FinBERT, BERT-base, and GPT-4.
The model demonstrated good generalization capability across three datasets.
Ablation experiments showed that the integration of dictionary knowledge and the neutral feature extractor significantly improved the model's performance, especially in identifying neutral sentiments.

### Ablation Experiments
The ablation experiments revealed that the neutral feature extractor contributed most significantly to the model's performance improvement, especially when processing financial texts with numerous neutral expressions.
Dictionary knowledge integration provided stable performance gains, particularly in understanding professional financial terminology.
Financial domain pre-training had limited effects on its own but produced significant synergistic improvements when combined with other components.

### Limitations And Future Directions
The model has limitations, including poor performance on cross-domain content and potential noise introduction when integrating financial dictionaries.
Future research directions could focus on expanding and optimizing the financial pre-training corpus, improving lexical knowledge incorporation methods, and further optimizing the neutral feature extractor to improve its ability to identify and process subtle sentiment expressions in complex financial contexts.


## Study subjects

### 2264 samples with expert consensus
- This dataset presents a natural imbalanced distribution, with neutral samples dominating, which reflects the characteristics of typical financial news. ==The evaluation used both the complete dataset and a high-consistency subset (2,264 samples with expert consensus).The FiQA Task 1 dataset includes 1,174 finance-related social media posts and news headlines, with continuous sentiment scores ranging from −1 to 1 ([^Maia_et+al_2018_a])==. These texts have an average length of 18.3 words, longer and more colloquial than Financial PhraseBank, and have a balanced distribution of positive, neutral, and negative sentiment

### 148 positive samples
- As can be seen from the figure, the main misjudgements of the model are concentrated between neutral emotions and other emotion categories. ==Of the 148 positive samples, 27.7% were misclassified as neutral; of the 561 neutral samples, 7.3% were misclassified as positive; and of the 261 negative samples, 3.8% were misclassified as neutral==. These three types of errors totalled 92 samples, representing 9.5% of the total sample size of 970, but 79.3% of the 116 total misclassifications

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

##  Builds on previous research
- For the Financial PhraseBank (FPB) dataset, two versions were used: one with 50% expert annotation agreement and another with 100% complete expert consensus. ==For FiQA Task 1, following BloombergGPT ([^Wu_et+al_2023_a]), this paper converted continuous sentiment values into a classification task for evaluation== ([^Wu_et+al_2023_a]).

##  Confirmation of earlier findings
- This model adopts innovative pre-training methods and optimized architecture design, showing excellent performance on general understanding tasks ([^Wang_et+al_2023_a]). Including Llama 2 in the baseline models for ==this paper helps to comprehensively compare performance differences of various types of large language models on financial sentiment analysis tasks, and to explore the capability comparison between open-source models and proprietary models==.

## Contributions
- This research introduces EnhancedFinSentiBERT, a financial sentiment analysis model that combines financial domain pre-training, lexical knowledge embedding, and neutral feature extraction. Validated through Financial PhraseBank, FiQA Task 1, and Headline datasets, our model outperforms baseline models such as BERT, XLNet, GPT-4, Llama, BloombergGPT, and FinBERT, especially in neutral sentiment identification. The integration of financial vocabulary knowledge enhances the model’s ability to capture subtle sentiments, while the neutral feature extractor improves accuracy in handling prevalent neutral expressions. Ablation experiments indicate that although financial domain pre-training alone has limited effects, its combination with other components produces significant synergistic improvements.

## Limitations
- The study notes that existing approaches to financial sentiment analysis face significant technical challenges, including the lack of domain-specific knowledge and the ineffective handling of neutral expressions. The study also notes that the model requires a large financial corpus to pre-train BERT with domain adaptation.
- The study notes that the model may still have limitations in capturing subtle market signals and nuances in financial texts. The study also acknowledges that the dataset used for pre-training may not be exhaustive.
- The study notes that even large models specifically trained for the financial domain may face challenges in sentiment analysis tasks, and that model architecture and task-specific optimization may be more important than relying solely on large-scale pre-training.
- The limitations of the study include the potential introduction of noise when integrating financial dictionaries, the poor performance of the model on cross-domain content, and the limited effects of financial domain pre-training alone. The study also highlights the need for future research to address these limitations.

## Future work
- The study suggests that future work could focus on improving the model's ability to handle complex financial texts, including those with subtle sentiment expressions. The study also suggests that future work could explore the application of the EnhancedFinSentiBERT model to other financial tasks, such as investment decision support and market sentiment analysis.
- The future work directions include expanding and optimizing the financial pre-training corpus, improving lexical knowledge incorporation methods, and further optimizing the neutral feature extractor. The study also suggests exploring more flexible vocabulary integration strategies to better handle cross-domain content and reduce potential noise impacts.


## References
[^Agarwal_2023_a]: Agarwal, B., 2023. Financial sentiment analysis model utilizing knowledge-base and domain-specific representation. Multimedia Tools Appl. 82 (6), 8899–8920.  [OA](https://engine.scholarcy.com/oa_version?query=Agarwal%2C%20B.%20Financial%20sentiment%20analysis%20model%20utilizing%20knowledge-base%20and%20domain-specific%20representation%202023&author=Agarwal&title=Financial%20sentiment%20analysis%20model%20utilizing%20knowledge-base%20and%20domain-specific%20representation&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Agarwal%2C%20B.%20Financial%20sentiment%20analysis%20model%20utilizing%20knowledge-base%20and%20domain-specific%20representation%202023) [Scite](/scite_tallies?query=author%3AAgarwal%2Ctitle%3AFinancial%20sentiment%20analysis%20model%20utilizing%20knowledge-base%20and%20domain-specific%20representation%2Cyear%3A2023)

[^Ahmad_2023_a]: Ahmad, H.O., Umar, S.U., 2023. Sentiment analysis of financial textual data using machine learning and deep learning models. Informatica 47 (5), 4673.  [OA](https://engine.scholarcy.com/oa_version?query=Ahmad%2C%20H.O.%20Umar%2C%20S.U.%20Sentiment%20analysis%20of%20financial%20textual%20data%20using%20machine%20learning%20and%20deep%20learning%20models%202023&author=Ahmad&title=Sentiment%20analysis%20of%20financial%20textual%20data%20using%20machine%20learning%20and%20deep%20learning%20models&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Ahmad%2C%20H.O.%20Umar%2C%20S.U.%20Sentiment%20analysis%20of%20financial%20textual%20data%20using%20machine%20learning%20and%20deep%20learning%20models%202023) [Scite](/scite_tallies?query=author%3AAhmad%2Ctitle%3ASentiment%20analysis%20of%20financial%20textual%20data%20using%20machine%20learning%20and%20deep%20learning%20models%2Cyear%3A2023)

[^Cam_et+al_2024_a]: Cam, H., Cam, A.V., Demirel, U., Ahmed, S., 2024. Sentiment analysis of financial Twitter posts on Twitter with the machine learning classifiers. Heliyon 10 (1), e23784.  [OA](https://engine.scholarcy.com/oa_version?query=Cam%2C%20H.%20Cam%2C%20A.V.%20Demirel%2C%20U.%20Ahmed%2C%20S.%20Sentiment%20analysis%20of%20financial%20Twitter%20posts%20on%20Twitter%20with%20the%20machine%20learning%20classifiers%202024&author=Cam&title=Sentiment%20analysis%20of%20financial%20Twitter%20posts%20on%20Twitter%20with%20the%20machine%20learning%20classifiers&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Cam%2C%20H.%20Cam%2C%20A.V.%20Demirel%2C%20U.%20Ahmed%2C%20S.%20Sentiment%20analysis%20of%20financial%20Twitter%20posts%20on%20Twitter%20with%20the%20machine%20learning%20classifiers%202024) [Scite](/scite_tallies?query=author%3ACam%2Ctitle%3ASentiment%20analysis%20of%20financial%20Twitter%20posts%20on%20Twitter%20with%20the%20machine%20learning%20classifiers%2Cyear%3A2024)

[^Choe_et+al_2023_a]: Choe, J., Noh, K., Kim, N., Ahn, S., Jung, W., 2023. Exploring the impact of corpus diversity on financial pretrained language models. In: Bouamor, H., Pino, J., Bali, K. (Eds.), Findings of EMNLP 2023 2101–2112. Association for Computational Linguistics, Singapore.  [OA](https://scholar.google.co.uk/scholar?q=Choe%2C%20J.%20Noh%2C%20K.%20Kim%2C%20N.%20Ahn%2C%20S.%20Exploring%20the%20impact%20of%20corpus%20diversity%20on%20financial%20pretrained%20language%20models%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Choe%2C%20J.%20Noh%2C%20K.%20Kim%2C%20N.%20Ahn%2C%20S.%20Exploring%20the%20impact%20of%20corpus%20diversity%20on%20financial%20pretrained%20language%20models%202023) 

[^Devlin_et+al_2019_a]: Devlin, J., Chang, M.W., Lee, K., Toutanova, K., 2019. BERT: Pre-training of deep bidirectional transformers for language understanding. arXiv:1810.04805.  [OA](https://arxiv.org/abs/1810.04805)  

[^Ding_et+al_2015_a]: Ding, X., Zhang, Y., Liu, T., Duan, J., 2015. Deep learning for event-driven stock prediction. In: International Joint Conference on Artificial Intelligence. IJCAI 2015, IJCAI, pp. 2327–2333.  [OA](https://scholar.google.co.uk/scholar?q=Ding%2C%20X.%20Zhang%2C%20Y.%20Liu%2C%20T.%20Duan%2C%20J.%20Deep%20learning%20for%20event-driven%20stock%20prediction%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Ding%2C%20X.%20Zhang%2C%20Y.%20Liu%2C%20T.%20Duan%2C%20J.%20Deep%20learning%20for%20event-driven%20stock%20prediction%202015) 

[^Du_et+al_2023_a]: Du, K., Xing, F., Cambria, E., 2023. Incorporating multiple knowledge sources for targeted aspect-based financial sentiment analysis. ACM Trans. Manag. Inf. Syst. 14 (3), 23:1–23:24.  [OA](https://engine.scholarcy.com/oa_version?query=Du%2C%20K.%20Xing%2C%20F.%20Cambria%2C%20E.%20Incorporating%20multiple%20knowledge%20sources%20for%20targeted%20aspect-based%20financial%20sentiment%20analysis%202023&author=Du&title=Incorporating%20multiple%20knowledge%20sources%20for%20targeted%20aspect-based%20financial%20sentiment%20analysis&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Du%2C%20K.%20Xing%2C%20F.%20Cambria%2C%20E.%20Incorporating%20multiple%20knowledge%20sources%20for%20targeted%20aspect-based%20financial%20sentiment%20analysis%202023) [Scite](/scite_tallies?query=author%3ADu%2Ctitle%3AIncorporating%20multiple%20knowledge%20sources%20for%20targeted%20aspect-based%20financial%20sentiment%20analysis%2Cyear%3A2023)

[^Du_et+al_2024_a]: Du, K., Xing, F., Mao, R., Cambria, E., 2024. Financial sentiment analysis: Techniques and applications. ACM Comput. Surv. 56 (9), 220:1–220:42.  [OA](https://engine.scholarcy.com/oa_version?query=Du%2C%20K.%20Xing%2C%20F.%20Mao%2C%20R.%20Cambria%2C%20E.%20Financial%20sentiment%20analysis%3A%20Techniques%20and%20applications%202024&author=Du&title=Financial%20sentiment%20analysis%3A%20Techniques%20and%20applications&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Du%2C%20K.%20Xing%2C%20F.%20Mao%2C%20R.%20Cambria%2C%20E.%20Financial%20sentiment%20analysis%3A%20Techniques%20and%20applications%202024) [Scite](/scite_tallies?query=author%3ADu%2Ctitle%3AFinancial%20sentiment%20analysis%3A%20Techniques%20and%20applications%2Cyear%3A2024)

[^Garcia_et+al_2023_a]: Garcia, D., Hu, X., Rohrer, M., 2023. The colour of finance words. J. Financ. Econ. 147 (3), 525–549.  [OA](https://engine.scholarcy.com/oa_version?query=Garcia%2C%20D.%20Hu%2C%20X.%20Rohrer%2C%20M.%20The%20colour%20of%20finance%20words%202023&author=Garcia&title=The%20colour%20of%20finance%20words&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Garcia%2C%20D.%20Hu%2C%20X.%20Rohrer%2C%20M.%20The%20colour%20of%20finance%20words%202023) [Scite](/scite_tallies?query=author%3AGarcia%2Ctitle%3AThe%20colour%20of%20finance%20words%2Cyear%3A2023)

[^Karanikola_et+al_2023_a]: Karanikola, A., Davrazos, G., Liapis, C.M., Kotsiantis, S., 2023. Financial sentiment analysis: Classic methods vs. deep learning models. Intell. Decis. Technol. 17 (4), 893–915.  [OA](https://engine.scholarcy.com/oa_version?query=Karanikola%2C%20A.%20Davrazos%2C%20G.%20Liapis%2C%20C.M.%20Kotsiantis%2C%20S.%20Financial%20sentiment%20analysis%3A%20Classic%20methods%20vs.%20deep%20learning%20models%202023&author=Karanikola&title=Financial%20sentiment%20analysis%3A%20Classic%20methods%20vs.%20deep%20learning%20models&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Karanikola%2C%20A.%20Davrazos%2C%20G.%20Liapis%2C%20C.M.%20Kotsiantis%2C%20S.%20Financial%20sentiment%20analysis%3A%20Classic%20methods%20vs.%20deep%20learning%20models%202023) [Scite](/scite_tallies?query=author%3AKaranikola%2Ctitle%3AFinancial%20sentiment%20analysis%3A%20Classic%20methods%20vs.%20deep%20learning%20models%2Cyear%3A2023)

[^Kaur_2023_a]: Kaur, G., Sharma, A., 2023. A deep learning-based model using hybrid feature extraction approach for consumer sentiment analysis. J. Big Data 10 (1), 5.  [OA](https://engine.scholarcy.com/oa_version?query=Kaur%2C%20G.%20Sharma%2C%20A.%20A%20deep%20learning-based%20model%20using%20hybrid%20feature%20extraction%20approach%20for%20consumer%20sentiment%20analysis%202023&author=Kaur&title=A%20deep%20learning-based%20model%20using%20hybrid%20feature%20extraction%20approach%20for%20consumer%20sentiment%20analysis&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Kaur%2C%20G.%20Sharma%2C%20A.%20A%20deep%20learning-based%20model%20using%20hybrid%20feature%20extraction%20approach%20for%20consumer%20sentiment%20analysis%202023) [Scite](/scite_tallies?query=author%3AKaur%2Ctitle%3AA%20deep%20learning-based%20model%20using%20hybrid%20feature%20extraction%20approach%20for%20consumer%20sentiment%20analysis%2Cyear%3A2023)

[^Kearney_2014_a]: Kearney, C., Liu, S., 2014. Textual sentiment in finance: A survey of methods and models. Int. Rev. Financ. Anal. 33, 171–185.  [OA](https://engine.scholarcy.com/oa_version?query=Kearney%2C%20C.%20Liu%2C%20S.%20Textual%20sentiment%20in%20finance%3A%20A%20survey%20of%20methods%20and%20models%202014&author=Kearney&title=Textual%20sentiment%20in%20finance%3A%20A%20survey%20of%20methods%20and%20models&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Kearney%2C%20C.%20Liu%2C%20S.%20Textual%20sentiment%20in%20finance%3A%20A%20survey%20of%20methods%20and%20models%202014) [Scite](/scite_tallies?query=author%3AKearney%2Ctitle%3ATextual%20sentiment%20in%20finance%3A%20A%20survey%20of%20methods%20and%20models%2Cyear%3A2014)

[^Li_et+al_2023_a]: Li, X., Chan, S., Zhu, X., Pei, Y., Ma, Z., Liu, X., Shah, S., 2023. Are ChatGPT and GPT-4 general-purpose solvers for financial text analytics? A study on several typical tasks. In: Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing: Industry Track. Association for Computational Linguistics, Singapore, pp. 408–422.  [OA](https://scholar.google.co.uk/scholar?q=Li%2C%20X.%20Chan%2C%20S.%20Zhu%2C%20X.%20Pei%2C%20Y.%20Are%20ChatGPT%20and%20GPT-4%20general-purpose%20solvers%20for%20financial%20text%20analytics%3F%20A%20study%20on%20several%20typical%20tasks%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Li%2C%20X.%20Chan%2C%20S.%20Zhu%2C%20X.%20Pei%2C%20Y.%20Are%20ChatGPT%20and%20GPT-4%20general-purpose%20solvers%20for%20financial%20text%20analytics%3F%20A%20study%20on%20several%20typical%20tasks%202023) 

[^Lin_2024_a]: Lin, W., Liao, L.C., 2024. Lexicon-based prompt for financial dimensional sentiment analysis. Expert Syst. Appl. 244, 122936.  [OA](https://engine.scholarcy.com/oa_version?query=Lin%2C%20W.%20Liao%2C%20L.C.%20Lexicon-based%20prompt%20for%20financial%20dimensional%20sentiment%20analysis%202024&author=Lin&title=Lexicon-based%20prompt%20for%20financial%20dimensional%20sentiment%20analysis&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Lin%2C%20W.%20Liao%2C%20L.C.%20Lexicon-based%20prompt%20for%20financial%20dimensional%20sentiment%20analysis%202024) [Scite](/scite_tallies?query=author%3ALin%2Ctitle%3ALexicon-based%20prompt%20for%20financial%20dimensional%20sentiment%20analysis%2Cyear%3A2024)

[^Loughran_2011_a]: Loughran, T., McDonald, B., 2011. When is a liability not a liability?, Textual analysis, dictionaries, 10-Ks. J. Financ. 66 (1), 35–65.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20McDonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%2C%20Textual%20analysis%2C%20dictionaries%2C%2010-Ks%202011&author=Loughran&title=When%20is%20a%20liability%20not%20a%20liability%3F%2C%20Textual%20analysis%2C%20dictionaries%2C%2010-Ks&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20McDonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%2C%20Textual%20analysis%2C%20dictionaries%2C%2010-Ks%202011) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3AWhen%20is%20a%20liability%20not%20a%20liability%3F%2C%20Textual%20analysis%2C%20dictionaries%2C%2010-Ks%2Cyear%3A2011)

[^Maia_et+al_2018_a]: Maia, M., Handschuh, S., Freitas, A., Davis, B., McDermott, R., Zarrouk, M., Balahur, A., 2018. WWW’18 open challenge: Financial opinion mining and question answering. In: The Web Conference 2018 1941–1942. ACM.  [OA](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20Davis%2C%20B.%20WWW%E2%80%9918%20open%20challenge%3A%20Financial%20opinion%20mining%20and%20question%20answering%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Maia%2C%20M.%20Handschuh%2C%20S.%20Freitas%2C%20A.%20Davis%2C%20B.%20WWW%E2%80%9918%20open%20challenge%3A%20Financial%20opinion%20mining%20and%20question%20answering%202018) 

[^Malo_et+al_2014_a]: Malo, P., Sinha, A., Korhonen, P., Wallenius, J., Takala, P., 2014. Good debt or bad debt: Detecting semantic orientations in economic texts. J. Assoc. Inf. Sci. Technol. 65 (4), 782–796.  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014&author=Malo&title=Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%2Cyear%3A2014)

[^Man_et+al_2019_a]: Man, X., Luo, T., Lin, J., 2019. Financial sentiment analysis (FSA): A survey. In: International Conference on Power System Technology. ICPS, IEEE, pp. 617–622.  [OA](https://scholar.google.co.uk/scholar?q=Man%2C%20X.%20Luo%2C%20T.%20Lin%2C%20J.%20Financial%20sentiment%20analysis%20%28FSA%29%3A%20A%20survey%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Man%2C%20X.%20Luo%2C%20T.%20Lin%2C%20J.%20Financial%20sentiment%20analysis%20%28FSA%29%3A%20A%20survey%202019) 

[^Mishev_et+al_2020_a]: Mishev, K., Gjorgjevikj, A., Vodenska, I., Chitkushev, L.T., Trajanov, D., 2020. Evaluation of sentiment analysis in finance: From lexicons to transformers. IEEE Access 8, 131662–131682.  [OA](https://engine.scholarcy.com/oa_version?query=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%202020&author=Mishev&title=Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%202020) [Scite](/scite_tallies?query=author%3AMishev%2Ctitle%3AEvaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2Cyear%3A2020)

[^Sinha_et+al_2022_a]: Sinha, A., Kedas, S., Kumar, R., Malo, P., 2022. SEntFiN 1.0: Entity-aware sentiment analysis for financial news. J. Assoc. Inf. Sci. Technol. 73 (9), 1314–1335.  [OA](https://engine.scholarcy.com/oa_version?query=Sinha%2C%20A.%20Kedas%2C%20S.%20Kumar%2C%20R.%20Malo%2C%20P.%20SEntFiN%201.0%3A%20Entity-aware%20sentiment%20analysis%20for%20financial%20news%202022&author=Sinha&title=SEntFiN%201.0%3A%20Entity-aware%20sentiment%20analysis%20for%20financial%20news&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Sinha%2C%20A.%20Kedas%2C%20S.%20Kumar%2C%20R.%20Malo%2C%20P.%20SEntFiN%201.0%3A%20Entity-aware%20sentiment%20analysis%20for%20financial%20news%202022) [Scite](/scite_tallies?query=author%3ASinha%2Ctitle%3ASEntFiN%201.0%3A%20Entity-aware%20sentiment%20analysis%20for%20financial%20news%2Cyear%3A2022)

[^Sinha_2021_a]: Sinha, A., Khandait, T., 2021. Impact of news on the commodity market: Dataset and results. In: Advances in Information and Communication: Proceedings of the 2021 Future of Information and Communication Conference. FICC, vol. 2, Springer, pp. 589–601.  [OA](https://scholar.google.co.uk/scholar?q=Sinha%2C%20A.%20Khandait%2C%20T.%20Impact%20of%20news%20on%20the%20commodity%20market%3A%20Dataset%20and%20results%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Sinha%2C%20A.%20Khandait%2C%20T.%20Impact%20of%20news%20on%20the%20commodity%20market%3A%20Dataset%20and%20results%202021) 

[^Sohangir_et+al_2018_a]: Sohangir, S., Wang, D., Pomeranets, A., Khoshgoftaar, T.M., 2018. Big data: Deep learning for financial sentiment analysis. J. Big Data 5 (1), 3.  [OA](https://engine.scholarcy.com/oa_version?query=Sohangir%2C%20S.%20Wang%2C%20D.%20Pomeranets%2C%20A.%20Khoshgoftaar%2C%20T.M.%20Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%202018&author=Sohangir&title=Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Sohangir%2C%20S.%20Wang%2C%20D.%20Pomeranets%2C%20A.%20Khoshgoftaar%2C%20T.M.%20Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%202018) [Scite](/scite_tallies?query=author%3ASohangir%2Ctitle%3ABig%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%2Cyear%3A2018)

[^Wang_et+al_2023_a]: Wang, N., Yang, H., Wang, C.D., 2023. Fingpt: Instruction tuning benchmark for open-source large language models in financial datasets. ArXiv preprint arXiv: 2310.04793.  [OA](https://arxiv.org/abs/2310.04793)  

[^Wu_et+al_2023_a]: Wu, S., Irsoy, O., Lu, S., Dabravolski, V., Dredze, M., Gehrmann, S., Kambadur, P., Rosenberg, D., Mann, G., 2023. Bloomberggpt: A large language model for finance. ArXiv preprint arXiv:2303.17564.  [OA](https://arxiv.org/abs/2303.17564)  

[^Yang_et+al_2020_a]: Yang, Y., Uy, M.C.S., Huang, A., 2020. FinBERT: A pretrained language model for financial communications. arXiv:2006.08097.  [OA](https://arxiv.org/abs/2006.08097)  

