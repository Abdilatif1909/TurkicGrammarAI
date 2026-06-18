# Results and Discussion Report

## Deliverables

- Section file: `paper_draft/06_Results_and_Discussion.md`
- Target journal: Journal of King Saud University – Computer and Information Sciences
- Scope: repository-supported results and critical interpretation

## Verification

- Word count: 2,527 words excluding Markdown headings
- Figures referenced: Figures 2, 3, 4, and 5
- Tables referenced: Tables 4, 5, 6, and 7

## Metrics Discussed

- Embedding Top-1, Top-5, and Top-10
- Mean cosine similarity
- Positive-pair and negative-pair similarity
- Separation margin
- Cognate, language-family, and morphology cluster separation
- Semantic-search Recall@1, Recall@5, Recall@10, and MRR
- RAG Recall@1, Recall@5, Recall@10, MRR, and average latency
- QA answer accuracy, source accuracy, and support coverage
- Category-level semantic-search, RAG, and QA results
- Derived Wilson intervals and category-distribution summaries

## Limitations Discussed

- No stored baseline evaluation or computable improvement
- No controlled retraining ablation
- Benchmark leakage from shared repository resources and semantic index
- Synthetic, projected, and candidate-review data
- Incomplete provenance and expert validation
- Negative cognate and language-family cluster separation
- Weak cross-language ranking and morphology QA
- QA term-overlap evaluation rather than free-form correctness
- Internal source identifiers rather than scholarly citations
- Unrecorded hardware for latency interpretation
