# Turkic RAG Retrieval Report

## Retrieval Layer

- Sources: semantic search, cognate groups, historical lineage, morphology metadata, words dataset.
- Ranking: final relevance score = semantic_score + cognate_score + historical_score + morphology_score + dictionary_score.
- API: `GET /api/rag/retrieve/?q=tangri`

## Index Coverage

- record_count: 100000
- languages: {'az': 16800, 'kk': 10296, 'ky': 10213, 'otk': 10132, 'tk': 9817, 'tr': 22477, 'ug': 2237, 'uz': 18028}
- sources: {'words_dataset': 58491, 'lemma_dictionary': 22290, 'cognates': 15948, 'morphology_benchmark:uzbek_lemma_benchmark.json': 873, 'morphology_benchmark:azerbaijani_morphology_benchmark.json': 496, 'morphology_benchmark:turkish_morphology_benchmark.json': 495, 'morphology_benchmark:kazakh_morphology_benchmark.json': 307, 'morphology_benchmark:old_turkic_morphology_benchmark.json': 300, 'morphology_benchmark:turkmen_morphology_benchmark.json': 246, 'morphology_benchmark:uyghur_morphology_benchmark.json': 246, 'morphology_benchmark:kyrgyz_morphology_benchmark.json': 222, 'morphology_benchmark:uzbek_derivational_benchmark.json': 86}
- cognate_groups: 2000
- lineage_forms: 17778

## Evaluation

| Metric | Value |
| --- | ---: |
| Queries | 1000 |
| Recall@1 | 27.0% |
| Recall@5 | 65.9% |
| Recall@10 | 84.3% |
| MRR | 0.455756 |
| Average retrieval latency | 53.173 ms |

## Category Metrics

| Category | Queries | Recall@10 |
| --- | ---: | ---: |
| cognate | 250 | 90.0% |
| cross_language | 250 | 77.2% |
| historical | 250 | 100.0% |
| morphology | 250 | 70.0% |

## Source Contribution Analysis

| Source | Results | Top-1 Results | Successful Hits |
| --- | ---: | ---: | ---: |
| cognate | 7247 | 1000 | 675 |
| dictionary | 17794 | 0 | 798 |
| historical | 9000 | 0 | 675 |
| morphology | 17495 | 0 | 915 |
| semantic | 16726 | 0 | 915 |

## Top Successful Cases

- tangri (cognate): matched `tanrı` at rank 2.
- tanrı (cognate): matched `taňry` at rank 3.
- kitob (cognate): matched `kitab` at rank 2.
- kitap (cognate): matched `kitab` at rank 4.
- uy (cognate): matched `үй` at rank 2.
- ev (cognate): matched `ئۆي` at rank 3.
- kishi (cognate): matched `كىشى` at rank 2.
- kişi (cognate): matched `كىشى` at rank 4.
- ota (cognate): matched `ata` at rank 2.
- ata (cognate): matched `ota` at rank 4.

## Top Failed Cases

- til (cognate): expected ['dil', 'тіл', 'тил', 'تىل', '𐱅𐰃𐰠'], returned ['til', 'til', 'tiltil', 'tilči', 'tiluŋ'].
- dil (cognate): expected ['til', 'тіл', 'тил', 'تىل', '𐱅𐰃𐰠'], returned ['dil', 'dil', 'dil', 'bul', 'үйчи'].
- məktəb (cognate): expected ['okul', 'кітапші', 'китепчи', 'kitapçi', 'كىتابچىلىق'], returned ['məktəb', 'məktəbi', 'məktəbu', 'məktəbü', 'məktəba'].
- göz (cognate): expected ['yurak', 'кітапді', 'китеплүк', 'kitapli', 'كىتابداش'], returned ['göz', 'göz', 'göz', 'gözı', 'gözı'].
- maktab (cognate): expected ['masa', 'кітаплі', 'китепсиз', 'kitapsiz', 'ئۆيچى'], returned ['maktab', 'maktabi', 'maktabmaktabni', 'maktabmaktabga', 'maktabmaktabda'].
- iş (cognate): expected ["ta'limchi", 'үйлық', 'үйчы', 'öýlik', 'ئادەم'], returned ['iş', 'iş', 'iş', 'işçy', 'işü'].
- gün (cognate): expected ['uyqu', 'үйді', 'үйлик', 'öýsyz', 'ئادەملىق'], returned ['gün', 'gün', 'gün', 'günı', 'günı'].
- öğrenci (cognate): expected ['ot', 'tələbə', 'адам', 'үйсуз', 'adamçi'], returned ['öğrenci', 'öğrenciün', 'öğrenciü', 'öğrenciın', 'öğrenciüm'].
- öğretmen (cognate): expected ['yosh', 'müllim', 'адамшы', 'үйсүз', 'adamlyk'], returned ['öğretmen', 'öğretmenü', 'öğretmenün', 'öğretmenı', 'öğretmencı'].
- arkadaş (cognate): expected ['ism', 'dost', 'адамлік', 'адам', 'adamli'], returned ['arkadaş', 'arkadaşü', 'arkadaşı', 'arkadaşüm', 'arkadaşde'].

## Output Schema

Each retrieved document returns lemma, word, root, language, cognate group, historical lineage, similarity, source_type, source_id, confidence, component scores, final_relevance_score, and source_trace.

## Readiness

The retriever is operational and `qa_ready_check.json` confirms the semantic, cognate, historical, morphology, and traceability connections.
