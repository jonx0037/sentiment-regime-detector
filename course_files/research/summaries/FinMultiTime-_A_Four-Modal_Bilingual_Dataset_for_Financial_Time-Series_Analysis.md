[[Xu_et+al_FinmultitimeFourmodalBilingualDatasetFinancial_2025]]

# [FinMultiTime: A Four-Modal Bilingual Dataset for Financial Time-Series Analysis](https://arxiv.org/abs/2506.05019v1)

## [[Wenyan Xu]]; [[Dawei Xiang]]; [[Yue Liu]] et al.

## Abstract
Pure time-series forecasting tasks typically focus exclusively on numerical features; however, real-world financial decision-making requires comparing and analyzing heterogeneous sources of information. Recent advances in deep learning and large language models (LLMs) have significantly improved their ability to capture sentiment and other qualitative signals, thereby enhancing the accuracy of financial time-series predictions. Despite these advances, most existing datasets consist solely of price series and news text, are confined to a single market, and remain limited in scale. In this paper, we introduce FinMultiTime, the first large-scale, multimodal financial time series dataset. FinMultiTime temporally aligns four distinct modalities: financial news, structured financial tables, K-line technical charts, and stock price time series across both the S&amp;P 500 and HS 300 universes. Covering 5,105 stocks from 2009 to 2025 in the United States and China, the dataset totals 112.6 GB and provides minute-level, daily, and quarterly resolutions, capturing short-, medium-, and long-term market signals with high fidelity. Our experiments demonstrate that (1) scale and data quality markedly boost prediction accuracy; (2) multimodal fusion yields moderate gains in Transformer models; and (3) a fully reproducible pipeline enables seamless dataset updates.

## Key concepts
#deep_learning; #real_world; #natural_language_processing; #stock_price; #large_language_model; #financial_news

## Quote
> FinMultiTime is a large-scale, multimodal financial time-series dataset that aligns four distinct modalities—financial news, structured financial tables, K-line technical charts, and stock price time series—across both the S&amp;P 500 and HS 300 universes, covering 5,105 stocks from 2009 to 2025.

## Key points
- The natural language processing (NLP) models enable sentiment analysis of financial news, event extraction from disclosures, table parsing in earnings reports, and automated chart summarization souma2019enhanced; araci2019finbert ; Yang2018dcfee; chapman2022towards ; la2020end
- We introduce FinMultiTime, a bilingual, large-scale dataset
- Lower-quality modalities can introduce variance and drag down accuracy. These results confirm FinMultiTime’s effectiveness and robustness for financial modeling and sentiment analysis: larger, multimodal training sets yield substantial gains, while small datasets are inherently limited
- Based on the results of the FNSPID experiments, we derive three primary conclusions that contribute to the understanding of stock-price forecasting using deep learning techniques


## Summary

### Dataset
FinMultiTime is a large-scale, multimodal financial time-series dataset that temporally aligns four distinct modalities: financial news, structured financial tables, K-line technical charts, and stock price time series.
The dataset covers 5,105 stocks from 2009 to 2025 in the United States and China, totaling 112.6 GB of minute-level, daily, and quarterly resolution data.

### Construction
The construction of FinMultiTime involves the systematic acquisition and processing of multi-source information.
The dataset is assembled from various sources, including Yahoo Finance API, Nasdaq news scraping, SEC Submissions and Company Facts APIs, and Tushare API.
The data is then preprocessed to extract and align the four modalities, including technical chart images, structured financial tables, normalized price series, and news text.

### Properties And Evaluation
FinMultiTime has a comprehensive, heterogeneous structure, with over 112.6 GB of data.
The dataset is multilingual, including Chinese and English news articles, tabular records, and charts.
The temporal distribution of the data reveals evolving trends and patterns, offering valuable insights into the historical progression of financial news coverage.
The industry distribution of the dataset shows that HS300 stocks are concentrated in finely segmented sub-sectors, whereas S&amp;P 500 constituents are dominated by large sectors.
The dataset is evaluated using quantitative and qualitative tests, demonstrating its effectiveness for stock price forecasting and sentiment analysis.

### Dataset And Model Performance
The study examines the impact of dataset scale on model performance in predicting short-term price movements.
Six deep learning architectures are compared, including Traditional sequence models (RNN, LSTM, GRU, and 1D CNN) and recent time-series methods (4-layer Vanilla Transformer and 4-layer TimesNet).
The results show that the Transformer model achieves the highest accuracy, with an average $R^{2}\approx 0.97$ at 35 stocks, followed by LSTM and GRU.
The performance of basic sequence models is limited by signal amplification in weak learners.

### Sentiment Analysis And Multimodal Inputs
The study also investigates the effectiveness of sentiment analysis and multimodal inputs in enhancing model performance.
The results show that only Transformer and LSTM models consistently benefit from adding sentiment, trend, or fundamental inputs.
The integration of high-quality multimodal inputs, such as combining textual news data, numerical stock indicators, and technical signals, substantially enhances the performance of Transformer-based architectures.

### Limitations And Future Work
The study discusses the limitations of the work, including the possibility that hyperparameter tuning could affect the results and the modest gains from adding sentiment and trend inputs.
The authors also outline future directions, including expanding the FinMultiTime dataset, unlocking its full potential through multimodal modeling, and exploring pre-training language models within a reinforcement-learning framework to improve multimodal feature extraction and its downstream applications.

