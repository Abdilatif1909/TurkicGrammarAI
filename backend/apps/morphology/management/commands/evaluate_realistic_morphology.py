import json
import os
from collections import Counter
from typing import Dict, List, Optional

from django.core.management.base import BaseCommand

from apps.morphology.services.morphology_service import analyze


LANGUAGES = ["uz", "tr", "az", "kk", "ky", "tk", "ug", "otk"]


def suffix_chain(analysis: Dict) -> List[str]:
    chain = []
    for item in analysis.get("suffixes", []) or []:
        if isinstance(item, dict):
            chain.append(item.get("suffix"))
        else:
            chain.append(item)
    return [s for s in chain if s]


def matches(analysis: Dict, expected_root: Optional[str], expected_lemma: Optional[str], expected_suffixes):
    root_match = expected_root and analysis.get("root") == expected_root
    lemma_match = expected_lemma and analysis.get("lemma") == expected_lemma
    if not (root_match or lemma_match):
        return False
    if expected_suffixes is None:
        return True
    return suffix_chain(analysis) == expected_suffixes


def matching_rank(analyses: List[Dict], expected_root: Optional[str], expected_lemma: Optional[str], expected_suffixes) -> Optional[int]:
    for idx, analysis in enumerate(analyses):
        if matches(analysis, expected_root, expected_lemma, expected_suffixes):
            return idx + 1
    return None


class Command(BaseCommand):
    help = "Evaluate morphology against independent root/lemma benchmarks"

    def add_arguments(self, parser):
        parser.add_argument("--path", default=os.path.join("backend", "data", "benchmark", "independent"))
        parser.add_argument("--report", default="REALISTIC_EVALUATION_REPORT.md")

    def handle(self, *args, **options):
        bench_dir = options["path"]
        report_path = options["report"]
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)

        all_stats = {}
        for language in LANGUAGES:
            bench_file = os.path.join(bench_dir, f"{language}_independent_morphology.json")
            if not os.path.isfile(bench_file):
                all_stats[language] = {"error": f"missing {bench_file}"}
                continue
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
                expected_lemma = case.get("lemma")
                expected_suffixes = case.get("expected_suffixes", None)
                analyses = analyze(surface, language, max_results=50)
                if analyses:
                    coverage += 1
                ambiguity.append(len(analyses))

                rank = matching_rank(analyses, expected_root, expected_lemma, expected_suffixes)
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
                    if len(failures) < 25:
                        failures.append({
                            "surface": surface,
                            "expected_root": expected_root,
                            "expected_lemma": expected_lemma,
                            "top": analyses[0] if analyses else None,
                        })

            all_stats[language] = {
                "total": total,
                "coverage_pct": round(coverage / total * 100, 2) if total else 0.0,
                "top1_pct": round(top1 / total * 100, 2) if total else 0.0,
                "top3_pct": round(top3 / total * 100, 2) if total else 0.0,
                "any_match_pct": round(any_match / total * 100, 2) if total else 0.0,
                "avg_ambiguity": round(sum(ambiguity) / max(1, total), 2),
                "confusion": dict(confusion),
                "failure_examples": failures,
            }

        stats_path = os.path.join(reports_dir, "realistic_morphology_statistics.json")
        with open(stats_path, "w", encoding="utf-8") as fh:
            json.dump(all_stats, fh, ensure_ascii=False, indent=2)

        with open(report_path, "w", encoding="utf-8") as md:
            md.write("# Realistic Evaluation Report\n\n")
            md.write("Independent benchmarks use dictionary/curated word-list surfaces with root/lemma annotations. ")
            md.write("They do not use analyzer rule files to generate expected suffix chains.\n\n")
            md.write("| Language | Cases | Top1 | Top3 | AnyMatch | Coverage |\n")
            md.write("| --- | ---: | ---: | ---: | ---: | ---: |\n")
            for language in LANGUAGES:
                stats = all_stats.get(language, {})
                md.write(
                    f"| {language} | {stats.get('total', 0)} | {stats.get('top1_pct', 0)}% | "
                    f"{stats.get('top3_pct', 0)}% | {stats.get('any_match_pct', 0)}% | {stats.get('coverage_pct', 0)}% |\n"
                )
            md.write("\n## Notes\n\n")
            md.write("- Synthetic benchmarks remain useful for rule coverage regression.\n")
            md.write("- Independent benchmarks are stricter on real dictionary surfaces but currently evaluate root/lemma correctness where suffix chains are not independently annotated.\n")
            md.write("- Full morpheme-level independent evaluation still requires hand-annotated suffix chains from corpus/dictionary sources.\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {report_path}"))
