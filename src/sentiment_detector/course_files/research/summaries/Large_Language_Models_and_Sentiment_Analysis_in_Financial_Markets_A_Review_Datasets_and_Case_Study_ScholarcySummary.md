[[Liu_et+al_LargeLanguageModelsSentimentAnalysis_2024]]

# [Large Language Models and Sentiment Analysis in Financial Markets: A Review, Datasets, and Case Study](https://doi.org/10.1109/access.2024.3445413)

## [[Chenghao Liu]]; [[Arunkumar Arulappan]]; [[Ranesh Kumar Naha]] et al

## Abstract

This paper comprehensively examines Large Language Models (LLMs) in sentiment analysis, specifically in financial markets, and explores the correlation between news sentiment and Bitcoin prices. We systematically categorize various LLMs used in financial sentiment analysis, highlighting their unique applications and features. We also investigate methodologies for effective data collection and categorization, underscoring the need for diverse, comprehensive datasets. Our research features a case study investigating the correlation between news sentiment and Bitcoin prices, utilizing advanced sentiment analysis and financial analysis methods to demonstrate the practical application of LLMs. The findings reveal a modest but discernible correlation between news sentiment and Bitcoin price fluctuations, with historical news patterns showing a more substantial impact on Bitcoin's longer-term price than immediate news events. This highlights LLMs' potential in market trend prediction and informed investment decision-making. © 2013 IEEE.

## Key concepts

# behavioral_economics; #sentiment_analysis; #finding/BERT; #BERT; #financial_sentiment_analysis; #ChatGPT; #claim/bitcoin; #bitcoin; #financial_markets; #natural_language_processing; #machine_learning; #claim/large_language_models; #large_language_models

## Quote
>
> This paper examines the use of Large Language Models (LLMs) in sentiment analysis for financial markets, specifically focusing on the correlation between news sentiment and Bitcoin prices, and highlights their potential in market trend prediction and informed investment decision-making.

## Key points

- Sentiment analysis (SA) in financial markets has emerged as a critical study area, given its widespread application in specific sectors like the stock market [^1], [^2], [^3], [^4]
- In this comprehensive literature review, we adeptly examine the intersection of Large Language Models (LLMs) and sentiment analysis within financial markets, providing a detailed exploration of LLMs’ evolution, application, and future opportunities in this domain
- The review navigates through the intricacies of sentiment analysis, underlining its significance in understanding market dynamics and investor behavior
- The review methodically dissects the role of LLMs in various financial contexts, from cryptocurrency market prediction to stock price forecasting, showcasing their capability to extract and interpret complex economic sentiments
- The case study on Bitcoin price and news sentiment further exemplifies the practical application of LLMs, reinforcing that sentiment analysis, powered by advanced language models, is pivotal in deciphering market trends
- The review is open to addressing the challenges and limitations inherent in the current state of LLMs

## Summary

### Introduction To LLMs

The paper examines Large Language Models (LLMs) in sentiment analysis, focusing on financial markets and the correlation between news sentiment and Bitcoin prices.
LLMs have shown remarkable proficiency in mimicking human language skills, resulting in significant transformations across various fields, including the financial domain.
The study categorizes various LLMs used in financial sentiment analysis, highlighting their unique applications and features.

### Sentiment Analysis

Sentiment analysis in financial markets has emerged as a critical research area, particularly given its widespread application in sectors such as the stock market.
The study investigates the correlation between news sentiment, as analyzed by LLMs, and Bitcoin price movements, utilizing advanced sentiment analysis and financial analysis methods.
The findings reveal a modest but discernible correlation between news sentiment and Bitcoin price fluctuations.
Sentiment analysis has been identified as a critical component in predicting stock prices and cryptocurrency market trends.
LLMs have been used to analyze social sentiment data from sources such as GitHub and Reddit, synthesizing emotional and sentiment indicators from social media commentary into hourly and daily series datasets.
The findings indicate that incorporating these social sentiment metrics markedly enhances the predictive accuracy of daily Bitcoin and Ethereum pricing.
For instance, Ortu et al. investigated cryptocurrency price prediction by analyzing social sentiment data and employing a pre-trained BERT-based model to synthesize emotional and sentiment indicators.

