"""Build retrieval benchmark that combines cognate, lineage, and morphology signals."""

from __future__ import annotations

from collections import defaultdict

from common import compact_entry, load_jsonl, project_root, write_jsonl


def index_entries(entries: list[dict]) -> dict[tuple[str, str], dict]:
    return {
        (entry["language"], entry["surface_form"]): entry
        for entry in entries
    }


def build_lemma_index(entries: list[dict]) -> dict[tuple[str, str], list[dict]]:
    index: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for entry in entries:
        lemma = entry.get("lemma")
        if lemma:
            index[(entry["language"], lemma)].append(entry)
    return index


def pick_query(link: dict) -> dict:
    descendants = sorted(
        link["descendant_entries"],
        key=lambda item: (item["language"], item["surface_form"], item["lemma"]),
    )
    return descendants[0]


def unique_entries(entries: list[dict]) -> list[dict]:
    seen = set()
    rows = []
    for entry in entries:
        key = (entry["lang"], entry["form"])
        if key not in seen:
            seen.add(key)
            rows.append(entry)
    return rows


def build_rows(entries: list[dict], lineage_links: list[dict]) -> list[dict]:
    entry_index = index_entries(entries)
    lemma_index = build_lemma_index(entries)
    rows = []

    for link in lineage_links:
        query_member = pick_query(link)
        query_entry = entry_index[(query_member["language"], query_member["surface_form"])]

        relevant = []
        for member in link["old_turkic_entries"] + link["descendant_entries"]:
            if (
                member["language"] == query_member["language"]
                and member["surface_form"] == query_member["surface_form"]
            ):
                continue
            entry = entry_index.get((member["language"], member["surface_form"]))
            if entry:
                relevant.append(compact_entry(entry) | {"signal": "lineage"})

        for entry in lemma_index.get((query_entry["language"], query_entry.get("lemma")), []):
            if entry["surface_form"] == query_entry["surface_form"]:
                continue
            relevant.append(compact_entry(entry) | {"signal": "morphology"})

        relevant = unique_entries(relevant)
        if relevant:
            rows.append(
                {
                    "query_form": query_entry["surface_form"],
                    "query_lang": query_entry["language"],
                    "query_lemma": query_entry.get("lemma"),
                    "group_id": link["source_cognate_id"],
                    "lineage_id": link["lineage_id"],
                    "anchor_type": link["anchor_type"],
                    "relevant": relevant,
                    "source": "lineage+cognate+morphology",
                }
            )

    return rows


def main() -> None:
    root = project_root()
    entries = load_jsonl(root / "data" / "processed" / "lexicon_master_full.jsonl")
    lineage_links = load_jsonl(root / "data" / "processed" / "lineage_links.jsonl")
    output_path = root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl"
    rows = build_rows(entries, lineage_links)
    count = write_jsonl(output_path, rows)

    print(f"rag_retrieval_queries: {count}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
