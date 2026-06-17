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


class Command(BaseCommand):
    help = "Evaluate Uzbek morphology against benchmark and produce multi-analysis statistics"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--rules", help="Path to uzbek_rules.json", default=None)

    def handle(self, *args, **options):
        base_bench = options.get("path") or os.path.join("backend", "data", "benchmark")
        bench_file = os.path.join(base_bench, "uzbek_morphology.json")
        reports_dir = os.path.join("backend", "data", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        stats_path = os.path.join(reports_dir, "uzbek_morphology_statistics.json")
        md_path = os.path.join(reports_dir, "UZBEK_MORPHOLOGY_EVALUATION.md")

        if not os.path.isfile(bench_file):
            self.stdout.write(self.style.ERROR(f"Missing benchmark at {bench_file}"))
            return

        with open(bench_file, encoding="utf-8") as fh:
            bench = json.load(fh)

        rules_path = options.get("rules") or os.path.join("backend", "data", "morphology", "uzbek_rules.json")
        if not os.path.isfile(rules_path):
            self.stdout.write(self.style.ERROR(f"Missing rules file at {rules_path}"))
            return
        with open(rules_path, encoding="utf-8") as fh:
            rules_json = json.load(fh).get("rules", [])

        rules_map = build_rules_map_from_list(rules_json)

        total = len(bench)
        coverage = 0
        top1_match = 0
        top3_match = 0
        any_match = 0
        ambiguity_counts = []
        confusion = Counter()
        valid_alternatives = []

        for case in bench:
            surface = case.get("surface")
            expected_root = case.get("stem")
            expected_suffixes = case.get("expected_suffixes", []) or []
            analyses = _discover_analyses(surface, rules_map, max_depth=6)

            if analyses:
                coverage += 1
            ambiguity_counts.append(len(analyses))

            rank = matching_rank(analyses, expected_root, expected_suffixes)
            if rank == 1:
                top1_match += 1
                top3_match += 1
                any_match += 1
                confusion["TOP1_MATCH"] += 1
            elif rank and rank <= 3:
                top3_match += 1
                any_match += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
                valid_alternatives.append({
                    "surface": surface,
                    "expected_root": expected_root,
                    "expected_suffixes": expected_suffixes,
                    "rank": rank,
                    "top_root": analyses[0].get("root") if analyses else None,
                    "top_suffixes": suffix_chain(analyses[0]) if analyses else [],
                })
            elif rank:
                any_match += 1
                confusion["VALID_ALTERNATIVE_ANALYSIS"] += 1
                valid_alternatives.append({
                    "surface": surface,
                    "expected_root": expected_root,
                    "expected_suffixes": expected_suffixes,
                    "rank": rank,
                    "top_root": analyses[0].get("root") if analyses else None,
                    "top_suffixes": suffix_chain(analyses[0]) if analyses else [],
                })
            else:
                missing_rules = [s for s in expected_suffixes if s and s not in rules_map]
                if missing_rules:
                    confusion["RULE_MISSING"] += 1
                elif expected_root and not any(a.get("root") == expected_root for a in analyses):
                    confusion["TRUE_ROOT_ERROR"] += 1
                else:
                    confusion["SCORING_ERROR"] += 1

        avg_ambiguity = sum(ambiguity_counts) / max(1, total)
        stats = {
            "total_bench_cases": total,
            "coverage_count": coverage,
            "coverage_pct": round(coverage / total * 100, 2) if total else 0.0,
            "top_match_count": top1_match,
            "top_match_pct": round(top1_match / total * 100, 2) if total else 0.0,
            "top1_count": top1_match,
            "top1_pct": round(top1_match / total * 100, 2) if total else 0.0,
            "top3_count": top3_match,
            "top3_pct": round(top3_match / total * 100, 2) if total else 0.0,
            "any_match_count": any_match,
            "any_match_pct": round(any_match / total * 100, 2) if total else 0.0,
            "avg_ambiguity": round(avg_ambiguity, 2),
            "confusion": dict(confusion),
            "valid_alternative_examples": valid_alternatives[:100],
        }

        with open(stats_path, "w", encoding="utf-8") as out:
            json.dump(stats, out, ensure_ascii=False, indent=2)

        with open(md_path, "w", encoding="utf-8") as md:
            md.write("# Uzbek Morphology Evaluation\n\n")
            md.write(f"- Total benchmark cases: {total}\n")
            md.write(f"- Coverage: {coverage} ({stats['coverage_pct']}%)\n")
            md.write(f"- Top-1 match: {top1_match} ({stats['top1_pct']}%)\n")
            md.write(f"- Top-3 match: {top3_match} ({stats['top3_pct']}%)\n")
            md.write(f"- Any-match: {any_match} ({stats['any_match_pct']}%)\n")
            md.write(f"- Average ambiguity: {stats['avg_ambiguity']}\n")
            md.write("\n## Confusion\n\n")
            md.write("| Type | Count |\n")
            md.write("| ---- | ----: |\n")
            for key, value in confusion.most_common():
                md.write(f"| {key} | {value} |\n")

        self.stdout.write(self.style.SUCCESS(f"Wrote stats to {stats_path} and report to {md_path}"))
