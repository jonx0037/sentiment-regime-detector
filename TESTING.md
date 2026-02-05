# Testing Strategy

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026
**Test Framework:** pytest with asyncio support

---

## 📁 Test Organization

All tests are located in the `/tests/` directory, mirroring the source code structure in `/src/sentiment_detector/`.

### Directory Structure

```text
tests/
├── conftest.py              # Shared fixtures and test configuration
├── data/                    # Test data fixtures
│   └── sample_spark_batch.json
├── test_api/                # API endpoint tests
│   ├── test_alerts.py
│   ├── test_health.py
│   ├── test_regime.py
│   └── test_sentiment.py
├── test_features/           # Feature engineering tests
│   └── test_features.py
├── test_models/             # Model tests
│   ├── test_jump_model.py
│   └── test_sentiment_ensemble.py
├── test_preprocessing/      # Preprocessing tests
│   ├── test_preprocessing.py
│   └── test_time_alignment.py
└── test_validation/         # Validation tests
    └── test_hypothesis_validator.py
```

**Rationale:** This structure follows Python application best practices:
- ✅ Clear separation between source code and tests
- ✅ Easy test discovery with `pytest`
- ✅ Mirrors source structure for intuitive navigation
- ✅ Centralized test configuration in `conftest.py`

---

## 🎯 Test Coverage

### Current Test Suite

