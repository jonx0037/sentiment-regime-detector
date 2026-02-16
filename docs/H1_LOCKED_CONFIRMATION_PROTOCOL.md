# H1 Locked Confirmation Protocol

## Purpose
Define and execute one fixed, reproducible confirmation analysis for H1 (Leading Indicator) after exploratory remediation.

## Lock Date
February 16, 2026 (UTC)

## Fixed Inputs
- Feature matrix: `results/pipeline_output/feature_matrix.csv`
- Regime labels: `results/pipeline_output/regime_labels.csv`
- Event set: `KEY_MARKET_EVENTS` from `src/sentiment_detector/validation/walk_forward_backtest.py`

## Fixed H1 Configuration
- Sentiment transform: `compound_x_abs_returns`
- Significance level: `alpha = 0.05`
- Max lag days: `10`
- VIX spike threshold: `25.0`

## Event-Conditioned Window Configuration
- Pre-event days: `180`
- Post-event days: `90`
- Minimum observations per event window: `80`

## Multiple-Testing Controls
- Benjamini-Hochberg FDR (`q < 0.05`)
- Bonferroni familywise threshold (`alpha / m`)

## Locked Decision Rule
1. Primary global criterion:
- Global H1 verdict is `supported`
- AND global optimal lag is in `1..5`.
2. Secondary event-conditioned criterion:
- Count events where all are true:
  - H1 verdict is `supported`
  - Optimal lag in `1..5`
  - Granger significance passes Bonferroni
  - Granger significance passes BH-FDR
  - False positive rate `<= 0.25`
3. Confirmation outcome:
- `confirmed` if primary criterion is true OR secondary count `>= 2`.
- Otherwise `not_confirmed`.

## Execution Command
```bash
PYTHONPATH=src python scripts/run_h1_locked_confirmation.py
```

## Output Artifacts
- `results/validation/h1_confirmation/locked_protocol/h1_locked_confirmation_<timestamp>.json`
- `results/validation/h1_confirmation/locked_protocol/h1_locked_confirmation_<timestamp>.md`
