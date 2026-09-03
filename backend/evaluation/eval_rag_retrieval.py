"""Evaluate RAG retrieval benchmark with FastText nearest neighbors."""

from __future__ import annotations

from gensim.models import KeyedVectors

from common import load_jsonl, project_root, write_json, wilson_interval
from vector_utils import has_relevant, topn_for_queries


def reciprocal_rank(neighbors: list[str], relevant: set[str]) -> float:
    for index, token in enumerate(neighbors, start=1):
        if token in relevant:
            return 1.0 / index
    return 0.0


def evaluate(kv, rows: list[dict]) -> dict:
    queries = {row["query_form"] for row in rows}
    neighbors_by_query = topn_for_queries(kv, queries, topn=10)
    hits = {1: 0, 5: 0, 10: 0}
    rr_total = 0.0
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
        rr_total += reciprocal_rank(neighbors, relevant)

    return {
        "queries": len(rows),
        "evaluated_queries": evaluated,
        "skipped_queries": skipped,
        "methodology": "Recall@K is query-level binary recall over top-K nearest neighbors. MRR is the mean reciprocal rank of the first relevant item within top 10, or 0 if none appears.",
        "metrics": {
            f"recall_at_{k}": {
                "value": hits[k] / evaluated if evaluated else None,
                "hits": hits[k],
                "n": evaluated,
                "wilson_95_ci": wilson_interval(hits[k], evaluated),
            }
            for k in hits
        }
        | {
            "mrr": {
                "value": rr_total / evaluated if evaluated else None,
                "n": evaluated,
            }
        },
    }


def main() -> None:
    root = project_root()
    kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext.vec")
    )
    rows = load_jsonl(root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl")
    result = evaluate(kv, rows)
    output_path = root / "docs" / "reproducibility" / "results_rag_retrieval.json"
    write_json(output_path, result)

    print(f"evaluated_queries: {result['evaluated_queries']}")
    for name, metric in result["metrics"].items():
        print(f"{name}: {metric['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
