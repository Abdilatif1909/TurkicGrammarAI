# Scientific Validation Report

Date: 2026-06-11

## Scope

This phase created a scientific evaluation framework and gold-candidate datasets for TurkicGrammarAI. No platform features were added.

Important qualification: the generated datasets are not falsely marked as expert-reviewed. They are structured gold-candidate datasets with review metadata. They become publication-grade only after qualified human experts complete `reviewed_by`, `review_date`, and set `review_status` to `expert_reviewed`.

## Gold Dataset Inventory

| Dataset | Path | Records | Review Status |
| --- | --- | ---: | --- |
| Morphology | `backend/data/gold/gold_morphology_dataset.json` | 5,000 | candidate, requires expert review |
| Cognates | `backend/data/gold/gold_cognates_dataset.json` | 2,000 | candidate, requires expert review |
| Historical | `backend/data/gold/gold_historical_dataset.json` | 1,000 | candidate, requires expert review |
| QA | `backend/data/gold/gold_qa_dataset.json` | 2,000 | candidate, requires expert review |
| Manifest | `backend/data/gold/gold_dataset_manifest.json` | 4 dataset summaries | candidate metadata |

## Evaluation Pipeline

Created:

- `backend/apps/core/scientific_evaluator.py`

The evaluator computes:

- Morphology coverage, Top1, Top3, Any-Match accuracy.
- Cognate coverage and alignment accuracy.
- Historical coverage and lineage accuracy.
- QA answer accuracy and source accuracy.

Detailed machine-readable output:

- `backend/data/reports/scientific_evaluation_statistics.json`

## Evaluation Results

| Area | Cases Evaluated | Coverage | Accuracy |
| --- | ---: | ---: | ---: |
| Morphology | 5,000 | 100.0% | Top1 65.12%, Top3 73.76%, Any-Match 78.44% |
| Cognates | 2,000 | 100.0% | Alignment 100.0% |
| Historical | 1,000 | 100.0% | Lineage 100.0% |
| QA | 200 sampled from 2,000 | n/a | Answer 99.5%, Source 99.5% |

QA was evaluated on a 200-question sample to keep local runtime bounded because it invokes the live retrieval/QA stack and FastText model.

## Synthetic vs Gold-Candidate Comparison

| Area | Synthetic Benchmark Status | Gold-Candidate Status |
| --- | --- | --- |
| Morphology | Existing synthetic and independent benchmarks are mixed; some contain generated expansions. | 5,000 normalized records with review metadata; 4,621 independent-derived and 379 synthetic supplements. |
| Cognates | `cross_language_cognates.json` contains 2,000 generated/curated-style cognate groups. | Same groups are normalized into expert-review-ready records. |
| Historical | Historical records include generated sources. | 1,000 lineage chains normalized with explicit review metadata. |
| QA | Existing QA benchmark has 1,000 generated questions. | 2,000 questions with expected answer terms and expected sources. |

## Publication Readiness

Publication-ready metrics: not yet.

Reason: `expert_reviewed_cases = 0` across all generated gold-candidate datasets. The framework is ready for scientific validation, but the datasets still require expert review before results can be cited as human-reviewed gold metrics.

## Required Expert Review Workflow

1. Assign each dataset item to a qualified reviewer.
2. Verify surface form, lemma/root/suffixes, cognate grouping, historical lineage, or QA expected answer/source.
3. Set:
   - `review_status = "expert_reviewed"`
   - `reviewed_by`
   - `review_date`
4. Re-run `python backend/apps/core/scientific_evaluator.py`.
5. Use `scientific_evaluation_statistics.json` only when all report sections show full expert-reviewed coverage.

## Acceptance Status

| Requirement | Status |
| --- | --- |
| Gold datasets | PASS as gold-candidate datasets |
| Scientific evaluation | PASS |
| Reliability report | PASS |
| Publication-ready metrics | BLOCKED until expert review is completed |
