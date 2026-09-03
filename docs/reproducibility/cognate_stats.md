# Cognate Grouping Statistics

Stage: Bosqich 3 - Cognate-aware layer

## Deterministic Rules

- Input is `data/processed/lexicon_master.jsonl`.
- Tier 1 groups entries by cross-language `surface_form` matches.
- Tier 2 groups entries by cross-language `lemma` matches.
- Text comparison applies Unicode NFC, casefolding, whitespace cleanup, Cyrillic-to-Latin character mapping for Kazakh/Kyrgyz-style Cyrillic, Latin diacritic folding, and removal of non-alphanumeric separators.
- A match is accepted when the cleaned strings are exactly equal, the comparison keys are exactly equal, or the comparison keys have edit distance <= 1 with both keys at least 4 characters long, the same first character, and at least one shared non-generic semantic gloss.
- A cognate group must contain at least two distinct languages.
- Edges require matching `pos` to reduce cross-POS homograph merges.
- Tier labels are `tier1`, `tier2`, or `both` depending on which edge types contributed to the final connected component.

## Script Audit

| Language | Latin | Cyrillic | Mixed | Other |
|---|---:|---:|---:|---:|
| `azerbaijani` | 937 | 0 | 0 | 0 |
| `kazakh` | 0 | 1294 | 0 | 0 |
| `kyrgyz` | 0 | 1375 | 0 | 0 |
| `old_turkic` | 719 | 0 | 0 | 0 |
| `turkish` | 909 | 0 | 0 | 0 |
| `turkmen` | 869 | 0 | 0 | 0 |
| `uzbek` | 1722 | 0 | 19 | 0 |

## Summary

- Total cognate groups: **147**
- Groups with Tier 1 support: **147**
- Groups with Tier 2 support: **130**
- Tier 1 only groups: **17**
- Tier 2 only groups: **0**
- Groups supported by both tiers: **130**
- Average languages per group: **3.3469**
- Isolated entries with no cognate group: **2470**

## Largest Groups

| Cognate ID | Tier | Languages | Members | Example members |
|---|---|---:|---:|---|
| `COGNATE_12` | `both` | 7 | 94 | azerbaijani:baş(baş); azerbaijani:başlar(baş); azerbaijani:başım(baş); azerbaijani:başın(baş); azerbaijani:başı(baş); azerbaijani:başda(baş); azerbaijani:başa(baş); azerbaijani:başsiz(baş); ... +86 more |
| `COGNATE_14` | `both` | 7 | 94 | azerbaijani:bilik(bilik); azerbaijani:biliklar(bilik); azerbaijani:biliklər(bilik); azerbaijani:bilikin(bilik); azerbaijani:biliki(bilik); azerbaijani:bilikdə(bilik); azerbaijani:bilikdən(bilik); azerbaijani:biliksiz(bilik); ... +86 more |
| `COGNATE_60` | `both` | 7 | 94 | azerbaijani:söz(söz); azerbaijani:sözlar(söz); azerbaijani:sözlər(söz); azerbaijani:sözüm(söz); azerbaijani:sözün(söz); azerbaijani:sözü(söz); azerbaijani:sözdən(söz); azerbaijani:sözsiz(söz); ... +86 more |

## Language Pair Cognate Density

| Language pair | Cognate groups shared |
|---|---:|
| `azerbaijani-kazakh` | 31 |
| `azerbaijani-kyrgyz` | 28 |
| `azerbaijani-old_turkic` | 24 |
| `azerbaijani-turkish` | 63 |
| `azerbaijani-turkmen` | 48 |
| `azerbaijani-uzbek` | 38 |
| `kazakh-kyrgyz` | 69 |
| `kazakh-old_turkic` | 30 |
| `kazakh-turkish` | 19 |
| `kazakh-turkmen` | 36 |
| `kazakh-uzbek` | 43 |
| `kyrgyz-old_turkic` | 24 |
| `kyrgyz-turkish` | 26 |
| `kyrgyz-turkmen` | 40 |
| `kyrgyz-uzbek` | 40 |
| `old_turkic-turkish` | 21 |
| `old_turkic-turkmen` | 23 |
| `old_turkic-uzbek` | 30 |
| `turkish-turkmen` | 39 |
| `turkish-uzbek` | 30 |
| `turkmen-uzbek` | 33 |

## Manual Spot-Check

| Cognate ID | Tier | Languages | Members | Review |
|---|---|---:|---:|---|
| `COGNATE_1` | `both` | 5 | 59 | Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages. Example: azerbaijani:ayaq(ayaq); azerbaijani:ayaqlar(ayaq); azerbaijani:ayaqım(ayaq); azerbaijani:ayaqın(ayaq); azerbaijani:ayaqı(ayaq); azerbaijani:ayaqda(ayaq); ... +53 more |
| `COGNATE_50` | `both` | 2 | 22 | Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages. Example: azerbaijani:proqram(proqram); azerbaijani:proqramlar(proqram); azerbaijani:proqramım(proqram); azerbaijani:proqramın(proqram); azerbaijani:proqramı(proqram); azerbaijani:proqramda(proqram); ... +16 more |
| `COGNATE_12` | `both` | 7 | 94 | Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages. Example: azerbaijani:baş(baş); azerbaijani:başlar(baş); azerbaijani:başım(baş); azerbaijani:başın(baş); azerbaijani:başı(baş); azerbaijani:başda(baş); ... +88 more |
| `COGNATE_14` | `both` | 7 | 94 | Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages. Example: azerbaijani:bilik(bilik); azerbaijani:biliklar(bilik); azerbaijani:biliklər(bilik); azerbaijani:bilikin(bilik); azerbaijani:biliki(bilik); azerbaijani:bilikdə(bilik); ... +88 more |
| `COGNATE_60` | `both` | 7 | 94 | Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages. Example: azerbaijani:söz(söz); azerbaijani:sözlar(söz); azerbaijani:sözlər(söz); azerbaijani:sözüm(söz); azerbaijani:sözün(söz); azerbaijani:sözü(söz); ... +88 more |
