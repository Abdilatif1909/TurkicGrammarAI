# Corpus app

This app implements corpus ingestion, normalization, deduplication, sentence segmentation, tokenization and statistics required to prepare a research-grade Turkic corpus for downstream embedding/model training.

Key components:

- `models.py`: `CorpusSource`, `CorpusDocument`, `CorpusSentence`, `CorpusToken`.
- `services/`: ingestion, normalization, dedupe, segmentation, tokenization, statistics.
- `management/commands/`: `import_corpus`, `normalize_corpus`, `build_sentences`, `build_tokens`.
- `views.py` + `urls.py`: `GET /api/corpus/statistics/`.

Usage examples:

1. Place files into `backend/data/corpus/<language>/` (supported formats: TXT/JSON/CSV/XML).
2. Run import:

```bash
python manage.py import_corpus --path backend/data/corpus --source wiktionary
```

3. Normalize texts:

```bash
python manage.py normalize_corpus
```

4. Build sentences and tokens:

```bash
python manage.py build_sentences
python manage.py build_tokens
```

Notes:
- This app deliberately avoids training any embeddings or models — it prepares the corpus only.
- The services are intentionally simple and meant to be replaced/integrated with language-specific NLP pipelines later.
