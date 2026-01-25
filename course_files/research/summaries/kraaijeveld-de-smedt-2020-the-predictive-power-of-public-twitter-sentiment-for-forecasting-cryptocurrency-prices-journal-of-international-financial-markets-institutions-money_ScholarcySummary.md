[[Kraaijeveld_PredictivePowerPublicTwitterSentiment_2020]]

# [The predictive power of public Twitter sentiment for forecasting cryptocurrency prices](https://doi.org/10.1016/j.intfin.2020.101188)

## [[Olivier Kraaijeveld]]; [[Johannes De Smedt]]

## Abstract

Cryptocurrencies have become a very popular topic recently, primarily due to their disruptive potential and reports of unprecedented returns. In addition, academics increasingly acknowledge Twitter's predictive power across a wide range of events, and more specifically in financial markets. This paper examines the extent to which public Twitter sentiment can predict price returns for the nine largest cryptocurrencies: Bitcoin, Ethereum, XRP, Bitcoin Cash, EOS, Litecoin, Cardano, Stellar, and TRON. Using a cryptocurrency-specific lexicon-based sentiment analysis approach, financial data, and bilateral Granger causality testing, it was found that Twitter sentiment has predictive power for the returns of Bitcoin, Bitcoin Cash, and Litecoin. Using a bullishness ratio, predictive power is found for EOS and TRON. Finally, a heuristic approach is developed to discover that at least 1–14% of the obtained Tweets were posted by Twitter ‘‘bot” accounts. This paper is the first to examine the predictive power of Twitter sentiment across multiple cryptocurrencies and to explore the presence of cryptocurrency-related Twitter bots.

## Key concepts

# claim/TRON; #TRON; #bots; #claim/bitcoin_cash; #bitcoin_cash; #financial_market; #finding/twitter; #twitter; #claim/price_return; #price_return; #predictive_power; #cryptocurrencies; #sentiment_analysis

## Quote

This study examines the predictive power of Twitter sentiment for the price returns of the nine largest cryptocurrencies, finding that Twitter sentiment can predict the price returns of Bitcoin, Bitcoin Cash, and Litecoin, and that predictive power for EOS and TRON can be achieved using a bullishness ratio.

## Key points

- Cryptocurrencies are digital currencies that make use of blockchain technology, a disruptive, decentralised, and cryptographic technology that enables the digitalisation of trust
- Bullishness is observed to be a strong effect of price returns, indicating that Twitter users Tweet more positively or negatively depending on Bitcoin’s price returns
- While the potential of cryptocurrencies reaches far beyond prices, this study has researched to what extent public Twitter sentiment can be used to forecast the prices of the nine largest cryptocurrencies by market capitalisation
- By implementing a robust cryptocurrency-specific lexicon-based sentiment analysis approach in combination with bivariate Granger-causality tests, it was found that Twitter sentiment can be used to predict the price returns of Bitcoin, Bitcoin Cash, and Litecoin
- Predictive power for price returns was found for EOS and TRON
- By applying a set of heuristics to estimate the presence of cryptocurrency-related Twitter bots, it was found that 1–14% of the Tweets in the obtained datasets were posted by bots

## Summary

### Introduction

The study examines the predictive power of public Twitter sentiment for forecasting cryptocurrency prices.
It focuses on the nine largest cryptocurrencies and uses a cryptocurrency-specific lexicon-based sentiment analysis approach, financial data, and bilateral Granger-causality testing.
The study finds that Twitter sentiment has predictive power for the returns of Bitcoin, Bitcoin Cash, and Litecoin, and a bullishness ratio shows predictive power for EOS and TRON.

### Cryptocurrency Market

Cryptocurrencies are digital currencies that use blockchain technology, a disruptive, decentralized, and cryptographic technology.
The market is highly volatile due to limited regulation, a lack of institutional guarantor, and a speculative nature.
The study reviews the theoretical foundations and related works on cryptocurrencies, Twitter sentiment analysis, and bot identification.
It also discusses the challenges in defining the asset class of cryptocurrencies, which share characteristics from various existing asset classes.

