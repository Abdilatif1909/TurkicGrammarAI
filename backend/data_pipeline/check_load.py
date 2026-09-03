"""Smoke check for the dynamic raw lexicon loader."""

from __future__ import annotations

from pathlib import Path

from loader import count_by_language, load_raw_lexicon


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_dir = project_root / "data" / "raw"
    records = load_raw_lexicon(raw_dir)
    counts = count_by_language(records)

    for language, count in counts.items():
        print(f"{language}: {count}")
    print(f"total: {len(records)}")


if __name__ == "__main__":
    main()
