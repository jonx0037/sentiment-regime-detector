[[Todd_et+al_TextbasedSentimentAnalysisFinanceSynthesising_2024]]

# [Text‐based sentiment analysis in finance: Synthesising the existing literature and exploring future directions](https://doi.org/10.1002/isaf.1549)

## [[Andrew Todd]]; [[James Bowden]]; [[Yashar Moshfeghi]]

## Abstract
Summary: Advances in Deep Learning have drastically improved the capabilities of Natural Language Processing (NLP) research, creating new state-of-the-art benchmarks. Two research streams at the forefront of NLP analysis are transformer architecture and multimodal analysis. This paper critically evaluates the extant literature applying sentiment analysis techniques to the financial domain. We classify the financial sentiment analysis literature according to the most used techniques in the area, with a focus on methods used to detect sentiment within corporate earnings conference calls, because of their dual modality (text‐audio) nature. We find that the financial literature follows a similar path to the NLP sentiment literature, in that more advanced techniques for defining sentiment are being used as the field progresses. However, the techniques used to determine financial sentiment currently lag state‐of‐the‐art NLP methods. Two future directions stem from this paper. Firstly, we propose adopting a transformer architecture to create robust representations of textual data, thereby enhancing sentiment analysis in academic finance. Secondly, the adoption of multimodal classifiers in finance represents a new, currently underexplored area of study that offers opportunities for finance research.

## Key concepts
#machine_learning; #finding/federal_open_markets_committee; #federal_open_markets_committee; #natural_language_processing; #claim/transformer_architecture; #transformer_architecture; #finding/bidirectional_encoder_representations_from_transformers; #bidirectional_encoder_representations_from_transformers; #claim/sentiment_analysis; #sentiment_analysis; #social_media

## Quote
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
Transformer architecture, introduced by Vaswani et al (2017), is a model that relies solely on attention mechanisms and has achieved state-of-the-art results in various NLP tasks.
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
Managers' sentiment during earnings calls can offset negative earnings surprises, and positive call sentiment can reduce stock price crash risk.
Analyst sentiment also affects investor uncertainty, with negative sentiment strongly influencing it.

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
The conclusions and future directions identified in this paper can be applied to various subdomains that leverage financial sentiment, such as financial fraud detection, sentiment classification in different languages, and assisting government reporting.
The application of transformer architecture and the leveraging of multiple modalities can benefit these areas of research, yielding more accurate and robust results.

### Paralinguistic Data
Paralinguistic data can be generated from earnings conference calls using speech analysis software, such as PRAAT, to create sentence-level audio clips and extract features like vocal pitch, intonation, and intensity.
Research has shown that these features impact speaker persuasion and listener perceptions/decision-making.
For example, a lower vocal pitch is associated with qualities such as credibility, tranquility, and trustworthiness.

### Financial Applications
The authors evaluate the relationship between stock returns and conference call content, including the tone of managerial introductory statements and analyst Q&A sessions.
They find that a one standard deviation shift in managerial introductory tone reflects a decrease in value uncertainty, while a one standard deviation shift in analyst Q&A tone reflects a decrease in value uncertainty.
Additionally, the authors find that manager-specific sentiment can be identified throughout different roles in their career and can enhance the prediction of future operating performance.


## Study subjects

### 3 listed firms
- Across the three models discussed above, BERT performs particularly well on sentiment classification tasks ([^Alamoudi_2021_a]; [^Munikar_et+al_2019_a]; [^Sun_et+al_2019_a]). However, the only paper to the authors' knowledge to use BERT in the financial domain is [^Hiew_et+al_2019_a], which applies BERT to posts on the Chinese social media platform Weibo relating to three listed firms on the Hong Kong Stock. Exchange (HKSE)—Tencent, Ping An, and CCB

## Data analysis
- #method/layered_voice_analysis_software
- #method/naïve_bayes_methods
- #method/dow_jones_internet_commerce_index
- #method/bert_model
- #method/finbert_model
- #method/german_deutscher_aktien_index

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
- Similar to traditional dictionary approaches, [^Howard_2018_a], show that transformer model performance for text classification can be significantly improved when further pretrained on a domain-specific corpus
- Controlling for the numerical representation of the earnings surprise, the authors demonstrate that positive and negative earnings call sentiment—defined using the [^Henry_2006_a]) finance-specific dictionary—is significantly related to (i) abnormal returns during the initial earnings announcement window48; (ii) the post-earnings announcement drift; and (iii) abnormal trading volume
- Furthermore, the authors demonstrate that at the time of the call, managerial and analyst sentiment is significantly associated with stock prices,65, and overall positive (negative) sentiments are related to positive (negative) abnormal returns
- A one standard deviation increase in extreme language results in a 6.9% increase in abnormal trading volume

## Differs from previous work
- [^Borochin_et+al_2017_a]) also identify earnings calls as an important medium for disseminating information to the market. However, unlike previous studies, the authors focus on uncertainty rather than abnormal returns.53 The results indicate that higher levels of pessimism lead to greater pricing uncertainty, with higher levels of optimism creating the opposite effect.54 The authors separate earnings call sentiment into three distinct aspects: (i) the manager's sentiment during the call introduction; (ii) the manager's sentiment during the Q&A session; and (iii) the analyst sentiment during the Q&A.

##  Confirmation of earlier findings
- Thus, forecasting ability, when incorporating the sentiment conveyed within earnings releases, is found to increase by 5.4%. A later study by [^Henry_2008_a]) lends support to these findings through the identification that greater levels of positive tone within corporate press releases result in higher abnormal returns even after controlling for financial results.13 Furthermore, the market reaction increases with the level of positive tone conveyed, up until a certain point.14.
- However, the conclusions drawn and future directions identified in this paper can also be applied to various other subdomains that leverage financial sentiment. For example, research on financial fraud detection ([^Goel_2012_a]; [^Goel_2016_a]; [^Humpherys_et+al_2011_a]; [^Moffitt_2009_a]) follows the same pattern as the studies discussed in this review, in that most papers use dictionary- and machine-learning-based content analysis methods.

## Contributions
- Advances in Deep Learning have drastically improved the abilities of Natural Language Processing (NLP) research, creating new state-of-the-art benchmarks. <mark class="fact">Two research streams at the forefront of NLP analysis are transformer architecture</mark> and multimodal analysis. <mark class="claim">This paper critically evaluates the extant literature applying sentiment analysis techniques to the financial domain</mark>. We classify the financial sentiment analysis literature by the most commonly used techniques, with a focus on methods for detecting sentiment in corporate earnings conference calls, given their dual modality (text-audio) nature. <mark class="claim"><mark class="fact">We find that the financial literature follows a similar path to NLP sentiment literature</mark>, in that <mark class="fact">more advanced techniques to define sentiment are being used as the field progresses</mark></mark>. However, the techniques used to determine financial sentiment currently lag state-of-the-art NLP methods. <mark class="fact">Two future directions stem from this paper</mark>. Firstly, <mark class="claim"><mark class="fact"><mark class="fact">we propose that the adoption of transformer architecture to create robust representations</mark></mark> of textual data could enhance sentiment analysis in academic finance</mark>. Secondly, the adoption of multimodal classifiers in finance represents a new, currently underexplored area of study that offers opportunities for finance research.

## Limitations
- The limitations of the study are that the bulk of the literature to date has been conducted with comparatively basic and well-established approaches that are less computationally demanding. The study also notes that nonverbal cues are virtually absent in the finance academic literature.
- The study highlights the limitations of transformer architectures, including high computational cost, large data requirements, and poor interpretability.

## Future work
- The future work proposed by the study involves the adoption of transformer architecture and multimodal classifiers to enhance sentiment analysis in academic finance. The study also proposes investigating future applications and extensions of text-based sentiment analysis.
- The study suggests that future research should focus on the adoption and inclusion of state-of-the-art NLP techniques, such as transformer architectures, and the incorporation of both text and audio modalities to analyze earnings calls sentiment.


## References
[^Abirami_2016_a]: Abirami, A. M., &amp; Gayathri, V. (2016). A survey on sentiment analysis methods and approaches. In 2016, IEEE Eighth International Conference on Advanced Computing (ICoAC) (pp. 72–76). Institute of Electrical and Electronics Engineers.  [OA](https://scholar.google.co.uk/scholar?q=Abirami%2C%20A.M.%20Gayathri%2C%20V.%20A%20survey%20on%20sentiment%20analysis%20methods%20and%20approach%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Abirami%2C%20A.M.%20Gayathri%2C%20V.%20A%20survey%20on%20sentiment%20analysis%20methods%20and%20approach%202016) 

[^Alamoudi_2021_a]: Alamoudi, E., &amp; Alghamdi, N. (2021). Sentiment classification and aspect-based sentiment analysis on Yelp reviews using deep learning and word embeddings. Journal of Decision Systems, 30(2–3), 259–281. https://doi.org/10.1080/12460125.2020.1864106  [OA](https://doi.org/10.1080/12460125.2020.1864106)  [Scite](/scite_tallies?query=https://doi.org/10.1080/12460125.2020.1864106)

[^Allen_et+al_2021_a]: Allen, E., O'Leary, D. E., Qu, H., & Swenson, C. W. (2021). Tax-specific versus generic accounting-based textual analysis and the relationship with effective tax rates: Building context. Journal of Information Systems, 35(2), 115–147. https://doi.org/10.2308/ISYS-2020-018  [OA](https://doi.org/10.2308/ISYS-2020-018)  [Scite](/scite_tallies?query=https://doi.org/10.2308/ISYS-2020-018)

[^Amoozegar_et+al_2020_a]: Amoozegar, A., Berger, D., Cao, X., &amp; Pukthuanthong, K. (2020). Earnings conference calls and institutional monitoring: Evidence from textual analysis. Journal of Financial Research, 43(1), 5–36. https://doi.org/10.1111/jfir.12199  [OA](https://doi.org/10.1111/jfir.12199)  [Scite](/scite_tallies?query=https://doi.org/10.1111/jfir.12199)

[^Antweiler_2004_a]: Antweiler, W., &amp; Frank, M. (2004). Is all that talk just noise? The information content of internet stock message boards. The Journal of Finance, 59(3), 1259–1294. https://doi.org/10.1111/j.1540-6261.2004.00662.x  [OA](https://doi.org/10.1111/j.1540-6261.2004.00662.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2004.00662.x)

[^Apple_et+al_1979_a]: Apple, W., Streeter, L. A., &amp; Krauss, R. M. (1979). Effects of pitch and speech rate on personal attributions. Journal of Personality and Social Psychology, 37(5), 715–727. https://doi.org/10.1037/0022-3514.37.5.715  [OA](https://doi.org/10.1037/0022-3514.37.5.715)  [Scite](/scite_tallies?query=https://doi.org/10.1037/0022-3514.37.5.715)

[^Asur_2010_a]: Asur, S., &amp; Huberman, B. A. (2010). Predicting the future with social media. In 2010, IEEE/WIC/ACM International Conference on Web Intelligence and Intelligent Agent Technology (Vol. 1, pp. 492–499). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Asur%2C%20S.%20Huberman%2C%20B.A.%20Predicting%20the%20future%20with%20social%20media%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Asur%2C%20S.%20Huberman%2C%20B.A.%20Predicting%20the%20future%20with%20social%20media%202010) 

