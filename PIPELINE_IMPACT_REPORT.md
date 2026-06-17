# Pipeline Impact Report

This report summarizes Phase 35 end-to-end evaluation after lexical expansion.

## Execution Status

| Step | Status | Output |
|---|---|---|
| Morphology evaluations | completed | `backend/data/reports/*_morphology_statistics.json` |
| Cognate alignment evaluation | completed | `backend/data/reports/cognate_alignment_statistics.json` |
| Embedding dataset rebuild | completed | `backend/data/embeddings/embedding_dataset.jsonl`, `EMBEDDING_DATASET_REPORT.md` |
| Embedding quality evaluation | completed | `backend/data/reports/embedding_quality_statistics.json` |
| Semantic search evaluation | completed | `backend/data/reports/semantic_search_statistics.json` |
| RAG retrieval evaluation | completed | `backend/data/reports/rag_retrieval_statistics.json` |
| QA evaluation | completed | `backend/data/reports/qa_statistics.json` |

## Impact By Subsystem

| Subsystem | Main Post Metric | Impact Interpretation |
|---|---:|---|
| Morphology | average AnyMatch 98.925% | Operational; same-benchmark before unavailable |
| Cognates | alignment 100% | Operational; before unavailable |
| Embeddings | Top10 86.06% | Comparable gain +1 Top10 points vs preserved baseline |
| Semantic Search | Recall@10 82.3% | Operational; before unavailable |
| RAG | Recall@10 84.3% | Operational; before unavailable |
| QA | Answer Accuracy 83.8% | Operational; before unavailable |

## Data Caveat

The evaluator runs overwrote several subsystem report/statistic files. Future impact sprints should snapshot `backend/data/reports` before re-running evaluations so every subsystem has a strict before/after comparison.
