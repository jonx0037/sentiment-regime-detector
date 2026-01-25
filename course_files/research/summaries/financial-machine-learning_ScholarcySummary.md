[[University_FinancialMachineLearning_2023]]

# [Financial Machine Learning]()

## [[Bryan Kelly Yale University]]; [[AQR Capital Management bryan.kelly@yale.edu]]

## Abstract

We survey the nascent literature on machine learning in the study of financial markets. We highlight the best examples of what this line of research offers and recommend promising directions for future research. This survey is designed for both financial economists interested in learning about machine learning tools and for statisticians and machine learners seeking interesting financial contexts where advanced methods may be deployed. Acknowledgements. We are grateful to Doron Avramov, Max Helman, Antti Ilmanen, Sydney Ludvigson, Yueran Ma, Semyon Malamud, Tobias Moskowitz, Lasse Pedersen, Markus Pelger, Seth Pruitt, and Guofu Zhou for helpful comments. AQR Capital Management is a global investment management firm, which may or may not apply similar investment techniques or methods of analysis as described herein. The views expressed here are those of the authors and not necessarily those of AQR.

## Key concepts

# ordinary_least_squares; #recurrent_neural_networks; #machine_learning; #stochastic_discount_factor; #partial_least_squares

## Quote
>
> This survey highlights the best examples of machine learning in financial markets research and recommends promising directions for future research, aiming to help readers recognize machine learning as an indispensable tool for developing our understanding of financial market phenomena.

## Key points

- The more structure you Introduction: The Case for Financial Machine Learning can impose in your model, the fewer parameters you need to estimate and the more efficiently your model can use available data points to cut through noise
- The search is underway for a theoretical rationale to explain the success of behemoth parameterizations and answer the question succinctly posed by [^Breiman_1995_a]: “Why don’t heavily parameterized neural networks overfit the data?” We offer a glimpse into the answer
- An exciting potential direction for research is to leverage the flexible model approximations afforded by machine learning to better detect and adapt to structural shifts
- While this survey has focused on the asset pricing side of finance, machine learning is making inroads in other fields such as corporate finance, entrepreneurship, household finance, and real estate
- While machine learning has seen far more extensive use in asset pricing, its further application to corporate finance problems is an exciting area of future research

## Summary

### Challenges

The application of machine learning in finance faces challenges due to the complexity of financial markets and the large sets of conditioning information that influence asset prices.
The study of asset prices is inextricably tied to information, and guiding questions in financial economics include what information market participants have and how they use it.
The vast scope of conditioning information lurking behind market prices makes it difficult to model asset behavior.

### Information

The production function of the modern asset management industry is a testament to the vast amount of information flowing into asset prices.
Professional managers routinely pore over news feeds, data releases, and expert predictions to inform their investment decisions.
The expanse of price-relevant information is compounded by the panel nature of financial markets, with time-series variation and cross-sectional behaviors that are distinct to individual assets or asset groups.

### Machine Learning

Machine learning is a toolkit that can help narrow the gap between researchers' and market participants' information sets by providing methods that enable researchers to assimilate larger information sets.
Machine learning methods are explicitly designed to approximate unknown data-generating functions and can help integrate many data sources into a single model.
The definition of machine learning includes a diverse collection of high-dimensional models for statistical prediction, combined with regularization methods for model selection and overfitting mitigation, and efficient algorithms for searching over a vast number of potential model specifications.
Machine learning involves selecting a preferred model from a diverse collection of candidate models, with model selection at the heart of the empirical design.
The process of searching through many models to find top performers is characteristic of all machine learning methods, but this can lead to in-sample overfitting and poor out-of-sample performance.
Regularization methods are used to constrain model size and to encourage stable out-of-sample performance.
Recent research has shown that models with large parameterizations can outperform simpler models, even when the number of parameters exceeds the number of training observations.
The success of these models can be attributed to their ability to approximate complex relationships between variables.
Random matrix theory can be used to describe the behavior of these models and provide insights into their expected out-of-sample performance.
Machine learning approaches can be used to improve portfolio choice solutions by integrating estimation and utility optimization.
The "plug-in" portfolio solution, which treats estimates of return distributions as known quantities, can perform poorly in practice, especially when the number of assets is large.
Kan and Zhou (2007) demonstrate that simple portfolio tweaks can improve expected utility, and that investors can mitigate out-of-sample utility loss by internalizing the impact of estimation uncertainty.
Machine learning methods can be used to parameterize the portfolio rule and optimize in-sample utility, while regularization techniques encourage stable out-of-sample performance.
Machine learning is being used to improve understanding of financial market phenomena, with a focus on areas such as return prediction, factor models of risk and return, stochastic discount factors, and portfolio choice.
Risk modeling and derivatives pricing are also important topics that benefit from machine learning methods.

### Challenges In Finance

Financial research presents challenges for machine learning, including small data sets, weak signal-to-noise ratios, and structural instability.
Many foundational questions in finance are frustrated by the "small data" reality of economic time series, and financial research often faces weak signal-to-noise ratios, particularly in return prediction.
Investors learn, and markets evolve, creating a moving target for machine learning prediction models.

### Economic Content

There are two cultures in financial economics: the "structural model/hypothesis test" culture and the "prediction model" culture.
The prediction model culture values statistical explanatory power above all else and is willing to espouse model specifications that may lack an explicit association with economic theory.
Machine learning research in finance has predominantly served the prediction model culture, but it can also be a potent tool for the structural hypothesis testing culture.
Both cultures are economically important, and research can draw on multiple tools to learn about economic mechanisms.