### LLM Applications

The study features a case study investigating the correlation between news sentiment and Bitcoin prices, utilizing advanced sentiment analysis and financial analysis methods to demonstrate the practical application of LLMs.
The paper makes a significant contribution to the field of financial sentiment analysis by integrating the advanced capabilities of LLMs with the dynamic realm of Bitcoin and cryptocurrency markets.
The focus on the unique features and applications of these LLMs in the financial domain reveals new insights into their transformative role in market trend prediction and investment decision-making.

### LLMs

LLMs are categorized into three types based on their architecture: encoder-only, encoder-decoder, and decoder-only.
Encoder-only LLMs, such as BERT, process input text into a hidden representation.
Encoder-decoder LLMs, such as FINMEM, integrate both an encoder and a decoder to produce output text.
Decoder-only LLMs, including the GPT series, use the decoder module to generate output text.
These models have shown promising performance in financial sentiment analysis, with applications in predicting market trends and optimizing trading strategies.

### Data Acquisition

Data is a crucial component in training LLMs, and its quality and diversity significantly influence model performance.
Datasets can be categorized into four groups: open-source, collected, constructed, and industrial.
Open-source datasets, such as FiQA and Financial PhraseBank, are publicly available and reliable.
Collected datasets are compiled from various sources, while constructed datasets are modified or enhanced to align with specific research goals.
Industrial datasets contain proprietary data and are essential for real-world business contexts.

### Applications

LLMs have diverse applications in financial sentiment analysis, including predicting market trends, optimizing trading strategies, and analyzing investor sentiments.
They can be used to automate financial report summaries, predict stock prices, and identify potential investment opportunities.
The integration of LLMs in the financial sector has marked a significant evolution in how financial data is analyzed and interpreted, with the potential to transform the industry.

### Predictive Analytics

The application of Large Language Models (LLMs) to predict cryptocurrency market trends has shown promising results, particularly when sentiment analysis is integrated.
Studies have demonstrated the potential of LLMs to distill sentiment from vast datasets, offering a novel dimension to forecasting models.
For example, Zou and Herremans introduced a pioneering multimodal model, PreBit, to anticipate significant Bitcoin price movements.
Other studies have highlighted the advantages of refining FinBERT with weakly labeled data, illustrating how even imprecisely labeled datasets can significantly improve text-based feature prediction and forecasting accuracy for cryptocurrency returns.

### Stock Market Forecasting

LLMs have been applied to stock market forecasting, demonstrating their versatility across a range of financial applications.
Studies have demonstrated the utility of LLMs in economic text mining, suggesting further application of FinBERT across different financial NLP tasks.
For example, Araci introduced FinBERT, a model tailored for the financial sector that demonstrated superior capabilities in economic text mining.
Other studies have shown that contextual embeddings substantially improve efficiency for sentiment analysis compared to traditional lexicons and static word encoders, suggesting the potential of LLMs to revolutionize sentiment analysis through a deeper understanding of contextual nuances in financial texts.

### Models

The DCC model allows for time-varying correlations, adding flexibility and realism to the analysis.
It directly accounts for heteroscedasticity by calculating Dynamic Conditional Correlations (DCCs) from standardized residuals.
The DCC model involves a two-step process to estimate conditional correlations: first, a univariate GARCH model is estimated for each return series.
Transfer entropy offers distinct advantages over traditional methods, facilitating nonparametric analysis of time-series data and minimizing the need for extensive assumptions about stochastic processes.

### Methodology

The DCC model is delineated using a two-step process, with a univariate GARCH model estimated for each return series.
Transfer entropy is calculated using the formula for transfer entropy from J to I, which measures the net information flow.
The Markov process is introduced to estimate the likelihood of transitioning from one state to another during information transfer.
The escort distribution is used to facilitate the prediction of potential transition matrix scenarios.

### Results

