[[Gadi_AnnotatorsSelectionImpactCreationSentiment_2023]]

# [Annotators’ Selection Impact on the Creation of a Sentiment Corpus for the Cryptocurrency Financial Domain](https://doi.org/10.1109/access.2023.3334260)

## [[Manoel Fernando Alonso Gadi]]; [[Miguel‐Ángel Sicilia]]

## Abstract

Well-labeled natural language corpus data is essential for most natural language processing techniques, especially in specialized fields. However, cohort biases remain a significant challenge in machine learning. The narrowness of data sampling or the use of human annotators in cohorts is a prevalent issue for machine learning researchers, as it can introduce bias into the final product. During the development of the CryptoLin corpus for another research project, the authors became concerned about the potential influence of cohort bias on annotator selection. Therefore, this paper addresses whether cohort diversity improves labeling results through a repeated annotator process involving two annotator cohorts and a statistically robust comparison methodology. The use of statistical tests, such as the Chi-Square Independence test for absolute frequency tables, and the construction of confidence intervals for Kappa point estimates facilitate a rigorous analysis of differences between Kappa estimates. Furthermore, the application of a two-proportion z-test to compare the accuracy scores of UTAD and IE annotators for various pre-trained models, including Vader Sentiment Analysis, TextBlob Sentiment Analysis, Flair NLP library, and FinBERT Financial Sentiment Analysis with BERT, contributes to the advancement of knowledge in this field. The paper uses Cryptocurrency Linguo (CryptoLin), a corpus of 2683 cryptocurrency-related news articles spanning more than 3 years, and compares two selection criteria for annotators. CryptoLin was annotated twice with discrete values representing negative, neutral, and positive news, respectively. The first annotation was done by twenty-seven annotators from the same cohort. Each news title was randomly assigned and blindly annotated by three human annotators. The second annotation was carried out by eighty-three annotators from three cohorts. Each news title was randomly assigned and blindly annotated by three human annotators, one from each cohort. In both annotations, a simple voting consensus mechanism was applied. The first annotation used the same cohort with students from the same nationality and background. The second used three cohorts with students from a very diverse set of nationalities and educational backgrounds. The results demonstrate that manual labeling done by both groups was acceptable according to inter-rater reliability coefficients Fleiss’s Kappa, Krippendorff’s Alpha, and Gwet’s AC1. Preliminary analysis using Vader, TextBlob, Flair, and FinBERT confirmed the utility of the dataset for further refining sentiment analysis algorithms. Our results also show that the more diverse the annotator pool, the better it performs across all measured aspects.

## Key concepts

#machine_learning; #natural_language_processing; #financial_domain; #inter_rater_reliability; #cohort_bias; #annotator; #bert_language_model; #cryptocurrency; #kappa_statistic; #sentiment_analysis

## Quote
>
> This research investigates the potential influence of cohort bias on the selection of annotators, providing insights into how cohort diversity can improve labeling results and highlighting the importance of considering cohort bias when selecting annotators.

## Key points

- This article aims to explore the impact of annotator selection on the creation of a sentiment corpus for the cryptocurrency financial domain in the context of event studies and provide insights into how to mitigate these biases
- This paper addresses a critical question in the field of machine learning and natural language processing: whether the diversity of annotator cohorts can improve the accuracy of labeling results
- The application of a two-proportion z-test to compare the accuracy scores of University Center for Technology and Digital Art (UTAD) and IE annotators for various pre-trained models contributes to the advancement of knowledge in this field
- The results suggest that there is a statistical difference between UTAD and IE annotators when selecting the news sentiment
- This research provides valuable insights into the potential influence of cohort bias on the selection of annotators. Both manual labeling done by the UTAD and the IE students was acceptable according to inter-rater reliability coefficients Fleiss’s Kappa, Krippendorff’s Alpha, and Gwet’s AC1; and preliminary analysis utilizing Vader, Textblob, Flair, and FinBERT confirmed the utility of the data set labeling for further refinement of sentiment analysis algorithms
- The findings suggest that there is a statistical difference between UTAD and IE annotators when selecting news sentiment, highlighting the importance of considering cohort bias when selecting annotators

