import json
import os
import random

from django.core.management.base import BaseCommand


def pick_stem():
    stems = [
        "kitob",
        "uy",
        "yoz",
        "ish",
        "o'q",
        "ta'lim",
        "bozor",
        "ma'no",
        "oila",
        "maktab",
        "uyqu",
        "yurak",
        "til",
        "daryo",
        "qalb",
        "davo",
        "so'z",
    ]
    return random.choice(stems)


class Command(BaseCommand):
    help = "Generate benchmark examples for Uzbek morphology"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--count", type=int, default=500)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        os.makedirs(bench_dir, exist_ok=True)
        bench_file = os.path.join(bench_dir, "uzbek_morphology.json")

        # load rules
        rules_path = os.path.join(os.path.dirname(bench_dir), "morphology", "uzbek_rules.json")
        if not os.path.isfile(rules_path):
            self.stdout.write(self.style.ERROR(f"Missing rules at {rules_path}"))
            return
        with open(rules_path, encoding="utf-8") as fh:
            rules = json.load(fh).get("rules", [])

        suffixes = [r["suffix"] for r in rules if r.get("suffix")]
        # create benchmark cases by sampling 1-3 suffix chains
        bench = []
        for i in range(options.get("count")):
            stem = pick_stem()
            chain_len = random.choice([1, 1, 2, 2, 3])
            chosen = []
            surface = stem
            for _ in range(chain_len):
                suf = random.choice(suffixes)
                # avoid nonsensical long combos by simple length guard
                if len(surface) + len(suf) > 50:
                    break
                surface = surface + suf
                chosen.append(suf)
            bench.append({
                "id": i + 1,
                "surface": surface,
                "stem": stem,
                "expected_suffixes": chosen,
            })

        with open(bench_file, "w", encoding="utf-8") as out:
            json.dump(bench, out, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Wrote {len(bench)} benchmark cases to {bench_file}"))
