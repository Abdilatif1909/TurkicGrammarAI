# Table Validation Report

## Validation Table

| Table | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Table 1: Language distribution | Validated | Counts reproduced from `embedding_dataset.jsonl` by language; records/lemmas/roots are direct counts. | No estimation. |
| Table 2: Lexical resource statistics | Validated | Values are direct counts from `embedding_dataset.jsonl`: records, languages, unique forms/lemmas/roots, cognate groups, historical lineage. | No estimation. |
| Table 3: Training configuration | Validated | Values exist in `backend/data/reports/fasttext_training_stats.json` and map to `train_fasttext_embeddings.py`. | No estimation. |
| Table 4: Embedding evaluation | Partially Validated | Cognate-aware values exist in `embedding_quality_statistics.json`; baseline and improvement are intentionally marked unavailable. | No estimated baseline. |
| Table 5: Confidence intervals | Partially Validated | Intervals are derived from stored percentages and benchmark sample sizes using Wilson formula. | Derived, not measured by evaluator. |
| Table 6: Ablation proxy summary | Partially Validated | Availability counts and RAG source contribution are real; interpretation is proxy evidence only. | Not a controlled ablation. |
| Table 7: Category distribution statistics | Partially Validated | Mean/min/max/population SD are derived from stored category metrics. | Derived aggregate. |

## Summary

Tables 1-3 are fully validated from repository artifacts. Table 4 is valid for observed cognate-aware metrics but has no baseline evidence. Tables 5-7 are reproducible derived analyses, not original evaluation outputs.
