# Methods & Results Audit

Audit date: 2026-02-15 (UTC)

## Scope
- Methodology claims vs implemented code.
- Validity and reproducibility of artifacts under `results/`.
- Documentation claims tied to measurable outputs.

## Executive Summary
The project has a functioning end-to-end regime pipeline, but several results artifacts were previously conflicting or weakly evidenced. The active results path has now been normalized to a single canonical run (`2026-02-11`) and conflicting/fallback outputs were archived. Core methodology is partially implemented (GARCH(1,1) + jump model + proxy connectedness), while full asymmetric GARCH-MIDAS and full walk-forward validation remain planned work.

## Findings (Prioritized)
1. High: Previous `results/` state had conflicting active outputs.
- Two different pipeline runs were simultaneously active under `results/pipeline_output/` and `results/pipeline_output/pipeline_output/`, with different transition counts.

2. High: One GARCH results file used fallback/default quality metrics.
- `results/garch_midas_results_20260213.json` had zeroed fit stats (`aic/bic/loglikelihood = 0`), indicating non-estimated fallback output quality.

3. High: Methodology wording in draft abstract overstated implementation status.
- Draft text described asymmetric GARCH-MIDAS + walk-forward validation as completed, while current executable pipeline uses GARCH(1,1), proxy TE/TCI features, and event matching.

4. Medium: H1 spike metric logic allowed overcounting.
- `_vix_spike_prediction` could count multiple sentiment drops toward one VIX spike, which could push hit-rate beyond 1.0.

5. Medium: Tooling still referenced deprecated nested parquet path.
- Several scripts defaulted to `results/sentiment_processed/sentiment_processed`.

## Methodology Alignment Matrix
| Area | Draft/Claimed | Implemented (Current) | Status |
|---|---|---|---|
| Volatility layer | Asymmetric GARCH-MIDAS | GARCH(1,1) in `scripts/hpc/run_analysis.py`; separate GARCH-MIDAS artifacts/scripts exist | Partial |
| Regime layer | Statistical Jump Model with jump penalty | Implemented jump-model dynamic programming (`scripts/hpc/run_analysis.py`) | Implemented |
| Connectedness / entropy | Entropy-based connectedness + TE divergence | Proxy features via rolling correlations and derived dispersion metrics | Partial |
| H1/H2/H3 statistical validation | Walk-forward + formal hypothesis testing | Validation modules exist in `src/sentiment_detector/validation/`; full reproducible run output not yet archived as canonical report | Partial |
| Walk-forward backtest | Completed in narrative | Framework exists (`walk_forward_backtest.py`), but canonical results not yet stored in `results/` | Pending evidence |

## Results Folder Validity (Post-Cleanup)
| Artifact | Status | Notes |
|---|---|---|
| `results/pipeline_output/*` | Canonical/Provisional | Promoted to single coherent run (2026-02-11) with fitted GARCH parameters. |
| `results/garch_midas_results_20260211.json` | Usable | Non-zero fit statistics and full payload. |
| `results/_archive/fallback_pipeline_output_20260212/*` | Archived | Fallback run with `arch not available` note; retained for traceability. |
| `results/_archive/invalid_garch/garch_midas_results_20260213.json` | Archived invalid | Fallback-quality file (zero fit statistics). |
| `results/sentiment_processed/*` | Not yet trusted | Parquet read failures observed in this environment; needs regeneration/verification. |

## Remediation Completed in This Pass
- Normalized active pipeline outputs to one canonical run in `results/pipeline_output/`.
- Archived fallback and conflicting outputs under `results/_archive/`.
- Removed duplicate nested output tree `results/sentiment_processed/sentiment_processed`.
- Added machine-readable manifest: `results/results_manifest.json`.
- Added tracked machine-readable manifest: `docs/RESULTS_MANIFEST.json`.
- Added contract doc: `docs/RESULTS_CONTRACT.md`.
- Fixed H1 spike overcounting bug and added regression tests.
- Updated script defaults to top-level scored parquet directory.

## Draft-1.x Wording Guidance
Use wording that reflects current implementation status:
- “Current implementation uses a two-stage pipeline with GARCH(1,1) volatility features and a statistical jump model over engineered sentiment/market features.”
- “Entropy-connectedness and transfer-entropy mechanisms are currently represented by proxy features; full asymmetric GARCH-MIDAS and full walk-forward validation remain planned extensions.”
