"""Build the normalized master lexicon and dataset manifest."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .loader import load_raw_lexicon
    from .normalize import build_dataset_manifest, normalize_lexicon
except ImportError:  # pragma: no cover - supports direct script execution
    from loader import load_raw_lexicon
    from normalize import build_dataset_manifest, normalize_lexicon


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    raw_dir = project_root / "data" / "raw"
    lexicon_path = project_root / "data" / "processed" / "lexicon_master.jsonl"
    manifest_path = (
        project_root / "docs" / "reproducibility" / "dataset_manifest.json"
    )

    raw_records = load_raw_lexicon(raw_dir)
    entries = normalize_lexicon(raw_records)
    manifest = build_dataset_manifest(entries)

    write_jsonl(lexicon_path, [entry.to_dict() for entry in entries])
    write_json(manifest_path, manifest)

    print(f"raw_records: {len(raw_records)}")
    print(f"normalized_records: {len(entries)}")
    print("records_by_language:")
    for language, stats in manifest["languages"].items():
        print(f"  {language}: {stats['records']}")
    print("unique_counts:")
    print(f"  surface_forms: {manifest['totals']['unique_surface_forms']}")
    print(
        "  lemmas_with_fallback: "
        f"{manifest['totals']['unique_lemmas_with_fallback']}"
    )
    print(
        "  roots_with_fallback: "
        f"{manifest['totals']['unique_roots_with_fallback']}"
    )
    print("inferred:")
    print(f"  lemma_inferred: {manifest['totals']['lemma_inferred_records']}")
    print(f"  root_inferred: {manifest['totals']['root_inferred_records']}")
    print("cross_language_surface_forms:")
    cross_stats = manifest["cross_language_surface_form_statistics"]
    print(
        "  2_plus_languages: "
        f"{cross_stats['surface_forms_in_2_plus_languages']}"
    )
    print(
        "  3_plus_languages: "
        f"{cross_stats['surface_forms_in_3_plus_languages']}"
    )
    print(
        "language_surface_duplicate_pairs: "
        f"{manifest['totals']['language_surface_duplicate_pairs']}"
    )
    print(f"wrote: {lexicon_path}")
    print(f"wrote: {manifest_path}")


if __name__ == "__main__":
    main()
