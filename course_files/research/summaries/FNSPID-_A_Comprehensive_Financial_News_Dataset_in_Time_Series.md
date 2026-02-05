[[Dong_et+al_FnspidComprehensiveFinancialNewsDataset_2024]]

# [FNSPID: A Comprehensive Financial News Dataset in Time Series](https://arxiv.org/abs/2402.06698v1)

## [[Zihan Dong]]; [[Xinyu Fan]]; [[Zhiyuan Peng]]

## Abstract
Financial market predictions utilize historical data to anticipate future stock prices and market trends. Traditionally, these predictions have focused on the statistical analysis of quantitative factors, such as stock prices, trading volumes, inflation rates, and changes in industrial production. Recent advancements in large language models motivate the integrated financial analysis of both sentiment data, particularly market news, and numerical factors. Nonetheless, this methodology often faces constraints due to the scarcity of datasets that combine quantitative and qualitative sentiment analyses. To address this challenge, we introduce a large-scale financial dataset, namely, the Financial News and Stock Price Integration Dataset (FNSPID). It comprises 29.7 million stock prices and 15.7 million time-aligned financial news records for 4,775 S&amp;P 500 companies, covering the period from 1999 to 2023, sourced from 4 stock market news websites. We demonstrate that FNSPID excels existing stock market datasets in scale and diversity while uniquely incorporating sentiment information. Through financial analysis experiments on FNSPID, we propose: (1) the dataset's size and quality significantly boost market prediction accuracy; (2) adding sentiment scores modestly enhances performance on the transformer-based model; (3) a reproducible procedure that can update the dataset. Completed work, code, documentation, and examples are available at github.com/Zdong104/FNSPID. FNSPID offers unprecedented opportunities for the financial research community to advance predictive modeling and analysis.

## Key concepts
#time_series; #sentiment_analysis; #machine_learning; #large_language_models; #deep_learning; #reinforcement_learning; #finding/stock_price; #stock_price; #claim/stock_market; #stock_market; #finding/financial_news; #financial_news

## Quote
The FNSPID dataset is a comprehensive collection of financial news and stock prices, providing a valuable resource for sentiment analysis and stock price prediction. It includes a wide range of data from 1999 to 2023, sourced from trusted financial news platforms such as NASDAQ.

## Key points
- 2 Related Work2.1 Evolution of Financial Analysis Models2.2 Existing Stock Dataset3.1 Data mining and processing
- Insight from Financial News and Stock Price Integration Dataset (FNSPID): Experiments utilizing FNSPID demonstrated that larger datasets lead to better performance in price prediction; the quality of sentiments leads to a positive effect on boosting accuracy
- We demonstrated the practical application and robustness of the FNSPID dataset, underscoring its value in financial modeling and sentiment analysis research
- Previous research has shown that financial news significantly impacts stock prices ([^Allen_et+al_2019_a])
- Our experiment revealed only a minor improvement in model performance, attributable to two main factors: firstly, the models’ already high prediction accuracy makes further improvements challenging; secondly, potential delays in news dissemination may delay its impact on stock prices
- We summarize 3 points from the experiment based on FNSPID: 1. Both the quality and quantity of the dataset largely affect the stock price prediction


## Summary

### Introduction To FNSPID
The Financial News and Stock Price Integration Dataset (FNSPID) is a large-scale financial dataset that combines 29.7 million stock prices and 15.7 million time-aligned financial news records for 4,775 S&amp;P 500 companies, covering the period from 1999 to 2023.
FNSPID is designed to support research on advanced machine learning techniques and to provide a solid foundation for the development of ML models for stock market prediction.

### Related Work And Background
Traditional financial market analysis models, such as the Fama-French Three-Factor Model and the Chen, Roll, and Ross Arbitrage Pricing Theory, have limitations in anticipating future market shifts.
Emerging machine learning techniques have shown promise in addressing these limitations, with studies demonstrating the effectiveness of integrating stock price and news sentiment into deep learning models for stock market prediction.
The evolution of financial analysis models has led to more sophisticated approaches, including those that use large language models and transformer technology.

### FNSPID Construction And Applications
FNSPID is constructed through data mining and processing, and its properties are evaluated through experiments, including both quantitative and qualitative tests.
The dataset has various applications, including sentiment analysis, trend evaluation, and risk assessment, and can be used to train larger stock prediction models more accurately.
FNSPID also enables more accurate training of larger stock prediction models for market dynamics analysis, leveraging a large volume of time-series news and stock price data.

### Data
The FNSPID dataset is a comprehensive collection of financial news and stock prices, covering the period from 1999 to 2023.
It encompasses over 30 GB of data, including numerical price data, news headlines, news text, sentiment scores, and articles summarized through four distinct methodologies.
The dataset is sourced from reputable financial news platforms like NASDAQ, Bloomberg, and Reuters, ensuring reliability and relevance for sentiment analysis and stock market prediction.

### Construction
The construction of FNSPID involved collecting numerical stock data from Yahoo Finance's API and sentiment data from various reputable sources.
The dataset was built in three tasks: collecting and processing raw data, summarizing news content using four methods, and quantifying sentiment scores using ChatGPT.
The sentiment scoring scale ranged from 1 to 5, with 1 indicating negative sentiment and 5 indicating positive sentiment.