## Summary

### Introduction to the Problem

Creating a sentiment corpus for the cryptocurrency financial domain is essential for event studies, but machine learning cohort biases can introduce bias into the final product.
This paper explores the impact of annotator selection on the creation of a sentiment corpus and whether cohort diversity improves the labeling result.

### Methodology

The paper uses CryptoLin, a corpus of 2683 cryptocurrency-related news articles, and compares two selection criteria for annotators.
The first annotation was done by 27 annotators from the same cohort, while the second annotation was carried out by 83 annotators from three cohorts with diverse nationalities and educational backgrounds.
The results demonstrate that manual labeling by both groups was acceptable, as indicated by inter-rater reliability coefficients.

### Results And Conclusion

The results show that the more diverse the annotator pool, the better it performs across all measured aspects.
The paper concludes that cohort diversity can improve labeling accuracy and provides insights into mitigating biases in machine learning.
The use of statistical tests and the construction of confidence intervals facilitate a rigorous analysis of differences in labeling results across cohorts.

### Annotators

The annotators were undergraduate data science students from the University Center for Technology and Digital Art in Spain and master's students at IE University with an average of eight years of work experience.
The annotators were fluent in English or had high reading ability and participated voluntarily.
There were 83 annotators in total, with a diverse range of nationalities and educational backgrounds.

### Annotation Process

Each news article was randomly assigned to three annotators, one from each cohort.
The annotators labeled each news article with 1 if positive for the Cryptocurrency industry, 0 if neutral, and -1 if negative.
A consensus mechanism was applied, and no annotator had access to information on which news was assigned to whom.
The annotation process was designed to maintain the students' existing biases and not unintentionally standardize bias.

### Results And Analysis

The results showed a statistical difference between the UTAD and IE annotators in their selection of news sentiment.
The inter-rater reliability coefficients, including Fleiss's Kappa, Krippendorff's Alpha, and Gwet's AC1, were calculated to assess the quality of the annotations.
The results indicated that the labeling carried out by the IE students consistently outperformed that of the other students in all aspects.
The use of pre-trained NLP algorithms, such as Vader, TextBlob, Flair, and FinBERT, confirmed the utility of the dataset labeling for further refining sentiment analysis algorithms.

### Findings

The research found a statistical difference between UTAD and IE annotators in their selection of news sentiment, highlighting the importance of accounting for cohort bias.
This suggests that cohort bias can impact annotator selection and assignment.

### Contribution

The study advances knowledge in the field by investigating cohort bias in annotator selection.
It presents an important step towards improving the understanding of how to mitigate cohort biases.

### Data

The UTAD and IE datasets, as well as the Jupyter Notebook containing the analysis, are available in separate GitHub projects for reproducibility.
The authors acknowledge the contributions of students from UTAD and IE University who labeled the CryptoLinUTAD and CryptoLinIE data sets.

## Study subjects

### 2683 cryptocurrency-related news articles

- Furthermore, the application of a two-proportion z-test to compare the accuracy scores of UTAD and IE annotators for various pre-trained models, including Vader Sentiment Analysis, TextBlob Sentiment Analysis, Flair NLP library, and FinBERT Financial Sentiment Analysis with BERT, contributes to the advancement of knowledge in this field. The paper uses Cryptocurrency Linguo (CryptoLin), a corpus of 2683 cryptocurrency-related news articles spanning more than 3 years, and compares two selection criteria for annotators. CryptoLin was annotated twice with discrete values representing negative, neutral, and positive news, respectively

### 3 human annotators

- The first annotation was done by twentyseven annotators from the same cohort. Each news title was randomly assigned and blindly annotated by three human annotators. The second annotation was carried out by eighty-three annotators from three cohorts

## Data analysis

