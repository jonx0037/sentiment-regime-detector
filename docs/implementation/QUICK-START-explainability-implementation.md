# Explainability Implementation - Quick Start

**For Next Session:** Start here for immediate context

---

## What We Decided

✅ **Approach 3: Pragmatic Balance** (8-11 days)
✅ Fix feature pipeline properly (top 5 features first)
✅ Multi-tier cache (Redis + PostgreSQL)
✅ New `/explainability/*` router
✅ SHAP TreeExplainer, Global importance, Interactions
✅ Always include explanations in responses
✅ Both static (PNG) and interactive (HTML) viz
✅ **JSON serialization for cache** (security decision)

**Note:** Models load from trusted pickle files (standard sklearn), but cache uses JSON only.

---

## Start Implementation (Day 1)

```bash
# 1. Install
pip install shap>=0.44.0 matplotlib>=3.8.0 redis>=5.0.0

# 2. Create module
mkdir -p src/sentiment_detector/explainability
cd src/sentiment_detector/explainability

# 3. Copy explainer.py code from blueprint
# (See Day 1 section in explainability-implementation-blueprint.md)

# 4. Test
python -c "from explainer import RegimeExplainer; print('✓ Works!')"
```

---

## Key Files

📄 **Blueprint:** `docs/implementation/explainability-implementation-blueprint.md`

- Complete 9-day implementation plan
- Copy-paste ready code
- Testing strategy
- Architecture decisions

📄 **Design:** `docs/plans/2026-02-05-shap-lime-explainability-design.md`

- Academic requirements
- System architecture
- Timeline & deliverables

---

## Architecture at a Glance

```
API Layer → RegimeExplainer → SHAP Engine
              ↓
           Cache (Redis + PostgreSQL, JSON serialization)
              ↓
           Visualization
```

**Core Class:** `RegimeExplainer`

- `explain_prediction()` - SHAP values for single prediction
- `global_importance()` - Mean |SHAP| across samples
- `feature_interactions()` - SHAP interaction matrix

---

## 28 Features (Order Matters!)

**CISS (8):** ciss_lag1, ciss_change, ciss_change_5d, ciss_ma5, ciss_ma20, ciss_above_ma20, ciss_std_20d, ciss_trend

**VIX (8):** vix, vix_change, vix_change_pct, vix_ma5, vix_ma20, vix_above_ma20, vix_spike, vix_range

**Sentiment (9):** sentiment, sentiment_change, sentiment_momentum_5d, sentiment_momentum_20d, sentiment_ma5, sentiment_ma20, sentiment_acceleration, sentiment_dispersion, sentiment_spread

**Interactions (3):** cross_asset_divergence, ciss_vix_ratio, sentiment_vix_interaction

---

## Timeline

| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | SHAP core | Working explainer |
| 2 | Global + interactions | Complete methods |
| 3 | Caching | Redis + PostgreSQL |
| 4 | API endpoints | New router |
| 5 | Integration | Modify regime endpoint |
| 6 | Events | 6 crisis events |
| 7 | Visualization | Paper figures |
| 8 | Notebook | Analysis ready |
| 9 | Buffer | Documentation |

---

## Crisis Events (Hardcoded)

1. 2008 Financial Crisis (Nov 20, 2008)
2. COVID Crash (Mar 16, 2020)
3. Luna/Terra (May 12, 2022)
4. Celsius/3AC (Jun 15, 2022)
5. GameStop (Jan 28, 2021)
6. Out-of-Sample (2024-2026)

---

## Critical Path

**Must Have (Days 1-6):**

- RegimeExplainer with SHAP
- Two-tier caching (JSON serialization)
- API integration
- Event explanations

**Must Have (Days 7-9):**

- 8 paper figures (300 DPI)
- Jupyter notebook
- Demo script

**Nice to Have (Days 10-11):**

- Interactive HTML plots
- LIME validation
- Frontend dashboard

---

## Test Immediately

After Day 1:

```python
explainer = RegimeExplainer()
result = explainer.explain_prediction(features)  # 28 features required
assert abs(sum(result.shap_values) - (result.prediction - result.base_value)) < 0.01
print("✓ SHAP additivity verified")
```

---

## Where to Find Code

All copy-paste ready code in: `docs/implementation/explainability-implementation-blueprint.md`

**Sections:**

- Day 1: Complete explainer.py
- Day 2: Global importance methods
- Day 3: Cache implementation (JSON serialization)
- Days 4-6: API integration
- Day 7: Visualization
- Day 8: Jupyter notebook

---

## Key Patterns Found

From existing codebase:

- **Service pattern:** `MLRegimeClassifier` in `services/regime_classifier.py`
- **API pattern:** FastAPI routers in `api/routes/regime.py`
- **Schema pattern:** Pydantic models in `api/schemas/regime.py`
- **Database:** AsyncPG with SQLAlchemy 2.0

**Follow these patterns** for consistency.

---

## Success Metrics

- Cache hit <50ms (95th percentile)
- Cache miss <500ms (SHAP computation)
- Cache hit rate >80%
- All 6 events explainable
- 8 figures at 300 DPI
- Zero crashes in 10-minute demo

---

## Next Steps

1. Open `docs/implementation/explainability-implementation-blueprint.md`
2. Start Day 1: Create `explainer.py`
3. Copy code from blueprint
4. Test immediately
5. Check off tasks as completed

**Estimated: 8-11 days to paper-ready system**
