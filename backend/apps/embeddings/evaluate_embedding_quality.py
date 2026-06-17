import json
import random
import time
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
from gensim.models import FastText


MODEL_PATH = Path("backend/models/turkic_fasttext.model")
COGNATES_PATH = Path("backend/data/cognates/cross_language_cognates.json")
DATASET_PATH = Path("backend/data/embeddings/embedding_dataset.jsonl")
BENCHMARK_PATH = Path("backend/data/embeddings/embedding_quality_benchmark.json")
STATS_PATH = Path("backend/data/reports/embedding_quality_statistics.json")
QUALITY_REPORT = Path("EMBEDDING_QUALITY_REPORT.md")
ERROR_REPORT = Path("EMBEDDING_ERROR_REPORT.md")
TRAINING_STATS = Path("backend/data/reports/fasttext_training_stats.json")

AUDIT_WORDS = ["tangri", "tanrı", "teŋri", "kitob", "kitap", "kishi", "kişi"]
RANDOM_SEED = 22


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_dataset_records(limit: int = 100_000) -> List[Dict]:
    records = []
    if not DATASET_PATH.exists():
        return records
    with DATASET_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            records.append(json.loads(line))
            if len(records) >= limit:
                break
    return records


def pair_record(word_a: str, word_b: str, category: str, label: int, expected_group: str = "") -> Dict:
    return {
        "word_a": word_a,
        "word_b": word_b,
        "category": category,
        "label": label,
        "expected_group": expected_group,
    }


def generate_embedding_quality_benchmark(path: Path = BENCHMARK_PATH, min_pairs: int = 5000) -> Dict:
    random.seed(RANDOM_SEED)
    cognates = load_json(COGNATES_PATH, [])
    records = load_dataset_records()
    pairs = []

    curated = [
        ("tangri", "tanrı", "cognates", 1),
        ("kitob", "kitap", "cognates", 1),
        ("kishi", "kişi", "cognates", 1),
        ("kitoblarimizdan", "kitaplarımızdan", "cross_language_equivalents", 1),
        ("kitob", "kitap", "cross_language_equivalents", 1),
        ("kitob", "kitoblar", "morphological_variants", 1),
        ("kitoblar", "kitoblarimiz", "morphological_variants", 1),
        ("kitoblarimiz", "kitoblarimizdan", "morphological_variants", 1),
        ("teŋri", "tangri", "historical_relations", 1),
        ("teŋri", "tanrı", "historical_relations", 1),
        ("kitob", "ot", "negative_pairs", 0),
        ("tanrı", "bozor", "negative_pairs", 0),
        ("kishi", "daryo", "negative_pairs", 0),
    ]
    for item in curated:
        pairs.append(pair_record(*item))

    for group in cognates:
        forms = [form for form in (group.get("forms") or {}).values() if form]
        for a, b in combinations(forms[:8], 2):
            pairs.append(pair_record(a, b, "cognates", 1, group.get("cognate_id", "")))
            if len(pairs) >= 1800:
                break
        if len(pairs) >= 1800:
            break

    for group in cognates[:250]:
        proto = group.get("proto_form", "").lstrip("*")
        for lang in ["uz", "tr", "kk", "ug", "otk"]:
            form = (group.get("forms") or {}).get(lang)
            if proto and form:
                pairs.append(pair_record(proto, form, "historical_relations", 1, group.get("cognate_id", "")))

    by_root = defaultdict(list)
    by_cognate = defaultdict(list)
    by_language = defaultdict(list)
    for record in records:
        by_root[(record.get("language"), record.get("root"))].append(record["surface_form"])
        if record.get("cognate_group"):
            by_cognate[record["cognate_group"]].append(record["surface_form"])
        by_language[record.get("language")].append(record["surface_form"])

    for forms in by_root.values():
        unique = list(dict.fromkeys(forms))
        if len(unique) < 2:
            continue
        for a, b in combinations(unique[:6], 2):
            pairs.append(pair_record(a, b, "morphological_variants", 1))
            if len(pairs) >= 3600:
                break
        if len(pairs) >= 3600:
            break

    for forms in by_cognate.values():
        unique = list(dict.fromkeys(forms))
        if len(unique) < 2:
            continue
        for a, b in combinations(unique[:5], 2):
            pairs.append(pair_record(a, b, "cross_language_equivalents", 1))
            if len(pairs) >= 4300:
                break
        if len(pairs) >= 4300:
            break

    vocabulary = list(dict.fromkeys(record["surface_form"] for record in records if record.get("surface_form")))
    while len(pairs) < min_pairs:
        a, b = random.sample(vocabulary, 2)
        pairs.append(pair_record(a, b, "negative_pairs", 0))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(pairs[:max(min_pairs, len(pairs))], fh, ensure_ascii=False, indent=2)
    categories = defaultdict(int)
    positives = 0
    for pair in pairs:
        categories[pair["category"]] += 1
        positives += int(pair["label"] == 1)
    return {
        "path": str(path),
        "pairs": len(pairs),
        "positive_pairs": positives,
        "negative_pairs": len(pairs) - positives,
        "categories": dict(categories),
    }


