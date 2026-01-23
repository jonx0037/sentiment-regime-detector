[[Fatouros_et+al_TransformingSentimentAnalysisFinancialDomain_2023]]

# [Transforming sentiment analysis in the financial domain with ChatGPT](https://doi.org/10.1016/j.mlwa.2023.100508)

## [[Georgios Fatouros]]; [[John Soldatos]]; [[Kalliopi Kouroumali]] et al.

## Abstract
Financial sentiment analysis plays a crucial role in decoding market trends and guiding strategic trading decisions. Despite the deployment of advanced deep learning techniques and language models to refine sentiment analysis in finance, this study breaks new ground by investigating the potential of large language models, particularly ChatGPT 3.5, in financial sentiment analysis, with a strong emphasis on the foreign exchange market (forex). ==Employing a zero-shot prompting approach, we examine multiple ChatGPT prompts on a meticulously curated dataset of forex-related news headlines, measuring performance using metrics such as precision, recall, f1-score, and Mean Absolute Error (MAE) of the sentiment class==. Additionally, we probe the correlation between predicted sentiment and market returns as an addition evaluation approach. ChatGPT, compared to FinBERT, a well-established sentiment analysis model for financial texts, exhibited approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns. By underlining the significance of prompt engineering, particularly in zero-shot contexts, this study spotlights ChatGPT’s potential to substantially boost sentiment analysis in financial applications. By sharing the utilized dataset, our intention is to stimulate further research and advancements in the field of financial services.

## Key concepts
#finding/ChatGPT; #ChatGPT; #language_model; #large_language_models; #sentiment_analysis; #artificial_intelligence; #claim/metrics; #metrics; #generative_pre_trained_transformers

## Quote
> This study explores the potential of large language models, particularly ChatGPT 3.5, in financial sentiment analysis, with a strong emphasis on the foreign exchange market, and finds that ChatGPT exhibits approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns compared to FinBERT.

## Key points
- We leverage a zero-shot prompting strategy, which assesses ChatGPT’s proficiency in interpreting forex-related financial text and emphasizes its ability to achieve this without domain-specific fine-tuning
- We present a comprehensive discussion of these results, comparing the performance of the various ChatGPT prompts and the established baseline, FinBERT, across various metrics
- While these results provide a promising outlook for the application of ChatGPT in financial sentiment analysis, they suggest areas for further investigation
- The superior understanding of overall market sentiment exhibited by prompts processing all daily news at once opens a pathway for future research exploring the integration of additional types of relevant financial data within the prompt
- Our work contributes to a burgeoning field, offering a comprehensive evaluation of ChatGPT’s application in financial sentiment analysis, and demonstrating its potential as a valuable tool in the realm of finance
- We hope that our findings and the released dataset will serve as a springboard for further advancements in this domain


## Summary

### Introduction To Sentiment Analysis
Financial sentiment analysis plays a crucial role in decoding market trends and guiding strategic trading decisions.
Despite advancements in deep learning techniques and language models, conventional sentiment analysis tools often fail to infer the subject of the text and lack the ability to adjust their output based on specific use-case context.
The financial services sector has been an early adopter of technological advancements, continually evolving to meet the demands of a rapidly changing global landscape.

### ChatGPT And Financial Sentiment Analysis
ChatGPT, a state-of-the-art language model developed by OpenAI, has demonstrated significant potential in revolutionizing multiple domains, including the financial sector.
The study pioneers the exploration of ChatGPT 3.5’s capabilities in discerning nuanced sentiment cues in forex news, leveraging a zero-shot prompting strategy.
ChatGPT exhibited approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns compared to FinBERT, a well-established sentiment analysis model for financial texts.

### Applications And Future Research
The study highlights the importance of prompt engineering, especially in zero-shot contexts, to optimize performance and enhance sentiment analysis efficacy.
The curated dataset and annotations, made publicly available, serve as a useful resource for future research endeavors in this domain.
The potential applications of ChatGPT in financial services, including risk analysis through sentiment analysis, are significant, and the study offers valuable insights that can guide developers and researchers in harnessing the model’s potential effectively.

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
The dataset was used to evaluate the performance of ChatGPT in financial sentiment analysis.
The study used a custom service to collect data from reputable platforms and stored it in a database.
The data was then processed to extract necessary details, and the headlines were annotated for sentiment.
The study used three categories for annotation: 'positive', 'negative', and 'neutral', which correspond to bullish, bearish, and hold sentiments respectively.
The dataset was made publicly accessible to contribute to the research community and foster transparency in the methodology.

### Sentiment Analysis
The FinBERT model outputs a set of probabilities for each sentiment class, which are used to determine the predicted class and a sentiment score.
ChatGPT is also used for sentiment analysis, with the goal of exploring its potential in financial sentiment analysis.
ChatGPT's ability to comprehend not only the literal meanings of words but also the underlying implications, idioms, or sentiments is expected to be beneficial in this task.

### Evaluation Metrics
The evaluation approach for sentiment classification is twofold, encompassing both a traditional evaluation grounded in comparison with the true sentiment class and a market-related model evaluation.
The traditional evaluation uses metrics such as accuracy, precision, recall, and F1-score, while the market-related evaluation uses metrics such as Sentiment Mean Absolute Error (S-MAE) and Directional Accuracy (DA).

