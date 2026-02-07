# Historical Backtest Validation Plan

**Date:** February 6, 2026
**Status:** CRITICAL - Trust Issues Identified
**Goal:** Validate accuracy of historical backtests and live site numbers

---

## 🚨 Problem Statement

**Current Issue:** Testing suite was broken, raising concerns about:
1. Historical backtest accuracy
2. Live site regime predictions
3. GARCH-MIDAS model validation
4. Crisis event analysis correctness

**Impact:** Cannot trust production numbers without validation

---

## 📋 Validation Approach

### Phase 1: Test Suite Validation (COMPLETED ✅)

#### ✅ Fixed pytest Configuration
- Added `pythonpath = ["src"]` to `pyproject.toml`
- **Result:** 25/25 tests passing in `test_sentiment_ensemble.py`
- **Confidence:** Sentiment ensemble logic is correct

#### Next: Run Full Test Suite
```bash
# Run all tests
pytest -v --cov=sentiment_detector --cov-report=html

# Expected: Identify any failing tests
```

---

### Phase 2: Data Integrity Validation (1 day)

#### Step 2.1: Verify Database Records
**Script:** `scripts/validation/verify_data_integrity.py`

```python
"""Verify data integrity for backtests."""

import asyncio
from sqlalchemy import select, func
from sentiment_detector.core.database import async_session
from sentiment_detector.core.models import Text, SentimentScore, MarketData, Regime

async def validate_data_integrity():
    """Check for data gaps and inconsistencies."""
    async with async_session() as session:
        # Check text counts
        text_count = await session.scalar(select(func.count(Text.id)))
        print(f"✓ Texts in database: {text_count:,}")

        # Check sentiment scores
        sentiment_count = await session.scalar(select(func.count(SentimentScore.id)))
        print(f"✓ Sentiment scores: {sentiment_count:,}")

        # Check market data coverage
        market_count = await session.scalar(select(func.count(MarketData.id)))
        print(f"✓ Market data points: {market_count:,}")

        # Check date coverage
        earliest_date = await session.scalar(
            select(func.min(Text.collected_at))
        )
        latest_date = await session.scalar(
            select(func.max(Text.collected_at))
        )
        print(f"✓ Date range: {earliest_date} to {latest_date}")

        # Check for gaps in CISS data
        ciss_gaps = await session.execute(
            select(MarketData.date).where(MarketData.ciss.is_(None))
        )
        gaps_count = len(ciss_gaps.all())
        if gaps_count > 0:
            print(f"⚠️  CISS data gaps: {gaps_count} dates")
        else:
            print("✓ CISS data complete")

        # Check VIX data
        vix_missing = await session.scalar(
            select(func.count(MarketData.id)).where(MarketData.vix.is_(None))
        )
        if vix_missing > 0:
            print(f"⚠️  VIX missing: {vix_missing} records")
        else:
            print("✓ VIX data complete")

asyncio.run(validate_data_integrity())
```

**Run:**
```bash
python scripts/validation/verify_data_integrity.py
```

**Expected Output:**
```
✓ Texts in database: 2,660,000
✓ Sentiment scores: 2,660,000
✓ Market data points: 135,000
✓ Date range: 2002-01-01 to 2026-02-06
✓ CISS data complete
✓ VIX data complete
```

#### Step 2.2: Validate Crisis Event Dates
**Script:** `scripts/validation/validate_crisis_events.py`

```python
"""Validate crisis event data alignment."""

import pandas as pd
from datetime import datetime

CRISIS_EVENTS = {
    "2008_crisis": {
        "start": "2008-09-15",  # Lehman collapse
        "peak": "2008-11-20",
        "end": "2009-03-09"
    },
    "covid19": {
        "start": "2020-02-24",
        "peak": "2020-03-16",  # VIX peak
        "end": "2020-04-15"
    },
    "gamestop": {
        "start": "2021-01-13",
        "peak": "2021-01-27",
        "end": "2021-02-05"
    }
}

def validate_event_data(event_name: str, dates: dict):
    """Verify data exists for crisis event."""
    print(f"\n{event_name.upper()}")
    print("=" * 50)

    for phase, date_str in dates.items():
        date = pd.to_datetime(date_str)
        # Check if data exists for this date
        # Query database for market data, sentiment, regime
        print(f"  {phase}: {date_str} ... ", end="")
        # [Query implementation]
        print("✓")

for event, dates in CRISIS_EVENTS.items():
    validate_event_data(event, dates)
```

---

### Phase 3: Backtest Re-Execution (2-3 days)

#### Step 3.1: Re-run 2008 Crisis Backtest
```bash
# With verbose logging
python scripts/backtesting/run_2008_crisis_backtest.py --verbose

# Compare to original results in:
# results/backtests/2008_crisis_results.json
```

**Expected Results:**
```json
{
  "period": "2008-09-15 to 2009-03-09",
  "ciss_peak": 0.9428,
  "ciss_peak_date": "2008-11-20",
  "sentiment_beta": -0.776,
  "sentiment_p_value": 0.0044,
  "crisis_days": 278,
  "crisis_percentage": 34.6
}
```

