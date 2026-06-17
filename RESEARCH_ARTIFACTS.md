# Research Artifacts

Generated for Phase 36.7 repository publication preparation on 2026-06-17.

This document inventories research-facing artifacts without changing algorithms, datasets, models, or evaluation results.

## Figures

Publication figures are stored in `paper_package/figures/`.

- `figure1_embedding_architecture.*`: embedding architecture figure.
- `figure2_dataset_distribution.*`: dataset distribution figure.
- `figure3_embedding_performance_comparison.*`: embedding performance comparison figure.
- `figure4_positive_negative_similarity.*`: positive/negative similarity figure.
- `figure5_language_coverage.*`: language coverage figure.

Each figure is available in PNG for manuscript drafting and SVG for editable/vector workflows.

## Tables

Publication tables are stored in `paper_package/tables/`.

- `table1_language_distribution.*`
- `table2_lexical_resource_statistics.*`
- `table3_training_configuration.*`
- `table4_embedding_evaluation.*`
- `table5_confidence_intervals.*`
- `table6_ablation_proxy_summary.*`
- `table7_category_distribution_statistics.*`

Tables are provided in CSV, Markdown, and LaTeX formats for reproducibility checks, manuscript drafting, and reviewer inspection.

## Validation Reports

Reviewer validation assets are stored in `paper_package/validation/`.

- Figure validation: `FIGURE_VALIDATION_REPORT.md`
- Table validation: `TABLE_VALIDATION_REPORT.md`
- Metric traceability: `METRIC_TRACEABILITY_REPORT.md`
- Publication evidence: `PUBLICATION_EVIDENCE_REPORT.md`
- Result classification: `RESULT_CLASSIFICATION.md`
- Threats to validity: `THREATS_TO_VALIDITY.md`
- Reviewer questions: `TOP_REVIEWER_QUESTIONS.md`
- Paper readiness: `PAPER_READINESS_REPORT.md`

These files document how manuscript-facing claims map to repository artifacts and where additional expert review is still required.

## Evaluation Reports

Root-level reports document current evaluation results and audit findings:

- Morphology: `MORPHOLOGY_SCIENTIFIC_AUDIT.md`, `MULTI_ANALYSIS_EVALUATION_REPORT.md`, language-specific `*_MORPHOLOGY_REPORT.md` files.
- Cognates: `COGNATE_ALIGNMENT_REPORT.md`, `COGNATE_AWARE_EMBEDDING_REPORT.md`.
- Embeddings: `EMBEDDING_QUALITY_REPORT.md`, `EMBEDDING_ERROR_REPORT.md`, `FASTTEXT_EMBEDDING_REPORT.md`.
- Semantic search: `SEMANTIC_SEARCH_REPORT.md`.
- RAG: `TURKIC_RAG_REPORT.md`.
- QA: `TURKIC_QA_REPORT.md`.
- Dataset and model manifests: `DATASET_MANIFEST.md`, `MODEL_MANIFEST.md`.

These reports should be cited with the exact repository commit used for a manuscript or reviewer package.

## Benchmark Reports

Benchmark and reliability reports include:

- `BENCHMARK_INTEGRITY_REPORT.md`
- `BENCHMARK_RELIABILITY_REPORT.md`
- `REALISTIC_EVALUATION_REPORT.md`
- `REGRESSION_TEST_REPORT.md`
- `SCIENTIFIC_VALIDATION_REPORT.md`
- `TESTING_GAP_REPORT.md`

Benchmark files are stored under `backend/data/benchmark/`, `backend/data/benchmark/independent/`, `backend/data/evaluation/`, `backend/data/gold/`, and selected `backend/data/embeddings/` benchmark JSON files.

## Publication Assets

Publication-facing assets are organized as:

- `paper_package/figures/`: manuscript figures.
- `paper_package/tables/`: manuscript tables.
- `paper_package/analysis/`: statistical analysis, ablation notes, and error analysis.
- `paper_package/validation/`: reviewer validation package.
- `paper_package/reports/`: paper package summaries.
- Root-level `*_REPORT.md`: project, dataset, benchmark, evaluation, and readiness reports.

The `paper_package/` directory is intentionally kept in the repository because it is small and directly supports scientific reproducibility.