### Introduction

The concept of first-best resource allocation is often hindered by mis-specification and noisy estimation, leading to "third-best" allocations.
Machine learning can help mitigate the gap between first-best and third-best allocations by providing improved predictions.
However, traditional econometric methods, such as the principle of parsimony, may not be suitable for modern machine learning algorithms that use large parameterizations.

### Model Complexity

The complexity of a model, measured by the ratio of parameters to training observations, plays a critical role in determining its performance.
Highly parameterized models can provide better approximations of the true data-generating process, but may also suffer from overfitting.
Regularization techniques, such as ridge regression, can help mitigate overfitting and improve the model's out-of-sample performance.
Research has shown that, in some cases, larger models can lead to better out-of-sample performance, contradicting the traditional principle of parsimony.
The relationship between model complexity and out-of-sample performance is a key theme.
As model complexity increases, the least-squares estimator's denominator blows up, leading to explosive forecast-error variance.
However, when the model is overparameterized, the ridgeless regression estimator can find betas with a smaller 2-norm that still interpolate the training data, acting as a form of shrinkage and biasing the beta estimate toward zero.
This results in a decrease in forecast variance and an improvement in R2.

### Shrinkage And Bias

The tradeoff between shrinkage and bias is another important theme.
As model complexity increases, the mis-specification bias is small, but the shrinkage bias becomes large.
The theory shows that expected returns rise with complexity, suggesting that misspecification bias is more costly than shrinkage bias.
The right amount of shrinkage can turn "double descent" into "permanent ascent", making complexity a virtue even in the low complexity regime.

### Investor Utility

The economic consequences of high complexity models are also a key theme.
As model complexity increases, trading strategy volatility continually decreases, and out-of-sample expected returns increase.
The out-of-sample Sharpe ratio is also increasing in complexity, showing that the performance of machine learning portfolios can be theoretically improved by pushing model parameterization far beyond the number of training observations.
However, the complexity wedge, defined as the expected difference between in-sample and out-of-sample performance, can limit the attainable Sharpe ratios due to the infeasibility of accurately estimating complex statistical relationships.

### Model Definition

The objective is to represent Et[Ri,t+1] as an immutable but otherwise general function g of the P-dimensional predictor variables zi,t available to researchers.
This function should fully explain the heterogeneity in expected returns across all assets and over all time.
The "universality" assumption is ambitious, as it is difficult to imagine that researchers can condition on the same information set as market participants.

### Literature Overview

The literature on machine learning methods for predicting returns in panels of many individual assets is newer, much larger, and continues to grow.
It falls under the rubric of "the cross section of returns" because early studies of single-name stocks sought to explain differences in unconditional average returns across stocks.
The panel aspect of the problem introduces a wealth of phenomena for empirical researchers to explore, document, and attempt to understand in an economic frame.

### Experimental Design

The process of estimating and selecting among many models is central to the definition of machine learning.
Common approaches for model selection are based on information criteria or cross-validation.
Cross-validation has the same goal as AIC and BIC, but approaches the problem in a more data-driven way, comparing models based on their "pseudo" out-of-sample performance.
Cross-validation selects models based on their predictive performance on pseudo-out-of-sample data and has become a widely used approach in the machine learning literature due to its adaptivity and universality.

### Model Selection

The K-fold cross-validation scheme can produce K distinct validation samples, enabling more informed model selection.
This method is particularly useful for serially uncorrelated data.
The recursive cross-validation scheme is another approach, where the training and validation samples are based on observations at 1, ..., t−1, and the selected model is re-estimated using all data through t − 1 to generate an out-of-sample forecast.

### Benchmark Models

The simple linear model is a foundational panel model for stock returns and can serve as a benchmark for machine learning methods.
The linear panel model fixes the prediction function as g(zi,t) = β zi,t, and there are various estimators for this model, including Fama and Macbeth (1973) regression.
Haugen and Baker (1996) and Lewellen (2015) have shown that simple linear panel models can estimate combinations of many predictors that are effective for forecasting returns and building trading strategies.

### Penalized Linear Models

Penalized linear models, such as the elastic net, can be used to constrain the model and avoid overfitting.
The elastic net involves two non-negative hyperparameters, λ and ρ, and includes two well-known regularizers as special cases: ridge regression and the lasso.
Gu et al. (2020b) showed that introducing elastic net penalization can reverse the failure of the OLS estimator in stock-month return prediction panels, leading to positive out-of-sample R2 and improved Sharpe ratios.

### Penalty Functions

Freyberger et al (2020) apply a penalty function known as group lasso, which selects either all K spline terms associated with a given characteristic j, or none of them.
Their results show that less than half of the commonly studied stock signals in the literature have independent predictive power for returns.
They also document the importance of nonlinearities, showing that the full nonlinear specification outperforms the nested linear specification in out-of-sample trading strategy performance.
Chinco et al. (2019) use lasso to study return predictability and find that the dominant predictors vary dramatically from period to period and tend to be returns on stocks reporting fundamental news.

### Dimension Reduction

