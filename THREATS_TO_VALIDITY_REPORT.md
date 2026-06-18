# Threats to Validity Report

## Deliverables

- Section file: `paper_draft/07_Threats_to_Validity.md`
- Target journal: Journal of King Saud University – Computer and Information Sciences

## Verification

- Word count: 1,012 words excluding Markdown headings

## Limitations Discussed

- Synthetic, semi-synthetic, generated, and projection-based resources
- Incomplete item-level provenance and inconsistent source normalization
- Uneven lexical and script normalization, including the Uyghur clean-data gap
- Gold-candidate status and absence of completed expert review
- Benchmark leakage from shared datasets and semantic index
- Sampled distractors and insufficiently difficult negative pairs
- Cognate-centered cross-language benchmark construction
- Term-overlap QA evaluation and internal rather than scholarly citations
- Absence of external shared-task evaluation
- No controlled feature-removal ablation
- No comparable vanilla FastText, historical, or external model baselines
- Manually weighted RAG ranking and limited candidate expansion
- Restricted language, dialect, script, and domain generalization
- Stored-artifact validation rather than a complete training rerun
- Environment, dependency, hardware, raw-distribution, CI, migration, and artifact-release gaps

## Audit Sources Used

- `paper_package/validation/THREATS_TO_VALIDITY.md`
- `DATASET_AUDIT_V2.md`
- `EMBEDDING_AND_RAG_AUDIT.md`
- `BENCHMARK_INTEGRITY_REPORT.md`
- `BENCHMARK_RELIABILITY_REPORT.md`
- `SCIENTIFIC_VALIDATION_REPORT.md`
- `MORPHOLOGY_SCIENTIFIC_AUDIT.md`
- `REPRODUCIBILITY_REPORT.md`
- `paper_package/validation/PUBLICATION_EVIDENCE_REPORT.md`
- `paper_package/validation/PAPER_READINESS_REPORT.md`
- `DATASET_MANIFEST.md`
- `RESEARCH_ARTIFACTS.md`
