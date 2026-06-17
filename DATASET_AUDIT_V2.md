# Dataset Audit V2

Audit date: 2026-06-17

Scope: `backend/data/words`, `backend/data/normalized`, `backend/data/morphology`, `backend/data/cognates`, `backend/data/historical`, `backend/data/embeddings`, `backend/data/benchmark`, `backend/data/gold`, and root statistics JSON files.

This report is based on repository data files, not prior summary reports.

## Summary

The data layer is operational for demos, but not yet publication-grade. The strongest blockers are stale statistics, mixed language-code conventions, heavy synthetic/projection-based generation, weak provenance, and benchmark leakage risk because benchmark builders derive expected cases directly from the same index/dataset used by retrieval.

## Inventory From Files

Words files in `backend/data/words`:

- `azerbaijani_words.json`: 11,903 records
- `kazakh_words.json`: 11,904 records
- `kyrgyz_words.json`: 11,905 records
- `old_turkic_words.json`: 10,928 records
- `turkish_words.json`: 14,905 records
- `turkmen_words.json`: 11,904 records
- `uyghur_words.json`: 11,679 records
- `uzbek_words.json`: 14,902 records

Real total inspected records: 100,038.

Important mismatch: root `words_dataset_statistics.json` says Uyghur is missing and total records are 60,000, but `backend/data/words/uyghur_words.json` exists and the real word files total 100,038 records.

## Major Findings

### 1. Stale dataset statistics

- Files: `words_dataset_statistics.json`, `backend/data/words/uyghur_words.json`
- Risk: high
- Evidence: `words_dataset_statistics.json` reports Uyghur file missing and 60,000 total records; actual `backend/data/words` contains `uyghur_words.json` and about 100,038 records.
- Recommendation: regenerate statistics from canonical data and include timestamp/source hash.

### 2. Language identifiers are inconsistent

- Files: `backend/data/words/*.json`
- Risk: high
- Evidence: records include both full names and codes, e.g. `azerbaijani` and `az`, `kazakh` and `kk`, `old` and `otk`, `uzbek` and `uz`.
- Impact: filters, seed imports, embedding language grouping, and statistics can split one language into multiple buckets.
- Recommendation: normalize every data record to canonical codes: `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, `otk`.

### 3. Uyghur coverage exists but is not normalized everywhere

- Files: `backend/data/words/uyghur_words.json`, `backend/data/normalized/`
- Risk: medium-high
- Evidence: raw Uyghur file has 11,679 records, but there is no `backend/data/normalized/uyghur_words_clean.json`.
- Recommendation: run the same validation/normalization pipeline for Uyghur and update manifests/statistics.

### 4. Provenance is too coarse for scientific release

- Files: `backend/data/words/*.json`, `backend/data/embeddings/embedding_dataset.jsonl`
- Risk: high
- Evidence: common source strings are broad; embedding records often use `source: "words_dataset"`.
- Recommendation: add structured provenance fields: `source_id`, `source_type`, `citation`, `license`, `curation_status`, `generated_by`, `reviewer`, `review_status`.

### 5. Synthetic/projection risk is visible in data

- Files: `backend/data/words/uyghur_words.json`, `backend/data/cognates/*.json`, `backend/data/embeddings/semantic_index.json`
- Risk: high
- Evidence: Uyghur source says projected from existing Turkic lexical inventory. Semantic index contains artificial-looking forms and proto IDs such as `*ptk_000178`.
- Recommendation: mark generated/projection items explicitly and exclude them from publication metrics unless reviewed.

### 6. Gold datasets are not actually gold yet

- File: `backend/data/gold/gold_dataset_manifest.json`
- Risk: high
- Evidence: manifest says morphology has 4,621 `candidate_requires_expert_review` and 379 `candidate_synthetic_requires_expert_review`; cognates, historical, and QA records all require expert review.
- Recommendation: rename to `gold_candidates` or add a reviewed subset.

### 7. Benchmark leakage risk is high

- Files: `backend/apps/embeddings/evaluate_semantic_search.py`, `backend/apps/embeddings/evaluate_rag_retrieval.py`, `backend/apps/embeddings/evaluate_turkic_qa.py`
- Risk: high
- Evidence: benchmark generators build expected queries from `semantic_index.json`, then evaluate the same search/retrieval over that index.
- Recommendation: create independent held-out benchmarks with source separation.

### 8. Morphology lemma files are tiny relative to rule files

- Files: `backend/data/morphology/*_lemmas.json`, `backend/data/morphology/*_rules.json`
- Risk: medium-high
- Evidence: lemma files have very small top-level structures compared with hundreds/thousands of rules.
- Recommendation: build language-specific lemma dictionaries from reviewed lexica and measure coverage by POS/language.

### 9. Embedding dataset is large but contaminated by generated sources

- File: `backend/data/embeddings/embedding_dataset.jsonl`
- Risk: high
- Evidence: 100,000 records include `source: "words_dataset"` and generated cognate/historical lineage fields.
- Recommendation: split training corpus from benchmark/test sets and include source strata in evaluation.

### 10. Canonical data roots are unclear

- Files: root-level `data/`, `backend/data/`, root report/stat JSONs.
- Risk: medium
- Evidence: active data seems to live under `backend/data`, but root has stale statistics and legacy reports.
- Recommendation: define one canonical data root and update loaders, README, and scripts.

## Release Blockers

- Normalize language codes in all word and embedding records.
- Regenerate dataset statistics and manifests from canonical data.
- Create reviewed, non-synthetic evaluation subsets.
- Add provenance schema and validation.
- Separate generated benchmarks from scientific benchmarks.

