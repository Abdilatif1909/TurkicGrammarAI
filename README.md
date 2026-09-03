# TurkicGrammarAI

TurkicGrammarAI is a reproducible lexical pipeline for building cognate-aware FastText embeddings, Old Turkic-attested lineage links, retrieval benchmarks, and template-based QA evaluations for Turkic language resources.

The current dataset contains **7,844 lexical records across 7 language files**: Azerbaijani, Kazakh, Kyrgyz, Old Turkic, Turkish, Turkmen, and Uzbek. Uyghur is **not yet included**; adding it would make the collection eight-language, but no eight-language claim applies to the current release.

## Installation

Python 3.10 or a compatible newer Python 3 release is recommended.

```bash
pip install -r requirements.txt
```

Run every command below from the repository root.

## Rebuild the pipeline from scratch

The order matters because every stage consumes artifacts produced by the preceding stage.

1. Normalize the raw lexical files and generate the dataset manifest.

   ```bash
   python backend/data_pipeline/build_lexicon.py
   ```

2. Build deterministic cross-language cognate groups.

   ```bash
   python backend/cognate/build_cognates.py
   ```

3. Build Old Turkic-attested lineage links.

   ```bash
   python backend/lineage/build_lineage.py
   ```

4. Build the tagged FastText training corpus.

   ```bash
   python backend/embeddings/build_corpus.py
   ```

5. Train the tagged FastText model and export its vectors.

   ```bash
   python backend/embeddings/train_fasttext.py
   ```

6. Generate all four benchmarks, then refresh their generation-rules document.

   ```bash
   python backend/evaluation/build_embedding_benchmark.py
   python backend/evaluation/build_semantic_search_benchmark.py
   python backend/evaluation/build_rag_benchmark.py
   python backend/evaluation/build_qa_benchmark.py
   python backend/evaluation/write_benchmark_rules.py
   ```

7. Run every evaluator, followed by the leakage diagnostic. The RAG and QA evaluators emit separate oracle and embedding-based results; the diagnostic also trains and evaluates the Surface+POS no-tag comparison model.

   ```bash
   python backend/evaluation/eval_embedding_quality.py
   python backend/evaluation/eval_semantic_search.py
   python backend/evaluation/eval_rag_retrieval.py
   python backend/evaluation/eval_qa.py
   python backend/evaluation/diagnose_leakage.py
   ```

8. Build the consolidated results tables.

   ```bash
   python backend/evaluation/build_results_tables.py
   ```

## Main results

These are selected headline values. See the complete [results tables](docs/reproducibility/results_tables.md) and the [reproducibility package guide](docs/reproducibility/README.md) for definitions, confidence intervals, and limitations.

| Evaluation | Result |
|---|---:|
| Embedding positive/negative similarity margin | 0.239160 |
| Semantic search Recall@1 / Recall@5 / Recall@10 | 88.44% / 92.52% / 93.20% |
| RAG embedding-only cross-language Recall@1 / Recall@5 / Recall@10 | 58.14% / 86.05% / 93.02% |
| RAG embedding-only cross-language MRR | 0.719961 |
| QA embedding-only answer accuracy | 28.95% |
| QA embedding-only source accuracy | 94.74% |

Oracle RAG and template QA both score 100%, but these values are pipeline-consistency checks and must not be presented as model generalization results.

## Methodological notes

### Old Turkic-attested lineage, not Proto-Turkic

The historical layer links cognate groups containing an attested Old Turkic member to modern-language members. It does **not** reconstruct Proto-Turkic and must be described as **Old Turkic-attested lineage**.

### Oracle versus embedding-based evaluation

Oracle/metadata modes directly reuse metadata-derived relationships and verify internal data and template consistency. Embedding-only modes retrieve vector neighbors and are the relevant model-performance measurements. The stricter RAG result excludes same-language morphological matches. See the [leakage diagnosis](docs/reproducibility/leakage_diagnosis.md) for the tagged-versus-no-tag comparison.

### Current scale

The project currently covers 7,844 records and 7 language files, including Old Turkic as the historical source. Uyghur data is absent. RAG evaluation has 43 Old Turkic-attested queries and QA has 197 generated template questions, of which 190 can be evaluated in embedding-only mode.

## License

This project is released under the [MIT License](LICENSE). Copyright (c) 2026 TurkicGrammarAI Contributors.
