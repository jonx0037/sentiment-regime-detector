[[Renault_IntradayOnlineInvestorSentimentReturn_2017]]

# [Intraday online investor sentiment and return patterns in the U.S. stock market](https://doi.org/10.1016/j.jbankfin.2017.07.002)

## [[Thomas Renault]]

## Abstract

We first implement a novel approach to derive investor sentiment from social media messages, then explore the relationship between online investor sentiment and intraday stock returns. Using an extensive dataset of messages posted on the microblogging platform StockTwits, we construct a lexicon of words used by online investors when they share opinions and ideas about the bullishness or the bearishness of the stock market. We demonstrate that a transparent, replicable approach significantly outperforms standard dictionary-based methods in the literature while remaining competitive with more complex machine learning algorithms. Aggregating individual message sentiment at half-hour intervals, we provide empirical evidence that online investor sentiment helps forecast intraday stock index returns. After controlling for past market returns, we find that the first half-hour change in investor sentiment predicts the last half-hour return of the S&P 500 index ETF. Examining users’ self-reported investment approach, holding period, and experience level, we find that the intraday sentiment effect is driven by shifts in novice traders' sentiment. Overall, our results provide direct empirical evidence of sentiment-driven intraday noise trading.

## Key concepts

# finding/machine_learning; #machine_learning; #investor_sentiment; #maximum_entropy; #claim/empirical_evidence; #empirical_evidence; #claim/stock_market; #stock_market; #social_media

## Quote

The study examines the relationship between online investor sentiment and intraday S&P 500 index ETF returns, finding that the first half-hour change in sentiment predicts the last half-hour return, with the sentiment effect mainly driven by novice traders.

## Key points

- Since the pioneering work of [^Antweiler_2004_a] and [^Das_2007_a] on the predictability of stock markets using data from Internet message boards, a growing number of researchers have tried to “explore” the Web to provide forecasts for the financial markets (see [^Nardo_et+al_2016_a] for a survey of the literature)
- We report the percentage of correct classification excluding unclassified messages CC, the percentage of correct classification per class, the percentage of classified messages CM, and the percentage of classified messages per class (CMbull and CMbear)
- In the first part of this paper, we construct a lexicon of words used by online investors when they share opinions and ideas about the bullishness or bearishness of the stock market by using an extensive dataset of messages for which sentiment is explicitly revealed by investors
- We demonstrate that a transparent and replicable approach significantly outperforms the benchmark dictionaries used in the literature while remaining competitive with more complex machine learning algorithms
- We explore the relation between online investor sentiment and intraday S&P 500 index ETF returns
- We focused on the predictability of aggregate market returns. We believe that the evolution of intraday investor sentiment over time and across users with different trading approaches, experiences, and investment horizons can be useful in many other situations, such as explaining the cross-section of average stock returns or forecasting stock market volatility

## Summary

### Sentiment Analysis

The study implements a novel approach to derive investor sentiment from social media messages, using a field-specific weighted lexicon (L1) and a field-specific non-weighted lexicon (L2) to classify sentiment.
The results show that L1, L2, and a supervised machine learning algorithm (M1) significantly outperform standard dictionary-based approaches.
The study also examines the relationship between online investor sentiment and intraday stock returns, finding that the first half-hour change in investor sentiment predicts the last half-hour returns of the S&P 500 index ETF.
The study reviews two approaches for textual sentiment analysis: dictionary-based classification and machine learning classification.
Dictionary-based classification involves computing a sentiment variable by counting the number of positive and negative words in a document using a predefined list of signed words.
Machine learning classification predicts sentiment classes from a set of features, such as words in a document.
The study highlights the limitations of dictionary-based approaches, including the need for field-specific dictionaries and the potential for overfitting.
The study analyzes the sentiment of user-generated content on StockTwits, a social media platform, to predict stock returns.
The authors use five different classifiers to derive sentiment scores and find that the first half-hour change in investor sentiment predicts the last half-hour stock market return.
The correlation coefficient between two of the sentiment indicators, sL1 and sM1, is high (0.9341), indicating that quantifying sentiment using a weighted field-specific lexicon is competitive with more complex machine learning methods.
The paper constructs a lexicon of words used by online investors to share opinions about the stock market, demonstrating that a transparent and replicable approach outperforms benchmark dictionaries and is competitive with complex machine learning algorithms.
The findings provide empirical evidence for developing a field-specific lexicon and for using simpler approaches over complex methods.
The paper also explores the relation between online investor sentiment and intraday S&P 500 index ETF returns, finding that the first half-hour change in investor sentiment predicts the last half-hour return.

