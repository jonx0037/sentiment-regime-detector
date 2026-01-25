[[Nasiopoulos_et+al_FinancialSentimentAnalysisClassificationComparative_2025]]

# [Financial Sentiment Analysis and Classification: A Comparative Study of Fine-Tuned Deep Learning Models](https://doi.org/10.3390/ijfs13020075)

## [[Dimitrios Κ. Nasiopoulos]]; [[Konstantinos I. Roumeliotis]]; [[Δαμιανός Π. Σακάς]] et al.

## Abstract

Financial sentiment analysis is crucial for making informed decisions in financial markets, as it helps predict trends, guide investment decisions, and assess economic conditions. Traditional methods for financial sentiment classification, such as Support Vector Machines (SVM), Random Forests, and Logistic Regression, served as our baseline models. While somewhat effective, these conventional approaches often struggled to capture the complexity and nuance of financial language. Recent advancements in deep learning, particularly transformer-based models like GPT and BERT, have significantly enhanced sentiment analysis by capturing intricate linguistic patterns. In this study, we explore the application of deep learning to financial sentiment analysis, focusing on fine-tuning GPT-4o, GPT-4o-mini, BERT, and FinBERT, and comparing them with traditional models. To ensure optimal configurations, we performed hyperparameter tuning using Bayesian optimization across 100 trials. Using a combined dataset of FiQA and Financial PhraseBank, we first apply zero-shot classification and then fine-tune each model to improve performance. The results demonstrate substantial improvements in sentiment prediction accuracy post-fine-tuning, with GPT-4o-mini showing strong efficiency and performance. Our findings highlight the potential of deep learning models, particularly GPT models, in advancing financial sentiment classification, offering valuable insights for investors and financial analysts seeking to understand market sentiment and make data-driven decisions.

## Key concepts

#finding/bidirectional_encoder_representations_from_transformers; #bidirectional_encoder_representations_from_transformers; #finding/sentiment_classification; #sentiment_classification; #finding/generative_pre_trained_transformers; #generative_pre_trained_transformers; #finding/support_vector_machines; #support_vector_machines; #claim/GPT_4; #GPT_4; #claim/logistic_regression; #logistic_regression

## Quote
>
> The study explores the adoption of Large Language Models (LLMs) in production-grade financial applications, with a focus on classifying financial sentiment from textual data, and highlights the need for cost-aware optimization strategies.

## Key points

- Financial sentiment analysis has emerged as a pivotal area in financial technology, offering valuable insights into market trends, investor decisions, and economic indicators. The ability to accurately classify sentiment in financial texts can significantly enhance decision-making processes, from predicting stock price movements to shaping investment strategies ([^Du_et+al_2024_a])
- Given the high-stakes nature of financial markets, leveraging advanced Natural Language Processing (NLP) techniques to extract meaningful sentiment from financial documents, news articles, and social media discussions is of paramount importance
- This study aims to conduct a comparative analysis of fine-tuned transformer models for financial sentiment classification, directly comparing them with traditional models such as Support Vector Machines (SVM), Random Forests, and Logistic Regression
- This section reviews recent research aimed at addressing these challenges, with a focus on transformer-based approaches (e.g., Bidirectional Encoder Representations from Transformers (BERT), FinBERT, Generative Pre-trained Transformers (GPT) variants) and other techniques applied to Financial Sentiment Analysis (FSA)
- Results In Section 3, a comprehensive examination of the methodology used to implement and fine-tune the transformer models GPT and BERT was conducted, along with the hyperparameter tuning strategies employed for training the SVM, Random Forest, and Logistic Regression algorithms in the context of financial sentiment analysis
- Achieved an 8.53% improvement in stock price prediction
- Restrictions, lack of transparency, and limited support for efficient training strategies. These findings suggest a tiered model selection strategy depending on application context: traditional models for cost-sensitive, high-volume tasks; transformer-based models like BERT and FinBERT for balanced performance and interpretability; and LLMs for high-stakes, data-scarce environments where accuracy is paramount

## Summary

### Introduction

