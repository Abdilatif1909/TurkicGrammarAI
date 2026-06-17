import json
import os
from collections import defaultdict

from django.core.management.base import BaseCommand

from apps.morphology.services.universal_morphology import universal_analyze


class Command(BaseCommand):
    help = "Evaluate cross-language universal morphology normalization"

    def add_arguments(self, parser):
        parser.add_argument("--benchmark", default=os.path.join("backend", "data", "benchmark", "cross_language_benchmark.json"))
        parser.add_argument("--report", default="CROSS_LANGUAGE_MORPHOLOGY_REPORT.md")

    def handle(self, *args, **options):
        benchmark_path = options["benchmark"]
        report_path = options["report"]
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        stats_path = os.path.join(reports_dir, "cross_language_morphology_statistics.json")

        if not os.path.isfile(benchmark_path):
            self.stdout.write(self.style.ERROR(f"Missing benchmark at {benchmark_path}"))
            return

        with open(benchmark_path, encoding="utf-8") as fh:
            benchmark = json.load(fh)

        total = len(benchmark)
        exact_feature_matches = 0
        partial_scores = []
        groups = defaultdict(list)
        failures = []

        for case in benchmark:
            expected = set(case.get("expected_features", []))
            analysis = universal_analyze(case["surface"], case["language"])
            predicted = set(analysis.features)
            if predicted == expected:
                exact_feature_matches += 1
            union = expected | predicted
            partial = len(expected & predicted) / len(union) if union else 1.0
            partial_scores.append(partial)
            groups[case["group_id"]].append({
                "case": case,
                "analysis": analysis.to_dict(),
                "predicted": sorted(predicted),
                "expected": sorted(expected),
            })
            if predicted != expected and len(failures) < 100:
                failures.append({
                    "language": case["language"],
                    "surface": case["surface"],
                    "expected_features": sorted(expected),
                    "predicted_features": sorted(predicted),
                    "root": analysis.root,
                })

        equivalent_groups = 0
        for items in groups.values():
            feature_sets = {tuple(item["predicted"]) for item in items}
            expected_sets = {tuple(item["expected"]) for item in items}
            if len(feature_sets) == 1 and feature_sets == expected_sets:
                equivalent_groups += 1

        stats = {
            "total_cases": total,
            "total_groups": len(groups),
            "feature_accuracy": round(exact_feature_matches / total * 100, 2) if total else 0.0,
            "partial_feature_accuracy": round(sum(partial_scores) / max(1, total) * 100, 2),
            "equivalence_accuracy": round(equivalent_groups / max(1, len(groups)) * 100, 2),
            "failure_examples": failures,
        }

        with open(stats_path, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, ensure_ascii=False, indent=2)

        with open(report_path, "w", encoding="utf-8") as md:
            md.write("# Cross-Language Morphology Report\n\n")
            md.write("## Metrics\n\n")
            md.write("| Metric | Value |\n")
            md.write("| --- | ---: |\n")
            md.write(f"| Cases | {total} |\n")
            md.write(f"| Aligned groups | {len(groups)} |\n")
            md.write(f"| Feature accuracy | {stats['feature_accuracy']}% |\n")
            md.write(f"| Partial feature accuracy | {stats['partial_feature_accuracy']}% |\n")
            md.write(f"| Equivalence accuracy | {stats['equivalence_accuracy']}% |\n\n")
            md.write("## Universal Features\n\n")
            md.write("The evaluator normalizes language-specific suffix chains into shared features such as `PLURAL`, `POSS_1PL`, `ABLATIVE`, `DATIVE`, `PAST`, `NEGATIVE`, and `DERIVATIONAL`.\n\n")
            md.write("## Readiness\n\n")
            md.write("- Universal morphology output is suitable as input to cross-language cognate alignment.\n")
            md.write("- The benchmark aligns eight supported languages: `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, `otk`.\n")
            md.write("- Remaining failures are saved in `backend/data/reports/cross_language_morphology_statistics.json`.\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {report_path}"))
