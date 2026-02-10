[[Shu_et+al_DownsideRiskReductionUsingRegimeswitching_2024]]

# [Downside risk reduction using regime-switching signals: a statistical jump model approach](https://doi.org/10.1057/s41260-024-00376-x)

## [[Yizhan Shu]]; [[Chenyu Yu]]; [[John M. Mulvey]]

## Abstract

This article investigates a regime-switching investment strategy that aims to mitigate downside risk by reducing market exposure during anticipated unfavorable market regimes. We highlight the statistical jump model (JM) for market regime identification, a recently developed robust model that distinguishes itself from traditional Markov-switching models by enhancing regime persistence through a jump penalty applied at each state transition. Our JM utilizes a feature set comprising risk and return measures derived solely from the return series, with the optimal jump penalty selected via time-series cross-validation that directly optimizes strategy performance. Our empirical analysis evaluates the out-of-sample performance of various strategies across major US, German, and Japanese equity indices from 1990 to 2023, accounting for transaction costs and trading delays. The results demonstrate the consistent outperformance of the JM-guided strategy in reducing risk metrics such as volatility and maximum drawdown, and in enhancing risk-adjusted returns, such as the Sharpe ratio, compared to both the hidden Markov model-guided strategy and the buy-and-hold strategy. These findings underscore the enhanced persistence, practicality, and versatility of strategies that use JMs for regime-switching signals.

## Key concepts

#claim/hidden_markov_model; #hidden_markov_model; #claim/downside_risk; #downside_risk; #bear_markets; #clustering; #claim/maximum_drawdown; #maximum_drawdown

## Quote
>
> This article investigates a regime-switching investment strategy using statistical jump models to mitigate downside risk by reducing market exposure during unfavorable market regimes and finds that the strategy consistently outperforms traditional hidden Markov model-guided and buy-and-hold strategies in terms of risk reduction and risk-adjusted returns.

## Key points

- We evaluate the out-of-sample performance of the 0/1 strategy using regimes inferred by jump model (JM) and hidden Markov models (HMMs), comparing it to the buy-and-hold strategy, when applied individually to daily equity indices from the US, Germany, and Japan
- Our results reveal that the 0/1 strategy, when informed by JMs, significantly reduces risk metrics like volatility and maximum drawdown, highlighting its effectiveness in mitigating downside risk
- We focus on statistical jump models that enhance k-means clustering by imposing a jump penalty with each regime switch, offering improved regime persistence and a potential for application in the 0/1 strategy that involves significant portfolio rebalancing
- We have presented a regime-switching investment strategy utilizing the statistical jump model (JM) to mitigate downside risk by timely shifting to safer assets in response to anticipated unfavorable market conditions
- Our JM employs a set of features including risk and return measures derived from the return series, with the optimal jump penalty determined through a time series cross-validation method that emphasizes the financial implications of identification accuracy
- The results indicate that the JM-guided strategy consistently outperforms both the hidden Markov model-guided strategy and the buy-and-hold strategy in reducing volatility and maximum drawdowns and enhancing risk-adjusted returns

## Summary

### Introduction To Regime Switching

Regime switching refers to the sudden yet persistent shift in market behavior, driven by a complex interplay of economic, behavioral, and political factors.
A financial regime is defined by extended, consecutive periods displaying homogeneous market behavior, manifesting as bull or bear markets.
Regime-switching models have been established across various asset classes, including equities, fixed income, and currencies.
These models have a key advantage in interpretability, with identified regimes often aligning with real-world events, such as different phases of the macroeconomic business cycle.

### Statistical Jump Models

Statistical jump models (JMs) are a type of regime identification model that distinguishes itself from traditional Markov-switching models by enhancing regime persistence through a jump penalty applied at each state transition.
JMs utilize a feature set comprising risk and return measures derived solely from the return series, with the optimal jump penalty selected via time-series cross-validation that directly optimizes strategy performance.
The results demonstrate the consistent outperformance of the JM-guided strategy in reducing risk metrics, such as volatility and maximum drawdown, and in enhancing risk-adjusted returns, such as the Sharpe ratio.

### Investment Strategy Performance

