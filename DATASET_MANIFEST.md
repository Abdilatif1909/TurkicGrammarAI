# Dataset Manifest

Generated for Phase 36.5 release preparation on 2026-06-17.

This manifest inventories repository datasets without changing records or evaluation results. Counts are file-level JSON/JSONL record counts where they can be safely inferred.

## Words

| File | Records | Languages | Size |
| --- | ---: | --- | ---: |
| `backend/data/words/azerbaijani_words.json` | 11,903 | `az` | 4,706,168 bytes |
| `backend/data/words/kazakh_words.json` | 11,904 | `kk` | 4,793,472 bytes |
| `backend/data/words/kyrgyz_words.json` | 11,905 | `ky` | 4,775,118 bytes |
| `backend/data/words/old_turkic_words.json` | 10,928 | `otk` | 4,591,741 bytes |
| `backend/data/words/turkish_words.json` | 14,905 | `tr` | 5,813,261 bytes |
| `backend/data/words/turkmen_words.json` | 11,904 | `tk` | 4,543,356 bytes |
| `backend/data/words/uyghur_words.json` | 11,679 | `ug` | 5,508,568 bytes |
| `backend/data/words/uzbek_words.json` | 14,902 | `uz` | 5,592,463 bytes |
| `backend/data/words/manifest.json` | 8 | language manifest | 2,663 bytes |

Total word records excluding `manifest.json`: 100,030.

## Normalized Words

| File | Records | Languages | Size |
| --- | ---: | --- | ---: |
| `backend/data/normalized/azerbaijani_words_clean.json` | 7,594 | `az` | 3,093,460 bytes |
| `backend/data/normalized/kazakh_words_clean.json` | 7,997 | `kk` | 3,334,291 bytes |
| `backend/data/normalized/kyrgyz_words_clean.json` | 8,000 | `ky` | 3,336,286 bytes |
| `backend/data/normalized/old_turkic_words_clean.json` | 7,835 | `otk` | 3,373,511 bytes |
| `backend/data/normalized/turkish_words_clean.json` | 9,486 | `tr` | 3,827,126 bytes |
| `backend/data/normalized/turkmen_words_clean.json` | 7,579 | `tk` | 3,048,811 bytes |
| `backend/data/normalized/uzbek_words_clean.json` | 10,000 | `uz` | 4,023,225 bytes |

Known gap: no normalized Uyghur clean file is present.

## Morphology

| File | Records | Size |
| --- | ---: | ---: |
| `backend/data/morphology/azerbaijani_lemmas.json` | 2 | 1,123,905 bytes |
| `backend/data/morphology/azerbaijani_rules.json` | 564 | 155,826 bytes |
| `backend/data/morphology/derivational_rules.json` | 2 | 3,653 bytes |
| `backend/data/morphology/kazakh_lemmas.json` | 3 | 1,283,679 bytes |
| `backend/data/morphology/kazakh_rules.json` | 2,045 | 449,679 bytes |
| `backend/data/morphology/kyrgyz_lemmas.json` | 3 | 1,252,712 bytes |
| `backend/data/morphology/kyrgyz_rules.json` | 1,840 | 412,275 bytes |
| `backend/data/morphology/old_turkic_lemmas.json` | 6 | 4,180,905 bytes |
| `backend/data/morphology/old_turkic_rules.json` | 5,804 | 2,203,424 bytes |
| `backend/data/morphology/turkish_lemmas.json` | 2 | 1,119,821 bytes |
| `backend/data/morphology/turkish_rules.json` | 564 | 152,136 bytes |
| `backend/data/morphology/turkmen_lemmas.json` | 3 | 1,159,278 bytes |
| `backend/data/morphology/turkmen_rules.json` | 2,061 | 444,964 bytes |
| `backend/data/morphology/universal_features.json` | 4 | 761 bytes |
| `backend/data/morphology/uyghur_lemmas.json` | 5 | 1,710,575 bytes |
| `backend/data/morphology/uyghur_rules.json` | 2,949 | 750,031 bytes |
| `backend/data/morphology/uzbek_lemmas.json` | 2 | 450,349 bytes |
| `backend/data/morphology/uzbek_rules.json` | 376 | 77,497 bytes |

## Cognates And Historical

| File | Records | Languages | Size |
| --- | ---: | --- | ---: |
| `backend/data/cognates/cognates.json` | 1,000 | Turkic cognate sets | 724,637 bytes |
| `backend/data/cognates/cross_language_cognates.json` | 2,000 | cross-language sets | 857,816 bytes |
| `backend/data/cognates/cognate_alignment_rules.json` | 7 | alignment rules | 1,687 bytes |
| `backend/data/cognates/sample_seed.json` | 1 | seed sample | 136 bytes |
| `backend/data/historical/historical_forms.json` | 2,000 | `az`, `kk`, `ky`, `otk`, `tk`, `tr`, `uz` | 614,018 bytes |

