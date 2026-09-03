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


def evaluate_embedding_only(
    kv,
    rows: list[dict],
    *,
    cross_language_only: bool = False,
) -> dict:
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
        relevant = {
            item["form"]
            for item in row["relevant"]
            if not cross_language_only or item["lang"] != row["query_lang"]
        }
        for k in hits:
            if has_relevant(neighbors, relevant, k):
                hits[k] += 1
        rr_total += reciprocal_rank(neighbors, relevant)

    return {
        "queries": len(rows),
        "mode": "embedding_only_cross_language" if cross_language_only else "embedding_only",
        "evaluated_queries": evaluated,
        "skipped_queries": skipped,
        "methodology": "Recall@K is query-level binary recall over top-K nearest neighbors. MRR is the mean reciprocal rank of the first relevant item within top 10, or 0 if none appears."
        + (" Same-language relevant entries are excluded." if cross_language_only else ""),
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


def evaluate_oracle(rows: list[dict]) -> dict:
    n = len(rows)
    return {
        "queries": n,
        "mode": "oracle_metadata",
        "evaluated_queries": n,
        "skipped_queries": 0,
        "methodology": "Oracle mode directly accepts the benchmark's metadata-derived relevant set as retrievable. It measures internal metadata pipeline consistency, not model generalization.",
        "metrics": {
            f"recall_at_{k}": {
                "value": 1.0 if n else None,
                "hits": n,
                "n": n,
                "wilson_95_ci": wilson_interval(n, n),
            }
            for k in (1, 5, 10)
        }
        | {"mrr": {"value": 1.0 if n else None, "n": n}},
    }


def main() -> None:
    root = project_root()
    kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext.vec")
    )
    rows = load_jsonl(root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl")
    result = {
        "oracle_metadata": evaluate_oracle(rows),
        "embedding_only": evaluate_embedding_only(kv, rows),
        "embedding_only_cross_language": evaluate_embedding_only(
            kv,
            rows,
            cross_language_only=True,
        ),
    }
    output_path = root / "docs" / "reproducibility" / "results_rag_retrieval.json"
    write_json(output_path, result)

    print(f"oracle_evaluated_queries: {result['oracle_metadata']['evaluated_queries']}")
    print(f"embedding_evaluated_queries: {result['embedding_only']['evaluated_queries']}")
    for name, metric in result["embedding_only"]["metrics"].items():
        print(f"{name}: {metric['value']:.6f}")
    for name, metric in result["embedding_only_cross_language"]["metrics"].items():
        print(f"cross_language_{name}: {metric['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
