# Embedding Error Analysis

## Data Sources

- `embedding_quality_statistics.json`
- `semantic_search_statistics.json`
- `rag_retrieval_statistics.json`
- `qa_statistics.json`

## Top Failure Groups

Semantic search failure examples by category:

| Category | Failure Examples |
| --- | --- |
| cognate | 84 |
| morphological | 16 |

RAG retrieval failure examples by category:

| Category | Failure Examples |
| --- | --- |
| cross_language | 51 |
| cognate | 24 |
| morphology | 10 |

Low-similarity cognate examples by category in the stored top-100 list:

| Category | Examples |
| --- | --- |
| historical_relations | 80 |
| cognates | 15 |
| cross_language_equivalents | 4 |
| morphological_variants | 1 |

## Cross-Language Confusion

Cross-language semantic Recall@10 is 54.57%, lower than exact and historical categories in the stored benchmark. RAG cross_language Recall@10 is 77.2%. This suggests that cross-language ranking remains a primary error surface.

## Historical Confusion

Stored aggregate RAG and QA historical metrics are strong, but embedding cluster metrics show negative separation for cognate and language-family clusters. Historical items can therefore be retrieved correctly in task-specific pipelines while still being imperfectly separated in the raw embedding neighborhood.

## Low-Confidence Cognates

The repository stores `top_100_low_similarity_cognates`; these are the best immediate candidates for expert review. The error pattern should be treated as a curation queue, not as proof that the cognate relation is wrong.

## Incorrect Nearest Neighbors

The stored `top_100_incorrect_neighbors` list indicates that nearest-neighbor ranking can surface high-similarity but label-incompatible items. This affects direct semantic search and any RAG pipeline that depends on raw nearest-neighbor ordering.

## Publication Recommendation

Report the strongest validated metrics alongside these failure modes. Avoid claiming that the embedding space cleanly separates all cognate or language-family clusters.
