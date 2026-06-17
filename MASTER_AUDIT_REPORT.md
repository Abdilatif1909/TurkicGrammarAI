# Master Audit Report

Audit date: 2026-06-17

Repository: `TurkicGrammarAI`

Audit basis: local repository code and configuration. Prior report claims were not treated as authoritative. Commands run: `python manage.py check`, `python manage.py test`, `npm run build`, route/config/data inspection.

## Scores

- Production readiness score: 58 / 100
- Scientific readiness score: 42 / 100
- Q1 publication readiness score: 28 / 100

Rationale: the app builds and backend tests pass, but API docs are inconsistent, morphology migrations are missing, deployment env handling is unsafe, scientific datasets/benchmarks are not yet cleanly reviewed or independent, and frontend/testing/CI coverage is incomplete.

## Top 10 Issues

### 1. Morphology models have no migrations

- File/module: `backend/apps/morphology/models.py`, missing `backend/apps/morphology/migrations`
- Endpoint: `/api/morphology/*`
- Risk: critical
- Recommendation: create initial migrations and add migration check in CI.

### 2. Public GET morphology endpoint writes to DB

- File/module: `backend/apps/morphology/views.py`
- Endpoint: `GET /api/morphology/analyze/`
- Risk: high
- Recommendation: make GET read-only; persist analyses only via explicit POST or analytics queue.

### 3. API docs claim `/api/v1/`, code uses `/api/`

- File/module: `API_SPECIFICATION.md`, `backend/config/urls.py`
- Endpoint: all API routes
- Risk: high
- Recommendation: make `/api/` the current release contract or intentionally add `/api/v1/` aliases.

### 4. OpenAPI schema is stale/incomplete

- File/module: `backend/openapi_generated.yaml`
- Endpoint: morphology, embeddings, RAG, QA, analytics, historical
- Risk: high
- Recommendation: regenerate schema and validate in CI.

### 5. Production Docker uses example env file

- File/module: `docker-compose.prod.yml`, `.env.production.example`
- Endpoint: deployment-wide
- Risk: critical
- Recommendation: use real secret source, not example file.

### 6. Dataset statistics are stale and language codes are inconsistent

- File/module: `words_dataset_statistics.json`, `backend/data/words/*.json`
- Endpoint: `/api/words/*`, embeddings/search
- Risk: high
- Recommendation: normalize language codes and regenerate stats from canonical data.

### 7. Gold/benchmark data is not publication-grade

- File/module: `backend/data/gold/gold_dataset_manifest.json`, `backend/apps/embeddings/evaluate_*.py`
- Endpoint: morphology/search/RAG/QA metrics
- Risk: high
- Recommendation: separate synthetic regression data from expert-reviewed held-out gold data.

### 8. Embedding/RAG benchmark leakage

- File/module: `backend/apps/embeddings/evaluate_semantic_search.py`, `evaluate_rag_retrieval.py`, `evaluate_turkic_qa.py`
- Endpoint: `/api/search/semantic/`, `/api/rag/retrieve/`, `/api/qa/ask/`
- Risk: high
- Recommendation: create independent benchmarks not generated from `semantic_index.json`.

### 9. Frontend has no tests and stores tokens in localStorage

- File/module: `frontend/package.json`, `frontend/src/services/api.js`
- Endpoint: auth/admin UI
- Risk: medium-high
- Recommendation: add frontend tests/E2E and revisit token storage for production.

### 10. No GitHub Actions workflow found

- File/module: `.github/`
- Endpoint: delivery pipeline
- Risk: high
- Recommendation: add CI for backend tests, migration check, OpenAPI validation, frontend build, and data validation.

## Backend Architecture

Strengths:

- Apps are separated into accounts, languages, words, morphology, cognates, historical, embeddings, corpus, analytics.
- Languages and words have service layers and cache invalidation.
- Settings are split into base/development/production.
- Redis cache and Celery settings exist.
- DRF throttling is configured globally.

Risks:

- App maturity is uneven: corpus only exposes statistics; chatbot/visualization directories exist but are not wired into settings/urls.
- Morphology has models but no migrations.
- Embedding/RAG logic is service-like but not integrated with async Celery jobs.
- Several public endpoints perform expensive work under `AllowAny`.
- Some modules use broad exception swallowing, e.g. historical evolution fallback returns `{}` on exception.

## Repository Documentation And CI

- `docs/` was present but no files were found during local inspection.
- No `.github` workflow files were found.
- There is no dedicated `reports/` directory; audit/report artifacts are mostly root-level Markdown/JSON files.
- Root-level report files are useful historical context, but this audit did not treat them as evidence unless confirmed in code/data.

## One-Week Fix Plan

1. Add morphology migrations and run migration check.
2. Remove DB writes from `GET /api/morphology/analyze/`.
3. Regenerate OpenAPI and update `API_SPECIFICATION.md` to `/api/`.
4. Replace Docker example env usage with real env file requirement.
5. Protect `/api/embeddings/warm/` behind admin auth or deployment-only access.
6. Normalize language codes in word datasets or add a validation failure gate.
7. Add CI: backend check/test, makemigrations dry-run, frontend build.
8. Add admin permission regression tests for `/api/admin/*`.

## One-Month Development Plan

1. Build reviewed gold subsets for morphology, cognates, historical, QA.
2. Split synthetic/generated datasets from reviewed data in manifests.
3. Add independent held-out embedding/RAG/QA benchmarks.
4. Add provenance schema to every dataset item.
5. Add frontend tests and Playwright smoke flows.
6. Add deployment health checks for DB, Redis, FastText warm status, OpenAPI version.
7. Add source-level retrieval citations and bibliographic metadata.
8. Decide API versioning policy and lock it with tests.

## Release Blockers

- Missing morphology migrations.
- `/api/v1/` documentation mismatch.
- Example env files used by Docker compose.
- Public warm/expensive endpoints not sufficiently protected.
- Dataset stats stale and language codes inconsistent.
- Generated benchmarks used as if scientific evaluation.
- No CI workflow.

## Do Not Do Now

- Do not add new NLP features before fixing migrations, API contract, and dataset provenance.
- Do not publish Q1-level metrics from generated benchmarks.
- Do not expand UI pages before adding E2E smoke coverage.
- Do not train larger models on current mixed-provenance data.
- Do not expose `/api/v1/` unless versioning is designed and tested.

## Generated Detailed Reports

- `API_CONSISTENCY_REPORT.md`
- `DATASET_AUDIT_V2.md`
- `MORPHOLOGY_SCIENTIFIC_AUDIT.md`
- `EMBEDDING_AND_RAG_AUDIT.md`
- `FRONTEND_PRODUCTION_AUDIT.md`
- `TESTING_GAP_REPORT.md`
- `SECURITY_AUDIT_REPORT.md`
