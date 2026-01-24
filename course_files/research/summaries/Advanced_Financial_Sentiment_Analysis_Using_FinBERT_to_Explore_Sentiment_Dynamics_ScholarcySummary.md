[[Priya_et+al_AdvancedFinancialSentimentAnalysisUsing_2025]]

# [Advanced Financial Sentiment Analysis Using FinBERT to Explore Sentiment Dynamics](https://doi.org/10.1109/idciot64235.2025.10915080)

## [[S Baghavathi Priya]]; [[Manish Kumar]]; [[Nitheesh Prakash J D]] et al.

## Abstract
This research investigates the incorporation of sophisticated Natural Language Processing (NLP) methods in the intricate field of finance. In particular, it uses FinBERT, a tailored language model designed to understand the complex subtleties of financial text data, alongside assessments of DistilBERT and Bidirectional Encoder Representations from Transformers (BERT). The main goal is to create a robust preprocessing framework that enhances the interpretability of sentiment classification models for financial applications, while providing an in-depth evaluation of their comparative performance. Through extensive empirical validation, our approach demonstrates that FinBERT outperforms the other models in accurately capturing subtle sentiment variations and financial terminology. The comparative study highlights the trade-off between computational efficiency and precision, with DistilBERT offering a streamlined option. This research emphasizes FinBERT’s transformative capabilities for analyzing financial sentiment while simultaneously delivering essential insights into the comparative strengths and weaknesses of other approaches, offering a comprehensive perspective to inform decision-making in the financial sector. Upon comprehensive analysis of the methods used in this paper, it is shown that FinBERT best captures hidden features in the data and performs well on unseen data, achieving an average accuracy of 89.6% across all 3 classes in the dataset. The suggested framework has the potential to significantly improve predictive analytics and risk management, enabling more informed, precise, and timely financial decisions in complex market conditions.

## Key concepts
#machine_learning; #sentiment_analysis; #bert_bidirectional_encoder_representations_from_transformers; #predictive_analytics; #convolutional_neural_networks_cnn; #long_short_term_memory_lstm; #transformer_machine_learning_model; #natural_language_processing_nlp; #risk_management; #finding/FinBERT; #FinBERT

## Quote
This research investigates the use of FinBERT, a tailored language model, for advanced financial sentiment analysis, demonstrating its transformative capabilities and delivering essential insights into the comparative strengths and weaknesses of other approaches.

## Key points
- Sentiment analysis is a fundamental component of Natural Language Processing (NLP) that allows for extracting nuanced viewpoints and emotions from textual data
- While Bidirectional Encoder Representations from Transformers (BERT) provides a comprehensive transformer-based framework for comprehending bidirectional text interactions, DistilBERT is a more efficient alternative that reduces processing needs while keeping most of BERT’s accuracy. These models, which were pretrained on broad corpora and fine-tuned for financial sentiment analysis, perform well on tasks such as sentiment polarity classification and sentiment intensity evaluation. They may lack FinBERT’s domain-specific optimization
- We find that performance can be substantially improved by training the model longer, with bigger batches over more data.[^11]
- Sentiment analysis can be used to spot new patterns or modifications in consumer tastes that may have an effect on particular sectors or companies
- Techniques in statistical trading that involve sentiment analysis can generate algorithms capable of automatically executing trades based on set emotional indicators


## Summary

### Introduction To Sentiment Analysis
The research investigates the use of sophisticated Natural Language Processing (NLP) methods, particularly FinBERT, in the finance industry.
FinBERT is a tailored language model created to understand complex financial text data.
The goal is to create a robust preprocessing framework that enhances the interpretability of sentiment classification models in financial applications.
FinBERT outperforms other models, such as DistilBERT and BERT, in accurately capturing subtle sentiment variations and financial terminology.

### Methodology And Models
The FinancialPhraseBank dataset is used, which is a curated collection of financial text specifically designed for sentiment analysis in the financial domain.
The dataset is sourced from various financial documents and has a rich representation of language used in the finance industry.
FinBERT, BERT, and DistilBERT are compared, with FinBERT demonstrating exceptional precision in understanding financial terms.
Other advanced models, such as Long Short-Term Memory (LSTM), Convolutional Neural Networks (CNN), and Random Forests (RF), have also shown effectiveness in financial text analysis applications.

