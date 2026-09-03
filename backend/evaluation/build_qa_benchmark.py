"""Build deterministic template-based QA benchmark."""

from __future__ import annotations

from common import compact_entry, load_jsonl, project_root, write_jsonl


def pick_group_query(group: dict) -> dict:
    return sorted(
        group["member_entries"],
        key=lambda item: (item["language"], item["surface_form"], item["lemma"]),
    )[0]


def build_cognate_questions(groups: list[dict]) -> list[dict]:
    rows = []
    for group in groups:
        query = pick_group_query(group)
        languages = sorted(
            {
                member["language"]
                for member in group["member_entries"]
                if member["language"] != query["language"]
            }
        )
        if not languages:
            continue
        rows.append(
            {
                "question": (
                    "Which language(s) share a cognate with "
                    f"'{query['surface_form']}' ({query['language']})?"
                ),
                "expected_answer": ", ".join(languages),
                "answer_type": "shared_cognate_languages",
                "supporting_entries": [
                    {
                        "form": member["surface_form"],
                        "lang": member["language"],
                        "lemma": member["lemma"],
                    }
                    for member in group["member_entries"]
                ],
                "group_id": group["cognate_id"],
            }
        )
    return rows


def build_lemma_questions(entries: list[dict]) -> list[dict]:
    rows = []
    seen_languages = set()
    for entry in sorted(entries, key=lambda item: (item["language"], item["surface_form"])):
        language = entry["language"]
        if language in seen_languages:
            continue
        seen_languages.add(language)
        rows.append(
            {
                "question": (
                    f"What is the lemma of '{entry['surface_form']}' in {language}?"
                ),
                "expected_answer": entry.get("lemma"),
                "answer_type": "lemma_lookup",
                "supporting_entries": [compact_entry(entry)],
                "group_id": entry.get("cognate_ids", [None])[0]
                if entry.get("cognate_ids")
                else None,
            }
        )
    return rows


def build_lineage_questions(lineage_links: list[dict]) -> list[dict]:
    rows = []
    for link in lineage_links:
        descendants = sorted(
            {member["language"] for member in link["descendant_entries"]}
        )
        rows.append(
            {
                "question": (
                    "Which modern language(s) have descendants linked to Old Turkic "
                    f"'{link['old_turkic_form']}'?"
                ),
                "expected_answer": ", ".join(descendants),
                "answer_type": "lineage_descendant_languages",
                "supporting_entries": [
                    {
                        "form": member["surface_form"],
                        "lang": member["language"],
                        "lemma": member["lemma"],
                    }
                    for member in link["old_turkic_entries"] + link["descendant_entries"]
                ],
                "group_id": link["source_cognate_id"],
                "lineage_id": link["lineage_id"],
            }
        )
    return rows


def main() -> None:
    root = project_root()
    entries = load_jsonl(root / "data" / "processed" / "lexicon_master_full.jsonl")
    groups = load_jsonl(root / "data" / "processed" / "cognate_groups.jsonl")
    lineage_links = load_jsonl(root / "data" / "processed" / "lineage_links.jsonl")
    output_path = root / "data" / "benchmarks" / "qa_benchmark.jsonl"

    rows = (
        build_cognate_questions(groups)
        + build_lemma_questions(entries)
        + build_lineage_questions(lineage_links)
    )
    count = write_jsonl(output_path, rows)

    print(f"qa_questions: {count}")
    print(f"cognate_questions: {len(build_cognate_questions(groups))}")
    print(f"lemma_questions: {len(build_lemma_questions(entries))}")
    print(f"lineage_questions: {len(build_lineage_questions(lineage_links))}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
