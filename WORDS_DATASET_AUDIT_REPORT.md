# Words Dataset Audit Report

Phase 32 audit verifies the existing Words Dataset only. No word records were generated or modified.

## Scope

- Dataset directory: `backend/data/words`
- Included files: language word JSON files only; `manifest.json` is metadata and was not counted as word records.
- Missing expected language files: `backend/data/words/uyghur_words.json` (ug)

## Summary Metrics

| Metric | Value |
|---|---:|
| total_records | 60,000 |
| unique_words | 57,037 |
| unique_lemmas | 520 |
| unique_roots | 520 |
| unique_language_word_pairs | 60,000 |
| real_unique_word_count | 57,037 |
| duplicate_percentage `(language, word)` | 0.0000% |
| global_duplicate_percentage `word` | 4.9383% |

## Language Distribution

| Language | Records | Coverage | File Status |
|---|---:|---:|---|
| uz | 10,000 | 16.6667% | present |
| tr | 10,000 | 16.6667% | present |
| az | 8,000 | 13.3333% | present |
| kk | 8,000 | 13.3333% | present |
| ky | 8,000 | 13.3333% | present |
| tk | 8,000 | 13.3333% | present |
| ug | 0 | 0.0000% | missing |
| otk | 8,000 | 13.3333% | present |

## Duplicate Analysis

| Duplicate Type | Duplicated Keys | Extra Records |
|---|---:|---:|
| word | 2,655 | 2,963 |
| lemma | 520 | 59,480 |
| root | 520 | n/a |
| (language, word) | 0 | 0 |
| (language, lemma) | 649 | 59,351 |

## Data Quality

| Issue | Count | Percent |
|---|---:|---:|
| missing_word | 0 | 0.0000% |
| missing_lemma | 0 | 0.0000% |
| missing_root | 0 | 0.0000% |
| empty_meaning | 0 | 0.0000% |
| empty_source | 0 | 0.0000% |

## Quality By Language

| Language | Records | Missing Lemma | Missing Root | Empty Meaning | Empty Source |
|---|---:|---:|---:|---:|---:|
| uz | 10,000 | 0 | 0 | 0 | 0 |
| tr | 10,000 | 0 | 0 | 0 | 0 |
| az | 8,000 | 0 | 0 | 0 | 0 |
| kk | 8,000 | 0 | 0 | 0 | 0 |
| ky | 8,000 | 0 | 0 | 0 | 0 |
| tk | 8,000 | 0 | 0 | 0 | 0 |
| ug | 0 | 0 | 0 | 0 | 0 |
| otk | 8,000 | 0 | 0 | 0 | 0 |

## Top 100 Duplicated Words