Dimension reduction plays an important role in asset pricing beyond prediction.
Principal components regression (PCR) and partial least squares (PLS) are two classic dimension reduction techniques.
PCR combines predictors into a few linear combinations, while PLS reduces dimensionality by directly exploiting covariation between predictors and the forecast target.
Ludvigson and Ng (2007) use PCR to forecast market returns and volatility and find that components derived from financial predictors exhibit significant out-of-sample forecasting power.
Kelly and Pruitt (2015) analyze the econometric properties of PLS prediction models and note their resilience when the predictor set contains dominant factors that are irrelevant for prediction.
Dimension reduction techniques such as PLS and PCA are used to combine multiple predictors to forecast a univariate time series.
Huang et al. (2014) show that PLS sentiment indices offer significant predictive benefits relative to PCR.
Chen et al (2022b) combine multiple investor attention proxies into a successful PLS-based market return forecaster.
Ahn and Bae (2022) find that the optimal number of PLS factors for forecasting could be much smaller than the number of common factors in the original predictor variables.

### Prediction Models

Avramov et al (2022b) study how dynamics of firm-level fundamentals associate with subsequent drift in a firm’s stock price, and find that a value-weight decile spread strategy based on their Fundamental Deviation Index earns an annualized out-of-sample information ratio of 0.8 relative to the Fama-French-Carhart four-factor model.
Jurado et al (2015) use PCR to estimate macroeconomic risk and find that improved estimates reveal a tighter link between rises in risk and depressed macroeconomic activity.
Chatelais et al (2023) use a PLS-based framework to forecast macroeconomic activity using a cross-section of asset prices.

### Panel Prediction

To predict the cross-section of returns, dimension reduction is generalized to a panel prediction setting.
Light et al (2017) apply pooled panel PLS in stock return prediction, and Gu et al (2020b) perform pooled panel PCA and PLS to predict individual stock returns.
The resulting portfolios earn a high Sharpe ratio and outperform the elastic-net-based long-short portfolio.

### Decision Trees

Decision trees provide a way to incorporate multi-way predictor interactions at much lower computational cost.
Regression trees partition data observations into groups that share common feature interactions.
The popularity of decision trees stems from the "greedy" algorithms that can effectively isolate highly predictive partitions at low computational cost.
Trees are typically used in regularized "ensembles," such as boosting, to counteract overfitting.

### Tree-Based Methods

Tree-based methods are used for return prediction and portfolio sorting.
The authors show that linear models for the conditional covariance are poorly specified, and this is likely responsible for the mixed results in prior tests of the ICAPM.
Boosted tree methodology reduces misspecification of the conditional covariance function.
Rossi (2018) uses boosted regression trees with macro-finance predictors to directly forecast aggregate stock returns and volatility.
Random forest models are also used for return prediction and portfolio sorting, and they can search more broadly for the most predictive multi-way interactions among stock signals.

### Neural Networks

Neural networks are used for return prediction and are perhaps the most popular and most successful models in machine learning.
They have theoretical underpinnings as “universal approximators” for any smooth predictive function.
Gu et al (2020b) analyze predictions from “feed-forward” networks and estimate monthly stock-level panel prediction models for the CRSP sample from 1957 to 2016.
The results show that neural networks can isolate predictable patterns that persist across business-cycle frequencies.
Neural networks are shown to be effective at predicting stock returns, with Gu et al. (2020b) reporting high out-of-sample R2 and significant trading gains.
The use of neural networks with multiple layers (NN1-NN5) is found to be particularly effective, with the best performing model being NN3.
The models are also found to be profitable when used to trade small stocks, with Avramov et al (2022a) demonstrating that neural network predictions are most successful among difficult-to-value and difficult-to-arbitrage stocks.

### Applications

Tree-based methods and neural networks are used in a range of financial prediction tasks beyond return prediction, including credit risk, liquidity, and volatility prediction.
Correia et al (2018) use a basic classification tree to forecast credit events, and Easley et al (2020) use random forest models to study the high-frequency dynamics of liquidity and risk.
Mittnik et al (2015) use boosted trees to forecast monthly stock market volatility.

### Comparative Analyses

Comparative analyses of machine learning models are conducted in various studies, including Gu et al. (2020b), Choi et al. (2022), and Bali et al. (2020).
These studies find that nonlinear models, particularly neural networks, outperform linear models in terms of predictive R2 and trading strategy performance.
The use of regularization and dimension reduction also improves the performance of linear models.
The studies also demonstrate the viability of transfer learning, with a model trained on US data delivering significant out-of-sample performance when used to forecast international stock returns.

### Advanced Models

Advanced neural network models, such as recurrent neural networks (RNNs) and long short-term memory (LSTM) networks, are also explored.
These models are effective at capturing complex dynamics in sequence data and are particularly useful for time-series prediction problems.
The LSTM model is found to be effective at accommodating long-range dependence and has been used in various studies, including Bali et al. (2020) and He et al. (2021).

### RNNs

Recurrent neural networks (RNNs) have seen limited application in the empirical finance literature, with notable exceptions including Bali et al. (2020) for predicting corporate bond returns and Cong et al. (2020) for monthly stock return prediction.
Guijarro-Ordonez et al (2022) use RNN architectures to predict daily stock returns.
The computer science literature has a more extensive use of neural networks for stock return prediction, but often focuses on high frequencies and small-scale experiments.

### Text Analysis

Textual analysis is a growing field in finance and economics research, with early literature using dictionary-based sentiment scoring methods.
Recent research has developed machine learning models for text-based return prediction, such as Jegadeesh and Wu (2013) and Ke et al (2019), who use a "bag of words" representation of text documents.
However, these representations have limitations, including oversimplification and high dimensionality.
Jiang et al. (2023) use large language models (LLMs) to construct refined news text representations that outperform prevailing text-based machine learning return predictions.

### Image Analysis