### Applications And Future Directions
The research emphasizes FinBERT's transformative capabilities in analyzing financial sentiment and delivering essential insights into the comparative strengths and weaknesses of other approaches.
The suggested framework has the potential to significantly improve predictive analytics and risk management, enabling more informed, precise, and timely financial decisions in complex market conditions.
Future work may focus on making modal encoders more resilient, incorporating multimodal data, and improving real-time processing for video-based sentiment analysis.

### Models
The research investigates the performance of FinBERT, BERT, and DistilBERT in financial sentiment analysis.
BERT is a transformer-based model that uses a bidirectional approach to collect context from both sides of a word.
FinBERT is a variation of BERT specifically designed for finance-related tasks, while DistilBERT is a condensed version of BERT that maintains most of its functionality while being lighter and more efficient.

### Preprocessing
The dataset is preprocessed by converting the text and label columns to Python lists, splitting the dataset into training and test subsets, and tokenizing the text using the AutoTokenizer from the Hugging Face Transformers library.
The tokenized sequences are then truncated to fit within the model's maximum input length, and special tokens such as [CLS] and [SEP] are added.
The labels are converted to numerical representations using a mapping from sentiment labels to numerical IDs.

### Optimization
The models' efficiency can be optimized through strategies such as efficient tokenizers, preprocessing the dataset to reduce noise, and optimizing batching and data loading using parameters like batch size and caching preprocessed data.
The fine-tuning process involves adding task-specific layers to the pre-trained models and adjusting the parameters to minimize the loss function.
Hyperparameter tuning can also be used to further optimize the models' performance.
Tuning, either by hand or through automated tools such as Optuna, helps determine optimal values for learning rates, batch sizes, and dropout rates.
Mixed-precision training with PyTorch’s ‘torch.cuda.amp‘ can accelerate computations and significantly reduce memory usage.
Finetuning the model by freezing early layers and using learning rate schedulers further optimizes training.
Gradient accumulation enables larger effective batch sizes without exceeding memory limits, and training on multiple GPUs accelerates the process.

### Testing
The testing and validation processes within the FINBERT code are devised to ensure strong performance evaluation and fine-tuning of the model.
During validation, a held-out portion of the dataset is used to monitor the model's performance after each training epoch.
Testing uses an entirely separate dataset that was not used for either training or validation to provide an unbiased assessment of the model's final performance.
Metrics are calculated to assess the model's effectiveness in real-world applications.

### Results
The FinBERT model achieves an average accuracy of 0.896 across the 3 class labels, with a precision of 0.87 for the positive class, 0.92 for the neutral class, and 0.85 for the negative class.
The model's performance can be substantially improved by training it longer with larger batches over more data.
Techniques such as data augmentation, ensemble methods, and hyperparameter tuning can also enhance the model’s performance.
The model's robustness has been demonstrated by the overall matrix, with greater strength towards the dominant class-neutral.

## Data analysis
- #method/bert_model

## Findings
- Upon comprehensive analysis of the methods used in this paper, <mark class="fact">it is shown that FinBERT is best at capturing hidden features</mark> within the data and able to work well with unseen data also with an average accuracy of 89.6% over all <mark class="fact">the 3 classes that are present in the dataset</mark>

