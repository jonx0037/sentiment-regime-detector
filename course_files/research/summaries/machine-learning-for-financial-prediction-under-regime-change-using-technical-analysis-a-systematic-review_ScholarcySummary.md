[[Suárez‐Cetrulo_et+al_MachineLearningFinancialPredictionUnder_2023]]

# [Machine Learning for Financial Prediction Under Regime Change Using Technical Analysis: A Systematic Review.](https://doi.org/10.9781/ijimai.2023.06.003)

## [[Andrés L. Suárez‐Cetrulo]]; [[David Quintana]]; [[Alejandro Cervantes]]

## Abstract

Recent crises, recessions, and bubbles have highlighted the non-stationarity and the presence of drastic structural changes in the financial domain. The most recent literature suggests the use of conventional machine learning and statistical approaches in this context. Unfortunately, several of these techniques are unable or slow to adapt to changes in the price-generation process. This study aims to survey the relevant literature on Machine Learning for financial prediction under regime change employing a systematic approach. It reviews key papers with a special emphasis on technical analysis. The study discusses the growing number of contributions that are bridging the gap between two separate communities, one focused on data stream learning and the other on economic research. However, it also makes apparent that we are still in an early stage. The range of machine learning algorithms tested in this domain is very wide, but the study's results do not suggest that any specific technique is currently clearly dominant.

## Key concepts

# finance; #expectation_maximisation; #financial_market; #regime_change; #concept_drift; #claim/machine_learning; #machine_learning; #deep_learning

## Quote
>
> The study reviews 140 relevant research works on regime changes and machine learning forecasting in the financial domain, focusing on non-stationary data and complex dynamics, and provides an overview of the literature on price forecasting under structural breaks.

## Key points

- Financial markets can be described as an evolutionary and nonlinear dynamical complex system [^1], [^2]
- This study aims to survey the relevant literature on Machine Learning for financial prediction under regime change, employing a systematic approach
- Among the key difficulties identified in the literature on financial prediction, we can mention structural change
- Some of these changes can recur over time as seasonal patterns, while others do not repeat, being abrupt breaks in the non-stationary price dynamics
- This study presented a systematic literature review of machine learning techniques for financial prediction under regime changes
- These results show that most of the reviewed papers use techniques from four main categories: Evolving systems, Ensemble-based systems, traditional systems adapted to concept change
- Out of a total of 140 relevant studies, these are distributed as follows: i) concept drift or online learning related (32.1%); ii) related to financial literacy for regime changes (15.7%), and iii) machine learning (ML) techniques applied to stock forecasting (52.1%)

## Summary

### Introduction

Financial markets are complex systems with a non-stationary nature and drastic structural changes.
Recent crises and recessions have highlighted the need for adaptive machine learning techniques to predict financial trends under regime change.
The study aims to survey the literature on machine learning for financial prediction under regime change, with a focus on technical analysis.

### Machine Learning

Machine learning algorithms have been successful in mapping nonlinear relationships in financial data.
Deep learning algorithms and ensembles have obtained the best results for stock trend prediction.
However, the literature on machine learning for financial prediction under regime change is limited.
Online incremental ML algorithms seem particularly well-suited to handling non-stationarities, shifts, and drifts in price-generating processes.
Machine learning (ML) techniques, including regime-switching models, have been applied to financial prediction under regime changes.
These techniques can detect changes in market regimes and predict future values.
Deep learning (DL) approaches, such as recurrent neural networks (RNNs), have also been used to address concept changes in financial data.
Online incremental algorithms, including clustering and forecasting algorithms, have been used to adapt to different cycles or seasonal behaviors in data streams.

### Regime Change

Regime change refers to a change in the collective behavior of market participants and their reactions.
Estimating the hidden processes driving the market into different regimes is often done using regime-switching models.
Detecting concept shifts helps lower the risks of financial exposure in high-frequency trading.
The study aims to identify directions for leveraging the benefits of modern algorithms that work across different scenarios and handle any changes that may arise in real time.

### Literature Review

The study reviewed 223 research works, classifying them into relevant, process assessment, and excluded works.
The relevant works were further filtered based on their relevance to regime changes or structural breaks in non-stationary data, and to machine learning forecasting in the financial field.
A total of 140 publications were classified as relevant, with the majority focusing on machine learning techniques for stock forecasting.

### Research Classification

The relevant studies were classified into two major areas: financial regime changes and data stream learning.
The financial regime change area focuses on statistical approaches to detect change points or forecast under different regimes, while the data stream learning area addresses the problem of concept drift.
The study found that the literature on online learning does not align with the literature on regime changes, but both areas address similar challenges, such as maintaining up-to-date models and retraining mechanisms.

### Machine Learning Techniques

