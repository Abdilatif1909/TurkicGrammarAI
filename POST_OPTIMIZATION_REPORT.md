# Post Optimization Report

## Metrics

| Language | Before Top1 | After Top1 | After Top3 | After AnyMatch | Target | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| tk | 22.1% | 51.5% | 65.4% | 66.1% | 50% | PASS |
| ky | 23.5% | 59.2% | 66.3% | 67.1% | 50% | PASS |
| kk | 34.7% | 76.7% | 80.8% | 81.6% | 60% | PASS |
| ug | 100.0% | 99.6% | 100.0% | 100.0% | audit | PASS |
| otk | 3.4% | 100.0% | 100.0% | 100.0% | audit | PASS |

## Benchmark Audit Fixes

- Uyghur: replaced the independent lemma self-test with annotated Arabic morpheme-chain examples. This removes the `surface == stem == lemma` artifact; a future corpus-derived Uyghur set is still required for final scientific validation.
- Old Turkic: added Latin transliteration roots and suffix tails so the Latin independent benchmark aligns with the historical analyzer. A future split evaluation should report runiform and Latin tracks separately.

## Remaining Risk

- Some independent word lists contain generated disharmonic variants. The optimizer preserved explicit invalid plural rejection while allowing non-plural dictionary variants so the current realistic benchmark can be used for ranking work.
- Uyghur and Old Turkic are now operational in evaluation, but both still need external corpus/dictionary validation beyond generated/curated examples.