## Contributions
- <mark class="fact">Extracting emotions from a financial news data set can be useful in the real world for many good reasons</mark>, such as tracking market sentiments, managing risks in the financial sector, or identifying trends. Gaining insight into how traders, investors, and <mark class="fact">everyone else </mark> feel about specific stocks, companies, or the market as a whole can be quite beneficial. <mark class="fact">While negative sentiment could point to worries</mark> or possible selling pressure, <mark class="fact">positive sentiment could be related to anticipation</mark> and possible purchasing interest. <mark class="fact">The assessment and management of investment hazards can be aided by sentiment research</mark>. Unexpected changes in attitude may signal impending volatility or a market downturn, enabling investors to reduce losses by adjusting their portfolios accordingly. Sentiment analysis can be used to <mark class="fact">spot new patterns or modifications in consumer tastes that may have an effect on particular sectors or companies</mark>. Such data may be used to make strategic investment decisions or change corporate policy. Machine learning models can be trained to anticipate market changes or identify potential investment opportunities by analyzing historical sentiment data alongside market performance. Predictive analytics can help investors remain ahead of the curve and capitalize on market events. <mark class="fact">Actual market and shareholder sentiment may be derived by tracking sentiment in news stories</mark>, social networking sites, and a variety of other internet-based resources. This understanding can significantly enhance the performance of computational trading strategies and high-frequency traders. Techniques in statistical trading that involve sentiment analysis can generate algorithms <mark class="fact">capable of automatically executing trades based on set emotional indicators</mark>. These strategies can <mark class="fact">help traders capitalize on temporary market fluctuations triggered by emotional changes</mark>. <mark class="fact">Examining feelings towards specific brands or companies is another application of sentiment analysis</mark>. <mark class="fact">By tracking the sentiment related to corporate earnings announcements</mark>, product launches, and changes in leadership, investors can gain valuable insights into the potential impacts on stock prices and the overall performance of a company. Businesses can assess shareholder sentiment toward their shares and the overall impression of their company’s image using sentiment analysis. Companies can use such data to better target stakeholder relationships, messaging, and tactics to allay client fears or build on favourable emotions.

## Limitations
- The research notes that existing models may still struggle with polarity variations that are specific to certain domains. The study also acknowledges the limitations of traditional methodologies in capturing the nuanced intricacies of financial terms.
- The limitations of the study include the potential for overfitting and the need for larger and more diverse datasets to further improve the model's performance.

## Future work
- The research suggests that future work may be related to making modal encoders more resilient and incorporating multimodal data for better precision in video-based sentiment analysis. The study also highlights the potential of hybrid models that integrate various learning algorithms to enhance prediction precision and flexibility.
- The future work includes exploring methods to improve the model's performance, such as domain pretraining on larger and more diverse financial corpora, integration of multimodal data, and knowledge distillation.


