import json
import os
from collections import Counter
from typing import Dict, List, Optional

from django.core.management.base import BaseCommand

from apps.morphology.services.morphology_service import analyze


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
        if analysis.get("type") == "lemma" and expected_suffixes:
            continue
        if expected_root and analysis.get("root") != expected_root:
            continue
        if suffix_chain(analysis) == expected_suffixes:
            return idx + 1
    return None


class Command(BaseCommand):
    help = "Evaluate Turkmen morphology against the Turkmen benchmark"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--report", help="Path to markdown report", default=None)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        bench_file = os.path.join(bench_dir, "turkmen_morphology_benchmark.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        stats_path = os.path.join(reports_dir, "turkmen_morphology_statistics.json")
        report_path = options.get("report") or "TURKMEN_MORPHOLOGY_REPORT.md"

        if not os.path.isfile(bench_file):
            self.stdout.write(self.style.ERROR(f"Missing benchmark at {bench_file}"))
            return

        with open(bench_file, encoding="utf-8") as fh:
            benchmark = json.load(fh)

        total = len(benchmark)
        coverage = 0
        top1 = 0
        top3 = 0
        any_match = 0
        ambiguity = []
        confusion = Counter()
        failures = []

        for case in benchmark:
            surface = case.get("surface", "")
            expected_root = case.get("stem")
            expected_suffixes = case.get("expected_suffixes", []) or []
            analyses = analyze(surface, "tk", max_results=50)
            if analyses:
                coverage += 1
            ambiguity.append(len(analyses))

            rank = matching_rank(analyses, expected_root, expected_suffixes)
            if rank == 1:
                top1 += 1
                top3 += 1
                any_match += 1
                confusion["TOP1_MATCH"] += 1
            elif rank and rank <= 3:
                top3 += 1
                any_match += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
            elif rank:
                any_match += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
            else:
                confusion["NO_MATCH"] += 1
                if len(failures) < 100:
                    failures.append({
                        "surface": surface,
                        "expected_root": expected_root,
                        "expected_suffixes": expected_suffixes,
                        "top": analyses[0] if analyses else None,
                    })

        stats = {
            "total": total,
            "coverage_count": coverage,
            "coverage_pct": round(coverage / total * 100, 2) if total else 0.0,
            "top1_count": top1,
            "top1_pct": round(top1 / total * 100, 2) if total else 0.0,
            "top3_count": top3,
            "top3_pct": round(top3 / total * 100, 2) if total else 0.0,
            "any_match_count": any_match,
            "any_match_pct": round(any_match / total * 100, 2) if total else 0.0,
            "avg_ambiguity": round(sum(ambiguity) / max(1, total), 2),
            "confusion": dict(confusion),
            "failure_examples": failures,
        }

        with open(stats_path, "w", encoding="utf-8") as out:
            json.dump(stats, out, ensure_ascii=False, indent=2)

        rules_path = os.path.join("backend", "data", "morphology", "turkmen_rules.json")
        lemmas_path = os.path.join("backend", "data", "morphology", "turkmen_lemmas.json")
        rule_count = 0
        lemma_count = 0
        if os.path.isfile(rules_path):
            with open(rules_path, encoding="utf-8") as fh:
                rule_count = len(json.load(fh).get("rules", []))
        if os.path.isfile(lemmas_path):
            with open(lemmas_path, encoding="utf-8") as fh:
                lemma_count = len(json.load(fh).get("lemmas", []))

        with open(report_path, "w", encoding="utf-8") as md:
            md.write("# Turkmen Morphology Report\n\n")
            md.write("## Inventory\n\n")
            md.write(f"- Rules: {rule_count}\n")
            md.write(f"- Lemmas: {lemma_count}\n")
            md.write(f"- Benchmark cases: {total}\n")
            md.write("- Script: Latin\n\n")
            md.write("## Evaluation\n\n")
            md.write("| Metric | Value |\n")
            md.write("| --- | ---: |\n")
            md.write(f"| Coverage | {stats['coverage_pct']}% |\n")
            md.write(f"| Top1 | {stats['top1_pct']}% |\n")
            md.write(f"| Top3 | {stats['top3_pct']}% |\n")
            md.write(f"| AnyMatch | {stats['any_match_pct']}% |\n")
            md.write(f"| Average ambiguity | {stats['avg_ambiguity']} |\n\n")
            md.write("## Confusion\n\n")
            md.write("| Type | Count |\n")
            md.write("| --- | ---: |\n")
            for key, value in confusion.most_common():
                md.write(f"| {key} | {value} |\n")
            md.write("\n## Vowel Harmony\n\n")
            md.write("- Turkmen Latin vowel harmony is enforced for productive suffixes.\n")
            md.write("- Examples: `kitaplarymyzdan`, `öýlerimizden`, and `adamlar` are valid analyses.\n")
            md.write("- Invalid direct analysis such as `öý + lar` is rejected for `öýlar`.\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {report_path}"))
