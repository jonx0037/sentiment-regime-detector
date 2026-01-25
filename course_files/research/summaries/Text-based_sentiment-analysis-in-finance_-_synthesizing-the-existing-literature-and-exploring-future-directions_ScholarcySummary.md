[[Todd_et+al_TextbasedSentimentAnalysisFinanceSynthesising_2024]]

# [Text‐based sentiment analysis in finance: Synthesising the existing literature and exploring future directions](https://doi.org/10.1002/isaf.1549)

## [[Andrew Todd]]; [[James Bowden]]; [[Yashar Moshfeghi]]

## Abstract

Summary: Advances in Deep Learning have drastically improved the capabilities of Natural Language Processing (NLP) research, creating new state-of-the-art benchmarks. Two research streams at the forefront of NLP analysis are transformer architecture and multimodal analysis. This paper critically evaluates the extant literature applying sentiment analysis techniques to the financial domain. We classify the financial sentiment analysis literature according to the most used techniques in the area, with a focus on methods used to detect sentiment within corporate earnings conference calls, because of their dual modality (text‐audio) nature. We find that the financial literature follows a similar path to the NLP sentiment literature, in that more advanced techniques for defining sentiment are being used as the field progresses. However, the techniques used to determine financial sentiment currently lag state‐of‐the‐art NLP methods. Two future directions stem from this paper. Firstly, we propose adopting a transformer architecture to create robust representations of textual data, thereby enhancing sentiment analysis in academic finance. Secondly, the adoption of multimodal classifiers in finance represents a new, currently underexplored area of study that offers opportunities for finance research.

## Key concepts

# machine_learning; #social_media; #claim/sentiment_analysis; #sentiment_analysis; #finding/bidirectional_encoder_representations_from_transformers; #bidirectional_encoder_representations_from_transformers; #claim/transformer_architecture; #transformer_architecture; #finding/federal_open_markets_committee; #federal_open_markets_committee; #natural_language_processing

## Quote
>
> This paper critically evaluates the extant literature applying sentiment analysis techniques to the financial domain, focusing on methods used to detect sentiment within corporate earnings conference calls, and proposes the adoption of transformer architecture and multimodal classifiers to enhance sentiment analysis in academic finance.

## Key points

- Since the arrival of the internet on a commercial scale in the mid1990s, the manner in which information is delivered to investors, and how investors respond to such information, has been altered considerably ([^Nardo_et+al_2016_a])
- We expect to see the adoption and inclusion of state-of-the-art Natural Language Processing (NLP) techniques within academic finance over time, in regard to the adoption of transformer architectures to classify the textual modality of financial text
- Since the introduction of the transformer architecture by [^Vaswani_et+al_2017_a]), the adoption of the model has quickly solidified itself as the dominant architecture for NLP tasks ([^Wolf_et+al_2020_a]) with models such as Bidirectional Encoder Representations from Transformers (BERT), GPT3 and T5 all adopting said architecture and returning state of the art results in a plethora of tasks ([^Nogueira_2020_a]; [^Sun_et+al_2019_a])
- In a similar light to previous findings that specific word lists improve the understanding of sentiment for a specific context (e.g. [^Loughran_2011_a]), transformer architecture becomes even more impressive with context-specific pre-training
- In line with similar conclusions from psychology literature surrounding the importance of paralinguistic cues in the communication process, there are a number of studies employing sentiment analysis techniques that suggest a combination of text and audio data may improve classification accuracy, and create a more robust representation of sentiment ([^Bhaskar_et+al_2014_a]; [^Dair_et+al_2021_a]; [^Houjeij_et+al_2012_a]; [^Yang_et+al_2020_a])
- Given that prior literature suggests both textual and vocal characteristics of earnings calls to be informative, and that Natural Language Processing literature finds a combination of text and audio to significantly increase classification accuracy, the adhesion of both measures represents a natural future direction for the literature

## Summary

### Introduction To Sentiment Analysis

The paper critically evaluates the existing literature on sentiment analysis techniques in the financial domain, focusing on methods for detecting sentiment in corporate earnings conference calls.
The authors find that the financial literature follows a similar path to NLP sentiment literature, with more advanced techniques being used as the field progresses.
However, the techniques used to determine financial sentiment currently lag state-of-the-art NLP methods.

### Sentiment Analysis Techniques

