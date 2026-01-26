# Cross-Asset Sentiment Regime Detector

## Automated Market Psychology Analysis Using Transformer-Based NLP

---

## 🎯 Project Overview

The Cross-Asset Sentiment Regime Detector is a capstone research project that combines advanced natural language processing (NLP) with quantitative finance to create an automated system for detecting market sentiment regimes. By analyzing social media discourse (Reddit) and financial news, the system identifies distinct psychological states in markets and generates actionable trading signals.

### Key Innovation

Traditional sentiment analysis treats market psychology as a continuous variable. This project recognizes that markets operate in distinct **regimes** (euphoria, fear, uncertainty, optimism) and uses transformer-based models to classify these states across multiple asset classes simultaneously.

---

## 👨‍🎓 Project Information

- **Author**: Jonathan Rocha
- **Email**: <jrocha@smu.edu>
- **Institution**: Southern Methodist University (SMU)
- **Program**: Master of Science in Data Science (MSDS)
- **Timeline**: Spring 2026 Capstone
- **Faculty Advisor**: *Searching - TBD*

---

## 🔬 Research Objectives

1. **Develop a multi-source sentiment aggregation framework** that combines Reddit discussions and financial news using transformer-based NLP (FinBERT, sentiment-focused BERT variants)

2. **Identify distinct sentiment regimes** through unsupervised clustering (k-means, GMM, HMM) of sentiment features across multiple asset classes

3. **Generate cross-asset trading signals** by detecting regime transitions and correlating sentiment patterns with price movements

4. **Validate economic significance** through backtesting on historical data (2020-2024) with risk-adjusted performance metrics

---

## 🛠️ Technical Architecture

### Data Pipeline

- **Social Media**: Reddit API → r/wallstreetbets, r/stocks, r/investing
- **Financial News**: NewsAPI → Bloomberg, Reuters, Financial Times
- **Market Data**: yfinance → Stocks, Crypto, Bonds, Commodities

### NLP Stack

- **Models**: FinBERT, RoBERTa-financial, custom fine-tuned transformers
- **Framework**: Hugging Face Transformers, PyTorch
- **Processing**: Sentiment scoring, entity recognition, topic modeling

### Regime Detection

- **Clustering**: K-means, Gaussian Mixture Models
- **Time-Series**: Hidden Markov Models for regime transitions
- **Features**: Multi-dimensional sentiment vectors across assets

### Application Layer

- **Frontend**: React + TypeScript (this documentation site will evolve into the live dashboard)
- **Backend**: FastAPI + PostgreSQL
- **Deployment**: Docker, Kubernetes, MANEFRAME HPC for training

---

## 📊 Expected Deliverables

### Academic Outputs

- ✅ Research Outline (Due: January 12, 2026)
- 📝 Draft 0: Expanded Introduction + Bibliography (Due: January 26, 2026)
- 📝 Draft 1: Full Literature Review (Due: February 16, 2026)
- 📝 Draft 2: Methodology + Preliminary Results (Due: March 16, 2026)
- 📝 Final Paper: Complete Research Manuscript (Due: April 20, 2026)

### Technical Outputs

- Data collection pipeline (Reddit + News APIs)
- Sentiment analysis models (fine-tuned transformers)
- Regime detection algorithms (clustering + HMM)
- Backtesting framework with performance metrics
- Interactive web dashboard (React application)
- Comprehensive technical documentation

---

## 📚 Documentation

- [Project Proposal](course_files/paper-drafts/project-proposal.md)
- [Research Outline Draft](course_files/paper-drafts/draft-0.md)
- [Technical Documentation](dev/docs/)
- [GitHub Repository Setup](dev/docs/github-setup.md)
- [MANEFRAME HPC Workflow](dev/docs/maneframe-hpc-workflow.md)

---

## 🎓 Academic Context

This project fulfills the capstone requirement for SMU's Master of Science in Data Science program. It demonstrates proficiency in:

- **Advanced NLP**: Transformer architectures, transfer learning, domain adaptation
- **Machine Learning**: Unsupervised learning, time-series analysis, feature engineering
- **Software Engineering**: API development, containerization, CI/CD pipelines
- **Financial Analytics**: Quantitative trading, risk metrics, backtesting methodologies
- **Research Methods**: Literature review, hypothesis testing, experimental design

---

## 🚀 Current Status

**Phase**: Research & Planning  
**Next Milestone**: Research Outline Submission (January 12, 2026)  
**Progress**:

- ✅ Project proposal completed
- ✅ GitHub repository initialized
- ✅ Initial documentation structure
- ✅ Literature review strategy defined
- 🔄 Research outline finalization (in progress)
- ⏳ Faculty advisor search (ongoing)

---

## 📞 Contact & Collaboration

**Jonathan Rocha**  
📧 <jrocha@smu.edu>  
🔗 [GitHub Repository](https://github.com/jonx0037/sentiment-regime-detector)  
🏫 Southern Methodist University - Lyle School of Engineering

*This project is open to collaboration and feedback from faculty, industry professionals, and fellow researchers interested in the intersection of NLP and quantitative finance.*

---

## 🔗 Quick Links

- [GitHub Repository](https://github.com/jonx0037/sentiment-regime-detector)
- [SMU MSDS Program](https://www.smu.edu/lyle/academics/graduate/data-science)
- [Project Documentation](https://github.com/jonx0037/sentiment-regime-detector/tree/main/dev/docs)
- [Submission Guide](SUBMISSION_GUIDE_JAN_12_TOMORROW.md)

---

*Built with ❤️ for advancing NLP applications in financial markets*  
*© 2026 Jonathan Rocha | SMU MSDS Capstone Project*
