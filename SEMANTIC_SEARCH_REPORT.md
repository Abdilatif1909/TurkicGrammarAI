# Semantic Search Report

## Index

- record_count: 100000
- languages: {'az': 16800, 'kk': 10296, 'ky': 10213, 'otk': 10132, 'tk': 9817, 'tr': 22477, 'ug': 2237, 'uz': 18028}
- sources: {'words_dataset': 58491, 'lemma_dictionary': 22290, 'cognates': 15948, 'morphology_benchmark:uzbek_lemma_benchmark.json': 873, 'morphology_benchmark:azerbaijani_morphology_benchmark.json': 496, 'morphology_benchmark:turkish_morphology_benchmark.json': 495, 'morphology_benchmark:kazakh_morphology_benchmark.json': 307, 'morphology_benchmark:old_turkic_morphology_benchmark.json': 300, 'morphology_benchmark:turkmen_morphology_benchmark.json': 246, 'morphology_benchmark:uyghur_morphology_benchmark.json': 246, 'morphology_benchmark:kyrgyz_morphology_benchmark.json': 222, 'morphology_benchmark:uzbek_derivational_benchmark.json': 86}
- cognate_groups: 2000
- lineage_forms: 17778

## Evaluation

| Metric | Value |
| --- | ---: |
| Queries | 2000 |
| Recall@1 | 36.25% |
| Recall@5 | 72.95% |
| Recall@10 | 82.3% |
| MRR | 0.529888 |

## Category Metrics

| Category | Queries | Recall@10 |
| --- | ---: | ---: |
| cognate | 550 | 82.36% |
| cross-language | 350 | 54.57% |
| exact | 350 | 100.0% |
| historical | 350 | 100.0% |
| morphological | 400 | 75.5% |

## Search Types

- Exact: direct indexed surface-form match.
- Morphological: shared lemma/root/features from the embedding dataset.
- Cognate: shared universal cognate group.
- Historical: shared historical lineage forms.
- Cross-language: FastText nearest-neighbor candidates plus cognate expansion across languages.

## Readiness

The semantic index and API are operational and support cross-language retrieval over the cognate-aware FastText model.