Financial sentiment analysis is crucial for making informed decisions in financial markets, as it helps predict trends, guide investment decisions, and assess economic conditions.
Traditional methods for financial sentiment classification, such as Support Vector Machines (SVM), Random Forests, and Logistic Regression, have limitations in capturing the complexity and nuance of financial language.
Recent advancements in deep learning, particularly transformer-based models like GPT and BERT, have significantly enhanced sentiment analysis by capturing intricate linguistic patterns.

### Methodology

This study explores the application of deep learning to financial sentiment analysis, focusing on fine-tuning GPT-4o, GPT-4o-mini, BERT, and FinBERT, and comparing them with traditional models.
The study uses a combined dataset of FiQA and Financial PhraseBank and performs hyperparameter tuning using Bayesian optimization across 100 trials.
The results demonstrate substantial improvements in sentiment prediction accuracy post-fine-tuning, with GPT-4o-mini showing strong efficiency and performance.

### Findings

The study highlights the potential of deep learning models, particularly GPT models, in advancing financial sentiment classification, offering valuable insights for investors and financial analysts seeking to understand market sentiment and make data-driven decisions.
The findings also emphasize the importance of domain-specific fine-tuning and the effectiveness of retrieval-augmented and instruction-tuned approaches in improving sentiment classification accuracy.

### Models

The Enhanced Neural Model (SSENM) improves sentiment predictions by 2-3% over baselines by leveraging dependency graphs and self-attention.
Other models, such as multi-agent and hybrid frameworks, have also shown promise in capturing a broader range of signals, leading to more robust financial sentiment analysis (FSA) systems.
For example, Xing's multi-agent paradigm and J.
Yang et al's hybrid LASSO-LSTM model has achieved improved results.
The study employed several models for financial sentiment classification, including SVM, Random Forest, Logistic Regression, BERT, FinBERT, and GPT.
The SVM model achieved a validation accuracy of 0.6899, while the Random Forest model achieved 0.6725.
The Logistic Regression model achieved a validation accuracy of 0.6899.

### Multimodal Approaches

Multimodal and social media-focused approaches have examined sentiment analysis of social media data and corporate communications.
Studies, such as Qian et al. 's analysis of Twitter sentiment and Todd et al. 's incorporation of speech emotion recognition, have demonstrated the potential of multimodal fusion to sharpen FSA performance.
Additionally, ensemble architectures, such as Sy et al.'s ensemble BERT, have shown improvements in argument unit identification.

### Robustness

Adversarial attacks and model robustness have become a focus of research, with studies revealing vulnerabilities in general-purpose keyword-based models.
However, domain-specific transformers like FinBERT have shown greater resilience.
The need for continual improvements in robust training methods, adversarial detection, and domain-tailored approaches has been highlighted to safeguard FSA insights.

### Optimization

The study used Bayesian optimization with the Optuna framework to fine-tune each model's hyperparameters.
The optimization process involved exploring a comprehensive hyperparameter space to improve each model's performance.
The importance of each hyperparameter was analyzed, and the results showed that the kernel type had the highest impact on the SVM model's performance, while the learning rate had the highest impact on the BERT model's performance.

### Performance

The study evaluated each model's performance on a validation and a test set.
The results showed that the BERT model achieved the highest validation accuracy, followed by the FinBERT model.
The GPT model was fine-tuned and deployed via the OpenAI API, and its performance was evaluated using a specialized class that manages API connectivity and constructs prompts.
The study also analyzed the average prediction time per sample for each model, with the Logistic Regression model achieving the fastest.

### Model Development

The response format adhered to standardized coding and accessibility principles, with output structured in compliance with the JSON standard.
A final prompt was developed that consistently yielded outputs in the desired format, enhancing both human comprehension and model efficiency.
The GPT-4o and GPT-4o-mini models were fine-tuned using the actual sentiment text labels, with two JSONL-formatted files generated to create prompt-response pairs.
The fine-tuning process used the default hyperparameter settings provided by OpenAI, with 3 epochs of training, a batch size of 3, and a learning rate multiplier of 1.8.

### Model Performance

