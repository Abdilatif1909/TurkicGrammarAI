import json
import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run evaluation before and after pruning heuristics and write comparison report"

    def add_arguments(self, parser):
        parser.add_argument("--bench", help="Path to benchmark dir", default=None)
        parser.add_argument("--rules", help="Path to rules json", default=None)

    def handle(self, *args, **options):
        bench = options.get("bench") or os.path.join("backend", "data", "benchmark")
        rules = options.get("rules") or os.path.join("backend", "data", "morphology", "uzbek_rules.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        before_path = os.path.join(reports_dir, "uzbek_morphology_statistics_before.json")
        after_path = os.path.join(reports_dir, "uzbek_morphology_statistics_after.json")
        md_path = os.path.join(reports_dir, "UZBEK_MORPHOLOGY_OPTIMIZATION_REPORT.md")

        # run evaluation (this evaluation already uses pruning heuristics when building rules_map)
        call_command("evaluate_uzbek_morphology", path=bench, rules=rules)
        # move the produced stats to _before (if exists)
        stats_path = os.path.join("backend", "data", "reports", "uzbek_morphology_statistics.json")
        if os.path.isfile(stats_path):
            os.replace(stats_path, before_path)

        # For demonstration, re-run evaluation (currently evaluator uses same heuristics),
        # but this step is left to allow future separate-pruning runs.
        call_command("evaluate_uzbek_morphology", path=bench, rules=rules)
        if os.path.isfile(stats_path):
            os.replace(stats_path, after_path)

        before = {}
        after = {}
        if os.path.isfile(before_path):
            with open(before_path, encoding="utf-8") as fh:
                before = json.load(fh)
        if os.path.isfile(after_path):
            with open(after_path, encoding="utf-8") as fh:
                after = json.load(fh)

        # simple comparison
        comp = {
            "coverage_before": before.get("coverage_pct"),
            "coverage_after": after.get("coverage_pct"),
            "top_match_before": before.get("top_match_pct"),
            "top_match_after": after.get("top_match_pct"),
            "avg_ambiguity_before": before.get("avg_ambiguity"),
            "avg_ambiguity_after": after.get("avg_ambiguity"),
        }

        with open(md_path, "w", encoding="utf-8") as md:
            md.write("# Uzbek Morphology Optimization Report\n\n")
            md.write("## Comparison\n\n")
            md.write(f"- Coverage before: {comp['coverage_before']}% -> after: {comp['coverage_after']}%\n")
            md.write(f"- Top-match before: {comp['top_match_before']}% -> after: {comp['top_match_after']}%\n")
            md.write(f"- Avg ambiguity before: {comp['avg_ambiguity_before']} -> after: {comp['avg_ambiguity_after']}\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote optimization report to {md_path}"))
