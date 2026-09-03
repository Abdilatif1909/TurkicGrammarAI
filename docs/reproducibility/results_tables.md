# Results Tables

Stage: Bosqich 7 - Evaluation

## Table 4 - Embedding Quality Results

| Metric | Value | N | Notes |
|---|---:|---:|---|
| Mean positive similarity | 0.904880 | 102947 | Cosine over positive pairs |
| Mean negative similarity | 0.665720 | 102947 | Cosine over fixed-seed negative controls |
| Separation margin | 0.239160 | 205894 | Positive mean minus negative mean |
| Top-1 accuracy | 0.91% | 102947 | Nearest-neighbor target hit |
| Top-5 accuracy | 4.60% | 102947 | Nearest-neighbor target hit |
| Top-10 accuracy | 10.30% | 102947 | Nearest-neighbor target hit |

## Table 5 - Wilson 95% Confidence Intervals

| Metric | Estimate | Wilson 95% CI | Successes | N |
|---|---:|---:|---:|---:|
| Embedding top_10_accuracy | 10.30% | 10.11% - 10.49% | 10602 | 102947 |
| Embedding top_1_accuracy | 0.91% | 0.86% - 0.97% | 939 | 102947 |
| Embedding top_5_accuracy | 4.60% | 4.48% - 4.73% | 4737 | 102947 |
| Semantic recall_at_1 | 88.44% | 82.26% - 92.65% | 130 | 147 |
| Semantic recall_at_10 | 93.20% | 87.93% - 96.26% | 137 | 147 |
| Semantic recall_at_5 | 92.52% | 87.10% - 95.77% | 136 | 147 |
| RAG embedding cross-language recall_at_1 | 58.14% | 43.33% - 71.62% | 25 | 43 |
| RAG embedding cross-language recall_at_10 | 93.02% | 81.39% - 97.60% | 40 | 43 |
| RAG embedding cross-language recall_at_5 | 86.05% | 72.74% - 93.44% | 37 | 43 |
| QA embedding answer_accuracy | 28.95% | 22.97% - 35.76% | 55 | 190 |
| QA embedding source_accuracy | 94.74% | 90.58% - 97.12% | 180 | 190 |

## Table 6 - Feature Availability And Benchmark Usage

| Feature | Available entries | Total entries | Availability | Benchmark usage count | Usage definition |
|---|---:|---:|---:|---:|---|
| ROOT | 7844 | 7844 | 100.00% | 43 | all lexicon rows include root; lemma/morphology used in RAG relevant sets |
| COGNATE | 5374 | 7844 | 68.51% | 50891 | semantic queries and cognate QA; embedding positives from cognate groups |
| LINEAGE | 2238 | 7844 | 28.53% | 52436 | RAG queries, lineage QA, and lineage-sourced embedding positives |
| LANGUAGE | 7844 | 7844 | 100.00% | 206281 | all benchmark rows carry language labels |

## Table 7 - Category-Level Evaluation

N/A - insufficient category granularity in the current dataset. The lexicon has POS labels and cognate/lineage groups, but no independent semantic category taxonomy suitable for a separate Table 7 without inventing labels.

## Semantic Search Results

| Metric | Value | Hits | N |
|---|---:|---:|---:|
| recall_at_1 | 88.44% | 130 | 147 |
| recall_at_10 | 93.20% | 137 | 147 |
| recall_at_5 | 92.52% | 136 | 147 |

## RAG Retrieval Results - Oracle Vs Embedding

Oracle/metadata-based retrieval demonstrates pipeline correctness. Embedding-based retrieval demonstrates model behavior; the cross-language row excludes same-language morphology hits.

| Mode | Recall@1 | Recall@5 | Recall@10 | MRR | N |
|---|---:|---:|---:|---:|---:|
| oracle_metadata | 100.00% | 100.00% | 100.00% | 1.000000 | 43 |
| embedding_only_all_relevant | 100.00% | 100.00% | 100.00% | 1.000000 | 43 |
| embedding_only_cross_language | 58.14% | 86.05% | 93.02% | 0.719961 | 43 |

## QA Results - Oracle Vs Embedding

Oracle/template lookup demonstrates database consistency. Embedding-based QA derives answer languages from top-10 vector neighbors; lemma lookup questions are skipped because exact lemma answers require direct database lookup.

| Mode | Answer Accuracy | Source Accuracy | Evaluated | Skipped |
|---|---:|---:|---:|---:|
| oracle_template_lookup | 100.00% | 100.00% | 197 | 0 |
| embedding_only_tagged_model | 28.95% | 94.74% | 190 | 7 |

## Leakage Diagnostic - No-Tag Model

The no-tag comparison model was trained with only `surface_form POS_<pos>` lines. It removes `LANG_`, `lemma`, `COGNATE_`, and `LINEAGE_` corpus tokens.

| Task | Metric | Tagged model | Surface+POS no-tag model | N |
|---|---|---:|---:|---:|
| RAG cross-language | Recall@1 | 58.14% | 37.21% | 43 |
| RAG cross-language | Recall@5 | 86.05% | 60.47% | 43 |
| RAG cross-language | Recall@10 | 93.02% | 62.79% | 43 |
| RAG cross-language | MRR | 0.719961 | 0.470155 | 43 |
| QA embedding | Answer accuracy | 28.95% | 11.05% | 190 |
| QA embedding | Source accuracy | 94.74% | 81.05% | 190 |

## Limitations Of Current Evaluation Scale

- RAG evaluation uses only 43 queries because it is limited to Old Turkic-attested lineage groups.
- QA evaluation uses 197 generated template questions, so confidence intervals are wider than for the embedding benchmark.
- Oracle RAG and template QA are circular by construction and should be reported only as metadata pipeline consistency checks.
- The tagged training corpus includes `COGNATE_` and `LINEAGE_` tokens, so tagged embedding results can overstate generalization on metadata-derived benchmarks.
- The benchmark is derived from the same lexicon used to build the corpus, so even embedding-only results test internal retrieval consistency more than external generalization.
- The current dataset lacks an independent semantic category taxonomy, so category-level claims should not be made.
