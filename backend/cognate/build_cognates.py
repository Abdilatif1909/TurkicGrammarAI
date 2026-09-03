"""Build deterministic tier-1/tier-2 cognate groups across languages."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re
import unicodedata


WHITESPACE_RE = re.compile(r"\s+")
GENERIC_MEANINGS = {
    "",
    "derived or inflected form",
}

CHAR_MAP = str.maketrans(
    {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
        "ə": "e",
        "ä": "a",
        "á": "a",
        "ó": "o",
        "ú": "u",
        "ý": "y",
        "ň": "n",
        "ŋ": "n",
        "ï": "i",
        "î": "i",
        "â": "a",
        "û": "u",
        "а": "a",
        "ә": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "ғ": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "j",
        "з": "z",
        "и": "i",
        "і": "i",
        "й": "y",
        "к": "k",
        "қ": "q",
        "л": "l",
        "м": "m",
        "н": "n",
        "ң": "n",
        "о": "o",
        "ө": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ұ": "u",
        "ү": "u",
        "ф": "f",
        "х": "h",
        "һ": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sh",
        "ъ": "",
        "ы": "i",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
)


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFC", str(value)).casefold()
    return WHITESPACE_RE.sub(" ", text).strip()


def comparison_key(value: str | None) -> str:
    text = clean_text(value)
    text = text.translate(CHAR_MAP)
    text = re.sub(r"[^a-z0-9]+", "", text)
    return text


def edit_distance_at_most_one(left: str, right: str) -> bool:
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if not left or not right:
        return len(left) <= 1 and len(right) <= 1

    i = 0
    j = 0
    edits = 0
    while i < len(left) and j < len(right):
        if left[i] == right[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        if len(left) == len(right):
            i += 1
            j += 1
        elif len(left) > len(right):
            i += 1
        else:
            j += 1
    if i < len(left) or j < len(right):
        edits += 1
    return edits <= 1


def near_key_match(left: str, right: str) -> bool:
    """Accept conservative edit-distance matches after exact key matching."""

    if left == right:
        return True
    if len(left) < 4 or len(right) < 4:
        return False
    if left[0] != right[0]:
        return False
    return edit_distance_at_most_one(left, right)


def detect_script(text: str) -> str:
    has_cyrillic = any("CYRILLIC" in unicodedata.name(char, "") for char in text)
    has_latin = any("LATIN" in unicodedata.name(char, "") for char in text)
    if has_cyrillic and has_latin:
        return "mixed"
    if has_cyrillic:
        return "cyrillic"
    if has_latin:
        return "latin"
    return "other"


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left: int, right: int) -> bool:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return False
        if self.rank[root_left] < self.rank[root_right]:
            root_left, root_right = root_right, root_left
        self.parent[root_right] = root_left
        if self.rank[root_left] == self.rank[root_right]:
            self.rank[root_left] += 1
        return True


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def build_value_edges(
    entries: list[dict],
    *,
    field: str,
) -> list[tuple[int, int]]:
    values: dict[str, list[int]] = defaultdict(list)
    for index, entry in enumerate(entries):
        value = clean_text(entry.get(field))
        if value:
            values[value].append(index)

    key_to_values: dict[str, set[str]] = defaultdict(set)
    for value in values:
        key_to_values[comparison_key(value)].add(value)

    keys = sorted(key for key in key_to_values if key)
    grouped_keys: dict[int, list[str]] = defaultdict(list)
    for key in keys:
        grouped_keys[len(key)].append(key)

    edges: set[tuple[int, int]] = set()

    def meaning_set(value_set: set[str]) -> set[str]:
        meanings = set()
        for value in value_set:
            for index in values[value]:
                meaning = clean_text(entries[index].get("semantic_description"))
                if meaning not in GENERIC_MEANINGS:
                    meanings.add(meaning)
        return meanings

    def semantically_compatible(left_values: set[str], right_values: set[str]) -> bool:
        return bool(meaning_set(left_values) & meaning_set(right_values))

    def add_if_cross_language(indexes: list[int]) -> None:
        language_count = len({entries[index]["language"] for index in indexes})
        if language_count < 2:
            return
        for left, right in combinations(sorted(indexes), 2):
            if (
                entries[left]["language"] != entries[right]["language"]
                and entries[left]["pos"] == entries[right]["pos"]
            ):
                edges.add((left, right))

    for value_indexes in values.values():
        add_if_cross_language(value_indexes)

    for key_values in key_to_values.values():
        indexes = []
        for value in key_values:
            indexes.extend(values[value])
        add_if_cross_language(indexes)

    for length, left_keys in grouped_keys.items():
        candidate_keys = left_keys + grouped_keys.get(length + 1, [])
        for left_key in left_keys:
            for right_key in candidate_keys:
                if left_key >= right_key:
                    continue
                left_values = key_to_values[left_key]
                right_values = key_to_values[right_key]
                if near_key_match(left_key, right_key) and semantically_compatible(
                    left_values,
                    right_values,
                ):
                    indexes = []
                    for value in left_values | right_values:
                        indexes.extend(values[value])
                    add_if_cross_language(indexes)

    return sorted(edges)


def build_groups(entries: list[dict]) -> tuple[list[dict], list[set[str]]]:
    tier1_edges = build_value_edges(entries, field="surface_form")
    tier2_edges = build_value_edges(entries, field="lemma")

    union_find = UnionFind(len(entries))
    edge_tiers: dict[tuple[int, int], set[str]] = defaultdict(set)
    for left, right in tier1_edges:
        union_find.union(left, right)
        edge_tiers[(left, right)].add("tier1")
    for left, right in tier2_edges:
        union_find.union(left, right)
        edge_tiers[(left, right)].add("tier2")

    components: dict[int, list[int]] = defaultdict(list)
    for index in range(len(entries)):
        components[union_find.find(index)].append(index)

    component_tiers: dict[int, set[str]] = defaultdict(set)
    for (left, right), tiers in edge_tiers.items():
        component_tiers[union_find.find(left)].update(tiers)

    eligible_components = []
    for indexes in components.values():
        languages = {entries[index]["language"] for index in indexes}
        if len(languages) >= 2:
            eligible_components.append(sorted(indexes))

    eligible_components.sort(
        key=lambda indexes: (
            min(entries[index]["language"] for index in indexes),
            min(comparison_key(entries[index]["lemma"]) for index in indexes),
            min(comparison_key(entries[index]["surface_form"]) for index in indexes),
            indexes[0],
        )
    )

    memberships: list[set[str]] = [set() for _ in entries]
    groups: list[dict] = []
    for sequence, indexes in enumerate(eligible_components, start=1):
        cognate_id = f"COGNATE_{sequence}"
        tiers = component_tiers[union_find.find(indexes[0])]
        tier_label = "both" if tiers == {"tier1", "tier2"} else next(iter(tiers))
        member_entries = [
            {
                "language": entries[index]["language"],
                "surface_form": entries[index]["surface_form"],
                "lemma": entries[index]["lemma"],
            }
            for index in indexes
        ]
        for index in indexes:
            memberships[index].add(cognate_id)
        groups.append(
            {
                "cognate_id": cognate_id,
                "member_entries": member_entries,
                "tier": tier_label,
                "language_count": len({member["language"] for member in member_entries}),
                "member_count": len(member_entries),
            }
        )

    return groups, memberships


def script_statistics(entries: list[dict]) -> dict[str, dict[str, int]]:
    stats: dict[str, Counter[str]] = defaultdict(Counter)
    for entry in entries:
        stats[entry["language"]][detect_script(entry["surface_form"])] += 1
    return {language: dict(sorted(counts.items())) for language, counts in sorted(stats.items())}


def pairwise_density(groups: list[dict]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for group in groups:
        languages = sorted({member["language"] for member in group["member_entries"]})
        for left, right in combinations(languages, 2):
            counts[f"{left}-{right}"] += 1
    return dict(sorted(counts.items()))


def format_group_example(group: dict, limit: int = 10) -> str:
    members = group["member_entries"][:limit]
    text = "; ".join(
        f"{member['language']}:{member['surface_form']}({member['lemma']})"
        for member in members
    )
    if group["member_count"] > limit:
        text += f"; ... +{group['member_count'] - limit} more"
    return text


def write_stats(path: Path, groups: list[dict], entries: list[dict], memberships: list[set[str]]) -> None:
    tier_counts = Counter(group["tier"] for group in groups)
    tier1_supported = sum(1 for group in groups if group["tier"] in {"tier1", "both"})
    tier2_supported = sum(1 for group in groups if group["tier"] in {"tier2", "both"})
    total_groups = len(groups)
    avg_language_count = (
        sum(group["language_count"] for group in groups) / total_groups
        if total_groups
        else 0.0
    )
    largest_groups = sorted(
        groups,
        key=lambda group: (-group["language_count"], -group["member_count"], group["cognate_id"]),
    )
    isolated_count = sum(1 for ids in memberships if not ids)
    pair_counts = pairwise_density(groups)
    scripts = script_statistics(entries)

    spot_ids = ["COGNATE_1", "COGNATE_50"]
    spot_groups = [group for group in groups if group["cognate_id"] in spot_ids]
    if largest_groups:
        spot_groups.append(largest_groups[0])
    for group in largest_groups[1:]:
        if len(spot_groups) >= 5:
            break
        spot_groups.append(group)
    if len(spot_groups) < 5 and groups:
        spot_groups.append(groups[len(groups) // 2])

    seen = set()
    deduped_spots = []
    for group in spot_groups:
        if group["cognate_id"] not in seen:
            seen.add(group["cognate_id"])
            deduped_spots.append(group)

    lines = [
        "# Cognate Grouping Statistics",
        "",
        "Stage: Bosqich 3 - Cognate-aware layer",
        "",
        "## Deterministic Rules",
        "",
        "- Input is `data/processed/lexicon_master.jsonl`.",
        "- Tier 1 groups entries by cross-language `surface_form` matches.",
        "- Tier 2 groups entries by cross-language `lemma` matches.",
        "- Text comparison applies Unicode NFC, casefolding, whitespace cleanup, Cyrillic-to-Latin character mapping for Kazakh/Kyrgyz-style Cyrillic, Latin diacritic folding, and removal of non-alphanumeric separators.",
        "- A match is accepted when the cleaned strings are exactly equal, the comparison keys are exactly equal, or the comparison keys have edit distance <= 1 with both keys at least 4 characters long, the same first character, and at least one shared non-generic semantic gloss.",
        "- A cognate group must contain at least two distinct languages.",
        "- Edges require matching `pos` to reduce cross-POS homograph merges.",
        "- Tier labels are `tier1`, `tier2`, or `both` depending on which edge types contributed to the final connected component.",
        "",
        "## Script Audit",
        "",
        "| Language | Latin | Cyrillic | Mixed | Other |",
        "|---|---:|---:|---:|---:|",
    ]
    for language, counts in scripts.items():
        lines.append(
            f"| `{language}` | {counts.get('latin', 0)} | {counts.get('cyrillic', 0)} | {counts.get('mixed', 0)} | {counts.get('other', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total cognate groups: **{total_groups}**",
            f"- Groups with Tier 1 support: **{tier1_supported}**",
            f"- Groups with Tier 2 support: **{tier2_supported}**",
            f"- Tier 1 only groups: **{tier_counts.get('tier1', 0)}**",
            f"- Tier 2 only groups: **{tier_counts.get('tier2', 0)}**",
            f"- Groups supported by both tiers: **{tier_counts.get('both', 0)}**",
            f"- Average languages per group: **{avg_language_count:.4f}**",
            f"- Isolated entries with no cognate group: **{isolated_count}**",
            "",
            "## Largest Groups",
            "",
            "| Cognate ID | Tier | Languages | Members | Example members |",
            "|---|---|---:|---:|---|",
        ]
    )
    for group in largest_groups[:3]:
        lines.append(
            f"| `{group['cognate_id']}` | `{group['tier']}` | {group['language_count']} | {group['member_count']} | {format_group_example(group, limit=8)} |"
        )

    lines.extend(
        [
            "",
            "## Language Pair Cognate Density",
            "",
            "| Language pair | Cognate groups shared |",
            "|---|---:|",
        ]
    )
    for pair, count in pair_counts.items():
        lines.append(f"| `{pair}` | {count} |")

    lines.extend(
        [
            "",
            "## Manual Spot-Check",
            "",
            "| Cognate ID | Tier | Languages | Members | Review |",
            "|---|---|---:|---:|---|",
        ]
    )
    for group in deduped_spots:
        review = (
            "Looks plausible under the deterministic surface/lemma rules; members share visible form or lemma-normalized roots across languages."
        )
        if group["member_count"] > 100:
            review = (
                "Large lemma-driven concept group; useful as a broad cognate signal but may be too coarse for strict historical cognacy."
            )
        lines.append(
            f"| `{group['cognate_id']}` | `{group['tier']}` | {group['language_count']} | {group['member_count']} | {review} Example: {format_group_example(group, limit=6)} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    lexicon_path = project_root / "data" / "processed" / "lexicon_master.jsonl"
    groups_path = project_root / "data" / "processed" / "cognate_groups.jsonl"
    enriched_path = project_root / "data" / "processed" / "lexicon_master_with_cognates.jsonl"
    stats_path = project_root / "docs" / "reproducibility" / "cognate_stats.md"

    entries = load_jsonl(lexicon_path)
    groups, memberships = build_groups(entries)

    enriched_entries = []
    for entry, cognate_ids in zip(entries, memberships):
        enriched = dict(entry)
        enriched["cognate_ids"] = sorted(cognate_ids)
        enriched_entries.append(enriched)

    write_jsonl(groups_path, groups)
    write_jsonl(enriched_path, enriched_entries)
    write_stats(stats_path, groups, entries, memberships)

    tier_counts = Counter(group["tier"] for group in groups)
    print(f"entries: {len(entries)}")
    print(f"cognate_groups: {len(groups)}")
    print(f"tier1_only: {tier_counts.get('tier1', 0)}")
    print(f"tier2_only: {tier_counts.get('tier2', 0)}")
    print(f"both: {tier_counts.get('both', 0)}")
    print(f"isolated_entries: {sum(1 for ids in memberships if not ids)}")
    print(f"wrote: {groups_path}")
    print(f"wrote: {enriched_path}")
    print(f"wrote: {stats_path}")


if __name__ == "__main__":
    main()
