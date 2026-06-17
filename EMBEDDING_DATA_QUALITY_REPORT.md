# Embedding Data Quality Report

Date: 2026-06-11

Scope: `backend/data/embeddings/embedding_dataset.jsonl`

## Summary

| Metric | Value |
| --- | ---: |
| Total records | 100,000 |
| Duplicate records by `(surface_form, language, lemma, root)` | 6,560 |
| Records missing `features` | 33,555 |
| Records missing `cognate_group` | 76,983 |
| Records missing `historical_lineage` | 76,983 |
| Orphan cognate records | 0 |
| Distinct cognate groups represented | 2,000 |

## Records Per Language

| Language | Records |
| --- | ---: |
| tr | 22,477 |
| uz | 18,028 |
| az | 16,800 |
| kk | 10,296 |
| ky | 10,213 |
| otk | 10,132 |
| tk | 9,817 |
| ug | 2,237 |

## Records Per Source

| Source | Records |
| --- | ---: |
| words_dataset | 58,491 |
| lemma_dictionary | 22,290 |
| cognates | 15,948 |
| morphology_benchmark:uzbek_lemma_benchmark.json | 873 |
| morphology_benchmark:azerbaijani_morphology_benchmark.json | 496 |
| morphology_benchmark:turkish_morphology_benchmark.json | 495 |
| morphology_benchmark:kazakh_morphology_benchmark.json | 307 |
| morphology_benchmark:old_turkic_morphology_benchmark.json | 300 |
| morphology_benchmark:uyghur_morphology_benchmark.json | 246 |
| morphology_benchmark:turkmen_morphology_benchmark.json | 246 |
| morphology_benchmark:kyrgyz_morphology_benchmark.json | 222 |
| morphology_benchmark:uzbek_derivational_benchmark.json | 86 |

## Findings

No orphan cognate records were found: every non-empty `cognate_group` in the embedding dataset is present in `cross_language_cognates.json`.

The remaining quality gap is coverage, not referential integrity. Most records from `words_dataset` and `lemma_dictionary` do not carry cognate or historical lineage metadata. This is acceptable for broad vocabulary coverage, but it limits cognate-aware and historical retrieval quality.

## Required Follow-Up

1. Deduplicate the 6,560 repeated records before the next training run.
2. Backfill morphology features for plain word and lemma records where language-specific analyzers can produce confident analyses.
3. Backfill cognate and historical lineage for words that match existing cognate groups.
4. Keep the current dataset usable for runtime, but do not treat it as fully lineage-complete.
