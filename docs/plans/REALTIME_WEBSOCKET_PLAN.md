# Real-Time WebSocket Integration Plan

**Date:** February 6, 2026
**Status:** HIGH PRIORITY
**Goal:** Implement WebSocket streaming for live sentiment and regime updates

---

## 🎯 Architecture Overview

```
┌─────────────────┐         WebSocket         ┌──────────────────┐
│  React Frontend │◄──────────────────────────►│  FastAPI Backend │
│   (Next.js)     │   (wss://api/v1/stream)   │   (Uvicorn)      │
└─────────────────┘                            └──────────────────┘
                                                        │
                                                        │ Subscribe
                                                        ▼
                                               ┌──────────────────┐
                                               │  Redis Pub/Sub   │
                                               │   (Real-time)    │
                                               └──────────────────┘
                                                        ▲
                                                        │ Publish
                                               ┌────────┴─────────┐
                                               │                  │
                                      ┌────────▼──────┐  ┌───────▼────────┐
                                      │ Data Collector │  │ Regime Monitor │
                                      │   (Background) │  │  (Background)  │
                                      └────────────────┘  └────────────────┘
```

---

## 📋 Implementation Checklist

### Phase 1: Backend WebSocket Infrastructure (1-2 days)

#### Step 1.1: Install Dependencies
```bash
# Add to pyproject.toml dependencies
pip install "websockets>=12.0"
pip install "python-socketio>=5.11.0"  # Alternative: Socket.IO
pip install "redis[hiredis]>=5.0.0"  # Already installed
```

#### Step 1.2: Create WebSocket Manager
**File:** `src/sentiment_detector/core/websocket.py`

```python
"""WebSocket connection manager for real-time updates."""

from typing import Dict, Set
import asyncio
import logging
from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as redis
import json

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections and broadcast messages."""

    def __init__(self):
        # Active connections by client_id
        self.active_connections: Dict[str, WebSocket] = {}
        # Subscriptions by topic
        self.subscriptions: Dict[str, Set[str]] = {
            "sentiment": set(),
            "regime": set(),
            "alerts": set(),
            "market": set()
        }
        self.redis: redis.Redis = None

    async def connect(self, client_id: str, websocket: WebSocket):
        """Accept new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected. Total: {len(self.active_connections)}")

    async def disconnect(self, client_id: str):
        """Remove WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        # Remove from all subscriptions
        for topic_subs in self.subscriptions.values():
            topic_subs.discard(client_id)
        logger.info(f"Client {client_id} disconnected. Total: {len(self.active_connections)}")

    async def subscribe(self, client_id: str, topic: str):
        """Subscribe client to topic."""
        if topic in self.subscriptions:
            self.subscriptions[topic].add(client_id)
            logger.info(f"Client {client_id} subscribed to {topic}")
        else:
            logger.warning(f"Unknown topic: {topic}")

    async def unsubscribe(self, client_id: str, topic: str):
        """Unsubscribe client from topic."""
        if topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)
            logger.info(f"Client {client_id} unsubscribed from {topic}")

    async def send_personal_message(self, message: dict, client_id: str):
        """Send message to specific client."""
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_json(message)
            except WebSocketDisconnect:
                await self.disconnect(client_id)

    async def broadcast_to_topic(self, message: dict, topic: str):
        """Broadcast message to all clients subscribed to topic."""
        if topic not in self.subscriptions:
            return

        disconnected_clients = []
        for client_id in self.subscriptions[topic]:
            if client_id in self.active_connections:
                websocket = self.active_connections[client_id]
                try:
                    await websocket.send_json(message)
                except WebSocketDisconnect:
                    disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            await self.disconnect(client_id)

    async def start_redis_listener(self, redis_client: redis.Redis):
        """Listen to Redis pub/sub for updates."""
        self.redis = redis_client
        pubsub = redis_client.pubsub()

        # Subscribe to all topics
        await pubsub.subscribe(
            "sentiment_updates",
            "regime_updates",
            "alert_updates",
            "market_updates"
        )

        async for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    topic = message["channel"].replace("_updates", "")
                    await self.broadcast_to_topic(data, topic)
                except Exception as e:
                    logger.error(f"Error processing Redis message: {e}")


# Global connection manager
manager = ConnectionManager()
```

#### Step 1.3: Create WebSocket Endpoint
**File:** `src/sentiment_detector/api/routes/websocket.py`

