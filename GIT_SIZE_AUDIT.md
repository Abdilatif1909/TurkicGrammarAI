# Git Size Audit

## Current Git Object Size

```text
count: 0
size: 0 bytes
in-pack: 11883
packs: 1
size-pack: 2.61 GiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
```

## Summary

- Current pack size before cleanup: approximately 2.61 GiB.
- Current commit count: 1.
- Largest cause: tracked FastText model artifacts under `backend/models/`.
- Additional tracked generated/vendor artifacts: `backend/venv/`, `frontend/node_modules/`, `backend/data/embeddings/`, and `paper_package/`.

## Top 100 Largest Tracked Working Tree Files

| Rank | Size | Path |
| --- | --- | --- |
| 1 | 2.24 GiB | backend/models/turkic_fasttext.model.wv.vectors_ngrams.npy |
| 2 | 461.54 MiB | backend/models/turkic_fasttext.vec |
| 3 | 163.66 MiB | backend/models/turkic_fasttext.model.wv.vectors_vocab.npy |
| 4 | 163.66 MiB | backend/models/turkic_fasttext.model.syn1neg.npy |
| 5 | 40.13 MiB | backend/data/embeddings/semantic_index.json |
| 6 | 32.45 MiB | backend/data/embeddings/embedding_dataset.jsonl |
| 7 | 18.83 MiB | backend/data/embeddings/fasttext_corpus.txt |
| 8 | 10.13 MiB | frontend/node_modules/@esbuild/win32-x64/esbuild.exe |
| 9 | 8.69 MiB | frontend/node_modules/typescript/lib/typescript.js |
| 10 | 5.93 MiB | frontend/node_modules/typescript/lib/_tsc.js |
| 11 | 5.64 MiB | backend/models/turkic_fasttext.model |
| 12 | 5.54 MiB | backend/data/words/turkish_words.json |
| 13 | 5.33 MiB | backend/data/words/uzbek_words.json |
| 14 | 5.25 MiB | backend/data/words/uyghur_words.json |
| 15 | 5.08 MiB | backend/venv/Lib/site-packages/psycopg2_binary.libs/libcrypto-3-x64-4b440ad6798c0ef77f25bca2a380e056.dll |
| 16 | 4.57 MiB | backend/data/words/kazakh_words.json |
| 17 | 4.55 MiB | backend/data/words/kyrgyz_words.json |
| 18 | 4.49 MiB | backend/data/words/azerbaijani_words.json |
| 19 | 4.38 MiB | backend/data/words/old_turkic_words.json |
| 20 | 4.33 MiB | backend/data/words/turkmen_words.json |
| 21 | 3.99 MiB | backend/data/morphology/old_turkic_lemmas.json |
| 22 | 3.84 MiB | backend/data/normalized/uzbek_words_clean.json |
| 23 | 3.65 MiB | backend/data/normalized/turkish_words_clean.json |
| 24 | 3.22 MiB | backend/data/normalized/old_turkic_words_clean.json |
| 25 | 3.18 MiB | backend/data/normalized/kyrgyz_words_clean.json |
| 26 | 3.18 MiB | backend/data/normalized/kazakh_words_clean.json |
| 27 | 3.06 MiB | backend/data/gold/gold_morphology_dataset.json |
| 28 | 2.95 MiB | backend/data/normalized/azerbaijani_words_clean.json |
| 29 | 2.91 MiB | backend/data/normalized/turkmen_words_clean.json |
| 30 | 2.46 MiB | frontend/node_modules/@rollup/rollup-win32-x64-msvc/rollup.win32-x64-msvc.node |
| 31 | 2.10 MiB | backend/data/morphology/old_turkic_rules.json |
| 32 | 1.92 MiB | frontend/node_modules/@rollup/rollup-win32-x64-gnu/rollup.win32-x64-gnu.node |
| 33 | 1.83 MiB | backend/data/gold/gold_qa_dataset.json |
| 34 | 1.79 MiB | frontend/node_modules/typescript/lib/lib.dom.d.ts |
| 35 | 1.78 MiB | backend/data/reports/rag_retrieval_statistics.json |
| 36 | 1.63 MiB | backend/data/morphology/uyghur_lemmas.json |
| 37 | 1.62 MiB | backend/data/gold/gold_cognates_dataset.json |
| 38 | 1.49 MiB | frontend/node_modules/.vite/deps/react-dom_client.js.map |
| 39 | 1.43 MiB | frontend/node_modules/vite/dist/node/chunks/dep-Dm0c1Wj2.js |
| 40 | 1.37 MiB | frontend/node_modules/@babel/parser/lib/index.js.map |
| 41 | 1.22 MiB | backend/data/morphology/kazakh_lemmas.json |
| 42 | 1.19 MiB | backend/data/morphology/kyrgyz_lemmas.json |
| 43 | 1.11 MiB | backend/data/morphology/turkmen_lemmas.json |
| 44 | 1.07 MiB | backend/data/morphology/azerbaijani_lemmas.json |
| 45 | 1.07 MiB | backend/data/morphology/turkish_lemmas.json |
| 46 | 1.03 MiB | frontend/node_modules/react-dom/cjs/react-dom-profiling.development.js |
| 47 | 1.02 MiB | frontend/node_modules/react-dom/cjs/react-dom-client.development.js |
| 48 | 981.90 KiB | frontend/node_modules/.vite/deps/react-dom_client.js |
| 49 | 922.62 KiB | frontend/node_modules/rollup/dist/es/shared/node-entry.js |
| 50 | 921.85 KiB | frontend/node_modules/rollup/dist/shared/rollup.js |
| 51 | 851.50 KiB | backend/venv/Lib/site-packages/psycopg2_binary.libs/libssl-3-x64-a84bb4e730bb00cd940a15a8db779c5b.dll |
| 52 | 837.71 KiB | backend/data/cognates/cross_language_cognates.json |
| 53 | 779.73 KiB | backend/data/gold/gold_historical_dataset.json |
| 54 | 757.00 KiB | backend/data/embeddings/embedding_quality_benchmark.json |
| 55 | 732.45 KiB | backend/data/morphology/uyghur_rules.json |
| 56 | 707.65 KiB | backend/data/cognates/cognates.json |
| 57 | 650.40 KiB | frontend/node_modules/@babel/types/lib/index.d.ts |
| 58 | 599.63 KiB | backend/data/historical/historical_forms.json |
| 59 | 597.50 KiB | backend/venv/Lib/site-packages/rpds/rpds.cp310-win_amd64.pyd |
| 60 | 595.27 KiB | frontend/node_modules/typescript/lib/lib.webworker.d.ts |
| 61 | 594.44 KiB | backend/data/benchmark/cross_language_cognate_benchmark.json |
| 62 | 593.39 KiB | frontend/node_modules/react-dom/cjs/react-dom-profiling.profiling.js |
| 63 | 574.30 KiB | frontend/node_modules/typescript/lib/typescript.d.ts |
| 64 | 527.77 KiB | backend/venv/Lib/site-packages/rest_framework/static/rest_framework/css/bootstrap.min.css.map |
| 65 | 523.45 KiB | frontend/node_modules/react-dom/cjs/react-dom-client.production.js |
| 66 | 500.65 KiB | frontend/node_modules/@babel/parser/lib/index.js |
| 67 | 439.79 KiB | backend/data/morphology/uzbek_lemmas.json |
| 68 | 439.14 KiB | backend/data/morphology/kazakh_rules.json |
| 69 | 437.98 KiB | backend/venv/Lib/site-packages/Django-5.0.dist-info/RECORD |
| 70 | 434.54 KiB | backend/data/morphology/turkmen_rules.json |
| 71 | 433.19 KiB | frontend/node_modules/typescript/lib/ru/diagnosticMessages.generated.json |
| 72 | 424.89 KiB | language_error_profiles.json |
| 73 | 424.89 KiB | backend/data/reports/language_error_profiles.json |
| 74 | 419.36 KiB | frontend/node_modules/react-dom/cjs/react-dom-server.node.development.js |
| 75 | 415.47 KiB | frontend/node_modules/react-dom/cjs/react-dom-server.edge.development.js |
| 76 | 414.71 KiB | frontend/node_modules/react-dom/cjs/react-dom-server.browser.development.js |
| 77 | 402.61 KiB | backend/data/morphology/kyrgyz_rules.json |
| 78 | 400.03 KiB | backend/data/benchmark/independent/ug_independent_morphology.json |
| 79 | 398.36 KiB | backend/data/embeddings/semantic_search_benchmark.json |
| 80 | 393.22 KiB | backend/venv/Lib/site-packages/redis/commands/core.py |
| 81 | 385.93 KiB | frontend/node_modules/react-dom/cjs/react-dom-server-legacy.browser.development.js |
| 82 | 385.93 KiB | frontend/node_modules/react-dom/cjs/react-dom-server-legacy.node.development.js |
| 83 | 379.71 KiB | backend/data/benchmark/independent/otk_independent_morphology.json |
| 84 | 372.46 KiB | frontend/node_modules/typescript/lib/ja/diagnosticMessages.generated.json |
| 85 | 365.93 KiB | backend/data/benchmark/independent/kk_independent_morphology.json |
| 86 | 365.47 KiB | backend/data/benchmark/independent/ky_independent_morphology.json |
| 87 | 359.69 KiB | backend/data/benchmark/independent/az_independent_morphology.json |
| 88 | 355.68 KiB | backend/data/benchmark/independent/tr_independent_morphology.json |
| 89 | 354.26 KiB | backend/data/benchmark/independent/tk_independent_morphology.json |
| 90 | 353.18 KiB | backend/data/benchmark/independent/uz_independent_morphology.json |
| 91 | 346.35 KiB | frontend/node_modules/react-dom/cjs/react-dom-server.bun.development.js |
| 92 | 338.03 KiB | frontend/node_modules/typescript/lib/ko/diagnosticMessages.generated.json |
| 93 | 337.91 KiB | frontend/node_modules/typescript/lib/fr/diagnosticMessages.generated.json |
| 94 | 336.35 KiB | frontend/node_modules/typescript/lib/de/diagnosticMessages.generated.json |
| 95 | 334.09 KiB | frontend/node_modules/typescript/lib/pl/diagnosticMessages.generated.json |
| 96 | 332.08 KiB | frontend/node_modules/typescript/lib/es/diagnosticMessages.generated.json |
| 97 | 331.60 KiB | frontend/node_modules/vite/dist/node/chunks/dep-CvfTChi5.js |
| 98 | 331.45 KiB | frontend/node_modules/typescript/lib/it/diagnosticMessages.generated.json |
| 99 | 326.50 KiB | backend/venv/Lib/site-packages/psycopg2_binary.libs/libpq-f8307c97fe34cd7eb00d5f773c2bb811.dll |
| 100 | 326.43 KiB | backend/data/embeddings/qa_benchmark.json |