The 0/1 strategy, which switches between 100% investment in a risky or risk-free asset based on inferred regimes, is evaluated using regimes inferred by JMs and hidden Markov models (HMMs).
The results reveal that the 0/1 strategy, particularly when informed by JMs, significantly reduces risk metrics like volatility and maximum drawdown, highlighting its effectiveness in mitigating downside risk.
The JM-informed strategy improves annualized returns by approximately 1–4% across regions, thereby improving risk-adjusted return metrics.

### Models

Parametric models, such as Markov-switching models and hidden Markov models (HMMs), assume specific probability distributions for observations and use estimated parameters to infer regime assignments.
Nonparametric models, including statistical jump models (JMs), adopt a likelihood-free, data-driven approach that focuses on directly identifying the unobserved regime sequence.
HMMs characterize regimes solely by conditional volatilities, whereas JMs consider a broader set of features, including both return and risk measures.

### Regime Identification

Both HMMs and JMs infer regimes directly from market data, specifically daily equity index returns, rather than macroeconomic indicators.
They employ a two-state implementation, which has proven sufficient for capturing the dynamics of a single return series.
The models generate daily switching signals to mitigate the impact of incorrect regime forecasts over longer periods, down to shorter spans.
The persistence of the inferred online state sequence is critical, and techniques such as median filtering and jump penalties are used to enhance it.

### Practical Considerations

The practical applicability of regime-switching strategies is influenced by factors such as the delay in trading the signal and the persistence of regime forecasts.
A one-day delay is assumed, and robustness tests are conducted to evaluate the impact of delays of up to two weeks.
The importance of regime persistence is highlighted, and techniques such as jump models are proposed to help prevent excessive rebalancing while maintaining identification accuracy.

### Model Development

The continuous statistical jump model (CJM) extends the jump model (JM), where the discrete hidden state variable is generalized to a probability vector over all states.
The JM employs a feature set consisting of three return and risk measures derived from an excess return series, including an exponentially weighted moving (EWM) downside deviation and EWM Sortino ratios.
The model parameters are updated every 6 months by solving the full optimization problem over a 3000-day training window.

### Online Inference

An online algorithm processes input data sequentially, and the state to which each day belongs is inferred from the features available at the end of that day.
A lookback window is incorporated to enhance the persistence of the online inferred regime sequence, and the dynamic programming (DP) algorithm is used to minimize the objective function over the state sequence.
The online inferred regimes are generated daily using only the latest available data.

### Performance Evaluation

The performance of the 0/1 strategy using online-inferred regimes from both the hidden Markov model (HMM) and JM is compared with that of the buy-and-hold strategy.
The hyperparameters are optimally selected using time-series cross-validation, and the performance metrics include compound annual growth rate, volatility, Sharpe ratio, maximum drawdown, and expected shortfall.
The results show that the 0/1 strategy effectively improves several risk measures, including volatility, maximum drawdown, and expected shortfall, and that JMs further enhance this reduction.

### Strategy

The 0/1 strategy using the statistical jump model (JM) achieves a baseline volatility of 13.1%, outperforming the buy-and-hold strategy and the hidden Markov model (HMM)-guided strategy.
The JM strategy enhances the compound annual growth rate (CAGR) by 1%, 1.8%, and 3.9% for the three indices, respectively.
The strategy also achieves higher risk-adjusted return metrics, including Sharpe and Calmar ratios, than both the buy-and-hold and HMM-guided strategies.

### Performance

The JM strategy exhibits milder drawdowns and provides more robust protection against adverse market movements, consistently delivering the highest returns across all indices.
The strategy's turnover is significantly reduced, at 44% for the S&P 500 index, indicating a relatively mild figure despite large portfolio rebalancing.
The strategy's performance is also robust to trading delays, with the JM strategy maintaining a Sharpe ratio comparable to or better than the index even at the longest two-week delay.

### Limitations

The identified regimes exhibit some latency at the beginnings and ends of market crashes and may sometimes misinterpret oscillations during prolonged turbulent periods.
A potential enhancement could involve including more descriptive features that detect trending or oscillatory patterns in the return series, or reflect broader macroeconomic conditions, to better inform JMs.
The HMM-inferred regimes display numerous short-lived, unintuitive, and difficult-to-trade regimes, frequently resulting in the HMM strategy underperforming the buy-and-hold strategy.

