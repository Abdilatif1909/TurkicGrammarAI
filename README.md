# TurkicGrammarAI

TurkicGrammarAI is a research-oriented platform for comparative and historical Turkic linguistics. It combines a Django REST API, a React/Vite client, curated lexical resources, rule-based morphology, cognate and historical-lineage metadata, FastText embeddings, semantic retrieval, RAG-style evidence retrieval, and structured question answering.

The project is intended for reproducible engineering experiments and research prototyping. The current benchmark results are internal measurements and should not be treated as externally validated linguistic accuracy or production readiness.

## Scope

- Compare lexical forms across Uzbek, Turkish, Azerbaijani, Kazakh, Kyrgyz, Turkmen, Uyghur, and Old Turkic.
- Analyze roots, lemmas, suffix chains, and selected morphology rules.
- Search cognate sets and historical forms.
- Train and query FastText embeddings.
- Expose semantic search, RAG retrieval, and structured QA endpoints.
- Preserve source-type traces for retrieved evidence.

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

The current research package contains 100,030 lexical records across eight languages. The embedding dataset derived from the repository sources contains 100,000 training records; these are related but distinct counts and should not be conflated.

| Metric | Value |
| --- | ---: |
| Total lexical records | 100,030 |
| Unique surface forms | 96,940 |
| Unique lemmas | 26,797 |
| Unique roots | 26,798 |
| Supported languages | 8 |

Embedding resource coverage includes 75,429 records with morphology features, 23,018 records with cognate-group assignments, and 25,018 records with historical lineage metadata.

## Validated Results

Validation date: **2026-08-20**.

The backend test suite passed completely in SQLite mode:

```text
Ran 92 tests in 24.504s
OK
```

The same 5,000-pair embedding benchmark was used for both models:

| Metric | Vanilla FastText baseline | Cognate-aware model |
| --- | ---: | ---: |
| Top-1 accuracy | 15.62% | 40.80% |
| Top-5 accuracy | 25.83% | 73.66% |
| Top-10 accuracy | 35.49% | 86.06% |
| Mean cosine similarity | 0.462310 | 0.577844 |
| Positive pair similarity | 0.452783 | 0.595108 |
| Negative pair similarity | 0.520538 | 0.472318 |
| Separation margin | -0.067755 | 0.122790 |

The vanilla baseline was trained on 100,000 records with vector size 300, window 5, minimum count 1, 20 epochs, and four workers. The baseline training completed in 46.727 seconds in the recorded environment.

## Interpretation Warnings

The benchmark is not an independent gold-standard evaluation. Several semantic-search, RAG, QA, and embedding resources share provenance with training data or are generated from the same repository index. This creates benchmark leakage risk and can inflate internal retrieval results.

The current gold-data manifests contain candidate records requiring expert review. Expert-reviewed gold datasets for morphology, cognates, historical relations, and QA are incomplete. The reported figures therefore support reproducibility and regression comparison, not broad claims of linguistic generalization or superiority over external systems.

## Installation

### Local Python and SQLite

Python 3.11 is recommended for the scientific dependencies, including `gensim`. Python 3.14 is not required to be removed if it is installed separately.

PowerShell:

```powershell
py -3.11 -m venv venv311
.\venv311\Scripts\python.exe -m pip install -r backend\requirements.txt
$env:USE_SQLITE = "1"
Set-Location backend
..\venv311\Scripts\python.exe manage.py migrate
..\venv311\Scripts\python.exe manage.py check
..\venv311\Scripts\python.exe manage.py test
```

To run the API locally:

```powershell
$env:USE_SQLITE = "1"
..\venv311\Scripts\python.exe manage.py runserver
```

To build the frontend:

```powershell
Set-Location frontend
npm install
npm run build
npm run dev
```

### Docker Compose

Copy the example environment file, review all secrets and hosts, then start the services:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Do not expose the example credentials or development settings publicly. PostgreSQL, Redis, Celery, the Django API, and the frontend should be configured for the target deployment before use outside local development.

## Reproducibility Commands

Build the embedding dataset from committed lexical sources:

```powershell
Set-Location backend
..\venv311\Scripts\python.exe -c "from apps.embeddings.embedding_dataset_builder import build_embedding_dataset; build_embedding_dataset()"
```

Train the vanilla baseline from the repository root:

```powershell
..\venv311\Scripts\python.exe backend\apps\embeddings\train_baseline_fasttext.py --workers 4
```

The publication figures are regenerated from the committed table values at publication resolution with:

```powershell
..\venv311\Scripts\python.exe scripts\regenerate_publication_figures.py
```

The paper package figures are stored in `paper_package/figures/`; the manuscript draft with updated embedded figures is `paper_draft/paper_fixed_v2.docx`.

## API Overview

The Django API is served under `/api/`:

- `/api/words/`
- `/api/morphology/`
- `/api/cognates/`
- `/api/historical/`
- `/api/embeddings/`
- `/api/search/semantic/`
- `/api/rag/retrieve/`
- `/api/qa/ask/`
- `/api/schema/`
- `/api/docs/`

Operational endpoints such as embedding warm-start should be protected before public deployment.

## Data and Code Availability

The source code and tracked research package are available at:

<https://github.com/Abdilatif1909/TurkicGrammarAI>

A Zenodo archive and DOI have **not yet been created**. The GitHub repository must first be connected to Zenodo and a versioned GitHub Release must be published by an authenticated repository owner. After that release exists, replace this paragraph with the minted DOI in both the paper and this README, for example:

```text
The datasets and code used in this study are archived at Zenodo:
https://doi.org/10.5281/zenodo.XXXXXXX (also available at
https://github.com/Abdilatif1909/TurkicGrammarAI).
```

## License Status

No `LICENSE` file is currently present in the repository. Before redistribution or formal publication, the maintainers should choose and add a license. MIT is a practical permissive option for code; Apache-2.0 is another option when explicit patent terms are desired. This README does not grant a license.

## Repository Layout

```text
backend/          Django project, apps, datasets, models, and tests
frontend/         React/Vite client
paper_package/    figures, tables, analyses, and validation reports
paper_draft/      manuscript drafts
scripts/          reproducibility and verification scripts
data/             auxiliary historical and research data
```

## Citation

```bibtex
@software{turkicgrammarai,
  title = {TurkicGrammarAI: AI-Powered Platform for Comparative and Historical Turkic Linguistics},
  author = {Meyliyev, Abdilatif and contributors},
  year = {2026},
  url = {https://github.com/Abdilatif1909/TurkicGrammarAI},
  note = {Research prototype; cite the exact commit used.}
}
```

Use the exact Git commit associated with any reported experiment. The repository is an active research prototype, and independent expert review, source-separated benchmarks, provenance metadata, CI, and deployment hardening remain future work.