### Evaluation
The FNSPID dataset was evaluated through statistical analysis and experiments to test its reliability.
The dataset was found to be comprehensive and varied, with a multilingual capacity and temporal depth.
The experimental results demonstrated the dataset's effectiveness for stock price predictions, with the inclusion of sentiment information improving performance.
The dataset was compared to other models, including LSTM, RNN, CNN, and GRU, and was found to be a valuable resource for researchers and practitioners in financial modeling and analysis.

### Model Performance
The Transformer-based model achieved the highest accuracy with $R^{2}=0.988$, followed by the LSTM model with $R^{2}=0.856$, and the GRU model with $R^{2}=0.827$.
The RNN model had the worst performance, with an $R^{2} $ of 0.617.
The quality and quantity of the dataset significantly affected stock price prediction, with a larger training dataset yielding better performance.
The Transformer model showed a positive effect on improvement when sentiment information was included, whereas other models did not.

### Dataset Applications
The FNSPID dataset has great potential for financial prediction and related tasks, including multimodal model training, sentiment data for market prediction, correlation analysis, and financial generative AI.
The dataset can help refine LLMs to improve financial advisory performance and can be used for anomaly detection and financial risk management.
The dataset provides aligned sentiment and numerical data, enabling more accurate sentiment labeling and analysis.

### Dataset Ethics And Limitations
The study adheres to ethical considerations, including privacy concerns in financial data analysis and the potential misuse of predictive models.
The dataset is transparently marked and rigorously referenced, promoting accountability and reproducibility.
However, the dataset has limitations, including the dynamic nature of website policies and the need for ongoing model validation.
Future work includes expanding the dataset, exploring its potential, and constructing multimodal models based on its diverse data types.

### Data Preparation
The selected summarized sentences are assigned a score of $n=1$ if the sentence is in the longer sentence $S_{long}$.
The final weight score $W_{t}$ is calculated by adding the sentence weight $W_{s}$ and the summarized weight $W_{t}$.
The dictionary of the sentence set is sorted by weight to generate the final summarized sentence.

### Weight Calculation
The weight $W_{S}(S,s)$ is assigned a value of $m$ if $S$ is in $T$, and 0 otherwise.
The weight $W_{t}(S_{\text{sum}},S_{\text{long}})$ is assigned a value of $n$ if $S_{\text{sum}}$ is in $S_{\text{long}}$, and 0 otherwise.
The final weight $W_{f}$ is the sum of $W_{S}$ and $W_{t}$.

### Normalization
The normalized change in a value ($S_{n}$) is calculated relative to its initial value ($V_{0}$) using the formula $S_{n}=(V_{n}/V_{0})-1$.
Variables are scaled to a range between 0 and 1 using the formula $X_{scaled}=(x-x_{min})/(x_{max}-x_{min})$, allowing data to be represented within a consistent range for comparison and analysis.


## Study subjects

### 1142 articles
- Cortis ([^Cortis_et+al_2017_a]) provided a dataset for fine-grained sentiment analysis of financial microblogs and news, including sentiment scores and lexical/semantic features. However, this dataset contains only a limited number of news headlines (1142 articles) and uses a proprietary sentiment scoring formula, which may not accurately reflect actual news sentiment. Moreover, Sinha et al ([^Sinha_et+al_2022_a]) SEntFiN 1.0 dataset, notable for its entity-sentiment annotations and extensive database of financial entities, provides relatively more handy information than the work provided previously

### 50 stock samples
- The collective effort, requiring approximately 4TB of computing power and 45 days, reflects our commitment to overcoming these challenges and ensuring the robustness of our analysis. Beyond the summary, we expanded our analysis to include 50 stock samples selected from the top 50 most influential stocks in the S&P 500 as of 2024. These samples were incorporated into our batch for sentiment labeling, resulting in a total of 402,546 news items with assigned sentiment scores

## Data analysis
- #method/gru_model
- #method/fama_french_three_factor_model
- #method/rnn_model
- #method/garch_model
- #method/chatgpt_model
- #method/linear_regression
- #method/transformer_model

## Findings
- The experimental result demonstrated on average 6.29 percent improvement of $R^{2}$ from 5 stocks of training to 25 stocks of training among all 6 models we conducted
- In comparing (Transformer) sentiment and non-sentiment, while <a class="keyword" href="#" title="Financial News and Stock Price Integration Dataset">FNSPID</a> Task 3 has a 0.2% improvement, the Textblob sentiment has a -1.16% impact on the overall <a class="keyword" href="https://en.wikipedia.org/wiki/stock_price" title="stock price">stock price</a> prediction

##  Builds on previous research
- Recent research conducted by Zhou ([^Zhou_et+al_2023_a]) explores the capabilities of LLMs backbone models for time series prediction. This study demonstrates considerable predictive accuracy when using these models, despite their frequent use in non-financial market applications and the challenges posed by the scarcity of robust datasets.

## Differs from previous work
- The limitation of computational resources does not allow most of the experiments, including models like ChatGPT, which has hundreds of billions of parameters. However, previous work shows that DL models can handle sentiment signals properly ([^Luo_et+al_2021_a]; [^Abdelwahab_et+al_2015_a]; [^Antonowicz_et+al_2022_a]; [^Riyadh_2022_a]; [^Ibrahim_2017_a]).

