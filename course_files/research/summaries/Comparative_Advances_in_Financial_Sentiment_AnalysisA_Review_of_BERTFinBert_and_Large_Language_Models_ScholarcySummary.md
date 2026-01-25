[[Mahendran_et+al_ComparativeAdvancesFinancialSentimentAnalysisa_2025]]

# [Comparative Advances in Financial Sentiment Analysis: A Review of BERT, FinBert, and Large Language Models](https://doi.org/10.1109/idciot64235.2025.10914764)

## [[M. Mahendran]]; [[Akilesh Gokul]]; [[P Sree Lakshmi]] et al

## Abstract

Capturing market sentiments and supporting well-informed financial decision-making depend on the developing field of Financial Sentiment Analysis (FSA). Natural language processing (NLP) has made significant strides in comprehending and categorizing sentiment in intricate financial texts, especially with the use of Large Language Models (LLMs). The application of various LLMs, such as Bidirectional Encoder Representations from Transformers(BERT) and Financial BERT (FinBERT), as well as distilled models, such as DistilBERT and DistilRoBERTa, on a variety of financial datasets, including Financial Phrase Bank and LexisNexis news articles, was the main focus of this review article. highlighting different approaches such as model finetuning, zero-shot and few-shot learning, and prompt engineering. The study focuses on practical model predictions through a case study of sentiment analysis of cryptocurrencies. While FinBERT, a financial variant of BERT, shows high accuracy and robustness, other LLMs achieve varying degrees of success depending on the dataset and domain requirements. The analysis focuses on the challenges, trade-offs, and potential avenues for improving LLMs for financial sentiment analysis.

## Key concepts

# machine_learning; #cryptocurrencies; #deep_learning; #natural_language_processing; #claim/FinBERT; #FinBERT; #financial_sentiment_analysis; #finding/BERT; #BERT; #risk_management; #large_language_models; #sentiment_analysis

## Quote

The article reviews advances in Financial Sentiment Analysis (FSA) using Large Language Models (LLMs), such as BERT and FinBERT, and their derivatives, highlighting their potential benefits, drawbacks, and applications for analyzing financial sentiment across various data sources.

## Key points

- Sentiment analysis is a critical application of Natural Language Processing (NLP) that classifies text as neutral, negative, or positive
- In an attempt to present an expansive analysis of the latest developments in the area of financial sentiment analysis, this paper aims to explore them specifically through the application of large language models like Bidirectional Encoder Representations from Transformers (BERT), Financial BERT (FinBERT), and their derivatives
- The domain-oriented dataset allows a model like FinBERT to learn some nuances of language in finance - its ability to understand how sentiment shifts around corporate earnings or macroeconomic trends
- Advanced NLP models such as BERT, FinBERT, or even ChatGPT are useful in making subtle analyses over news sentiment as it understands what complex financial language is conveyed, thus allowing for further insight on how public discourse influences markets[^29]
- Incorporating large language models like BERT into financial sentiment analysis presents a host of challenges, including model bias, lack of interpretability, high computational requirements, and ethical concerns around data privacy and market manipulation[^32]-34]

## Summary

### Introduction To FSA

Financial Sentiment Analysis (FSA) is a developing field that leverages Natural Language Processing (NLP) to capture market sentiment and support well-informed financial decision-making.
FSA classifies text as neutral, negative, or positive, enabling predictions about market movements.
Large Language Models (LLMs) like BERT and FinBERT have significantly enhanced sentiment analysis by processing large-scale financial data with precision.

### LLMs For FSA

LLMs, including BERT and FinBERT, and their distilled models have improved sentiment analysis in finance.
FinBERT, a financial variant of BERT, achieves high accuracy and robustness, whereas other LLMs show varying degrees of success across datasets and domains.
DistilBERT and DistilRoBERTa are distilled models that retain most of BERT's capabilities while requiring fewer resources, making them suitable for low-latency applications.

### Challenges And Future Directions

Despite advances in FSA, challenges remain, including model interpretability, normative considerations, and computational demands.
Future research directions include integrating multimodal LLMs, which could combine textual data with images, videos, and transactional information to provide a comprehensive view of market sentiment.
Ethical challenges, such as preventing market manipulation and ensuring compliance with privacy laws, must also be addressed.
The use of advanced NLP models in financial sentiment analysis introduces several challenges, including model bias, limited interpretability, high computational requirements, and ethical concerns regarding data privacy and market manipulation.
Domain-specific adaptation is essential, as financial language is rich in jargon and subtle expressions.
Transparency, bias reduction, and regulatory compliance are critical for building trust and integrity in financial sentiment analysis.
The trade-offs between model complexity and efficiency are also important, particularly for firms that rely on high-frequency trading, which requires low latency and high-precision predictions.