## Data analysis

- #method/k_means_clustering
- #method/markov_model
- #method/maximum_likelihood_estimation
- #method/viterbi_algorithm

## Findings

- [^Aydınhan_et+al_2024_a]) expand <a class="keyword" href="#" title="jump model">JMs</a> into the continuous statistical jump model (<a class="keyword" href="#" title="continuous statistical jump model">CJM</a>) by generalizing the discrete hidden state variable into a probability vector across all states, offering a probabilistic interpretation where the hidden state vector represents the probability of each period belonging to each regime. While these probability values hold potential use, the discrete nature of the 0/1 weighting scheme we employ here shows no significant difference in strategy performance between <a class="keyword" href="#" title="jump model">JM</a> and <a class="keyword" href="#" title="continuous statistical jump model">CJM</a>, based on our experiences
- The expected shortfall also improves by approximately 1%
- For the S&amp;P 500 index, the <a class="keyword" href="#" title="jump model">JM</a>-guided 0/1 strategy achieves √a leverage of 80%, leading to a baseline volatility of 18.2% × 0.8 = 16.3% , while our strategy further reduces volatility to 13.1%

##  Builds on previous research

- No. [^Bemporad_et+al_2018_a]) introduce statistical jump models (JMs) as a general unsupervised learning algorithm that fits multiple model parameters to time series data while incorporating temporal information.

## Differs from previous work

- The ability of HMMs to reduce risk and enhance risk-adjusted return when applied to the 0/1 strategy has been substantiated in Bulla et al (2011), and thus they serve as the benchmark model in our study. Despite the long research history of Markov-switching models, recent studies have highlighted the sensitivity of HMMs to model mis-estimation and mis-specification ([^Nystrup_et+al_2020_a], b).
- While those studies focus on economic regimes that influence all considered assets or regions through broad economic conditions, our research aims to identify financial regimes tailored to specific markets based on asset returns. Second, both models employ a two-state implementation (K = 2), which, despite statistical criteria often favoring more states ([^Guidolin_2011_a]).

##  Confirmation of earlier findings

- For instance, [^Nystrup_et+al_2018_a] report that “the median [latency] in detecting regime changes is 25 (calendar) days.” We observe a latency of approximately half a month in detecting both the onset and conclusion of the market crash, which is representative in our study and aligns with typical results in similar studies.

## Contributions

- We conclude with a basic robustness test concerning the trading delay. Our previous discussions assume a one-day delay, meaning that the identified regime for day t is applied to trading at the end of the following day, t + 1. However, Return Sharpe Calmar

## Future work

- Future work could involve applying the statistical jump model approach to other asset classes and investment strategies, and exploring the use of other machine learning models for regime identification.
- The study suggests that future work could focus on evaluating the out-of-sample performance of other regime identification models, such as trend filtering and spectral clustering. The study also suggests that future work could focus on incorporating insights from machine learning algorithms into regime identification models.
- The study suggests several promising directions for further research, including refining the model’s accuracy and adaptability with a more comprehensive feature set, investigating how the influential features dynamically change over time, and extending the 0/1 strategy to a broader range of asset classes.

## References

