[[Shen_FinancialSentimentAnalysisNewsReports_2024]]

# [Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT](https://doi.org/10.1109/icpics62053.2024.10796670)

## [[Yaoxin Shen]]; [[Pulin Kirin Zhang]]

## Abstract
Financial sentiment analysis (FSA) is crucial for evaluating market sentiment and making well-informed financial decisions. The advent of large language models (LLMs) such as BERT and its financial variant, FinBERT, has notably enhanced sentiment analysis capabilities. ==This paper investigates the application of LLMs and FinBERT for FSA, comparing their performance on news articles, financial reports and company announcements==. The study emphasizes the advantages of prompt engineering with zero-shot and few-shot strategy to improve sentiment classification accuracy. Experimental results indicate that GPT-4o, with few-shot examples of financial texts, can be as competent as a well finetuned FinBERT in this specialized field.

## Key concepts
#GPT_4; #prompt_engineering; #artificial_general_intelligence; #natural_language_processing; #financial_sentiment_analysis; #large_language_models; #deep_learning; #sentiment_analysis; #claim/FinBERT; #FinBERT; #claim/BERT; #BERT

## Quote
> This paper explores the application of large language models (LLMs) and FinBERT for financial sentiment analysis, comparing their performance on news articles, financial reports, and company announcements, and highlighting the advantages of prompt engineering with zero-shot and few-shot strategy to improve sentiment classification accuracy.

## Key points
- Sentiment analysis has a long history [^1], [^2], [^3] and focuses on identifying and extracting opinions and emotions from text data [^4], [^5]
- This study investigated the use of large language models (LLMs) and FinBERT for financial sentiment analysis (FSA) using financial news articles and reports
- FinBERT, which was fine-tuned on the Financial PhraseBank dataset, consistently outperformed general-purpose LLMs
- It achieved the highest scores in accuracy, precision, recall, and F1-score. These results highlight the significance of domain-specific pre-training for effective financial sentiment analysis
- Further exploration into fine-tuning strategies and leveraging additional domain-specific datasets could enhance the capabilities of LLMs for Financial Sentiment Analysis (FSA).There is potential for integrating LLMs with real-time financial data, enabling dynamic and context-aware sentiment analysis that can adapt to market fluctuations and emerging trends
- To create a robust training set, we set aside 20% of the sentences as a test set and used 20% of the remaining sentences as a validation set
- Effective prompt engineering can significantly enhance the performance of LLMs, making them viable tools for FSA in real-world applications


## Summary

### Introduction To FSA
Financial sentiment analysis (FSA) is crucial for evaluating market sentiment and making well-informed financial decisions.
The advent of large language models (LLMs) such as BERT and its financial variant, FinBERT, has notably enhanced sentiment analysis capabilities.
FSA presents several challenges that distinguish it from general sentiment analysis, such as the need for domain-specific knowledge, dealing with ambiguities, and managing uncertainties.

### LLMs And Prompt Engineering
Large language models (LLMs) represent a new paradigm in Natural Language Understanding, setting them apart from traditional NLP models.
LLMs offer numerous advantages over conventional NLP models, including scalability, generality, data efficiency, and transferability.
Prompt engineering, the craft of designing natural language input instructions known as prompts, offers a promising solution to the challenge of utilizing pre-trained knowledge and adapting it to specific domains and tasks.
This technique does not require extra training or fine-tuning.

### Methodology And Results
The study investigates the application of LLMs and FinBERT for FSA, comparing their performance on news articles, financial reports, and company announcements.
The experiment aims to observe the response of LLMs to few-shot prompts in financial sentiment analysis.
The primary dataset for sentiment analysis is the Financial PhraseBank, which contains 4845 English sentences randomly selected from financial news in the LexisNexis database.
Experimental results indicate that GPT-4, with few-shot examples of financial texts, can be as competent as a well-finetuned FinBERT in this specialized field.

### Models
The study utilized various models, including GPT-3.5-turbo, GPT-4o, and FinBERT, under different configurations such as zero-shot, few-shot, and fine-tuning approaches.
FinBERT, which was fine-tuned on the Financial PhraseBank dataset, consistently outperformed general-purpose LLMs.
GPT-4o, with its advanced capabilities, also performed well, especially in the few-shot setting.