```python
"""WebSocket endpoints for real-time updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sentiment_detector.core.websocket import manager
import uuid
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates.

    Client sends:
        {"type": "subscribe", "topic": "sentiment"}
        {"type": "unsubscribe", "topic": "regime"}
        {"type": "ping"}

    Server sends:
        {"type": "sentiment", "data": {...}}
        {"type": "regime", "data": {...}}
        {"type": "pong"}
    """
    client_id = str(uuid.uuid4())
    await manager.connect(client_id, websocket)

    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "welcome",
            "client_id": client_id,
            "available_topics": ["sentiment", "regime", "alerts", "market"]
        }, client_id)

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            msg_type = message.get("type")

            if msg_type == "subscribe":
                topic = message.get("topic")
                await manager.subscribe(client_id, topic)
                await manager.send_personal_message({
                    "type": "subscribed",
                    "topic": topic
                }, client_id)

            elif msg_type == "unsubscribe":
                topic = message.get("topic")
                await manager.unsubscribe(client_id, topic)
                await manager.send_personal_message({
                    "type": "unsubscribed",
                    "topic": topic
                }, client_id)

            elif msg_type == "ping":
                await manager.send_personal_message({
                    "type": "pong",
                    "timestamp": message.get("timestamp")
                }, client_id)

    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        await manager.disconnect(client_id)


@router.get("/active_connections")
async def get_active_connections():
    """Get count of active WebSocket connections (admin endpoint)."""
    return {
        "active_connections": len(manager.active_connections),
        "subscriptions": {
            topic: len(subs)
            for topic, subs in manager.subscriptions.items()
        }
    }
```

#### Step 1.4: Register WebSocket Router
**File:** `src/sentiment_detector/api/router.py`

```python
from sentiment_detector.api.routes import websocket

# Register WebSocket routes
api_router.include_router(
    websocket.router,
    prefix="/ws",
    tags=["websocket"]
)
```

---

### Phase 2: Background Data Publishers (2-3 days)

#### Step 2.1: Sentiment Publisher
**File:** `src/sentiment_detector/background/sentiment_publisher.py`

```python
"""Background task to publish sentiment updates."""

import asyncio
import redis.asyncio as redis
from datetime import datetime, timedelta
import logging
from sentiment_detector.services.sentiment_service import SentimentService

logger = logging.getLogger(__name__)


async def publish_sentiment_updates(redis_client: redis.Redis):
    """
    Publish sentiment updates every 5 minutes.

    Aggregates new sentiment data and broadcasts to subscribers.
    """
    sentiment_service = SentimentService()
    last_update = datetime.utcnow() - timedelta(minutes=5)

    while True:
        try:
            # Get latest sentiment aggregates
            current_sentiment = await sentiment_service.get_latest_aggregate()

            # Publish to Redis
            await redis_client.publish(
                "sentiment_updates",
                {
                    "type": "sentiment",
                    "data": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "overall": current_sentiment.overall_score,
                        "by_asset_class": {
                            "equities": current_sentiment.equities_score,
                            "crypto": current_sentiment.crypto_score,
                            "forex": current_sentiment.forex_score,
                            "commodities": current_sentiment.commodities_score
                        },
                        "trend": current_sentiment.trend,  # "rising", "falling", "stable"
                        "confidence": current_sentiment.confidence
                    }
                }
            )

            last_update = datetime.utcnow()
            logger.info(f"Published sentiment update: {current_sentiment.overall_score:.3f}")

        except Exception as e:
            logger.error(f"Error publishing sentiment: {e}")

        # Wait 5 minutes
        await asyncio.sleep(300)
```

#### Step 2.2: Regime Publisher
**File:** `src/sentiment_detector/background/regime_publisher.py`