### Model Performance
The performance of ChatGPT under varying prompts (P1-P4) is compared with that of the FinBERT model.
The evaluation includes a comparative analysis among different models, with the goal of highlighting the impact of prompt selection on the performance of ChatGPT.
The results are expected to provide a comprehensive understanding of the effectiveness of ChatGPT in financial sentiment analysis.
The GPT models consistently outperform FinBERT in sentiment classification tasks, with GPT-P2 and GPT-P4 achieving the highest accuracy, recall, and F1-score.
GPT-P4 exhibits the highest precision and F1-score for the Positive sentiment class, while GPT-P2 dominates in recall and F1-score for the Negative sentiment class.
The performance of the GPT models varies depending on the specific forex pair, with GPT-P2 and GPT-P4 showing superior performance for certain pairs.

### Sentiment Score Relation
The sentiment scores predicted by the models are correlated with market price movements, with GPT-P4 exhibiting the highest correlation with true sentiment.
The correlation between sentiment scores and market returns is measured using the Pearson correlation coefficient, with GPT-P4 showing a higher correlation than the true sentiment itself.
The models that generate sentiment scores ranging from -1 to 1 exhibit a more fitting alignment with market movements.

### Directional Accuracy
The GPT models exhibit high directional accuracy (DA) in predicting the correct direction of market movement based on sentiment scores, with GPT-P1N achieving the highest DA at 67.2%.
The numerical models tend to have a higher DA than their categorical counterparts, and the GPT models perform nearly on par with human-annotated sentiment.
The DA of the models varies across different forex pairs, with GPT-P4AN emerging as the top performer for the AUDUSD pair and GPT-P6N outperforming its counterparts for the EURUSD and GBPUSD pairs.

### Performance
The study evaluates the performance of ChatGPT in financial sentiment analysis, with a focus on processing time and token consumption.
The results show that prompts P1, P2, and P3 exhibit similar average times and tokens, while P4 generates more tokens, potentially leading to higher costs.
P5 and P6, despite generating more tokens, benefit from processing multiple headlines at once, resulting in lower average times and tokens per headline.

### Applications
The study highlights the potential applications of ChatGPT in financial services, including predicting market trends and providing actionable insights.
The results suggest that strategic prompt selection is crucial, and the choice of ideal prompt may vary depending on the specific use case and financial instrument.
The study also notes that sentiment analysis using language models like ChatGPT should be integrated into a more holistic approach to financial market analysis.

### Limitations
The study acknowledges several limitations, including the duration of the dataset and the potential for model collapse.
The results show that the models did not entirely align with market movements, indicating that sentiment only explains a part of the variations in market prices.
The study suggests that future research should focus on validating and generalizing the findings, exploring the integration of additional types of relevant financial data, and evaluating the performance of newer models like GPT-4.

### Acknowledgments
The project was funded by the Union under grant agreement no 101092639.
The authors express gratitude to FAME partners, JRC Capital Management Consultancy Research GmbH and KMcube Asset Management SA, for their contributions and expertise in data labeling.

### Feedback
The authors appreciate the anonymous reviewers for their constructive feedback, which enhanced the manuscript's quality.

### Funding
The grant agreement number for the Union's funding of Project FAME is 101092639.


## Study subjects

### 461 articles with an average of 5
- The total number of articles collected for each pair ranges from 55 for EURCHF to 758 for EURUSD. ==Specifically, AUDUSD has 461 articles with an average of 5.36 articles daily, GBPUSD comprises 518 articles averaging 6.02 daily, and USDJPY includes 499 articles with a daily average of 5.8==. The daily average articles vary for each pair, with EURUSD having the highest daily average of 8.81 articles and EURCHF recording the lowest with 0.64 articles per day

### 5000 articles
- Taking into account that the cost of utilizing the OpenAI API for the ChatGPT-3.5 model is 0.002 USD per 1 K tokens, the financial implications of integrating ChatGPT into existing services seem relatively low, especially considering the volume of data processed daily. ==As a reference, Bloomberg News produces approximately 5000 articles on a daily basis ([^Bloomberg_2023_a])==. To illustrate, let us consider using the P6N model, which generates the highest number of tokens among the models tested in this study

## Data analysis
- #method/pearson_correlation_coefficient
- #method/pearson_correlation
- #method/finbert_model

## Findings
- <a class="keyword" href="https://en.wikipedia.org/wiki/ChatGPT" title="ChatGPT">ChatGPT</a>, compared to FinBERT, a well-established <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment_analysis" title="sentiment analysis">sentiment analysis</a> model for financial texts, exhibited approximately 35% enhanced performance in sentiment classification and a 36% higher correlation with market returns

##  Builds on previous research
- This method recognizes the currency market’s acute sensitivity to economic news, which significantly influences many trading strategies ([^Evans_2005_a]). Instead of solely focusing on the textual content, ==we ascertained sentiment based on the potential short-term impact of the headline on its corresponding forex pair==. .
- As the landscape of LLMs continues to evolve with remarkable speed, it is imperative that future research delves into the comparison and assessment of the unique capabilities of both existing and emerging models. ==For instance, newer models such as GPT-4 ([^Openai_2023_a]) hold potential to enhance the performance exhibited by ChatGPT in our study==.

## Contributions
- In conclusion, <mark class="fact">our work contributes to a burgeoning field</mark>, offering a comprehensive evaluation of ChatGPT’s application in financial sentiment analysis, and demonstrating its potential as a valuable tool in the realm of finance. <mark class="fact">We hope that our findings</mark> and <mark class="fact">the released dataset will serve as a springboard for further advancements</mark> in this domain. The exploration and refinement of LLMs in financial services is still in its early stages, and there is much more terrain to uncover.

## Future work
- The study suggests that future research could explore the integration of additional types of relevant financial data within the prompt, and that more refined and robust models such as GPT4 could further enhance the performance of financial sentiment analysis.
- The study suggests areas for further investigation, including the integration of additional types of relevant financial data within the prompt, and the evaluation of open-source LLMs like BLOOM.


