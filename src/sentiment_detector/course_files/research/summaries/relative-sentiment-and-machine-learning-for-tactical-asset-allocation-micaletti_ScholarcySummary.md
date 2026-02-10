[[Micaletti_RelativeSentimentMachineLearningTactical_2022]]

# [Relative Sentiment and Machine Learning for Tactical Asset Allocation]()

## [[Raymond C. Micaletti]]

## Abstract

We examine Sentix sentiment indices for use in tactical asset allocation. In particular, we construct monthly relative sentiment factors for the U.S., Europe, Japan, and Asia ex-Japan by taking the difference in 6-month economic expectations between each region’s institutional and individual investors. These factors (along with one-month forward equity returns) then serve as inputs to a wide array of machine learning algorithms. Employing combinatorial cross-validation and adjusting for data snooping, we find relative sentiment factors have robust and significant predictive power in all four regions; that they surpass both standalone sentiment and time-series momentum in terms of informational content; and that they demonstrate the ability to identify the subsequent best- and worst-performing global equity markets from along a cross-section. The results are consistent with previous findings on relative sentiment, discovered using unrelated datasets.

## Key concepts

# claim/support_vector_machines; #support_vector_machines; #claim/predictive_power; #predictive_power; #claim/machine_learning; #machine_learning; #claim/equity_market; #equity_market; #n_m

## Quote

This study examines the use of Sentix sentiment indices in tactical asset allocation and finds that relative sentiment factors have robust, significant predictive power across all four regions, surpassing standalone sentiment and time-series momentum.

## Key points

- While the effectiveness of machine learning techniques for predicting financial markets has been called into question (e.g., Makridakis et al (2018)), we find several of the machine learning techniques investigated here, in conjunction with various combinations of relative sentiment factors, produce statistically significant results, even after adjusting for data snooping
- For the support vector machines (SVM) algorithms, we considered several different parameter combinations
- We examine whether the rank order of relative sentiment across regions is predictive of one-month forward relative equity market returns
- The present study, which investigates relative sentiment factors derived from Sentix economic sentiment indices, corroborates those findings and adds to that body of evidence
- We observe that the best performing relative sentiment strategies from region to region tended to be produced by the same handful of machine learning algorithms

## Summary

### Introduction

The study examines Sentix sentiment indices for use in tactical asset allocation, constructing monthly relative sentiment factors for the U.S, Europe, Japan, and Asia ex-Japan.
These factors are used as inputs to machine learning algorithms to forecast one-month forward equity returns.

### Methodology

The dataset consists of Sentix 6-month economic expectations indices for the U.S., Europe, Japan, and Asia ex-Japan, available on platforms such as Bloomberg and FactSet.
The indices are the result of a monthly online survey conducted by Sentix, and the data timestamp is set to the end of the month.
Relative sentiment factors are constructed by subtracting the private sentiment from the institutional sentiment for each region.
The study uses combinatorial cross-validation and adjusts for data snooping to evaluate the performance of the machine learning models.
The study used 90 machine learning models, with 11 factor subsets, resulting in 990 backtests of relative sentiment for each regional equity market.
The models were trained using two different cross-validation (CCV) procedures, CCV{15,2} and CCV{24,2}, which used 85% and 75% of the data for training, respectively.
The study also applied component sentiment analysis to decompose the relative sentiment factors into their component sentiments.

### Results

The study finds that relative sentiment factors have robust, significant predictive power across all four regions, surpassing both standalone sentiment and time-series momentum in terms of informational content.
The results are consistent with previous findings on relative sentiment and demonstrate the ability to identify the subsequent best- and worst-performing global equity markets from along a cross-section.
The study also finds that relative sentiment works not only for U.S. markets but also for global markets and that it has more predictive power than time-series momentum.
The study found that relative sentiment far surpassed component sentiment in terms of statistical significance, with several dozen relative sentiment strategies registering as significant at the most extreme values of α.
The number of significant strategies declined slightly for CCV{24,2}, as fewer points were used to train the models.
The study also found that relative sentiment produced both more significant strategies and strategies that registered greater extreme significance than component sentiment.

### Performance

