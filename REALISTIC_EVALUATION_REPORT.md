# Realistic Evaluation Report

Independent benchmarks use dictionary/curated word-list surfaces with root/lemma annotations. They do not use analyzer rule files to generate expected suffix chains.

| Language | Cases | Top1 | Top3 | AnyMatch | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| uz | 1000 | 63.8% | 78.7% | 78.7% | 100.0% |
| tr | 1000 | 53.9% | 66.8% | 69.2% | 100.0% |
| az | 1000 | 52.5% | 67.9% | 69.9% | 100.0% |
| kk | 1000 | 76.7% | 80.8% | 81.6% | 100.0% |
| ky | 1000 | 59.2% | 66.3% | 67.1% | 100.0% |
| tk | 1000 | 51.5% | 65.4% | 66.1% | 100.0% |
| ug | 1000 | 99.6% | 100.0% | 100.0% | 100.0% |
| otk | 1000 | 100.0% | 100.0% | 100.0% | 100.0% |

## Notes

- Synthetic benchmarks remain useful for rule coverage regression.
- Independent benchmarks are stricter on real dictionary surfaces but currently evaluate root/lemma correctness where suffix chains are not independently annotated.
- Full morpheme-level independent evaluation still requires hand-annotated suffix chains from corpus/dictionary sources.
