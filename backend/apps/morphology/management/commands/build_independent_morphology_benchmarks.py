import json
import os
from typing import Dict, Iterable, List

from django.core.management.base import BaseCommand


LANGUAGES = {
    "uz": "uzbek",
    "tr": "turkish",
    "az": "azerbaijani",
    "kk": "kazakh",
    "ky": "kyrgyz",
    "tk": "turkmen",
    "ug": "uyghur",
    "otk": "old_turkic",
}


def source_candidates(slug: str) -> Iterable[str]:
    yield os.path.join("backend", "data", "normalized", f"{slug}_words_clean.json")
    yield os.path.join("backend", "data", "words", f"{slug}_words.json")
    yield os.path.join("backend", "data", "morphology", f"{slug}_lemmas.json")


def load_records(code: str, slug: str) -> List[Dict]:
    for path in source_candidates(slug):
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            rows = data.get("lemmas", [])
            if rows:
                return [
                    {
                        "surface": row.get("lemma") if isinstance(row, dict) else row,
                        "stem": row.get("lemma") if isinstance(row, dict) else row,
                        "lemma": row.get("lemma") if isinstance(row, dict) else row,
                        "pos": row.get("category") if isinstance(row, dict) else None,
                        "source": path,
                        "source_type": "lemma_dictionary",
                    }
                    for row in rows
                ]
        if isinstance(data, list):
            return [
                {
                    "surface": row.get("word"),
                    "stem": row.get("root") or row.get("lemma"),
                    "lemma": row.get("lemma") or row.get("root"),
                    "pos": row.get("pos"),
                    "source": row.get("source") or path,
                    "source_type": "dictionary_or_curated_word_list",
                }
                for row in data
                if isinstance(row, dict)
            ]
    return []


class Command(BaseCommand):
    help = "Build independent morphology benchmarks from dictionary/curated word sources"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=1000)
        parser.add_argument("--out", default=os.path.join("backend", "data", "benchmark", "independent"))

    def handle(self, *args, **options):
        limit = int(options["limit"])
        out_dir = options["out"]
        os.makedirs(out_dir, exist_ok=True)

        summary = {}
        for code, slug in LANGUAGES.items():
            records = load_records(code, slug)
            selected = []
            seen = set()
            for record in records:
                surface = record.get("surface")
                stem = record.get("stem")
                if not surface or not stem:
                    continue
                if surface in seen:
                    continue
                seen.add(surface)
                selected.append({
                    "language": code,
                    "surface": surface,
                    "stem": stem,
                    "lemma": record.get("lemma") or stem,
                    "expected_suffixes": None,
                    "annotation_type": "independent_root_or_lemma",
                    "pos": record.get("pos"),
                    "source": record.get("source"),
                    "source_type": record.get("source_type"),
                })
                if len(selected) >= limit:
                    break

            path = os.path.join(out_dir, f"{code}_independent_morphology.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(selected, fh, ensure_ascii=False, indent=2)
            summary[code] = {"count": len(selected), "path": path}

        summary_path = os.path.join(out_dir, "independent_benchmark_summary.json")
        with open(summary_path, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Wrote independent benchmark summary to {summary_path}"))
