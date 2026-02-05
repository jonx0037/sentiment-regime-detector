# Quick Reference - Sentiment Regime Detector

## 🚀 Start Everything

```bash
cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
./scripts/start_dev.sh
```

## 🌐 Access Points

- **Dashboard**: <http://localhost:3000>
- **API**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>

## 🔧 Individual Commands

### Database

```bash
# Start containers
docker-compose -f docker-compose.dev.yml up -d

# Stop containers
docker-compose -f docker-compose.dev.yml down

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Seed data
python scripts/seed_data.py

# Analyze texts
python scripts/analyze_texts.py
```

### Backend

```bash
# Start server
source .venv/bin/activate
PYTHONPATH=src uvicorn sentiment_detector.main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Check health
curl http://localhost:8000/api/v1/health
```

### Frontend

```bash
# Start dev server
cd frontend && npm run dev

# Build for production
npm run build

# Install new package
npm install <package-name>
```

## 📊 Current Data

### Sentiment Scores

- COMMODITY: -0.381 (BEARISH)
- CRYPTO: -0.188 (BEARISH)
- EQUITY: +0.049 (NEUTRAL)
- FOREX: +0.017 (NEUTRAL)

### Market Data

- VIX: 16.15 (Normal)
- SPY: $692.73
- BTC: $88,451

## 🔍 Useful Endpoints

```bash
# Current sentiment
curl http://localhost:8000/api/v1/sentiment/current | jq

# Sentiment history
curl "http://localhost:8000/api/v1/sentiment/history?asset_class=equity&start_date=2026-01-01T00:00:00Z" | jq

# Current regime
curl http://localhost:8000/api/v1/regime/current | jq

# Health check
curl http://localhost:8000/api/v1/health | jq
```

## 📁 Key Files

### Backend

- `src/sentiment_detector/main.py` - FastAPI app
- `src/sentiment_detector/api/routes/sentiment.py` - Sentiment endpoints
- `src/sentiment_detector/services/sentiment_service.py` - Business logic
- `src/sentiment_detector/services/sentiment_engine.py` - DistilBERT

### Frontend

- `frontend/src/app/page.tsx` - Main dashboard
- `frontend/src/services/api.ts` - API client
- `frontend/src/components/` - React components

### Scripts

- `scripts/seed_data.py` - Populate database
- `scripts/analyze_texts.py` - Run sentiment analysis
- `scripts/test_api.py` - Test API directly
- `scripts/test_market_data.py` - Test market data collector

## 🐛 Troubleshooting

### Port already in use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Database connection error

```bash
# Restart containers
docker-compose -f docker-compose.dev.yml restart

# Check container status
docker ps
```

### Frontend build error

```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

## 📚 Next Steps

1. View dashboard at <http://localhost:3000>
2. Install Recharts: `cd frontend && npm install recharts`
3. Add real chart visualizations
4. Request MANEFRAME access
5. Fine-tune models on HPC
