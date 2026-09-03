# TurkicGrammarAI Data Audit

Stage: Bosqich 0 - Audit
Date: 2026-09-03
Workspace: `D:\Maqolar\scopus\TurcishGrammarAI`
Raw data directory: `words/`

## Scope

The audit inspected every file matching `words/*_words.json`. The language list is detected from filenames and is not hardcoded. `uyghur_words.json` is currently absent, so downstream code should discover available files dynamically.

## Files Found

| File | Detected language | Records | Size bytes | Top-level JSON | Record shape |
|---|---:|---:|---:|---|---|
| `azerbaijani_words.json` | `azerbaijani` | 937 | 332470 | array | flat object |
| `kazakh_words.json` | `kazakh` | 1294 | 471698 | array | flat object |
| `kyrgyz_words.json` | `kyrgyz` | 1375 | 503256 | array | flat object |
| `old_turkic_words.json` | `old_turkic` | 719 | 269105 | array | flat object |
| `turkish_words.json` | `turkish` | 909 | 317425 | array | flat object |
| `turkmen_words.json` | `turkmen` | 869 | 303505 | array | flat object |
| `uzbek_words.json` | `uzbek` | 1741 | 612358 | array | flat object |

Total records across audited files: **7,844**.

## Common Schema

All audited files use the same field set. Each JSON file is a top-level array of objects.

| Field | Observed type | Empty/missing values | Notes |
|---|---|---:|---|
| `word` | string | 0 in every file | Surface word form. |
| `lemma` | string | 0 in every file | Lemma/base form supplied in source data. |
| `root` | string | 0 in every file | Root supplied in source data. |
| `pos` | string | 0 in every file | Values observed in every file: `adjective`, `noun`, `verb`. |
| `ipa` | string | 0 in every file | Broad pronunciation/transliteration-like representation. |
| `meaning` | string | 0 in every file | English gloss or generated description. |
| `frequency` | integer | 0 in every file | Integer frequency-like score. |
| `source` | string | 0 in every file | Source description string. |
| `notes` | string | 0 in every file | Base/derivation notes. |

## Schema Differences Between Languages

No field-level schema differences were found among the seven audited files:

- All files are top-level arrays.
- All records are flat objects.
- All files contain exactly these fields: `word`, `lemma`, `root`, `pos`, `ipa`, `meaning`, `frequency`, `source`, `notes`.
- No audited file contains nested objects or arrays inside records.
- No audited file has missing or empty values for the common fields.

Observed content differences are language/script-specific:

- `azerbaijani`, `turkish`, `turkmen`, `uzbek`, and `old_turkic` mostly use Latin-script forms.
- `kazakh` and `kyrgyz` use Cyrillic-script forms in `word`, `lemma`, and `root`, while `ipa` contains Latin transliteration-like text mixed with suffix notation.
- `old_turkic_words.json` functions as the historical layer source for later lineage processing.

## Duplicate Check

Within each individual language file, duplicate `word` forms were checked. No duplicate `word` values were found inside any single audited file.

| File | Duplicate `word` forms within file |
|---|---:|
| `azerbaijani_words.json` | 0 |
| `kazakh_words.json` | 0 |
| `kyrgyz_words.json` | 0 |
| `old_turkic_words.json` | 0 |
| `turkish_words.json` | 0 |
| `turkmen_words.json` | 0 |
| `uzbek_words.json` | 0 |

## Example Records

### Azerbaijani

```json
{
  "word": "kitab",
  "lemma": "kitab",
  "root": "kitab",
  "pos": "noun",
  "ipa": "kitab",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Azerbaijani lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Kazakh

```json
{
  "word": "кітап",
  "lemma": "кітап",
  "root": "кітап",
  "pos": "noun",
  "ipa": "kitap",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Kazakh lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Kyrgyz

```json
{
  "word": "китеп",
  "lemma": "китеп",
  "root": "китеп",
  "pos": "noun",
  "ipa": "kitep",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Kyrgyz lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Old Turkic

```json
{
  "word": "bodun",
  "lemma": "bodun",
  "root": "bodun",
  "pos": "noun",
  "ipa": "bodun",
  "meaning": "people",
  "frequency": 100000,
  "source": "curated Old Turkic/Orkhon-style lexeme list with historical Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Turkish

```json
{
  "word": "kitap",
  "lemma": "kitap",
  "root": "kitap",
  "pos": "noun",
  "ipa": "kitap",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Turkish lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Turkmen

```json
{
  "word": "kitap",
  "lemma": "kitap",
  "root": "kitap",
  "pos": "noun",
  "ipa": "kitap",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Turkmen lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

### Uzbek

```json
{
  "word": "kitob",
  "lemma": "kitob",
  "root": "kitob",
  "pos": "noun",
  "ipa": "kitob",
  "meaning": "book",
  "frequency": 100000,
  "source": "curated Uzbek lexeme list with Turkic derivational and inflectional expansions",
  "notes": "base lexeme"
}
```

## Implications For Later Stages

- Stage 2 can map `word` to `surface_form`, `meaning` to `semantic_description`, and keep `source`, `frequency`, `ipa`, and `notes` under `source_metadata`.
- `language` should be derived from the filename by removing the `_words.json` suffix.
- `historical_lineage_metadata` should be populated only where lineage information is generated or inferred in later stages; it is not present explicitly in the raw records.
- Because every file currently contains `lemma` and `root`, Stage 2 does not need fallback derivation for the present dataset, but the pipeline should still support null/fallback behavior for future files.
- Future files such as `uyghur_words.json` should be accepted automatically if they match the `*_words.json` pattern, with schema validation warnings if their fields differ.
