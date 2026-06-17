# TurkicGrammarAI

AI-Powered Platform for Comparative and Historical Turkic Linguistics

TurkicGrammarAI is a research-oriented web platform for working with Turkic lexical, morphological, cognate, historical, embedding, retrieval, and question-answering data. The project combines a Django REST backend, a React/Vite frontend, curated and generated linguistic datasets, rule-based morphology, FastText-based embeddings, semantic search, RAG-style retrieval, and a template-based QA layer.

This repository is under active development. Current functionality is suitable for experimentation, reproducible engineering tests, and research prototyping. It should not yet be described as production-ready, state-of-the-art, Q1-ready, or fully scientifically validated.

## Overview

The platform currently includes:

- Morphology: rule-based analyzers for Turkic word forms, including suffix-chain analysis and selected vowel-harmony checks.
- Cognates: cross-language cognate sets and search utilities for related forms across Turkic languages.
- Historical forms: historical lineage data and endpoints for tracing modern forms back through older stages.
- Embeddings: FastText model artifacts and embedding datasets built from available linguistic resources.
- Semantic search: indexed lookup over words, lemmas, roots, cognate groups, and historical metadata.
- RAG retrieval: retrieval over semantic, morphology, cognate, historical, and dictionary-like evidence.
- QA: retrieval-based structured answers with internal source traces.
- Analytics: feedback and admin-oriented usage/QA monitoring endpoints.

## Architecture Diagram

```text
Words Dataset
    |
    v
Morphology
    |
    v
Cognates
    |
    v
Historical Forms
    |
    v
Embeddings
    |
    v
Semantic Search
    |
    v
RAG Retrieval
    |
    v
QA System
```

## Supported Languages

| Code | Language |
| --- | --- |
| `uz` | Uzbek |
| `tr` | Turkish |
| `az` | Azerbaijani |
| `kk` | Kazakh |
| `ky` | Kyrgyz |
| `tk` | Turkmen |
| `ug` | Uyghur |
| `otk` | Old Turkic |

## Current Dataset Statistics

The numbers below were recalculated from `backend/data/words/*.json` and exclude `manifest.json`.

| Metric | Current value |
| --- | ---: |
| Word records | 100,030 |
| Unique surface words | 96,940 |
| Unique language-word pairs | 100,030 |
| Unique lemmas | 32,776 |
| Unique roots | 32,776 |
| Supported language set | 8 languages |

Records by canonical file:

| Code | Records |
| --- | ---: |
| `uz` | 14,902 |
| `tr` | 14,905 |
| `az` | 11,903 |
| `kk` | 11,904 |
| `ky` | 11,905 |
| `tk` | 11,904 |
| `ug` | 11,679 |
| `otk` | 10,928 |

Known data issue: some raw records still mix full language names and language codes internally. The canonical supported language codes are listed above, but dataset normalization is still an open task.

## Main Features

### Morphology Analyzer

Rule-based morphology endpoints analyze roots, lemmas, suffix chains, and ranked candidate analyses. The analyzer is useful for regression tests and exploratory linguistic workflows, but its scores are heuristic and require additional expert-reviewed validation.

### Cross-Language Cognates

Cognate endpoints expose cognate sets, statistics, direct search, and universal search across supported Turkic languages.

### Historical Evolution

Historical endpoints provide list/search/statistics/evolution views over historical form data.

### FastText Embeddings

The backend includes FastText model loading, similarity, nearest-neighbor, status, and warm-start utilities. Model warm-up is important before serving embedding-dependent traffic.

### Semantic Search

Semantic search combines indexed lexical, morphological, cognate, and historical metadata. Current ranking is deterministic and heuristic.

### RAG Retrieval

RAG retrieval returns structured evidence documents with source types, source IDs, component scores, and confidence-like values. These values are ranking signals, not calibrated scientific probabilities.

### Question Answering

The QA layer is retrieval-based and template-driven. It returns answer text, answer items, citations, and support documents. It is not an LLM-based research assistant.

### Analytics

Analytics endpoints support user feedback, QA error logging, admin usage statistics, most requested words/languages, and analytics health.

## API Overview

The current implemented API uses `/api/`. There is no implemented `/api/v1/` prefix in the current URL configuration.

Core endpoint groups:

| Area | Real endpoints |
| --- | --- |
| Auth | `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/refresh/`, `GET/PATCH /api/auth/profile/` |
| Words | `GET /api/words/`, `GET /api/words/search/`, `GET /api/words/statistics/`, `GET /api/words/quality/`, `GET /api/words/<uuid:id>/` |
| Morphology | `GET /api/morphology/analyze/`, `GET /api/morphology/universal-analyze/`, `POST /api/morphology/batch-analyze/`, `GET /api/morphology/statistics/` |
| Cognates | `GET /api/cognates/`, `GET /api/cognates/search/`, `GET /api/cognates/universal-search/`, `GET /api/cognates/statistics/`, `GET /api/cognates/<uuid:pk>/` |
| Historical | `GET /api/historical/`, `GET /api/historical/search/`, `GET /api/historical/statistics/`, `GET /api/historical/evolution/`, `GET /api/historical/<int:pk>/` |
| Embeddings | `GET /api/embeddings/similarity/`, `GET /api/embeddings/neighbors/`, `GET /api/embeddings/warm/`, `GET /api/embeddings/status/` |
| Semantic search | `GET /api/search/semantic/?q=<query>` |
| RAG retrieval | `GET /api/rag/retrieve/?q=<query>` |
| QA | `GET /api/qa/ask/?q=<question>` |
| Analytics | `POST /api/feedback/`, `GET /api/analytics/health/`, `GET /api/admin/analytics/usage/`, `GET /api/admin/analytics/qa-trends/`, `GET /api/admin/analytics/most-requested-words/`, `GET /api/admin/analytics/most-requested-languages/` |
| Schema | `GET /api/schema/`, `GET /api/docs/` |

Admin endpoints under `/api/admin/*` require authenticated admin/super-admin access.

## Installation

### Backend

Create and activate a Python environment, then install dependencies:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

For Unix-like shells, use:

```bash
source venv/bin/activate
```

Run Django checks and tests:

```bash
python manage.py check
python manage.py test
```

### Frontend

```bash
cd frontend
npm install
npm run build
```

Development server:

```bash
npm run dev
```

### Docker

For local Docker development:

```bash
docker compose up --build
```

The production compose file exists, but do not deploy directly with example environment files. Replace example values with real secrets and deployment-specific settings before any public deployment.

### Environment Variables

Common backend variables:

- `DJANGO_SETTINGS_MODULE`
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`
- `DATABASE_URL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

Useful local-only variable:

- `USE_SQLITE=True`

Frontend variable:

- `VITE_API_BASE_URL`

## Development Setup

### Local Development With SQLite

SQLite mode is useful for quick checks and tests:

```bash
cd backend
set USE_SQLITE=True
python manage.py check
python manage.py test
python manage.py runserver
```

PowerShell:

```powershell
cd backend
$env:USE_SQLITE = "True"
python manage.py check
python manage.py test
python manage.py runserver
```

### PostgreSQL Mode

Use PostgreSQL through Docker or provide a `DATABASE_URL` pointing to a running PostgreSQL instance:

```bash
DATABASE_URL=postgres://user:password@localhost:5432/turkicgrammarai
python manage.py migrate
python manage.py runserver
```

### FastText Warm-Start

Embedding-dependent endpoints can be slow on cold start. Warm the model before routing user traffic:

```bash
curl http://127.0.0.1:8000/api/embeddings/warm/
curl http://127.0.0.1:8000/api/embeddings/status/
```

Security note: audit reports recommend protecting warm-start operational endpoints before public deployment.

## Project Structure

```text
TurkicGrammarAI/
  backend/
    apps/
      accounts/
      analytics/
      cognates/
      corpus/
      core/
      embeddings/
      historical/
      languages/
      morphology/
      words/
    config/
    data/
      benchmark/
      cognates/
      embeddings/
      gold/
      historical/
      morphology/
      normalized/
      reports/
      words/
    models/
  frontend/
    src/
      pages/
      services/
    dist/
  data/
  paper_package/
    analysis/
    figures/
    reports/
    tables/
    validation/
  infra/
    nginx.conf
  scripts/
  *_REPORT.md
```

There is no dedicated top-level `reports/` directory in the current repository. Most audit/report Markdown files are stored at the repository root, while generated backend data reports live under `backend/data/reports/`.

## Research Reproducibility Package

`paper_package/` is the manuscript and reviewer reproducibility package. It should remain tracked in Git because it contains compact, publication-facing evidence generated for manuscript preparation and validation.

- `paper_package/figures/`: manuscript figures in PNG and SVG formats.
- `paper_package/tables/`: manuscript tables in CSV, Markdown, and LaTeX formats.
- `paper_package/analysis/`: statistical analysis, ablation notes, and embedding error analysis.
- `paper_package/validation/`: figure/table validation, metric traceability, reviewer questions, threats to validity, and publication evidence reports.
- `paper_package/reports/`: paper data summaries and package-level documentation.

These files were generated from the repository's research artifacts for manuscript drafting, validation, and reviewer inspection. They document evidence and traceability; they do not modify algorithms, datasets, models, or evaluation results.

## Scientific Evaluation

### Validated Engineering Checks

The latest audit verified:

- `python manage.py check` passed in SQLite mode.
- `python manage.py test` passed with 92 backend tests.
- `npm run build` passed for the React frontend.

These are engineering checks, not scientific accuracy claims.

### Experimental Components

The following components are implemented but should be interpreted cautiously:

- Rule-based morphology ranking and confidence scores.
- FastText similarity and nearest-neighbor outputs.
- Semantic search ranking.
- RAG retrieval relevance scores.
- QA answer construction and internal citations.