### Twitter Sentiment Analysis

The study uses a sentiment analysis tool specifically constructed for cryptocurrency-related Tweets, accounting for jargon.
It finds that at least 1-14% of the obtained Tweets were posted by Twitter "bot" accounts, which may affect the findings.
The study's results are supported by related work that reported promising results using Twitter sentiment to predict financial markets.
The findings of this study contribute to understanding the predictive power of Twitter sentiment across multiple cryptocurrencies and to the exploration of the presence of cryptocurrency-related Twitter bots.

### Market Efficiency

The cryptocurrency market is considered inefficient, with studies such as Urquhart (2016), Mensi et al (2019), and Sensoy (2019) finding that Bitcoin and other cryptocurrency markets do not fully reflect available information in market prices.
The Adaptive Markets Hypothesis (AMH) is deemed a more appropriate framework for studying the cryptocurrency market, as it accounts for the coexistence of rationality and irrationality in financial markets.
The AMH suggests that markets are competitive and adaptive, with varying degrees of efficiency over time.

### Sentiment Analysis

Sentiment analysis is a crucial aspect of understanding financial markets, with Twitter sentiment analysis being a valuable tool for extracting emotional intelligence and predicting market movements.
Studies such as Bollen et al (2011) and Li et al (2017) have demonstrated the effectiveness of Twitter sentiment analysis in predicting stock prices and financial markets.
Twitter data is a rich source of information that can affect markets, and sentiment analysis can assign a positive, negative, or neutral polarity score to unstructured text.
The predictive power of Twitter sentiment for financial markets is generally strongest between 1 and 4 days.
Most related works use a sentiment analysis approach, combined with regression models or Granger causality tests, to examine the predictive power of Twitter sentiment in financial markets.
Studies that use a hybrid or lexicon-based approach often draw on the Loughran & McDonald financial corpus and/or the Harvard IV-4 psychological corpus.
The sentiment analysis showed that the polarity scores for all nine cryptocurrencies are relatively constant over time, with a mean polarity of 0.33.
The results also suggest a seasonal pattern in the hourly sentiment, with a bullish trend in the first 12 hours and a bearish trend in the next 12 hours.
Outliers in the sentiment polarity time series occur sporadically and usually quickly recover.
Twitter sentiment can be used to predict the price returns of Bitcoin, Bitcoin Cash, and Litecoin.
A bullishness ratio also showed predictive power for price returns of EOS and TRON.
The strongest predictors on the daily level are Twitter sentiment and message volume.

### Price Driving Factors

Cryptocurrency prices are influenced by a range of internal and external factors, including supply and demand, mining difficulty, market trends, and macroeconomic factors.
Other factors that affect cryptocurrency prices include the S&p 500, gold prices, the USD/EUR exchange rate, Twitter mentions, news sentiment and volume, speculation, regulation announcements, and Initial Coin Offerings (ICOs).
Understanding these factors is essential for predicting cryptocurrency prices and identifying potential investment opportunities.

### Cryptocurrency Research

Researchers have used forum posts and news articles to perform sentiment analysis and predict fluctuations in Bitcoin’s price.
Most researchers acknowledge the predictive power of social media and news sentiment for Bitcoin prices and/or trading volume in the short-term and long-term.
The volume of posts or messages also correlates with Bitcoin’s trading volume.

### Methodology

