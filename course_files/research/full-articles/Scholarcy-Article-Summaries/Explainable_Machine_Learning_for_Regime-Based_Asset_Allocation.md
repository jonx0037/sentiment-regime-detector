[[Zhang_et+al_ExplainableMachineLearningRegimebasedAsset_2020]]

# [Explainable Machine Learning for Regime-Based Asset Allocation](https://doi.org/10.1109/bigdata50022.2020.9378332)

## [[Ruoyun Zhang]]; [[Chao Yi]]; [[Yixin Chen]]

## Abstract
==This paper explores an explainable AI model in the financial industry==. Macroeconomic and market data serve as inputs of Hierarchical Clustering to distinguish among different economic regimes. Compared with traditional models such as Investment Clock, this method can adjust the classification standard in time according to recent market sentiment. The regime, therefore, can be interpreted by not only macro indicators but also investors' mood swings using Artificial Intelligence. ==When we compute the statistical characteristics of returns of each asset, we find that they can be well distinguished among regimes==. This method can also identify the abnormally large wave of the stock market from 2015 to 2016 by separating it as an unusual regime, which cannot be realized by traditional methods. The clustering technique enables us to explain and understand the current market status and predict different assets' performances. Therefore, thanks to the superior interpretability of AI, the mean and variance of returns in each regime are estimated and viewed as viewpoints of the Black-Litterman asset allocation model to construct portfolios. To simulate the real situation, a dynamic backtesting method is used and asset weights change because of the rolling time windows. ==The results show that equipped with a simple timing strategy, the clustering technique can improve the results and yield excess returns==. Some other machine learning techniques are also applied in an attempt to improve the model.

## Key concepts
#market_sentiment; #black_litterman_model; #explainable_machine_learning; #macroeconomic_environment; #asset_allocation; #artificial_intelligence; #machine_learning; #hierarchical_clustering; #mean_variance_model; #bayesian_method

## Quote
> The study proposes a dynamic asset allocation framework that combines economic regime division using hierarchical clustering with the Black-Litterman model, and introduces a rotation of objective optimization functions to solve the imbalanced weights problem and obtain more excess returns.

## Key points
- Asset allocation optimization is one of the most important research fields in asset management
- In the 1950s, Markowitz brought up the mean-variance model, seeking to maximize expected return given level of risk or minimize risk with a certain level of return
- Asset allocation started to change from simple methods such as equal-weighted or 60/40 rule, to the quantitative era
- The Bayesian method used in the Black-Litterman model gives it great flexibility
- The change of macroeconomic environment has a certain ability to explain the performances of assets
- All three BL models applying the clustering technique significantly outperform the benchmark, and the rotation model is significantly better than the others
- Due to its high interpretability by visualization and numerical analysis, an explainable AI model is incorporated into an asset allocation strategy and performs well in the last decade, which shows the great prospects of explainable AI in financial industry


## Summary

### Introduction
The paper explores an explainable AI model for regime-based asset allocation in the financial industry.
Macroeconomic and market data are used as inputs for Hierarchical Clustering to distinguish between different economic regimes.
The model adjusts the classification standard in time according to recent market sentiment, allowing for the interpretation of regimes by both macro indicators and investors' mood swings using Artificial Intelligence.

### Regime Switching
The paper discusses regime switching, including the Merill Lynch Investment Clock theory, which separates the business cycle into four phases: reflation, recovery, overheat, and stagflation.
The authors propose a model that includes more macro factors and reflects the economic status comprehensively using Hierarchical Clustering.
The model divides the economic status into four categories and uses the Ward algorithm to minimize the increment of the sum of squared deviations after the two clusters are merged.

### Asset Allocation
The paper discusses dynamic regime-switching asset allocation using the Black-Litterman model, which combines the market equilibrium and the view of investors.
The model uses the Capital Asset Pricing Model (CAPM) theory to calculate the equilibrium return of the market and integrates the investor's subjective viewpoints of return to obtain the posterior return using the Bayesian method.
The authors use the monthly market technical indicators along with macroeconomic indicators to cluster the economy each month into four regimes and extract historical price information of all assets in the regime to calculate estimated mean and covariance of return.
The results show that the strategy achieves an annual return of 22.53% and a Sharpe ratio of 1.06 from August 2010 to May 2020, outperforming the equal-weighted benchmark model and classical Black-Litterman model.
The asset allocation framework combines the economic regime division by hierarchical clustering with the BL model.
The model preprocesses macroeconomics data with hp filtering and combines it with market technical indicators to divide the economic regimes into four categories using clustering.
The model then assesses the historical returns' performances of all assets and computes the empirical expectation and covariance, which are used as viewpoints to calculate posteriors for the BL model.