### Intraday Return Predictability

The study provides empirical evidence that online investor sentiment helps forecast intraday stock index returns.
After controlling for past market returns, the study finds that the first half-hour change in investor sentiment predicts the last half-hour return of the S&P 500 index ETF.
Predictability disappears when sentiment is computed using standard dictionary-based methods.
The study also finds that the intraday sentiment effect is mainly driven by shifts in novice traders' sentiment.

### Market Efficiency

The study supports the role of investor sentiment in predicting intraday stock returns, adding to the existing literature on market efficiency.
The results contrast with previous findings, demonstrating that the intraday price momentum has disappeared during the most recent sample period.
The study also demonstrates that the intraday sentiment-driven anomaly is very short-lived: a positive sentiment-driven price pressure on day t is followed by a price reversal the next day.

### Data Collection

The study collects data from StockTwits, a social microblogging platform, between January 1, 2012, and December 31, 2016.
The dataset contains 59,598,856 messages from 239,996 distinct users, with 9,434,321 messages classified as bullish (15.85%) and 2,286,292 as bearish (3.84%).
The remaining messages are unclassified.
The data is stored in a MongoDB NoSQL database, with each message including a unique identifier, username, message content, timestamp, and sentiment.
The study collected a dataset of 750,000 messages from StockTwits, with 375,000 "bullish" messages and 375,000 "bearish" messages.
The data was preprocessed by removing stopwords, adding negation prefixes, and replacing tickers, links, and user mentions with common words.
The study used a bag-of-words approach to extract unigrams and bigrams and to calculate the sentiment weight for each term.

### Research Methodology

The study aims to explore the relation between online investor sentiment and intraday stock returns, with a focus on user-generated content on StockTwits.
The study uses a transparent, replicable measure of investor sentiment, enabling a direct test of the noise-trading hypothesis.
The paper is structured to describe the StockTwits platform, review the differences between dictionary-based methods and machine learning techniques, and explore the relationship between online investor sentiment and intraday stock returns.

### Lexicon Creation

The study created two lexicons: L1, a weighted field-specific lexicon, and L2, a manual field-specific lexicon.
L1 was created by sorting all n-grams by their sentiment weight and selecting the top and bottom quintiles.
L2 was created by manually classifying each n-gram as positive, negative, or neutral.
The study found that L1 and L2 had a higher accuracy than benchmark dictionary-based approaches.

### Classification Accuracy

The study evaluated the accuracy of L1, L2, and other classifiers using a time-order evaluation holdout.
The results showed that L1 and L2 achieved higher accuracy than benchmark dictionary-based approaches, with L1 achieving 74.62% and L2 achieving 76.36%.
The study also found that the supervised machine learning method M1 had a slightly higher accuracy than L1, but that the results were qualitatively similar when using L1, L2, or M1 to compute intraday investor sentiment indicators.

### Predictive Regressions

The authors run predictive regressions to explore the relation between changes in intraday investor sentiment and the half-hour S&P 500 ETF return.
They find that the first half-hour change in investor sentiment predicts the last half-hour stock market return, with significant, positive coefficients at the 0.1% level when investor sentiment is computed using L1 or M1.
The R2 values are comparable to those reported in previous studies.

### Intraday Sentiment Effect

The study examines whether the intraday sentiment effect is driven by the release of macroeconomic news before the market opens or during the trading day.
The authors find that the intraday sentiment effect is concentrated on days without macroeconomic news announcements.
They also analyze whether users' self-reported investment approach, holding period, and experience level contain value-relevant information to understand the reason behind the intraday sentiment effect.

### Sentiment Effect

The study finds that investor sentiment, as measured by StockTwits data, has a significant impact on stock prices, particularly in the last half-hour of the trading day.
The sentiment effect is driven by noise trading, with novice traders and those using technical analysis strategies contributing most to it.
The first half-hour change in investor sentiment predicts the return in the last half-hour, with a significant price reversal on the next trading day.

