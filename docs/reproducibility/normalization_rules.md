# Normalization Rules

Bosqich 2 maps every raw record into the unified `LexicalEntry` schema.

## Field Mapping

| Unified field | Raw source |
|---|---|
| `surface_form` | `word` |
| `language` | Filename with `_words.json` removed |
| `lemma` | `lemma` |
| `root` | `root` |
| `pos` | `pos` |
| `semantic_description` | `meaning` |
| `source_metadata.source` | `source` |
| `source_metadata.notes` | `notes` |
| `source_metadata.ipa` | `ipa` |
| `source_metadata.frequency` | `frequency` |
| `source_metadata.source_file` | Raw filename |
| `source_metadata.is_historical` | `true` only for `old_turkic` |
| `historical_lineage_metadata` | `{"is_historical": true}` only for `old_turkic`, otherwise `null` |

## Text Cleanup

- All text values are normalized with Unicode NFC.
- Runs of whitespace, tabs, and newlines are collapsed to a single space.
- Leading and trailing whitespace is stripped.
- Empty strings become `null`.

## Fallbacks

- If `lemma` is empty after cleanup, `lemma` is set to `surface_form` and `source_metadata.lemma_inferred` is set to `true`.
- If `root` is empty after cleanup, `root` is set to `surface_form` and `source_metadata.root_inferred` is set to `true`.
- When a value is present in the raw file, the corresponding inferred flag is `false`.

## Duplicate Checks

- Duplicates are checked after normalization by `(language, surface_form)`.
- Cross-language shared surface forms are reported as statistics only. Cognate grouping is intentionally deferred to Bosqich 3.
