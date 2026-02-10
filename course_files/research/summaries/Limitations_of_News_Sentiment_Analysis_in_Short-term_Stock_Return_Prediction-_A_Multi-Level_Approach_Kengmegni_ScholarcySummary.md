[[kengmegni.gael@gmail.com_LimitationsOfNewsSentimentAnalysis_2024]]

# [LIMITATIONS OF NEWS SENTIMENT ANALYSIS IN SHORT-TERM STOCK RETURN PREDICTION: A MULTI-LEVEL APPROACH]()

## [[Gaël Kengmegni kengmegni.gael@gmail.com]]

## Abstract

In this paper, I investigate the challenges and limitations of using news sentiment analysis for predicting next-day stock returns in the U.S. equity market. While sentiment analysis has shown promise in long-term market prediction, its effectiveness for short-term prediction remains contentious. I propose a novel multi-level approach that integrates sentiment analysis across individual stocks, industries, and the broader economy, extending previous hierarchical market analysis frameworks using a comprehensive dataset combining financial news from Bloomberg, Reuters, and Yahoo Finance (2009-2023). My methodology employs an instruction-pretrained LLaMA 3 8B model for sentiment analysis and benchmarks it against other state-of-the-art models, including RoBERTa Large, FinBERT, and LLaMA 3 8B, on the FiQA and FPB datasets. Following recent advances in financial NLP, I augment traditional sentiment features with market data, implementing separate models of high-coverage (&gt;150 articles annually) and low-coverage stocks to account for varying news frequency. My results demonstrate several key findings. First, even with sophisticated sentiment analysis and feature augmentation, accurate next-day return prediction remains elusive, supporting the efficient market hypothesis at short time horizons. Second, when incorporating both sentiment and market features, models tend to overfit on price-based features, diminishing the impact of sentiment signals. Third, I find that economy-wide sentiment features exhibit greater predictive power than industry- or stock-specific sentiment, underscoring the importance of broader market sentiment over individual stock news. My back-testing reveals that the most robust results come from focusing on less-covered stocks with a consistent correlation between sentiment and returns, though even these strategies show limited economic significance when transaction costs are accounted for. Surprisingly, sources often considered less reliable (Benzinga, Zacks) showed more stable sentiment signals than traditional news providers. These findings contribute to the growing body of literature on the limitations of sentiment-based trading strategies and highlight the importance of realistic expectations in sentimentdriven algorithmic trading. It should be noted that all analyses and conclusions are subject to the limitations of the underlying datasets, including potential survivorship bias in the stock universe and varying news coverage quality across sources and time periods.

## Key concepts

# algorithmic_trading; #claim/sentiment_analysis; #sentiment_analysis; #claim/economy; #economy; #news_sentiment; #multi_level

## Quote

This study investigates the challenges of using news sentiment analysis to predict next-day stock returns in the U.S. equity market and proposes a novel multi-level approach that integrates sentiment analysis across individual stocks, industries, and the broader economy.

## Key points

- This research into next-day stock return prediction stems from several key observations
- The relationship between news sentiment and stock returns appears to be weakening over time, as evidenced by the declining variance in sentiment-return agreement rates from 2009 to 2023
- This suggests that markets are becoming more efficient at processing sentiment information, potentially due to the proliferation of algorithmic trading strategies
- The hierarchical nature of sentiment signals, with market-level sentiment proving more reliable than stock-specific sentiment, suggests that traditional bottom-up approaches to sentiment analysis might need reconsideration
- The success of market-level signals indicates that sentiment might be more valuable for broad market timing than for individual stock selection
- Sentiment analysis appears more valuable as one component of a broader investment process rather than as a standalone predictor of returns

## Summary

### Introduction

The study investigates the challenges of using news sentiment analysis to predict next-day stock returns in the U.S. equity market.
It proposes a novel multi-level approach that integrates sentiment analysis across individual stocks, industries, and the broader economy.
The methodology employs an instruction-pre-trained LLaMA 3 8B model for sentiment analysis and combines traditional market data with sentiment indicators.

### Methodology

The study uses a comprehensive dataset combining financial news from Bloomberg, Reuters, and Yahoo Finance (2009-2023) and evaluates four leading language models for financial sentiment analysis.
It examines traditional market data alongside sentiment indicators at three levels: individual stocks, industries, and the overall economy.
The analysis also compares the predictive quality of stocks with heavy news coverage to that of those with less coverage.

### Findings

The results demonstrate that accurate next-day return prediction remains elusive, even with sophisticated sentiment analysis and feature augmentation.
The study finds that economy-wide sentiment features exhibit greater predictive power than industry- or stock-specific sentiment.
The trading strategy back tests reveal that focusing on less-covered stocks with consistent correlation between sentiment and returns yields the most robust results, although these strategies show limited economic significance when accounting for transaction costs.