### Model Development
The Black-Litterman (BL) model is used with a rotation of objective optimization functions to solve the imbalanced weights problem and obtain more excess returns.
The model combines economic regime division by hierarchical clustering with the BL model.
The rotation of objective optimization functions changes the objective function to seeking maximum return under a risk level of 20% when the stock market volatility exceeds a certain value and there is an upward breakthrough trend.

### Backtesting Results
The backtesting results show that the rotation model outperforms the equal-weighted benchmark portfolio and other counterparties.
The annualized return of the model reaches 22.53%, and the Sharpe ratio is about 1.06.
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
- The return of investment product A is 2% higher than that of B, then
- <mark class="claim">During the backtesting, <mark class="fact">we found that the volatility of stocks can reach</mark> 40%, while the volatility of bonds is stable and remains less than 1%</mark>
- <mark class="claim">All three BL models applying the clustering technique significantly outperform the benchmark, and <mark class="fact">the rotation model is significantly better than the others</mark></mark>
- <mark class="fact">The maximum drawdown of it is constrained below 10%</mark>, much smaller than the maximum return model achieving the second largest annual return in the table

## Contributions
- <mark class="fact">The change of macroeconomic environment has a certain ability to explain the performances of assets</mark>. Market sentiment also explains the rise and fall of prices. <mark class="fact">The fear of future uncertainties prompts people to flock to the gold or bonds market when negative events occur</mark>. It is not uncommon to <mark class="fact">select assets according to investors’ reactions</mark>. Using the AI technique, we are able to explain the market status by both the macroeconomic environment and market sentiment. It allows us to capture information of hotspot events such as policies or natural disasters, which might cause great insecurity among investors. After our analysis and data visualization, <mark class="fact">it can be clearly seen that the AI technique successfully integrates market</mark> and macro data in order to comprehensively recognize the regime. This paper sets an asset allocation framework that combines the economic regime division by hierarchical clustering with the Black-Litterman model. It is also found that setting up the rotation of the objective optimization functions can solve the imbalanced weights problem and obtain more excess returns. Firstly, we preprocess macroeconomics data with hp filtering and combine <mark class="fact">it with market technical indicators to divide the economic regimes into four categories using clustering</mark>. Then, for each regime, we assess the historical returns’ performances of all assets and compute the empirical expectation and covariance. <mark class="fact">They are used as viewpoints to calculate posteriors for the BL model</mark>. BL optimization weights are then calculated through the rotation of the objective optimization functions to achieve dynamic asset allocation. <mark class="claim">The results show that during the backtest period from August 2010 to May 2020, the annualized return of the model reaches 22.53%, and the Sharpe ratio is about 1.06, <mark class="fact">which is significantly better than the equal-weighted benchmark portfolio</mark> and other counterparties</mark>. The model integrates macro-scenarios and has strong flexibility. <mark class="fact">It can respond to market fluctuations in a timely manner</mark>. Experiments show that it successfully captures two large upswing signals of the stock market and withdraws before the plunge. In conclusion, due to its high interpretability by visualization and numerical analysis, <mark class="fact">an explainable AI model is incorporated into an asset allocation strategy</mark> and performs well in the last decade, <mark class="fact">which shows the great prospects of explainable AI in financial industry</mark>.

## Limitations
- The study has some limitations, including the use of a limited dataset and the reliance on historical data. The study also assumes that the market equilibrium weight is calculated as the ratio of investment product market value and total market value.
- The study does not discuss the limitations of the proposed framework, but mentions that the use of historical returns as inputs to the Black-Litterman model may not be reasonable.
- The limitations of the research are not addressed in the provided text.

## Future work
- The study suggests that future work could include the use of more advanced machine learning techniques, such as deep learning. The study also suggests that future work could include the use of more diverse datasets, including alternative data sources.
- There is no discussion of future work in the given text.