## Top 100 Largest Git History Blobs

| Rank | Unpacked Size | Blob | Path |
| --- | --- | --- | --- |
| 1 | 2.24 GiB | 9803ff6d30f1 | backend/models/turkic_fasttext.model.wv.vectors_ngrams.npy |
| 2 | 461.54 MiB | 607378630d7a | backend/models/turkic_fasttext.vec |
| 3 | 163.66 MiB | ba578bfe1b2a | backend/models/turkic_fasttext.model.wv.vectors_vocab.npy |
| 4 | 163.66 MiB | 4ce4c4a72713 | backend/models/turkic_fasttext.model.syn1neg.npy |
| 5 | 40.13 MiB | 17230c81d5d8 | backend/data/embeddings/semantic_index.json |
| 6 | 32.36 MiB | c4489cef6ab2 | backend/data/embeddings/embedding_dataset.jsonl |
| 7 | 18.73 MiB | 6c47b8478b64 | backend/data/embeddings/fasttext_corpus.txt |
| 8 | 10.13 MiB | afe150252c5b | frontend/node_modules/@esbuild/win32-x64/esbuild.exe |
| 9 | 8.69 MiB | 0554fc3fc707 | frontend/node_modules/typescript/lib/typescript.js |
| 10 | 5.93 MiB | 612a1f7eed0f | frontend/node_modules/typescript/lib/_tsc.js |
| 11 | 5.64 MiB | 2af6b575f7ab | backend/models/turkic_fasttext.model |
| 12 | 5.12 MiB | b1761f95034f | backend/data/words/uyghur_words.json |
| 13 | 5.08 MiB | 8e43cbfc44e4 | backend/venv/Lib/site-packages/psycopg2_binary.libs/libcrypto-3-x64-4b440ad6798c0ef77f25bca2a380e056.dll |
| 14 | 4.43 MiB | 58f28cc3afef | backend/data/words/kyrgyz_words.json |
| 15 | 3.83 MiB | 4b3c1841b9c8 | backend/data/morphology/old_turkic_lemmas.json |
| 16 | 3.72 MiB | 84d8927c5366 | backend/data/normalized/uzbek_words_clean.json |
| 17 | 2.99 MiB | 434dc6a238da | backend/data/gold/gold_morphology_dataset.json |
| 18 | 2.46 MiB | 1322fc1ac0cb | frontend/node_modules/@rollup/rollup-win32-x64-msvc/rollup.win32-x64-msvc.node |
| 19 | 2.05 MiB | badfea6fc09a | backend/data/morphology/old_turkic_rules.json |
| 20 | 1.92 MiB | c8792b52abf1 | frontend/node_modules/@rollup/rollup-win32-x64-gnu/rollup.win32-x64-gnu.node |
| 21 | 1.79 MiB | 14508e8dc3ef | frontend/node_modules/typescript/lib/lib.dom.d.ts |
| 22 | 1.77 MiB | f284b9297436 | backend/data/gold/gold_qa_dataset.json |
| 23 | 1.72 MiB | bb4487d0c81c | backend/data/reports/rag_retrieval_statistics.json |
| 24 | 1.58 MiB | ac74106f7dba | backend/data/gold/gold_cognates_dataset.json |
| 25 | 1.49 MiB | ccfb298e9a08 | frontend/node_modules/.vite/deps/react-dom_client.js.map |
| 26 | 1.47 MiB | 30de86c47b6c | backend/data/words/old_turkic_words.json |
| 27 | 1.43 MiB | 25b83f9c0400 | frontend/node_modules/vite/dist/node/chunks/dep-Dm0c1Wj2.js |
| 28 | 1.37 MiB | b3d52258ce2c | frontend/node_modules/@babel/parser/lib/index.js.map |
| 29 | 1.24 MiB | 1c82b6acd40a | backend/data/words/turkish_words.json |
| 30 | 1.18 MiB | a561f6332181 | backend/data/words/turkmen_words.json |
| 31 | 1.16 MiB | e3b0888923cd | backend/data/words/uzbek_words.json |
| 32 | 1.14 MiB | 88b0c1fed339 | backend/data/morphology/kyrgyz_lemmas.json |
| 33 | 1.03 MiB | 0df4ce8bc7ab | frontend/node_modules/react-dom/cjs/react-dom-profiling.development.js |
| 34 | 1.02 MiB | f41d45037c51 | backend/data/morphology/turkish_lemmas.json |
| 35 | 990.33 KiB | c5b20c38ed58 | backend/data/normalized/old_turkic_words_clean.json |
| 36 | 981.90 KiB | 99473d62db70 | frontend/node_modules/.vite/deps/react-dom_client.js |
| 37 | 959.74 KiB | 6330263b0946 | backend/data/words/kazakh_words.json |
| 38 | 941.77 KiB | 8b75391d7038 | backend/data/normalized/kyrgyz_words_clean.json |
| 39 | 922.62 KiB | 07b9af837b1c | frontend/node_modules/rollup/dist/es/shared/node-entry.js |
| 40 | 921.85 KiB | 6c725b97f319 | frontend/node_modules/rollup/dist/shared/rollup.js |
| 41 | 900.02 KiB | b3e3ebd4fefa | backend/data/words/azerbaijani_words.json |
| 42 | 851.50 KiB | 16b64855812a | backend/venv/Lib/site-packages/psycopg2_binary.libs/libssl-3-x64-a84bb4e730bb00cd940a15a8db779c5b.dll |
| 43 | 837.27 KiB | 7f65157213a6 | backend/data/normalized/turkish_words_clean.json |
| 44 | 753.66 KiB | f4fe0c46ac13 | backend/data/morphology/uyghur_lemmas.json |
| 45 | 750.44 KiB | c1137c8e37a3 | backend/data/gold/gold_historical_dataset.json |
| 46 | 722.82 KiB | b92efcb93d6f | backend/data/embeddings/embedding_quality_benchmark.json |
| 47 | 671.52 KiB | 3a9891387adb | backend/data/cognates/cognates.json |
| 48 | 650.40 KiB | efa49cb138a8 | frontend/node_modules/@babel/types/lib/index.d.ts |
| 49 | 597.50 KiB | 572e6420f9df | backend/venv/Lib/site-packages/rpds/rpds.cp310-win_amd64.pyd |
| 50 | 595.27 KiB | 12f4460b8d7f | frontend/node_modules/typescript/lib/lib.webworker.d.ts |
| 51 | 593.39 KiB | 91621dbe568c | frontend/node_modules/react-dom/cjs/react-dom-profiling.profiling.js |
| 52 | 576.19 KiB | 5027d703158b | backend/data/historical/historical_forms.json |
| 53 | 575.64 KiB | a556cffd32d9 | backend/data/normalized/azerbaijani_words_clean.json |
| 54 | 574.30 KiB | 2c56042e22d0 | frontend/node_modules/typescript/lib/typescript.d.ts |
| 55 | 561.23 KiB | 225406daa168 | backend/data/benchmark/cross_language_cognate_benchmark.json |
| 56 | 559.28 KiB | ef4e215666a7 | backend/data/normalized/turkmen_words_clean.json |
| 57 | 527.77 KiB | 0ae3de50864d | backend/venv/Lib/site-packages/rest_framework/static/rest_framework/css/bootstrap.min.css.map |
| 58 | 523.45 KiB | bbeab5ad7211 | frontend/node_modules/react-dom/cjs/react-dom-client.production.js |
| 59 | 522.41 KiB | a066edadda6c | backend/data/normalized/kazakh_words_clean.json |
| 60 | 500.65 KiB | a7c46672efaa | frontend/node_modules/@babel/parser/lib/index.js |
| 61 | 433.55 KiB | 5e65ad81b200 | backend/venv/Lib/site-packages/Django-5.0.dist-info/RECORD |
| 62 | 433.19 KiB | 68ab58f9ca04 | frontend/node_modules/typescript/lib/ru/diagnosticMessages.generated.json |
| 63 | 419.36 KiB | 50c798df55b5 | frontend/node_modules/react-dom/cjs/react-dom-server.node.development.js |
| 64 | 414.71 KiB | d9c73349e1a6 | frontend/node_modules/react-dom/cjs/react-dom-server.browser.development.js |
| 65 | 410.83 KiB | 5d01dd333c60 | backend/data/reports/language_error_profiles.json |
| 66 | 393.22 KiB | 5967dd3f3533 | backend/venv/Lib/site-packages/redis/commands/core.py |
| 67 | 390.03 KiB | ee8c83a568f3 | backend/data/morphology/kyrgyz_rules.json |
| 68 | 386.96 KiB | d25892578753 | backend/data/benchmark/independent/ug_independent_morphology.json |
| 69 | 376.91 KiB | 8d6450b1ed1e | backend/data/embeddings/semantic_search_benchmark.json |
| 70 | 372.46 KiB | 11bd919bbd56 | frontend/node_modules/typescript/lib/ja/diagnosticMessages.generated.json |
| 71 | 368.96 KiB | 58e64b8e43b3 | backend/data/benchmark/independent/otk_independent_morphology.json |
| 72 | 351.23 KiB | 358909ca152b | backend/data/morphology/kazakh_lemmas.json |
| 73 | 338.03 KiB | 9da61fd9c382 | frontend/node_modules/typescript/lib/ko/diagnosticMessages.generated.json |
| 74 | 337.91 KiB | 0359e6bc561b | frontend/node_modules/typescript/lib/fr/diagnosticMessages.generated.json |
| 75 | 336.35 KiB | 8b740ebd328a | frontend/node_modules/typescript/lib/de/diagnosticMessages.generated.json |
| 76 | 334.09 KiB | 55ea56f33dfa | frontend/node_modules/typescript/lib/pl/diagnosticMessages.generated.json |
| 77 | 332.08 KiB | 5f9440ecd907 | frontend/node_modules/typescript/lib/es/diagnosticMessages.generated.json |
| 78 | 331.60 KiB | 79afdb88dcd5 | frontend/node_modules/vite/dist/node/chunks/dep-CvfTChi5.js |
| 79 | 331.45 KiB | cd46108800ab | frontend/node_modules/typescript/lib/it/diagnosticMessages.generated.json |
| 80 | 329.72 KiB | 877691fc5751 | backend/data/morphology/uyghur_rules.json |
| 81 | 326.50 KiB | f473b6def4e4 | backend/venv/Lib/site-packages/psycopg2_binary.libs/libpq-f8307c97fe34cd7eb00d5f773c2bb811.dll |
| 82 | 322.93 KiB | f76cb1f07ec3 | frontend/node_modules/typescript/lib/tr/diagnosticMessages.generated.json |
| 83 | 322.74 KiB | 0bcd9bb90d43 | frontend/node_modules/typescript/lib/pt-br/diagnosticMessages.generated.json |
| 84 | 317.55 KiB | 215482c45a6a | backend/venv/Lib/site-packages/django/contrib/admin/static/admin/js/vendor/xregexp/xregexp.js |
| 85 | 312.94 KiB | 4193ea320660 | frontend/node_modules/typescript/lib/cs/diagnosticMessages.generated.json |
| 86 | 288.97 KiB | bba374c6224b | frontend/node_modules/typescript/lib/zh-cn/diagnosticMessages.generated.json |
| 87 | 283.44 KiB | 377396963244 | frontend/node_modules/@babel/types/lib/validators/generated/index.js.map |
| 88 | 278.63 KiB | 1a86433c2230 | backend/venv/Lib/site-packages/django/contrib/admin/static/admin/js/vendor/jquery/jquery.js |
| 89 | 274.22 KiB | 2437c2e329e5 | backend/data/evaluation/human_evaluation_benchmark.json |
| 90 | 270.55 KiB | 0fbdd06b9cd1 | frontend/node_modules/react-dom/cjs/react-dom-server.node.production.js |
| 91 | 266.06 KiB | 5ec1afe02d4d | backend/venv/Lib/site-packages/pip/_vendor/certifi/cacert.pem |
| 92 | 263.57 KiB | ad5ee31ef533 | backend/venv/Lib/site-packages/setuptools/config/_validate_pyproject/fastjsonschema_validations.py |
| 93 | 261.78 KiB | 68586fea6363 | frontend/node_modules/react-dom/cjs/react-dom-server.browser.production.js |
| 94 | 257.84 KiB | baf2738773a1 | frontend/node_modules/rollup/dist/es/shared/watch.js |
| 95 | 252.00 KiB | 6ef9b770c1c0 | backend/venv/Lib/site-packages/yaml/_yaml.cp310-win_amd64.pyd |
| 96 | 251.27 KiB | b19f1fde5e2f | backend/venv/Scripts/pythonw.exe |
| 97 | 250.79 KiB | 5bf57823f298 | backend/data/morphology/turkmen_lemmas.json |
| 98 | 248.21 KiB | 5eed8f0f5ad1 | frontend/node_modules/rollup/dist/shared/index.js |
| 99 | 238.01 KiB | 4610b71dad91 | backend/venv/Lib/site-packages/pip/_vendor/idna/uts46data.py |
| 100 | 230.09 KiB | c373361a1420 | frontend/node_modules/vite/dist/node/chunks/dep-DDtvSN7_.js |