### Reproducibility
The paper provides sufficient information to reproduce the main experimental results, including details on the experiments, training, and test settings, as well as the statistical significance of the results.
The authors have released the code and documentation on GitHub, along with instructions for reproducing the results.
The paper also specifies all the training details, including data splits, hyperparameters, and the type of optimizer.

### Ethics And Transparency
The research conducted in the paper conforms to the NeurIPS Code of Ethics, and the authors have reviewed and confirmed compliance with all its guidelines.
The paper discusses potential future work but does not address societal impact.
The authors have properly credited all third-party assets used in the paper, including code, datasets, and pretrained models, by citing the original sources and mentioning the license and terms of use.

### Experimental Setup
The paper provides sufficient information on the computer resources needed to reproduce the experiments, including the types of compute workers, memory, and execution time.
The experimental environment is presented, and the authors have provided scripts to reproduce all experimental results for the new proposed method and baselines.
The paper reports error bars suitably and correctly defined, providing information about the statistical significance of the experiments.

### Data
The paper should provide documentation for new assets, including details about training, license, and limitations.
For existing datasets that are re-packaged, both the original license and the license of the derived asset should be provided.
Researchers should include details of the dataset/code/model as part of their submissions using structured templates.

### Human Subjects
The paper should discuss whether and how consent was obtained from people whose asset is used.
For crowdsourcing experiments and research involving human subjects, the paper should include the full text of the instructions provided to participants, screenshots (if applicable), and details about compensation.
Institutional review board (IRB) approvals or equivalent for research with human subjects should be obtained and clearly stated in the paper.

### Methods
The paper should describe the usage of Large Language Models (LLMs) if they are an important, original, or non-standard component of the core methods in this research.
The core method development in this research does not involve LLMs as any important, original, or non-standard components; therefore, a declaration is not required.


## Study subjects

### 500 companies
- Structured financial tables are obtained primarily via the SEC Submissions and Company Facts APIs 333https://www.sec.gov/search-filings/edgar-application-programming-interfaces. From 10-K and 10-Q filings of S&amp;P 500 companies since 2000, we automatically extract key indicators from XBRL facts in balance sheets, cash flow statements, and statements of shareholders’ equity, while removing irrelevant fields such as announcement dates and filing types. For details on the retrieved tabular data, see Table LABEL:table: Financial_Tables_Comparison

### 500 datasets
- Different models learn different patterns, leading to varied prediction accuracy. We trained on bilingual HS300/S&amp;P 500 datasets of three sizes (5, 15, and 35 stocks) to study how dataset scale affects model performance. We compared six deep-learning architectures:

## Findings
- <mark class="claim">As the training set grew from 5 to 35 stocks, <mark class="fact">we found that Transformer achieved the highest accuracy</mark> (average $R^{2}\approx 0.97$ at 35 stocks); LSTM ranked second ($R^{2}\approx 0.84$); GRU ranked third ($R^{2}\approx 0.83$); TimesNet performed worst ($R^{2}\approx 0.31$)</mark>

## Contributions
- In summary, Figures 3 and 3 illustrate the five-level sentiment rubric, while Figure 4 shows that the resulting score distributions are approximately Gaussian. Mild asymmetry is observable: S&P 500 scores lean left (a slight negative bias), whereas HS 300 scores lean right (neutral-to-positive skew), consistent with a gentle U.S. pullback versus a protracted Chinese rally during the sampling window and with editorial tone differences across English and Chinese outlets.

## Limitations
- The study notes that the performance of the models can be affected by hyperparameter tuning. The study also notes that sentiment analysis can be limited by the quality of sentiment labels.

## Future work
- The study suggests that future work could involve expanding the dataset to include more stocks and more types of data. The study also suggests that future work could involve using more advanced techniques, such as reinforcement learning.
- The future work of the paper is to continue promoting transparency, reproducibility, and ethics in research, and to develop new methodologies and guidelines for authors to follow.
- There is no explicit mention of future work in the paper, but it is implied that the authors may continue to develop and refine their research methods and submissions.