Image analysis techniques, such as convolutional neural networks (CNNs), have been introduced to the return prediction problem by Jiang et al (2022).
They represent historical prices as an image and use CNN machinery to search for predictive patterns.
This approach can detect subtle and complex patterns in price data, and has been shown to be effective in predicting returns.
The use of CNNs enables a systematic machine learning approach to elicit return-predictive patterns, rather than testing specific ad hoc hypotheses.

### Convolutional Neural Networks

Convolutional Neural Networks (CNNs) are used to analyze image data in various fields, including finance.
A building block of a CNN model consists of a convolutional layer, a leaky ReLU layer, and a max-pooling layer.
Max pooling acts as both a dimension-reduction device and a denoising tool.
By stacking many of these blocks together, the network creates representations of small image components and gradually assembles them into representations of larger areas.
Jiang et al (2022) train a panel CNN model to predict the direction of future stock returns using daily US stock data from 1993 to 2019.
Glaeser et al. (2018) use a pre-trained CNN to convert images of residential real estate properties into feature vectors for a hedonic house-pricing model.

### Asset Pricing Models

The Arbitrage Pricing Theory (APT) of Ross (1976) lays the groundwork for data-driven, machine learning analysis of factor pricing models.
Unconditional factor models have difficulty describing stock-level data but perform better when modeling portfolios.
Kelly et al. (2020b) demonstrate that factor models estimated from a panel of anomaly portfolios price those portfolios with economically small pricing errors.
The three-pass estimator, proposed by Giglio and Xiu (2021), is used to estimate the risk premium of a non-tradable factor by constructing a factor mimicking portfolio and estimating its expected returns.

### Latent Factor Models

Latent factor models are used to estimate factors and loadings from portfolio-level data.
Principal Component Analysis (PCA) is a common method for estimating latent factors.
However, PCA suffers from indeterminacy, meaning that factors and loadings are identifiable only up to an invertible linear transformation.
Despite this, PCA has been shown to be successful at modeling portfolios and has been used to estimate risk premia and stochastic discount factors.
The three-pass estimator provides a way to make inferences about quantities of interest in asset pricing with latent-factor models, including risk premia and alphas.

### Factor Estimation

Estimates of risk premia using different methods are presented for various non-tradable factors, including AR(1) innovations in industrial production growth, VAR(1) innovations in macro-finance variables, and factors from Novy-Marx (2014).
The two-pass estimates depend on the benchmark factors selected as controls, and omitting these factors can bias the risk-premia estimates.
The three-pass approach addresses both omitted-variable bias and measurement error by estimating latent factors in the first pass, using them as controls in the second-pass cross-sectional regression, and then using another time-series regression in the third pass to remove measurement error.

### PCA Extensions

Alternatives to PCA, such as matrix completion and risk-premia PCA (RP-PCA), are discussed.
RP-PCA applies PCA to an uncentered second moment of returns and can improve the overall performance of PCA estimators by incorporating factor loading information contained in the first moment of returns data.
Instrumented principal components analysis (IPCA) imposes restrictions that link assets' betas to observables, enabling the estimation of conditional latent factor models.

### Factor Selection

The challenge of selecting relevant factors from a large set of candidates is addressed using machine learning methods, such as Lasso regression and a double machine learning framework.
These methods can help identify a parsimonious set of factors that price the cross-section of assets, but selection mistakes are inevitable.
Empirical findings suggest that only a small fraction of candidate factors are useful, while many are redundant or useless.

### IPCA Model

The IPCA model parameterizes betas with characteristics that determine a stock's risk and return, allowing it to track the migration of an asset's identity through its betas.
This eliminates the need to manually group assets into portfolios.
The model accommodates high-dimensional systems of assets without ad hoc portfolio formation and estimates alpha as a linear combination of characteristics that best explain conditional expected returns.

### Complex Factor Models

Complex factor models, such as the conditional autoencoder model, allow for nonlinear associations between expected returns and state variables.
These models can provide more accurate descriptions of assets' conditional compensation for factor risk.
Theoretical results show that adding more factors to an asset pricing model can improve its out-of-sample performance, challenging the traditional APT perspective that a small number of risk factors fully describe the risk-return trade-off.

### High-frequency Models

High-frequency models utilize transaction-level data to estimate risks of individual assets and their interdependencies.
Machine learning techniques can be used to estimate high-dimensional covariances and improve volatility forecasting with high-frequency data.
Accurate covariance estimates are critical to successful portfolio construction, and various methods, such as factor-model-based covariance matrix estimators, can be used to improve estimates.

### Factor Models

Factor models have been developed to handle intraday data, allowing for applications in continuous time.
Fan et al (2016a) and Ait-Sahalia and Xiu (2017) have developed estimators of large covariance matrices using high-frequency data for individual stocks.
Bollerslev et al (2016) have computed individual stock betas with respect to continuous and jump components of a single market factor.
Ait-Sahalia et al (2021) have provided inference for risk premia in a unified continuous-time framework, allowing for multiple factors and stochastic betas.

### Volatility Forecasting

The use of high-frequency data has also led to a promising agenda in volatility forecasting.
The heterogeneous autoregressive (HAR) model has emerged as a leading volatility forecasting model.
Recent papers have examined machine learning strategies for volatility forecasting, including Li and Tang (2022) and Bollerslev et al (2022).
However, it is unclear whether machine learning forecasts outperform existing HAR models in economic terms.

### Alpha Testing