The GPT-4o and GPT-4o-mini models were evaluated on a zero-shot basis, achieving accuracies of 0.7984 and 0.7752, respectively.
After fine-tuning, both models exhibited substantial performance improvements, with GPT-4o improving its accuracy from 0.7984 to 0.8779 and GPT-4o-mini improving from 0.7752 to 0.8779.
The fine-tuned LLMs outperformed the fine-tuned BERT models, with GPT-4o and GPT-4o-mini achieving virtually identical accuracies of 0.8779.
Traditional machine learning algorithms, including SVM, Random Forest, and Logistic Regression, lagged behind deep learning approaches, with accuracies of 0.6453-0.6531.
The fine-tuned GPT-4o models delivered the highest accuracy, but at the cost of increased computational time and cost.
The GPT-4o-mini model offered a balance between efficiency and performance, making it a viable option for applications requiring lower latency and cost-effective processing.
The BERT and FinBERT models exhibited significantly lower prediction times and costs, but their performance metrics remained lower than those of the fine-tuned GPT-4o models.
Fine-tuned LLMs surpassed BERT models, achieving a greater mean accuracy of 9%.
LLMs, particularly fine-tuned versions of GPT-4o, consistently achieved the highest accuracy, outperforming all other models by a substantial margin.
Transformer-based models, such as BERT and FinBERT, demonstrated a notable advantage in handling neutral sentiments.

### Comparison And Insights

The results highlight the efficacy and adaptability of large language models, with GPT-4o and GPT-4o-mini achieving high performance in financial sentiment classification.
The general BERT model outperformed FinBERT, despite FinBERT being pre-trained on financial corpora.
The fine-tuned LLMs were 8.11% more accurate than the fine-tuned BERT model and 9.68% more accurate than the fine-tuned FinBERT model.
The results also suggest that smaller architectures, such as GPT-4o-mini, can effectively learn domain-specific knowledge when supported by high-quality training data and well-optimized hyperparameter settings.

### Sentiment Classification

Neutral sentiment remained the most difficult to classify accurately, with higher misclassification rates concentrated there.
The fine-tuned GPT-4o model misclassified 26 neutral samples as negative, while the fine-tuned GPT-4o-mini model misclassified only 24 neutral instances as negative.
The BERT and FinBERT models also struggled with neutral sentiment, with BERT incorrectly classifying 28 neutral instances as negative and FinBERT misclassifying 23 neutral samples as negative.

### Efficiency And Cost

The traditional models, such as Logistic Regression, SVM, and Random Forest, were the most computationally efficient options, but their performance metrics were significantly lower than those of the transformer-based models.
The fine-tuned GPT-4o models had higher computational demands, while the GPT-4o-mini model demonstrated significantly faster prediction times and lower costs.
The BERT and FinBERT models were highly efficient and cost-effective, but their performance was lower than that of the fine-tuned GPT-4o models.

### Cost And Efficiency

Fine-tuning LLMs was found to be significantly more expensive than fine-tuning BERT models, with the GPT-4o model costing 558.26 times as much.
LLMs also required longer training and prediction times compared to BERT and traditional models.
The high computational costs and limitations of LLMs, including API restrictions and limited transparency, pose challenges to their adoption in production-grade applications.

### Applications And Limitations

The study's findings have direct implications for real-world applications, particularly in the financial technology sector, where transformer-based models and fine-tuned LLMs can be integrated to automate sentiment analysis and provide real-time insights.
However, the study is limited to the classification of financial sentiment from textual data and does not generalize to other NLP tasks or domains.
Additionally, the use of closed-source models and economic constraints played a central role in model selection and tuning, highlighting the need for further research on parameter-efficient fine-tuning techniques and cost-aware optimization strategies.

## Study subjects

### 16 individual annotators

- Semantic Orientations in Economic Texts” published in the Journal of the Association for Information Science and Technology ([^Malo_et+al_2014_a]; [^Malo_2024_a]). This dataset is original and human-annotated, not synthetic, as the sentiment labels were assigned by 16 individual annotators, with a reported average pairwise agreement of 74.9%. The dataset includes two columns: Sentence, containing the financial text, and Sentiment, labeling each sentence as positive, negative, or neutral

