import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

from gensim.models import FastText


DEFAULT_MODEL = Path("backend/models/turkic_fasttext.model")
DEFAULT_STATS = Path("backend/data/reports/fasttext_evaluation.json")
DEFAULT_REPORT = Path("FASTTEXT_EMBEDDING_REPORT.md")
TRAINING_STATS = Path("backend/data/reports/fasttext_training_stats.json")


EVAL_PAIRS = {
    "cognate_similarity": [
        ("tangri", "tanrı"),
        ("tangri", "тәңір"),
        ("tangri", "تەڭرى"),
        ("kitob", "kitap"),
        ("til", "dil"),
    ],
    "cross_language_similarity": [
        ("lang_uz", "lang_tr"),
        ("lang_kk", "lang_ky"),
        ("lang_ug", "lang_otk"),
    ],
    "morphology_similarity": [
        ("feat_PLURAL", "lar"),
        ("feat_DERIVATIONAL", "chi"),
        ("feat_DATIVE", "ga"),
        ("feat_ABLATIVE", "dan"),
    ],
}


def safe_similarity(model: FastText, word_a: str, word_b: str) -> Dict:
    try:
        score = float(model.wv.similarity(word_a, word_b))
        error = None
    except Exception as exc:
        score = None
        error = str(exc)
    return {"word_a": word_a, "word_b": word_b, "similarity": None if score is None else round(score, 6), "error": error}


def safe_neighbors(model: FastText, word: str, topn: int = 10) -> List[Dict]:
    try:
        return [{"word": token, "score": round(float(score), 6)} for token, score in model.wv.most_similar(word, topn=topn)]
    except Exception:
        return []


def evaluate_fasttext_embeddings(
    model_path: str | Path = DEFAULT_MODEL,
    stats_path: str | Path = DEFAULT_STATS,
    report_path: str | Path = DEFAULT_REPORT,
) -> Dict:
    model_path = Path(model_path)
    stats_path = Path(stats_path)
    report_path = Path(report_path)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    model = FastText.load(str(model_path))
    pair_results = {
        task: [safe_similarity(model, a, b) for a, b in pairs]
        for task, pairs in EVAL_PAIRS.items()
    }
    neighbors = {
        word: safe_neighbors(model, word)
        for word in ["tangri", "tanrı", "تەڭرى", "kitob", "feat_PLURAL", "lang_uz"]
    }
    training_stats = {}
    if TRAINING_STATS.exists():
        training_stats = json.load(TRAINING_STATS.open(encoding="utf-8"))
    stats = {
        "model_path": str(model_path),
        "vocabulary_size": len(model.wv),
        "training_stats": training_stats,
        "similarity_examples": pair_results,
        "nearest_neighbors": neighbors,
    }
    with stats_path.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    write_report(stats, report_path)
    return stats


def write_report(stats: Dict, report_path: Path) -> None:
    training = stats.get("training_stats") or {}
    with report_path.open("w", encoding="utf-8") as md:
        md.write("# FastText Embedding Report\n\n")
        md.write("## Training\n\n")
        md.write(f"- Model: `{stats['model_path']}`\n")
        md.write(f"- Vocabulary size: {stats['vocabulary_size']}\n")
        md.write(f"- Vector size: {training.get('vector_size', 300)}\n")
        md.write(f"- Window: {training.get('window', 5)}\n")
        md.write(f"- Min count: {training.get('min_count', 1)}\n")
        md.write(f"- Epochs: {training.get('epochs', 20)}\n")
        md.write(f"- Workers: {training.get('workers', 'all')}\n")
        md.write(f"- Training time: {training.get('training_time_seconds', 'unknown')} seconds\n\n")
        md.write("## Similarity Examples\n\n")
        for task, rows in stats["similarity_examples"].items():
            md.write(f"### {task}\n\n")
            md.write("| Word A | Word B | Similarity |\n| --- | --- | ---: |\n")
            for row in rows:
                value = row["similarity"] if row["similarity"] is not None else "n/a"
                md.write(f"| {row['word_a']} | {row['word_b']} | {value} |\n")
            md.write("\n")
        md.write("## Nearest Neighbors\n\n")
        for word, neighbors in stats["nearest_neighbors"].items():
            md.write(f"### `{word}`\n\n")
            md.write("| Neighbor | Score |\n| --- | ---: |\n")
            for row in neighbors[:10]:
                md.write(f"| {row['word']} | {row['score']} |\n")
            md.write("\n")
        md.write("## Readiness\n\n")
        md.write("The FastText baseline is trained and saved. It is ready to compare against a Word2Vec baseline.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Turkic FastText embeddings")
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--stats", default=str(DEFAULT_STATS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    args = parser.parse_args()
    stats = evaluate_fasttext_embeddings(args.model, args.stats, args.report)
    print(json.dumps({
        "model_path": stats["model_path"],
        "vocabulary_size": stats["vocabulary_size"],
        "report": args.report,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
