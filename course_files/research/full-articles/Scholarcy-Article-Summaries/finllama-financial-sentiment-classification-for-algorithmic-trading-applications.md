[[Konstantinidis_et+al_FinllamaFinancialSentimentClassificationAlgorithmic_2024]]

# [FinLlama: Financial Sentiment Classification for Algorithmic Trading Applications](https://arxiv.org/abs/2403.12285v1)

## [[Thanos Konstantinidis]]; [[Giorgos Iacovides]]; [[Mingxue Xu]] et al.

## Abstract
There are multiple sources of financial news online which influence market movements and trader's decisions. This highlights the need for accurate sentiment analysis, in addition to having appropriate algorithmic trading techniques, to arrive at better informed trading decisions. Standard lexicon based sentiment approaches have demonstrated their power in aiding financial decisions. However, they are known to suffer from issues related to context sensitivity and word ordering. Large Language Models (LLMs) can also be used in this context, but they are not finance-specific and tend to require significant computational resources. ==To facilitate a finance specific LLM framework, we introduce a novel approach based on the Llama 2 7B foundational model, in order to benefit from its generative nature and comprehensive language manipulation==. This is achieved by fine-tuning the Llama2 7B model on a small portion of supervised financial sentiment analysis data, so as to jointly handle the complexities of financial lexicon and context, and further equipping it with a neural network based decision mechanism. Such a generator-classifier scheme, referred to as FinLlama, is trained not only to classify the sentiment valence but also quantify its strength, thus offering traders a nuanced insight into financial news articles. Complementing this, the implementation of parameter-efficient fine-tuning through LoRA optimises trainable parameters, thus minimising computational and memory requirements, without sacrificing accuracy. Simulation results demonstrate the ability of the proposed FinLlama to provide a framework for enhanced portfolio management decisions and increased market returns. These results underpin the ability of FinLlama to construct high-return portfolios which exhibit enhanced resilience, even during volatile periods and unpredictable market events.

## Key concepts
#fine_tuning; #algorithmic_trading; #claim/sentiment_analysis; #sentiment_analysis; #large_language_models; #natural_language_processing; #claim/finance; #finance

## Quote
> The FinLlama model is a fine-tuned version of the Llama 2 7B model, specifically designed for financial sentiment analysis, which can provide accurate sentiment classification and quantification of sentiment strength, while minimizing computational resources.

## Key points
- The ultimate goal of FinLlama is to enhance the performance of financial sentiment analysis, whilst leveraging on parameter-efficient fine-tuning (PEFT) and 8-bit quantization, through LoRA [^3], to minimise resource utilisation
- Our work aims to embark upon the immense expressive power and contextual understanding of general-purpose Large Language Models (LLMs) in order to make them finance-specific
- We have introduced an innovative approach to financial sentiment analysis which rests upon the fine-tuning of a general-purpose LLM
- The proposed method has capitalised on the extensive knowledge base and reasoning abilities inherent to LLMs, whilst shifting their primary objective from text generation to classification tasks
- Such an approach has enabled the LLMs to become more attuned to the nuanced language of the finance sector, whilst minimising their resource utilisation and computational demands
- The top 35% of companies in terms of performance were allocated to long positions, while the bottom 35% were allocated to short positions
- Our fine-tuned Llama2 7B model, termed FinLlama, has been used to construct a portfolio, yielding results that have surpassed those of the leading current method in the field, the FinBERT


## Summary

### Introduction
The increasing importance of algorithmic trading in quantitative finance has created a need for reliable AI-aided intelligence from large amounts of data.
Sentiment analysis, which quantifies opinions in textual data, can help bridge the gap between market movements and quantitative trading.
However, extracting sentiment from financial text is challenging due to its nuanced and heterogeneous nature.

### Methodology
The proposed FinLlama model is a fine-tuned version of the Llama 2 7B model, specifically designed for financial sentiment analysis.
The model is trained on a small corpus of financial data and equipped with a neural network-based decision mechanism.
The fine-tuning process utilizes the AdamW optimizer and the LoRA implementation to minimize trainable parameters, making it possible to implement on a single A100 GPU.