The paper discusses various sentiment analysis techniques, including general dictionary approaches such as the Harvard IV psychosocial word lists and the General Inquirer (GI) system, which have been widely used in academic finance.
The authors also discuss domain-specific dictionary approaches, which have been shown to be more effective in classifying content in domain-specific settings.
The use of machine learning methods, such as GloVe and BERT, has also led to additional sentiment analysis methods in the academic literature.

### Future Directions

The paper proposes two future directions for sentiment analysis in finance: adopting a transformer architecture to create robust representations of textual data and adopting multimodal classifiers that incorporate audio, as well as textual, cues.
The authors highlight the potential of state-of-the-art methods for detecting and classifying financial sentiment, particularly in the context of earnings conference calls, which offer multiple modalities (text and audio) and can reduce information asymmetry.

### Sentiment Analysis

The market reaction to corporate press releases increases with the level of positive tone conveyed, and the use of financial dictionaries, such as the Loughran and McDonald (2011) dictionary, can help capture a more accurate measure of market response to earnings calls.
The LM dictionary has been widely used in the literature for word-count sentiment analysis, and studies have found that sentiment defined using this dictionary captures a more accurate measure of market response to earnings calls than general dictionary approaches.
The findings suggest that language extremity is strongly associated with analyst revisions, and analysts react more strongly to extreme positive language.
Sentiment analysis techniques are becoming more complex to capture more robust sentiment measures.
The use of advanced sentiment classification techniques, such as transformer architectures, can improve the understanding of market movements and sentiment.
Precision score is the number of positive class predictions that belong to the positive class, while recall score is the number of positive class predictions from all positive examples in the dataset.
The F1 score is a single metric that combines precision and recall.
Publicly available financial sentiment datasets include 4840 sentences from financial news, 10,000 sentences labelled as positive, negative, or neutral from analyst reports, and an open challenge dataset of 1111 sentences annotated for financial sentiment.

### Machine Learning

Machine learning approaches have been used to detect sentiment in financial texts, and studies have found that these approaches are more accurate at classifying financial sentiment than dictionary methods.
The probabilistic Naive Bayesian classifier is a commonly used ML algorithm for sentiment analysis, estimating the probability that a document is positive or negative based on its content.
Other studies have used more complex algorithms, such as the Reuters NewsScope Sentiment Engine, to evaluate sentiment in financial news and on social media.

### Natural Language Processing

State-of-the-art natural language processing methods have been used to analyze financial sentiment, and studies have found that these methods can provide more accurate sentiment measures than dictionary-based and machine learning approaches.
However, the field of accounting and finance lags behind NLP research in financial sentiment classification, and further research is needed to develop more accurate and complex models for sentiment analysis in finance.

### NLP Techniques

The application of advanced NLP techniques, such as transformer architecture and multimodal analysis, has been shown to improve financial sentiment classification.
Transformer architecture, introduced by Vaswani et al. (2017), relies solely on attention mechanisms and has achieved state-of-the-art results across various NLP tasks.
Multimodal analysis, which combines text, audio, and visual data, has also been shown to be more robust at classifying sentiment than singular-modality-based models.

### Multimodal Analysis

Multimodal sentiment analysis has been shown to provide additional behavioral cues and to capture sentiment more robustly.
The combination of text, audio, and visual data has been found to be more effective than bimodal and unimodal models.
However, there are limitations to multimodal sentiment analysis, including access to multimodal data, adhesion of different modalities into a successful classifier, and generalization of multimodal models.

### Sentiment Analysis On Earnings Calls

Earnings calls provide a rich source of information for sentiment analysis, as they contain natural language conversations surrounding firm performance.
Research has shown that the sentiment of earnings calls is significantly related to abnormal returns, post-earnings announcement drift, and abnormal trading volume.
The Q&A section of the call has been found particularly significant for predicting these outcomes, and the use of advanced NLP techniques, such as transformer architectures and multimodal analysis, may further improve the accuracy of sentiment analysis on earnings calls.

### Sentiment And Market Reaction

Earnings call sentiment has significant explanatory power over abnormal returns at the market level, with positive sentiment associated with higher abnormal returns and negative sentiment associated with lower abnormal returns.
Managers' sentiment during earnings calls can offset negative earnings surprises, and positive call sentiment can reduce the risk of a stock price crash.
Analyst sentiment also affects investor uncertainty, with negative sentiment heavily influencing it.

