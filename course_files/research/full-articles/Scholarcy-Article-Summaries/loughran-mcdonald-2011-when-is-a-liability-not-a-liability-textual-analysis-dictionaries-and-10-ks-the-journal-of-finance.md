[[Loughran_WhenIsLiabilityNotLiability_2011]]

# [When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10‐Ks](https://doi.org/10.1111/j.1540-6261.2010.01625.x)

## [[Tim Loughran]]; [[Bill McDonald]]

## Abstract
ABSTRACT Previous research uses negative word counts to measure the tone of a text. ==We show that word lists developed for other disciplines misclassify common words in financial text==. In a large sample of 10‐Ks during 1994 to 2008, almost three‐fourths of the words identified as negative by the widely used Harvard Dictionary are words typically not considered negative in financial contexts. ==We develop an alternative negative word list, along with five other word lists, that better reflect tone in financial text==. We link the word lists to 10‐K filing returns, trading volume, return volatility, fraud, material weakness, and unexpected earnings.

## Key concepts
#claim/common_word; #common_word; #textual_analysis; #claim/management_discussion_and_analysis; #management_discussion_and_analysis

## Quote
> The study reveals that word lists developed for other disciplines misclassify common words in financial text, and proposes an alternative negative word list that better reflects tone in financial text, finding significant relations between the word lists and file date returns, trading volume, and subsequent return volatility.

## Key points
- Previous research uses negative word counts to measure the tone of a text
- We show that word lists developed for other disciplines misclassify common words in financial text
- We focus on the TAGNeg file used in [^Tetlock_et+al_2008_a]) because it is a nonproprietary list that has been used frequently in prior studies and should be representative of negative word lists developed in disciplines other than finance and accounting
- We find that almost three-fourths of negative word counts in 10-K filings based on the Harvard dictionary are typically not negative in a financial context
- Even though the apparent power of the two negative word lists is similar, we suggest the use of our list to avoid those words in the Harvard-IV-4 TagNeg (H4N) list that might proxy for industry or other unintended effects
- Our results and others’, suggest that textual analysis can contribute to our ability to understand the impact of information on stock returns, and even if tone does not directly cause returns it might be an efficient way for analysts to capture other sources of information


## Summary

### Introduction To Textual Analysis
The use of textual analysis in finance and accounting research has grown, with studies examining the tone and sentiment of corporate 10-K reports, newspaper articles, and investor message boards.
However, the word lists used to measure tone, such as the Harvard Psychosociological Dictionary, may not be suitable for financial contexts due to the multiple meanings of English words.

### Limitations Of Existing Word Lists
The Harvard-IV-4 TagNeg (H4N) list, a commonly used source for word classifications, misclassifies many words in financial texts.
Almost three-fourths of the words identified as negative by the H4N list are words typically not considered negative in financial contexts, such as "tax", "cost", "capital", and "liability".
These misclassifications can add noise to the measurement of tone and attenuate estimated regression coefficients.

### Development Of Alternative Word Lists
To address these limitations, an alternative negative word list, Fin-Neg, has been developed, which better reflects tone in financial text.
The Fin-Neg list includes 2,337 words that typically have negative implications in a financial sense.
Additionally, five other word lists have been created, including positive, uncertainty, litigious, strong modal, and weak modal word categories.
These word lists have been linked to 10-K filing returns, trading volume, return volatility, fraud, material weakness, and unexpected earnings, and have been shown to produce significant relations with these variables.

### Data Collection
The study requires at least 250 words in the MD&amp;A section of 10-K filings, resulting in 37,287 firm-year observations.
The parsing process involves excluding 10-K tables and exhibits, as they contain template language that is less meaningful in measuring tone.
The study also considers two samples documenting negative financial events: firms subject to shareholder litigation under Rule 10b-5 and firms disclosing material weaknesses in internal control.

### Methodology
The study uses a bag of words method, requiring the parsing of 10-K documents into vectors of words and word counts.
Term weighting schemes are used to acknowledge that raw word counts are not the best measure of a word's information content.
The study uses a modified term weighting scheme that adjusts for document length, and examines both the simple proportion of words for a given tonal classification and the tf.idf weighted measures.
The study uses 1973 regressions with Newey–West 1987 standard errors and one lag.
The estimates are based on a sample of 50,115 10-Ks over 1994 to 2008.
The study also uses Fama-French 1997 industry dummies, a constant, and control variables from Table IV.
The term weighting procedure (tf.idf) is used to improve the signal-to-noise in the lists.

### Textual Analysis
The study focuses on the TAGNeg file used in prior studies, which is a nonproprietary list of negative words.
The classification of words in a document accounts for inflections, and the study expands the H4N list by inflecting each word to forms that retain the original meaning of the root word.
The study also proposes five other word lists: positive, uncertainty, litigious, strong modal words, and weak modal words.
A discipline-specific word list, such as the Fin-Neg list, can reduce measurement error and increase power, as it is tailored to business terminology.