### Synthetic Benchmark Status

Some benchmark and evaluation files are generated from the same datasets or semantic index used by the system. These are useful for regression testing, but they are not independent scientific validation.

### Gold Dataset Status

The current `backend/data/gold/gold_dataset_manifest.json` marks many records as candidates requiring expert review. Expert-reviewed gold datasets are incomplete and should be completed before publication-level claims.

### Reviewer Reproducibility

Reviewers can reproduce the current evaluation artifacts from the committed code and data. The commands below assume dependencies are installed from `backend/requirements.txt` and run from `backend/` unless noted.

- Morphology evaluation: run the relevant Django management commands in `backend/apps/morphology/management/commands/`, including `evaluate_uzbek_morphology`, `evaluate_cross_language_morphology`, and the language-specific morphology evaluators. Compare outputs with root-level morphology reports and `backend/data/benchmark/`.
- Cognate evaluation: run `python manage.py evaluate_cognate_alignment` and compare with `COGNATE_ALIGNMENT_REPORT.md`, `COGNATE_AWARE_EMBEDDING_REPORT.md`, and `backend/data/benchmark/cross_language_cognate_benchmark.json`.
- Embedding evaluation: run the embedding evaluation modules in `backend/apps/embeddings/`, especially `evaluate_fasttext_embeddings.py` and `evaluate_embedding_quality.py`, using the local FastText artifacts or regenerated embeddings as configured.
- Semantic search evaluation: run `backend/apps/embeddings/evaluate_semantic_search.py` and compare with `SEMANTIC_SEARCH_REPORT.md` and `backend/data/embeddings/semantic_search_benchmark.json`.
- RAG evaluation: run `backend/apps/embeddings/evaluate_rag_retrieval.py` and compare with `TURKIC_RAG_REPORT.md` and `backend/data/embeddings/rag_retrieval_benchmark.json`.
- QA evaluation: run `backend/apps/embeddings/evaluate_turkic_qa.py` and compare with `TURKIC_QA_REPORT.md`, `backend/data/embeddings/qa_benchmark.json`, and `backend/data/gold/gold_qa_dataset.json`.

The `paper_package/validation/` reports provide reviewer-facing traceability for manuscript tables, figures, metric classification, and known threats to validity.

## Current Limitations

- API documentation and generated OpenAPI need to be regenerated and kept aligned with the real `/api/` routes.
- `backend/apps/morphology/models.py` currently has no committed migrations.
- `GET /api/morphology/analyze/` currently persists a top analysis, so it has a GET side effect that should be removed or moved to an explicit write endpoint.
- Language identifiers in raw word data are not fully normalized.
- Some datasets include generated or projected records that need clearer provenance.
- Benchmark leakage risk exists in semantic search, RAG, and QA evaluations.
- External validation and expert-reviewed gold datasets are still needed.
- Frontend tests and end-to-end tests are not yet present.
- GitHub Actions workflows were not found during the latest local audit.
- Production deployment requires security hardening, especially environment secrets, token storage, and expensive public endpoints.

## Roadmap

### Near-Term Goals

- Add morphology migrations and migration checks.
- Remove write side effects from GET endpoints.
- Regenerate and validate OpenAPI from current code.
- Normalize dataset language codes.
- Regenerate dataset statistics from canonical data.
- Add CI for backend tests, frontend build, migrations, OpenAPI, and data validation.
- Protect operational endpoints such as FastText warm-start.
- Add frontend tests and Playwright smoke checks.

### Long-Term Goals

- Build expert-reviewed gold datasets for morphology, cognates, historical forms, and QA.
- Separate synthetic regression benchmarks from scientific evaluation benchmarks.
- Add item-level provenance, citations, license metadata, and reviewer status.
- Create independent held-out benchmarks for semantic search, RAG, and QA.
- Improve morphology ambiguity ranking and derivational analysis evaluation.
- Add calibrated retrieval metrics and source-level evaluation.
- Expand contributor documentation and scientific reproducibility workflows.

## Citation

If you use this repository in academic work, cite the repository and the exact commit hash used for experiments. A formal citation will be added once the dataset and evaluation protocol are stabilized.

```bibtex
@software{turkicgrammarai,
  title = {TurkicGrammarAI: AI-Powered Platform for Comparative and Historical Turkic Linguistics},
  author = {TurkicGrammarAI contributors},
  year = {2026},
  url = {https://github.com/Abdilatif1909/TurkicGrammarAI},
  note = {Research prototype. Cite the exact commit used.}
}
```

## License

No license file was found during the latest audit. Add a repository license before public reuse, redistribution, or external publication workflows.

## Contributors

Contributions are welcome, especially in:

- Turkic language data curation
- expert review of morphology/cognate/historical datasets
- Django API hardening
- React frontend testing
- independent NLP evaluation
- documentation and reproducibility

Before contributing new features, prioritize audit blockers: migrations, API consistency, dataset provenance, independent evaluation, CI, and security hardening.
