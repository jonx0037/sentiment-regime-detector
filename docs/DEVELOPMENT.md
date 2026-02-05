# Development Guide

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

---

## 🚀 Quick Start

### Prerequisites

- **Python:** 3.11-3.13
- **Docker:** 24+ with Compose
- **Git:** For version control
- **PostgreSQL:** 15+ (via Docker)
- **Redis:** 7+ (via Docker)

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd DS_6210_Capstone

# 2. Create virtual environment (recommended: uv)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
uv pip install -e ".[dev]"

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Start services
docker-compose --profile dev up -d

# 6. Run database migrations
alembic upgrade head

# 7. Verify installation
python scripts/validation/test_api.py
```

---

## 📁 Project Structure

```
DS_6210_Capstone/
├── src/sentiment_detector/   # Core Python package
│   ├── api/                   # FastAPI endpoints
│   ├── collectors/            # Data collection
│   ├── core/                  # Database, config
│   ├── features/              # Feature engineering
│   ├── models/                # ML models
│   ├── pipeline/              # Processing pipeline
│   ├── preprocessing/         # Text cleaning
│   ├── services/              # Business logic
│   └── validation/            # Data validation
├── frontend/                  # React dashboard
├── tests/                     # Test suite
├── scripts/                   # Utility scripts
├── data/                      # Data storage
├── docs/                      # Documentation
├── pyproject.toml            # Dependencies & config
├── docker-compose.yml        # Service orchestration
└── .env.example              # Environment template
```

---

## 🛠️ Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

```bash
# Edit code
vim src/sentiment_detector/...

# Run tests frequently
pytest tests/

# Check code formatting
ruff check src/
```

### 3. Test Locally

```bash
# Start development services
docker-compose --profile dev up

# Access services:
# - API: http://localhost:8000
# - Frontend: http://localhost:5173
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### 4. Commit Changes

```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "feat: Add feature description

- Bullet point 1
- Bullet point 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to remote
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- Open PR on GitHub
- Fill in PR template
- Request review
- Address feedback
- Merge when approved

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=sentiment_detector --cov-report=html

# Specific test file
pytest tests/test_api/test_health.py

# Tests matching pattern
pytest -k "sentiment"

# View coverage report
open htmlcov/index.html
```

### Writing Tests

See [TESTING.md](../TESTING.md) for comprehensive testing guide.

**Quick example:**

```python
# tests/test_api/test_your_endpoint.py
import pytest
from httpx import AsyncClient

async def test_your_endpoint(client):
    """Test your endpoint description."""
    response = await client.get("/api/v1/your-endpoint")
    assert response.status_code == 200
    assert "expected_key" in response.json()
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/sentiment_db

# Redis
REDIS_URL=redis://localhost:6379/0

# API Keys (data collection)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
TWITTER_API_KEY=your_twitter_api_key

# ML Models
MODEL_CACHE_DIR=~/.cache/huggingface
```

### pyproject.toml

**Dependency Groups:**

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "httpx>=0.25.0",
]

hpc = [
    "pyspark>=3.5.0",
    # ... HPC-specific dependencies
]
```

**Install groups:**

```bash
# Development dependencies
uv pip install -e ".[dev]"

# HPC dependencies
uv pip install -e ".[hpc]"

# All dependencies
uv pip install -e ".[dev,hpc]"
```

---

## 📊 Database Management

### Migrations with Alembic

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Review generated migration
vim alembic/versions/<timestamp>_add_new_table.py

# Apply migration
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Database Access

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d sentiment_db

# Run SQL queries
\dt  # List tables
\d texts  # Describe texts table
SELECT COUNT(*) FROM texts;

# Backup database
docker-compose exec postgres pg_dump -U postgres sentiment_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres sentiment_db < backup.sql
```

---

## 🎨 Code Style

### Formatting with Ruff

```bash
# Check formatting
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

### Style Guidelines

- **Line Length:** 100 characters
- **Imports:** Sorted with `ruff`
- **Type Hints:** Use for function signatures
- **Docstrings:** Google style
- **Naming:**
  - Variables/functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

---

## 🐛 Debugging

### VSCode Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "sentiment_detector.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### Debugging Tips

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Print debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Variable value: {variable}")

# Pytest debugging
pytest --pdb  # Drop into debugger on failure
pytest -s     # Show print statements
```

---

## 📦 Dependency Management

### Adding Dependencies

```bash
# Add new dependency
uv pip install package-name

# Add to pyproject.toml
# Edit [project.dependencies] or [project.optional-dependencies]

# Lock dependencies (recommended)
uv pip freeze > requirements-lock.txt
```

### Upgrading Dependencies

```bash
# Upgrade specific package
uv pip install --upgrade package-name

# Upgrade all packages
uv pip install --upgrade -e ".[dev]"

# Check for outdated packages
pip list --outdated
```

### Dependency Conflicts

See [DEPENDENCY_MIGRATION.md](../DEPENDENCY_MIGRATION.md) for resolving conflicts.

---

## 🚀 Running Services

### Backend (FastAPI)

```bash
# Development (with auto-reload)
uvicorn sentiment_detector.main:app --reload --port 8000

# Production
uvicorn sentiment_detector.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build
npm run preview
```

### Background Workers (future)

```bash
# Start Celery worker
celery -A sentiment_detector.workers worker --loglevel=info

# Start Celery beat (scheduler)
celery -A sentiment_detector.workers beat --loglevel=info
```

---

## 📝 Common Tasks

### Collect Data

```bash
# Collect Reddit data
python scripts/data_collection/collect_reddit_data.py

# Collect multi-source
python scripts/data_collection/collect_multi_source.py --sources reddit,twitter,rss
```

### Process Data

```bash
# Import collected data
python scripts/data_import/import_collected_data.py --input data/raw/latest.json

# Export for HPC
python scripts/hpc/export_phase1_hpc.py

# Import HPC results
python scripts/data_import/import_phased_hpc_results.py --phase 1
```

### Run Backtests

```bash
# Historical backtest
python scripts/backtesting/run_historical_backtests.py --start-date 2020-01-01

# Crisis backtest
python scripts/backtesting/run_2008_crisis_backtest.py

# Generate visualizations
python scripts/visualization/generate_comparative_visualizations.py
```

---

## 🔍 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Reinstall package in editable mode
uv pip install -e .

# Verify PYTHONPATH
echo $PYTHONPATH

# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres

# Verify connection
psql postgresql://postgres:password@localhost:5432/sentiment_db
```

#### Redis Connection Issues

```bash
# Check Redis is running
docker-compose ps redis

# Test Redis connection
redis-cli -h localhost -p 6379 ping

# Check Redis logs
docker-compose logs redis
```

---

## 📚 Additional Resources

- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Documentation:** [API.md](API.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Testing:** [../TESTING.md](../TESTING.md)
- **Scripts:** [../scripts/README.md](../scripts/README.md)

---

## 💬 Getting Help

- **Issues:** Create GitHub issue
- **Questions:** Contact Jonathan Rocha (<jrocha@smu.edu>)
- **Documentation:** Check [docs/](.) directory

---

**Happy coding! 🚀**
