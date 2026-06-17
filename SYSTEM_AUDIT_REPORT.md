# TurkicGrammarAI Full System Audit

Date: 2026-06-11

Scope: backend apps, API inventory, frontend pages, datasets, model/runtime behavior, deployment configuration, and security posture. No new product features were added during this audit.

## Executive Summary

Release readiness score: 68 / 100.

The platform is functional as a research MVP and has broad module coverage: Django tests pass, the React frontend builds, the FastText model loads, and semantic/RAG/QA services return results. The main blockers for production release are API documentation gaps, frontend/API auth mismatch for morphology, slow cold-start behavior for the FastText model, data quality issues in benchmarks and embedding coverage, and incomplete deployment hardening around TLS/runtime validation.

## Validation Results

| Check | Result |
| --- | --- |
| Django system check | PASS: no issues |
| Django tests | PASS: 90 tests |
| Frontend production build | PASS |
| OpenAPI schema generation | PARTIAL: generated, but 68 schema errors across 17 unique APIViews |
| Docker Compose config | PASS with local Docker credential warning |
| FastText model load | PASS, cold load about 50.8s |
| Semantic search service | PASS, sample latency about 4.15s |
| RAG service | PASS, sample latency about 1.85s |
| QA service | PASS, sample latency about 112ms after model/index warmup |

## Backend App Inventory

| App | Models | Serializers | Views | URLs | Tests | Migrations |
| --- | --- | --- | --- | --- | --- | --- |
| accounts | yes | yes | yes | yes | yes | yes |
| languages | yes | yes | yes | yes | yes | yes |
| words | yes | yes | yes | yes | yes | yes |
| morphology | yes | yes | yes | yes | yes | no DB migrations |
| cognates | yes | yes | yes | yes | yes | yes |
| historical | yes | yes | yes | yes | yes | yes |
| corpus | yes | yes | yes | yes | yes | yes |
| embeddings | no DB models | no serializers | yes | yes | no tests | no DB migrations |
| analytics | yes | yes | yes | yes | no tests | yes |

## API Inventory

Primary API endpoints verified from Django URL resolver:

- Auth: `/api/auth/register/`, `/api/auth/login/`, `/api/auth/refresh/`, `/api/auth/profile/`
- Health: `/api/health/`, `/api/analytics/health/`
- Languages: `/api/languages/`, `/api/languages/search/`, `/api/languages/statistics/`, `/api/languages/<uuid:id>/`
- Words: `/api/words/`, `/api/words/search/`, `/api/words/statistics/`, `/api/words/quality/`, `/api/words/<uuid:id>/`
- Corpus: `/api/corpus/statistics/`
- Cognates: `/api/cognates/`, `/api/cognates/search/`, `/api/cognates/universal-search/`, `/api/cognates/statistics/`, `/api/cognates/<uuid:pk>/`
- Historical: `/api/historical/`, `/api/historical/search/`, `/api/historical/statistics/`, `/api/historical/evolution/`, `/api/historical/<int:pk>/`
- Morphology: `/api/morphology/analyze/`, `/api/morphology/universal-analyze/`, `/api/morphology/batch-analyze/`, `/api/morphology/statistics/`
- Embeddings/search: `/api/embeddings/similarity/`, `/api/embeddings/neighbors/`, `/api/search/semantic/`, `/api/rag/retrieve/`, `/api/qa/ask/`
- Analytics/admin: `/api/feedback/`, `/api/admin/feedback/`, `/api/admin/qa-errors/`, `/api/admin/analytics/events/`, `/api/admin/analytics/usage/`, `/api/admin/analytics/qa-trends/`, `/api/admin/analytics/most-requested-words/`, `/api/admin/analytics/most-requested-languages/`
- Documentation: `/api/schema/`, `/api/docs/`

Sample unauthenticated API smoke results:

| Endpoint | Status |
| --- | --- |
| `/api/languages/` | 200 |
| `/api/words/search/?q=kitob` | 200 |
| `/api/cognates/universal-search/?q=tangri` | 200 |
| `/api/historical/evolution/?q=tangri` | 200 |
| `/api/morphology/analyze/?word=kitoblarimizdan&language=uz` | 401 |
| `/api/embeddings/similarity/?word_a=kitob&word_b=kitap` | 200 |
| `/api/feedback/` | 201 |
| `/api/admin/feedback/` | 401 |

## Frontend Audit

Pages found in `frontend/src/main.jsx`:

- QA Chat
- Morphology Analyzer
- Cognate Explorer
- Semantic Search
- Historical Explorer
- Analytics Dashboard

Frontend strengths:

- Shared `useAsyncAction` handles loading and error state.
- Responsive CSS breakpoints exist at 980px and 640px.
- QA feedback form is integrated with `/api/feedback/`.
- Admin dashboard calls analytics usage, trends, requested words, requested languages, and health endpoints.

Frontend gaps:

- API helper does not attach JWT Authorization headers.
- Morphology page calls endpoints that currently return 401 without auth.
- Admin dashboard states that admin auth is required but has no login/token flow.
- No frontend test suite or lint script is configured.

## Dataset Audit

Morphology rule and lemma counts:

