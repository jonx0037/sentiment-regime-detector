[[Roumeliotis_et+al_LlmsNlpModelsCryptocurrencySentiment_2024]]

# [LLMs and NLP Models in Cryptocurrency Sentiment Analysis: A Comparative Classification Study](https://doi.org/10.3390/bdcc8060063)

## [[Konstantinos I. Roumeliotis]]; [[Nikolaos D. Tselikas]]; [[Dimitrios Κ. Nasiopoulos]]

## Abstract

Cryptocurrencies are becoming increasingly prominent in financial investments, as more investors diversify their portfolios and individuals are drawn to their ease of use and decentralized financial opportunities. However, this accessibility also brings significant risks and rewards, often influenced by news and the sentiments of crypto investors, known as crypto signals. This paper explores the capabilities of large language models (LLMs) and natural language processing (NLP) models for sentiment analysis of cryptocurrency-related news articles. We fine-tune state-of-the-art models such as GPT-4, BERT, and FinBERT for this specific task, evaluating their performance and comparing their effectiveness in sentiment classification. By leveraging these advanced techniques, we aim to enhance understanding of sentiment dynamics in the cryptocurrency market, providing insights to inform investment decisions and risk management strategies. The outcomes of this comparative study contribute to the broader discourse on applying advanced NLP models to cryptocurrency sentiment analysis, with implications for both academic research and practical applications in financial markets.

## Key concepts

# claim/news_article; #news_article; #sentiment_analysis; #social_media; #finding/bidirectional_encoder_representations_from_transformers; #bidirectional_encoder_representations_from_transformers; #claim/large_language_models; #large_language_models; #finding/GPT_4; #GPT_4; #claim/natural_language_processing; #natural_language_processing

## Quote

This study explores the use of large language models (LLMs) and natural language processing (NLP) models for sentiment analysis and classification in the cryptocurrency sector, with a focus on fine-tuning and evaluating the performance of GPT-4, BERT, and FinBERT.

## Key points

- The volatility of cryptocurrency markets is often influenced by a myriad of factors, including news articles, social media discussions, crypto signals, and investor sentiment [^1],[^2],[^3]
- This study initially focuses on utilizing the innovative GPT-4 large language models (LLMs), alongside a parallel comparison with bidirectional encoder representations from transformers (BERT) and FinBERT natural language processing (NLP) models
- Results In Section 3, we explore the methodological approach used to assess the predictive abilities of the GPT-4 LLM, BERT, and FinBERT NLP models in crypto sentiment analysis and classification, seeking to understand their underlying complexities
- The integration of LLMs and NLP models for cryptocurrency sentiment analysis represents a powerful toolset that enhances investment decision-making in the dynamic cryptocurrency market
- This study showcases the efficacy of state-of-the-art models like GPT-4 and BERT in accurately interpreting and categorizing sentiments extracted from cryptocurrency news articles
- It is imperative to highlight that even without fine-tuning, the GPT-4 base model achieved 82.9% accuracy
- By providing a deeper understanding of sentiment dynamics in cryptocurrency markets, this study facilitates a more informed and data-driven approach to cryptocurrency investment, enabling investors to make well-informed decisions based on the real-time sentiment analysis of news articles and other relevant sources

## Summary

### Snapshot

This study explores the use of large language models (LLMs) and natural language processing (NLP) models for sentiment analysis and classification in the cryptocurrency sector, with a focus on fine-tuning and evaluating the performance of GPT-4, BERT, and FinBERT models.

### Key findings

The key findings of the study include demonstrating the feasibility of automated sentiment analysis for cryptocurrency trading decisions based on Twitter data and identifying correlations between sentiment metrics and Bitcoin price movements. Additionally, the study found that fine-tuning NLP models, such as GPT-4, can significantly enhance their performance in sentiment analysis tasks.
This study showcases the efficacy of state-of-the-art models like GPT-4 and BERT in accurately interpreting and categorizing sentiments extracted from cryptocurrency news articles
It is imperative to highlight that even without fine-tuning, the GPT-4 base model achieved 82.9% accuracy
By providing a deeper understanding of sentiment dynamics in cryptocurrency markets, this study facilitates a more informed and data-driven approach to cryptocurrency investment, enabling investors to make well-informed decisions based on the real-time sentiment analysis of news articles and other relevant sources

### Objectives

The primary objectives of the study are twofold: first, to evaluate the performance of LLMs and NLP models in cryptocurrency sentiment analysis through a comparative classification study, providing insights to inform investment strategies and risk management practices in cryptocurrency markets. Secondly, to address specific research inquiries that previous studies have not adequately covered, such as which fine-tuned model demonstrates superior predictive capabilities in cryptocurrency news sentiment analysis and classification.

