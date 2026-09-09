# Reproducibility Package

This directory is the entry point for auditing and reproducing the TurkicGrammarAI dataset, derived linguistic layers, training setup, benchmarks, and reported results. The current release covers **7,844 records in 7 language files**;

## Recommended reading order

1. **Audit — [`../data_audit.md`](../data_audit.md)**  

2. **Dataset — [`dataset_manifest.json`](dataset_manifest.json)**  
   Read the machine-readable normalization manifest for language counts, totals, POS distribution, unique forms, and cross-language surface-form statistics. [`normalization_rules.md`](normalization_rules.md) and [`raw_data_strategy.md`](raw_data_strategy.md) document how that manifest and the normalized lexicon are produced.

3. **Cognates — [`cognate_stats.md`](cognate_stats.md)**  
   Review the deterministic surface/lemma grouping rules, cognate-group totals, script audit, language-pair density, and manual spot checks.

4. **Lineage — [`lineage_stats.md`](lineage_stats.md)**  
   Review the historical-link coverage and claim boundary. These links are **Old Turkic-attested lineage signals**, not Proto-Turkic reconstructions.

5. **Training — [`training_config.json`](training_config.json)**  
   Use the exact FastText hyperparameters, seed, corpus/model paths, package version, vocabulary size, and recorded training metadata. [`corpus_format.md`](corpus_format.md) explains the tagged corpus representation.

6. **Benchmarks — [`benchmark_generation_rules.md`](benchmark_generation_rules.md)**  
   Inspect how the embedding-quality, semantic-search, RAG retrieval, and QA benchmarks are generated, including measured sizes and sample records.

7. **Results — [`results_tables.md`](results_tables.md)**  
   Use this as the canonical consolidated result report. It separates oracle/metadata consistency checks from embedding-only model measurements and includes confidence intervals and scale limitations. Machine-readable evaluator outputs are stored alongside it as `results_*.json`.

8. **Leakage diagnosis — [`leakage_diagnosis.md`](leakage_diagnosis.md)**  
   Finish with the circularity analysis and tagged-versus-Surface+POS comparison. The corresponding machine-readable output is [`leakage_diagnosis.json`](leakage_diagnosis.json).

## Interpretation rule

Do not report the 100% oracle RAG or template-QA figures as model accuracy. They test metadata/template consistency. For model behavior, use embedding-only QA and embedding-only cross-language RAG, and disclose the no-tag leakage comparison.
