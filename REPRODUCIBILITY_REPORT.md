# Reproducibility Report

Generated for Phase 36.5 release preparation on 2026-06-17.

## Scope

This report verifies setup and repeatability for the current repository state without changing algorithms or evaluation results.

## Backend Setup

Recommended local setup:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py check
python manage.py test
```

Unix-like shells:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py test
```

SQLite quick mode:

```powershell
cd backend
$env:USE_SQLITE = "True"
python manage.py check
python manage.py test
```

PostgreSQL mode:

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Use `DATABASE_URL` or the `POSTGRES_*` variables from `.env.example`.

## Frontend Setup

```bash
cd frontend
npm install
npm run build
npm run dev
```

The frontend uses Vite. `VITE_API_BASE_URL` can be set for non-proxy deployments.

## Docker Setup

Development:

```bash
docker compose up --build
```

Production-style compose:

```bash
cp .env.production.example .env.production
# edit .env.production before deployment
docker compose -f docker-compose.prod.yml up --build
```

`docker-compose.prod.yml` now expects `.env.production` instead of `.env.production.example`.

## FastText Warm-Start

Embedding-dependent paths should be warmed before serving traffic:

```bash
curl http://127.0.0.1:8000/api/embeddings/warm/
curl http://127.0.0.1:8000/api/embeddings/status/
```

Security note: public deployment should protect warm-start operational endpoints.

## Validation Results

Commands run during Phase 36.5:

| Command | Working directory | Result |
| --- | --- | --- |
| `python manage.py check` | `backend/` | Passed: no issues |
| `python manage.py test` | `backend/` | Passed: 92 tests |
| `npm run build` | `frontend/` | Passed: Vite build completed |

README link check:

- `README.md` contains no local markdown links requiring file-resolution checks.

## Reproducibility Notes

- The root `requirements.txt` and `backend/requirements.txt` are aligned for the current backend and embedding code paths.
- `gensim`, `numpy`, `scipy`, `smart_open`, and `gunicorn` are included because they are required by embedding/model loading and production serving paths.
- `frontend/dist/`, logs, local SQLite databases, virtual environments, and dependency folders are ignored by `.gitignore`.
- Large FastText model artifacts are present under `backend/models/`; release policy should decide Git LFS, GitHub Release assets, or external archival storage.

## Known Reproducibility Risks

- `backend/apps/morphology` has models but no committed migrations.
- Some benchmark files are generated from project datasets/indexes and should not be treated as independent scientific validation.
- `.env.production` must be created manually from `.env.production.example`.
- No GitHub Actions workflow is currently present.
