# Repository Publication Status

Generated for Phase 36.7 repository publication preparation on 2026-06-17.

## Repository Readiness

Status: ready for public research prototype release after committing this documentation update.

- Source code, datasets, benchmarks, and documentation are organized in discoverable top-level directories.
- `paper_package/` is preserved as the scientific reproducibility package.
- New publication support documents inventory research artifacts, size policy, Scopus preparation, and readiness status.
- No algorithms, datasets, models, or evaluation results were modified during this phase.

## Reproducibility Readiness

Status: ready for reviewer-oriented reproducibility checks with known limitations.

- README now documents the `paper_package/` structure and reviewer reproduction paths.
- `RESEARCH_ARTIFACTS.md` maps figures, tables, validation reports, evaluation reports, benchmark reports, and publication assets.
- `REPRODUCIBILITY_REPORT.md` remains the main setup and command reference.
- Independent scientific validation is still incomplete and should be clearly stated in manuscript claims.

## Reviewer Readiness

Status: ready for transparent review package inspection.

- Reviewer-facing assets are available under `paper_package/validation/`.
- Manuscript figures and tables are available in editable and manuscript-friendly formats.
- Known threats to validity, metric traceability, result classification, and top reviewer questions are documented.
- Reviewers should cite or inspect the exact commit used for any reproduction attempt.

## GitHub Readiness

Status: GitHub-friendly working tree.

- Current Git pack size is about 4.45 MiB.
- Largest tracked files are compact enough for GitHub.
- Oversized local artifacts are ignored: virtual environments, `node_modules`, FastText binaries, generated embedding indexes/corpora, logs, caches, and local databases.
- `paper_package/` is intentionally not ignored and should be tracked.

## Publication Readiness

Status: ready for manuscript drafting; not yet ready for final Scopus submission claims.

- Current assets support drafting, validation traceability, and reviewer preparation.
- Remaining publication work includes expert-reviewed gold data, stronger independent benchmarks, provenance/licensing cleanup, artifact archival for large models, and CI-backed reproducibility.
- The repository should be described as an active research prototype unless and until external validation is completed.

## Acceptance Checklist

- `paper_package/` preserved: yes.
- Reviewer assets documented: yes.
- Reproducibility documented: yes.
- GitHub-friendly structure documented: yes.
- Ready for manuscript drafting: yes.
- Ready for public research release: yes, as a research prototype with stated limitations.
