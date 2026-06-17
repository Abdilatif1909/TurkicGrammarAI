# Morphology Scientific Audit

Audit date: 2026-06-17

Scope: `backend/apps/morphology`, `backend/data/morphology`, `backend/data/benchmark`, morphology tests, and related generated reports/data.

## Summary

The morphology analyzer is useful as a rule-based prototype, but its scientific metrics are not yet reliable enough for publication. The implementation mixes database rules, JSON fallback rules, heuristic scoring, language-specific vowel-harmony filters, derivational discovery, and request-time persistence. The biggest production blocker is that `apps.morphology.models` has no migrations.

## Findings

### 1. Morphology app has models but no migrations

- Files: `backend/apps/morphology/models.py`, `backend/apps/morphology/migrations`
- Endpoint: `/api/morphology/analyze/`, `/api/morphology/statistics/`
- Risk: critical
- Evidence: `python manage.py showmigrations morphology` returns `(no migrations)`, while models define `MorphologicalRule` and `MorphologicalAnalysis`.
- Recommendation: create and commit initial migrations for morphology.

### 2. Public analyze endpoint writes to database on GET

- File: `backend/apps/morphology/views.py`
- Endpoint: `GET /api/morphology/analyze/`
- Risk: high
- Evidence: `AnalyzeView.get()` calls `MorphologicalAnalysis.objects.create(...)`.
- Recommendation: make GET read-only. Move persistence to explicit POST or async analytics event with throttling.

### 3. Batch analysis stores wrong surface form

- File: `backend/apps/morphology/views.py`
- Endpoint: `POST /api/morphology/batch-analyze/`
- Risk: medium
- Evidence: `surface_form=top["lemma"]` is used instead of the original input word.
- Recommendation: iterate with original input word and store `surface_form=word`.

### 4. Analyzer depends on fallback JSON rules if DB unavailable

- File: `backend/apps/morphology/services/morphology_service.py`
- Risk: medium
- Evidence: `_load_rules()` catches DB errors and reads `backend/data/morphology/*_rules.json`.
- Recommendation: make source mode explicit and fail loudly in production if DB rules are expected but unavailable.

### 5. Scoring is heuristic

- File: `backend/apps/morphology/services/morphology_service.py`
- Risk: high for scientific claims
- Evidence: scoring adds/subtracts constants for curated/synthetic/long suffixes and harmony checks.
- Recommendation: document scoring as heuristic and evaluate against expert-reviewed held-out analyses.

### 6. Ambiguity handling exists but is shallow

- Files: `backend/apps/morphology/services/morphology_service.py`, `backend/apps/morphology/tests.py`
- Risk: medium
- Evidence: tests assert multiple analyses for examples like `yozuvchi`, but no calibrated ambiguity ranking or confidence interpretation is proven.
- Recommendation: add ambiguity benchmark with expected ranking.

### 7. Derivational morphology is under-specified

- Files: `backend/apps/morphology/services/derivational_service.py`, `backend/data/morphology/derivational_rules.json`
- Risk: medium-high
- Evidence: derivational rule inventory is very small compared with inflectional rule files.
- Recommendation: separate inflectional and derivational evaluation.

### 8. Benchmark integrity is not sufficient for publication

- Files: `backend/data/benchmark/*_morphology*.json`, `backend/data/benchmark/independent/*.json`, `backend/data/gold/gold_dataset_manifest.json`
- Risk: high
- Evidence: `gold_dataset_manifest.json` marks most "gold" morphology records as candidate/requires expert review.
- Recommendation: use only reviewed gold records for publication metrics.

## Which Metrics Are Trustworthy

Trustworthy for engineering regression:

- Unit tests passing: 92 backend tests passed with SQLite.
- Rule loading and basic suffix-chain behavior for selected examples.
- Selected vowel-harmony negative tests.

Not trustworthy as scientific accuracy:

- Metrics produced by synthetic/generated morphology benchmarks.
- Metrics where benchmark records are generated from the same rules/lemmas the analyzer uses.
- "Gold" metrics before expert review is completed.

## Recommendations

1. Add morphology migrations before any release.
2. Stop writing DB rows from GET.
3. Add reviewed gold morphology set per language.
4. Report exact-match root, lemma, suffix-chain, and feature accuracy separately.
5. Report ambiguity ranking quality: top-1, top-3, MRR.
6. Split synthetic regression benchmarks from scientific benchmarks.
7. Add provenance to every rule.

