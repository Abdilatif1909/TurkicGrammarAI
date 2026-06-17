# Scopus Preparation

Generated for Phase 36.7 repository publication preparation on 2026-06-17.

## Current Publication Assets

The repository now contains a compact manuscript support package:

- `paper_package/figures/`: five manuscript figures in PNG and SVG.
- `paper_package/tables/`: seven manuscript tables in CSV, Markdown, and LaTeX.
- `paper_package/analysis/`: statistical analysis, ablation study notes, and embedding error analysis.
- `paper_package/validation/`: figure validation, table validation, metric traceability, publication evidence, result classification, threats to validity, reviewer questions, and paper readiness.
- `paper_package/reports/`: paper data summary and package report.

Additional research documentation is available in:

- `RESEARCH_ARTIFACTS.md`
- `DATASET_MANIFEST.md`
- `MODEL_MANIFEST.md`
- `REPRODUCIBILITY_REPORT.md`
- `GITHUB_SIZE_REPORT.md`
- Root-level evaluation, audit, benchmark, and readiness reports.

## Current Limitations

- Expert-reviewed gold datasets remain incomplete.
- Some benchmark files are generated from project datasets or indexes and should be treated as regression evidence rather than independent scientific validation.
- Benchmark leakage risk remains for semantic search, RAG, and QA evaluation.
- Dataset provenance, licensing metadata, and item-level citations require additional normalization before publication-level claims.
- FastText model binaries and generated embedding indexes are not suitable for direct Git tracking and need an external artifact distribution plan.
- API documentation should be regenerated and verified against the implemented `/api/` routes.
- GitHub Actions or another CI workflow should be added for repeatable reviewer checks.
- Public deployment security hardening is still required before exposing expensive or operational endpoints.

## Remaining Work Before Submission

- Finalize the manuscript scope and align all claims with `paper_package/validation/RESULT_CLASSIFICATION.md`.
- Complete expert review for gold datasets used in morphology, cognate, semantic search, RAG, and QA claims.
- Separate synthetic/regression benchmarks from independent evaluation benchmarks in the manuscript methods section.
- Add explicit dataset licenses, provenance fields, citation metadata, and generation notes.
- Archive large models and generated embedding artifacts in a stable external repository such as Zenodo, OSF, institutional storage, or GitHub Releases.
- Record the exact repository commit, Python version, Node version, dependency lock state, and operating system used for final experiments.
- Add or verify CI commands for backend tests, frontend build, data validation, and selected evaluation scripts.
- Prepare a reproducibility appendix that points to `RESEARCH_ARTIFACTS.md`, `REPRODUCIBILITY_REPORT.md`, and `paper_package/`.

## Submission Readiness Note

The repository is suitable for manuscript drafting and public research release as a transparent prototype. It should not yet be presented as fully externally validated or production-grade. Scopus submission should wait until independent evaluation, provenance, licensing, and artifact archival are complete.