### Methods

The study undertakes an extensive review of the existing literature on sentiment analysis and classification pertaining to cryptocurrencies. The study also employs fine-tuned models such as GPT-4, BERT, and FinBERT to discern sentiment in cryptocurrency news articles. The study reviews 49 papers on the evolving role of sentiment analysis in understanding and predicting cryptocurrency market dynamics.
The methods used in the study include fine-tuning NLP models, such as GPT-4 and BERT, on a dataset of cryptocurrency-related text, and evaluating their performance using metrics such as accuracy and cross-entropy loss.

### Results

The results of the study show that fine-tuning NLP models can significantly enhance their performance in sentiment analysis tasks and that automated sentiment analysis can be effective for predicting cryptocurrency price movements.

### Conclusions

The study's conclusions include demonstrating the potential of NLP models, such as GPT-4 and BERT, for sentiment analysis in cryptocurrency markets and identifying correlations between sentiment metrics and Bitcoin price movements. Additionally, the study highlights the importance of fine-tuning NLP models for improved performance in sentiment analysis tasks.
The study concludes that fine-tuning is essential for improving model performance and that the choice of model and optimizer can significantly affect the accuracy of sentiment analysis and classification. The study also highlights the importance of evaluating model performance using multiple metrics.

## Study subjects

### 1000 crypto news articles

- usedand a setafter fine-tuning for cryptocurrency news sentiment. Remarkably, analysis andthe classification. This section of 1000 crypto news articles is for this investigation. models demonstrated almost flawless prediction accuracy. Few-shot learning reveals research discoveries and post-fine-tuning insights from the authors' learning, concerning the effective maximum. Specifically, the fine-tuned

### 49 papers

- Previous Studies on Sentiment Analysis in Cryptocurrencies. Our literature review presents a comprehensive overview of 49 papers on the evolving role of sentiment analysis in understanding and predicting cryptocurrency market dynamics. The studies showcase a diverse array of methodologies, ranging from traditional sentiment analysis to cutting-edge deep learning models, that highlight the significant impact of sentiment-driven factors on cryptocurrency price movements and investor behavior

## Data analysis

- #method/time_series_analysis
- #method/bert_model
- #method/finbert_model
- #method/nlp_model
- #method/gpt_model

## Findings

- It is important to highlight that achieving an 82.9% accuracy rate in predictive modeling is quite high, indicating that the model can be confidently applied to <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment_Analysis" title="sentiment analysis">sentiment analysis</a> and classification tasks
- The fine-tuned <a class="keyword" href="https://en.wikipedia.org/wiki/GPT-4" title="GPT-4">GPT-4</a> model emerges as the top performer, boasting an impressive accuracy rate of 86.7%, closely followed by FinBERT with 84.3%, and <a class="keyword" href="https://en.wikipedia.org/wiki/bidirectional_encoder_representations_from_transformers" title="bidirectional encoder representations from transformers">BERT</a> with 83.3%
- <mark class="claim">The F1-score, striking a balance between precision and recall for each class, showcases the ft:gpt-4 model’s superior performance with the highest F1-score for class 1. The F1-score, striking a balance between precision and recall for each class, showcases its balanced precision and recall for that class</mark>
- In Figure 1, both the base and fine-tuned <a class="keyword" href="https://en.wikipedia.org/wiki/GPT-4" title="GPT-4">GPT-4</a> models demonstrate a ballabels, despite achieving 88% accuracy in predicting negative labels
- 88% accuracy in sentiment prediction unveils the research and insights gained by the authors concerning the to
- <mark class="fact">ADAMW optimizer led to a slight decrease in accuracy</mark>, <mark class="fact">around 3.2% lower compared to the ADAM optimizer</mark>
- It is imperative to highlight that even without fine-tuning, the <a class="keyword" href="https://en.wikipedia.org/wiki/GPT-4" title="GPT-4">GPT-4</a> base model achieved 82.9% accuracy

## Builds on previous research

- Our research findings confirm that both the LLMs and NLP models are highly accurate in their predictions, with the fine-tuned GPT demonstrating significantly higher performance compared to its base version and the BERT model. The complete codebase used in this study, including dataset cleaning classes, fine-tuning procedures, and datasets, is openly available in a GitHub repository under the MIT open-source license [^53].

## Contributions

- In summary, while each model displays strengths in specific metrics, it fine-tuned its balanced precision and recall for that class.

## Limitations

- The limitations of the study include the reliance on a specific dataset and the potential for bias in the sentiment analysis results. Additionally, the study highlights the need for further research on the use of NLP models in cryptocurrency markets.

## Future work