### Managerial Sentiment

Managerial sentiment and style have a significant impact on market reaction to earnings calls.
Managers' linguistic features, such as tone and language choice, can be used to detect financial reporting manipulation or misstatements.
Nonverbal communication, such as vocal cues, can also convey information about a manager's affective state and the firm's financial future.
Manager-specific optimism can influence the language used in earnings calls and impact market reaction.

### Analyst Sentiment

Analyst sentiment is significantly associated with stock prices and abnormal returns, with positive sentiment associated with positive abnormal returns.
Analyst sentiment is quickly incorporated into stock prices, and market participants place greater weight on analyst sentiment than on managerial sentiment.
Analyst compliments, or praise, are significantly and positively associated with abnormal earnings announcement stock returns and can be a robust predictor of positive firm performance.

### Future Research

Two main streams of future research are identified: the adoption of state-of-the-art NLP techniques, particularly transformer architectures, and the leveraging of both text and audio modalities to assess market characteristics.
The use of transformer architectures can improve classification accuracy and provide more robust sentiment representations.
The inclusion of nonverbal cues, such as vocal attributes, can also enhance the understanding of sentiment and market movements.

### Applications

The conclusions and future directions identified in this paper can be applied to various subdomains that leverage financial sentiment, such as financial fraud detection, sentiment classification across different languages, and government reporting assistance.
The application of transformer architecture and the leveraging of multiple modalities can benefit these areas of research, yielding more accurate and robust results.

### Paralinguistic Data

Paralinguistic data can be generated from earnings conference calls using speech analysis software, such as PRAAT, to create sentence-level audio clips and extract features like vocal pitch, intonation, and intensity.
Research has shown that these features impact speaker persuasion and listener perceptions/decision-making.
For example, a lower vocal pitch is associated with qualities such as credibility, tranquility, and trustworthiness.

### Financial Applications

The authors evaluate the relationship between stock returns and conference call content, including the tone of managerial introductory statements and analyst Q&A sessions.
They find that a one standard deviation shift in managerial introductory tone reflects a decrease in value uncertainty, while a one standard deviation shift in analyst Q&A tone reflects a decrease in value uncertainty.
Additionally, the authors find that manager-specific sentiment can be identified throughout different roles in their careers and can enhance the prediction of future operating performance.

## Study subjects

### 3 listed firms

- Across the three models discussed above, BERT performs particularly well on sentiment classification tasks ([^Alamoudi_2021_a]; [^Munikar_et+al_2019_a]; [^Sun_et+al_2019_a]). However, the only paper, to the authors' knowledge, to use BERT in the financial domain is [^Hiew_et+al_2019_a], which applies BERT to posts on the Chinese social media platform Weibo about three listed firms on the Hong Kong Stock Exchange. Exchange (HKSE)—Tencent, Ping An, and CCB

## Data analysis

- #method/finbert_model
- #method/dow_jones_internet_commerce_index
- #method/naïve_bayes_methods
- #method/german_deutscher_aktien_index
- #method/layered_voice_analysis_software
- #method/bert_model

## Findings

