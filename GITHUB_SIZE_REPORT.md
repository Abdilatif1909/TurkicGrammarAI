# GitHub Size Report

Generated for Phase 36.7 repository publication preparation on 2026-06-17.

## Summary

Current Git object size:

```text
count: 1
size: 3.50 KiB
in-pack: 485
packs: 1
size-pack: 4.45 MiB
```

Current tracked working-tree files are GitHub-friendly. The largest tracked files are linguistic datasets and morphology resources, mostly between 3 MB and 6 MB. The `paper_package/` directory is about 188 KB across 44 files and should remain in Git.

Large local artifacts are present on disk but ignored by `.gitignore`: FastText binaries, generated embedding indexes/corpora, virtual environments, `node_modules`, and logs.

## Keep In Repository

These files and directories should remain tracked for public research release and reviewer reproducibility:

- Source code: `backend/apps/`, `backend/config/`, `frontend/src/`, `scripts/`, `infra/`.
- Dependency manifests and configuration examples: `requirements.txt`, `backend/requirements.txt`, `frontend/package.json`, `frontend/package-lock.json`, `.env.example`, `.env.production.example`.
- Canonical datasets needed for reproducibility: `backend/data/words/`, `backend/data/morphology/`, `backend/data/cognates/`, `backend/data/historical/`, `backend/data/benchmark/`, `backend/data/evaluation/`, `backend/data/gold/`.
- Documentation and reports: `README.md`, `docs/`, root-level `*_REPORT.md`, `DATASET_MANIFEST.md`, `MODEL_MANIFEST.md`, `REPRODUCIBILITY_REPORT.md`.
- Scientific paper package: `paper_package/figures/`, `paper_package/tables/`, `paper_package/analysis/`, `paper_package/validation/`, `paper_package/reports/`.
- Publication support docs: `RESEARCH_ARTIFACTS.md`, `SCOPUS_PREPARATION.md`, `REPOSITORY_PUBLICATION_STATUS.md`, `GITHUB_SIZE_REPORT.md`.

## Remove From Repository

These should not be committed to Git. They are already ignored in the current `.gitignore` or should remain external artifacts:

- Virtual environments: `.venv/`, `venv/`, `backend/venv/`, `env/`, `ENV/`.
- Node dependencies and builds: `node_modules/`, `frontend/node_modules/`, `frontend/dist/`, `dist/`.
- FastText/model binaries: `backend/models/`, `*.model`, `*.vec`, `*.npy`.
- Generated embedding/search artifacts: `backend/data/embeddings/semantic_index.json`, `embedding_dataset.jsonl`, `fasttext_corpus.txt`, generated embedding benchmarks, and related caches unless a specific publication release decides to archive them externally.
- Generated runtime reports and logs: `backend/data/reports/`, `logs/`, `backend/logs/`, `*.log`, `*.pid`.
- Local databases and caches: `*.sqlite3`, `*.db`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.coverage`, `htmlcov/`.
- OS/editor state: `.DS_Store`, `Thumbs.db`, `.vscode/`, `.idea/`.

## Largest Tracked Files

Largest tracked files at this review:

| Size | Path |
| ---: | --- |
| 5,813,261 bytes | `backend/data/words/turkish_words.json` |
| 5,592,463 bytes | `backend/data/words/uzbek_words.json` |
| 5,508,568 bytes | `backend/data/words/uyghur_words.json` |
| 4,793,472 bytes | `backend/data/words/kazakh_words.json` |
| 4,775,118 bytes | `backend/data/words/kyrgyz_words.json` |
| 4,706,168 bytes | `backend/data/words/azerbaijani_words.json` |
| 4,591,741 bytes | `backend/data/words/old_turkic_words.json` |
| 4,543,356 bytes | `backend/data/words/turkmen_words.json` |
| 4,180,905 bytes | `backend/data/morphology/old_turkic_lemmas.json` |
| 4,023,225 bytes | `backend/data/normalized/uzbek_words_clean.json` |

These sizes are acceptable for GitHub.

## Largest Local Ignored Files

Largest local files observed on disk but excluded from Git:

| Size | Path |
| ---: | --- |
| 2,400,000,128 bytes | `backend/models/turkic_fasttext.model.wv.vectors_ngrams.npy` |
| 483,955,501 bytes | `backend/models/turkic_fasttext.vec` |
| 171,613,328 bytes | `backend/models/turkic_fasttext.model.syn1neg.npy` |
| 171,613,328 bytes | `backend/models/turkic_fasttext.model.wv.vectors_vocab.npy` |
| 42,081,946 bytes | `backend/data/embeddings/semantic_index.json` |
| 34,028,032 bytes | `backend/data/embeddings/embedding_dataset.jsonl` |
| 19,744,457 bytes | `backend/data/embeddings/fasttext_corpus.txt` |
| 10,617,344 bytes | `frontend/node_modules/@esbuild/win32-x64/esbuild.exe` |
| 9,112,572 bytes | `frontend/node_modules/typescript/lib/typescript.js` |
| 6,213,092 bytes | `frontend/node_modules/typescript/lib/_tsc.js` |

These files should be distributed through GitHub Releases, Git LFS, institutional storage, Zenodo/OSF, or regenerated locally from documented scripts rather than committed directly.

## GitHub Recommendation

The working tree is ready for a GitHub-friendly public release after committing the documentation updates and tracking `paper_package/`. Do not commit ignored model binaries, generated embedding indexes, dependency folders, caches, or logs.
