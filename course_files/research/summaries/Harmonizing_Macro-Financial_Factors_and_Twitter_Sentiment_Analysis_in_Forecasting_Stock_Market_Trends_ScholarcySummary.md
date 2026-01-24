[[Amin_et+al_HarmonizingMacrofinancialFactorsTwitterSentiment_2024]]

# [Harmonizing Macro-Financial Factors and Twitter Sentiment Analysis in Forecasting Stock Market Trends](https://doi.org/10.32996/jcsts)

## [[Md Shahedul Amin]]; [[✉]]; [[Eftekhar Hossain Ayon]] et al.

## Abstract
ABSTRACT: The surge in generative artificial intelligence technologies, exemplified by systems such as ChatGPT, has sparked widespread interest and discourse, prominently observed on social media platforms such as Twitter. This paper examines whether sentiment expressed in tweets discussing advancements in AI can forecast day-to-day fluctuations in the stock prices of associated companies. Our investigation involves analyzing tweets containing hashtags related to ChatGPT from December 2022 to March 2023. Leveraging natural language processing techniques, we extract features, including positive/negative sentiment scores, from the collected tweets. A range of machine learning classification models, including gradient boosting, decision trees, and random forests, are trained on tweet sentiments and associated features to predict stock price movements for key companies, such as Microsoft and OpenAI. These models undergo training and testing phases using an empirical dataset collected during the specified timeframe. Our preliminary findings reveal intriguing indications of a plausible correlation between public sentiment reflected in Twitter discussions surrounding ChatGPT and generative AI and the subsequent impact on market valuation and trading activities for pertinent companies, as gauged by stock prices. This study aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets. In conjunction with this Twitter-based sentiment analysis, we incorporate control variables including macroeconomic indicators, the Twitter uncertainty index, and stock market data for several prominent companies.

## Key concepts
#claim/ChatGPT; #ChatGPT; #consumer_price_index; #sentiment_analysis; #market_trend; #social_media; #claim/stock_price; #stock_price; #tweets; #claim/stock_market; #stock_market

## Quote
> The study evaluates the performance of various machine learning models, including Random Forest, Decision Tree, Extra Tree, Gradient Boosting, and Naive Bayes, in predicting stock market trends, with Random Forest demonstrating robust performance in identifying both Bearish and Bullish trends.

## Key points
- The sentiment analysis of tweets spanning December 2022 to March 2023 holds the potential to significantly impact the stock trends of various influential companies
- 5. Conclusion: The analysis of Twitter data in anticipation of stock market trends presents a compelling narrative when juxtaposed against macroeconomic indicators and company-specific stock data
- This multifaceted approach seeks to unravel the intricate interplay between sentiment analysis derived from social media, broader economic conditions, and the individual performance of companies in the stock market
- The integration of sentiment analysis from Twitter data alongside macroeconomic indicators offers a holistic view of market sentiment
- Incorporating company-specific stock data, including financial reports, revenue, and earnings, provides granular insights into individual stock performance. This holistic approach illuminates the intricate relationships between sentiment, economic conditions, and market dynamics. It unveils the potential synergy between social sentiment and economic indicators in predicting market trends, offering a more comprehensive understanding of market behavior
- In identifying Bullish trends, Random Forest again emerged with the highest accuracy of 100%, followed by Decision Tree (89%) and Gradient Boosting (93%)
- While sentiment analysis offers a window into public perception, its amalgamation with broader economic indicators and detailed company-specific data augments predictive models, fostering a nuanced comprehension of market behavior and trends


## Summary

### Introduction
The study examines the relationship between sentiment expressed in tweets about AI advancements and day-to-day fluctuations in the stock prices of associated companies.
The investigation involves analyzing tweets containing hashtags related to ChatGPT from December 2022 to March 2023.
The research aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets.

### Methodology
The study employs natural language processing techniques to extract features, including positive/negative sentiment scores, from the collected tweets.
A range of machine learning classification models, including gradient boosting, decision trees, and random forests, are used to train on tweet sentiments and associated features to predict stock price movements for key companies.
The features extracted from Twitter data are systematically linked to daily stock prices, and supervised learning models are trained on the amalgamated paired dataset.
The study employs sentiment analysis of the tweet dataset to forecast bullish or bearish stock market trends.
The analysis integrates Twitter-derived sentiment with control variables, including the Consumer Confidence Index, Unemployment Rate, and Consumer Price Index.
The study also incorporates company-specific stock market data, including the Stock Market Uncertainty Index and Volume.
Feature engineering involves computing sentiment scores, including positive, neutral, and negative sentiments, and introducing a small value to prevent potential issues arising from zero values.