### Word Lists
The study creates several word lists, including Fin-Neg (negative words), Fin-Pos (positive words), Fin-Unc (uncertainty words), Fin-Lit (litigious words), MW-Strong (strong modal words), and MW-Weak (weak modal words).
The Fin-Neg list has 2,337 words, including inflections, and is compared to the H4N-Inf list, which has 4,187 words.
The Fin-Neg list is found to be more suitable for financial documents, as it includes words that are more likely to be negative in a financial sense.
The study examines the relationship between word lists, specifically the Harvard-IV-4-Neg with inflections (H4N-Inf) and Fin-Neg lists, and filing period returns.
The Fin-Neg list appears to capture useful information, with firms including a lower percentage of pessimistic words having slightly negative returns, while those with a high percentage of negative words have sharply negative median returns.
The term-weighted measures of H4N-Inf and Fin-Neg are both negative in sign, significant, and essentially identical in their impact.

### Tone Analysis
The study examines the tone of 10-K documents using the word lists.
The results show that the H4N-Inf list misclassifies many words as negative, which can add noise to the measure of tone.
For example, words like "costs" and "capital" are not typically negative in financial documents.
The Fin-Neg list is found to be more accurate in capturing negative tone, with words like "loss", "litigation", and "termination" being more likely to be negative in a financial sense.

### Industry Effects
The study also examines the industry effects of the word lists.
The results show that some words, like "mine" in the mining industry, can be misclassified as negative due to their common usage in the industry.
The Fin-Neg list is found to be less prone to these industry effects, making it a better choice for financial researchers.
The study also notes that the association of the H4N-Inf list with financial variables may be due to its unintentional capture of industry effects.

### Regression Results
The regression results show that the Fin-Neg list has a significantly negative coefficient, indicating that higher proportions of negative words are associated with lower excess returns.
The weighted measures of both word lists are negative in sign and significant, but the adjusted R2 is still low, around 2.6%.
The results also show that the MD&amp;A section of the 10-K does not contain richer tonal content, and the sample for which the MD&amp;A section is available varies systematically over time.

### Trading Strategy
The study calculates the Fama and French four-factor portfolio returns generated by taking a long position in stocks with a low negative word count and a short position in stocks with a high negative count.
Although the alphas across the four regressions are positive, none of the values are statistically significant, indicating that the relation between 1-year returns and negative word counts is not enough to warrant active trading by investors.

### Results
The study finds that the word lists are highly significant in explaining postevent return volatility.
The coefficients on the word lists have positive signs, indicating that a higher proportion of positive, negative, or modal words is linked with larger stock return volatility in the year after the filing.
The study also finds that firms with a higher proportion of negative financial words or strong modal words are more likely to report material weaknesses in their internal accounting controls.

### Applications
The study applies the word lists to predict quarterly earnings and finds that the coefficients on the Harvard and Fin-Neg word lists are positive and statistically significant, indicating that more negative words point to more positive subsequent earnings surprises for the firm.
The study also provides preliminary correlation evidence of the relative performance of the Harvard and Fin-Neg dictionaries in two other applications: seasoned equity offerings and news stories relating to U.S firms in the Dow Jones archive.
The paper finds evidence that some word lists are related to market reactions around the 10-K filing date, trading volume, unexpected earnings, and subsequent stock return volatility.
The word lists are also linked to firms accused of accounting fraud and to firms reporting material weaknesses in their accounting controls.
The use of term weighting and the proposed word list can contribute to a better understanding of the impact of information on stock returns, although the causal link between tone and returns is still unclear.

### Limitations
The Harvard dictionary's negative word list has limitations in a financial context, with almost three-fourths of negative word counts not being negative in this context.
Common words like depreciation, liability, foreign, and board are not tonal when occurring in a 10-K filing.
The use of nonbusiness word lists can lead to a high misclassification rate and spurious correlations.

### Solutions
The paper proposes two solutions to this measurement problem.
First, a list of words with negative meaning in financial reports is created by examining words that occur in at least 5% of the SEC's 10-K universe.
Second, a term weighting scheme is developed to attenuate the impact of high frequency words and allow less frequently used words to have greater impact.
This scheme can lower the noise introduced by word misclassifications.


## Study subjects

### 60 observations
- The volume of shares traded in days [−252, −6] prior to the file date divided by shares outstanding on the file date. ==At least 60 observations of daily volume must be available to be included in the sample==. The prefile date Fama–French alpha based on a regression of their three-factor model using days [−252, −6]

### 44822 firms
- We download all 10-Ks and 10-K405s, excluding amended documents, from the EDGAR website (www.sec.gov) over 1994 to 2008.4 Table I shows how the original sample of 10-Ks is impacted by our data filters and data requirements. ==Most notably, the requirement of a CRSP PERMNO match reduces the original sample of 121,217 10-Ks by 44,822 firms.5==. This is not surprising as many of the

