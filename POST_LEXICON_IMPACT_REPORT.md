# Post-Lexicon Impact Report

Phase 35 re-ran the existing evaluation pipeline after Phase 34 lexical expansion. No new features were added.

## Baseline Availability

| Subsystem | Before Phase 34 | After Phase 34 | Comparison Status |
|---|---|---|---|
| Morphology | Not preserved in same-command statistic files | Available | Post-only |
| Cognates | Not preserved | Available | Post-only |
| Embeddings | COGNATE_AWARE_EMBEDDING_REPORT.md Phase 23 after metrics | Available | Comparable |
| Semantic Search | Not preserved; report/stat file overwritten by run | Available | Post-only |
| RAG | Not preserved; report/stat file overwritten by run | Available | Post-only |
| QA | Not preserved; report/stat file overwritten by run | Available | Post-only |

## Lexicon Context

| Metric | After Phase 34 |
|---|---:|
| total_records | 100030 |
| global_unique_words | 96940 |
| total_language_lemmas | 33000 |
| total_language_roots | 33000 |
| languages_covered | 8 |

## Morphology Post-Run Metrics

| Language | Cases | Coverage | Top1 | Top3 | AnyMatch | Avg Ambiguity |
|---|---:|---:|---:|---:|---:|---:|
| uz | 500 | 100 | 23.4 | 47.6 | 91.4 | 67.6 |
| tr | 500 | 100 | 99.8 | 99.8 | 100 | 6.38 |
| az | 500 | 100 | 99.8 | 99.8 | 100 | 5.93 |
| kk | 500 | 100 | 99.8 | 99.8 | 100 | 8.4 |
| ky | 500 | 100 | 100 | 100 | 100 | 5.03 |
| tk | 500 | 100 | 100 | 100 | 100 | 7.22 |
| ug | 500 | 100 | 99.6 | 100 | 100 | 6.3 |
| otk | 1000 | 100 | 90.9 | 92.9 | 100 | 7.56 |

## Cognates Post-Run Metrics

| Metric | Value |
|---|---:|
| coverage | 100 |
| alignment_accuracy | 100 |
| total_cases | 2000 |
| new_cognate_coverage | not separately reported by existing evaluator |

## Embedding Before vs After

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| top1 | 41.17 | 40.8 | -0.37 |
| top5 | 71.86 | 73.66 | +1.8 |
| top10 | 85.06 | 86.06 | +1 |
| positive_pair_similarity | 0.5944 | 0.5951 | +0.0007 |
| negative_pair_similarity | 0.4648 | 0.4723 | +0.0075 |
| separation_margin | 0.1296 | 0.1228 | -0.0068 |

## Retrieval And QA Post-Run Metrics

| Subsystem | Metric A | Metric B | Metric C | Metric D | Extra |
|---|---:|---:|---:|---:|---:|
| Semantic Search | R@1 36.25 | R@5 72.95 | R@10 82.3 | MRR 0.5299 | queries 2000 |
| RAG | R@1 27 | R@5 65.9 | R@10 84.3 | MRR 0.4558 | latency_ms 53.173 |
| QA | Answer 83.8 | Source 99.7 | Coverage 83.8 | questions 1000 | n/a |

## Overall Gain/Loss

- Embeddings are the only subsystem with a preserved comparable pre-Phase34 baseline. Top10 improved from 85.06 to 86.06, while margin decreased from 0.129558 to 0.12279 but stayed positive.
- Morphology, cognates, semantic search, RAG, and QA were re-evaluated successfully, but their same-benchmark pre-Phase34 snapshots were not preserved. Their impact is therefore reported as post-run operational status, not numeric before/after gain.
- The expanded lexicon increased available language lemma/root inventory to 33,000 while maintaining 0 duplicate `(language, word)` records in the lexical audit.
