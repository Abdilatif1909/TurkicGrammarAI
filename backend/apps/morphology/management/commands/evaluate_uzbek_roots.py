import json
import os
from typing import Dict

from django.core.management.base import BaseCommand

from apps.morphology.services.morphology_service import _discover_analyses, build_rules_map_from_list
from apps.morphology.services.derivational_service import discover_derivations
from apps.morphology.services.lemma_dictionary import LemmaDictionary


class Command(BaseCommand):
    help = "Evaluate root/lemma accuracy on uzbek_lemma_benchmark.json"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--rules", help="Path to uzbek_rules.json", default=None)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        bench_file = os.path.join(bench_dir, "uzbek_lemma_benchmark.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        stats_path = os.path.join(reports_dir, "uzbek_root_statistics.json")
        md_path = os.path.join(reports_dir, "UZBEK_ROOT_ANALYSIS_REPORT.md")

        if not os.path.isfile(bench_file):
            self.stdout.write(self.style.ERROR(f"Missing benchmark: {bench_file}"))
            return

        with open(bench_file, encoding="utf-8") as fh:
            bench = json.load(fh)

        # load rules from file to avoid DB usage
        rules_path = options.get("rules") or os.path.join("backend", "data", "morphology", "uzbek_rules.json")
        rules_path = os.path.abspath(rules_path)
        if not os.path.isfile(rules_path):
            self.stdout.write(self.style.ERROR(f"Missing rules file: {rules_path}"))
            return
        with open(rules_path, encoding="utf-8") as fh:
            rules_json = json.load(fh).get("rules", [])
        rules_map = build_rules_map_from_list(rules_json)

        LemmaDictionary.load()
        total = len(bench)
        correct_root = 0
        correct_lemma = 0
        conflicts: Dict[str, int] = {}

        for case in bench:
            surface = case.get("surface")
            expected_root = case.get("expected_root")

            derivational = discover_derivations(surface, "uz")
            if derivational:
                analyses = derivational
            # Step 1: exact lemma
            elif LemmaDictionary.is_lemma(surface):
                predicted_root = surface
                predicted_lemma = surface
                analyses = [{"root": predicted_root, "lemma": predicted_lemma, "suffixes": [], "score": 1.0}]
            else:
                # Step 2: longest matching lemma prefix
                longest = LemmaDictionary.longest_prefix(surface)
                analyses = _discover_analyses(surface, rules_map, max_depth=6)
                if longest:
                    # boost analyses with root == longest
                    for a in analyses:
                        if a.get("root") == longest:
                            a["score"] = a.get("score", 0.0) + 1.0
                    analyses.sort(key=lambda x: (x["score"], -len(x.get("suffixes", []))), reverse=True)

            top = analyses[0] if analyses else None
            predicted_root = top.get("root") if top else None
            predicted_lemma = top.get("lemma") if top else predicted_root

            if predicted_root == expected_root:
                correct_root += 1
            if LemmaDictionary.is_lemma(predicted_lemma):
                correct_lemma += 1
            if predicted_root != expected_root:
                conflicts.setdefault(expected_root, 0)
                conflicts[expected_root] += 1

        stats = {
            "total": total,
            "root_accuracy": round(correct_root / total * 100, 2) if total else 0.0,
            "lemma_accuracy": round(correct_lemma / total * 100, 2) if total else 0.0,
            "top_conflicts": sorted(conflicts.items(), key=lambda x: x[1], reverse=True)[:20],
        }

        with open(stats_path, "w", encoding="utf-8") as out:
            json.dump(stats, out, ensure_ascii=False, indent=2)

        with open(md_path, "w", encoding="utf-8") as md:
            md.write("# Uzbek Root Analysis Report\n\n")
            md.write(f"Total cases: {total}\n")
            md.write(f"Root accuracy: {stats['root_accuracy']}%\n")
            md.write(f"Lemma accuracy: {stats['lemma_accuracy']}%\n")
            md.write("\nTop root conflicts:\n\n")
            for root, cnt in stats['top_conflicts']:
                md.write(f"- {root}: {cnt}\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {md_path}"))
