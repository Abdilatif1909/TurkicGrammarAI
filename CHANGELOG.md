# Changelog

All notable repository-level changes are documented here.

## Unreleased

- Rewrote `README.md` for public GitHub and research-review audiences.
- Added audit-aligned release preparation documents.
- Added dataset, model, documentation, reproducibility, and GitHub release reports.
- Added `.gitignore` for Python, Django, Node, logs, local DBs, and generated frontend artifacts.
- Aligned root `requirements.txt` with the backend dependency set used by the current codebase.
- Added `gunicorn`, `gensim`, `numpy`, `scipy`, and `smart_open` to dependency manifests for deployment and embedding code paths.
- Updated `docker-compose.prod.yml` to use `.env.production` instead of `.env.production.example`.
- Set `SECURE_SSL_REDIRECT=True` in `.env.production.example`.
- Replaced roadmap with audit-aligned release and scientific-readiness milestones.

## 0.1.0-research-preview

- Initial public research-preview preparation target.
- Django REST backend with apps for accounts, languages, words, morphology, cognates, historical data, embeddings, corpus statistics, and analytics.
- React/Vite frontend for QA, morphology, cognates, semantic search, historical retrieval, and analytics views.
- FastText-based embedding assets and retrieval datasets.