- [^Twedt_2012_a]) apply the <a class="keyword" href="#" title="General Inquirer">GI</a> to financial analyst reports and show that a change from the lowest quartile of analyst report tone (most pessimistic) to the highest quartile of analyst report tone (most optimistic) results in an average increase in return of 0.7%, holding all else equal
- The authors observe a classification accuracy of 73.3%
- When considering the calm sentiment indicator from <a class="keyword" href="#" title="Google Profile of Mood States">GPOMS</a> in addition to the previous prices, the accuracy increases to 86.7%
- Whereas a model only using financial variables returns a forecasting accuracy of 54.12%, the accuracy increases to 59.52% when including the sentiment measure
- Forecasting ability, when incorporating the sentiment conveyed within earnings releases, is found to increase by 5.4%
- [^Mao_et+al_2011_a]) create a negative news sentiment (<a class="keyword" href="#" title="negative news sentiment">NNS</a>) indicator by applying [^Loughran_2011_a]) negative word lexicon applied to financial news headlines, to evaluate the sentiment measures in relation to the <a class="keyword" href="#" title="Dow Jones Industrial Average">DJIA</a> market index. They find that the <a class="keyword" href="#" title="negative news sentiment">NNS</a> is significantly correlated to market log returns (À0.147)
- A one standard deviation increase in tweet sentiment on <a class="keyword" href="https://en.wikipedia.org/wiki/Federal_Open_Markets_Committee" title="Federal Open Markets Committee">FOMC</a> days results in an increase of 0.58% in returns the following day
- [^Brown_et+al_2020_a]) train an autoregressive language model (GPT3) on 175 billion parameters,35 of which returned the highest accuracy of 86.4% on the LAMBADA language modelling task.36
- The authors show that the general <a class="keyword" href="#" title="Bidirectional Encoder Representations from Transformers">BERT</a> model, not pretrained on any specific data only finetuned towards the specific tasks, performed competitively (80.5% accuracy, representing a 7.7% absolute improvement on <a class="keyword" href="#" title="General Language Understanding Evaluation">GLUE</a>).37
- Similar to traditional dictionary approaches, [^Howard_2018_a]) show that transformer model performance for text classification can be significantly improved when further pretrained on a domain-specific corpus
- Controlling for the numerical representation of the earnings surprise, the authors demonstrate that positive and negative earnings call sentiment—defined using the [^Henry_2006_a]) finance-specific dictionary—is significantly related to (i) abnormal returns during the initial earnings announcement window48; (ii) the post-earnings announcement drift; and (iii) abnormal trading volume
- Furthermore, the authors demonstrate that at the time of the call, managerial and analyst sentiment is significantly associated with stock prices,65, and overall positive (negative) sentiments are related to positive (negative) abnormal returns
- A one standard deviation increase in extreme language results in a 6.9% increase in abnormal trading volume

## Differs from previous work

- [^Borochin_et+al_2017_a]) also identify earnings calls as an important medium for disseminating information to the market. However, unlike previous studies, the authors focus on uncertainty rather than abnormal returns.53 The results indicate that higher levels of pessimism lead to greater pricing uncertainty, with higher levels of optimism creating the opposite effect.54 The authors separate earnings call sentiment into three distinct aspects: (i) the manager's sentiment during the call introduction; (ii) the manager's sentiment during the Q&A session; and (iii) the analyst sentiment during the Q&A.

## Confirmation of earlier findings

- Thus, forecasting ability, when incorporating the sentiment conveyed within earnings releases, is found to increase by 5.4%. A later study by [^Henry_2008_a] lends support to these findings by showing that greater levels of positive tone in corporate press releases are associated with higher abnormal returns, even after controlling for financial results.13 Furthermore, the market reaction increases with the level of positive tone conveyed, up until a certain point.14.
- However, the conclusions drawn and future directions identified in this paper can also be applied to various other subdomains that leverage financial sentiment. For example, research on financial fraud detection ([^Goel_2012_a]; [^Goel_2016_a]; [^Humpherys_et+al_2011_a]; [^Moffitt_2009_a]) follows the same pattern as the studies discussed in this review, in that most papers use dictionary- and machine-learning-based content analysis methods.

## Contributions

- Advances in Deep Learning have drastically improved the abilities of Natural Language Processing (NLP) research, creating new state-of-the-art benchmarks. <mark class="fact">Two research streams at the forefront of NLP analysis are transformer architecture</mark> and multimodal analysis. <mark class="claim">This paper critically evaluates the extant literature applying sentiment analysis techniques to the financial domain</mark>. We classify the financial sentiment analysis literature by the most commonly used techniques, with a focus on methods for detecting sentiment in corporate earnings conference calls due to their dual modality (text-audio). <mark class="claim"><mark class="fact">We find that the financial literature follows a similar path to NLP sentiment literature</mark>, in that <mark class="fact">more advanced techniques to define sentiment are being used as the field progresses</mark></mark>. However, the techniques used to determine financial sentiment currently lag state-of-the-art NLP methods. <mark class="fact">Two future directions stem from this paper</mark>. Firstly, <mark class="claim"><mark class="fact"><mark class="fact">we propose that the adoption of transformer architecture to create robust representations</mark></mark> of textual data could enhance sentiment analysis in academic finance</mark>. Secondly, the adoption of multimodal classifiers in finance represents a new, currently underexplored area of study that offers opportunities for finance research.

## Limitations

