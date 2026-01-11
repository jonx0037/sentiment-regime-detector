# Usage Commands

## Development Setup

```bash
# Build and start development environment
docker-compose -f docker-compose.dev.yml up --build

# Run specific service
docker-compose -f docker-compose.dev.yml up api

# Execute commands in running container
docker-compose -f docker-compose.dev.yml exec api bash

# Run tests
docker-compose -f docker-compose.dev.yml exec api pytest

# Access Jupyter notebook
docker-compose -f docker-compose.dev.yml up jupyter
# Navigate to http://localhost:8888
```

## Production Deployment

```bash
# Build production image
docker-compose up --build -d

# View logs
docker-compose logs -f api

# Scale API service
docker-compose up -d --scale api=3

# Stop all services
docker-compose down

# Remove volumes (careful - deletes data)
docker-compose down -v
```
