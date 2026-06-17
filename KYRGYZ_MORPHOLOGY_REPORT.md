# Kyrgyz Morphology Report

## Inventory

- Rules: 1840
- Lemmas: 12050
- Benchmark cases: 500
- Script: Cyrillic

## Evaluation

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 100.0% |
| Top3 | 100.0% |
| AnyMatch | 100.0% |
| Average ambiguity | 5.03 |

## Confusion

| Type | Count |
| --- | ---: |
| TOP1_MATCH | 500 |

## Vowel Harmony

- Kyrgyz Cyrillic four-way vowel harmony is enforced for productive suffixes.
- Examples: `китептерибизден`, `үйлөрүбүздөн`, and `адамдар` are valid analyses.
- Invalid direct analysis such as `үй + лар` is rejected for `үйлар`.
