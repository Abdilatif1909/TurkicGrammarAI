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


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def wilson_interval(successes: float, n: int, z: float = 1.959963984540054) -> dict:
    if n <= 0:
        return {"low": None, "high": None}
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half_width = (
        z
        * ((p * (1 - p) + z * z / (4 * n)) / n) ** 0.5
        / denominator
    )
    return {"low": center - half_width, "high": center + half_width}