### Performance
The experimental results indicate that fine-tuning FinBERT on a domain-specific corpus yields the best performance for financial sentiment analysis.
The precision metric demonstrates that prompt engineering can greatly improve the efficiency of large language models even without extensive fine-tuning.
GPT-4o, with few-shot examples of financial texts, can be as competent as a well-finetuned FinBERT in this specialized field.

### Future Work
Future research should focus on improving prompt designs and incorporating more comprehensive few-shot examples to bridge the gap in zero-shot learning.
Further exploration into fine-tuning strategies and leveraging additional domain-specific datasets could enhance the capabilities of LLMs for financial sentiment analysis.
There is also potential for integrating LLMs with real-time financial data, enabling dynamic and context-aware sentiment analysis that can adapt to market fluctuations and emerging trends.


## Study subjects

### 16 individuals with expertise in finance and business
- The Financial PhraseBank contains 4845 English sentences randomly selected from financial news in the LexisNexis database. ==These sentences were annotated by 16 individuals with expertise in finance and business==. The annotators labeled the sentences based on how they believed the information might impact the stock price of the mentioned company

## Data analysis
- #method/large_language_models

## Findings
- To create a robust training set, we set aside 20% of the sentences as a test set and used 20% of the remaining sentences as a validation set
- 20% of the sentences were set aside as the test set, and another 20% of the remaining sentences were used for validation, leaving 3,101 sentences for training

## Contributions
- In conclusion, while domain-specific models like FinBERT remain superior due to their tailored pre-training, general-purpose LLMs like GPT-3.5-turbo and GPT-4o show promise for financial sentiment analysis with little setup. <mark class="fact">Effective prompt engineering can significantly enhance the performance of LLMs</mark>, making them viable tools for FSA in real-world applications. Future work should continue to refine these models and explore innovative approaches to further improve their accuracy and contextual understanding.

## Limitations
- The study notes that the scarcity of extensive labeled financial datasets poses a challenge in effectively utilizing neural networks for sentiment analysis. The study also acknowledges the limitations of LLMs, including high computational costs, environmental impact, ethical concerns, and reliability issues.
- The study notes that zero-shot learning has limitations due to the lack of contextual information, and that future research should focus on improving prompt designs and incorporating more comprehensive few-shot examples. The study also acknowledges that the results may differ with future versions of the LLMs, as they receive periodic updates.


