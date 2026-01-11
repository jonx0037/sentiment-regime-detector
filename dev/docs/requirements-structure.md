# Requirements Files Structure

## requirements-base.txt

```txt
# Core Deep Learning & NLP
torch>=2.0.0
transformers>=4.30.0
sentence-transformers>=2.2.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Data Collection & APIs
praw>=7.7.0
tweepy>=4.14.0
newsapi-python>=0.2.7
requests>=2.31.0
beautifulsoup4>=4.12.0

# Financial Data
yfinance>=0.2.0
pandas-datareader>=0.10.0

# Time Series & Statistical Analysis
statsmodels>=0.14.0
scipy>=1.11.0

# Backend API Framework
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Utilities
python-dotenv>=1.0.0
tqdm>=4.65.0
joblib>=1.3.0

# NLP Tools
nltk>=3.8.0
textblob>=0.17.0

# Data Validation
jsonschema>=4.18.0
```

## requirements-dev.txt

```txt
-r requirements-base.txt

# Development & Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Code Quality
black>=23.7.0
flake8>=6.0.0
pylint>=2.17.0
mypy>=1.4.0
isort>=5.12.0

# Jupyter & Analysis
jupyter>=1.0.0
ipykernel>=6.25.0
notebook>=7.0.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0

# Advanced NLP (for experimentation)
spacy>=3.6.0

# Development Tools
pre-commit>=3.3.0
python-language-server>=0.36.2

# Debugging
ipdb>=0.13.13
```

## requirements-prod.txt

```txt
-r requirements-base.txt

# Production Server
gunicorn>=21.2.0

# Monitoring & Logging
python-json-logger>=2.0.7

# Performance
orjson>=3.9.0  # Faster JSON parsing
```