### Results
The FinLlama model is evaluated against other sentiment analysis methods using finance-specific real-world metrics.
The results demonstrate the ability of FinLlama to provide a framework for enhanced portfolio management decisions and increased market returns.
The model is able to construct high-return portfolios that exhibit enhanced resilience, even during volatile periods and unpredictable market events.

### Portfolio Construction
The long-short portfolio was constructed using sentiment as a parameter to determine which companies should be in a long or short position.
The sentiment signal obtained from each of the five methods was used to construct five distinct portfolios.
Companies were ranked daily according to their sentiment, with those having the highest positive sentiment placed in long positions and those with the strongest negative sentiment placed in short positions.
An equally-weighted portfolio strategy was used, with 35% of companies in long positions and 35% in short positions.

### Sentiment Analysis
The sentiment analysis was performed using five different methods, including lexicon-based approaches (HIV-4 and VADER) and deep learning approaches (FinBERT and FinLlama).
The FinLlama model, a fine-tuned Llama-2 model, was found to outperform the other methods, achieving significantly higher cumulative returns and a higher Sharpe ratio while exhibiting lower volatility.

### Performance Evaluation
The performance of the portfolios was evaluated using real-world financial metrics, including cumulative returns, annualized return, annualized volatility, and the Sharpe ratio.
The results showed that the FinLlama model outperformed the other methods, with a 44.7% higher cumulative return than the FinBERT model, and a significantly higher Sharpe ratio and lower annualized volatility.


## Study subjects

### 4 labelled financial text datasets
- To tackle these challenges, our work revisits the first principles of LLMs in order to align them to the task of financial sentiment analysis. ==This is achieved by using four labelled financial text datasets as training data to fine-tune the Llama 2 model==. Such training on financial data, equipped the model with the ability to understand the linguistic nuances present in the financial domain

### 34180 labelled samples
- This made it possible to alter the primary function of the model from text generation to sentiment classification. ==Our training data was a combination of four labelled publicly available financial news datasets, resulting in a comprehensive collection of 34,180 labelled samples==. Each sample was annotated with one of the three labels: positive, negative, and neutral

## Data analysis
- #method/finbert_model
- #method/finllama_model
- #method/large_language_models

## Findings
- Through the LoRA implementation, the number of trainable parameters was set to 4.2M, amounting to just 0.0638% of the total number of parameters in the Llama 2 7B model
- The top 35% of companies in terms of performance were allocated to long positions, while the bottom 35% were allocated to short positions

##  Builds on previous research
- where $N$ is the total number of investing days, totaling 1,672, $r_{log}(i)$ is the logarithmic daily return, $\bar{r}$ is the average daily logarithmic return, $R_{f}$ is the annualized risk-free rate of return and 252 is the number of business days in a year. The risk-free return, $R_{f}$, typically represents the yield of the 10-Year Treasury Note; ==however, due to its prolonged low yield [^22] during the analysed period, a 0% rate is commonly used and is adopted in our analysis==.

## Contributions
- Conclusion and Future Work<mark class="claim"><mark class="fact">We have introduced an innovative approach to financial sentiment analysis</mark> <mark class="fact">which rests upon the fine-tuning of a general-purpose LLM</mark></mark>. In this way, <mark class="fact">the proposed method has capitalised on the extensive knowledge base and reasoning abilities</mark> inherent to LLMs, whilst shifting their primary objective from text generation to classification tasks. In addition, such an approach has <mark class="fact">enabled the LLMs to become more attuned to the nuanced language of the finance sector</mark>, whilst minimising their resource utilisation and computational demands.Our fine-tuned Llama2 7B model, termed FinLlama, has been used to construct a portfolio, <mark class="fact">yielding results that have surpassed those of the leading current method in the field</mark>, the FinBERT. The FinLlama has achieved cumulative returns which have outperformed the FinBERT model by 44.7%, while achieving a significantly higher Sharpe ratio and lower annualized volatility. This represents both a substantial contribution to the field of a conjoint framework involving sentiment analysis and LLMs, and demonstrates that fine-tuning an LLM can yield superior results, even with a small amount of task-specific data. In addition, <mark class="fact">the present work has set a new benchmark in the field</mark>, transcending traditional measures such as accuracy and F1-score, commonly used in the literature. Instead, <mark class="claim"><mark class="fact">we focus on practical, finance-specific metrics which have greater relevance to end-users</mark></mark>. <mark class="fact">It is our hope that such an approach is a step towards narrowing down the divide</mark> between academic research and practical applications within quantitative finance.