## Data analysis
- #method/t_test
- #method/negative_word_lists_using_filing_period_excess_return_regressions

## Findings
- The word loss appears in more than 90% of the documents, which implies that the second term will decrease the first term
- As the Fin-Neg list has only about half as many words as the <a class="keyword" href="#" title="Harvard-IV-4 TagNeg">H4N</a>-Inf list, it is not surprising that, on average, a lower percentage of 10-K words are in the Fin-Neg word list (3.79% vs. 1.39%)
- Other Variables Event period [0,3] excess return Size ($billions) Book-to-market Turnover One-year preevent FF alpha Institutional ownership NASDAQ dummy Standardized unexpected earnings Analysts’ earnings forecast dispersion Analysts’ earnings revisions the mean for <a class="keyword" href="#" title="Harvard-IV-4 TagNeg">H4N</a>-Inf rising from about 3.5% to 4.3% and the mean for FinNeg rising from about 1.1% to 1.7%
- FinNeg reports a much smaller percentage increase for the median value (1.36%
- In an extreme example, the word mine in the 1999 10-K of Coeur d’Alene Mines Corporation accounts for over 25% of all the <a class="keyword" href="#" title="Harvard-IV-4 TagNeg">H4N</a>-Inf negative word counts
- Consistent with the bivariate correlations, <a class="keyword" href="#" title="Harvard-IV-4 TagNeg">H4N</a>-Inf is not significantly related to the file date excess returns while Fin-Neg has a significantly negative coefficient (t-statistic of −2.64)
- The last row of Panel B reports that all of the word lists are positively signed and significantly related to subsequent stock return volatility.19
- In tests on the 10-K filing date, <mark class="fact">our negative word list is significantly related to announcement returns</mark>

##  Builds on previous research
- Examples of qualitative studies not based on textual analysis include [^Coval_2001_a]), who examine the relation between trading volume in futures contracts and noise levels in the trading pits, and Mayew and Venkatachalam (2009), who analyze conference call audio files for positive or negative vocal cues revealed by managers’ vocal signatures. ==Although we focus on the more common word categorization== (bag of words) method for measuring tone, other papers consider alternative approaches based on vector distance, Naıve Bayes classifications, likelihood ratios, or other classification algorithms. (See, for example, [^Das_2001_a]), [^Antweiler_2004_a]), or [^Li_2009_a])).
- Firms in the 10b-5 sample include Enron, Boston Chicken, and Cardinal Health. ==Our seco==nd sample considers [^Doyle_et+al_2007_a]) firms disclosing at least one material weakness in internal control between August 2002 and November 2005.10 These disclosures are an artifact of Sections 302 and 404 of the Sarbanes-Oxley Act.
- The event period for the file date return is based on Griffin (2003, Table II), who documents that 10-Ks’ “elevated response extends to day 3” (p. 447).11. ==In our regressions we include as control variables firm size, book-to-market, share turnover, prefile date Fama==–French alpha (Pre FFAlpha), institutional ownership, and a dummy variable for NASDAQ listing.12 The first four of these variables are used in [^Tetlock_et+al_2008_a]).
- 12 See the Appendix at the end of the main text for detailed definitions of the variables described in this section. ==the control variables to include analyst dispersion and analyst revisions, as in== [^Tetlock_et+al_2008_a]).
- For a more general discussion of term weighting see Manning and Schutze (2003) or [^Chisholm_1999_a]). Since ==we are comparing different documents, length matters==. .
- The current version of the Harvard Psychosociological Dictionary, is available through the GI website (see http://www.wjh.harvard.edu/∼inquirer/). ==We focus== on the TAGNeg file used in [^Tetlock_et+al_2008_a]) because it is a nonproprietary list that has been used frequently in prior studies and should be representative of negative word lists developed in disciplines other than finance and accounting.
- For completeness, however, when we create additional. 14 For a discussion of the ==early research in textual analysis, see [^Stone_et+al_1966_a]). 15 We expand the word list by explicitly identifying appropriate inflections to avoid errors associated with stemming== (i.e., assigning morphological variants to common root words).

## Differs from previous work
- Our tests focus on the infected H4N list, which we label H4N-Inf. [^Tetlock_2007_a]), Engelberg (2008), and [^Kothari_et+al_2008_a]) find little incremental information in the Harvard positive word list, and thus ==we do not include this GI category in the analysis==.

##  Confirmation of earlier findings
- Examples are [^Antweiler_2004_a]), [^Tetlock_2007_a]), Engelberg (2008), Li (2008), and [^Tetlock_et+al_2008_a]). ==The results to date indicate that negative word classifications can be effective in measuring tone, as reflected by significant correlations with other financial variables==.

