# Results Contract

## Purpose
Define one canonical result set for reporting, and keep all non-canonical outputs archived.

## Canonical Active Artifacts
- `results/pipeline_output/pipeline_summary.json`
- `results/pipeline_output/feature_matrix.csv`
- `results/pipeline_output/regime_labels.csv`
- `results/pipeline_output/regime_transitions.csv`
- `results/garch_midas_results_20260211.json`

These files are the only active artifacts to cite in Draft-1.x unless a newer canonical run is explicitly promoted.

## Archived / Non-Canonical Artifacts
- `results/_archive/fallback_pipeline_output_20260212/*`
- `results/_archive/invalid_garch/garch_midas_results_20260213.json`

Archived artifacts are retained for traceability and must not be cited as final evidence.

## Promotion Rules for New Runs
A new run may replace canonical active artifacts only if all conditions hold:
1. All 4 pipeline files share one run timestamp and are internally consistent:
- `feature_matrix` row count == `regime_labels` row count
- `regime_transitions` row count == `pipeline_summary.jump_model.n_transitions`
2. Fit-quality is explicit:
- If GARCH fallback is used, run is marked `provisional`.
- If fit stats are zero/default placeholders, run is `invalid` and archived.
3. File hashes and quality flags are recorded in `docs/RESULTS_MANIFEST.json`.

## Regeneration Rules
- Never write nested active outputs like `results/pipeline_output/pipeline_output`.
- Never use nested scored parquet path `results/sentiment_processed/sentiment_processed` as default input.
- Archive superseded runs under `results/_archive/<reason>_<yyyymmdd>/`.
- Refresh manifest after promotion: `python scripts/validate_results_manifest.py --manifest docs/RESULTS_MANIFEST.json`.

## Reporting Rules
- Draft narrative must distinguish:
- `implemented`
- `provisional`
- `planned`
- Any metric without canonical artifact support should be labeled target/expected, not achieved.
