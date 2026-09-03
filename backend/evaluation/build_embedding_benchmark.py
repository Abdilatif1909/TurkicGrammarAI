"""Build embedding-quality positive and negative pair benchmark."""

from __future__ import annotations

from itertools import combinations
import random

from common import entry_key, load_jsonl, project_root, write_jsonl


RANDOM_SEED = 42


def build_positive_pairs(groups: list[dict]) -> list[dict]:
    rows = []
    pair_index = 1
    for group in groups:
        members = sorted(
            group["member_entries"],
            key=lambda item: (item["language"], item["surface_form"], item["lemma"]),
        )
        for left, right in combinations(members, 2):
            if left["language"] == right["language"]:
                continue
            source = "lineage" if group_has_old_turkic(group) else "cognate"
            rows.append(
                {
                    "pair_id": f"EPOS_{pair_index:06d}",
                    "form_a": left["surface_form"],
                    "lang_a": left["language"],
                    "form_b": right["surface_form"],
                    "lang_b": right["language"],
                    "label": "positive",
                    "source": source,
                    "group_id": group["cognate_id"],
                }
            )
            pair_index += 1
    return rows


def group_has_old_turkic(group: dict) -> bool:
    return any(member["language"] == "old_turkic" for member in group["member_entries"])


def build_entry_cognate_map(entries: list[dict]) -> dict[tuple[str, str], set[str]]:
    return {
        entry_key(entry): set(entry.get("cognate_ids", []))
        for entry in entries
    }


def build_negative_pairs(entries: list[dict], target_count: int) -> list[dict]:
    rng = random.Random(RANDOM_SEED)
    candidates = sorted(
        entries,
        key=lambda item: (item["language"], item["surface_form"], item.get("lemma") or ""),
    )
    cognate_map = build_entry_cognate_map(candidates)
    seen: set[tuple[tuple[str, str], tuple[str, str]]] = set()
    rows = []
    attempts = 0
    max_attempts = target_count * 100

    while len(rows) < target_count and attempts < max_attempts:
        attempts += 1
        left, right = rng.sample(candidates, 2)
        if left["language"] == right["language"]:
            continue
        left_key = entry_key(left)
        right_key = entry_key(right)
        ordered = tuple(sorted([left_key, right_key]))
        if ordered in seen:
            continue
        if cognate_map[left_key] & cognate_map[right_key]:
            continue
        seen.add(ordered)
        rows.append(
            {
                "pair_id": f"ENEG_{len(rows) + 1:06d}",
                "form_a": left["surface_form"],
                "lang_a": left["language"],
                "form_b": right["surface_form"],
                "lang_b": right["language"],
                "label": "negative",
                "source": "random",
                "group_id": None,
            }
        )

    if len(rows) < target_count:
        raise RuntimeError(
            f"Could only generate {len(rows)} negative pairs for target {target_count}"
        )
    return rows


def main() -> None:
    root = project_root()
    entries = load_jsonl(root / "data" / "processed" / "lexicon_master_full.jsonl")
    groups = load_jsonl(root / "data" / "processed" / "cognate_groups.jsonl")
    output_path = root / "data" / "benchmarks" / "embedding_quality_benchmark.jsonl"

    positives = build_positive_pairs(groups)
    negatives = build_negative_pairs(entries, len(positives))
    count = write_jsonl(output_path, positives + negatives)

    print(f"positive_pairs: {len(positives)}")
    print(f"negative_pairs: {len(negatives)}")
    print(f"total_pairs: {count}")
    print(f"random_seed: {RANDOM_SEED}")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
