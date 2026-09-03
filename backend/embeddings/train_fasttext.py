"""Train FastText embeddings for TurkicGrammarAI."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time

from gensim.models import FastText


VECTOR_SIZE = 300
WINDOW = 5
MIN_COUNT = 1
EPOCHS = 20


class LineSentence:
    def __init__(self, path: Path) -> None:
        self.path = path

    def __iter__(self):
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                tokens = line.strip().split()
                if tokens:
                    yield tokens


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    corpus_path = project_root / "data" / "processed" / "fasttext_corpus.txt"
    model_path = project_root / "models" / "turkic_fasttext.model"
    vector_path = project_root / "models" / "turkic_fasttext.vec"
    config_path = project_root / "docs" / "reproducibility" / "training_config.json"

    workers = os.cpu_count() or 1
    sentences = LineSentence(corpus_path)

    started_at = datetime.now(timezone.utc)
    start = time.perf_counter()
    model = FastText(
        vector_size=VECTOR_SIZE,
        window=WINDOW,
        min_count=MIN_COUNT,
        workers=workers,
        sg=1,
        seed=42,
    )
    model.build_vocab(corpus_iterable=sentences)
    model.train(
        corpus_iterable=LineSentence(corpus_path),
        total_examples=model.corpus_count,
        epochs=EPOCHS,
    )
    training_time_seconds = time.perf_counter() - start
    finished_at = datetime.now(timezone.utc)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))
    model.wv.save_word2vec_format(str(vector_path))

    config = {
        "vector_size": VECTOR_SIZE,
        "window": WINDOW,
        "min_count": MIN_COUNT,
        "epochs": EPOCHS,
        "workers": workers,
        "vocabulary_size": len(model.wv),
        "corpus_lines": count_lines(corpus_path),
        "training_time_seconds": training_time_seconds,
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": finished_at.isoformat(),
        "corpus_path": "data/processed/fasttext_corpus.txt",
        "model_path": "models/turkic_fasttext.model",
        "vector_path": "models/turkic_fasttext.vec",
        "gensim_version": __import__("gensim").__version__,
        "architecture": "gensim.models.FastText skip-gram",
        "seed": 42,
    }
    write_json(config_path, config)

    print(f"corpus_lines: {config['corpus_lines']}")
    print(f"vocabulary_size: {config['vocabulary_size']}")
    print(f"workers: {workers}")
    print(f"training_time_seconds: {training_time_seconds:.6f}")
    print(f"wrote: {model_path}")
    print(f"wrote: {vector_path}")
    print(f"wrote: {config_path}")


if __name__ == "__main__":
    main()
