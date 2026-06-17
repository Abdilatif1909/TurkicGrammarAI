import json
import os
from collections import Counter
from typing import Dict, List, Optional

from django.core.management.base import BaseCommand

from apps.morphology.services.morphology_service import _discover_analyses, build_rules_map_from_list


def suffix_chain(analysis: Dict) -> List[str]:
    chain = []
    for item in analysis.get("suffixes", []) or []:
        if isinstance(item, dict):
            chain.append(item.get("suffix"))
        else:
            chain.append(item)
    return [s for s in chain if s]


def matching_rank(analyses: List[Dict], expected_root: Optional[str], expected_suffixes: List[str]) -> Optional[int]:
    for idx, analysis in enumerate(analyses):
        if expected_root and analysis.get("root") != expected_root:
            continue
        if suffix_chain(analysis) == expected_suffixes:
            return idx + 1
    return None


def classify_error(case: Dict, analyses: List[Dict], rules_map: Dict):
    expected = case.get("expected_suffixes", []) or []
    stem = case.get("stem")

    if not analyses:
        if any(s and s not in rules_map for s in expected):
            return "RULE_MISSING", None
        return "SCORING_ERROR", None

    rank = matching_rank(analyses, stem, expected)
    if rank == 1:
        return None, rank
    if rank:
        return "VALID_ALTERNATIVE_ANALYSIS", rank

    missing = [s for s in expected if s and s not in rules_map]
    if missing:
        return "RULE_MISSING", None

    if stem and not any(a.get("root") == stem for a in analyses):
        return "TRUE_ROOT_ERROR", None

    return "SCORING_ERROR", None


class Command(BaseCommand):
    help = "Analyze benchmark errors and produce multi-analysis error report"

    def add_arguments(self, parser):
        parser.add_argument("--bench", help="Path to benchmark dir", default=None)
        parser.add_argument("--rules", help="Path to rules json", default=None)

    def handle(self, *args, **options):
        bench_dir = options.get("bench") or os.path.join("backend", "data", "benchmark")
        bench_file = os.path.join(bench_dir, "uzbek_morphology.json")
        rules_path = options.get("rules") or os.path.join("backend", "data", "morphology", "uzbek_rules.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)

        if not os.path.isfile(bench_file):
            self.stdout.write(self.style.ERROR(f"Missing benchmark file: {bench_file}"))
            return
        if not os.path.isfile(rules_path):
            self.stdout.write(self.style.ERROR(f"Missing rules file: {rules_path}"))
            return

        with open(bench_file, encoding="utf-8") as fh:
            bench = json.load(fh)
        with open(rules_path, encoding="utf-8") as fh:
            rules_json = json.load(fh).get("rules", [])

        rules_map = build_rules_map_from_list(rules_json)

        errors = []
        type_counter = Counter()
        suffix_conflicts = Counter()
        root_conflicts = Counter()
        pattern_counter = Counter()

        for case in bench:
            surface = case.get("surface")
            expected = case.get("expected_suffixes", []) or []
            stem = case.get("stem")
            analyses = _discover_analyses(surface, rules_map, max_depth=6)

            top = analyses[0] if analyses else None
            predicted = suffix_chain(top) if top else []
            predicted_root = top.get("root") if top else None
            score = top.get("score") if top else 0.0

            etype, rank = classify_error(case, analyses, rules_map)
            if etype is None:
                continue

            type_counter[etype] += 1
            suffix_conflicts[tuple(expected), tuple(predicted)] += 1

            if stem and predicted_root and predicted_root != stem:
                root_conflicts[(stem, predicted_root)] += 1

            expected_str = "|".join(expected) if expected else "<empty>"
            predicted_str = "|".join(predicted) if predicted else "<empty>"
            pattern_counter[f"{expected_str} -> {predicted_str}"] += 1

            errors.append({
                "word": surface,
                "expected_root": stem,
                "predicted_root": predicted_root,
                "expected": expected,
                "predicted": predicted,
                "rank": rank,
                "score": float(score),
                "type": etype,
            })

        err_path = os.path.join(reports_dir, "uzbek_morphology_errors.json")
        with open(err_path, "w", encoding="utf-8") as out:
            json.dump(errors, out, ensure_ascii=False, indent=2)

        confusion_path = os.path.join(reports_dir, "uzbek_morphology_confusion.json")
        with open(confusion_path, "w", encoding="utf-8") as out:
            json.dump({
                "error_type_counts": dict(type_counter),
                "suffix_conflicts": [
                    {"expected": list(exp), "predicted": list(pred), "count": count}
                    for (exp, pred), count in suffix_conflicts.most_common(100)
                ],
                "root_conflicts": [
                    {"expected_root": exp, "predicted_root": pred, "count": count}
                    for (exp, pred), count in root_conflicts.most_common(100)
                ],
            }, out, ensure_ascii=False, indent=2)

        md_path = os.path.join(reports_dir, "UZBEK_MORPHOLOGY_ERROR_REPORT.md")
        with open(md_path, "w", encoding="utf-8") as md:
            md.write("# Uzbek Morphology Error Report\n\n")
            md.write(f"Total benchmark cases: {len(bench)}\n")
            md.write(f"Total non-top or failing cases: {len(errors)}\n\n")
            md.write("## Error type counts\n\n")
            md.write("| Error Type | Count |\n")
            md.write("| ---------- | -----:|\n")
            for t, c in type_counter.most_common():
                md.write(f"| {t} | {c} |\n")

            md.write("\n## Top 50 failure patterns\n\n")
            for pat, cnt in pattern_counter.most_common(50):
                md.write(f"- {pat} - {cnt}\n")

            md.write("\n## Most frequent suffix conflicts\n\n")
            for (exp, pred), cnt in suffix_conflicts.most_common(20):
                md.write(f"- {list(exp)} -> {list(pred)} : {cnt}\n")

            md.write("\n## Most frequent root conflicts\n\n")
            for (exp_root, pred_root), cnt in root_conflicts.most_common(20):
                md.write(f"- {exp_root} -> {pred_root} : {cnt}\n")

        self.stdout.write(
            self.style.SUCCESS(f"Wrote errors to {err_path}, confusion to {confusion_path}, and report to {md_path}")
        )
