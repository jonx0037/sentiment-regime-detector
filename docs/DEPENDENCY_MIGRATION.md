# Dependency Management Migration (Feb 2026)

## Changes

As of February 2026, this project has migrated from `requirements.txt` to using **`pyproject.toml` exclusively** for dependency management, following modern Python packaging standards (PEP 518, PEP 621).

## What Changed

### Before
```bash
pip install -r requirements.txt
pip install -r requirements.minimal.txt  # For CPU-only
```

### After
```bash
# Standard installation
pip install -e .

# With development tools
pip install -e .[dev]

# With Jupyter notebooks
pip install -e .[notebook]

# With HPC/distributed processing
pip install -e .[hpc]

# Multiple groups
pip install -e .[dev,notebook,hpc]
```

## Installation Groups

| Group | Purpose | Key Packages |
|-------|---------|--------------|
| `(default)` | Core application | FastAPI, transformers, torch, pandas, NLP tools |
| `[dev]` | Development & testing | pytest, ruff, mypy, pre-commit |
| `[notebook]` | Jupyter analysis | jupyter, matplotlib, seaborn, plotly |
| `[hpc]` | HPC distributed processing | PySpark, wandb, optuna, xgboost |

## For HPC Users

The HPC setup scripts have been updated:
- [scripts/package_for_hpc.sh](scripts/package_for_hpc.sh:24) now uses `pyproject.toml`
- Installation includes: `pip install -e .[hpc]`
- See [src/sentiment_detector/spark/README.md](src/sentiment_detector/spark/README.md:73) for Spark-specific setup

## Migration Timeline

- **Removed**: `requirements.txt`, `requirements.minimal.txt`
- **Active**: `pyproject.toml` (all dependencies consolidated)
- **Tracking**: All new dependencies should be added to `pyproject.toml`

## Rationale

1. **Single source of truth**: One file manages all dependencies
2. **Modern standard**: PEP 621 is the official Python packaging spec
3. **Better organization**: Optional dependency groups for different use cases
4. **Tool integration**: Better support from pip, build tools, and IDEs
5. **Reduced redundancy**: Eliminated duplicate definitions across 3 files

---
*This migration was completed as part of the February 2026 workspace audit and cleanup.*
