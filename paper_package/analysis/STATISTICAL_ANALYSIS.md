# Statistical Analysis

## Confidence Intervals

Wilson 95% confidence intervals were computed for stored proportion metrics only. See `paper_package/tables/table5_confidence_intervals.md`.

## Positive vs Negative Similarity

- Positive pair mean similarity: 0.595108
- Negative pair mean similarity: 0.472318
- Mean separation margin: 0.12279

A standardized effect size such as Cohen's d cannot be computed from the stored aggregate files because positive and negative standard deviations are not stored. The mean difference is reported, but no distribution-level effect size is invented.

## Category-Level Distribution Statistics

| Metric Group | N | Mean | Min | Max | Population SD |
| --- | --- | --- | --- | --- | --- |
| Semantic Recall@10 categories | 5 | 82.49 | 54.57 | 100.00 | 16.98 |
| RAG Recall@10 categories | 4 | 84.30 | 70.00 | 100.00 | 11.55 |
| QA answer accuracy categories | 4 | 83.80 | 68.80 | 100.00 | 11.83 |

## Benchmark Sample Sizes

- Embedding quality benchmark pairs: 5000
- Semantic search queries: 2000
- RAG retrieval queries: 1000
- QA questions: 1000

## Interpretation Limits

The confidence intervals assume benchmark items are independent samples. Because several benchmark sets are synthetic or semi-synthetic according to repository audit reports, these intervals describe internal benchmark uncertainty and should not be interpreted as external linguistic validity.