| Rank | Word | Count | Languages |
|---:|---|---:|---|
| 1 | `bil` | 5 | az, otk, tk, tr, uz |
| 2 | `bildi` | 5 | az, otk, tk, tr, uz |
| 3 | `yer` | 4 | az, otk, tr, uz |
| 4 | `yerlar` | 4 | az, otk, tr, uz |
| 5 | `yerim` | 4 | az, otk, tr, uz |
| 6 | `yeri` | 4 | az, otk, tr, uz |
| 7 | `yerda` | 4 | az, otk, tr, uz |
| 8 | `yerdan` | 4 | az, otk, tr, uz |
| 9 | `yersiz` | 4 | az, otk, tr, uz |
| 10 | `yerlik` | 4 | az, otk, tr, uz |
| 11 | `internet` | 4 | az, tk, tr, uz |
| 12 | `internetlar` | 4 | az, tk, tr, uz |
| 13 | `internetim` | 4 | az, tk, tr, uz |
| 14 | `interneti` | 4 | az, tk, tr, uz |
| 15 | `internetda` | 4 | az, tk, tr, uz |
| 16 | `internetdan` | 4 | az, tk, tr, uz |
| 17 | `internetsiz` | 4 | az, tk, tr, uz |
| 18 | `internetli` | 4 | az, tk, tr, uz |
| 19 | `internetlik` | 4 | az, tk, tr, uz |
| 20 | `bildik` | 4 | az, tk, tr, uz |
| 21 | `yarat` | 4 | az, otk, tr, uz |
| 22 | `yaratdi` | 4 | az, otk, tr, uz |
| 23 | `söz` | 4 | az, otk, tk, tr |
| 24 | `sözlar` | 4 | az, otk, tk, tr |
| 25 | `sözim` | 4 | az, otk, tk, tr |
| 26 | `sözum` | 4 | az, otk, tk, tr |
| 27 | `sözüm` | 4 | az, otk, tk, tr |
| 28 | `sözi` | 4 | az, otk, tk, tr |
| 29 | `sözda` | 4 | az, otk, tk, tr |
| 30 | `sözdan` | 4 | az, otk, tk, tr |
| 31 | `sözsiz` | 4 | az, otk, tk, tr |
| 32 | `sözlik` | 4 | az, otk, tk, tr |
| 33 | `baş` | 4 | az, otk, tk, tr |
| 34 | `başlar` | 4 | az, otk, tk, tr |
| 35 | `başim` | 4 | az, otk, tk, tr |
| 36 | `başum` | 4 | az, otk, tk, tr |
| 37 | `başüm` | 4 | az, otk, tk, tr |
| 38 | `başi` | 4 | az, otk, tk, tr |
| 39 | `başda` | 4 | az, otk, tk, tr |
| 40 | `başdan` | 4 | az, otk, tk, tr |
| 41 | `başsiz` | 4 | az, otk, tk, tr |
| 42 | `başlik` | 4 | az, otk, tk, tr |
| 43 | `al` | 4 | az, otk, tk, tr |
| 44 | `aldi` | 4 | az, otk, tk, tr |
| 45 | `alma` | 4 | az, otk, tk, tr |
| 46 | `almaz` | 4 | az, otk, tk, tr |
| 47 | `bilma` | 4 | az, otk, tk, tr |
| 48 | `bilmaz` | 4 | az, otk, tk, tr |
| 49 | `yerli` | 3 | az, tr, uz |
| 50 | `bilim` | 3 | tk, tr, uz |
| 51 | `bilimlar` | 3 | tk, tr, uz |
| 52 | `bilimim` | 3 | tk, tr, uz |
| 53 | `bilimi` | 3 | tk, tr, uz |
| 54 | `bilimda` | 3 | tk, tr, uz |
| 55 | `bilimdan` | 3 | tk, tr, uz |
| 56 | `bilimsiz` | 3 | tk, tr, uz |
| 57 | `bilimli` | 3 | tk, tr, uz |
| 58 | `bilimlik` | 3 | tk, tr, uz |
| 59 | `model` | 3 | az, tr, uz |
| 60 | `modellar` | 3 | az, tr, uz |
| 61 | `modelim` | 3 | az, tr, uz |
| 62 | `modeli` | 3 | az, tr, uz |
| 63 | `modelda` | 3 | az, tr, uz |
| 64 | `modeldan` | 3 | az, tr, uz |
| 65 | `modelsiz` | 3 | az, tr, uz |
| 66 | `modelli` | 3 | az, tr, uz |
| 67 | `modellik` | 3 | az, tr, uz |
| 68 | `eski` | 3 | otk, tr, uz |
| 69 | `eskisiz` | 3 | otk, tr, uz |
| 70 | `ber` | 3 | otk, tk, uz |
| 71 | `berdi` | 3 | otk, tk, uz |
| 72 | `bildim` | 3 | tk, tr, uz |
| 73 | `yaratdik` | 3 | az, tr, uz |
| 74 | `iş` | 3 | az, tk, tr |
| 75 | `işlar` | 3 | az, tk, tr |
| 76 | `işim` | 3 | az, tk, tr |
| 77 | `işum` | 3 | az, tk, tr |
| 78 | `işüm` | 3 | az, tk, tr |
| 79 | `işi` | 3 | az, tk, tr |
| 80 | `işda` | 3 | az, tk, tr |
| 81 | `işdan` | 3 | az, tk, tr |
| 82 | `işa` | 3 | az, tk, tr |
| 83 | `işsiz` | 3 | az, tk, tr |
| 84 | `işli` | 3 | az, tk, tr |
| 85 | `işlik` | 3 | az, tk, tr |
| 86 | `dil` | 3 | az, tk, tr |
| 87 | `dillar` | 3 | az, tk, tr |
| 88 | `dilim` | 3 | az, tk, tr |
| 89 | `dilum` | 3 | az, tk, tr |
| 90 | `dilüm` | 3 | az, tk, tr |
| 91 | `dili` | 3 | az, tk, tr |
| 92 | `dilda` | 3 | az, tk, tr |
| 93 | `dildan` | 3 | az, tk, tr |
| 94 | `dila` | 3 | az, tk, tr |
| 95 | `dilsiz` | 3 | az, tk, tr |
| 96 | `dilli` | 3 | az, tk, tr |
| 97 | `dillik` | 3 | az, tk, tr |
| 98 | `sözler` | 3 | otk, tk, tr |
| 99 | `sözım` | 3 | az, otk, tr |
| 100 | `sözı` | 3 | az, otk, tr |

## Top 100 Duplicated Lemmas

