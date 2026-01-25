[[Pankwaen_et+al_GlobalCrossmarketTradingOptimizationUsing_2025]]

# [Global Cross-Market Trading Optimization Using Iterative Combined Algorithm: A Multi-Asset Approach with Stocks and Cryptocurrencies](https://doi.org/10.3390/math13081317)

## [[Kansuda Pankwaen]]; [[Sukrit Thongkairat]]; [[Worrawat Saijai]]

## Abstract

This study presents an advanced adaptive trading framework that integrates Deep Reinforcement Learning (DRL) with the Iterative Model Combining Algorithm (IMCA) to overcome the critical limitations of static ensemble methods in global portfolio optimization. Using a diverse cross-market dataset of 39 stocks from the US, Australia, Europe, Thailand, and one cryptocurrency (BTC-USD), the research rigorously evaluates models’ adaptability under volatile market conditions. Volatile market conditions—such as COVID-19, the SVB crisis, and the 2022 crypto crash—are captured via volatility metrics (e.g., drawdowns), with DRL models like PPO/TD3 adapting to dynamic reward signals. This cross-asset integration is particularly critical, as it captures the complex dynamics and correlations between traditional financial markets and emerging digital assets. Although DRL models like PPO and TD3 outperform traditional strategies, they remain vulnerable to market drawdowns and high volatility. IMCA significantly surpasses these models, achieving the highest cumulative return of 29.52% and a superior Sharpe ratio of 0.829 by dynamically recalibrating model weights in response to real-time market dynamics. This study addresses a substantial research gap by highlighting the failure of traditional ensemble models—reliant on static weightings—to adapt to evolving financial conditions, leading to suboptimal risk-adjusted returns. IMCA offers a dynamic, data-driven approach that continuously optimizes portfolio strategies across fluctuating market regimes, demonstrating its scalability and robustness across diverse asset classes and regional markets, and providing an empirical framework for adaptive portfolio management. Policy recommendations underscore the need for financial institutions to adopt AI-driven adaptive models, such as IMCA, to enhance portfolio resilience, profitability, and responsiveness in uncertain markets.

## Key concepts

# claim/reinforcement_learning; #reinforcement_learning; #claim/IMCA; #IMCA; #claim/deep_reinforcement_learning; #deep_reinforcement_learning; #capital_asset_pricing_model

## Quote
>
> This study evaluates the effectiveness of Deep Reinforcement Learning (DRL) algorithms and an Integrated Model with Continuous Adaptation (IMCA) in optimizing trading strategies across multiple global financial markets, with IMCA outperforming other models in volatile markets.

## Key points

- Automated trading systems have revolutionized financial markets by enabling rapid, data-driven decision-making with unparalleled speed, accuracy, and consistency
- The Iterative Model Combining Algorithm (IMCA) framework demonstrates enhanced scalability across various asset classes and regional markets by dynamically adjusting model selection based on real-time financial conditions, positioning it as a robust solution for institutional and retail investors managing globally diversified portfolios
- While policy optimization (PPO) and TD3 emerge as top-performing Deep Reinforcement Learning (DRL) algorithms, the IMCA framework surpasses both by dynamically recalibrating model weights to align with evolving market conditions, thereby achieving superior cumulative returns and risk-adjusted performance
- Unlike individual models that rely on fixed parameters and training environments, IMCA dynamically adjusts model selection based on real-time market conditions
- The results show that IMCA achieves an annual return of 6.80 percent and a cumulative return of 29.5 percent, surpassing traditional strategies while maintaining competitive risk-adjusted returns
- IMCA’s adaptive nature ensures that it remains effective across multiple market regimes, allowing it to be deployed in various financial environments ranging from high-frequency trading to long-term portfolio management

## Summary

### Snapshot

This study evaluates the effectiveness of Deep Reinforcement Learning (DRL) algorithms and an Integrated Model with Continuous Adaptation (IMCA) in optimizing trading strategies across multiple global financial markets, with IMCA outperforming other models in volatile markets.

### Key findings

