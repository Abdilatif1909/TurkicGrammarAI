import argparse
import json
import multiprocessing
import time
from pathlib import Path

from gensim.models import FastText
from gensim.models.word2vec import LineSentence


DEFAULT_DATASET = Path("backend/data/embeddings/embedding_dataset.jsonl")
DEFAULT_CORPUS = Path("backend/data/embeddings/fasttext_baseline_corpus.txt")
DEFAULT_MODEL = Path("backend/models/turkic_fasttext_baseline.model")
DEFAULT_VECTORS = Path("backend/models/turkic_fasttext_baseline.vec")
DEFAULT_STATS = Path("backend/data/reports/fasttext_baseline_training_stats.json")


def normalize_token(value: object) -> str:
    return str(value or "").strip().replace(" ", "_")


def marker(prefix: str, value: object) -> str:
    token = normalize_token(value)
    return f"{prefix}_{token}" if token else ""


def record_tokens(record: dict) -> list[str]:
    tokens = [
        normalize_token(record.get("surface_form")),
        normalize_token(record.get("lemma")),
        marker("ROOT", record.get("root")),
        marker("LANG", record.get("language")),
    ]
    tokens.extend(
        f"FEATURE_{normalize_token(feature).upper()}"
        for feature in record.get("features") or []
    )
    return [token for token in tokens if token]


def build_baseline_corpus(dataset_path: Path, corpus_path: Path) -> dict:
    corpus_path.parent.mkdir(parents=True, exist_ok=True)
    lines = 0
    tokens = 0
    with dataset_path.open(encoding="utf-8") as source, corpus_path.open("w", encoding="utf-8") as target:
        for line in source:
            line_tokens = record_tokens(json.loads(line))
            if line_tokens:
                target.write(" ".join(line_tokens) + "\n")
                lines += 1
                tokens += len(line_tokens)
    return {"corpus_path": str(corpus_path), "lines": lines, "tokens": tokens}


def train_baseline_fasttext(
    dataset_path: str | Path = DEFAULT_DATASET,
    corpus_path: str | Path = DEFAULT_CORPUS,
    model_path: str | Path = DEFAULT_MODEL,
    vector_path: str | Path = DEFAULT_VECTORS,
    stats_path: str | Path = DEFAULT_STATS,
    vector_size: int = 300,
    window: int = 5,
    min_count: int = 1,
    epochs: int = 20,
    workers: int | None = None,
) -> dict:
    dataset_path = Path(dataset_path)
    corpus_path = Path(corpus_path)
    model_path = Path(model_path)
    vector_path = Path(vector_path)
    stats_path = Path(stats_path)
    corpus_stats = build_baseline_corpus(dataset_path, corpus_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    vector_path.parent.mkdir(parents=True, exist_ok=True)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    workers = workers or multiprocessing.cpu_count()

    start = time.perf_counter()
    model = FastText(vector_size=vector_size, window=window, min_count=min_count, workers=workers, sg=1)
    model.build_vocab(corpus_iterable=LineSentence(str(corpus_path)))
    model.train(
        corpus_iterable=LineSentence(str(corpus_path)),
        total_examples=model.corpus_count,
        epochs=epochs,
    )
    training_stats = {
        **corpus_stats,
        "model_path": str(model_path),
        "vector_path": str(vector_path),
        "vector_size": vector_size,
        "window": window,
        "min_count": min_count,
        "epochs": epochs,
        "workers": workers,
        "vocabulary_size": len(model.wv),
        "training_time_seconds": round(time.perf_counter() - start, 3),
        "enrichment_tokens": [],
    }
    model.save(str(model_path))
    model.wv.save_word2vec_format(str(vector_path))
    with stats_path.open("w", encoding="utf-8") as target:
        json.dump(training_stats, target, ensure_ascii=False, indent=2)
    return training_stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Train FastText without cognate or lineage enrichment")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--vectors", default=str(DEFAULT_VECTORS))
    parser.add_argument("--stats", default=str(DEFAULT_STATS))
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(train_baseline_fasttext(
        dataset_path=args.dataset,
        corpus_path=args.corpus,
        model_path=args.model,
        vector_path=args.vectors,
        stats_path=args.stats,
        workers=args.workers or None,
    ), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()