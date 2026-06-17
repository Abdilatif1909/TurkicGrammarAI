# Figure Validation Report

## Validation Table

| Figure | Classification | Evidence | Validation Status |
| --- | --- | --- | --- |
| Figure 1: Embedding architecture | Architecture-derived | Derived from documented/code-backed pipeline: lexicon, morphology, cognates, historical forms, feature injection, FastText, embedding space. | Validated as conceptual architecture, not measured data. |
| Figure 2: Dataset distribution | Real data-derived | Records per language from `embedding_dataset.jsonl` / Table 1. | Validated. |
| Figure 3: Stored evaluation metrics | Real data-derived | Uses stored Top-1/Top-5/Top-10, semantic Recall@10, RAG Recall@10, QA accuracy. | Validated; not a baseline comparison. |
| Figure 4: Positive vs negative similarity | Real data-derived | Uses positive_pair_similarity, negative_pair_similarity, separation_margin from `embedding_quality_statistics.json`. | Validated. |
| Figure 5: Language coverage | Derived from real data | Percent share computed from Table 1 record counts. | Derived but reproducible. |

## Figure Risk Notes

- Figure 1 should be captioned as architecture, not experimental evidence.
- Figure 3 should not be described as baseline-vs-method performance because no baseline result is stored.
- Figures 2 and 5 are based on the embedding dataset, not necessarily the full raw lexical resource inventory.
