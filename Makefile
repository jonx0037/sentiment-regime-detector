# =============================================================================
# Sentiment Regime Detector - Makefile
# =============================================================================
# Common commands for development, testing, and deployment

.PHONY: help install dev test lint format run docker-up docker-down clean

# Default target
help:
	@echo "Sentiment Regime Detector - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install production dependencies"
	@echo "  make dev          Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run          Run the API locally (requires DB)"
	@echo "  make docker-up    Start all services with Docker"
	@echo "  make docker-down  Stop all Docker services"
	@echo "  make logs         Tail Docker logs"
	@echo ""
	@echo "Quality:"
	@echo "  make test         Run tests with coverage"
	@echo "  make lint         Run linter (ruff)"
	@echo "  make format       Format code (ruff)"
	@echo "  make typecheck    Run type checker (mypy)"
	@echo ""
	@echo "Database:"
	@echo "  make db-migrate   Run database migrations"
	@echo "  make db-upgrade   Apply pending migrations"
	@echo "  make db-reset     Reset database (WARNING: deletes data)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove build artifacts"

# =============================================================================
# Setup
# =============================================================================

install:
	pip install -e .

dev:
	pip install -e ".[dev,notebook]"
	pre-commit install

# =============================================================================
# Development
# =============================================================================

run:
	uvicorn sentiment_detector.main:app --reload --host 0.0.0.0 --port 8000

docker-up:
	docker compose up -d
	@echo ""
	@echo "Services started:"
	@echo "  API:      http://localhost:8000"
	@echo "  Docs:     http://localhost:8000/docs"
	@echo "  Postgres: localhost:5432"
	@echo "  Redis:    localhost:6379"

docker-down:
	docker compose down

docker-build:
	docker compose build --no-cache

logs:
	docker compose logs -f

# =============================================================================
# Quality
# =============================================================================

test:
	pytest tests/ -v --cov=sentiment_detector --cov-report=term-missing

test-fast:
	pytest tests/ -v -x --ff

lint:
	ruff check src/ tests/

format:
	ruff check --fix src/ tests/
	ruff format src/ tests/

typecheck:
	mypy src/

# =============================================================================
# Database
# =============================================================================

db-migrate:
	alembic revision --autogenerate -m "$(msg)"

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-reset:
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	docker compose down -v
	docker compose up -d db redis
	sleep 3
	alembic upgrade head

# =============================================================================
# Cleanup
# =============================================================================

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# =============================================================================
# Data Collection (Phase 1)
# =============================================================================

collect-reddit:
	python -m sentiment_detector.cli.collect --source reddit

collect-news:
	python -m sentiment_detector.cli.collect --source news

collect-all:
	python -m sentiment_detector.cli.collect --source all
