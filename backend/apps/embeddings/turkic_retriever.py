import json
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, Set

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from apps.embeddings.semantic_search import load_semantic_index, semantic_search


INDEX_PATH = PROJECT_ROOT / "backend/data/embeddings/semantic_index.json"
LANGUAGE_FILE_STEMS = {
    "uz": "uzbek",
    "tr": "turkish",
    "az": "azerbaijani",
    "kk": "kazakh",
    "ky": "kyrgyz",
    "tk": "turkmen",
    "ug": "uyghur",
    "otk": "old_turkic",
}


def _record_id_maps(index: Dict) -> Dict[str, Dict]:
    return index["maps"]


def _add_candidate(candidates: Dict[int, Set[str]], ids: Iterable[int], source: str) -> None:
    for rid in ids or []:
        candidates.setdefault(int(rid), set()).add(source)


def _lineage_forms(record: Dict) -> Set[str]:
    return {item.get("form") for item in record.get("historical_lineage", []) if item.get("form")}


@lru_cache(maxsize=8)
def _words_for_language(language: str) -> Set[str]:
    stem = LANGUAGE_FILE_STEMS.get(language, language)
    paths = [
        PROJECT_ROOT / f"backend/data/words/{stem}_words.json",
        PROJECT_ROOT / f"backend/data/normalized/{stem}_words_clean.json",
    ]
    words: Set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        try:
            payload = json.load(path.open(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, str):
                    words.add(item)
                elif isinstance(item, dict):
                    for key in ("word", "surface_form", "lemma", "root"):
                        value = item.get(key)
                        if value:
                            words.add(str(value))
        elif isinstance(payload, dict):
            for item in payload.values():
                if isinstance(item, str):
                    words.add(item)
                elif isinstance(item, list):
                    words.update(str(value) for value in item if value)
                elif isinstance(item, dict):
                    for key in ("word", "surface_form", "lemma", "root"):
                        value = item.get(key)
                        if value:
                            words.add(str(value))
    return words


def _words_dataset_score(record: Dict) -> float:
    language = record.get("language", "")
    words = _words_for_language(language)
    if not words:
        return 0.0
    return 0.08 if record.get("word") in words or record.get("lemma") in words or record.get("root") in words else 0.0


def _source_id(record: Dict, source_type: str) -> str:
    if source_type == "cognate":
        return record.get("cognate_group", "")
    if source_type == "historical":
        lineage = record.get("historical_lineage", [])
        return lineage[0].get("form", "") if lineage else ""
    if source_type == "morphology":
        return f"{record.get('language', '')}:{record.get('root', '')}"
    if source_type == "dictionary":
        return f"{record.get('language', '')}:{record.get('lemma') or record.get('word', '')}"
    return f"{record.get('language', '')}:{record.get('word', '')}"


def _primary_source(scores: Dict[str, float], sources: Set[str]) -> str:
    source_order = ["cognate", "historical", "morphology", "dictionary", "semantic"]
    normalized_scores = dict(scores)
    if "words" in normalized_scores:
        normalized_scores["dictionary"] = normalized_scores.pop("words")
    for source in source_order:
        if source in sources and normalized_scores.get(source, 0.0) > 0:
            return source
    return max(normalized_scores, key=normalized_scores.get)


def _source_scores(record: Dict, sources: Set[str], semantic_similarity: float) -> Dict[str, float]:
    has_morphology = "morphology" in sources or "morphological" in sources
    scores = {
        "semantic": max(0.0, semantic_similarity) * 0.62,
        "cognate": 0.18 if "cognate" in sources else 0.0,
        "historical": 0.14 if "historical" in sources else 0.0,
        "morphology": 0.1 if has_morphology else 0.0,
        "dictionary": _words_dataset_score(record),
    }
    if "exact" in sources:
        scores["semantic"] += 0.16
    return scores


def _candidate_ids_from_metadata(query: str, index: Dict) -> Dict[int, Set[str]]:
    maps = _record_id_maps(index)
    records = index["records"]
    candidates: Dict[int, Set[str]] = defaultdict(set)

    exact_ids = maps["by_word"].get(query, [])
    _add_candidate(candidates, exact_ids, "exact")
    _add_candidate(candidates, exact_ids, "dictionary")

    lineage_ids = maps["by_lineage_form"].get(query, [])
    _add_candidate(candidates, lineage_ids, "historical")

    seed_ids = list(dict.fromkeys([*exact_ids, *lineage_ids]))
    for rid in seed_ids:
        record = records[int(rid)]
        _add_candidate(candidates, maps["by_lemma"].get(record.get("lemma", ""), []), "morphology")
        _add_candidate(candidates, maps["by_root"].get(f"{record.get('language')}:{record.get('root')}", []), "morphology")
        if record.get("cognate_group"):
            _add_candidate(candidates, maps["by_cognate"].get(record["cognate_group"], []), "cognate")
        for form in _lineage_forms(record):
            _add_candidate(candidates, maps["by_lineage_form"].get(form, []), "historical")

    return candidates


def retrieve(query: str, topn: int = 20, index_path: str = str(INDEX_PATH)) -> Dict:
    query = (query or "").strip()
    if not query:
        return {"query": query, "retrieved_documents": []}

    index = load_semantic_index(index_path)
    records = index["records"]
    candidates = _candidate_ids_from_metadata(query, index)
    semantic_payload = semantic_search(query, topn=max(topn * 4, 80), index_path=index_path)

    word_language_to_id = {
        (record["word"], record["language"]): idx
        for idx, record in enumerate(records)
    }
    semantic_by_id: Dict[int, float] = {}
    for item in semantic_payload["results"]:
        rid = word_language_to_id.get((item["word"], item["language"]))
        if rid is None:
            continue
        candidates.setdefault(rid, set()).update(item.get("search_types", []))
        candidates[rid].add("semantic")
        semantic_by_id[rid] = max(semantic_by_id.get(rid, 0.0), float(item.get("similarity", 0.0)))

    ranked = []
    for rid, sources in candidates.items():
        record = records[int(rid)]
        semantic_similarity = semantic_by_id.get(rid, 1.0 if record.get("word") == query else 0.0)
        normalized_sources = {"morphology" if item == "morphological" else item for item in sources}
        scores = _source_scores(record, normalized_sources, semantic_similarity)
        total_score = sum(scores.values())
        primary_source = _primary_source(scores, normalized_sources)
        confidence = min(0.99, max(0.0, total_score))
        ranked.append({
            "lemma": record.get("lemma", record.get("word", "")),
            "word": record.get("word", ""),
            "root": record.get("root", ""),
            "language": record.get("language", ""),
            "cognate_group": record.get("cognate_group", ""),
            "historical_lineage": record.get("historical_lineage", []),
            "similarity": round(semantic_similarity, 6),
            "semantic_score": round(scores["semantic"], 6),
            "cognate_score": round(scores["cognate"], 6),
            "historical_score": round(scores["historical"], 6),
            "morphology_score": round(scores["morphology"], 6),
            "dictionary_score": round(scores["dictionary"], 6),
            "final_relevance_score": round(total_score, 6),
            "source_type": primary_source,
            "source_id": _source_id(record, primary_source),
            "confidence": round(confidence, 6),
            "score": round(total_score, 6),
            "scores": {key: round(value, 6) for key, value in scores.items()},
            "sources": sorted(normalized_sources),
            "source_trace": [
                {
                    "source_type": source,
                    "source_id": _source_id(record, source),
                    "confidence": round(min(0.99, scores.get(source, 0.0)), 6),
                }
                for source in ("semantic", "cognate", "historical", "morphology", "dictionary")
                if scores.get(source, 0.0) > 0
            ],
        })

    ranked.sort(key=lambda item: (item["score"], item["similarity"], item["word"]), reverse=True)
    deduped = []
    seen = set()
    for item in ranked:
        key = (item["word"], item["language"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
        if len(deduped) >= topn:
            break

    return {"query": query, "retrieved_documents": deduped}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Retrieve RAG documents from Turkic linguistic sources")
    parser.add_argument("query")
    parser.add_argument("--topn", type=int, default=20)
    args = parser.parse_args()
    print(json.dumps(retrieve(args.query, args.topn), ensure_ascii=False, indent=2))