The study extracted data from the relevant publications, including the machine learning techniques used.
The techniques were grouped into eight broad categories, with the majority of the reviewed papers using techniques from four main categories: evolving systems, ensemble-based systems, traditional systems adapted to concept change, and neural networks and deep learning.
The study found that machine learning algorithms can handle nonlinear relationships without prior knowledge, outperforming traditional time series methods, and can be used to predict price changes based on the time horizon and market efficiency.

### Market Changes

Financial markets are non-stationary and subject to regime changes or structural breaks, which can be abrupt and may or may not be transitory.
These changes can significantly affect financial exposure, and their timely recognition is crucial.
The adaptive market hypothesis (AMH) suggests that market efficiency evolves as market participants adapt to a changing environment.

### Concept Drift

Concept drift, the change in the underlying distribution of data, is a significant challenge in financial prediction.
Various techniques, including meta-learning, evolving intelligent systems (EIS), and ensemble methods, have been proposed to address concept drift.
These techniques can adapt to changing market conditions and improve the accuracy of financial predictions.
Meta-learning approaches, in particular, have shown promise in predicting the sequence of change between discrete concepts and maximizing profits in trading strategies.

### ML In Finance

Machine learning (ML) has proven to be a powerful tool for tackling financial prediction under concept drift, which refers to structural breaks that can occur at any frequency level.
Many meta-learning approaches rely on unsupervised algorithms to identify the recurrence of a concept and retrieve previous models, or to detect drifts.
The use of sequential deep learning models, such as RNNs, can be insufficient to handle abrupt changes because they retain the memory of previous market dynamics.

### Techniques And Models

Researchers suggest solutions based on model retraining at regular intervals, upon detection of changes or drift, or on online incremental algorithms.
These approaches involve using up-to-date models with forgetting mechanisms to avoid overfitting and to adapt to new market behaviors.
Ensembles and evolving fuzzy systems are popular solutions, and deep learning has further boosted the popularity of approaches that rely on artificial neural networks.

### Future Research

Future research is likely to emphasize the application of data stream classification algorithms to financial streams, and online machine learning has not been widely applied to the financial domain.
The availability of high-frequency data and computational resources will likely lead to major progress in the near future, with a focus on handling price change dynamics and financial regime shifts.

## Study subjects

### 140 relevant studies

- Total Publications 56 34 20 16 5 5 4. Fig. 2 shows that, out of a total of 140 relevant studies, the majority of the reviewed works use ML techniques for stock forecasting. Some of these works overlap with regime change research, focusing primarily on probabilistic models to classify directional changes and represent different regimes

### 20 data

- Records identi ied from: Databases (n = 7) Registers (n = 0). Records removed before screening: Duplicate record removed (n = 20). Records removed for not being available or not having a subscription (n = 8). Records screened (n = 643)

## Data analysis

- #method/evolving_clustering
- #method/baum_welch_algorithm
- #method/k_means
- #method/gaussian_distribution
- #method/welch
- #method/markov_model

## Findings

- <mark class="claim">These results show that most of the reviewed papers use techniques from four main categories: Evolving systems (that include Evolving clustering, Evolving fuzzy rules and Fuzzy neuro systems), Ensemble based systems (usually with treebased components), <mark class="fact">traditional systems adapted to concept change</mark></mark>

## Builds on previous research

- Among the advantages that they offer, we can mention the fact that they can handle non-stationarities, shifts, and drifts in price generation processes. Another aspect that makes them a good fit for this context is their scalability for continuous learning scenarios [^30].
- While its application to high-frequency markets is still an open problem, recent research works are making progress in understanding how to apply ML to intraday resolutions. Among them, we could mention the one presented by Sirignano and Cont [^73], who claimed that financial data at high frequencies exhibit stylised facts and may hold learnable stationary patterns over long periods.

## Differs from previous work

- In finance, a change in the collective behaviour of market participants and their reactions is called a regime change (RC). As covered by the marked efficiency hypothesis [^25], we cannot observe a trader's individual behaviour or intentions.
- We must also point out that the prediction of future financial trends can be tackled using fundamental or technical analysis. Despite some controversy regarding its potential [^25], [^42], the latter is widely used in short-term trading [^43], which is why the focus is on this approach.

## Contributions

- Summary of Results<mark class="claim">In order to analyse the 223 works, <mark class="fact">we found the need to classify them in more ways</mark> than just according <mark class="fact">to the methodology defined in Section II</mark></mark>. When needed, the topics were updated or clarified during the classification process. <mark class="fact">Results of the classification process with regard to the research questions are detailed in Table I</mark>. Question Q1 Q1 and Q2Topic Regime changesML in stock forecastingConcept drift and online MLRelevant Studies [^14], [^15], [^18], [^19], [^23], [^26], [^29], [^49]–[^63][^1]–[^13], [^20]–[^22], [^24], [^25], [^27], [^28], [^37], [^38], [^42]–[^45], [^64]–[110][^16], [^17], [^30]–[^36], [^39]–[^41], [111]–[143]<mark class="fact">The data required for analysis were extracted by exploring the full text of each research work</mark>. <mark class="fact">Table II presents the results of the search</mark> and the source of the documents. <mark class="fact">Table III presents the results in the second stage</mark>. As mentioned before, <mark class="fact">the total number of papers remaining after the exclusion process was</mark> 140. <mark class="fact">Table I summarises their classification according to the knowledge area</mark>.

