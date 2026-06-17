# Old Turkic Morphology Report

## Inventory

- Rules: 5804
- Lemmas: 15086
- Benchmark cases: 1000
- Script: Old Turkic runiform
- Optional transliteration: Latin metadata fields included
- Historical lineage: Proto Turkic -> Old Turkic -> Uyghur -> Uzbek; Proto Turkic -> Old Turkic -> Turkish

## Evaluation

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 90.9% |
| Top3 | 92.9% |
| AnyMatch | 100.0% |
| Average ambiguity | 7.56 |

## Confusion

| Type | Count |
| --- | ---: |
| TOP1_MATCH | 909 |
| VALID_ALTERNATIVE_ANALYSIS | 91 |

## Historical Integration

- Rules and lemmas include `historical_lineage` metadata for Proto Turkic -> Old Turkic -> Uyghur -> Uzbek and Proto Turkic -> Old Turkic -> Turkish paths.
- Lemma entries include `latin_transliteration` for alignment with Latin scholarly forms such as `teŋri`, `kiši`, and `til`.
- Lemma entries include `cognate_set` keys for Cognates Engine integration.