## Contributions
- In conclusion, <mark class="claim">we summarize <mark class="fact">3 points from the experiment based on FNSPID</mark>: 1. Both the quality and quantity of the dataset largely affect the stock price prediction</mark>.

## Limitations
- The limitations of the study include the limited access to high-quality, open-source datasets and the challenges faced by conventional algorithms and language models in accurately scoring sentiments. The study also notes that the dataset may not be comprehensive for all types of financial news and stock prices.
- The study acknowledges several limitations, including the potential constraints of small datasets, the need for ongoing model validations, and the potential misuse of predictive models. The study also notes that the sentiment labeling methods used may lead to some information being lost, resulting in underperformance in sentiment detection.

## Future work
- The future work suggested by the study includes the potential for expanding the dataset to include more companies and news sources, and the development of more advanced machine learning techniques for predictive modeling. Additionally, the study suggests that the dataset can be used for various applications, including sentiment analysis, trend evaluation, and risk assessment.
- The future work of the study includes expanding the dataset to include more types of financial news and stock prices, and improving the sentiment analysis and stock price prediction models. The study also suggests that future research should focus on developing more advanced machine learning models for financial sentiment analysis and stock price prediction.
- The study proposes several avenues for future work, including expanding the FNSPID dataset, exploring the use of multimodal models, and developing more advanced sentiment analysis methods. The study also suggests that the FNSPID dataset could be used for a range of applications, including stock correlation analysis, anomaly detection, and financial risk management.


## References
[^Abdelwahab_et+al_2015_a]: Abdelwahab et al. (2015) Omar Abdelwahab, Mohamed Bahgat, Christopher J. Lowrance, and Adel Said Elmaghraby. 2015. Effect of training set size on SVM and Naive Bayes for Twitter sentiment analysis. 2015 IEEE International Symposium on Signal Processing and Information Technology (ISSPIT) (2015), 46–51. https://doi.org/10.1109/ISSPIT.2015.7394379  [OA](https://doi.org/10.1109/ISSPIT.2015.7394379)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ISSPIT.2015.7394379)

[^Allen_et+al_2019_a]: Allen et al. (2019) David E. Allen, Michael McAleer, and Abhay K. Singh. 2019. Daily market news sentiment and stock prices. Applied Economics 51, 30 (2019), 3212–3235. https://doi.org/10.1080/00036846.2018.1564115  [OA](https://doi.org/10.1080/00036846.2018.1564115)  [Scite](/scite_tallies?query=https://doi.org/10.1080/00036846.2018.1564115)

[^Antonowicz_et+al_2022_a]: Antonowicz et al. (2022) Pawel Antonowicz, Michal Podpora, and Joanna Rut. 2022. Digital Stereotypes in HMI and mdash The Influence of Feature Quantity Distribution in Deep Learning Models Training. Sensors 22, 18 (2022). https://doi.org/10.3390/s22186739  [OA](https://doi.org/10.3390/s22186739)  [Scite](/scite_tallies?query=https://doi.org/10.3390/s22186739)

[^Billah_et+al_2024_a]: Billah et al. (2024) Md Masum Billah, Azmery Sultana, Farzana Bhuiyan, and Mohammed Golam Kaosar. 2024. Stock price prediction: comparison of different moving average techniques using deep learning model. Neural Computing and Applications Volume 33, Issue 5 (2024), 1–18. https://doi.org/10.1007/s00521-023-09369-0  [OA](https://doi.org/10.1007/s00521-023-09369-0)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s00521-023-09369-0)