### 516 samples

- files—train_set.csv, validation_set.csv, and test_set.csv—for subsequent modeling phases. The final dataset distributions included 516 samples in the test set, 516 in the validation set, and 1548 in the training set, all equally distributed among the three sentiment labels. It is also important to consider that some machine learning algorithms can process string labels directly, while others require numerical encoding

## Data analysis

- #method/svm_model
- #method/bert_model
- #method/random_forest_model
- #method/the_logistic_regression_model
- #method/logistic_regression

## Findings

- Showed ChatGPT with effective prompt engineering improved performance by 35% over
- Achieved an 8.53% improvement in stock price prediction
- Introduced a retrieval-augmented LLM framework that integrates external knowledge sources for <a class="keyword" href="https://en.wikipedia.org/wiki/sentiment_classification" title="sentiment classification">sentiment classification</a>, achieving a 15–48% accuracy advantage over baseline models
- Employed Parameter-Efficient Fine-Tuning (<a class="keyword" href="#" title="Parameter-Efficient Fine-Tuning">PEFT</a>) on LLaMA 2 LLM within a retrieval-augmented setup, reaching 89% accuracy
- [^Yang_et+al_2022_a]) combined sentiment features with technical indicators in a hybrid LASSO-LSTM model, achieving an 8.53% improvement for stock price prediction
- <mark class="claim">When evaluated on the test set, the model achieved an accuracy of 0.6453</mark>
- <mark class="claim">The worst-performing trial achieved an accuracy of 0.4981, while the best trial showed an improvement of 0.1744 (35.02%) over this worst result</mark>
- <mark class="claim">For the test set, the model achieved a test accuracy of 0.6531, with similar performance across the sentiment classes</mark>
- <mark class="claim">The optimization process took 0.78 min, with the worst-performing trial achieving an accuracy of 0.0000</mark>
- <mark class="claim">On the test set, the model achieved an accuracy of 0.6492, with a classification report showing <mark class="fact">slightly lower performance compared to the validation set</mark></mark>
- Improvement over the worst-performing trial and a 1.76% improvement over the average trial accuracy
- <a class="keyword" href="#" title="Generative Pre-trained Transformers">GPT</a>-4o improved its accuracy from 0.7984 to 0.8779 (a 9.96% improvement), increasing its precision, recall, and F1-score to around the 0.88 range
- <a class="keyword" href="#" title="Generative Pre-trained Transformers">GPT</a>-4o-mini’s accuracy improvement was even greater, rising from 0.7752 to 0.8779 (a 13.25% improvement), and its precision, recall, and F1-scores also converged around 0.8770–0.8780
- The fine-tuned LLMs are 8.11% more accurate than the fine-tuned <a class="keyword" href="#" title="Bidirectional Encoder Representations from Transformers">BERT</a> model and 9.68% more accurate than the fine-tuned FinBERT model
- Increase for <a class="keyword" href="#" title="Generative Pre-trained Transformers">GPT</a>-4o and an even greater improvement of 13.25% for <a class="keyword" href="#" title="Generative Pre-trained Transformers">GPT</a>-4o-mini
- And FinBERT) demonstrated a mean higher accuracy by 24.18% over traditional models (<a class="keyword" href="https://en.wikipedia.org/wiki/Support_Vector_Machines" title="Support Vector Machines">SVM</a>, RF, LR)
- <mark class="claim"><mark class="fact">While the traditional models achieved a mean accuracy of only 64.92%</mark>, it is important to contextualize this result</mark>
- After fine-tuning, LLMs surpassed <a class="keyword" href="#" title="Bidirectional Encoder Representations from Transformers">BERT</a> models, achieving a greater mean accuracy of 9%

## Contributions

- In summary, the results highlight the efficacy and adaptability of large language models and, unexpectedly, the general BERT model over FinBERT in the domain of financial sentiment classification. The comparable performance of GPT-4o-mini and GPT-4o underscores the value of parameter-efficient architectures, whereas the relatively modest scores of traditional ML methods confirm the advantages of deep contextualized embeddings for complex sentiment analysis tasks.

