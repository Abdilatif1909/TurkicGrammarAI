# Testing Gap Report

Audit date: 2026-06-17

Commands run:

- `USE_SQLITE=True python manage.py check`: passed.
- `USE_SQLITE=True python manage.py test`: 92 tests passed in 11.143s.
- `npm run build`: passed.

## Summary

Backend unit/API coverage exists for core apps and selected morphology behavior. Frontend has no test suite. There are no GitHub Actions workflows in the local repository. Scientific evaluation tests are not independent enough for publication claims.

## Current Backend Coverage

Test files found:

- `backend/apps/accounts/tests.py`
- `backend/apps/core/tests.py`
- `backend/apps/languages/tests.py`
- `backend/apps/words/tests.py`
- `backend/apps/words/test_validation.py`
- `backend/apps/morphology/tests.py`
- `backend/apps/cognates/tests.py`
- `backend/apps/historical/tests.py`
- `backend/apps/corpus/tests.py`

## Major Gaps

### 1. No CI workflow

- Files: `.github/`
- Risk: high
- Evidence: no `.github` workflows were found locally.
- Recommendation: add GitHub Actions for backend tests, frontend build, OpenAPI validation, and security checks.

### 2. Frontend has no tests

- File: `frontend/package.json`
- Risk: high
- Evidence: no test scripts or test dependencies.
- Recommendation: add Vitest/React Testing Library and Playwright.

### 3. Morphology tests pass despite no migrations

- Files: `backend/apps/morphology/models.py`, absent `backend/apps/morphology/migrations`
- Risk: critical
- Evidence: `showmigrations morphology` reports no migrations, but tests pass because test DB can create tables for unmigrated apps.
- Recommendation: add migrations and add CI check that every app with models has migrations.

### 4. GET side effects are not tested as contract violations

- File: `backend/apps/morphology/views.py`
- Endpoint: `GET /api/morphology/analyze/`
- Risk: high
- Evidence: endpoint writes `MorphologicalAnalysis`.
- Recommendation: add API contract test that public GET endpoints do not mutate DB.

### 5. Embedding/RAG tests need independent fixtures

- Files: `backend/apps/embeddings/evaluate_*.py`
- Risk: high
- Evidence: benchmark generation uses semantic index as source.
- Recommendation: add static held-out fixtures not generated from the retrieval index.

### 6. Security tests are missing

- Files: admin endpoints under languages/words/analytics
- Risk: high
- Recommendation: assert unauthenticated and non-admin users cannot access all `/api/admin/*` endpoints.

### 7. API documentation consistency is untested

- Files: `API_SPECIFICATION.md`, `backend/openapi_generated.yaml`, `backend/config/urls.py`
- Risk: medium-high
- Recommendation: add schema generation check and route inventory test.

### 8. Load/performance tests are not in CI

- Files: `scripts/load_test.py`, embedding warm endpoints
- Risk: medium
- Recommendation: add a small smoke performance check and separate manual load-test workflow.

## Recommended CI Jobs

1. Backend: `python manage.py check` and `python manage.py test`.
2. Migration check: `python manage.py makemigrations --check --dry-run`.
3. OpenAPI: `python manage.py spectacular --validate --file tmp-schema.yaml`.
4. Frontend: `npm ci`, `npm run build`, test suite once added.
5. Data validation: run lightweight dataset schema/provenance checks.

