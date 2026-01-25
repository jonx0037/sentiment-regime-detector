[[Shi_UnderstandingGoldDollarPriceMovements_2025]]

# [Understanding Gold and Dollar Price Movements: A Sentiment-Based GARCH-MIDAS Approach](https://doi.org/10.2991/978-94-6463-835-6_47)

## [[Chengyu Shi]]

## Abstract

Generally, gold prices exhibit an inverse relationship with the US Dollar Index (DXY). However, a notable deviation occurred in 2020 and 2022 when both markets displayed synchronized upward trends, challenging conventional financial theories. To explore this anomaly, this study proposes an innovative framework by integrating sentiment indicators into the GARCH-MIDAS model, thereby constructing a GARCH-MIDAS-Sentiment hybrid model. Leveraging high-frequency market data and textual sentiment indices derived from news and social media, the research quantifies the behavioral factors that influence gold's safe-haven attributes during macroeconomic shocks. Empirical results demonstrate that the augmented model reduces out-of-sample prediction errors by 18.7% compared to traditional volatility models, while significantly improving the explainability of tail risks during crisis periods. Specifically, sentiment-driven herding effects, amplified by pandemic uncertainties and geopolitical tensions, were identified as critical channels driving the shift in the gold-DXY correlation. This methodology advances precious metals market analysis by bridging behavioral finance with macroeconometric modeling, offering institutional investors a dynamic tool for portfolio hedging under structural-break scenarios. The findings further underscore the need to incorporate nonlinear sentiment dynamics into commodity pricing models amid escalating global market interconnectedness.

## Key concepts

# finding/dollar_index; #dollar_index; #finding/gold_price; #gold_price; #claim/MIDAS; #MIDAS; #random_forests; #safe_haven

## Quote
>
> This study proposes a sentiment-based GARCH-MIDAS approach to understand the price movements of gold and the US Dollar Index, finding that sentiment-driven herding effects are critical channels driving the gold-DXY correlation shift.

## Key points

- As a unique asset combining commodity and financial attributes, gold price fluctuations have historically been significantly influenced by traditional factors such as the U.S dollar index and real interest rates
- Leveraging the World Gold Council’s global holdings data, transaction flows, and sentiment databases, this study aims to quantify sentiment factors through machine learning methods and integrate them into an enhanced GARCH-MIDAS model to unravel the drivers behind the “co-rise” of the dollar index and gold prices
- This study develops a gold price volatility forecasting framework by embedding sentiment factors into a GARCH-MIDAS model with mixed-frequency data, revealing the significant enhancement of market sentiment mechanisms in explaining precious metal
- Empirical results demonstrate that sentiment factors effectively capture the nonlinear characteristics of gold price volatility, accounting for approximately 15% of unobserved heteroskedasticity in long-term volatility components
- The analysis identifies interaction effects between sentiment factors and macroeconomic uncertainty, suggesting that multi-factor coupling models may better capture complex market dynamics
- This research validates the effectiveness of sentiment factors in gold volatility prediction within mixed-frequency frameworks, establishing a new paradigm for interdisciplinary studies in behavioural finance and volatility modelling

## Summary

### Snapshot

This study proposes a sentiment-based GARCH-MIDAS approach to understand the price movements of gold and the US Dollar Index, finding that sentiment-driven herding effects are critical channels driving the shift in the gold-DXY correlation.

### Key findings

The study finds that sentiment-driven herding effects, amplified by pandemic uncertainties and geopolitical tensions, are critical channels driving the shift in the gold-DXY correlation, and that the augmented model reduces out-of-sample prediction errors by 18.7% compared to traditional volatility models.
The study finds that sentiment factors effectively capture the nonlinearities in gold price volatility, accounting for approximately 15% of the unobserved heteroskedasticity in long-term volatility components. The marginal impact of negative sentiment on volatility is 1.8 times stronger than that of positive sentiment.
Empirical results demonstrate that sentiment factors effectively capture the nonlinear characteristics of gold price volatility, accounting for approximately 15% of unobserved heteroskedasticity in long-term volatility components
The analysis identifies interaction effects between sentiment factors and macroeconomic uncertainty, suggesting that multi-factor coupling models may better capture complex market dynamics
This research validates the effectiveness of sentiment factors in gold volatility prediction within mixed-frequency frameworks, establishing a new paradigm for interdisciplinary studies in behavioural finance and volatility modelling

### Objectives

The study aims to develop a framework for forecasting gold price volatility by incorporating sentiment factors into a GARCH-MIDAS model. The objective is to provide a forward-looking quantitative framework for analyzing asset price dynamics in the presence of significant event-driven disruptions.

### Methods

