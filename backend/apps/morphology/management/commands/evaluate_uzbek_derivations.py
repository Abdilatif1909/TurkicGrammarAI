import json
import os
from collections import Counter
from typing import Dict, List

from django.core.management.base import BaseCommand

from apps.morphology.services.morphology_service import analyze


def matching_rank(analyses: List[Dict], expected_root: str, expected_derivation: str):
    for idx, analysis in enumerate(analyses):
        if analysis.get("type") != "derivational":
            continue
        if analysis.get("root") == expected_root and analysis.get("derivation") == expected_derivation:
            return idx + 1
    return None


class Command(BaseCommand):
    help = "Evaluate Uzbek derivational morphology against a dedicated benchmark"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--benchmark", help="Path to derivational benchmark JSON", default=None)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        bench_file = options.get("benchmark") or os.path.join(bench_dir, "uzbek_derivational_benchmark.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)

        stats_path = os.path.join(reports_dir, "uzbek_derivational_statistics.json")
        report_path = os.path.join(reports_dir, "DERIVATIONAL_MORPHOLOGY_REPORT.md")

        if not os.path.isfile(bench_file):
            self.stdout.write(self.style.ERROR(f"Missing benchmark: {bench_file}"))
            return

        with open(bench_file, encoding="utf-8") as fh:
            bench = json.load(fh)

        total = len(bench)
        coverage = 0
        top1_match = 0
        top3_match = 0
        any_match = 0
        root_any_match = 0
        derivation_any_match = 0
        failures = []
        category_counts = Counter()
        category_correct = Counter()
        confusion = Counter()

        for case in bench:
            surface = case.get("surface")
            expected_root = case.get("expected_root")
            expected_derivation = case.get("expected_derivation")
            category = case.get("category", "Unknown")
            category_counts[category] += 1

            analyses = analyze(surface, "uz", max_results=10)
            if analyses:
                coverage += 1

            rank = matching_rank(analyses, expected_root, expected_derivation)
            root_ok_any = any(a.get("root") == expected_root for a in analyses)
            derivation_ok_any = any(
                a.get("type") == "derivational" and a.get("derivation") == expected_derivation
                for a in analyses
            )

            if root_ok_any:
                root_any_match += 1
            if derivation_ok_any:
                derivation_any_match += 1

            if rank == 1:
                top1_match += 1
                top3_match += 1
                any_match += 1
                category_correct[category] += 1
                confusion["TOP1_MATCH"] += 1
            elif rank and rank <= 3:
                top3_match += 1
                any_match += 1
                category_correct[category] += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
            elif rank:
                any_match += 1
                category_correct[category] += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
            else:
                if not root_ok_any:
                    confusion["TRUE_ROOT_ERROR"] += 1
                elif not derivation_ok_any:
                    confusion["DERIVATION_ERROR"] += 1
                else:
                    confusion["SCORING_ERROR"] += 1
                top = analyses[0] if analyses else {}
                failures.append({
                    "surface": surface,
                    "expected_root": expected_root,
                    "predicted_root": top.get("root"),
                    "expected_derivation": expected_derivation,
                    "predicted_derivation": top.get("derivation"),
                    "category": category,
                    "top_analysis": top,
                })

        stats = {
            "total": total,
            "coverage_count": coverage,
            "coverage_pct": round(coverage / total * 100, 2) if total else 0.0,
            "top1_count": top1_match,
            "top1_pct": round(top1_match / total * 100, 2) if total else 0.0,
            "top3_count": top3_match,
            "top3_pct": round(top3_match / total * 100, 2) if total else 0.0,
            "any_match_count": any_match,
            "any_match_pct": round(any_match / total * 100, 2) if total else 0.0,
            "derivation_accuracy_count": any_match,
            "derivation_accuracy_pct": round(any_match / total * 100, 2) if total else 0.0,
            "root_accuracy_count": root_any_match,
            "root_accuracy_pct": round(root_any_match / total * 100, 2) if total else 0.0,
            "derivation_label_accuracy_count": derivation_any_match,
            "derivation_label_accuracy_pct": round(derivation_any_match / total * 100, 2) if total else 0.0,
            "derivational_failure_count": len(failures),
            "confusion": dict(confusion),
            "category_accuracy": {
                category: {
                    "total": count,
                    "correct": category_correct[category],
                    "accuracy_pct": round(category_correct[category] / count * 100, 2) if count else 0.0,
                }
                for category, count in sorted(category_counts.items())
            },
            "failures": failures[:100],
        }

        with open(stats_path, "w", encoding="utf-8") as out:
            json.dump(stats, out, ensure_ascii=False, indent=2)

        with open(report_path, "w", encoding="utf-8") as md:
            md.write("# Derivational Morphology Report\n\n")
            md.write(f"- Total benchmark cases: {total}\n")
            md.write(f"- Coverage: {coverage} ({stats['coverage_pct']}%)\n")
            md.write(f"- Top-1 match: {top1_match} ({stats['top1_pct']}%)\n")
            md.write(f"- Top-3 match: {top3_match} ({stats['top3_pct']}%)\n")
            md.write(f"- Any-match: {any_match} ({stats['any_match_pct']}%)\n")
            md.write(f"- Root any-match: {root_any_match} ({stats['root_accuracy_pct']}%)\n")
            md.write(f"- Derivational failures: {len(failures)}\n\n")
            md.write("## Category Accuracy\n\n")
            md.write("| Category | Correct | Total | Accuracy |\n")
            md.write("| -------- | ------: | ----: | -------: |\n")
            for category, item in stats["category_accuracy"].items():
                md.write(
                    f"| {category} | {item['correct']} | {item['total']} | "
                    f"{item['accuracy_pct']}% |\n"
                )
            md.write("\n## Confusion\n\n")
            md.write("| Type | Count |\n")
            md.write("| ---- | ----: |\n")
            for key, value in confusion.most_common():
                md.write(f"| {key} | {value} |\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {report_path}"))
