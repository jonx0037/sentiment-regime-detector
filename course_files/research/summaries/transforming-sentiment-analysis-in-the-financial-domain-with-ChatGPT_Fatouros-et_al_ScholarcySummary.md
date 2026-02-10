[[Fatouros_et+al_TransformingSentimentAnalysisFinancialDomain_2023]]

# [Transforming sentiment analysis in the financial domain with ChatGPT](https://doi.org/10.1016/j.mlwa.2023.100508)

## [[Georgios Fatouros]]; [[John Soldatos]]; [[Kalliopi Kouroumali]] et al

## Abstract

Financial sentiment analysis plays a crucial role in decoding market trends and guiding strategic trading decisions. Despite the deployment of advanced deep learning techniques and language models to refine sentiment analysis in finance, this study breaks new ground by investigating the potential of large language models, particularly ChatGPT 3.5, in financial sentiment analysis, with a strong emphasis on the foreign exchange market (forex). Using a zero-shot prompting approach, we examine multiple ChatGPT prompts on a meticulously curated dataset of forex-related news headlines and measure performance using metrics such as precision, recall, F1-score, and Mean Absolute Error (MAE) for the sentiment class. Additionally, we probe the correlation between predicted sentiment and market returns as an additional evaluation approach. ChatGPT, compared to FinBERT, a well-established sentiment analysis model for financial texts, exhibited approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns. By highlighting the importance of prompt engineering, particularly in zero-shot settings, this study underscores ChatGPT’s potential to substantially improve sentiment analysis in financial applications. By sharing the dataset used, we aim to stimulate further research and advancements in the field of financial services.

## Key concepts

# finding/ChatGPT; #ChatGPT; #language_model; #large_language_models; #sentiment_analysis; #artificial_intelligence; #claim/metrics; #metrics; #generative_pre_trained_transformers

## Quote
>
> This study explores the potential of large language models, particularly ChatGPT 3.5, in financial sentiment analysis, with a strong emphasis on the foreign exchange market, and finds that ChatGPT exhibits approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns compared to FinBERT.

## Key points

- We leverage a zero-shot prompting strategy, which assesses ChatGPT’s proficiency in interpreting forex-related financial text and emphasizes its ability to achieve this without domain-specific fine-tuning
- We present a comprehensive discussion of these results, comparing the performance of the various ChatGPT prompts and the established baseline, FinBERT, across various metrics
- While these results provide a promising outlook for the application of ChatGPT in financial sentiment analysis, they suggest areas for further investigation
- The superior understanding of overall market sentiment exhibited by promptly processing all daily news at once opens a pathway for future research exploring the integration of additional types of relevant financial data within the prompt
- Our work contributes to a burgeoning field, offering a comprehensive evaluation of ChatGPT’s application in financial sentiment analysis and demonstrating its potential as a valuable tool in the realm of finance
- We hope that our findings and the released dataset will serve as a springboard for further advancements in this domain

## Summary

### Introduction To Sentiment Analysis

Financial sentiment analysis plays a crucial role in decoding market trends and guiding strategic trading decisions.
Despite advancements in deep learning techniques and language models, conventional sentiment analysis tools often fail to infer the text's subject and lack the ability to adjust their output based on specific use-case context.
The financial services sector has been an early adopter of technological advancements, continually evolving to meet the demands of a rapidly changing global landscape.

### ChatGPT And Financial Sentiment Analysis

ChatGPT, a state-of-the-art language model developed by OpenAI, has demonstrated significant potential in revolutionizing multiple domains, including the financial sector.
The study pioneers the exploration of ChatGPT 3.5’s capabilities in discerning nuanced sentiment cues in forex news, leveraging a zero-shot prompting strategy.
ChatGPT achieved approximately 35% higher sentiment classification performance and a 36% higher correlation with market returns than FinBERT, a well-established sentiment analysis model for financial texts.

### Applications And Future Research

The study highlights the importance of prompt engineering, especially in zero-shot settings, to optimize performance and enhance the efficacy of sentiment analysis.
The curated dataset and annotations, made publicly available, serve as a useful resource for future research endeavors in this domain.
The potential applications of ChatGPT in financial services, including risk analysis via sentiment analysis, are significant, and the study offers valuable insights to help developers and researchers effectively harness the model’s capabilities.

### Background

Recent studies have highlighted the potential of large language models (LMs) in financial sentiment analysis.
FinBERT has been shown to be robust in financial sentiment analysis, outperforming keyword-based methods.
However, current models have limitations, such as the need to comprehend domain-specific jargon and disentangle subtle sentiments associated with multiple financial instruments.

