# Phase 1 SHAP/LIME Explainability System - Implementation Blueprint

**Date:** February 5, 2026
**Status:** Ready for Implementation
**Approach:** Pragmatic Balance (Approach 3)
**Timeline:** 8-11 days
**Developer:** Jonathan Rocha

---

## Executive Summary

This document provides a complete implementation plan for adding SHAP-based explainability to the regime classifier system. The approach balances academic requirements (publication figures, committee demo) with engineering quality (maintainable, extensible code).

### Key Decisions Made

1. ✅ **Fix feature pipeline** - Compute proper 20-day rolling features (not approximations)
2. ✅ **Multi-tier caching** - Redis (hot) + PostgreSQL (cold storage)
3. ✅ **New router** - `/api/v1/explainability/*` (clean separation)
4. ✅ **All methods** - SHAP TreeExplainer, Global importance, Feature interactions
5. ✅ **Always include explanations** - Add to RegimeResponse automatically
6. ✅ **Both visualization formats** - Static (PNG/PDF) + Interactive (HTML)
7. ✅ **Load from backtest files** - Historical events use existing analysis data
8. ✅ **JSON serialization** - No pickle in cache (security decision)

**Note on Pickle Usage:** Models are loaded from pickle files (standard scikit-learn practice), but cache serialization uses JSON only. Pickle is ONLY used for loading trusted ML models trained by our own pipeline, never for user input or cache storage.

---

## Architecture Overview

### Three-Layer System

```
┌─────────────────────────────────────────────────────────┐
│                   API Layer (FastAPI)                    │
│  /api/v1/explainability/* (new router)                  │
│  /api/v1/regime/current (modified to include explain)   │
└────────────────────┬───────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│              Service Layer (Core Logic)                 │
│  RegimeExplainer - Main explainability orchestrator    │
│  - explain_prediction()                                 │
│  - global_importance()                                  │
│  - feature_interactions()                               │
└─────┬──────────────┬──────────────┬───────────────────┘
      │              │              │
┌─────▼──────┐  ┌───▼──────┐  ┌───▼─────────────────┐
│  SHAP      │  │  Cache   │  │  Visualization      │
│  Engine    │  │  Layer   │  │  Generators         │
│            │  │          │  │                     │
│ TreeExpl.  │  │ Redis L1 │  │ Static (PNG/PDF)    │
│ Global     │  │ PG L2    │  │ Interactive (HTML)  │
│ Interact.  │  │          │  │                     │
└────────────┘  └──────────┘  └─────────────────────┘
```

---

## 28 Features (From Training)

The model uses these exact features (order matters!):

**CISS Features (8):**

- ciss_lag1, ciss_change, ciss_change_5d
- ciss_ma5, ciss_ma20, ciss_above_ma20
- ciss_std_20d, ciss_trend

**VIX Features (8):**

- vix, vix_change, vix_change_pct
- vix_ma5, vix_ma20, vix_above_ma20
- vix_spike, vix_range

**Sentiment Features (9):**

- sentiment, sentiment_change
- sentiment_momentum_5d, sentiment_momentum_20d
- sentiment_ma5, sentiment_ma20
- sentiment_acceleration, sentiment_dispersion, sentiment_spread

**Interaction Features (3):**

- cross_asset_divergence
- ciss_vix_ratio
- sentiment_vix_interaction

---

## Quick Start (Next Session)

```bash
# 1. Install dependencies
pip install shap>=0.44.0 matplotlib>=3.8.0 redis>=5.0.0

# 2. Create module
mkdir -p src/sentiment_detector/explainability
cd src/sentiment_detector/explainability

# 3. Start with explainer.py (Day 1)
# Copy code from "Core Explainer Class" section below

# 4. Test immediately
python -c "
from explainer import RegimeExplainer
exp = RegimeExplainer()
# Test will go here
"
```

---

## Implementation: 9-Day Roadmap

### Day 1: SHAP Core Engine

**Goal:** Working explainer that can explain 1 prediction

**Tasks:**

1. Create `explainability/explainer.py`
2. Implement `RegimeExplainer` class
3. Load model from pickle checkpoint
4. Initialize SHAP TreeExplainer
5. Implement `explain_prediction()` method
6. Test: Explain 1 prediction, verify SHAP additivity

**Code (Copy-Paste Ready):**