The results of the case study analyzing the volatility of Bitcoin prices and news sentiment indicate a low long-term correlation between the two.
The DCC-GARCH model reveals dynamic adjustments in conditional correlation within a multivariate framework.
Transfer entropy values highlight significant spillover effects within cryptocurrency markets, with smaller-market-cap cryptocurrencies reacting more sensitively to changes.
News events that substantially affect Bitcoin's valuation often initiate a domino effect, impacting the valuations of other cryptocurrencies.

### Challenges

The study highlights several challenges associated with using Large Language Models (LLMs) in sentiment analysis, including technical difficulties, generalizability, and interpretability.
The increasing size of LLMs, such as GPT-1 to GPT-3, poses significant computational and storage demands, raising concerns about accessibility in resource-limited contexts.
Additionally, LLMs often struggle to maintain consistent performance across diverse domains and tasks, and their opacity can undermine trust and reliability.

### Future Opportunities

The future of LLMs in sentiment analysis holds promise, with opportunities for optimization, expansion of natural language processing capabilities, and performance improvements in existing sentiment analysis tasks.
The development of more efficient deployment strategies, improved generalizability, and enhanced interpretability is crucial to advancing LLMs.
The integration of more diverse data types, such as spoken language, diagrams, and multimodal data, could significantly expand LLMs' capabilities for capturing and interpreting varied forms of user sentiment.

### Limitations

The study acknowledges the limitations of current LLMs, including the need for larger datasets, standardized research methods, and a universal evaluation framework.
The lack of transparency in many LLMs, concerns over data quality and ownership, and potential vulnerability to adversarial attacks are also highlighted as significant challenges.
Addressing these limitations is essential for the continued innovation and development of LLMs in sentiment analysis.

## Study subjects

### 46143 documents

- TRC2-financial is a specialized subset of the TRC244 collection from Reuters, which encompasses 1.8 million news articles released between 2008 and 2010. This subset specifically contains 46,143 documents, totaling nearly 29 million words and close to 400,000 sentences [^12]. SemEval 2017 Task 5 focuses on fine-grained sentiment analysis (FSA) of news headlines and microblogs [^59]

### 1694 microblog posts

- SemEval 2017 Task 5 focuses on fine-grained sentiment analysis (FSA) of news headlines and microblogs [^59]. The training set for this task includes 1,142 financial news headlines and 1,694 microblog posts, each annotated with target entities and their corresponding sentiment scores. The test set comprises 491 financial news headlines and 794 posts [^11]

## Data analysis

- #method/gpt_model
- #method/adf_test
- #method/large_language_models
- #method/adf_test_statistic
- #method/finbert_model
- #method/dcc_model
- #method/garch_model

## Findings

- Furthermore, LLaMA2 has proven effective, reaching an accuracy of 84.03% through supervised learning and aligning financial texts [^54]
- Our dataset represents over 80% of the cryptocurrency market’s total market capitalization, ensuring a comprehensive analysis scope
- FinBERT’s performance in <a class="keyword" href="https://en.wikipedia.org/wiki/Sentiment_analysis#Financial_sentiment_analysis" title="financial sentiment analysis">financial sentiment analysis</a> tasks showed a notable 15% improvement over generic <a class="keyword" href="https://en.wikipedia.org/wiki/BERT_(language_model)" title="BERT">BERT</a> models [^12]

## Builds on previous research

- However, it is important to mention that there is no widely agreed-upon standard in the literature for the minimum parameter size for an LLM, as its efficiency is linked to the dataset’s size and the total computing power used. In our study, we follow the classification and taxonomy of LLMs introduced by Pan et al [^38], dividing mainstream LLMs into three categories based on their architecture: encoder-only, encoder-decoder, and decoder-only.

## Confirmation of earlier findings

- Nonetheless, Bitcoin exerts a more profound influence on these cryptocurrencies. Given that Bitcoin accounts for approximately 50% of the total market capitalization of all cryptocurrencies, our observations align with those reported by Zhang et al. [^83].

## Counterpoint to earlier claims