## References
[^1]: Dogu Araci. Finbert: Financial sentiment analysis with pre-trained language models. arXiv preprint arXiv:1908.10063, 2019.  [OA](https://arxiv.org/abs/1908.10063)  

[^2]: Adebiyi A Ariyo, Adewumi O Adewumi, and Charles K Ayo. Stock price prediction using the arima model. In 2014 UKSim-AMSS 16th international conference on computer modelling and simulation, pages 106–112. IEEE, 2014.  [OA](https://scholar.google.co.uk/scholar?q=Ariyo%2C%20Adebiyi%20A.%20Adewumi%2C%20Adewumi%20O.%20Ayo%2C%20Charles%20K.%20Stock%20price%20prediction%20using%20the%20arima%20model%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Ariyo%2C%20Adebiyi%20A.%20Adewumi%2C%20Adewumi%20O.%20Ayo%2C%20Charles%20K.%20Stock%20price%20prediction%20using%20the%20arima%20model%202014) 

[^3]: Luc Bauwens, Sébastien Laurent, and Jeroen VK Rombouts. Multivariate garch models: a survey. Journal of applied econometrics, 21(1):79–109, 2006.  [OA](https://engine.scholarcy.com/oa_version?query=Bauwens%2C%20Luc%20Laurent%2C%20S%C3%A9bastien%20Rombouts%2C%20Jeroen%20V.K.%20Multivariate%20garch%20models%3A%20a%20survey%202006&author=Bauwens&title=Multivariate%20garch%20models%3A%20a%20survey&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Bauwens%2C%20Luc%20Laurent%2C%20S%C3%A9bastien%20Rombouts%2C%20Jeroen%20V.K.%20Multivariate%20garch%20models%3A%20a%20survey%202006) [Scite](/scite_tallies?query=author%3ABauwens%2Ctitle%3AMultivariate%20garch%20models%3A%20a%20survey%2Cyear%3A2006)

[^4]: Lei Chai, Hongfeng Xu, Zhiming Luo, and Shaozi Li. A multi-source heterogeneous data analytic method for future price fluctuation prediction. Neurocomputing, 418:11–20, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Chai%2C%20Lei%20Xu%2C%20Hongfeng%20Luo%2C%20Zhiming%20Li%2C%20Shaozi%20A%20multi-source%20heterogeneous%20data%20analytic%20method%20for%20future%20price%20fluctuation%20prediction%202020&author=Chai&title=A%20multi-source%20heterogeneous%20data%20analytic%20method%20for%20future%20price%20fluctuation%20prediction&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Chai%2C%20Lei%20Xu%2C%20Hongfeng%20Luo%2C%20Zhiming%20Li%2C%20Shaozi%20A%20multi-source%20heterogeneous%20data%20analytic%20method%20for%20future%20price%20fluctuation%20prediction%202020) [Scite](/scite_tallies?query=author%3AChai%2Ctitle%3AA%20multi-source%20heterogeneous%20data%20analytic%20method%20for%20future%20price%20fluctuation%20prediction%2Cyear%3A2020)

[^5]: Clayton Leroy Chapman, Lars Hillebrand, Marc Robin Stenzel, Tobias Deußer, David Biesner, Christian Bauckhage, and Rafet Sifa. Towards generating financial reports from tabular data using transformers. In International Cross-Domain Conference for Machine Learning and Knowledge Extraction, pages 221–232.  [OA](https://scholar.google.co.uk/scholar?q=Chapman%2C%20Clayton%20Leroy%20Hillebrand%2C%20Lars%20Stenzel%2C%20Marc%20Robin%20Deu%C3%9Fer%2C%20Tobias%20Towards%20generating%20financial%20reports%20from%20tabular%20data%20using%20transformers) [GScholar](https://scholar.google.co.uk/scholar?q=Chapman%2C%20Clayton%20Leroy%20Hillebrand%2C%20Lars%20Stenzel%2C%20Marc%20Robin%20Deu%C3%9Fer%2C%20Tobias%20Towards%20generating%20financial%20reports%20from%20tabular%20data%20using%20transformers) 

[^6]: Zihan Chen, Lei Nico Zheng, Cheng Lu, Jialu Yuan, and Di Zhu. Chatgpt informed graph neural network for stock movement prediction. arXiv preprint arXiv:2306.03763, 2023.  [OA](https://arxiv.org/abs/2306.03763)  

[^7]: Junyan Cheng and Peter Chin. Sociodojo: Building lifelong analytical agents with real-world text and time series. In The Twelfth International Conference on Learning Representations, 2024.  [OA](https://scholar.google.co.uk/scholar?q=Cheng%2C%20Junyan%20Chin%2C%20Peter%20Sociodojo%3A%20Building%20lifelong%20analytical%20agents%20with%20real-world%20text%20and%20time%20series%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Cheng%2C%20Junyan%20Chin%2C%20Peter%20Sociodojo%3A%20Building%20lifelong%20analytical%20agents%20with%20real-world%20text%20and%20time%20series%202024) 

[^8]: Zihan Dong, Xinyu Fan, and Zhiyuan Peng. Fnspid: A comprehensive financial news dataset in time series. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 4918–4927, 2024.  [OA](https://scholar.google.co.uk/scholar?q=Dong%2C%20Zihan%20Fan%2C%20Xinyu%20Peng%2C%20Zhiyuan%20Fnspid%3A%20A%20comprehensive%20financial%20news%20dataset%20in%20time%20series%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Dong%2C%20Zihan%20Fan%2C%20Xinyu%20Peng%2C%20Zhiyuan%20Fnspid%3A%20A%20comprehensive%20financial%20news%20dataset%20in%20time%20series%202024) 

[^9]: Kui Fu and Yanbin Zhang. Incorporating multi-source market sentiment and price data for stock price prediction. Mathematics, 12(10):1572, 2024.  [OA](https://engine.scholarcy.com/oa_version?query=Fu%2C%20Kui%20Zhang%2C%20Yanbin%20Incorporating%20multi-source%20market%20sentiment%20and%20price%20data%20for%20stock%20price%20prediction%202024&author=Fu&title=Incorporating%20multi-source%20market%20sentiment%20and%20price%20data%20for%20stock%20price%20prediction&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Fu%2C%20Kui%20Zhang%2C%20Yanbin%20Incorporating%20multi-source%20market%20sentiment%20and%20price%20data%20for%20stock%20price%20prediction%202024) [Scite](/scite_tallies?query=author%3AFu%2Ctitle%3AIncorporating%20multi-source%20market%20sentiment%20and%20price%20data%20for%20stock%20price%20prediction%2Cyear%3A2024)

[^10]: Udit Gupta. Gpt-investar: Enhancing stock investment strategies through annual report analysis with large language models. arXiv preprint arXiv:2309.03079, 2023.  [OA](https://arxiv.org/abs/2309.03079)  

[^11]: Yu Huang, Chenzhuang Du, Zihui Xue, Xuanyao Chen, Hang Zhao, and Longbo Huang. What makes multi-modal learning better than single (provably). Advances in Neural Information Processing Systems, 34:10944–10956, 2021.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20Yu%20Du%2C%20Chenzhuang%20Xue%2C%20Zihui%20Chen%2C%20Xuanyao%20What%20makes%20multi-modal%20learning%20better%20than%20single%20%28provably%202021&author=Huang&title=What%20makes%20multi-modal%20learning%20better%20than%20single%20%28provably&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20Yu%20Du%2C%20Chenzhuang%20Xue%2C%20Zihui%20Chen%2C%20Xuanyao%20What%20makes%20multi-modal%20learning%20better%20than%20single%20%28provably%202021) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AWhat%20makes%20multi-modal%20learning%20better%20than%20single%20%28provably%2Cyear%3A2021)

[^12]: Bryan Kelly, Dacheng Xiu, et al. Financial machine learning. Foundations and Trends® in Finance, 13(3-4):205–363, 2023.  [OA](https://engine.scholarcy.com/oa_version?query=Kelly%2C%20Bryan%20Xiu%2C%20Dacheng%20Financial%20machine%20learning%202023&author=Kelly&title=Financial%20machine%20learning&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Kelly%2C%20Bryan%20Xiu%2C%20Dacheng%20Financial%20machine%20learning%202023) [Scite](/scite_tallies?query=author%3AKelly%2Ctitle%3AFinancial%20machine%20learning%2Cyear%3A2023)

[^13]: Kyoung-jae Kim. Financial time series forecasting using support vector machines. Neurocomputing, 55(1-2):307–319, 2003.  [OA](https://engine.scholarcy.com/oa_version?query=Kim%2C%20Kyoung-jae%20Financial%20time%20series%20forecasting%20using%20support%20vector%20machines%202003&author=Kim&title=Financial%20time%20series%20forecasting%20using%20support%20vector%20machines&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Kim%2C%20Kyoung-jae%20Financial%20time%20series%20forecasting%20using%20support%20vector%20machines%202003) [Scite](/scite_tallies?query=author%3AKim%2Ctitle%3AFinancial%20time%20series%20forecasting%20using%20support%20vector%20machines%2Cyear%3A2003)

[^14]: Kelvin JL Koa, Yunshan Ma, Ritchie Ng, and Tat-Seng Chua. Learning to generate explainable stock predictions using self-reflective large language models. In Proceedings of the ACM Web Conference 2024, pages 4304–4315, 2024.  [OA](https://scholar.google.co.uk/scholar?q=Koa%2C%20Kelvin%20J.L.%20Ma%2C%20Yunshan%20Ng%2C%20Ritchie%20Chua%2C%20Tat-Seng%20Learning%20to%20generate%20explainable%20stock%20predictions%20using%20self-reflective%20large%20language%20models%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Koa%2C%20Kelvin%20J.L.%20Ma%2C%20Yunshan%20Ng%2C%20Ritchie%20Chua%2C%20Tat-Seng%20Learning%20to%20generate%20explainable%20stock%20predictions%20using%20self-reflective%20large%20language%20models%202024) 

[^15]: Yaxuan Kong, Yiyuan Yang, Yoontae Hwang, Wenjie Du, Stefan Zohren, Zhangyang Wang, Ming Jin, and Qingsong Wen. Time-mqa: Time series multi-task question answering with context enhancement. arXiv preprint arXiv:2503.01875, 2025.  [OA](https://arxiv.org/abs/2503.01875)  

[^16]: Ross Koval, Nicholas Andrews, and Xifeng Yan. Financial forecasting from textual and tabular time series. In Findings of the Association for Computational Linguistics: EMNLP 2024, pages 8289–8300, 2024.  [OA](https://scholar.google.co.uk/scholar?q=Koval%2C%20Ross%20Andrews%2C%20Nicholas%20Yan%2C%20Xifeng%20Financial%20forecasting%20from%20textual%20and%20tabular%20time%20series%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Koval%2C%20Ross%20Andrews%2C%20Nicholas%20Yan%2C%20Xifeng%20Financial%20forecasting%20from%20textual%20and%20tabular%20time%20series%202024) 

[^17]: Bjoern Krollner, Bruce Vanstone, and Gavin Finnie. Financial time series forecasting with machine learning techniques: A survey. In European Symposium on Artificial Neural Networks: Computational Intelligence and Machine Learning, pages 25–30, 2010.  [OA](https://scholar.google.co.uk/scholar?q=Krollner%2C%20Bjoern%20Vanstone%2C%20Bruce%20Finnie%2C%20Gavin%20Financial%20time%20series%20forecasting%20with%20machine%20learning%20techniques%3A%20A%20survey%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Krollner%2C%20Bjoern%20Vanstone%2C%20Bruce%20Finnie%2C%20Gavin%20Financial%20time%20series%20forecasting%20with%20machine%20learning%20techniques%3A%20A%20survey%202010) 

[^18]: Moreno La Quatra and Luca Cagliero. End-to-end training for financial report summarization. In Proceedings of the 1st Joint Workshop on Financial Narrative Processing and MultiLing Financial Summarisation, pages 118–123, 2020.  [OA](https://scholar.google.co.uk/scholar?q=Quatra%2C%20Moreno%20Cagliero%2C%20Luca%20End-to-end%20training%20for%20financial%20report%20summarization%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Quatra%2C%20Moreno%20Cagliero%2C%20Luca%20End-to-end%20training%20for%20financial%20report%20summarization%202020) 

[^19]: Geon Lee, Wenchao Yu, Kijung Shin, Wei Cheng, and Haifeng Chen. Timecap: Learning to contextualize, augment, and predict time series events with large language model agents. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 18082–18090, 2025.  [OA](https://scholar.google.co.uk/scholar?q=Lee%2C%20Geon%20Yu%2C%20Wenchao%20Shin%2C%20Kijung%20Cheng%2C%20Wei%20Timecap%3A%20Learning%20to%20contextualize%2C%20augment%2C%20and%20predict%20time%20series%20events%20with%20large%20language%20model%20agents%202025) [GScholar](https://scholar.google.co.uk/scholar?q=Lee%2C%20Geon%20Yu%2C%20Wenchao%20Shin%2C%20Kijung%20Cheng%2C%20Wei%20Timecap%3A%20Learning%20to%20contextualize%2C%20augment%2C%20and%20predict%20time%20series%20events%20with%20large%20language%20model%20agents%202025) 

[^20]: Haoxin Liu, Shangqing Xu, Zhiyuan Zhao, Lingkai Kong, Harshavardhan Prabhakar Kamarthi, Aditya Sasanur, Megha Sharma, Jiaming Cui, Qingsong Wen, Chao Zhang, et al. Time-mmd: Multi-domain multimodal dataset for time series analysis. Advances in Neural Information Processing Systems, 37:77888–77933, 2024.  [OA](https://engine.scholarcy.com/oa_version?query=Liu%2C%20Haoxin%20Xu%2C%20Shangqing%20Zhao%2C%20Zhiyuan%20Kong%2C%20Lingkai%20Time-mmd%3A%20Multi-domain%20multimodal%20dataset%20for%20time%20series%20analysis%202024&author=Liu&title=Time-mmd%3A%20Multi-domain%20multimodal%20dataset%20for%20time%20series%20analysis&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Haoxin%20Xu%2C%20Shangqing%20Zhao%2C%20Zhiyuan%20Kong%2C%20Lingkai%20Time-mmd%3A%20Multi-domain%20multimodal%20dataset%20for%20time%20series%20analysis%202024) [Scite](/scite_tallies?query=author%3ALiu%2Ctitle%3ATime-mmd%3A%20Multi-domain%20multimodal%20dataset%20for%20time%20series%20analysis%2Cyear%3A2024)

[^21]: Xiao-Yang Liu, Guoxuan Wang, Hongyang Yang, and Daochen Zha. Fingpt: Democratizing internet-scale data for financial large language models. In NeurIPS 2023 Workshop on Instruction Tuning and Instruction Following.  [OA](https://scholar.google.co.uk/scholar?q=Liu%2C%20Xiao-Yang%20Wang%2C%20Guoxuan%20Yang%2C%20Hongyang%20Zha%2C%20Daochen%20Fingpt%3A%20Democratizing%20internet-scale%20data%20for%20financial%20large%20language%20models%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Xiao-Yang%20Wang%2C%20Guoxuan%20Yang%2C%20Hongyang%20Zha%2C%20Daochen%20Fingpt%3A%20Democratizing%20internet-scale%20data%20for%20financial%20large%20language%20models%202023) 

[^22]: Xiao-Yang Liu, Hongyang Yang, Qian Chen, Runjia Zhang, Liuqing Yang, Bowen Xiao, and Christina Dan Wang. Finrl: A deep reinforcement learning library for automated stock trading in quantitative finance. arXiv preprint arXiv:2011.09607, 2020.  [OA](https://arxiv.org/abs/2011.09607)  

[^23]: Alejandro Lopez-Lira and Yuehua Tang. Can chatgpt forecast stock price movements? return predictability and large language models. arXiv preprint arXiv:2304.07619, 2023.  [OA](https://arxiv.org/abs/2304.07619)  

[^24]: Mantas Lukauskas, Vaida Pilinkienė, Jurgita Bruneckienė, Alina Stundžienė, Andrius Grybauskas, and Tomas Ruzgas. Economic activity forecasting based on the sentiment analysis of news. Mathematics, 10(19):3461, 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Lukauskas%2C%20Mantas%20Pilinkien%C4%97%2C%20Vaida%20Bruneckien%C4%97%2C%20Jurgita%20Stund%C5%BEien%C4%97%2C%20Alina%20Economic%20activity%20forecasting%20based%20on%20the%20sentiment%20analysis%20of%20news%202022&author=Lukauskas&title=Economic%20activity%20forecasting%20based%20on%20the%20sentiment%20analysis%20of%20news&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Lukauskas%2C%20Mantas%20Pilinkien%C4%97%2C%20Vaida%20Bruneckien%C4%97%2C%20Jurgita%20Stund%C5%BEien%C4%97%2C%20Alina%20Economic%20activity%20forecasting%20based%20on%20the%20sentiment%20analysis%20of%20news%202022) [Scite](/scite_tallies?query=author%3ALukauskas%2Ctitle%3AEconomic%20activity%20forecasting%20based%20on%20the%20sentiment%20analysis%20of%20news%2Cyear%3A2022)

[^25]: Burton G. Malkiel and Eugene F. Fama. Efficient capital markets: A review of theory and empirical work. The Journal of Finance, 25(2):383–417, 1970.  [OA](https://engine.scholarcy.com/oa_version?query=Malkiel%2C%20Burton%20G.%20Fama%2C%20Eugene%20F.%20Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%201970&author=Malkiel&title=Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work&year=1970) [GScholar](https://scholar.google.co.uk/scholar?q=Malkiel%2C%20Burton%20G.%20Fama%2C%20Eugene%20F.%20Efficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%201970) [Scite](/scite_tallies?query=author%3AMalkiel%2Ctitle%3AEfficient%20capital%20markets%3A%20A%20review%20of%20theory%20and%20empirical%20work%2Cyear%3A1970)

[^26]: Eliza Mik. Smart contracts: terminology, technical limitations and real world complexity. Law, innovation and technology, 9(2):269–300, 2017.  [OA](https://engine.scholarcy.com/oa_version?query=Mik%2C%20Eliza%20Smart%20contracts%3A%20terminology%2C%20technical%20limitations%20and%20real%20world%20complexity%202017&author=Mik&title=Smart%20contracts%3A%20terminology%2C%20technical%20limitations%20and%20real%20world%20complexity&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Mik%2C%20Eliza%20Smart%20contracts%3A%20terminology%2C%20technical%20limitations%20and%20real%20world%20complexity%202017) [Scite](/scite_tallies?query=author%3AMik%2Ctitle%3ASmart%20contracts%3A%20terminology%2C%20technical%20limitations%20and%20real%20world%20complexity%2Cyear%3A2017)

[^27]: Omer Berat Sezer, Mehmet Ugur Gudelek, and Ahmet Murat Ozbayoglu. Financial time series forecasting with deep learning: A systematic literature review: 2005–2019. Applied soft computing, 90:106181, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Omer%20Berat%20Sezer%20Mehmet%20Ugur%20Gudelek%20and%20Ahmet%20Murat%20Ozbayoglu%20Financial%20time%20series%20forecasting%20with%20deep%20learning%20A%20systematic%20literature%20review%2020052019%20Applied%20soft%20computing%2090106181%202020&author=Sezer&title=Financial%20time%20series%20forecasting%20with%20deep%20learning%3A%20A%20systematic%20literature%20review%3A%202005%E2%80%932019&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Omer%20Berat%20Sezer%20Mehmet%20Ugur%20Gudelek%20and%20Ahmet%20Murat%20Ozbayoglu%20Financial%20time%20series%20forecasting%20with%20deep%20learning%20A%20systematic%20literature%20review%2020052019%20Applied%20soft%20computing%2090106181%202020) [Scite](/scite_tallies?query=author%3ASezer%2Ctitle%3AFinancial%20time%20series%20forecasting%20with%20deep%20learning%3A%20A%20systematic%20literature%20review%3A%202005%E2%80%932019%2Cyear%3A2020)

[^28]: Wataru Souma, Irena Vodenska, and Hideaki Aoyama. Enhanced news sentiment analysis using deep learning methods. Journal of Computational Social Science, 2(1):33–46, 2019.  [OA](https://engine.scholarcy.com/oa_version?query=Souma%2C%20Wataru%20Vodenska%2C%20Irena%20Aoyama%2C%20Hideaki%20Enhanced%20news%20sentiment%20analysis%20using%20deep%20learning%20methods%202019&author=Souma&title=Enhanced%20news%20sentiment%20analysis%20using%20deep%20learning%20methods&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Souma%2C%20Wataru%20Vodenska%2C%20Irena%20Aoyama%2C%20Hideaki%20Enhanced%20news%20sentiment%20analysis%20using%20deep%20learning%20methods%202019) [Scite](/scite_tallies?query=author%3ASouma%2Ctitle%3AEnhanced%20news%20sentiment%20analysis%20using%20deep%20learning%20methods%2Cyear%3A2019)

[^29]: Xinlei Wang, Maike Feng, Jing Qiu, Jinjin Gu, and Junhua Zhao. From news to forecast: Integrating event analysis in llm-based time series forecasting with reflection. Advances in Neural Information Processing Systems, 37:58118–58153, 2024.  [OA](https://engine.scholarcy.com/oa_version?query=Wang%2C%20Xinlei%20Feng%2C%20Maike%20Qiu%2C%20Jing%20Gu%2C%20Jinjin%20From%20news%20to%20forecast%3A%20Integrating%20event%20analysis%20in%20llm-based%20time%20series%20forecasting%20with%20reflection%202024&author=Wang&title=From%20news%20to%20forecast%3A%20Integrating%20event%20analysis%20in%20llm-based%20time%20series%20forecasting%20with%20reflection&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Wang%2C%20Xinlei%20Feng%2C%20Maike%20Qiu%2C%20Jing%20Gu%2C%20Jinjin%20From%20news%20to%20forecast%3A%20Integrating%20event%20analysis%20in%20llm-based%20time%20series%20forecasting%20with%20reflection%202024) [Scite](/scite_tallies?query=author%3AWang%2Ctitle%3AFrom%20news%20to%20forecast%3A%20Integrating%20event%20analysis%20in%20llm-based%20time%20series%20forecasting%20with%20reflection%2Cyear%3A2024)

[^30]: Sanford Weisberg. Applied linear regression, volume 528. John Wiley &amp;amp; Sons, 2005.  [OA](https://scholar.google.co.uk/scholar?q=Weisberg%2C%20Sanford%20Applied%20linear%20regression%2C%20volume%20528%202005) [GScholar](https://scholar.google.co.uk/scholar?q=Weisberg%2C%20Sanford%20Applied%20linear%20regression%2C%20volume%20528%202005) 

[^31]: Andrew Robert Williams, Arjun Ashok, Étienne Marcotte, Valentina Zantedeschi, Jithendaraa Subramanian, Roland Riachi, James Requeima, Alexandre Lacoste, Irina Rish, Nicolas Chapados, et al. Context is key: A benchmark for forecasting with essential textual information. arXiv preprint arXiv:2410.18959, 2024.  [OA](https://arxiv.org/abs/2410.18959)  

[^32]: Huizhe Wu, Wei Zhang, Weiwei Shen, and Jun Wang. Hybrid deep sequential modeling for social text-driven stock prediction. In Proceedings of the 27th ACM international conference on information and knowledge management, pages 1627–1630, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Wu%2C%20Huizhe%20Zhang%2C%20Wei%20Shen%2C%20Weiwei%20Wang%2C%20Jun%20Hybrid%20deep%20sequential%20modeling%20for%20social%20text-driven%20stock%20prediction%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Wu%2C%20Huizhe%20Zhang%2C%20Wei%20Shen%2C%20Weiwei%20Wang%2C%20Jun%20Hybrid%20deep%20sequential%20modeling%20for%20social%20text-driven%20stock%20prediction%202018) 

[^33]: Qianqian Xie, Weiguang Han, Zhengyu Chen, Ruoyu Xiang, Xiao Zhang, Yueru He, Mengxi Xiao, Dong Li, Yongfu Dai, Duanyu Feng, et al. Finben: A holistic financial benchmark for large language models. Advances in Neural Information Processing Systems, 37:95716–95743, 2024.  [OA](https://engine.scholarcy.com/oa_version?query=Xie%2C%20Qianqian%20Han%2C%20Weiguang%20Chen%2C%20Zhengyu%20Xiang%2C%20Ruoyu%20Finben%3A%20A%20holistic%20financial%20benchmark%20for%20large%20language%20models%202024&author=Xie&title=Finben%3A%20A%20holistic%20financial%20benchmark%20for%20large%20language%20models&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Xie%2C%20Qianqian%20Han%2C%20Weiguang%20Chen%2C%20Zhengyu%20Xiang%2C%20Ruoyu%20Finben%3A%20A%20holistic%20financial%20benchmark%20for%20large%20language%20models%202024) [Scite](/scite_tallies?query=author%3AXie%2Ctitle%3AFinben%3A%20A%20holistic%20financial%20benchmark%20for%20large%20language%20models%2Cyear%3A2024)

[^34]: Frank Z Xing, Erik Cambria, and Roy E Welsch. Natural language based financial forecasting: a survey. Artificial Intelligence Review, 50(1):49–73, 2018.  [OA](https://engine.scholarcy.com/oa_version?query=Xing%2C%20Frank%20Z.%20Cambria%2C%20Erik%20Welsch%2C%20Roy%20E.%20Natural%20language%20based%20financial%20forecasting%3A%20a%20survey%202018&author=Xing&title=Natural%20language%20based%20financial%20forecasting%3A%20a%20survey&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Xing%2C%20Frank%20Z.%20Cambria%2C%20Erik%20Welsch%2C%20Roy%20E.%20Natural%20language%20based%20financial%20forecasting%3A%20a%20survey%202018) [Scite](/scite_tallies?query=author%3AXing%2Ctitle%3ANatural%20language%20based%20financial%20forecasting%3A%20a%20survey%2Cyear%3A2018)

[^35]: Yumo Xu and Shay B Cohen. Stock movement prediction from tweets and historical prices. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1970–1979, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Xu%2C%20Yumo%20Cohen%2C%20Shay%20B.%20Stock%20movement%20prediction%20from%20tweets%20and%20historical%20prices%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Xu%2C%20Yumo%20Cohen%2C%20Shay%20B.%20Stock%20movement%20prediction%20from%20tweets%20and%20historical%20prices%202018) 

[^36]: Hang Yang, Yubo Chen, Kang Liu, Yang Xiao, and Jun Zhao. Dcfee: A document-level chinese financial event extraction system based on automatically labeled training data. In Proceedings of ACL 2018, System Demonstrations, pages 50–55, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20Hang%20Chen%2C%20Yubo%20Liu%2C%20Kang%20Xiao%2C%20Yang%20Dcfee%3A%20A%20document-level%20chinese%20financial%20event%20extraction%20system%20based%20on%20automatically%20labeled%20training%20data%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Hang%20Chen%2C%20Yubo%20Liu%2C%20Kang%20Xiao%2C%20Yang%20Dcfee%3A%20A%20document-level%20chinese%20financial%20event%20extraction%20system%20based%20on%20automatically%20labeled%20training%20data%202018) 

[^37]: Yi Yang, Yixuan Tang, and Kar Yan Tam. Investlm: A large language model for investment using financial domain instruction tuning. arXiv preprint arXiv:2309.13064, 2023.  [OA](https://arxiv.org/abs/2309.13064)  

[^38]: Wentao Zhang, Lingxuan Zhao, Haochong Xia, Shuo Sun, Jiaze Sun, Molei Qin, Xinyi Li, Yuqing Zhao, Yilei Zhao, Xinyu Cai, et al. A multimodal foundation agent for financial trading: Tool-augmented, diversified, and generalist. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 4314–4325, 2024.  [OA](https://scholar.google.co.uk/scholar?q=Zhang%2C%20Wentao%20Zhao%2C%20Lingxuan%20Xia%2C%20Haochong%20Sun%2C%20Shuo%20A%20multimodal%20foundation%20agent%20for%20financial%20trading%3A%20Tool-augmented%2C%20diversified%2C%20and%20generalist%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Zhang%2C%20Wentao%20Zhao%2C%20Lingxuan%20Xia%2C%20Haochong%20Sun%2C%20Shuo%20A%20multimodal%20foundation%20agent%20for%20financial%20trading%3A%20Tool-augmented%2C%20diversified%2C%20and%20generalist%202024) 

[^39]: Yanzhao Zou and Dorien Herremans. Prebit—a multimodal model with twitter finbert embeddings for extreme price movement prediction of bitcoin. Expert Systems with Applications, 233:120838, 2023.  [OA](https://engine.scholarcy.com/oa_version?query=Zou%2C%20Yanzhao%20Herremans%2C%20Dorien%20Prebit%E2%80%94a%20multimodal%20model%20with%20twitter%20finbert%20embeddings%20for%20extreme%20price%20movement%20prediction%20of%20bitcoin%202023&author=Zou&title=Prebit%E2%80%94a%20multimodal%20model%20with%20twitter%20finbert%20embeddings%20for%20extreme%20price%20movement%20prediction%20of%20bitcoin&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Zou%2C%20Yanzhao%20Herremans%2C%20Dorien%20Prebit%E2%80%94a%20multimodal%20model%20with%20twitter%20finbert%20embeddings%20for%20extreme%20price%20movement%20prediction%20of%20bitcoin%202023) [Scite](/scite_tallies?query=author%3AZou%2Ctitle%3APrebit%E2%80%94a%20multimodal%20model%20with%20twitter%20finbert%20embeddings%20for%20extreme%20price%20movement%20prediction%20of%20bitcoin%2Cyear%3A2023)

[^3]: Theory assumptions and proofs  [OA](https://scholar.google.co.uk/scholar?q=Theory%20assumptions%20and%20proofs) [GScholar](https://scholar.google.co.uk/scholar?q=Theory%20assumptions%20and%20proofs) 

[^4]: Experimental result reproducibility  [OA](https://scholar.google.co.uk/scholar?q=Experimental%20result%20reproducibility) [GScholar](https://scholar.google.co.uk/scholar?q=Experimental%20result%20reproducibility) 

[^5]: Open access to data and code  [OA](https://scholar.google.co.uk/scholar?q=Open%20access%20to%20data%20and%20code) [GScholar](https://scholar.google.co.uk/scholar?q=Open%20access%20to%20data%20and%20code) 

[^6]: Experimental setting/details  [OA](https://scholar.google.co.uk/scholar?q=Experimental%20settingdetails) [GScholar](https://scholar.google.co.uk/scholar?q=Experimental%20settingdetails) 

[^7]: Experiment statistical significance  [OA](https://scholar.google.co.uk/scholar?q=Experiment%20statistical%20significance) [GScholar](https://scholar.google.co.uk/scholar?q=Experiment%20statistical%20significance) 

[^8]: Experiments compute resources  [OA](https://scholar.google.co.uk/scholar?q=Experiments%20compute%20resources) [GScholar](https://scholar.google.co.uk/scholar?q=Experiments%20compute%20resources) 

[^9]: Code of ethics  [OA](https://scholar.google.co.uk/scholar?q=Code%20of%20ethics) [GScholar](https://scholar.google.co.uk/scholar?q=Code%20of%20ethics) 

[^10]: Broader impacts  [OA](https://scholar.google.co.uk/scholar?q=Broader%20impacts) [GScholar](https://scholar.google.co.uk/scholar?q=Broader%20impacts) 

[^12]: Licenses for existing assets  [OA](https://scholar.google.co.uk/scholar?q=Licenses%20for%20existing%20assets) [GScholar](https://scholar.google.co.uk/scholar?q=Licenses%20for%20existing%20assets) 

[^14]: Crowdsourcing and research with human subjects  [OA](https://scholar.google.co.uk/scholar?q=Crowdsourcing%20and%20research%20with%20human%20subjects) [GScholar](https://scholar.google.co.uk/scholar?q=Crowdsourcing%20and%20research%20with%20human%20subjects) 

[^15]: Institutional review board (IRB) approvals or equivalent for research with human subjects  [OA](https://scholar.google.co.uk/scholar?q=Institutional%20review%20board%20IRB%20approvals%20or%20equivalent%20for%20research%20with%20human%20subjects) [GScholar](https://scholar.google.co.uk/scholar?q=Institutional%20review%20board%20IRB%20approvals%20or%20equivalent%20for%20research%20with%20human%20subjects) 

[^16]: Declaration of LLM usage   [OA](https://scholar.google.co.uk/scholar?q=Declaration%20of%20LLM%20usage) [GScholar](https://scholar.google.co.uk/scholar?q=Declaration%20of%20LLM%20usage) 