def vector(model: FastText, word: str) -> np.ndarray:
    return model.wv.get_vector(word)


def cosine(model: FastText, word_a: str, word_b: str) -> float:
    return float(model.wv.similarity(word_a, word_b))


def rank_target(model: FastText, query: str, target: str, distractors: List[str]) -> int:
    candidates = list(dict.fromkeys([target, *distractors]))
    scored = [(candidate, cosine(model, query, candidate)) for candidate in candidates]
    scored.sort(key=lambda item: item[1], reverse=True)
    for index, (candidate, _) in enumerate(scored, start=1):
        if candidate == target:
            return index
    return len(scored) + 1


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return round(sum(values) / len(values), 6) if values else 0.0


def cluster_similarity(model: FastText, clusters: Dict[str, List[str]], max_items: int = 8) -> Dict:
    intra = []
    inter = []
    cluster_items = {key: list(dict.fromkeys(values))[:max_items] for key, values in clusters.items() if len(set(values)) >= 2}
    keys = list(cluster_items)
    for values in cluster_items.values():
        for a, b in combinations(values, 2):
            intra.append(cosine(model, a, b))
    for left, right in zip(keys[::2], keys[1::2]):
        for a in cluster_items[left][:3]:
            for b in cluster_items[right][:3]:
                inter.append(cosine(model, a, b))
    return {
        "clusters": len(cluster_items),
        "intra_cluster_similarity": mean(intra),
        "inter_cluster_similarity": mean(inter),
        "separation": round(mean(intra) - mean(inter), 6),
    }


def evaluate_embedding_quality() -> Dict:
    benchmark_info = generate_embedding_quality_benchmark()
    benchmark = load_json(BENCHMARK_PATH, [])
    records = load_dataset_records()
    model = FastText.load(str(MODEL_PATH))
    start = time.perf_counter()

    vocabulary = list(dict.fromkeys(record["surface_form"] for record in records if record.get("surface_form")))[:20000]
    rng = random.Random(RANDOM_SEED)
    similarities = []
    positive_sims = []
    negative_sims = []
    top_hits = {1: 0, 5: 0, 10: 0}
    positive_count = 0
    low_similarity_cognates = []

    positive_targets = defaultdict(set)
    for pair in benchmark:
        if pair["label"] == 1:
            positive_targets[pair["word_a"]].add(pair["word_b"])
            positive_targets[pair["word_b"]].add(pair["word_a"])

    for pair in benchmark:
        score = cosine(model, pair["word_a"], pair["word_b"])
        similarities.append(score)
        if pair["label"] == 1:
            positive_count += 1
            positive_sims.append(score)
            distractors = rng.sample(vocabulary, min(50, len(vocabulary)))
            rank = rank_target(model, pair["word_a"], pair["word_b"], distractors)
            for k in top_hits:
                if rank <= k:
                    top_hits[k] += 1
            if score < 0.35:
                low_similarity_cognates.append({**pair, "similarity": round(score, 6)})
        else:
            negative_sims.append(score)

    neighbor_audit = {
        word: [{"word": token, "score": round(float(score), 6)} for token, score in model.wv.most_similar(word, topn=20)]
        for word in AUDIT_WORDS
    }

    incorrect_neighbors = []
    for anchor, expected in list(positive_targets.items())[:500]:
        expected_norm = set(expected)
        for token, score in model.wv.most_similar(anchor, topn=20):
            if token not in expected_norm:
                incorrect_neighbors.append({"anchor": anchor, "neighbor": token, "score": round(float(score), 6)})
    incorrect_neighbors.sort(key=lambda item: item["score"], reverse=True)

    cognate_clusters = defaultdict(list)
    family_clusters = defaultdict(list)
    morphology_clusters = defaultdict(list)
    for record in records[:50000]:
        if record.get("cognate_group"):
            cognate_clusters[record["cognate_group"]].append(record["surface_form"])
        lang = record.get("language")
        if lang in {"tr", "az", "tk"}:
            family_clusters["oghuz"].append(record["surface_form"])
        elif lang in {"kk", "ky"}:
            family_clusters["kipchak"].append(record["surface_form"])
        elif lang in {"uz", "ug"}:
            family_clusters["karluk"].append(record["surface_form"])
        elif lang == "otk":
            family_clusters["old_turkic"].append(record["surface_form"])
        for feature in record.get("features") or []:
            morphology_clusters[feature].append(record["surface_form"])

    cluster_metrics = {
        "cognate_clusters": cluster_similarity(model, cognate_clusters),
        "language_family_clusters": cluster_similarity(model, family_clusters),
        "morphological_clusters": cluster_similarity(model, morphology_clusters),
    }
    training_stats = load_json(TRAINING_STATS, {})
    metrics = {
        "benchmark": benchmark_info,
        "vocabulary_size": len(model.wv),
        "model_parameters": {
            "vector_size": training_stats.get("vector_size", model.vector_size),
            "window": training_stats.get("window"),
            "min_count": training_stats.get("min_count"),
            "epochs": training_stats.get("epochs"),
            "workers": training_stats.get("workers"),
        },
        "top1": round(top_hits[1] / positive_count * 100, 2) if positive_count else 0.0,
        "top5": round(top_hits[5] / positive_count * 100, 2) if positive_count else 0.0,
        "top10": round(top_hits[10] / positive_count * 100, 2) if positive_count else 0.0,
        "mean_cosine_similarity": mean(similarities),
        "positive_pair_similarity": mean(positive_sims),
        "negative_pair_similarity": mean(negative_sims),
        "separation_margin": round(mean(positive_sims) - mean(negative_sims), 6),
        "neighbor_audit": neighbor_audit,
        "cluster_metrics": cluster_metrics,
        "evaluation_time_seconds": round(time.perf_counter() - start, 3),
        "top_100_incorrect_neighbors": incorrect_neighbors[:100],
        "top_100_low_similarity_cognates": sorted(low_similarity_cognates, key=lambda item: item["similarity"])[:100],
    }
    STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with STATS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(metrics, fh, ensure_ascii=False, indent=2)
    write_quality_report(metrics)
    write_error_report(metrics)
    return metrics