## Embedding And Retrieval Data

| File | Records | Languages | Size |
| --- | ---: | --- | ---: |
| `backend/data/embeddings/embedding_dataset.jsonl` | 100,000 | `az`, `kk`, `ky`, `otk`, `tk`, `tr`, `ug`, `uz` | 34,028,032 bytes |
| `backend/data/embeddings/semantic_index.json` | 100,000 | `az`, `kk`, `ky`, `otk`, `tk`, `tr`, `ug`, `uz` | 42,081,946 bytes |
| `backend/data/embeddings/fasttext_corpus.txt` | n/a | training corpus text | 19,744,457 bytes |

## Benchmarks

| File | Records | Size |
| --- | ---: | ---: |
| `backend/data/benchmark/azerbaijani_morphology_benchmark.json` | 500 | 66,320 bytes |
| `backend/data/benchmark/cross_language_benchmark.json` | 1,000 | 243,141 bytes |
| `backend/data/benchmark/cross_language_cognate_benchmark.json` | 2,000 | 608,704 bytes |
| `backend/data/benchmark/kazakh_morphology_benchmark.json` | 500 | 81,245 bytes |
| `backend/data/benchmark/kyrgyz_morphology_benchmark.json` | 500 | 79,995 bytes |
| `backend/data/benchmark/old_turkic_morphology_benchmark.json` | 1,000 | 215,155 bytes |
| `backend/data/benchmark/turkish_morphology_benchmark.json` | 500 | 65,588 bytes |
| `backend/data/benchmark/turkmen_morphology_benchmark.json` | 500 | 72,819 bytes |
| `backend/data/benchmark/uyghur_morphology_benchmark.json` | 500 | 80,777 bytes |
| `backend/data/benchmark/uzbek_derivational_benchmark.json` | 500 | 77,825 bytes |
| `backend/data/benchmark/uzbek_lemma_benchmark.json` | 1,000 | 138,182 bytes |
| `backend/data/benchmark/uzbek_morphology.json` | 500 | 72,842 bytes |
| `backend/data/benchmark/independent/az_independent_morphology.json` | 1,000 | 368,322 bytes |
| `backend/data/benchmark/independent/kk_independent_morphology.json` | 1,000 | 374,713 bytes |
| `backend/data/benchmark/independent/ky_independent_morphology.json` | 1,000 | 374,239 bytes |
| `backend/data/benchmark/independent/otk_independent_morphology.json` | 1,000 | 388,818 bytes |
| `backend/data/benchmark/independent/tk_independent_morphology.json` | 1,000 | 362,765 bytes |
| `backend/data/benchmark/independent/tr_independent_morphology.json` | 1,000 | 364,213 bytes |
| `backend/data/benchmark/independent/ug_independent_morphology.json` | 1,000 | 409,631 bytes |
| `backend/data/benchmark/independent/uz_independent_morphology.json` | 1,000 | 361,655 bytes |
| `backend/data/embeddings/embedding_benchmark.json` | 5 | 1,577 bytes |
| `backend/data/embeddings/embedding_quality_benchmark.json` | 5,000 | 775,166 bytes |
| `backend/data/embeddings/qa_benchmark.json` | 1,000 | 334,260 bytes |
| `backend/data/embeddings/rag_retrieval_benchmark.json` | 1,000 | 221,843 bytes |
| `backend/data/embeddings/semantic_search_benchmark.json` | 2,000 | 407,918 bytes |

## Gold Candidate Data

| File | Records | Status | Size |
| --- | ---: | --- | ---: |
| `backend/data/gold/gold_cognates_dataset.json` | 2,000 | candidate, requires expert review | 1,703,816 bytes |
| `backend/data/gold/gold_historical_dataset.json` | 1,000 | candidate, requires expert review | 798,447 bytes |
| `backend/data/gold/gold_morphology_dataset.json` | 5,000 | candidate, requires expert review | 3,213,330 bytes |
| `backend/data/gold/gold_qa_dataset.json` | 2,000 | candidate, requires expert review | 1,913,929 bytes |
| `backend/data/gold/gold_dataset_manifest.json` | 4 sections | manifest | 555 bytes |

## Notes

- This manifest does not certify scientific validity.
- Synthetic/projection and benchmark leakage limitations are documented in `DATASET_AUDIT_V2.md` and `EMBEDDING_AND_RAG_AUDIT.md`.
- Use expert-reviewed subsets only for publication-grade claims.
