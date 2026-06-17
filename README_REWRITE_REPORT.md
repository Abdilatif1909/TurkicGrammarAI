# README Rewrite Report

Date: 2026-06-17

Phase: 36 - GitHub README Rewrite

## Summary

`README.md` was rewritten from scratch to reflect the current codebase and the latest audit reports. The new README avoids unsupported claims and presents TurkicGrammarAI as an active research prototype rather than production-ready or publication-ready software.

## Sources Used

- `MASTER_AUDIT_REPORT.md`
- `API_CONSISTENCY_REPORT.md`
- `DATASET_AUDIT_V2.md`
- `MORPHOLOGY_SCIENTIFIC_AUDIT.md`
- `EMBEDDING_AND_RAG_AUDIT.md`
- `FRONTEND_PRODUCTION_AUDIT.md`
- `TESTING_GAP_REPORT.md`
- `SECURITY_AUDIT_REPORT.md`
- Current backend/frontend code and dataset files

## Outdated Sections Removed

- Old backend-foundation-only project description.
- Incomplete endpoint list that omitted current morphology, historical, embeddings, semantic search, RAG, QA, and analytics endpoints.
- Outdated dataset statistics from root-level `words_dataset_statistics.json`.
- Any wording implying production readiness without audit support.
- Any `/api/v1/` API contract references.

## Statistics Updated

Dataset statistics were recalculated from `backend/data/words/*.json`, excluding `manifest.json`.

Current verified values:

- Word records: 100,030
- Unique surface words: 96,940
- Unique language-word pairs: 100,030
- Unique lemmas: 32,776
- Unique roots: 32,776
- Supported language set: 8 languages

Per-file canonical counts:

- `uz`: 14,902
- `tr`: 14,905
- `az`: 11,903
- `kk`: 11,904
- `ky`: 11,905
- `tk`: 11,904
- `ug`: 11,679
- `otk`: 10,928

The README also notes the unresolved language-code normalization issue.

## Endpoint Corrections

The README now documents only the real `/api/` routes from the current URL configuration:

- `/api/auth/`
- `/api/words/`
- `/api/morphology/analyze/`
- `/api/morphology/universal-analyze/`
- `/api/cognates/`
- `/api/historical/`
- `/api/embeddings/`
- `/api/search/semantic/`
- `/api/rag/retrieve/`
- `/api/qa/ask/`
- `/api/feedback/`
- `/api/analytics/health/`
- `/api/admin/analytics/...`
- `/api/schema/`
- `/api/docs/`

The README explicitly states that `/api/v1/` is not implemented in the current URL configuration.

## Audit Alignment Summary

The rewritten README aligns with audit findings by:

- avoiding production-ready, Q1-ready, state-of-the-art, or human-level claims;
- separating engineering checks from scientific validation;
- marking morphology, embeddings, semantic search, RAG, and QA metrics as experimental unless independently validated;
- documenting benchmark leakage and synthetic data limitations;
- warning that expert-reviewed gold datasets are incomplete;
- documenting missing license status;
- warning about production security concerns around example env files, token storage, and public warm-start endpoints;
- listing near-term roadmap items that correspond to release blockers in `MASTER_AUDIT_REPORT.md`.

## Verification

No application code was changed. This phase only rewrote documentation.
