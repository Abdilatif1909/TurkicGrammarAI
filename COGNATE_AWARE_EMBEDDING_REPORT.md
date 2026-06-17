# Cognate-Aware Embedding Report

## Corpus Signals

- Injected `COGNATE_<id>` tokens for aligned cognate groups.
- Injected `LINEAGE_<stage>` and `LINEAGE_FORM_<form>` tokens from historical lineage.
- Injected `LANG_<language>`, `ROOT_<root>`, and `FEATURE_<feature>` tokens.
- Added grouped signal lines for cognate groups, root clusters, and feature clusters.

## Training

- vector_size: 300
- window: 5
- min_count: 1
- epochs: 20
- workers: 12
- vocabulary_size: 143011
- training_time_seconds: 172.217

## Before vs After

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| vocabulary_size | 90825 | 143011 | 52186 |
| top1 | 18.38 | 41.17 | 22.79 |
| top5 | 31.88 | 71.86 | 39.98 |
| top10 | 44.38 | 85.06 | 40.68 |
| positive_pair_similarity | 0.398441 | 0.594379 | 0.195938 |
| negative_pair_similarity | 0.494986 | 0.464821 | -0.030165 |
| separation_margin | -0.096545 | 0.129558 | 0.226103 |

## Cluster Metrics

| Cluster Type | Intra | Inter | Separation |
| --- | ---: | ---: | ---: |
| cognate_clusters | 0.634234 | 0.697581 | -0.063347 |
| language_family_clusters | 0.556224 | 0.610933 | -0.054709 |
| morphological_clusters | 0.699947 | 0.543781 | 0.156166 |

## Target Status

- Positive similarity > negative similarity: True
- Margin > 0: True
- Top10 > 60%: True

## Readiness

The cognate-aware FastText baseline meets the Phase 23 quality targets and is ready for Word2Vec baseline comparison.