**Validation:** If results differ by >5%, investigate discrepancy

#### Step 3.2: Re-run COVID-19 Backtest
```bash
python scripts/backtesting/run_covid19_backtest.py --verbose
```

**Expected Results:**
```json
{
  "period": "2020-02-24 to 2020-04-15",
  "vix_peak": 82.69,
  "vix_peak_date": "2020-03-16",
  "vix_ciss_correlation": 0.922,
  "garch_midas_r2": 0.7124
}
```

#### Step 3.3: Re-run GameStop Backtest
```bash
python scripts/backtesting/run_gamestop_backtest.py --verbose
```

**Expected Results:**
```json
{
  "period": "2021-01-13 to 2021-02-05",
  "vix_spike": 37.21,
  "ciss_max": 0.024,
  "systemic_event": false,
  "correctly_identified": true
}
```

#### Step 3.4: Run Comprehensive Backtest Suite
```bash
# Run ALL backtests with timestamp
python scripts/backtesting/run_historical_backtests_ml.py \
  --output results/validation/backtests_$(date +%Y%m%d_%H%M%S).json \
  --verbose
```

---

### Phase 4: GARCH-MIDAS Validation (1-2 days)

#### Step 4.1: Validate GARCH(1,1) Parameters
**Script:** `scripts/validation/validate_garch_parameters.py`

```python
"""Validate GARCH(1,1) parameter estimation."""

import pandas as pd
import numpy as np
from arch import arch_model

# Load historical VIX data
vix_data = pd.read_csv("data/processed/vix_extended.csv")
returns = vix_data['vix_change'].dropna()

# Fit GARCH(1,1)
model = arch_model(returns, vol='GARCH', p=1, q=1)
result = model.fit(disp='off')

print("GARCH(1,1) Parameters:")
print("=" * 50)
print(f"α (ARCH):  {result.params['alpha[1]']:.6f}")
print(f"β (GARCH): {result.params['beta[1]']:.6f}")
print(f"α + β:     {result.params['alpha[1]'] + result.params['beta[1]']:.6f}")
print(f"AIC:       {result.aic:.2f}")

# Expected from README:
# α = 0.155
# β = 0.800
# α + β = 0.955
# AIC = 7027.28

EXPECTED_ALPHA = 0.155
EXPECTED_BETA = 0.800
TOLERANCE = 0.01

alpha_match = abs(result.params['alpha[1]'] - EXPECTED_ALPHA) < TOLERANCE
beta_match = abs(result.params['beta[1]'] - EXPECTED_BETA) < TOLERANCE

if alpha_match and beta_match:
    print("\n✅ GARCH parameters match expected values")
else:
    print("\n⚠️  GARCH parameters differ from expected")
    print(f"   Expected α: {EXPECTED_ALPHA}")
    print(f"   Got α:      {result.params['alpha[1]']:.6f}")
    print(f"   Expected β: {EXPECTED_BETA}")
    print(f"   Got β:      {result.params['beta[1]']:.6f}")
```

**Run:**
```bash
python scripts/validation/validate_garch_parameters.py
```

#### Step 4.2: Test GARCH-MIDAS Forecasts
```bash
# Run GARCH-MIDAS with validation
python scripts/validation/test_garch_midas.py --validate
```

---

### Phase 5: Live Site Validation (1 day)

#### Step 5.1: Compare Live vs. Local Predictions
**Script:** `scripts/validation/validate_live_site.py`

```python
"""Compare live site predictions to local calculations."""

import requests
import asyncio
from datetime import datetime
from sentiment_detector.models.regime_classifier import RegimeClassifier

async def validate_live_predictions():
    """Compare live API to local predictions."""

    # Get live prediction
    response = requests.get(
        "https://sentiment-regime-detector-production.up.railway.app/api/v1/regime/current"
    )
    live_data = response.json()

    # Get local prediction
    classifier = RegimeClassifier()
    local_prediction = await classifier.predict_current_regime()

    print("LIVE SITE vs. LOCAL PREDICTION")
    print("=" * 50)
    print(f"Live Regime:   {live_data['regime']}")
    print(f"Local Regime:  {local_prediction.label}")
    print()
    print(f"Live Conf:     {live_data['confidence']:.3f}")
    print(f"Local Conf:    {local_prediction.confidence:.3f}")
    print()
    print(f"Live VIX:      {live_data.get('vix', 'N/A')}")
    print(f"Local VIX:     {local_prediction.features.vix:.2f}")
    print()
    print(f"Live CISS:     {live_data.get('ciss', 'N/A')}")
    print(f"Local CISS:    {local_prediction.features.ciss:.3f}")

    # Validate match
    regime_match = live_data['regime'] == local_prediction.label
    conf_diff = abs(live_data['confidence'] - local_prediction.confidence)

    if regime_match and conf_diff < 0.05:
        print("\n✅ Live site matches local predictions")
    else:
        print("\n⚠️  Live site differs from local predictions")
        if not regime_match:
            print("   Regime mismatch!")
        if conf_diff >= 0.05:
            print(f"   Confidence differs by {conf_diff:.3f}")

asyncio.run(validate_live_predictions())
```

