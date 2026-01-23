[[Bollen_et+al_TwitterMoodPredictsStockMarket_2011]]

# [Twitter mood predicts the stock market](https://doi.org/10.1016/j.jocs.2010.12.007)

## [[Johan Bollen]]; [[Huina Mao]]; [[Xiao‐Jun Zeng]]

## Abstract

Behavioral economics tells us that emotions can profoundly affect individual behavior and decisionmaking. ==Does this also apply to societies at large, i.e. can societies experience mood states that affect their collective decision making? By extension is the public mood correlated or even predictive of economic indicators? Here we investigate whether measurements of collective mood states derived from largescale Twitter feeds are correlated to the value of the Dow Jones Industrial Average (DJIA) over time==. We analyze the text content of daily Twitter feeds by two mood tracking tools, namely OpinionFinder that measures positive vs. negative mood and Google-Profile of Mood States (GPOMS) that measures mood in terms of 6 dimensions (Calm, Alert, Sure, Vital, Kind, and Happy). We cross-validate the resulting mood time series by comparing their ability to detect the public’s response to the presidential election and Thanksgiving day in 2008. A Granger causality analysis and a Self-Organizing Fuzzy Neural Network are then used to investigate the hypothesis that public mood states, as measured by the OpinionFinder and GPOMS mood time series, are predictive of changes in DJIA closing values. ==Our results indicate that the accuracy of DJIA predictions can be significantly improved by the inclusion of specific public mood dimensions but not others==. ==We find an accuracy of 86.7% in predicting the daily up and down changes in the closing values of the DJIA and a reduction of the Mean Average Percentage Error (MAPE) by more than 6%==.

## Key concepts

# claim/stock_market_prediction; #stock_market_prediction; #finding/dow_jones_industrial_average; #dow_jones_industrial_average; #stock_market

## Quote
>
> The study investigates whether measurements of collective mood states derived from large-scale Twitter feeds are correlated to the value of the Dow Jones Industrial Average (DJIA) over time, finding that the accuracy of DJIA predictions can be significantly improved by the inclusion of specific public mood dimensions.

## Key points

- Stock market prediction has attracted much attention from academia as well as business
- 8 Gilbert and Karahalios [^17] uses only one mood index, namely Anxiety, but we investigate the relation between Dow Jones Industrial Average (DJIA) values and all Twitter mood dimensions measured by Google-Profile of Mood States (GPOMS) and OpinionFinder
- Our results show that changes in the public mood state can be tracked from the content of large-scale Twitter feeds by means of rather simple text processing techniques and that such changes respond to a variety of socio-cultural drivers in a highly differentiated manner
- We do not observe this effect for OpinionFinder’s assessment of public mood states in terms of positive vs. negative mood but rather for the GPOMS dimension labeled “Calm”
- A Self-Organizing Fuzzy Neural Network trained on the basis of past DJIA values and our public mood time series demonstrated the ability of the latter to significantly improve the accuracy of even the most basic models to predict DJIA closing values
- Compared to I0 and all other input combinations, adding input I1 leads to significant improvements in Mean Average Percentage Error (MAPE) values (1.83% vs. the maximum of 2.13% and 1.95% for IOF) and direction accuracy (86.7% compared to 73.3% for IOF and 46.7% for I1,3)
- Given the performance increase for a relatively basic model such as the Self-organizing Fuzzy Neural Network (SOFNN) we are hopeful to find equal or better improvements for more sophisticated market models that may include other information derived from news sources, and a variety of relevant economic indicators

## Summary

### Introduction

Behavioral economics suggests that emotions can affect individual behavior and decision-making, and this may also apply to societies at large.
The study investigates whether measurements of collective mood states derived from large-scale Twitter feeds are correlated to the value of the Dow Jones Industrial Average (DJIA) over time.

### Methodology

The study uses two mood tracking tools, OpinionFinder and Google-Profile of Mood States (GPOMS), to analyze the text content of daily Twitter feeds.
OpinionFinder measures positive vs. negative mood, while GPOMS measures mood in terms of 6 dimensions (Calm, Alert, Sure, Vital, Kind, and Happy).
The resulting mood time series are correlated to the DJIA to assess their ability to predict changes in the DJIA over time.
The study uses OpinionFinder (OF) and GPOMS measurements to analyze public mood responses to significant events, such as the Presidential election and Thanksgiving.
The resulting mood time series are expressed in z-scores.
The researchers apply multiple regression to test the correlation between OF lexicon and GPOMS dimensions, and Granger causality analysis to determine the relationship between mood time series and DJIA values.
The study used a Self-Organizing Fuzzy Neural Network (SOFNN) to predict DJIA values based on historical data and public mood states extracted from Twitter feeds.
The SOFNN was trained on data from December 1 to December 19, 2008, and its performance was evaluated using metrics such as Mean Absolute Percentage Error (MAPE) and direction accuracy.
The study also used Granger causality analysis to determine the relationship between public mood states and DJIA values.