## Contributions
- Summary Statistics for the1994 to 2008 10-K SampleThe first seven variables represent the proportion of occurrences for a given word list relative to the total number of words. The word lists are available in the Internet Appendix or at http://www.nd.edu/∼mcdonald/Word Lists.html. See the Appendix for the other variable definitions. The sample sizes for the last three earnings-related variables are 28,679 for the full 10-K sample and 21,240 for the MD&amp;A subsample.    Variable

## Future work
- The future work suggested by the study is to use the proposed word lists to address specific topics of interest, and to explore the use of textual analysis to understand the impact of information on stock returns.


## References
[^Antweiler_2004_a]: Antweiler, Werner, and Murray Z. Frank, 2004, Is all that talk just noise? The information content of Internet stock message boards, Journal of Finance 59, 1259–1293.  [OA](https://engine.scholarcy.com/oa_version?query=Antweiler%2C%20Werner%20Frank%2C%20Murray%20Z.%20Is%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20Internet%20stock%20message%20boards%202004&author=Antweiler&title=Is%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20Internet%20stock%20message%20boards&year=2004) [GScholar](https://scholar.google.co.uk/scholar?q=Antweiler%2C%20Werner%20Frank%2C%20Murray%20Z.%20Is%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20Internet%20stock%20message%20boards%202004) [Scite](/scite_tallies?query=author%3AAntweiler%2Ctitle%3AIs%20all%20that%20talk%20just%20noise%3F%20The%20information%20content%20of%20Internet%20stock%20message%20boards%2Cyear%3A2004)

[^Baayen_2001_a]: Baayen, R. Harald, 2001, Word Frequency Distributions (Kluwer Academic Publishers, The Netherlands).  [OA](https://scholar.google.co.uk/scholar?q=Baayen%2C%20R.Harald%20Word%20Frequency%20Distributions%20%28Kluwer%20Academic%20Publishers%2C%20The%20Netherlands%202001) [GScholar](https://scholar.google.co.uk/scholar?q=Baayen%2C%20R.Harald%20Word%20Frequency%20Distributions%20%28Kluwer%20Academic%20Publishers%2C%20The%20Netherlands%202001) 

[^Berelson_1952_a]: Berelson, Bernard R., 1952, Content Analysis in Communication Research (The Free Press, Glencoe, IL).  [OA](https://scholar.google.co.uk/scholar?q=Berelson%2C%20Bernard%20R.%20Content%20Analysis%20in%20Communication%20Research%201952) [GScholar](https://scholar.google.co.uk/scholar?q=Berelson%2C%20Bernard%20R.%20Content%20Analysis%20in%20Communication%20Research%201952) 

[^Chisholm_1999_a]: Chisholm, Erica, and Tamara G. Kolda, 1999, New term weighting formulas for the vector space method in information retrieval, Technical Report Number ORNL-TM-13756, Oak Ridge National Laboratory, Oak Ridge, TN.  [OA](https://scholar.google.co.uk/scholar?q=Chisholm%2C%20Erica%20Kolda%2C%20Tamara%20G.%20New%20term%20weighting%20formulas%20for%20the%20vector%20space%20method%20in%20information%20retrieval%201999) [GScholar](https://scholar.google.co.uk/scholar?q=Chisholm%2C%20Erica%20Kolda%2C%20Tamara%20G.%20New%20term%20weighting%20formulas%20for%20the%20vector%20space%20method%20in%20information%20retrieval%201999) 

[^Coval_2001_a]: Coval, Joshua D., and Tyler Shumway, 2001, Is sound just noise? Journal of Finance 56, 1887–1910.  [OA](https://engine.scholarcy.com/oa_version?query=Coval%2C%20Joshua%20D.%20Shumway%2C%20Tyler%20Is%20sound%20just%20noise%3F%202001&author=Coval&title=Is%20sound%20just%20noise%3F&year=2001) [GScholar](https://scholar.google.co.uk/scholar?q=Coval%2C%20Joshua%20D.%20Shumway%2C%20Tyler%20Is%20sound%20just%20noise%3F%202001) [Scite](/scite_tallies?query=author%3ACoval%2Ctitle%3AIs%20sound%20just%20noise%3F%2Cyear%3A2001)

[^Das_2001_a]: Das, Sanjiv, and Mike Chen, 2001, Yahoo! for Amazon: Opinion extraction from small talk on the web, Working paper, Santa Clara University. Demers, Elizabeth, and Clara Vega, 2008, Soft information in earnings announcements: News or noise? Working paper, INSEAD. Dovring, Karin, 1954, Quantitative semantics in 18th century Sweden, Public Opinion Quarterly  [OA](https://scholar.google.co.uk/scholar?q=Das%2C%20Sanjiv%20Chen%2C%20Mike%20Yahoo%21%20for%20Amazon%3A%20Opinion%20extraction%20from%20small%20talk%20on%20the%20web%2C%20Working%20paper%2C%20Santa%20Clara%20University%202001) [GScholar](https://scholar.google.co.uk/scholar?q=Das%2C%20Sanjiv%20Chen%2C%20Mike%20Yahoo%21%20for%20Amazon%3A%20Opinion%20extraction%20from%20small%20talk%20on%20the%20web%2C%20Working%20paper%2C%20Santa%20Clara%20University%202001) 

[^Doyle_et+al_2007_a]: Doyle, Jeffrey, Weili Ge, and Sarah McVay, 2007, Accruals quality and internal control over financial reporting, The Accounting Review 82, 1141–1170.  [OA](https://engine.scholarcy.com/oa_version?query=Doyle%2C%20Jeffrey%20Ge%2C%20Weili%20McVay%2C%20Sarah%20Accruals%20quality%20and%20internal%20control%20over%20financial%20reporting%202007&author=Doyle&title=Accruals%20quality%20and%20internal%20control%20over%20financial%20reporting&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Doyle%2C%20Jeffrey%20Ge%2C%20Weili%20McVay%2C%20Sarah%20Accruals%20quality%20and%20internal%20control%20over%20financial%20reporting%202007) [Scite](/scite_tallies?query=author%3ADoyle%2Ctitle%3AAccruals%20quality%20and%20internal%20control%20over%20financial%20reporting%2Cyear%3A2007)

[^Engelberg_et+al_2008_a]: Engelberg, Joseph, 2008, Costly information processing: Evidence from earnings announcements, Working paper, Northwestern University. Fama, Eugene F., and Kenneth R. French, 1993, Common risk factors in the returns of stocks and bonds, Journal of Financial Economics 33, 3–56.  [OA](https://engine.scholarcy.com/oa_version?query=Engelberg%2C%20Joseph%20paper%2C%20Northwestern%20University%20Fama%20F.%2C%20Eugene%20R%2C%20Kenneth%20Costly%20information%20processing%3A%20Evidence%20from%20earnings%20announcements%202008&author=Engelberg&title=Costly%20information%20processing%3A%20Evidence%20from%20earnings%20announcements&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Engelberg%2C%20Joseph%20paper%2C%20Northwestern%20University%20Fama%20F.%2C%20Eugene%20R%2C%20Kenneth%20Costly%20information%20processing%3A%20Evidence%20from%20earnings%20announcements%202008) [Scite](/scite_tallies?query=author%3AEngelberg%2Ctitle%3ACostly%20information%20processing%3A%20Evidence%20from%20earnings%20announcements%2Cyear%3A2008)

[^Fama_1997_a]: Fama, Eugene F., and Kenneth R. French, 1997, Industry costs of equity, Journal of Financial  [OA](https://scholar.google.co.uk/scholar?q=Fama%20Eugene%20F%20and%20Kenneth%20R%20French%201997%20Industry%20costs%20of%20equity%20Journal%20of%20Financial) [GScholar](https://scholar.google.co.uk/scholar?q=Fama%20Eugene%20F%20and%20Kenneth%20R%20French%201997%20Industry%20costs%20of%20equity%20Journal%20of%20Financial) 

[^Fama_2001_b]: Fama, Eugene F., and Kenneth R. French, 2001, Disappearing dividends: Changing firm characteristics or lower propensity to pay? Journal of Financial Economics 60, 3–43.  [OA](https://engine.scholarcy.com/oa_version?query=Fama%20Eugene%20F%20and%20Kenneth%20R%20French%202001%20Disappearing%20dividends%20Changing%20firm%20characteristics%20or%20lower%20propensity%20to%20pay%20Journal%20of%20Financial%20Economics%2060%20343&author=Fama&title=French%2C%202001%2C%20Disappearing%20dividends%3A%20Changing%20firm%20characteristics%20or%20lower%20propensity%20to%20pay%3F&year=2001) [GScholar](https://scholar.google.co.uk/scholar?q=Fama%20Eugene%20F%20and%20Kenneth%20R%20French%202001%20Disappearing%20dividends%20Changing%20firm%20characteristics%20or%20lower%20propensity%20to%20pay%20Journal%20of%20Financial%20Economics%2060%20343) [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3AFrench%2C%202001%2C%20Disappearing%20dividends%3A%20Changing%20firm%20characteristics%20or%20lower%20propensity%20to%20pay%3F%2Cyear%3A2001)

[^Fama_1973_a]: Fama, Eugene F., and James MacBeth, 1973, Risk, return, and equilibrium: Empirical tests, Journal of Political Economy 81, 607–636.  [OA](https://engine.scholarcy.com/oa_version?query=Fama%2C%20Eugene%20F.%20MacBeth%2C%20James%20Risk%2C%20return%2C%20and%20equilibrium%3A%20Empirical%20tests%201973&author=Fama&title=Risk%2C%20return%2C%20and%20equilibrium%3A%20Empirical%20tests&year=1973) [GScholar](https://scholar.google.co.uk/scholar?q=Fama%2C%20Eugene%20F.%20MacBeth%2C%20James%20Risk%2C%20return%2C%20and%20equilibrium%3A%20Empirical%20tests%201973) [Scite](/scite_tallies?query=author%3AFama%2Ctitle%3ARisk%2C%20return%2C%20and%20equilibrium%3A%20Empirical%20tests%2Cyear%3A1973)

[^Feldman_et+al_2003_a]: Feldman, Ronen, Suresh Govindaraj, Joshua Livnat, and Benjamin Segal, 2008, The incremental information content of tone change in management discussion and analysis, Working paper, INSEAD. Griffin, Paul, 2003, Got information? Investor response to Form 10-K and Form 10-Q EDGAR filings, Review of Accounting Studies 8, 433–460.  [OA](https://engine.scholarcy.com/oa_version?query=Feldman%2C%20Ronen%20Govindaraj%2C%20Suresh%20Livnat%2C%20Joshua%20Segal%2C%20Benjamin%20The%20incremental%20information%20content%20of%20tone%20change%20in%20management%20discussion%20and%20analysis%2C%20Working%20paper%2C%20INSEAD%202003&author=Feldman&title=The%20incremental%20information%20content%20of%20tone%20change%20in%20management%20discussion%20and%20analysis%2C%20Working%20paper%2C%20INSEAD&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Feldman%2C%20Ronen%20Govindaraj%2C%20Suresh%20Livnat%2C%20Joshua%20Segal%2C%20Benjamin%20The%20incremental%20information%20content%20of%20tone%20change%20in%20management%20discussion%20and%20analysis%2C%20Working%20paper%2C%20INSEAD%202003) [Scite](/scite_tallies?query=author%3AFeldman%2Ctitle%3AThe%20incremental%20information%20content%20of%20tone%20change%20in%20management%20discussion%20and%20analysis%2C%20Working%20paper%2C%20INSEAD%2Cyear%3A2003)

[^Hanley_2010_a]: Hanley, Kathleen Weiss, and Gerard Hoberg, 2010, The information content of IPO prospectuses, Review of Financial Studies 23, 2821–2864.  [OA](https://engine.scholarcy.com/oa_version?query=Hanley%2C%20Kathleen%20Weiss%20Hoberg%2C%20Gerard%20The%20information%20content%20of%20IPO%20prospectuses%202010&author=Hanley&title=The%20information%20content%20of%20IPO%20prospectuses&year=2010) [GScholar](https://scholar.google.co.uk/scholar?q=Hanley%2C%20Kathleen%20Weiss%20Hoberg%2C%20Gerard%20The%20information%20content%20of%20IPO%20prospectuses%202010) [Scite](/scite_tallies?query=author%3AHanley%2Ctitle%3AThe%20information%20content%20of%20IPO%20prospectuses%2Cyear%3A2010)

[^Henry_2008_a]: Henry, Elaine, 2008, Are investors influenced by the way earnings press releases are written? The Journal of Business Communication 45, 363–407.  [OA](https://engine.scholarcy.com/oa_version?query=Henry%2C%20Elaine%20Are%20investors%20influenced%20by%20the%20way%20earnings%20press%20releases%20are%20written%3F%202008&author=Henry&title=Are%20investors%20influenced%20by%20the%20way%20earnings%20press%20releases%20are%20written%3F&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Henry%2C%20Elaine%20Are%20investors%20influenced%20by%20the%20way%20earnings%20press%20releases%20are%20written%3F%202008) [Scite](/scite_tallies?query=author%3AHenry%2Ctitle%3AAre%20investors%20influenced%20by%20the%20way%20earnings%20press%20releases%20are%20written%3F%2Cyear%3A2008)

[^Jordan_2009_a]: Jordan, R.R., 1999, Academic Writing Course (Longman, London). Jurafsky, Daniel, and James H. Martin, 2009, Speech and Language Processing (Prentice Hall, Upper Saddle River, NJ).  [OA](https://scholar.google.co.uk/scholar?q=Jordan%20RR%201999%20Academic%20Writing%20Course%20Longman%20London%20Jurafsky%20Daniel%20and%20James%20H%20Martin%202009%20Speech%20and%20Language%20Processing%20Prentice%20Hall%20Upper%20Saddle%20River%20NJ) [GScholar](https://scholar.google.co.uk/scholar?q=Jordan%20RR%201999%20Academic%20Writing%20Course%20Longman%20London%20Jurafsky%20Daniel%20and%20James%20H%20Martin%202009%20Speech%20and%20Language%20Processing%20Prentice%20Hall%20Upper%20Saddle%20River%20NJ) 

[^Kothari_et+al_2008_a]: Kothari, S.P., Xu Li, and James Short, 2008, The effect of disclosures by management, analysts, and financial press on cost of capital, return volatility, and analyst forecasts: A study using content analysis, Working paper, MIT. Li, Feng, 2008, Annual report readability, current earnings, and earnings persistence, Journal of Accounting and Economics 45, 221–247.  [OA](https://engine.scholarcy.com/oa_version?query=Kothari%2C%20S.P.%20Li%2C%20Xu%20Short%2C%20James%20The%20effect%20of%20disclosures%20by%20management%2C%20analysts%2C%20and%20financial%20press%20on%20cost%20of%20capital%2C%20return%20volatility%2C%20and%20analyst%20forecasts%3A%20A%20study%20using%20content%20analysis%2C%20Working%20paper%2C%20MIT%202008&author=Kothari&title=The%20effect%20of%20disclosures%20by%20management%2C%20analysts%2C%20and%20financial%20press%20on%20cost%20of%20capital%2C%20return%20volatility%2C%20and%20analyst%20forecasts%3A%20A%20study%20using%20content%20analysis%2C%20Working%20paper%2C%20MIT&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Kothari%2C%20S.P.%20Li%2C%20Xu%20Short%2C%20James%20The%20effect%20of%20disclosures%20by%20management%2C%20analysts%2C%20and%20financial%20press%20on%20cost%20of%20capital%2C%20return%20volatility%2C%20and%20analyst%20forecasts%3A%20A%20study%20using%20content%20analysis%2C%20Working%20paper%2C%20MIT%202008) [Scite](/scite_tallies?query=author%3AKothari%2Ctitle%3AThe%20effect%20of%20disclosures%20by%20management%2C%20analysts%2C%20and%20financial%20press%20on%20cost%20of%20capital%2C%20return%20volatility%2C%20and%20analyst%20forecasts%3A%20A%20study%20using%20content%20analysis%2C%20Working%20paper%2C%20MIT%2Cyear%3A2008)

[^Li_2009_a]: Li, Feng, 2009, The determinants and information content of the forward-looking statements in corporate filings—a Naıve Bayesian machine learning approach, Working paper, University of Michigan. Manning, Christopher D., and Hinrich Schutze, 2003, Foundations of Statistical Natural Language Processing (MIT Press, Cambridge, MA). Mayew, William J., and Mohan Venkatachalam, 2009, The power of voice: Managerial affective states and future firm performance, Working paper, Duke University. Newey, Whitney K., and Kenneth D. West, 1987, A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix, Econometrica 55, 703–708. Public Company Accounting Oversight Board (PCAOB), 2004, An audit of internal control over financial reporting performed in conjunction with an audit of financial statements. Auditing Standard No. 2, (Washington, DC.) Roll, Richard, 1988, R2, Journal of Finance 43, 541–566.  [OA](https://scholar.google.co.uk/scholar?q=Li%20Feng%202009%20The%20determinants%20and%20information%20content%20of%20the%20forwardlooking%20statements%20in%20corporate%20filingsa%20Na%C4%B1ve%20Bayesian%20machine%20learning%20approach%20Working%20paper%20University%20of%20Michigan%20Manning%20Christopher%20D%20and%20Hinrich%20Schutze%202003%20Foundations%20of%20Statistical%20Natural%20Language%20Processing%20MIT%20Press%20Cambridge%20MA%20Mayew%20William%20J%20and%20Mohan%20Venkatachalam%202009%20The%20power%20of%20voice%20Managerial%20affective%20states%20and%20future%20firm%20performance%20Working%20paper%20Duke%20University%20Newey%20Whitney%20K%20and%20Kenneth%20D%20West%201987%20A%20simple%20positive%20semidefinite%20heteroskedasticity%20and%20autocorrelation%20consistent%20covariance%20matrix%20Econometrica%2055%20703708%20Public%20Company%20Accounting%20Oversight%20Board%20PCAOB%202004%20An%20audit%20of%20internal%20control%20over%20financial%20reporting%20performed%20in%20conjunction%20with%20an%20audit%20of%20financial%20statements%20Auditing%20Standard%20No%202%20Washington%20DC%20Roll%20Richard%201988%20R2%20Journal%20of%20Finance%2043%20541566) [GScholar](https://scholar.google.co.uk/scholar?q=Li%20Feng%202009%20The%20determinants%20and%20information%20content%20of%20the%20forwardlooking%20statements%20in%20corporate%20filingsa%20Na%C4%B1ve%20Bayesian%20machine%20learning%20approach%20Working%20paper%20University%20of%20Michigan%20Manning%20Christopher%20D%20and%20Hinrich%20Schutze%202003%20Foundations%20of%20Statistical%20Natural%20Language%20Processing%20MIT%20Press%20Cambridge%20MA%20Mayew%20William%20J%20and%20Mohan%20Venkatachalam%202009%20The%20power%20of%20voice%20Managerial%20affective%20states%20and%20future%20firm%20performance%20Working%20paper%20Duke%20University%20Newey%20Whitney%20K%20and%20Kenneth%20D%20West%201987%20A%20simple%20positive%20semidefinite%20heteroskedasticity%20and%20autocorrelation%20consistent%20covariance%20matrix%20Econometrica%2055%20703708%20Public%20Company%20Accounting%20Oversight%20Board%20PCAOB%202004%20An%20audit%20of%20internal%20control%20over%20financial%20reporting%20performed%20in%20conjunction%20with%20an%20audit%20of%20financial%20statements%20Auditing%20Standard%20No%202%20Washington%20DC%20Roll%20Richard%201988%20R2%20Journal%20of%20Finance%2043%20541566) 

[^Singhal_2009_a]: Singhal, Amit, 2009, Modern information retrieval: A brief overview, Working paper, Google, Inc.  [OA](https://scholar.google.co.uk/scholar?q=Singhal%2C%20Amit%20Modern%20information%20retrieval%3A%20A%20brief%20overview%2C%20Working%20paper%2C%20Google%202009) [GScholar](https://scholar.google.co.uk/scholar?q=Singhal%2C%20Amit%20Modern%20information%20retrieval%3A%20A%20brief%20overview%2C%20Working%20paper%2C%20Google%202009) 

[^Stone_et+al_1966_a]: Stone, Philip J., Dexter C. Dunphy, Marshall S. Smith, and Daniel M. Ogilvie, 1966, The General Inquirer: A Computer Approach to Content Analysis (MIT Press, Cambridge, MA).  [OA](https://scholar.google.co.uk/scholar?q=Stone%20Philip%20J%20Dexter%20C%20Dunphy%20Marshall%20S%20Smith%20and%20Daniel%20M%20Ogilvie%201966%20The%20General%20Inquirer%20A%20Computer%20Approach%20to%20Content%20Analysis%20MIT%20Press%20Cambridge%20MA) [GScholar](https://scholar.google.co.uk/scholar?q=Stone%20Philip%20J%20Dexter%20C%20Dunphy%20Marshall%20S%20Smith%20and%20Daniel%20M%20Ogilvie%201966%20The%20General%20Inquirer%20A%20Computer%20Approach%20to%20Content%20Analysis%20MIT%20Press%20Cambridge%20MA) 

[^Tetlock_2007_a]: Tetlock, Paul C., 2007, Giving content to investor sentiment: The role of media in the stock market, Journal of Finance 62, 1139–1168.  [OA](https://engine.scholarcy.com/oa_version?query=Tetlock%2C%20Paul%20C.%20Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%202007&author=Tetlock&title=Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market&year=2007) [GScholar](https://scholar.google.co.uk/scholar?q=Tetlock%2C%20Paul%20C.%20Giving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%202007) [Scite](/scite_tallies?query=author%3ATetlock%2Ctitle%3AGiving%20content%20to%20investor%20sentiment%3A%20The%20role%20of%20media%20in%20the%20stock%20market%2Cyear%3A2007)

[^Tetlock_et+al_2008_a]: Tetlock, Paul C., M. Saar-Tsechansky, and S. Macskassy, 2008, More than words: Quantifying language to measure firms’ fundamentals, Journal of Finance 63, 1437–1467.  [OA](https://engine.scholarcy.com/oa_version?query=Tetlock%2C%20Paul%20C.%20Saar-Tsechansky%2C%20M.%20Macskassy%2C%20S.%20More%20than%20words%3A%20Quantifying%20language%20to%20measure%20firms%E2%80%99%20fundamentals%202008&author=Tetlock&title=More%20than%20words%3A%20Quantifying%20language%20to%20measure%20firms%E2%80%99%20fundamentals&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Tetlock%2C%20Paul%20C.%20Saar-Tsechansky%2C%20M.%20Macskassy%2C%20S.%20More%20than%20words%3A%20Quantifying%20language%20to%20measure%20firms%E2%80%99%20fundamentals%202008) [Scite](/scite_tallies?query=author%3ATetlock%2Ctitle%3AMore%20than%20words%3A%20Quantifying%20language%20to%20measure%20firms%E2%80%99%20fundamentals%2Cyear%3A2008)

[^Tomz_et+al_2003_a]: Tomz, Michael, Gary King, and Langche Zeng, 2003, ReLogit: Rare events logistic regression, Journal of Statistical Software 8, 1–27.  [OA](https://engine.scholarcy.com/oa_version?query=Tomz%2C%20Michael%20King%2C%20Gary%20Zeng%2C%20Langche%20ReLogit%3A%20Rare%20events%20logistic%20regression%202003&author=Tomz&title=ReLogit%3A%20Rare%20events%20logistic%20regression&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Tomz%2C%20Michael%20King%2C%20Gary%20Zeng%2C%20Langche%20ReLogit%3A%20Rare%20events%20logistic%20regression%202003) [Scite](/scite_tallies?query=author%3ATomz%2Ctitle%3AReLogit%3A%20Rare%20events%20logistic%20regression%2Cyear%3A2003)

