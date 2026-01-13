[[Bollen_et+al_TwitterMoodPredictsStockMarket_2011]]

# [Twitter mood predicts the stock market](https://doi.org/10.1016/j.jocs.2010.12.007)

## [[Johan Bollen]]; [[Huina Mao]]; [[Xiao‐Jun Zeng]]

## Abstract
Behavioral economics tells us that emotions can profoundly affect individual behavior and decisionmaking. ==Does this also apply to societies at large, i.e. can societies experience mood states that affect their collective decision making? By extension is the public mood correlated or even predictive of economic indicators? Here we investigate whether measurements of collective mood states derived from largescale Twitter feeds are correlated to the value of the Dow Jones Industrial Average (DJIA) over time==. We analyze the text content of daily Twitter feeds by two mood tracking tools, namely OpinionFinder that measures positive vs. negative mood and Google-Profile of Mood States (GPOMS) that measures mood in terms of 6 dimensions (Calm, Alert, Sure, Vital, Kind, and Happy). We cross-validate the resulting mood time series by comparing their ability to detect the public’s response to the presidential election and Thanksgiving day in 2008. A Granger causality analysis and a Self-Organizing Fuzzy Neural Network are then used to investigate the hypothesis that public mood states, as measured by the OpinionFinder and GPOMS mood time series, are predictive of changes in DJIA closing values. ==Our results indicate that the accuracy of DJIA predictions can be significantly improved by the inclusion of specific public mood dimensions but not others==. ==We find an accuracy of 86.7% in predicting the daily up and down changes in the closing values of the DJIA and a reduction of the Mean Average Percentage Error (MAPE) by more than 6%==.

## Key concepts
#claim/stock_market_prediction; #stock_market_prediction; #finding/dow_jones_industrial_average; #dow_jones_industrial_average; #stock_market

## Quote
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
- Since news is unpredictable, <a class="keyword" href="https://en.wikipedia.org/wiki/Stock_market" title="stock market">stock market</a> prices will follow a random walk pattern and cannot be predicted with more than 50% accuracy [^43]
- The multiple linear regression results are provided in Table 1 (coefficient and p-values), and indicate that YOF is significantly correlated with X3 (Sure), X4 (Vital) and X6 (Happy), but not with X1 (Calm), X2 (Alert) and X5 (Kind)
- In fact the p-value for this shorter period, i.e. August 1, 2008 to October 30, 2008, is significantly lower (lag n−3, p = 0.009) than that listed in Table 2 for the period February 28, 2008 to November 3, 2008
- Compared to I0 and all other input combinations, adding input I1 leads to significant improvements in <a class="keyword" href="#" title="Mean Average Percentage Error">MAPE</a> values (1.83% vs. the maximum of 2.13% and 1.95% for IOF) and direction accuracy (86.7% compared to 73.3% for IOF and 46.7% for I1,3)
- It is notable that I1,6, i.e. a combination of X6 and X1 does significantly reduce average <a class="keyword" href="#" title="Mean Average Percentage Error">MAPE</a>, and provides good direction accuracy (80%)
- In combination with Calm, it produces a more accurate <a class="keyword" href="#" title="Self-organizing Fuzzy Neural Network">SOFNN</a> prediction (<a class="keyword" href="#" title="Mean Average Percentage Error">MAPE</a> = 1.79%) and direction accuracy (80%)
- To assess the statistical significance of the <a class="keyword" href="#" title="Self-organizing Fuzzy Neural Network">SOFNN</a> achieving the above mentioned accuracy of 87.6% in predicting the up and down movement of the <a class="keyword" href="https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average" title="Dow Jones Industrial Average">DJIA</a> we calculate the odds of this result occurring by chance

##  Builds on previous research
- However, Granger causality analysis is based on linear regression whereas the relation between public mood and stock market values is almost certainly non-linear. ==To better address these non-linear effects and assess the contribution that public mood assessments can make in predictive models of DJIA values, we compare the performance of a Self-organizing Fuzzy Neural Network== (SOFNN) model [^28] that predicts DJIA values on the basis of two sets of inputs: (1) the past 3 days of DJIA values, and (2) the same combined with various permutations of our mood time series (explained below).
- Compared with some notable fuzzy nerural network models, such as the adaptive-network-based fuzzy inference systems (ANFIS) [^22], self-organizing dynamic fuzzy neural network (DFNN) [^11] and GDFNN [^49], SOFNN provides a more efficient algorithm for online learning due to its simple and effective parameter and structure learning algorithm [^28]. In ==our previous work, SOFNN has proven its value in electrical load forecasting== [^32], exchange rate forecasting [^28] and other applications [^29].
- Given the performance increase for a relatively basic model such as the SOFNN we are hopeful to find equal or better improvements for more sophisticated market models that may in fact include other information derived from news sources, and a variety of relevant economic indicators. ==These results have implications for existing sentiment tracking tools as well as surveys of “self-reported subjective well-being” in which individuals evaluate the extent to which they experience positive and negative affect, happiness, or satisfaction with life== [^15].