```python
"""Background task to publish regime updates."""

import asyncio
import redis.asyncio as redis
from datetime import datetime
import logging
from sentiment_detector.models.regime_classifier import RegimeClassifier

logger = logging.getLogger(__name__)


async def publish_regime_updates(redis_client: redis.Redis):
    """
    Publish regime updates every 1 minute.

    Detects regime transitions and broadcasts alerts.
    """
    classifier = RegimeClassifier()
    last_regime = None

    while True:
        try:
            # Predict current regime
            current_regime = await classifier.predict_current_regime()

            # Check for regime transition
            regime_changed = last_regime and current_regime.label != last_regime.label

            # Publish update
            await redis_client.publish(
                "regime_updates",
                {
                    "type": "regime",
                    "data": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "regime": current_regime.label,  # "risk_on", "risk_off", "transition"
                        "confidence": current_regime.confidence,
                        "vix": current_regime.features.vix,
                        "ciss": current_regime.features.ciss,
                        "sentiment": current_regime.features.sentiment_score,
                        "changed": regime_changed,
                        "previous_regime": last_regime.label if last_regime else None
                    }
                }
            )

            # If regime changed, publish alert
            if regime_changed:
                await redis_client.publish(
                    "alert_updates",
                    {
                        "type": "alert",
                        "data": {
                            "timestamp": datetime.utcnow().isoformat(),
                            "alert_type": "regime_transition",
                            "severity": "high" if current_regime.label == "risk_off" else "medium",
                            "message": f"Regime transition: {last_regime.label} → {current_regime.label}",
                            "data": {
                                "old_regime": last_regime.label,
                                "new_regime": current_regime.label,
                                "confidence": current_regime.confidence
                            }
                        }
                    }
                )

            last_regime = current_regime
            logger.info(f"Published regime update: {current_regime.label} ({current_regime.confidence:.2f})")

        except Exception as e:
            logger.error(f"Error publishing regime: {e}")

        # Wait 1 minute
        await asyncio.sleep(60)
```

#### Step 2.3: Start Background Tasks
**File:** `src/sentiment_detector/main.py`

```python
import redis.asyncio as redis
from sentiment_detector.core.websocket import manager
from sentiment_detector.background.sentiment_publisher import publish_sentiment_updates
from sentiment_detector.background.regime_publisher import publish_regime_updates

@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup."""
    # Initialize Redis
    redis_client = redis.from_url(settings.REDIS_URL)

    # Start Redis listener for WebSocket broadcasts
    asyncio.create_task(manager.start_redis_listener(redis_client))

    # Start background publishers
    asyncio.create_task(publish_sentiment_updates(redis_client))
    asyncio.create_task(publish_regime_updates(redis_client))

    logger.info("Background tasks started")
```

---

### Phase 3: Frontend WebSocket Client (2 days)

#### Step 3.1: Create WebSocket Hook
**File:** `frontend/src/hooks/useWebSocket.ts`

```typescript
import { useEffect, useState, useCallback, useRef } from 'react';

interface WebSocketMessage {
  type: string;
  data?: any;
  topic?: string;
  timestamp?: string;
}

interface UseWebSocketOptions {
  url: string;
  topics?: string[];
  reconnectInterval?: number;
  reconnectAttempts?: number;
}

export function useWebSocket({
  url,
  topics = [],
  reconnectInterval = 3000,
  reconnectAttempts = 5
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const ws = useRef<WebSocket | null>(null);
  const reconnectCount = useRef(0);
  const reconnectTimeout = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    try {
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setError(null);
        reconnectCount.current = 0;

        // Subscribe to topics
        topics.forEach(topic => {
          ws.current?.send(JSON.stringify({
            type: 'subscribe',
            topic
          }));
        });
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data) as WebSocketMessage;
        setLastMessage(message);
      };

      ws.current.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError(new Error('WebSocket connection error'));
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);

        // Attempt reconnect
        if (reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;
          console.log(`Reconnecting... (${reconnectCount.current}/${reconnectAttempts})`);
          reconnectTimeout.current = setTimeout(connect, reconnectInterval);
        } else {
          setError(new Error('Max reconnection attempts reached'));
        }
      };
    } catch (err) {
      setError(err as Error);
    }
  }, [url, topics, reconnectInterval, reconnectAttempts]);

  const disconnect = useCallback(() => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
    }
    ws.current?.close();
    ws.current = null;
  }, []);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (ws.current && isConnected) {
      ws.current.send(JSON.stringify(message));
    }
  }, [isConnected]);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    error,
    sendMessage,
    reconnect: connect
  };
}
```