### Literature Review
Prior research has utilized sentiment analysis of Twitter messages to construct a daily happiness index, offering insights into the influence of social media on financial markets.
Studies have also explored the influence of social media sentiment on stock market volatility, elucidating the effects of sentiments linked to significant global events on investor attitudes and transactional trading metrics.
The application of machine learning methodologies has been instrumental in developing predictive models that assess the relationship between tweet content and stock prices, underscoring the promise of machine learning for predicting future stock prices through sentiment analysis.

### Data
The study combines tweet data related to ChatGPT with historical stock prices of five technology giants - Google, Amazon, Meta, Nvidia, and Microsoft - from December 2022 to March 2023.
The dataset includes over 500,000 tweets and 90 trading days of historical price data.
The fusion of these datasets enables correlating daily Twitter sentiment and engagement metrics with end-of-day stock price movements.

### Results
The study evaluates the performance of various classification models, including Random Forest, Decision Tree, Extra Trees Classifier, and Naive Bias Classifier, in predicting stock market trends.
The models are trained on a subset of the dataset and validated on an independent section.
The evaluation metrics include accuracy, F1, and recall scores.
The results show that Random Forest performs strongly, achieving high accuracy and recall in identifying bearish and bullish trends.

### Models
Random Forest achieved high accuracy, recall, and F1 scores in identifying both Bearish and Bullish trends, demonstrating its potential as an effective model for financial market trend prediction.
Decision Tree and Extra Tree also exhibited commendable performance, while Gradient Boosting and Naive Bayes showed relatively lower predictive performance.
However, Gradient Boosting achieved the highest accuracy score for both bullish and bearish predictions in certain scenarios, followed by Random Forest and Decision Tree.

### Predictions
The analysis of Twitter data to anticipate stock market trends presents a compelling narrative when juxtaposed with macroeconomic indicators and company-specific stock data.
The integration of sentiment analysis from Twitter data alongside macroeconomic indicators offers a holistic view of market sentiment.
The quantitative assessment of sentiment provides valuable insights, with models such as Random Forests achieving high accuracy, recall, and F1 scores.

### Trends
The convergence of sentiment analysis with macroeconomic indicators and company-specific data further enriches the predictive landscape.
While sentiment analysis captures public perception and emotions, macroeconomic indicators offer a broader economic context.
Incorporating company-specific stock data provides granular insights into individual stock performance, illuminating the intricate relationships between sentiment, economic conditions, and market dynamics.
This holistic approach unveils the potential synergy between social sentiment and economic indicators in predicting market trends.


## Study subjects

### 500000 tweets
- Our preliminary findings reveal intriguing indications suggesting a plausible correlation between public sentiment reflected in Twitter discussions surrounding ChatGPT and generative AI and the subsequent impact on market valuation and trading activities concerning pertinent companies, gauged through stock prices. This study aims to forecast bullish or bearish stock market trends by leveraging sentiment analysis derived from an extensive dataset of 500,000 tweets. In conjunction with this sentiment analysis derived from Twitter, we incorporate control variables encompassing macroeconomic indicators, Twitter uncertainty index, and stock market data for several prominent companies

### 500000 tweets
- This research embarks on an exploration leveraging two prominent datasets recently published, both offering distinct yet complementary dimensions to the study. Firstly, the 500k ChatGPT-related Tweets dataset, sourced from Kaggle and meticulously curated by users, comprises over 500,000 tweets spanning December 2022 to March 2023. This rich dataset encompasses diverse attributes, including tweet text, temporal information, engagement metrics such as likes and retweets, user follower counts, and sentiment evaluations, all intricately associated with the ChatGPT conversational AI system

## Data analysis
- #method/consumer_price_index
- #method/twitter_uncertainty_index
- #method/gradient_boosting_classifier_model
- #method/consumer_confidence_index

## Findings
- For the identification of Bearish trends, Random Forest emerged as a prominent performer, showcasing a notable accuracy score of 82%, closely followed by Decision Tree at 81% and Extra Tree at 76%
- Gradient Boosting and Naive Bayes exhibited comparatively lower accuracies of 74% and 68%, respectively
- Extra Tree and Decision Tree followed with accuracies of 89% and 85%, respectively, while Gradient Boosting and Naive Bayes exhibited lower accuracy rates of 95% and 73%
- In Table 3, identifying Google Stock Bearish trends, Random Forest exhibited the highest accuracy at 96%, followed by Gradient Boosting (98%) and Extra Trees (90%)
- In identifying Bullish trends, Random Forest again emerged with the highest accuracy of 100%, followed by Decision Tree (89%) and Gradient Boosting (93%)