## Limitations
- The study acknowledges that the FinLlama model is limited by the quality and availability of financial data, as well as the computational resources required for fine-tuning. The study also notes that the model may not perform well in situations where the financial data is noisy or biased.
- The study does not provide a detailed analysis of the limitations of the proposed approach. However, the study mentions that the fine-tuning of a general-purpose LLM requires a small amount of task-specific data.

## Future work
- The study suggests that future work could focus on improving the FinLlama model by incorporating additional financial data sources and fine-tuning the model on larger datasets. The study also notes that the model could be applied to other areas of finance, such as risk management and portfolio optimization.
- The study suggests that future research should aim to enhance both the sentiment classification accuracy and efficiency of the proposed model. The study also suggests that future research should focus on practical, finance-specific metrics, rather than traditional measures such as accuracy and F1-score.


## References
[^1]: K. Mishev, A. Gjorgjevikj, I. Vodenska, L. T. Chitkushev, and D. Trajanov, “Evaluation of sentiment analysis in finance: From lexicons to transformers,” IEEE Access, vol. 8, pp. 131 662–131 682, 07 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%202020&author=Mishev&title=Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Mishev%2C%20K.%20Gjorgjevikj%2C%20A.%20Vodenska%2C%20I.%20Chitkushev%2C%20L.T.%20Evaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%202020) [Scite](/scite_tallies?query=author%3AMishev%2Ctitle%3AEvaluation%20of%20sentiment%20analysis%20in%20finance%3A%20From%20lexicons%20to%20transformers%2Cyear%3A2020)

