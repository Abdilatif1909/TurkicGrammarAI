"""Write benchmark generation rules and measured sizes."""

from __future__ import annotations

import json
from pathlib import Path

from common import load_jsonl, project_root


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def sample_jsonl(path: Path, limit: int = 3) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
            if len(rows) >= limit:
                break
    return rows


def write_doc(path: Path) -> None:
    root = project_root()
    embedding_path = root / "data" / "benchmarks" / "embedding_quality_benchmark.jsonl"
    semantic_path = root / "data" / "benchmarks" / "semantic_search_benchmark.jsonl"
    rag_path = root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl"
    qa_path = root / "data" / "benchmarks" / "qa_benchmark.jsonl"

    embedding_rows = load_jsonl(embedding_path)
    positive_count = sum(1 for row in embedding_rows if row["label"] == "positive")
    negative_count = sum(1 for row in embedding_rows if row["label"] == "negative")
    qa_rows = load_jsonl(qa_path)
    qa_type_counts: dict[str, int] = {}
    for row in qa_rows:
        answer_type = row["answer_type"]
        qa_type_counts[answer_type] = qa_type_counts.get(answer_type, 0) + 1

    content = [
        "# Benchmark Generation Rules",
        "",
        "Stage: Bosqich 6 - Benchmark generation",
        "",
        "All benchmarks are generated from existing project artifacts. No target counts from the paper are copied. Sizes below are measured from the generated files.",
        "",
        "## Embedding Quality Benchmark",
        "",
        "- Input: `cognate_groups.jsonl` and `lexicon_master_full.jsonl`.",
        "- Positive pairs: every cross-language member pair inside each cognate group.",
        "- Positive `source` is `lineage` when the cognate group contains an `old_turkic` member, otherwise `cognate`.",
        "- Negative pairs: random cross-language pairs that do not share any `cognate_id`.",
        "- Random seed: `42`.",
        f"- Positive pairs: **{positive_count}**.",
        f"- Negative pairs: **{negative_count}**.",
        f"- Total rows: **{line_count(embedding_path)}**.",
        "",
        "## Semantic Search Benchmark",
        "",
        "- Input: `cognate_groups.jsonl`.",
        "- One query member is selected per cognate group using deterministic sort order, preferring modern languages over `old_turkic`.",
        "- Relevant results are the other members of the same cognate group.",
        "- Purpose: test whether a surface form retrieves cross-language cognate neighbors.",
        f"- Total queries: **{line_count(semantic_path)}**.",
        "",
        "## RAG Retrieval Benchmark",
        "",
        "- Input: `lineage_links.jsonl` and `lexicon_master_full.jsonl`.",
        "- One query is selected per Old Turkic-attested lineage group.",
        "- Relevant results include lineage-linked descendants/Old Turkic anchors plus same-language morphological variants sharing the query lemma.",
        "- Difference from semantic search: semantic search uses only cognate group membership, while RAG retrieval combines lineage, cognate, and morphology signals.",
        f"- Total queries: **{line_count(rag_path)}**.",
        "",
        "## QA Benchmark",
        "",
        "- Input: `cognate_groups.jsonl`, `lineage_links.jsonl`, and `lexicon_master_full.jsonl`.",
        "- Questions are template-based, not LLM-generated.",
        "- Templates cover shared cognate languages, lemma lookup, and Old Turkic-attested descendant languages.",
        f"- Total questions: **{line_count(qa_path)}**.",
    ]
    for answer_type, count in sorted(qa_type_counts.items()):
        content.append(f"- `{answer_type}` questions: **{count}**.")

    content.extend(
        [
            "",
            "## Samples",
            "",
            "### Embedding",
            "",
            "```json",
            json.dumps(sample_jsonl(embedding_path, 3), ensure_ascii=False, indent=2),
            "```",
            "",
            "### Semantic Search",
            "",
            "```json",
            json.dumps(sample_jsonl(semantic_path, 3), ensure_ascii=False, indent=2),
            "```",
            "",
            "### RAG Retrieval",
            "",
            "```json",
            json.dumps(sample_jsonl(rag_path, 3), ensure_ascii=False, indent=2),
            "```",
            "",
            "### QA",
            "",
            "```json",
            json.dumps(sample_jsonl(qa_path, 3), ensure_ascii=False, indent=2),
            "```",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def main() -> None:
    root = project_root()
    output_path = root / "docs" / "reproducibility" / "benchmark_generation_rules.md"
    write_doc(output_path)
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
