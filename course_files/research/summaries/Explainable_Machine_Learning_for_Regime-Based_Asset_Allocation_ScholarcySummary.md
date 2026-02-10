[[Zhang_et+al_ExplainableMachineLearningRegimebasedAsset_2020]]

# [Explainable Machine Learning for Regime-Based Asset Allocation](https://doi.org/10.1109/bigdata50022.2020.9378332)

## [[Ruoyun Zhang]]; [[Chao Yi]]; [[Yixin Chen]]

## Abstract

This paper explores an explainable AI model in the financial industry. Macroeconomic and market data serve as inputs for Hierarchical Clustering to distinguish among different economic regimes. Compared with traditional models such as the Investment Clock, this method can adjust the classification standard over time in response to recent market sentiment. The regime can therefore be interpreted not only from macro indicators but also from investors' mood swings using Artificial Intelligence. When we compute the statistical characteristics of each asset's returns, we find that they can be well distinguished across regimes. This method can also identify the abnormally large wave in the stock market from 2015 to 2016 as an unusual regime, which traditional methods cannot capture. The clustering technique enables us to understand the current market status and predict the performance of different assets. Therefore, thanks to the superior interpretability of AI, the mean and variance of returns in each regime are estimated and viewed as viewpoints of the Black-Litterman asset allocation model to construct portfolios. To simulate the real situation, a dynamic backtesting method is used, with asset weights updated via rolling time windows. The results show that, with a simple timing strategy, the clustering technique can improve performance and yield excess returns. Other machine learning techniques are also applied to improve the model.

## Key concepts

#market_sentiment; #black_litterman_model; #explainable_machine_learning; #macroeconomic_environment; #asset_allocation; #artificial_intelligence; #machine_learning; #hierarchical_clustering; #mean_variance_model; #bayesian_method

## Quote

The study proposes a dynamic asset allocation framework that combines economic regime division via hierarchical clustering with the Black-Litterman model and introduces a rotation of objective optimization functions to address imbalanced weights and achieve higher excess returns.

## Key points

- Asset allocation optimization is one of the most important research fields in asset management
- In the 1950s, Markowitz brought up the mean-variance model, seeking to maximize expected return given the level of risk or minimize risk with a certain level of return
- Asset allocation started to change from simple methods such as equal-weighted or the 60/40 rule, to the quantitative era
- The Bayesian method used in the Black-Litterman model gives it great flexibility
- The change of macroeconomic environment has a certain ability to explain the performance of assets
- All three BL models applying the clustering technique significantly outperform the benchmark, and the rotation model is significantly better than the others
- Due to its high interpretability by visualization and numerical analysis, an explainable AI model is incorporated into an asset allocation strategy and performs well in the last decade, which shows the great prospects of explainable AI in the financial industry

## Summary

### Introduction

The paper explores an explainable AI model for regime-based asset allocation in the financial industry.
Macroeconomic and market data are used as inputs for Hierarchical Clustering to distinguish between different economic regimes.
The model adjusts the classification standard over time in response to recent market sentiment, enabling the interpretation of regimes using both macro indicators and investors' mood swings via Artificial Intelligence.

### Regime Switching

The paper discusses regime switching, including the Merrill Lynch Investment Clock theory, which separates the business cycle into four phases: reflation, recovery, overheating, and stagflation.
The authors propose a model that includes additional macro factors and comprehensively reflects economic status using Hierarchical Clustering.
The model divides economic status into four categories and uses the Ward algorithm to minimize the increase in the sum of squared deviations after merging the two clusters.

### Asset Allocation

The paper discusses dynamic regime-switching asset allocation using the Black-Litterman model, which combines market equilibrium with investor views.
The model uses the Capital Asset Pricing Model (CAPM) to calculate the market's equilibrium return and integrates the investor's subjective return expectations to obtain the posterior return using the Bayesian method.
The authors use monthly market technical indicators, along with macroeconomic indicators, to cluster the economy each month into four regimes and extract historical price information for all assets in each regime to calculate the estimated mean and covariance of returns.
The results show that the strategy achieves an annual return of 22.53% and a Sharpe ratio of 1.06 from August 2010 to May 2020, outperforming both the equal-weighted benchmark and the classical Black-Litterman model.
The asset allocation framework combines hierarchical clustering of economic regimes with the BL model.
The model preprocesses macroeconomic data with HP filtering and combines it with market technical indicators to cluster economic regimes into 4 categories.
The model then assesses the historical performance of all assets and computes the empirical expectation and covariance, which are used as priors to calculate posteriors for the BL model.

