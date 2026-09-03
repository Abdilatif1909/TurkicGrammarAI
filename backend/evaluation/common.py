"""Shared helpers for benchmark generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
            count += 1
    return count


def entry_key(entry: dict) -> tuple[str, str]:
    return entry["language"], entry["surface_form"]


def compact_entry(entry: dict) -> dict:
    return {
        "form": entry["surface_form"],
        "lang": entry["language"],
        "lemma": entry.get("lemma"),
    }


def group_members_by_key(groups: list[dict]) -> dict[str, list[dict]]:
    return {
        group["cognate_id"]: group["member_entries"]
        for group in groups
    }
