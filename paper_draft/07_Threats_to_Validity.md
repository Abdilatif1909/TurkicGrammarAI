# 7. Threats to Validity

## 7.1 Dataset Validity

The principal dataset threat is the heterogeneous status of the resources merged into the embedding dataset. The 100,000 records combine word datasets, morphology benchmarks, lemma dictionaries, cognate groups, historical forms, and corpus hooks. This integration increases coverage, but it also combines records produced through different curation and generation procedures. Repository audits identify synthetic, semi-synthetic, generated, and projection-based material in the lexical, morphology, cognate, and historical layers. In particular, the Uyghur resource includes projected material, and generated Proto-Turkic-style identifiers and artificial-looking forms occur in embedding and semantic-index records.

Morphology benchmarks are largely suitable for engineering regression rather than independent linguistic accuracy measurement. The benchmark integrity audit reports that synthetic suffix-chain cases have high overlap with the rule inventories used to create or analyze them. Independent root and lemma candidate sets are available, but a fully independent morpheme-level benchmark with manually annotated suffix boundaries has not been completed. The derivational inventory is also small relative to the inflectional rule resources.

Provenance remains incomplete. Broad source values such as `words_dataset` do not provide item-level citations, licenses, curation status, generation metadata, or reviewer information. Language identifiers are not uniformly normalized in all source files, and the repository contains stale root-level statistics that differ from the canonical backend data. Uyghur lacks a normalized clean file comparable to those available for several other languages. Lemma and root quality therefore depends on the source data and fallback or generation procedures used for each record.

The available “gold” datasets are gold candidates rather than expert-reviewed gold standards. The scientific validation report records zero fully expert-reviewed cases. Morphology, cognate, historical, and QA candidates all require qualified review, with reviewer identity, date, and status recorded before they can support claims of human-validated linguistic correctness. Cognate membership, reconstructed forms, historical lineage, lemmas, roots, and acceptable QA answers should therefore be interpreted as repository annotations pending specialist validation.

## 7.2 Evaluation Validity

Benchmark leakage is the most important evaluation threat. The semantic-search, RAG, and QA benchmark generators construct cases from `semantic_index.json` and then evaluate retrieval against the same index. The embedding-quality benchmark is also generated from repository cognate and embedding resources used by the broader pipeline. This circularity can overestimate performance relative to independently curated data.

Benchmark construction introduces additional constraints. FastText ranking uses stored positive pairs and sampled distractors, so the measured difficulty depends on the distractor-generation procedure. Negative pairs are sampled and may not constitute linguistically difficult negatives. Cross-language cases are substantially based on cognate groups and may not represent non-cognate translation equivalence. QA expected answers are term-based, and QA accuracy measures expected-word occurrence rather than completeness, explanatory quality, or independently assessed factual correctness. Internal source identifiers also do not constitute scholarly citations.

The study has not been evaluated on a widely accepted external multilingual embedding benchmark or shared task. Consequently, the reported metrics measure internal consistency and retrieval behavior within the project resources. They do not establish comparative performance, external linguistic validity, or robustness on independently sourced Turkic data.

## 7.3 Experimental Validity

The repository does not contain controlled retraining ablations for the `ROOT`, `COGNATE`, `LINEAGE`, or `LANGUAGE` signals. Existing feature-availability and RAG source-contribution counts show that these evidence paths participate in retrieval, but they do not measure the causal effect of adding or removing a feature. The proxy ablation summary must therefore not be interpreted as a controlled ablation experiment.

Comparable baseline evaluation is also unavailable. No stored evaluation exists for a vanilla FastText model trained on the same corpus without linguistic signal injection, and no directly comparable Word2Vec, BM25, multilingual transformer, or sentence-embedding baseline is reported. Improvement over a baseline is consequently not computable. Historical-only or morphology-only baseline variants are likewise absent.

Other experimental constraints documented in the audits include manually fixed RAG ranking weights and narrow semantic-search candidate expansion. These choices have not been tuned or validated on an independent development set. Stored cluster results also show negative separation for cognate and language-family clusters, demonstrating that positive pair-level similarity does not imply clean global clustering. No unreported statistical tests or effect sizes are used to compensate for these gaps.

## 7.4 Generalization Validity

The dataset covers eight varieties—Uzbek, Turkish, Azerbaijani, Kazakh, Kyrgyz, Turkmen, Uyghur, and Old Turkic—but it does not cover the full Turkic language family, its dialectal diversity, or all historical stages. Results may not generalize to unseen Turkic languages, dialects, orthographic variants, or expert-curated lexica outside the repository.

Domain diversity is also limited. The audits do not establish performance on independently collected corpora, noisy OCR, social-media text, or other naturally occurring domain shifts. Multiple scripts are represented, including Uyghur Arabic, Cyrillic, Latin, and Old Turkic runiform forms, but external normalization and coverage quality require specialist review. The present results therefore should not be generalized to unrestricted multilingual or historical text processing.

Future validation requires source-separated train, validation, and hidden test partitions; expert-reviewed cognate, morphology, historical, and QA annotations; external multilingual benchmarks; and robustness testing across unseen corpora, scripts, dialects, and noisy text.

## 7.5 Reproducibility Considerations

The repository provides substantial reproducibility material. The `paper_package` directory contains figures, tables in CSV, Markdown, and LaTeX formats, statistical and error analyses, metric traceability, table and figure validation, result classification, publication-evidence notes, and reviewer-oriented validity reports. Dataset and model manifests inventory the embedding dataset, semantic index, FastText corpus, model artifacts, benchmark files, and stored evaluation outputs. Evaluator scripts are retained for embedding quality, semantic search, RAG, QA, and cognate alignment. The reproducibility report also documents backend, frontend, SQLite, PostgreSQL, and Docker setup procedures.

Remaining gaps limit exact reruns. Current manuscript validation traces stored artifacts but does not rerun training or regenerate all metrics. FastText results can vary with library versions, worker count, random state, and corpus ordering. Exact hardware specifications were not recorded, so training and latency measurements are environment-specific. Raw similarity distributions are not stored, preventing reproduction of standardized effect sizes. Large model artifacts require an explicit release mechanism, and the repository has no GitHub Actions workflow. The morphology application also has models without committed migrations, while production configuration requires manual environment-file creation.

Reproduction should therefore use an exact repository commit, preserve dependency versions, benchmark-generation procedures, random settings, and corpus order, and distinguish reconstruction of stored results from independent scientific validation.
