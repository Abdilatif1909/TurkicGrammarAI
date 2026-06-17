# Result Classification

## Classification Table

| Result | Value | Class | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| Uzbek (uz) records | 18314 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Uzbek (uz) lemmas | 5465 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Uzbek (uz) roots | 5466 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkish (tr) records | 15798 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkish (tr) lemmas | 4366 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkish (tr) roots | 4366 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Azerbaijani (az) records | 10372 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Azerbaijani (az) lemmas | 2824 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Azerbaijani (az) roots | 2824 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kazakh (kk) records | 10582 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kazakh (kk) lemmas | 2580 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kazakh (kk) roots | 2580 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kyrgyz (ky) records | 10499 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kyrgyz (ky) lemmas | 2548 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Kyrgyz (ky) roots | 2548 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkmen (tk) records | 10102 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkmen (tk) lemmas | 2577 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Turkmen (tk) roots | 2577 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Uyghur (ug) records | 13916 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Uyghur (ug) lemmas | 4324 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Uyghur (ug) roots | 4324 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Old Turkic (otk) records | 10417 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Old Turkic (otk) lemmas | 2534 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Old Turkic (otk) roots | 2534 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Embedding dataset records | 100000 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Languages represented | 8 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Unique surface forms | 88712 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Unique lemmas | 26797 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Unique roots | 26798 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Records with morphology features | 75429 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Records with cognate group | 23018 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Unique cognate groups | 2000 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Records with historical lineage | 25018 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| Historical lineage entries | 215162 | Measured | backend/data/embeddings/embedding_dataset.jsonl | High |
| vector_size | 300 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| window | 5 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| min_count | 1 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| epochs | 20 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| workers | 12 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| vocabulary_size | 143011 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| training_time_seconds | 172.217 | Measured | backend/data/reports/fasttext_training_stats.json | High |
| corpus_path | backend\data\embeddings\fasttext_corpus.txt | Measured | backend/data/reports/fasttext_training_stats.json | High |
| model_path | backend\models\turkic_fasttext.model | Measured | backend/data/reports/fasttext_training_stats.json | High |
| vector_path | backend\models\turkic_fasttext.vec | Measured | backend/data/reports/fasttext_training_stats.json | High |
| Top-1 accuracy (%) | 40.8 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Top-5 accuracy (%) | 73.66 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Top-10 accuracy (%) | 86.06 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Mean cosine similarity | 0.577844 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Positive pair similarity | 0.595108 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Negative pair similarity | 0.472318 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Separation margin | 0.12279 | Measured | backend/data/reports/embedding_quality_statistics.json | High |
| Semantic Recall@1 | 36.25 | Measured | backend/data/reports/semantic_search_statistics.json | High |
| Semantic Recall@5 | 72.95 | Measured | backend/data/reports/semantic_search_statistics.json | High |
| Semantic Recall@10 | 82.3 | Measured | backend/data/reports/semantic_search_statistics.json | High |
| Semantic MRR | 0.529888 | Measured | backend/data/reports/semantic_search_statistics.json | High |
| RAG Recall@1 | 27.0 | Measured | backend/data/reports/rag_retrieval_statistics.json | High |
| RAG Recall@5 | 65.9 | Measured | backend/data/reports/rag_retrieval_statistics.json | High |
| RAG Recall@10 | 84.3 | Measured | backend/data/reports/rag_retrieval_statistics.json | High |
| RAG MRR | 0.455756 | Measured | backend/data/reports/rag_retrieval_statistics.json | High |
| Average retrieval latency ms | 53.173 | Measured | backend/data/reports/rag_retrieval_statistics.json | High |
| QA answer accuracy | 83.8 | Measured | backend/data/reports/qa_statistics.json | High |
| QA source accuracy | 99.7 | Measured | backend/data/reports/qa_statistics.json | High |
| QA top-k support coverage | 83.8 | Measured | backend/data/reports/qa_statistics.json | High |
| Cognate alignment accuracy | 100.0 | Measured | backend/data/reports/cognate_alignment_statistics.json | High |
| Cognate coverage | 100.0 | Measured | backend/data/reports/cognate_alignment_statistics.json | High |
| Cognate total cases | 2000 | Measured | backend/data/reports/cognate_alignment_statistics.json | High |
| Embedding Top-1 Wilson 95% CI | 39.45% - 42.17% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| Embedding Top-5 Wilson 95% CI | 72.42% - 74.86% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| Embedding Top-10 Wilson 95% CI | 85.07% - 86.99% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| Semantic Recall@1 Wilson 95% CI | 34.17% - 38.38% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| Semantic Recall@5 Wilson 95% CI | 70.96% - 74.85% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| Semantic Recall@10 Wilson 95% CI | 80.57% - 83.91% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| RAG Recall@1 Wilson 95% CI | 24.34% - 29.84% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| RAG Recall@5 Wilson 95% CI | 62.91% - 68.77% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| RAG Recall@10 Wilson 95% CI | 81.91% - 86.42% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| QA Answer Accuracy Wilson 95% CI | 81.39% - 85.95% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| QA Source Accuracy Wilson 95% CI | 99.12% - 99.90% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| QA Support Coverage Wilson 95% CI | 81.39% - 85.95% | Derived | paper_package/tables/table5_confidence_intervals.csv | Medium |
| ROOT proxy contribution | availability=75429; successful_hits=915 | Estimated | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Medium |
| COGNATE proxy contribution | availability=23018; successful_hits=675 | Estimated | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Medium |
| LINEAGE proxy contribution | availability=25018; successful_hits=675 | Estimated | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Medium |
| LANGUAGE proxy contribution | availability=100000; successful_hits=798 | Estimated | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Medium |
| Semantic Recall@10 categories distribution | mean=82.49, min=54.57, max=100.00, sd=16.98 | Derived | backend/data/reports/*_statistics.json | Medium |
| RAG Recall@10 categories distribution | mean=84.30, min=70.00, max=100.00, sd=11.55 | Derived | backend/data/reports/*_statistics.json | Medium |
| QA answer accuracy categories distribution | mean=83.80, min=68.80, max=100.00, sd=11.83 | Derived | backend/data/reports/*_statistics.json | Medium |
| Effect of removing ROOT features | Not measured | Hypothesized | paper_package/analysis/ABLATION_STUDY.md | Low |
| Effect of removing COGNATE features | Not measured | Hypothesized | paper_package/analysis/ABLATION_STUDY.md | Low |
| Effect of removing LINEAGE features | Not measured | Hypothesized | paper_package/analysis/ABLATION_STUDY.md | Low |
| Effect of removing LANGUAGE markers | Not measured | Hypothesized | paper_package/analysis/ABLATION_STUDY.md | Low |

## Definitions

- Measured: produced by an existing evaluator or direct repository artifact.
- Derived: computed from measured values without changing source data, for example percentages, Wilson intervals, or distribution summaries.
- Estimated: proxy interpretation from existing data, not controlled experimental measurement.
- Hypothesized: forward-looking expectation requiring a future controlled experiment.
