# Deployment Guide

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026

---

## 📋 Table of Contents

- [Overview](#overview)
- [Docker Development](#docker-development)
- [Docker Production](#docker-production)
- [HPC Deployment (ManeFrame III)](#hpc-deployment-maneframe-iii)
- [Cloud Deployment (Future)](#cloud-deployment-future)
- [Environment Configuration](#environment-configuration)
- [Health Checks & Monitoring](#health-checks--monitoring)

---

## 🎯 Overview

The project supports three deployment modes:

1. **Local Development** - Docker Compose with hot reload
2. **Production** - Docker Compose with optimized settings
3. **HPC Processing** - ManeFrame III SLURM jobs for batch sentiment analysis

---

## 🐳 Docker Development

### Infrastructure Only (Recommended)

Run PostgreSQL and Redis in Docker, API locally:

```bash
# Start database and cache
docker-compose up -d

# Run API locally (separate terminal)
pip install -e ".[dev]"
uvicorn sentiment_detector.main:app --reload --port 8000

# Frontend (optional, separate terminal)
cd frontend
npm run dev
```

**Advantages:**
- Fast code reload (no container rebuild)
- Easy debugging with IDE
- Full Python tooling available

**Ports:**
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- API: `localhost:8000` (local)
- Frontend: `localhost:5173` (local)

---

### Full Stack in Docker

Run everything in containers:

```bash
# Start all services
docker-compose --profile api up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down
```

**When to use:**
- Testing deployment setup
- Reproducing production environment
- CI/CD pipeline testing

---

### Common Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs           # All services
docker-compose logs api       # API only
docker-compose logs -f        # Follow mode

# Restart service
docker-compose restart db
docker-compose restart api

# Rebuild after code changes
docker-compose --profile api build api
docker-compose --profile api up -d api

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v

# Access PostgreSQL shell
docker-compose exec db psql -U postgres -d sentiment_db

# Access Redis CLI
docker-compose exec redis redis-cli
```

---

### Service Details

| Service | Port | Purpose | Profile Required |
|---------|------|---------|------------------|
| **db** (PostgreSQL 15) | 5432 | Primary database | None (always runs) |
| **redis** (Redis 7) | 6379 | Cache & sessions | None (always runs) |
| **api** (FastAPI) | 8000 | REST API | `--profile api` |

---

### Hot Reloading

**How it works:**

```yaml
# docker-compose.yml
api:
  volumes:
    - ./src:/app/src:ro  # Read-only mount
  command: uvicorn sentiment_detector.main:app --reload --host 0.0.0.0
```

**Benefits:**
- Code changes auto-detected
- No container rebuilds needed
- Fast iteration cycle

**Limitations:**
- Dependency changes require rebuild
- Some Python modules don't reload well

---

## 🚀 Docker Production

### Production Profile

```bash
# Start production stack
docker-compose --profile prod up -d

# Or use explicit production compose file
docker-compose -f docker-compose.prod.yml up -d
```

### Production Optimizations

**1. Multi-stage Build**

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --user .

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY ./src /app/src
CMD ["uvicorn", "sentiment_detector.main:app", "--host", "0.0.0.0"]
```

**2. Gunicorn + Uvicorn Workers**

```bash
# Production command (in Dockerfile)
CMD ["gunicorn", "sentiment_detector.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-"]
```

**3. Health Checks**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**4. Resource Limits**

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```

---

## 🖥️ HPC Deployment (ManeFrame III)

### Overview

SMU's ManeFrame III cluster processes sentiment analysis batches using GPU acceleration.

**Specifications:**
- **Nodes:** Up to 30 parallel jobs
- **GPU:** NVIDIA A100 (1 per job)
- **Memory:** 32GB per job
- **Storage:** /lustre/scratch (high-performance)

---

### Setup on ManeFrame

#### 1. Initial Setup

```bash
# SSH to ManeFrame
ssh jarocha@m3.smu.edu

# Create project directory
mkdir -p ~/sentiment-detector
cd ~/sentiment-detector

# Load modules
module load cuda/11.8
module load python/3.11

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-hpc.txt
```

#### 2. Package Data for Transfer

**On local machine:**

```bash
# Create HPC package
bash scripts/hpc/package_for_hpc.sh

# Transfer to ManeFrame
scp sentiment-hpc.tar.gz jarocha@m3.smu.edu:~/sentiment-detector/

# Transfer batch data
rsync -avz data/hpc_batches/ jarocha@m3.smu.edu:~/sentiment-detector/data/hpc_batches/
```

**On ManeFrame:**

```bash
# Extract package
cd ~/sentiment-detector
tar -xzf sentiment-hpc.tar.gz

# Verify structure
ls -la
# Should see: src/, data/, scripts/, requirements-hpc.txt
```

---

### Running Sentiment Analysis

#### Submit SLURM Job Array

```bash
# Submit batch processing job
sbatch scripts/hpc/slurm_job_array.sh

# Check job status
squeue -u $USER

# View job output
tail -f slurm-<job_id>_<array_id>.out

# Cancel job if needed
scancel <job_id>
```

**SLURM Job Script:**

```bash
#!/bin/bash
#SBATCH --job-name=sentiment_batch
#SBATCH --array=0-29
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --mem=32GB
#SBATCH --time=04:00:00
#SBATCH --output=slurm-%A_%a.out

# Load modules
module load cuda/11.8
module load python/3.11

# Activate environment
source .venv/bin/activate

# Run processing
python scripts/processing/process_batch.py \
  --batch-id $SLURM_ARRAY_TASK_ID \
  --input data/hpc_batches/batch_$(printf "%04d" $SLURM_ARRAY_TASK_ID).json \
  --output data/processed/results_$(printf "%04d" $SLURM_ARRAY_TASK_ID).json
```

---

### Monitoring HPC Jobs

```bash
# Job status
squeue -u jarocha

# Detailed job info
scontrol show job <job_id>

# Resource usage
sacct -j <job_id> --format=JobID,JobName,State,Elapsed,MaxRSS,MaxVMSize

# Failed jobs
sacct -u jarocha --state=FAILED

# GPU utilization (during job)
nvidia-smi
```

---

### Retrieving Results

**On ManeFrame:**

```bash
# Package results
cd ~/sentiment-detector
tar -czf results-phase1.tar.gz data/processed/

# Check size
ls -lh results-phase1.tar.gz
```

**On local machine:**

```bash
# Download results
scp jarocha@m3.smu.edu:~/sentiment-detector/results-phase1.tar.gz .

# Extract
tar -xzf results-phase1.tar.gz

# Import to PostgreSQL
python scripts/data_import/import_phased_hpc_results.py --phase 1
```

---

### HPC Best Practices

**1. Test Small First:**

```bash
# Test with 1 batch before submitting 30
#SBATCH --array=0-0  # Single job first
```

**2. Monitor GPU Usage:**

```bash
# Check GPU efficiency
nvidia-smi dmon -s u
```

**3. Handle Failures:**

```bash
# Identify failed batches
python scripts/hpc/identify_failed_batches.py

# Resubmit only failed jobs
#SBATCH --array=3,7,15  # Specific failed jobs
```

**4. Storage Management:**

```bash
# Scratch has automatic cleanup (30 days)
# Move important results to $HOME
mv data/processed/*.json $HOME/sentiment-detector/results/
```

---

## ☁️ Cloud Deployment (Future)

### AWS Architecture (Planned)

```
┌─────────────────────────────────────┐
│      Route 53 (DNS)                 │
│      domain.com                     │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Application Load Balancer          │
│  (ALB) - HTTPS/TLS                  │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼───┐
│ ECS    │      │ ECS    │
│ Task 1 │      │ Task 2 │
│ (API)  │      │ (API)  │
└───┬────┘      └────┬───┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │                 │
┌───▼────────┐ ┌──────▼──────┐
│ RDS        │ │ ElastiCache │
│ PostgreSQL │ │ Redis       │
└────────────┘ └─────────────┘
```

**Services:**
- **ECS Fargate:** Serverless container hosting
- **RDS:** Managed PostgreSQL
- **ElastiCache:** Managed Redis
- **S3:** Data storage
- **CloudWatch:** Logging and monitoring

---

## ⚙️ Environment Configuration

### Environment Variables

**Development (.env):**

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/sentiment_db
DATABASE_ECHO=false

# Redis
REDIS_URL=redis://localhost:6379/0

# API
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_KEY=dev_test_key

# Data Collection
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret

# ML Models
MODEL_CACHE_DIR=~/.cache/huggingface
CUDA_VISIBLE_DEVICES=0  # GPU device ID
```

**Production (.env.production):**

```bash
# Database (use managed service)
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db.region.rds.amazonaws.com/sentiment_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis (use managed service)
REDIS_URL=redis://prod-redis.cache.amazonaws.com:6379/0

# API
ENVIRONMENT=production
LOG_LEVEL=INFO
API_KEY=${API_KEY_SECRET}  # From secrets manager

# Security
CORS_ORIGINS=https://app.domain.com,https://api.domain.com
SECRET_KEY=${SECRET_KEY}

# ML Models
MODEL_CACHE_DIR=/app/models
```

**HPC (.env.hpc):**

```bash
# Paths
DATA_DIR=/lustre/scratch/users/jarocha/sentiment-detector/data
MODEL_CACHE=/lustre/work/users/jarocha/.cache

# Processing
BATCH_SIZE=32
MAX_LENGTH=512
DEVICE=cuda
```

---

## 🏥 Health Checks & Monitoring

### Health Check Endpoint

```bash
# Basic health check
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "timestamp": "2026-02-03T12:00:00Z",
  "database": "connected",
  "redis": "connected"
}
```

### Docker Health Checks

**PostgreSQL:**

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 5s
  timeout: 5s
  retries: 5
```

**Redis:**

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 5s
  timeout: 3s
  retries: 5
```

**API:**

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

### Monitoring (Future)

**Metrics to Track:**

| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| API Latency (p95) | CloudWatch | >100ms |
| Error Rate | CloudWatch | >1% |
| Database Connections | CloudWatch | >80% pool |
| Redis Memory | CloudWatch | >4GB |
| CPU Usage | CloudWatch | >70% |
| Disk Space | CloudWatch | >85% |

**Logging:**

- **Structured Logging:** JSON format
- **Log Levels:** DEBUG (dev), INFO (prod)
- **Centralized:** CloudWatch Logs or ELK Stack
- **Retention:** 30 days

---

## 🔒 Security Considerations

### Production Checklist

- [ ] Use HTTPS/TLS for all connections
- [ ] Rotate API keys regularly
- [ ] Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] Enable database encryption at rest
- [ ] Configure firewall rules (security groups)
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Vulnerability scanning (Snyk, Trivy)

---

## 📚 Related Documentation

- **Development Setup:** [DEVELOPMENT.md](DEVELOPMENT.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Data Pipeline:** [DATA_PIPELINE.md](DATA_PIPELINE.md)
- **API Reference:** [API.md](API.md)
- **Docker Compose Reference:** [../DOCKER_GUIDE.md](../DOCKER_GUIDE.md) (deprecated - see this file)

---

**For deployment support, contact:** Jonathan Rocha (<jrocha@smu.edu>)
