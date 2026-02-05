# Project Conventions & Standards

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

---

## 📋 Purpose

This document establishes consistent naming conventions and coding standards for the project to improve readability, maintainability, and collaboration.

---

## 📁 File & Directory Naming

### Directories

**Standard:** `snake_case` (lowercase with underscores)

✅ **Good Examples:**
```
scripts/data_collection/
scripts/data_import/
src/sentiment_detector/
data/hpc_batches/
tests/test_api/
```

❌ **Avoid:**
```
scripts/DataCollection/       # PascalCase
scripts/data-collection/      # kebab-case
data/HPC-Batches/            # Mixed case
```

**Rationale:**
- Python import system prefers underscores
- Consistent with Python package naming (PEP 8)
- Easier to type (no shift key for underscores)

---

### Python Files

**Standard:** `snake_case.py` (lowercase with underscores)

✅ **Good Examples:**
```python
collect_reddit_data.py
import_collected_data.py
run_historical_backtests.py
export_phase1_hpc.py
```

❌ **Avoid:**
```python
CollectRedditData.py          # PascalCase
collect-reddit-data.py        # kebab-case
collectRedditData.py          # camelCase
```

**Rationale:** PEP 8 standard for module names

---

### Test Files

**Standard:** `test_{module_name}.py`

✅ **Good Examples:**
```python
test_api.py
test_sentiment.py
test_preprocessing.py
test_jump_model.py
```

**Test Directories:** Mirror source structure

```
src/sentiment_detector/api/sentiment.py
tests/test_api/test_sentiment.py

src/sentiment_detector/models/jump_model.py
tests/test_models/test_jump_model.py
```

---

### Configuration Files

**Standard:** Lowercase with appropriate extension

✅ **Good Examples:**
```
pyproject.toml
docker-compose.yml
.env.example
.gitignore
requirements-hpc.txt
```

---

### Documentation Files

**Standard:** `UPPERCASE.md` or `lowercase.md` depending on importance

**Root-level (important):**
```
README.md                    # Project overview
TESTING.md                   # Testing guide
CONVENTIONS.md               # This file
DEPENDENCY_MIGRATION.md      # Migration guide
```

**Docs directory:**
```
docs/API.md                  # Major topics in UPPERCASE
docs/ARCHITECTURE.md
docs/README.md               # Directory index

docs/datasets.md             # Minor topics in lowercase (if needed)
```

---

### Session Logs & Archive

**Standard:** `YYYY-MM-DD_DESCRIPTION.md` or `DESCRIPTION.md` (descriptive)

✅ **Good Examples:**
```
archive/dev-sessions-jan-feb-2026/MORNING_SESSION_FEB2.md
archive/dev-sessions-jan-feb-2026/EVENING_SESSION_JAN31.md
archive/dev-sessions-jan-feb-2026/IMPLEMENTATION_PROGRESS.md
```

❌ **Avoid:**
```
session1.md                  # Non-descriptive
2026-2-3-notes.md           # Inconsistent date format
```

---

## 🐍 Python Code Conventions

### Variables & Functions

**Standard:** `snake_case`

```python
# Variables
sentiment_score = 0.75
max_retry_count = 3
database_url = "postgresql://..."

# Functions
def calculate_sentiment(text: str) -> float:
    pass

def import_reddit_data(source: str) -> None:
    pass
```

---

### Classes

**Standard:** `PascalCase`

```python
class SentimentAnalyzer:
    pass

class RegimeClassifier:
    pass

class DatabaseConnection:
    pass
```

---

### Constants

**Standard:** `UPPER_SNAKE_CASE`

```python
MAX_BATCH_SIZE = 50000
DEFAULT_TIMEOUT = 30
API_VERSION = "v1"
REDIS_TTL = 60

# Also for environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

### Private/Internal

**Standard:** Single leading underscore `_name`

```python
class SentimentModel:
    def __init__(self):
        self._model = None          # Private instance variable
        self._cache = {}

    def _preprocess_text(self, text):  # Private method
        pass
```

---

### Module-level "Constants"

**Standard:** Module with UPPER_SNAKE_CASE

```python
# config.py
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
MODEL_CACHE_DIR = Path.home() / ".cache" / "models"

# Use elsewhere
from config import DATABASE_URL
```

---

## 📦 Import Organization

**Standard:** PEP 8 order with separators

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Optional

# 2. Third-party imports
import numpy as np
import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine

# 3. Local application imports
from sentiment_detector.core.database import get_session
from sentiment_detector.models.sentiment import SentimentModel
```

**Tool:** Use `ruff` for automatic sorting

```bash
ruff check --select I --fix src/
```

---

## 💬 Docstrings & Comments

### Docstring Style: Google Format

```python
def calculate_volatility(prices: pd.Series, window: int = 30) -> pd.Series:
    """Calculate rolling volatility using standard deviation.

    Args:
        prices: Time series of asset prices
        window: Rolling window size in days (default: 30)

    Returns:
        Time series of volatility values

    Raises:
        ValueError: If window is less than 2

    Example:
        >>> prices = pd.Series([100, 101, 102, 101, 100])
        >>> volatility = calculate_volatility(prices, window=3)
    """
    if window < 2:
        raise ValueError("Window must be at least 2")
    return prices.rolling(window).std()
```

### Comments

**When to comment:**
- **Why** not what (code shows what)
- Complex algorithms
- Non-obvious business logic
- Workarounds for bugs
- TODOs with context

