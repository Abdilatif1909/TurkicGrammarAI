# Rule Gap Report

Source: `backend/backend/backend/data/reports/uzbek_morphology_errors.json`

Baseline error counts:

| Error Type | Count |
| ---------- | ----: |
| ROOT_ERROR | 177 |
| RULE_MISSING | 135 |
| SCORING_ERROR | 77 |

## RULE_MISSING Extraction

Extracted `RULE_MISSING` cases: 135

Unique missing expected suffix tokens after rule-map pruning: 46

## Top Missing Suffixes

| Missing suffix | Count | Category | Decision |
| -------------- | ----: | -------- | -------- |
| nimagan | 6 | suffix chain | skipped: object marker + verb participle chain, not a valid single Uzbek suffix |
| lariyor | 5 | suffix chain | skipped: generated plural/possessive + `yor` chain |
| ingizda | 5 | noun morphology | added: 2pl possessive + locative |
| yorning | 5 | suffix chain | skipped: `yor` + genitive chain, not a productive Uzbek suffix rule |
| taish | 5 | derivational chain | skipped: generated `ta` + `ish` chain |
| qaingiz | 5 | noun chain | skipped: invalid Uzbek morpheme order |
| ginda | 5 | particle/case chain | skipped: generated `gin` + locative chain |
| ingish | 4 | derivational chain | skipped: generated possessive + verbal noun chain |
| iyma | 4 | derivational chain | skipped: generated adjectival + nominalizer chain |
| maganden | 4 | verb chain | skipped: non-Uzbek `den` allomorph in this context |
| diringiz | 4 | verb/copular chain | skipped: not added as productive Uzbek suffix |
| lerning | 4 | noun chain | skipped: non-Uzbek `ler` + genitive chain |
| ilari | 4 | noun chain | skipped: invalid Uzbek morpheme order |
| moqdadan | 4 | verb/case chain | skipped: progressive + ablative chain is synthetic here |
| inggina | 4 | noun morphology | added: 2sg possessive + restrictive `-gina` |
| yoruvchi | 4 | derivational chain | skipped: generated `yor` + agentive chain |
| ginaadi | 4 | particle/verb chain | skipped: generated restrictive + finite verb chain |
| dalari | 4 | noun chain | skipped: invalid Uzbek morpheme order |

## Top Missing Suffix Chains

| Missing chain | Count | Decision |
| ------------- | ----: | -------- |
| `ingizda` | 3 | added |
| `moqdadan` | 2 | skipped as synthetic |
| `qaingiz` | 2 | skipped as invalid morpheme order |
| `taish` | 2 | skipped as synthetic |
| `imo'` | 2 | skipped as synthetic/orthographic artifact |
| `damoqda` | 2 | skipped as generated verb chain |
| `uvdeni -> ingish` | 1 | skipped as generated chain |
| `adini -> iyma` | 1 | skipped as generated chain |
| `dir -> ishning` | 1 | partially repaired by adding `ishning` |
| `gina -> ginaadi` | 1 | skipped as generated finite chain |

## Added Rule Groups

Noun morphology:

- `ingizda`: possessive 2pl + locative, as in `kitobingizda`.
- `idan`: possessive 3sg + ablative, as in `uyidan`.
- `inggina`: possessive 2sg + restrictive particle, as in `kitobinggina`.

Verb morphology:

- `magandi`: negative past participle with contracted past copular form, as in `yozmagandi`.

Derivational morphology:

- `ishning`: verbal noun `-ish` + genitive, as in `o'qishning`.
- `ginacha`: restrictive `-gina` + approximative `-cha`, as in `shunginacha`.

## Skipped Patterns

The remaining high-frequency gaps are mostly generated suffix chains and are intentionally not added before scoring optimization. Adding them would reduce `RULE_MISSING` numerically but would encode synthetic combinations as rules.
