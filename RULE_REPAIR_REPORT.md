# Rule Repair Report

Commands run:

```text
python backend\manage.py evaluate_uzbek_morphology
python backend\manage.py analyze_uzbek_errors
```

Reports refreshed:

- `backend/data/reports/uzbek_morphology_statistics.json`
- `backend/data/reports/uzbek_morphology_errors.json`
- `backend/data/reports/UZBEK_MORPHOLOGY_EVALUATION.md`
- `backend/data/reports/UZBEK_MORPHOLOGY_ERROR_REPORT.md`

## Before vs After

| Metric | Before | After | Change |
| ------ | -----: | ----: | -----: |
| RULE_MISSING | 135 | 117 | -18 |
| ROOT_ERROR | 177 | 186 | +9 |
| SCORING_ERROR | 77 | 82 | +5 |
| Total failures | 389 | 385 | -4 |
| Top-match | 111 / 500 (22.2%) | 115 / 500 (23.0%) | +4 cases |
| Coverage | 500 / 500 (100.0%) | 500 / 500 (100.0%) | no change |
| Rule match rate | 365 / 500 (73.0%) | 383 / 500 (76.6%) | +3.6 pp |
| Average ambiguity | 32.38 | 32.72 | +0.34 |

## Added Rules

| Suffix | Rule type | Priority area |
| ------ | --------- | ------------- |
| `ingizda` | Possessive-2pl-Locative | noun morphology |
| `idan` | Possessive-3sg-Ablative | noun morphology |
| `inggina` | Possessive-2sg-Restrictive | noun morphology |
| `magandi` | Verb-NegPastPart-Past | verb morphology |
| `ishning` | VerbalNoun-Genitive | derivational morphology |
| `ginacha` | Restrictive-Approximation | derivational morphology |

## Result

`RULE_MISSING` was reduced significantly without adding the high-frequency synthetic chains (`nimagan`, `lariyor`, `qaingiz`, `taish`, `moqdadan`, etc.).

Top-match improved from 22.2% to 23.0%. The remaining errors are now more concentrated in root selection and scoring, so the project is ready for scoring optimization after a root-error pass.