- The limitations of the study are that the bulk of the literature to date has been conducted with comparatively basic and well-established approaches that are less computationally demanding. The study also notes that nonverbal cues are virtually absent in the finance academic literature.
- The study highlights the limitations of transformer architectures, including high computational cost, large data requirements, and poor interpretability.

## Future work

- The future work proposed by the study involves the adoption of transformer architecture and multimodal classifiers to enhance sentiment analysis in academic finance. The study also proposes investigating future applications and extensions of text-based sentiment analysis.
- The study suggests that future research should focus on the adoption and inclusion of state-of-the-art NLP techniques, such as transformer architectures, and the incorporation of both text and audio modalities to analyze earnings calls sentiment.

## References

[^Alamoudi_2021_a]: Alamoudi, E., &amp; Alghamdi, N. (2021). Sentiment classification and aspect-based sentiment analysis on Yelp reviews using deep learning and word embeddings. Journal of Decision Systems, 30(2–3), 259–281. <https://doi.org/10.1080/12460125.2020.1864106>  [OA](https://doi.org/10.1080/12460125.2020.1864106)  [Scite](/scite_tallies?query=https://doi.org/10.1080/12460125.2020.1864106)

[^Bhaskar_et+al_2014_a]: Bhaskar, J., Sruthi, K., &amp; Nedungadi, P. (2014). Enhanced sentiment analysis of informal textual communication in social media by considering objective words and intensifiers. In International Conference on Recent Advances and Innovations in Engineering (ICRAIE-2014) (pp. 1–6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Bhaskar%2C%20J.%20Sruthi%2C%20K.%20Nedungadi%2C%20P.%20Enhanced%20sentiment%20analysis%20of%20informal%20textual%20communication%20in%20social%20media%20by%20considering%20objective%20words%20and%20intensifiers%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Bhaskar%2C%20J.%20Sruthi%2C%20K.%20Nedungadi%2C%20P.%20Enhanced%20sentiment%20analysis%20of%20informal%20textual%20communication%20in%20social%20media%20by%20considering%20objective%20words%20and%20intensifiers%202014)

[^Borochin_et+al_2017_a]: Borochin, P., Cicon, J., DeLisle, R., &amp; Price, S. (2017). The effects of conference call tones on market perceptions of value uncertainty. Journal of Financial Markets, 40, 75–91. <https://doi.org/10.1016/j.finmar.2017.12.003>  [OA](https://doi.org/10.1016/j.finmar.2017.12.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.finmar.2017.12.003)

