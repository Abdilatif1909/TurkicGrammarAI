# Model Manifest

Generated for Phase 36.5 release preparation on 2026-06-17.

This manifest inventories model and embedding artifacts without modifying algorithms or evaluation results.

## FastText Model Artifacts

| File | Size | Last modified |
| --- | ---: | --- |
| `backend/models/turkic_fasttext.model` | 5,909,365 bytes | 2026-06-09 17:58:31 |
| `backend/models/turkic_fasttext.model.syn1neg.npy` | 171,613,328 bytes | 2026-06-09 17:58:31 |
| `backend/models/turkic_fasttext.model.wv.vectors_ngrams.npy` | 2,400,000,128 bytes | 2026-06-09 17:58:30 |
| `backend/models/turkic_fasttext.model.wv.vectors_vocab.npy` | 171,613,328 bytes | 2026-06-09 17:58:25 |
| `backend/models/turkic_fasttext.vec` | 483,955,501 bytes | 2026-06-09 17:58:50 |

## Embedding Data

| File | Records | Size |
| --- | ---: | ---: |
| `backend/data/embeddings/embedding_dataset.jsonl` | 100,000 | 34,028,032 bytes |
| `backend/data/embeddings/fasttext_corpus.txt` | n/a | 19,744,457 bytes |
| `backend/data/embeddings/semantic_index.json` | 100,000 | 42,081,946 bytes |

## Embedding And Retrieval Benchmarks

| File | Records | Size |
| --- | ---: | ---: |
| `backend/data/embeddings/embedding_benchmark.json` | 5 | 1,577 bytes |
| `backend/data/embeddings/embedding_quality_benchmark.json` | 5,000 | 775,166 bytes |
| `backend/data/embeddings/semantic_search_benchmark.json` | 2,000 | 407,918 bytes |
| `backend/data/embeddings/rag_retrieval_benchmark.json` | 1,000 | 221,843 bytes |
| `backend/data/embeddings/qa_benchmark.json` | 1,000 | 334,260 bytes |

## Evaluation Files

| File | Purpose |
| --- | --- |
| `backend/apps/embeddings/evaluate_fasttext_embeddings.py` | FastText evaluation routine |
| `backend/apps/embeddings/evaluate_embedding_quality.py` | embedding quality evaluation routine |
| `backend/apps/embeddings/evaluate_semantic_search.py` | semantic search benchmark generation/evaluation |
| `backend/apps/embeddings/evaluate_rag_retrieval.py` | RAG retrieval benchmark generation/evaluation |
| `backend/apps/embeddings/evaluate_turkic_qa.py` | QA benchmark generation/evaluation |
| `backend/data/reports/fasttext_evaluation.json` | FastText evaluation output |
| `backend/data/reports/embedding_quality_statistics.json` | embedding quality statistics |
| `backend/data/reports/semantic_search_statistics.json` | semantic search statistics |
| `backend/data/reports/rag_retrieval_statistics.json` | RAG retrieval statistics |
| `backend/data/reports/qa_statistics.json` | QA statistics |

## Release Notes

- The FastText vector artifacts are large. A public release should decide whether to use Git LFS, GitHub Release assets, or an external archive.
- Benchmark generation for semantic search, RAG, and QA is not independent from the semantic index. Treat these as regression/evaluation artifacts, not publication-grade validation.
- Do not modify model artifacts or evaluation outputs during release-preparation-only changes.
