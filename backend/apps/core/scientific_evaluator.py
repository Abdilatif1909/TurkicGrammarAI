import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

GOLD_DIR = PROJECT_ROOT / "backend/data/gold"
REPORTS_DIR = PROJECT_ROOT / "backend/data/reports"


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else []
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def suffix_chain(analysis: Dict) -> List[str]:
    chain = []
    for item in analysis.get("suffixes", []) or []:
        chain.append(item.get("suffix") if isinstance(item, dict) else item)
    return [item for item in chain if item]


def morphology_match(analysis: Dict, case: Dict) -> bool:
    root_ok = analysis.get("root") == case.get("expected_root")
    lemma_ok = analysis.get("lemma") == case.get("expected_lemma")
    suffixes = case.get("expected_suffixes")
    suffix_ok = True if suffixes is None else suffix_chain(analysis) == suffixes
    return (root_ok or lemma_ok) and suffix_ok


def evaluate_morphology(limit: Optional[int] = None) -> Dict:
    from apps.morphology.services.morphology_service import analyze

    cases = load_json(GOLD_DIR / "gold_morphology_dataset.json", [])
    if limit:
        cases = cases[:limit]
    total = len(cases)
    covered = top1 = top3 = any_match = 0
    reviewed = 0
    failures = []
    for case in cases:
        if case.get("review_status") == "expert_reviewed":
            reviewed += 1
        analyses = analyze(case.get("surface", ""), case.get("language", ""), max_results=20)
        covered += int(bool(analyses))
        rank = None
        for idx, analysis in enumerate(analyses):
            if morphology_match(analysis, case):
                rank = idx + 1
                break
        if rank == 1:
            top1 += 1
        if rank and rank <= 3:
            top3 += 1
        if rank:
            any_match += 1
        elif len(failures) < 50:
            failures.append({"surface": case.get("surface"), "language": case.get("language"), "expected_root": case.get("expected_root"), "top": analyses[0] if analyses else None})
    return {
        "cases": total,
        "expert_reviewed_cases": reviewed,
        "coverage": pct(covered, total),
        "top1_accuracy": pct(top1, total),
        "top3_accuracy": pct(top3, total),
        "any_match_accuracy": pct(any_match, total),
        "failures": failures,
    }


def evaluate_cognates() -> Dict:
    from apps.cognates.services.universal_cognates import UniversalCognateService

    cases = load_json(GOLD_DIR / "gold_cognates_dataset.json", [])
    total = len(cases)
    covered = correct = reviewed = 0
    failures = []
    for case in cases:
        if case.get("review_status") == "expert_reviewed":
            reviewed += 1
        query = case.get("proto_form") or next(iter(case.get("forms", {}).values()), "")
        results = UniversalCognateService.search(query=query, limit=5)
        covered += int(bool(results))
        predicted = results[0].get("cognate_id") if results else None
        if predicted == case.get("expected_cognate_group"):
            correct += 1
        elif len(failures) < 50:
            failures.append({"query": query, "expected": case.get("expected_cognate_group"), "predicted": predicted})
    return {"cases": total, "expert_reviewed_cases": reviewed, "coverage": pct(covered, total), "alignment_accuracy": pct(correct, total), "failures": failures}


def evaluate_historical() -> Dict:
    cases = load_json(GOLD_DIR / "gold_historical_dataset.json", [])
    total = len(cases)
    historical_records = load_json(PROJECT_ROOT / "backend/data/historical/historical_forms.json", [])
    by_modern = {row.get("modern_form"): row for row in historical_records}
    correct = covered = reviewed = 0
    failures = []
    for case in cases:
        if case.get("review_status") == "expert_reviewed":
            reviewed += 1
        row = by_modern.get(case.get("modern_form"))
        covered += int(bool(row))
        if row and row.get("proto_form") == case.get("expected_proto_form"):
            correct += 1
        elif len(failures) < 50:
            failures.append({"modern_form": case.get("modern_form"), "expected_proto": case.get("expected_proto_form"), "found": row})
    return {"cases": total, "expert_reviewed_cases": reviewed, "coverage": pct(covered, total), "lineage_accuracy": pct(correct, total), "failures": failures}


def evaluate_qa(limit: Optional[int] = 200) -> Dict:
    from apps.embeddings.turkic_qa import ask

    cases = load_json(GOLD_DIR / "gold_qa_dataset.json", [])
    if limit:
        cases = cases[:limit]
    total = len(cases)
    answer_hits = source_hits = reviewed = 0
    failures = []
    for case in cases:
        if case.get("review_status") == "expert_reviewed":
            reviewed += 1
        payload = ask(case.get("question", ""), topk=10)
        answer_text = json.dumps(payload, ensure_ascii=False).lower()
        expected_terms = [str(term).lower() for term in case.get("expected_answer_terms", []) if term]
        answer_ok = any(term in answer_text for term in expected_terms)
        expected_sources = {item.get("source_id") for item in case.get("expected_sources", []) if item.get("source_id")}
        returned_sources = {item.get("source_id") for item in payload.get("citations", []) if item.get("source_id")}
        source_ok = bool(expected_sources.intersection(returned_sources)) if expected_sources else bool(payload.get("citations"))
        answer_hits += int(answer_ok)
        source_hits += int(source_ok)
        if not answer_ok and len(failures) < 50:
            failures.append({"question": case.get("question"), "expected_terms": case.get("expected_answer_terms", [])[:8], "answer": payload.get("answer")})
    return {"cases": total, "expert_reviewed_cases": reviewed, "answer_accuracy": pct(answer_hits, total), "source_accuracy": pct(source_hits, total), "failures": failures}


def pct(value: int, total: int) -> float:
    return round(value / total * 100, 2) if total else 0.0


def run_all(qa_limit: Optional[int] = 200) -> Dict:
    import django

    django.setup()
    results = {
        "morphology": evaluate_morphology(),
        "cognates": evaluate_cognates(),
        "historical": evaluate_historical(),
        "qa": evaluate_qa(limit=qa_limit),
    }
    results["publication_ready"] = all(section.get("expert_reviewed_cases") == section.get("cases") for section in results.values() if isinstance(section, dict))
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with (REPORTS_DIR / "scientific_evaluation_statistics.json").open("w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=2)
    return results


if __name__ == "__main__":
    print(json.dumps(run_all(), ensure_ascii=False, indent=2))
