# Security Audit Report

Audit date: 2026-06-17

Scope: Django settings, auth/JWT, permissions, public endpoints, CORS/CSRF, Docker/Nginx, frontend token handling, environment examples.

## Summary

The project has a reasonable baseline: JWT auth, admin-only permissions for many write/admin endpoints, DRF throttling, CSRF middleware, production security settings, and CORS allowlist support. The main security blockers are example env files being used as Docker env files, localStorage refresh tokens, public expensive endpoints, GET endpoints with database side effects, incomplete admin permission tests, and deployment ambiguity around HTTPS.

## Findings

### 1. Production compose uses `.env.production.example`

- File: `docker-compose.prod.yml`
- Risk: critical
- Evidence: services use `env_file: .env.production.example`.
- Recommendation: use `.env.production` or secret manager; fail deployment if placeholder values remain.

### 2. Development compose uses `.env.example`

- File: `docker-compose.yml`
- Risk: medium
- Evidence: `env_file: .env.example` includes template secret, database, and local superuser password variables.
- Recommendation: keep examples as templates only; require local `.env`.

### 3. Frontend stores access and refresh tokens in localStorage

- File: `frontend/src/services/api.js`
- Risk: high if XSS occurs
- Evidence: tokens are stored under `turkicgrammarai.access` and `turkicgrammarai.refresh`.
- Recommendation: move refresh token to HttpOnly Secure SameSite cookie or implement strict CSP and short-lived refresh rotation.

### 4. Public morphology GET writes to database

- File: `backend/apps/morphology/views.py`
- Endpoint: `GET /api/morphology/analyze/`
- Risk: high
- Evidence: anonymous GET creates `MorphologicalAnalysis`.
- Recommendation: make GET read-only; use POST with auth/throttle for persistence.

### 5. Public expensive endpoints have only global throttles

- Files: `backend/apps/embeddings/views.py`, `backend/apps/morphology/views.py`
- Endpoints: `/api/embeddings/warm/`, `/api/search/semantic/`, `/api/rag/retrieve/`, `/api/qa/ask/`
- Risk: high
- Evidence: views use `AllowAny`; `warm` can load FastText and prime semantic search.
- Recommendation: protect warm/status operational endpoints, add stricter scoped throttles for search/QA.

### 6. Public feedback endpoint can be spammed

- File: `backend/apps/analytics/views.py`
- Endpoint: `POST /api/feedback/`
- Risk: medium
- Evidence: `FeedbackCreateView` uses `AllowAny`.
- Recommendation: add anonymous throttle scope, max payload length, and moderation fields.

### 7. Admin endpoints depend on role checks but need full regression tests

- Files: `backend/apps/languages/views.py`, `backend/apps/words/views.py`, `backend/apps/analytics/views.py`
- Risk: medium
- Evidence: language/word admin views use `IsAuthenticated, IsSuperAdmin`; analytics admin uses `IsAdminUser`.
- Recommendation: add tests for anonymous, student, researcher, staff, and super admin for every `/api/admin/*`.

### 8. SSL redirect disabled in production example

- File: `.env.production.example`
- Risk: medium
- Evidence: `SECURE_SSL_REDIRECT=False`.
- Recommendation: keep production default true and override only for local reverse-proxy testing with explicit docs.

### 9. CORS default is reasonable but deployment must lock it down

- File: `backend/config/settings/base.py`
- Risk: medium
- Evidence: `CORS_ALLOW_ALL_ORIGINS` can be enabled by env; default allowlist includes localhost.
- Recommendation: never enable allow-all in production.

### 10. No visible dependency/security CI

- Files: `.github/`
- Risk: medium
- Evidence: no workflows found locally.
- Recommendation: add dependency scanning, `pip-audit`/npm audit policy, and secret scanning.

## Positive Controls

- `backend/config/settings/base.py` has DRF JWT authentication and global throttling.
- `backend/config/settings/production.py` enables secure cookies, HSTS, and proxy SSL header.
- `infra/nginx.conf` proxies `/api/` and `/admin/` and serves static frontend.
- Admin write endpoints for words/languages require authenticated super admin.

## Release Blockers

1. Stop using example env files in production compose.
2. Protect `/api/embeddings/warm/`.
3. Remove GET write side effect in morphology analyze.
4. Add admin permission regression tests.
5. Decide secure token storage strategy.