### Data

The dataset consists of news articles from 2006 to 2013, including Reuters and Bloomberg, both known for their neutral, fact-based reporting.
In contrast, sources like Nasdaq, Benzinga, and Zacks tend to have more attention-grabbing headlines.
The distribution of news coverage across companies is highly skewed, with most firms receiving fewer than 100 articles annually.
Market data is collected from Yahoo Finance's API, including daily stock prices and trading volume for all U.S. stocks currently trading.
However, the dataset has a significant limitation due to survivorship bias, as it only includes companies that have survived from 2009 to the present.

### Model Development

The evaluation of four state-of-the-art language models for financial sentiment analysis revealed that FinBERT and LLaMA 3 8B demonstrated robust performance.
The instruction-pretrained LLaMA 3 8B was selected for subsequent analysis due to its domain adaptation through instruction tuning.
The text processing pipeline involves timestamp conversion, entity detection, industry references, and article summarization using the LexRank algorithm.
The market data processing involves aligning price data with news flow and calculating close-to-close returns.
The feature sets include sentiment features, such as mean sentiment score and sentiment dispersion, and market features, such as multi-horizon returns and technical signals.

### Results

The results of the sentiment analysis show clear patterns in sentiment distribution and source reliability.
The sentiment score distribution exhibits clustering around -1, 0, and 1, and both the mean and median sentiment scores demonstrate a significant positive bias.
The agreement between sentiment and stock returns is limited, with sentiment-return sign agreement ratios clustering around 0.5, approximating a random distribution.
This finding challenges the common assumption that sentiment directly leads price movements at daily frequencies.

### Market Efficiency

The relationship between sentiment and stock returns is evolving, with market efficiency increasing over time.
The standard deviation of agreement between sentiment and returns has declined from 0.2 in 2009 to 0.065 in 2023, indicating reduced volatility.
This shift suggests that simple sentiment-based trading strategies may not be effective in current market conditions.

### Model Performance

The performance of different modeling methods, including linear models and CatBoost, was compared.
CatBoost showed greater potential, with a maximum test R-squared of 0.005 and superior directional accuracy of 0.548.
However, linear models showed greater stability and interpretability of coefficients, making them more suitable for practical implementation.
Feature importance analysis revealed that market-level signals consistently outperform stock-specific metrics in both price and sentiment domains.

### Trading Strategy

The analysis found that a specialized approach focusing on sentiment features, low-coverage stocks, and implementing a 0.1 correlation threshold in training sets achieved moderate but consistent results, with an average Sharpe ratio of 0.609 and a mean total return of 8.7%.
Implementing a trading strategy requires careful consideration of practical constraints, including transaction costs, market impact, and position sizing.
The results suggest that sentiment analysis may be more valuable as part of a broader strategy than as a standalone approach.

### Implications

The findings have implications for practitioners considering sentiment-based trading strategies.
Market-level sentiment suggests that traders might benefit from focusing their sentiment analysis efforts on broad market indicators rather than individual stock news.
This approach could reduce computational overhead and noise inherent in stock-specific sentiment signals.
The results also suggest that traditional approaches to news source selection might need revision, with a focus on temporal stability rather than perceived source quality.

### Limitations

The research has several limitations, including survivorship bias in the dataset, data quality issues, and the focus on U.S. stocks trading in U.S. markets.
The approach to news timing and market hours introduces another limitation, as important after-hours news flow may be missed.
These limitations suggest promising directions for future investigation, including extending the approach to intraday data and exploring different prediction horizons.

### Future Research

Several promising research directions emerge from the limitations, including analyzing how sentiment impacts returns at different frequencies, exploring different prediction horizons, and adjusting the hierarchical level of prediction.
The research also suggests that sentiment analysis might be more valuable for risk management and portfolio optimization rather than as a standalone predictor of returns.
Alternative applications of sentiment analysis, such as predicting volatility spikes or trading volume, could provide valuable trading signals even when direct return prediction proves challenging.

### Features

The framework utilizes various features to analyze stock performance, including excess returns, moving averages, volatility, trend estimates, relative performance, return dispersion, higher moments, volume-weighted returns, and Hurst exponent.
These features help to isolate stock-specific performance, smooth noisy price data, quantify price uncertainty, and identify potential regime changes.

### Portfolio Optimization

The portfolio optimization process involves generating a combined prediction score from high- and low-coverage model predictions.
The objective function aims to maximize the portfolio return while minimizing risk, subject to constraints such as full investment, position limits, and capacity constraints.
The position size calculation is based on the optimized weight for each stock, and the portfolio value evolution is simulated with daily rebalancing, accounting for transaction costs and market impact.

