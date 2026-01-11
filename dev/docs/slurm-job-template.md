# SLURM Job Script Template

```bash
#!/bin/bash
#SBATCH --job-name=sentiment_train
#SBATCH --output=logs/sentiment_%j.out
#SBATCH --error=logs/sentiment_%j.err
#SBATCH --time=24:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32G

module load python/3.9 cuda/11.8
source activate sentiment

python train_sentiment_model.py --model finbert --epochs 5 --batch_size 32
```

## GitHub Repository Structure

```text
sentiment-regime-detector/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── data/                       # Data collection scripts
│   ├── reddit_scraper.py
│   ├── twitter_scraper.py
│   ├── news_scraper.py
│   └── data_pipeline.py       # Orchestrator
│
├── preprocessing/              # Data cleaning
│   ├── text_cleaner.py
│   ├── asset_labeler.py
│   └── eda.ipynb              # Exploratory analysis
│
├── models/                     # ML models
│   ├── sentiment/
│   │   ├── train_finbert.py
│   │   ├── train_roberta.py
│   │   └── ensemble.py
│   ├── regime/
│   │   ├── train_rf.py
│   │   ├── train_xgboost.py
│   │   └── train_lstm.py
│   └── utils.py
│
├── evaluation/                 # Model evaluation
│   ├── sentiment_eval.py
│   ├── regime_eval.py
│   └── backtesting.py
│
├── api/                        # Backend API
│   ├── app.py                 # FastAPI app
│   ├── routes/
│   │   ├── sentiment.py
│   │   ├── regime.py
│   │   └── alerts.py
│   └── database.py            # PostgreSQL connection
│
├── frontend/                   # React dashboard
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SentimentGauge.jsx
│   │   │   ├── RegimeIndicator.jsx
│   │   │   ├── DivergenceAlerts.jsx
│   │   │   └── HistoricalChart.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_sentiment_experiments.ipynb
│   └── 03_regime_modeling.ipynb
│
├── paper/                      # Capstone paper
│   ├── draft_0.pdf
│   ├── draft_1.pdf
│   ├── draft_2.pdf
│   ├── figures/
│   └── references.bib
│
├── docs/                       # Documentation
│   ├── api_spec.md
│   ├── model_card.md
│   └── deployment_guide.md
│
└── tests/                      # Unit tests
    ├── test_data_pipeline.py
    ├── test_sentiment_model.py
    └── test_api.py
```