### Results

The study finds that the accuracy of DJIA predictions can be significantly improved by the inclusion of specific public mood dimensions, but not others.
Variations along the public mood dimensions of Calm and Happiness as measured by GPOMS seem to have a predictive effect, but not general happiness as measured by the OpinionFinder tool.
The study achieves an accuracy of 86.7% in predicting the daily up and down changes in the closing values of the DJIA and a reduction of the Mean Average Percentage Error (MAPE) by more than 6%.
The GPOMS results reveal a differentiated public mood response to the Presidential election, with significant drops in Calm and increases in Vital, Happy, and Kind scores on election day.
The public mood response to Thanksgiving shows a spike in Happy values, but no other elevated mood dimensions.
The study finds that GPOMS' Happy dimension best approximates the mood trend provided by OpinionFinder.
The multiple linear regression results indicate that YOF is significantly correlated with X3 (Sure), X4 (Vital), and X6 (Happy).
The Granger causality analysis shows that X1 (Calm) has the highest Granger causality relation with DJIA for lags ranging from 2 to 6 days.
The results showed that adding Calm, a mood dimension extracted using the GPOMS method, to the SOFNN model significantly improved its prediction accuracy.
The combination of Calm and Happy, another mood dimension, also produced accurate results, despite Happy not having a strong Granger causality relation with DJIA.
The study found that the SOFNN's direction accuracy was 87.6%, which is unlikely to occur by chance.
The results also suggested a nonlinear relationship between the mood dimensions and DJIA values.

### Modeling

The study uses a Self-organizing Fuzzy Neural Network (SOFNN) model to predict DJIA values based on past DJIA values and mood time series.
The SOFNN model is compared to a baseline model that only uses historical DJIA values.
The results show that the SOFNN model with mood time series inputs outperforms the baseline model, indicating that public mood assessments can improve predictive models of DJIA values.
The study investigates seven permutations of input variables to the SOFNN model, including combinations of historical DJIA values and GPOMS mood dimensions.

### Implications

The study's findings have implications for sentiment tracking tools and surveys of self-reported subjective well-being.
Public mood analysis from Twitter feeds offers a fast, free, and large-scale addition to these tools, which can be optimized to measure various dimensions of public mood.
However, the study acknowledges limitations, such as geographical and cultural sampling errors, and the need for future research to examine the causative mechanisms between public mood states and DJIA values, as well as social and cognitive effects in online social networking environments.

## Study subjects

### 9853498 tweets

- Data and methods overview. ==We obtained a collection of public tweets that was recorded from February 28 to December 19th, 2008 (9,853,498 tweets posted by approximately 2.7 M users)==. For each tweet these records provide a tweet identifier, the date–time of the submission (GMT+0), its submission type, and the text content of the Tweet which is by design limited to 140 characters

### 342255 tweets

- We perform the Granger causality analysis according to model L1 and L2 shown in Eqs. (3) and (4) for the period of time between February 28 to November 3, 2008 to exclude the exceptional public mood response to the Presidential Election and Thanksgiving from the comparison. ==GPOMS and OpinionFinder time series were produced for 342,255 tweets in that period, and the daily Dow Jones Industrial Average (DJIA) was retrieved from Yahoo! Finance for each day.9 n==. L1 : Dt =  ̨ + ˇiDt−i + εt

## Data analysis

- #method/sofnn_model
- #method/consumer_confidence_index
- #method/
- #method/time_series_analysis
- #method/linear_regression
- #method/questionnaire
- #method/linear_models

## Findings

