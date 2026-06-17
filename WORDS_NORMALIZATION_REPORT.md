# Words Normalization Report

Phase 33 updated lexical datasets only. No morphology, cognate, embedding, RAG, QA, or frontend modules were modified.

## Baseline To V2

| Metric | Previous | V2 |
|---|---:|---:|
| total_records | 60,000 | 68,000 |
| real_unique_word_count | 57,037 | 65,037 |
| unique_lemmas | 520 | 841 |
| unique_roots | 520 | 841 |
| ug_words | 0 | 8,000 |
| duplicate `(language, word)` records | 0 | 0 |

## Lemma Inventory Explanation

The dataset now contains 65,037 unique surface word values but 841 unique lemmas. This is expected for the current dataset design because each language file stores productive inflectional and derivational variants under a compact set of seed lemmas.

Average words per lemma: 80.8561
Lemma diversity ratio: 1.2368%

## Root Inventory Explanation

The dataset has 841 unique roots. Root count tracks lemma count because generated lexical variants preserve the base root instead of introducing derived roots as separate root entries.

Average words per root: 80.8561
Root diversity ratio: 1.2368%

## Data Quality Validation

| Check | Count |
|---|---:|
| missing_word | 0 |
| missing_lemma | 0 |
| missing_root | 0 |
| missing_language | 0 |
| missing_source | 0 |
| empty_meaning | 0 |
| empty_values_any_required | 0 |
| invalid_pos_tags | 0 |

## Duplicate Classification

| Class | Count |
|---|---:|
| cross_language_homographs | 2,655 |
| identical_lexical_entries | 0 |
| generated_variant_lemmas | 841 |
| potential_data_errors | 0 |

Detailed JSON outputs: `lemma_distribution.json`, `root_distribution.json`, `duplicate_analysis.json`, `words_dataset_statistics_v2.json`.