### Sentiment Analysis

Financial sentiment analysis draws on various datasets, including the Financial Phrase Bank, LexisNexis, and TRC2financial, each serving different analytical needs.
These datasets are used to train models that classify sentiments in financial language.
The Financial Phrase Bank, for example, comprises 4,845 annotated sentences with labels indicating their effect on stock prices.
Advanced NLP models, such as FinBERT, can learn the nuances of financial language and understand how sentiment shifts around corporate earnings and macroeconomic trends.

### Data Preprocessing

Data preprocessing is a crucial step in converting raw financial text into structured data for models like FinBERT.
This involves data cleaning, tokenization, data balancing, Named Entity Recognition (NER), and entity linking.
These steps ensure that models focus on meaningful financial terms and sentiments, maintain domain-specific language, and handle ambiguities in company names.
Advanced techniques, such as sentiment disambiguation and data normalization, are also applied to detect sentiments masked by rhetorical expressions and to standardize representations of currency, dates, and other factors.

## Study subjects

### 46143 financial documents

- It also captures shifts in sentiment based on the changes in the global or regional economies. The TRC2-financial dataset is derived from Reuters TRC2 news and comprises 46,143 financial documents from 2008 to 2010; it contains 29 million words and 400,000 sentences[^24]. The domain-oriented dataset allows a model like FinBERT to learn some nuances of language in finance - its ability to understand how sentiment shifts around corporate earnings or macroeconomic trends

## Data analysis

- #method/time_series_analysis
- #method/the_language_model
- #method/large_language_models

## Findings

- Hugging Face developed DistilBERT, retaining 97% of the capabilities of the <a class="keyword" href="https://en.wikipedia.org/wiki/BERT_(language_model)" title="BERT">BERT</a> language while coming with half the parameters, hence very property-suitable for low-latency applications like algorithmic trading and market monitoring[^20]

## Contributions

- Innovations within financial markets, propelled by the incorporation of machine learning and correlation-centric indexing, are redefining investment approaches and enhancing risk management practices. Conventional capitalization-weighted indices frequently skew performance evaluations by disproportionately highlighting large-cap stocks; in contrast, correlation-based indices provide a more equitable depiction of sector interactions, thereby enhancing benchmarking accuracy and fostering stability. Advanced machine learning frameworks like CNN-LSTM improve analytical capacity <mark class="fact">significantly because these frameworks can effectively capture non-linear patterns in stock fluctuation and market signals</mark>, which helps investors better identify trends and optimize their returns while at the same time reducing risk. Moreover, contemporary methodologies, such as HRP (Hierarchical Risk Parity) portfolio optimization, align with these indices, providing powerful solutions for risk management, especially in turbulent markets, thereby motivating sustainable investing practices. Advanced corporate-level indexing enables organisations to better measure performance and make well-informed strategic decisions. On the other hand, machine learning frameworks provide greater market visibility and compliance monitoring, even though their "black box" <mark class="fact">traits highlight the need to explain AI to sustain trust and accountability</mark>. Emerging trends in multimodal analysis, integrating data about executive tone and financial media visuals, promise a better understanding of market sentiment, advancing both finance sentiment analysis and model evaluation. Altogether, <mark class="fact"><mark class="fact">innovations improve the state of the representation of the market</mark></mark>, its risk management, and its forecasting capabilities, fortifying a more resilient financial system capable of adaptation in a complex and evolving economic landscape.

## Limitations

- The study highlights the limitations of using LLMs in financial sentiment analysis, such as the need for large amounts of labeled data, the risk of overfitting, and the computational demands of these models. The study also highlights the limitations of distilled models, such as DistilBERT and DistilRoBERTa, which may not perform as well as larger models.
- The study highlights several limitations of financial sentiment analysis, including the potential for bias and the need for transparency and interpretability. The study also notes that LLMs can be computationally expensive and require significant resources.

## Future work

