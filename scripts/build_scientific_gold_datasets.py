import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = ROOT / "backend/data/gold"
BENCHMARK_DIR = ROOT / "backend/data/benchmark"
INDEPENDENT_DIR = BENCHMARK_DIR / "independent"
COGNATE_PATH = ROOT / "backend/data/cognates/cross_language_cognates.json"
HISTORICAL_PATH = ROOT / "backend/data/historical/historical_forms.json"
QA_PATH = ROOT / "backend/data/embeddings/qa_benchmark.json"


LANG_FILES = {
    "uz": "uz_independent_morphology.json",
    "tr": "tr_independent_morphology.json",
    "az": "az_independent_morphology.json",
    "kk": "kk_independent_morphology.json",
    "ky": "ky_independent_morphology.json",
    "tk": "tk_independent_morphology.json",
    "ug": "ug_independent_morphology.json",
    "otk": "otk_independent_morphology.json",
}

SYNTHETIC_MORPHOLOGY_FILES = {
    "uz": "uzbek_morphology.json",
    "tr": "turkish_morphology_benchmark.json",
    "az": "azerbaijani_morphology_benchmark.json",
    "kk": "kazakh_morphology_benchmark.json",
    "ky": "kyrgyz_morphology_benchmark.json",
    "tk": "turkmen_morphology_benchmark.json",
    "ug": "uyghur_morphology_benchmark.json",
    "otk": "old_turkic_morphology_benchmark.json",
}


def load_json(path, default=None):
    if not path.exists():
        return default if default is not None else []
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def review_meta(source, level="candidate_requires_expert_review"):
    return {
        "review_status": level,
        "reviewed_by": None,
        "review_date": None,
        "source": source,
        "scientific_note": (
            "Gold-candidate item generated from existing project resources. "
            "Do not treat as publication-grade until expert review fields are completed."
        ),
    }


def build_morphology():
    records = []
    per_language_target = 625
    idx = 1
    for language, filename in LANG_FILES.items():
        rows = load_json(INDEPENDENT_DIR / filename, [])
        seen = set()
        selected = []
        for row in rows:
            key = (row.get("surface"), row.get("stem"), row.get("lemma"), json.dumps(row.get("expected_suffixes"), ensure_ascii=False))
            if key in seen:
                continue
            seen.add(key)
            selected.append(row)
            if len(selected) >= per_language_target:
                break
        for row in selected:
            records.append({
                "id": f"gold_morph_{idx:05d}",
                "language": language,
                "surface": row.get("surface"),
                "expected_root": row.get("stem"),
                "expected_lemma": row.get("lemma") or row.get("stem"),
                "expected_suffixes": row.get("expected_suffixes"),
                "pos": row.get("pos"),
                "annotation_type": row.get("annotation_type"),
                **review_meta(row.get("source") or filename),
            })
            idx += 1
    seen_surfaces = {(row["language"], row["surface"]) for row in records}
    for language, filename in SYNTHETIC_MORPHOLOGY_FILES.items():
        if len(records) >= 5000:
            break
        rows = load_json(BENCHMARK_DIR / filename, [])
        for row in rows:
            surface = row.get("surface")
            if not surface or (language, surface) in seen_surfaces:
                continue
            seen_surfaces.add((language, surface))
            records.append({
                "id": f"gold_morph_{idx:05d}",
                "language": language,
                "surface": surface,
                "expected_root": row.get("stem"),
                "expected_lemma": row.get("lemma") or row.get("stem"),
                "expected_suffixes": row.get("expected_suffixes"),
                "pos": row.get("pos"),
                "annotation_type": "synthetic_rule_regression_supplement",
                **review_meta(f"backend/data/benchmark/{filename}", "candidate_synthetic_requires_expert_review"),
            })
            idx += 1
            if len(records) >= 5000:
                break
    write_json(GOLD_DIR / "gold_morphology_dataset.json", records[:5000])
    return records[:5000]


def build_cognates():
    rows = load_json(COGNATE_PATH, [])
    records = []
    for idx, row in enumerate(rows[:2000], start=1):
        records.append({
            "id": f"gold_cognate_{idx:05d}",
            "cognate_id": row.get("cognate_id"),
            "proto_form": row.get("proto_form"),
            "semantic_domain": row.get("semantic_domain"),
            "forms": row.get("forms", {}),
            "expected_cognate_group": row.get("cognate_id"),
            "confidence": row.get("confidence"),
            **review_meta("backend/data/cognates/cross_language_cognates.json"),
        })
    write_json(GOLD_DIR / "gold_cognates_dataset.json", records)
    return records


def build_historical():
    rows = load_json(HISTORICAL_PATH, [])
    records = []
    seen = set()
    for row in rows:
        key = (row.get("proto_form"), row.get("old_turkic_form"), row.get("middle_turkic_form"), row.get("modern_language"), row.get("modern_form"))
        if key in seen:
            continue
        seen.add(key)
        records.append({
            "id": f"gold_hist_{len(records) + 1:05d}",
            "lineage": [
                {"stage": "Proto Turkic", "form": row.get("proto_form")},
                {"stage": "Old Turkic", "form": row.get("old_turkic_form")},
                {"stage": "Middle Turkic", "form": row.get("middle_turkic_form")},
                {"stage": row.get("modern_language"), "form": row.get("modern_form")},
            ],
            "modern_language": row.get("modern_language"),
            "modern_form": row.get("modern_form"),
            "gloss": row.get("gloss"),
            "expected_proto_form": row.get("proto_form"),
            **review_meta(row.get("source") or "backend/data/historical/historical_forms.json"),
        })
        if len(records) >= 1000:
            break
    write_json(GOLD_DIR / "gold_historical_dataset.json", records)
    return records


def build_qa():
    base = load_json(QA_PATH, [])
    cognates = load_json(COGNATE_PATH, [])
    rows = []
    idx = 1
    for item in base:
        rows.append({
            "id": f"gold_qa_{idx:05d}",
            "question": item.get("question"),
            "category": item.get("category"),
            "query": item.get("query"),
            "expected_answer_terms": item.get("expected_words", []),
            "expected_sources": [{"source_type": item.get("expected_source_type"), "source_id": item.get("expected_cognate_id", "")}],
            "expected_answer": "; ".join(item.get("expected_words", [])[:8]),
            **review_meta("backend/data/embeddings/qa_benchmark.json"),
        })
        idx += 1
    while len(rows) < 2000 and cognates:
        cog = cognates[(len(rows) - len(base)) % len(cognates)]
        forms = cog.get("forms", {})
        query = forms.get("uz") or forms.get("tr") or cog.get("proto_form", "")
        rows.append({
            "id": f"gold_qa_{idx:05d}",
            "question": f"{query} so'zining turkiy tillardagi shakllari qanday?",
            "category": "cognate",
            "query": query,
            "expected_answer_terms": list(forms.values()),
            "expected_sources": [{"source_type": "cognate", "source_id": cog.get("cognate_id")}],
            "expected_answer": "; ".join(list(forms.values())[:8]),
            **review_meta("backend/data/cognates/cross_language_cognates.json"),
        })
        idx += 1
    write_json(GOLD_DIR / "gold_qa_dataset.json", rows[:2000])
    return rows[:2000]


def main():
    datasets = {
        "morphology": build_morphology(),
        "cognates": build_cognates(),
        "historical": build_historical(),
        "qa": build_qa(),
    }
    manifest = {
        name: {
            "records": len(rows),
            "review_status": dict(Counter(row.get("review_status") for row in rows)),
        }
        for name, rows in datasets.items()
    }
    write_json(GOLD_DIR / "gold_dataset_manifest.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
