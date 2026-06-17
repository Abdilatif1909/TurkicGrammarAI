import json
import os
import random

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate Uzbek lemma benchmark using uzbek_lemmas.json and suffix inventory"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--count", type=int, default=1000)
        parser.add_argument("--lemmas", help="Path to uzbek_lemmas.json", default=None)
        parser.add_argument("--rules", help="Path to uzbek_rules.json", default=None)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        os.makedirs(bench_dir, exist_ok=True)
        bench_file = os.path.join(bench_dir, "uzbek_lemma_benchmark.json")

        lemmas_path = options.get("lemmas") or os.path.join("backend", "data", "morphology", "uzbek_lemmas.json")
        rules_path = options.get("rules") or os.path.join("backend", "data", "morphology", "uzbek_rules.json")
        lemmas_path = os.path.abspath(lemmas_path)
        rules_path = os.path.abspath(rules_path)
        if not os.path.isfile(lemmas_path) or not os.path.isfile(rules_path):
            self.stdout.write(self.style.ERROR("Missing lemmas or rules files"))
            return

        with open(lemmas_path, encoding="utf-8") as fh:
            lemmas = json.load(fh).get("lemmas", [])
        with open(rules_path, encoding="utf-8") as fh:
            rules = json.load(fh).get("rules", [])
        suffixes = [r.get("suffix") for r in rules if r.get("suffix")]

        bench = []
        for i in range(options.get("count")):
            lemma = random.choice(lemmas)
            chain_len = random.choice([0, 1, 1, 2])
            surface = lemma
            chosen = []
            for _ in range(chain_len):
                suf = random.choice(suffixes)
                surface = surface + suf
                chosen.append(suf)
            bench.append({"id": i + 1, "surface": surface, "expected_root": lemma, "expected_suffixes": chosen})

        with open(bench_file, "w", encoding="utf-8") as out:
            json.dump(bench, out, ensure_ascii=False, indent=2)
        self.stdout.write(self.style.SUCCESS(f"Wrote {len(bench)} lemma benchmark to {bench_file}"))