def write_quality_report(metrics: Dict) -> None:
    with QUALITY_REPORT.open("w", encoding="utf-8") as md:
        md.write("# Embedding Quality Report\n\n")
        md.write("## Model\n\n")
        md.write(f"- Vocabulary size: {metrics['vocabulary_size']}\n")
        for key, value in metrics["model_parameters"].items():
            md.write(f"- {key}: {value}\n")
        md.write("\n## Evaluation Metrics\n\n")
        md.write("| Metric | Value |\n| --- | ---: |\n")
        for key in ["top1", "top5", "top10", "mean_cosine_similarity", "positive_pair_similarity", "negative_pair_similarity", "separation_margin"]:
            md.write(f"| {key} | {metrics[key]} |\n")
        md.write("\n## Benchmark\n\n")
        md.write(f"- Pairs: {metrics['benchmark']['pairs']}\n")
        md.write(f"- Positive pairs: {metrics['benchmark']['positive_pairs']}\n")
        md.write(f"- Negative pairs: {metrics['benchmark']['negative_pairs']}\n\n")
        md.write("## Cluster Metrics\n\n")
        md.write("| Cluster Type | Clusters | Intra | Inter | Separation |\n| --- | ---: | ---: | ---: | ---: |\n")
        for name, values in metrics["cluster_metrics"].items():
            md.write(f"| {name} | {values['clusters']} | {values['intra_cluster_similarity']} | {values['inter_cluster_similarity']} | {values['separation']} |\n")
        md.write("\n## Neighbor Audit\n\n")
        for word, neighbors in metrics["neighbor_audit"].items():
            md.write(f"### `{word}`\n\n")
            md.write("| Neighbor | Score |\n| --- | ---: |\n")
            for row in neighbors:
                md.write(f"| {row['word']} | {row['score']} |\n")
            md.write("\n")
        md.write("## Error Analysis Summary\n\n")
        md.write(f"- Incorrect neighbor examples: {len(metrics['top_100_incorrect_neighbors'])}\n")
        md.write(f"- Low-similarity cognate examples: {len(metrics['top_100_low_similarity_cognates'])}\n")
        md.write("- Detailed error tables are in `EMBEDDING_ERROR_REPORT.md`.\n")


def write_error_report(metrics: Dict) -> None:
    with ERROR_REPORT.open("w", encoding="utf-8") as md:
        md.write("# Embedding Error Report\n\n")
        md.write("## Top 100 Incorrect Neighbors\n\n")
        md.write("| Anchor | Neighbor | Score |\n| --- | --- | ---: |\n")
        for row in metrics["top_100_incorrect_neighbors"]:
            md.write(f"| {row['anchor']} | {row['neighbor']} | {row['score']} |\n")
        md.write("\n## Top 100 Low-Similarity Cognates\n\n")
        md.write("| Word A | Word B | Category | Similarity |\n| --- | --- | --- | ---: |\n")
        for row in metrics["top_100_low_similarity_cognates"]:
            md.write(f"| {row['word_a']} | {row['word_b']} | {row['category']} | {row['similarity']} |\n")


if __name__ == "__main__":
    stats = evaluate_embedding_quality()
    print(json.dumps({
        "benchmark_pairs": stats["benchmark"]["pairs"],
        "top1": stats["top1"],
        "top5": stats["top5"],
        "top10": stats["top10"],
        "positive_pair_similarity": stats["positive_pair_similarity"],
        "negative_pair_similarity": stats["negative_pair_similarity"],
        "separation_margin": stats["separation_margin"],
    }, ensure_ascii=False, indent=2))