## Unnecessary Tracked File Groups Detected

- `backend/venv/`: tracked Python virtual environment.
- `frontend/node_modules/`: tracked npm dependencies.
- `backend/models/`: generated FastText model/vector/numpy artifacts.
- `backend/data/embeddings/`: generated embedding dataset, benchmarks, semantic index, and FastText corpus.
- `paper_package/`: generated manuscript package and validation reports.
- `backend/data/reports/`: generated runtime/evaluation reports.

Detected unnecessary tracked paths in targeted groups: 8957.

## Model File Review

Model artifacts should be kept locally but removed from Git history:

- `backend/models/turkic_fasttext.model.wv.vectors_ngrams.npy` (~2.24 GiB)
- `backend/models/turkic_fasttext.vec` (~461.54 MiB)
- `backend/models/turkic_fasttext.model.wv.vectors_vocab.npy` (~163.66 MiB)
- `backend/models/turkic_fasttext.model.syn1neg.npy` (~163.66 MiB)
- `backend/models/turkic_fasttext.model` (~5.64 MiB)

Regeneration procedure is documented in `GITHUB_PUSH_FIX_REPORT.md`.

## Dataset Review

The following embedding artifacts are generated and should not be tracked:

- `backend/data/embeddings/embedding_dataset.jsonl`
- `backend/data/embeddings/fasttext_corpus.txt`
- `backend/data/embeddings/semantic_index.json`
- generated benchmark JSON files under `backend/data/embeddings/`

Source datasets under `backend/data/words/`, `backend/data/morphology/`, `backend/data/cognates/`, `backend/data/historical/`, `backend/data/benchmark/`, and `backend/data/gold/` are retained.