### Investor Heterogeneity

The study analyzes the heterogeneity of investors based on their self-reported investment approach, holding period, and experience level.
The results show that traders with technical, growth, and value investing strategies, as well as position traders, drive the sentiment effect.
The significance of the results decreases with traders' self-reported experience, with novice investors having the most significant impact.

### Trading Strategies

The study evaluates the performance of a sentiment-driven trading strategy that buys or sells the S&P 500 ETF based on changes in novice investor sentiment during the first half-hour of the day.
The strategy outperforms other benchmark strategies, with an average annualized return of 4.55% and a Sharpe ratio of 1.496.
The results provide empirical evidence of sentiment-driven intraday noise trading.

### Noise Trading

The paper finds that the sentiment effect is mainly driven by shifts in novice traders' sentiment, and that a strategy using changes in novice investors' sentiment as trading signals significantly outperforms other baseline strategies.
The results provide direct empirical evidence of intraday sentiment-driven noise trading: short-term sentiment-driven price pressure is followed by a price reversal on the next trading day.

### Methodology

The paper uses a simple relative word-count weighting scheme to compute sentiment weights, which is found to be similar to the TF-IDF scheme.
The results are robust to the method used for term weighting, and the paper favors the simplest approach given the standardized sizes of messages posted on social media.
The paper also experiments with machine learning algorithms, finding that the maximum entropy method provides better results than naive Bayes and yields results similar to those of support vector machines.

## Study subjects

### 5 intraday investor sentiment indicators

- sL1 1.0000 sL2 0.6250 1.0000 sB1 0.2292 0.3365 1.0000 sB2 0.2328 0.3000 0.3112 1.0000 sM1 0.9341 0.6581 0.2629 0.2361 1.0000. Notes: This table shows the correlation matrix of our five intraday investor sentiment indicators, sx, where x={L1, L2, B1, B2, M1}. 4. Intraday online investor sentiment and stock returns

### 300000 users

- StockTwits is a social microblogging platform dedicated to financial markets on which individuals, investors, market professionals, and public companies can publish 140-character messages to “Tap into the Pulse of the Markets”. According to StockTwits.com, more than 300,000 users now use the platform to share information and ideas, producing streams that are viewed by an audience of more than 40 million across the financial web and social media platforms. In September 2012, StockTwits implemented a new feature that allows users to express their sentiment directly when they publish a message on the platform

## Data analysis

- #method/thomson_reuters_marketpsych_index
- #method/correlation_coefficient

## Findings

- <mark class="claim">We demonstrate that a transparent and replicable approach significantly outperforms standard <mark class="fact">dictionary-based methods used in the literature</mark> while remaining competitive with more complex machine learning algorithms</mark>
- <mark class="claim">While the Harvard-IV and the LM dictionary consider only unigrams, <mark class="fact">we find that adding bigrams provides additional information</mark> and improves the accuracy of the classification.8</mark>
- And contrary to [^Oliveira_et+al_2016_a]), <mark class="fact">we find that the accuracy</mark> and the percentage of the classified messages are nearly equivalent for the bullish and bearish messages for L1.10 However, the percentage of correct classification of benchmark dictionary-based approaches B1 (LM) and B2 (Harvard-IV) is significantly lower, with an accuracy of 63.06% and 58.29%, respectively
- Out-of-sample classification accuracy between 75% and 80% is standard on user-generated content sentiment analysis (see [^Pang_et+al_2002_a], [^Go_et+al_2009_a], or Smailovicet al. (2014), among others)
- <mark class="claim">We demonstrate that a transparent and <mark class="fact">replicable approach significantly outperforms the benchmark dictionaries used in the literature</mark> while remaining competitive with more complex machine learning algorithms</mark>
- <mark class="claim">Smailovicet al. (2014) confirmed that the TF approach is statistically significantly better than the TD-IDF-based approach to data from Twitter</mark>

## Builds on previous research

