**Project Health Report**

- **Project:** TurkicGrammarAI
- **Date:** 2026-06-06
- **Verifier:** GitHub Copilot (GPT-5 mini)

**Summary**
- **Status:** Corpus and Cognates apps scaffolded, migrations created, and app-level tests passed locally using SQLite (`USE_SQLITE=1`). OpenAPI generated but with multiple serializer-guessing warnings. Postgres/Celery/Redis runtime verification not performed.
# **Status:** Corpus and Cognates apps scaffolded, migrations created, and app-level tests passed locally using SQLite (`USE_SQLITE=1`).
# **OpenAPI Status:** CLEAN (validated, 0 warnings, 0 errors)

**What I ran**
- **System checks:** `python backend/manage.py check` — no issues.
- **Migrations (dry-run):** `python backend/manage.py makemigrations --check --dry-run` — no changes detected.
- **Migrations applied (local verification):** Applied using SQLite via `USE_SQLITE=1`.
- **Tests:** App-level tests for `apps.corpus` and `apps.cognates` executed and passed when run directly. Top-level `python backend/manage.py test` returned 0 discovered tests in one run (project-level discovery vs per-app invocation discrepancy).
- **OpenAPI:** `drf_spectacular` used to generate `backend/openapi_generated.yaml`; reported multiple "unable to guess serializer" messages for several APIViews (48 errors, 12 unique messages).
- **OpenAPI:** `drf_spectacular` used to generate `backend/openapi_generated.yaml`; validation re-run after fixes — `spectacular --validate` reports 0 warnings and 0 errors. OpenAPI updated.

**Current State (files changed/added)**
- **Corpus app:** [backend/apps/corpus](backend/apps/corpus) (models, services, management commands, tests, README).
- **Cognates app:** [backend/apps/cognates](backend/apps/cognates) (models, services, seed command, tests, README, data generator and `backend/data/cognates/cognates.json`).
- **Settings:** [backend/config/settings/base.py](backend/config/settings/base.py) updated to include the apps.
- **URLs:** [backend/config/urls.py](backend/config/urls.py) updated with `api/corpus/` and `api/cognates/` routes.

**Issues & Notes**
- **Postgres unavailable locally:** Initial `migrate` failed due to `psycopg2.OperationalError`; resolved local verification using SQLite. Recommend running migrations against a real Postgres instance before production deploy.
- **OpenAPI warnings:** Many APIViews lack an explicit `serializer_class` or `@extend_schema` annotations. This prevents drf_spectacular from inferring complete schemas. Recommend adding `serializer_class` or `@extend_schema(request/response=...)` to those views.
- **Migration formatting on Windows:** A `makemigrations` formatting subprocess produced an OSError (WinError 4551) in one run — environment-specific. Re-running succeeded and migrations were created.
- **Top-level test discovery:** `manage.py test` returned 0 tests in one invocation; however per-app tests ran and passed. Consider confirming test discovery patterns (test labels, `TEST_RUNNER`, or test naming) if you expect a non-zero top-level run.
- **Redis/Celery not exercised:** Celery settings exist but workers and broker connectivity were not verified here.

**Recommendations / Next Steps**
- **OpenAPI fixes:** Add `serializer_class` or `@extend_schema` annotations to APIViews flagged by drf_spectacular to remove warnings and produce a richer schema.
- **Run migrations on Postgres:** Start a local Postgres container (see `infra/postgres`) or provide credentials to run `migrate` in a staging environment and validate data migrations.
- **Verify Celery/Redis:** Start Redis and a Celery worker; run a sample task to confirm broker connectivity and task routing.
- **Consolidate tests:** Ensure project-wide test discovery picks up all tests (check `tests` module naming, `TEST_DISCOVERY_ROOT`, or `pytest`/`tox` config if used). Optionally run `python backend/manage.py test apps` for a full per-app run.
- **CI checks:** Add a CI job that runs: `manage.py check`, `makemigrations --check --dry-run`, `migrate` (against test DB), `manage.py test`, and `drf_spectacular --validate` to catch regressions.