Alpha testing is a key area of research, focusing on distinguishing alpha from "fair" compensation for factor risk exposure.
The GRS test is a well-known test of the null hypothesis that all alphas are equal to zero.
Fan et al (2015) and Pesaran and Yamagata (2017) have proposed tests of the same null in high-dimensional settings.
Da et al. (2022) revisited the APT and relaxed the assumption of known parameters, showing that the feasible Sharpe ratio is below 0.5, suggesting that the APT holds empirically.
Multiple testing is also an important issue in alpha testing, requiring control of the false discovery rate (FDR) to avoid false rejections.

### Multiple Testing

Jensen et al. (2021) propose a Bayesian hierarchical model for multiple testing correction, which allows the factor's alpha estimates to shrink toward the prior and borrow strength from one another.
This approach can lead to less conservative trading strategies than traditional methods, such as FDR control.
Jensen et al. (2021) demonstrate that using a Bayesian hierarchical multiple-testing approach can result in significant improvements over more conservative approaches.

### Portfolio Choice

The portfolio choice problem is a fundamental issue in finance, aiming to efficiently allocate investor resources to maximize growth-optimal savings.
The mean-variance efficient portfolio (MVE) is a tradable representation of the stochastic discount factor (SDF) that summarizes how market participants trade off risk and return to arrive at equilibrium prices.
The MVE portfolio can be used to explain cross-sectional differences in average returns.

### Portfolio Optimization

The portfolio optimization problem is formulated within a machine learning framework that integrates statistical and economic objectives.
The decision-theoretical structure of the problem compels the use of open-minded machine learning specifications.
The portfolio choice problem is formulated as a one-step procedure that integrates utility maximization into the statistical problem of estimating the weight function.
The approach makes no distributional assumptions about returns and specifies the investor's utility and an explicit functional form for the investor's portfolio weight function in terms of observable covariates.

### Machine Learning Methods

Machine learning methods for portfolio choice explicitly incorporate utility optimization when estimating portfolio rules.
The "parametric portfolio weight" approach estimates parameters of the weight function by maximizing average in-sample utility.
The maximum Sharpe ratio regression (MSRR) formulation is attractive for incorporating machine learning methods into parameterized portfolio problems.
MSRR can be extended to incorporate large-K regressions, lasso and elastic-net regression, and other machine learning methods.

### SDF Estimation

The equivalence between portfolio efficiency and other asset pricing restrictions implies that there are statistical objectives to guide optimal portfolio estimation.
The stochastic discount factor (SDF) estimation problem is formulated as a portfolio w of excess returns, and an SDF must satisfy the standard investor Euler equation.
Machine learning approaches to SDF estimation focus on the mean-variance portfolio choice problem, motivated by Hansen and Richard's theorem on the equivalence between the SDF and the mean-variance frontier.
The Britten-Jones (1999) MSRR problem is connected to SDF estimation and Sharpe ratio maximization, resulting in the tangency portfolio as the estimated SDF weights.
Kozak et al. (2020) propose an SDF estimation problem in a conditional, parameterized form, introducing regularization into the conditional SDF estimation.
They analyze ridge regularization, which corresponds to the MSRR ridge estimator, and show that ridge shrinkage is stronger for lower-ranked components.

### Machine Learning SDFs

Chen et al. (2021) extend the SDF estimation problem by modeling stock-specific weights using a flexible weight function that includes a recurrent neural network component.
They formulate their estimator via GMM with a sophisticated instrumental variable scheme, where the instrumental variables are generated adversarially.
Didisheim et al. (2023) theoretically analyze the role of model complexity in shaping the properties of SDF estimators, finding that expected out-of-sample SDF performance strictly improves with increasing SDF model complexity when appropriate shrinkage is employed.

### Non-Tradable SDF Estimation

Chen and Ludvigson (2009) use a feed-forward neural network as a generic approximating model for the habit function in a nonlinear habit consumption utility specification.
They estimate an SDF by minimizing the norm of the model-implied conditional moments of the Euler equation, using macroeconomic data as instruments.
The Hansen-Jagannathan distance is a metric for model comparison that uses a model-independent weighting matrix to aggregate pricing errors.

### HJ-Distance

The HJ-distance is a measure of the worst-case pricing error of a model and describes the least-squares distance between the model's stochastic discount factor (SDF) and the SDF family that correctly prices all assets.
Minimizing the HJ-distance can yield a robust, minimally misspecified model.
The HJ-distance has been linked to SDF estimation approaches with ridge or lasso penalties, and it has been analyzed in the context of model comparison via conditional and unconditional HJ-distance.

### Trading Costs

Trading costs pose a critical challenge for predictive methods in finance, making it difficult to implement portfolio strategies in practice.
The literature on portfolio choice in the face of trading costs typically assumes a known trading cost function, but recent work has introduced machine learning approaches that can learn the optimal portfolio rule while accounting for trading costs.
Jensen et al. (2022) propose a model that combines economic structure with the flexibility of machine learning, allowing for nonlinear prediction functions and stationary yet unrestricted time-series dynamics.

### Reinforcement Learning

Reinforcement learning is a type of machine learning that is well-suited to solving sequential decision-making problems under uncertainty.
While it may be limited in the basic portfolio-choice problem, where the investor is a price taker, it can be valuable for investors with significant price impact, such as financial intermediaries.
The use of reinforcement learning in portfolio choice can help investors learn how their decisions affect market dynamics and optimize their future rewards.
However, there is currently minimal work on reinforcement learning for portfolio choice in the mainstream finance literature.

### Finance

The finance profession has been slow to adopt reinforcement learning, but this is expected to change in the coming years.
The computer science literature has applied reinforcement learning to higher-frequency portfolio problems, such as market-making and trade execution.

### Research