## Contributions
- In summary, the application of machine learning classifiers such as gradient boosting, decision tree, random forest, naive Bayes, and <mark class="fact">extra tree classifiers has been extensively explored in predicting stock market trends and prices</mark>. These models have been applied across diverse contexts and optimized for improved performance, demonstrating the significance of machine learning in stock market prediction.

## Limitations
- The study does not explicitly state its limitations, but it can be inferred that the study is limited to the analysis of tweets containing hashtags related to ChatGPT and the stock prices of key companies such as Microsoft and OpenAI. The study also relies on the accuracy of the natural language processing techniques and machine learning models used to extract features and predict stock price movements.
- The study does not discuss any limitations of the research, but potential limitations could include the limited scope of the study to five major tech companies and the potential for bias in the Twitter sentiment data.
- The limitations of the study include the potential overfitting or insufficient feature importance considerations of certain models, such as Decision Tree, and the limited suitability of models like Naive Bayes and Extra Tree for this task.

## Future work
- The study suggests that future research can focus on exploring the application of machine learning methodologies in constructing predictive models that assess the interconnection between tweet content and stock values. The study also suggests that future research can investigate the influence of social media rumors on stock market volatility.
- The study suggests that future work could involve exploring the use of other social media platforms and machine learning models to predict stock market trends.


## References
[^Agarwal_et+al_2021_a]: Agarwal, S., Kumar, S., &amp; Goel, U. (2021). Social media and the stock markets: an emerging market perspective. Journal of Business Economics and Management, 22(6), 1614-1632. https://doi.org/10.3846/jbem.2021.15619  [OA](https://doi.org/10.3846/jbem.2021.15619)  [Scite](/scite_tallies?query=https://doi.org/10.3846/jbem.2021.15619)

[^Ampomah_et+al_2020_a]: Ampomah, E. K., Qin, Z., &amp; Nyame, G. (2020). Evaluation of tree-based ensemble machine learning models in predicting the stock price direction of movement. Information, 11(6), 332. https://doi.org/10.3390/info11060332  [OA](https://doi.org/10.3390/info11060332)  [Scite](/scite_tallies?query=https://doi.org/10.3390/info11060332)

[^Alshammari_et+al_2022_a]: Alshammari, B. M., Aldhmour, F., AlQenaei, Z. M., &amp; Almohri, H. (2022). Stock market prediction by applying big data mining. Arab Gulf Journal of Scientific Research, 40(2), 139-152. https://doi.org/10.1108/AGJSR-05-2022-0053  [OA](https://doi.org/10.1108/AGJSR-05-2022-0053)  [Scite](/scite_tallies?query=https://doi.org/10.1108/AGJSR-05-2022-0053)

[^Almehmadi_2021_a]: Almehmadi, A. (2021). COVID-19 Pandemic Data Predict the Stock Market. Computer Systems Science &amp; Engineering, 36(3). https://doi.org/10.32604/csse.2021.015309  [OA](https://doi.org/10.32604/csse.2021.015309)  [Scite](/scite_tallies?query=https://doi.org/10.32604/csse.2021.015309)

[^Bagga_2022_a]: Bagga, A. R., &amp; Patel, H. (2022). Stock Market Forecasting using Ensemble Learning and Statistical Indicators. Journal of Engineering Research. https://doi.org/10.36909/jer.16629  [OA](https://doi.org/10.36909/jer.16629)  [Scite](/scite_tallies?query=https://doi.org/10.36909/jer.16629)

[^Eachempati_2023_a]: Eachempati, P., &amp; Srivastava, P. R. (2023). Prediction of the Stock Market From Linguistic Phrases: A Deep Neural Network Approach. Journal of Database Management (JDM), 34(1), 1-22. https://doi.org/10.4018/JDM.322020  [OA](https://doi.org/10.4018/JDM.322020)  [Scite](/scite_tallies?query=https://doi.org/10.4018/JDM.322020)

[^Ecer_et+al_2020_a]: Ecer, F., Ardabili, S., Band, S. S., &amp; Mosavi, A. (2020). Training a multilayer perceptron with genetic algorithms and particle swarm optimization for modeling stock price index prediction. Entropy, 22(11), 1239. https://doi.org/10.3390/e22111239  [OA](https://doi.org/10.3390/e22111239)  [Scite](/scite_tallies?query=https://doi.org/10.3390/e22111239)

