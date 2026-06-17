# API Consistency Report

Audit date: 2026-06-17

Scope: README.md, API_SPECIFICATION.md, backend/config/urls.py, app urlconfs, backend/openapi_generated.yaml, frontend/src.

## Summary

The implemented API uses `/api/` as the only runtime API prefix. There is no `/api/v1/` route in `backend/config/urls.py`. `README.md`, frontend calls, and `backend/openapi_generated.yaml` mostly match the real `/api/` contract. `API_SPECIFICATION.md` is mixed: it starts by declaring `/api/v1/`, lists many unimplemented `/api/v1/*` resources, then later acknowledges that this repository currently uses `/api/`.

Production risk: high for external consumers, moderate for current frontend. The app can run, but the public API contract is not authoritative.

## Real API Surface From Code

Evidence: `backend/config/urls.py` plus urlconfs under `backend/apps/*/urls.py`.

Implemented endpoints include:

- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/refresh/`, `GET/PATCH /api/auth/profile/`
- `GET /api/health/`
- `GET /api/languages/`, `GET /api/languages/search/`, `GET /api/languages/statistics/`, `GET /api/languages/<uuid:id>/`
- `GET/POST /api/admin/languages/`, `GET /api/admin/languages/export/`, `GET/PATCH/DELETE /api/admin/languages/<uuid:id>/`, `POST /api/admin/seed/languages/`
- `GET /api/words/`, `GET /api/words/search/`, `GET /api/words/statistics/`, `GET /api/words/quality/`, `GET /api/words/<uuid:id>/`
- `GET/POST /api/admin/words/`, `GET /api/admin/words/export/`, `POST /api/admin/words/benchmark-import/`, `GET/PATCH/DELETE /api/admin/words/<uuid:id>/`, `POST /api/admin/seed/words/`
- `GET /api/morphology/analyze/`, `GET /api/morphology/universal-analyze/`, `POST /api/morphology/batch-analyze/`, `GET /api/morphology/statistics/`
- `GET /api/cognates/`, `GET /api/cognates/statistics/`, `GET /api/cognates/search/`, `GET /api/cognates/universal-search/`, `GET /api/cognates/<uuid:pk>/`
- `GET /api/historical/`, `GET /api/historical/search/`, `GET /api/historical/statistics/`, `GET /api/historical/evolution/`, `GET /api/historical/<int:pk>/`
- `GET /api/embeddings/similarity/`, `GET /api/embeddings/neighbors/`, `GET /api/embeddings/warm/`, `GET /api/embeddings/status/`
- `GET /api/search/semantic/`, `GET /api/rag/retrieve/`, `GET /api/qa/ask/`
- `POST /api/feedback/`, `GET /api/admin/feedback/`, `GET /api/admin/qa-errors/`, `GET /api/admin/analytics/events/`, `GET /api/admin/analytics/usage/`, `GET /api/admin/analytics/qa-trends/`, `GET /api/admin/analytics/most-requested-words/`, `GET /api/admin/analytics/most-requested-languages/`, `GET /api/analytics/health/`
- `GET /api/corpus/statistics/`, `GET /api/schema/`, `GET /api/docs/`

## Mismatches

### 1. API_SPECIFICATION.md declares `/api/v1/` but code does not route it

- File: `API_SPECIFICATION.md`
- Code evidence: `backend/config/urls.py` only includes `path("api/...", ...)`; no `api/v1/`.
- Risk: high.
- Recommendation: choose one versioning policy. Either update docs to `/api/` for this release, or introduce `/api/v1/` aliases intentionally and update frontend/OpenAPI.

### 2. API_SPECIFICATION.md lists unimplemented auth endpoints

- File: `API_SPECIFICATION.md`
- Claimed endpoints: `/api/v1/auth/logout/`, `/api/v1/auth/me/`, password change/reset.
- Code evidence: `backend/apps/accounts/urls.py` only has `register/`, `login/`, `refresh/`, `profile/`.
- Risk: medium.
- Recommendation: remove these from release docs or create tracked backlog items.

### 3. API_SPECIFICATION.md lists broad module endpoints not implemented in urlconfs

- File: `API_SPECIFICATION.md`
- Examples: `/api/v1/corpus/corpora/`, `/api/v1/cognates/detect/`, `/api/v1/embeddings/models/`, `/api/v1/chatbot/sessions/`, visualization endpoints, jobs/exports.
- Code evidence: `backend/apps/corpus/urls.py` exposes only `statistics/`; `backend/apps/embeddings/urls.py` exposes only similarity/neighbors/warm/status; `apps.chatbot` and `apps.visualization` are not included in `INSTALLED_APPS` or `backend/config/urls.py`.
- Risk: high.
- Recommendation: split `API_SPECIFICATION.md` into "Implemented API" and "Roadmap API", or regenerate from OpenAPI and keep roadmap separate.

### 4. README.md is closer to code but incomplete

- File: `README.md`
- Matches: auth/profile, languages, words, schema/docs mostly match code.
- Missing implemented endpoints: morphology, cognates universal search, historical, embeddings, semantic search, RAG, QA, analytics, corpus statistics.
- Risk: medium.
- Recommendation: update README endpoint list from `backend/config/urls.py` or generated OpenAPI.

### 5. OpenAPI file appears stale/incomplete

- File: `backend/openapi_generated.yaml`
- Evidence: grep showed core/languages/words/cognates/corpus but not all current morphology, embeddings warm/status, semantic search, RAG, QA, historical, or analytics admin routes.
- Risk: medium-high.
- Recommendation: regenerate OpenAPI after all apps are loaded and commit one canonical schema.

### 6. Frontend is aligned with `/api/`, not `/api/v1/`

- Files: `frontend/src/services/api.js`, `frontend/src/pages/*.jsx`.
- Evidence: calls use `/api/auth/login/`, `/api/morphology/analyze/`, `/api/qa/ask/`, `/api/search/semantic/`, `/api/admin/analytics/...`.
- Risk: low for current UI, high if backend docs are followed by external clients.
- Recommendation: do not change frontend until API version policy is decided.

## Release Actions

1. Treat `/api/` as release contract for the current version.
2. Replace or archive `/api/v1/` sections in `API_SPECIFICATION.md`.
3. Regenerate `backend/openapi_generated.yaml`.
4. Add CI validation with `python manage.py spectacular --validate`.
5. Add a route inventory test that asserts key public frontend endpoints exist.

