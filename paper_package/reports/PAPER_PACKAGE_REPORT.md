# Paper Package Report

## Package Status

The paper package was generated from existing repository artifacts only. No algorithms were changed, no model was retrained, no datasets were modified, and no evaluation result was edited.

## Figures

- Figure 1: `paper_package/figures/figure1_embedding_architecture.png` and `.svg` - TurkicGrammarAI embedding architecture from lexicon to embedding space.
- Figure 2: `paper_package/figures/figure2_dataset_distribution.png` and `.svg` - Language-wise distribution of records in the embedding dataset.
- Figure 3: `paper_package/figures/figure3_embedding_performance_comparison.png` and `.svg` - Stored embedding, semantic retrieval, RAG, and QA performance metrics.
- Figure 4: `paper_package/figures/figure4_positive_negative_similarity.png` and `.svg` - Mean positive and negative pair similarity with separation margin.
- Figure 5: `paper_package/figures/figure5_language_coverage.png` and `.svg` - Percentage share of embedding records by language.

## Tables

- `paper_package/tables/table1_language_distribution.md`
- `paper_package/tables/table2_lexical_resource_statistics.md`
- `paper_package/tables/table3_training_configuration.md`
- `paper_package/tables/table4_embedding_evaluation.md`
- `paper_package/tables/table5_confidence_intervals.md`
- `paper_package/tables/table6_ablation_proxy_summary.md`
- `paper_package/tables/table7_category_distribution_statistics.md`

## Ready-to-Insert LaTeX Tables

```latex
\input{paper_package/tables/table1_language_distribution.tex}
\input{paper_package/tables/table2_lexical_resource_statistics.tex}
\input{paper_package/tables/table3_training_configuration.tex}
\input{paper_package/tables/table4_embedding_evaluation.tex}
\input{paper_package/tables/table5_confidence_intervals.tex}
\input{paper_package/tables/table6_ablation_proxy_summary.tex}
\input{paper_package/tables/table7_category_distribution_statistics.tex}
```

## Ready-to-Insert Captions

- Figure 1. TurkicGrammarAI embedding architecture showing the flow from lexical resources through morphology, cognates, historical forms, feature injection, FastText training, and embedding space construction.
- Figure 2. Language distribution of records in the embedding dataset used for cognate-aware multilingual embedding experiments.
- Figure 3. Stored evaluation metrics for embedding retrieval, semantic search, RAG retrieval, and QA. No baseline metric is plotted because baseline evaluation artifacts are not present in the repository.
- Figure 4. Mean cosine similarity for positive and negative benchmark pairs, including the observed separation margin.
- Figure 5. Language coverage share across the embedding dataset.

## Core Metrics

- Embedding Top-1 / Top-5 / Top-10: 40.8 / 73.66 / 86.06 percent
- Positive / negative similarity: 0.595108 / 0.472318
- Separation margin: 0.12279
- Semantic search Recall@10: 82.3 percent
- RAG Recall@10: 84.3 percent
- QA answer accuracy: 83.8 percent

## Analysis Files

- `paper_package/reports/PAPER_DATA_SUMMARY.md`
- `paper_package/analysis/ABLATION_STUDY.md`
- `paper_package/analysis/EMBEDDING_ERROR_ANALYSIS.md`
- `paper_package/analysis/STATISTICAL_ANALYSIS.md`

## Publication Notes

- Use Table 4 cautiously: baseline and improvement are unavailable in repository artifacts.
- Describe the ablation as proxy evidence, not as controlled retraining-based ablation.
- Mention synthetic or semi-synthetic benchmark limitations where these metrics are reported.
