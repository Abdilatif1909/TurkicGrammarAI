# Uzbek Morphology v1 Milestone

Date: 2026-06-08

## Scope

This milestone freezes the current Uzbek morphology baseline before further scoring optimization.

Included work:

- Multi-analysis evaluation alignment.
- Derivational morphology support with ranked lemma and derivational analyses.
- Rule completion sprint reducing active `RULE_MISSING` cases below 50.
- Report generation for derivational morphology, multi-analysis evaluation, and rule completion.

## Metrics

| Metric | Value |
| --- | ---: |
| Coverage | 100.0% |
| Top1 | 27.8% |
| Top3 | 52.4% |
| AnyMatch | 79.2% |
| RULE_MISSING | 43 |
| TRUE_ROOT_ERROR | 61 |
| SCORING_ERROR | 0 |

## Verification

Commands run:

```powershell
python manage.py test
python manage.py check
python backend\manage.py validate_uzbek_morphology
```

Results:

- `python manage.py test` passed from `backend`: 76 tests.
- `python manage.py check` passed from `backend`: no issues.
- `python backend\manage.py validate_uzbek_morphology` passed from the project root and regenerated `backend/data/reports/uzbek_morphology_report.json`.

Note: `validate_uzbek_morphology` currently resolves data paths relative to the project root, so it should be run as `python backend\manage.py validate_uzbek_morphology` from the repository root.

## Required Reports

Verified present:

- `RULE_COMPLETION_REPORT.md`
- `MULTI_ANALYSIS_EVALUATION_REPORT.md`
- `DERIVATIONAL_MORPHOLOGY_REPORT.md`

## Commit

Requested commit message:

```text
feat(morphology): complete Uzbek morphology v1 milestone
```

The local workspace does not currently contain a `.git` directory, so the milestone is documented and ready to commit once the workspace is attached to a git repository.