| Language | Rules | Lemmas | Target Status |
| --- | ---: | ---: | --- |
| Uzbek | 376 | 5,077 | below later-language target scale |
| Turkish | 564 | 10,500 | meets phase target |
| Azerbaijani | 564 | 10,500 | meets phase target |
| Kazakh | 2,045 | 12,050 | meets phase target |
| Kyrgyz | 1,840 | 12,050 | meets phase target |
| Turkmen | 2,061 | 12,050 | meets phase target |
| Uyghur | 2,949 | 12,050 | rules below requested 2,000+ target is met; near Old Turkic scale |
| Old Turkic | 5,804 | 15,086 | meets phase target |

Other dataset counts:

- Words datasets: 58,000 total records across `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `otk`; no Uyghur words dataset file was found in `backend/data/words`.
- Cross-language cognates: 2,000 records.
- Embedding dataset: 100,000 records.
- Semantic index: 100,000 records.
- Human evaluation benchmark: 500 records.
- `backend/data/historical/historical_forms.json`: 0 records.
- `data/historical/historical_forms.json`: 2,000 records.

Dataset quality issues:

- `embedding_dataset.jsonl`: 9,676 duplicate best-key records.
- `embedding_dataset.jsonl`: 76,983 records without cognate group and historical lineage.
- `embedding_dataset.jsonl`: 33,555 records with empty `features`.
- Synthetic benchmark duplication detected in several benchmark files, including Kazakh, Kyrgyz, Turkmen, Uyghur, Old Turkic, and cross-language benchmark files.
- `cross_language_cognate_benchmark.json` has 1,984 records where `language` is present but empty.
- Historical data path mismatch exists between `backend/data/historical/historical_forms.json` and `data/historical/historical_forms.json`.

## Model Audit

FastText files exist under `backend/models/`:

- `turkic_fasttext.model`
- `turkic_fasttext.model.syn1neg.npy`
- `turkic_fasttext.model.wv.vectors_ngrams.npy`
- `turkic_fasttext.model.wv.vectors_vocab.npy`
- `turkic_fasttext.vec`

Measured runtime:

| Component | Result |
| --- | --- |
| FastText cold load | about 50.8s |
| Vocabulary size | 143,011 |
| Semantic search sample | 20 results, about 4.15s |
| RAG sample | 20 results, about 1.85s |
| QA sample | 10 results, about 112ms after warmup |

Memory usage was not reliably measured because `psutil` was unavailable in the audit environment. The on-disk model footprint is large, dominated by the 2.4GB n-gram vector file.

## Deployment Audit

Deployment files exist:

- `Dockerfile`
- `docker-compose.yml`
- `docker-compose.prod.yml`
- `.env.production.example`
- `infra/nginx.conf`

`docker-compose -f docker-compose.prod.yml config` renders successfully. A local Docker credential warning was emitted, but the compose file itself is parseable.

Deployment gaps:

- `.env.production.example` uses placeholder secrets/passwords.
- `.env.production.example` sets `SECURE_SSL_REDIRECT=False`.
- Nginx config only listens on port 80 and has no TLS server block.
- No automated production smoke test verifies Django, Postgres, Redis, Nginx, static assets, and model loading together.

## Security Audit

Implemented:

- JWT authentication is configured.
- Default DRF permission is `IsAuthenticated`.
- Admin analytics endpoints use `IsAdminUser`.
- Public feedback endpoint uses `AllowAny`.
- Public read endpoints are explicitly open in languages, words, historical, embeddings, and health.
- Rate limiting is configured for anonymous and authenticated users.
- Production settings enable HSTS, secure cookies, and proxy SSL header.

Security gaps:

- Frontend does not support JWT token storage or Authorization headers.
- Admin dashboard UI cannot authenticate against admin analytics APIs.
- Production sample disables SSL redirect.
- Public embedding/search/QA endpoints can be computationally expensive under anonymous rate limits.

## Issue Summary

### Critical Issues

1. Morphology frontend/API mismatch: frontend calls morphology endpoints anonymously, but backend returns 401 because morphology APIViews inherit the global `IsAuthenticated` permission.
2. FastText cold start is production-hostile at about 50.8s and loads a multi-GB n-gram matrix.
3. API documentation is incomplete: schema generation reports 68 errors across 17 unique APIViews due missing serializers/schema annotations.

### High Priority Issues

1. Historical data path mismatch: backend historical data file is empty while root `data/historical/historical_forms.json` contains 2,000 records.
2. Embedding dataset has high missing cognate/historical coverage and 9,676 duplicate best-key records.
3. Frontend has no JWT auth flow, so admin dashboard cannot be used against protected endpoints.
4. Production TLS is incomplete in sample deployment.

### Medium Priority Issues

1. Analytics app has no tests.
2. Embeddings app has no tests despite carrying model, search, RAG, and QA runtime logic.
3. Several benchmark datasets contain high duplicate rates.
4. No frontend lint/test pipeline exists.
5. Load testing script exists, but no audited live load-test run was performed.

### Low Priority Issues

1. `__pycache__` files are present in the workspace.
2. Some generated reports and benchmark artifacts appear to be synthetic and should be labeled more clearly.
3. Docker Compose uses `.env.production.example` directly instead of a required real production `.env`.

## Release Readiness

Current score: 68 / 100.

Recommended gate for public production: 85 / 100.

Minimum release blockers to resolve:

1. Fix morphology auth contract or frontend authentication.
2. Add schema serializers/annotations for all APIViews.
3. Preload or externalize FastText model service to avoid cold-start request failures.
4. Resolve historical data path mismatch.
5. Harden production TLS and replace sample secrets.