The study uses a high-frequency dataset encompassing gold prices, macroeconomic indicators, and market sentiment variables, and employs a FinBERT model to score sentiment from global mainstream financial media texts.
The study uses a GARCH-MIDAS model with mixed-frequency data and incorporates sentiment factors. The analysis employs mixed-frequency decomposition to disentangle long-term volatility components driven by sentiment shocks from short-term GARCH-driven fluctuations.

### Results

The study finds that the hybrid model exhibits remarkable efficacy in identifying regime-switching dynamics, particularly in capturing cyclical turning points in gold prices, and that the mean squared error (MSE) for out-of-sample predictions is reduced by 23.6% compared to traditional GARCH models.
The study finds that the enhanced model exhibits incremental predictive power in volatility forecasting compared to traditional GARCH models and baseline GARCH-MIDAS models without sentiment factors. The results show a significant interaction effect between sentiment factors and macroeconomic uncertainty.

### Conclusions

The study concludes that the sentiment-based GARCH-MIDAS approach provides a robust foundation for academic inquiry and practical asset management, and that the findings underscore the need to incorporate nonlinear sentiment dynamics into commodity pricing models amid escalating global market interconnectedness.
The study concludes that sentiment factors are effective at capturing the nonlinear characteristics of gold price volatility and significantly enhance the explanatory power of market sentiment mechanisms in explaining precious metal market fluctuations. The findings establish a new paradigm for interdisciplinary studies in behavioural finance and volatility modelling.

## Data analysis

- #method/figarch_model
- #method/
- #method/finbert_model
- #method/correlation_coefficient

## Findings

- Despite a cumulative 12% rise in the U.S <a class="keyword" href="https://en.wikipedia.org/wiki/Dollar_Index" title="dollar index">dollar index</a>, <a class="keyword" href="https://en.wikipedia.org/wiki/Gold_price" title="gold prices">gold prices</a> surged over 40% in tandem [^3]
- The SI series is subjected to ADF unit root tests; non-stationarity (p &gt; 0.05) necessitates first differencing, (ΔSIt = SIt − SIt − 1ΔSIt = SIt − SIt − 1) ensuring stationarity (p &lt; 0.01 post − differencing)
- The mean squared error (<a class="keyword" href="#" title="mean squared error">MSE</a>) for out-of-sample predictions is reduced by 23.6% compared to traditional GARCH models

## Contributions

- <mark class="claim">This study develops a gold price volatility forecasting framework by embedding sentiment factors into a GARCH-MIDAS model with mixed-frequency data, revealing the significant enhancement of market sentiment mechanisms in explaining precious metal</mark> market fluctuations. <mark class="fact">Empirical results demonstrate that sentiment factors effectively capture the nonlinear characteristics of gold price volatility</mark>, accounting for approximately 15% of unobserved heteroskedasticity in long-term volatility components. Compared to traditional GARCH models and baseline GARCH-MIDAS models without sentiment factors, the enhanced model exhibits incremental predictive power in volatility forecasting. <mark class="fact">The framework successfully disentangles long-term volatility components driven by sentiment shocks from short-term</mark> GARCH-driven fluctuations through mixed-frequency decomposition. Notably, the marginal impact of negative sentiment on volatility is 1.8 times stronger than that of positive sentiment—an asymmetric effect consistent with the loss aversion hypothesis in behavioural finance, providing novel empirical evidence for cross-market sentiment transmission mechanisms.

## Limitations

- The study notes that traditional models face limitations in capturing nonlinear interactions and sentiment factors, and that the study's methodology advances precious metal market analysis by bridging behavioral finance with macroeconometric modeling.
- The study notes that the static sentiment composite indicators employed in the study inadequately capture the time-varying characteristics of sentiment factors. Future research could integrate dynamic regularisation techniques from GINN models to address this limitation.

## Future work

- The study suggests that future research should continue to explore the role of sentiment factors in commodity pricing models, and that the hybrid GARCH-MIDAS framework provides a computable interface for a multi-layered pricing mechanism.
- The study suggests that future research could integrate dynamic regularisation techniques from GINN models and implement LSTM networks for adaptive sentiment weight adjustments. Additionally, the study recommends incorporating regime-switching mechanisms from MS-VECM frameworks to explore volatility dynamics across macroeconomic cycles.

## References

[^3]: World Gold Council. Gold Market Commentary March 2025. World Gold Council (2025, April 8), last accessed 2025/04/10.  [OA](https://scholar.google.co.uk/scholar?q=World%20Gold%20Council%20Gold%20Market%20Commentary%20March%202025%20World%20Gold%20Council%202025%20April%208%20last%20accessed%2020250410) [GScholar](https://scholar.google.co.uk/scholar?q=World%20Gold%20Council%20Gold%20Market%20Commentary%20March%202025%20World%20Gold%20Council%202025%20April%208%20last%20accessed%2020250410)