- #method/categorical_variables
- #method/roc_curve_method
- #method/inter_rater_reliability_coefficients
- #method/kappa_statistic
- #method/chi_square_statistic
- #method/chisquare_independence_test
- #method/chi_square_test

## Findings

- <mark class="claim"><mark class="fact">The results demonstrate that manual labeling done by both groups was acceptable according to inter-rater reliability coefficients</mark> Fleiss’s Kappa, Krippendorff’s Alpha, and Gwet’s AC1</mark>
- <mark class="claim"><mark class="fact">The results suggest that there is a statistical difference between UTAD</mark> and IE annotators when selecting the news sentiment</mark>
- <mark class="claim">The findings suggest that there is indeed a statistical difference between UTAD and IE annotators when selecting news sentiment, highlighting the importance of considering cohort bias when selecting annotators</mark>

##  Builds on previous research

- According to their website, The Block is dedicated to transparent journalism and had 65 employees as of Tuesday, May 3rd, 2022. Moreover, we have adopted the consensus mechanism proposed by [^14], using three individual annotators selected from independent, diverse cohorts rather than work groups.
- The column ‘reasoning’ provides an explanation of the combined decision. The color green represents an easy decision, while the colors yellow and red represent decisions that have some sort of disagreement between annotators, but instead of using a 4th annotator in controversial cases as done by [^3], we decided to set the annotation equal to 0 (neutral) as the number of cases is small and, as we will see later, both inter-annotator agreement study and pre-trained sentiment analysis show effective quality of the annotation as it is.
- IV. INTER-ANNOTATOR AGREEMENT STUDY As a first quality control of CryptoLin we used the steps followed by [^4] and calculated the inter-rater reliability coefficients: Fleiss’ kappa (κ) [^18], Krippendorf’s alpha (α) [^19], and Gwet’s AC1 [^20] on the aligned span annotations using the Multi Class Confusion Matrix Library for Python provided by [^21].

## Contributions

- In conclusion, this paper addresses the question of whether cohort diversity improves the labeling result through the implementation of a repeated annotator process. The utilization of statistical tests and <mark class="fact">the construction of confidence intervals facilitates a rigorous analysis of the differences between Kappa estimates</mark>. The application of a two-proportion z-test to compare the accuracy scores of UTAD and IE annotators across various <mark class="fact">pre-trained models </mark> advances knowledge in this field. <mark class="claim"><mark class="fact">The results suggest that there is a statistical difference between UTAD</mark> and IE annotators when selecting the news sentiment</mark>. This research provides valuable insights into the potential influence of cohort bias on annotator selection.

## Limitations

- The study has limitations, including the potential for noise or bias due to the use of heuristics or emoticons to label the data automatically. The study also notes that using a small sample or a specific domain of the data may limit the generalizability or applicability of the results.
- The study has some limitations, including the use of a specific data set and the reliance on statistical tests to analyze the differences between Kappa estimates.

## Future work

- The study suggests that future work could explore the use of conversational AI for labeling. The study also notes that further research is needed to investigate the impact of annotator selection on the creation of a sentiment corpus.
- The study suggests that future research should focus on exploring the impact of cohort diversity on the labeling results of other types of data, and on developing new methods for selecting and assigning annotators.
- The future work may involve further investigation into the influence of cohort bias on annotator selection and the development of methods to mitigate cohort biases.

## References

[^3]: T. Daudert, ‘‘A multi-source entity-level sentiment corpus for the financial domain: The FinLin corpus,’’ Lang. Resour. Eval., vol. 56, no. 1, pp. 333–356, Mar. 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Daudert%2C%20T.%20%E2%80%98A%20multi-source%20entity-level%20sentiment%20corpus%20for%20the%20financial%20domain%3A%20The%20FinLin%20corpus%2C%E2%80%99%202022-03&author=Daudert&title=%E2%80%98A%20multi-source%20entity-level%20sentiment%20corpus%20for%20the%20financial%20domain%3A%20The%20FinLin%20corpus%2C%E2%80%99&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Daudert%2C%20T.%20%E2%80%98A%20multi-source%20entity-level%20sentiment%20corpus%20for%20the%20financial%20domain%3A%20The%20FinLin%20corpus%2C%E2%80%99%202022-03) [Scite](/scite_tallies?query=author%3ADaudert%2Ctitle%3A%E2%80%98A%20multi-source%20entity-level%20sentiment%20corpus%20for%20the%20financial%20domain%3A%20The%20FinLin%20corpus%2C%E2%80%99%2Cyear%3A2022)