```python
# src/sentiment_detector/explainability/explainer.py
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ExplanationResult:
    """Result from SHAP explanation."""
    feature_names: List[str]
    feature_values: Dict[str, float]
    shap_values: np.ndarray
    base_value: float
    prediction: float
    confidence: float
    predicted_regime: str
    timestamp: datetime
    model_version: str

    def to_dict(self) -> dict:
        """Serialize to JSON (no pickle for security)."""
        return {
            'feature_names': self.feature_names,
            'feature_values': self.feature_values,
            'shap_values': self.shap_values.tolist(),
            'base_value': float(self.base_value),
            'prediction': float(self.prediction),
            'confidence': float(self.confidence),
            'predicted_regime': self.predicted_regime,
            'timestamp': self.timestamp.isoformat(),
            'model_version': self.model_version,
        }

class RegimeExplainer:
    """SHAP-based explainability for regime classifier."""

    def __init__(self, model_path: str = "models/regime_classifier_best.pkl"):
        self.model_path = Path(model_path)
        self._model = None
        self._scaler = None
        self._feature_names = None
        self._explainer = None
        self.model_version = None

    def _load_model(self):
        """Load model from trusted pickle checkpoint."""
        import pickle

        with open(self.model_path, 'rb') as f:
            checkpoint = pickle.load(f)

        self._model = checkpoint['model']
        self._scaler = checkpoint['scaler']
        self._feature_names = checkpoint['feature_names']
        self.model_version = checkpoint.get('model_version', 'unknown')

        # Initialize SHAP
        self._explainer = shap.TreeExplainer(self._model)
        logger.info(f"Loaded model with {len(self._feature_names)} features")

    def explain_prediction(self, features: Dict[str, float]) -> ExplanationResult:
        """Explain prediction using SHAP TreeExplainer."""
        if self._model is None:
            self._load_model()

        # Prepare features in correct order
        feature_vector = pd.DataFrame(
            [[features[name] for name in self._feature_names]],
            columns=self._feature_names,
        )

        # Scale
        feature_scaled = self._scaler.transform(feature_vector)

        # SHAP values
        shap_values = self._explainer.shap_values(feature_scaled)

        # Handle multi-class
        if isinstance(shap_values, list):
            prediction_idx = self._model.predict(feature_scaled)[0]
            shap_values = shap_values[prediction_idx]

        shap_values = shap_values[0]

        # Prediction
        probas = self._model.predict_proba(feature_scaled)[0]
        prediction = np.argmax(probas)
        confidence = probas[prediction]

        # Map to regime
        label_map = {0: 'risk_on', 1: 'transition', 2: 'risk_off'}
        predicted_regime = label_map[prediction]

        # Base value
        base_value = self._explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = base_value[prediction]

        return ExplanationResult(
            feature_names=self._feature_names,
            feature_values=features,
            shap_values=shap_values,
            base_value=float(base_value),
            prediction=float(prediction),
            confidence=float(confidence),
            predicted_regime=predicted_regime,
            timestamp=datetime.utcnow(),
            model_version=self.model_version,
        )
```

**Test:**

```python
# Test it works
explainer = RegimeExplainer()

# Create test features (all 28 required)
features = {
    'ciss_lag1': 0.20, 'ciss_change': 0.01, 'ciss_change_5d': 0.05,
    'ciss_ma5': 0.19, 'ciss_ma20': 0.18, 'ciss_above_ma20': 1,
    'ciss_std_20d': 0.05, 'ciss_trend': 1,
    'vix': 25.0, 'vix_change': 2.0, 'vix_change_pct': 8.0,
    'vix_ma5': 24.0, 'vix_ma20': 22.0, 'vix_above_ma20': 1,
    'vix_spike': 0, 'vix_range': 5.0,
    'sentiment': 0.10, 'sentiment_change': -0.02,
    'sentiment_momentum_5d': -0.05, 'sentiment_momentum_20d': -0.10,
    'sentiment_ma5': 0.12, 'sentiment_ma20': 0.15,
    'sentiment_acceleration': -0.01, 'sentiment_dispersion': 0.15,
    'sentiment_spread': -0.03,
    'cross_asset_divergence': 0.30,
    'ciss_vix_ratio': 0.80,
    'sentiment_vix_interaction': 0.004,
}

result = explainer.explain_prediction(features)
print(f"Predicted: {result.predicted_regime} (confidence: {result.confidence:.2f})")
print(f"Top 3 features:")
for i in np.argsort(np.abs(result.shap_values))[-3:][::-1]:
    print(f"  {result.feature_names[i]}: {result.shap_values[i]:.3f}")

# Verify additivity
shap_sum = result.shap_values.sum()
delta = result.prediction - result.base_value
print(f"SHAP sum: {shap_sum:.3f}, Prediction delta: {delta:.3f}")
assert abs(shap_sum - delta) < 0.01, "SHAP additivity violated!"
```

