# Kazakh Morphology Report

## Inventory

- Rules: 2045
- Lemmas: 12050
- Benchmark cases: 500
- Script: Cyrillic

## Evaluation

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 99.8% |
| Top3 | 99.8% |
| AnyMatch | 100.0% |
| Average ambiguity | 8.4 |

## Confusion

| Type | Count |
| --- | ---: |
| TOP1_MATCH | 499 |
| VALID_ALTERNATIVE_ANALYSIS | 1 |

## Vowel Harmony

- Kazakh Cyrillic major vowel harmony is enforced for productive suffixes.
- Examples: `кітаптар`, `үйлер`, and `үйлерімізден` are valid analyses.
- Invalid direct analysis such as `үй + лар` is rejected for `үйлар`.