The composite relative sentiment strategies in the U.S. outperformed their benchmarks by roughly 650-700 basis points per annum over the 17-year period, yielding a total return approximately three times that of the benchmark.
The strategies achieved higher Sharpe ratios and lower maximum drawdowns, with average monthly equity allocations around 73% and average monthly turnover between 26% and 30%.
Similar patterns were observed in Europe, Japan, and Asia ex-Japan, with relative sentiment strategies outperforming their benchmarks by 400-550 basis points per annum.

### Relative Sentiment

Relative sentiment appears to drive directional returns, regardless of the state of time-series momentum.
The state of relative sentiment is a more powerful predictor of subsequent returns than momentum.
When time-series momentum is negative, but relative sentiment is positive, the annualized average one-month forward return over all regions is approximately 27%.
In contrast, when momentum is negative and relative sentiment is also negative, the annualized average one-month forward return over all regions is approximately -23%—a difference of 50 percentage points depending on the state of relative sentiment.

### Cross-Sectional Returns

Relative sentiment is predictive of equity market performance across regions.
The rank order of relative sentiment across regions is predictive of one-month forward relative equity market returns.
The concatenated returns of the sequentially top-ranked regions produced a total return of 883% over the test period, while the lowest-ranked regions mustered a total return of just 248%.
The annualized average difference in one-month forward returns for every head-to-head matchup between regions is positive, meaning the region with higher-ranked relative sentiment tended to outperform the region with lower-ranked relative sentiment over a one-month horizon.

### Machine Learning Algorithms

The best-performing relative sentiment strategies across regions tended to be produced by the same handful of machine learning algorithms, including generalized boosted models, random forests, and certain types of support vector machines.
This consistency suggests there might be some underlying structure to the data that these algorithms are uniquely suited to uncover.
The top-performing algorithms in each region are listed in tables, along with their factor subsets and relevant parameters.

## Study subjects

### 10000 bootstrap samples

- We consider three MHT algorithms, namely, the Step-RC method (RC = “Reality Check”) ([^Romano_2007_a])), the Step-SPA method (SPA = “Superior Predictive Ability”) (Hsu et al (2014)), and a method found in the R package “multtest” (using the function “mhp”) ([^Pollard_et+al_2005_a])). Each approach is bootstrap-based, and we use 10,000 bootstrap samples in our testing. The aforementioned MHT algorithms are all designed to control the “k-family-wise error rate” (k-FWER), i.e., the probability of identifying at least k false positives amongst all the strategies identified as significant

## Findings

- <mark class="claim">We report results for both cases</mark>

## Confirmation of earlier findings

- 1. And lastly, it corroborates the results in [^Micaletti_2019_a], which show that relative sentiment has the potential to identify the subsequent best- and worst-performing markets across a cross-section.
- The annualized average one-month forward return spread between positive and negative relative sentiment in this case is approximately 22%. These results are consistent with [^Micaletti_2018_a], which found similar annualized spreads in U.S equity market returns depending on the state of relative sentiment.
- This suggests relative sentiment might indeed have predictive power along the cross-section. These results are consistent with [^Micaletti_2019_a], which reported similar effects using a positions-based relative sentiment indicator derived from the Commitments of Traders report.
- The composites of the top 10 relative sentiment strategies in each region outperformed their respective benchmarks by anywhere from 400 to 700 basis points per annum with higher Sharpe ratios and lower drawdowns. (Such levels would likely survive any realistic transaction-cost assumptions.) Moreover, it again appears as though relative sentiment may provide more predictive power than time-series momentum, confirming the results in [^Micaletti_2018_a].
- A similar (though not as dramatic) result was observed when momentum was positive. Beyond demonstrating the ability to beneficially adjust equity allocations within regions, relative sentiment also demonstrated the ability to adjust equity allocations across regions (affirming the results in [^Micaletti_2019_a]).

## Contributions

- Past work on relative sentiment, whether direct or indirect, has unearthed substantial evidence of its predictive power for equity markets over intermediate time horizons. The present study, <mark class="fact">which investigates relative sentiment factors derived from Sentix economic sentiment indices</mark> (for the U.S, Europe, Japan, and Asia ex-Japan), corroborates those findings and adds to that body of evidence. Sentix-based relative sentiment factors, coupled with certain machine learning models, appear to generate statistically significant tactical asset allocation strategies for regional equity markets. Of the nearly 1000 relative sentiment strategies tested, dozens to several hundred (depending on the region) registered as significant after adjusting for data snooping. The levels of significance ranged from moderate in Asia (excluding Japan) and Europe to strong in Japan to extremely strong in the U.S.