| Rank | Lemma | Count | Languages |
|---:|---|---:|---|
| 1 | `yer` | 480 | az, otk, tr, uz |
| 2 | `söz` | 458 | az, otk, tk, tr |
| 3 | `baş` | 457 | az, otk, tk, tr |
| 4 | `internet` | 437 | az, tk, tr, uz |
| 5 | `ay` | 383 | az, otk, tr |
| 6 | `yol` | 361 | az, otk, tr |
| 7 | `el` | 360 | otk, tk, tr |
| 8 | `bilim` | 336 | tk, tr, uz |
| 9 | `model` | 334 | az, tr, uz |
| 10 | `ata` | 334 | az, otk, tk |
| 11 | `eski` | 329 | otk, tr, uz |
| 12 | `iş` | 318 | az, tk, tr |
| 13 | `dil` | 318 | az, tk, tr |
| 14 | `gün` | 318 | az, tk, tr |
| 15 | `bahar` | 318 | az, tk, tr |
| 16 | `göz` | 318 | az, tk, tr |
| 17 | `et` | 270 | az, tk, tr |
| 18 | `yıl` | 264 | otk, tr |
| 19 | `yürek` | 263 | otk, tr |
| 20 | `til` | 259 | otk, uz |
| 21 | `жаз` | 240 | kk, ky |
| 22 | `qız` | 237 | az, otk |
| 23 | `ana` | 237 | az, otk |
| 24 | `ogul` | 237 | otk, tk |
| 25 | `ini` | 237 | otk, tk |
| 26 | `qulaq` | 236 | az, otk |
| 27 | `ağıl` | 236 | az, otk |
| 28 | `kitap` | 221 | tk, tr |
| 29 | `ev` | 221 | az, tr |
| 30 | `insan` | 221 | az, tr |
| 31 | `oğul` | 221 | az, tr |
| 32 | `halk` | 221 | tk, tr |
| 33 | `su` | 221 | az, tr |
| 34 | `fikir` | 221 | az, tr |
| 35 | `sistem` | 221 | az, tr |
| 36 | `universitet` | 216 | az, uz |
| 37 | `algoritm` | 216 | tk, uz |
| 38 | `texnologiya` | 215 | az, uz |
| 39 | `xalq` | 212 | az, uz |
| 40 | `gök` | 203 | tk, tr |
| 41 | `мектеп` | 197 | kk, ky |
| 42 | `үй` | 197 | kk, ky |
| 43 | `адам` | 197 | kk, ky |
| 44 | `бала` | 197 | kk, ky |
| 45 | `дос` | 197 | kk, ky |
| 46 | `сөз` | 197 | kk, ky |
| 47 | `студент` | 197 | kk, ky |
| 48 | `университет` | 197 | kk, ky |
| 49 | `жол` | 197 | kk, ky |
| 50 | `нан` | 197 | kk, ky |
| 51 | `сүт` | 197 | kk, ky |
| 52 | `гүл` | 197 | kk, ky |
| 53 | `жер` | 197 | kk, ky |
| 54 | `күн` | 197 | kk, ky |
| 55 | `ай` | 197 | kk, ky |
| 56 | `түн` | 197 | kk, ky |
| 57 | `жыл` | 197 | kk, ky |
| 58 | `күз` | 197 | kk, ky |
| 59 | `көз` | 197 | kk, ky |
| 60 | `ой` | 197 | kk, ky |
| 61 | `компьютер` | 197 | kk, ky |
| 62 | `интернет` | 197 | kk, ky |
| 63 | `сан` | 197 | kk, ky |
| 64 | `алгоритм` | 197 | kk, ky |
| 65 | `технология` | 197 | kk, ky |
| 66 | `qara` | 195 | az, otk |
| 67 | `dost` | 194 | az, tk |
| 68 | `gül` | 194 | az, tk |
| 69 | `yeni` | 184 | az, tr |
| 70 | `yavaş` | 184 | az, tr |
| 71 | `uzak` | 184 | tk, tr |
| 72 | `ak` | 184 | tk, tr |
| 73 | `mavi` | 183 | az, tr |
| 74 | `qan` | 179 | otk |
| 75 | `yaz` | 170 | az, tr |
| 76 | `жаман` | 153 | kk, ky |
| 77 | `тез` | 151 | kk, ky |
| 78 | `алыс` | 151 | kk, ky |
| 79 | `көк` | 151 | kk, ky |
| 80 | `bodun` | 140 | otk |
| 81 | `beg` | 140 | otk |
| 82 | `tegin` | 140 | otk |
| 83 | `er` | 140 | otk |
| 84 | `kiši` | 140 | otk |
| 85 | `eči` | 140 | otk |
| 86 | `bitig` | 140 | otk |
| 87 | `tamga` | 140 | otk |
| 88 | `sub` | 140 | otk |
| 89 | `tağ` | 140 | otk |
| 90 | `orman` | 140 | otk |
| 91 | `eb` | 140 | otk |
| 92 | `ot` | 140 | otk |
| 93 | `kün` | 140 | otk |
| 94 | `yultuz` | 140 | otk |
| 95 | `tün` | 140 | otk |
| 96 | `öd` | 140 | otk |
| 97 | `adak` | 139 | otk |
| 98 | `köz` | 139 | otk |
| 99 | `bilig` | 139 | otk |
| 100 | `küč` | 139 | otk |

## Notes

- Duplicate percentage is calculated from duplicate `(language, word)` records because it best reflects duplicate entries inside a language-specific word dataset.
- Global duplicate word values can be valid cross-language homographs; they are reported separately and should not be treated as automatic data errors.
- Missing `ug` coverage reflects that no `uyghur_words.json` file is present in `backend/data/words` during this audit.
