[[Fottner_et+al_RedditFinancialImagePostSentiment_2022]]

# [Reddit financial image post sentiment dataset](https://doi.org/10.1016/j.dib.2022.108759)

## [[Alexander Fottner]]; [[Yarema Okhrin]]; [[Jonathan Pfahler]] et al.

## Abstract
The dataset presented in this paper consists of sentiment information extracted from images and text in financial subreddit posts. Members of these subreddits post about their trading behavior, express their opinions, and discuss capital market trends. Their posts contain sentiment information about financial topics and signal information about trading decisions. Frequently, members post screenshots of their portfolios from their mobile broker apps. We collected the posts, processed them to extract sentiment scores using various methods, and anonymized them. The dataset, therefore, consists not of content from the posts or information about the author, but of processed sentiment information within the posts. Further financial tickers mentioned in the posts are tracked, such that the effect of sentiment in the posts can be attributed to financial products and used in the context of financial forecasting. The posts were collected using the Reddit [2] and Pushshift [3] APIs and processed within an Amazon Web Services architecture. A fine-tuned MobileNet [4] was used to classify images into four categories identified in a preliminary analysis. The categories included classical memes, number posts (e.g., screenshots of mobile broker portfolios), text posts (e.g.

## Key concepts
#sentiment_analysis; #social_media

## Quote
> The study analyzed sentiment in social media posts from Reddit using a custom feature extraction pipeline and a Mobile Nets artificial neural network to classify images into four categories, resulting in a dataset of sentiment variables from image and textual information.

## Key points
- The dataset presented consists of sentiment information extracted from image and text data of financial subreddit posts
- A fine-tuned MobileNets artificial neural network [^4] was used to classify images into four distinct categories, which had been determined in a preliminary analysis
- The data [^1] is available on a 20-minute basis and can be used in many areas, such as financial forecasting and analyzing sentiment dynamics in social media posts
- The data provides quantitative sentiment extracted from text and images on finance-related social media posts on Reddit
- As the data set consists of sentiment extracted from financial subreddit posts, it allows for analyses in the context of behavioral finance with respect to the members of such forums
- The data [^1] consists of sentiment information extracted from social media posts of financial subreddits


## Summary

### Data
The dataset consists of sentiment information extracted from image and text data of financial subreddit posts, collected using the Reddit and Pushshift APIs and processed using an Amazon Web Services architecture.
The data is available in three CSV files: meta_time_series.csv, features.csv, and comments.csv, which contain time series information, static sentiment features, and sentiment information from comments, respectively.
The data is anonymized by hashing the user ID for each post and can be used for financial forecasting, sentiment analysis, and behavioral finance research.

### Methods
The dataset was created using a custom-built feature engineering pipeline that includes a fine-tuned MobileNet-based artificial neural network to classify images into four distinct categories.
OCR methods were used to extract text from images, and custom methods were applied to extract sentiment and other information from the resulting text.
The data was collected at 20-minute intervals and can be aggregated to 20-minute, hourly, or daily intervals for time-series analyses.

### Applications
The dataset can be used in various areas, such as financial forecasting, sentiment analysis, and behavioral finance research.
The data can be used to analyze how changes in sentiment affect stocks, and the extensive time-series information enables research into the dynamics that drive the popularity of memes and other social media posts.
The data can also serve as additional data for conventional datasets in stock price prediction, and educators can use the variety of features to demonstrate models and methods in the fields of Machine Learning and Data Mining.

### Data Collection
The data was collected using the Reddit and Pushshift APIs and processed with a custom feature-extraction pipeline on Amazon Web Services servers.
The data includes meta-information derived directly from each post via an API call, such as the average number of long sentiment in all comments of a post, the number of comments of a post with positive sentiment, and the sum of scores of all comments of a post.

### Sentiment Analysis
The text in comments is evaluated using the VADER sentiment classification model to determine negative, positive, and absolute sentiment.
Additional custom weights are introduced to assess sentiment based on group-specific keywords used by communities in the considered subreddits.
The resulting score is weighted by the number of comments of the associated post.
A MobileNet-based artificial neural network was trained to classify images in posts into four categories.

### Data Characteristics
The time series in the data are relatively short, with posts tracked for as long as they remain relevant and never longer than 24 hours.
Some variables include outliers that are not filtered out, leaving it to the individual researcher to decide how to address this issue.
The data is fully anonymized, and Reddit's data redistribution policies were complied with.

## Data analysis
- #method/time_series_analyses

##  Builds on previous research
- Subsequently, they were processed using a custom feature extraction pipeline running on Amazon Web Services servers. A Mobile Nets artificial neural network [^4] was trained to classify images in posts into four categories, since the images were so inherently different in their content structure that different methods for sentiment extraction were needed.

## Limitations
- The limitations of this study are that the dataset has different start dates for each file and that the data was anonymized by hashing the user ID for each post, which may limit the ability to identify the author of the post.
- The limitations of the study include the short time series sequences contained in the data and the presence of outliers in some of the variables. The study also notes that the methods used cannot filter out scenarios in which a post author might exaggerate or post unrealistically high numbers as a joke.

## Future work
- The future work of this study includes investigating the relationship between sentiment contained in social media posts on Reddit and movements on the financial markets, and analyzing the dynamics and changes in sentiment over time and across posts.
- The future work includes further analysis of the dataset of sentiment variables, and potentially using the dataset to predict stock prices or other financial outcomes. The study also notes that the dataset is fully anonymized and can be used by other researchers.


## References
[^1]: Jonathan Pfahler, Alexander Fottner, Julian Wustl, Yarema Okhrin, “Reddit financial image post sentiment dataset”, Mendeley Data (2022) V3, doi:10.17632/b6ns6d8xv3.3.  [OA](https://doi.org/10.17632/b6ns6d8xv3.3)  [Scite](/scite_tallies?query=https://doi.org/10.17632/b6ns6d8xv3.3)

[^2]: reddit inc. reddit api documentation. https://www.reddit.com/dev/api/, 2021a.  [OA](https://www.reddit.com/dev/api/)  

[^3]: Baumgartner J. M., pushshift api, https://github.com/pushshift/api, 2021.  [OA](https://github.com/pushshift/api)  

[^4]: Howard A. G., Zhu M., Chen B., Kalenichenko D., Wang W., Weyand T., Andreetto M., Adam H.. Mobilenets, Efficient convolutional neural net- works for mobile vision applications, CoRR, abs/1704.04861, 2017, URL http://arxiv.org/abs/1704.04861.  [OA](http://arxiv.org/abs/1704.04861)  

[^5]: Hoffstaetter S., Bochi J., Lee M., Kistner L., Mitchell R., Cecchini E., Hagen J., Morawiec D., Bedada E., and Akyüz U., Python tesseract„ v0.3.8, June 04, 2021., https://github.com/madmaze/pytesseract.  [OA](https://github.com/madmaze/pytesseract)  

[^6]: C. Hutto, E. Gilbert, Vader, A parsimonious rule-based model for sentiment analysis of social media text, in: Proceedings of the International AAAI Conference on Web and Social Media, 8, May 2014, pp. 216–225. https://ojs.aaai.org/index.php/ICWSM/article/view/14550.   [OA](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)  

