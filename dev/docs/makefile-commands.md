# Makefile (Convenience Commands)

## Makefile

```makefile
.PHONY: help dev prod clean test

help:
 @echo "Available commands:"
 @echo "  make dev       - Start development environment"
 @echo "  make prod      - Start production environment"
 @echo "  make test      - Run tests"
 @echo "  make clean     - Stop and remove containers"
 @echo "  make shell     - Open shell in API container"
 @echo "  make logs      - View API logs"

dev:
 docker-compose -f docker-compose.dev.yml up --build

prod:
 docker-compose up --build -d

test:
 docker-compose -f docker-compose.dev.yml exec api pytest tests/ -v

clean:
 docker-compose down -v
 docker-compose -f docker-compose.dev.yml down -v

shell:
 docker-compose -f docker-compose.dev.yml exec api bash

logs:
 docker-compose logs -f api

install-dev:
 pip install -r requirements-dev.txt

install-prod:
 pip install -r requirements-prod.txt
```