The study finds that IMCA significantly surpasses other models, achieving the highest cumulative return of 29.52% and a superior Sharpe ratio of 0.829 by dynamically recalibrating model weights in response to real-time market dynamics.
The key findings of the study include IMCA's outperformance in volatile markets, the adaptability of DRL models in managing portfolio allocations, and the importance of adaptive trading frameworks for cross-market portfolio management.
Unlike individual models that rely on fixed parameters and training environments, IMCA dynamically adjusts model selection based on real-time market conditions
The results show that IMCA achieves an annual return of 6.80 percent and a cumulative return of 29.5 percent, surpassing traditional strategies while maintaining competitive risk-adjusted returns
IMCA’s adaptive nature ensures that it remains effective across multiple market regimes, allowing it to be deployed in various financial environments ranging from high-frequency trading to long-term portfolio management

### Objectives

The primary objective of the study is to evaluate the effectiveness of Reinforcement Learning-based trading strategies across diverse global markets, encompassing equities and cryptocurrencies, while assessing their adaptability to fluctuating financial conditions.

### Methods

The study employs six Deep Reinforcement Learning (DRL) algorithms—A2C, PPO, DDPG, TD3, SAC, and IMCA—selected for their strengths in balancing risk-reward tradeoffs, processing high-dimensional data, and adapting to volatile market conditions.
The study employs a cross-market approach, adopting DRL models and the IMCA framework to optimize multi-asset portfolio allocations, and assesses their performance using key metrics such as cumulative returns, Sharpe ratios, and maximum drawdowns.

### Results

The results show that DRL-based algorithms are highly adaptable and efficient in managing portfolio allocations, offering competitive returns with optimal risk. IMCA achieves an annual return of 6.80 percent and a cumulative return of 29.5 percent, surpassing traditional strategies while maintaining competitive risk-adjusted returns.
The results show that DRL models consistently outperform traditional portfolio optimization techniques, with IMCA achieving the highest cumulative return of 29.5 percent and the best Sharpe ratio of 0.829.

### Conclusions

The study concludes that IMCA offers a dynamic, data-driven approach that continuously optimizes portfolio strategies across fluctuating market regimes, demonstrating its scalability and robustness across diverse asset classes and regional markets.
The study concludes that IMCA is a robust solution for institutional and retail investors managing globally diversified portfolios, and that adaptive trading frameworks are critical in responding to macroeconomic shocks and navigating dynamic markets.

## Study subjects

### 64 observations

- Episodes: 1000 episodes were used to ensure the models achieve convergence while capturing diverse trading patterns. Batch Size: 64 observations per batch, balancing computational efficiency with stable gradient updates. Discount Factor (γ): Set at 0.99 to prioritize long-term rewards while ensuring short-term fluctuations do not overly influence decisions

## Data analysis

- #method/capm_model
- #method/reinforcement_learning_models
- #method/imca_model

## Findings

- Specific periods include the Eurozone Sovereign Debt Crisis (2010–2012) [^68], the COVID-19 pandemic crash in 2020 [^69], the major cryptocurrency crash in 2022 marked by Bitcoin’s drawdown of over 60% from its peak [^70], and the 2023 banking crisis involving <a class="keyword" href="#" title="Silicon Valley Bank">SVB</a> and Credit Suisse [^71]

## Differs from previous work

- The cross-market comparison of DRL and IMCA underscores their ability to generate consistently higher returns while maintaining a risk profile comparable to traditional investment strategies. However, the analysis also reveals that DRL models remain vulnerable to high volatility and periods of extreme market stress, with annual volatility exceeding that of traditional approaches [^6].

## Confirmation of earlier findings

- This establishes IMCA as a more resilient and scalable framework for multi-asset, cross-market portfolio allocation. Second, the analysis confirms that DRL models systematically outperform traditional investment strategies, reinforcing previous findings that demonstrated the superior riskadjusted returns of DRL-based trading systems [^3],[^5].

## Contributions

