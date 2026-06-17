# Publication Evidence Report

## Experimentally Verified in Repository Artifacts

- FastText training configuration and vocabulary size are stored in `fasttext_training_stats.json`.
- Embedding retrieval metrics are stored in `embedding_quality_statistics.json` and are traceable to `evaluate_embedding_quality.py`.
- Semantic search Recall@1/5/10 and MRR are stored in `semantic_search_statistics.json` and traceable to `evaluate_semantic_search.py`.
- RAG Recall@1/5/10, MRR, latency, and source contribution are stored in `rag_retrieval_statistics.json` and traceable to `evaluate_rag_retrieval.py`.
- QA answer/source/support metrics are stored in `qa_statistics.json` and traceable to `evaluate_turkic_qa.py`.
- Cognate alignment accuracy and coverage are stored in `cognate_alignment_statistics.json` and traceable to the cognate alignment management command.

## Supported by Repository Evidence

- The embedding dataset contains 100,000 records and covers eight language codes.
- The data pipeline combines lexical forms, morphology-derived features, cognate groups, and historical lineage metadata.
- Retrieval and QA pipelines are operational in stored evaluations.
- Positive pair similarity is higher than negative pair similarity in the stored embedding benchmark.

## Requires External Validation

- Expert validation of cognate groups, historical reconstructions, lemmas, and roots.
- Evaluation on independent benchmark sets not generated from repository resources.
- Baseline comparison against standard FastText and other multilingual embedding models.
- Controlled ablation experiments for ROOT, COGNATE, LINEAGE, and LANGUAGE features.
- Broader robustness testing across unseen corpora, scripts, dialects, and noisy text.

## Manuscript Guidance

The paper can present the current system as a research-preview embedding and retrieval framework with repository-backed internal evaluations. It should not claim state-of-the-art performance, production-grade validity, or externally verified linguistic authority without additional evidence.