[^Brown_et+al_2020_a]: Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., &amp; Agarwal, S. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877–1901.  [OA](https://engine.scholarcy.com/oa_version?query=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020&author=Brown&title=Language%20models%20are%20few-shot%20learners&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020) [Scite](/scite_tallies?query=author%3ABrown%2Ctitle%3ALanguage%20models%20are%20few-shot%20learners%2Cyear%3A2020)

[^Dair_et+al_2021_a]: Dair, Z., Donovan, R., &amp; O&#39;Reilly, R. (2021). Classification of emotive expression using verbal and non-verbal components of speech. In 2021 32nd Irish Signals and Systems Conference (ISSC) (pp. 1–8). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Dair%2C%20Z.%20Donovan%2C%20R.%20O%27Reilly%2C%20R.%20Classification%20of%20emotive%20expression%20using%20verbal%20and%20non-verbal%20components%20of%20speech%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Dair%2C%20Z.%20Donovan%2C%20R.%20O%27Reilly%2C%20R.%20Classification%20of%20emotive%20expression%20using%20verbal%20and%20non-verbal%20components%20of%20speech%202021)

[^Goel_2012_a]: Goel, S., &amp; Gangolly, J. (2012). Beyond the numbers: Mining the annual reports for hidden cues indicative of financial statement fraud. Intelligent Systems in Accounting, Finance and Management, 19(2), 75–89. <https://doi.org/10.1002/isaf.1326>  [OA](https://doi.org/10.1002/isaf.1326)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1326)

[^Goel_2016_a]: Goel, S., &amp; Uzuner, O. (2016). Do sentiments matter in fraud detection? Estimating semantic orientation of annual reports. Intelligent Systems in Accounting, Finance and Management, 23(3), 215–239. <https://doi.org/10.1002/isaf.1392>  [OA](https://doi.org/10.1002/isaf.1392)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1392)

[^Henry_2006_a]: Henry, E. (2006). Market reaction to verbal components of earnings press releases: Event study using a predictive algorithm. Journal of Emerging  [OA](https://engine.scholarcy.com/oa_version?query=Henry%2C%20E.%20Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%202006&author=Henry&title=Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Henry%2C%20E.%20Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%202006) [Scite](/scite_tallies?query=author%3AHenry%2Ctitle%3AMarket%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%2Cyear%3A2006)

[^Henry_2008_a]: Henry, E. (2008). Are investors influenced by how earnings press releases are written? Journal of Business Communication, 45(4), 363–407. <https://doi.org/10.1177/0021943608319388>  [OA](https://doi.org/10.1177/0021943608319388)  [Scite](/scite_tallies?query=https://doi.org/10.1177/0021943608319388)

[^Hiew_et+al_2019_a]: Hiew, J., Huang, X., Mou, H., Li, D., Wu, Q., &amp; Xu, Y. (2019). BERT-based financial sentiment index and LSTM-based stock return predictability. Cornell University Working Paper.  [OA](https://scholar.google.co.uk/scholar?q=Hiew%20J%20Huang%20X%20Mou%20H%20Li%20D%20Wu%20Q%20%20Xu%20Y%202019%20BERTbased%20financial%20sentiment%20index%20and%20LSTMbased%20stock%20return%20predictability%20Cornell%20University%20Working%20Paper) [GScholar](https://scholar.google.co.uk/scholar?q=Hiew%20J%20Huang%20X%20Mou%20H%20Li%20D%20Wu%20Q%20%20Xu%20Y%202019%20BERTbased%20financial%20sentiment%20index%20and%20LSTMbased%20stock%20return%20predictability%20Cornell%20University%20Working%20Paper)

[^Houjeij_et+al_2012_a]: Houjeij, A., Hamieh, L., Mehdi, N., &amp; Hajj, H. (2012). A novel approach for emotion classification based on fusion of text and speech. In 2012 19th International Conference on Telecommunications (ICT) (pp. 1–6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Houjeij%2C%20A.%20Hamieh%2C%20L.%20Mehdi%2C%20N.%20Hajj%2C%20H.%20A%20novel%20approach%20for%20emotion%20classification%20based%20on%20fusion%20of%20text%20and%20speech%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Houjeij%2C%20A.%20Hamieh%2C%20L.%20Mehdi%2C%20N.%20Hajj%2C%20H.%20A%20novel%20approach%20for%20emotion%20classification%20based%20on%20fusion%20of%20text%20and%20speech%202012)

[^Howard_2018_a]: Howard, J., &amp; Ruder, S. (2018). Universal language model fine-tuning for text classification. arXiv preprint arXiv:1801.06146.  [OA](https://arxiv.org/abs/1801.06146)  

[^Humpherys_et+al_2011_a]: Humpherys, S. L., Moffitt, K. C., Burns, M. B., Burgoon, J. K., &amp; Felix, W. F. (2011). Identification of fraudulent financial statements using linguistic credibility analysis. Decision Support Systems, 50(3), 585–594. <https://doi.org/10.1016/j.dss.2010.08.009>  [OA](https://doi.org/10.1016/j.dss.2010.08.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2010.08.009)

[^Loughran_2011_a]: Loughran, T., &amp; McDonald, B. (2011). When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35–65. <https://doi.org/10.1111/j.1540-6261.2010.01625.x>  [OA](https://doi.org/10.1111/j.1540-6261.2010.01625.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2010.01625.x)

[^Mao_et+al_2011_a]: Mao, H., Counts, S., &amp; Bollen, J. (2011). Predicting financial markets: Comparing survey, news, twitter and search engine data. arXiv preprint arXiv: 1112.1051.  [OA](https://arxiv.org/abs/1112.1051)  

[^Moffitt_2009_a]: Moffitt, K., &amp; Burns, M. B. (2009). What does that mean? Investigating obfuscation and readability cues as indicators of deception in fraudulent financial reports. In AMCIS 2009 Proceedings (p. 399).  [OA](https://scholar.google.co.uk/scholar?q=Moffitt%2C%20K.%20Burns%2C%20M.B.%20What%20does%20that%20mean%3F%20Investigating%20obfuscation%20and%20readability%20cues%20as%20indicators%20of%20deception%20in%20fraudulent%20financial%20reports%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Moffitt%2C%20K.%20Burns%2C%20M.B.%20What%20does%20that%20mean%3F%20Investigating%20obfuscation%20and%20readability%20cues%20as%20indicators%20of%20deception%20in%20fraudulent%20financial%20reports%202009)

[^Munikar_et+al_2019_a]: Munikar, M., Shakya, S., &amp; Shrestha, A. (2019). Fine-grained sentiment classification using BERT. In 2019 Artificial Intelligence for Transforming Business and Society (AITB) (Vol. 1, pp. 1–5). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Munikar%2C%20M.%20Shakya%2C%20S.%20Shrestha%2C%20A.%20Fine-grained%20sentiment%20classification%20using%20BERT%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Munikar%2C%20M.%20Shakya%2C%20S.%20Shrestha%2C%20A.%20Fine-grained%20sentiment%20classification%20using%20BERT%202019)

[^Nardo_et+al_2016_a]: Nardo, M., Petracco-Giudici, M., &amp; Naltsidis, M. (2016). Walking down wall street with a tablet: A survey of stock market predictions using the web. Journal of Economic Surveys, 30(2), 356–369. <https://doi.org/10.1111/joes.12102>  [OA](https://doi.org/10.1111/joes.12102)  [Scite](/scite_tallies?query=https://doi.org/10.1111/joes.12102)

[^Nogueira_2020_a]: Nogueira, R., &amp; Cho, K. (2020). Passage re-ranking with BERT. Cornell University Working Paper.  [OA](https://scholar.google.co.uk/scholar?q=Nogueira%2C%20R.%20Cho%2C%20K.%20Passage%20re-ranking%20with%20BERT%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Nogueira%2C%20R.%20Cho%2C%20K.%20Passage%20re-ranking%20with%20BERT%202020)

[^Sun_et+al_2019_a]: Sun, C., Qiu, X., Xu, Y., &amp; Huang, X. (2019). How to fine-tune BERT for text classification? In Chinese Computational Linguistics: 18th China National Conference, CCL 2019, Kunming, China, October 18–20, 2019, Proceedings 18 (pp. 194–206). Springer International Publishing.  [OA](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20fine-tune%20BERT%20for%20text%20classification%3F%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20fine-tune%20BERT%20for%20text%20classification%3F%202019)

[^Twedt_2012_a]: Twedt, B., &amp; Rees, L. (2012). Reading between the lines: An empirical examination of qualitative attributes of financial analysts&#39; reports. Journal of Accounting and Public Policy, 31(1), 1–21. <https://doi.org/10.1016/j.jaccpubpol.2011.10.010>  [OA](https://doi.org/10.1016/j.jaccpubpol.2011.10.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jaccpubpol.2011.10.010)

[^Vaswani_et+al_2017_a]: Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., &amp; Polosukhin, I. (2017). Attention Is All You Need. Advances in neural information processing systems, 30.  [OA](https://engine.scholarcy.com/oa_version?query=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20Is%20All%20You%20Need%202017&author=Vaswani&title=Attention%20Is%20All%20You%20Need&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20Is%20All%20You%20Need%202017) [Scite](/scite_tallies?query=author%3AVaswani%2Ctitle%3AAttention%20Is%20All%20You%20Need%2Cyear%3A2017)

[^Wolf_et+al_2020_a]: Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz, M., Davison, J., Shleifer, S., von Platen, P., Ma, C., Jernite, Y., Plu, J., Xu, C., Le Scao, T., Gugger, S.,... Rush, A. (2020). Transformers: State-of-the-art natural language processing. In Proceedings of the 2020 conference on empirical methods in natural language processing: System demonstrations (pp. 38–45).  [OA](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020)

[^Yang_et+al_2020_a]: Yang, K., Xu, H., &amp; Gao, K. (2020). CM-BERT: Cross-modal bert for textaudio sentiment analysis. In Proceedings of the 28th ACM International Conference on Multimedia (pp. 521–528).  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20K.%20Xu%2C%20H.%20Gao%2C%20K.%20CM-BERT%3A%20Cross-modal%20bert%20for%20textaudio%20sentiment%20analysis%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20K.%20Xu%2C%20H.%20Gao%2C%20K.%20CM-BERT%3A%20Cross-modal%20bert%20for%20textaudio%20sentiment%20analysis%202020)