- Messages published by online investors on the Internet are usually shorter and less formal than content published on traditional media, making the correct classification of tone difficult ([^Loughran_2016_a]). Nonetheless, as stated by [^Nardo_et+al_2016_a], ”a good text classifier for a financial corpus is a good avenue for future research,” as it could facilitate the comparability and enhance the replicability of previous findings.
- Notes: This table shows four examples of messages before and after data preprocessing (removing stopwords, adding prefix for negation, replacing users’ mention by “usertag”, tickers by “cashtag”, links by “linktag”...). ging), we choose to use a conservative approach by removing only three stopwords from all messages (“a”, “an” and “the”).6 We also convert positive emoticons into a common word “emojipos” and negative emoticons into a common word “emojineg”7, as in [^Go_et+al_2009_a]).
- For example, using data from StockTwits and exploiting investor base heterogeneity, [^Cookson_2016_a], find that investor disagreement robustly forecasts abnormal trading volume at a daily frequency. In a similar fashion, we assess in this subsection whether a specific type of trader or a specific trading strategy drives the previously identified sentiment effect.
- We also consider a First Half-Hour Return Strategy buying (selling) the ETF on days with a positive (negative) first half-hour return and selling (buying) it at market close, and a 12th Half-Hour Return Strategy buying (selling) the ETF on days with a positive (negative) 12th half-hour return and selling (buying) it at market close. As in [^Roger_2014_a], we compare the Sharpe ratio of each strategy to the simulated Sharpe ratio distribution by generating 10,000 strategies randomly buying (selling) the S&P 500 ETF.
- We compute a sentiment score between −1 and +1 for all messages published on StockTwits (SS(m)) by adopting dictionary-based approaches and a machine learning method. For the dictionary-based approach L1, we use a methodology similar to [^Oliveira_et+al_2016_a].
- We end up with a sentiment score for the message equal to −1 for L2, 0 for B1 (no term identified), and 0 for B2 (two positive terms and two negative terms). We experiment with three machine learning algorithms as in [^Pang_et+al_2002_a] and [^Go_et+al_2009_a]: naive Bayes (NB), maximum entropy (MaxEnt), and support vector machines (SVM).

## Differs from previous work

- Numerous papers report increasing use of social media by market participants, from large quantitative hedge funds to family offices and high-frequency-trading firms.2 Little anecdotal evidence, like the integration of Twitter and StockTwits feeds into financial platforms (Bloomberg Terminal and Thomson Reuters Eikon), seems to confirm this phenomenon. Given the evolution of the regulatory framework3 and the constantly changing nature of communication on the Internet, we believe that the “news or noise” question raised by [^Antweiler_2004_a]) must be reassessed frequently.
- 10 As we focus our analysis on financial messages published on social media with self-reported sentiment, we cannot compare the accuracy of our field-specific approach with previous results from the literature on textual analysis directly. However, out-of-sample classification accuracy between 75% and 80% is standard on user-generated content sentiment analysis (see [^Pang_et+al_2002_a], [^Go_et+al_2009_a], or Smailovic et al. (2014), among others).
- Academic research may have destroyed stock return predictability ([^Mclean_2016_a]), or previous results may have been caused by data-snooping, market frictions, or omitted variables. We leave this question for further research.
- 12 For readability, we only present our results when L1 is used to compute investor sentiment. 13 [^Sun_et+al_2016_a]) find that ”there appears to be some evidence of reversal at longer horizons”, but the coefficient estimates for β1 are not significant in most of their regressions, with the exception of the 11th half-hour.
- For readability, we present the results only when the field-specific lexicon L1 is used to quantify individual message sentiment. As only 1.01% of users self-declared following a “Global Macro” trading approach, we remove this strategy from [^Cookson_2016_a].

## Confirmation of earlier findings

- The LM dictionary was created by examining formal corporate 10-K reports in such a way that it is not well-suited to analyze informal messages published on social media. This first result confirms [^Kearney_2014_a ]'s discussion on the need to construct more authoritative and extensive field-specific dictionaries in order to improve textual analysis classification.
- This finding is consistent with [^Hoffmann_2014_a], who find, using private data from a sample of discount brokerage clients, that individual investors who use technical analysis are disproportionately likely to speculate in the short-term stock market. Furthermore, analyzing users’ self-reported experience, we find that the last half-hour predictability is driven by shifts in the sentiment of novice traders and, to a lesser extent, by shifts in the sentiment of traders following technical analysis strategies.

