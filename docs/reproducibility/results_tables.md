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
| RAG recall_at_1 | 100.00% | 91.80% - 100.00% | 43 | 43 |
| RAG recall_at_10 | 100.00% | 91.80% - 100.00% | 43 | 43 |
| RAG recall_at_5 | 100.00% | 91.80% - 100.00% | 43 | 43 |
| QA answer_accuracy | 100.00% | 98.09% - 100.00% | 197 | 197 |
| QA source_accuracy | 100.00% | 98.09% - 100.00% | 197 | 197 |

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

## RAG Retrieval Results

| Metric | Value | Hits/N |
|---|---:|---:|
| mrr | 1.000000 | N=43 |
| recall_at_1 | 100.00% | 43/43 |
| recall_at_10 | 100.00% | 43/43 |
| recall_at_5 | 100.00% | 43/43 |

## QA Results

| Metric | Value | Hits | N |
|---|---:|---:|---:|
| Answer accuracy | 100.00% | 197 | 197 |
| Source accuracy | 100.00% | 197 | 197 |

## Limitations Of Current Evaluation Scale

- RAG evaluation uses only 43 queries because it is limited to Old Turkic-attested lineage groups.
- QA evaluation uses 197 generated template questions, so confidence intervals are wider than for the embedding benchmark.
- The benchmark is derived from the same lexicon used to build the corpus, so results test internal retrieval consistency rather than external generalization.
- The current dataset lacks an independent semantic category taxonomy, so category-level claims should not be made.