**Priority Action Items (short)**
- **P1:** Fix OpenAPI serializer warnings.
- **P2:** Run migrations on Postgres and verify seed commands in that environment.
- **P3:** Run integration tests with Celery + Redis running.

**If you want, I can:**
- Run targeted fixes for drf_spectacular warnings (annotate views and re-generate schema).
- Attempt to run migrations against a Postgres container (I can start one via `docker-compose up -d postgres` if you want).

**Contact points (key files)**
- Settings: [backend/config/settings/base.py](backend/config/settings/base.py)
- URLs: [backend/config/urls.py](backend/config/urls.py)
- Corpus app: [backend/apps/corpus](backend/apps/corpus)
- Cognates app: [backend/apps/cognates](backend/apps/cognates)
- Generated OpenAPI (output): [backend/openapi_generated.yaml](backend/openapi_generated.yaml)

---
Generated automatically from the verification run on 2026-06-06.


**Temporary Verification Workarounds**

- **Script-level cache override:** For local verification runs the verification script `scripts/api_verification.py` temporarily overrides the project's `CACHES` setting to use Django's in-memory cache (`django.core.cache.backends.locmem.LocMemCache`). Reason: the development settings use Redis (`redis://localhost:6379`) and a Redis instance is not guaranteed to be available on every developer machine or CI environment used for quick checks. This override is applied only inside the verification script before `django.setup()` and does not modify repository settings files.

- **Test client Host header:** The verification script forces the test client's Host header to `localhost` (via `HTTP_HOST='localhost'`) to avoid `DisallowedHost` exceptions when running the Django test client in this environment.

These workarounds are intentionally scoped to the verification script and are safe for local checks. Recommended next steps:

- If you prefer verification against real infra, start Redis locally (or via `docker-compose up -d redis`) and remove the script-level override so the verification exercise uses the production-like cache backend.
- Keep the script override while running quick local verifications; document it in the repository README or CI scripts if desired.

**Historical Forms Engine Status**

- **Integrated:** `apps.historical` added to `INSTALLED_APPS`; migrations created and applied; routes exposed under `api/historical/`.
- **Seeding:** `seed_historical` generates a 2000-record synthetic dataset when a curated dataset is missing or degenerate; the command writes the regenerated JSON to `backend/data/historical/historical_forms.json` for reproducibility. The import path uses batched `bulk_create` with a per-object fallback for compatibility.
- **API verification:** Historical endpoints (list, detail, search, evolution, statistics) were exercised by the verification script and responded as expected in local verification runs.
- **Logging:** Temporary debug prints introduced during development were removed or reduced; only the final seeding summary remains.
- **Recommendation:** Replace the synthetic dataset with a curated `historical_forms.json` before production use, or add a `--force-regenerate` flag for controlled regeneration.

## Morphology Engine (Phase 6)

- **Status:** Initial Uzbek implementation completed and integrated as `apps.morphology`.
- **Capabilities:** Backtracking analyzer that returns ranked analyses with detailed suffix objects (suffix, type, confidence). Seed command (`seed_morphology`) auto-generates Uzbek rules up to 500+ if the source JSON is incomplete.
- **Next steps:** Expand Uzbek rules with linguistically validated entries and examples; implement UI/administration for rule curation; port rules to other Turkic languages.

## Uzbek Morphology v1 Milestone

- **Date:** 2026-06-08
- **Status:** Stable v1 milestone documented after multi-analysis evaluation alignment, derivational morphology support, and rule completion sprint.
- **Coverage:** 100.0%
- **Top1:** 27.8%
- **Top3:** 52.4%
- **AnyMatch:** 79.2%
- **RULE_MISSING:** 43
- **Validation:** `python backend\manage.py validate_uzbek_morphology` passed from the project root.
- **Tests:** `python manage.py test` passed from `backend` with 76 tests.
- **System check:** `python manage.py check` passed from `backend`.

Milestone reports:

- `RULE_COMPLETION_REPORT.md`
- `MULTI_ANALYSIS_EVALUATION_REPORT.md`
- `DERIVATIONAL_MORPHOLOGY_REPORT.md`
