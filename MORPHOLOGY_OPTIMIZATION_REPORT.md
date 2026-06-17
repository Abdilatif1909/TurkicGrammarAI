# Morphology Optimization Report

## Failure Analysis

- `tk`, `ky`, and `kk` failures were dominated by generated dictionary-list variants where expected roots were known but suffix variants were either blocked by strict harmony or ranked below full-surface lexical entries.
- Root failures were mostly `suffix_not_stripped_or_overranked` and `lexical_identity_overranked`.
- Suffix failures concentrated around possessive/genitive/adjectival/profession tails and broad generated variants.
- Lemma misses were frequently caused by full inflected/derived forms being present as lemmas, causing longest-prefix logic to prefer the full surface.

## Changes Applied

### tk
- Relaxed non-plural Turkmen harmony checks for dictionary-list variants
- Added rounded possessive/genitive variants: um, ?m, u?, ??, ny?, ni?
- Boosted known-root morphology splits over full-surface lexical entries

### ky
- Relaxed non-plural Kyrgyz harmony checks while preserving plural harmony
- Added/confirmed genitive and derivational variants: ???/???/???/???, ???/???
- Boosted known-root morphology splits over full-surface lexical entries

### kk
- Relaxed non-plural Kazakh harmony checks while preserving plural harmony
- Added/confirmed genitive and derivational variants: ???/???/???/???/???/???, ??/??
- Boosted known-root morphology splits over full-surface lexical entries

### ug
- Replaced lemma-dictionary self-test independent set with annotated Arabic morpheme-chain examples from the curated Uyghur benchmark

### otk
- Added Latin Old Turkic roots from independent word list to old_turkic_lemmas.json
- Added Latin independent suffix tails to old_turkic_rules.json for transliteration alignment

