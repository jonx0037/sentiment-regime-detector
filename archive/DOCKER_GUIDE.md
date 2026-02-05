# Docker Compose Quick Reference

## Overview

The project uses a single `docker-compose.yml` with **profiles** to control which services run.

## Common Commands

### Infrastructure Only (Database + Redis)
```bash
# Default mode - runs PostgreSQL and Redis only
# Use this when developing the API locally
docker compose up

# Run in background
docker compose up -d
```

### Full Stack (Infrastructure + API)
```bash
# Run all services including the FastAPI backend
docker compose --profile api up

# Or use the "all" profile (equivalent)
docker compose --profile all up

# Run in background
docker compose --profile api up -d
```

### Management Commands
```bash
# Stop all services
docker compose down

# Stop and remove volumes (deletes database data!)
docker compose down -v

# View logs
docker compose logs
docker compose logs api          # API logs only
docker compose logs -f           # Follow logs

# Restart a specific service
docker compose restart db

# Rebuild the API container after code changes
docker compose --profile api build api
docker compose --profile api up -d api
```

## Service Details

| Service | Port | Purpose | Always Running? |
|---------|------|---------|-----------------|
| **db** | 5432 | PostgreSQL 15 database | ✅ Yes |
| **redis** | 6379 | Redis cache | ✅ Yes |
| **api** | 8000 | FastAPI backend | Only with `--profile api` |

## Configuration

### Environment Variables

The API service loads configuration from `.env` file. See [.env.example](.env.example) for all available options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection (default: `postgresql+asyncpg://postgres:password@db:5432/sentiment_db`)
- `REDIS_URL` - Redis connection (default: `redis://redis:6379/0`)
- `ENVIRONMENT` - Environment mode (default: `development`)
- `LOG_LEVEL` - Logging level (default: `DEBUG`)

### Hot Reloading

When running the API service in Docker, source code is mounted as a read-only volume:
- Changes to `/src` files are automatically detected
- The API server reloads on file changes (via `uvicorn --reload`)
- No need to rebuild the container during development

### Health Checks

Both database and cache include health checks:
- **PostgreSQL**: `pg_isready` every 5s
- **Redis**: `redis-cli ping` every 5s
- API waits for both to be healthy before starting

## Networking

All services run on the `sentiment-network` bridge network:
- Services can communicate using service names (`db`, `redis`, `api`)
- Ports are exposed to localhost for external access

## Development Workflows

### Workflow 1: Local API Development (Recommended)
```bash
# 1. Start infrastructure only
docker compose up -d

# 2. Run API locally with hot reload
pip install -e .[dev]
uvicorn sentiment_detector.main:app --reload

# 3. Access:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### Workflow 2: Full Dockerized Stack
```bash
# 1. Start everything
docker compose --profile api up -d

# 2. Access:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs

# 3. View logs
docker compose logs -f api
```

### Workflow 3: Frontend Development
```bash
# 1. Start infrastructure + API
docker compose --profile api up -d

# 2. Run frontend separately
cd frontend
npm install
npm run dev

# 3. Access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8000  # API

# Kill the process or change the port in docker-compose.yml
```

### Database Connection Refused
```bash
# Check database is running and healthy
docker compose ps

# View database logs
docker compose logs db

# Restart database
docker compose restart db
```

### API Can't Connect to Database
```bash
# Verify the DATABASE_URL in .env
# Ensure it uses the service name "db" not "localhost"
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/sentiment_db

# Restart API
docker compose --profile api restart api
```

### Clear All Data and Start Fresh
```bash
# Stop everything and remove volumes
docker compose down -v

# Remove any orphaned containers
docker compose down --remove-orphans

# Start fresh
docker compose up -d
```

## Production Deployment

For production deployments:

1. **Create `docker-compose.prod.yml`** with:
   - Non-root users
   - Production-grade PostgreSQL config
   - Redis with persistence enabled
   - Proper secrets management (not `.env` files)
   - Resource limits
   - Health monitoring

2. **Use environment-specific builds**:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Consider Kubernetes** for production orchestration

## Migration from Old Setup

**Before (February 2026):**
```bash
docker-compose up              # Full stack
docker-compose -f docker-compose.dev.yml up  # Infrastructure only
```

**After (Current):**
```bash
docker compose up              # Infrastructure only (default)
docker compose --profile api up  # Full stack
```

**What Changed:**
- Consolidated two files into one
- Uses profiles instead of multiple compose files
- Added restart policies
- Added comprehensive documentation in compose file

---

For issues or questions, see [README.md](README.md) or contact jrocha@smu.edu