- The future work includes exploring the use of other NLP models and techniques, such as multimodal sentiment analysis and graph-based methods, for improved performance in sentiment analysis tasks. Additionally, the study highlights the need for further research on the application of NLP models in cryptocurrency markets, including the development of more robust and accurate models.
- The future work suggested by the study includes exploring the use of other LLMs and NLP models for sentiment analysis and classification, and evaluating their performance in different sectors and datasets. The study also suggests that further research is needed to improve the accuracy and robustness of sentiment analysis and classification models.

## References

[^1]: Huang, X.; Zhang, W.; Tang, X.; Zhang, M.; Surbiryala, J.; Iosifidis, V.; Liu, Z.; Zhang, J. LSTM-Based Sentiment Analysis for Cryptocurrency Prediction. In Lecture Notes in Computer Science; Springer: Berlin/Heidelberg, Germany, 2021; Volume 12683, pp. 617–621. [CrossRef]  [OA](https://scholar.google.co.uk/scholar?q=Huang%2C%20X.%20Zhang%2C%20W.%20Tang%2C%20X.%20Zhang%2C%20M.%20LSTM%20Based%20Sentiment%20Analysis%20for%20Cryptocurrency%20Prediction%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20X.%20Zhang%2C%20W.%20Tang%2C%20X.%20Zhang%2C%20M.%20LSTM%20Based%20Sentiment%20Analysis%20for%20Cryptocurrency%20Prediction%202021)

[^2]: Azmina, N.; Zamani, M.; Liew, J.; Yan, S.; Yusof, A.M. XLNET-GRU Sentiment Regression Model for Cryptocurrency News in English and Malay. ACl Anthol. 2022, 24, 36–42.  [OA](https://engine.scholarcy.com/oa_version?query=Azmina%2C%20N.%20Zamani%2C%20M.%20Liew%2C%20J.%20Yan%2C%20S.%20XLNET-GRU%20Sentiment%20Regression%20Model%20for%20Cryptocurrency%20News%20in%20English%20and%20Malay%202022&author=Azmina&title=XLNET-GRU%20Sentiment%20Regression%20Model%20for%20Cryptocurrency%20News%20in%20English%20and%20Malay&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Azmina%2C%20N.%20Zamani%2C%20M.%20Liew%2C%20J.%20Yan%2C%20S.%20XLNET-GRU%20Sentiment%20Regression%20Model%20for%20Cryptocurrency%20News%20in%20English%20and%20Malay%202022) [Scite](/scite_tallies?query=author%3AAzmina%2Ctitle%3AXLNET-GRU%20Sentiment%20Regression%20Model%20for%20Cryptocurrency%20News%20in%20English%20and%20Malay%2Cyear%3A2022)

[^3]: Sakas, D.P.; Giannakopoulos, N.T.; Margaritis, M.; Kanellos, N. Modeling Supply Chain Firms’ Stock Prices in the Fertilizer Industry through Innovative Cryptocurrency Market Big Data. Int. J. Financ. Stud. 2023, 11, 88. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Sakas%2C%20D.P.%20Giannakopoulos%2C%20N.T.%20Margaritis%2C%20M.%20Kanellos%2C%20N.%20Modeling%20Supply%20Chain%20Firms%E2%80%99%20Stock%20Prices%20in%20the%20Fertilizer%20Industry%20through%20Innovative%20Cryptocurrency%20Market%20Big%20Data%202023&author=Sakas&title=Modeling%20Supply%20Chain%20Firms%E2%80%99%20Stock%20Prices%20in%20the%20Fertilizer%20Industry%20through%20Innovative%20Cryptocurrency%20Market%20Big%20Data&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Sakas%2C%20D.P.%20Giannakopoulos%2C%20N.T.%20Margaritis%2C%20M.%20Kanellos%2C%20N.%20Modeling%20Supply%20Chain%20Firms%E2%80%99%20Stock%20Prices%20in%20the%20Fertilizer%20Industry%20through%20Innovative%20Cryptocurrency%20Market%20Big%20Data%202023) [Scite](/scite_tallies?query=author%3ASakas%2Ctitle%3AModeling%20Supply%20Chain%20Firms%E2%80%99%20Stock%20Prices%20in%20the%20Fertilizer%20Industry%20through%20Innovative%20Cryptocurrency%20Market%20Big%20Data%2Cyear%3A2023)

[^53]: GitHub—Kroumeliotis/LLM-and-NLP-Models-in-Cryptocurrency-Sentiment-Analysis: Crypto. Available online: <https://github.com/kroumeliotis/LLM-and-NLP-models-in-Cryptocurrency-Sentiment-Analysis> (accessed on 12 April 2024).  [OA](https://github.com/kroumeliotis/LLM-and-NLP-models-in-Cryptocurrency-Sentiment-Analysis)  
