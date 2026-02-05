# API Documentation

**Project:** Cross-Asset Sentiment Regime Detector
**Last Updated:** February 3, 2026
**Base URL:** `http://localhost:8000` (development)
**API Version:** v1

---

## 📋 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Sentiment Analysis](#sentiment-analysis)
  - [Regime Detection](#regime-detection)
  - [Alert Management](#alert-management)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## 🎯 Overview

The Sentiment Regime Detector API provides real-time access to:
- **Cross-asset sentiment analysis** (stocks, crypto, forex, commodities)
- **Market regime detection** (Risk-On, Risk-Off, Transition)
- **Systemic stress indicators** (CISS, VIX)
- **Configurable alerts** for regime transitions

**Technology Stack:**
- Framework: FastAPI
- Database: PostgreSQL + Redis
- Authentication: API Key (Bearer token)
- Response Format: JSON

---

## 🔐 Authentication

All endpoints (except `/health`) require authentication via API key.

### Request Header

```http
Authorization: Bearer YOUR_API_KEY
```

### Example

```bash
curl -H "Authorization: Bearer sk_live_..." http://localhost:8000/api/v1/sentiment/current
```

### Getting an API Key

API keys are managed through environment variables during development:

```bash
# .env file
API_KEY=your_secure_api_key_here
```

---

## 🛣️ Endpoints

### Health Check

#### `GET /health`

Check API health and database connectivity.

**Authentication:** Not required

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2026-02-03T12:00:00Z",
  "database": "connected",
  "redis": "connected"
}
```

**Status Codes:**
- `200 OK` - Service healthy
- `503 Service Unavailable` - Database or Redis unavailable

---

## 💭 Sentiment Analysis

### Get Current Sentiment

#### `GET /api/v1/sentiment/current`

Retrieve the latest sentiment scores across all asset classes.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asset_class` | string | No | Filter by asset class: `equities`, `crypto`, `forex`, `commodities`, `all` (default) |
| `sources` | string | No | Filter by source: `reddit`, `twitter`, `news`, `all` (default) |

**Response:**

```json
{
  "timestamp": "2026-02-03T12:00:00Z",
  "overall_sentiment": 0.42,
  "confidence": 0.87,
  "by_asset_class": {
    "equities": {
      "sentiment": 0.45,
      "volume": 15234,
      "sources": ["reddit", "twitter", "news"]
    },
    "crypto": {
      "sentiment": 0.38,
      "volume": 8912,
      "sources": ["reddit", "twitter"]
    },
    "forex": {
      "sentiment": 0.41,
      "volume": 3421,
      "sources": ["news"]
    },
    "commodities": {
      "sentiment": 0.46,
      "volume": 1876,
      "sources": ["news"]
    }
  },
  "top_drivers": [
    {
      "text": "Fed signals rate cuts ahead, market rallies",
      "sentiment": 0.89,
      "asset_class": "equities",
      "source": "news"
    }
  ]
}
```

**Example:**

```bash
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8000/api/v1/sentiment/current?asset_class=crypto"
```

---

### Get Sentiment History

#### `GET /api/v1/sentiment/history`

Retrieve historical sentiment data.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | string | Yes | ISO 8601 date (e.g., `2026-01-01`) |
| `end_date` | string | No | ISO 8601 date (default: today) |
| `asset_class` | string | No | Filter by asset class |
| `granularity` | string | No | `hourly`, `daily` (default), `weekly` |

**Response:**

```json
{
  "start_date": "2026-01-01",
  "end_date": "2026-02-03",
  "granularity": "daily",
  "data": [
    {
      "date": "2026-01-01",
      "sentiment": 0.35,
      "volume": 12543,
      "confidence": 0.82
    },
    {
      "date": "2026-01-02",
      "sentiment": 0.38,
      "volume": 14231,
      "confidence": 0.85
    }
  ]
}
```

---

## 🎯 Regime Detection

### Get Current Regime

#### `GET /api/v1/regime/current`

Retrieve the current market regime classification.

**Authentication:** Required

**Response:**

```json
{
  "timestamp": "2026-02-03T12:00:00Z",
  "regime": "risk_on",
  "confidence": 0.89,
  "vix": 14.23,
  "ciss": 0.042,
  "sentiment_score": 0.45,
  "duration_days": 14,
  "indicators": {
    "vix_regime": "low_volatility",
    "ciss_regime": "calm",
    "sentiment_regime": "positive",
    "garch_volatility_forecast": 0.0156
  },
  "transition_probability": {
    "to_risk_off": 0.12,
    "to_transition": 0.23,
    "stay_risk_on": 0.65
  }
}
```

**Regime Types:**
- `risk_on` - Low volatility, positive sentiment, risk appetite
- `risk_off` - High volatility, negative sentiment, risk aversion
- `transition` - Mixed signals, regime uncertainty

---

### Get Regime History

#### `GET /api/v1/regime/history`

Retrieve historical regime classifications.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | string | Yes | ISO 8601 date |
| `end_date` | string | No | ISO 8601 date (default: today) |
| `include_transitions` | boolean | No | Include transition events (default: false) |

**Response:**

```json
{
  "start_date": "2025-01-01",
  "end_date": "2026-02-03",
  "current_regime": "risk_on",
  "regime_distribution": {
    "risk_on": 234,
    "risk_off": 87,
    "transition": 44
  },
  "history": [
    {
      "date": "2025-01-01",
      "regime": "risk_on",
      "vix": 15.2,
      "ciss": 0.048,
      "duration_days": 23
    }
  ],
  "transitions": [
    {
      "date": "2025-03-15",
      "from": "risk_on",
      "to": "transition",
      "trigger": "vix_spike",
      "vix_change": 8.5
    }
  ]
}
```

---

### Get Regime Transitions

#### `GET /api/v1/regime/transitions`

Get detected regime transitions with triggering events.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max results (default: 50, max: 200) |
| `transition_type` | string | No | Filter: `to_risk_off`, `to_risk_on`, `to_transition` |

**Response:**

```json
{
  "transitions": [
    {
      "date": "2026-01-15",
      "from_regime": "risk_on",
      "to_regime": "risk_off",
      "confidence": 0.94,
      "triggers": [
        {
          "indicator": "vix",
          "change": 12.3,
          "threshold_crossed": true
        },
        {
          "indicator": "sentiment",
          "change": -0.35,
          "threshold_crossed": true
        }
      ],
      "market_impact": {
        "spy_return": -0.0234,
        "gold_return": 0.0156
      }
    }
  ]
}
```

---

### Get CISS History

#### `GET /api/v1/regime/ciss/history`

Retrieve ECB Composite Indicator of Systemic Stress history.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_date` | string | Yes | ISO 8601 date |
| `end_date` | string | No | ISO 8601 date (default: today) |

**Response:**

```json
{
  "start_date": "2020-01-01",
  "end_date": "2026-02-03",
  "data": [
    {
      "date": "2020-03-16",
      "ciss": 0.848,
      "regime": "crisis",
      "event": "COVID-19 Pandemic"
    }
  ],
  "statistics": {
    "mean": 0.125,
    "max": 0.848,
    "crisis_days": 45
  }
}
```

---

### Get VIX-CISS Divergence

#### `GET /api/v1/regime/divergence`

Detect divergence between VIX and CISS indicators.

**Authentication:** Required

**Response:**

```json
{
  "current_divergence": 0.23,
  "interpretation": "moderate_divergence",
  "vix": {
    "value": 18.5,
    "regime": "moderate_volatility"
  },
  "ciss": {
    "value": 0.085,
    "regime": "elevated_stress"
  },
  "signal": "vix_leads_ciss",
  "explanation": "VIX indicates market volatility while CISS shows systemic stress building"
}
```

---

## 🔔 Alert Management

### Subscribe to Alerts

#### `POST /api/v1/alerts/subscribe`

Create a new alert configuration.

**Authentication:** Required

**Request Body:**

```json
{
  "alert_type": "regime_transition",
  "conditions": {
    "from_regime": "risk_on",
    "to_regime": "risk_off",
    "min_confidence": 0.8
  },
  "delivery": {
    "method": "webhook",
    "endpoint": "https://your-app.com/webhooks/regime-change"
  },
  "enabled": true
}
```

**Alert Types:**
- `regime_transition` - Regime state changes
- `sentiment_threshold` - Sentiment crosses threshold
- `vix_spike` - VIX sudden increase
- `ciss_crisis` - CISS enters crisis zone (>0.5)

**Response:**

```json
{
  "alert_id": "alt_1a2b3c4d",
  "status": "active",
  "created_at": "2026-02-03T12:00:00Z"
}
```

---

### Get Alert Subscriptions

#### `GET /api/v1/alerts/subscriptions`

List all active alert configurations.

**Authentication:** Required

**Response:**

```json
{
  "subscriptions": [
    {
      "alert_id": "alt_1a2b3c4d",
      "alert_type": "regime_transition",
      "enabled": true,
      "created_at": "2026-02-03T12:00:00Z",
      "last_triggered": "2026-02-01T15:30:00Z",
      "trigger_count": 3
    }
  ]
}
```

---

### Get Alert History

#### `GET /api/v1/alerts/history`

Retrieve alert trigger history.

**Authentication:** Required

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max results (default: 100) |
| `alert_id` | string | No | Filter by specific alert |
| `start_date` | string | No | ISO 8601 date |

**Response:**

```json
{
  "history": [
    {
      "alert_id": "alt_1a2b3c4d",
      "triggered_at": "2026-02-01T15:30:00Z",
      "alert_type": "regime_transition",
      "data": {
        "from_regime": "risk_on",
        "to_regime": "risk_off",
        "confidence": 0.92
      },
      "acknowledged": true,
      "acknowledged_at": "2026-02-01T15:32:00Z"
    }
  ]
}
```

---

### Acknowledge Alert

#### `POST /api/v1/alerts/history/{alert_id}/acknowledge`

Mark an alert as acknowledged.

**Authentication:** Required

**Response:**

```json
{
  "alert_id": "alt_1a2b3c4d",
  "acknowledged": true,
  "acknowledged_at": "2026-02-03T12:00:00Z"
}
```

---

## 📊 Data Models

### SentimentResponse

```typescript
{
  timestamp: string;           // ISO 8601
  overall_sentiment: number;   // [-1, 1]
  confidence: number;          // [0, 1]
  by_asset_class: {
    [key: string]: {
      sentiment: number;
      volume: number;
      sources: string[];
    }
  };
  top_drivers: Array<{
    text: string;
    sentiment: number;
    asset_class: string;
    source: string;
  }>;
}
```

### RegimeResponse

```typescript
{
  timestamp: string;
  regime: "risk_on" | "risk_off" | "transition";
  confidence: number;
  vix: number;
  ciss: number;
  sentiment_score: number;
  duration_days: number;
  indicators: {
    vix_regime: string;
    ciss_regime: string;
    sentiment_regime: string;
    garch_volatility_forecast: number;
  };
  transition_probability: {
    to_risk_off: number;
    to_transition: number;
    stay_risk_on: number;
  };
}
```

---

## ⚠️ Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "asset_class must be one of: equities, crypto, forex, commodities, all",
    "details": {
      "parameter": "asset_class",
      "provided": "stocks"
    }
  },
  "timestamp": "2026-02-03T12:00:00Z",
  "request_id": "req_1a2b3c4d"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing API key |
| `FORBIDDEN` | 403 | API key lacks required permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `INVALID_PARAMETER` | 400 | Invalid request parameter |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Database or dependency unavailable |

---

## 🚦 Rate Limiting

**Rate Limits (per API key):**
- `/sentiment/*`: 100 requests/minute
- `/regime/*`: 100 requests/minute
- `/alerts/*`: 50 requests/minute
- `/health`: No limit

**Headers:**

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1643897400
```

When rate limit exceeded:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit of 100 requests per minute exceeded",
    "retry_after": 23
  }
}
```

---

## 💡 Examples

### Python

```python
import requests

API_KEY = "sk_live_..."
BASE_URL = "http://localhost:8000"

headers = {"Authorization": f"Bearer {API_KEY}"}

# Get current regime
response = requests.get(f"{BASE_URL}/api/v1/regime/current", headers=headers)
regime = response.json()
print(f"Current regime: {regime['regime']} (confidence: {regime['confidence']})")

# Get sentiment history
params = {
    "start_date": "2026-01-01",
    "asset_class": "crypto",
    "granularity": "daily"
}
response = requests.get(
    f"{BASE_URL}/api/v1/sentiment/history",
    headers=headers,
    params=params
)
history = response.json()
```

### JavaScript (fetch)

```javascript
const API_KEY = "sk_live_...";
const BASE_URL = "http://localhost:8000";

const headers = {
  "Authorization": `Bearer ${API_KEY}`
};

// Get current sentiment
fetch(`${BASE_URL}/api/v1/sentiment/current`, { headers })
  .then(res => res.json())
  .then(data => console.log("Sentiment:", data.overall_sentiment));

// Subscribe to alerts
fetch(`${BASE_URL}/api/v1/alerts/subscribe`, {
  method: "POST",
  headers: {
    ...headers,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    alert_type: "regime_transition",
    conditions: {
      to_regime: "risk_off",
      min_confidence: 0.85
    },
    delivery: {
      method: "webhook",
      endpoint: "https://myapp.com/webhooks/regime"
    }
  })
})
.then(res => res.json())
.then(data => console.log("Alert created:", data.alert_id));
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Get current regime
curl -H "Authorization: Bearer $API_KEY" \
  http://localhost:8000/api/v1/regime/current

# Get sentiment history
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8000/api/v1/sentiment/history?start_date=2026-01-01&asset_class=equities"

# Create alert
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "alert_type": "vix_spike",
    "conditions": {"threshold": 25},
    "delivery": {"method": "webhook", "endpoint": "https://myapp.com/alerts"}
  }' \
  http://localhost:8000/api/v1/alerts/subscribe
```

---

## 📚 Additional Resources

- **Interactive API Docs:** `http://localhost:8000/docs` (Swagger UI)
- **ReDoc Documentation:** `http://localhost:8000/redoc`
- **OpenAPI Spec:** `http://localhost:8000/openapi.json`
- **Source Code:** [src/sentiment_detector/api/](../src/sentiment_detector/api/)

---

**For API support, contact:** Jonathan Rocha (<jrocha@smu.edu>)