### LLMs

The advent of LLMs like GPT offers promising potential for financial sentiment analysis.
Models like BloombergGPT and Google's Bard have shown excellent performance in financial NLP tasks.
However, these models have limitations, such as the lack of an open API or the need for specialized knowledge and computational resources.
ChatGPT, on the other hand, has an open API and has been shown to have considerable potential and practical utility.

### Methodology

The study collected news headlines relevant to key forex pairs and manually annotated each headline for sentiment.
The dataset was used to evaluate ChatGPT's performance in financial sentiment analysis.
The study used a custom service to collect data from reputable platforms and stored it in a database.
The data was then processed to extract necessary details, and the headlines were annotated for sentiment.
The study used three annotation categories: 'positive', 'negative', and 'neutral', corresponding to bullish, bearish, and hold sentiments, respectively.
The dataset was made publicly accessible to contribute to the research community and foster transparency in the methodology.

### Sentiment Analysis

The FinBERT model outputs a set of probabilities for each sentiment class, which are used to determine the predicted class and a sentiment score.
ChatGPT is also used for sentiment analysis, with the goal of exploring its potential in financial sentiment analysis.
ChatGPT's ability to comprehend not only the literal meanings of words but also their underlying implications, idioms, and sentiments is expected to be beneficial for this task.

### Evaluation Metrics

The evaluation approach for sentiment classification is twofold, encompassing both a traditional evaluation grounded in comparison with the true sentiment class and a market-related model evaluation.
The traditional evaluation uses metrics such as accuracy, precision, recall, and F1-score, while the market-related evaluation uses metrics such as Sentiment Mean Absolute Error (S-MAE) and Directional Accuracy (DA).

### Model Performance

The performance of ChatGPT under varying prompts (P1-P4) is compared with that of the FinBERT model.
The evaluation includes a comparative analysis of different models to highlight the impact of prompt selection on ChatGPT's performance.
The results are expected to provide a comprehensive understanding of ChatGPT's effectiveness in financial sentiment analysis.
The GPT models consistently outperform FinBERT in sentiment classification tasks, with GPT-P2 and GPT-P4 achieving the highest accuracy, recall, and F1-score.
GPT-P4 exhibits the highest precision and F1-score for the Positive sentiment class, while GPT-P2 dominates in recall and F1-score for the Negative sentiment class.
The performance of GPT models varies by forex pair, with GPT-P2 and GPT-P4 showing superior performance on some pairs.

### Sentiment Score Relation

The models' sentiment scores are correlated with market price movements, with GPT-P4 exhibiting the highest correlation with true sentiment.
The correlation between sentiment scores and market returns is measured using the Pearson correlation coefficient, with GPT-P4 showing a stronger correlation than the true sentiment.
The models that generate sentiment scores ranging from -1 to 1 exhibit a more fitting alignment with market movements.

### Directional Accuracy

The GPT models exhibit high directional accuracy (DA) in predicting market direction from sentiment scores, with GPT-P1N achieving the highest DA of 67.2%.
Numerical models tend to have higher DA than their categorical counterparts, and GPT models perform nearly as well as human-annotated sentiment.
The DA of the models varies across different forex pairs, with GPT-P4AN emerging as the top performer for the AUDUSD pair and GPT-P6N outperforming its counterparts for the EURUSD and GBPUSD pairs.

### Performance

The study evaluates ChatGPT's performance in financial sentiment analysis, focusing on processing time and token consumption.
The results show that prompts P1, P2, and P3 exhibit similar average time and token counts, whereas P4 generates more tokens, potentially leading to higher costs.
P5 and P6, despite generating more tokens, benefit from processing multiple headlines at once, resulting in lower average times and tokens per headline.

### Applications

The study highlights the potential applications of ChatGPT in financial services, including predicting market trends and providing actionable insights.
The results suggest that strategic prompt selection is crucial, and the choice of an ideal prompt may vary depending on the specific use case and financial instrument.
The study also notes that sentiment analysis using language models like ChatGPT should be integrated into a more holistic approach to financial market analysis.

### Limitations

The study acknowledges several limitations, including the dataset's limited duration and the potential for model collapse.
The results show that the models did not fully align with market movements, indicating that sentiment explains only part of the variation in market prices.
The study suggests that future research should focus on validating and generalizing the findings, integrating additional relevant financial data, and evaluating the performance of newer models such as GPT-4.

