# Cross-Language Morphology Report

## Metrics

| Metric | Value |
| --- | ---: |
| Cases | 1000 |
| Aligned groups | 125 |
| Feature accuracy | 100.0% |
| Partial feature accuracy | 100.0% |
| Equivalence accuracy | 100.0% |

## Universal Features

The evaluator normalizes language-specific suffix chains into shared features such as `PLURAL`, `POSS_1PL`, `ABLATIVE`, `DATIVE`, `PAST`, `NEGATIVE`, and `DERIVATIONAL`.

## Readiness

- Universal morphology output is suitable as input to cross-language cognate alignment.
- The benchmark aligns eight supported languages: `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, `otk`.
- Remaining failures are saved in `backend/data/reports/cross_language_morphology_statistics.json`.