- <mark class="fact">This study conducted a comprehensive analysis of the performance of various DRL models</mark>, including DDPG, PPO, TD3, SAC, and A2C, along with the IMCA. <mark class="fact">The primary objective was to evaluate the effectiveness of Reinforcement Learning-based trading strategies across diverse global markets</mark>, encompassing equities and cryptocurrency assets, while assessing their adaptability under fluctuating financial conditions. By adopting a cross-market approach, <mark class="fact">the research underscores the capacity of DRL models to optimize multi-asset portfolio allocations</mark>, offering a data-driven alternative to conventional strategies. Moreover, the IMCA framework demonstrates enhanced scalability across various asset classes and <mark class="fact">regional markets by dynamically adjusting model selection based on real-time financial conditions</mark>, positioning it as a robust solution for institutional and retail investors managing globally diversified portfolios.

## Limitations

- The study notes that IMCA relies on historical data and Reinforcement Learning algorithms, which present the risk of overfitting in non-stationary market conditions. The study also notes that transaction costs and liquidity risks are not explicitly modeled.
- The study acknowledges several limitations, including the reliance on historical data, the risk of overfitting, and the need for more robust generalization techniques to ensure model effectiveness across unseen financial environments.

## Future work

- The study suggests that future research could focus on developing Reinforcement Learning frameworks that dynamically adjust across different financial environments to further enhance portfolio stability. The study also notes that risk management remains a fundamental concern for Reinforcement Learning-based models in periods of market stress.
- Future research should focus on refining risk-control mechanisms, integrating macroeconomic indicators, and improving execution efficiency to enhance portfolio stability and mitigate sudden portfolio losses.

## References