## Counterpoint to earlier claims

- As the number of features is much greater in L1 (approximately 8000 n-grams) than in L2 (approximately 1300 n-grams), the percentage of classified messages CM is greater for L1 (90.03%) than for L2 (61.78%), leading to an expected arbitrage between accuracy and exhaustiveness. Interestingly, and contrary to [^Oliveira_et+al_2016_a], we find that the accuracy and the percentage of classified messages are nearly equivalent for both bullish and bearish messages at L1.10. However, the percentages of correct classification for benchmark dictionary-based approaches B1 (LM) and B2 (Harvard-IV) are significantly lower, at 63.06% and 58.29%, respectively.

## Contributions

- <mark class="fact">Improving the transparency and replicability of results is of utmost importance</mark> for the big-data and finance environment. Although developing public field-specific lexicons will obviously not <mark class="fact">solve all issues related to replicability and comparability</mark>, it still constitutes an important step to facilitate further research in this area, as stated by [^Nardo_et+al_2016_a]) in a recent survey of the literature of financial market prediction using the Web. In the first part of this paper, <mark class="fact">we construct a lexicon of words used by online investors when they share opinions and ideas</mark> <mark class="fact">about the bullishness or bearishness of the stock market by using an extensive dataset of messages for which sentiment is explicitly revealed by investors</mark>. <mark class="claim">We demonstrate that a transparent and <mark class="fact">replicable approach significantly outperforms the benchmark dictionaries used in the literature</mark> while remaining competitive with more complex machine learning algorithms</mark>. The findings provide empirical evidence to [^Kearney_2014_a ]'s conclusion about the need to develop a more authoritative field-specific lexicon and of [^Loughran_2016_a ]'s recommendations that alternative complex methods (machine learning) should be considered only when they add substantive value beyond simpler and more transparent approaches (bag-of-words).

## Limitations

- The study notes that the results are based on a specific dataset and may not be generalizable to other datasets. The study also notes that the methodology used to derive sentiment may not be perfect.
- The study notes that developing public field-specific lexicons will not solve all issues related to replicability and comparability. The study also acknowledges that the results are based on a specific dataset and may not be generalizable to other markets or contexts.

## Future work

- The study suggests that future research could explore the use of alternative methodologies to derive sentiment. The study also suggests that future research could investigate the relationship between online investor sentiment and other financial markets.
- The study suggests that further research is needed to explore the evolution of intraday investor sentiment over time and across users with different trading approaches, experiences, and investment horizons. The study also encourages further research in this area by making the field-specific weighted lexicon developed for this paper publicly available.

## References

