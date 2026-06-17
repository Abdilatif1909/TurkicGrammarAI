# Uyghur Dataset Report

## Summary

| Metric | Value |
|---|---:|
| records | 8,000 |
| unique_words | 8,000 |
| unique_lemmas | 321 |
| unique_roots | 321 |
| duplicate `(language, word)` records | 0 |
| missing lemma | 0 |
| missing root | 0 |
| missing source | 0 |
| invalid POS tags | 0 |

## Method

Uyghur entries were added as Arabic-script lexical records using transliterated seed lemmas from the existing Turkic lexical inventory plus productive Uyghur-style noun, possessive, case, and derivational surface forms. Colliding surface forms were skipped to preserve zero duplicate `(language, word)` records.

## Limitation

This is a completion dataset for platform coverage and requires expert review before being treated as a publication-grade Uyghur dictionary.
