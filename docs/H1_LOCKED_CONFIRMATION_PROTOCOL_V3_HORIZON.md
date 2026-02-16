# H1 Locked Confirmation Protocol V3 (Horizon Extension)

## Purpose
Run one final pre-registered H1 confirmation pass with a widened lead-time confirmation horizon while keeping all other controls fixed.

## Lock Date
February 16, 2026 (UTC)

## Fixed Inputs
- Feature matrix: `results/pipeline_output/feature_matrix.csv`
- Regime labels: `results/pipeline_output/regime_labels.csv`
- Event set: `docs/h1_event_universe_v2.json` (11 events)

## Fixed H1 Configuration
- Sentiment transform: `compound_x_abs_returns`
- Significance level: `alpha = 0.05`
- Max lag days searched: `10`
- VIX spike threshold: `25.0`

## Fixed Confirmation Horizon
- Global and event lag-eligibility horizon: `1..7` days

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
- AND global optimal lag is in `1..7`.
2. Secondary event-conditioned criterion:
- Count events where all are true:
  - H1 verdict is `supported`
  - Optimal lag in `1..7`
  - Granger significance passes Bonferroni
  - Granger significance passes BH-FDR
  - False positive rate `<= 0.25`
3. Confirmation outcome:
- `confirmed` if primary criterion is true OR secondary count `>= 2`.
- Otherwise `not_confirmed`.

## Execution Command
```bash
PYTHONPATH=src python scripts/run_h1_locked_confirmation.py \
  --protocol-id H1_LOCKED_CONFIRMATION_PROTOCOL_V3_HORIZON \
  --events-json docs/h1_event_universe_v2.json \
  --confirm-lag-min 1 \
  --confirm-lag-max 7
```

## Output Artifacts
- `results/validation/h1_confirmation/locked_protocol/h1_locked_confirmation_20260216_022558.json`
- `results/validation/h1_confirmation/locked_protocol/h1_locked_confirmation_20260216_022558.md`