- The study suggests that future work should focus on addressing the challenges and limitations of using LLMs in financial sentiment analysis, such as developing more efficient and effective models, and addressing ethical challenges. The study also suggests that future work should explore integrating multimodal LLMs to provide a comprehensive view of market sentiment.

## References

[^20]: Kumar, S., & Chaturvedi, R. Evaluating the Efficacy of Distilled Transformer Models for Sentiment Analysis in Financial Texts: A Comparative Study.  [OA](https://scholar.google.co.uk/scholar?q=Kumar%2C%20S.%20Chaturvedi%2C%20R.%20Evaluating%20The%20Efficacy%20Of%20Distilled%20Transformer%20Models%20For%20Sentiment%20Analysis%20In%20Financial%20Texts%3A%20A%20Comparative%20Study) [GScholar](https://scholar.google.co.uk/scholar?q=Kumar%2C%20S.%20Chaturvedi%2C%20R.%20Evaluating%20The%20Efficacy%20Of%20Distilled%20Transformer%20Models%20For%20Sentiment%20Analysis%20In%20Financial%20Texts%3A%20A%20Comparative%20Study)

[^24]: Pan, R., García-Díaz, J. A., &; Valencia-García, R. (2024). Individual-vs. Multiple-Objective Strategies for Targeted Sentiment Analysis in Finances Using the Spanish MTSA 2023 Corpus. Electronics, 13(4), 717.  [OA](https://engine.scholarcy.com/oa_version?query=Pan%20R%20Garc%C3%ADaD%C3%ADaz%20J%20A%20%20ValenciaGarc%C3%ADa%20R%202024%20Individualvs%20MultipleObjective%20Strategies%20for%20Targeted%20Sentiment%20Analysis%20in%20Finances%20Using%20the%20Spanish%20MTSA%202023%20Corpus%20Electronics%20134%20717&author=Pan&title=Individual-vs.%20Multiple-Objective%20Strategies%20for%20Targeted%20Sentiment%20Analysis%20in%20Finances%20Using%20the%20Spanish%20MTSA%202023%20Corpus&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Pan%20R%20Garc%C3%ADaD%C3%ADaz%20J%20A%20%20ValenciaGarc%C3%ADa%20R%202024%20Individualvs%20MultipleObjective%20Strategies%20for%20Targeted%20Sentiment%20Analysis%20in%20Finances%20Using%20the%20Spanish%20MTSA%202023%20Corpus%20Electronics%20134%20717) [Scite](/scite_tallies?query=author%3APan%2Ctitle%3AIndividual-vs.%20Multiple-Objective%20Strategies%20for%20Targeted%20Sentiment%20Analysis%20in%20Finances%20Using%20the%20Spanish%20MTSA%202023%20Corpus%2Cyear%3A2024)

[^29]: Husain, A. S., &amp; Othman, R. (2018, March). Information Dissemination Model for Scholars on Cryptocurrencies. In 2018, Fourth International Conference on Information Retrieval and Knowledge Management (CAMP) (pp. 1-6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Husain%2C%20A.S.%20Othman%2C%20R.%20Information%20Dissemination%20Model%20for%20Scholars%20on%20Cryptocurrencies%202018-03) [GScholar](https://scholar.google.co.uk/scholar?q=Husain%2C%20A.S.%20Othman%2C%20R.%20Information%20Dissemination%20Model%20for%20Scholars%20on%20Cryptocurrencies%202018-03)

[^32]: Hadi, M. U., Al Tashi, Q., Shah, A., Qureshi, R., Muneer, A., Irfan, M.,... &amp; Shah, M. (2024). Large language models: a comprehensive survey of their applications, challenges, limitations, and future prospects. Authorea Preprints.   [OA](https://scholar.google.co.uk/scholar?q=Hadi%2C%20M.U.%20Al%20Tashi%2C%20Q.%20Shah%2C%20A.%20Qureshi%2C%20R.%20Large%20language%20models%3A%20a%20comprehensive%20survey%20of%20its%20applications%2C%20challenges%2C%20limitations%2C%20and%20future%20prospects%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Hadi%2C%20M.U.%20Al%20Tashi%2C%20Q.%20Shah%2C%20A.%20Qureshi%2C%20R.%20Large%20language%20models%3A%20a%20comprehensive%20survey%20of%20its%20applications%2C%20challenges%2C%20limitations%2C%20and%20future%20prospects%202024)