[^Haque_et+al_2023_a]: Haque, M. S., Amin, M. S., &; Miah, J. (2023). Retail Demand Forecasting: A Comparative Study for Multivariate Time Series. arXiv e-prints. https://doi.org/10.48550/arXiv.2308.11939  [OA](https://doi.org/10.48550/arXiv.2308.11939)  [Scite](/scite_tallies?query=https://doi.org/10.48550/arXiv.2308.11939)

[^Khan_et+al_2023_a]: Khan, R. H., Miah, J., Arafat, S. M. Y., Syeed, M. M. M., &amp; Ca, D. M. (2023). Improving Traffic Density Forecasting in Intelligent Transportation  [OA](https://scholar.google.co.uk/scholar?q=Khan%2C%20R.H.%20Miah%2C%20J.%20Arafat%2C%20S.M.Y.%20Syeed%2C%20M.M.M.%20Improving%20Traffic%20Density%20Forecasting%20in%20Intelligent%20Transportation%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Khan%2C%20R.H.%20Miah%2C%20J.%20Arafat%2C%20S.M.Y.%20Syeed%2C%20M.M.M.%20Improving%20Traffic%20Density%20Forecasting%20in%20Intelligent%20Transportation%202023) 

[^Khan_et+al_2023_b]: Khan, R. H., Miah, J., Arafat, S. M., Syeed, M. M., &amp; Ca, D. M. (2023). Improving Traffic Density Forecasting in Intelligent Transportation Systems Using Gated Graph Neural Networks. arXiv preprint arXiv:2310.17729.  [OA](https://arxiv.org/abs/2310.17729)  

[^Khan_et+al_2023_c]: Khan, R. H., Miah, J., Rahat, M. A. R., Ahmed, A.H., Shahriyar M.A and Lipu, E.R. (2023). A Comparative Analysis of Machine Learning Approaches for Chronic Kidney Disease Detection, 2023 8th International Conference on Electrical, Electronics and Information Engineering (ICEEIE), Malang City, Indonesia, 2023, pp. 1-6, doi:10.1109/ICEEIE59078.2023.10334765.  [OA](https://doi.org/10.1109/ICEEIE59078.2023.10334765)  [Scite](/scite_tallies?query=https://doi.org/10.1109/ICEEIE59078.2023.10334765)

[^Khan_XXXX_a]: Khan, R. H., and Miah, J. (n.d). Performance Evaluation of a new one-time password (OTP) scheme using stochastic Petri net (SPN), 2022 IEEE World AI IoT Congress (AIIoT), Seattle, WA, USA, 2022. 407-412, doi:10.1109/AIIoT54504.2022.9817203.  [OA](https://doi.org/10.1109/AIIoT54504.2022.9817203)  [Scite](/scite_tallies?query=https://doi.org/10.1109/AIIoT54504.2022.9817203)

[^Liao_2023_a]: Liao, L., &amp; Huang, T. (2023). The Impact of Social Media Sentiment on the Stock Market Based on User Classification. In Digitalization and Management Innovation (pp. 1-16). IOS Press. https://doi.org/10.3233/FAIA230002  [OA](https://doi.org/10.3233/FAIA230002)  [Scite](/scite_tallies?query=https://doi.org/10.3233/FAIA230002)

[^Miah_et+al_2023_a]: Miah, J., Ca, D. M., Sayed, M. A., Lipu, E. R., Mahmud, F., &amp; Arafat, S. M. Y. (2023). Improving Cardiovascular Disease Prediction Through Comparative Analysis of Machine Learning Models: A Case Study on Myocardial Infarction. arXiv preprint, 2311.00517.  [OA](https://arxiv.org/abs/2311.00517)  

[^Miah_et+al_2023_b]: Miah, J., Cao, D. M., Sayed, M. A., &amp; Haque, M. S. (2023). Generative AI Model for Artistic Style Transfer Using Convolutional Neural Networks. arXiv preprint arXiv:2310.18237  [OA](https://arxiv.org/abs/2310.18237)  

[^Mabu_et+al_2023_a]: MAbu S., Tayaba, M., Islam, M. T., & Bishnu P G. (2023). Parkinson’s Disease Detection through Vocal Biomarkers and Advanced Machine Learning Algorithms. Journal of Computer Science and Technology Studies, 5(4), 142–149. https://doi.org/10.32996/jcsts.2023.5.4.14  [OA](https://doi.org/10.32996/jcsts.2023.5.4.14)  [Scite](/scite_tallies?query=https://doi.org/10.32996/jcsts.2023.5.4.14)

[^Mia_et+al_2023_a]: Mia, M. T., Ray, R. K., Ghosh, B. P., Chowdhury, M. S., Al-Imran, M., Das, R., Sarkar, M., Sultana, N., Nahian, S. A., &; Puja, A. R. (2023). Dominance of External Features in Stock Price Prediction in a Predictable Macroeconomic Environment. Journal of Business and Management Studies, 5(6), 128–133. https://doi.org/10.32996/jbms.2023.5.6.10  [OA](https://doi.org/10.32996/jbms.2023.5.6.10)  [Scite](/scite_tallies?query=https://doi.org/10.32996/jbms.2023.5.6.10)

[^Miah_et+al_2023_c]: Miah, J., Ca, D. M., Sayed, M. A., Lipu, E. R., Mahmud, F., &amp; Arafat, S. M. Y. (2023). Improving Cardiovascular Disease Prediction Through Comparative Analysis of Machine Learning Models: A Case Study on Myocardial Infarction. arXiv preprint, 2311.00517.  [OA](https://arxiv.org/abs/2311.00517)  

[^Miah_et+al_2023_d]: Miah, J., Cao, D. M., Sayed, M. A., Taluckder, M. S., Haque, M. S., &amp; Mahmud, F. (2023). Advancing Brain Tumor Detection: A Thorough Investigation of CNNs, Clustering, and SoftMax Classification in the Analysis of MRI Images. arXiv preprint arXiv:2310.17720.  [OA](https://arxiv.org/abs/2310.17720)  

[^Miah_2019_a]: Miah, J., &amp; Khan, R. H. (2019, November). Service Development of Smart Home Automation System: A Formal Method Approach. In Proceedings of the 2019 2nd International Conference on Computational Intelligence and Intelligent Systems (pp. 161-167).  [OA](https://scholar.google.co.uk/scholar?q=Miah%2C%20J.%20Khan%2C%20R.H.%20Service%20Development%20of%20Smart%20Home%20Automation%20System%3A%20A%20Formal%20Method%20Approach%202019-11) [GScholar](https://scholar.google.co.uk/scholar?q=Miah%2C%20J.%20Khan%2C%20R.H.%20Service%20Development%20of%20Smart%20Home%20Automation%20System%3A%20A%20Formal%20Method%20Approach%202019-11) 

[^Mendoza-Urdiales_et+al_2022_a]: Mendoza-Urdiales, R. A., Núñez-Mora, J. A., Santillán-Salgado, R. J., &; Valencia-Herrera, H. (2022). Twitter Sentiment Analysis and Influence on Stock Performance Using Transfer Entropy and EGARCH Methods. Entropy, 24(7), 874. https://doi.org/10.3390/e24070874  [OA](https://doi.org/10.3390/e24070874)  [Scite](/scite_tallies?query=https://doi.org/10.3390/e24070874)

[^Maqsood_et+al_2022_a]: Maqsood, H., Maqsood, M., Yasmin, S., Mehmood, I., Moon, J., &amp; Rho, S. (2022). Analyzing the stock exchange markets of EU nations: A case study of Brexit social media sentiment. Systems, 10(2), 24.https://doi.org/10.3390/systems10020024  [OA](https://doi.org/10.3390/systems10020024)  [Scite](/scite_tallies?query=https://doi.org/10.3390/systems10020024)

[^Miah_et+al_2023_e]: Miah, J., Ca, D. M., and Arafat, S. M. Y. (2023). Improving Cardiovascular Disease Prediction Through Comparative Analysis of Machine Learning Models: A Case Study on Myocardial Infarction, 2023 15th International Conference on Innovations in Information Technology (IIT), Al Ain, United Arab Emirates, 2023, pp. 49-54, doi:10.1109/IIT59782.2023.10366476.  [OA](https://doi.org/10.1109/IIT59782.2023.10366476)  [Scite](/scite_tallies?query=https://doi.org/10.1109/IIT59782.2023.10366476)

[^Nti_et+al_2019_a]: Nti, K. O., Adekoya, A., &amp; Weyori, B. (2019). Random forest-based feature selection of macroeconomic variables for stock market prediction. American Journal of Applied Sciences, 16(7), 200-212. https://doi.org/10.3844/ajassp.2019.200.212  [OA](https://doi.org/10.3844/ajassp.2019.200.212)  [Scite](/scite_tallies?query=https://doi.org/10.3844/ajassp.2019.200.212)

[^Pourroostaei_et+al_2023_a]: Pourroostaei Ardakani, S., Du, N., Lin, C., Yang, J. C., Bi, Z., &; Chen, L. (2023). A federated learning-enabled predictive analysis to forecast stock market trends. Journal of Ambient Intelligence and Humanized Computing, 14(4), 4529-4535. https://doi.org/10.1007/s12652-02304570-4  [OA](https://doi.org/10.1007/s12652-02304570-4)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s12652-02304570-4)

[^Sarkar_et+al_2023_a]: Sarkar, M., Ayon, E. H., Mia, M. T., Ray, R. K., Chowdhury, M. S., Ghosh, B. P., Al-Imran, M., Islam, M. T., Tayaba, M., &amp; Puja, A. R. (2023). Optimizing E-Commerce Profits: A Comprehensive Machine Learning Framework for Dynamic Pricing and Predicting Online Purchases. Journal of Computer Science and Technology Studies, 5(4), 186–193. https://doi.org/10.32996/jcsts.2023.5.4.19  [OA](https://doi.org/10.32996/jcsts.2023.5.4.19)  [Scite](/scite_tallies?query=https://doi.org/10.32996/jcsts.2023.5.4.19)

[^Syeed_et+al_2021_a]: Syeed, M. M., Khan, R. H., &amp; Miah, J. (2021). Agile Fitness of Software Companies in Bangladesh: An Empirical Investigation. International Journal of Advanced Computer Science and Applications, 12(2).  [OA](https://engine.scholarcy.com/oa_version?query=Syeed%2C%20M.M.%20Khan%2C%20R.H.%20Miah%2C%20J.%20Agile%20Fitness%20of%20Software%20Companies%20in%20Bangladesh%3A%20An%20Empirical%20Investigation%202021&author=Syeed&title=Agile%20Fitness%20of%20Software%20Companies%20in%20Bangladesh%3A%20An%20Empirical%20Investigation&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Syeed%2C%20M.M.%20Khan%2C%20R.H.%20Miah%2C%20J.%20Agile%20Fitness%20of%20Software%20Companies%20in%20Bangladesh%3A%20An%20Empirical%20Investigation%202021) [Scite](/scite_tallies?query=author%3ASyeed%2Ctitle%3AAgile%20Fitness%20of%20Software%20Companies%20in%20Bangladesh%3A%20An%20Empirical%20Investigation%2Cyear%3A2021)

[^Tayaba_et+al_2023_a]: Tayaba, M., Ayon, E. H., Mia, M. T., Sarkar, M., Ray, R. K., Chowdhury, M. S., Al-Imran, M., Nobe, N., Ghosh, B. P., Islam, M. T., &amp; Puja, A. R. (2023). Transforming Customer Experience in the Airline Industry: A Comprehensive Analysis of Twitter Sentiments Using Machine Learning and Association Rule Mining. Journal of Computer Science and Technology Studies, 5(4), 194–202. https://doi.org/10.32996/jcsts.2023.5.4.20  [OA](https://doi.org/10.32996/jcsts.2023.5.4.20)  [Scite](/scite_tallies?query=https://doi.org/10.32996/jcsts.2023.5.4.20)

[^Vlah_2020_a]: Vlah Jerić, S. (2020). Comparing classification algorithms for prediction on CROBEX data. Croatian Review of Economic, Business and Social Statistics, 6(2), 4-11. https://doi.org/10.2478/crebss-2020-0007  [OA](https://doi.org/10.2478/crebss-2020-0007)  [Scite](/scite_tallies?query=https://doi.org/10.2478/crebss-2020-0007)

[^Yin_et+al_2023_a]: Yin, L., Li, B., Li, P., &amp; Zhang, R. (2023). Research on a stock trend prediction method based on an optimized random forest. CAAI Transactions on Intelligence Technology, 8(1), 274-284. https://doi.org/10.1049/cit2.12067  [OA](https://doi.org/10.1049/cit2.12067)  [Scite](/scite_tallies?query=https://doi.org/10.1049/cit2.12067)

[^Zhang_et+al_2022_a]: Zhang, H., Chen, Y., Rong, W., et al. (2022). Effect of social media rumors on stock market volatility: A case of data mining in China. Frontiers. https://doi.org/10.3389/fphy.2022.987799   [OA](https://doi.org/10.3389/fphy.2022.987799)  [Scite](/scite_tallies?query=https://doi.org/10.3389/fphy.2022.987799)