## Contributions
- * p &lt; 0.1. ** p &lt; 0.05. *** p &lt; 0.001.

## Limitations
- The study notes that the accuracy of the methods used to assess public mood may be limited by the low degree to which the chosen indicators are expected to be correlated with public mood. The study also notes that the study is not interested in proposing an optimal DJIA prediction model, but to assess the effects of including public mood information on the accuracy of a “baseline” prediction model.
- The study is limited to a 2-month period and a specific set of sociocultural events, which may not be representative of all public mood and DJIA relationships. The study also relies on a specific set of mood measurements and DJIA values, which may not capture all aspects of public mood and stock market behavior.
- The study acknowledges several limitations, including the lack of geographical and cultural diversity in the Twitter user base, the absence of "ground truth" for public mood states, and the need for further research on the causative mechanisms connecting online public mood states with DJIA values.

## Future work
- The study suggests that future work could involve exploring the extraction of indicators of public mood state from online sources and relating them to economic indicators. The study also suggests that future work could involve proposing an optimal DJIA prediction model that incorporates public mood information.
- The study suggests that future research should examine the relationship between public mood and DJIA values over longer periods and using different mood measurements and DJIA values. The study also suggests that future research should explore the use of different machine learning models and techniques to improve predictive accuracy.
- The study suggests several areas for future research, including the examination of location and language factors, the investigation of direct assessments of public mood states, and the analysis of social and cognitive effects in online social networking environments.


## References
[^1]: S. Asur, B.A. Huberman, Predicting the Future with Social Media, 2010, http://www.arxiv.org arXiv:1003.5699v1.  [OA](http://www.arxiv.org)  