| Module | Test File | Coverage Area |
|--------|-----------|---------------|
| **API** | test_api/*.py | FastAPI endpoints (health, sentiment, regime, alerts) |
| **Features** | test_features.py | Granger causality, transfer entropy, connectedness |
| **Models** | test_jump_model.py | Statistical jump model (Shu et al. 2024) |
| **Models** | test_sentiment_ensemble.py | Ensemble sentiment classification |
| **Preprocessing** | test_preprocessing.py | Text cleaning, stop words, asset classification |
| **Preprocessing** | test_time_alignment.py | Temporal alignment utilities |
| **Validation** | test_hypothesis_validator.py | Hypothesis testing framework |

**Total Tests:** 10 test files across 7 modules

---

## 🚀 Running Tests

### Run All Tests

```bash
# Run entire test suite
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=sentiment_detector --cov-report=term-missing

# With coverage HTML report
pytest --cov=sentiment_detector --cov-report=html
```

### Run Specific Test Suites

```bash
# API tests only
pytest tests/test_api/

# Model tests only
pytest tests/test_models/

# Preprocessing tests only
pytest tests/test_preprocessing/

# Single test file
pytest tests/test_models/test_jump_model.py

# Single test function
pytest tests/test_api/test_health.py::test_health_check
```

### Run Tests Matching Pattern

```bash
# All tests with "sentiment" in name
pytest -k sentiment

# All tests with "api" or "health" in name
pytest -k "api or health"

# Exclude slow tests
pytest -m "not slow"
```

---

## ⚙️ Configuration

### pytest Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"           # Auto-detect async tests
testpaths = ["tests"]           # Look for tests in /tests/ only
addopts = "-v --cov=sentiment_detector --cov-report=term-missing"

[tool.coverage.run]
source = ["src/sentiment_detector"]
branch = true                   # Track branch coverage

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

### Async Tests

Tests for async functions automatically work with `asyncio_mode = "auto"`:

```python
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
```

---

## 🧪 Writing New Tests

### File Naming Convention

- **Test files:** `test_<module_name>.py`
- **Test functions:** `test_<function_name>()`
- **Test classes:** `TestClassName` (PascalCase)

### Location Guidelines

Place tests in the directory corresponding to the source module:

| Source Module | Test Location |
|---------------|---------------|
| `src/sentiment_detector/api/` | `tests/test_api/` |
| `src/sentiment_detector/models/` | `tests/test_models/` |
| `src/sentiment_detector/features/` | `tests/test_features/` |
| `src/sentiment_detector/preprocessing/` | `tests/test_preprocessing/` |
| `src/sentiment_detector/core/` | `tests/test_core/` (create if needed) |

### Example Test Structure

```python
"""
Tests for module_name.

Brief description of what this test file covers.
"""

import pytest
from src.sentiment_detector.module_name import function_to_test

def test_basic_functionality():
    """Test basic functionality with valid input."""
    result = function_to_test(valid_input)
    assert result == expected_output

def test_edge_case():
    """Test edge case handling."""
    result = function_to_test(edge_case_input)
    assert result is not None

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result.status == "success"

def test_error_handling():
    """Test that function raises expected error."""
    with pytest.raises(ValueError):
        function_to_test(invalid_input)
```

---

## 🔧 Fixtures

### Shared Fixtures (conftest.py)

Common fixtures are defined in `tests/conftest.py` and available to all tests:

```python
@pytest.fixture
def sample_text():
    """Sample financial text for testing."""
    return "The stock market rose 3% today as earnings exceeded expectations."

@pytest.fixture
def db_session():
    """Database session for testing."""
    # Setup test database
    yield session
    # Teardown
```

### Fixture Scopes

- `function` (default) - Created/destroyed per test function
- `class` - Created/destroyed per test class
- `module` - Created/destroyed per test module
- `session` - Created once for entire test session

---

## 📊 Coverage Goals

### Current Coverage

Run `pytest --cov=sentiment_detector --cov-report=html` to generate detailed coverage report.

### Coverage Targets

| Module Type | Target Coverage |
|-------------|-----------------|
| **API endpoints** | 90%+ |
| **Core business logic** | 85%+ |
| **Models** | 80%+ |
| **Preprocessing** | 75%+ |
| **Utilities** | 70%+ |

### Viewing Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=sentiment_detector --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Open in browser (Linux)
xdg-open htmlcov/index.html
```

---

## 🏷️ Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.slow
def test_expensive_operation():
    """Test that takes >5 seconds."""
    pass

@pytest.mark.integration
def test_database_integration():
    """Test requiring database connection."""
    pass

@pytest.mark.unit
def test_pure_function():
    """Fast unit test with no dependencies."""
    pass
```

Run specific markers:

```bash
# Run only fast tests
pytest -m "not slow"

# Run integration tests
pytest -m integration

# Run unit tests only
pytest -m unit
```

---

## 🐛 Debugging Tests

### Run Tests in Debug Mode

```bash
# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Verbose output with print statements
pytest -v -s
```

### VSCode Integration

Add to `.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.testing.unittestEnabled": false
}
```

---

## 📝 Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- Every push to `main` branch
- Every pull request
- Nightly builds

See `.github/workflows/tests.yml` for CI configuration.

### Pre-commit Hooks

Run tests before committing:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## 🚫 What NOT to Test

Avoid testing:
- Third-party library functionality (assume it works)
- Simple getters/setters with no logic
- Auto-generated code (e.g., ORM models)
- Configuration files

Focus on:
- Business logic
- Data transformations
- Edge cases and error handling
- Integration points
- API contracts

---

## 📚 Testing Resources

### pytest Documentation
- [pytest official docs](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

### Project-Specific Testing Guides
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

---

## 📞 Getting Help

**Questions about testing?**
- Check existing tests in `tests/` for examples
- Consult `conftest.py` for available fixtures
- Review this document for guidelines
- Contact: Jonathan Rocha (<jrocha@smu.edu>)

---

## 📝 Changelog

### February 3, 2026 - Test Consolidation
- **Moved all tests to `/tests/` directory** (from split across `/tests/` and `/src/*/tests/`)
- Created mirrored directory structure matching source code
- Updated documentation with comprehensive testing guide
- All tests now discoverable via `pytest` command

**Migration Details:**
- Moved 5 test files from `/src/sentiment_detector/*/tests/` to `/tests/test_*/`
- Preserved git history using `git mv`
- Added `__init__.py` files to all test directories
- Verified test discovery and import paths

---

*Last updated: February 3, 2026*
