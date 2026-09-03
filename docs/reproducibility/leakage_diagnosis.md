# Leakage Diagnosis

Stage: Bosqich 7.5 - Leakage/tautology check

## Diagnosis

- RAG benchmark relevant sets are generated from `lineage_links.jsonl`, which itself is generated from `cognate_id`/`lineage_id` metadata. A metadata lookup retriever and the benchmark answer key would therefore use the same source. That oracle setup is tautological and only measures internal metadata consistency.
- The Bosqich 7 RAG evaluator used cosine nearest neighbors, not direct metadata lookup, but the benchmark relevant set includes same-language morphological variants. That makes Recall@1 artificially easy because near-inflectional variants are often the nearest vector neighbors.
- QA 100% accuracy is confirmed to be database/template lookup, not open-ended QA. The engine parses the generated template and reads the exact answer from cognate/lineage/lexicon metadata.
- The training corpus includes `COGNATE_` and `LINEAGE_` tokens. This can make metadata-derived retrieval easier because all members of a group co-occur with the same artificial tags during training.

## No-Tag Model Check

A comparison model was trained from only `surface_form POS_<pos>` lines. This removes `LANG_`, `lemma`, `COGNATE_`, and `LINEAGE_` training tokens. The diagnostic model uses `bucket=50000` to avoid the 2M default FastText subword allocation in the constrained local environment.

- Surface+POS corpus lines: **7844**
- Surface+POS vocabulary size: **7196**
- Surface+POS training time seconds: **1.836054**

## Cross-Language Embedding-Only RAG Comparison

| Model | Recall@1 | Recall@5 | Recall@10 | MRR | N |
|---|---:|---:|---:|---:|---:|
| Tagged training corpus | 58.14% | 86.05% | 93.02% | 0.719961 | 43 |
| Surface+POS only corpus | 37.21% | 60.47% | 62.79% | 0.470155 | 43 |

## Embedding-Based QA Comparison

Lemma lookup questions are skipped in embedding-only QA because answering them exactly requires direct lexicon lookup.

| Model | Answer Accuracy | Source Accuracy | Evaluated | Skipped |
|---|---:|---:|---:|---:|
| Tagged training corpus | 28.95% | 94.74% | 190 | 7 |
| Surface+POS only corpus | 11.05% | 81.05% | 190 | 7 |

## Conclusion

Tautology is confirmed for oracle/metadata-based RAG and template QA. Paper results should report oracle numbers only as pipeline consistency checks. The credible model-performance numbers are the embedding-only cross-language RAG and embedding-based QA results, preferably with the surface+POS no-tag comparison disclosed.