This study focuses on predicting the price returns of the nine largest cryptocurrencies, ranked by market capitalisation.
The data collection is divided into two sections: collecting Tweets from Twitter and collecting financial data from CoinMarketCap.
A live stream crawler was implemented using the Twitter API to collect Tweets, and the CoinMarketCap API to collect financial data at daily and hourly intervals.
The collected Twitter data requires extensive pre-processing to be useful for sentiment analysis, including tokenisation, normalisation, and removal of noise.
The study used a simple heuristic approach to test for the presence of Twitter bots in the collected data, proposing six heuristics based on findings from previous studies and patterns found through manual inspection of the datasets.
A Tweet was considered to be posted by a cryptocurrency bot if it met two or more of the following criteria: containing "give away" or "giving away", containing "pump" and either "register" or "join", containing more than 14 hashtags, containing more than 14 ticker symbols, having a platform source containing "bot", or having a user with less than 1000 accounts followed and a high follower-to-following ratio.
The study also used the Valence Aware Dictionary and Sentiment Reasoner (VADER) algorithm for sentiment analysis, combining it with the Loughran &amp; McDonald financial corpus and a manually compiled cryptocurrency lexicon.

### Data Preprocessing

The study applied various preprocessing techniques to the Twitter data, including removing "RT" if present, applying case-folding, removing hashtags if they were not in the Reuters corpus, expanding contractions, removing ticker symbols, removing tokens containing numerical characters, applying WordNet lemmatisation, and removing stop words using a custom list.
The total number of Tweets after preprocessing was 22,912,039.
The study also used UTC-1 timestamps for all data to mitigate potential time differences between the Twitter and financial datasets.

### Granger-Causality Testing

The study applied the augmented Toda & Yamamoto Granger-causality test to explore whether certain factors were driving prices, using daily and hourly Twitter sentiment, bullishness, and message volume as independent variables to assess their predictive power for price returns and daily trading volume.
The study also used the Breusch-Godfrey LM test to evaluate autocorrelation in the residuals and applied Johansen's Trace and Maximum Eigenvalue tests to test the validity of the results for series that involved at least one non-stationary series.
The study found that Twitter sentiment has predictive power for the price returns of Bitcoin, Bitcoin Cash, and Litecoin.
The results vary across different cryptocurrencies and levels of analysis.
Twitter sentiment is found to be a strong predictor on the intraday level, followed by bullishness and message volume.
The study suggests that Twitter is slightly more of a "cause" than an "effect" of the cryptocurrency market on the daily level.

### Bot Accounts

The study found that the lowest percentage of bot accounts is for Bitcoin, while the largest relative presence of bot accounts is observed for Tweets related to Cardano.
The actual number of Twitter bots in the cryptocurrency space is likely higher than the observed percentages suggest.
The results are close to the estimated 8.5% of all Twitter accounts being bot accounts.

### Predictive Power

Message volume predicts price returns for Litecoin and XRP, but for most other cryptocurrencies, price returns help predict message volume, suggesting that investors simply respond to the market.
The strongest predictor variable on the intraday level is price returns.

### Future Research

Cryptocurrencies form a young and uncharted research topic, with many areas available for future research.
Suggestions for future research include applying this research to a larger set of cryptocurrencies, extending the observation period, experimenting with different levels of granularity, and investigating the effects of user/social influence.
Additionally, researching the presence and effects of cryptocurrency-related Twitter bots on prices and/or trading volumes could be a valuable area of study.

## Study subjects

### 9 datasets with a total of 24,035

- 3.1.1. Twitter data: Tweets were obtained separately for each cryptocurrency between 4 June 2018 and 4 August 2018, resulting in 9 datasets totaling 24,035,075 public Tweets. A live stream crawler was implemented using the Twitter API, which continuously stored Tweets as they were posted in real-time

## Data analysis

- #method/vector_error_correction_models
- #method/breusch_godfrey_lm_test
- #method/
- #method/vader_algorithm
- #method/var_model

## Findings

