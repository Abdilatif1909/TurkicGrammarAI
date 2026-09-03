"""Evaluate template QA benchmark."""

from __future__ import annotations

import sys

from gensim.models import KeyedVectors

from common import load_jsonl, project_root, write_json, wilson_interval

sys.path.append(str(project_root() / "backend" / "qa"))
from simple_qa_engine import EmbeddingQAEngine, SimpleQAEngine  # noqa: E402


def source_matches(row: dict, result: dict) -> bool:
    source_ids = set(result["source_ids"])
    expected_ids = set()
    if row.get("group_id"):
        expected_ids.add(row["group_id"])
    if row.get("lineage_id"):
        expected_ids.add(row["lineage_id"])
    if not expected_ids:
        return bool(result["supporting_entries"])
    return bool(source_ids & expected_ids)


def evaluate_with_engine(rows: list[dict], engine, *, mode: str, methodology: str) -> dict:
    answer_hits = 0
    source_hits = 0
    skipped = 0
    type_counts: dict[str, dict[str, int]] = {}

    for row in rows:
        result = engine.answer(row["question"])
        if result.get("skipped"):
            skipped += 1
            continue
        answer_ok = result["generated_answer"] == row["expected_answer"]
        source_ok = source_matches(row, result)
        answer_hits += int(answer_ok)
        source_hits += int(source_ok)
        answer_type = row["answer_type"]
        if answer_type not in type_counts:
            type_counts[answer_type] = {
                "n": 0,
                "answer_hits": 0,
                "source_hits": 0,
            }
        type_counts[answer_type]["n"] += 1
        type_counts[answer_type]["answer_hits"] += int(answer_ok)
        type_counts[answer_type]["source_hits"] += int(source_ok)

    n = len(rows) - skipped
    by_type = {}
    for answer_type, counts in sorted(type_counts.items()):
        by_type[answer_type] = {
            **counts,
            "answer_accuracy": counts["answer_hits"] / counts["n"],
            "source_accuracy": counts["source_hits"] / counts["n"],
        }

    return {
        "questions": n,
        "mode": mode,
        "benchmark_questions": len(rows),
        "evaluated_questions": n,
        "skipped_questions": skipped,
        "methodology": methodology,
        "answer_accuracy": {
            "value": answer_hits / n if n else None,
            "hits": answer_hits,
            "n": n,
            "wilson_95_ci": wilson_interval(answer_hits, n),
        },
        "source_accuracy": {
            "value": source_hits / n if n else None,
            "hits": source_hits,
            "n": n,
            "wilson_95_ci": wilson_interval(source_hits, n),
        },
        "by_answer_type": by_type,
    }


def evaluate_oracle(rows: list[dict]) -> dict:
    return evaluate_with_engine(
        rows,
        SimpleQAEngine(project_root()),
        mode="oracle_template_lookup",
        methodology="Template lookup mode parses each generated question and directly retrieves the matching lexicon/cognate/lineage source. This is database lookup consistency, not model generalization.",
    )


def evaluate_embedding_only(rows: list[dict], kv) -> dict:
    return evaluate_with_engine(
        rows,
        EmbeddingQAEngine(project_root(), kv, topn=10),
        mode="embedding_only",
        methodology="Embedding QA mode parses the question only to extract the query form, retrieves top-10 vector neighbors, and derives answer languages from retrieved entries. Lemma lookup questions are skipped because embeddings alone cannot produce exact lemmas without direct database lookup.",
    )


def main() -> None:
    root = project_root()
    rows = load_jsonl(root / "data" / "benchmarks" / "qa_benchmark.jsonl")
    kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext.vec")
    )
    result = {
        "oracle_template_lookup": evaluate_oracle(rows),
        "embedding_only": evaluate_embedding_only(rows, kv),
    }
    output_path = root / "docs" / "reproducibility" / "results_qa.json"
    write_json(output_path, result)

    print(f"oracle_evaluated_questions: {result['oracle_template_lookup']['evaluated_questions']}")
    print(f"embedding_evaluated_questions: {result['embedding_only']['evaluated_questions']}")
    print(f"embedding_skipped_questions: {result['embedding_only']['skipped_questions']}")
    print(f"embedding_answer_accuracy: {result['embedding_only']['answer_accuracy']['value']:.6f}")
    print(f"embedding_source_accuracy: {result['embedding_only']['source_accuracy']['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