### Model Development

The Black-Litterman (BL) model is used with a rotation of objective functions to address the imbalance in weights and achieve higher excess returns.
The model combines hierarchical clustering of economic regimes with the BL model.
The rotation of objective optimization functions changes the objective to seek maximum return at a 20% risk level when the stock market volatility exceeds a certain threshold and an upward breakout trend is in place.

### Backtesting Results

The backtesting results show that the rotation model outperforms the equal-weighted benchmark portfolio and other counterparts.
The model's annualized return is 22.53%, and its Sharpe ratio is about 1.06.
The model captures two large upswing signals of the stock market and withdraws before the plunge.
The rotation model has relatively higher returns than the maximum Sharpe model and is relatively more stable than the maximum return model.

### Work

The text mentions work.

### Suggestions

It also mentions making precious suggestions.

### Context

The context in which the work and suggestions are made is collaborative.

## Data analysis

- #method/ward_algorithm
- #method/markowitz_model
- #method/bayesian_method
- #method/relative_strength_index
- #method/lstm_model
- #method/black_litterman_model
- #method/covariance_matrix
- #method/hierarchical_clustering
- #method/capital_asset_pricing_model

## Findings

- The return on investment product A is 2% higher than that of B, then
- <mark class="claim">During the backtesting, <mark class="fact">we found that the volatility of stocks can reach</mark> 40%, while the volatility of bonds is stable and remains less than 1%</mark>
- <mark class="claim">All three BL models applying the clustering technique significantly outperform the benchmark, and <mark class="fact">the rotation model is significantly better than the others</mark></mark>
- <mark class="fact">The maximum drawdown of it is constrained below 10%</mark>, much smaller than the maximum return model achieving the second largest annual return in the table

## Contributions

- <mark class="fact">The change of macroeconomic environment has a certain ability to explain the performances of assets</mark>. Market sentiment also explains the rise and fall of prices. <mark class="fact">The fear of future uncertainties prompts people to flock to the gold or bonds market when negative events occur</mark>. It is not uncommon to <mark class="fact">select assets according to investors’ reactions</mark>. Using AI techniques, we can explain market status by both macroeconomic factors and market sentiment. It allows us to capture information on hotspot events, such as policy changes or natural disasters, which might cause significant insecurity among investors. After our analysis and data visualization, <mark class="fact">it is clear that the AI technique successfully integrates market and macro data to comprehensively recognize the regime. </mark> This paper sets an asset allocation framework that combines the economic regime division by hierarchical clustering with the Black-Litterman model. It is also found that setting the rotation of the objective optimization functions can solve the imbalanced weights problem and yield higher excess returns. Firstly, we preprocess macroeconomics data with hp filtering and combine <mark class="fact">it with market technical indicators to divide the economic regimes into four categories using clustering</mark>. Then, for each regime, we assess the historical returns’ performances of all assets and compute the empirical expectation and covariance. <mark class="fact">They are used as viewpoints to calculate posteriors for the BL model</mark>. BL optimization weights are then calculated by rotating the objective optimization functions to achieve dynamic asset allocation. <mark class="claim">The results show that during the backtest period from August 2010 to May 2020, the annualized return of the model reaches 22.53%, and the Sharpe ratio is about 1.06, <mark class="fact">which is significantly better than the equal-weighted benchmark portfolio</mark> and other counterparties</mark>. The model integrates macro-scenarios and has strong flexibility. <mark class="fact">It can respond to market fluctuations in a timely manner</mark>. Experiments show that it successfully captures two large upswing signals of the stock market and withdraws before the plunge. In conclusion, due to its high interpretability by visualization and numerical analysis, <mark class="fact">an explainable AI model is incorporated into an asset allocation strategy</mark> and performs well in the last decade, <mark class="fact">which shows the great prospects of explainable AI in financial industry</mark>.

## Limitations

- The study has some limitations, including the use of a limited dataset and the reliance on historical data. The study also assumes that the market equilibrium weight is calculated as the ratio of the investment product market value and the total market value.
- The study does not discuss the limitations of the proposed framework, but mentions that the use of historical returns as inputs to the Black-Litterman model may not be reasonable.
- The limitations of the research are not addressed in the provided text.

## Future work

- The study suggests that future work could include the use of more advanced machine learning techniques, such as deep learning. The study also suggests that future work could include the use of more diverse datasets, including alternative data sources.
- There is no discussion of future work in the given text.

## References