- From the peak of the market in December 2017 to October 2018, the market has lost more than 75% of its value (CoinMarketCap, 2018)
- It was found that a prolonged manipulation campaign accounted for 50% of Bitcoin’s price increase and 64% of major altcoin price increases between March 2017 and March 2018
- Although the work of [^Bollen_et+al_2011_a] is remarkable with an accuracy of 86.7%, the study has also been heavily criticised for making incorrect statistical assumptions ([^Lachanski_2017_a])
- The authors obtained an accuracy of 89.6% and only found a short-term correlation between positive <a class="keyword" href="https://en.wikipedia.org/wiki/Twitter" title="Twitter">Twitter</a> sentiment and Bitcoin’s price
- Results per cryptocurrency. For the daily intervals of Bitcoin, <a class="keyword" href="https://en.wikipedia.org/wiki/Twitter" title="Twitter">Twitter</a> sentiment (p &lt; 0.01) and bullishness (p &lt; 0.05) strongly affect the trading volume for various lags

## Builds on previous research

- This study distinguishes two types of factors that can affect cryptocurrency prices: internal factors (e.g., supply, demand, and mining difficulty) and external factors (e.g., market trends and macro-economic factors). Other factors that affect cryptocurrency prices include, but are not limited to, the S&p 500 (Sovbetov, 2018), gold prices ([^Poyser_2017_a]), the USD/EUR exchange rate ([^Georgoula_et+al_2015_a]), mining difficulty (Li and Wang, 2017), the political situation of a country (e.g. Venezuela) ([^Poyser_2017_a]), Twitter mentions (Li and Wang, 2017), news sentiment and volume ([^Polasik_et+al_2015_a]), speculation (Sovbetov, 2018), regulation announcements, Initial Coin Offerings (ICO)6, hard forks7, airdrops8, cryptocurrency exchange hacks and cryptocurrency exchange (de)-listings.
- In addition, [^Mai_et+al_2015_a] incorporates intraday analysis and shows that Twitter posts are useful for predicting Bitcoin returns at an hourly interval. However, this study was limited by Bitcoin’s price being sourced from only one exchange.

## Differs from previous work

- In addition, a study by Dyhrberg (2016) analyzes Bitcoin by using GARCH-modelling and finds that Bitcoin shows several similarities to gold and the USD. A more recent study by [^Baur_et+al_2018_a]) finds that Bitcoin is a speculative asset and not an alternative currency.
- The EMH is the neoclassical standard theory of financial markets, but it focuses less on the behavioural and emotional effects that market actors have on prices. Given the more behavioural nature of this work and the strong presence of emotionally driven investment decisions, as evidenced by the volatility in the cryptocurrency market, the Adaptive Markets Hypothesis (AMH) proposed by [^Lo_2004_a] is deemed a more appropriate framework for this study. [^Lo_2004_a] argues that the EMH is not wrong but merely incomplete because it does not fully explain market behaviour as irrationality and rationality coexist in financial markets.

## Confirmation of earlier findings

- Fig. 2 also shows the percentage distribution of the number of bot characteristics per cryptocurrency. The results in Table 4 are close to the aforementioned Twitter estimates, which reported that 8.5% of all Twitter accounts are bot accounts ([^Subrahmanian_et+al_2016_a]).
- The scores are also consistently positively skewed with a mean polarity of 0.33. This is consistent with the results of [^Kennedy_2006_a], who observe that lexicon-based approaches generally have a positive bias, which can be attributed to a human tendency to prefer positive language.
- Fig. 4 interestingly suggests that, particularly for Bitcoin and Ethereum, their daily message and trading volume, respectively, follow very correlated patterns. Although no immediate cause for this is known, it would align with the findings of the study by [^Ciaian_et+al_2018_a]), who observe that Bitcoin and altcoin markets are strongly correlated.

## Contributions

- Over the course of 2017 and early 2018, the cryptocurrency market received large-scale attention due to its extreme value gains and losses. While the potential of cryptocurrencies reaches far beyond prices, <mark class="fact">this study has researched to what extent public Twitter sentiment can be used to forecast the prices of the</mark> nine largest cryptocurrencies by market capitalisation.

## Limitations

- The study has several limitations, including the fact that the data collection is limited to a specific time period and that the study only examines the nine largest cryptocurrencies by market capitalization. Additionally, the study notes that the possible effects of Twitter bots on sentiment and/or prices have not researched.

