# Raw Data Strategy

For Bosqich 1, raw JSON files from `words/` were copied into `data/raw/`.

Reason: copies are portable across Windows setups and do not require symlink privileges or Developer Mode. This keeps the loader and future reproducibility scripts usable from a fresh checkout without depending on the original `words/` directory layout.

The loader still discovers languages dynamically from files matching `*_words.json`, so a future file such as `uyghur_words.json` will be picked up automatically when placed in the configured raw data directory.
