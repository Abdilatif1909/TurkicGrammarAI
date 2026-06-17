# Technical Debt Report

Date: 2026-06-11

## Critical Debt

### Morphology Permission Contract

`backend/apps/morphology/views.py` defines APIViews without explicit `permission_classes`. Because global DRF permission is `IsAuthenticated`, these endpoints return 401 for anonymous calls. The React morphology page does not attach JWT headers, so the page cannot work in the current unauthenticated web UX.

Impact: user-facing morphology feature is functionally broken unless the user has an authenticated token flow that the frontend does not provide.

### API Schema Coverage

OpenAPI generation reports 68 errors across 17 unique APIViews. The main cause is APIViews without `serializer_class` or schema annotations in morphology, embeddings, analytics statistics, historical custom views, and cognate custom search views.

Impact: API contract is not fully documented, SDK generation is unreliable, and production API review cannot be completed from schema alone.

### FastText Runtime Coupling

The FastText model is loaded directly in request-serving Python code. Cold load measured about 50.8s, with a very large n-gram vector file on disk.

Impact: slow startup, poor autoscaling behavior, high memory pressure, and possible request timeouts after worker recycle.

## High Priority Debt

### Historical Data Duplication and Path Drift

Two historical data locations exist:

- `backend/data/historical/historical_forms.json`: 0 records.
- `data/historical/historical_forms.json`: 2,000 records.

Impact: services may read an empty backend dataset while active research data lives elsewhere.

### Embedding Dataset Quality

`backend/data/embeddings/embedding_dataset.jsonl` has:

- 100,000 records.
- 9,676 duplicate best-key records.
- 33,555 records with empty `features`.
- 76,983 records without `cognate_group`.
- 76,983 records without `historical_lineage`.

Impact: embedding quality and retrieval scoring may be skewed away from the cognate/historical objective.

### Missing Tests for Newer Runtime Apps

Apps with missing or weak tests:

- `analytics`: no `tests.py`.
- `embeddings`: no `tests.py`.
- Frontend: no test or lint script.

Impact: regressions in QA, RAG, semantic search, analytics, and dashboard behavior are likely to slip through.

### Frontend Authentication Gap

The frontend API helper only sends JSON headers and does not support Authorization. Admin dashboard pages call protected admin endpoints, but no login/token flow exists in the web app.

Impact: admin dashboard is structurally present but not operational for real admins.

## Medium Priority Debt

### Benchmark Duplication

Duplicate best-key records were detected in multiple benchmark files:

- `cross_language_benchmark.json`: high duplicate rate.
- `kazakh_morphology_benchmark.json`.
- `kyrgyz_morphology_benchmark.json`.
- `old_turkic_morphology_benchmark.json`.
- `turkmen_morphology_benchmark.json`.
- `uyghur_morphology_benchmark.json`.
- `semantic_search_benchmark.json`.
- `rag_retrieval_benchmark.json`.
- `qa_benchmark.json`.

Impact: accuracy metrics may overstate real performance or underrepresent long-tail cases.

### Synthetic Data Labeling

Several reports and generated data files indicate synthetic generation, but downstream benchmark/evaluation files do not always carry a clear `source` or `review_status`.

Impact: scientific claims are hard to defend without separating generated data from curated or corpus-derived examples.

### Operational Observability

Request logging and analytics tracking exist, but there is no integrated error-monitoring backend, alerting policy, dashboard export, or production SLO definition.

Impact: production incident response would be manual.

## Low Priority Debt

### Generated Cache Files in Workspace

`__pycache__` files are present under backend app directories.

Impact: noisy workspace and possible accidental packaging if ignore rules are incomplete.

### Docker Compose Example Uses Example Env Directly

`docker-compose.prod.yml` references `.env.production.example` directly.

Impact: easy to accidentally deploy with placeholder secrets unless deployment process replaces it.

### Frontend Implementation Concentration

Most frontend logic lives in a single `frontend/src/main.jsx` file.

Impact: acceptable for MVP, but harder to test and maintain as pages grow.

## Recommended Paydown Order

1. Fix frontend/backend auth contract for morphology and admin pages.
2. Add OpenAPI serializers or `extend_schema` annotations for all APIViews.
3. Split FastText into a warmed service or preload workers during deployment.
4. Consolidate historical data source path.
5. Add regression tests for analytics and embeddings.
6. Deduplicate and source-label benchmark datasets.
7. Add frontend lint/test tooling.