Future research directions for financial machine learning include using machine learning to shed light on economic mechanisms and equilibria, solving sophisticated structural models, and detecting and adapting to structural shifts in economies and markets.
Machine learning is also being applied to other fields, such as corporate finance, entrepreneurship, household finance, and real estate, with examples including analyzing video pitches, earnings calls, and investment decisions.

## Study subjects

### 100 monthly observations

- First, while machine learning is often viewed as a “big data” tool, many foundational questions in finance are frustrated by the decidedly “small data” reality of economic time series. Standard datasets in macrofinance, for example, are confined to a few hundred monthly observations. This kind of data scarcity is unusual in other machine learning domains, where researchers often have, for all intents and purposes, unlimited data (or the ability to generate new data as needed)

### 74 industry indicators

- [^Gu_et+al_2020_b]) estimate monthly stock-level panel prediction models for the CRSP sample from 1957 to 2016. Their raw features include 94 rank-standardized stock characteristics interacted with eight macro-finance time series, as well as 74 industry indicators for a total of 920 features. They infer the trade-offs of network depth in the return forecasting problem by analyzing the performance of networks with one to five hidden layers (denoted NN1 through NN5)

## Data analysis

- #method/matlab
- #method/factor_analysis
- #method/linear_model
- #method/arg_max
- #method/fundamental_deviation_index
- #method/time_series_analysis
- #method/linear_regressions
- #method/nonlinear_models
- #method/continuous_variables
- #method/linear_regression_coefficients

## Findings

- In related work, [^Rossi_2018_a] uses boosted regression trees with macro-finance predictors to directly forecast aggregate stock returns (and volatility) at the monthly frequency, but without imposing the ICAPM’s restriction that predictability enters through conditional variance and covariances with economic state variables. He shows that boosted tree forecasts generate a monthly return prediction R2 of 0.3% per month out-of-sample (compared to −0.7% using a historical mean return forecast), with directional accuracy of 57.3% per month
- The out-of-sample R2 rises to 3.40% when forecasting annual returns rather than monthly, illustrating that the neural networks are also able to isolate predictable patterns that persist over business cycle frequencies
- To accomplish this, however, observable factors rely on vastly more parameters than <a class="keyword" href="#" title="Instrumented principal components analysis">IPCA</a>. In this sample of 11,452 stocks with 37 instruments over 599 months, observable factor models estimate 18 times (≈ 11452/(37 + 599)) as many parameters as <a class="keyword" href="#" title="Instrumented principal components analysis">IPCA</a>! In short, <a class="keyword" href="#" title="Instrumented principal components analysis">IPCA</a> provides a similar description of systematic risk in stock returns as leading observable factors while using almost 95% fewer parameters
- The linear portfolio specification with the same predictors earns an annualized out-of-sample Sharpe ratio of 1.8, while the neural network portfolio achieves a Sharpe ratio of 2.5, or a 40% improvement

## Builds on previous research

- The advent of machine learning allows us to target this functional form ambiguity with a quiver of nonlinear models. In early work, [^Connor_et+al_2012_a] and [^Fan_et+al_2016_b] allow for nonlinear beta specification by treating betas as nonparametric functions of conditioning characteristics (but, unlike IPCA, the characteristics are fixed over time for tractability). [^Kim_et+al_2020_a]) adopt this framework to study the behavior of “arbitrage” portfolios that hedge out factor risk.
- The same literature documents the relative “feature importance” of different return prediction characteristics (e.g., Chen et al, 2021). These findings suggest that the predictive success of machine learning methods is often driven by short-lived characteristics that work well for small and illiquid stocks (e.g., [^Avramov_et+al_2022_a]), suggesting that they might be less important for the real economy (e.g., Van Binsbergen and Opp, 2019).

## Differs from previous work

- We must recognize that investors use information in ways that we as researchers cannot know explicitly and thus cannot exhaustively (and certainly not concisely) specify in a parametric statistical model. Just as [^Cochrane_2009_a] reminds us to be circumspect in our consideration of conditioning information, we must be equally circumspect in our consideration of functional forms.
- Meanwhile, the computer science literature has largely applied reinforcement learning to higher frequency portfolio problems related to market making and trade execution. While we do not cover this literature here, we recommend the survey by [^Hambly_et+al_2022_a] for interested readers.

## Confirmation of earlier findings

- This is a good example of the complementarity between machine learning and economic structure, echoing the argument of [^Israel_et+al_2020_a]. They find that “once we impose the Merton (1974) model structure, equity characteristics provide significant improvement above and beyond bond characteristics for future bond returns, whereas the incremental power of equity characteristics for predicting bond returns is quite limited in the reduced-form approach when such economic structure is not imposed.”
- Proposition 3 of [^Jensen_et+al_2022_a] shows that the optimal portfolio rule in the presence of trading costs is wt ≈ mgtwt−1 + (I − m)At (5.25). These vary over time in predictable ways related to the conditioning variable set st, though for purposes here we discuss the simplified model with static covariances and trading costs. κt is investor assets under management (the scale of the investor’s portfolio is a first-order consideration for trading costs), and gt is wealth growth from the previous period.

## Counterpoint to earlier claims

- They use approximately 1,000 predictors that are multiplicative interactions of roughly 100 stock characteristics with demonstrated forecast power for individual stock returns and 10 aggregate macro-finance predictors with demonstrated success in predicting the market return. Despite these predictors individually showing promise in prior research, [^Gu_et+al_2020_b] show that OLS cannot achieve a stable fit with so many parameters at once, resulting in disastrous out-of-sample performance.

## Contributions