## Future work

- The study suggests several avenues for future research, including applying the research to a larger set of cryptocurrencies, extending the period of observation, and experimenting with various levels of granularity. The study also suggests testing the reproducibility of the research by trying to replicate the results or using the findings to predict price returns.
- The study suggests several areas for future research, including applying the study to a larger set of cryptocurrencies, extending the period of observation, and experimenting with different levels of granularity. The study also suggests researching the effects of user and social influence on Twitter sentiment and cryptocurrency prices.

## References

[^Baur_et+al_2018_a]: Baur, D.G., Hong, K.H., Lee, A.D., 2018. Bitcoin: Medium of exchange or speculative asset? J. Int. Financ. Markets Inst. Money 54, 177–189. Bitinfocharts.com, 2018. Cryptocurrency Statistics.  [OA](https://engine.scholarcy.com/oa_version?query=Baur%2C%20D.G.%20Hong%2C%20K.H.%20Lee%2C%20A.D.%20Bitcoin%3A%20Medium%20of%20exchange%20or%20speculative%20assets%3F%202018&author=Baur&title=Bitcoin%3A%20Medium%20of%20exchange%20or%20speculative%20assets%3F&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Baur%2C%20D.G.%20Hong%2C%20K.H.%20Lee%2C%20A.D.%20Bitcoin%3A%20Medium%20of%20exchange%20or%20speculative%20assets%3F%202018) [Scite](/scite_tallies?query=author%3ABaur%2Ctitle%3ABitcoin%3A%20Medium%20of%20exchange%20or%20speculative%20assets%3F%2Cyear%3A2018)

[^Bollen_et+al_2011_a]: Bollen, J., Mao, H., Zeng, X., 2011. Twitter mood predicts the stock market. J. Comput. Sci. 2 (1), 1–8.  [OA](https://engine.scholarcy.com/oa_version?query=Bollen%2C%20J.%20Mao%2C%20H.%20Zeng%2C%20X.%20Twitter%20mood%20predicts%20the%20stock%20market%202011&author=Bollen&title=Twitter%20mood%20predicts%20the%20stock%20market&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Bollen%2C%20J.%20Mao%2C%20H.%20Zeng%2C%20X.%20Twitter%20mood%20predicts%20the%20stock%20market%202011) [Scite](/scite_tallies?query=author%3ABollen%2Ctitle%3ATwitter%20mood%20predicts%20the%20stock%20market%2Cyear%3A2011)

[^Ciaian_et+al_2018_a]: Ciaian, P., Rajcaniova, M., Kancs, D., 2018. Virtual relationships: short- and long-run evidence from Bitcoin and altcoin markets. J. Int. Financ. Markets Inst.  [OA](https://engine.scholarcy.com/oa_version?query=Ciaian%2C%20P.%20Rajcaniova%2C%20M.%20Kancs%2C%20D.%20Virtual%20relationships%3A%20short-%20and%20long-run%20evidence%20from%20Bitcoin%20and%20altcoin%20markets%202018&author=Ciaian&title=Virtual%20relationships%3A%20short-%20and%20long-run%20evidence%20from%20Bitcoin%20and%20altcoin%20markets&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Ciaian%2C%20P.%20Rajcaniova%2C%20M.%20Kancs%2C%20D.%20Virtual%20relationships%3A%20short-%20and%20long-run%20evidence%20from%20Bitcoin%20and%20altcoin%20markets%202018) [Scite](/scite_tallies?query=author%3ACiaian%2Ctitle%3AVirtual%20relationships%3A%20short-%20and%20long-run%20evidence%20from%20Bitcoin%20and%20altcoin%20markets%2Cyear%3A2018)

[^Georgoula_et+al_2015_a]: Georgoula, I., Pournarakis, D., Bilanakos, C., Sotiropoulos, D.N., Giaglis, G.M., 2015. Using time-series and sentiment analysis to detect the determinants of bitcoin prices. SSRN Electron. J. Giachanou, A., Crestani, F., 2016. Like it or not: a survey of Twitter sentiment analysis methods. ACM Comput. Surv. 49 (2), 1–41.  [OA](https://engine.scholarcy.com/oa_version?query=Georgoula%2C%20I.%20Pournarakis%2C%20D.%20Bilanakos%2C%20C.%20Sotiropoulos%2C%20D.N.%20Using%20time-series%20and%20sentiment%20analysis%20to%20detect%20the%20determinants%20of%20bitcoin%20prices%202015&author=Georgoula&title=Using%20time-series%20and%20sentiment%20analysis%20to%20detect%20the%20determinants%20of%20bitcoin%20prices&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Georgoula%2C%20I.%20Pournarakis%2C%20D.%20Bilanakos%2C%20C.%20Sotiropoulos%2C%20D.N.%20Using%20time-series%20and%20sentiment%20analysis%20to%20detect%20the%20determinants%20of%20bitcoin%20prices%202015) [Scite](/scite_tallies?query=author%3AGeorgoula%2Ctitle%3AUsing%20time-series%20and%20sentiment%20analysis%20to%20detect%20the%20determinants%20of%20bitcoin%20prices%2Cyear%3A2015)

[^Kennedy_2006_a]: Kennedy, A., Inkpen, D., 2006. Sentiment classification of movie reviews using contextual valence shifters. Comput. Intell. 22 (2), 110–125.  [OA](https://engine.scholarcy.com/oa_version?query=Kennedy%2C%20A.%20Inkpen%2C%20D.%20Sentiment%20classification%20of%20movie%20reviews%20using%20contextual%20valence%20shifters%202006&author=Kennedy&title=Sentiment%20classification%20of%20movie%20reviews%20using%20contextual%20valence%20shifters&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Kennedy%2C%20A.%20Inkpen%2C%20D.%20Sentiment%20classification%20of%20movie%20reviews%20using%20contextual%20valence%20shifters%202006) [Scite](/scite_tallies?query=author%3AKennedy%2Ctitle%3ASentiment%20classification%20of%20movie%20reviews%20using%20contextual%20valence%20shifters%2Cyear%3A2006)

[^Lachanski_2017_a]: Lachanski, M., Pav, S., 2017. Shy of the character limit: Twitter mood predicts the stock market revisited. Econ J. Watch 14 (3), 302.  [OA](https://engine.scholarcy.com/oa_version?query=Lachanski%2C%20M.%20Pav%2C%20S.%20Shy%20of%20the%20character%20limit%3A%20Twitter%20mood%20predicts%20the%20stock%20market%20revisited%202017&author=Lachanski&title=Shy%20of%20the%20character%20limit%3A%20Twitter%20mood%20predicts%20the%20stock%20market%20revisited&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Lachanski%2C%20M.%20Pav%2C%20S.%20Shy%20of%20the%20character%20limit%3A%20Twitter%20mood%20predicts%20the%20stock%20market%20revisited%202017) [Scite](/scite_tallies?query=author%3ALachanski%2Ctitle%3AShy%20of%20the%20character%20limit%3A%20Twitter%20mood%20predicts%20the%20stock%20market%20revisited%2Cyear%3A2017)

[^Lo_2004_a]: Lo, A.W., 2004. The adaptive markets hypothesis: Market efficiency from an evolutionary perspective.  [OA](https://scholar.google.co.uk/scholar?q=Lo%2C%20A.W.%20The%20adaptive%20markets%20hypothesis%3A%20Market%20efficiency%20from%20an%20evolutionary%20perspective%202004) [GScholar](https://scholar.google.co.uk/scholar?q=Lo%2C%20A.W.%20The%20adaptive%20markets%20hypothesis%3A%20Market%20efficiency%20from%20an%20evolutionary%20perspective%202004)

[^Mai_et+al_2015_a]: Mai, F., Bai, Q., Shan, Z., Wang, X.S., Chiang, R.H., 2015. From Bitcoin to big coin: the impacts of social media on Bitcoin performance. SSRN Electron. J., 1–16 Mai, F., Shan, Z., Bai, Q., Wang, X.S., Chiang, R.H., 2018. How does social media impact Bitcoin value? A test of the silent majority hypothesis. J. Manage.  [OA](https://engine.scholarcy.com/oa_version?query=Mai%2C%20F.%20Bai%2C%20Q.%20Shan%2C%20Z.%20Wang%2C%20X.S.%20From%20Bitcoin%20to%20big%20coin%3A%20the%20impacts%20of%20social%20media%20on%20Bitcoin%20performance%202015&author=Mai&title=From%20Bitcoin%20to%20big%20coin%3A%20the%20impacts%20of%20social%20media%20on%20Bitcoin%20performance&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Mai%2C%20F.%20Bai%2C%20Q.%20Shan%2C%20Z.%20Wang%2C%20X.S.%20From%20Bitcoin%20to%20big%20coin%3A%20the%20impacts%20of%20social%20media%20on%20Bitcoin%20performance%202015) [Scite](/scite_tallies?query=author%3AMai%2Ctitle%3AFrom%20Bitcoin%20to%20big%20coin%3A%20the%20impacts%20of%20social%20media%20on%20Bitcoin%20performance%2Cyear%3A2015)

[^Polasik_et+al_2015_a]: Polasik, M., Piotrowska, A.I., Wisniewski, T.P., Kotkowski, R., Lightfoot, G., 2015. Price fluctuations and the use of Bitcoin: an empirical inquiry. Int. J. Electron.  [OA](https://engine.scholarcy.com/oa_version?query=Polasik%2C%20M.%20Piotrowska%2C%20A.I.%20Wisniewski%2C%20T.P.%20Kotkowski%2C%20R.%20Price%20fluctuations%20and%20the%20use%20of%20Bitcoin%3A%20an%20empirical%20inquiry%202015&author=Polasik&title=Price%20fluctuations%20and%20the%20use%20of%20Bitcoin%3A%20an%20empirical%20inquiry&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Polasik%2C%20M.%20Piotrowska%2C%20A.I.%20Wisniewski%2C%20T.P.%20Kotkowski%2C%20R.%20Price%20fluctuations%20and%20the%20use%20of%20Bitcoin%3A%20an%20empirical%20inquiry%202015) [Scite](/scite_tallies?query=author%3APolasik%2Ctitle%3APrice%20fluctuations%20and%20the%20use%20of%20Bitcoin%3A%20an%20empirical%20inquiry%2Cyear%3A2015)

[^Poyser_2017_a]: Poyser, O., 2017. Exploring the determinants of Bitcoin’s price: an application of Bayesian Structural Time Series. arXiv preprint: 1706.01437.  [OA](https://arxiv.org/abs/1706.01437)  

[^Subrahmanian_et+al_2016_a]: Subrahmanian, V., Azaria, A., Durst, S., Kagan, V., Galstyan, A., Lerman, K., Zhu, L., Ferrara, E., Flammini, A., Menczer, F., 2016. The DARPA Twitter Bot  [OA](https://scholar.google.co.uk/scholar?q=Subrahmanian%20V%20Azaria%20A%20Durst%20S%20Kagan%20V%20Galstyan%20A%20Lerman%20K%20Zhu%20L%20Ferrara%20E%20Flammini%20A%20Menczer%20F%202016%20The%20DARPA%20Twitter%20Bot) [GScholar](https://scholar.google.co.uk/scholar?q=Subrahmanian%20V%20Azaria%20A%20Durst%20S%20Kagan%20V%20Galstyan%20A%20Lerman%20K%20Zhu%20L%20Ferrara%20E%20Flammini%20A%20Menczer%20F%202016%20The%20DARPA%20Twitter%20Bot)
