"""Evaluate semantic-search benchmark with FastText nearest neighbors."""

from __future__ import annotations

from gensim.models import KeyedVectors

from common import load_jsonl, project_root, write_json, wilson_interval
from vector_utils import has_relevant, topn_for_queries


def evaluate(kv, rows: list[dict]) -> dict:
    queries = {row["query_form"] for row in rows}
    neighbors_by_query = topn_for_queries(kv, queries, topn=10)
    hits = {1: 0, 5: 0, 10: 0}
    evaluated = 0
    skipped = 0

    for row in rows:
        neighbors = neighbors_by_query.get(row["query_form"])
        if neighbors is None:
            skipped += 1
            continue
        evaluated += 1
        relevant = {item["form"] for item in row["relevant"]}
        for k in hits:
            if has_relevant(neighbors, relevant, k):
                hits[k] += 1

    return {
        "queries": len(rows),
        "evaluated_queries": evaluated,
        "skipped_queries": skipped,
        "methodology": "Recall@K is query-level binary recall: 1 if at least one relevant form appears in the top-K nearest neighbors, else 0; averaged over evaluated queries.",
        "metrics": {
            f"recall_at_{k}": {
                "value": hits[k] / evaluated if evaluated else None,
                "hits": hits[k],
                "n": evaluated,
                "wilson_95_ci": wilson_interval(hits[k], evaluated),
            }
            for k in hits
        },
    }


def main() -> None:
    root = project_root()
    kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext.vec")
    )
    rows = load_jsonl(root / "data" / "benchmarks" / "semantic_search_benchmark.jsonl")
    result = evaluate(kv, rows)
    output_path = root / "docs" / "reproducibility" / "results_semantic_search.json"
    write_json(output_path, result)

    print(f"evaluated_queries: {result['evaluated_queries']}")
    for name, metric in result["metrics"].items():
        print(f"{name}: {metric['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
