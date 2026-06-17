# Multi-Analysis Evaluation Report

## Evaluation Alignment

Evaluation now matches the multi-analysis analyzer design:

- A case is correct if any returned analysis matches the expected analysis.
- Top-1, Top-3, and Any-Match are reported separately.
- Valid lower-ranked analyses are counted as `VALID_ALTERNATIVE_ANALYSIS`, not as root or scoring errors.
- `TRUE_ROOT_ERROR` is separated from valid alternatives.

## Morphology Benchmark

Source: `backend/data/benchmark/uzbek_morphology.json`

| Metric | Count | Percent |
| ------ | ----: | ------: |
| Coverage | 500 / 500 | 100.0% |
| Top-1 Accuracy | 115 / 500 | 23.0% |
| Top-3 Accuracy | 215 / 500 | 43.0% |
| Any-Match Accuracy | 331 / 500 | 66.2% |

Recalculated confusion:

| Type | Count |
| ---- | ----: |
| TOP1_MATCH | 115 |
| VALID_ALTERNATIVE_ANALYSIS | 216 |
| RULE_MISSING | 117 |
| TRUE_ROOT_ERROR | 52 |
| SCORING_ERROR | 0 |

Corrected baseline:

- `ROOT_ERROR` is now represented as `TRUE_ROOT_ERROR = 52`.
- `RULE_MISSING = 117`.
- `SCORING_ERROR = 0` after recognizing valid alternative analyses.
- `VALID_ALTERNATIVE_ANALYSIS = 216`.

## Derivational Benchmark

Source: `backend/data/benchmark/uzbek_derivational_benchmark.json`

| Metric | Count | Percent |
| ------ | ----: | ------: |
| Coverage | 500 / 500 | 100.0% |
| Top-1 Accuracy | 323 / 500 | 64.6% |
| Top-3 Accuracy | 500 / 500 | 100.0% |
| Any-Match Accuracy | 500 / 500 | 100.0% |
| Root Any-Match | 500 / 500 | 100.0% |

Derivational confusion:

| Type | Count |
| ---- | ----: |
| TOP1_MATCH | 323 |
| VALID_ALTERNATIVE_ANALYSIS | 177 |

## Generated Artifacts

- `backend/data/reports/uzbek_morphology_statistics.json`
- `backend/data/reports/uzbek_derivational_statistics.json`
- `backend/data/reports/uzbek_morphology_errors.json`
- `backend/data/reports/uzbek_morphology_confusion.json`
- `backend/data/reports/UZBEK_MORPHOLOGY_EVALUATION.md`
- `backend/data/reports/DERIVATIONAL_MORPHOLOGY_REPORT.md`
- `backend/data/reports/UZBEK_MORPHOLOGY_ERROR_REPORT.md`

## New Baseline

The new baseline should use Any-Match Accuracy as the primary coverage-oriented measure and Top-1 Accuracy as the ranking/scoring measure.

Scoring optimization should now target the 216 morphology `VALID_ALTERNATIVE_ANALYSIS` cases and the 177 derivational `VALID_ALTERNATIVE_ANALYSIS` cases without treating them as missing rules or root failures.