#### Step 3.2: Create Live Dashboard Component
**File:** `frontend/src/components/LiveDashboard.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';

interface SentimentData {
  timestamp: string;
  overall: number;
  by_asset_class: {
    equities: number;
    crypto: number;
    forex: number;
    commodities: number;
  };
  trend: 'rising' | 'falling' | 'stable';
  confidence: number;
}

interface RegimeData {
  timestamp: string;
  regime: 'risk_on' | 'risk_off' | 'transition';
  confidence: number;
  vix: number;
  ciss: number;
  sentiment: number;
  changed: boolean;
}

export function LiveDashboard() {
  const [sentiment, setSentiment] = useState<SentimentData | null>(null);
  const [regime, setRegime] = useState<RegimeData | null>(null);

  const { isConnected, lastMessage, error } = useWebSocket({
    url: 'wss://sentiment-regime-detector-production.up.railway.app/api/v1/ws/stream',
    topics: ['sentiment', 'regime']
  });

  useEffect(() => {
    if (lastMessage) {
      if (lastMessage.type === 'sentiment') {
        setSentiment(lastMessage.data);
      } else if (lastMessage.type === 'regime') {
        setRegime(lastMessage.data);
      }
    }
  }, [lastMessage]);

  return (
    <div className="live-dashboard">
      <div className="connection-status">
        {isConnected ? (
          <span className="status-connected">● Live</span>
        ) : (
          <span className="status-disconnected">○ Disconnected</span>
        )}
      </div>

      {error && (
        <div className="error-banner">
          Connection error: {error.message}
        </div>
      )}

      <div className="data-grid">
        <div className="sentiment-card">
          <h3>Live Sentiment</h3>
          {sentiment ? (
            <>
              <div className="score-display">
                {sentiment.overall.toFixed(3)}
              </div>
              <div className="trend-indicator">
                {sentiment.trend === 'rising' ? '↑' :
                 sentiment.trend === 'falling' ? '↓' : '→'}
              </div>
              <div className="asset-breakdown">
                <div>Equities: {sentiment.by_asset_class.equities.toFixed(2)}</div>
                <div>Crypto: {sentiment.by_asset_class.crypto.toFixed(2)}</div>
                <div>Forex: {sentiment.by_asset_class.forex.toFixed(2)}</div>
                <div>Commodities: {sentiment.by_asset_class.commodities.toFixed(2)}</div>
              </div>
            </>
          ) : (
            <div>Waiting for data...</div>
          )}
        </div>

        <div className="regime-card">
          <h3>Current Regime</h3>
          {regime ? (
            <>
              <div className={`regime-badge regime-${regime.regime}`}>
                {regime.regime.replace('_', ' ').toUpperCase()}
              </div>
              {regime.changed && (
                <div className="transition-alert">
                  ⚠️ Regime Transition Detected
                </div>
              )}
              <div className="metrics">
                <div>VIX: {regime.vix.toFixed(2)}</div>
                <div>CISS: {regime.ciss.toFixed(3)}</div>
                <div>Confidence: {(regime.confidence * 100).toFixed(0)}%</div>
              </div>
            </>
          ) : (
            <div>Waiting for data...</div>
          )}
        </div>
      </div>
    </div>
  );
}
```

---

## 📊 Testing Plan

### Test 1: WebSocket Connection
```bash
# Use wscat to test endpoint
npm install -g wscat
wscat -c ws://localhost:8000/api/v1/ws/stream

# Send subscribe message
> {"type": "subscribe", "topic": "sentiment"}

# Should receive updates every 5 minutes
```

### Test 2: Load Testing
```python
# scripts/validation/test_websocket_load.py
import asyncio
import websockets
import json

async def connect_client(client_id: int):
    uri = "ws://localhost:8000/api/v1/ws/stream"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "subscribe", "topic": "regime"}))
        async for message in ws:
            data = json.loads(message)
            print(f"Client {client_id}: {data['type']}")

async def main():
    # Simulate 100 concurrent clients
    tasks = [connect_client(i) for i in range(100)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

**Target:** Handle 100+ concurrent connections with <100ms message delivery latency

---

## 📅 Timeline

| Phase | Duration | Priority |
|-------|----------|----------|
| **Phase 1: Backend Infrastructure** | 1-2 days | CRITICAL |
| **Phase 2: Background Publishers** | 2-3 days | HIGH |
| **Phase 3: Frontend Client** | 2 days | HIGH |

**Total:** 5-7 days to production

---

## 🚀 Deployment

### Railway Configuration
Add to `Procfile`:
```
web: uvicorn sentiment_detector.main:app --host 0.0.0.0 --port $PORT --ws websockets
```

### Environment Variables
```bash
REDIS_URL=redis://...  # Already configured
WEBSOCKET_HEARTBEAT=30  # Ping interval (seconds)
WEBSOCKET_MAX_CONNECTIONS=1000
```

---

**Contact:** Jonathan Rocha (jrocha@smu.edu)
**Advisor:** David (King Ip) Lin, Ph.D. (kdlin@smu.edu)
