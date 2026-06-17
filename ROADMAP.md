# Roadmap

This roadmap is scoped to repository hardening, reproducibility, and scientific release readiness. It intentionally avoids unsupported production-ready or Q1-ready claims.

## Near Term

- Add committed migrations for `backend/apps/morphology`.
- Remove write side effects from `GET /api/morphology/analyze/`.
- Regenerate OpenAPI from current code and keep it checked in.
- Normalize language codes in word and embedding datasets.
- Regenerate dataset statistics from canonical files.
- Add CI for backend checks, tests, migration validation, frontend build, and OpenAPI validation.
- Protect operational endpoints such as `/api/embeddings/warm/`.
- Add frontend unit tests and Playwright smoke checks.

## Scientific Readiness

- Separate synthetic regression benchmarks from scientific evaluation sets.
- Build expert-reviewed gold datasets for morphology, cognates, historical forms, retrieval, and QA.
- Add item-level provenance, source citations, license metadata, and reviewer status.
- Create held-out benchmarks that are not generated from `semantic_index.json`.
- Report morphology metrics by root, lemma, suffix chain, feature set, ambiguity rank, and language.

## Release Engineering

- Decide whether large model artifacts are stored in Git LFS, GitHub Releases, or an external archive.
- Add a public license before broad reuse or publication.
- Add dependency and secret scanning in CI.
- Add Docker production smoke tests.
- Keep documentation source-of-truth files indexed in `docs/INDEX.md`.

## Long Term

- Improve morphology ambiguity ranking after reviewed benchmarks exist.
- Expand validated corpora and provenance-backed lexical sources.
- Add calibrated retrieval metrics and source-level retrieval evaluation.
- Prepare a paper package with frozen commit hash, manifests, and reproducibility scripts.