[^Antweiler_2004_a]: Antweiler, W., Frank, M.Z., 2004. Is all that talk just noise? The information content of Internet stock message boards. J. Finance 59 (3), 1259–1294.  [OA](https://engine.scholarcy.com/oa_version?query=Antweiler%2C%20W.%20Frank%2C%20M.Z.%20Is%20all%20that%20talk%20just%20noise%3F%20the%20information%20content%20of%20internet%20stock%20message%20boards%202004&author=Antweiler&title=Is%20all%20that%20talk%20just%20noise%3F%20the%20information%20content%20of%20internet%20stock%20message%20boards&year=2004) [GScholar](https://scholar.google.co.uk/scholar?q=Antweiler%2C%20W.%20Frank%2C%20M.Z.%20Is%20all%20that%20talk%20just%20noise%3F%20the%20information%20content%20of%20internet%20stock%20message%20boards%202004) [Scite](/scite_tallies?query=author%3AAntweiler%2Ctitle%3AIs%20all%20that%20talk%20just%20noise%3F%20the%20information%20content%20of%20internet%20stock%20message%20boards%2Cyear%3A2004)

[^Cookson_2016_a]: Cookson, J. A., Niessner, M., 2016. Why don’t we agree? evidence from a social network of investors. Working Paper, Colorado University.  [OA](https://engine.scholarcy.com/oa_version?query=Cookson%2C%20J.A.%20Niessner%2C%20M.%20Why%20don%E2%80%99t%20we%20agree%3F%20evidence%20from%20a%20social%20network%20of%20investors%202016&author=Cookson&title=Why%20don%E2%80%99t%20we%20agree%3F%20evidence%20from%20a%20social%20network%20of%20investors&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Cookson%2C%20J.A.%20Niessner%2C%20M.%20Why%20don%E2%80%99t%20we%20agree%3F%20evidence%20from%20a%20social%20network%20of%20investors%202016) [Scite](/scite_tallies?query=author%3ACookson%2Ctitle%3AWhy%20don%E2%80%99t%20we%20agree%3F%20evidence%20from%20a%20social%20network%20of%20investors%2Cyear%3A2016)

[^Das_2007_a]: Das, S.R., Chen, M.Y., 2007. Yahoo! for amazon: sentiment extraction from small talk on the web. Manag. Sci. 53 (9), 1375–1388.  [OA](https://engine.scholarcy.com/oa_version?query=Das%2C%20S.R.%20Chen%2C%20M.Y.%20Yahoo%21%20for%20amazon%3A%20sentiment%20extraction%20from%20small%20talk%20on%20the%20web%202007&author=Das&title=Yahoo%21%20for%20amazon%3A%20sentiment%20extraction%20from%20small%20talk%20on%20the%20web&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Das%2C%20S.R.%20Chen%2C%20M.Y.%20Yahoo%21%20for%20amazon%3A%20sentiment%20extraction%20from%20small%20talk%20on%20the%20web%202007) [Scite](/scite_tallies?query=author%3ADas%2Ctitle%3AYahoo%21%20for%20amazon%3A%20sentiment%20extraction%20from%20small%20talk%20on%20the%20web%2Cyear%3A2007)

[^Go_et+al_2009_a]: Go, A., Bhayani, R., Huang, L., 2009. Twitter sentiment classification using distant supervision. Working paper. Stanford University.  [OA](https://scholar.google.co.uk/scholar?q=Go%2C%20A.%20Bhayani%2C%20R.%20Huang%2C%20L.%20Twitter%20sentiment%20classification%20using%20distant%20supervision%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Go%2C%20A.%20Bhayani%2C%20R.%20Huang%2C%20L.%20Twitter%20sentiment%20classification%20using%20distant%20supervision%202009)

[^Hoffmann_2014_a]: Hoffmann, A.O., Shefrin, H., 2014. Technical analysis and individual investors. J. Econ.  [OA](https://engine.scholarcy.com/oa_version?query=Hoffmann%20AO%20Shefrin%20H%202014%20Technical%20analysis%20and%20individual%20investors%20J%20Econ&author=Hoffmann&title=&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Hoffmann%20AO%20Shefrin%20H%202014%20Technical%20analysis%20and%20individual%20investors%20J%20Econ) [Scite](/scite_tallies?query=Hoffmann%2C%20A.O.%2C%20Shefrin%2C%20H.%2C%202014.%20Technical%20analysis%20and%20individual%20investors.%20J.%20Econ.)

[^Loughran_2016_a]: Loughran, T., McDonald, B., 2016. Textual analysis in accounting and finance: a survey. J. Account. Res. 54 (4), 1187–1230.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20McDonald%2C%20B.%20Textual%20analysis%20in%20accounting%20and%20finance%3A%20a%20survey%202016&author=Loughran&title=Textual%20analysis%20in%20accounting%20and%20finance%3A%20a%20survey&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20McDonald%2C%20B.%20Textual%20analysis%20in%20accounting%20and%20finance%3A%20a%20survey%202016) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3ATextual%20analysis%20in%20accounting%20and%20finance%3A%20a%20survey%2Cyear%3A2016)

[^Mclean_2016_a]: McLean, R.D., Pontiff, J., 2016. Does academic research destroy stock return predictability? J. Finance 71 (1), 5–32.  [OA](https://engine.scholarcy.com/oa_version?query=McLean%2C%20R.D.%20Pontiff%2C%20J.%20Does%20academic%20research%20destroy%20stock%20return%20predictability%3F%202016&author=Mclean&title=Does%20academic%20research%20destroy%20stock%20return%20predictability%3F&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=McLean%2C%20R.D.%20Pontiff%2C%20J.%20Does%20academic%20research%20destroy%20stock%20return%20predictability%3F%202016) [Scite](/scite_tallies?query=author%3AMclean%2Ctitle%3ADoes%20academic%20research%20destroy%20stock%20return%20predictability%3F%2Cyear%3A2016)

[^Nardo_et+al_2016_a]: Nardo, M., Petracco, M., Naltsidis, M., 2016. Walking down wall street with a tablet: a survey of stock market predictions using the web. J. Econ. Surv. 30 (2), 356–369.  [OA](https://engine.scholarcy.com/oa_version?query=Nardo%2C%20M.%20Petracco%2C%20M.%20Naltsidis%2C%20M.%20Walking%20down%20wall%20street%20with%20a%20tablet%3A%20a%20survey%20of%20stock%20market%20predictions%20using%20the%20web%202016&author=Nardo&title=Walking%20down%20wall%20street%20with%20a%20tablet%3A%20a%20survey%20of%20stock%20market%20predictions%20using%20the%20web&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Nardo%2C%20M.%20Petracco%2C%20M.%20Naltsidis%2C%20M.%20Walking%20down%20wall%20street%20with%20a%20tablet%3A%20a%20survey%20of%20stock%20market%20predictions%20using%20the%20web%202016) [Scite](/scite_tallies?query=author%3ANardo%2Ctitle%3AWalking%20down%20wall%20street%20with%20a%20tablet%3A%20a%20survey%20of%20stock%20market%20predictions%20using%20the%20web%2Cyear%3A2016)

[^Oliveira_et+al_2016_a]: Oliveira, N., Cortez, P., Areal, N., 2016. Stock market sentiment lexicon acquisition using microblogging data and statistical measures. Decis. Support Syst. 85, 62– 73. <http://www.sciencedirect.com/science/article/pii/S0167923616300240>.  [OA](http://www.sciencedirect.com/science/article/pii/S0167923616300240)  [Scite](/scite_tallies?query=author%3AOliveira%2Ctitle%3AStock%20market%20sentiment%20lexicon%20acquisition%20using%20microblogging%20data%20and%20statistical%20measures%2Cyear%3A2016)

[^Pang_et+al_2002_a]: Pang, B., Lee, L., Vaithyanathan, S., 2002. Thumbs up? Sentiment classification using machine learning techniques. In: Proceedings of the ACL-02 conference on Empirical methods in natural language processing, Vol. 10. Association for Computational Linguistics, pp. 79–86.  [OA](https://scholar.google.co.uk/scholar?q=Pang%2C%20B.%20Lee%2C%20L.%20Vaithyanathan%2C%20S.%20Thumbs%20up%3F%20Sentiment%20classification%20using%20machine%20learning%20techniques%202002) [GScholar](https://scholar.google.co.uk/scholar?q=Pang%2C%20B.%20Lee%2C%20L.%20Vaithyanathan%2C%20S.%20Thumbs%20up%3F%20Sentiment%20classification%20using%20machine%20learning%20techniques%202002)

[^Roger_2014_a]: Roger, P., 2014. The 99% market sentiment index. Finance 35 (3), 53–96.  [OA](https://engine.scholarcy.com/oa_version?query=Roger%2C%20P.%20The%2099%25%20market%20sentiment%20index%202014&author=Roger&title=The%2099%25%20market%20sentiment%20index&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Roger%2C%20P.%20The%2099%25%20market%20sentiment%20index%202014) [Scite](/scite_tallies?query=author%3ARoger%2Ctitle%3AThe%2099%25%20market%20sentiment%20index%2Cyear%3A2014)

[^Sun_et+al_2016_a]: Sun, L., Najand, M., Shen, J., 2016. Stock return predictability and investor sentiment: a high-frequency perspective. J. Bank. Finance 73, 147–164. <http://www.sciencedirect.com/science/article/pii/S0378426616301595>.  [OA](http://www.sciencedirect.com/science/article/pii/S0378426616301595)  [Scite](/scite_tallies?query=author%3ASun%2Ctitle%3AStock%20return%20predictability%20and%20investor%20sentiment%3A%20a%20high-frequency%20perspective%2Cyear%3A2016)