## References
[^Arner_et+al_2015_a]: Arner, D. W., Barberis, J., &amp; Buckley, R. P. (2015). The evolution of fintech: A new post-crisis paradigm. Geological Journal of the International’l Letters, 47, 1271.  [OA](https://engine.scholarcy.com/oa_version?query=Arner%2C%20D.W.%20Barberis%2C%20J.%20Buckley%2C%20R.P.%20The%20evolution%20of%20fintech%3A%20A%20new%20post-crisis%20paradigm%202015&author=Arner&title=The%20evolution%20of%20fintech%3A%20A%20new%20post-crisis%20paradigm&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Arner%2C%20D.W.%20Barberis%2C%20J.%20Buckley%2C%20R.P.%20The%20evolution%20of%20fintech%3A%20A%20new%20post-crisis%20paradigm%202015) [Scite](/scite_tallies?query=author%3AArner%2Ctitle%3AThe%20evolution%20of%20fintech%3A%20A%20new%20post-crisis%20paradigm%2Cyear%3A2015)

[^Baker_2007_a]: Baker, M., &amp; Wurgler, J. (2007). Investor sentiment in the stock market. Journal of Economic Perspectives, 21, 129–151.  [OA](https://engine.scholarcy.com/oa_version?query=Baker%2C%20M.%20Wurgler%2C%20J.%20Investor%20sentiment%20in%20the%20stock%20market%202007&author=Baker&title=Investor%20sentiment%20in%20the%20stock%20market&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Baker%2C%20M.%20Wurgler%2C%20J.%20Investor%20sentiment%20in%20the%20stock%20market%202007) [Scite](/scite_tallies?query=author%3ABaker%2Ctitle%3AInvestor%20sentiment%20in%20the%20stock%20market%2Cyear%3A2007)

[^Bing_2012_a]: Bing, L. (2012). synthesis lectures on human language technologies, Sentiment analysis and opinion mining. Chicago, IL, USA: University of Illinois.  [OA](https://scholar.google.co.uk/scholar?q=Bing%2C%20L.%20synthesis%20lectures%20on%20human%20language%20technologies%2C%20Sentiment%20analysis%20and%20opinion%20mining%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Bing%2C%20L.%20synthesis%20lectures%20on%20human%20language%20technologies%2C%20Sentiment%20analysis%20and%20opinion%20mining%202012) 

[^Blaskowitz_2011_a]: Blaskowitz, O., &amp; Herwartz, H. (2011). On economic evaluation of directional forecasts. International Journal of Forecasting, 27, 1058–1065.  [OA](https://engine.scholarcy.com/oa_version?query=Blaskowitz%2C%20O.%20Herwartz%2C%20H.%20On%20economic%20evaluation%20of%20directional%20forecasts%202011&author=Blaskowitz&title=On%20economic%20evaluation%20of%20directional%20forecasts&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Blaskowitz%2C%20O.%20Herwartz%2C%20H.%20On%20economic%20evaluation%20of%20directional%20forecasts%202011) [Scite](/scite_tallies?query=author%3ABlaskowitz%2Ctitle%3AOn%20economic%20evaluation%20of%20directional%20forecasts%2Cyear%3A2011)

[^Bloomberg_2023_a]: Bloomberg (2023). Bloomberg media distribution. URL https://www.bloomberg.com/distribution/products/news/.accessed:May 26, 2023.  [OA](https://www.bloomberg.com/distribution/products/news/.accessed:May)  

[^Bollen_et+al_2011_a]: Bollen, J., Mao, H., &amp; Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2, 1–8.  [OA](https://engine.scholarcy.com/oa_version?query=Bollen%2C%20J.%20Mao%2C%20H.%20Zeng%2C%20X.%20Twitter%20mood%20predicts%20the%20stock%20market%202011&author=Bollen&title=Twitter%20mood%20predicts%20the%20stock%20market&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Bollen%2C%20J.%20Mao%2C%20H.%20Zeng%2C%20X.%20Twitter%20mood%20predicts%20the%20stock%20market%202011) [Scite](/scite_tallies?query=author%3ABollen%2Ctitle%3ATwitter%20mood%20predicts%20the%20stock%20market%2Cyear%3A2011)

[^Brock_et+al_2018_a]: Brock, A., Donahue, J., &amp; Simonyan, K. (2018). Large scale gan training for high fidelity natural image synthesis. arXiv preprint arXiv:1809.11096.  [OA](https://arxiv.org/abs/1809.11096)  

[^Brown_et+al_2020_a]: Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., et al. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877–1901.  [OA](https://engine.scholarcy.com/oa_version?query=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020&author=Brown&title=Language%20models%20are%20few-shot%20learners&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020) [Scite](/scite_tallies?query=author%3ABrown%2Ctitle%3ALanguage%20models%20are%20few-shot%20learners%2Cyear%3A2020)

[^Chen_et+al_2014_a]: Chen, H., De, P., Hu, Y. J., &amp; Hwang, B. H. (2014). Wisdom of crowds: The value of stock opinions transmitted through social media. The Review of Financial Studies, 27, 1367–1403.  [OA](https://engine.scholarcy.com/oa_version?query=Chen%2C%20H.%20De%2C%20P.%20Hu%2C%20Y.J.%20Hwang%2C%20B.H.%20Wisdom%20of%20crowds%3A%20The%20value%20of%20stock%20opinions%20transmitted%20through%20social%20media%202014&author=Chen&title=Wisdom%20of%20crowds%3A%20The%20value%20of%20stock%20opinions%20transmitted%20through%20social%20media&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%2C%20H.%20De%2C%20P.%20Hu%2C%20Y.J.%20Hwang%2C%20B.H.%20Wisdom%20of%20crowds%3A%20The%20value%20of%20stock%20opinions%20transmitted%20through%20social%20media%202014) [Scite](/scite_tallies?query=author%3AChen%2Ctitle%3AWisdom%20of%20crowds%3A%20The%20value%20of%20stock%20opinions%20transmitted%20through%20social%20media%2Cyear%3A2014)

[^Chen_et+al_2018_a]: Chen, C., Fengler, M. R., &amp; Härdle, Y. (2018). Textual sentiment, option characteristics, and stock return predictability.  [OA](https://scholar.google.co.uk/scholar?q=Chen%2C%20C.%20Fengler%2C%20M.R.%20H%C3%A4rdle%2C%20Y.%20Textual%20sentiment%2C%20option%20characteristics%2C%20and%20stock%20return%20predictability%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%2C%20C.%20Fengler%2C%20M.R.%20H%C3%A4rdle%2C%20Y.%20Textual%20sentiment%2C%20option%20characteristics%2C%20and%20stock%20return%20predictability%202018) 

[^Dakhel_et+al_2023_a]: Dakhel, A. M., Majdinasab, V., Nikanjam, A., Khomh, F., Desmarais, M. C., &amp; Jiang, Z. M. (2023). Github copilot ai pair programmer: Asset or liability? Journal of Systems and Software, Article 111734.  [OA](https://engine.scholarcy.com/oa_version?query=Dakhel%2C%20A.M.%20Majdinasab%2C%20V.%20Nikanjam%2C%20A.%20Khomh%2C%20F.%20Github%20copilot%20ai%20pair%20programmer%3A%20Asset%20or%20liability%3F%202023&author=Dakhel&title=Github%20copilot%20ai%20pair%20programmer%3A%20Asset%20or%20liability%3F&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Dakhel%2C%20A.M.%20Majdinasab%2C%20V.%20Nikanjam%2C%20A.%20Khomh%2C%20F.%20Github%20copilot%20ai%20pair%20programmer%3A%20Asset%20or%20liability%3F%202023) [Scite](/scite_tallies?query=author%3ADakhel%2Ctitle%3AGithub%20copilot%20ai%20pair%20programmer%3A%20Asset%20or%20liability%3F%2Cyear%3A2023)

[^Devlin_et+al_2018_a]: Devlin, J., Chang, M. W., Lee, K., &amp; Toutanova, K. (2018). Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv: 1810.04805.  [OA](https://arxiv.org/abs/1810.04805)  

[^Evans_2005_a]: Evans, M. D., &amp; Lyons, R. K. (2005). Do currency markets absorb news quickly? Journal of International Money and Finance, 24, 197–217.  [OA](https://engine.scholarcy.com/oa_version?query=Evans%2C%20M.D.%20Lyons%2C%20R.K.%20Do%20currency%20markets%20absorb%20news%20quickly%3F%202005&author=Evans&title=Do%20currency%20markets%20absorb%20news%20quickly%3F&year=2005) [GScholar](https://scholar.google.co.uk/scholar?q=Evans%2C%20M.D.%20Lyons%2C%20R.K.%20Do%20currency%20markets%20absorb%20news%20quickly%3F%202005) [Scite](/scite_tallies?query=author%3AEvans%2Ctitle%3ADo%20currency%20markets%20absorb%20news%20quickly%3F%2Cyear%3A2005)

[^Farimani_et+al_2022_a]: Farimani, S. A., Jahan, M. V., Fard, A. M., &amp; Tabbakh, S. R. K. (2022). Investigating the informativeness of technical indicators and news sentiment in financial market price prediction. Knowledge-Based Systems, 247, Article 108742.  [OA](https://engine.scholarcy.com/oa_version?query=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Tabbakh%2C%20S.R.K.%20Investigating%20the%20informativeness%20of%20technical%20indicators%20and%20news%20sentiment%20in%20financial%20market%20price%20prediction%202022&author=Farimani&title=Investigating%20the%20informativeness%20of%20technical%20indicators%20and%20news%20sentiment%20in%20financial%20market%20price%20prediction&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Farimani%2C%20S.A.%20Jahan%2C%20M.V.%20Fard%2C%20A.M.%20Tabbakh%2C%20S.R.K.%20Investigating%20the%20informativeness%20of%20technical%20indicators%20and%20news%20sentiment%20in%20financial%20market%20price%20prediction%202022) [Scite](/scite_tallies?query=author%3AFarimani%2Ctitle%3AInvestigating%20the%20informativeness%20of%20technical%20indicators%20and%20news%20sentiment%20in%20financial%20market%20price%20prediction%2Cyear%3A2022)

[^Fatouros_2023_a]: Fatouros, G., &amp; Kouroumali, K. (2023). Forex news annotated dataset for sentiment analysis. http://dx.doi.org/10.5281/zenodo.7976208, [Data set].  [OA](https://doi.org/10.5281/zenodo.7976208)  [Scite](/scite_tallies?query=https://doi.org/10.5281/zenodo.7976208)

[^Fatouros_et+al_2023_b]: Fatouros, G., Makridis, G., Kotios, D., Soldatos, J., Filippakis, M., &amp; Kyriazis, D. (2023). Deepvar: a framework for portfolio risk assessment leveraging probabilistic deep neural networks. Digital Finance, 5, 29–56.  [OA](https://engine.scholarcy.com/oa_version?query=Fatouros%2C%20G.%20Makridis%2C%20G.%20Kotios%2C%20D.%20Soldatos%2C%20J.%20Deepvar%3A%20a%20framework%20for%20portfolio%20risk%20assessment%20leveraging%20probabilistic%20deep%20neural%20networks%202023&author=Fatouros&title=Deepvar%3A%20a%20framework%20for%20portfolio%20risk%20assessment%20leveraging%20probabilistic%20deep%20neural%20networks&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Fatouros%2C%20G.%20Makridis%2C%20G.%20Kotios%2C%20D.%20Soldatos%2C%20J.%20Deepvar%3A%20a%20framework%20for%20portfolio%20risk%20assessment%20leveraging%20probabilistic%20deep%20neural%20networks%202023) [Scite](/scite_tallies?query=author%3AFatouros%2Ctitle%3ADeepvar%3A%20a%20framework%20for%20portfolio%20risk%20assessment%20leveraging%20probabilistic%20deep%20neural%20networks%2Cyear%3A2023)

[^George_2023_a]: George, A. S., &amp; George, A. H. (2023). A review of chatgpt ai’s impact on several business sectors. Partners Universal International Innovation Journal, 1, 9–23.  [OA](https://engine.scholarcy.com/oa_version?query=George%2C%20A.S.%20George%2C%20A.H.%20A%20review%20of%20chatgpt%20ai%E2%80%99s%20impact%20on%20several%20business%20sectors%202023&author=George&title=A%20review%20of%20chatgpt%20ai%E2%80%99s%20impact%20on%20several%20business%20sectors&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=George%2C%20A.S.%20George%2C%20A.H.%20A%20review%20of%20chatgpt%20ai%E2%80%99s%20impact%20on%20several%20business%20sectors%202023) [Scite](/scite_tallies?query=author%3AGeorge%2Ctitle%3AA%20review%20of%20chatgpt%20ai%E2%80%99s%20impact%20on%20several%20business%20sectors%2Cyear%3A2023)

[^Goodfellow_et+al_2014_a]: Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., et al. (2014). Generative adversarial nets. Advances in Neural Information Processing Systems, 27.  [OA](https://scholar.google.co.uk/scholar?q=Goodfellow%2C%20I.%20Pouget-Abadie%2C%20J.%20Mirza%2C%20M.%20Xu%2C%20B.%20Generative%20adversarial%20nets%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Goodfellow%2C%20I.%20Pouget-Abadie%2C%20J.%20Mirza%2C%20M.%20Xu%2C%20B.%20Generative%20adversarial%20nets%202014) 

[^Hossin_2015_a]: Hossin, M., &amp; Sulaiman, M. N. (2015). A review on evaluation metrics for data classification evaluations. International Journal of Data Mining &amp; Knowledge Management Process, 5, 1.  [OA](https://engine.scholarcy.com/oa_version?query=Hossin%2C%20M.%20Sulaiman%2C%20M.N.%20A%20review%20on%20evaluation%20metrics%20for%20data%20classification%20evaluations%202015&author=Hossin&title=A%20review%20on%20evaluation%20metrics%20for%20data%20classification%20evaluations&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Hossin%2C%20M.%20Sulaiman%2C%20M.N.%20A%20review%20on%20evaluation%20metrics%20for%20data%20classification%20evaluations%202015) [Scite](/scite_tallies?query=author%3AHossin%2Ctitle%3AA%20review%20on%20evaluation%20metrics%20for%20data%20classification%20evaluations%2Cyear%3A2015)

[^Howard_2018_a]: Howard, J., &amp; Ruder, S. (2018). Universal language model fine-tuning for text classification. arXiv preprint arXiv:1801.06146.  [OA](https://arxiv.org/abs/1801.06146)  

[^Jasperai_2023_a]: JasperAI (2023). The ai in business trend report. URL https://www.jasper.ai/blog/aibusiness-trend-report.accessed:May 26, 2023.  [OA](https://www.jasper.ai/blog/aibusiness-trend-report.accessed:May)  

[^Keynes_1937_a]: Keynes, J. M. (1937). The general theory of employment. The Quarterly Journal of Economics, 51, 209–223.  [OA](https://engine.scholarcy.com/oa_version?query=Keynes%2C%20J.M.%20The%20general%20theory%20of%20employment%201937&author=Keynes&title=The%20general%20theory%20of%20employment&year=1937) [GScholar](https://scholar.google.co.uk/scholar?q=Keynes%2C%20J.M.%20The%20general%20theory%20of%20employment%201937) [Scite](/scite_tallies?query=author%3AKeynes%2Ctitle%3AThe%20general%20theory%20of%20employment%2Cyear%3A1937)

[^Kotios_et+al_2022_a]: Kotios, D., Makridis, G., Fatouros, G., &amp; Kyriazis, D. (2022). Deep learning enhancing banking services: a hybrid transaction classification and cash flow prediction approach. Journal of Big Data, 9, 100.  [OA](https://engine.scholarcy.com/oa_version?query=Kotios%2C%20D.%20Makridis%2C%20G.%20Fatouros%2C%20G.%20Kyriazis%2C%20D.%20Deep%20learning%20enhancing%20banking%20services%3A%20a%20hybrid%20transaction%20classification%20and%20cash%20flow%20prediction%20approach%202022&author=Kotios&title=Deep%20learning%20enhancing%20banking%20services%3A%20a%20hybrid%20transaction%20classification%20and%20cash%20flow%20prediction%20approach&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Kotios%2C%20D.%20Makridis%2C%20G.%20Fatouros%2C%20G.%20Kyriazis%2C%20D.%20Deep%20learning%20enhancing%20banking%20services%3A%20a%20hybrid%20transaction%20classification%20and%20cash%20flow%20prediction%20approach%202022) [Scite](/scite_tallies?query=author%3AKotios%2Ctitle%3ADeep%20learning%20enhancing%20banking%20services%3A%20a%20hybrid%20transaction%20classification%20and%20cash%20flow%20prediction%20approach%2Cyear%3A2022)

[^Leippold_2023_a]: Leippold, M. (2023). Sentiment spin: Attacking financial sentiment with gpt-3. Finance Research Letters, Article 103957.  [OA](https://engine.scholarcy.com/oa_version?query=Leippold%2C%20M.%20Sentiment%20spin%3A%20Attacking%20financial%20sentiment%20with%20gpt-3%202023&author=Leippold&title=Sentiment%20spin%3A%20Attacking%20financial%20sentiment%20with%20gpt-3&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Leippold%2C%20M.%20Sentiment%20spin%3A%20Attacking%20financial%20sentiment%20with%20gpt-3%202023) [Scite](/scite_tallies?query=author%3ALeippold%2Ctitle%3ASentiment%20spin%3A%20Attacking%20financial%20sentiment%20with%20gpt-3%2Cyear%3A2023)

[^Liu_et+al_2021_a]: Liu, Z., Huang, D., Huang, K., Li, Z., &amp; Zhao, J. (2021). Finbert: A pre-trained financial language representation model for financial text mining. In Proceedings of the twentyninth international conference on international joint conferences on artificial intelligence (pp. 4513–4519).  [OA](https://scholar.google.co.uk/scholar?q=Liu%2C%20Z.%20Huang%2C%20D.%20Huang%2C%20K.%20Li%2C%20Z.%20Finbert%3A%20A%20pre-trained%20financial%20language%20representation%20model%20for%20financial%20text%20mining%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Z.%20Huang%2C%20D.%20Huang%2C%20K.%20Li%2C%20Z.%20Finbert%3A%20A%20pre-trained%20financial%20language%20representation%20model%20for%20financial%20text%20mining%202021) 

[^Loughran_2011_a]: Loughran, T., &amp; McDonald, B. (2011). When is a liability not a liability? textual analysis, dictionaries, and 10-ks. The Journal of Finance, 66, 35–65.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20McDonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%20textual%20analysis%2C%20dictionaries%2C%20and%2010-ks%202011&author=Loughran&title=When%20is%20a%20liability%20not%20a%20liability%3F%20textual%20analysis%2C%20dictionaries%2C%20and%2010-ks&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20McDonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%20textual%20analysis%2C%20dictionaries%2C%20and%2010-ks%202011) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3AWhen%20is%20a%20liability%20not%20a%20liability%3F%20textual%20analysis%2C%20dictionaries%2C%20and%2010-ks%2Cyear%3A2011)

[^Malo_et+al_2014_a]: Malo, P., Sinha, A., Korhonen, P., Wallenius, J., &amp; Takala, P. (2014). Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology, 65, 782–796.  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014&author=Malo&title=Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20P.%20Sinha%2C%20A.%20Korhonen%2C%20P.%20Wallenius%2C%20J.%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%2Cyear%3A2014)

[^Intelligence_2022_a]: Mordor Intelligence (2022). Ai in fintech market - growth, trends, covid-19 impact, and forecasts (2023–2028). URL: https://www.mordorintelligence.com/industryreports/ai-in-fintech-market. Accessed:April 20, 2023.  [OA](https://www.mordorintelligence.com/industryreports/ai-in-fintech-market)  

[^Openai_2023_a]: OpenAI (2023). Gpt-4 technical report. arXiv:2303.08774.  [OA](https://arxiv.org/abs/2303.08774)  

[^Peters_et+al_2018_a]: Peters, M. E., Neumann, M., Iyyer, M., Gardner, M., Clark, C., Lee, K., et al. (2018).  [OA](https://scholar.google.co.uk/scholar?q=Peters%20M%20E%20Neumann%20M%20Iyyer%20M%20Gardner%20M%20Clark%20C%20Lee%20K%20et%20al%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Peters%20M%20E%20Neumann%20M%20Iyyer%20M%20Gardner%20M%20Clark%20C%20Lee%20K%20et%20al%202018) 

[^Representations_2018_a]: Deep contextualized word representations. In Proceedings of the 2018 conference of the north american chapter of the association for computational linguistics: human language technologies, Volume 1 (long papers) (pp. 2227–2237). New Orleans, Louisiana: Association for Computational Linguistics, http://dx.doi.org/10.18653/v1/N18-1202, URL https://aclanthology.org/N18-1202.  [OA](https://doi.org/10.18653/v1/N18-1202)  [Scite](/scite_tallies?query=https://doi.org/10.18653/v1/N18-1202)

[^Poria_et+al_2017_a]: Poria, S., Cambria, E., Bajpai, R., &amp; Hussain, A. (2017). A review of affective computing: From unimodal analysis to multimodal fusion. Information Fusion, 37, 98–125.  [OA](https://engine.scholarcy.com/oa_version?query=Poria%2C%20S.%20Cambria%2C%20E.%20Bajpai%2C%20R.%20Hussain%2C%20A.%20A%20review%20of%20affective%20computing%3A%20From%20unimodal%20analysis%20to%20multimodal%20fusion%202017&author=Poria&title=A%20review%20of%20affective%20computing%3A%20From%20unimodal%20analysis%20to%20multimodal%20fusion&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Poria%2C%20S.%20Cambria%2C%20E.%20Bajpai%2C%20R.%20Hussain%2C%20A.%20A%20review%20of%20affective%20computing%3A%20From%20unimodal%20analysis%20to%20multimodal%20fusion%202017) [Scite](/scite_tallies?query=author%3APoria%2Ctitle%3AA%20review%20of%20affective%20computing%3A%20From%20unimodal%20analysis%20to%20multimodal%20fusion%2Cyear%3A2017)

[^Poria_et+al_2016_a]: Poria, S., Cambria, E., &amp; Gelbukh, A. (2016). Aspect extraction for opinion mining with a deep convolutional neural network. Knowledge-Based Systems, 108, 42–49.  [OA](https://engine.scholarcy.com/oa_version?query=Poria%2C%20S.%20Cambria%2C%20E.%20Gelbukh%2C%20A.%20Aspect%20extraction%20for%20opinion%20mining%20with%20a%20deep%20convolutional%20neural%20network%202016&author=Poria&title=Aspect%20extraction%20for%20opinion%20mining%20with%20a%20deep%20convolutional%20neural%20network&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Poria%2C%20S.%20Cambria%2C%20E.%20Gelbukh%2C%20A.%20Aspect%20extraction%20for%20opinion%20mining%20with%20a%20deep%20convolutional%20neural%20network%202016) [Scite](/scite_tallies?query=author%3APoria%2Ctitle%3AAspect%20extraction%20for%20opinion%20mining%20with%20a%20deep%20convolutional%20neural%20network%2Cyear%3A2016)

[^Radford_et+al_2018_a]: Radford, A., Narasimhan, K., Salimans, T., Sutskever, I., et al. (2018). Improving language understanding by generative pre-training.  [OA](https://scholar.google.co.uk/scholar?q=Radford%2C%20A.%20Narasimhan%2C%20K.%20Salimans%2C%20T.%20Sutskever%2C%20I.%20Improving%20language%20understanding%20by%20generative%20pre-training%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Radford%2C%20A.%20Narasimhan%2C%20K.%20Salimans%2C%20T.%20Sutskever%2C%20I.%20Improving%20language%20understanding%20by%20generative%20pre-training%202018) 

[^Radford_et+al_2019_a]: Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al. (2019). Language models are unsupervised multitask learners. OpenAI Blog, 1, 9.  [OA](https://engine.scholarcy.com/oa_version?query=Radford%2C%20A.%20Wu%2C%20J.%20Child%2C%20R.%20Luan%2C%20D.%20Language%20models%20are%20unsupervised%20multitask%20learners%202019&author=Radford&title=Language%20models%20are%20unsupervised%20multitask%20learners&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Radford%2C%20A.%20Wu%2C%20J.%20Child%2C%20R.%20Luan%2C%20D.%20Language%20models%20are%20unsupervised%20multitask%20learners%202019) [Scite](/scite_tallies?query=author%3ARadford%2Ctitle%3ALanguage%20models%20are%20unsupervised%20multitask%20learners%2Cyear%3A2019)

[^Refaeli_2021_a]: Refaeli, D., &amp; Hajek, P. (2021). Detecting fake online reviews using fine-tuned bert. 7, In Proceedings of the 2021 5th International Conference on E-Business and Internet (pp. 6–80).  [OA](https://scholar.google.co.uk/scholar?q=Refaeli%2C%20D.%20Hajek%2C%20P.%20Detecting%20fake%20online%20reviews%20using%20fine-tuned%20bert%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Refaeli%2C%20D.%20Hajek%2C%20P.%20Detecting%20fake%20online%20reviews%20using%20fine-tuned%20bert%202021) 

[^Sallam_2023_a]: Sallam, M. (2023). Chatgpt utility in healthcare education, research, and practice: systematic review on the promising perspectives and valid concerns. In Healthcare (p. 887). MDPI.  [OA](https://scholar.google.co.uk/scholar?q=Sallam%2C%20M.%20Chatgpt%20utility%20in%20healthcare%20education%2C%20research%2C%20and%20practice%3A%20systematic%20review%20on%20the%20promising%20perspectives%20and%20valid%20concerns%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Sallam%2C%20M.%20Chatgpt%20utility%20in%20healthcare%20education%2C%20research%2C%20and%20practice%3A%20systematic%20review%20on%20the%20promising%20perspectives%20and%20valid%20concerns%202023) 

[^Scao_et+al_2022_a]: Scao, T. L., Fan, A., Akiki, C., Pavlick, E., Ilić, D., Castagné, A. S., et al. (2022). Bloom: A 176b-parameter open-access multilingual language model. arXiv preprint arXiv:2211.05100.  [OA](https://arxiv.org/abs/2211.05100)  

[^Schumaker_2009_a]: Schumaker, R. P., &amp; Chen, H. (2009). Textual analysis of stock market prediction using breaking financial news: The azfin text system. ACM Transctions on Information Systems (TOIS), 27, 1–19.  [OA](https://engine.scholarcy.com/oa_version?query=Schumaker%2C%20R.P.%20Chen%2C%20H.%20Textual%20analysis%20of%20stock%20market%20prediction%20using%20breaking%20financial%20news%3A%20The%20azfin%20text%20system%202009&author=Schumaker&title=Textual%20analysis%20of%20stock%20market%20prediction%20using%20breaking%20financial%20news%3A%20The%20azfin%20text%20system&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Schumaker%2C%20R.P.%20Chen%2C%20H.%20Textual%20analysis%20of%20stock%20market%20prediction%20using%20breaking%20financial%20news%3A%20The%20azfin%20text%20system%202009) [Scite](/scite_tallies?query=author%3ASchumaker%2Ctitle%3ATextual%20analysis%20of%20stock%20market%20prediction%20using%20breaking%20financial%20news%3A%20The%20azfin%20text%20system%2Cyear%3A2009)

[^Siering_et+al_2018_a]: Siering, M., Muntermann, J., &amp; Rajagopalan, B. (2018). Explaining and predicting online review helpfulness: The role of content and reviewer-related signals. Decision Support Systems, 108, 1–12.  [OA](https://engine.scholarcy.com/oa_version?query=Siering%2C%20M.%20Muntermann%2C%20J.%20Rajagopalan%2C%20B.%20Explaining%20and%20predicting%20online%20review%20helpfulness%3A%20The%20role%20of%20content%20and%20reviewer-related%20signals%202018&author=Siering&title=Explaining%20and%20predicting%20online%20review%20helpfulness%3A%20The%20role%20of%20content%20and%20reviewer-related%20signals&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Siering%2C%20M.%20Muntermann%2C%20J.%20Rajagopalan%2C%20B.%20Explaining%20and%20predicting%20online%20review%20helpfulness%3A%20The%20role%20of%20content%20and%20reviewer-related%20signals%202018) [Scite](/scite_tallies?query=author%3ASiering%2Ctitle%3AExplaining%20and%20predicting%20online%20review%20helpfulness%3A%20The%20role%20of%20content%20and%20reviewer-related%20signals%2Cyear%3A2018)

[^Tetlock_2007_a]: Tetlock, P. C. (2007). Giving content to investor sentiment: The role of media in the stock market. The Journal of Finance, 62, 1139–1168.  [OA](https://engine.scholarcy.com/oa_version?query=Tetlock%2C%20P.C.%20Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%202007&author=Tetlock&title=Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Tetlock%2C%20P.C.%20Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%202007) [Scite](/scite_tallies?query=author%3ATetlock%2Ctitle%3AGiving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%2Cyear%3A2007)

[^Thoppilan_et+al_2022_a]: Thoppilan, R., Freitas, D. De., Hall, J., Shazeer, N., Kulshreshtha, A., Cheng, H. T., et al. (2022). Lamda: Language models for dialog applications. arXiv preprint arXiv:2201.08239.  [OA](https://arxiv.org/abs/2201.08239)  

[^Wolf_et+al_2020_a]: Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., et al. (2020). Transformers: State-of-the-art natural language processing. In Proceedings of the 2020 conference on empirical methods in natural language processing: system demonstrations (pp. 38–45).  [OA](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020) 

[^Wu_et+al_2023_a]: Wu, S., Irsoy, O., Lu, S., Dabravolski, V., Dredze, M., Gehrmann, S., et al. (2023). Bloomberggpt: A large language model for finance. arXiv preprint arXiv:2303. 17564.  [OA](https://scholar.google.co.uk/scholar?q=Wu%2C%20S.%20Irsoy%2C%20O.%20Lu%2C%20S.%20Dabravolski%2C%20V.%20Bloomberggpt%3A%20A%20large%20language%20model%20for%20finance%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Wu%2C%20S.%20Irsoy%2C%20O.%20Lu%2C%20S.%20Dabravolski%2C%20V.%20Bloomberggpt%3A%20A%20large%20language%20model%20for%20finance%202023) 

[^Yeshayahou_2021_a]: Yeshayahou, K. (2021). Israeli co similarweb files for nyse ipo. URL: https://en.globes.co.il/en/article-israeli-co-similarweb-files-for-nyse-ipo-1001367823. Accessed:May 11, 2023.  [OA](https://en.globes.co.il/en/article-israeli-co-similarweb-files-for-nyse-ipo-1001367823)  

[^Yue_et+al_2023_a]: Yue, T., Au, D., Au, C. C., &amp; Iu, K. Y. (2023). Democratizing financial knowledge with chatgpt by openai: Unleashing the power of technology. Available at SSRN 4346152.  [OA](https://scholar.google.co.uk/scholar?q=Yue%2C%20T.%20Au%2C%20D.%20Au%2C%20C.C.%20Iu%2C%20K.Y.%20Democratizing%20financial%20knowledge%20with%20chatgpt%20by%20openai%3A%20Unleashing%20the%20power%20of%20technology%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Yue%2C%20T.%20Au%2C%20D.%20Au%2C%20C.C.%20Iu%2C%20K.Y.%20Democratizing%20financial%20knowledge%20with%20chatgpt%20by%20openai%3A%20Unleashing%20the%20power%20of%20technology%202023) 

[^Zhang_et+al_2021_a]: Zhang, C., Bengio, S., Hardt, M., Recht, B., &amp; Vinyals, O. (2021). Understanding deep learning (still) requires rethinking generalization. Communications of the ACM, 64, 107–115.  [OA](https://engine.scholarcy.com/oa_version?query=Zhang%2C%20C.%20Bengio%2C%20S.%20Hardt%2C%20M.%20Recht%2C%20B.%20Understanding%20deep%20learning%20%28still%29%20requires%20rethinking%20generalization%202021&author=Zhang&title=Understanding%20deep%20learning%20%28still%29%20requires%20rethinking%20generalization&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Zhang%2C%20C.%20Bengio%2C%20S.%20Hardt%2C%20M.%20Recht%2C%20B.%20Understanding%20deep%20learning%20%28still%29%20requires%20rethinking%20generalization%202021) [Scite](/scite_tallies?query=author%3AZhang%2Ctitle%3AUnderstanding%20deep%20learning%20%28still%29%20requires%20rethinking%20generalization%2Cyear%3A2021)