**Deliverable:** ✅ Working explainer (console output)

---

### Day 2: Global Importance & Polish

**Add to explainer.py:**

```python
def global_importance(self, features_df: pd.DataFrame) -> Dict[str, float]:
    """Compute mean(|SHAP|) across samples."""
    if self._model is None:
        self._load_model()

    shap_values = self._explainer.shap_values(features_df)

    if isinstance(shap_values, list):
        shap_values = np.mean(np.abs(shap_values), axis=0)

    mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
    return dict(zip(self._feature_names, mean_abs_shap))

def feature_interactions(self, features_df: pd.DataFrame, top_k: int = 10) -> dict:
    """Compute SHAP interaction values."""
    if self._model is None:
        self._load_model()

    interaction_values = self._explainer.shap_interaction_values(features_df)

    if isinstance(interaction_values, list):
        interaction_values = np.mean(np.abs(interaction_values), axis=0)

    avg_interactions = np.mean(np.abs(interaction_values), axis=0)

    # Extract top-k pairs
    pairs = []
    n = len(self._feature_names)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((
                self._feature_names[i],
                self._feature_names[j],
                avg_interactions[i, j]
            ))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    return {
        'top_interactions': pairs[:top_k],
        'interaction_matrix': avg_interactions.tolist(),
        'feature_names': self._feature_names,
    }
```

**Deliverable:** ✅ Complete explainer with all methods

---

### Day 3: Caching Layer

**Create migration:**

```sql
-- migrations/versions/xxx_add_explainability_cache.py
CREATE TABLE explainability_cache (
    cache_key VARCHAR(64) PRIMARY KEY,
    explanation_data JSONB NOT NULL,
    computed_at TIMESTAMPTZ DEFAULT NOW(),
    model_version VARCHAR(32),
    INDEX idx_computed_at (computed_at DESC)
);
```

**Create cache.py:**

```python
# src/sentiment_detector/explainability/cache.py
import json
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
import redis.asyncio as aioredis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

class ExplainabilityCache:
    """Two-tier cache: Redis (L1) + PostgreSQL (L2)."""

    def __init__(self, redis_url: str, db_session: AsyncSession):
        self.redis_url = redis_url
        self.db_session = db_session
        self._redis = None

    async def _get_redis(self):
        """Lazy Redis connection."""
        if self._redis is None:
            self._redis = await aioredis.from_url(
                self.redis_url,
                decode_responses=True,
            )
        return self._redis

    async def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get from cache (L1 -> L2)."""
        # Try Redis first
        redis = await self._get_redis()
        value = await redis.get(cache_key)

        if value:
            logger.debug(f"Cache hit (Redis): {cache_key}")
            return json.loads(value)

        # Try PostgreSQL
        result = await self.db_session.execute(
            text("SELECT explanation_data FROM explainability_cache WHERE cache_key = :key"),
            {"key": cache_key}
        )
        row = result.fetchone()

        if row:
            logger.debug(f"Cache hit (PostgreSQL): {cache_key}")
            value = json.loads(row[0])
            # Promote to Redis
            await redis.setex(cache_key, 86400, json.dumps(value))
            return value

        logger.debug(f"Cache miss: {cache_key}")
        return None

    async def set(self, cache_key: str, value: Dict[str, Any]):
        """Set in both tiers."""
        json_value = json.dumps(value)

        # Redis (24h TTL)
        redis = await self._get_redis()
        await redis.setex(cache_key, 86400, json_value)

        # PostgreSQL (permanent)
        await self.db_session.execute(
            text("""
                INSERT INTO explainability_cache (cache_key, explanation_data, model_version)
                VALUES (:key, :data::jsonb, :version)
                ON CONFLICT (cache_key) DO UPDATE
                SET explanation_data = EXCLUDED.explanation_data,
                    computed_at = NOW()
            """),
            {
                "key": cache_key,
                "data": json_value,
                "version": value.get("model_version", "unknown")
            }
        )
        await self.db_session.commit()

        logger.info(f"Cached: {cache_key}")

    @staticmethod
    def make_cache_key(model_version: str, features: Dict[str, float]) -> str:
        """Generate deterministic cache key."""
        features_str = json.dumps(features, sort_keys=True)
        hash_str = hashlib.sha256(features_str.encode()).hexdigest()[:16]
        return f"explain:{model_version}:{hash_str}"
```