[^Chen_et+al_2016_a]: Chen et al. (2016) JF Chen, WL Chen, and CP Huang. 2016. Financial time-series data analysis using deep convolutional neural networks. In 2016 3rd International Conference on Systems and Informatics (ICSAI). IEEE, 924–929.  [OA](https://scholar.google.co.uk/scholar?q=Chen%20JF%20Chen%2C%20WL%20Chen%2C%20and%20CP%20Huang%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%20JF%20Chen%2C%20WL%20Chen%2C%20and%20CP%20Huang%202016) 

[^Chen_1983_a]: Chen (1983) Nai-Fu Chen. 1983. Some Empirical Tests of the Theory of Arbitrage Pricing. The Journal of Finance 38, 5 (1983), 1393–1414. http://www.jstor.org/stable/2327577  [OA](http://www.jstor.org/stable/2327577)  [Scite](/scite_tallies?query=author%3AChen%2Ctitle%3ANai-Fu%20Chen%2Cyear%3A1983)

[^Cortis_et+al_2017_a]: Cortis et al. (2017) Keith Cortis, Andre Freitas, Tobias Daudert, Manuela Hurlimann, Manel Zarrouk, Siegfried Handschuh, and Brian Davis. 2017. SemEval-2017 Task 5: Fine-Grained Sentiment Analysis on Financial Microblogs and News. https://doi.org/10.18653/v1/S17-2089  [OA](https://doi.org/10.18653/v1/S17-2089)  [Scite](/scite_tallies?query=https://doi.org/10.18653/v1/S17-2089)

[^Darapaneni_et+al_2022_a]: Darapaneni et al. (2022) Narayana Darapaneni, Anwesh Reddy Paduri, Himank Sharma, Milind Manjrekar, Nutan Hindlekar, Pranali Bhagat, Usha Aiyer, and Yogesh Agarwal. 2022. Stock Price Prediction using Sentiment Analysis and Deep Learning for Indian Markets. arXiv:2204.05783 [q-fin.ST]  [OA](https://arxiv.org/abs/2204.05783)  

[^Fabozzi_et+al_2002_a]: Fabozzi et al. (2002) Frank J Fabozzi, Francis Gupta, and Harry M Markowitz. 2002. The legacy of modern portfolio theory. The journal of investing 11, 3 (2002), 7–22.  [OA](https://engine.scholarcy.com/oa_version?query=Fabozzi%20Fabozzi%2C%20Frank%20J.%20Gupta%2C%20Francis%20Markowitz%2C%20Harry%20M.%20The%20legacy%20of%20modern%20portfolio%20theory%202002&author=Fabozzi&title=The%20legacy%20of%20modern%20portfolio%20theory&year=2002) [GScholar](https://scholar.google.co.uk/scholar?q=Fabozzi%20Fabozzi%2C%20Frank%20J.%20Gupta%2C%20Francis%20Markowitz%2C%20Harry%20M.%20The%20legacy%20of%20modern%20portfolio%20theory%202002) [Scite](/scite_tallies?query=author%3AFabozzi%2Ctitle%3AThe%20legacy%20of%20modern%20portfolio%20theory%2Cyear%3A2002)

[^Fama_et+al_1992_a]: Fama and French (1992) Eugene F Fama and Kenneth R French. 1992. The cross-section of expected stock returns. The Journal of Finance 47, 2 (1992), 427–465.  [OA](https://engine.scholarcy.com/oa_version?query=Fama%20French%20Fama%2C%20Eugene%20F.%20French%2C%20Kenneth%20R.%20The%20cross-section%20of%20expected%20stock%20returns%201992&author=Fama&title=The%20cross-section%20of%20expected%20stock%20returns&year=1992) [GScholar](https://scholar.google.co.uk/scholar?q=Fama%20French%20Fama%2C%20Eugene%20F.%20French%2C%20Kenneth%20R.%20The%20cross-section%20of%20expected%20stock%20returns%201992) [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3AThe%20cross-section%20of%20expected%20stock%20returns%2Cyear%3A1992)

[^Farimani_et+al_2021_a]: Farimani et al. (2021) Saeede Anbaee Farimani, M. V. Jahan, A. M. Fard, and Gholamreza Haffari. 2021. Leveraging Latent Economic Concepts and Sentiments in the News for Market Prediction. https://consensus.app/papers/leveraging-latent-economic-concepts-sentiments-news-farimani/802f15acfcd75b2b8514e7bc4b7377a7/?utm_source=chatgpt21867 news with headline and news content included for currency (including cryptocurrency)exchange rate news. Eg USDJPY, BTCUSD.  [OA](https://consensus.app/papers/leveraging-latent-economic-concepts-sentiments-news-farimani/802f15acfcd75b2b8514e7bc4b7377a7/?utm_source=chatgpt21867)  

[^Fatouros_et+al_2023_a]: Fatouros et al. (2023) Georgios Fatouros, John Soldatos, Kalliopi Kouroumali, Georgios Makridis, and Dimosthenis Kyriazis. 2023. Transforming sentiment analysis in the financial domain with ChatGPT. Machine Learning with Applications 14 (2023), 100508.  [OA](https://engine.scholarcy.com/oa_version?query=Fatouros%20Georgios%20Fatouros%2C%20John%20Soldatos%2C%20Kalliopi%20Kouroumali%2C%20Georgios%20Makridis%2C%20and%20Dimosthenis%20Kyriazis%202023&author=Fatouros&title=Georgios%20Fatouros%2C%20John%20Soldatos%2C%20Kalliopi%20Kouroumali%2C%20Georgios%20Makridis%2C%20and%20Dimosthenis%20Kyriazis&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Fatouros%20Georgios%20Fatouros%2C%20John%20Soldatos%2C%20Kalliopi%20Kouroumali%2C%20Georgios%20Makridis%2C%20and%20Dimosthenis%20Kyriazis%202023) [Scite](/scite_tallies?query=author%3AFatouros%2Ctitle%3AGeorgios%20Fatouros%2C%20John%20Soldatos%2C%20Kalliopi%20Kouroumali%2C%20Georgios%20Makridis%2C%20and%20Dimosthenis%20Kyriazis%2Cyear%3A2023)

[^Gupta_2020_a]: Gupta and Chen (2020) Rubi Gupta and Min Chen. 2020. Sentiment Analysis for Stock Price Prediction., 213-218 pages. https://doi.org/10.1109/MIPR49039.2020.00051  [OA](https://doi.org/10.1109/MIPR49039.2020.00051)  [Scite](/scite_tallies?query=https://doi.org/10.1109/MIPR49039.2020.00051)

[^Hsu_et+al_2021_a]: Hsu et al. (2021) Yen-Ju Hsu, Yang-Cheng Lu, and J Jimmy Yang. 2021. News sentiment and stock market volatility. Review of Quantitative Finance and Accounting 57 (2021), 1093–1122.  [OA](https://engine.scholarcy.com/oa_version?query=Hsu%20Yen-Ju%20Hsu%2C%20Yang-Cheng%20Lu%2C%20and%20J%20Jimmy%20Yang%202021&author=Hsu&title=Yen-Ju%20Hsu%2C%20Yang-Cheng%20Lu%2C%20and%20J%20Jimmy%20Yang&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Hsu%20Yen-Ju%20Hsu%2C%20Yang-Cheng%20Lu%2C%20and%20J%20Jimmy%20Yang%202021) [Scite](/scite_tallies?query=author%3AHsu%2Ctitle%3AYen-Ju%20Hsu%2C%20Yang-Cheng%20Lu%2C%20and%20J%20Jimmy%20Yang%2Cyear%3A2021)

[^Ibrahim_2017_a]: Ibrahim and Yusoff (2017) Mohd Naim Mohd Ibrahim and Mohd Zaliman Mohd Yusoff. 2017. The impact of different training data set on the accuracy of sentiment classification of Naïve Bayes technique. In 2017 IEEE Conference on Open Systems (ICOS). 17–20. https://doi.org/10.1109/ICOS.2017.8280267  [OA](https://doi.org/10.1109/ICOS.2017.8280267)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ICOS.2017.8280267)

[^Kocoń_et+al_2023_a]: Kocoń et al. (2023) Jan Kocoń, Igor Cichecki, Oliwier Kaszyca, Mateusz Kochanek, Dominika Szydło, Joanna Baran, Julita Bielaniewicz, Marcin Gruza, Arkadiusz Janz, Kamil Kanclerz, et al. 2023. ChatGPT: Jack of all trades, master of none. Information Fusion (2023), 101861.  [OA](https://engine.scholarcy.com/oa_version?query=Koco%C5%84%20Koco%C5%84%2C%20Jan%20Cichecki%2C%20Igor%20Kaszyca%2C%20Oliwier%20ChatGPT%3A%20Jack%20of%20all%20trades%2C%20master%20of%20none%202023&author=Koco%C5%84&title=ChatGPT%3A%20Jack%20of%20all%20trades%2C%20master%20of%20none&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Koco%C5%84%20Koco%C5%84%2C%20Jan%20Cichecki%2C%20Igor%20Kaszyca%2C%20Oliwier%20ChatGPT%3A%20Jack%20of%20all%20trades%2C%20master%20of%20none%202023) [Scite](/scite_tallies?query=author%3AKoco%C5%84%2Ctitle%3AChatGPT%3A%20Jack%20of%20all%20trades%2C%20master%20of%20none%2Cyear%3A2023)

[^Konstantinov_et+al_2020_a]: Konstantinov et al. (2020) Gueorgui Konstantinov, Andreas Chorus, and Jonas Rebmann. 2020. A network and machine learning approach to factor, asset, and blended allocation. The Journal of Portfolio Management 46, 6 (2020), 54–71.  [OA](https://engine.scholarcy.com/oa_version?query=Konstantinov%20Gueorgui%20Konstantinov%2C%20Andreas%20Chorus%2C%20and%20Jonas%20Rebmann%202020&author=Konstantinov&title=Gueorgui%20Konstantinov%2C%20Andreas%20Chorus%2C%20and%20Jonas%20Rebmann&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Konstantinov%20Gueorgui%20Konstantinov%2C%20Andreas%20Chorus%2C%20and%20Jonas%20Rebmann%202020) [Scite](/scite_tallies?query=author%3AKonstantinov%2Ctitle%3AGueorgui%20Konstantinov%2C%20Andreas%20Chorus%2C%20and%20Jonas%20Rebmann%2Cyear%3A2020)

[^Kurani_et+al_2023_a]: Kurani et al. (2023) Akshit Kurani, Pavan Doshi, Aarya Vakharia, and Manan Shah. 2023. A Comprehensive Comparative Study of Artificial Neural Network (ANN) and Support Vector Machines (SVM) on Stock Forecasting. Annals of Data Science Volume 10, Issue 1 (2023), 183–208. https://doi.org/10.1007/s40745-021-00344-x  [OA](https://doi.org/10.1007/s40745-021-00344-x)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s40745-021-00344-x)

[^Lee_2001_a]: Lee (2001) Jae Won Lee. 2001. Stock price prediction using reinforcement learning. In ISIE 2001. 2001 IEEE International Symposium on Industrial Electronics Proceedings (Cat. No.01TH8570), Vol. 1. 690–695 vol.1. https://doi.org/10.1109/ISIE.2001.931880  [OA](https://doi.org/10.1109/ISIE.2001.931880)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ISIE.2001.931880)

[^Li_et+al_2022_a]: Li et al. (2022) Jianlong Li, Siyuan Wang, Zhihang Zhu, Minghao Liu, Changjiang Zhang, and Bingyan Han. 2022. Stock Prediction Based on Deep Learning and its Application in Pairs Trading. In 2022 International Symposium on Networks, Computers and Communications (ISNCC). 1–7. https://doi.org/10.1109/ISNCC55209.2022.9851776  [OA](https://doi.org/10.1109/ISNCC55209.2022.9851776)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ISNCC55209.2022.9851776)

[^Li_2020_a]: Li and Pan (2020) Yang Li and Yi Pan. 2020. A novel ensemble deep learning model for stock prediction based on stock prices and news. https://consensus.app/papers/novel-learning-model-stock-prediction-based-stock-prices-li/8b3afff9cf6d5073aa99142d106d2ec6/?utm_source=chatgptNot a dataset, but it shows the sentiment information+stock price can make the prediction better..  [OA](https://consensus.app/papers/novel-learning-model-stock-prediction-based-stock-prices-li/8b3afff9cf6d5073aa99142d106d2ec6/?utm_source=chatgptNot)  

[^Liapis_et+al_2023_a]: Liapis et al. (2023) Charalampos M. Liapis, Aikaterini Karanikola, and S. Kotsiantis. 2023. Investigating Deep Stock Market Forecasting with Sentiment Analysis. Entropy 25 (2023). https://doi.org/10.3390/e25020219  [OA](https://doi.org/10.3390/e25020219)  [Scite](/scite_tallies?query=https://doi.org/10.3390/e25020219)

[^Liu_et+al_2024_a]: Liu et al. (2024) Xiao-Yang Liu, Ziyi Xia, Hongyang Yang, Jiechao Gao, Daochen Zha, Ming Zhu, Christina Dan Wang, Zhaoran Wang, and Jian Guo. 2024. Dynamic Datasets and Market Environments for Financial Reinforcement Learning. Machine Learning - Springer Nature (2024).  [OA](https://scholar.google.co.uk/scholar?q=Liu%20Liu%2C%20Xiao-Yang%20Xia%2C%20Ziyi%20Yang%2C%20Hongyang%20Dynamic%20Datasets%20and%20Market%20Environments%20for%20Financial%20Reinforcement%20Learning%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%20Liu%2C%20Xiao-Yang%20Xia%2C%20Ziyi%20Yang%2C%20Hongyang%20Dynamic%20Datasets%20and%20Market%20Environments%20for%20Financial%20Reinforcement%20Learning%202024) 

[^Lopez-Lira_2023_a]: Lopez-Lira and Tang (2023) Alejandro Lopez-Lira and Yuehua Tang. 2023. Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models. arXiv:2304.07619 [q-fin.ST]  [OA](https://arxiv.org/abs/2304.07619)  

[^Luo_et+al_2021_a]: Luo et al. (2021) Jiawei Luo, Mondher Bouazizi, and T. Ohtsuki. 2021. Data Augmentation for Sentiment Analysis Using Sentence Compression-Based SeqGAN With Data Screening. IEEE Access 9 (2021), 99922–99931. https://doi.org/10.1109/ACCESS.2021.3094023  [OA](https://doi.org/10.1109/ACCESS.2021.3094023)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ACCESS.2021.3094023)

[^Lutz_et+al_2018_a]: Lutz et al. (2018) Bernhard Lutz, Nicolas Pröllochs, and Dirk Neumann. 2018. Sentence-Level Sentiment Analysis of Financial News Using Distributed Text Representations and Multi-Instance Learning. https://consensus.app/papers/sentencelevel-sentiment-analysis-financial-news-using-lutz/ec1a20b55e835dfea090a966be42768d/?utm_source=chatgpt1000 sentiment labeled news. No timestamp..  [OA](https://consensus.app/papers/sentencelevel-sentiment-analysis-financial-news-using-lutz/ec1a20b55e835dfea090a966be42768d/?utm_source=chatgpt1000)  

[^Maciel_2008_a]: Maciel and Ballini (2008) LEANDRO S Maciel and Rosângela Ballini. 2008. Design a neural network for time series financial forecasting: Accuracy and robustness analysis. Anales do 9o Encontro Brasileiro de Finanças, Sao Pablo, Brazil (2008).  [OA](https://scholar.google.co.uk/scholar?q=Maciel%20Ballini%20LEANDRO%20S%20Maciel%20and%20Ros%C3%A2ngela%20Ballini%202008) [GScholar](https://scholar.google.co.uk/scholar?q=Maciel%20Ballini%20LEANDRO%20S%20Maciel%20and%20Ros%C3%A2ngela%20Ballini%202008) 

[^Manurung_et+al_2018_a]: Manurung et al. (2018) Adler Haymans Manurung, Widodo Budiharto, and Harry Budi Santoso. 2018. Algorithm and modeling of stock prices forecasting based on long short-term memory (LSTM). ICIC Express Letters (2018).  [OA](https://engine.scholarcy.com/oa_version?query=Manurung%20Adler%20Haymans%20Manurung%2C%20Widodo%20Budiharto%2C%20and%20Harry%20Budi%20Santoso%202018&author=Manurung&title=Adler%20Haymans%20Manurung%2C%20Widodo%20Budiharto%2C%20and%20Harry%20Budi%20Santoso&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Manurung%20Adler%20Haymans%20Manurung%2C%20Widodo%20Budiharto%2C%20and%20Harry%20Budi%20Santoso%202018) [Scite](/scite_tallies?query=author%3AManurung%2Ctitle%3AAdler%20Haymans%20Manurung%2C%20Widodo%20Budiharto%2C%20and%20Harry%20Budi%20Santoso%2Cyear%3A2018)

[^Meng_2019_a]: Meng and Khushi (2019) Terry Lingze Meng and Matloob Khushi. 2019. Reinforcement Learning in Financial Markets. Data 4, 3 (2019). https://doi.org/10.3390/data4030110  [OA](https://doi.org/10.3390/data4030110)  [Scite](/scite_tallies?query=https://doi.org/10.3390/data4030110)

[^Mohan_et+al_2019_a]: Mohan et al. (2019) Saloni Mohan, Sahitya Mullapudi, Sudheer Sammeta, Parag Vijayvergia, and David C. Anastasiu. 2019. Stock Price Prediction Using News Sentiment Analysis. In 2019 IEEE Fifth International Conference on Big Data Computing Service and Applications (BigDataService). IEEE, 205–208. https://doi.org/10.1109/BigDataService.2019.00035  [OA](https://doi.org/10.1109/BigDataService.2019.00035)  [Scite](/scite_tallies?query=https://doi.org/10.1109/BigDataService.2019.00035)

[^Openai_2023_a]: OpenAI (2023) OpenAI. 2023. ChatGPT. https://openai.com/chatgptOct 12, 2023.  [OA](https://openai.com/chatgptOct)  

[^Remy_2015_a]: Philippe Remy (2015) Xiao Ding Philippe Remy. 2015. Financial News Dataset from Bloomberg and Reuters. https://github.com/philipperemy/financial-news-dataset.  [OA](https://github.com/philipperemy/financial-news-dataset)  

[^Qudah_2016_a]: Qudah and Rabhi (2016) I. Qudah and F. Rabhi. 2016. News Sentiment Impact Analysis (NSIA) Framework. https://consensus.app/papers/news-sentiment-impact-analysis-nsia-framework-qudah/cd2fd31ffc8052eda8fe3a637a35ec49/?utm_source=chatgptNot a dataset, it introduced how should the sentiment dataset been build up as..  [OA](https://consensus.app/papers/news-sentiment-impact-analysis-nsia-framework-qudah/cd2fd31ffc8052eda8fe3a637a35ec49/?utm_source=chatgptNot)  [Scite](/scite_tallies?query=author%3AQudah%2Ctitle%3AI.%20Qudah%20and%20F%2Cyear%3A2016)

[^Riyadh_2022_a]: Riyadh and Shafiq (2022) M. Riyadh and M. O. Shafiq. 2022. GAN-BElectra: Enhanced Multi-class Sentiment Analysis with Limited Labeled Data. Applied Artificial Intelligence 36 (2022). https://doi.org/10.1080/08839514.2022.2083794  [OA](https://doi.org/10.1080/08839514.2022.2083794)  [Scite](/scite_tallies?query=https://doi.org/10.1080/08839514.2022.2083794)

[^Sakariyahu_et+al_2023_a]: Sakariyahu et al. (2023) Rilwan Sakariyahu, Sofia Johan, Rodiat Lawal, Audrey Paterson, and Eleni Chatzivgeri. 2023. Dynamic connectedness between investors’ sentiment and asset prices: A comparison between major markets in Europe and USA. Journal of International Financial Markets, Institutions and Money 89 (2023), 101866. https://doi.org/10.1016/j.intfin.2023.101866  [OA](https://doi.org/10.1016/j.intfin.2023.101866)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.intfin.2023.101866)

[^Sharpe_1964_a]: Sharpe (1964) William F Sharpe. 1964. Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk. Journal of Finance 19 (1964), 425–442.  [OA](https://engine.scholarcy.com/oa_version?query=Sharpe%20William%20F%20Sharpe%201964&author=Sharpe&title=William%20F%20Sharpe&year=1964) [GScholar](https://scholar.google.co.uk/scholar?q=Sharpe%20William%20F%20Sharpe%201964) [Scite](/scite_tallies?query=author%3ASharpe%2Ctitle%3AWilliam%20F%20Sharpe%2Cyear%3A1964)

[^Shen_et+al_2018_a]: Shen et al. (2018) G Shen, Q Tan, H Zhang, P Zeng, and J Xu. 2018. Deep learning with gated recurrent unit networks for financial sequence predictions. Procedia Computer Science 131 (2018), 895–903.  [OA](https://engine.scholarcy.com/oa_version?query=Shen%20Shen%2C%20G.%20Tan%2C%20Q.%20Zhang%2C%20H.%20Deep%20learning%20with%20gated%20recurrent%20unit%20networks%20for%20financial%20sequence%20predictions%202018&author=Shen&title=Deep%20learning%20with%20gated%20recurrent%20unit%20networks%20for%20financial%20sequence%20predictions&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Shen%20Shen%2C%20G.%20Tan%2C%20Q.%20Zhang%2C%20H.%20Deep%20learning%20with%20gated%20recurrent%20unit%20networks%20for%20financial%20sequence%20predictions%202018) [Scite](/scite_tallies?query=author%3AShen%2Ctitle%3ADeep%20learning%20with%20gated%20recurrent%20unit%20networks%20for%20financial%20sequence%20predictions%2Cyear%3A2018)

[^Sheth_2023_a]: Sheth and Shah (2023) Dhruhi Sheth and Manan Shah. 2023. Predicting stock market using machine learning: best and accurate way to know future stock prices. International Journal of System Assurance Engineering and Management Volume 14, Issue 1 (2023), 1–18. https://doi.org/10.1007/s13198-022-01811-1  [OA](https://doi.org/10.1007/s13198-022-01811-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s13198-022-01811-1)

[^Shi_2023_a]: Shi (2023) Zhongyu Shi. 2023. Layout guide for Journal of Physics: conference series using Microsoft Word. 12509 (2023), 125090M – 125090M–6. https://doi.org/10.1117/12.2655886  [OA](https://doi.org/10.1117/12.2655886)  [Scite](/scite_tallies?query=https://doi.org/10.1117/12.2655886)

[^Sinha_et+al_2022_a]: Sinha et al. (2022) Ankur Sinha, Satishwar Kedas, Rishu Kumar, and Pekka Malo. 2022. SEntFiN 1.0: Entity‐aware sentiment analysis for financial news. https://consensus.app/papers/sentfin-entity‐aware-sentiment-analysis-news-sinha/39969235e7ed532a9a2f0f813bd132Fine-grained financial sentiment analysis on news headlines is a challenging task requiring human-annotated datasets to achieve high performance..  [OA](https://consensus.app/papers/sentfin-entity‐aware-sentiment-analysis-news-sinha/39969235e7ed532a9a2f0f813bd132Fine-grained)  

[^Vaswani_et+al_2017_a]: Vaswani et al. (2017) Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. Advances in neural information processing systems 30 (2017).  [OA](https://engine.scholarcy.com/oa_version?query=Vaswani%20Vaswani%2C%20Ashish%20Shazeer%2C%20Noam%20Parmar%2C%20Niki%20Attention%20is%20all%20you%20need%202017&author=Vaswani&title=Attention%20is%20all%20you%20need&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%20Vaswani%2C%20Ashish%20Shazeer%2C%20Noam%20Parmar%2C%20Niki%20Attention%20is%20all%20you%20need%202017) [Scite](/scite_tallies?query=author%3AVaswani%2Ctitle%3AAttention%20is%20all%20you%20need%2Cyear%3A2017)

[^Venuti_2021_a]: Venuti (2021) Keenan Venuti. 2021. Predicting Mergers and Acquisitions using Graph-based Deep Learning. ArXiv abs/2104.01757 (2021).  [OA](https://arxiv.org/abs/2104.01757)  

[^Vu_2024_a]: Vu ([n. d.]) Quan Vu. [n. d.]. Finnhub Stock APIs. https://finnhub.io/. Accessed: Jan.14, 2024.  [OA](https://finnhub.io/)  

[^Wang_et+al_2017_a]: Wang et al. (2017) Feng Wang, Yongquan Zhang, Qi Rao, Kangshun Li, and H. Zhang. 2017. Exploring mutual information-based sentimental analysis with kernel-based extreme learning machine for stock prediction. Soft Computing 21 (2017), 3193–3205. https://doi.org/10.1007/s00500-015-2003-z  [OA](https://doi.org/10.1007/s00500-015-2003-z)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s00500-015-2003-z)

[^Wang_et+al_2023_a]: Wang et al. (2023) Neng Wang, Hongyang Yang, and Christina Dan Wang. 2023. FinGPT: Instruction Tuning Benchmark for Open-Source Large Language Models in Financial Datasets. arXiv:2310.04793 [cs.CL]  [OA](https://arxiv.org/abs/2310.04793)  

[^Wu_et+al_2023_a]: Wu et al. (2023) Haixu Wu, Tengge Hu, Yong Liu, Hang Zhou, Jianmin Wang, and Mingsheng Long. 2023. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis. arXiv:2210.02186 [cs.LG]  [OA](https://arxiv.org/abs/2210.02186)  

[^Wu_et+al_2020_a]: Wu et al. (2020) Xing Wu, Haolei Chen, Jianjia Wang, Luigi Troiano, Vincenzo Loia, and Hamido Fujita. 2020. Adaptive stock trading strategies with deep reinforcement learning methods. Information Sciences 538 (2020), 142–158. https://doi.org/10.1016/j.ins.2020.05.066  [OA](https://doi.org/10.1016/j.ins.2020.05.066)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.ins.2020.05.066)

[^Yang_et+al_2021_a]: Yang et al. (2021) Hongyang Yang, Xiao-Yang Liu, Shan Zhong, and Anwar Walid. 2021. Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy. In Proceedings of the First ACM International Conference on AI in Finance (New York, New York) (ICAIF ’20). Association for Computing Machinery, New York, NY, USA, Article 31, 8 pages. https://doi.org/10.1145/3383455.3422540  [OA](https://doi.org/10.1145/3383455.3422540)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3383455.3422540)

[^Yutkin_2019_a]: Yutkin (2019) Dmitry Yutkin. 2019. Corpus of news articles of Lenta.Ru. https://github.com/yutkin/Lenta.Ru-News-Dataset. Accessed:12/30/2023.  [OA](https://github.com/yutkin/Lenta.Ru-News-Dataset)  

[^Zhang_et+al_2023_a]: Zhang et al. (2023) Boyu Zhang, Hongyang Yang, and Xiao-Yang Liu. 2023. Instruct-FinGPT: Financial Sentiment Analysis by Instruction Tuning of General-Purpose Large Language Models. arXiv preprint arXiv:2306.12659 (2023).  [OA](https://arxiv.org/abs/2306.12659)  

[^Zhou_et+al_2023_a]: Zhou et al. (2023) Tian Zhou, PeiSong Niu, Xue Wang, Liang Sun, and Rong Jin. 2023. One Fits All:Power General Time Series Analysis by Pretrained LM. arXiv:2302.11939 [cs.LG]  [OA](https://arxiv.org/abs/2302.11939)  