- <mark class="claim"><mark class="fact">Our results indicate that the accuracy of DJIA predictions can be significantly improved by the inclusion</mark> of specific public mood dimensions but not others</mark>
- <mark class="claim"><mark class="fact">We find an accuracy of 86.7%</mark> in predicting the daily up and down changes in the closing values of the DJIA and a reduction of the Mean Average Percentage Error (MAPE) by more than 6%</mark>
- Since news is unpredictable, [stock market](https://en.wikipedia.org/wiki/Stock_market "stock market") prices will follow a random walk pattern and cannot be predicted with more than 50% accuracy [^43]
- The multiple linear regression results are provided in Table 1 (coefficient and p-values), and indicate that YOF is significantly correlated with X3 (Sure), X4 (Vital) and X6 (Happy), but not with X1 (Calm), X2 (Alert) and X5 (Kind)
- In fact the p-value for this shorter period, i.e. August 1, 2008 to October 30, 2008, is significantly lower (lag n−3, p = 0.009) than that listed in Table 2 for the period February 28, 2008 to November 3, 2008
- Compared to I0 and all other input combinations, adding input I1 leads to significant improvements in [MAPE](# "Mean Average Percentage Error") values (1.83% vs. the maximum of 2.13% and 1.95% for IOF) and direction accuracy (86.7% compared to 73.3% for IOF and 46.7% for I1,3)
- It is notable that I1,6, i.e. a combination of X6 and X1 does significantly reduce average [MAPE](# "Mean Average Percentage Error"), and provides good direction accuracy (80%)
- In combination with Calm, it produces a more accurate [SOFNN](# "Self-organizing Fuzzy Neural Network") prediction ([MAPE](# "Mean Average Percentage Error") = 1.79%) and direction accuracy (80%)
- To assess the statistical significance of the [SOFNN](# "Self-organizing Fuzzy Neural Network") achieving the above mentioned accuracy of 87.6% in predicting the up and down movement of the [DJIA](https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average "Dow Jones Industrial Average") we calculate the odds of this result occurring by chance

## Builds on previous research

- However, Granger causality analysis is based on linear regression whereas the relation between public mood and stock market values is almost certainly non-linear. ==To better address these non-linear effects and assess the contribution that public mood assessments can make in predictive models of DJIA values, we compare the performance of a Self-organizing Fuzzy Neural Network== (SOFNN) model [^28] that predicts DJIA values on the basis of two sets of inputs: (1) the past 3 days of DJIA values, and (2) the same combined with various permutations of our mood time series (explained below).
- Compared with some notable fuzzy nerural network models, such as the adaptive-network-based fuzzy inference systems (ANFIS) [^22], self-organizing dynamic fuzzy neural network (DFNN) [^11] and GDFNN [^49], SOFNN provides a more efficient algorithm for online learning due to its simple and effective parameter and structure learning algorithm [^28]. In ==our previous work, SOFNN has proven its value in electrical load forecasting== [^32], exchange rate forecasting [^28] and other applications [^29].
- Given the performance increase for a relatively basic model such as the SOFNN we are hopeful to find equal or better improvements for more sophisticated market models that may in fact include other information derived from news sources, and a variety of relevant economic indicators. ==These results have implications for existing sentiment tracking tools as well as surveys of “self-reported subjective well-being” in which individuals evaluate the extent to which they experience positive and negative affect, happiness, or satisfaction with life== [^15].

## Contributions

- - p &lt; 0.1. ** p &lt; 0.05. *** p &lt; 0.001.

## Limitations

- The study notes that the accuracy of the methods used to assess public mood may be limited by the low degree to which the chosen indicators are expected to be correlated with public mood. The study also notes that the study is not interested in proposing an optimal DJIA prediction model, but to assess the effects of including public mood information on the accuracy of a “baseline” prediction model.
- The study is limited to a 2-month period and a specific set of sociocultural events, which may not be representative of all public mood and DJIA relationships. The study also relies on a specific set of mood measurements and DJIA values, which may not capture all aspects of public mood and stock market behavior.
- The study acknowledges several limitations, including the lack of geographical and cultural diversity in the Twitter user base, the absence of "ground truth" for public mood states, and the need for further research on the causative mechanisms connecting online public mood states with DJIA values.

## Future work

- The study suggests that future work could involve exploring the extraction of indicators of public mood state from online sources and relating them to economic indicators. The study also suggests that future work could involve proposing an optimal DJIA prediction model that incorporates public mood information.
- The study suggests that future research should examine the relationship between public mood and DJIA values over longer periods and using different mood measurements and DJIA values. The study also suggests that future research should explore the use of different machine learning models and techniques to improve predictive accuracy.
- The study suggests several areas for future research, including the examination of location and language factors, the investigation of direct assessments of public mood states, and the analysis of social and cognitive effects in online social networking environments.

## References

[^11]: M.J. Er, S. Wu, A fast learning algorithm for parsimonious fuzzy neural systems, Fuzzy Sets and Systems 126 (3) (2002) 337–351, <http://www.sciencedirect.com/science/article/B6V05-4550NT7->  [OA](http://www.sciencedirect.com/science/article/B6V05-4550NT7-)  [Scite](/scite_tallies?query=author%3AEr%2Ctitle%3AA%20fast%20learning%20algorithm%20for%20parsimonious%20fuzzy%20neural%20systems%2Cyear%3A2002)

[^15]: B.S. Frey, Happiness: A Revolution in Economics, MIT Press Books, The MIT Press, June 2008, <http://ideas.repec.org/b/mtp/titles/0262062771.html>.  [OA](http://ideas.repec.org/b/mtp/titles/0262062771.html)  

[^17]: E. Gilbert, K. Karahalios, Widespread worry and the stock market, in: Fourth International AAAI Conference on Weblogs and Social Media, Washington, DC, 2010, pp. 58–65, <http://www.aaai.org/ocs/index.php/ICWSM/> ICWSM10/paper/download/1513/1833.  [OA](http://www.aaai.org/ocs/index.php/ICWSM/ICWSM10/paper/download/1513/1833)  

[^22]: J.S.R. Jang, ANFIS: adaptive-network-based fuzzy inference system, IEEE Transactions on Systems, Man and Cybernetics 23 (August (3)) (2002) 665–685, <http://dx.doi.org/10.1109/21.256541>.  [OA](https://doi.org/10.1109/21.256541)  [Scite](/scite_tallies?query=https://doi.org/10.1109/21.256541)

[^28]: G. Leng, G. Prasad, T.M. McGinnity, An on-line algorithm for creating selforganizing fuzzy neural networks, Neural Networks: The Official Journal of the International Neural Network Society 17 (December (10)) (2004) 1477–1493, <http://www.ncbi.nlm.nih.gov/pubmed/15541949>.  [OA](http://www.ncbi.nlm.nih.gov/pubmed/15541949)  [Scite](/scite_tallies?query=author%3ALeng%2Ctitle%3AAn%20on-line%20algorithm%20for%20creating%20selforganizing%20fuzzy%20neural%20networks%2Cyear%3A2004)

[^29]: G. Leng, X.-J. Zeng, J.A. Keane, A hybrid learning algorithm with a similarity-based pruning strategy for self-adaptive neuro-fuzzy systems, Applied Soft Computing 9 (September (4)) (2009) 1354–1366, <http://portal.acm.org/citation.cfm?id=1595891.1596017>.  [OA](http://portal.acm.org/citation.cfm?id=1595891.1596017)  [Scite](/scite_tallies?query=author%3ALeng%2Ctitle%3AA%20hybrid%20learning%20algorithm%20with%20a%20similarity-based%20pruning%20strategy%20for%20self-adaptive%20neuro-fuzzy%20systems%2Cyear%3A2009)

[^32]: H. Mao, X.-J. Zeng, G. Leng, Y. Zhai, J.A. Keane, Short and mid-term load forecasting using a bilevel optimization model, IEEE Transactions On Power Systems 24 (2) (2009) 1080–1090.  [OA](https://engine.scholarcy.com/oa_version?query=Mao%2C%20H.%20Zeng%2C%20X.-J.%20Leng%2C%20G.%20Zhai%2C%20Y.%20Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%202009&author=Mao&title=Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Mao%2C%20H.%20Zeng%2C%20X.-J.%20Leng%2C%20G.%20Zhai%2C%20Y.%20Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%202009) [Scite](/scite_tallies?query=author%3AMao%2Ctitle%3AShort%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%2Cyear%3A2009)

[^43]: Qian, Bo, Rasheed, Khaled, Stock market prediction with multiple classifiers, Applied Intelligence 26 (February (1)) (2007) 25–33, <http://dx.doi.org/10.1007/s10489-006-0001-7>.  [OA](https://doi.org/10.1007/s10489-006-0001-7)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10489-006-0001-7)

[^49]: S. Wu, M.J. Er, Y. Gao, A fast approach for automatic generation of fuzzy rules by generalized dynamic fuzzy neural networks, IEEE Transactions on Fuzzy Systems 9 (4) (2001) 578–594, <http://ieeexplore.ieee.org/xpls/abs\all.jsp?arnumber=940970>.  [OA](http://ieeexplore.ieee.org/xpls/abs\all.jsp?arnumber=940970)  [Scite](/scite_tallies?query=author%3AWu%2Ctitle%3AA%20fast%20approach%20for%20automatic%20generation%20of%20fuzzy%20rules%20by%20generalized%20dynamic%20fuzzy%20neural%20networks%2Cyear%3A2001)
