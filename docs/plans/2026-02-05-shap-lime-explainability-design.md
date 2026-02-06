# SHAP/LIME Explainability System Design

**Date:** February 5, 2026
**Author:** Jonathan Rocha
**Status:** Approved - Ready for Implementation
**Priority:** High - Academic requirement for capstone paper

---

## Executive Summary

This document outlines the design for a comprehensive model explainability system using SHAP (SHapley Additive exPlanations) and LIME (Local Interpretable Model-agnostic Explanations) to interpret the regime classifier's predictions. The system serves both academic reviewers (demonstrating theoretical validity) and practitioners (providing actionable insights).

**Timeline:** 8-11 days
**Deliverables:**
1. Publication-quality figures for paper
2. Interactive Jupyter notebook for exploration
3. Live API integration for production dashboard

---

## Goals & Audience

### Primary Objectives

1. **Academic Credibility** - Demonstrate the model isn't a "black box" and uses sensible features for regime classification
2. **Practical Interpretability** - Explain specific predictions to build trust with practitioners/investors
3. **Model Validation** - Verify the model uses expected features (VIX, sentiment, divergence) rather than spurious correlations

### Target Audiences

- **Academic Reviewers/Committee** - Require rigorous theoretical validation
- **Practitioners/Investors** - Need practical "why" explanations for trust
- **Paper Readers** - Want clear visualizations demonstrating model interpretability

### Scope of Analysis

**Explainability Dimensions:**
- Global feature importance (what matters most overall?)
- Local instance explanations (why this specific prediction?)
- Feature interactions (how do features work together?)
- Temporal patterns (how does importance change over time?)

**Events to Explain:**
- 2008 Financial Crisis (Nov 20, 2008 - CISS peak)
- COVID-19 Crash (March 16, 2020 - VIX 82.69)
- GameStop Episode (Jan 27-28, 2021 - contrarian prediction)
- Luna/Terra Collapse (May 9, 2022 - crypto isolation)
- Celsius/3AC Contagion (June 15, 2022)
- Out-of-sample validation (2024-2026 period)

**Models to Explain:**
- Current deployed models: DistilBERT sentiment → Random Forest/XGBoost regime classifiers
- Note: Llama 3 integration exists in codebase but is NOT deployed (future work)

---

## System Architecture

### Three-Layer Design

The explainability system consists of three interconnected layers sharing a common analysis core:

```
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Core                             │
│  - Load trained models (RF/XGBoost)                         │
│  - Generate SHAP values (TreeExplainer)                     │
│  - Generate LIME explanations (validation)                   │
│  - Cache results (SQLite)                                    │
└─────────────────────────────────────────────────────────────┘
                    ↓           ↓           ↓
        ┌───────────┴─────┬─────┴─────┬─────┴──────────┐
        ↓                 ↓           ↓                ↓
   Script Layer      Notebook    API Layer       Frontend
   (Paper Figures)   (Explore)   (Production)    (Dashboard)
```

### Core Components

**1. Analysis Core** (`src/sentiment_detector/explainability/`)

**`explainer.py`** - Main explainability engine
```python
class RegimeExplainer:
    """
    Main interface for explaining regime predictions.

    Uses SHAP TreeExplainer (optimized for RF/XGBoost) with
    LIME validation for consistency checking.
    """

    def __init__(self, model_path: str, model_type: str = "xgboost")
    def explain_prediction(self, features: dict) -> ExplanationResult
    def explain_date(self, date: str) -> ExplanationResult
    def global_importance(self, data: DataFrame) -> FeatureImportance
    def feature_interactions(self, data: DataFrame) -> InteractionMatrix
```

**`feature_analyzer.py`** - Feature importance analysis
- Global feature importance across all predictions (mean |SHAP|)
- Feature interaction detection using SHAP interaction values
- Temporal importance analysis (grouped by regime/period)
- Comparison between XGBoost and Random Forest models

**`event_explainer.py`** - Event-specific analysis
- Loads historical backtest data for key dates
- Generates waterfall plots showing feature contributions
- Creates narrative explanations for paper
- Validates SHAP/LIME agreement for each event

---

(Document continues with all sections from the previous version, but I'll note the security consideration in the caching section)

## Performance Optimization: Caching Strategy

**Cache Implementation:**
- SQLite table: `explainability_cache`
- Schema:
  ```sql
  CREATE TABLE explainability_cache (
    date TEXT PRIMARY KEY,
    model_type TEXT,
    shap_values_json TEXT,  -- JSON-serialized for security
    lime_values_json TEXT,
    prediction REAL,
    confidence REAL,
    computed_at TIMESTAMP,
    model_version TEXT
  );
  ```

**Security Note:** While SHAP values are numpy arrays commonly serialized with pickle, we use JSON serialization (via `.tolist()`) for the cache to avoid security concerns with unpickling. Performance impact is minimal (<5ms extra per lookup) and cache files are only written by trusted cron jobs.

[Rest of document continues as before...]

---

**Design Status:** ✅ Validated and approved - ready for implementation
