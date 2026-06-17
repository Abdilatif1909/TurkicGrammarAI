# Benchmark Integrity Report
## Summary
The existing morphology benchmarks are mostly synthetic. Uzbek has checked-in generators that sample directly from rule files. Turkish, Azerbaijani, Kazakh, Kyrgyz, Turkmen, Uyghur, and Old Turkic benchmarks were created during engine phases from curated paradigms and productive rule inventories, so they should be treated as rule-coverage benchmarks, not independent accuracy benchmarks.
Independent root/lemma benchmark files were generated under `backend/data/benchmark/independent/` from dictionary/curated word-list sources where available, and from lemma dictionaries only where no separate word list exists. These sets do not include suffix-chain labels generated from analyzer rules.
## Leakage Metrics
| Language | Synthetic cases | Independent cases | Synthetic lemma overlap | Synthetic rule overlap | Synthetic word overlap | Independent lemma overlap | Independent rule overlap | Synthetic/independent word overlap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| uz | 500 | 1000 | 100.0% | 100.0% | 15.8% | 48.7% | 0.0% | 0.81% |
| tr | 500 | 1000 | 100.0% | 99.86% | 0.8% | 51.4% | 0.0% | 19.8% |
| az | 500 | 1000 | 100.0% | 100.0% | 0.6% | 37.9% | 0.0% | 17.34% |
| kk | 500 | 1000 | 99.8% | 100.0% | 15.4% | 79.2% | 0.0% | 23.45% |
| ky | 500 | 1000 | 100.0% | 100.0% | 2.4% | 52.8% | 0.0% | 21.17% |
| tk | 500 | 1000 | 100.0% | 100.0% | 2.4% | 45.9% | 0.0% | 18.29% |
| ug | 500 | 1000 | 100.0% | 100.0% | 2.4% | 100.0% | 0.0% | 2.44% |
| otk | 1000 | 1000 | 100.0% | 100.0% | 39.9% | 24.0% | 0.0% | 0.0% |

## Generator Audit
- `uz`: generate_uzbek_benchmark samples suffixes directly from uzbek_rules.json
- `tr`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `az`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `kk`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `ky`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `tk`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `ug`: created during phase implementation from curated paradigms/rule inventory; no checked-in generator
- `otk`: created during phase implementation from historical paradigms/rule inventory; no checked-in generator

## Interpretation
- Synthetic suffix-chain benchmarks have high rule overlap by construction where suffix chains are annotated. They are useful for regression and coverage, but they overstate real-world accuracy.
- Independent benchmarks intentionally avoid rule-generated suffix chains. Current realistic evaluation therefore measures root/lemma recovery, not full morpheme-chain accuracy.
- A fully independent morpheme-level test set still requires manually annotated corpus/dictionary examples with suffix boundaries.

## Independent Files
- `backend/data/benchmark/independent/uz_independent_morphology.json`
- `backend/data/benchmark/independent/tr_independent_morphology.json`
- `backend/data/benchmark/independent/az_independent_morphology.json`
- `backend/data/benchmark/independent/kk_independent_morphology.json`
- `backend/data/benchmark/independent/ky_independent_morphology.json`
- `backend/data/benchmark/independent/tk_independent_morphology.json`
- `backend/data/benchmark/independent/ug_independent_morphology.json`
- `backend/data/benchmark/independent/otk_independent_morphology.json`
