import json
import os

from django.core.management.base import BaseCommand

from apps.cognates.services.universal_cognates import UniversalCognateService


class Command(BaseCommand):
    help = "Evaluate universal cross-language cognate alignment"

    def add_arguments(self, parser):
        parser.add_argument(
            "--benchmark",
            default=os.path.join("backend", "data", "benchmark", "cross_language_cognate_benchmark.json"),
        )
        parser.add_argument("--report", default="COGNATE_ALIGNMENT_REPORT.md")

    def handle(self, *args, **options):
        benchmark_path = options["benchmark"]
        report_path = options["report"]
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        stats_path = os.path.join(reports_dir, "cognate_alignment_statistics.json")

        if not os.path.isfile(benchmark_path):
            self.stdout.write(self.style.ERROR(f"Missing benchmark at {benchmark_path}"))
            return

        with open(benchmark_path, encoding="utf-8") as fh:
            benchmark = json.load(fh)

        total = len(benchmark)
        aligned = 0
        covered = 0
        failures = []
        language_totals = {}
        language_hits = {}

        for case in benchmark:
            language = case.get("language") or "proto"
            language_totals[language] = language_totals.get(language, 0) + 1
            results = UniversalCognateService.search(
                query=case.get("query"),
                language=None if language == "proto" else language,
                limit=5,
            )
            if results:
                covered += 1
            expected_id = case.get("expected_cognate_id")
            top_id = results[0]["cognate_id"] if results else None
            if top_id == expected_id:
                aligned += 1
                language_hits[language] = language_hits.get(language, 0) + 1
            elif len(failures) < 100:
                failures.append({
                    "query": case.get("query"),
                    "language": language,
                    "expected_cognate_id": expected_id,
                    "predicted_cognate_id": top_id,
                })

        by_language = {
            lang: round(language_hits.get(lang, 0) / count * 100, 2)
            for lang, count in sorted(language_totals.items())
            if count
        }
        stats = {
            "total_cases": total,
            "alignment_accuracy": round(aligned / total * 100, 2) if total else 0.0,
            "coverage": round(covered / total * 100, 2) if total else 0.0,
            "by_language_alignment_accuracy": by_language,
            "failure_examples": failures,
        }

        with open(stats_path, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, ensure_ascii=False, indent=2)

        with open(report_path, "w", encoding="utf-8") as md:
            md.write("# Cognate Alignment Report\n\n")
            md.write("## Metrics\n\n")
            md.write("| Metric | Value |\n")
            md.write("| --- | ---: |\n")
            md.write(f"| Benchmark cases | {total} |\n")
            md.write(f"| Alignment accuracy | {stats['alignment_accuracy']}% |\n")
            md.write(f"| Coverage | {stats['coverage']}% |\n\n")
            md.write("## Language Accuracy\n\n")
            md.write("| Language | Accuracy |\n")
            md.write("| --- | ---: |\n")
            for lang, value in by_language.items():
                md.write(f"| {lang} | {value}% |\n")
            md.write("\n## Readiness\n\n")
            md.write("- Universal cognate groups cover `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, and `otk`.\n")
            md.write("- Search normalizes Latin, Cyrillic, Uyghur Arabic, and Old Turkic runiform forms.\n")
            md.write("- The output includes a historical chain suitable for embedding and semantic-search alignment.\n")
            md.write("- Detailed failures are saved in `backend/data/reports/cognate_alignment_statistics.json`.\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {report_path}"))
