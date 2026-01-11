# Workspace Organization Guide

Quick reference for where files should live in the restructured workspace.

---

## 📁 Directory Structure

```plaintext
DS_6210_Capstone/
├── .gitignore                          # Git ignore rules
├── README.md                           # Project overview (you are here!)
│
├── course_files/                       # 📚 SMU-provided materials (READ-ONLY)
│   ├── MSDS Journal Paper Template.pdf
│   ├── ds-6120_syllabus.pdf
│   ├── sample_of_draft_0.pdf
│   └── [other course materials]
│
└── dev/                                # 🛠️ Development workspace
    │
    ├── code/                           # 💻 Source code
    │   ├── todoist_setup.py           # Project management automation
    │   ├── data-pipeline-orchestrator.md  # Data collection pipeline
    │   ├── reddit-data-collection.md  # Reddit scraper
    │   └── [future: sentiment_model.py, regime_classifier.py, etc.]
    │
    ├── config/                         # ⚙️ Configuration files
    │   ├── config-template.md         # API keys template
    │   ├── environment-files.md       # .env file structure
    │   ├── requirements.md            # Python dependencies
    │   └── requirements-hpc.md        # MANEFRAME-specific deps
    │
    ├── data/                           # 📊 Data collection & storage
    │   ├── [scripts for data download]
    │   ├── raw/                       # Raw scraped data (GIT-IGNORED)
    │   └── processed/                 # Cleaned datasets (GIT-IGNORED)
    │
    ├── docs/                           # 📖 Technical documentation
    │   ├── week-1-checklist.md        # Current week tasks
    │   ├── backend-deployment.md      # Deployment configs
    │   ├── ci-cd-pipeline.md          # GitHub Actions workflows
    │   ├── docker-compose.md          # Multi-container setup
    │   ├── dockerfile-dev.md          # Development container
    │   ├── dockerfile-prod.md         # Production container
    │   ├── frontend-dockerfile.md     # React app container
    │   ├── git-workflow.md            # Branch strategy
    │   ├── k8s-deployment.md          # Kubernetes manifests
    │   ├── makefile-commands.md       # Convenience commands
    │   ├── maneframe-hpc-workflow.md  # HPC usage guide
    │   ├── requirements-structure.md  # Dependency organization
    │   ├── slurm-job-template.md      # SLURM batch script
    │   └── usage-commands.md          # CLI reference
    │
    ├── research/                       # 📝 Academic deliverables
    │   ├── draft-0.md                 # Current draft (Week 1)
    │   ├── project-proposal.md        # Original proposal
    │   ├── literature-review-prompts.md  # Search strategies
    │   └── [future: literature-notes.md, draft-1.md, final-paper.md]
    │
    └── results/                        # 📈 Outputs & visualizations
        ├── figures/                   # Charts, plots (GIT-IGNORED)
        ├── logs/                      # Training logs (GIT-IGNORED)
        └── [future: backtesting results, model performance metrics]
```

---

## 🔄 File Movement Summary (Completed)

### From Root → Subdirectories

| Original File | New Location |
| ------------ | ------------ |
| `backend-deployment - yaml.md` | `docs/backend-deployment.md` |
| `CI-CD pipeline - Sentiment Regime Detector - YML.md` | `docs/ci-cd-pipeline.md` |
| `Config File Template.md` | `config/config-template.md` |
| `Docker Compose Configuration.md` | `docs/docker-compose.md` |
| `Dockerfile (Development).md` | `docs/dockerfile-dev.md` |
| `Dockerfile (Production).md` | `docs/dockerfile-prod.md` |
| `Environment Files.md` | `config/environment-files.md` |
| `Frontend Dockerfile.md` | `docs/frontend-dockerfile.md` |
| `Git Workflow Best Practices.md` | `docs/git-workflow.md` |
| `Kubernetes Deployment Manifests.md` | `docs/k8s-deployment.md` |
| `Makefile (Convenience Commands).md` | `docs/makefile-commands.md` |
| `MANEFRAME HPC Workflow.md` | `docs/maneframe-hpc-workflow.md` |
| `Master Data Pipeline Orchestrator.md` | `code/data-pipeline-orchestrator.md` |
| `Project-Proposal.md` | `research/project-proposal.md` |
| `Reddit Data Collection (Pushshift-PRAW).md` | `code/reddit-data-collection.md` |
| `Requirements Files Structure.md` | `docs/requirements-structure.md` |
| `requirements-hpc-txt.md` | `config/requirements-hpc.md` |
| `requirements-txt.md` | `config/requirements.md` |
| `SLURM Job Script Template.md` | `docs/slurm-job-template.md` |
| `Usage Commands.md` | `docs/usage-commands.md` |
| `drafts/Cross-Asset Sentiment Regime Detector...md` | `research/draft-0.md` |

---

## 📝 Naming Conventions

### ✅ Good File Names (Use These)

- `kebab-case-for-multi-word-files.md`
- `short_descriptive_names.py`
- `draft-0.md`, `draft-1.md`, `final-paper.md`
- `config-template.md`, `requirements-hpc.md`

### ❌ Avoid (Legacy Files)

- `File Name With Spaces.md`
- `File (With Parentheses).md`
- `File - with - dashes.md`
- `ReallyLongDescriptiveFileNameThatGoesOnForever.md`