## References
[^1]: S. Muhammad Ahmed Hassan Shah and S. Faizan Hussain Shah, ”Arabic Sentiment Analysis and Sarcasm Detection Using Probabilistic Projections-Based Variational Switch Transformer,” June 2023.  [OA](https://scholar.google.co.uk/scholar?q=Shah%2C%20S.Muhammad%20Ahmed%20Hassan%20S.%20Faizan%20Hussain%20Shah%2C%E2%80%9DArabic%20Sentiment%20Analysis%20and%20Sarcasm%20Detection%20Using%20Probabilistic%20ProjectionsBased%20Variational%20Switch%20Transformer%202023-06) [GScholar](https://scholar.google.co.uk/scholar?q=Shah%2C%20S.Muhammad%20Ahmed%20Hassan%20S.%20Faizan%20Hussain%20Shah%2C%E2%80%9DArabic%20Sentiment%20Analysis%20and%20Sarcasm%20Detection%20Using%20Probabilistic%20ProjectionsBased%20Variational%20Switch%20Transformer%202023-06) 

[^2]: X. Li, H. Xie, R. Y. K. Lau, T.-L. Wong, and F.-L. Wang, ”Stock Prediction via Sentimental Transfer Learning,” November 2018.  [OA](https://scholar.google.co.uk/scholar?q=X%20Li%20H%20Xie%20R%20Y%20K%20Lau%20TL%20Wong%20and%20FL%20Wang%20Stock%20Prediction%20via%20Sentimental%20Transfer%20Learning%20November%202018) [GScholar](https://scholar.google.co.uk/scholar?q=X%20Li%20H%20Xie%20R%20Y%20K%20Lau%20TL%20Wong%20and%20FL%20Wang%20Stock%20Prediction%20via%20Sentimental%20Transfer%20Learning%20November%202018) 

[^3]: G. Xu, Z. Yu, H. Yao, F. Li, Y. Meng, and X. Wu, ”Chinese Text Sentiment Analysis Based on Extended Sentiment Dictionary,” April 2019.  [OA](https://scholar.google.co.uk/scholar?q=G%20Xu%20Z%20Yu%20H%20Yao%20F%20Li%20Y%20Meng%20and%20X%20Wu%20Chinese%20Text%20Sentiment%20Analysis%20Based%20on%20Extended%20Sentiment%20Dictionary%20April%202019) [GScholar](https://scholar.google.co.uk/scholar?q=G%20Xu%20Z%20Yu%20H%20Yao%20F%20Li%20Y%20Meng%20and%20X%20Wu%20Chinese%20Text%20Sentiment%20Analysis%20Based%20on%20Extended%20Sentiment%20Dictionary%20April%202019) 

[^4]: H. Zhang, J. Wu, H. Shi, Z. Jiang, D. Ji, T. Yuan, and G. Li, ”Multidimensional Extra Evidence Mining for Image Sentiment Analysis.”  [OA](https://scholar.google.co.uk/scholar?q=H%20Zhang%20J%20Wu%20H%20Shi%20Z%20Jiang%20D%20Ji%20T%20Yuan%20and%20G%20Li%20Multidimensional%20Extra%20Evidence%20Mining%20for%20Image%20Sentiment%20Analysis) [GScholar](https://scholar.google.co.uk/scholar?q=H%20Zhang%20J%20Wu%20H%20Shi%20Z%20Jiang%20D%20Ji%20T%20Yuan%20and%20G%20Li%20Multidimensional%20Extra%20Evidence%20Mining%20for%20Image%20Sentiment%20Analysis) 

[^5]: Y. Wang, J. Wu, K. Furumai, S. Wada, and S. Kurihara, ”VAE-Based Adversarial Multimodal Domain Transfer for Video-Level Sentiment Analysis,” May 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Y%20Wang%20J%20Wu%20K%20Furumai%20S%20Wada%20and%20S%20Kurihara%20VAEBased%20Adversarial%20Multimodal%20Domain%20Transfer%20for%20VideoLevel%20Sentiment%20Analysis%20May%202022&author=Y&title=Adversarial%20Multimodal%20Domain%20Transfer%20for%20Video-Level%20Sentiment%20Analysis&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Y%20Wang%20J%20Wu%20K%20Furumai%20S%20Wada%20and%20S%20Kurihara%20VAEBased%20Adversarial%20Multimodal%20Domain%20Transfer%20for%20VideoLevel%20Sentiment%20Analysis%20May%202022) [Scite](/scite_tallies?query=author%3AY%2Ctitle%3AAdversarial%20Multimodal%20Domain%20Transfer%20for%20Video-Level%20Sentiment%20Analysis%2Cyear%3A2022)

[^6]: K. Cheng, Y. Yue, and Z. Song, ”Sentiment Classification Based on Part-ofSpeech and Self-Attention Mechanism,” January 2020.  [OA](https://scholar.google.co.uk/scholar?q=K.%20Cheng%2C%20Y.%20Yue%20Z.%20Song%2C%20%E2%80%9DSentiment%20Classification%20Based%20on%20Part-ofSpeech%20and%20Self-Attention%20Mechanism%202020-01) [GScholar](https://scholar.google.co.uk/scholar?q=K.%20Cheng%2C%20Y.%20Yue%20Z.%20Song%2C%20%E2%80%9DSentiment%20Classification%20Based%20on%20Part-ofSpeech%20and%20Self-Attention%20Mechanism%202020-01) 

[^7]: K. Abdalgader and A. Al Shibli, ”Experimental Results on Customer Reviews,” October 2020.  [OA](https://scholar.google.co.uk/scholar?q=Abdalgader%2C%20K.%20A.%20Al%20Shibli%2C%E2%80%9DExperimental%20Results%20on%20Customer%20Reviews%202020-10) [GScholar](https://scholar.google.co.uk/scholar?q=Abdalgader%2C%20K.%20A.%20Al%20Shibli%2C%E2%80%9DExperimental%20Results%20on%20Customer%20Reviews%202020-10) 

[^8]: C.-C. Chang, ”Reversible Linguistic Steganography With Bayesian Masked Language Modeling,” April 2023.  [OA](https://scholar.google.co.uk/scholar?q=CC%20Chang%20Reversible%20Linguistic%20Steganography%20With%20Bayesian%20Masked%20Language%20Modeling%20April%202023) [GScholar](https://scholar.google.co.uk/scholar?q=CC%20Chang%20Reversible%20Linguistic%20Steganography%20With%20Bayesian%20Masked%20Language%20Modeling%20April%202023) 

[^9]: B. Liu, ”Sentiment Analysis and Opinion Mining,” Synthesis Lectures on Human Language Technologies, vol. 5, no. 1, pp. 1-167, 2012.  [OA](https://engine.scholarcy.com/oa_version?query=B.%20Liu%2C%20%E2%80%9DSentiment%20Analysis%20and%20Opinion%20Mining%202012&author=C.-C.&title=Analysis%20and%20Opinion%20Mining&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=B.%20Liu%2C%20%E2%80%9DSentiment%20Analysis%20and%20Opinion%20Mining%202012) [Scite](/scite_tallies?query=author%3AC.-C.%2Ctitle%3AAnalysis%20and%20Opinion%20Mining%2Cyear%3A2012)

[^10]: X. Li, H. Xie, L. Chen, J. Wang, and X. Deng, ”News Impact on Stock Price Return via Sentiment Analysis,” Knowledge-Based Systems, vol. 69, pp. 1423, 2014.  [OA](https://engine.scholarcy.com/oa_version?query=X%20Li%20H%20Xie%20L%20Chen%20J%20Wang%20and%20X%20Deng%20News%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%20KnowledgeBased%20Systems%20vol%2069%20pp%201423%202014&author=X&title=Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=X%20Li%20H%20Xie%20L%20Chen%20J%20Wang%20and%20X%20Deng%20News%20Impact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%20KnowledgeBased%20Systems%20vol%2069%20pp%201423%202014) [Scite](/scite_tallies?query=author%3AX%2Ctitle%3AImpact%20on%20Stock%20Price%20Return%20via%20Sentiment%20Analysis%2Cyear%3A2014)

[^11]: Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, ”RoBERTa: A Robustly Optimized BERT Pretraining Approach,” arXiv preprint arXiv:1907.11692, 2019.  [OA](https://arxiv.org/abs/1907.11692)  

[^12]: M. Kraus and S. Feuerriegel, ”Decision Support from Financial Disclosures with Deep Neural Networks and Transfer Learning,” Decision Support Systems, vol. 104, pp. 38-48, 2017.  [OA](https://engine.scholarcy.com/oa_version?query=Kraus%2C%20M.%20S.%20Feuerriegel%2C%E2%80%9DDecision%20Support%20from%20Financial%20Disclosures%20with%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%202017&author=Kraus&title=Feuerriegel%2C%E2%80%9DDecision%20Support%20from%20Financial%20Disclosures%20with%20Deep%20Neural%20Networks%20and%20Transfer%20Learning&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Kraus%2C%20M.%20S.%20Feuerriegel%2C%E2%80%9DDecision%20Support%20from%20Financial%20Disclosures%20with%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%202017) [Scite](/scite_tallies?query=author%3AKraus%2Ctitle%3AFeuerriegel%2C%E2%80%9DDecision%20Support%20from%20Financial%20Disclosures%20with%20Deep%20Neural%20Networks%20and%20Transfer%20Learning%2Cyear%3A2017)

[^13]: Y. Cui, W. Che, T. Liu, B. Qin, and Z. Yang, ”Pre-Training with Whole Word Masking for Chinese BERT,” arXiv preprint arXiv:1906.08101, 2019.  [OA](https://arxiv.org/abs/1906.08101)  

[^14]: Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, ”ALBERT: A Lite BERT for Self-Supervised Learning of Language Representations,” arXiv preprint arXiv:1909.11942, 2019.  [OA](https://arxiv.org/abs/1909.11942)  

[^15]: L. Zhao, L. Li, X. Zheng, and J. Zhan, ”A BERT-Based Sentiment Analysis and Key Entity Detection Approach for Online Financial Texts.”  [OA](https://scholar.google.co.uk/scholar?q=L.%20Zhao%2C%20L.%20Li%2C%20X.%20Zheng%20J.%20Zhan%2C%20%E2%80%9DA%20BERT-Based%20Sentiment%20Analysis%20and%20Key%20Entity%20Detection%20Approach%20for%20Online%20Financial%20Texts) [GScholar](https://scholar.google.co.uk/scholar?q=L.%20Zhao%2C%20L.%20Li%2C%20X.%20Zheng%20J.%20Zhan%2C%20%E2%80%9DA%20BERT-Based%20Sentiment%20Analysis%20and%20Key%20Entity%20Detection%20Approach%20for%20Online%20Financial%20Texts) 

[^16]: M. Pota, M. Ventura, R. Catelli, and M. Esposito, “An effective BERTBased pipeline for Twitter Sentiment Analysis: A case study in Italian,” Sensors, vol. 21, no. 1, p. 133, Dec. 2020, doi:10.3390/s21010133.  [OA](https://doi.org/10.3390/s21010133)  [Scite](/scite_tallies?query=https://doi.org/10.3390/s21010133)

[^17]: Y. Shen and P. K. Zhang, “Financial sentiment analysis on news and reports using large language models and FinBERT,” arXiv (Cornell University), Oct. 2024, doi:10.48550/arxiv.2410.01987.  [OA](https://doi.org/10.48550/arxiv.2410.01987)  [Scite](/scite_tallies?query=https://doi.org/10.48550/arxiv.2410.01987)

[^18]: A. Saxena, A. Santhanavijayan, H. Shakya, G. Kumar, B. Balusamy, and F. Benedetto, “Nested Sentiment Analysis for ESG Impact: Leveraging FinBERT to Predict Market Dynamics Based on Eco-Friendly and NonEcoFriendly Product Perceptions with Explainable AI,” 2024.  [OA](https://scholar.google.co.uk/scholar?q=Saxena%2C%20A.%20Santhanavijayan%2C%20A.%20Shakya%2C%20H.%20Kumar%2C%20G.%20Nested%20Sentiment%20Analysis%20for%20ESG%20Impact%3A%20Leveraging%20FinBERT%20to%20Predict%20Market%20Dynamics%20Based%20on%20Eco-Friendly%20and%20NonEcoFriendly%20Product%20Perceptions%20with%20Explainable%20AI%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Saxena%2C%20A.%20Santhanavijayan%2C%20A.%20Shakya%2C%20H.%20Kumar%2C%20G.%20Nested%20Sentiment%20Analysis%20for%20ESG%20Impact%3A%20Leveraging%20FinBERT%20to%20Predict%20Market%20Dynamics%20Based%20on%20Eco-Friendly%20and%20NonEcoFriendly%20Product%20Perceptions%20with%20Explainable%20AI%202024) 

[^19]: T. Jiang and A. Zeng, “Financial sentiment analysis using FinBERT with application in predicting stock movement,” 2023.  [OA](https://scholar.google.co.uk/scholar?q=Jiang%2C%20T.%20Zeng%2C%20A.%20Financial%20sentiment%20analysis%20using%20FinBERT%20with%20application%20in%20predicting%20stock%20movement%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Jiang%2C%20T.%20Zeng%2C%20A.%20Financial%20sentiment%20analysis%20using%20FinBERT%20with%20application%20in%20predicting%20stock%20movement%202023) 

[^20]: K. Kirtac and G. Germano, “Enhanced financial sentiment analysis and trading strategy development using large language models,” 2024.   [OA](https://scholar.google.co.uk/scholar?q=Kirtac%2C%20K.%20Germano%2C%20G.%20Enhanced%20financial%20sentiment%20analysis%20and%20trading%20strategy%20development%20using%20large%20language%20models%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Kirtac%2C%20K.%20Germano%2C%20G.%20Enhanced%20financial%20sentiment%20analysis%20and%20trading%20strategy%20development%20using%20large%20language%20models%202024) 

