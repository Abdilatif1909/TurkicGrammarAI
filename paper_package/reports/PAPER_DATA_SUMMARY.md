# Paper Data Summary

Paper: Cognate-Aware Multilingual Embeddings for Turkic Languages Using Morphological and Historical Linguistic Knowledge

## Extraction Scope

This package was generated from existing repository artifacts only. No algorithms, datasets, trained models, or evaluation results were modified.

## Primary Sources

- `backend/data/embeddings/embedding_dataset.jsonl`
- `backend/data/reports/embedding_quality_statistics.json`
- `backend/data/reports/fasttext_training_stats.json`
- `backend/data/reports/semantic_search_statistics.json`
- `backend/data/reports/rag_retrieval_statistics.json`
- `backend/data/reports/qa_statistics.json`
- `backend/data/reports/cognate_alignment_statistics.json`
- Morphology reports under `backend/data/reports/*morphology*statistics.json`

## Dataset Summary

- Embedding records: 100000
- Languages represented: 8
- Unique surface forms: 88712
- Unique lemmas: 26797
- Unique roots: 26798
- Records with cognate groups: 23018
- Unique cognate groups: 2000
- Records with historical lineage: 25018

## Source Distribution

- words_dataset: 70170
- cognates: 15948
- lemma_dictionary: 8611
- historical_forms: 2000
- morphology_benchmark:uzbek_lemma_benchmark.json: 873
- morphology_benchmark:azerbaijani_morphology_benchmark.json: 496
- morphology_benchmark:turkish_morphology_benchmark.json: 495
- morphology_benchmark:kazakh_morphology_benchmark.json: 307
- morphology_benchmark:old_turkic_morphology_benchmark.json: 300
- morphology_benchmark:turkmen_morphology_benchmark.json: 246
- morphology_benchmark:uyghur_morphology_benchmark.json: 246
- morphology_benchmark:kyrgyz_morphology_benchmark.json: 222
- morphology_benchmark:uzbek_derivational_benchmark.json: 86

## Embedding Benchmark Summary

- Benchmark pairs: 5000
- Positive pairs: 4297
- Negative pairs: 703
- Vocabulary size: 143011
- Top-1: 40.8%
- Top-5: 73.66%
- Top-10: 86.06%
- Mean cosine similarity: 0.577844
- Positive pair similarity: 0.595108
- Negative pair similarity: 0.472318
- Separation margin: 0.12279

## Benchmark Categories

- cognates: 1790
- cross_language_equivalents: 702
- morphological_variants: 553
- historical_relations: 1252
- negative_pairs: 703

## Cluster Metrics

- cognate_clusters: intra=None, inter=None, separation=-0.063336
- language_family_clusters: intra=None, inter=None, separation=-0.054709
- morphological_clusters: intra=None, inter=None, separation=0.156166

## Downstream Evaluation Summary

- Semantic search: Recall@10=82.3%, MRR=0.529888
- RAG retrieval: Recall@10=84.3%, MRR=0.455756, average latency=53.173 ms
- QA: answer accuracy=83.8%, source accuracy=99.7%
- Cognate alignment: accuracy=100.0%, coverage=100.0%

## Baseline Status

The repository artifacts used for this package do not contain a separate baseline embedding evaluation. Table 4 therefore reports baseline and improvement as unavailable rather than inventing comparison values.
