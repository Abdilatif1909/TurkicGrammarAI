import argparse
import json
import multiprocessing
import time
from pathlib import Path

from gensim.models import FastText
from gensim.models.word2vec import LineSentence


DEFAULT_CORPUS = Path("backend/data/embeddings/fasttext_corpus.txt")
DEFAULT_MODEL = Path("backend/models/turkic_fasttext.model")
DEFAULT_VECTORS = Path("backend/models/turkic_fasttext.vec")
DEFAULT_STATS = Path("backend/data/reports/fasttext_training_stats.json")


def train_fasttext_embeddings(
    corpus_path: str | Path = DEFAULT_CORPUS,
    model_path: str | Path = DEFAULT_MODEL,
    vector_path: str | Path = DEFAULT_VECTORS,
    vector_size: int = 300,
    window: int = 5,
    min_count: int = 1,
    epochs: int = 20,
    workers: int | None = None,
) -> dict:
    corpus_path = Path(corpus_path)
    model_path = Path(model_path)
    vector_path = Path(vector_path)
    stats_path = DEFAULT_STATS
    model_path.parent.mkdir(parents=True, exist_ok=True)
    vector_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    workers = workers or multiprocessing.cpu_count()

    start = time.perf_counter()
    sentences = LineSentence(str(corpus_path))
    model = FastText(
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=workers,
        sg=1,
    )
    model.build_vocab(corpus_iterable=sentences)
    model.train(
        corpus_iterable=LineSentence(str(corpus_path)),
        total_examples=model.corpus_count,
        epochs=epochs,
    )
    training_time = round(time.perf_counter() - start, 3)
    model.save(str(model_path))
    model.wv.save_word2vec_format(str(vector_path))
    stats = {
        "corpus_path": str(corpus_path),
        "model_path": str(model_path),
        "vector_path": str(vector_path),
        "vector_size": vector_size,
        "window": window,
        "min_count": min_count,
        "epochs": epochs,
        "workers": workers,
        "vocabulary_size": len(model.wv),
        "training_time_seconds": training_time,
    }
    with stats_path.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Turkic FastText embeddings")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--vectors", default=str(DEFAULT_VECTORS))
    parser.add_argument("--vector-size", type=int, default=300)
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--min-count", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()
    stats = train_fasttext_embeddings(
        corpus_path=args.corpus,
        model_path=args.model,
        vector_path=args.vectors,
        vector_size=args.vector_size,
        window=args.window,
        min_count=args.min_count,
        epochs=args.epochs,
        workers=args.workers or None,
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