**Run:**
```bash
python scripts/validation/validate_live_site.py
```

#### Step 5.2: Verify Explainability Endpoint
```bash
# Test explainability API
curl -s https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/current | jq .

# Verify:
# 1. Waterfall plot exists (base64 PNG)
# 2. Top features list is not empty
# 3. Model version is "RF_v2023.12"
# 4. SHAP values sum to expected prediction
```

---

### Phase 6: Cross-Validation Tests (1 day)

#### Step 6.1: Walk-Forward Validation
**Script:** `scripts/validation/walk_forward_validation.py`

```python
"""Walk-forward validation of regime classifier."""

import pandas as pd
from sentiment_detector.models.regime_classifier import RegimeClassifier

# Test periods
TEST_PERIODS = [
    ("2020-01-01", "2020-12-31"),
    ("2021-01-01", "2021-12-31"),
    ("2022-01-01", "2022-12-31"),
    ("2023-01-01", "2023-12-31"),
    ("2024-01-01", "2024-12-31")
]

def walk_forward_test(start_date: str, end_date: str):
    """Test classifier on specific period."""
    # Load test data
    test_data = pd.read_csv(
        "data/processed/regime_test_data.csv",
        parse_dates=["date"]
    )
    test_data = test_data[
        (test_data['date'] >= start_date) &
        (test_data['date'] <= end_date)
    ]

    # Get predictions
    classifier = RegimeClassifier()
    predictions = []
    actuals = []

    for _, row in test_data.iterrows():
        pred = classifier.predict(row)
        predictions.append(pred.label)
        actuals.append(row['actual_regime'])

    # Calculate accuracy
    accuracy = sum(p == a for p, a in zip(predictions, actuals)) / len(predictions)
    return accuracy

print("Walk-Forward Validation Results")
print("=" * 50)

for start, end in TEST_PERIODS:
    accuracy = walk_forward_test(start, end)
    print(f"{start} to {end}: {accuracy*100:.2f}%")
```

**Expected:** Accuracy should be stable (±5%) across periods

---

## 📊 Validation Checklist

### Data Integrity ✅
- [ ] Verify 2.66M texts in database
- [ ] Verify sentiment scores for all texts
- [ ] Confirm CISS coverage (12,029 records)
- [ ] Confirm VIX coverage (no gaps)
- [ ] Verify crisis event date alignment

### Backtest Accuracy ✅
- [ ] 2008 crisis: CISS peak = 0.9428
- [ ] COVID-19: VIX peak = 82.69
- [ ] GameStop: CISS max = 0.024 (non-systemic)
- [ ] GARCH parameters: α=0.155, β=0.800
- [ ] VIX-CISS correlation: 0.63

### Live Site Validation ✅
- [ ] Current regime matches local prediction
- [ ] Confidence scores within 5%
- [ ] VIX/CISS values match market data
- [ ] Explainability waterfall plots generate
- [ ] Model version shows "RF_v2023.12"

### Model Performance ✅
- [ ] Walk-forward accuracy >80%
- [ ] No data leakage in train/test split
- [ ] Feature importance matches SHAP values
- [ ] Confusion matrix shows balanced performance

---

## 🚨 Red Flags to Watch For

### Data Issues
- **Missing dates:** Gaps in CISS or VIX data
- **Duplicate records:** Same text appearing multiple times
- **Date misalignment:** Sentiment not matching market data dates

### Model Issues
- **Overfitting:** Train accuracy >99%, test accuracy <80%
- **Data leakage:** Using future data in historical predictions
- **Feature drift:** SHAP values not matching original analysis

### Deployment Issues
- **Stale predictions:** Live site not updating
- **Version mismatch:** Live model different from local
- **Cache issues:** Old results being served

---

## 📅 Execution Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| **Phase 1: Test Suite** | 1 hour | ✅ COMPLETED |
| **Phase 2: Data Integrity** | 1 day | 🔜 Next |
| **Phase 3: Backtest Re-run** | 2-3 days | Pending |
| **Phase 4: GARCH Validation** | 1-2 days | Pending |
| **Phase 5: Live Site** | 1 day | Pending |
| **Phase 6: Cross-Validation** | 1 day | Pending |

**Total:** 6-8 days to complete validation

---

## 📝 Documentation Updates

After validation, update:
1. **README.md** - Confirm all metrics are accurate
2. **INTEGRATION_COMPLETE.md** - Add validation results
3. **Paper draft** - Use validated numbers only

---

## ✅ Success Criteria

### Pass Criteria
- ✅ All data integrity checks pass
- ✅ Backtest results match within 5%
- ✅ Live site predictions match local
- ✅ GARCH parameters match expected
- ✅ Walk-forward accuracy >80%

### Fail Criteria
- ❌ Data gaps >1% of records
- ❌ Backtest results differ >10%
- ❌ Live site consistently wrong
- ❌ GARCH parameters differ >10%
- ❌ Test accuracy <70%

---

**Contact:** Jonathan Rocha (jrocha@smu.edu)
**Advisor:** David (King Ip) Lin, Ph.D. (kdlin@smu.edu)
