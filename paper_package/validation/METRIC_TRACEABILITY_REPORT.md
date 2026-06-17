# Metric Traceability Report

## Scope

This report traces every metric used in the Phase 37 paper package. It does not rerun training, modify datasets, or alter evaluation results.

## Traceability Table

| Metric | Value | Source File | Evaluation Script | Confidence Level | Generation Process |
| --- | --- | --- | --- | --- | --- |
| Uzbek (uz) records | 18314 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Uzbek (uz) lemmas | 5465 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Uzbek (uz) roots | 5466 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Turkish (tr) records | 15798 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Turkish (tr) lemmas | 4366 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Turkish (tr) roots | 4366 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Azerbaijani (az) records | 10372 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Azerbaijani (az) lemmas | 2824 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Azerbaijani (az) roots | 2824 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Kazakh (kk) records | 10582 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Kazakh (kk) lemmas | 2580 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Kazakh (kk) roots | 2580 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Kyrgyz (ky) records | 10499 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Kyrgyz (ky) lemmas | 2548 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Kyrgyz (ky) roots | 2548 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Turkmen (tk) records | 10102 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Turkmen (tk) lemmas | 2577 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Turkmen (tk) roots | 2577 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Uyghur (ug) records | 13916 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Uyghur (ug) lemmas | 4324 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Uyghur (ug) roots | 4324 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Old Turkic (otk) records | 10417 | backend/data/embeddings/embedding_dataset.jsonl | backend/apps/embeddings/embedding_dataset_builder.py; Phase 37 extraction script | High | Counted from JSONL records grouped by language |
| Old Turkic (otk) lemmas | 2534 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique lemma values grouped by language |
| Old Turkic (otk) roots | 2534 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Unique root values grouped by language |
| Embedding dataset records | 100000 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Languages represented | 8 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Unique surface forms | 88712 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Unique lemmas | 26797 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Unique roots | 26798 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Records with morphology features | 75429 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Records with cognate group | 23018 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script; backend/apps/embeddings/embedding_dataset_builder.py | High | Direct JSONL count or unique set count |
| Unique cognate groups | 2000 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script; backend/apps/embeddings/embedding_dataset_builder.py | High | Direct JSONL count or unique set count |
| Records with historical lineage | 25018 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| Historical lineage entries | 215162 | backend/data/embeddings/embedding_dataset.jsonl | Phase 37 extraction script | High | Direct JSONL count or unique set count |
| vector_size | 300 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| window | 5 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| min_count | 1 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| epochs | 20 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| workers | 12 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| vocabulary_size | 143011 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| training_time_seconds | 172.217 | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| corpus_path | backend\data\embeddings\fasttext_corpus.txt | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| model_path | backend\models\turkic_fasttext.model | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| vector_path | backend\models\turkic_fasttext.vec | backend/data/reports/fasttext_training_stats.json | backend/apps/embeddings/train_fasttext_embeddings.py | High | Stored training configuration/statistics |
| Top-1 accuracy (%) | 40.8 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Top-5 accuracy (%) | 73.66 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Top-10 accuracy (%) | 86.06 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Mean cosine similarity | 0.577844 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Positive pair similarity | 0.595108 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Negative pair similarity | 0.472318 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Separation margin | 0.12279 | backend/data/reports/embedding_quality_statistics.json | backend/apps/embeddings/evaluate_embedding_quality.py | High | Computed by existing evaluator from FastText model and embedding quality benchmark |
| Semantic Recall@1 | 36.25 | backend/data/reports/semantic_search_statistics.json | backend/apps/embeddings/evaluate_semantic_search.py | High | Stored semantic-search benchmark metric |
| Semantic Recall@5 | 72.95 | backend/data/reports/semantic_search_statistics.json | backend/apps/embeddings/evaluate_semantic_search.py | High | Stored semantic-search benchmark metric |
| Semantic Recall@10 | 82.3 | backend/data/reports/semantic_search_statistics.json | backend/apps/embeddings/evaluate_semantic_search.py | High | Stored semantic-search benchmark metric |
| Semantic MRR | 0.529888 | backend/data/reports/semantic_search_statistics.json | backend/apps/embeddings/evaluate_semantic_search.py | High | Stored semantic-search benchmark metric |
| RAG Recall@1 | 27.0 | backend/data/reports/rag_retrieval_statistics.json | backend/apps/embeddings/evaluate_rag_retrieval.py | High | Stored RAG benchmark metric |
| RAG Recall@5 | 65.9 | backend/data/reports/rag_retrieval_statistics.json | backend/apps/embeddings/evaluate_rag_retrieval.py | High | Stored RAG benchmark metric |
| RAG Recall@10 | 84.3 | backend/data/reports/rag_retrieval_statistics.json | backend/apps/embeddings/evaluate_rag_retrieval.py | High | Stored RAG benchmark metric |
| RAG MRR | 0.455756 | backend/data/reports/rag_retrieval_statistics.json | backend/apps/embeddings/evaluate_rag_retrieval.py | High | Stored RAG benchmark metric |
| Average retrieval latency ms | 53.173 | backend/data/reports/rag_retrieval_statistics.json | backend/apps/embeddings/evaluate_rag_retrieval.py | High | Stored RAG benchmark metric |
| QA answer accuracy | 83.8 | backend/data/reports/qa_statistics.json | backend/apps/embeddings/evaluate_turkic_qa.py | High | Stored QA benchmark metric |
| QA source accuracy | 99.7 | backend/data/reports/qa_statistics.json | backend/apps/embeddings/evaluate_turkic_qa.py | High | Stored QA benchmark metric |
| QA top-k support coverage | 83.8 | backend/data/reports/qa_statistics.json | backend/apps/embeddings/evaluate_turkic_qa.py | High | Stored QA benchmark metric |
| Cognate alignment accuracy | 100.0 | backend/data/reports/cognate_alignment_statistics.json | backend/apps/cognates/management/commands/evaluate_cognate_alignment.py | High | Stored cognate benchmark metric |
| Cognate coverage | 100.0 | backend/data/reports/cognate_alignment_statistics.json | backend/apps/cognates/management/commands/evaluate_cognate_alignment.py | High | Stored cognate benchmark metric |
| Cognate total cases | 2000 | backend/data/reports/cognate_alignment_statistics.json | backend/apps/cognates/management/commands/evaluate_cognate_alignment.py | High | Stored cognate benchmark metric |
| Embedding Top-1 Wilson 95% CI | 39.45% - 42.17% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| Embedding Top-5 Wilson 95% CI | 72.42% - 74.86% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| Embedding Top-10 Wilson 95% CI | 85.07% - 86.99% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| Semantic Recall@1 Wilson 95% CI | 34.17% - 38.38% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| Semantic Recall@5 Wilson 95% CI | 70.96% - 74.85% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| Semantic Recall@10 Wilson 95% CI | 80.57% - 83.91% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| RAG Recall@1 Wilson 95% CI | 24.34% - 29.84% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| RAG Recall@5 Wilson 95% CI | 62.91% - 68.77% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| RAG Recall@10 Wilson 95% CI | 81.91% - 86.42% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| QA Answer Accuracy Wilson 95% CI | 81.39% - 85.95% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| QA Source Accuracy Wilson 95% CI | 99.12% - 99.90% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| QA Support Coverage Wilson 95% CI | 81.39% - 85.95% | paper_package/tables/table5_confidence_intervals.csv | Phase 37 extraction script | Medium | Derived from stored proportion and sample size using Wilson interval |
| ROOT proxy contribution | availability=75429; successful_hits=915 | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Phase 37 extraction script | Medium | Proxy evidence only; not controlled ablation |
| COGNATE proxy contribution | availability=23018; successful_hits=675 | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Phase 37 extraction script | Medium | Proxy evidence only; not controlled ablation |
| LINEAGE proxy contribution | availability=25018; successful_hits=675 | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Phase 37 extraction script | Medium | Proxy evidence only; not controlled ablation |
| LANGUAGE proxy contribution | availability=100000; successful_hits=798 | backend/data/embeddings/embedding_dataset.jsonl; backend/data/reports/rag_retrieval_statistics.json | Phase 37 extraction script | Medium | Proxy evidence only; not controlled ablation |
| Semantic Recall@10 categories distribution | mean=82.49, min=54.57, max=100.00, sd=16.98 | backend/data/reports/*_statistics.json | Phase 37 extraction script | Medium | Derived across stored category metrics |
| RAG Recall@10 categories distribution | mean=84.30, min=70.00, max=100.00, sd=11.55 | backend/data/reports/*_statistics.json | Phase 37 extraction script | Medium | Derived across stored category metrics |
| QA answer accuracy categories distribution | mean=83.80, min=68.80, max=100.00, sd=11.83 | backend/data/reports/*_statistics.json | Phase 37 extraction script | Medium | Derived across stored category metrics |

## Confidence Legend

- High: value exists directly in repository data/report artifacts or is a direct count from `embedding_dataset.jsonl`.
- Medium: value is derived from stored metrics without changing source results, for example confidence intervals or proxy ablation counts.
- Low: value is hypothesized or not directly measurable from current artifacts. Low-confidence values are intentionally excluded from core metric tables.

## Important Gaps

- No baseline embedding evaluation artifact is present, so improvement over baseline is not traceable.
- Controlled ablation metrics are not present, so feature contribution is traceable only as proxy evidence.
- Raw positive/negative similarity distributions are not stored, so standardized effect sizes such as Cohen's d are not reproducible from current artifacts.