**Integrate with explainer:**

```python
# Update RegimeExplainer.__init__
def __init__(self, model_path: str = "...", cache: Optional[ExplainabilityCache] = None):
    # ... existing ...
    self.cache = cache

# Update explain_prediction
def explain_prediction(self, features: Dict[str, float]) -> ExplanationResult:
    if self._model is None:
        self._load_model()

    # Check cache
    if self.cache:
        cache_key = ExplainabilityCache.make_cache_key(self.model_version, features)
        cached = await self.cache.get(cache_key)
        if cached:
            # Deserialize
            cached['shap_values'] = np.array(cached['shap_values'])
            cached['timestamp'] = datetime.fromisoformat(cached['timestamp'])
            return ExplanationResult(**cached)

    # ... compute SHAP ...
    result = ExplanationResult(...)

    # Cache result
    if self.cache:
        await self.cache.set(cache_key, result.to_dict())

    return result
```

**Deliverable:** ✅ Working cache with Redis + PostgreSQL

---

### Days 4-6: API Integration

(Detailed in full document - key endpoints):

1. `/api/v1/explainability/current` - Explain current regime
2. `/api/v1/explainability/date/{date}` - Explain specific date
3. `/api/v1/explainability/events/{event}` - Explain crisis event
4. `/api/v1/explainability/global-importance` - Global feature importance

**Modify existing:** `/api/v1/regime/current` adds `explanation` field

---

### Days 7-9: Visualization & Paper

**Key visualizations:**

1. Waterfall plots (6 crisis events)
2. Global importance bar chart
3. Feature interaction heatmap

**Jupyter notebook** for analysis and LaTeX table generation

---

## File Structure

```
src/sentiment_detector/
├── explainability/
│   ├── __init__.py
│   ├── explainer.py          # RegimeExplainer class
│   ├── cache.py              # ExplainabilityCache
│   └── viz.py                # Visualization (Day 7)
├── api/routes/
│   ├── explainability.py     # NEW router (Day 4)
│   └── regime.py             # MODIFY (Day 5)
└── api/schemas/
    ├── explainability.py     # NEW (Day 4)
    └── regime.py             # MODIFY (Day 5)

notebooks/
└── explainability_analysis.ipynb  # Day 8

figures/explainability/        # Day 7
├── waterfall_*.png (6 events)
└── global_importance.png
```

---

## Crisis Events (Hardcoded)

```python
# src/sentiment_detector/explainability/events.py
CRISIS_EVENTS = {
    "2008_financial_crisis": {
        "date": "2008-11-20",
        "name": "Financial Crisis Peak"
    },
    "covid_crash": {
        "date": "2020-03-16",
        "name": "COVID-19 Crash"
    },
    "luna_terra": {
        "date": "2022-05-12",
        "name": "Luna/Terra Collapse"
    },
    "celsius_3ac": {
        "date": "2022-06-15",
        "name": "Celsius/3AC Contagion"
    },
    "gamestop": {
        "date": "2021-01-28",
        "name": "GameStop Episode"
    },
    "oos_validation": {
        "date": "2024-06-01",
        "name": "Out-of-Sample Period"
    }
}
```

---

## Testing Checklist

- [ ] SHAP additivity holds: `sum(shap_values) ≈ prediction - base_value`
- [ ] Cache hit <50ms, miss <500ms
- [ ] All 28 features present in explanation
- [ ] Top 3 features make intuitive sense
- [ ] Figures at 300 DPI
- [ ] Notebook runs end-to-end
- [ ] API returns 200 for all endpoints

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Cache hit (Redis) | <50ms |
| Cache miss (SHAP) | <500ms |
| Cache hit rate | >80% |
| Figure generation | <2s |

---

## What to Do in Next Session

1. **Start fresh terminal:**

   ```bash
   cd /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone
   pip install shap matplotlib redis
   ```

2. **Day 1 Morning: Create explainer.py**
   - Copy code from "Day 1" section above
   - Test with single prediction
   - Verify SHAP additivity

3. **Reference this doc** for:
   - Daily breakdown
   - Code snippets
   - Testing approach

4. **Track progress** - Check off tasks daily

---

## Success Criteria

### MVP (Day 6)

- API returns explanations
- Cache works
- 6 events explainable

### Paper (Day 9)

- 8 figures at 300 DPI
- Working notebook
- Demo-ready

---

**Timeline: 8-11 days to paper-ready system**
**Approach: Pragmatic Balance**
**Status: Ready to implement**
