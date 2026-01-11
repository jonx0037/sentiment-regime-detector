# Git Workflow Best Practices

```bash
# Create branches for major features
git checkout -b feature/sentiment-model
git checkout -b feature/regime-classifier
git checkout -b feature/dashboard

# Commit frequently with descriptive messages
git commit -m "feat: Add FinBERT fine-tuning script"
git commit -m "fix: Handle missing timestamps in Reddit data"
git commit -m "docs: Add API endpoint documentation"

# Use .gitignore for sensitive data
echo "data/raw/" >> .gitignore
echo "models/*.pth" >> .gitignore
echo "config/api_keys.json" >> .gitignore
```

---

## Finding 10+ Peer-Reviewed Sources

I already have 15 sources in the "Draft 0 outline," but here is a  **strategic search plan** for finding more:

### **Search Strategy:**

**1. Google Scholar Queries:**

```text
"financial sentiment analysis" "machine learning" "market regime"
"cross-asset" "sentiment" "NLP"
"social media sentiment" "stock market" "prediction"
"transformer models" "financial text"
"Reddit" OR "Twitter" "stock price" "sentiment"
"regime switching" "volatility" "sentiment indicator"
"FinBERT" OR "RoBERTa" "financial NLP"
```

**2. Key Journals/Conferences:**

- *Journal of Finance*, *Journal of Financial Economics*
- *Quantitative Finance*, *Journal of Banking & Finance*
- ACL, EMNLP, NAACL (NLP conferences with FinNLP tracks)
- ICAIF (ACM International Conference on AI in Finance)
- KDD, AAAI (Data mining conferences)

**3. Snowball Method:**

- Start with the 15 sources I listed in Draft 0
- Check "Cited by" on Google Scholar for each paper
- Review reference lists of most relevant papers

**4. Specific Author Searches:**

- Tim Loughran (Financial sentiment lexicons)
- Johan Bollen (Twitter sentiment + stock market)
- Raphael Flauger (NLP for finance)
- Doyne Farmer (Market microstructure + agent-based models)

### **Source Organization:**

I recommend using **Zotero** or **Mendeley** for reference management:

```text
Project: Sentiment Regime Detector
└── Collections:
    ├── Financial Sentiment Analysis (8 papers)
    ├── Market Regime Detection (6 papers)
    ├── Social Media & Markets (7 papers)
    ├── Transformer Models (5 papers)
    └── Cross-Asset Analysis (4 papers)
    