[^4]: G. Jacobs and V. Hoste, ‘‘SENTiVENT: Enabling supervised information extraction of company-specific events in economic and financial news,’’ Lang. Resour. Eval., vol. 56, no. 1, pp. 225–257, Mar. 2022.  [OA](https://engine.scholarcy.com/oa_version?query=Jacobs%2C%20G.%20Hoste%2C%20V.%20%E2%80%98SENTiVENT%3A%20Enabling%20supervised%20information%20extraction%20of%20company-specific%20events%20in%20economic%20and%20financial%20news%2C%E2%80%99%202022-03&author=Jacobs&title=%E2%80%98SENTiVENT%3A%20Enabling%20supervised%20information%20extraction%20of%20company-specific%20events%20in%20economic%20and%20financial%20news%2C%E2%80%99&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Jacobs%2C%20G.%20Hoste%2C%20V.%20%E2%80%98SENTiVENT%3A%20Enabling%20supervised%20information%20extraction%20of%20company-specific%20events%20in%20economic%20and%20financial%20news%2C%E2%80%99%202022-03) [Scite](/scite_tallies?query=author%3AJacobs%2Ctitle%3A%E2%80%98SENTiVENT%3A%20Enabling%20supervised%20information%20extraction%20of%20company-specific%20events%20in%20economic%20and%20financial%20news%2C%E2%80%99%2Cyear%3A2022)

[^14]: O. R. Meireles, G. Rosman, M. S. Altieri, L. Carin, G. Hager, A. Madani, N. Padoy, C. M. Pugh, P. Sylla, T. M. Ward, and D. A. Hashimoto, ‘‘SAGES consensus recommendations on an annotation framework for surgical video,’’ Surgical Endoscopy, vol. 35, pp. 4918–4929, Jul. 2021.  [OA](https://engine.scholarcy.com/oa_version?query=Meireles%2C%20O.R.%20Rosman%2C%20G.%20Altieri%2C%20M.S.%20Carin%2C%20L.%20%E2%80%98SAGES%20consensus%20recommendations%20on%20an%20annotation%20framework%20for%20surgical%20video%2C%E2%80%99%202021-07&author=Meireles&title=%E2%80%98SAGES%20consensus%20recommendations%20on%20an%20annotation%20framework%20for%20surgical%20video%2C%E2%80%99&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Meireles%2C%20O.R.%20Rosman%2C%20G.%20Altieri%2C%20M.S.%20Carin%2C%20L.%20%E2%80%98SAGES%20consensus%20recommendations%20on%20an%20annotation%20framework%20for%20surgical%20video%2C%E2%80%99%202021-07) [Scite](/scite_tallies?query=author%3AMeireles%2Ctitle%3A%E2%80%98SAGES%20consensus%20recommendations%20on%20an%20annotation%20framework%20for%20surgical%20video%2C%E2%80%99%2Cyear%3A2021)

[^18]: J. L. Fleiss, ‘‘Measuring nominal scale agreement among many raters,’’ Psychol. Bull., vol. 76, no. 5, pp. 378–382, Nov. 1971.  [OA](https://engine.scholarcy.com/oa_version?query=Fleiss%2C%20J.L.%20%E2%80%98Measuring%20nominal%20scale%20agreement%20among%20many%20raters%2C%E2%80%99%201971-11&author=Fleiss&title=%E2%80%98Measuring%20nominal%20scale%20agreement%20among%20many%20raters%2C%E2%80%99&year=1971) [GScholar](https://scholar.google.co.uk/scholar?q=Fleiss%2C%20J.L.%20%E2%80%98Measuring%20nominal%20scale%20agreement%20among%20many%20raters%2C%E2%80%99%201971-11) [Scite](/scite_tallies?query=author%3AFleiss%2Ctitle%3A%E2%80%98Measuring%20nominal%20scale%20agreement%20among%20many%20raters%2C%E2%80%99%2Cyear%3A1971)

[^19]: K. Krippendorff, ‘‘Reliability in content analysis: Some common misconceptions and recommendations,’’ Hum. Commun. Res., vol. 30, no. 3, pp. 411–433, 2006.  [OA](https://engine.scholarcy.com/oa_version?query=Krippendorff%2C%20K.%20%E2%80%98Reliability%20in%20content%20analysis%3A%20Some%20common%20misconceptions%20and%20recommendations%2C%E2%80%99%202006&author=Krippendorff&title=%E2%80%98Reliability%20in%20content%20analysis%3A%20Some%20common%20misconceptions%20and%20recommendations%2C%E2%80%99&year=2006) [GScholar](https://scholar.google.co.uk/scholar?q=Krippendorff%2C%20K.%20%E2%80%98Reliability%20in%20content%20analysis%3A%20Some%20common%20misconceptions%20and%20recommendations%2C%E2%80%99%202006) [Scite](/scite_tallies?query=author%3AKrippendorff%2Ctitle%3A%E2%80%98Reliability%20in%20content%20analysis%3A%20Some%20common%20misconceptions%20and%20recommendations%2C%E2%80%99%2Cyear%3A2006)

[^20]: K. L. Gwet, ‘‘Computing inter-rater reliability and its variance in the presence of high agreement,’’ Brit. J. Math. Stat. Psychol., vol. 61, no. 1, pp. 29–48, May 2008.  [OA](https://engine.scholarcy.com/oa_version?query=Gwet%2C%20K.L.%20%E2%80%98Computing%20inter-rater%20reliability%20and%20its%20variance%20in%20the%20presence%20of%20high%20agreement%2C%E2%80%99%202008-05&author=Gwet&title=%E2%80%98Computing%20inter-rater%20reliability%20and%20its%20variance%20in%20the%20presence%20of%20high%20agreement%2C%E2%80%99&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Gwet%2C%20K.L.%20%E2%80%98Computing%20inter-rater%20reliability%20and%20its%20variance%20in%20the%20presence%20of%20high%20agreement%2C%E2%80%99%202008-05) [Scite](/scite_tallies?query=author%3AGwet%2Ctitle%3A%E2%80%98Computing%20inter-rater%20reliability%20and%20its%20variance%20in%20the%20presence%20of%20high%20agreement%2C%E2%80%99%2Cyear%3A2008)

[^21]: S. Haghighi, M. Jasemi, and S. Hessabi, ‘‘PyCM: Multi class confusion matrix library in Python,’’ Zenodo, Tech. Rep., 2018.  [OA](https://engine.scholarcy.com/oa_version?query=Haghighi%2C%20S.%20Jasemi%2C%20M.%20Hessabi%2C%20S.%20%E2%80%98PyCM%3A%20Multi%20class%20confusion%20matrix%20library%20in%20Python%2C%E2%80%99%202018&author=Haghighi&title=%E2%80%98PyCM%3A%20Multi%20class%20confusion%20matrix%20library%20in%20Python%2C%E2%80%99&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Haghighi%2C%20S.%20Jasemi%2C%20M.%20Hessabi%2C%20S.%20%E2%80%98PyCM%3A%20Multi%20class%20confusion%20matrix%20library%20in%20Python%2C%E2%80%99%202018) [Scite](/scite_tallies?query=author%3AHaghighi%2Ctitle%3A%E2%80%98PyCM%3A%20Multi%20class%20confusion%20matrix%20library%20in%20Python%2C%E2%80%99%2Cyear%3A2018)