### Risk Management

The framework incorporates risk management techniques, including volatility measurement, volatility ratios, and higher-moment analysis.
The volatility ratio compares recent to historical volatility to identify regime changes, while the higher moments analysis captures non-normal characteristics of returns that might signal future price movements.
These techniques help to quantify price uncertainty and identify potential risks.

## Study subjects

### 150 articles

- The analysis examines traditional market data alongside sentiment indicators at three levels: individual stocks, industries, and the overall economy. The study also aims to compare prediction quality between stocks with heavy news coverage(over 150 articles per year) and those with less coverage to understand how news frequency affects prediction accuracy. An important aspect is analyzing which factors matter most for predictions

### 500000 Bloomberg articles

- FNSPID is supplemented with the Edaz financial news dataset, containing over 11 million Yahoo Finance articles spanning from pre-2000 to 2023. The third source is Philippe Remy’s dataset of more than 500,000 Bloomberg articles and Reuters headlines from 2006 to 2013, which offers high-quality coverage from traditional financial news providers. The news sources in the dataset display interesting patterns in their coverage and style

## Data analysis

- #method/linear_models
- #method/linear_model
- #method/covariance_matrix
- #method/model_performance_analysis_testing_models
- #method/catboost_model
- #method/non_linear_models
- #method/bert_model

## Findings

- • FinBERT demonstrated robust performance (84.2% accuracy on FPB, 74.7% on FiQA)despite its relative age
- • LLaMA 3 8B achieved the highest accuracy scores (97.0% on FPB, 84.4% on FiQA)
- 2019 consistently emerges as the strongest period for prediction accuracy, with R-squared values reaching 0.004 and directional accuracy exceeding 53%
- By limiting individual positions to no more than 10% of typical daily volume, the strategy maintains the ability to adjust positions without creating excessive market impact

## Differs from previous work

- Machine learning approaches initially seemed more promising. Early studies by [^Kimoto_et+al_1990_a] using neural networks and [^Tay_2001_a] with support vector machines reported impressive results, but most of these didn’t hold up in real-world trading.

## Contributions

- In conclusion, while the holy grail of reliable next-day return prediction through sentiment analysis remains elusive, the research reveals valuable insights about market information processing and the practical limitations of sentiment-based trading. These findings should help both researchers and practitioners develop more realistic approaches to incorporating sentiment analysis into investment strategies.

## Future work

- The study suggests several promising directions for future research, including investigating the relationship between news coverage intensity and predictability, the role of retail-oriented news sources in price formation, and the interaction between sentiment signals and market microstructure.
- The research suggests several promising directions for future work, including investigating the relationship between news coverage intensity and predictability. The role of retail-oriented news sources in price formation also merits further study. Additionally, the study suggests exploring alternative applications of sentiment analysis, such as predicting industry-level returns, broad market movements, and trading volume.

## References

[^Kimoto_et+al_1990_a]: Tsuneo Kimoto, Kazuo Asakawa, Masakazu Yoda, and Masanori Takeoka. Stock market prediction system with modular neural networks. Neural Networks, 1:1–6, 1990.  [OA](https://engine.scholarcy.com/oa_version?query=Kimoto%2C%20Tsuneo%20Asakawa%2C%20Kazuo%20Yoda%2C%20Masakazu%20Takeoka%2C%20Masanori%20Stock%20market%20prediction%20system%20with%20modular%20neural%20networks%201990&author=Kimoto&title=Stock%20market%20prediction%20system%20with%20modular%20neural%20networks&year=1990) [GScholar](https://scholar.google.co.uk/scholar?q=Kimoto%2C%20Tsuneo%20Asakawa%2C%20Kazuo%20Yoda%2C%20Masakazu%20Takeoka%2C%20Masanori%20Stock%20market%20prediction%20system%20with%20modular%20neural%20networks%201990) [Scite](/scite_tallies?query=author%3AKimoto%2Ctitle%3AStock%20market%20prediction%20system%20with%20modular%20neural%20networks%2Cyear%3A1990)

[^Tay_2001_a]: Francis E. Tay and Lijuan Cao. Application of support vector machines in financial time series forecasting. Omega, 29 (4):309–317, 2001.  [OA](https://engine.scholarcy.com/oa_version?query=Tay%2C%20Francis%20E.%20Cao%2C%20Lijuan%20Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%202001&author=Tay&title=Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting&year=2001) [GScholar](https://scholar.google.co.uk/scholar?q=Tay%2C%20Francis%20E.%20Cao%2C%20Lijuan%20Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%202001) [Scite](/scite_tallies?query=author%3ATay%2Ctitle%3AApplication%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%2Cyear%3A2001)