## References
[^1]: Z. Nanli, Z. Ping, L. Weiguo, and C. Meng, “Sentiment analysis: A literature review,” in 2012 International Symposium on Management of Technology (ISMOT), pp. 572–576, IEEE, 2012.  [OA](https://scholar.google.co.uk/scholar?q=Nanli%2C%20Z.%20Ping%2C%20Z.%20Weiguo%2C%20L.%20Meng%2C%20C.%20Sentiment%20analysis%3A%20A%20literature%20review%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Nanli%2C%20Z.%20Ping%2C%20Z.%20Weiguo%2C%20L.%20Meng%2C%20C.%20Sentiment%20analysis%3A%20A%20literature%20review%202012) 

[^2]: M. V. Mäntylä, D. Graziotin, and M. Kuutila, “The evolution of sentiment analysis—a review of research topics, venues, and top cited papers,” Computer Science Review, vol. 27, pp. 16–32, 2018.  [OA](https://engine.scholarcy.com/oa_version?query=M%C3%A4ntyl%C3%A4%2C%20M.V.%20Graziotin%2C%20D.%20Kuutila%2C%20M.%20The%20evolution%20of%20sentiment%20analysis%E2%80%94a%20review%20of%20research%20topics%2C%20venues%2C%20and%20top%20cited%20papers%202018&author=Maentylae&title=The%20evolution%20of%20sentiment%20analysis%E2%80%94a%20review%20of%20research%20topics%2C%20venues%2C%20and%20top%20cited%20papers&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=M%C3%A4ntyl%C3%A4%2C%20M.V.%20Graziotin%2C%20D.%20Kuutila%2C%20M.%20The%20evolution%20of%20sentiment%20analysis%E2%80%94a%20review%20of%20research%20topics%2C%20venues%2C%20and%20top%20cited%20papers%202018) [Scite](/scite_tallies?query=author%3AMaentylae%2Ctitle%3AThe%20evolution%20of%20sentiment%20analysis%E2%80%94a%20review%20of%20research%20topics%2C%20venues%2C%20and%20top%20cited%20papers%2Cyear%3A2018)

[^3]: A. Yadav and D. K. Vishwakarma, “Sentiment analysis using deep learning architectures: a review,” Artificial Intelligence Review, vol. 53, no. 6, pp. 4335–4385, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Yadav%2C%20A.%20Vishwakarma%2C%20D.K.%20Sentiment%20analysis%20using%20deep%20learning%20architectures%3A%20a%20review%202020&author=Yadav&title=Sentiment%20analysis%20using%20deep%20learning%20architectures%3A%20a%20review&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Yadav%2C%20A.%20Vishwakarma%2C%20D.K.%20Sentiment%20analysis%20using%20deep%20learning%20architectures%3A%20a%20review%202020) [Scite](/scite_tallies?query=author%3AYadav%2Ctitle%3ASentiment%20analysis%20using%20deep%20learning%20architectures%3A%20a%20review%2Cyear%3A2020)

[^4]: S. Liu, C. Zheng, O. Demasi, S. Sabour, Y. Li, Z. Yu, Y. Jiang, and M. Huang, “Towards emotional support dialog systems,” arXiv preprint arXiv:2106.01144, 2021.  [OA](https://arxiv.org/abs/2106.01144)  

[^5]: S. Poria, D. Hazarika, N. Majumder, and R. Mihalcea, “Beneath the tip of the iceberg: Current challenges and new directions in sentiment analysis research,” IEEE Transactions on Affective Computing, 2020.  [OA](https://engine.scholarcy.com/oa_version?query=Poria%2C%20S.%20Hazarika%2C%20D.%20Majumder%2C%20N.%20Mihalcea%2C%20R.%20Beneath%20the%20tip%20of%20the%20iceberg%3A%20Current%20challenges%20and%20new%20directions%20in%20sentiment%20analysis%20research%202020&author=Poria&title=Beneath%20the%20tip%20of%20the%20iceberg%3A%20Current%20challenges%20and%20new%20directions%20in%20sentiment%20analysis%20research&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Poria%2C%20S.%20Hazarika%2C%20D.%20Majumder%2C%20N.%20Mihalcea%2C%20R.%20Beneath%20the%20tip%20of%20the%20iceberg%3A%20Current%20challenges%20and%20new%20directions%20in%20sentiment%20analysis%20research%202020) [Scite](/scite_tallies?query=author%3APoria%2Ctitle%3ABeneath%20the%20tip%20of%20the%20iceberg%3A%20Current%20challenges%20and%20new%20directions%20in%20sentiment%20analysis%20research%2Cyear%3A2020)

[^6]: F. Xing, L. Malandri, Y. Zhang, and E. Cambria, “Financial sentiment analysis: An investigation into common mistakes and silver bullets,” in Proceedings of the 28th International Conference on Computational Linguistics, (Barcelona, Spain (Online)), pp. 978–987, International Committee on Computational Linguistics, Dec. 2020.  [OA](https://scholar.google.co.uk/scholar?q=Xing%2C%20F.%20Malandri%2C%20L.%20Zhang%2C%20Y.%20Cambria%2C%20E.%20Financial%20sentiment%20analysis%3A%20An%20investigation%20into%20common%20mistakes%20and%20silver%20bullets%202020-12) [GScholar](https://scholar.google.co.uk/scholar?q=Xing%2C%20F.%20Malandri%2C%20L.%20Zhang%2C%20Y.%20Cambria%2C%20E.%20Financial%20sentiment%20analysis%3A%20An%20investigation%20into%20common%20mistakes%20and%20silver%20bullets%202020-12) 

[^7]: X. Man, T. Luo, and J. Lin, “Financial sentiment analysis (fsa): A survey,” in 2019 IEEE International Conference on Industrial Cyber Physical Systems (ICPS), pp. 617–622, IEEE, 2019.  [OA](https://scholar.google.co.uk/scholar?q=Man%2C%20X.%20Luo%2C%20T.%20Lin%2C%20J.%20Financial%20sentiment%20analysis%20%28fsa%29%3A%20A%20survey%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Man%2C%20X.%20Luo%2C%20T.%20Lin%2C%20J.%20Financial%20sentiment%20analysis%20%28fsa%29%3A%20A%20survey%202019) 

[^8]: F. Barbieri, J. Camacho-Collados, L. Neves, and L. Espinosa-Anke, “Tweeteval: Unified benchmark and comparative evaluation for tweet classification,” arXiv preprint arXiv:2010.12421, 2020.  [OA](https://arxiv.org/abs/2010.12421)  

[^9]: M. Wankhade, A. C. S. Rao, and C. Kulkarni, “A survey on sentiment analysis methods, applications, and challenges,” Artificial Intelligence Review, vol. 55, no. 7, pp. 5731–5780, 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Wankhade%2C%20M.%20Rao%2C%20A.C.S.%20Kulkarni%2C%20C.%20A%20survey%20on%20sentiment%20analysis%20methods%2C%20applications%2C%20and%20challenges%202022&author=Wankhade&title=A%20survey%20on%20sentiment%20analysis%20methods%2C%20applications%2C%20and%20challenges&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Wankhade%2C%20M.%20Rao%2C%20A.C.S.%20Kulkarni%2C%20C.%20A%20survey%20on%20sentiment%20analysis%20methods%2C%20applications%2C%20and%20challenges%202022) [Scite](/scite_tallies?query=author%3AWankhade%2Ctitle%3AA%20survey%20on%20sentiment%20analysis%20methods%2C%20applications%2C%20and%20challenges%2Cyear%3A2022)

[^10]: F. Z. Xing, E. Cambria, and R. E. Welsch, “Natural language based financial forecasting: a survey,” Artificial Intelligence Review, vol. 50, no. 1, pp. 49–73, 2018.  [OA](https://engine.scholarcy.com/oa_version?query=Xing%2C%20F.Z.%20Cambria%2C%20E.%20Welsch%2C%20R.E.%20Natural%20language%20based%20financial%20forecasting%3A%20a%20survey%202018&author=Xing&title=Natural%20language%20based%20financial%20forecasting%3A%20a%20survey&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Xing%2C%20F.Z.%20Cambria%2C%20E.%20Welsch%2C%20R.E.%20Natural%20language%20based%20financial%20forecasting%3A%20a%20survey%202018) [Scite](/scite_tallies?query=author%3AXing%2Ctitle%3ANatural%20language%20based%20financial%20forecasting%3A%20a%20survey%2Cyear%3A2018)

[^11]: S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y. Li, S. Lundberg, et al., “Sparks of artificial general intelligence: Early experiments with gpt-4,” arXiv preprint arXiv:2303.12712, 2023.  [OA](https://arxiv.org/abs/2303.12712)  

[^12]: H. Xu, B. Liu, L. Shu, and P. S. Yu, “Dombert: Domain-oriented language model for aspect-based sentiment analysis,” arXiv preprint arXiv:2004.13816, 2020.  [OA](https://arxiv.org/abs/2004.13816)  

[^13]: W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, et al., “A survey of large language models,” arXiv preprint arXiv:2303.18223, 2023.  [OA](https://arxiv.org/abs/2303.18223)  

[^14]: L. Fan, L. Li, Z. Ma, S. Lee, H. Yu, and L. Hemphill, “A bibliometric review of large language models research from 2017 to 2023,” arXiv preprint arXiv:2304.02020, 2023.  [OA](https://arxiv.org/abs/2304.02020)  

[^15]: D. Araci, “Finbert: Financial sentiment analysis with pre-trained language models,” arXiv preprint arXiv:1908.10063, 2019.  [OA](https://arxiv.org/abs/1908.10063)  

[^16]: P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, “Pre-train, prompt, and predict: A systematic survey of prompting methods in natural language processing,” ACM Computing Surveys, vol. 55, no. 9, pp. 1–35, 2023.   [OA](https://engine.scholarcy.com/oa_version?query=Liu%2C%20P.%20Yuan%2C%20W.%20Fu%2C%20J.%20Jiang%2C%20Z.%20Pre-train%2C%20prompt%2C%20and%20predict%3A%20A%20systematic%20survey%20of%20prompting%20methods%20in%20natural%20language%20processing%202023&author=Liu&title=Pre-train%2C%20prompt%2C%20and%20predict%3A%20A%20systematic%20survey%20of%20prompting%20methods%20in%20natural%20language%20processing&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20P.%20Yuan%2C%20W.%20Fu%2C%20J.%20Jiang%2C%20Z.%20Pre-train%2C%20prompt%2C%20and%20predict%3A%20A%20systematic%20survey%20of%20prompting%20methods%20in%20natural%20language%20processing%202023) [Scite](/scite_tallies?query=author%3ALiu%2Ctitle%3APre-train%2C%20prompt%2C%20and%20predict%3A%20A%20systematic%20survey%20of%20prompting%20methods%20in%20natural%20language%20processing%2Cyear%3A2023)