### Acknowledgments

The project was funded by the Union under grant agreement no 101092639.
The authors express their gratitude to the FAME partners, JRC Capital Management Consultancy Research GmbH, and KMcube Asset Management SA, for their contributions and expertise in data labeling.

### Feedback

The authors appreciate the anonymous reviewers for their constructive feedback, which enhanced the manuscript's quality.

### Funding

The grant agreement number for the Union's funding of Project FAME is 101092639.

## Study subjects

### 461 articles with an average of 5

- The total number of articles collected for each pair ranges from 55 for EURCHF to 758 for EURUSD. Specifically, AUDUSD has 461 articles, averaging 5.36 per day; GBPUSD has 518 articles, averaging 6.02 per day; and USDJPY has 499 articles, averaging 5.8 per day. The daily average articles vary for each pair, with EURUSD having the highest daily average of 8.81 articles and EURCHF recording the lowest with 0.64 articles per day

### 5000 articles

- Taking into account that the cost of utilizing the OpenAI API for the ChatGPT-3.5 model is 0.002 USD per 1 K tokens, the financial implications of integrating ChatGPT into existing services seem relatively low, especially considering the volume of data processed daily. As a reference, Bloomberg News produces approximately 5000 articles on a daily basis ([^Bloomberg_2023_a]). To illustrate, let us consider using the P6N model, which generates the highest number of tokens among the models tested in this study

## Data analysis

- #method/pearson_correlation_coefficient
- #method/pearson_correlation
- #method/finbert_model

## Findings

- <a class="keyword" href="https://en.wikipedia.org/wiki/ChatGPT" title="ChatGPT">ChatGPT</a>, compared to FinBERT, a well-established <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment_analysis" title="sentiment analysis">sentiment analysis</a> model for financial texts, exhibited approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns

## Builds on previous research

- This method recognizes the currency market’s acute sensitivity to economic news, which significantly influences many trading strategies ([^Evans_2005_a]). Instead of solely focusing on the textual content, we ascertained sentiment based on the potential short-term impact of the headline on its corresponding forex pair.
- As the landscape of LLMs continues to evolve with remarkable speed, it is imperative that future research delves into the comparison and assessment of the unique capabilities of both existing and emerging models. For instance, newer models such as GPT-4 ([^Openai_2023_a]) could enhance ChatGPT's performance in our study.

## Contributions

- In conclusion, <mark class="fact">our work contributes to a burgeoning field</mark>, offering a comprehensive evaluation of ChatGPT’s application in financial sentiment analysis, and demonstrating its potential as a valuable tool in the realm of finance. <mark class="fact">We hope that our findings</mark> and <mark class="fact">the released dataset will serve as a springboard for further advancements</mark> in this domain. The exploration and refinement of LLMs in financial services is still in its early stages, and there is much more terrain to uncover.

## Future work

- The study suggests that future research could explore the integration of additional types of relevant financial data within the prompt, and that more refined and robust models, such as GPT4, could further enhance the performance of financial sentiment analysis.
- The study suggests areas for further investigation, including the integration of additional types of relevant financial data within the prompt and the evaluation of open-source LLMs like BLOOM.

## References

[^Bloomberg_2023_a]: Bloomberg (2023). Bloomberg media distribution. URL <https://www.bloomberg.com/distribution/products/news/.accessed:May> 26, 2023.  [OA](https://www.bloomberg.com/distribution/products/news/.accessed:May)  

[^Evans_2005_a]: Evans, M. D., &amp; Lyons, R. K. (2005). Do currency markets absorb news quickly? Journal of International Money and Finance, 24, 197–217.  [OA](https://engine.scholarcy.com/oa_version?query=Evans%2C%20M.D.%20Lyons%2C%20R.K.%20Do%20currency%20markets%20absorb%20news%20quickly%3F%202005&author=Evans&title=Do%20currency%20markets%20absorb%20news%20quickly%3F&year=2005) [GScholar](https://scholar.google.co.uk/scholar?q=Evans%2C%20M.D.%20Lyons%2C%20R.K.%20Do%20currency%20markets%20absorb%20news%20quickly%3F%202005) [Scite](/scite_tallies?query=author%3AEvans%2Ctitle%3ADo%20currency%20markets%20absorb%20news%20quickly%3F%2Cyear%3A2005)

[^Openai_2023_a]: OpenAI (2023). GPT-4 Technical Report. arXiv:2303.08774.  [OA](https://arxiv.org/abs/2303.08774)  