**Rationale:** Kebab-case is CLI-friendly, git-friendly, and cross-platform compatible.

---

## 🚀 Quick Navigation Commands

```bash
# Jump to specific directories
cd ~/Documents/SMU/DS_6210_Capstone/dev/code      # Source code
cd ~/Documents/SMU/DS_6210_Capstone/dev/research  # Papers/drafts
cd ~/Documents/SMU/DS_6210_Capstone/dev/docs      # Documentation

# List files in each category
ls dev/code/       # Python scripts
ls dev/config/     # Configuration templates
ls dev/research/   # Academic papers

# Search for specific file types
find dev/ -name "*.py"     # All Python files
find dev/ -name "*.md"     # All Markdown files
find dev/ -name "*draft*"  # Files with "draft" in name
```

---

## 🎯 When to Use Each Directory

### `code/`

**Use for:** Executable code, scripts, notebooks
**Examples:**

- `data_scraper.py` - Reddit/Twitter collection
- `sentiment_model.py` - FinBERT fine-tuning
- `regime_classifier.py` - ML model training
- `app.py` - FastAPI backend
- `analysis.ipynb` - Jupyter notebooks

### `config/`

**Use for:** Configuration templates, requirements, environment variables

**Examples:**

- `config-template.md` - API keys structure
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `model_config.yaml` - Hyperparameter configs

### `data/`

**Use for:** Data collection scripts and datasets (raw/processed)
**Note:** Large files (.csv, .json, .pkl) are git-ignored
**Examples:**

- `raw/reddit_2020_2024.csv`
- `processed/sentiment_indices.parquet`
- `scripts/download_historical.py`

### `docs/`

**Use for:** Technical documentation, deployment guides, checklists
**Examples:**

- `week-1-checklist.md` - Weekly task list
- `docker-compose.md` - Container setup
- `maneframe-hpc-workflow.md` - HPC usage guide
- `api-documentation.md` - Backend API docs

### `research/`

**Use for:** Academic papers, literature notes, proposals
**Examples:**

- `draft-0.md` - Current working draft
- `literature-notes.md` - Paper summaries
- `project-proposal.md` - Original proposal
- `final-paper.pdf` - Submission-ready version

### `results/`

**Use for:** Model outputs, visualizations, logs
**Note:** Most files here are git-ignored (too large)
**Examples:**

- `figures/sentiment_time_series.png`
- `logs/training_run_20260115.log`
- `backtesting_results.csv`
- `model_performance_metrics.json`

---

## 🔒 What Gets Git-Ignored

From [.gitignore](../../.gitignore):

### Always Ignored

- API keys, secrets, credentials (`config/api_keys.json`, `.env`)
- Large data files (`*.csv`, `*.parquet`, `*.pkl`, `*.h5`)
- Model checkpoints (`*.pt`, `*.pth`, `*.h5`)
- Results/outputs (`results/figures/`, `results/logs/`)
- Python bytecode (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.conda/`)
- IDE configs (`.vscode/`, `.idea/`)
- MacOS files (`.DS_Store`)

### Version Controlled

- Code (`*.py`, `*.js`, `*.jsx`)
- Documentation (`*.md`)
- Configuration templates (`.example` files)
- Requirements files (`requirements.txt`)
- Dockerfiles, Makefiles, YAML configs
- Small sample datasets (<1MB)

---

## 📋 File Cleanup Checklist

If you create a new file, ask:

1. **Is it code?** → Put in `code/`
2. **Is it a config/template?** → Put in `config/`
3. **Is it documentation?** → Put in `docs/`
4. **Is it a paper/draft?** → Put in `research/`
5. **Is it output/results?** → Put in `results/`
6. **Is it data?** → Put in `data/`

If you're unsure, default to `docs/` and reorganize later.

---

## 🛠️ Maintenance Tasks

### Weekly

- [ ] Review `docs/` for outdated checklists
- [ ] Update `README.md` progress log
- [ ] Archive completed drafts (`research/archive/`)

### Before Commits

- [ ] Check no secrets in staged files (`git diff --staged`)
- [ ] Verify large files are git-ignored (`git status`)
- [ ] Update `README.md` if structure changes

### End of Project

- [ ] Clean up unused files
- [ ] Consolidate duplicate docs
- [ ] Create `FINAL_DELIVERABLES/` folder with:
  - `final-paper.pdf`
  - `presentation-slides.pdf`
  - `deployed-app-url.txt`
  - `github-repo-link.txt`

---

## 🆘 Troubleshooting

**Q: I can't find a file I created yesterday.**  
**A:** Check if it's in the old location (root `dev/`) or new subdirectory. Use: `find dev/ -name "*filename*"`

**Q: Git says a file is too large.**  
**A:** Add it to `.gitignore` and use Git LFS or external storage (Google Drive, Dropbox)

**Q: Should I commit my data files?**  
**A:** No, data files are git-ignored. Only commit data collection **scripts**, not the data itself.

**Q: Where do I put Jupyter notebooks?**  
**A:** Exploratory notebooks → `code/` | Analysis for paper → `research/` | Results notebooks → `results/`

---

**Last Updated:** January 10, 2026  
**Maintained By:** Jonathan Rocha