## Limitations

- The study limitations include the lack of comprehensive reviews on the topic. The study also notes that the literature on machine learning for financial prediction under regime change is limited.
- The limitations of the study are that it cannot guarantee completeness and that some relevant works may have been missed. The study also notes that the classification of research works into relevant, process assessment, and excluded works may be subjective.
- The limitations of the study include the complexity of managing large amounts of data at high frequencies. The limitations also include the need for further research on seasonality and intraday changes.

## Future work

- The study suggests that future work should focus on exploring the application of data stream learning and concept drift to financial markets. The study also notes that developing new machine learning algorithms to handle non-stationarities, shifts, and drifts in price-generating processes is an area of future research.
- The future work suggested by the study includes further research on the use of machine learning techniques in financial forecasting and the development of new methods for handling regime changes. The study also suggests that further research is needed on the application of regime-switching models to financial forecasting.
- The future work includes developing techniques to adapt to concept drifts and changes in market behaviour. The future work also includes applying machine learning techniques to high-frequency markets.
- The future work in this area is likely to focus on the application of data stream classification algorithms to financial streams, as well as the development of new machine learning techniques that can adapt to changing market conditions.

## References

[^1]: Y. S. Abu-Mostafa, A. F. Atiya, “Introduction to financial forecasting,” Applied Intelligence, vol. 6, pp. 205–213, 7 1996.  [OA](https://engine.scholarcy.com/oa_version?query=Abu-Mostafa%2C%20Y.S.%20Atiya%2C%20A.F.%20Introduction%20to%20financial%20forecasting%201996&author=Abu-Mostafa&title=Introduction%20to%20financial%20forecasting&year=1996) [GScholar](https://scholar.google.co.uk/scholar?q=Abu-Mostafa%2C%20Y.S.%20Atiya%2C%20A.F.%20Introduction%20to%20financial%20forecasting%201996) [Scite](/scite_tallies?query=author%3AAbu-Mostafa%2Ctitle%3AIntroduction%20to%20financial%20forecasting%2Cyear%3A1996)

[^2]: W. Huang, Y. Nakamori, S.-Y. Wang, “Forecasting stock market movement direction with support vector machine,” Computers &amp; Operations Research, vol. 32, pp. 2513–2522, 2005.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20W.%20Nakamori%2C%20Y.%20Wang%2C%20S.-Y.%20Forecasting%20stock%20market%20movement%20direction%20with%20support%20vector%20machine%202005&author=Huang&title=Forecasting%20stock%20market%20movement%20direction%20with%20support%20vector%20machine&year=2005) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20W.%20Nakamori%2C%20Y.%20Wang%2C%20S.-Y.%20Forecasting%20stock%20market%20movement%20direction%20with%20support%20vector%20machine%202005) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AForecasting%20stock%20market%20movement%20direction%20with%20support%20vector%20machine%2Cyear%3A2005)

[^13]: J. Patel, S. Shah, P. Thakkar, K. Kotecha, “Predicting stock and stock price index movement using trend deterministic data preparation and machine learning techniques,” Expert Systems with Applications, vol. 42, no. 1, pp. 259–268, 2015, doi:<https://doi.org/10.1016/j.eswa.2014.07.040>.  [OA](https://doi.org/10.1016/j.eswa.2014.07.040)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2014.07.040)

