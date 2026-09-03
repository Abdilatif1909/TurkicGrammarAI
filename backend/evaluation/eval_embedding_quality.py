"""Evaluate embedding-quality benchmark with real FastText similarities."""

from __future__ import annotations

from statistics import mean

from gensim.models import KeyedVectors

from common import load_jsonl, project_root, write_json, wilson_interval
from vector_utils import topn_for_queries


def evaluate_pairs(kv, rows: list[dict]) -> dict:
    positive_scores = []
    negative_scores = []
    skipped_similarity = 0

    for row in rows:
        form_a = row["form_a"]
        form_b = row["form_b"]
        try:
            score = float(kv.similarity(form_a, form_b))
        except KeyError:
            skipped_similarity += 1
            continue
        if row["label"] == "positive":
            positive_scores.append(score)
        else:
            negative_scores.append(score)

    positives = [row for row in rows if row["label"] == "positive"]
    queries = {row["form_a"] for row in positives}
    neighbors_by_query = topn_for_queries(kv, queries, topn=10)

    evaluated_topk = 0
    skipped_topk = 0
    hits = {1: 0, 5: 0, 10: 0}
    for row in positives:
        form_a = row["form_a"]
        form_b = row["form_b"]
        neighbors = neighbors_by_query.get(form_a)
        if neighbors is None or form_b not in kv.key_to_index:
            skipped_topk += 1
            continue
        evaluated_topk += 1
        for k in hits:
            if form_b in neighbors[:k]:
                hits[k] += 1

    mean_positive = mean(positive_scores) if positive_scores else None
    mean_negative = mean(negative_scores) if negative_scores else None
    margin = (
        mean_positive - mean_negative
        if mean_positive is not None and mean_negative is not None
        else None
    )

    topk_metrics = {}
    for k, success_count in hits.items():
        value = success_count / evaluated_topk if evaluated_topk else None
        topk_metrics[f"top_{k}_accuracy"] = {
            "value": value,
            "hits": success_count,
            "n": evaluated_topk,
            "wilson_95_ci": wilson_interval(success_count, evaluated_topk),
        }

    return {
        "benchmark_rows": len(rows),
        "positive_pairs": len(positives),
        "negative_pairs": sum(1 for row in rows if row["label"] == "negative"),
        "similarity_evaluated_pairs": len(positive_scores) + len(negative_scores),
        "similarity_skipped_pairs": skipped_similarity,
        "positive_similarity_pairs": len(positive_scores),
        "negative_similarity_pairs": len(negative_scores),
        "mean_positive_similarity": mean_positive,
        "mean_negative_similarity": mean_negative,
        "separation_margin": margin,
        "topk_methodology": "For each positive pair, check whether form_b appears among the top-K nearest in-vocabulary neighbors of form_a; self-neighbor is excluded.",
        "topk_evaluated_positive_pairs": evaluated_topk,
        "topk_skipped_positive_pairs": skipped_topk,
        "topk": topk_metrics,
    }


def main() -> None:
    root = project_root()
    kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext.vec")
    )
    rows = load_jsonl(root / "data" / "benchmarks" / "embedding_quality_benchmark.jsonl")
    result = evaluate_pairs(kv, rows)
    output_path = root / "docs" / "reproducibility" / "results_embedding_quality.json"
    write_json(output_path, result)

    print(f"similarity_evaluated_pairs: {result['similarity_evaluated_pairs']}")
    print(f"topk_evaluated_positive_pairs: {result['topk_evaluated_positive_pairs']}")
    print(f"mean_positive_similarity: {result['mean_positive_similarity']:.6f}")
    print(f"mean_negative_similarity: {result['mean_negative_similarity']:.6f}")
    print(f"separation_margin: {result['separation_margin']:.6f}")
    for name, metric in result["topk"].items():
        print(f"{name}: {metric['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
