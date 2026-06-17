# Embedding and RAG Audit

Audit date: 2026-06-17

Scope: `backend/apps/embeddings`, `backend/data/embeddings`, FastText model artifacts, semantic search, RAG retrieval, QA, and frontend consumers.

## Summary

The embedding/RAG stack is a deterministic retrieval system around FastText plus metadata expansion. It is operational for demos, but its evaluation is contaminated because benchmark cases are generated from the same semantic index being evaluated. It should not be presented as independent scientific evidence yet.

## Findings

### 1. Evaluation leakage is built into benchmark generation

- Files: `backend/apps/embeddings/evaluate_semantic_search.py`, `evaluate_rag_retrieval.py`, `evaluate_turkic_qa.py`
- Endpoints: `/api/search/semantic/`, `/api/rag/retrieve/`, `/api/qa/ask/`
- Risk: high
- Evidence: benchmark cases are generated from `semantic_index.json`, then evaluated by searching/retrieving against that same index.
- Recommendation: create independent, held-out benchmarks not derived from `semantic_index.json`.

### 2. Retrieval ranking is manually weighted

- File: `backend/apps/embeddings/turkic_retriever.py`
- Risk: medium-high
- Evidence: final score is a fixed sum of semantic, cognate, historical, morphology, and dictionary weights.
- Recommendation: document as heuristic ranking and tune on independent validation data.

### 3. Semantic search candidate expansion is narrow

- File: `backend/apps/embeddings/semantic_search.py`
- Risk: medium
- Evidence: `nearest_limit` defaults to 0 in `semantic_search()`.
- Recommendation: add controlled nearest-neighbor fallback with latency guard and evaluate separately.

### 4. FastText model is process-local and requires warm-up

- File: `backend/apps/embeddings/fasttext_service.py`
- Endpoint: `/api/embeddings/warm/`
- Risk: medium
- Evidence: `load_fasttext_model()` is `lru_cache(maxsize=1)` and loads model into each process.
- Recommendation: production startup should call warm endpoint per worker or preload model with deployment-specific strategy.

### 5. Embedding data provenance is insufficient

- File: `backend/data/embeddings/embedding_dataset.jsonl`
- Risk: high
- Evidence: records often use broad `source` values and inherit generated cognate/historical metadata.
- Recommendation: include source strata and exclude synthetic strata from scientific evaluation unless reviewed.

### 6. QA is extractive/template-based, not generative reasoning

- File: `backend/apps/embeddings/turkic_qa.py`
- Endpoint: `/api/qa/ask/`
- Risk: medium
- Evidence: `infer_question_type()`, `extract_query_term()`, and `build_answer()` use rule-based templates.
- Recommendation: present as retrieval-based structured answer builder, not as an LLM research assistant.

### 7. Citations are internal IDs, not scholarly citations

- Files: `backend/apps/embeddings/turkic_qa.py`, `backend/apps/embeddings/turkic_retriever.py`
- Risk: high for Q1 publication claims
- Evidence: citations include `source_type`, `source_id`, and confidence, not bibliographic references.
- Recommendation: attach dataset/source bibliography to each evidence item before publication.

### 8. OpenAPI coverage appears stale

- Files: `backend/openapi_generated.yaml`, `backend/apps/embeddings/views.py`
- Risk: medium
- Evidence: code has warm/status/semantic/RAG/QA endpoints, while OpenAPI grep did not show all current embedding/RAG/QA surfaces.
- Recommendation: regenerate and validate OpenAPI.

## Trustworthy Claims

- The endpoints exist in code and can return deterministic retrieval/QA payloads if model/index assets are present.
- FastText warm/status endpoints exist.
- Frontend pages call the current `/api/search/semantic/`, `/api/rag/retrieve/`, `/api/qa/ask/` endpoints.

## Claims To Avoid

- Do not claim independent semantic search accuracy from generated benchmark scores.
- Do not claim RAG answer correctness without expert-reviewed QA benchmark.
- Do not claim scholarly citation support until sources are bibliographic and item-level.

## Required Actions

1. Build held-out benchmark data independent from training/index data.
2. Split metrics by source type.
3. Add source bibliography and license fields to retrieval documents.
4. Add latency tests for cold/warm FastText paths.
5. Rebuild OpenAPI and include all current embedding/RAG/QA endpoints.

