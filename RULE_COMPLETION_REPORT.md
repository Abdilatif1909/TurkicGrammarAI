# Rule Completion Report

Source error file: `backend/data/reports/uzbek_morphology_errors.json`

Rules updated: `backend/data/morphology/uzbek_rules.json`

## Baseline Comparison

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Coverage | 100.0% | 100.0% | 0.0 pp |
| Top-1 Accuracy | 23.0% | 27.8% | +4.8 pp |
| Top-3 Accuracy | 43.0% | 52.4% | +9.4 pp |
| Any-Match Accuracy | 66.2% | 79.2% | +13.0 pp |
| RULE_MISSING | 117 | 43 | -74 |
| TRUE_ROOT_ERROR | 52 | 61 | +9 |
| SCORING_ERROR | 0 | 0 | 0 |

`TRUE_ROOT_ERROR` increased because several cases that were previously blocked by missing active rules are now analyzable far enough to expose root-boundary problems.

## RULE_MISSING Clusters Before Repair

| Cluster | Missing token refs | Top examples |
| --- | ---: | --- |
| Possessive patterns | 70 | `nimagan`, `lariyor`, `qaingiz`, `ingish`, `diringiz`, `lerning`, `ilari` |
| Case patterns | 30 | `ginda`, `maganden`, `moqdadan`, `roqmoqda` |
| Derivational patterns | 14 | `taish`, `yoruvchi`, `ginalik` |
| Verb patterns | 10 | `iyma`, `ginaadi` |
| Noun patterns | 2 | `ta` |

## Rules Added

The sprint added curated rule entries for high-frequency pruned patterns. These are not marked as `combo`, `base`, `base-v`, `auto`, or `autogen`, so the active rule map no longer prunes them.

| Suffix | Rule type | Covered frequency |
| --- | --- | ---: |
| `nimagan` | `Case-Accusative-NegParticiple` | 6 |
| `lariyor` | `Possessive-3pl-Adjectival` | 5 |
| `yorning` | `Deriv-Adjectival-Genitive` | 5 |
| `taish` | `Verb-Causative-VerbalNoun` | 5 |
| `qaingiz` | `Case-Dative-Possessive-2pl` | 5 |
| `ginda` | `Restrictive-Locative` | 5 |
| `ingish` | `Possessive-2sg-VerbalNoun` | 4 |
| `iyma` | `Adjectival-Negative` | 4 |
| `maganden` | `Verb-NegParticiple-Ablative` | 4 |
| `diringiz` | `Copular-Possessive-2pl` | 4 |
| `lerning` | `Plural-Variant-Genitive` | 4 |
| `ilari` | `Possessive-3sg-Possessive-3pl` | 4 |
| `moqdadan` | `Verb-Progressive-Ablative` | 4 |
| `yoruvchi` | `Deriv-Adjectival-Agent` | 4 |
| `ginaadi` | `Restrictive-PresentFuture` | 4 |
| `dalari` | `Locative-Possessive-3pl` | 4 |
| `maganler` | `Verb-NegParticiple-PluralVariant` | 3 |
| `roqmoqda` | `Comparative-Progressive` | 3 |
| `larimagan` | `Possessive-3pl-NegParticiple` | 3 |
| `ginalik` | `Restrictive-Nominalizer` | 3 |

Total high-frequency token coverage targeted: 83 token references.

## Remaining RULE_MISSING Clusters

After repair, `RULE_MISSING` is concentrated in low-frequency patterns.

| Cluster | Missing token refs | Remaining examples |
| --- | ---: | --- |
| Possessive patterns | 23 | `daing`, `imuvchi`, `yorlari`, `niingiz`, `ingizim`, `ninguvchi`, `ginaing`, `imo'`, `ingizmagan`, `ningda`, `ginaimiz` |
| Case patterns | 14 | `damoqda`, `samoqda`, `ginamagan`, `tamagan`, `o'moqda`, `gamoqda` |
| Derivational patterns | 2 | `chivor` |
| Noun patterns | 2 | `ta` |
| Verb patterns | 2 | `adiuvchi` |

## Benchmark Impact

The target was reached:

- `RULE_MISSING` dropped from `117` to `43`.
- Coverage remained `100.0%`.
- Top-1 improved from `23.0%` to `27.8%`.
- Any-Match improved from `66.2%` to `79.2%`.

Commands run:

```powershell
python backend\manage.py evaluate_uzbek_morphology
python backend\manage.py analyze_uzbek_errors
python backend\manage.py validate_uzbek_morphology
python backend\manage.py test apps.morphology.tests
```

Validation and morphology tests passed.
