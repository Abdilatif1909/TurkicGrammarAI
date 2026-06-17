# Language Quality Audit

## Benchmark Audit

- Uyghur realistic Top1 is 100% because `ug_independent_morphology.json` was built from `uyghur_lemmas.json`, not from an external corpus/dictionary word list. Each case has `surface == stem == lemma`, and `ug` always receives a high-confidence lexical analysis. This is a self-test, not an independent benchmark.
- Old Turkic realistic Top1 is 3.4% because `otk_independent_morphology.json` was built from Latin normalized word-list data, while the Old Turkic analyzer and rules are primarily runiform. Most Latin inflected forms are not normalized into runiform before analysis.
- For modern languages except Uyghur, independent sets come from normalized dictionary/curated word lists. They are more realistic than synthetic suffix-chain benchmarks but still include many generated inflectional expansions.

## Current Realistic Scores

| Language | Top1 | Top3 | AnyMatch | Top1 errors | Main error types |
| --- | ---: | ---: | ---: | ---: | --- |
| uz | 63.8% | 78.7% | 78.7% | 362 | lexical_identity_overranked:197, suffix_not_stripped_or_overranked:165 |
| tr | 54.3% | 66.2% | 69.2% | 457 | suffix_not_stripped_or_overranked:457 |
| az | 52.8% | 67.7% | 69.9% | 472 | suffix_not_stripped_or_overranked:470, lexical_identity_overranked:2 |
| kk | 34.7% | 52.7% | 62.5% | 653 | suffix_not_stripped_or_overranked:425, lexical_identity_overranked:228 |
| ky | 23.5% | 39.3% | 41.3% | 765 | suffix_not_stripped_or_overranked:732, lexical_identity_overranked:33 |
| tk | 22.1% | 44.4% | 49.4% | 779 | suffix_not_stripped_or_overranked:712, lexical_identity_overranked:67 |
| ug | 100.0% | 100.0% | 100.0% | 0 | none |
| otk | 3.4% | 3.4% | 3.4% | 966 | suffix_not_stripped_or_overranked:966 |

## Top Failure Files

Top 100 failures per language are stored in `language_error_profiles.json` and `backend/data/reports/language_error_profiles.json`.

## Language Notes

### uz
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'xon': 52, 'ni': 35, 'ning': 35, 'i': 34, 'siz': 25, 'li': 25, 'chi': 25, 'lik': 25, 'lar': 13, 'lari': 13}
- Dominant error classes: {'lexical_identity_overranked': 197, 'suffix_not_stripped_or_overranked': 165}

### tr
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'un': 32, 'ün': 32, 'u': 32, 'ü': 32, 'da': 30, 'ın': 29, 'ı': 29, 'in': 25, 'i': 25, 'de': 25}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 457}

### az
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'ün': 33, 'ü': 33, 'un': 32, 'u': 32, 'da': 32, 'ın': 30, 'ı': 30, 'də': 28, 'in': 22, 'i': 22}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 470, 'lexical_identity_overranked': 2}

### kk
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'ды': 30, 'ді': 30, 'ның': 30, 'нің': 30, 'лы': 29, 'шы': 29, 'лі': 27, 'ші': 27, 'сыз': 26, 'сіз': 26}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 425, 'lexical_identity_overranked': 228}

### ky
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'нын': 30, 'нин': 30, 'луу': 30, 'лүү': 30, 'чы': 30, 'чи': 30, 'сыз': 27, 'лык': 27, 'сиз': 26, 'лик': 26}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 732, 'lexical_identity_overranked': 33}

### tk
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'um': 37, 'üm': 37, 'uň': 37, 'üň': 37, 'nyň': 37, 'niň': 37, 'ly': 37, 'çy': 37, 'çi': 37, 'li': 36}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 712, 'lexical_identity_overranked': 67}

### ug
- Source mix: {'lemma_dictionary': 1000}
- Frequent expected-root tails: {}
- Dominant error classes: {}

### otk
- Source mix: {'dictionary_or_curated_word_list': 1000}
- Frequent expected-root tails: {'ım': 34, 'im': 34, 'um': 34, 'üm': 34, 'ıŋ': 34, 'iŋ': 34, 'uŋ': 34, 'üŋ': 34, 'ı': 33, 'i': 33}
- Dominant error classes: {'suffix_not_stripped_or_overranked': 966}