- Table 6 details the outcomes of unit root tests conducted on the variables utilized in this study, explicitly presenting the Augmented Dickey-Fuller (ADF) test results for each factor. Although stationarity is not a prerequisite for using the transfer entropy approach, which can handle probability density functions from a single realization as highlighted by Wollstadt et al. [^82], we nevertheless performed a stationarity test.

## Contributions

- In this comprehensive literature review, <mark class="fact">we adeptly examine the intersection of LLMs</mark> and sentiment analysis within financial markets, providing a detailed exploration of LLMs’ evolution, application, and future opportunities in this domain. <mark class="fact">The review navigates through the intricacies of sentiment analysis</mark>, underlining its significance in understanding market dynamics and investor behavior. Our meticulous analysis of LLMs, particularly their evolution from BERT [^14] to more sophisticated models such as FinBERT [^12] and ChatGPT, reveals their substantial impact on financial sentiment analysis.<mark class="fact">The review methodically dissects the role of LLMs in various financial contexts</mark>, from cryptocurrency market prediction to stock price forecasting, showcasing their capability to extract and interpret complex economic sentiments. <mark class="fact">The case study on Bitcoin price and news sentiment further exemplifies the practical application of LLMs</mark>, reinforcing that sentiment analysis, powered by advanced language models, is pivotal in deciphering market trends.

## Future work

- The future work includes overcoming the limitations of LLMs, such as improving their generalizability and interpretability. The study also suggests expanding LLM capabilities to include multimodal data inputs and implementing a standard evaluation framework.
- No information is provided about future work related to the study.

## References