[^2]: H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale et al., “Llama 2: Open foundation and fine-tuned chat models,” arXiv preprint arXiv:2307.09288, 2023.  [OA](https://arxiv.org/abs/2307.09288)  

[^3]: E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen, “LoRA: Low-rank adaptation of large language models,” arXiv preprint arXiv:2106.09685, 2021.  [OA](https://arxiv.org/abs/2106.09685)  

[^4]: E. F. Fama, “Efficient capital markets: A review of theory and empirical work,” The Journal of Finance, vol. 25, no. 2, pp. 383–417, 1970.  [OA](https://engine.scholarcy.com/oa_version?query=Fama%2C%20E.F.%20Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%201970&author=Fama&title=Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work&year=1970) [GScholar](https://scholar.google.co.uk/scholar?q=Fama%2C%20E.F.%20Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%201970) [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3AEfficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%2Cyear%3A1970)

[^5]: X. Li, H. Xie, L. Chen, J. Wang, and X. Deng, “News impact on stock price return via sentiment analysis,” Knowledge-Based Systems, vol. 69, pp. 14–23, 2014.  [OA](https://engine.scholarcy.com/oa_version?query=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%202014&author=Li&title=News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Li%2C%20X.%20Xie%2C%20H.%20Chen%2C%20L.%20Wang%2C%20J.%20News%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%202014) [Scite](/scite_tallies?query=author%3ALi%2Ctitle%3ANews%20impact%20on%20stock%20price%20return%20via%20sentiment%20analysis%2Cyear%3A2014)

[^6]: Z. T. Ke, B. T. Kelly, and D. Xiu, “Predicting returns with text data,” National Bureau of Economic Research, Tech. Rep., 2019.  [OA](https://engine.scholarcy.com/oa_version?query=Ke%2C%20Z.T.%20Kelly%2C%20B.T.%20Xiu%2C%20D.%20Predicting%20returns%20with%20text%20data%202019&author=Ke&title=Predicting%20returns%20with%20text%20data&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Ke%2C%20Z.T.%20Kelly%2C%20B.T.%20Xiu%2C%20D.%20Predicting%20returns%20with%20text%20data%202019) [Scite](/scite_tallies?query=author%3AKe%2Ctitle%3APredicting%20returns%20with%20text%20data%2Cyear%3A2019)

[^7]: N. Cristianini and J. Shawe-Taylor, An introduction to support vector machines and other kernel-based learning methods. Cambridge University Press, 2000.  [OA](https://scholar.google.co.uk/scholar?q=Cristianini%2C%20N.%20Shawe-Taylor%2C%20J.%20An%20introduction%20to%20support%20vector%20machines%20and%20other%20kernel-based%20learning%20methods%202000) [GScholar](https://scholar.google.co.uk/scholar?q=Cristianini%2C%20N.%20Shawe-Taylor%2C%20J.%20An%20introduction%20to%20support%20vector%20machines%20and%20other%20kernel-based%20learning%20methods%202000) 

[^8]: Z. Yang, D. Yang, C. Dyer, X. He, A. Smola, and E. Hovy, “Hierarchical attention networks for document classification,” 01 2016, pp. 1480–1489.  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20Z.%20Yang%2C%20D.%20Dyer%2C%20C.%20He%2C%20X.%20Hierarchical%20attention%20networks%20for%20document%20classification%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Z.%20Yang%2C%20D.%20Dyer%2C%20C.%20He%2C%20X.%20Hierarchical%20attention%20networks%20for%20document%20classification%202016) 

[^9]: J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” in North American Chapter of the Association for Computational Linguistics, 2019. [Online]. Available: https://api.semanticscholar.org/CorpusID:52967399  [OA](https://api.semanticscholar.org/CorpusID:52967399)  

[^10]: D. Araci, “FinBERT: Financial sentiment analysis with pre-trained language models,” arXiv preprint arXiv:1908.10063, 2019.  [OA](https://arxiv.org/abs/1908.10063)  

[^11]: Z. Chen, S. Gössi, W. Kim, B. Bermeitinger, and S. Handschuh, “FinBERT-FOMC: Fine-tuned FinBERT Model with sentiment focus method for enhancing sentiment analysis of FOMC minutes.” Proceedings of the 4th ACM International Conference on AI in Finance, 2023, pp. 357–364.  [OA](https://scholar.google.co.uk/scholar?q=Chen%2C%20Z.%20G%C3%B6ssi%2C%20S.%20Kim%2C%20W.%20Bermeitinger%2C%20B.%20FinBERT-FOMC%3A%20Fine-tuned%20FinBERT%20Model%20with%20sentiment%20focus%20method%20for%20enhancing%20sentiment%20analysis%20of%20FOMC%20minutes%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%2C%20Z.%20G%C3%B6ssi%2C%20S.%20Kim%2C%20W.%20Bermeitinger%2C%20B.%20FinBERT-FOMC%3A%20Fine-tuned%20FinBERT%20Model%20with%20sentiment%20focus%20method%20for%20enhancing%20sentiment%20analysis%20of%20FOMC%20minutes%202023) 

[^12]: X.-Y. Liu, G. Wang, and D. Zha, “FinGPT: Democratizing internet-scale data for financial large language models,” arXiv preprint arXiv:2307.10485, 2023.  [OA](https://arxiv.org/abs/2307.10485)  

[^13]: H. Yang, X.-Y. Liu, and C. D. Wang, “FinGPT: Open-source financial large language models,” arXiv preprint arXiv:2306.06031, 2023.  [OA](https://arxiv.org/abs/2306.06031)  

[^14]: B. Zhang, H. Yang, and X.-Y. Liu, “Instruct-FinGPT: Financial sentiment analysis by instruction tuning of general-purpose large language models,” ArXiv, vol. abs/2306.12659, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:259224880  [OA](https://api.semanticscholar.org/CorpusID:259224880)  

[^15]: S. Wu, O. Irsoy, S. Lu, V. Dabravolski, M. Dredze, S. Gehrmann, P. Kambadur, D. Rosenberg, and G. Mann, “BloombergGPT: A large language model for finance,” ArXiv, vol. abs/2303.17564, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:257833842  [OA](https://api.semanticscholar.org/CorpusID:257833842)  

[^16]: I. Loshchilov and F. Hutter, “Fixing weight decay regularization in Adam,” ArXiv, vol. abs/1711.05101, 2017. [Online]. Available: https://api.semanticscholar.org/CorpusID:3312944  [OA](https://api.semanticscholar.org/CorpusID:3312944)  

[^17]: T. Loughran and B. Mcdonald, “When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks,” The Journal of Finance, vol. 66, pp. 35 – 65, 02 2011.  [OA](https://engine.scholarcy.com/oa_version?query=Loughran%2C%20T.%20Mcdonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%20Textual%20analysis%2C%20dictionaries%2C%20and%2010-Ks%202011&author=Loughran&title=When%20is%20a%20liability%20not%20a%20liability%3F%20Textual%20analysis%2C%20dictionaries%2C%20and%2010-Ks&year=2011) [GScholar](https://scholar.google.co.uk/scholar?q=Loughran%2C%20T.%20Mcdonald%2C%20B.%20When%20is%20a%20liability%20not%20a%20liability%3F%20Textual%20analysis%2C%20dictionaries%2C%20and%2010-Ks%202011) [Scite](/scite_tallies?query=author%3ALoughran%2Ctitle%3AWhen%20is%20a%20liability%20not%20a%20liability%3F%20Textual%20analysis%2C%20dictionaries%2C%20and%2010-Ks%2Cyear%3A2011)

[^18]: P. J. Stone, D. C. Dunphy, M. S. Smith, and D. M. Ogilvie, The General Inquirer: A Computer Approach to Content Analysis. MIT Press, 1966.  [OA](https://scholar.google.co.uk/scholar?q=Stone%2C%20P.J.%20Dunphy%2C%20D.C.%20Smith%2C%20M.S.%20Ogilvie%2C%20D.M.%20The%20General%20Inquirer%3A%20A%20Computer%20Approach%20to%20Content%20Analysis%201966) [GScholar](https://scholar.google.co.uk/scholar?q=Stone%2C%20P.J.%20Dunphy%2C%20D.C.%20Smith%2C%20M.S.%20Ogilvie%2C%20D.M.%20The%20General%20Inquirer%3A%20A%20Computer%20Approach%20to%20Content%20Analysis%201966) 

[^19]: C. Hutto and E. Gilbert, “VADER: A parsimonious rule-based model for sentiment analysis of social media text,” vol. 08, no. 01. Proceedings of the 8th International Conference on Weblogs and Social Media, ICWSM 2014, 2015, pp. 216–225.  [OA](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20Gilbert%2C%20E.%20VADER%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20social%20media%20text%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Hutto%2C%20C.%20Gilbert%2C%20E.%20VADER%3A%20A%20parsimonious%20rule-based%20model%20for%20sentiment%20analysis%20of%20social%20media%20text%202015) 

[^20]: Z. T. Ke, B. T. Kelly, and D. Xiu, “Predicting returns with text data,” National Bureau of Economic Research, Inc, NBER Working Papers 26186, 2019. [Online]. Available: https://EconPapers.repec.org/RePEc:nbr:nberwo:26186  [OA](https://EconPapers.repec.org/RePEc:nbr:nberwo:26186)  

[^21]: J. B. Berk and P. M. DeMarzo, “Corporate finance,” vol. 5, 2019.  [OA](https://scholar.google.co.uk/scholar?q=Berk%2C%20J.B.%20DeMarzo%2C%20P.M.%20Corporate%20finance%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Berk%2C%20J.B.%20DeMarzo%2C%20P.M.%20Corporate%20finance%202019) 

[^22]: Yahoo Finance, “Treasury yield 10 years historical data.” 2023. [Online]. Available: https://finance.yahoo.com/quote/%5ETNX/history   [OA](https://finance.yahoo.com/quote/%5ETNX/history)  

