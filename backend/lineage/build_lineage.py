"""Build Old Turkic-attested historical lineage links."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path


OLD_TURKIC = "old_turkic"


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def old_turkic_members(group: dict) -> list[dict]:
    return [
        member
        for member in group["member_entries"]
        if member["language"] == OLD_TURKIC
    ]


def descendant_members(group: dict) -> list[dict]:
    return [
        member
        for member in group["member_entries"]
        if member["language"] != OLD_TURKIC
    ]


def pick_old_turkic_anchor(members: list[dict]) -> dict:
    base_like = [
        member
        for member in members
        if member["surface_form"] == member["lemma"]
    ]
    candidates = base_like or members
    return sorted(
        candidates,
        key=lambda member: (len(member["surface_form"]), member["surface_form"]),
    )[0]


def build_lineage_links(groups: list[dict]) -> tuple[list[dict], list[dict]]:
    anchored_groups = []
    no_anchor_groups = []

    for group in groups:
        old_members = old_turkic_members(group)
        descendants = descendant_members(group)
        if old_members and descendants:
            anchored_groups.append((group, old_members, descendants))
        elif not old_members and group["language_count"] >= 3:
            no_anchor_groups.append(group)

    anchored_groups.sort(key=lambda item: item[0]["cognate_id"])

    lineage_links = []
    for sequence, (group, old_members, descendants) in enumerate(
        anchored_groups,
        start=1,
    ):
        lineage_id = f"LINEAGE_{sequence}"
        anchor = pick_old_turkic_anchor(old_members)
        lineage_links.append(
            {
                "lineage_id": lineage_id,
                "source_cognate_id": group["cognate_id"],
                "old_turkic_form": anchor["surface_form"],
                "old_turkic_lemma": anchor["lemma"],
                "old_turkic_entries": sorted(
                    old_members,
                    key=lambda member: (member["lemma"], member["surface_form"]),
                ),
                "descendant_entries": sorted(
                    descendants,
                    key=lambda member: (
                        member["language"],
                        member["lemma"],
                        member["surface_form"],
                    ),
                ),
                "anchor_type": "old_turkic_attested",
                "lineage_form_tokens": {
                    language: f"LINEAGE_FORM_{sequence}_{language}"
                    for language in sorted(
                        {member["language"] for member in group["member_entries"]}
                    )
                },
            }
        )

    return lineage_links, no_anchor_groups


def enrich_entries(entries: list[dict], lineage_links: list[dict]) -> list[dict]:
    cognate_to_lineage = {
        link["source_cognate_id"]: link for link in lineage_links
    }
    enriched = []

    for entry in entries:
        row = dict(entry)
        matched_links = [
            cognate_to_lineage[cognate_id]
            for cognate_id in row.get("cognate_ids", [])
            if cognate_id in cognate_to_lineage
        ]
        if matched_links:
            lineage_ids = [link["lineage_id"] for link in matched_links]
            row["lineage_ids"] = lineage_ids
            metadata = []
            for link in matched_links:
                token = link["lineage_form_tokens"].get(row["language"])
                role = "ancestor" if row["language"] == OLD_TURKIC else "descendant"
                metadata.append(
                    {
                        "lineage_id": link["lineage_id"],
                        "source_cognate_id": link["source_cognate_id"],
                        "anchor_type": link["anchor_type"],
                        "old_turkic_form": link["old_turkic_form"],
                        "old_turkic_lemma": link["old_turkic_lemma"],
                        "role": role,
                        "lineage_form_token": token,
                        "proto_turkic_reconstruction": False,
                    }
                )
            row["historical_lineage_metadata"] = metadata
        else:
            row["lineage_ids"] = []
            if row.get("historical_lineage_metadata") is None:
                row["historical_lineage_metadata"] = None
        enriched.append(row)

    return enriched


def lineage_participation_stats(lineage_links: list[dict]) -> dict:
    old_lemma_to_languages: dict[str, set[str]] = defaultdict(set)
    for link in lineage_links:
        for descendant in link["descendant_entries"]:
            old_lemma_to_languages[link["old_turkic_lemma"]].add(
                descendant["language"]
            )

    rows = [
        {
            "old_turkic_lemma": lemma,
            "descendant_language_count": len(languages),
            "descendant_languages": sorted(languages),
        }
        for lemma, languages in old_lemma_to_languages.items()
    ]
    rows.sort(
        key=lambda row: (
            -row["descendant_language_count"],
            row["old_turkic_lemma"],
        )
    )

    return {
        "unique_old_turkic_lemmas": len(rows),
        "max_descendant_examples": rows[:5],
        "min_descendant_examples": sorted(
            rows,
            key=lambda row: (
                row["descendant_language_count"],
                row["old_turkic_lemma"],
            ),
        )[:5],
    }


def pairwise_density(lineage_links: list[dict]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for link in lineage_links:
        languages = sorted(
            {entry["language"] for entry in link["descendant_entries"]}
            | {OLD_TURKIC}
        )
        for left, right in combinations(languages, 2):
            counts[f"{left}-{right}"] += 1
    return dict(sorted(counts.items()))


def format_members(members: list[dict], limit: int = 6) -> str:
    sample = members[:limit]
    text = "; ".join(
        f"{member['language']}:{member['surface_form']}({member['lemma']})"
        for member in sample
    )
    if len(members) > limit:
        text += f"; ... +{len(members) - limit} more"
    return text


def write_stats(
    path: Path,
    *,
    groups: list[dict],
    lineage_links: list[dict],
    no_anchor_groups: list[dict],
    enriched_entries: list[dict],
) -> None:
    lineage_entry_count = sum(1 for entry in enriched_entries if entry["lineage_ids"])
    old_turkic_cognate_groups = {
        link["source_cognate_id"] for link in lineage_links
    }
    no_anchor_ids = [group["cognate_id"] for group in no_anchor_groups]
    lemma_stats = lineage_participation_stats(lineage_links)
    density = pairwise_density(lineage_links)
    largest = sorted(
        lineage_links,
        key=lambda link: (
            -len(
                {member["language"] for member in link["descendant_entries"]}
            ),
            -len(link["descendant_entries"]),
            link["lineage_id"],
        ),
    )
    spot_links = []
    for link in largest[:3]:
        spot_links.append(link)
    for target in ("LINEAGE_1", "LINEAGE_10"):
        match = next(
            (link for link in lineage_links if link["lineage_id"] == target),
            None,
        )
        if match:
            spot_links.append(match)
    deduped_spots = []
    seen = set()
    for link in spot_links:
        if link["lineage_id"] not in seen:
            seen.add(link["lineage_id"])
            deduped_spots.append(link)

    lines = [
        "# Historical Lineage Statistics",
        "",
        "Stage: Bosqich 4 - Historical lineage encoding",
        "",
        "## Scope And Claim Boundary",
        "",
        "Lineage here means an **attested Old Turkic -> modern language** continuity signal derived from cognate groups that contain `old_turkic` members.",
        "",
        "This is **not** a Proto-Turkic reconstruction. The current dataset does not include reconstructed Proto-Turkic forms or reconstruction metadata. Any paper wording that claims `Proto-Turkic reconstructions` should be softened or removed unless a separate reconstruction source is added.",
        "",
        "## Summary",
        "",
        f"- Total cognate groups inspected: **{len(groups)}**",
        f"- Cognate groups with Old Turkic member and modern descendants: **{len(old_turkic_cognate_groups)}**",
        f"- Lineage groups emitted: **{len(lineage_links)}**",
        f"- Modern 3+ language groups with no historical anchor: **{len(no_anchor_groups)}**",
        f"- Entries participating in lineage groups: **{lineage_entry_count}**",
        f"- Isolated or non-lineage entries: **{len(enriched_entries) - lineage_entry_count}**",
        f"- Unique Old Turkic anchor lemmas: **{lemma_stats['unique_old_turkic_lemmas']}**",
        "",
        "## No Historical Anchor Groups",
        "",
        f"Count: **{len(no_anchor_groups)}**",
        "",
        "Example IDs: "
        + (", ".join(f"`{item}`" for item in no_anchor_ids[:20]) if no_anchor_ids else "none"),
        "",
        "## Old Turkic Lemma Descendant Coverage",
        "",
        "### Most Connected",
        "",
        "| Old Turkic lemma | Modern language count | Modern languages |",
        "|---|---:|---|",
    ]
    for row in lemma_stats["max_descendant_examples"]:
        lines.append(
            f"| `{row['old_turkic_lemma']}` | {row['descendant_language_count']} | {', '.join(row['descendant_languages'])} |"
        )

    lines.extend(
        [
            "",
            "### Least Connected",
            "",
            "| Old Turkic lemma | Modern language count | Modern languages |",
            "|---|---:|---|",
        ]
    )
    for row in lemma_stats["min_descendant_examples"]:
        lines.append(
            f"| `{row['old_turkic_lemma']}` | {row['descendant_language_count']} | {', '.join(row['descendant_languages'])} |"
        )

    lines.extend(
        [
            "",
            "## Lineage Pair Density",
            "",
            "| Language pair | Lineage groups shared |",
            "|---|---:|",
        ]
    )
    for pair, count in density.items():
        lines.append(f"| `{pair}` | {count} |")

    lines.extend(
        [
            "",
            "## Manual Spot-Check",
            "",
            "| Lineage ID | Source cognate | Old Turkic anchor | Descendant sample | Review |",
            "|---|---|---|---|---|",
        ]
    )
    for link in deduped_spots[:5]:
        review = (
            "Plausible Old Turkic-attested lineage signal under the deterministic cognate rules; this should be stated as attested continuity, not Proto-Turkic reconstruction."
        )
        lines.append(
            f"| `{link['lineage_id']}` | `{link['source_cognate_id']}` | `{link['old_turkic_form']}` / `{link['old_turkic_lemma']}` | {format_members(link['descendant_entries'], limit=8)} | {review} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    lexicon_path = (
        project_root / "data" / "processed" / "lexicon_master_with_cognates.jsonl"
    )
    groups_path = project_root / "data" / "processed" / "cognate_groups.jsonl"
    lineage_path = project_root / "data" / "processed" / "lineage_links.jsonl"
    full_lexicon_path = (
        project_root / "data" / "processed" / "lexicon_master_full.jsonl"
    )
    stats_path = project_root / "docs" / "reproducibility" / "lineage_stats.md"

    entries = load_jsonl(lexicon_path)
    groups = load_jsonl(groups_path)
    lineage_links, no_anchor_groups = build_lineage_links(groups)
    enriched_entries = enrich_entries(entries, lineage_links)

    write_jsonl(lineage_path, lineage_links)
    write_jsonl(full_lexicon_path, enriched_entries)
    write_stats(
        stats_path,
        groups=groups,
        lineage_links=lineage_links,
        no_anchor_groups=no_anchor_groups,
        enriched_entries=enriched_entries,
    )

    print(f"cognate_groups: {len(groups)}")
    print(f"old_turkic_anchored_lineage_groups: {len(lineage_links)}")
    print(f"modern_3plus_no_historical_anchor_groups: {len(no_anchor_groups)}")
    print(
        "lineage_participating_entries: "
        f"{sum(1 for entry in enriched_entries if entry['lineage_ids'])}"
    )
    print(f"wrote: {lineage_path}")
    print(f"wrote: {full_lexicon_path}")
    print(f"wrote: {stats_path}")


if __name__ == "__main__":
    main()