[^Aydınhan_et+al_2024_a]: Aydınhan, A. O., P. N. Kolm, J. M. Mulvey, and Y. Shu. 2024. Identifying patterns in financial markets: extending the statistical jump model for regime identification. Annals of Operations Research. To appear.  [OA](https://engine.scholarcy.com/oa_version?query=Ayd%C4%B1nhan%2C%20A.O.%20Kolm%2C%20P.N.%20Mulvey%2C%20J.M.%20Shu%2C%20Y.%20Identifying%20patterns%20in%20financial%20markets%3A%20extending%20the%20statistical%20jump%20model%20for%20regime%20identification%202024&author=Ayd%C4%B1nhan&title=Identifying%20patterns%20in%20financial%20markets%3A%20extending%20the%20statistical%20jump%20model%20for%20regime%20identification&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Ayd%C4%B1nhan%2C%20A.O.%20Kolm%2C%20P.N.%20Mulvey%2C%20J.M.%20Shu%2C%20Y.%20Identifying%20patterns%20in%20financial%20markets%3A%20extending%20the%20statistical%20jump%20model%20for%20regime%20identification%202024) [Scite](/scite_tallies?query=author%3AAyd%C4%B1nhan%2Ctitle%3AIdentifying%20patterns%20in%20financial%20markets%3A%20extending%20the%20statistical%20jump%20model%20for%20regime%20identification%2Cyear%3A2024)

[^Bemporad_et+al_2018_a]: Bemporad, A., V. Breschi, D. Piga, and S. P. Boyd. 2018. Fitting jump models. Automatica 96: 11–21.  [OA](https://engine.scholarcy.com/oa_version?query=Bemporad%2C%20A.%20Breschi%2C%20V.%20Piga%2C%20D.%20Boyd%2C%20S.P.%20Fitting%20jump%20models%202018&author=Bemporad&title=Fitting%20jump%20models&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Bemporad%2C%20A.%20Breschi%2C%20V.%20Piga%2C%20D.%20Boyd%2C%20S.P.%20Fitting%20jump%20models%202018) [Scite](/scite_tallies?query=author%3ABemporad%2Ctitle%3AFitting%20jump%20models%2Cyear%3A2018)

[^Guidolin_2011_a]: Guidolin, M. 2011. Markov switching models in empirical finance. In Missing Data Methods: Time-Series Methods and Applications, vol. 27, ed. D.M. Drukker. Part 2 of Advances in Econometrics, 1–86. Leeds: Emerald Group Publishing Limited.  [OA](https://scholar.google.co.uk/scholar?q=Guidolin%2C%20M.%20Markov%20switching%20models%20in%20empirical%20finance%202011) [GScholar](https://scholar.google.co.uk/scholar?q=Guidolin%2C%20M.%20Markov%20switching%20models%20in%20empirical%20finance%202011) 

[^Nystrup_et+al_2018_a]: Nystrup, P., B. W. Hansen, H. O. Larsen, H. Madsen, and E. Lindström. 2018a. Dynamic allocation or diversification: A regimebased approach to multiple assets. The Journal of Portfolio Management 44 (2): 62–73. Multi-Asset Special Issue.  [OA](https://engine.scholarcy.com/oa_version?query=Nystrup%2C%20P.%20Hansen%2C%20B.W.%20Larsen%2C%20H.O.%20Madsen%2C%20H.%20Dynamic%20allocation%20or%20diversification%3A%20A%20regimebased%20approach%20to%20multiple%20assets%202018&author=Nystrup&title=Dynamic%20allocation%20or%20diversification%3A%20A%20regimebased%20approach%20to%20multiple%20assets&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Nystrup%2C%20P.%20Hansen%2C%20B.W.%20Larsen%2C%20H.O.%20Madsen%2C%20H.%20Dynamic%20allocation%20or%20diversification%3A%20A%20regimebased%20approach%20to%20multiple%20assets%202018) [Scite](/scite_tallies?query=author%3ANystrup%2Ctitle%3ADynamic%20allocation%20or%20diversification%3A%20A%20regimebased%20approach%20to%20multiple%20assets%2Cyear%3A2018)

[^Nystrup_et+al_2020_a]: Nystrup, P., P. N. Kolm, and E. Lindström. 2020. Greedy online classification of persistent market states using realized intraday volatility features. The Journal of Financial Data Science 2 (3): 25–39.  [OA](https://engine.scholarcy.com/oa_version?query=Nystrup%2C%20P.%20Kolm%2C%20P.N.%20Lindstr%C3%B6m%2C%20E.%20Greedy%20online%20classification%20of%20persistent%20market%20states%20using%20realized%20intraday%20volatility%20features%202020&author=Nystrup&title=Greedy%20online%20classification%20of%20persistent%20market%20states%20using%20realized%20intraday%20volatility%20features&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Nystrup%2C%20P.%20Kolm%2C%20P.N.%20Lindstr%C3%B6m%2C%20E.%20Greedy%20online%20classification%20of%20persistent%20market%20states%20using%20realized%20intraday%20volatility%20features%202020) [Scite](/scite_tallies?query=author%3ANystrup%2Ctitle%3AGreedy%20online%20classification%20of%20persistent%20market%20states%20using%20realized%20intraday%20volatility%20features%2Cyear%3A2020)
