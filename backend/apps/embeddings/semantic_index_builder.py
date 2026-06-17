import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List


DATASET_PATH = Path("backend/data/embeddings/embedding_dataset.jsonl")
INDEX_PATH = Path("backend/data/embeddings/semantic_index.json")


def compact_record(record: Dict, record_id: int) -> Dict:
    return {
        "id": record_id,
        "word": record.get("surface_form") or "",
        "lemma": record.get("lemma") or record.get("surface_form") or "",
        "root": record.get("root") or record.get("lemma") or record.get("surface_form") or "",
        "language": record.get("language") or "",
        "features": record.get("features") or [],
        "cognate_group": record.get("cognate_group") or "",
        "historical_lineage": record.get("historical_lineage") or [],
        "source": record.get("source") or "",
    }


def build_semantic_index(dataset_path: str | Path = DATASET_PATH, output_path: str | Path = INDEX_PATH) -> Dict:
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    seen = set()
    maps = {
        "by_word": defaultdict(list),
        "by_lemma": defaultdict(list),
        "by_root": defaultdict(list),
        "by_cognate": defaultdict(list),
        "by_feature": defaultdict(list),
        "by_lineage_form": defaultdict(list),
    }
    languages = Counter()
    sources = Counter()

    with dataset_path.open(encoding="utf-8") as fh:
        for line in fh:
            raw = json.loads(line)
            key = (raw.get("surface_form"), raw.get("language"), raw.get("source"))
            if key in seen:
                continue
            seen.add(key)
            record = compact_record(raw, len(records))
            records.append(record)
            rid = record["id"]
            maps["by_word"][record["word"]].append(rid)
            maps["by_lemma"][record["lemma"]].append(rid)
            maps["by_root"][f"{record['language']}:{record['root']}"].append(rid)
            if record["cognate_group"]:
                maps["by_cognate"][record["cognate_group"]].append(rid)
            for feature in record["features"]:
                maps["by_feature"][feature].append(rid)
            for item in record["historical_lineage"]:
                form = item.get("form")
                if form:
                    maps["by_lineage_form"][form].append(rid)
            languages[record["language"]] += 1
            sources[record["source"]] += 1

    serializable_maps = {name: dict(value) for name, value in maps.items()}
    index = {
        "version": "1.0",
        "dataset_path": str(dataset_path),
        "records": records,
        "maps": serializable_maps,
        "statistics": {
            "record_count": len(records),
            "languages": dict(sorted(languages.items())),
            "sources": dict(sources.most_common()),
            "cognate_groups": len(maps["by_cognate"]),
            "lineage_forms": len(maps["by_lineage_form"]),
        },
    }
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(index, fh, ensure_ascii=False)
    return {"output_path": str(output_path), **index["statistics"]}


if __name__ == "__main__":
    print(json.dumps(build_semantic_index(), ensure_ascii=False, indent=2))