```python
# Good: Explains WHY
# Use exponential smoothing to reduce noise in sentiment signal
smoothed = sentiment.ewm(span=7).mean()

# Bad: States the obvious
# Calculate the mean
average = sum(values) / len(values)

# Good: Provides context
# HACK: Twitter API returns null for deleted tweets, treating as neutral
if tweet is None:
    sentiment = 0.0
```

---

## 🗄️ Database Naming

### Tables

**Standard:** Plural `snake_case`

```sql
texts
sentiment_scores
market_data
regimes
alert_subscriptions
```

### Columns

**Standard:** Singular `snake_case`

```sql
CREATE TABLE sentiment_scores (
    id BIGSERIAL PRIMARY KEY,
    text_id BIGINT,
    sentiment_score FLOAT,
    confidence FLOAT,
    created_at TIMESTAMP
);
```

### Indexes

**Standard:** `idx_{table}_{column(s)}`

```sql
CREATE INDEX idx_texts_collected ON texts(collected_at);
CREATE INDEX idx_sentiment_text_id ON sentiment_scores(text_id);
CREATE INDEX idx_market_date ON market_data(date);
```

---

## 🔧 Git Conventions

### Branch Names

**Standard:** `{type}/{short-description}`

✅ **Good Examples:**
```
feature/add-regime-alerts
bugfix/fix-sentiment-overflow
hotfix/redis-connection-timeout
refactor/consolidate-tests
docs/add-api-documentation
```

**Types:**
- `feature/` - New functionality
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `refactor/` - Code restructuring
- `docs/` - Documentation only
- `test/` - Test additions/fixes

❌ **Avoid:**
```
feature                      # No description
Feature/AddRegimeAlerts     # Capital letters
add-regime-alerts           # No type prefix
```

---

### Commit Messages

**Standard:** Conventional Commits format

```
{type}({scope}): {subject}

{body}

{footer}
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting (no code change)
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance

✅ **Good Examples:**
```
feat(api): Add regime transition alerts endpoint

- Implement POST /api/v1/alerts/subscribe
- Add alert configuration validation
- Create alert history tracking

Closes #123

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

```
fix(sentiment): Handle null text in preprocessing

Prevents NoneType error when processing deleted tweets

Fixes #456
```

```
docs: Add comprehensive API documentation

- Create docs/API.md with all endpoints
- Add authentication examples
- Include error handling guide
```

❌ **Avoid:**
```
fixed bug                    # Vague
WIP                         # Too brief
Updated files               # No context
```

---

## 📊 Data File Naming

### Raw Data

**Standard:** `{source}_{description}_{date}.{ext}`

```
reddit_finance_2024-01-15.json
multi_source_2024-02-03.json
vix_data_2024.csv
```

### Processed Data

**Standard:** `{type}_{description}.{ext}`

```
sentiment_scores_phase1.json
vix_regimes_extended.json
garch_midas_forecasts.csv
backtest_results_2008_crisis.csv
```

### HPC Batches

**Standard:** `batch_{NNNN}.json` (zero-padded)

```
batch_0000.json
batch_0001.json
...
batch_0029.json
```

---

## 🎨 Code Formatting

### Line Length

**Standard:** 100 characters (Python), 80 for docstrings

```python
# OK
very_long_function_name(parameter1, parameter2, parameter3)

# Better (if > 100 chars)
very_long_function_name(
    parameter1,
    parameter2,
    parameter3
)
```

### Spacing

```python
# Operators: space around binary operators
x = 1 + 2
result = x * y

# Function calls: no space before parentheses
function(arg1, arg2)

# Commas: space after, not before
my_list = [1, 2, 3]
```

### Blank Lines

```python
# 2 blank lines between top-level definitions
class MyClass:
    pass


def my_function():
    pass


# 1 blank line between methods
class MyClass:
    def method1(self):
        pass

    def method2(self):
        pass
```

---

## 🛠️ Tool Configuration

### Ruff Configuration

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # isort
    "N",  # pep8-naming
    "W",  # pycodestyle warnings
]

ignore = [
    "E501",  # line too long (formatter handles this)
]
```

### Black Configuration (Alternative)

```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
```

---

## ✅ Enforcement

### Pre-commit Checks

**Recommended:** Set up pre-commit hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI/CD Checks

All pull requests should pass:
- ✅ Ruff formatting check
- ✅ Type checking (mypy)
- ✅ Test suite
- ✅ Coverage threshold (>70%)

---

## 📚 Exceptions

### When to Deviate

**External/Third-party:**
- Kaggle datasets may have inconsistent naming (keep as-is for traceability)
- Third-party libraries dictate their naming
- Legacy code may need gradual migration

**Domain-specific:**
- Well-known acronyms: `VIX`, `CISS`, `SPY` (don't force lowercase)
- Financial terms: `risk_on`, `risk_off` (established terminology)

---

## 🔄 Migration Plan

### Current Inconsistencies

**Data directories:** Some use kebab-case
- `wsb-2022/` → Keep (matches Kaggle source name)
- `wsb-echo-chamber/` → Keep (matches Kaggle source name)
- `financial-news/` → Keep (external source)

**Rationale:** Data directories from external sources preserve original naming for traceability. New directories should use `snake_case`.

### Future Work

- [ ] Document frontend naming conventions (React/TypeScript)
- [ ] Add SQL query style guide
- [ ] Define API endpoint naming patterns
- [ ] Document environment variable conventions

---

## 📞 Questions?

If unsure about a naming decision:
1. Check this document first
2. Look at similar existing code
3. Prefer consistency over perfection
4. When in doubt, ask: **Jonathan Rocha** (<jrocha@smu.edu>)

---

**Remember:** Consistency is more important than the specific convention chosen.
