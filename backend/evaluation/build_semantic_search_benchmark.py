"""Build cognate-centered semantic search benchmark."""

from __future__ import annotations

from common import load_jsonl, project_root, write_jsonl


def pick_query(members: list[dict]) -> dict:
    modern = [member for member in members if member["language"] != "old_turkic"]
    pool = modern or members
    return sorted(pool, key=lambda item: (item["language"], item["surface_form"]))[0]


def build_rows(groups: list[dict]) -> list[dict]:
    rows = []
    for group in groups:
        members = sorted(
            group["member_entries"],
            key=lambda item: (item["language"], item["surface_form"], item["lemma"]),
        )
        query = pick_query(members)
        relevant = [
            {
                "form": member["surface_form"],
                "lang": member["language"],
                "lemma": member["lemma"],
            }
            for member in members
            if not (
                member["surface_form"] == query["surface_form"]
                and member["language"] == query["language"]
            )
        ]
        if relevant:
            rows.append(
                {
                    "query_form": query["surface_form"],
                    "query_lang": query["language"],
                    "relevant": relevant,
                    "group_id": group["cognate_id"],
                    "source": "cognate",
                }
            )
    return rows


def main() -> None:
    root = project_root()
    groups = load_jsonl(root / "data" / "processed" / "cognate_groups.jsonl")
    output_path = root / "data" / "benchmarks" / "semantic_search_benchmark.jsonl"
    rows = build_rows(groups)
    count = write_jsonl(output_path, rows)

    print(f"semantic_search_queries: {count}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
