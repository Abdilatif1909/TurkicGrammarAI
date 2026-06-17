# Azerbaijani Morphology Report

## Inventory

- Rules: 564
- Lemmas: 10500
- Benchmark cases: 500

## Evaluation

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 99.8% |
| Top3 | 99.8% |
| AnyMatch | 100.0% |
| Average ambiguity | 5.93 |

## Confusion

| Type | Count |
| --- | ---: |
| TOP1_MATCH | 499 |
| VALID_ALTERNATIVE_ANALYSIS | 1 |

## Vowel Harmony

- Major vowel harmony is enforced for suffixes such as `lar/lər`, `da/də`, and `dan/dən`.
- Minor vowel harmony is enforced for four-way suffixes such as possessive and accusative variants.
- Example: `kitablar` and `evlər` are valid; `evlar` is rejected as a direct `ev + lar` analysis.
