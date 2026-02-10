# Dataset Research 2/1/2026

> **Note:** API keys have been moved to `.env` file for security. See `.env.example` for reference.

## Updated Bitcoin Twitter Sentiment

```text
ckandemir/bitcoin_tweets_sentiment_kaggle

from datasets import load_dataset

ds = load_dataset("ckandemir/bitcoin_tweets_sentiment_kaggle")

or

import pandas as pd

splits = {'train': 'data/train-00000-of-00001-cc8461398e266567.parquet', 'test': 'data/test-00000-of-00001-922aa10406034550.parquet', 'eval': 'data/eval-00000-of-00001-dc793d916ae447cb.parquet'}
df = pd.read_parquet("hf://datasets/ckandemir/bitcoin_tweets_sentiment_kaggle/" + splits["train"])
```

### Reddit Dataset with Sentiment Analysis

(already downloaded via zip file) - [financial_news_market_events_dataset_2025.zip](media/17699675158608/financial_news_market_events_dataset_2025.zip)


    ```text
    # Install dependencies as needed:
    # pip install kagglehub[pandas-datasets]
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    
    # Set the path to the file you'd like to load
    file_path = ""
    
    # Load the latest version
    df = kagglehub.load_dataset(
      KaggleDatasetAdapter.PANDAS,
      "vijayj0shi/reddit-dataset-with-sentiment-analysis",
      file_path,
      # Provide any additional arguments like 
      # sql_query or pandas_kwargs. See the 
      # documenation for more information:
      # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
    )
    
    print("First 5 records:", df.head())
    ```


### The "Echo Chamber" Effect:

(downloaded via zip file) - [wallstreetbets_reddit_data_-_10:2020_-_04:2022.zip](media/17699675158608/wallstreetbets_reddit_data_-_10:2020_-_04:2022.zip)


```text
dataset posted on 2023-02-04, 11:11 authored by Longo
Data used in the article "The Echo Chamber Effect Resounds on Financial Markets: A Social Media Alert System for Meme Stocks" by Ilaria Gianstefani, Luigi Longo, and Massimo Riccaboni.

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4053771

To cite the paper:

@article{gianstefani2022echo,
 title={The echo chamber effect resounds on financial markets: A social media alert system for meme stocks},
 author={Gianstefani, Ilaria and Longo, Luigi and Riccaboni, Massimo},
 journal={arXiv preprint arXiv:2203.13790},
 year={2022}
}

Gianstefani, Ilaria and Longo, Luigi and Riccaboni, Massimo, The Echo Chamber Effect Resounds on Financial Markets: A Social Media Alert System for Meme Stocks (March 9, 2022). Available at SSRN: https://ssrn.com/abstract=4053771 or http://dx.doi.org/10.2139/ssrn.4053771

The folder common_stats contains raw data for submissions and comments related to keywords.

The folder reddit_raw contains statistics computed with the methodology used in the paper.
```


### Financial News Market Events Dataset for NLP 2025

(downloaded via zip file) - [financial_news_market_events_dataset_2025.zip](media/17699675158608/financial_news_market_events_dataset_2025.zip)

I think this is the CSV file associated with this dataset. If it is not, it is associated with another dataset in this document.
```
[financial_news_events.csv](media/17699675158608/financial_news_events.csv)
```

```text
import kagglehub

# Download latest version
path = kagglehub.dataset_download("pratyushpuri/financial-news-market-events-dataset-2025")

print("Path to dataset files:", path)
```

### Reddit financial image post sentiment dataset

(downloaded via zip file) - [financial_news_market_events_dataset_for_NLP_2025.zip](media/17699675158608/reddit_financial_image_post_sentiment_dataset.zip)

```
Pfahler, Jonathan; Fottner, Alexander; wustl, julian; Okhrin, Yarema (2022), “Reddit financial image post sentiment dataset”, Mendeley Data, V3, doi: 10.17632/b6ns6d8xv3.3

or 

Fottner A, Okhrin Y, Pfahler J, Wustl J. Reddit financial image post sentiment dataset. Data Brief. 2022 Nov 17;45:108759. doi: 10.1016/j.dib.2022.108759. PMID: 36533290; PMCID: PMC9747619.
```

### 2022 Sentiment Analysis of Reddit Posts and BTC

```text
import kagglehub

# Download latest version
path = kagglehub.dataset_download("leukipp/reddit-crypto-data")

print("Path to dataset files:", path)
```

```
[2022-sentiment-analysis-of-reddit-posts-and-btc.ipynb](media/17699675158608/2022-sentiment-analysis-of-reddit-posts-and-btc.ipynb)
```

### COVID-19 - World Major Indices Historical Data

```
import kagglehub

# Download latest version
path = kagglehub.dataset_download("alvarob96/covid19-world-major-indices-historical-data")

print("Path to dataset files:", path)
```

(downloaded via zip file)

```text
[COVID-19_-_World_Major_Indices_Historical_Data.zip](media/17699675158608/COVID-19_-_World_Major_Indices_Historical_Data.zip)
```

### Sentiment Analysis of Commodity News (Gold)

```text
import kagglehub

# Download latest version
path = kagglehub.dataset_download("ankurzing/sentiment-analysis-in-commodity-market-gold")

print("Path to dataset files:", path)
```

(downloaded via zip file)
```text
[sentiment_analysis_of_commodity_news-gold-.zip](media/17699675158608/sentiment_analysis_of_commodity_news-gold-.zip)
```

### FNSPID: A Comprehensive Financial News Dataset in Time Series

https://arxiv.org/html/2402.06698v1/github.com/Zdong104/FNSPID

### FinMultiTime: A Four-Modal Bilingual Dataset for Financial Time-Series Analysis

```text
https://huggingface.co/datasets/Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting; 
Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting
```

```text
@article{xu2025finmultitime,
  title={FinMultiTime: A Four-Modal Bilingual Dataset for Financial Time-Series Analysis},
  author={Xu, Wenyan and Xiang, Dawei and Liu, Yue and Wang, Xiyu and Ma, Yanxiang and Zhang, Liang and Xu, Chang and Zhang, Jiaheng},
  journal={arXiv preprint arXiv:2506.05019},
  year={2025}
}
```

### NOSIBLE/financial-sentiment-v1.1-base

```text
https://huggingface.co/NOSIBLE/financial-sentiment-v1.1-base; 

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-generation", model="NOSIBLE/financial-sentiment-v1.1-base")
messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe(messages)

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("NOSIBLE/financial-sentiment-v1.1-base")
model = AutoModelForCausalLM.from_pretrained("NOSIBLE/financial-sentiment-v1.1-base")
messages = [
    {"role": "user", "content": "Who are you?"},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=40)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
```

## CyrptoMarket_Regime_Classifier

```text
https://github.com/akash-kumar5/CryptoMarket_Regime_Classifier

gh repo clone akash-kumar5/CryptoMarket_Regime_Classifier
```

## NEW CISS - Composite Indicator of Systemic Stress., Euro area, Daily

```text
https://data.ecb.europa.eu/data/datasets/CISS/CISS.D.U2.Z0Z.4F.EC.SS_CIN.IDX
```
(downloaded csv file)
```text
[ECB Data Portal_20260201200956.csv](media/17699675158608/ECB%20Data%20Portal_20260201200956.csv)
```

## Other sources that might help

- https://en.macromicro.me/charts/55592/north-america-geopolitical-risk-index