- In summary, these results challenge the dogma of parsimony discussed at the start of this section. They demonstrate that, in the realistic case of mis-specified empirical models, complexity is a virtue. This is true not just in terms of out-of-sample statistical performance (as shown by [^Belkin_et+al_2019_a]; [^Hastie_et+al_2019_a], and others) but also in the economic terms of out-of-sample investor utility. Contrary to conventional wisdom, the performance of machine learning portfolios can be theoretically improved by pushing model parameterization far beyond the number of training observations.

## Limitations

- The limitations of the survey include the scope of the survey, which has forced the authors to limit or omit coverage of some important financial machine learning topics. The survey also notes that the success of machine learning methods is often driven by short-lived characteristics that work well for small, illiquid stocks but may be less important for the real economy.
- The limitations of the research are not discussed in the provided text.

## Future work

- Future work in financial machine learning includes leveraging the flexible model approximations afforded by machine learning to better detect and adapt to structural shifts, and using machine learning methods to solve sophisticated and highly nonlinear structural models. The survey also highlights the potential for machine learning to be applied to corporate finance problems, such as risk modeling and derivatives pricing.
- The text implies that further application of a method to corporate finance problems is an area of future research.

## References

[^Avramov_et+al_2022_a]: Avramov, D., S. Cheng, and L. Metzker. (2022a). “Machine Learning vs. Economic Restrictions: Evidence from Stock Return Predictability”. Management Science, forthcoming.  [OA](https://engine.scholarcy.com/oa_version?query=Avramov%2C%20D.%20Cheng%2C%20S.%20Metzker%2C%20L.%20Machine%20Learning%20vs.%20Economic%20Restrictions%3A%20Evidence%20from%20Stock%20Return%20Predictability%E2%80%9D%202022&author=Avramov&title=Machine%20Learning%20vs.%20Economic%20Restrictions%3A%20Evidence%20from%20Stock%20Return%20Predictability%E2%80%9D&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Avramov%2C%20D.%20Cheng%2C%20S.%20Metzker%2C%20L.%20Machine%20Learning%20vs.%20Economic%20Restrictions%3A%20Evidence%20from%20Stock%20Return%20Predictability%E2%80%9D%202022) [Scite](/scite_tallies?query=author%3AAvramov%2Ctitle%3AMachine%20Learning%20vs.%20Economic%20Restrictions%3A%20Evidence%20from%20Stock%20Return%20Predictability%E2%80%9D%2Cyear%3A2022)

[^Belkin_et+al_2019_a]: Belkin, M., A. Rakhlin, and A. B. Tsybakov. (2019). “Does data interpolation contradict statistical optimality?” In: The 22nd International Conference on Artificial Intelligence and Statistics. PMLR. 1611– 1619.  [OA](https://scholar.google.co.uk/scholar?q=Belkin%2C%20M.%20Rakhlin%2C%20A.%20Tsybakov%2C%20A.B.%20Does%20data%20interpolation%20contradict%20statistical%20optimality%3F%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Belkin%2C%20M.%20Rakhlin%2C%20A.%20Tsybakov%2C%20A.B.%20Does%20data%20interpolation%20contradict%20statistical%20optimality%3F%202019)

[^Breiman_1995_a]: Breiman, L. (1995). “The Mathematics of Generalization”. In: CRC Press. Chap. Reflections After Refereeing Papers for NIPS. 11–15.  [OA](https://scholar.google.co.uk/scholar?q=Breiman%2C%20L.%20The%20Mathematics%20of%20Generalization%E2%80%9D%201995) [GScholar](https://scholar.google.co.uk/scholar?q=Breiman%2C%20L.%20The%20Mathematics%20of%20Generalization%E2%80%9D%201995)

[^Cochrane_2009_a]: Cochrane, J. H. (2009). Asset pricing: Revised edition. Princeton university press.  [OA](https://scholar.google.co.uk/scholar?q=Cochrane%2C%20J.H.%20Asset%20pricing%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Cochrane%2C%20J.H.%20Asset%20pricing%202009)

[^Connor_et+al_2012_a]: Connor, G., M. Hagmann, and O. Linton. (2012). “Efficient semiparametric estimation of the Fama–French model and extensions”. Econometrica. 80(2): 713–754.  [OA](https://engine.scholarcy.com/oa_version?query=Connor%2C%20G.%20Hagmann%2C%20M.%20Linton%2C%20O.%20Efficient%20semiparametric%20estimation%20of%20the%20Fama%E2%80%93French%20model%20and%20extensions%E2%80%9D%202012&author=Connor&title=Efficient%20semiparametric%20estimation%20of%20the%20Fama%E2%80%93French%20model%20and%20extensions%E2%80%9D&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Connor%2C%20G.%20Hagmann%2C%20M.%20Linton%2C%20O.%20Efficient%20semiparametric%20estimation%20of%20the%20Fama%E2%80%93French%20model%20and%20extensions%E2%80%9D%202012) [Scite](/scite_tallies?query=author%3AConnor%2Ctitle%3AEfficient%20semiparametric%20estimation%20of%20the%20Fama%E2%80%93French%20model%20and%20extensions%E2%80%9D%2Cyear%3A2012)

[^Fan_et+al_2016_b]: Fan, J., Y. Liao, and W. Wang. (2016b). “Projected principal component analysis in factor models”. Annals of Statistics. 44(1): 219.  [OA](https://engine.scholarcy.com/oa_version?query=Fan%2C%20J.%20Liao%2C%20Y.%20Wang%2C%20W.%20Projected%20principal%20component%20analysis%20in%20factor%20models%E2%80%9D%202016&author=Fan&title=Projected%20principal%20component%20analysis%20in%20factor%20models%E2%80%9D&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Fan%2C%20J.%20Liao%2C%20Y.%20Wang%2C%20W.%20Projected%20principal%20component%20analysis%20in%20factor%20models%E2%80%9D%202016) [Scite](/scite_tallies?query=author%3AFan%2Ctitle%3AProjected%20principal%20component%20analysis%20in%20factor%20models%E2%80%9D%2Cyear%3A2016)

[^Gu_et+al_2020_b]: Gu, S., B. Kelly, and D. Xiu. (2020b). “Empirical asset pricing via machine learning”. The Review of Financial Studies. 33(5): 2223– 2273.  [OA](https://engine.scholarcy.com/oa_version?query=Gu%2C%20S.%20Kelly%2C%20B.%20Xiu%2C%20D.%20Empirical%20asset%20pricing%20via%20machine%20learning%E2%80%9D%202020&author=Gu&title=Empirical%20asset%20pricing%20via%20machine%20learning%E2%80%9D&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Gu%2C%20S.%20Kelly%2C%20B.%20Xiu%2C%20D.%20Empirical%20asset%20pricing%20via%20machine%20learning%E2%80%9D%202020) [Scite](/scite_tallies?query=author%3AGu%2Ctitle%3AEmpirical%20asset%20pricing%20via%20machine%20learning%E2%80%9D%2Cyear%3A2020)

[^Hambly_et+al_2022_a]: Hambly, B., R. Xu, and H. Yang. (2022). “Recent Advances in Reinforcement Learning in Finance”. Tech. rep. University of Oxford.  [OA](https://scholar.google.co.uk/scholar?q=Hambly%2C%20B.%20Xu%2C%20R.%20Yang%2C%20H.%20Recent%20Advances%20in%20Reinforcement%20Learning%20in%20Finance%E2%80%9D%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Hambly%2C%20B.%20Xu%2C%20R.%20Yang%2C%20H.%20Recent%20Advances%20in%20Reinforcement%20Learning%20in%20Finance%E2%80%9D%202022)

[^Hastie_et+al_2019_a]: Hastie, T., A. Montanari, S. Rosset, and R. J. Tibshirani. (2019). “Surprises in high-dimensional ridgeless least squares interpolation”. arXiv preprint arXiv:1903.08560.  [OA](https://arxiv.org/abs/1903.08560)  

[^Israel_et+al_2020_a]: Israel, R., B. Kellly, and T. J. Moskowitz. (2020). “Can Machines “Learn” Finance?” Journal of Investment Management. 18(2): 23–36.  [OA](https://engine.scholarcy.com/oa_version?query=Israel%2C%20R.%20Kellly%2C%20B.%20Moskowitz%2C%20T.J.%20Can%20Machines%20%E2%80%9CLearn%202020&author=Israel&title=Can%20Machines%20%E2%80%9CLearn&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Israel%2C%20R.%20Kellly%2C%20B.%20Moskowitz%2C%20T.J.%20Can%20Machines%20%E2%80%9CLearn%202020) [Scite](/scite_tallies?query=author%3AIsrael%2Ctitle%3ACan%20Machines%20%E2%80%9CLearn%2Cyear%3A2020)

[^Jensen_et+al_2022_a]: Jensen, T. I., B. Kellly, C. Seminario-Amez, and L. H. Pedersen. (2022). “Machine Learning and the Implementable Efficient Frontier”. Tech. rep. Copenhagen Business School.  [OA](https://engine.scholarcy.com/oa_version?query=Jensen%2C%20T.I.%20Kellly%2C%20B.%20Seminario-Amez%2C%20C.%20Pedersen%2C%20L.H.%20Machine%20Learning%20and%20the%20Implementable%20Efficient%20Frontier%E2%80%9D%202022&author=Jensen&title=Machine%20Learning%20and%20the%20Implementable%20Efficient%20Frontier%E2%80%9D&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Jensen%2C%20T.I.%20Kellly%2C%20B.%20Seminario-Amez%2C%20C.%20Pedersen%2C%20L.H.%20Machine%20Learning%20and%20the%20Implementable%20Efficient%20Frontier%E2%80%9D%202022) [Scite](/scite_tallies?query=author%3AJensen%2Ctitle%3AMachine%20Learning%20and%20the%20Implementable%20Efficient%20Frontier%E2%80%9D%2Cyear%3A2022)

[^Kim_et+al_2020_a]: Kim, S., R. Korajczyk, and A. Neuhierl. (2020). “Arbitrage Portfolios”. Review of Financial Studies, forthcoming.  [OA](https://scholar.google.co.uk/scholar?q=Kim%2C%20S.%20Korajczyk%2C%20R.%20Neuhierl%2C%20A.%20Arbitrage%20Portfolios%E2%80%9D%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Kim%2C%20S.%20Korajczyk%2C%20R.%20Neuhierl%2C%20A.%20Arbitrage%20Portfolios%E2%80%9D%202020)

[^Rossi_2018_a]: Rossi, A. G. (2018). “Predicting stock market returns with machine learning”. Georgetown University.  [OA](https://scholar.google.co.uk/scholar?q=Rossi%2C%20A.G.%20Predicting%20stock%20market%20returns%20with%20machine%20learning%E2%80%9D%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Rossi%2C%20A.G.%20Predicting%20stock%20market%20returns%20with%20machine%20learning%E2%80%9D%202018)