## Limitations

- The study has several limitations, including the confinement to the classification of financial sentiment from textual data, which may not generalize to other NLP tasks or domains. Additionally, the study notes that LLMs incur high computational costs and face multiple limitations, including API restrictions, limited transparency, and limited support for efficient training strategies.
- The limitations of the study are that economic constraints played a central role in model selection and tuning, and that the study may not generalize to other NLP tasks or domains.

## Future work

- Future research should explore parameter-efficient fine-tuning techniques and cost-aware optimization strategies to bridge the performance-efficiency gap and enable broader adoption of deep learning models for financial sentiment analysis. Additionally, the study suggests that future work could focus on applying transformer models to other NLP tasks or domains.
- The future work suggested by the study is to explore parameter-efficient fine-tuning techniques and cost-aware optimization strategies to bridge the performance-efficiency gap and enable broader adoption of LLMs in production-grade financial applications.

## References

[^Du_et+al_2024_a]: Du, K., Xing, F., Mao, R., &; Cambria, E. (2024). Financial Sentiment analysis: Techniques and applications. ACM Computing Surveys, 56(9), 220. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Du%2C%20K.%20Xing%2C%20F.%20Mao%2C%20R.%20Cambria%2C%20E.%20Financial%20Sentiment%20analysis%3A%20Techniques%20and%20applications%202024&author=Du&title=Financial%20Sentiment%20analysis%3A%20Techniques%20and%20applications&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Du%2C%20K.%20Xing%2C%20F.%20Mao%2C%20R.%20Cambria%2C%20E.%20Financial%20Sentiment%20analysis%3A%20Techniques%20and%20applications%202024) [Scite](/scite_tallies?query=author%3ADu%2Ctitle%3AFinancial%20Sentiment%20analysis%3A%20Techniques%20and%20applications%2Cyear%3A2024)

[^Malo_2024_a]: Malo, P., &amp; Sinha, A. (2024). takala/financial_phrasebank datasets at Hugging Face. Available online: https://huggingface.co/datasets/takala/financial_phrasebank (accessed on 20 April 2025).  [OA](https://huggingface.co/datasets/takala/financial_phrasebank)  

[^Malo_et+al_2014_a]: Malo, P., Sinha, A., Korhonen, P., Wallenius, J., &; Takala, P. (2014). Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology, 65(4), 782–796. [CrossRef] Mathebula, M., Modupe, A., &amp; Marivate, V. (2024). Fine-tuning retrieval-augmented generation with an auto-regressive language model for sentiment analysis in financial reviews. Applied Sciences, 14(23), 10782. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014&author=Malo&title=Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%2Cyear%3A2014)

[^Yang_et+al_2022_a]: Yang, J., Wang, Y., &amp; Li, X. (2022). The LASSO-LSTM model for predicting stock price direction combines technical indicators and financial sentiment analysis. PeerJ Computer Science, 8, e1148. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Yang%2C%20J.%20Wang%2C%20Y.%20Li%2C%20X.%20Prediction%20of%20stock%20price%20direction%20using%20the%20LASSO-LSTM%20model%20combines%20technical%20indicators%20and%20financial%20sentiment%20analysis%202022&author=Yang&title=Prediction%20of%20stock%20price%20direction%20using%20the%20LASSO-LSTM%20model%20combines%20technical%20indicators%20and%20financial%20sentiment%20analysis&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20J.%20Wang%2C%20Y.%20Li%2C%20X.%20Prediction%20of%20stock%20price%20direction%20using%20the%20LASSO-LSTM%20model%20combines%20technical%20indicators%20and%20financial%20sentiment%20analysis%202022) [Scite](/scite_tallies?query=author%3AYang%2Ctitle%3APrediction%20of%20stock%20price%20direction%20using%20the%20LASSO-LSTM%20model%20combines%20technical%20indicators%20and%20financial%20sentiment%20analysis%2Cyear%3A2022)