[^Audrino_2019_a]: Audrino, F., & Tetereva, A. (2019). Sentiment spillover effects for US and European companies. Journal of Banking &amp; Finance, 106, 542–567. https://doi.org/10.1016/j.jbankfin.2019.07.022  [OA](https://doi.org/10.1016/j.jbankfin.2019.07.022)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2019.07.022)

[^Azar_2016_a]: Azar, P., &amp; Lo, A. (2016). The wisdom of Twitter crowds: Predicting stock market reactions to FOMC meetings via Twitter feeds. The Journal of Portfolio Management, 42(5), 123–134. https://doi.org/10.3905/jpm.2016.42.5.123  [OA](https://doi.org/10.3905/jpm.2016.42.5.123)  [Scite](/scite_tallies?query=https://doi.org/10.3905/jpm.2016.42.5.123)

[^Bannier_et+al_2017_a]: Bannier, C., Pauls, T., & Walter, A. (2017). CEO-speeches and stock returns (Vol. 583). Center for Financial Studies.  [OA](https://scholar.google.co.uk/scholar?q=Bannier%2C%20C.%20Pauls%2C%20T.%20Walter%2C%20A.%20CEO-speeches%20and%20stock%20returns%20%28Vol.%20583%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Bannier%2C%20C.%20Pauls%2C%20T.%20Walter%2C%20A.%20CEO-speeches%20and%20stock%20returns%20%28Vol.%20583%202017) 

[^Bernanke_2005_a]: Bernanke, B., &amp; Kuttner, K. (2005). What explains the stock market&#39;s reaction to federal reserve policy? The Journal of Finance, 60(3), 1221– 1257. https://doi.org/10.1111/j.1540-6261.2005.00760.x  [OA](https://doi.org/10.1111/j.1540-6261.2005.00760.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2005.00760.x)

[^Bhaskar_et+al_2014_a]: Bhaskar, J., Sruthi, K., &amp; Nedungadi, P. (2014). Enhanced sentiment analysis of informal textual communication in social media by considering objective words and intensifiers. In International Conference on Recent Advances and Innovations in Engineering (ICRAIE-2014) (pp. 1–6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Bhaskar%2C%20J.%20Sruthi%2C%20K.%20Nedungadi%2C%20P.%20Enhanced%20sentiment%20analysis%20of%20informal%20textual%20communication%20in%20social%20media%20by%20considering%20objective%20words%20and%20intensifiers%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Bhaskar%2C%20J.%20Sruthi%2C%20K.%20Nedungadi%2C%20P.%20Enhanced%20sentiment%20analysis%20of%20informal%20textual%20communication%20in%20social%20media%20by%20considering%20objective%20words%20and%20intensifiers%202014) 

[^Bhonde_et+al_2015_a]: Bhonde, R., Bhagwat, B., Ingulkar, S., &amp; Pande, A. (2015). Sentiment analysis based on a dictionary approach. International Journal of Emerging Engineering Research and Technology, 3(1), 51–54.  [OA](https://engine.scholarcy.com/oa_version?query=Bhonde%2C%20R.%20Bhagwat%2C%20B.%20Ingulkar%2C%20S.%20Pande%2C%20A.%20Sentiment%20analysis%20based%20on%20dictionary%20approach%202015&author=Bhonde&title=Sentiment%20analysis%20based%20on%20dictionary%20approach&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Bhonde%2C%20R.%20Bhagwat%2C%20B.%20Ingulkar%2C%20S.%20Pande%2C%20A.%20Sentiment%20analysis%20based%20on%20dictionary%20approach%202015) [Scite](/scite_tallies?query=author%3ABhonde%2Ctitle%3ASentiment%20analysis%20based%20on%20dictionary%20approach%2Cyear%3A2015)

[^Blau_et+al_2015_a]: Blau, B., DeLisle, J., &amp; Price, S. (2015). Do sophisticated investors interpret earnings conference call tone differently than investors at large? Evidence from short sales. Journal of Corporate Finance, 31, 203–219. https://doi.org/10.1016/j.jcorpfin.2015.02.003  [OA](https://doi.org/10.1016/j.jcorpfin.2015.02.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jcorpfin.2015.02.003)

[^Blume_et+al_1994_a]: Blume, L., Easley, D., &amp; O&#39;Hara, M. (1994). Market statistics and technical analysis: The role of volume. The Journal of Finance, 49(1), 153–181. https://doi.org/10.1111/j.1540-6261.1994.tb04424.x  [OA](https://doi.org/10.1111/j.1540-6261.1994.tb04424.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.1994.tb04424.x)

[^Bochkay_et+al_2020_a]: Bochkay, K., Hales, J., &amp; Chava, S. (2020). Hyperbole or reality? Investor response to extreme language in earnings conference calls. The Accounting Review, 95(2), 31–60. https://doi.org/10.2308/accr-52507  [OA](https://doi.org/10.2308/accr-52507)  [Scite](/scite_tallies?query=https://doi.org/10.2308/accr-52507)

[^Bollen_et+al_2011_a]: Bollen, J., Mao, H., &amp; Zeng, X. (2011). Twitter mood predicts the stock market. Journal of Computational Science, 2(1), 1–8. https://doi.org/10.1016/j.jocs.2010.12.007  [OA](https://doi.org/10.1016/j.jocs.2010.12.007)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jocs.2010.12.007)

[^Borochin_et+al_2017_a]: Borochin, P., Cicon, J., DeLisle, R., &amp; Price, S. (2017). The effects of conference call tones on market perceptions of value uncertainty. Journal of Financial Markets, 40, 75–91. https://doi.org/10.1016/j.finmar.2017.12.003  [OA](https://doi.org/10.1016/j.finmar.2017.12.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.finmar.2017.12.003)

[^Borth_et+al_2013_a]: Borth, D., Ji, R., Chen, T., Breuel, T., &amp; Chang, S. F. (2013). Large-scale visual sentiment ontology and detectors using adjective noun pairs. In Proceedings of the 21st ACM International Conference on Multimedia (pp. 223–232).  [OA](https://scholar.google.co.uk/scholar?q=Borth%2C%20D.%20Ji%2C%20R.%20Chen%2C%20T.%20Breuel%2C%20T.%20Large-scale%20visual%20sentiment%20ontology%20and%20detectors%20using%20adjective%20noun%20pairs%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Borth%2C%20D.%20Ji%2C%20R.%20Chen%2C%20T.%20Breuel%2C%20T.%20Large-scale%20visual%20sentiment%20ontology%20and%20detectors%20using%20adjective%20noun%20pairs%202013) 

[^Bowden_et+al_2019_a]: Bowden, J., Kwiatkowski, A., &amp; Rambaccussing, D. (2019). Economy through a lens: Distortions of policy coverage in UK national newspapers. Journal of Comparative Economics, 47(4), 881–906. https://doi.org/10.1016/j.jce.2019.07.002  [OA](https://doi.org/10.1016/j.jce.2019.07.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jce.2019.07.002)

[^Bowen_et+al_2002_a]: Bowen, R. M., Davis, A. K., &amp; Matsumoto, D. A. (2002). Do conference calls affect analysts' forecasts? The Accounting Review, 77(2), 285–316. https://doi.org/10.2308/accr.2002.77.2.285  [OA](https://doi.org/10.2308/accr.2002.77.2.285)  [Scite](/scite_tallies?query=https://doi.org/10.2308/accr.2002.77.2.285)

[^Bradac_et+al_1988_a]: Bradac, J. J., Mulac, A., &amp; House, A. (1988). Lexical diversity and magnitude of convergent versus divergent style shifting: Perceptual and evaluative consequences. Language and Communication, 8(3–4), 213–228. https://doi.org/10.1016/0271-5309(88)90019-5  [OA](https://doi.org/10.1016/0271-5309(88)90019-5)  [Scite](/scite_tallies?query=https://doi.org/10.1016/0271-5309(88)90019-5)

[^Brockman_et+al_2015_a]: Brockman, P., Li, X., &amp; Price, S. (2015). Differences in conference call tones: Managers vs. analysts. Financial Analysts Journal, 71(4), 24–42. https://doi.org/10.2469/faj.v71.n4.1  [OA](https://doi.org/10.2469/faj.v71.n4.1)  [Scite](/scite_tallies?query=https://doi.org/10.2469/faj.v71.n4.1)

[^Brooke_1986_a]: Brooke, M. E., &amp; Ng, S. H. (1986). Language and social influence in small conversational groups. Journal of Language and Social Psychology, 5(3), 201–210. https://doi.org/10.1177/0261927X8600500303  [OA](https://doi.org/10.1177/0261927X8600500303)  [Scite](/scite_tallies?query=https://doi.org/10.1177/0261927X8600500303)

[^Brown_et+al_2020_a]: Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., &amp; Agarwal, S. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877–1901.  [OA](https://engine.scholarcy.com/oa_version?query=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020&author=Brown&title=Language%20models%20are%20few-shot%20learners&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Brown%2C%20T.%20Mann%2C%20B.%20Ryder%2C%20N.%20Subbiah%2C%20M.%20Language%20models%20are%20few-shot%20learners%202020) [Scite](/scite_tallies?query=author%3ABrown%2Ctitle%3ALanguage%20models%20are%20few-shot%20learners%2Cyear%3A2020)

[^Cambria_2014_a]: Cambria, E., &amp; White, B. (2014). Jumping NLP curves: A review of natural language processing research [Review Article]. IEEE Computational Intelligence Magazine, 9(2), 48–57. https://doi.org/10.1109/MCI.2014.2307227  [OA](https://doi.org/10.1109/MCI.2014.2307227)  [Scite](/scite_tallies?query=https://doi.org/10.1109/MCI.2014.2307227)

[^Chan_et+al_2021_a]: Chan, C., Bajjalieh, J., Auvil, L., Wessler, H., Althaus, S., Welbers, K., van Atteveldt, W., &; Jungblut, M. (2021). Four best practices for measuring news sentiment using ‘off-the-shelf’ dictionaries: A large-scale p-hacking experiment. Computational Communication Research, 3(1), 1– 27. https://doi.org/10.5117/CCR2021.1.001.CHAN  [OA](https://doi.org/10.5117/CCR2021.1.001.CHAN)  [Scite](/scite_tallies?query=https://doi.org/10.5117/CCR2021.1.001.CHAN)

[^Chan_2017_a]: Chan, S. W., &amp; Chong, M. W. (2017). Sentiment analysis in financial texts. Decision Support Systems, 94, 53–64. https://doi.org/10.1016/j.dss.2016.10.006  [OA](https://doi.org/10.1016/j.dss.2016.10.006)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2016.10.006)

[^Chan_2003_a]: Chan, W. S. (2003). Stock price reaction to news and no-news: Drift and reversal after headlines. Journal of Financial Economics, 70(2), 223– 260. https://doi.org/10.1016/S0304-405X(03)00146-6  [OA](https://doi.org/10.1016/S0304-405X(03)00146-6)  [Scite](/scite_tallies?query=https://doi.org/10.1016/S0304-405X(03)00146-6)

[^Chattopadhyay_et+al_2003_a]: Chattopadhyay, A., Dahl, D. W., Ritchie, R. J., &amp; Shahin, K. N. (2003). Hearing voices: The impact of announcer speech characteristics on consumer response to broadcast advertising. Journal of Consumer Psychology, 13(3), 198–204. https://doi.org/10.1207/S15327663JCP1303_02  [OA](https://doi.org/10.1207/S15327663JCP1303_02)  [Scite](/scite_tallies?query=https://doi.org/10.1207/S15327663JCP1303_02)

[^Chen_et+al_2018_a]: Chen, J., Nagar, V., &amp; Schoenfeld, J. (2018). Manager-analyst conversations in earnings conference calls. Review of Accounting Studies, 23(4), 1315–1354. https://doi.org/10.1007/s11142-018-9453-3  [OA](https://doi.org/10.1007/s11142-018-9453-3)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11142-018-9453-3)

[^Chua_et+al_2020_a]: Chua, G. Y. P., Er, H. J., Liaw, S. Y., &; He, T. S. (2020). Pitch right: The effect of vocal pitch on risk aversion. Economics Bulletin, 40(4), 3131–3139.  [OA](https://engine.scholarcy.com/oa_version?query=Chua%2C%20G.Y.P.%20Er%2C%20H.J.%20Liaw%2C%20S.Y.%20He%2C%20T.S.%20Pitch%20right%3A%20The%20effect%20of%20vocal%20pitch%20on%20risk%20aversion%202020&author=Chua&title=Pitch%20right%3A%20The%20effect%20of%20vocal%20pitch%20on%20risk%20aversion&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Chua%2C%20G.Y.P.%20Er%2C%20H.J.%20Liaw%2C%20S.Y.%20He%2C%20T.S.%20Pitch%20right%3A%20The%20effect%20of%20vocal%20pitch%20on%20risk%20aversion%202020) [Scite](/scite_tallies?query=author%3AChua%2Ctitle%3APitch%20right%3A%20The%20effect%20of%20vocal%20pitch%20on%20risk%20aversion%2Cyear%3A2020)

[^Chung_et+al_2014_a]: Chung, J., Gulcehre, C., Cho, K., &; Bengio, Y. (2014). Empirical evaluation of gated recurrent neural networks on sequence modelling in Deep learning and representation learning workshop. Neural Information Processing Systems.  [OA](https://scholar.google.co.uk/scholar?q=Chung%2C%20J.%20Gulcehre%2C%20C.%20Cho%2C%20K.%20Bengio%2C%20Y.%20Empirical%20evaluation%20of%20gated%20recurrent%20neural%20networks%20on%20sequence%20modelling%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Chung%2C%20J.%20Gulcehre%2C%20C.%20Cho%2C%20K.%20Bengio%2C%20Y.%20Empirical%20evaluation%20of%20gated%20recurrent%20neural%20networks%20on%20sequence%20modelling%202014) 

[^Cieslak_et+al_2014_a]: Cieslak, A., Morse, A., &amp; Vissing-Jorgensen, A. (2014). Stock returns over the FOMC cycle. NBER Working Paper. https://doi.org/10.2139/ssrn.2687614  [OA](https://doi.org/10.2139/ssrn.2687614)  [Scite](/scite_tallies?query=https://doi.org/10.2139/ssrn.2687614)

[^Conley_et+al_1978_a]: Conley, J. M., O&#39;Barr, W. M., &amp; Lind, E. A. (1978). The power of language: Presentational style in the courtroom (Vol. 1978) (p. 1375). Duke Lj. https://doi.org/10.2307/1372218  [OA](https://doi.org/10.2307/1372218)  [Scite](/scite_tallies?query=https://doi.org/10.2307/1372218)

[^Dair_et+al_2021_a]: Dair, Z., Donovan, R., &amp; O&#39;Reilly, R. (2021). Classification of emotive expression using verbal and non-verbal components of speech. In 2021 32nd Irish Signals and Systems Conference (ISSC) (pp. 1–8). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Dair%2C%20Z.%20Donovan%2C%20R.%20O%27Reilly%2C%20R.%20Classification%20of%20emotive%20expression%20using%20verbal%20and%20non-verbal%20components%20of%20speech%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Dair%2C%20Z.%20Donovan%2C%20R.%20O%27Reilly%2C%20R.%20Classification%20of%20emotive%20expression%20using%20verbal%20and%20non-verbal%20components%20of%20speech%202021) 

[^D&#39;Andrea_et+al_2019_a]: D&#39;Andrea, E., Ducange, P., Bechini, A., Renda, A., &amp; Marcelloni, F. (2019). Monitoring public opinion on vaccination through tweet analysis. Expert Systems with Applications, 116, 209–226. https://doi.org/10.1016/j.eswa.2018.09.009  [OA](https://doi.org/10.1016/j.eswa.2018.09.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2018.09.009)

[^Daudert_2021_a]: Daudert, T. (2021). Exploiting textual and relationship information for fine-grained financial sentiment analysis. Knowledge-Based Systems, 230, 107389. https://doi.org/10.1016/j.knosys.2021.107389  [OA](https://doi.org/10.1016/j.knosys.2021.107389)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.knosys.2021.107389)

[^Davis_et+al_2015_a]: Davis, A., Ge, W., Matsumoto, D., &amp; Zhang, J. (2015). The effect of manager-specific optimism on the tone of earnings conference calls. Review of Accounting Studies, 20(2), 639–673. https://doi.org/10.1007/s11142-014-9309-4  [OA](https://doi.org/10.1007/s11142-014-9309-4)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11142-014-9309-4)

[^Davis_et+al_2012_a]: Davis, A. K., Ge, W., Matsumoto, D., &amp; Zhang, J. L. (2012). The effect of managerial “style” on the tone of earnings conference calls. In the CAAA Annual Conference. Retrieved from http://www.usc.edu/schools/business/FBE/seminars/papers/ARF_9-21-12_GE.pdf  [OA](http://www.usc.edu/schools/business/FBE/seminars/papers/ARF_9-21-12_GE.pdf)  

[^Davis_2012_b]: Davis, A., &amp; Tama-Sweet, I. (2012). Managers&#39 use of language across alternative disclosure outlets: Earnings press releases versus MD&A*. Contemporary Accounting Research, 29(3), 804–837. https://doi.org/10.1111/j.1911-3846.2011.01125.x  [OA](https://doi.org/10.1111/j.1911-3846.2011.01125.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1911-3846.2011.01125.x)

[^Devlin_et+al_2019_a]: Devlin, J., Chang, M. W., Lee, K., &amp; Toutanova, K. (2019). Bert: Pre-training of deep bidirectional Transformers for language understanding. arXiv preprint arXiv:1810.04805.  [OA](https://arxiv.org/abs/1810.04805)  

[^Dey_et+al_2016_a]: Dey, L., Chakraborty, S., Biswas, A., Bose, B., &amp; Tiwari, S. (2016). Sentiment analysis of review datasets using Naïve Bayes&#39; and K-NN classifier. International Journal of Information Engineering and Electronic Business, 8(4), 54–62. https://doi.org/10.5815/ijieeb.2016.04.07  [OA](https://doi.org/10.5815/ijieeb.2016.04.07)  [Scite](/scite_tallies?query=https://doi.org/10.5815/ijieeb.2016.04.07)

[^Diesner_2015_a]: Diesner, J., &amp; Evans, C. (2015). Little bad concerns: Using sentiment analysis to assess structural balance in communication networks. In Proceedings of the 2015 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining 2015 (pp. 342–348).  [OA](https://scholar.google.co.uk/scholar?q=Diesner%2C%20J.%20Evans%2C%20C.%20Little%20bad%20concerns%3A%20Using%20sentiment%20analysis%20to%20assess%20structural%20balance%20in%20communication%20networks%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Diesner%2C%20J.%20Evans%2C%20C.%20Little%20bad%20concerns%3A%20Using%20sentiment%20analysis%20to%20assess%20structural%20balance%20in%20communication%20networks%202015) 

[^Doran_et+al_2012_a]: Doran, J., Peterson, D., &; Price, S. (2012). Earnings conference call content and stock price: The case of REITs. The Journal of Real Estate Finance and Economics, 45(2), 402–434. https://doi.org/10.1007/s11146-0109266-z  [OA](https://doi.org/10.1007/s11146-0109266-z)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11146-0109266-z)

[^Duan_et+al_2022_a]: Duan, H. K., Hu, H., Yoon, Y., &amp; Vasarhelyi, M. (2022). Increasing the utility of performance audit reports: Using textual analytics tools to improve government reporting. Intelligent Systems in Accounting, Finance and Management, 29(4), 201–218. https://doi.org/10.1002/isaf.1526  [OA](https://doi.org/10.1002/isaf.1526)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1526)

[^El-Haj_et+al_2019_a]: El-Haj, M., Rayson, P., Walker, M., Young, S., &; Simaki, V. (2019). In search of meaning: Lessons, resources, and next steps for computational analysis of financial discourse. Journal of Business Finance &amp; Accounting, 46(3–4), 265–306.  [OA](https://engine.scholarcy.com/oa_version?query=El-Haj%2C%20M.%20Rayson%2C%20P.%20Walker%2C%20M.%20Young%2C%20S.%20In%20search%20of%20meaning%3A%20Lessons%2C%20resources%20and%20next%20steps%20for%20computational%20analysis%20of%20financial%20discourse%202019&author=El-Haj&title=In%20search%20of%20meaning%3A%20Lessons%2C%20resources%20and%20next%20steps%20for%20computational%20analysis%20of%20financial%20discourse&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=El-Haj%2C%20M.%20Rayson%2C%20P.%20Walker%2C%20M.%20Young%2C%20S.%20In%20search%20of%20meaning%3A%20Lessons%2C%20resources%20and%20next%20steps%20for%20computational%20analysis%20of%20financial%20discourse%202019) [Scite](/scite_tallies?query=author%3AEl-Haj%2Ctitle%3AIn%20search%20of%20meaning%3A%20Lessons%2C%20resources%20and%20next%20steps%20for%20computational%20analysis%20of%20financial%20discourse%2Cyear%3A2019)

[^Erickson_et+al_1978_a]: Erickson, B., Lind, E. A., Johnson, B. C., &amp; O&#39;Barr, W. M. (1978). Speech style and impression formation in a court setting: The effects of “powerful” and “powerless” speech. Journal of Experimental Social Psychology, 14(3), 266–279. https://doi.org/10.1016/0022-1031(78)90015-X  [OA](https://doi.org/10.1016/0022-1031(78)90015-X)  [Scite](/scite_tallies?query=https://doi.org/10.1016/0022-1031(78)90015-X)

[^Feinberg_et+al_2005_a]: Feinberg, D. R., Jones, B. C., Little, A. C., Burt, D. M., &amp; Perrett, D. I. (2005). Manipulations of fundamental and formant frequencies influence the attractiveness of human male voices. Animal Behaviour, 69(3), 561–568. https://doi.org/10.1016/j.anbehav.2004.06.012  [OA](https://doi.org/10.1016/j.anbehav.2004.06.012)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.anbehav.2004.06.012)

[^Ferguson_et+al_2015_a]: Ferguson, N., Philip, D., Lam, H., &amp; Guo, J. (2015). Media content and stock returns: The predictive power of press. Multinational Finance Journal, 19(1), 1–31. https://doi.org/10.17578/19-1-1  [OA](https://doi.org/10.17578/19-1-1)  [Scite](/scite_tallies?query=https://doi.org/10.17578/19-1-1)

[^Fisher_et+al_2016_a]: Fisher, I. E., Garnsey, M. R., &amp; Hughes, M. E. (2016). Natural language processing in accounting, auditing, and finance: A synthesis of the literature with a roadmap for future research. Intelligent Systems in Accounting, Finance and Management, 23(3), 157–214. https://doi.org/10.1002/isaf.1386  [OA](https://doi.org/10.1002/isaf.1386)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1386)

[^Frankel_et+al_1999_a]: Frankel, R., Johnson, M., &amp; Skinner, D. J. (1999). An empirical examination of conference calls as a voluntary disclosure medium. Journal of  [OA](https://scholar.google.co.uk/scholar?q=Frankel%2C%20R.%20Johnson%2C%20M.%20Skinner%2C%20D.J.%20An%20empirical%20examination%20of%20conference%20calls%20as%20a%20voluntary%20disclosure%20medium%201999) [GScholar](https://scholar.google.co.uk/scholar?q=Frankel%2C%20R.%20Johnson%2C%20M.%20Skinner%2C%20D.J.%20An%20empirical%20examination%20of%20conference%20calls%20as%20a%20voluntary%20disclosure%20medium%201999) 

[^Accounting_0000_a]: Accounting Research, 37(1), 133–150. https://doi.org/10.2307/2491400  [OA](https://doi.org/10.2307/2491400)  [Scite](/scite_tallies?query=https://doi.org/10.2307/2491400)

[^Fu_et+al_2019_a]: Fu, X., Wu, X., &amp; Zhang, Z. (2019). The information role of earnings conference call tone: Evidence from stock price crash risk. Journal of Business Ethics, 173, 643–660. https://doi.org/10.1007/s10551-019-04326-1  [OA](https://doi.org/10.1007/s10551-019-04326-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10551-019-04326-1)

[^Gandhi_et+al_2023_a]: Gandhi, A., Adhvaryu, K., Poria, S., Cambria, E., &amp; Hussain, A. (2023). Multimodal sentiment analysis: A systematic review of history, datasets, multimodal fusion methods, applications, challenges and future directions. Information Fusion, 91, 424–444. https://doi.org/10.1016/j.inffus.2022.09.025  [OA](https://doi.org/10.1016/j.inffus.2022.09.025)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.inffus.2022.09.025)

[^Garcia_2012_a]: Garcia, D. (2012). Sentiment during recessions. The Journal of Finance, 68(3), 1267–1300.  [OA](https://engine.scholarcy.com/oa_version?query=Garcia%2C%20D.%20Sentiment%20during%20recessions%202012&author=Garcia&title=Sentiment%20during%20recessions&year=2012) [GScholar](https://scholar.google.co.uk/scholar?q=Garcia%2C%20D.%20Sentiment%20during%20recessions%202012) [Scite](/scite_tallies?query=author%3AGarcia%2Ctitle%3ASentiment%20during%20recessions%2Cyear%3A2012)

[^G_et+al_1996_a]: Gélinas-Chebat, C., Chebat, J. C., &amp; Vaninsky, A. (1996). Voice and advertising: Effects of intonation and intensity of voice on source credibility, attitudes toward the advertised service and the intent to buy. Perceptual and Motor Skills, 83(1), 243–262. https://doi.org/10.2466/pms.1996.83.1.243  [OA](https://doi.org/10.2466/pms.1996.83.1.243)  [Scite](/scite_tallies?query=https://doi.org/10.2466/pms.1996.83.1.243)

[^Ghahfarrokhi_2020_a]: Ghahfarrokhi, A., &amp; Shamsfard, M. (2020). Tehran stock exchange prediction using sentiment analysis of online textual opinions. Intelligent Systems in Accounting, Finance and Management, 27(1), 22–37. https://doi.org/10.1002/isaf.1465  [OA](https://doi.org/10.1002/isaf.1465)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1465)

[^Giddens_et+al_2013_a]: Giddens, C. L., Barron, K. W., Byrd-Craven, J., Clark, K. F., &amp; Winter, A. S. (2013). Vocal indices of stress: a review. Journal of Voice, 27(3), 390–e21.  [OA](https://engine.scholarcy.com/oa_version?query=Giddens%2C%20C.L.%20Barron%2C%20K.W.%20Byrd-Craven%2C%20J.%20Clark%2C%20K.F.%20Vocal%20indices%20of%20stress%3A%20a%20review%202013&author=Giddens&title=Vocal%20indices%20of%20stress%3A%20a%20review&year=2013) [GScholar](https://scholar.google.co.uk/scholar?q=Giddens%2C%20C.L.%20Barron%2C%20K.W.%20Byrd-Craven%2C%20J.%20Clark%2C%20K.F.%20Vocal%20indices%20of%20stress%3A%20a%20review%202013) [Scite](/scite_tallies?query=author%3AGiddens%2Ctitle%3AVocal%20indices%20of%20stress%3A%20a%20review%2Cyear%3A2013)

[^Given_2008_a]: Given, L. (2008). The SAGE encyclopedia of qualitative research methods. DICTION (Software). https://doi.org/10.4135/9781412963909  [OA](https://doi.org/10.4135/9781412963909)  [Scite](/scite_tallies?query=https://doi.org/10.4135/9781412963909)

[^Goel_2012_a]: Goel, S., &amp; Gangolly, J. (2012). Beyond the numbers: Mining the annual reports for hidden cues indicative of financial statement fraud. Intelligent Systems in Accounting, Finance and Management, 19(2), 75–89. https://doi.org/10.1002/isaf.1326  [OA](https://doi.org/10.1002/isaf.1326)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1326)

[^Goel_2016_a]: Goel, S., &amp; Uzuner, O. (2016). Do sentiments matter in fraud detection? Estimating the semantic orientation of annual reports. Intelligent Systems in Accounting, Finance and Management, 23(3), 215–239. https://doi.org/10.1002/isaf.1392  [OA](https://doi.org/10.1002/isaf.1392)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1392)

[^González-Bailon_2015_a]: González-Bailon, S., &; Paltoglou, G. (2015). Signals of public opinion in online communication. The Annals of the American Academy of Political and Social Science, 659(1), 95–107. https://doi.org/10.1177/0002716215569192  [OA](https://doi.org/10.1177/0002716215569192)  [Scite](/scite_tallies?query=https://doi.org/10.1177/0002716215569192)

[^Graebner_et+al_2012_a]: Gräbner, D., Zanker, M., Fliedl, G., &; Fuchs, M. (2012). Classification of customer reviews based on sentiment analysis. In Information and communication technologies in tourism 2012 (pp. 460–470). Springer.  [OA](https://scholar.google.co.uk/scholar?q=Gr%C3%A4bner%2C%20D.%20Zanker%2C%20M.%20Fliedl%2C%20G.%20Fuchs%2C%20M.%20Classification%20of%20customer%20reviews%20based%20on%20sentiment%20analysis%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Gr%C3%A4bner%2C%20D.%20Zanker%2C%20M.%20Fliedl%2C%20G.%20Fuchs%2C%20M.%20Classification%20of%20customer%20reviews%20based%20on%20sentiment%20analysis%202012) 

[^Grimmer_2013_a]: Grimmer, J., &amp; Stewart, B. (2013). Text as data: The promise and pitfalls of automatic content analysis methods for political texts. Political Analysis, 21(3), 267–297. https://doi.org/10.1093/pan/mps028  [OA](https://doi.org/10.1093/pan/mps028)  [Scite](/scite_tallies?query=https://doi.org/10.1093/pan/mps028)

[^Gross-Klussmann_2011_a]: Groß-Klußmann, A., &; Hautsch, N. (2011). When machines read the news: Using automated text analytics to quantify high frequency newsimplied market reactions. Journal of Empirical Finance, 18(2), 321–340. https://doi.org/10.1016/j.jempfin.2010.11.009  [OA](https://doi.org/10.1016/j.jempfin.2010.11.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jempfin.2010.11.009)

[^Gu_2020_a]: Gu, C., &amp; Kurov, A. (2020). Informational role of social media: Evidence from Twitter sentiment. Journal of Banking &amp; Finance, 121, 105969. https://doi.org/10.1016/j.jbankfin.2020.105969  [OA](https://doi.org/10.1016/j.jbankfin.2020.105969)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2020.105969)

[^Guo_et+al_2016_a]: Guo, L., Shi, F., &; Tu, J. (2016). Textual analysis and machine learning: Crack unstructured data in finance and accounting. The Journal of Finance and Data Science, 2(3), 153–170. https://doi.org/10.1016/j.jfds.2017.02.001  [OA](https://doi.org/10.1016/j.jfds.2017.02.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfds.2017.02.001)

[^Guyer_et+al_2018_a]: Guyer, J. J., Fabrigar, L. R., Vaughan-Johnston, T. I., &amp; Tang, C. (2018). The counterintuitive influence of vocal affect on the efficacy of affectively-based persuasive messages. Journal of Experimental Social Psychology, 74, 161–173.  [OA](https://engine.scholarcy.com/oa_version?query=Guyer%2C%20J.J.%20Fabrigar%2C%20L.R.%20Vaughan-Johnston%2C%20T.I.%20Tang%2C%20C.%20The%20counterintuitive%20influence%20of%20vocal%20affect%20on%20the%20efficacy%20of%20affectively-based%20persuasive%20messages%202018&author=Guyer&title=The%20counterintuitive%20influence%20of%20vocal%20affect%20on%20the%20efficacy%20of%20affectively-based%20persuasive%20messages&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Guyer%2C%20J.J.%20Fabrigar%2C%20L.R.%20Vaughan-Johnston%2C%20T.I.%20Tang%2C%20C.%20The%20counterintuitive%20influence%20of%20vocal%20affect%20on%20the%20efficacy%20of%20affectively-based%20persuasive%20messages%202018) [Scite](/scite_tallies?query=author%3AGuyer%2Ctitle%3AThe%20counterintuitive%20influence%20of%20vocal%20affect%20on%20the%20efficacy%20of%20affectively-based%20persuasive%20messages%2Cyear%3A2018)

[^Harris_1993_a]: Harris, M., &amp; Raviv, A. (1993). Differences of opinion make a horse race. Review of Financial Studies, 6(3), 473–506. https://doi.org/10.1093/rfs/5.3.473  [OA](https://doi.org/10.1093/rfs/5.3.473)  [Scite](/scite_tallies?query=https://doi.org/10.1093/rfs/5.3.473)

[^Henry_2006_a]: Henry, E. (2006). Market reaction to verbal components of earnings press releases: Event study using a predictive algorithm. Journal of Emerging  [OA](https://engine.scholarcy.com/oa_version?query=Henry%2C%20E.%20Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%202006&author=Henry&title=Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Henry%2C%20E.%20Market%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%202006) [Scite](/scite_tallies?query=author%3AHenry%2Ctitle%3AMarket%20reaction%20to%20verbal%20components%20of%20earnings%20press%20releases%3A%20Event%20study%20using%20a%20predictive%20algorithm%2Cyear%3A2006)

[^Technologies_0000_b]: Technologies in Accounting., 3(1), 1–19. https://doi.org/10.2308/jeta.2006.3.1.1  [OA](https://doi.org/10.2308/jeta.2006.3.1.1)  [Scite](/scite_tallies?query=https://doi.org/10.2308/jeta.2006.3.1.1)

[^Henry_2008_a]: Henry, E. (2008). Are investors influenced by how earnings press releases are written? Journal of Business Communication, 45(4), 363–407. https://doi.org/10.1177/0021943608319388  [OA](https://doi.org/10.1177/0021943608319388)  [Scite](/scite_tallies?query=https://doi.org/10.1177/0021943608319388)

[^Hiew_et+al_2019_a]: Hiew, J., Huang, X., Mou, H., Li, D., Wu, Q., &amp; Xu, Y. (2019). BERT-based financial sentiment index and LSTM-based stock return predictability. Cornell University Working Paper.  [OA](https://scholar.google.co.uk/scholar?q=Hiew%20J%20Huang%20X%20Mou%20H%20Li%20D%20Wu%20Q%20%20Xu%20Y%202019%20BERTbased%20financial%20sentiment%20index%20and%20LSTMbased%20stock%20return%20predictability%20Cornell%20University%20Working%20Paper) [GScholar](https://scholar.google.co.uk/scholar?q=Hiew%20J%20Huang%20X%20Mou%20H%20Li%20D%20Wu%20Q%20%20Xu%20Y%202019%20BERTbased%20financial%20sentiment%20index%20and%20LSTMbased%20stock%20return%20predictability%20Cornell%20University%20Working%20Paper) 

[^Hirshleifer_1977_a]: Hirshleifer, J. (1977). Economics from a biological viewpoint. The Journal of Law and Economics, 20(1), 1–52. https://doi.org/10.1086/466891  [OA](https://doi.org/10.1086/466891)  [Scite](/scite_tallies?query=https://doi.org/10.1086/466891)

[^Hochreiter_1997_a]: Hochreiter, S., &amp; Schmidhuber, J. (1997). Long short-term memory. Neural Computation, 9(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735  [OA](https://doi.org/10.1162/neco.1997.9.8.1735)  [Scite](/scite_tallies?query=https://doi.org/10.1162/neco.1997.9.8.1735)

[^Houjeij_et+al_2012_a]: Houjeij, A., Hamieh, L., Mehdi, N., &amp; Hajj, H. (2012). A novel approach for emotion classification based on fusion of text and speech. In 2012 19th International Conference on Telecommunications (ICT) (pp. 1–6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Houjeij%2C%20A.%20Hamieh%2C%20L.%20Mehdi%2C%20N.%20Hajj%2C%20H.%20A%20novel%20approach%20for%20emotion%20classification%20based%20on%20fusion%20of%20text%20and%20speech%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Houjeij%2C%20A.%20Hamieh%2C%20L.%20Mehdi%2C%20N.%20Hajj%2C%20H.%20A%20novel%20approach%20for%20emotion%20classification%20based%20on%20fusion%20of%20text%20and%20speech%202012) 

[^Howard_2018_a]: Howard, J., &amp; Ruder, S. (2018). Universal language model fine-tuning for text classification. arXiv preprint arXiv:1801.06146.  [OA](https://arxiv.org/abs/1801.06146)  

[^Huang_et+al_2023_a]: Huang, A. H., Wang, H., &amp; Yang, Y. (2023). FinBERT: A large language model for extracting information from financial text. Contemporary Accounting Research, 40(2), 806–841. https://doi.org/10.1111/19113846.12832  [OA](https://doi.org/10.1111/19113846.12832)  [Scite](/scite_tallies?query=https://doi.org/10.1111/19113846.12832)

[^Humpherys_et+al_2011_a]: Humpherys, S. L., Moffitt, K. C., Burns, M. B., Burgoon, J. K., &amp; Felix, W. F. (2011). Identification of fraudulent financial statements using linguistic credibility analysis. Decision Support Systems, 50(3), 585–594. https://doi.org/10.1016/j.dss.2010.08.009  [OA](https://doi.org/10.1016/j.dss.2010.08.009)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2010.08.009)

[^Jegadeesh_2012_a]: Jegadeesh, N., &amp; Wu, A. (2012). Word power: A new approach for content analysis. Journal of Financial Economics, 3(110), 712–729. https://doi.org/10.1016/j.jfineco.2013.08.018  [OA](https://doi.org/10.1016/j.jfineco.2013.08.018)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfineco.2013.08.018)

[^Jiang_et+al_2019_a]: Jiang, F., Lee, J., Martin, X., &amp; Zhou, G. (2019). Manager sentiment and stock returns. Journal of Financial Economics, 132(1), 126–149. https://doi.org/10.1016/j.jfineco.2018.10.001  [OA](https://doi.org/10.1016/j.jfineco.2018.10.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jfineco.2018.10.001)

[^Jiang_2021_a]: Jiang, W. (2021). Applications of deep learning in stock market prediction: recent progress. Expert Systems with Applications, 184, 115537. https://doi.org/10.1016/j.eswa.2021.115537  [OA](https://doi.org/10.1016/j.eswa.2021.115537)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.eswa.2021.115537)

[^Johnman_et+al_2018_a]: Johnman, M., Vanstone, B., &amp; Gepp, A. (2018). Predicting FTSE 100 returns and volatility using sentiment analysis. Accounting and Finance, 58(S1), 253–274. https://doi.org/10.1111/acfi.12373  [OA](https://doi.org/10.1111/acfi.12373)  [Scite](/scite_tallies?query=https://doi.org/10.1111/acfi.12373)

[^Joulin_et+al_2016_a]: Joulin, A., Grave, E., Bojanowski, P., Douze, M., Jégou, H., &amp; Mikolov, T. (2016). Fasttext. zip: Compressing text classification models. arXiv preprint arXiv:1612.03651.  [OA](https://arxiv.org/abs/1612.03651)  

[^Jozefowicz_et+al_2016_a]: Jozefowicz, R., Vinyals, O., Schuster, M., Shazeer, N., &amp; Wu, Y. (2016). Exploring the limits of language modeling. arXiv preprint arXiv: 1602.02410.  [OA](https://arxiv.org/abs/1602.02410)  

[^Kartik_et+al_2007_a]: Kartik, N., Ottaviani, M., &amp; Squintani, F. (2007). Credulity, lies, and costly talk. Journal of Economic Theory, 134(1), 93–116. https://doi.org/10.1016/j.jet.2006.04.003  [OA](https://doi.org/10.1016/j.jet.2006.04.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jet.2006.04.003)

[^Kaushik_et+al_2013_a]: Kaushik, L., Sangwan, A., &amp; Hansen, J. H. (2013). Sentiment extraction from natural audio streams. In 2013 IEEE International Conference on Acoustics, Speech and Signal Processing (pp. 8485–8489). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Kaushik%2C%20L.%20Sangwan%2C%20A.%20Hansen%2C%20J.H.%20Sentiment%20extraction%20from%20natural%20audio%20streams%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Kaushik%2C%20L.%20Sangwan%2C%20A.%20Hansen%2C%20J.H.%20Sentiment%20extraction%20from%20natural%20audio%20streams%202013) 

[^Kearney_2014_a]: Kearney, C., &amp; Liu, S. (2014). Textual sentiment in finance: A survey of methods and models. International Review of Financial Analysis, 33, 171–185. https://doi.org/10.1016/j.irfa.2014.02.006  [OA](https://doi.org/10.1016/j.irfa.2014.02.006)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.irfa.2014.02.006)

[^Khan_et+al_2022_a]: Khan, S., Naseer, M., Hayat, M., Zamir, S. W., Khan, F. S., &amp; Shah, M. (2022). Transformers in vision: A survey. ACM Computing Surveys (CSUR), 54(10s), 1–41. https://doi.org/10.1145/3505244  [OA](https://doi.org/10.1145/3505244)  [Scite](/scite_tallies?query=https://doi.org/10.1145/3505244)

[^Kim_2014_a]: Kim, Y. (2014). Convolutional neural networks for sentence classification. arXiv preprint arXiv:1408.5882.  [OA](https://arxiv.org/abs/1408.5882)  

[^Klofstad_et+al_2012_a]: Klofstad, C. A., Anderson, R. C., &amp; Peters, S. (2012). Sounds like a winner: Voice pitch influences perception of leadership capacity in both men and women. Proceedings of the Royal Society B: Biological Sciences, 279(1738), 2698–2704. https://doi.org/10.1098/rspb.2012.0311  [OA](https://doi.org/10.1098/rspb.2012.0311)  [Scite](/scite_tallies?query=https://doi.org/10.1098/rspb.2012.0311)

[^Koolagudi_2012_a]: Koolagudi, S. G., &amp; Rao, K. S. (2012). Emotion recognition from speech: A review. International Journal of Speech Technology, 15(2), 99–117. https://doi.org/10.1007/s10772-011-9125-1  [OA](https://doi.org/10.1007/s10772-011-9125-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10772-011-9125-1)

[^Larcker_2012_a]: Larcker, D., &amp; Zakolyukina, A. (2012). Detecting deceptive discussions in conference calls. Journal of Accounting Research, 50(2), 495–540. https://doi.org/10.1111/j.1475-679X.2012.00450.x  [OA](https://doi.org/10.1111/j.1475-679X.2012.00450.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1475-679X.2012.00450.x)

[^Levi_2008_a]: Levi, S. (2008). Voluntary disclosure of accruals in earnings press releases and the pricing of accruals. Review of Accounting Studies, 13(1), 1–21. https://doi.org/10.1007/s11142-007-9059-7  [OA](https://doi.org/10.1007/s11142-007-9059-7)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11142-007-9059-7)

[^Li_2010_a]: Li, F. (2010). The information content of forward-looking statements in corporate filings—A Naïve Bayesian machine learning approach. Journal of Accounting Research, 48(5), 1049–1102. https://doi.org/10.1111/j.1475-679X.2010.00382.x  [OA](https://doi.org/10.1111/j.1475-679X.2010.00382.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1475-679X.2010.00382.x)

[^Loughran_2011_a]: Loughran, T., &amp; McDonald, B. (2011). When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. The Journal of Finance, 66(1), 35–65. https://doi.org/10.1111/j.1540-6261.2010.01625.x  [OA](https://doi.org/10.1111/j.1540-6261.2010.01625.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2010.01625.x)

[^Loughran_2016_a]: Loughran, T., &amp; McDonald, B. (2016). Textual analysis in accounting and finance: A survey. Journal of Accounting Research, 54(4), 1187–1230. https://doi.org/10.1111/1475-679X.12123  [OA](https://doi.org/10.1111/1475-679X.12123)  [Scite](/scite_tallies?query=https://doi.org/10.1111/1475-679X.12123)

[^Louis_et+al_2008_a]: Louis, H., Robinson, D., &amp; Sbaraglia, A. (2008). An integrated analysis of the association between accrual disclosure and the abnormal accrual anomaly. Review of Accounting Studies, 13(1), 23–54. https://doi.org/10.1007/s11142-007-9038-z  [OA](https://doi.org/10.1007/s11142-007-9038-z)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11142-007-9038-z)

[^Lucca_2015_a]: Lucca, D., &amp; Moench, E. (2015). The pre-FOMC announcement drift. The Journal of Finance, 70(1), 329–371. https://doi.org/10.1111/jofi.12196  [OA](https://doi.org/10.1111/jofi.12196)  [Scite](/scite_tallies?query=https://doi.org/10.1111/jofi.12196)

[^Luong_et+al_2015_a]: Luong, M. T., Pham, H., &amp; Manning, C. D. (2015). Effective approaches to attention-based neural machine translation. arXiv preprint arXiv: 1508.04025.  [OA](https://arxiv.org/abs/1508.04025)  

[^Mairesse_et+al_2012_a]: Mairesse, F., Polifroni, J., &amp; Di Fabbrizio, G. (2012). Can prosody inform sentiment analysis? experiments on short spoken reviews. In 2012 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 5093–5096). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Mairesse%2C%20F.%20Polifroni%2C%20J.%20Fabbrizio%2C%20G.%20Can%20prosody%20inform%20sentiment%20analysis%3F%20experiments%20on%20short%20spoken%20reviews%202012) [GScholar](https://scholar.google.co.uk/scholar?q=Mairesse%2C%20F.%20Polifroni%2C%20J.%20Fabbrizio%2C%20G.%20Can%20prosody%20inform%20sentiment%20analysis%3F%20experiments%20on%20short%20spoken%20reviews%202012) 

[^Mao_et+al_2011_a]: Mao, H., Counts, S., &amp; Bollen, J. (2011). Predicting financial markets: Comparing survey, news, twitter and search engine data. arXiv preprint arXiv: 1112.1051.  [OA](https://arxiv.org/abs/1112.1051)  

[^Martín-Santana_et+al_2015_a]: Martín-Santana, J. D., Muela-Molina, C., Reinares-Lara, E., &amp; RodríguezGuerra, M. (2015). Effectiveness of radio spokesperson&#39;s gender, vocal pitch and accent and the use of music in radio advertising. BRQ Business Research Quarterly, 18(3), 143–160. https://doi.org/10.1016/j.brq.2014.06.001  [OA](https://doi.org/10.1016/j.brq.2014.06.001)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.brq.2014.06.001)

[^Matsumoto_et+al_2011_a]: Matsumoto, D., Pronk, M., &amp; Roelofsen, E. (2011). What makes conference calls useful? The information content of managers&#39; presentations and analysts&#39; discussion sessions. The Accounting Review, 86(4), 1383– 1414. https://doi.org/10.2308/accr-10034  [OA](https://doi.org/10.2308/accr-10034)  [Scite](/scite_tallies?query=https://doi.org/10.2308/accr-10034)

[^Mayew_2012_a]: Mayew, W., &amp; Venkatachalam, M. (2012). The power of voice: Managerial affective states and future firm performance. The Journal of Finance, 67(1), 1–43. https://doi.org/10.1111/j.1540-6261.2011.01705.x  [OA](https://doi.org/10.1111/j.1540-6261.2011.01705.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2011.01705.x)

[^Mcgurk_et+al_2020_a]: McGurk, Z., Nowak, A., &amp; Hall, J. (2020). Stock returns and investor sentiment: textual analysis and social media. Journal of Economics and Finance, 44(3), 458–485. https://doi.org/10.1007/s12197-01909494-4  [OA](https://doi.org/10.1007/s12197-01909494-4)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s12197-01909494-4)

[^Mckay_et+al_2012_a]: McKay Price, S., Doran, J., Peterson, D., &amp; Bliss, B. (2012). Earnings conference calls and stock returns: The incremental informativeness of textual tone. Journal of Banking &amp; Finance, 36(4), 992–1011. https://doi.org/10.1016/j.jbankfin.2011.10.013  [OA](https://doi.org/10.1016/j.jbankfin.2011.10.013)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2011.10.013)

[^Medhat_et+al_2014_a]: Medhat, W., Hassan, A., &amp; Korashy, H. (2014). Sentiment analysis algorithms and applications: A survey. Ain Shams Engineering Journal, 5(4), 1093–1113. https://doi.org/10.1016/j.asej.2014.04.011  [OA](https://doi.org/10.1016/j.asej.2014.04.011)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.asej.2014.04.011)

[^Mehrabian_1968_a]: Mehrabian, A. (1968). Inference of attitudes from the posture, orientation, and distance of a communicator. Journal of Consulting and Clinical Psychology, 32(3), 296–308. https://doi.org/10.1037/h0025906  [OA](https://doi.org/10.1037/h0025906)  [Scite](/scite_tallies?query=https://doi.org/10.1037/h0025906)

[^Mendoza_1998_a]: Mendoza, E., &amp; Carballo, G. (1998). Acoustic analysis of induced vocal stress by means of cognitive workload tasks. Journal of Voice, 12(3), 263–273. https://doi.org/10.1016/S0892-1997(98)80017-9  [OA](https://doi.org/10.1016/S0892-1997(98)80017-9)  [Scite](/scite_tallies?query=https://doi.org/10.1016/S0892-1997(98)80017-9)

[^Milian_2017_a]: Milian, J., &amp; Smith, A. (2017). An investigation of analysts&#39; praise of management during earnings conference calls. Journal of Behavioral Finance, 18(1), 65–77. https://doi.org/10.1080/15427560.2017.1276068  [OA](https://doi.org/10.1080/15427560.2017.1276068)  [Scite](/scite_tallies?query=https://doi.org/10.1080/15427560.2017.1276068)

[^Moffitt_2009_a]: Moffitt, K., &amp; Burns, M. B. (2009). What does that mean? Investigating obfuscation and readability cues as indicators of deception in fraudulent financial reports. In AMCIS 2009 Proceedings (p. 399).  [OA](https://scholar.google.co.uk/scholar?q=Moffitt%2C%20K.%20Burns%2C%20M.B.%20What%20does%20that%20mean%3F%20Investigating%20obfuscation%20and%20readability%20cues%20as%20indicators%20of%20deception%20in%20fraudulent%20financial%20reports%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Moffitt%2C%20K.%20Burns%2C%20M.B.%20What%20does%20that%20mean%3F%20Investigating%20obfuscation%20and%20readability%20cues%20as%20indicators%20of%20deception%20in%20fraudulent%20financial%20reports%202009) 

[^Morency_et+al_2011_a]: Morency, L.-P., Mihalcea, R., &amp; Doshi, P. (2011). Towards multimodal sentiment analysis: Harvesting opinions from the web. In Proceedings of the 13th international conference on multimodal interfaces (pp. 169–176).  [OA](https://scholar.google.co.uk/scholar?q=Morency%2C%20L.-P.%20Mihalcea%2C%20R.%20Doshi%2C%20P.%20Towards%20multimodal%20sentiment%20analysis%3A%20Harvesting%20opinions%20from%20the%20web%202011) [GScholar](https://scholar.google.co.uk/scholar?q=Morency%2C%20L.-P.%20Mihalcea%2C%20R.%20Doshi%2C%20P.%20Towards%20multimodal%20sentiment%20analysis%3A%20Harvesting%20opinions%20from%20the%20web%202011) 

[^Munikar_et+al_2019_a]: Munikar, M., Shakya, S., &amp; Shrestha, A. (2019). Fine-grained sentiment classification using BERT. In 2019 Artificial Intelligence for Transforming Business and Society (AITB) (Vol. 1, pp. 1–5). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Munikar%2C%20M.%20Shakya%2C%20S.%20Shrestha%2C%20A.%20Fine-grained%20sentiment%20classification%20using%20BERT%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Munikar%2C%20M.%20Shakya%2C%20S.%20Shrestha%2C%20A.%20Fine-grained%20sentiment%20classification%20using%20BERT%202019) 

[^Nardo_et+al_2016_a]: Nardo, M., Petracco-Giudici, M., &amp; Naltsidis, M. (2016). Walking down wall street with a tablet: A survey of stock market predictions using the web. Journal of Economic Surveys, 30(2), 356–369. https://doi.org/10.1111/joes.12102  [OA](https://doi.org/10.1111/joes.12102)  [Scite](/scite_tallies?query=https://doi.org/10.1111/joes.12102)

[^Nogueira_2020_a]: Nogueira, R., &amp; Cho, K. (2020). Passage re-ranking with BERT. Cornell University Working Paper.  [OA](https://scholar.google.co.uk/scholar?q=Nogueira%2C%20R.%20Cho%2C%20K.%20Passage%20re-ranking%20with%20BERT%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Nogueira%2C%20R.%20Cho%2C%20K.%20Passage%20re-ranking%20with%20BERT%202020) 

[^O&#39;Leary_2011_a]: O&#39;Leary, D. E. (2011). Blog mining-review and extensions: “From each according to his opinion”. Decision Support Systems, 51(4), 821–830. https://doi.org/10.1016/j.dss.2011.01.016  [OA](https://doi.org/10.1016/j.dss.2011.01.016)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2011.01.016)

[^O&#39;Leary_2016_a]: O&#39;Leary, D. E. (2016). On the relationship between number of votes and sentiment in crowdsourcing ideas and comments for innovation: A case study of Canada&#39;s digital compass. Decision Support Systems, 88, 28–37. https://doi.org/10.1016/j.dss.2016.05.006  [OA](https://doi.org/10.1016/j.dss.2016.05.006)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.dss.2016.05.006)

[^Park_et+al_2011_a]: Park, C. K., Lee, S., Park, H. J., Baik, Y. S., Park, Y. B., &amp; Park, Y. J. (2011). Autonomic function, voice, and mood states. Clinical Autonomic Research, 21, 103–110. https://doi.org/10.1007/s10286-010-0095-1  [OA](https://doi.org/10.1007/s10286-010-0095-1)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s10286-010-0095-1)

[^Pereira_et+al_2014_a]: Pereira, J., Luque, J., &amp; Anguera, X. (2014). Sentiment retrieval on web reviews using spontaneous natural speech. In 2014 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (pp. 4583–4587). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Pereira%2C%20J.%20Luque%2C%20J.%20Anguera%2C%20X.%20Sentiment%20retrieval%20on%20web%20reviews%20using%20spontaneous%20natural%20speech%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Pereira%2C%20J.%20Luque%2C%20J.%20Anguera%2C%20X.%20Sentiment%20retrieval%20on%20web%20reviews%20using%20spontaneous%20natural%20speech%202014) 

[^Poria_et+al_2015_a]: Poria, S., Cambria, E., &amp; Gelbukh, A. (2015). Deep convolutional neural network textual features and multiple kernel learning for utterance-level multimodal sentiment analysis. In Proceedings of the 2015 conference on empirical methods in natural language processing (pp. 2539–2544).  [OA](https://scholar.google.co.uk/scholar?q=Poria%2C%20S.%20Cambria%2C%20E.%20Gelbukh%2C%20A.%20Deep%20convolutional%20neural%20network%20textual%20features%20and%20multiple%20kernel%20learning%20for%20utterance-level%20multimodal%20sentiment%20analysis%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Poria%2C%20S.%20Cambria%2C%20E.%20Gelbukh%2C%20A.%20Deep%20convolutional%20neural%20network%20textual%20features%20and%20multiple%20kernel%20learning%20for%20utterance-level%20multimodal%20sentiment%20analysis%202015) 

[^Raffel_et+al_2020_a]: Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., &amp; Liu, P. J. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer. The Journal of Machine Learning Research, 21(1), 5485–5551.  [OA](https://engine.scholarcy.com/oa_version?query=Raffel%2C%20C.%20Shazeer%2C%20N.%20Roberts%2C%20A.%20Lee%2C%20K.%20Exploring%20the%20limits%20of%20transfer%20learning%20with%20a%20unified%20text-to-text%20transformer%202020&author=Raffel&title=Exploring%20the%20limits%20of%20transfer%20learning%20with%20a%20unified%20text-to-text%20transformer&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Raffel%2C%20C.%20Shazeer%2C%20N.%20Roberts%2C%20A.%20Lee%2C%20K.%20Exploring%20the%20limits%20of%20transfer%20learning%20with%20a%20unified%20text-to-text%20transformer%202020) [Scite](/scite_tallies?query=author%3ARaffel%2Ctitle%3AExploring%20the%20limits%20of%20transfer%20learning%20with%20a%20unified%20text-to-text%20transformer%2Cyear%3A2020)

[^Renault_2017_a]: Renault, T. (2017). Intraday online investor sentiment and return patterns in the U.S. stock market. Journal of Banking &amp; Finance, 84, 25–40. https://doi.org/10.1016/j.jbankfin.2017.07.002  [OA](https://doi.org/10.1016/j.jbankfin.2017.07.002)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2017.07.002)

[^Renault_2020_a]: Renault, T. (2020). Sentiment analysis and machine learning in finance: A comparison of methods and models on one million messages. Digital Finance, 2(1–2), 1–13. https://doi.org/10.1007/s42521-019-00014-x  [OA](https://doi.org/10.1007/s42521-019-00014-x)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s42521-019-00014-x)

[^Ribeiro_et+al_2016_a]: Ribeiro, F., Araújo, M., Gonçalves, P., André Gonçalves, M., &amp; Benevenuto, F. (2016). SentiBench - a benchmark comparison of state-of-the-practice sentiment analysis methods. EPJ Data Science, 5(1), 23. https://doi.org/10.1140/epjds/s13688-016-0085-1  [OA](https://doi.org/10.1140/epjds/s13688-016-0085-1)  [Scite](/scite_tallies?query=https://doi.org/10.1140/epjds/s13688-016-0085-1)

[^Siganos_et+al_2014_a]: Siganos, A., Vagenas-Nanos, E., &amp; Verwijmeren, P. (2014). Facebook&#39;s daily sentiment and international stock markets. Journal of Economic Behavior &amp; Organization, 107, 730–743. https://doi.org/10.1016/j.jebo.2014.06.004  [OA](https://doi.org/10.1016/j.jebo.2014.06.004)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jebo.2014.06.004)

[^Siganos_et+al_2017_a]: Siganos, A., Vagenas-Nanos, E., &amp; Verwijmeren, P. (2017). Divergence of sentiment and stock market trading. Journal of Banking &amp; Finance, 78, 130–141. https://doi.org/10.1016/j.jbankfin.2017.02.005  [OA](https://doi.org/10.1016/j.jbankfin.2017.02.005)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2017.02.005)

[^Soleymani_et+al_2017_a]: Soleymani, M., Garcia, D., Jou, B., Schuller, B., Chang, S., &amp; Pantic, M. (2017). A survey of multimodal sentiment analysis. Image and Vision Computing, 65, 3–14. https://doi.org/10.1016/j.imavis.2017.08.003  [OA](https://doi.org/10.1016/j.imavis.2017.08.003)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.imavis.2017.08.003)

[^Song_et+al_2020_a]: Song, S., Baba, J., Nakanishi, J., Yoshikawa, Y., &amp; Ishiguro, H. (2020). Mind the voice!: Effect of robot voice pitch, robot voice gender, and user gender on user perception of teleoperated robots. In Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems (pp. 1–8).  [OA](https://scholar.google.co.uk/scholar?q=Song%2C%20S.%20Baba%2C%20J.%20Nakanishi%2C%20J.%20Yoshikawa%2C%20Y.%20Mind%20the%20voice%21%3A%20Effect%20of%20robot%20voice%20pitch%2C%20robot%20voice%20gender%2C%20and%20user%20gender%20on%20user%20perception%20of%20teleoperated%20robots%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Song%2C%20S.%20Baba%2C%20J.%20Nakanishi%2C%20J.%20Yoshikawa%2C%20Y.%20Mind%20the%20voice%21%3A%20Effect%20of%20robot%20voice%20pitch%2C%20robot%20voice%20gender%2C%20and%20user%20gender%20on%20user%20perception%20of%20teleoperated%20robots%202020) 

[^Sprenger_et+al_2013_a]: Sprenger, T., Tumasjan, A., Sandner, P., &amp; Welpe, I. (2013). Tweets and trades: The information content of stock microblogs. European Financial Management, 20(5), 926–957. https://doi.org/10.1111/j.1468036X.2013.12007.x  [OA](https://doi.org/10.1111/j.1468036X.2013.12007.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1468036X.2013.12007.x)

[^Stice_1991_a]: Stice, E. (1991). The market reaction to 10-K and 10-Q filings and to subsequent The Wall Street journal earnings announcements. The Accounting Review, 66(1), 42–55.  [OA](https://engine.scholarcy.com/oa_version?query=Stice%2C%20E.%20The%20market%20reaction%20to%2010-K%20and%2010-Q%20filings%20and%20to%20subsequent%20The%20Wall%20Street%20journal%20earnings%20announcements%201991&author=Stice&title=The%20market%20reaction%20to%2010-K%20and%2010-Q%20filings%20and%20to%20subsequent%20The%20Wall%20Street%20journal%20earnings%20announcements&year=1991) [GScholar](https://scholar.google.co.uk/scholar?q=Stice%2C%20E.%20The%20market%20reaction%20to%2010-K%20and%2010-Q%20filings%20and%20to%20subsequent%20The%20Wall%20Street%20journal%20earnings%20announcements%201991) [Scite](/scite_tallies?query=author%3AStice%2Ctitle%3AThe%20market%20reaction%20to%2010-K%20and%2010-Q%20filings%20and%20to%20subsequent%20The%20Wall%20Street%20journal%20earnings%20announcements%2Cyear%3A1991)

[^Stone_1963_a]: Stone, P., &amp; Hunt, E. (1963). A computer approach to content analysis: Studies using the general inquirer system. In Proceedings of the May 21-23, 1963, spring joint computer conference (pp. 241–256).  [OA](https://scholar.google.co.uk/scholar?q=Stone%2C%20P.%20Hunt%2C%20E.%20A%20computer%20approach%20to%20content%20analysis%3A%20Studies%20using%20the%20general%20inquirer%20system%201963) [GScholar](https://scholar.google.co.uk/scholar?q=Stone%2C%20P.%20Hunt%2C%20E.%20A%20computer%20approach%20to%20content%20analysis%3A%20Studies%20using%20the%20general%20inquirer%20system%201963) 

[^Sun_et+al_2019_a]: Sun, C., Qiu, X., Xu, Y., &amp; Huang, X. (2019). How to fine-tune BERT for text classification? In Chinese Computational Linguistics: 18th China National Conference, CCL 2019, Kunming, China, October 18–20, 2019, Proceedings 18 (pp. 194–206). Springer International Publishing.  [OA](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20fine-tune%20BERT%20for%20text%20classification%3F%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Sun%2C%20C.%20Qiu%2C%20X.%20Xu%2C%20Y.%20Huang%2C%20X.%20How%20to%20fine-tune%20BERT%20for%20text%20classification%3F%202019) 

[^Sun_et+al_2016_a]: Sun, L., Najand, M., &amp; Shen, J. (2016). Stock return predictability and investor sentiment: A high-frequency perspective. Journal of Banking &amp; Finance, 73, 147–164. https://doi.org/10.1016/j.jbankfin.2016.09.010  [OA](https://doi.org/10.1016/j.jbankfin.2016.09.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jbankfin.2016.09.010)

[^Tetlock_2007_a]: Tetlock, P. (2007). Giving content to investor sentiment: The role of media in the stock market. The Journal of Finance, 62(3), 1139–1168. https://doi.org/10.1111/j.1540-6261.2007.01232.x  [OA](https://doi.org/10.1111/j.1540-6261.2007.01232.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.1540-6261.2007.01232.x)

[^Tetlock_et+al_2008_a]: Tetlock, P., Saar-Tsechansky, M., &amp; Macskassy, S. (2008). More than words: Quantifying language to measure firms&#39; fundamentals. The Journal of Finance, 63(3), 1437–1467. https://doi.org/10.1111/j.15406261.2008.01362.x  [OA](https://doi.org/10.1111/j.15406261.2008.01362.x)  [Scite](/scite_tallies?query=https://doi.org/10.1111/j.15406261.2008.01362.x)

[^Troussas_et+al_2013_a]: Troussas, C., Virvou, M., Espinosa, K., Llaguno, K., &amp; Caro, J. (2013). Sentiment analysis of Facebook statuses using Naive Bayes classifier for language learning. In IISA 2013 (pp. 1–6). IEEE.  [OA](https://scholar.google.co.uk/scholar?q=Troussas%2C%20C.%20Virvou%2C%20M.%20Espinosa%2C%20K.%20Llaguno%2C%20K.%20Sentiment%20analysis%20of%20Facebook%20statuses%20using%20Naive%20Bayes%20classifier%20for%20language%20learning%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Troussas%2C%20C.%20Virvou%2C%20M.%20Espinosa%2C%20K.%20Llaguno%2C%20K.%20Sentiment%20analysis%20of%20Facebook%20statuses%20using%20Naive%20Bayes%20classifier%20for%20language%20learning%202013) 

[^Tumasjan_et+al_2010_a]: Tumasjan, A., Sprenger, T., Sandner, P., &amp; Welpe, I. (2010). Predicting elections with twitter: What 140 characters reveal about political sentiment. In Proceedings of the international AAAI conference on web and social media (Vol. 4, No. 1, pp. 178–185).  [OA](https://scholar.google.co.uk/scholar?q=Tumasjan%2C%20A.%20Sprenger%2C%20T.%20Sandner%2C%20P.%20Welpe%2C%20I.%20Predicting%20elections%20with%20twitter%3A%20What%20140%20characters%20reveal%20about%20political%20sentiment%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Tumasjan%2C%20A.%20Sprenger%2C%20T.%20Sandner%2C%20P.%20Welpe%2C%20I.%20Predicting%20elections%20with%20twitter%3A%20What%20140%20characters%20reveal%20about%20political%20sentiment%202010) 

[^Twedt_2012_a]: Twedt, B., &amp; Rees, L. (2012). Reading between the lines: An empirical examination of qualitative attributes of financial analysts&#39; reports. Journal of Accounting and Public Policy, 31(1), 1–21. https://doi.org/10.1016/j.jaccpubpol.2011.10.010  [OA](https://doi.org/10.1016/j.jaccpubpol.2011.10.010)  [Scite](/scite_tallies?query=https://doi.org/10.1016/j.jaccpubpol.2011.10.010)

[^Vaswani_et+al_2017_a]: Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., &amp; Polosukhin, I. (2017). Attention Is All You Need. Advances in neural information processing systems, 30.  [OA](https://engine.scholarcy.com/oa_version?query=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20Is%20All%20You%20Need%202017&author=Vaswani&title=Attention%20Is%20All%20You%20Need&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Shazeer%2C%20N.%20Parmar%2C%20N.%20Uszkoreit%2C%20J.%20Attention%20Is%20All%20You%20Need%202017) [Scite](/scite_tallies?query=author%3AVaswani%2Ctitle%3AAttention%20Is%20All%20You%20Need%2Cyear%3A2017)

[^Wallbott_1982_a]: Wallbott, H. G. (1982). Contributions of the German “expression psychology” to nonverbal communication research: Part III: Gait, gestures, and body movement. Journal of Nonverbal Behavior, 7, 20–32. https://doi.org/10.1007/BF01001775  [OA](https://doi.org/10.1007/BF01001775)  [Scite](/scite_tallies?query=https://doi.org/10.1007/BF01001775)

[^Wang_et+al_2012_a]: Wang, N., Kosinski, M., Stillwell, D., &amp; Rust, J. (2012). Can well-being be measured using Facebook status updates? Validation of Facebook&#39;s Gross National Happiness Index. Social Indicators Research, 115(1), 483–491. https://doi.org/10.1007/s11205-012-9996-9  [OA](https://doi.org/10.1007/s11205-012-9996-9)  [Scite](/scite_tallies?query=https://doi.org/10.1007/s11205-012-9996-9)

[^Wang_et+al_2018_a]: Wang, T. Y., Kawaguchi, I., Kuzuoka, H., &amp; Otsuki, M. (2018). Effect of manipulated amplitude and frequency of human voice on dominance and persuasiveness in audio conferences. Proceedings of the ACM on Human-Computer Interaction, 2(CSCW), 1–18.  [OA](https://engine.scholarcy.com/oa_version?query=Wang%2C%20T.Y.%20Kawaguchi%2C%20I.%20Kuzuoka%2C%20H.%20Otsuki%2C%20M.%20Effect%20of%20manipulated%20amplitude%20and%20frequency%20of%20human%20voice%20on%20dominance%20and%20persuasiveness%20in%20audio%20conferences%202018&author=Wang&title=Effect%20of%20manipulated%20amplitude%20and%20frequency%20of%20human%20voice%20on%20dominance%20and%20persuasiveness%20in%20audio%20conferences&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Wang%2C%20T.Y.%20Kawaguchi%2C%20I.%20Kuzuoka%2C%20H.%20Otsuki%2C%20M.%20Effect%20of%20manipulated%20amplitude%20and%20frequency%20of%20human%20voice%20on%20dominance%20and%20persuasiveness%20in%20audio%20conferences%202018) [Scite](/scite_tallies?query=author%3AWang%2Ctitle%3AEffect%20of%20manipulated%20amplitude%20and%20frequency%20of%20human%20voice%20on%20dominance%20and%20persuasiveness%20in%20audio%20conferences%2Cyear%3A2018)

[^Wang_2014_a]: Wang, W., &amp; Hua, Z. (2014). A semiparametric Gaussian copula regression model for predicting financial risks from earnings calls. In Proceedings of the 52nd annual meeting of the association for computational linguistics (Volume 1: Long Papers, pp. 1155–1165).  [OA](https://scholar.google.co.uk/scholar?q=Wang%2C%20W.%20Hua%2C%20Z.%20A%20semiparametric%20Gaussian%20copula%20regression%20model%20for%20predicting%20financial%20risks%20from%20earnings%20calls%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Wang%2C%20W.%20Hua%2C%20Z.%20A%20semiparametric%20Gaussian%20copula%20regression%20model%20for%20predicting%20financial%20risks%20from%20earnings%20calls%202014) 

[^Wolf_et+al_2020_a]: Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz, M., Davison, J., Shleifer, S., von Platen, P., Ma, C., Jernite, Y., Plu, J., Xu, C., Le Scao, T., Gugger, S.,... Rush, A. (2020). Transformers: State-of-the-art natural language processing. In Proceedings of the 2020 conference on empirical methods in natural language processing: System demonstrations (pp. 38–45).  [OA](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Wolf%2C%20T.%20Debut%2C%20L.%20Sanh%2C%20V.%20Chaumond%2C%20J.%20Transformers%3A%20State-of-the-art%20natural%20language%20processing%202020) 

[^Wu_et+al_2016_a]: Wu, Y., Schuster, M., Chen, Z., Le, Q.V., Norouzi, M., Macherey, W., Krikun, M., Cao, Y., Gao, Q., Macherey, K., &amp; Klingner, J. (2016). Google&#39;s neural machine translation system: Bridging the gap between human and machine translation. arXiv preprint arXiv:1609.08144.  [OA](https://arxiv.org/abs/1609.08144)  

[^Yang_et+al_2020_a]: Yang, K., Xu, H., &amp; Gao, K. (2020). CM-BERT: Cross-modal bert for textaudio sentiment analysis. In Proceedings of the 28th ACM International Conference on Multimedia (pp. 521–528).  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20K.%20Xu%2C%20H.%20Gao%2C%20K.%20CM-BERT%3A%20Cross-modal%20bert%20for%20textaudio%20sentiment%20analysis%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20K.%20Xu%2C%20H.%20Gao%2C%20K.%20CM-BERT%3A%20Cross-modal%20bert%20for%20textaudio%20sentiment%20analysis%202020) 

[^Article_et+al_2024_a]: How to cite this article: Todd, A., Bowden, J., &amp; Moshfeghi, Y. (2024). Text-based sentiment analysis in finance: Synthesising the existing literature and exploring future directions. Intelligent Systems in Accounting, Finance and Management, 31(1), e1549. https://doi.org/10.1002/isaf.1549  [OA](https://doi.org/10.1002/isaf.1549)  [Scite](/scite_tallies?query=https://doi.org/10.1002/isaf.1549)