[^14]: D. Ardia, K. Bluteau, M. Rüede, “Regime changes in Bitcoin GARCH volatility dynamics,” Finance Research Letters, vol. 29, pp. 266–271, Jun. 2019, doi:10.1016/J.FRL.2018.08.009.  [OA](https://doi.org/10.1016/J.FRL.2018.08.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/J.FRL.2018.08.009)

[^15]: A. Ang, A. Timmermann, “Regime changes and financial markets,” Annual Review of Financial Economics, vol. 4, no. 1, pp. 313–337, 2012.  [OA](https://engine.scholarcy.com/oa_version?query=Ang%2C%20A.%20Timmermann%2C%20A.%20Regime%20changes%20and%20financial%20markets%202012&author=Ang&title=Regime%20changes%20and%20financial%20markets&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Ang%2C%20A.%20Timmermann%2C%20A.%20Regime%20changes%20and%20financial%20markets%202012) [Scite](/scite_tallies?query=author%3AAng%2Ctitle%3ARegime%20changes%20and%20financial%20markets%2Cyear%3A2012)

[^16]: A. Tsymbal, “The Problem of Concept Drift: Definitions and Related Work,” Technical Report: TCD-CS-2004-15, Department of Computer Science, Trinity College, Dublin, 2004.  [OA](https://scholar.google.co.uk/scholar?q=Tsymbal%2C%20A.%20The%20Problem%20of%20Concept%20Drift%3A%20Definitions%20and%20Related%20Work%202004) [GScholar](https://scholar.google.co.uk/scholar?q=Tsymbal%2C%20A.%20The%20Problem%20of%20Concept%20Drift%3A%20Definitions%20and%20Related%20Work%202004)

[^17]: A. L. Suárez-Cetrulo, A. Cervantes, D. Quintana, “Incremental Market Behavior Classification in Presence of Recurring Concepts,” Entropy, vol. 21, p. 25, Jan. 2019, doi:10.3390/e21010025.  [OA](https://doi.org/10.3390/e21010025)  [Scite](/scite_tallies?query=https://doi.org/10.3390/e21010025)

[^18]: M. C. Münnix, T. Shimada, R. Schäfer, F. Leyvraz, T. H. Seligman, T. Guhr, H. E. Stanley, “Identifying States of a Financial Market,” Scientific Reports, vol. 2, p. 644, 12 2012.  [OA](https://engine.scholarcy.com/oa_version?query=M%C3%BCnnix%2C%20M.C.%20Shimada%2C%20T.%20Sch%C3%A4fer%2C%20R.%20Leyvraz%2C%20F.%20Identifying%20States%20of%20a%20Financial%20Market%202012&author=Muennix&title=Identifying%20States%20of%20a%20Financial%20Market&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=M%C3%BCnnix%2C%20M.C.%20Shimada%2C%20T.%20Sch%C3%A4fer%2C%20R.%20Leyvraz%2C%20F.%20Identifying%20States%20of%20a%20Financial%20Market%202012) [Scite](/scite_tallies?query=author%3AMuennix%2Ctitle%3AIdentifying%20States%20of%20a%20Financial%20Market%2Cyear%3A2012)

[^19]: E. Tsang, J. Chen, Detecting regime change in computational finance: data science, machine learning and algorithmic trading. CRC Press, 2020.  [OA](https://scholar.google.co.uk/scholar?q=Tsang%2C%20E.%20Chen%2C%20J.%20Detecting%20regime%20change%20in%20computational%20finance%3A%20data%20science%2C%20machine%20learning%20and%20algorithmic%20trading%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Tsang%2C%20E.%20Chen%2C%20J.%20Detecting%20regime%20change%20in%20computational%20finance%3A%20data%20science%2C%20machine%20learning%20and%20algorithmic%20trading%202020)

[^20]: R. T. Das, K. K. Ang, C. Quek, “IeRSPOP: A novel incremental rough set-based pseudo outer-product with ensemble learning,” Applied Soft Computing Journal, vol. 46, pp. 170–186, 9 2016.  [OA](https://engine.scholarcy.com/oa_version?query=Das%2C%20R.T.%20Ang%2C%20K.K.%20Quek%2C%20C.%20IeRSPOP%3A%20A%20novel%20incremental%20rough%20set-based%20pseudo%20outer-product%20with%20ensemble%20learning%202016&author=Das&title=IeRSPOP%3A%20A%20novel%20incremental%20rough%20set-based%20pseudo%20outer-product%20with%20ensemble%20learning&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Das%2C%20R.T.%20Ang%2C%20K.K.%20Quek%2C%20C.%20IeRSPOP%3A%20A%20novel%20incremental%20rough%20set-based%20pseudo%20outer-product%20with%20ensemble%20learning%202016) [Scite](/scite_tallies?query=author%3ADas%2Ctitle%3AIeRSPOP%3A%20A%20novel%20incremental%20rough%20set-based%20pseudo%20outer-product%20with%20ensemble%20learning%2Cyear%3A2016)

[^22]: Y. Hu, K. Liu, X. Zhang, K. Xie, W. Chen, Y. Zeng, M. Liu, “Concept drift mining of portfolio selection factors in stock market,” Electronic Commerce Research and Applications, vol. 14, no. 6, pp. 444–455, 2015.  [OA](https://engine.scholarcy.com/oa_version?query=Hu%2C%20Y.%20Liu%2C%20K.%20Zhang%2C%20X.%20Xie%2C%20K.%20Concept%20drift%20mining%20of%20portfolio%20selection%20factors%20in%20stock%20market%202015&author=Hu&title=Concept%20drift%20mining%20of%20portfolio%20selection%20factors%20in%20stock%20market&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Hu%2C%20Y.%20Liu%2C%20K.%20Zhang%2C%20X.%20Xie%2C%20K.%20Concept%20drift%20mining%20of%20portfolio%20selection%20factors%20in%20stock%20market%202015) [Scite](/scite_tallies?query=author%3AHu%2Ctitle%3AConcept%20drift%20mining%20of%20portfolio%20selection%20factors%20in%20stock%20market%2Cyear%3A2015)

[^23]: B. Silva, N. Marques, G. Panosso, “Applying neural networks for concept drift detection in financial markets,” in CEUR Workshop Proceedings, vol. 960, 2012, pp. 43–47.  [OA](https://scholar.google.co.uk/scholar?q=Silva%2C%20B.%20Marques%2C%20N.%20Panosso%2C%20G.%20Applying%20neural%20networks%20for%20concept%20drift%20detection%20in%20financial%20markets%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Silva%2C%20B.%20Marques%2C%20N.%20Panosso%2C%20G.%20Applying%20neural%20networks%20for%20concept%20drift%20detection%20in%20financial%20markets%202012)

[^24]: X. Gu, P. P. Angelov, A. M. Ali, W. A. Gruver, G. Gaydadjiev, “Online evolving fuzzy rule-based prediction model for high frequency trading financial data stream,” in 2016 IEEE Conference on Evolving and Adaptive Intelligent Systems (EAIS), 5 2016, pp. 169–175, IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Gu%2C%20X.%20Angelov%2C%20P.P.%20Ali%2C%20A.M.%20Gruver%2C%20W.A.%20Online%20evolving%20fuzzy%20rule-based%20prediction%20model%20for%20high%20frequency%20trading%20financial%20data%20stream%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Gu%2C%20X.%20Angelov%2C%20P.P.%20Ali%2C%20A.M.%20Gruver%2C%20W.A.%20Online%20evolving%20fuzzy%20rule-based%20prediction%20model%20for%20high%20frequency%20trading%20financial%20data%20stream%202016)

[^25]: E. F. Fama, “Efficient Capital Markets: A Review of Theory and Empirical Work,” The Journal of Finance, vol. 25, no. 2, p. 383, 1970, doi:10.2307/2325486.  [OA](https://doi.org/10.2307/2325486)  [Scite](/scite_tallies?query=https://doi.org/10.2307/2325486)

[^26]: J. Piger, Econometrics: Models of Regime Changes, pp. 2744–2757. New York, NY: Springer New York, 2009.  [OA](https://scholar.google.co.uk/scholar?q=Piger%2C%20J.%20Econometrics%3A%20Models%20of%20Regime%20Changes%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Piger%2C%20J.%20Econometrics%3A%20Models%20of%20Regime%20Changes%202009)

[^27]: A. G. Hoepner, D. McMillan, A. Vivian, Wese Simen, “Significance, relevance and explainability in the machine learning age: an econometrics and financial data science perspective,” The European Journal of Finance, vol. 27, no. 1-2, pp. 1–7, 2021.  [OA](https://engine.scholarcy.com/oa_version?query=Hoepner%2C%20A.G.%20McMillan%2C%20D.%20Vivian%2C%20A.%20Simen%2C%20Wese%20Significance%2C%20relevance%20and%20explainability%20in%20the%20machine%20learning%20age%3A%20an%20econometrics%20and%20financial%20data%20science%20perspective%202021&author=Hoepner&title=Significance%2C%20relevance%20and%20explainability%20in%20the%20machine%20learning%20age%3A%20an%20econometrics%20and%20financial%20data%20science%20perspective&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Hoepner%2C%20A.G.%20McMillan%2C%20D.%20Vivian%2C%20A.%20Simen%2C%20Wese%20Significance%2C%20relevance%20and%20explainability%20in%20the%20machine%20learning%20age%3A%20an%20econometrics%20and%20financial%20data%20science%20perspective%202021) [Scite](/scite_tallies?query=author%3AHoepner%2Ctitle%3ASignificance%2C%20relevance%20and%20explainability%20in%20the%20machine%20learning%20age%3A%20an%20econometrics%20and%20financial%20data%20science%20perspective%2Cyear%3A2021)

[^28]: P. Bracke, A. Datta, C. Jung, S. Sen, “Machine learning explainability in finance: an application to default risk analysis,” Bank of England, 2019.  [OA](https://engine.scholarcy.com/oa_version?query=Bracke%2C%20P.%20Datta%2C%20A.%20Jung%2C%20C.%20Sen%2C%20S.%20Machine%20learning%20explainability%20in%20finance%3A%20an%20application%20to%20default%20risk%20analysis%202019&author=Bracke&title=Machine%20learning%20explainability%20in%20finance%3A%20an%20application%20to%20default%20risk%20analysis&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Bracke%2C%20P.%20Datta%2C%20A.%20Jung%2C%20C.%20Sen%2C%20S.%20Machine%20learning%20explainability%20in%20finance%3A%20an%20application%20to%20default%20risk%20analysis%202019) [Scite](/scite_tallies?query=author%3ABracke%2Ctitle%3AMachine%20learning%20explainability%20in%20finance%3A%20an%20application%20to%20default%20risk%20analysis%2Cyear%3A2019)

[^29]: M. Kritzman, S. Page, D. Turkington, “Regime shifts: Implications for dynamic strategies (corrected),” Financial Analysts Journal, vol. 68, no. 3, pp. 22–39, 2012.  [OA](https://engine.scholarcy.com/oa_version?query=Kritzman%2C%20M.%20Page%2C%20S.%20Turkington%2C%20D.%20Regime%20shifts%3A%20Implications%20for%20dynamic%20strategies%20%28corrected%202012&author=Kritzman&title=Regime%20shifts%3A%20Implications%20for%20dynamic%20strategies%20%28corrected&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Kritzman%2C%20M.%20Page%2C%20S.%20Turkington%2C%20D.%20Regime%20shifts%3A%20Implications%20for%20dynamic%20strategies%20%28corrected%202012) [Scite](/scite_tallies?query=author%3AKritzman%2Ctitle%3ARegime%20shifts%3A%20Implications%20for%20dynamic%20strategies%20%28corrected%2Cyear%3A2012)

[^30]: R. Elwell, R. Polikar, “Incremental learning of concept drift in nonstationary environments,” IEEE transactions on neural networks, vol. 22, pp. 1517–31, 10 2011.  [OA](https://engine.scholarcy.com/oa_version?query=Elwell%2C%20R.%20Polikar%2C%20R.%20Incremental%20learning%20of%20concept%20drift%20in%20nonstationary%20environments%202011&author=Elwell&title=Incremental%20learning%20of%20concept%20drift%20in%20nonstationary%20environments&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Elwell%2C%20R.%20Polikar%2C%20R.%20Incremental%20learning%20of%20concept%20drift%20in%20nonstationary%20environments%202011) [Scite](/scite_tallies?query=author%3AElwell%2Ctitle%3AIncremental%20learning%20of%20concept%20drift%20in%20nonstationary%20environments%2Cyear%3A2011)

[^36]: A. R. Masegosa, A. M. Martínez, D. Ramos-López, H. Langseth, T. D. Nielsen, A. Salmerón, “Analyzing concept drift: A case study in the financial sector,” Intelligent Data Analysis, vol. 24, no. 3, pp. 665–688, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Masegosa%2C%20A.R.%20Mart%C3%ADnez%2C%20A.M.%20Ramos-L%C3%B3pez%2C%20D.%20Langseth%2C%20H.%20Analyzing%20concept%20drift%3A%20A%20case%20study%20in%20the%20financial%20sector%202020&author=Masegosa&title=Analyzing%20concept%20drift%3A%20A%20case%20study%20in%20the%20financial%20sector&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Masegosa%2C%20A.R.%20Mart%C3%ADnez%2C%20A.M.%20Ramos-L%C3%B3pez%2C%20D.%20Langseth%2C%20H.%20Analyzing%20concept%20drift%3A%20A%20case%20study%20in%20the%20financial%20sector%202020) [Scite](/scite_tallies?query=author%3AMasegosa%2Ctitle%3AAnalyzing%20concept%20drift%3A%20A%20case%20study%20in%20the%20financial%20sector%2Cyear%3A2020)

[^37]: M. Pratama, E. Lughofer, J. Er, S. Anavatti, C.-P. Lim, “Data-driven modelling based on Recurrent Interval-Valued Metacognitive Scaffolding Fuzzy Neural Network,” Neurocomputing, vol. 262, pp. 4–27, 2017.  [OA](https://engine.scholarcy.com/oa_version?query=Pratama%2C%20M.%20Lughofer%2C%20E.%20Er%2C%20J.%20Anavatti%2C%20S.%20Data%20driven%20modelling%20based%20on%20Recurrent%20Interval-Valued%20Metacognitive%20Scaffolding%20Fuzzy%20Neural%20Network%202017&author=Pratama&title=Data%20driven%20modelling%20based%20on%20Recurrent%20Interval-Valued%20Metacognitive%20Scaffolding%20Fuzzy%20Neural%20Network&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Pratama%2C%20M.%20Lughofer%2C%20E.%20Er%2C%20J.%20Anavatti%2C%20S.%20Data%20driven%20modelling%20based%20on%20Recurrent%20Interval-Valued%20Metacognitive%20Scaffolding%20Fuzzy%20Neural%20Network%202017) [Scite](/scite_tallies?query=author%3APratama%2Ctitle%3AData%20driven%20modelling%20based%20on%20Recurrent%20Interval-Valued%20Metacognitive%20Scaffolding%20Fuzzy%20Neural%20Network%2Cyear%3A2017)

[^38]: M. Pratama, J. Lu, E. Lughofer, G. Zhang, M. J. Er, “Incremental Learning of Concept Drift Using Evolving Type-2 Recurrent Fuzzy Neural Network,” IEEE Transactions on Fuzzy Systems, pp. 1–1, 2016, doi:10.1109/ TFUZZ.2016.2599855.  [OA](https://engine.scholarcy.com/oa_version?query=Pratama%2C%20M.%20Lu%2C%20J.%20Lughofer%2C%20E.%20Zhang%2C%20G.%20Incremental%20Learning%20of%20Concept%20Drift%20Using%20Evolving%20Type-2%20Recurrent%20Fuzzy%20Neural%20Network%202016&author=Pratama&title=Incremental%20Learning%20of%20Concept%20Drift%20Using%20Evolving%20Type-2%20Recurrent%20Fuzzy%20Neural%20Network&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Pratama%2C%20M.%20Lu%2C%20J.%20Lughofer%2C%20E.%20Zhang%2C%20G.%20Incremental%20Learning%20of%20Concept%20Drift%20Using%20Evolving%20Type-2%20Recurrent%20Fuzzy%20Neural%20Network%202016) [Scite](/scite_tallies?query=author%3APratama%2Ctitle%3AIncremental%20Learning%20of%20Concept%20Drift%20Using%20Evolving%20Type-2%20Recurrent%20Fuzzy%20Neural%20Network%2Cyear%3A2016)

[^39]: C. Alippi, G. Boracchi, M. Roveri, “Just-in-time classifiers for recurrent concepts,” IEEE Transactions on Neural Networks and Learning Systems, vol. 24, pp. 620–634, 4 2013.  [OA](https://engine.scholarcy.com/oa_version?query=Alippi%2C%20C.%20Boracchi%2C%20G.%20Roveri%2C%20M.%20Just-in-time%20classifiers%20for%20recurrent%20concepts%202013&author=Alippi&title=Just-in-time%20classifiers%20for%20recurrent%20concepts&year=2013) [GScholar](https://scholar.google.co.uk/scholar?q=Alippi%2C%20C.%20Boracchi%2C%20G.%20Roveri%2C%20M.%20Just-in-time%20classifiers%20for%20recurrent%20concepts%202013) [Scite](/scite_tallies?query=author%3AAlippi%2Ctitle%3AJust-in-time%20classifiers%20for%20recurrent%20concepts%2Cyear%3A2013)

[^41]: P. M. Gonçalves Jr, R. Souto, M. De Barros, “RCD: A recurring concept drift framework,” Pattern Recognition Letters, vol. 34, pp. 1018–1025, 2013.  [OA](https://engine.scholarcy.com/oa_version?query=Gon%C3%A7alves%2C%20Jr%2C%20P.M.%20Souto%2C%20R.%20Barros%2C%20M.%20RCD%3A%20A%20recurring%20concept%20drift%20framework%202013&author=Gon%C3%A7alves&title=RCD%3A%20A%20recurring%20concept%20drift%20framework&year=2013) [GScholar](https://scholar.google.co.uk/scholar?q=Gon%C3%A7alves%2C%20Jr%2C%20P.M.%20Souto%2C%20R.%20Barros%2C%20M.%20RCD%3A%20A%20recurring%20concept%20drift%20framework%202013) [Scite](/scite_tallies?query=author%3AGon%C3%A7alves%2Ctitle%3ARCD%3A%20A%20recurring%20concept%20drift%20framework%2Cyear%3A2013)

[^42]: A. W. Lo, H. Mamaysky, J. Wang, “Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation,” The Journal of Finance, vol. 55, pp. 1705–1765, 8 2000.  [OA](https://engine.scholarcy.com/oa_version?query=Lo%2C%20A.W.%20Mamaysky%2C%20H.%20Wang%2C%20J.%20Foundations%20of%20Technical%20Analysis%3A%20Computational%20Algorithms%2C%20Statistical%20Inference%2C%20and%20Empirical%20Implementation%202000&author=Lo&title=Foundations%20of%20Technical%20Analysis%3A%20Computational%20Algorithms%2C%20Statistical%20Inference%2C%20and%20Empirical%20Implementation&year=2000) [GScholar](https://scholar.google.co.uk/scholar?q=Lo%2C%20A.W.%20Mamaysky%2C%20H.%20Wang%2C%20J.%20Foundations%20of%20Technical%20Analysis%3A%20Computational%20Algorithms%2C%20Statistical%20Inference%2C%20and%20Empirical%20Implementation%202000) [Scite](/scite_tallies?query=author%3ALo%2Ctitle%3AFoundations%20of%20Technical%20Analysis%3A%20Computational%20Algorithms%2C%20Statistical%20Inference%2C%20and%20Empirical%20Implementation%2Cyear%3A2000)

[^43]: F. E. Tay, L. Cao, “Application of support vector machines in financial time series forecasting,” Omega, vol. 29, pp. 309–317, 8 2001.  [OA](https://engine.scholarcy.com/oa_version?query=Tay%2C%20F.E.%20Cao%2C%20L.%20Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%202001&author=Tay&title=Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting&year=2001) [GScholar](https://scholar.google.co.uk/scholar?q=Tay%2C%20F.E.%20Cao%2C%20L.%20Application%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%202001) [Scite](/scite_tallies?query=author%3ATay%2Ctitle%3AApplication%20of%20support%20vector%20machines%20in%20financial%20time%20series%20forecasting%2Cyear%3A2001)

[^45]: C. H. Chen, P. Y. Chen, J. C. W. Lin, “An Ensemble Classifier for Stock Trend Prediction Using Sentence- Level Chinese News Sentiment and Technical Indicators,” International Journal of Interactive Multimedia and Artificial Intelligence, vol. 7, no. 3, pp. 53–64, 2022, doi:10.9781/ijimai.2022.02.004.  [OA](https://doi.org/10.9781/ijimai.2022.02.004)  [Scite](/scite_tallies?query=https://doi.org/10.9781/ijimai.2022.02.004)

[^49]: A. W. Lo, “Reconciling efficient markets with behavioral finance: the adaptive markets hypothesis,” Journal of Investment Consulting, vol. 7, no. 2, pp. 21–44, 2005.  [OA](https://engine.scholarcy.com/oa_version?query=Lo%2C%20A.W.%20Reconciling%20efficient%20markets%20with%20behavioral%20finance%3A%20the%20adaptive%20markets%20hypothesis%202005&author=Lo&title=Reconciling%20efficient%20markets%20with%20behavioral%20finance%3A%20the%20adaptive%20markets%20hypothesis&year=2005) [GScholar](https://scholar.google.co.uk/scholar?q=Lo%2C%20A.W.%20Reconciling%20efficient%20markets%20with%20behavioral%20finance%3A%20the%20adaptive%20markets%20hypothesis%202005) [Scite](/scite_tallies?query=author%3ALo%2Ctitle%3AReconciling%20efficient%20markets%20with%20behavioral%20finance%3A%20the%20adaptive%20markets%20hypothesis%2Cyear%3A2005)

[^63]: J. D. Hamilton, “Macroeconomic regimes and regime shifts,” Handbook of macroeconomics, vol. 2, pp. 163– 201, 2016.  [OA](https://engine.scholarcy.com/oa_version?query=Hamilton%2C%20J.D.%20Macroeconomic%20regimes%20and%20regime%20shifts%202016&author=Hamilton&title=Macroeconomic%20regimes%20and%20regime%20shifts&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Hamilton%2C%20J.D.%20Macroeconomic%20regimes%20and%20regime%20shifts%202016) [Scite](/scite_tallies?query=author%3AHamilton%2Ctitle%3AMacroeconomic%20regimes%20and%20regime%20shifts%2Cyear%3A2016)

[^64]: J. G. Dias, J. K. Vermunt, S. Ramos, “Clustering financial time series: New insights from an extended hidden Markov model,” European Journal of Operational Research, vol. 243, no. 3, pp. 852–864, 2015.  [OA](https://engine.scholarcy.com/oa_version?query=Dias%2C%20J.G.%20Vermunt%2C%20J.K.%20Ramos%2C%20S.%20Clustering%20financial%20time%20series%3A%20New%20insights%20from%20an%20extended%20hidden%20markov%20model%202015&author=Dias&title=Clustering%20financial%20time%20series%3A%20New%20insights%20from%20an%20extended%20hidden%20markov%20model&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Dias%2C%20J.G.%20Vermunt%2C%20J.K.%20Ramos%2C%20S.%20Clustering%20financial%20time%20series%3A%20New%20insights%20from%20an%20extended%20hidden%20markov%20model%202015) [Scite](/scite_tallies?query=author%3ADias%2Ctitle%3AClustering%20financial%20time%20series%3A%20New%20insights%20from%20an%20extended%20hidden%20markov%20model%2Cyear%3A2015)

[^73]: J. Sirignano, R. Cont, “Universal features of price formation in financial markets: perspectives from deep learning,” Quantitative Finance, 2019, doi:10.1080/14697688.2019.1622295.  [OA](https://doi.org/10.1080/14697688.2019.1622295)  [Scite](/scite_tallies?query=https://doi.org/10.1080/14697688.2019.1622295)