## Limitations

- The study notes that the effectiveness of machine learning techniques for predicting financial markets has been called into question. The study also notes that the dataset used has a three-month period, from October 2002 to December 2002, missing.
- The study notes that the results may be subject to data snooping bias and that the use of multiple hypothesis testing algorithms is necessary to control for this bias.
- The study does not discuss any limitations of the research, but it does note that the results are robust to the number of relative sentiment strategies used to generate the composite equity allocations.

## Future work

- The study suggests that future work could involve examining relative sentiment factors in other markets and regions. The study also suggests that future work could involve using other machine learning algorithms and techniques to forecast equity returns.
- The study suggests that future research could focus on exploring the use of relative sentiment in other markets and asset classes, and on developing more sophisticated machine learning models to predict equity market returns.

## References

[^Micaletti_2018_a]: Micaletti, Raymond, 2018, Want smart beta? follow the smart money: Market and factor timing using relative sentiment, SSRN Electronic Journal, URL: <https://ssrn.com/abstract=3164081>.  [OA](https://ssrn.com/abstract=3164081)  [Scite](/scite_tallies?query=author%3AMicaletti%2Ctitle%3AWant%20smart%20beta%3F%20follow%20the%20smart%20money%3A%20Market%20and%20factor%20timing%20using%20relative%20sentiment%2Cyear%3A2018)

[^Micaletti_2019_a]: Micaletti, Raymond, 2019, The smart money indicator: A new risk-management tool, Alpha Architect, URL: <https://alphaarchitect.com/2019/02/08/relative-sentiment-aunique-market-timing-tool-that-isnt-trend-following>.  [OA](https://alphaarchitect.com/2019/02/08/relative-sentiment-aunique-market-timing-tool-that-isnt-trend-following)  [Scite](/scite_tallies?query=author%3AMicaletti%2Ctitle%3AThe%20smart%20money%20indicator%3A%20A%20new%20risk-management%20tool%2Cyear%3A2019)

[^Pollard_et+al_2005_a]: Pollard, Katherine S., Sandrine Dudoit, and Mark J. van der Laan, 2005, Multiple Testing Procedures: R multtest Package and Applications to Genomics, in Bioinformatics and Computational Biology Solutions Using R and Bioconductor (Springer).  [OA](https://scholar.google.co.uk/scholar?q=Pollard%20Katherine%20S%20Sandrine%20Dudoit%20and%20Mark%20J%20van%20der%20Laan%202005%20Multiple%20Testing%20Procedures%20R%20multtest%20Package%20and%20Applications%20to%20Genomics%20in%20Bioinformatics%20and%20Computational%20Biology%20Solutions%20Using%20R%20and%20Bioconductor%20Springer) [GScholar](https://scholar.google.co.uk/scholar?q=Pollard%20Katherine%20S%20Sandrine%20Dudoit%20and%20Mark%20J%20van%20der%20Laan%202005%20Multiple%20Testing%20Procedures%20R%20multtest%20Package%20and%20Applications%20to%20Genomics%20in%20Bioinformatics%20and%20Computational%20Biology%20Solutions%20Using%20R%20and%20Bioconductor%20Springer)

[^Romano_2007_a]: Romano, Joseph P., and Michael Wolf, 2007, Control of generalized error rates in multiple testing, Annals of Statistics 35, 1378–1408.  [OA](https://engine.scholarcy.com/oa_version?query=Romano%2C%20Joseph%20P.%20Wolf%2C%20Michael%20Control%20of%20generalized%20error%20rates%20in%20multiple%20testing%202007&author=Romano&title=Control%20of%20generalized%20error%20rates%20in%20multiple%20testing&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Romano%2C%20Joseph%20P.%20Wolf%2C%20Michael%20Control%20of%20generalized%20error%20rates%20in%20multiple%20testing%202007) [Scite](/scite_tallies?query=author%3ARomano%2Ctitle%3AControl%20of%20generalized%20error%20rates%20in%20multiple%20testing%2Cyear%3A2007)
