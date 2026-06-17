# GitHub Release Report

Generated for Phase 36.5 release preparation on 2026-06-17.

## Repository Status

Status: prepared for a public research-preview release, with known limitations.

Completed release-preparation work:

- Rewrote public README in Phase 36.
- Added `.gitignore`.
- Cleaned local logs, pid files, SQLite DB, Python bytecode, and post-validation generated artifacts.
- Added release documents: `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and updated `ROADMAP.md`.
- Added `docs/INDEX.md`.
- Added `DATASET_MANIFEST.md`.
- Added `MODEL_MANIFEST.md`.
- Added `REPRODUCIBILITY_REPORT.md`.
- Updated `docker-compose.prod.yml` to use `.env.production`.
- Updated `.env.production.example` to default `SECURE_SSL_REDIRECT=True`.
- Sanitized local absolute paths in public-facing reports/scripts where they were not evaluation metrics.
- Replaced example local passwords with placeholder values.

## Dataset Status

Canonical dataset inventory is documented in `DATASET_MANIFEST.md`.

Current word dataset summary:

- Word records: 100,030
- Unique surface words: 96,940
- Unique lemmas: 32,776
- Unique roots: 32,776
- Supported language set: `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, `otk`

Known dataset limitations:

- Raw language identifiers still require full normalization.
- Normalized Uyghur clean file is missing.
- Some records are generated or projected and require clearer provenance.
- Expert-reviewed gold datasets are incomplete.

## Model Status

Model inventory is documented in `MODEL_MANIFEST.md`.

FastText artifacts are present under `backend/models/`. They are large, especially `turkic_fasttext.model.wv.vectors_ngrams.npy` at about 2.4 GB. A public release should decide whether these stay in Git, move to Git LFS, or become GitHub Release/external archive assets.

## Documentation Status

Current documentation entry point:

- `README.md`
- `docs/INDEX.md`

Release docs added:

- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `ROADMAP.md`
- `DATASET_MANIFEST.md`
- `MODEL_MANIFEST.md`
- `REPRODUCIBILITY_REPORT.md`

Legacy root reports remain as historical artifacts and are indexed separately. They are not the current source of truth unless confirmed against code and current manifests.

## Security And Public Repository Review

Scan findings:

- No private key material or real API tokens were found.
- Template environment variables remain in `.env.example` and `.env.production.example`.
- Local absolute paths were sanitized in scripts/reports where practical.
- Logs, local databases, pid files, generated frontend build output, dependency folders, and virtual environments are ignored.

Known security limitations:

- Frontend stores JWT tokens in localStorage.
- Public expensive endpoints need stronger protection before production deployment.
- Production secrets must be supplied through `.env.production` or a secret manager.

## Validation

Commands executed:

- `python manage.py check`: passed.
- `python manage.py test`: passed, 92 tests.
- `npm run build`: passed.
- README local link check: no missing local markdown links.

## Known Limitations

- Morphology app has models but no committed migrations.
- `GET /api/morphology/analyze/` still has a database write side effect.
- OpenAPI should be regenerated from the current URL configuration.
- No GitHub Actions workflow is present.
- Scientific validation remains incomplete.
- Synthetic benchmark limitations and benchmark leakage risks remain documented.
- No repository license file was found.

## Publication Readiness

Ready for:

- public GitHub research-preview release;
- paper package planning;
- reproducibility documentation baseline;
- contributor onboarding for cleanup, validation, and scientific review.

Not yet ready for:

- production deployment claims;
- Q1 publication-level claims;
- state-of-the-art claims;
- final scientific benchmark reporting.

## Recommended Release Metadata

Recommended commit message:

```text
Prepare repository for public research preview
```

Recommended Git tag:

```text
v0.1.0-research-preview
```

## Final Assessment

The repository is prepared for public GitHub release as a research preview, provided the known limitations are clearly retained in the README and release notes. No algorithms or evaluation results were intentionally changed during this phase.
