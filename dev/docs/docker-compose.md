# Docker Compose Configuration

## docker-compose.yml

```yaml
version: '3.8'

services:
  # Backend API
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/capstone
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=production
    env_file:
      - .env
    depends_on:
      - db
      - redis
    volumes:
      - ./models:/app/models  # Mount models directory
      - ./data:/app/data      # Mount data directory
    restart: unless-stopped
    networks:
      - capstone-network

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=capstone
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - capstone-network

  # Redis for caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - capstone-network

  # React Frontend (optional - for full-stack deployment)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - capstone-network

volumes:
  postgres_data:
  redis_data:

networks:
  capstone-network:
    driver: bridge
```

## docker-compose.dev.yml (development)

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
      - "8888:8888"  # Jupyter notebook
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/capstone_dev
      - ENVIRONMENT=development
    env_file:
      - .env.dev
    depends_on:
      - db
      - redis
    volumes:
      - .:/app  # Mount entire project for hot-reload
      - /app/__pycache__  # Exclude pycache
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - capstone-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=capstone_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
    ports:
      - "5433:5432"  # Different port to avoid conflicts
    networks:
      - capstone-network

  redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
    networks:
      - capstone-network

  # Jupyter notebook service
  jupyter:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8888:8888"
    volumes:
      - .:/app
    command: jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''
    networks:
      - capstone-network

volumes:
  postgres_dev_data:

networks:
  capstone-network:
    driver: bridge
```

## 5. .dockerignore

**`.dockerignore`**:

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints
*.ipynb

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Environment
.env
.env.dev
.env.local

# Data files (large datasets should not be in image)
data/*.csv
data/*.json
data/*.parquet
models/*.pt
models/*.pth
models/*.h5

# Logs
*.log
logs/

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Documentation
README.md
docs/
*.md

# Node (if you have frontend in same repo)
node_modules/
npm-debug.log
```