## References
[^1]: Black, Fischer, and Robert Litterman. “Global portfolio optimization, ” Financial analysts journal 48.5 (1992): 28-43.  [OA](https://engine.scholarcy.com/oa_version?query=Black%2C%20Fischer%20Litterman%2C%20Robert%20Global%20portfolio%20optimization%201992&author=Black&title=Global%20portfolio%20optimization&year=1992) [GScholar](https://scholar.google.co.uk/scholar?q=Black%2C%20Fischer%20Litterman%2C%20Robert%20Global%20portfolio%20optimization%201992) [Scite](/scite_tallies?query=author%3ABlack%2Ctitle%3AGlobal%20portfolio%20optimization%2Cyear%3A1992)

[^2]: He, Guangliang, and Robert Litterman. “The intuition behind BlackLitterman model portfolios, ” Available at SSRN 334304(2002).  [OA](https://engine.scholarcy.com/oa_version?query=He%2C%20Guangliang%20Litterman%2C%20Robert%20The%20intuition%20behind%20BlackLitterman%20model%20portfolios%202002&author=He&title=The%20intuition%20behind%20BlackLitterman%20model%20portfolios&year=2002) [GScholar](https://scholar.google.co.uk/scholar?q=He%2C%20Guangliang%20Litterman%2C%20Robert%20The%20intuition%20behind%20BlackLitterman%20model%20portfolios%202002) [Scite](/scite_tallies?query=author%3AHe%2Ctitle%3AThe%20intuition%20behind%20BlackLitterman%20model%20portfolios%2Cyear%3A2002)

[^3]: Martellini, Lionel, and Volker Ziemann. “Extending Black-Litterman analysis beyond the mean-variance framework,” The Journal of Portfolio Management 33.4 (2007): 33-44.  [OA](https://engine.scholarcy.com/oa_version?query=Martellini%2C%20Lionel%20Ziemann%2C%20Volker%20Extending%20Black-Litterman%20analysis%20beyond%20the%20mean-variance%20framework%202007&author=Martellini&title=Extending%20Black-Litterman%20analysis%20beyond%20the%20mean-variance%20framework&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Martellini%2C%20Lionel%20Ziemann%2C%20Volker%20Extending%20Black-Litterman%20analysis%20beyond%20the%20mean-variance%20framework%202007) [Scite](/scite_tallies?query=author%3AMartellini%2Ctitle%3AExtending%20Black-Litterman%20analysis%20beyond%20the%20mean-variance%20framework%2Cyear%3A2007)

[^4]: Zhou, Guofu. “Beyond Black–Litterman: Letting the Data Speak, ” The Journal of Portfolio Management 36.1 (2009): 36-45.  [OA](https://engine.scholarcy.com/oa_version?query=Zhou%2C%20Guofu%20Beyond%20Black%E2%80%93Litterman%3A%20Letting%20the%20Data%20Speak%202009&author=Zhou&title=Beyond%20Black%E2%80%93Litterman%3A%20Letting%20the%20Data%20Speak&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Zhou%2C%20Guofu%20Beyond%20Black%E2%80%93Litterman%3A%20Letting%20the%20Data%20Speak%202009) [Scite](/scite_tallies?query=author%3AZhou%2Ctitle%3ABeyond%20Black%E2%80%93Litterman%3A%20Letting%20the%20Data%20Speak%2Cyear%3A2009)

[^5]: Xing, Frank Z., et al. “Discovering Bayesian market views for intelligent asset allocation, ” Joint European Conference on Machine Learning and Knowledge Discovery in Databases. Springer, Cham, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Xing%2C%20Frank%20Z.%20Discovering%20Bayesian%20market%20views%20for%20intelligent%20asset%20allocation%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Xing%2C%20Frank%20Z.%20Discovering%20Bayesian%20market%20views%20for%20intelligent%20asset%20allocation%202018) 

[^6]: Chong, James, and G. Michael Phillips. “Tactical Asset Allocation with Macroeconomic Factors,” The Journal of Wealth Management 17.1 (2014): 58-69.  [OA](https://engine.scholarcy.com/oa_version?query=Chong%2C%20James%20Phillips%2C%20G.Michael%20Tactical%20Asset%20Allocation%20with%20Macroeconomic%20Factors%202014&author=Chong&title=Tactical%20Asset%20Allocation%20with%20Macroeconomic%20Factors&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Chong%2C%20James%20Phillips%2C%20G.Michael%20Tactical%20Asset%20Allocation%20with%20Macroeconomic%20Factors%202014) [Scite](/scite_tallies?query=author%3AChong%2Ctitle%3ATactical%20Asset%20Allocation%20with%20Macroeconomic%20Factors%2Cyear%3A2014)

[^7]: Sheikh, Abdullah Z., and Jianxiong Sun. “Regime change: Implications of macroeconomic shifts on asset class and portfolio performance,” The Journal of Investing 21.3 (2012): 36-54.  [OA](https://engine.scholarcy.com/oa_version?query=Sheikh%2C%20Abdullah%20Z.%20Sun%2C%20Jianxiong%20Regime%20change%3A%20Implications%20of%20macroeconomic%20shifts%20on%20asset%20class%20and%20portfolio%20performance%202012&author=Sheikh&title=Regime%20change%3A%20Implications%20of%20macroeconomic%20shifts%20on%20asset%20class%20and%20portfolio%20performance&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Sheikh%2C%20Abdullah%20Z.%20Sun%2C%20Jianxiong%20Regime%20change%3A%20Implications%20of%20macroeconomic%20shifts%20on%20asset%20class%20and%20portfolio%20performance%202012) [Scite](/scite_tallies?query=author%3ASheikh%2Ctitle%3ARegime%20change%3A%20Implications%20of%20macroeconomic%20shifts%20on%20asset%20class%20and%20portfolio%20performance%2Cyear%3A2012)

[^8]: Kollar, Miroslav. “A Sketch of Macro-based Asset Allocation,” International Journal of Economic Sciences 2.3 (2013): 101-120.  [OA](https://engine.scholarcy.com/oa_version?query=Kollar%2C%20Miroslav%20A%20Sketch%20of%20Macro-based%20Asset%20Allocation%202013&author=Kollar&title=A%20Sketch%20of%20Macro-based%20Asset%20Allocation&year=2013) [GScholar](https://scholar.google.co.uk/scholar?q=Kollar%2C%20Miroslav%20A%20Sketch%20of%20Macro-based%20Asset%20Allocation%202013) [Scite](/scite_tallies?query=author%3AKollar%2Ctitle%3AA%20Sketch%20of%20Macro-based%20Asset%20Allocation%2Cyear%3A2013)

[^9]: Graham, John R., and Campbell R. Harvey. “Market timing ability and volatility implied in investment newsletters&#39; asset allocation recommendations,” Journal of Financial Economics42.3 (1996): 397421.  [OA](https://engine.scholarcy.com/oa_version?query=Graham%2C%20John%20R.%20Harvey%2C%20Campbell%20R.%20Market%20timing%20ability%20and%20volatility%20implied%20in%20investment%20newsletters%27%20asset%20allocation%20recommendations%201996&author=Graham&title=Market%20timing%20ability%20and%20volatility%20implied%20in%20investment%20newsletters%27%20asset%20allocation%20recommendations&year=1996) [GScholar](https://scholar.google.co.uk/scholar?q=Graham%2C%20John%20R.%20Harvey%2C%20Campbell%20R.%20Market%20timing%20ability%20and%20volatility%20implied%20in%20investment%20newsletters%27%20asset%20allocation%20recommendations%201996) [Scite](/scite_tallies?query=author%3AGraham%2Ctitle%3AMarket%20timing%20ability%20and%20volatility%20implied%20in%20investment%20newsletters%27%20asset%20allocation%20recommendations%2Cyear%3A1996)

[^10]: Clare, Andrew, et al. “The trend is our friend: Risk parity, momentum and trend following in global asset allocation,” Journal of Behavioral and Experimental Finance 9 (2016): 63-80.  [OA](https://engine.scholarcy.com/oa_version?query=Clare%2C%20Andrew%20The%20trend%20is%20our%20friend%3A%20Risk%20parity%2C%20momentum%20and%20trend%20following%20in%20global%20asset%20allocation%202016&author=Clare&title=The%20trend%20is%20our%20friend%3A%20Risk%20parity%2C%20momentum%20and%20trend%20following%20in%20global%20asset%20allocation&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Clare%2C%20Andrew%20The%20trend%20is%20our%20friend%3A%20Risk%20parity%2C%20momentum%20and%20trend%20following%20in%20global%20asset%20allocation%202016) [Scite](/scite_tallies?query=author%3AClare%2Ctitle%3AThe%20trend%20is%20our%20friend%3A%20Risk%20parity%2C%20momentum%20and%20trend%20following%20in%20global%20asset%20allocation%2Cyear%3A2016)

[^11]: Chen, Haiqiang, Terence Tai-Leung Chong, and Xin Duan. “A principalcomponent approach to measuring investor sentiment, ” Quantitative Finance 10.4 (2010): 339-347.  [OA](https://engine.scholarcy.com/oa_version?query=Chen%2C%20Haiqiang%20Chong%2C%20Terence%20Tai-Leung%20Duan%2C%20Xin%20A%20principalcomponent%20approach%20to%20measuring%20investor%20sentiment%202010&author=Chen&title=A%20principalcomponent%20approach%20to%20measuring%20investor%20sentiment&year=2010) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%2C%20Haiqiang%20Chong%2C%20Terence%20Tai-Leung%20Duan%2C%20Xin%20A%20principalcomponent%20approach%20to%20measuring%20investor%20sentiment%202010) [Scite](/scite_tallies?query=author%3AChen%2Ctitle%3AA%20principalcomponent%20approach%20to%20measuring%20investor%20sentiment%2Cyear%3A2010)

[^12]: Malandri, Lorenzo, et al. “Public mood–driven asset allocation: the importance of financial sentiment in portfolio management,” Cognitive Computation 10.6 (2018): 1167-1176.  [OA](https://engine.scholarcy.com/oa_version?query=Malandri%2C%20Lorenzo%20Public%20mood%E2%80%93driven%20asset%20allocation%3A%20the%20importance%20of%20financial%20sentiment%20in%20portfolio%20management%202018&author=Malandri&title=Public%20mood%E2%80%93driven%20asset%20allocation%3A%20the%20importance%20of%20financial%20sentiment%20in%20portfolio%20management&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Malandri%2C%20Lorenzo%20Public%20mood%E2%80%93driven%20asset%20allocation%3A%20the%20importance%20of%20financial%20sentiment%20in%20portfolio%20management%202018) [Scite](/scite_tallies?query=author%3AMalandri%2Ctitle%3APublic%20mood%E2%80%93driven%20asset%20allocation%3A%20the%20importance%20of%20financial%20sentiment%20in%20portfolio%20management%2Cyear%3A2018)

[^13]: Raffinot, Thomas. “Hierarchical clustering-based asset allocation,” The Journal of Portfolio Management 44.2 (2017): 89-99.  [OA](https://engine.scholarcy.com/oa_version?query=Raffinot%2C%20Thomas%20Hierarchical%20clustering-based%20asset%20allocation%202017&author=Raffinot&title=Hierarchical%20clustering-based%20asset%20allocation&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Raffinot%2C%20Thomas%20Hierarchical%20clustering-based%20asset%20allocation%202017) [Scite](/scite_tallies?query=author%3ARaffinot%2Ctitle%3AHierarchical%20clustering-based%20asset%20allocation%2Cyear%3A2017)

[^14]: Snow, Derek. “Machine Learning in Asset Management—Part 2: Portfolio Construction—Weight Optimization,” The Journal of Financial Data Science 2.2 (2020): 17-24.  [OA](https://engine.scholarcy.com/oa_version?query=Snow%2C%20Derek%20Machine%20Learning%20in%20Asset%20Management%E2%80%94Part%202%3A%20Portfolio%20Construction%E2%80%94Weight%20Optimization%202020&author=Snow&title=Machine%20Learning%20in%20Asset%20Management%E2%80%94Part%202%3A%20Portfolio%20Construction%E2%80%94Weight%20Optimization&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Snow%2C%20Derek%20Machine%20Learning%20in%20Asset%20Management%E2%80%94Part%202%3A%20Portfolio%20Construction%E2%80%94Weight%20Optimization%202020) [Scite](/scite_tallies?query=author%3ASnow%2Ctitle%3AMachine%20Learning%20in%20Asset%20Management%E2%80%94Part%202%3A%20Portfolio%20Construction%E2%80%94Weight%20Optimization%2Cyear%3A2020)

[^15]: Greetham, Trevor, and H. Hartnett. “The Investment Clock Special Report# 1: Making Money From Macro,” Merrill Lynch, 2004.   [OA](https://scholar.google.co.uk/scholar?q=Greetham%2C%20Trevor%20Hartnett%2C%20H.%20The%20Investment%20Clock%20Special%20Report%23%201%3A%20Making%20Money%20From%20Macro%202004) [GScholar](https://scholar.google.co.uk/scholar?q=Greetham%2C%20Trevor%20Hartnett%2C%20H.%20The%20Investment%20Clock%20Special%20Report%23%201%3A%20Making%20Money%20From%20Macro%202004) 