[^1]: M. Baker and J. Wurgler, ‘‘Investor sentiment in the stock market,’’ J. Econ. Perspect., vol. 21, no. 2, pp. 129–152, 2007.  [OA](https://engine.scholarcy.com/oa_version?query=Baker%2C%20M.%20Wurgler%2C%20J.%20%E2%80%98Investor%20sentiment%20in%20the%20stock%20market%2C%E2%80%99%202007&author=Baker&title=%E2%80%98Investor%20sentiment%20in%20the%20stock%20market%2C%E2%80%99&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Baker%2C%20M.%20Wurgler%2C%20J.%20%E2%80%98Investor%20sentiment%20in%20the%20stock%20market%2C%E2%80%99%202007) [Scite](/scite_tallies?query=author%3ABaker%2Ctitle%3A%E2%80%98Investor%20sentiment%20in%20the%20stock%20market%2C%E2%80%99%2Cyear%3A2007)

[^2]: P. C. Tetlock, ‘‘Giving content to investor sentiment: The role of media in the stock market,’’ J. Finance, vol. 62, pp. 1139–1168, Jun. 2007. [Online]. Available: <https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.2007.01232.x>  [OA](https://doi.org/10.1111/j.1540-6261.2007.01232.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2007.01232.x)

[^3]: L. A. Smales, ‘‘The importance of fear: Investor sentiment and stock market returns,’’ Appl. Econ., vol. 49, no. 34, pp. 3395–3421, Jul. 2017. [Online]. Available: <https://www.tandfonline.com/doi/abs/10.1080/00036846.2016.1259754>  [OA](https://doi.org/10.1080/00036846.2016.1259754)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2016.1259754)

[^4]: T. Rao and S. Srivastava. (2012). Analyzing Stock Market Movements Using Twitter Sentiment Analysis. [Online]. Available: <http://dx.doi.org/10.1109/ASONAM.2012.30> and <https://repository.lincoln.ac.uk/articles/conference_contribution/Analyzing_stock_market_movements_using_T> witter_sentiment_analysis/25165223/2?file=44450105  [OA](https://doi.org/10.1109/ASONAM.2012.30)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ASONAM.2012.30)

[^11]: K. Mishev, A. Gjorgjevikj, I. Vodenska, L. T. Chitkushev, and D. Trajanov, ‘‘Evaluation of sentiment analysis in finance: From lexicons to transformers,’’ IEEE Access, vol. 8, pp. 131662–131682, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20%E2%80%98Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2C%E2%80%99%202020&author=Mishev&title=%E2%80%98Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2C%E2%80%99&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20%E2%80%98Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2C%E2%80%99%202020) [Scite](/scite_tallies?query=author%3AMishev%2Ctitle%3A%E2%80%98Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2C%E2%80%99%2Cyear%3A2020)

[^12]: D. Araci, ‘‘FinBERT: Financial sentiment analysis with pre-trained language models,’’ 2019, arXiv:1908.10063.  [OA](https://arxiv.org/abs/1908.10063)  

[^14]: J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, ‘‘BERT: Pre-training of deep bidirectional transformers for language understanding,’’ in Proc. Conf. North Amer. Chapter Assoc. Comput. Linguistics, Hum. Lang. Technol., vol. 1, Oct. 2018, pp. 4171–4186.  [OA](https://engine.scholarcy.com/oa_version?query=Devlin%2C%20J.%20Chang%2C%20M.-W.%20Lee%2C%20K.%20Toutanova%2C%20K.%20%E2%80%98BERT%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%2C%E2%80%99%202018-10&author=Devlin&title=%E2%80%98BERT%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%2C%E2%80%99&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Devlin%2C%20J.%20Chang%2C%20M.-W.%20Lee%2C%20K.%20Toutanova%2C%20K.%20%E2%80%98BERT%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%2C%E2%80%99%202018-10) [Scite](/scite_tallies?query=author%3ADevlin%2Ctitle%3A%E2%80%98BERT%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%2C%E2%80%99%2Cyear%3A2018)

[^38]: S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu, ‘‘Unifying large language models and knowledge graphs: A roadmap,’’ 2023, arXiv:2306.08302.  [OA](https://arxiv.org/abs/2306.08302)  

[^54]: B. Peng, E. Chersoni, Y.-Y. Hsu, L. Qiu, and C.-R. Huang, ‘‘Supervised cross-momentum contrast: Aligning representations with prototypical examples to enhance financial sentiment analysis,’’ Knowl.-Based Syst., vol. 295, Jul. 2024, Art. no. 111683.  [OA](https://engine.scholarcy.com/oa_version?query=Peng%2C%20B.%20Chersoni%2C%20E.%20Hsu%2C%20Y.-Y.%20Qiu%2C%20L.%20%E2%80%98Supervised%20cross-momentum%20contrast%3A%20Aligning%20representations%20with%20prototypical%20examples%20to%20enhance%20financial%20sentiment%20analysis%2C%E2%80%99%202024-07&author=Peng&title=%E2%80%98Supervised%20cross-momentum%20contrast%3A%20Aligning%20representations%20with%20prototypical%20examples%20to%20enhance%20financial%20sentiment%20analysis%2C%E2%80%99&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Peng%2C%20B.%20Chersoni%2C%20E.%20Hsu%2C%20Y.-Y.%20Qiu%2C%20L.%20%E2%80%98Supervised%20cross-momentum%20contrast%3A%20Aligning%20representations%20with%20prototypical%20examples%20to%20enhance%20financial%20sentiment%20analysis%2C%E2%80%99%202024-07) [Scite](/scite_tallies?query=author%3APeng%2Ctitle%3A%E2%80%98Supervised%20cross-momentum%20contrast%3A%20Aligning%20representations%20with%20prototypical%20examples%20to%20enhance%20financial%20sentiment%20analysis%2C%E2%80%99%2Cyear%3A2024)

[^59]: K. Cortis, A. Freitas, T. Daudert, M. Huerlimann, M. Zarrouk, S. Handschuh, and B. Davis, ‘‘SemEval-2017 task 5: Fine-grained sentiment analysis on financial microblogs and news,’’ in Proc. 11th Int. Workshop Semantic Eval. (SemEval), 2017, pp. 519–535.  [OA](https://scholar.google.co.uk/scholar?q=Cortis%2C%20K.%20Freitas%2C%20A.%20Daudert%2C%20T.%20Huerlimann%2C%20M.%20%E2%80%98SemEval-2017%20task%205%3A%20Fine-grained%20sentiment%20analysis%20on%20financial%20microblogs%20and%20news%2C%E2%80%99%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Cortis%2C%20K.%20Freitas%2C%20A.%20Daudert%2C%20T.%20Huerlimann%2C%20M.%20%E2%80%98SemEval-2017%20task%205%3A%20Fine-grained%20sentiment%20analysis%20on%20financial%20microblogs%20and%20news%2C%E2%80%99%202017)

[^82]: P. Wollstadt, M. Martínez-Zarzuela, R. Vicente, F. J. Díaz-Pernas, and M. Wibral, ‘‘Efficient transfer entropy analysis of non-stationary neural time series,’’ PLoS ONE, vol. 9, no. 7, Jul. 2014, Art. no. e102833.  [OA](https://engine.scholarcy.com/oa_version?query=Wollstadt%2C%20P.%20Mart%C3%ADnez-Zarzuela%2C%20M.%20Vicente%2C%20R.%20D%C3%ADaz-Pernas%2C%20F.J.%20%E2%80%98Efficient%20transfer%20entropy%20analysis%20of%20non-stationary%20neural%20time%20series%2C%E2%80%99%202014-07&author=Wollstadt&title=%E2%80%98Efficient%20transfer%20entropy%20analysis%20of%20non-stationary%20neural%20time%20series%2C%E2%80%99&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Wollstadt%2C%20P.%20Mart%C3%ADnez-Zarzuela%2C%20M.%20Vicente%2C%20R.%20D%C3%ADaz-Pernas%2C%20F.J.%20%E2%80%98Efficient%20transfer%20entropy%20analysis%20of%20non-stationary%20neural%20time%20series%2C%E2%80%99%202014-07) [Scite](/scite_tallies?query=author%3AWollstadt%2Ctitle%3A%E2%80%98Efficient%20transfer%20entropy%20analysis%20of%20non-stationary%20neural%20time%20series%2C%E2%80%99%2Cyear%3A2014)

[^83]: H. Zhang, H. Hong, Y. Guo, and C. Yang, ‘‘Information spillover effects from media coverage to the crude oil, gold, and Bitcoin markets during the COVID-19 pandemic: Evidence from the time and frequency domains,’’ Int. Rev. Econ. Finance, vol. 78, pp. 267–285, Mar. 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Zhang%2C%20H.%20Hong%2C%20H.%20Guo%2C%20Y.%20Yang%2C%20C.%20%E2%80%98Information%20spillover%20effects%20from%20media%20coverage%20to%20the%20crude%20oil%2C%20gold%2C%20and%20Bitcoin%20markets%20during%20the%20COVID-19%20pandemic%3A%20Evidence%20from%20the%20time%20and%20frequency%20domains%2C%E2%80%99%202022-03&author=Zhang&title=%E2%80%98Information%20spillover%20effects%20from%20media%20coverage%20to%20the%20crude%20oil%2C%20gold%2C%20and%20Bitcoin%20markets%20during%20the%20COVID-19%20pandemic%3A%20Evidence%20from%20the%20time%20and%20frequency%20domains%2C%E2%80%99&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Zhang%2C%20H.%20Hong%2C%20H.%20Guo%2C%20Y.%20Yang%2C%20C.%20%E2%80%98Information%20spillover%20effects%20from%20media%20coverage%20to%20the%20crude%20oil%2C%20gold%2C%20and%20Bitcoin%20markets%20during%20the%20COVID-19%20pandemic%3A%20Evidence%20from%20the%20time%20and%20frequency%20domains%2C%E2%80%99%202022-03) [Scite](/scite_tallies?query=author%3AZhang%2Ctitle%3A%E2%80%98Information%20spillover%20effects%20from%20media%20coverage%20to%20the%20crude%20oil%2C%20gold%2C%20and%20Bitcoin%20markets%20during%20the%20COVID-19%20pandemic%3A%20Evidence%20from%20the%20time%20and%20frequency%20domains%2C%E2%80%99%2Cyear%3A2022)