[^3]: Jiang, Z.; Xu, D.; Liang, J. A Deep Reinforcement Learning framework for the financial portfolio management problem. arXiv 2017, arXiv:1706.10059.  [OA](https://arxiv.org/abs/1706.10059)  

[^5]: Lu, C.I. Evaluation of Deep Reinforcement Learning Algorithms for Portfolio Optimization. arXiv 2023, arXiv:2307.07694.  [OA](https://arxiv.org/abs/2307.07694)  

[^6]: Vishal, M.; Vadlamani, R.; Ramanuj, L. Ensemble Deep Reinforcement Learning for Financial Trading. In Machine Learning Approaches in Financial Analytics; Maglaras, L.A., Das, S., Tripathy, N., Patnaik, S., Eds.; Springer Nature: Cham, Switzerland, 2024; pp. 191–207. [CrossRef]  [OA](https://scholar.google.co.uk/scholar?q=Vishal%2C%20M.%20Vadlamani%2C%20R.%20Ramanuj%2C%20L.%20Ensemble%20Deep%20Reinforcement%20Learning%20for%20Financial%20Trading%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Vishal%2C%20M.%20Vadlamani%2C%20R.%20Ramanuj%2C%20L.%20Ensemble%20Deep%20Reinforcement%20Learning%20for%20Financial%20Trading%202024)

[^68]: Lane, P. The European Sovereign Debt Crisis. J. Econ. Perspect. 2012, 26, 49–67. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Lane%2C%20P.%20The%20European%20Sovereign%20Debt%20Crisis%202012&author=Lane&title=The%20European%20Sovereign%20Debt%20Crisis&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Lane%2C%20P.%20The%20European%20Sovereign%20Debt%20Crisis%202012) [Scite](/scite_tallies?query=author%3ALane%2Ctitle%3AThe%20European%20Sovereign%20Debt%20Crisis%2Cyear%3A2012)

[^69]: Baker, S.R.; Bloom, N.; Davis, S.J.; Kost, K.; Sammon, M.; Viratyosin, T. The Unprecedented Stock Market Reaction to COVID-19. Rev. Asset Pricing Stud. 2020, 10, 742–758. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Baker%2C%20S.R.%20Bloom%2C%20N.%20Davis%2C%20S.J.%20Kost%2C%20K.%20The%20Unprecedented%20Stock%20Market%20Reaction%20to%20COVID-19%202020&author=Baker&title=The%20Unprecedented%20Stock%20Market%20Reaction%20to%20COVID-19&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Baker%2C%20S.R.%20Bloom%2C%20N.%20Davis%2C%20S.J.%20Kost%2C%20K.%20The%20Unprecedented%20Stock%20Market%20Reaction%20to%20COVID-19%202020) [Scite](/scite_tallies?query=author%3ABaker%2Ctitle%3AThe%20Unprecedented%20Stock%20Market%20Reaction%20to%20COVID-19%2Cyear%3A2020)

[^70]: Arner, D.W.; Zetzsche, D.A.; Buckley, R.P.; Kirkwood, J. The Financialization of Crypto: Lessons from FTX and the Crypto Winter of 2022–2023; No. 2023/19; UNSW Law Res. Pap.; No. 23-31; University of Hong Kong Faculty of Law Research Paper: Hong Kong, China, 2023. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Arner%20DW%20Zetzsche%20DA%20Buckley%20RP%20Kirkwood%20J%20The%20Financialization%20of%20Crypto%20Lessons%20from%20FTX%20and%20the%20Crypto%20Winter%20of%2020222023%20No%20202319%20UNSW%20Law%20Res%20Pap%20No%202331%20University%20of%20Hong%20Kong%20Faculty%20of%20Law%20Research%20Paper%20Hong%20Kong%20China%202023%20CrossRef&author=Arner&title=The%20Financialization%20of%20Crypto%3A%20Lessons%20from%20FTX%20and%20the%20Crypto%20Winter%20of%202022%E2%80%932023%3B%20No.%202023/19%3B%20UNSW%20Law%20Res&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Arner%20DW%20Zetzsche%20DA%20Buckley%20RP%20Kirkwood%20J%20The%20Financialization%20of%20Crypto%20Lessons%20from%20FTX%20and%20the%20Crypto%20Winter%20of%2020222023%20No%20202319%20UNSW%20Law%20Res%20Pap%20No%202331%20University%20of%20Hong%20Kong%20Faculty%20of%20Law%20Research%20Paper%20Hong%20Kong%20China%202023%20CrossRef) [Scite](/scite_tallies?query=author%3AArner%2Ctitle%3AThe%20Financialization%20of%20Crypto%3A%20Lessons%20from%20FTX%20and%20the%20Crypto%20Winter%20of%202022%E2%80%932023%3B%20No.%202023/19%3B%20UNSW%20Law%20Res%2Cyear%3A2023)

[^71]: Aharon, D.Y.; Ali, S.; Naved, M. Too Big to Fail: The Aftermath of Silicon Valley Bank (SVB) Collapse and Its Impact on Financial Markets. Res. Int. Bus. Financ. 2023, 66, 102036. [CrossRef]  [OA](https://engine.scholarcy.com/oa_version?query=Aharon%2C%20D.Y.%20Ali%2C%20S.%20Naved%2C%20M.%20Too%20Big%20to%20Fail%3A%20The%20Aftermath%20of%20Silicon%20Valley%20Bank%20%28SVB%29%20Collapse%20and%20Its%20Impact%20on%20Financial%20Markets%202023&author=Aharon&title=Too%20Big%20to%20Fail%3A%20The%20Aftermath%20of%20Silicon%20Valley%20Bank%20%28SVB%29%20Collapse%20and%20Its%20Impact%20on%20Financial%20Markets&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Aharon%2C%20D.Y.%20Ali%2C%20S.%20Naved%2C%20M.%20Too%20Big%20to%20Fail%3A%20The%20Aftermath%20of%20Silicon%20Valley%20Bank%20%28SVB%29%20Collapse%20and%20Its%20Impact%20on%20Financial%20Markets%202023) [Scite](/scite_tallies?query=author%3AAharon%2Ctitle%3AToo%20Big%20to%20Fail%3A%20The%20Aftermath%20of%20Silicon%20Valley%20Bank%20%28SVB%29%20Collapse%20and%20Its%20Impact%20on%20Financial%20Markets%2Cyear%3A2023)
