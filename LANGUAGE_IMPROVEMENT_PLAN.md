# Language Improvement Plan

## Improvement Potential Ranking

| Rank | Language | Current Top1 | Target | Gap | Top1 errors | Caveat |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | tk | 22.1% | 60% | 37.9 | 779 |  |
| 2 | otk | 3.4% | 40% | 36.6 | 966 | script_mismatch_latin_benchmark_vs_runiform_analyzer |
| 3 | ky | 23.5% | 60% | 36.5 | 765 |  |
| 4 | kk | 34.7% | 60% | 25.3 | 653 |  |
| 5 | az | 52.8% | 70% | 17.2 | 472 |  |
| 6 | tr | 54.3% | 70% | 15.7 | 457 |  |
| 7 | uz | 63.8% | 70% | 6.2 | 362 |  |
| 8 | ug | 100.0% | 70% | 0 | 0 | benchmark_not_independent_lemma_dictionary_self_test |

## Optimization Roadmap

### Benchmark Fixes First
- Rebuild Uyghur independent evaluation from corpus/dictionary word sources instead of `uyghur_lemmas.json`; current 100% is not credible.
- Split Old Turkic evaluation into `otk_runiform` and `otk_latin` tracks, or add a Latin transliteration normalization layer before analysis. Current 3.4% mostly measures script mismatch.

### Analyzer Ranking Fixes
- Reduce lexical identity priority for surfaces where a known lemma prefix plus productive suffix chain exists. This is the dominant issue for Uzbek and several modern languages.
- Add root/lemma prefix bonuses for dictionary-sourced inflected forms and penalize full-surface lemma analyses when a shorter root is known.
- Expand/repair common case, possessive, plural, and derivational tails from `frequent_surface_tails_after_expected_root` in `language_error_profiles.json`.

### Per-Language Targets
- `tr`: 54.3% -> 70%: focus on ['suffix_not_stripped_or_overranked'] and frequent tails ['un', 'ün', 'u', 'ü', 'da', 'ın', 'ı', 'in'].
- `az`: 52.8% -> 70%: focus on ['suffix_not_stripped_or_overranked', 'lexical_identity_overranked'] and frequent tails ['ün', 'ü', 'un', 'u', 'da', 'ın', 'ı', 'də'].
- `kk`: 34.7% -> 60%: focus on ['suffix_not_stripped_or_overranked', 'lexical_identity_overranked'] and frequent tails ['ды', 'ді', 'ның', 'нің', 'лы', 'шы', 'лі', 'ші'].
- `ky`: 23.5% -> 60%: focus on ['suffix_not_stripped_or_overranked', 'lexical_identity_overranked'] and frequent tails ['нын', 'нин', 'луу', 'лүү', 'чы', 'чи', 'сыз', 'лык'].
- `tk`: 22.1% -> 60%: focus on ['suffix_not_stripped_or_overranked', 'lexical_identity_overranked'] and frequent tails ['um', 'üm', 'uň', 'üň', 'nyň', 'niň', 'ly', 'çy'].
- `otk`: 3.4% -> 40%: focus on ['suffix_not_stripped_or_overranked'] and frequent tails ['ım', 'im', 'um', 'üm', 'ıŋ', 'iŋ', 'uŋ', 'üŋ'].

## Ready For Optimization Sprint

Recommended order: fix benchmark validity for `ug` and `otk`, then apply cross-language ranking changes for lexical identity over-ranking, then run suffix-tail repair by language.
