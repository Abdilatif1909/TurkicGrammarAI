import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Set

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from apps.embeddings.fasttext_service import load_fasttext_model


INDEX_PATH = PROJECT_ROOT / "backend/data/embeddings/semantic_index.json"


@lru_cache(maxsize=1)
def load_semantic_index(path: str = str(INDEX_PATH)) -> Dict:
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)


def record_lineage_forms(record: Dict) -> Set[str]:
    return {item.get("form") for item in record.get("historical_lineage", []) if item.get("form")}


def candidate_ids_for_query(query: str, index: Dict, nearest_limit: int = 0) -> Dict[int, Set[str]]:
    maps = index["maps"]
    records = index["records"]
    candidate_types: Dict[int, Set[str]] = {}

    def add(ids: Iterable[int], search_type: str) -> None:
        for rid in ids or []:
            candidate_types.setdefault(int(rid), set()).add(search_type)

    exact_ids = maps["by_word"].get(query, [])
    add(exact_ids, "exact")

    for rid in exact_ids:
        record = records[int(rid)]
        add(maps["by_lemma"].get(record["lemma"], []), "morphological")
        add(maps["by_root"].get(f"{record['language']}:{record['root']}", []), "morphological")
        if record.get("cognate_group"):
            add(maps["by_cognate"].get(record["cognate_group"], []), "cognate")
            add(maps["by_cognate"].get(record["cognate_group"], []), "cross-language")
        for form in record_lineage_forms(record):
            add(maps["by_lineage_form"].get(form, []), "historical")

    add(maps["by_lineage_form"].get(query, []), "historical")
    for rid in maps["by_lineage_form"].get(query, []):
        record = records[int(rid)]
        if record.get("cognate_group"):
            add(maps["by_cognate"].get(record["cognate_group"], []), "cognate")
            add(maps["by_cognate"].get(record["cognate_group"], []), "cross-language")

    if nearest_limit > 0:
        model = load_fasttext_model()
        for token, _ in model.wv.most_similar(query, topn=nearest_limit):
            add(maps["by_word"].get(token, []), "cross-language")

    return candidate_types


def semantic_search(query: str, topn: int = 20, index_path: str = str(INDEX_PATH)) -> Dict:
    query = (query or "").strip()
    if not query:
        return {"query": query, "results": []}
    index = load_semantic_index(index_path)
    records = index["records"]
    model = load_fasttext_model()
    candidate_types = candidate_ids_for_query(query, index)
    boosts = {
        "exact": 0.2,
        "cognate": 0.12,
        "historical": 0.1,
        "morphological": 0.06,
        "cross-language": 0.03,
    }
    results = []
    for rid, search_types in candidate_types.items():
        record = records[rid]
        try:
            similarity = float(model.wv.similarity(query, record["word"]))
        except Exception:
            similarity = 0.0
        boost = sum(boosts.get(item, 0.0) for item in search_types)
        if record["word"] == query:
            boost += 0.2
        score = similarity + boost
        results.append({
            "word": record["word"],
            "language": record["language"],
            "similarity": round(similarity, 6),
            "score": round(score, 6),
            "search_types": sorted(search_types),
            "cognate_group": record.get("cognate_group", ""),
            "historical_lineage": record.get("historical_lineage", []),
        })
    results.sort(key=lambda item: (item["score"], item["similarity"]), reverse=True)

    deduped = []
    seen = set()
    for item in results:
        key = (item["word"], item["language"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
        if len(deduped) >= topn:
            break
    return {"query": query, "results": deduped}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search the Turkic semantic index")
    parser.add_argument("query")
    parser.add_argument("--topn", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(semantic_search(args.query, args.topn), ensure_ascii=False, indent=2))
