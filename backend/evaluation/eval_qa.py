"""Evaluate template QA benchmark."""

from __future__ import annotations

import sys

from common import load_jsonl, project_root, write_json, wilson_interval

sys.path.append(str(project_root() / "backend" / "qa"))
from simple_qa_engine import SimpleQAEngine  # noqa: E402


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


def evaluate(rows: list[dict]) -> dict:
    engine = SimpleQAEngine(project_root())
    answer_hits = 0
    source_hits = 0
    type_counts: dict[str, dict[str, int]] = {}

    for row in rows:
        result = engine.answer(row["question"])
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

    n = len(rows)
    by_type = {}
    for answer_type, counts in sorted(type_counts.items()):
        by_type[answer_type] = {
            **counts,
            "answer_accuracy": counts["answer_hits"] / counts["n"],
            "source_accuracy": counts["source_hits"] / counts["n"],
        }

    return {
        "questions": n,
        "evaluated_questions": n,
        "methodology": "Template QA engine parses each generated question, retrieves the matching lexicon/cognate/lineage source, and compares generated_answer with expected_answer exactly.",
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


def main() -> None:
    root = project_root()
    rows = load_jsonl(root / "data" / "benchmarks" / "qa_benchmark.jsonl")
    result = evaluate(rows)
    output_path = root / "docs" / "reproducibility" / "results_qa.json"
    write_json(output_path, result)

    print(f"evaluated_questions: {result['evaluated_questions']}")
    print(f"answer_accuracy: {result['answer_accuracy']['value']:.6f}")
    print(f"source_accuracy: {result['source_accuracy']['value']:.6f}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
