import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict


DEFAULT_DATASET = Path("backend/data/embeddings/embedding_dataset.jsonl")
DEFAULT_STATS = Path("backend/data/reports/embedding_dataset_validation.json")
REQUIRED_FIELDS = {
    "surface_form",
    "lemma",
    "root",
    "language",
    "features",
    "cognate_group",
    "historical_lineage",
    "source",
}


def validate_embedding_dataset(path: str | Path = DEFAULT_DATASET, min_records: int = 100_000) -> Dict:
    path = Path(path)
    total = 0
    missing = Counter()
    languages = Counter()
    features = Counter()
    sources = Counter()
    seen = set()
    duplicates = 0
    malformed = 0

    with path.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            total += 1
            for field in REQUIRED_FIELDS:
                if field not in record or record.get(field) in (None, ""):
                    if field not in {"cognate_group", "historical_lineage"}:
                        missing[field] += 1
            key = (record.get("language"), record.get("surface_form"), record.get("lemma"), record.get("root"), record.get("source"))
            if key in seen:
                duplicates += 1
            seen.add(key)
            languages[record.get("language") or ""] += 1
            sources[record.get("source") or ""] += 1
            for feature in record.get("features") or []:
                features[feature] += 1

    duplicate_rate = round(duplicates / total * 100, 4) if total else 0.0
    stats = {
        "total_records": total,
        "min_records": min_records,
        "passes": (
            total >= min_records
            and malformed == 0
            and missing.get("lemma", 0) == 0
            and missing.get("root", 0) == 0
            and missing.get("language", 0) == 0
            and duplicate_rate <= 5.0
        ),
        "missing": dict(missing),
        "malformed_records": malformed,
        "duplicate_records": duplicates,
        "duplicate_rate": duplicate_rate,
        "records_per_language": dict(sorted(languages.items())),
        "records_per_feature": dict(sorted(features.items())),
        "records_per_source": dict(sources.most_common()),
    }
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate expanded embedding dataset JSONL")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--stats", default=str(DEFAULT_STATS))
    parser.add_argument("--min-records", type=int, default=100_000)
    args = parser.parse_args()
    stats = validate_embedding_dataset(args.dataset, args.min_records)
    stats_path = Path(args.stats)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if not stats["passes"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
