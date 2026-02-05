# Documentation Index

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

Welcome to the comprehensive documentation for the Sentiment Regime Detector project.

---

## 📚 Documentation Structure

### Core Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| **[API.md](API.md)** | Complete API reference with endpoints, authentication, examples | Frontend developers, API consumers |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design, components, data flow, ML pipeline | Architects, senior developers |
| **[DATA_PIPELINE.md](DATA_PIPELINE.md)** | Detailed pipeline stages, processing flow, optimization | Data engineers, ML engineers |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Setup, workflow, debugging, testing | All developers |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Docker, HPC, production deployment | DevOps, system administrators |

### Reference Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| **[DATASETS.md](DATASETS.md)** | Dataset catalog and import guide (links to `/data/`) | Data scientists, researchers |
| **[SCRIPTS.md](SCRIPTS.md)** | Utility scripts reference (links to `/scripts/`) | Developers, operators |

---

## 🚀 Quick Start Guides

### I'm a Developer...

**Getting Started:**
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Setup and workflow
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) - System overview
3. Check [API.md](API.md) - API endpoints

**Common Tasks:**
- Setting up local environment → [DEVELOPMENT.md#quick-start](DEVELOPMENT.md#quick-start)
- Running tests → [TESTING.md](../TESTING.md)
- Making database changes → [DEVELOPMENT.md#database-management](DEVELOPMENT.md#database-management)

---

### I'm a Data Scientist...

**Getting Started:**
1. Review [DATASETS.md](DATASETS.md) - Available datasets
2. Read [DATA_PIPELINE.md](DATA_PIPELINE.md) - Processing workflow
3. Check [SCRIPTS.md](SCRIPTS.md) - Analysis scripts

**Common Tasks:**
- Importing new datasets → [DATASETS.md#import-scripts](DATASETS.md#import-scripts)
- Running backtests → [SCRIPTS.md#backtesting](SCRIPTS.md#backtesting)
- Analyzing results → [SCRIPTS.md#analysis](SCRIPTS.md#analysis)

---

### I'm a DevOps Engineer...

**Getting Started:**
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) - All deployment methods
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) - System components
3. Check [API.md](API.md#error-handling) - Health checks

**Common Tasks:**
- Docker deployment → [DEPLOYMENT.md#docker-production](DEPLOYMENT.md#docker-production)
- HPC setup → [DEPLOYMENT.md#hpc-deployment-maneframe-iii](DEPLOYMENT.md#hpc-deployment-maneframe-iii)
- Monitoring → [DEPLOYMENT.md#health-checks--monitoring](DEPLOYMENT.md#health-checks--monitoring)

---

### I'm a Researcher...

**Getting Started:**
1. Review [ARCHITECTURE.md](ARCHITECTURE.md#ml-pipeline) - ML methodology
2. Check [DATASETS.md](DATASETS.md) - Data sources and coverage
3. Read [DATA_PIPELINE.md](DATA_PIPELINE.md) - Feature engineering

**Common Tasks:**
- Understanding the model → [ARCHITECTURE.md#ml-pipeline](ARCHITECTURE.md#ml-pipeline)
- Reproducing results → [SCRIPTS.md#backtesting](SCRIPTS.md#backtesting)
- Accessing data → [DATASETS.md](DATASETS.md)

---

## 📖 Documentation by Topic

### Architecture & Design

- **System Overview:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Data Flow:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **ML Pipeline:** [ARCHITECTURE.md#ml-pipeline](ARCHITECTURE.md#ml-pipeline)
- **Database Schema:** [ARCHITECTURE.md#database-schema](ARCHITECTURE.md#database-schema)

### Development

- **Setup Guide:** [DEVELOPMENT.md#quick-start](DEVELOPMENT.md#quick-start)
- **Testing:** [../TESTING.md](../TESTING.md)
- **Code Style:** [DEVELOPMENT.md#code-style](DEVELOPMENT.md#code-style)
- **Debugging:** [DEVELOPMENT.md#debugging](DEVELOPMENT.md#debugging)

### Data & Processing

- **Dataset Catalog:** [DATASETS.md](DATASETS.md) → [/data/kaggle/README.md](../data/kaggle/README.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **Import Scripts:** [SCRIPTS.md#data-import](SCRIPTS.md#data-import)
- **Processing Scripts:** [SCRIPTS.md#processing](SCRIPTS.md#processing)

### API & Integration

- **API Reference:** [API.md](API.md)
- **Authentication:** [API.md#authentication](API.md#authentication)
- **Endpoints:** [API.md#endpoints](API.md#endpoints)
- **Error Handling:** [API.md#error-handling](API.md#error-handling)

### Deployment & Operations

- **Docker Setup:** [DEPLOYMENT.md#docker-development](DEPLOYMENT.md#docker-development)
- **Production Deploy:** [DEPLOYMENT.md#docker-production](DEPLOYMENT.md#docker-production)
- **HPC Processing:** [DEPLOYMENT.md#hpc-deployment-maneframe-iii](DEPLOYMENT.md#hpc-deployment-maneframe-iii)
- **Monitoring:** [DEPLOYMENT.md#health-checks--monitoring](DEPLOYMENT.md#health-checks--monitoring)

---

## 🔍 Finding Information

### By Task

| I want to... | See Document | Section |
|-------------|--------------|---------|
| Set up my development environment | [DEVELOPMENT.md](DEVELOPMENT.md) | Quick Start |
| Understand how the system works | [ARCHITECTURE.md](ARCHITECTURE.md) | Overview |
| Call the API | [API.md](API.md) | Endpoints |
| Import new data | [DATASETS.md](DATASETS.md) | Import Scripts |
| Run a backtest | [SCRIPTS.md](SCRIPTS.md) | Backtesting |
| Deploy to production | [DEPLOYMENT.md](DEPLOYMENT.md) | Docker Production |
| Process data on HPC | [DEPLOYMENT.md](DEPLOYMENT.md) | HPC Deployment |
| Debug an issue | [DEVELOPMENT.md](DEVELOPMENT.md) | Debugging |
| Run tests | [../TESTING.md](../TESTING.md) | Running Tests |
| Add a dependency | [DEVELOPMENT.md](DEVELOPMENT.md) | Dependency Management |

### By Component

| Component | Documentation |
|-----------|--------------|
| **FastAPI Backend** | [API.md](API.md), [DEVELOPMENT.md](DEVELOPMENT.md) |
| **React Frontend** | [DEVELOPMENT.md#frontend](DEVELOPMENT.md#running-services) |
| **PostgreSQL** | [ARCHITECTURE.md#database-schema](ARCHITECTURE.md#database-schema) |
| **Redis Cache** | [ARCHITECTURE.md](ARCHITECTURE.md#api-serving-phase) |
| **FinBERT Model** | [ARCHITECTURE.md#ml-pipeline](ARCHITECTURE.md#ml-pipeline) |
| **GARCH-MIDAS** | [DATA_PIPELINE.md#garch-midas-volatility-forecasting](DATA_PIPELINE.md#garch-midas-volatility-forecasting) |
| **HPC Processing** | [DEPLOYMENT.md#hpc-deployment](DEPLOYMENT.md#hpc-deployment-maneframe-iii) |
| **Data Pipeline** | [DATA_PIPELINE.md](DATA_PIPELINE.md) |

---

## 📂 Additional Resources

### In This Repository

- **Project README:** [../README.md](../README.md) - Project overview and results
- **Testing Guide:** [../TESTING.md](../TESTING.md) - Comprehensive testing documentation
- **Scripts Reference:** [../scripts/README.md](../scripts/README.md) - Detailed script catalog
- **Data Directory:** [../data/README.md](../data/README.md) - Data organization
- **Kaggle Datasets:** [../data/kaggle/README.md](../data/kaggle/README.md) - Dataset details
- **Docker Guide:** [../DOCKER_GUIDE.md](../DOCKER_GUIDE.md) - Docker quick reference (deprecated - see [DEPLOYMENT.md](DEPLOYMENT.md))
- **Dependency Migration:** [../DEPENDENCY_MIGRATION.md](../DEPENDENCY_MIGRATION.md) - pyproject.toml migration guide

### External Links

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **PostgreSQL Docs:** https://www.postgresql.org/docs/
- **Hugging Face Transformers:** https://huggingface.co/docs/transformers/
- **FinBERT Model:** https://huggingface.co/ProsusAI/finbert
- **SMU ManeFrame III:** https://www.smu.edu/OIT/Services/HPC

---

## 🆘 Getting Help

### Documentation Issues

If you find errors or gaps in documentation:
1. Check if there's a more recent version
2. Create an issue describing the problem
3. Suggest improvements or corrections

### Technical Questions

- **General:** Review relevant documentation first
- **Setup Issues:** Check [DEVELOPMENT.md#troubleshooting](DEVELOPMENT.md#troubleshooting)
- **API Questions:** See [API.md](API.md) examples
- **Data Pipeline:** Check [DATA_PIPELINE.md](DATA_PIPELINE.md) error handling

### Contact

**Jonathan Rocha**
- Email: <jrocha@smu.edu>
- Project: SMU MSDS Capstone, Spring 2026

---

## 📝 Documentation Standards

### Writing Guidelines

When contributing to documentation:

1. **Clarity First** - Write for your audience
2. **Examples** - Include code examples and commands
3. **Links** - Cross-reference related documentation
4. **Currency** - Keep "Last Updated" dates current
5. **Structure** - Use consistent heading hierarchy
6. **Code Blocks** - Use syntax highlighting
7. **Tables** - For structured comparisons
8. **Diagrams** - Mermaid for flowcharts

### File Organization

```
docs/
├── README.md              # This file (index)
├── API.md                 # API reference (35+ endpoints)
├── ARCHITECTURE.md        # System design (comprehensive)
├── DATA_PIPELINE.md       # Pipeline stages (detailed)
├── DEVELOPMENT.md         # Dev setup & workflow
├── DEPLOYMENT.md          # All deployment methods
├── DATASETS.md            # Dataset index (links to /data/)
└── SCRIPTS.md             # Scripts index (links to /scripts/)
```

---

## 🗓️ Recent Updates

### February 3, 2026

- ✅ Created comprehensive `/docs/` directory
- ✅ Added 7 core documentation files
- ✅ Documented all 21 Kaggle datasets
- ✅ Cataloged 89 utility scripts
- ✅ Consolidated test strategy
- ✅ Fixed .gitignore issues
- ✅ Created cross-references between docs

### Next Steps

- [ ] Add architecture diagrams (Mermaid)
- [ ] Document CI/CD pipeline
- [ ] Add performance benchmarks
- [ ] Create video tutorials
- [ ] Add troubleshooting guide
- [ ] Document cloud deployment

---

## 📊 Documentation Coverage

| Component | Status | Documentation |
|-----------|--------|---------------|
| **API** | ✅ Complete | [API.md](API.md) |
| **Architecture** | ✅ Complete | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **Data Pipeline** | ✅ Complete | [DATA_PIPELINE.md](DATA_PIPELINE.md) |
| **Development** | ✅ Complete | [DEVELOPMENT.md](DEVELOPMENT.md) |
| **Deployment** | ✅ Complete | [DEPLOYMENT.md](DEPLOYMENT.md) |
| **Testing** | ✅ Complete | [../TESTING.md](../TESTING.md) |
| **Datasets** | ✅ Complete | [DATASETS.md](DATASETS.md) |
| **Scripts** | ✅ Complete | [SCRIPTS.md](SCRIPTS.md) |
| **CI/CD** | ⏳ Coming Soon | TBD |
| **Troubleshooting** | ⏳ Coming Soon | TBD |

---

**Welcome aboard! Happy building! 🚀**
