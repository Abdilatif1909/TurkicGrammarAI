# Uyghur Morphology Report

## Inventory

- Rules: 2949
- Lemmas: 12050
- Benchmark cases: 500
- Script: Arabic
- Optional transliteration: Latin metadata fields included
- Historical lineage: Proto Turkic -> Old Turkic -> Uyghur -> Uzbek

## Evaluation

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 99.6% |
| Top3 | 100.0% |
| AnyMatch | 100.0% |
| Average ambiguity | 6.3 |

## Confusion

| Type | Count |
| --- | ---: |
| TOP1_MATCH | 498 |
| VALID_ALTERNATIVE_ANALYSIS | 2 |

## Historical Integration Readiness

- Data files include `historical_lineage` metadata for Proto Turkic -> Old Turkic -> Uyghur -> Uzbek linking.
- Lemma entries include a `latin_transliteration` field for future transliteration alignment.
- Rules are file-backed and language-scoped under `ug` for reuse by Historical Forms services.