[^2]: S. Bergsma, L. Dekang, R. Goebel, Web-scale N-gram models for lexical disambiguation, in: Proceedings of the Twenty-first International Joint Conference on Artificial Intelligence (IJCAI-09), Pasadena, CA, 2009, pp. 1507–1512.  [OA](https://scholar.google.co.uk/scholar?q=Bergsma%2C%20S.%20Dekang%2C%20L.%20Goebel%2C%20R.%20Web-scale%20N-gram%20models%20for%20lexical%20disambiguation%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Bergsma%2C%20S.%20Dekang%2C%20L.%20Goebel%2C%20R.%20Web-scale%20N-gram%20models%20for%20lexical%20disambiguation%202009) 

[^3]: T. Brants, A. Franz, Web 1T 5-gram Version 1, Tech. rep., Linguistic Data Consortium, Philadelphia, 2006.  [OA](https://engine.scholarcy.com/oa_version?query=Brants%2C%20T.%20Franz%2C%20A.%20Web%201T%205-gram%20Version%201%202006&author=Brants&title=Web%201T%205-gram%20Version%201&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Brants%2C%20T.%20Franz%2C%20A.%20Web%201T%205-gram%20Version%201%202006) [Scite](/scite_tallies?query=author%3ABrants%2Ctitle%3AWeb%201T%205-gram%20Version%201%2Cyear%3A2006)

[^4]: K.C. Butler, S.J. Malaikah, Efficiency and inefficiency in thinly traded stock markets: Kuwait and Saudi Arabia, Journal of Banking &amp; Finance 16 (1) (1992) 197–210, http://www.econpapers.repec.org/RePEc:eee:jbfina:v:16:y:1992:i:1:p:197-210.  [OA](http://www.econpapers.repec.org/RePEc:eee:jbfina:v:16:y:1992:i:1:p:197-210)  [Scite](/scite_tallies?query=author%3AButler%2Ctitle%3AEfficiency%20and%20inefficiency%20in%20thinly%20traded%20stock%20markets%3A%20Kuwait%20and%20Saudi%20Arabia%2Cyear%3A1992)

[^5]: G.A. Carpenter, S. Grossberg, The ART of adaptive pattern recognition by a self-organizing neural network, Computer 21 (March (3)) (1988) 77–88, http://portal.acm.org/citation.cfm?id=47861.47867.  [OA](http://portal.acm.org/citation.cfm?id=47861.47867)  [Scite](/scite_tallies?query=author%3ACarpenter%2Ctitle%3AThe%20ART%20of%20adaptive%20pattern%20recognition%20by%20a%20self-organizing%20neural%20network%2Cyear%3A1988)

[^6]: H. Choi, H. Varian, Predicting the Present with Google Trends, Tech. rep., Google, 2009.  [OA](https://engine.scholarcy.com/oa_version?query=Choi%2C%20H.%20Varian%2C%20H.%20Predicting%20the%20Present%20with%20Google%20Trends%202009&author=Choi&title=Predicting%20the%20Present%20with%20Google%20Trends&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Choi%2C%20H.%20Varian%2C%20H.%20Predicting%20the%20Present%20with%20Google%20Trends%202009) [Scite](/scite_tallies?query=author%3AChoi%2Ctitle%3APredicting%20the%20Present%20with%20Google%20Trends%2Cyear%3A2009)

[^7]: A.R. Damasio, Descartes’ Error: Emotion Reason, and the Human Brain, Putnam, 1994.  [OA](https://scholar.google.co.uk/scholar?q=Damasio%2C%20A.R.%20Descartes%E2%80%99%20Error%3A%20Emotion%20Reason%2C%20and%20the%20Human%20Brain%201994) [GScholar](https://scholar.google.co.uk/scholar?q=Damasio%2C%20A.R.%20Descartes%E2%80%99%20Error%3A%20Emotion%20Reason%2C%20and%20the%20Human%20Brain%201994) 

[^8]: P.S. Dodds, C.M. Danforth, Measuring the happiness of large-scale written expression: songs, blogs, and presidents, Journal of Happiness (July) (2009).  [OA](https://engine.scholarcy.com/oa_version?query=Dodds%2C%20P.S.%20Danforth%2C%20C.M.%20Measuring%20the%20happiness%20of%20large-scale%20written%20expression%3A%20songs%2C%20blogs%2C%20and%20presidents%20July&author=Dodds&title=Measuring%20the%20happiness%20of%20large-scale%20written%20expression%3A%20songs%2C%20blogs%2C%20and%20presidents&year=July) [GScholar](https://scholar.google.co.uk/scholar?q=Dodds%2C%20P.S.%20Danforth%2C%20C.M.%20Measuring%20the%20happiness%20of%20large-scale%20written%20expression%3A%20songs%2C%20blogs%2C%20and%20presidents%20July) [Scite](/scite_tallies?query=author%3ADodds%2Ctitle%3AMeasuring%20the%20happiness%20of%20large-scale%20written%20expression%3A%20songs%2C%20blogs%2C%20and%20presidents%2Cyear%3AJuly)

[^9]: R.J. Dolan, Emotion cognition, and behavior, Science 298 (5596) (2002) 1191–1194, http://www.sciencemag.org/cgi/content/abstract/298/5596/  [OA](http://www.sciencemag.org/cgi/content/abstract/298/5596/)  [Scite](/scite_tallies?query=author%3ADolan%2Ctitle%3AEmotion%20cognition%2C%20and%20behavior%2Cyear%3A2002)

[^10]: A. Edmans, D. García, O.Y. Norli, Sports sentiment and stock returns, Journal of Finance 62 (4) (2007) 1967–1998, http://econpapers.repec.org/  [OA](http://econpapers.repec.org/)  [Scite](/scite_tallies?query=author%3AEdmans%2Ctitle%3ASports%20sentiment%20and%20stock%20returns%2Cyear%3A2007)

[^11]: M.J. Er, S. Wu, A fast learning algorithm for parsimonious fuzzy neural systems, Fuzzy Sets and Systems 126 (3) (2002) 337–351, http://www.sciencedirect.com/science/article/B6V05-4550NT7-  [OA](http://www.sciencedirect.com/science/article/B6V05-4550NT7-)  [Scite](/scite_tallies?query=author%3AEr%2Ctitle%3AA%20fast%20learning%20algorithm%20for%20parsimonious%20fuzzy%20neural%20systems%2Cyear%3A2002)

[^12]: E.F. Fama, The behavior of stock-market prices, The Journal of Business 38 (1) (1965) 34–105, http://dx.doi.org/10.2307/2350752.  [OA](https://doi.org/10.2307/2350752)  [Scite](/scite_tallies?query=https://doi.org/10.2307/2350752)

[^13]: E.F. Fama, Efficient capital markets: II, Journal of Finance 46 (5) (1991) 1575–1617, http://econpapers.repec.org/RePEc:bla:jfinan:v:46:y:1991:i:5:p:1575-617.  [OA](http://econpapers.repec.org/RePEc:bla:jfinan:v:46:y:1991:i:5:p:1575-617)  [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3AEfficient%20capital%20markets%3A%20II%2Cyear%3A1991)

[^14]: E.F. Fama, L. Fischer, M.C. Jensen, R. Roll, The adjustment of stock prices to new information, International Economic Review 10 (February (1)) (1969) 1–21, http://ideas.repec.org/a/ier/iecrev/v10y1969i1p1-21.html.  [OA](http://ideas.repec.org/a/ier/iecrev/v10y1969i1p1-21.html)  [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3AThe%20adjustment%20of%20stock%20prices%20to%20new%20information%2Cyear%3A1969)

[^15]: B.S. Frey, Happiness: A Revolution in Economics, MIT Press Books, The MIT Press, June 2008, http://ideas.repec.org/b/mtp/titles/0262062771.html.  [OA](http://ideas.repec.org/b/mtp/titles/0262062771.html)  

[^16]: L.A. Gallagher, M.P. Taylor, Permanent and temporary components of stock prices: evidence from assessing macroeconomic shocks, Southern Economic Journal 69 (2) (2002) 345–362, http://www.jstor.org/stable/1061676.  [OA](http://www.jstor.org/stable/1061676)  [Scite](/scite_tallies?query=author%3AGallagher%2Ctitle%3APermanent%20and%20temporary%20components%20of%20stock%20prices%3A%20evidence%20from%20assessing%20macroeconomic%20shocks%2Cyear%3A2002)

[^17]: E. Gilbert, K. Karahalios, Widespread worry and the stock market, in: Fourth International AAAI Conference on Weblogs and Social Media, Washington, DC, 2010, pp. 58–65, http://www.aaai.org/ocs/index.php/ICWSM/ ICWSM10/paper/download/1513/1833.  [OA](http://www.aaai.org/ocs/index.php/ICWSM/ICWSM10/paper/download/1513/1833)  

[^18]: D. Gruhl, R. Guha, R. Kumar, J. Novak, A. Tomkins, The predictive power of online chatter, in: KDD ‘05: Proceeding of the Eleventh ACM SIGKDD International Conference on Knowledge Discovery in Data Mining, ACM Press, New York, NY, 2005, pp. 78–87.  [OA](https://scholar.google.co.uk/scholar?q=Gruhl%2C%20D.%20Guha%2C%20R.%20Kumar%2C%20R.%20Novak%2C%20J.%20The%20predictive%20power%20of%20online%20chatter%2C%20in%3A%20KDD%20%E2%80%9805%202005) [GScholar](https://scholar.google.co.uk/scholar?q=Gruhl%2C%20D.%20Guha%2C%20R.%20Kumar%2C%20R.%20Novak%2C%20J.%20The%20predictive%20power%20of%20online%20chatter%2C%20in%3A%20KDD%20%E2%80%9805%202005) 

[^19]: H. Cootner P, The Random Character of Stock Market Prices, MIT, 1964.  [OA](https://scholar.google.co.uk/scholar?q=P%2C%20H.Cootner%20The%20Random%20Character%20of%20Stock%20Market%20Prices%201964) [GScholar](https://scholar.google.co.uk/scholar?q=P%2C%20H.Cootner%20The%20Random%20Character%20of%20Stock%20Market%20Prices%201964) 

[^20]: D. Hirshleifer, T. Shumway, Good day sunshine: stock returns and the weather, Journal of Finance 58 (3) (2003) 1009–1032, http://ideas.repec.org/a/bla/jfinan/v58y2003i3p1009-1032.html.  [OA](http://ideas.repec.org/a/bla/jfinan/v58y2003i3p1009-1032.html)  [Scite](/scite_tallies?query=author%3AHirshleifer%2Ctitle%3AGood%20day%20sunshine%3A%20stock%20returns%20and%20the%20weather%2Cyear%3A2003)

[^21]: J.J. Hopfield, Neurons with graded response have collective computational properties like those of two-state neurons, Proceedings of the National Academy of Sciences of the United States of America 81 (May (10)) (1984) 3088–3092, http://www.pnas.org/content/81/10/3088.abstract.  [OA](http://www.pnas.org/content/81/10/3088.abstract)  [Scite](/scite_tallies?query=author%3AHopfield%2Ctitle%3ANeurons%20with%20graded%20response%20have%20collective%20computational%20properties%20like%20those%20of%20two-state%20neurons%2Cyear%3A1984)

[^22]: J.S.R. Jang, ANFIS: adaptive-network-based fuzzy inference system, IEEE Transactions on Systems, Man and Cybernetics 23 (August (3)) (2002) 665–685, http://dx.doi.org/10.1109/21.256541.  [OA](https://doi.org/10.1109/21.256541)  [Scite](/scite_tallies?query=https://doi.org/10.1109/21.256541)

[^23]: D. Kahneman, A. Tversky, Prospect theory: an analysis of decision under risk, Econometrica 47 (2) (1979) 263–291.  [OA](https://engine.scholarcy.com/oa_version?query=Kahneman%2C%20D.%20Tversky%2C%20A.%20Prospect%20theory%3A%20an%20analysis%20of%20decision%20under%20risk%201979&author=Kahneman&title=Prospect%20theory%3A%20an%20analysis%20of%20decision%20under%20risk&year=1979) [GScholar](https://scholar.google.co.uk/scholar?q=Kahneman%2C%20D.%20Tversky%2C%20A.%20Prospect%20theory%3A%20an%20analysis%20of%20decision%20under%20risk%201979) [Scite](/scite_tallies?query=author%3AKahneman%2Ctitle%3AProspect%20theory%3A%20an%20analysis%20of%20decision%20under%20risk%2Cyear%3A1979)

[^24]: M. Kavussanos, E. Dockery, A multivariate test for stock market efficiency: the case of ASE, Applied Financial Economics 11 (5) (2001) 573–579, http://econpapers.repec.org/RePEc:taf:apfiec:v:11:y:2001:i:5:p:573-79.  [OA](http://econpapers.repec.org/RePEc:taf:apfiec:v:11:y:2001:i:5:p:573-79)  [Scite](/scite_tallies?query=author%3AKavussanos%2Ctitle%3AA%20multivariate%20test%20for%20stock%20market%20efficiency%3A%20the%20case%20of%20ASE%2Cyear%3A2001)

[^25]: T. Kimoto, K. Asakawa, M. Yoda, M. Takeoka, Stock market prediction system with modular neural networks, in: Proceedings of the International Joint Conference on Neural Networks, IEEE, San Diego, CA, 1990, pp. 1–6.  [OA](https://scholar.google.co.uk/scholar?q=Kimoto%2C%20T.%20Asakawa%2C%20K.%20Yoda%2C%20M.%20Takeoka%2C%20M.%20Stock%20market%20prediction%20system%20with%20modular%20neural%20networks%201990) [GScholar](https://scholar.google.co.uk/scholar?q=Kimoto%2C%20T.%20Asakawa%2C%20K.%20Yoda%2C%20M.%20Takeoka%2C%20M.%20Stock%20market%20prediction%20system%20with%20modular%20neural%20networks%201990) 

[^26]: A. Lapedes, R. Farber, Nonlinear signal processing using neural networks: prediction and system modelling, in: IEEE International Conference on Neural Networks, IEEE, San Diego, CA, 1987.  [OA](https://scholar.google.co.uk/scholar?q=Lapedes%2C%20A.%20Farber%2C%20R.%20Nonlinear%20signal%20processing%20using%20neural%20networks%3A%20prediction%20and%20system%20modelling%201987) [GScholar](https://scholar.google.co.uk/scholar?q=Lapedes%2C%20A.%20Farber%2C%20R.%20Nonlinear%20signal%20processing%20using%20neural%20networks%3A%20prediction%20and%20system%20modelling%201987) 

[^27]: D. Lazer, D. Brewer, N. Christakis, J. Fowler, G. King, Life in the network: the coming age of computational social science, Science 323 (5915) (2009) 721–723.  [OA](https://engine.scholarcy.com/oa_version?query=Lazer%2C%20D.%20Brewer%2C%20D.%20Christakis%2C%20N.%20Fowler%2C%20J.%20Life%20in%20the%20network%3A%20the%20coming%20age%20of%20computational%20social%20science%202009&author=Lazer&title=Life%20in%20the%20network%3A%20the%20coming%20age%20of%20computational%20social%20science&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Lazer%2C%20D.%20Brewer%2C%20D.%20Christakis%2C%20N.%20Fowler%2C%20J.%20Life%20in%20the%20network%3A%20the%20coming%20age%20of%20computational%20social%20science%202009) [Scite](/scite_tallies?query=author%3ALazer%2Ctitle%3ALife%20in%20the%20network%3A%20the%20coming%20age%20of%20computational%20social%20science%2Cyear%3A2009)

[^28]: G. Leng, G. Prasad, T.M. McGinnity, An on-line algorithm for creating selforganizing fuzzy neural networks, Neural Networks: The Official Journal of the International Neural Network Society 17 (December (10)) (2004) 1477–1493, http://www.ncbi.nlm.nih.gov/pubmed/15541949.  [OA](http://www.ncbi.nlm.nih.gov/pubmed/15541949)  [Scite](/scite_tallies?query=author%3ALeng%2Ctitle%3AAn%20on-line%20algorithm%20for%20creating%20selforganizing%20fuzzy%20neural%20networks%2Cyear%3A2004)

[^29]: G. Leng, X.-J. Zeng, J.A. Keane, A hybrid learning algorithm with a similarity-based pruning strategy for self-adaptive neuro-fuzzy systems, Applied Soft Computing 9 (September (4)) (2009) 1354–1366, http://portal.acm.org/citation.cfm?id=1595891.1596017.  [OA](http://portal.acm.org/citation.cfm?id=1595891.1596017)  [Scite](/scite_tallies?query=author%3ALeng%2Ctitle%3AA%20hybrid%20learning%20algorithm%20with%20a%20similarity-based%20pruning%20strategy%20for%20self-adaptive%20neuro-fuzzy%20systems%2Cyear%3A2009)

[^30]: Y. Liu, X. Huang, A. An, X. Yu, ARSA: a sentiment-aware model for predicting sales performance using blogs, in: SIGIR ‘07: Proceedings of the 30th Annual International ACM SIGIR Conference on Research and Development in Information Retrieval, ACM, New York, NY, 2007, pp. 607–614.  [OA](https://scholar.google.co.uk/scholar?q=Liu%2C%20Y.%20Huang%2C%20X.%20An%2C%20A.%20Yu%2C%20X.%20ARSA%3A%20a%20sentiment-aware%20model%20for%20predicting%20sales%20performance%20using%20blogs%2C%20in%3A%20SIGIR%20%E2%80%9807%202007) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Y.%20Huang%2C%20X.%20An%2C%20A.%20Yu%2C%20X.%20ARSA%3A%20a%20sentiment-aware%20model%20for%20predicting%20sales%20performance%20using%20blogs%2C%20in%3A%20SIGIR%20%E2%80%9807%202007) 

[^31]: B.G. Malkiel, The efficient market hypothesis and its critics, The Journal of Economic Perspectives 17 (1) (2003), http://dx.doi.org/10.2307/3216840.  [OA](https://doi.org/10.2307/3216840)  [Scite](/scite_tallies?query=https://doi.org/10.2307/3216840)

[^32]: H. Mao, X.-J. Zeng, G. Leng, Y. Zhai, J.A. Keane, Short and mid-term load forecasting using a bilevel optimization model, IEEE Transactions On Power Systems 24 (2) (2009) 1080–1090.  [OA](https://engine.scholarcy.com/oa_version?query=Mao%2C%20H.%20Zeng%2C%20X.-J.%20Leng%2C%20G.%20Zhai%2C%20Y.%20Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%202009&author=Mao&title=Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model&year=2009) [GScholar](https://scholar.google.co.uk/scholar?q=Mao%2C%20H.%20Zeng%2C%20X.-J.%20Leng%2C%20G.%20Zhai%2C%20Y.%20Short%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%202009) [Scite](/scite_tallies?query=author%3AMao%2Ctitle%3AShort%20and%20mid-term%20load%20forecasting%20using%20a%20bilevel%20optimization%20model%2Cyear%3A2009)

[^33]: D.M. McNair, J.W.P. Heuchert, E. Shilony, Profile of Mood States. Bibliography 1964–2002, Multi-Health Systems, 2003, https://www.mhs.com/ecom/ TechBrochures/POMSBibliography.pdf.  [OA](https://www.mhs.com/ecom/TechBrochures/POMSBibliography.pdf)  

[^34]: G. Mishne, M.D. Rijke, Capturing global mood levels using blog posts, in: N. Nicolov, F. Salvetti, M. Liberman, J.H. Martin (Eds.), AAAI 2006 Spring Symposium on Computational Approaches to Analysing Weblogs, The AAAI Press, Menlo Park, CA/Stanford University, CA, August, 2006, pp. 145–152.  [OA](https://scholar.google.co.uk/scholar?q=Mishne%2C%20G.%20Rijke%2C%20M.D.%20Capturing%20global%20mood%20levels%20using%20blog%20posts%202006-08) [GScholar](https://scholar.google.co.uk/scholar?q=Mishne%2C%20G.%20Rijke%2C%20M.D.%20Capturing%20global%20mood%20levels%20using%20blog%20posts%202006-08) 

[^35]: A. Nigrin, Neural Networks for Pattern Recognition, MIT Press, Cambridge, MA, 1993.  [OA](https://scholar.google.co.uk/scholar?q=Nigrin%2C%20A.%20Neural%20Networks%20for%20Pattern%20Recognition%201993) [GScholar](https://scholar.google.co.uk/scholar?q=Nigrin%2C%20A.%20Neural%20Networks%20for%20Pattern%20Recognition%201993) 

[^36]: J.R. Nofsinger, Social mood and financial economics, Journal of Behaviour Finance 6 (3) (2005) 144–160.  [OA](https://engine.scholarcy.com/oa_version?query=Nofsinger%2C%20J.R.%20Social%20mood%20and%20financial%20economics%202005&author=Nofsinger&title=Social%20mood%20and%20financial%20economics&year=2005) [GScholar](https://scholar.google.co.uk/scholar?q=Nofsinger%2C%20J.R.%20Social%20mood%20and%20financial%20economics%202005) [Scite](/scite_tallies?query=author%3ANofsinger%2Ctitle%3ASocial%20mood%20and%20financial%20economics%2Cyear%3A2005)

[^37]: J.C. Norcross, E. Guadagnoli, J.O. Prochaska, Factor structure of the profile of mood states (POMS): two partial replications, Journal of Clinical Psychology 40 (5) (2006) 1270–1277.  [OA](https://engine.scholarcy.com/oa_version?query=Norcross%2C%20J.C.%20Guadagnoli%2C%20E.%20Prochaska%2C%20J.O.%20Factor%20structure%20of%20the%20profile%20of%20mood%20states%20%28POMS%29%3A%20two%20partial%20replications%202006&author=Norcross&title=Factor%20structure%20of%20the%20profile%20of%20mood%20states%20%28POMS%29%3A%20two%20partial%20replications&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Norcross%2C%20J.C.%20Guadagnoli%2C%20E.%20Prochaska%2C%20J.O.%20Factor%20structure%20of%20the%20profile%20of%20mood%20states%20%28POMS%29%3A%20two%20partial%20replications%202006) [Scite](/scite_tallies?query=author%3ANorcross%2Ctitle%3AFactor%20structure%20of%20the%20profile%20of%20mood%20states%20%28POMS%29%3A%20two%20partial%20replications%2Cyear%3A2006)

[^38]: B. O’Connor, R. Balasubramanyan, B.R. Routledge, N.A. Smith, From tweets to polls: linking text sentiment to public opinion time series, in: Proceedings of the International AAAI Conference on Weblogs and Social Media, Washington, DC, May, 2010, http://www.aaai.org/ocs/index.php/ ICWSM/ICWSM10/paper/view/1536.  [OA](http://www.aaai.org/ocs/index.php/ICWSM/ICWSM10/paper/view/1536)  

[^39]: A. Pak, P. Paroubek, Twitter as a corpus for sentiment analysis and opinion mining, in: N. Calzolari, K. Choukri, B. Maegaard, J. Mariani, J. Odijk, S. Piperidis, M. Rosner, D. Tapias (Eds.), Proceedings of the Seventh conference on International Language Resources and Evaluation (LREC’10), European Language Resources Association (ELRA), Valletta, Malta, May 2010, pp. 19–21.  [OA](https://scholar.google.co.uk/scholar?q=Pak%2C%20A.%20Paroubek%2C%20P.%20Twitter%20as%20a%20corpus%20for%20sentiment%20analysis%20and%20opinion%20mining%202010-05) [GScholar](https://scholar.google.co.uk/scholar?q=Pak%2C%20A.%20Paroubek%2C%20P.%20Twitter%20as%20a%20corpus%20for%20sentiment%20analysis%20and%20opinion%20mining%202010-05) 

[^40]: B. Pang, L. Lee, Opinion mining and sentiment analysis, Foundations and Trends in Information Retrieval 2 (1–2) (2008) 1–135.  [OA](https://engine.scholarcy.com/oa_version?query=Pang%2C%20B.%20Lee%2C%20L.%20Opinion%20mining%20and%20sentiment%20analysis%202008&author=Pang&title=Opinion%20mining%20and%20sentiment%20analysis&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Pang%2C%20B.%20Lee%2C%20L.%20Opinion%20mining%20and%20sentiment%20analysis%202008) [Scite](/scite_tallies?query=author%3APang%2Ctitle%3AOpinion%20mining%20and%20sentiment%20analysis%2Cyear%3A2008)

[^41]: R.R. Prechter, W.D. Parker, The financial/economic dichotomy in social behavioral dynamics: the socionomic perspective, Journal of Behavioral Finance 8 (2) (2007) 84–108, http://dx.doi.org/10.1080/15427560701381028.  [OA](https://doi.org/10.1080/15427560701381028)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560701381028)

[^42]: R.J. Prechter Robert, The wave principle of human social behavior and the new science of socionomics, New Classics Library, GA, 2002.  [OA](https://scholar.google.co.uk/scholar?q=Robert%2C%20R.J.Prechter%20The%20wave%20principle%20of%20human%20social%20behavior%20and%20the%20new%20science%20of%20socionomics%202002) [GScholar](https://scholar.google.co.uk/scholar?q=Robert%2C%20R.J.Prechter%20The%20wave%20principle%20of%20human%20social%20behavior%20and%20the%20new%20science%20of%20socionomics%202002) 

[^43]: Qian, Bo, Rasheed, Khaled, Stock market prediction with multiple classifiers, Applied Intelligence 26 (February (1)) (2007) 25–33, http://dx.doi.org/10.1007/s10489-006-0001-7.  [OA](https://doi.org/10.1007/s10489-006-0001-7)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10489-006-0001-7)

[^44]: E. Riloff, J. Wiebe, Learning extraction patterns for subjective expressions, in: Proceedings of the 2003 Conference on Empirical Methods in Natural Language Processing, Association for Computational Linguistics, Morristown, NJ, 2003, pp. 105–112.  [OA](https://scholar.google.co.uk/scholar?q=Riloff%2C%20E.%20Wiebe%2C%20J.%20Learning%20extraction%20patterns%20for%20subjective%20expressions%202003) [GScholar](https://scholar.google.co.uk/scholar?q=Riloff%2C%20E.%20Wiebe%2C%20J.%20Learning%20extraction%20patterns%20for%20subjective%20expressions%202003) 

[^45]: E. Riloff, J. Wiebe, T. Wilson, Learning subjective nouns using extraction pattern bootstrapping, in: Proceedings of the Seventh Conference on Natural Language Learning at HLT-NAACL 2003, Association for Computational Linguistics, Morristown, NJ, 2003, pp. 25–32.  [OA](https://scholar.google.co.uk/scholar?q=E%20Riloff%20J%20Wiebe%20T%20Wilson%20Learning%20subjective%20nouns%20using%20extraction%20pattern%20bootstrapping%20in%20Proceedings%20of%20the%20Seventh%20Conference%20on%20Natural%20Language%20Learning%20at%20HLTNAACL%202003%20Association%20for%20Computational%20Linguistics%20Morristown%20NJ%202003%20pp%202532) [GScholar](https://scholar.google.co.uk/scholar?q=E%20Riloff%20J%20Wiebe%20T%20Wilson%20Learning%20subjective%20nouns%20using%20extraction%20pattern%20bootstrapping%20in%20Proceedings%20of%20the%20Seventh%20Conference%20on%20Natural%20Language%20Learning%20at%20HLTNAACL%202003%20Association%20for%20Computational%20Linguistics%20Morristown%20NJ%202003%20pp%202532) 

[^46]: R.P. Schumaker, H. Chen, Textual analysis of stock market prediction using breaking financial news, ACM Transactions on Information Systems 27 (February (2)) (2009) 1–19, http://portal.acm.org/citation.cfm?doid=1462198.1462204.  [OA](http://portal.acm.org/citation.cfm?doid=1462198.1462204)  [Scite](/scite_tallies?query=author%3ASchumaker%2Ctitle%3ATextual%20analysis%20of%20stock%20market%20prediction%20using%20breaking%20financial%20news%2Cyear%3A2009)

[^47]: V.L. Smith, Constructivist and ecological rationality in economics, American Economic Review 93 (2003) 465–508.  [OA](https://engine.scholarcy.com/oa_version?query=Smith%2C%20V.L.%20Constructivist%20and%20ecological%20rationality%20in%20economics%202003&author=Smith&title=Constructivist%20and%20ecological%20rationality%20in%20economics&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Smith%2C%20V.L.%20Constructivist%20and%20ecological%20rationality%20in%20economics%202003) [Scite](/scite_tallies?query=author%3ASmith%2Ctitle%3AConstructivist%20and%20ecological%20rationality%20in%20economics%2Cyear%3A2003)

[^48]: T. Wilson, J. Wiebe, P. Hofimann, Recognizing contextual polarity in phrase-level sentiment analysis, in: Proceedings of the Conference on Human Language Technology and Empirical Methods in Natural Language Processing—HLT ‘05 (October), 2005, pp. 347–354, http://portal.acm.org/citation.cfm?doid=1220575.1220619.  [OA](http://portal.acm.org/citation.cfm?doid=1220575.1220619)  

[^49]: S. Wu, M.J. Er, Y. Gao, A fast approach for automatic generation of fuzzy rules by generalized dynamic fuzzy neural networks, IEEE Transactions on Fuzzy Systems 9 (4) (2001) 578–594, http://ieeexplore.ieee.org/xpls/abs\all.jsp?arnumber=940970.  [OA](http://ieeexplore.ieee.org/xpls/abs\all.jsp?arnumber=940970)  [Scite](/scite_tallies?query=author%3AWu%2Ctitle%3AA%20fast%20approach%20for%20automatic%20generation%20of%20fuzzy%20rules%20by%20generalized%20dynamic%20fuzzy%20neural%20networks%2Cyear%3A2001)

[^50]: X. Zhang, H. Fuehres, P.A. Gloor, Predicting Stock Market Indicators Through Twitter I Hope It is Not as Bad as I Fear, Collaborative Innovation Networks (COINs), Savannah, GA, 2010, http:\\www.elsevier com/locate/procedia.  [OA](http://www.elsevier)  

[^51]: X. Zhu, H. Wang, L. Xu, H. Li, Predicting stock index increments by neural networks: the role of trading volume under different horizons, Expert Systems with Applications 34 (4) (2008) 3043–3054. Huina Mao is a Ph.D. student at the Indiana University School of Informatics and Computing since 2008. Her research focus is on electrical load forecasting and web mining. She has published on topics in fuzzy logic, expert systems, and utility load-forecasting. She is presently working on public sentiment tracking from large-scale online, social networking environments with the objective of modeling and predicting socio-economic indicators.  [OA](https://engine.scholarcy.com/oa_version?query=Zhu%2C%20X.%20Wang%2C%20H.%20Xu%2C%20L.%20Li%2C%20H.%20Predicting%20stock%20index%20increments%20by%20neural%20networks%3A%20the%20role%20of%20trading%20volume%20under%20different%20horizons%202008&author=Zhu&title=Predicting%20stock%20index%20increments%20by%20neural%20networks%3A%20the%20role%20of%20trading%20volume%20under%20different%20horizons&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Zhu%2C%20X.%20Wang%2C%20H.%20Xu%2C%20L.%20Li%2C%20H.%20Predicting%20stock%20index%20increments%20by%20neural%20networks%3A%20the%20role%20of%20trading%20volume%20under%20different%20horizons%202008) [Scite](/scite_tallies?query=author%3AZhu%2Ctitle%3APredicting%20stock%20index%20increments%20by%20neural%20networks%3A%20the%20role%20of%20trading%20volume%20under%20different%20horizons%2Cyear%3A2008)

