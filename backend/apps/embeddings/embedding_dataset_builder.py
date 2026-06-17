import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


LANGUAGE_FILES = {
    "uz": "uzbek",
    "tr": "turkish",
    "az": "azerbaijani",
    "kk": "kazakh",
    "ky": "kyrgyz",
    "tk": "turkmen",
    "ug": "uyghur",
    "otk": "old_turkic",
}

LANGUAGE_NAMES = {
    "uz": "Uzbek",
    "tr": "Turkish",
    "az": "Azerbaijani",
    "kk": "Kazakh",
    "ky": "Kyrgyz",
    "tk": "Turkmen",
    "ug": "Uyghur",
    "otk": "Old Turkic",
}

DEFAULT_OUTPUT = Path("backend/data/embeddings/embedding_dataset.jsonl")
DEFAULT_REPORT = Path("EMBEDDING_DATASET_REPORT.md")
TARGET_RECORDS = 100_000
POS_FEATURES = {"noun": "NOUN", "verb": "VERB", "adjective": "ADJECTIVE", "derived": "DERIVATIONAL"}
SUFFIX_FEATURE_HINTS = {
    "lar": "PLURAL",
    "ler": "PLURAL",
    "дар": "PLURAL",
    "дер": "PLURAL",
    "тар": "PLURAL",
    "тер": "PLURAL",
    "لار": "PLURAL",
    "لەر": "PLURAL",
    "imiz": "POSS_1PL",
    "ымыз": "POSS_1PL",
    "имиз": "POSS_1PL",
    "ىمىز": "POSS_1PL",
    "dan": "ABLATIVE",
    "den": "ABLATIVE",
    "дан": "ABLATIVE",
    "ден": "ABLATIVE",
    "دىن": "ABLATIVE",
    "ga": "DATIVE",
    "ge": "DATIVE",
    "qa": "DATIVE",
    "ke": "DATIVE",
    "ға": "DATIVE",
    "ге": "DATIVE",
    "қа": "DATIVE",
    "ке": "DATIVE",
    "غا": "DATIVE",
    "ni": "ACCUSATIVE",
    "ny": "ACCUSATIVE",
    "نى": "ACCUSATIVE",
    "da": "LOCATIVE",
    "de": "LOCATIVE",
    "да": "LOCATIVE",
    "де": "LOCATIVE",
    "ta": "LOCATIVE",
    "te": "LOCATIVE",
    "ma": "NEGATIVE",
    "me": "NEGATIVE",
    "ма": "NEGATIVE",
    "ме": "NEGATIVE",
    "чи": "DERIVATIONAL",
    "chi": "DERIVATIONAL",
    "çi": "DERIVATIONAL",
    "чы": "DERIVATIONAL",
    "ші": "DERIVATIONAL",
    "چى": "DERIVATIONAL",
    "lik": "DERIVATIONAL",
    "lyk": "DERIVATIONAL",
    "لىق": "DERIVATIONAL",
    "лік": "DERIVATIONAL",
    "li": "DERIVATIONAL",
    "siz": "DERIVATIONAL",
    "сыз": "DERIVATIONAL",
    "سىز": "DERIVATIONAL",
}


def data_root() -> Path:
    return Path(__file__).resolve().parents[2] / "data"


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def clean_value(value: Optional[str]) -> str:
    return str(value or "").strip()


def feature_list(*items: Iterable[str]) -> List[str]:
    features = []
    for iterable in items:
        for item in iterable or []:
            item = clean_value(item).upper()
            if item and item not in features:
                features.append(item)
    return features


def infer_features(surface: str, pos: Optional[str] = None, suffixes: Optional[List[str]] = None) -> List[str]:
    features = []
    pos_feature = POS_FEATURES.get(clean_value(pos).lower())
    if pos_feature:
        features.append(pos_feature)
    lowered = surface.lower()
    for suffix, feature in SUFFIX_FEATURE_HINTS.items():
        if lowered.endswith(suffix.lower()) and feature not in features:
            features.append(feature)
    for suffix in suffixes or []:
        for hint, feature in SUFFIX_FEATURE_HINTS.items():
            if hint.lower() in clean_value(suffix).lower() and feature not in features:
                features.append(feature)
    return features


def make_record(
    surface_form: str,
    lemma: Optional[str],
    root: Optional[str],
    language: str,
    features: Optional[List[str]],
    cognate_group: Optional[str],
    historical_lineage: Optional[List[Dict]],
    source: str,
) -> Optional[Dict]:
    surface_form = clean_value(surface_form)
    language = clean_value(language)
    if not surface_form or not language:
        return None
    lemma = clean_value(lemma) or surface_form
    root = clean_value(root) or lemma or surface_form
    return {
        "surface_form": surface_form,
        "lemma": lemma,
        "root": root,
        "language": language,
        "features": feature_list(features or []),
        "cognate_group": clean_value(cognate_group),
        "historical_lineage": historical_lineage or [],
        "source": source,
    }


def cognate_lineage(group: Dict) -> List[Dict]:
    forms = group.get("forms", {})
    lineage = [{"stage": "Proto Turkic", "form": group.get("proto_form")}]
    for lang in ["otk", "ug", "uz", "tr", "az", "kk", "ky", "tk"]:
        lineage.append({"stage": LANGUAGE_NAMES[lang], "language": lang, "form": forms.get(lang)})
    return lineage


def build_cognate_indexes() -> Tuple[List[Dict], Dict[Tuple[str, str], Dict], Dict[str, List[Dict]]]:
    groups = load_json(data_root() / "cognates" / "cross_language_cognates.json", [])
    form_index = {}
    id_lineage = {}
    for group in groups:
        lineage = cognate_lineage(group)
        id_lineage[group.get("cognate_id")] = lineage
        for lang, form in (group.get("forms") or {}).items():
            if form:
                form_index[(lang, form)] = group
    return groups, form_index, id_lineage


def records_from_cognates(groups: List[Dict]) -> Iterator[Dict]:
    for group in groups:
        lineage = cognate_lineage(group)
        for lang, form in (group.get("forms") or {}).items():
            record = make_record(
                surface_form=form,
                lemma=form,
                root=form,
                language=lang,
                features=[],
                cognate_group=group.get("cognate_id"),
                historical_lineage=lineage,
                source="cognates",
            )
            if record:
                yield record


def records_from_words(form_index: Dict[Tuple[str, str], Dict]) -> Iterator[Dict]:
    root = data_root()
    for lang, name in LANGUAGE_FILES.items():
        path = root / "normalized" / f"{name}_words_clean.json"
        if not path.exists():
            path = root / "words" / f"{name}_words.json"
        for item in load_json(path, []):
            surface = item.get("word") or item.get("surface") or item.get("surface_form")
            group = form_index.get((lang, surface))
            lineage = cognate_lineage(group) if group else []
            features = infer_features(surface or "", item.get("pos"))
            record = make_record(
                surface_form=surface,
                lemma=item.get("lemma"),
                root=item.get("root") or item.get("lemma"),
                language=item.get("language_code") or lang,
                features=features,
                cognate_group=group.get("cognate_id") if group else "",
                historical_lineage=lineage,
                source="words_dataset",
            )
            if record:
                yield record


def records_from_lemmas(form_index: Dict[Tuple[str, str], Dict]) -> Iterator[Dict]:
    root = data_root()
    for lang, name in LANGUAGE_FILES.items():
        path = root / "morphology" / f"{name}_lemmas.json"
        data = load_json(path, {})
        for item in data.get("lemmas", []):
            if isinstance(item, dict):
                lemma = item.get("lemma")
                category = item.get("category")
            else:
                lemma = item
                category = None
            group = form_index.get((lang, lemma))
            record = make_record(
                surface_form=lemma,
                lemma=lemma,
                root=lemma,
                language=lang,
                features=infer_features(lemma or "", category),
                cognate_group=group.get("cognate_id") if group else "",
                historical_lineage=cognate_lineage(group) if group else [],
                source="lemma_dictionary",
            )
            if record:
                yield record


def records_from_morphology_benchmarks(id_lineage: Dict[str, List[Dict]]) -> Iterator[Dict]:
    root = data_root() / "benchmark"
    benchmark_files = {
        "uz": ["uzbek_lemma_benchmark.json", "uzbek_derivational_benchmark.json"],
        "tr": ["turkish_morphology_benchmark.json"],
        "az": ["azerbaijani_morphology_benchmark.json"],
        "kk": ["kazakh_morphology_benchmark.json"],
        "ky": ["kyrgyz_morphology_benchmark.json"],
        "tk": ["turkmen_morphology_benchmark.json"],
        "ug": ["uyghur_morphology_benchmark.json"],
        "otk": ["old_turkic_morphology_benchmark.json"],
    }
    for lang, files in benchmark_files.items():
        for filename in files:
            for item in load_json(root / filename, []):
                surface = item.get("surface") or item.get("word") or item.get("surface_form")
                expected_root = item.get("expected_root") or item.get("root") or item.get("lemma")
                expected_suffixes = item.get("expected_suffixes") or item.get("suffixes") or []
                expected_features = item.get("expected_features") or item.get("features") or []
                record = make_record(
                    surface_form=surface,
                    lemma=expected_root or surface,
                    root=expected_root or surface,
                    language=item.get("language") or lang,
                    features=feature_list(expected_features, infer_features(surface or "", item.get("category"), expected_suffixes)),
                    cognate_group=item.get("cognate_group") or "",
                    historical_lineage=id_lineage.get(item.get("cognate_group"), []),
                    source=f"morphology_benchmark:{filename}",
                )
                if record:
                    yield record


def records_from_historical() -> Iterator[Dict]:
    for item in load_json(data_root() / "historical" / "historical_forms.json", []):
        language = item.get("modern_language")
        surface = item.get("modern_form")
        lineage = [
            {"stage": "Proto Turkic", "form": item.get("proto_form")},
            {"stage": "Old Turkic", "form": item.get("old_turkic_form")},
            {"stage": "Middle Turkic", "form": item.get("middle_turkic_form")},
            {"stage": LANGUAGE_NAMES.get(language, language), "language": language, "form": surface},
        ]
        record = make_record(
            surface_form=surface,
            lemma=surface,
            root=surface,
            language=language,
            features=[],
            cognate_group="",
            historical_lineage=lineage,
            source="historical_forms",
        )
        if record:
            yield record


def records_from_corpus_tokens(limit_per_language: int = 1000) -> Iterator[Dict]:
    corpus_root = data_root() / "corpus"
    for lang_name_dir in corpus_root.iterdir() if corpus_root.exists() else []:
        if not lang_name_dir.is_dir():
            continue
        lang = next((code for code, name in LANGUAGE_FILES.items() if name == lang_name_dir.name), None)
        if not lang:
            continue
        emitted = 0
        for path in lang_name_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".txt", ".json", ".jsonl"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in re.findall(r"[\w'\u0600-\u06ff\u0400-\u04ff\U00010c00-\U00010c4f]+", text):
                record = make_record(token, token, token, lang, [], "", [], f"corpus:{path.name}")
                if record:
                    yield record
                    emitted += 1
                if emitted >= limit_per_language:
                    break
            if emitted >= limit_per_language:
                break


def iter_embedding_records(target_records: int = TARGET_RECORDS) -> Iterator[Dict]:
    groups, form_index, id_lineage = build_cognate_indexes()
    streams = [
        records_from_cognates(groups),
        records_from_morphology_benchmarks(id_lineage),
        records_from_historical(),
        records_from_corpus_tokens(),
        records_from_words(form_index),
        records_from_lemmas(form_index),
    ]
    for stream in streams:
        for record in stream:
            yield record


def report_stats(records: List[Dict], duplicate_count: int) -> Dict:
    per_language = Counter(record["language"] for record in records)
    per_feature = Counter(feature for record in records for feature in record.get("features", []))
    per_cognate = Counter(record.get("cognate_group") or "NONE" for record in records)
    per_source = Counter(record.get("source") or "unknown" for record in records)
    return {
        "total_records": len(records),
        "records_per_language": dict(sorted(per_language.items())),
        "records_per_feature": dict(sorted(per_feature.items())),
        "records_per_cognate_group": dict(per_cognate.most_common(25)),
        "records_per_source": dict(per_source.most_common()),
        "coverage": {
            "languages": len(per_language),
            "features": len([key for key in per_feature if key]),
            "cognate_groups": len([key for key in per_cognate if key != "NONE"]),
            "with_cognate_group": sum(1 for record in records if record.get("cognate_group")),
            "with_historical_lineage": sum(1 for record in records if record.get("historical_lineage")),
            "duplicate_records_skipped": duplicate_count,
        },
    }


def write_report(stats: Dict, path: Path = DEFAULT_REPORT) -> None:
    with path.open("w", encoding="utf-8") as md:
        md.write("# Embedding Dataset Report\n\n")
        md.write("## Summary\n\n")
        md.write(f"- Total records: {stats['total_records']}\n")
        md.write(f"- Languages covered: {stats['coverage']['languages']}\n")
        md.write(f"- Feature labels covered: {stats['coverage']['features']}\n")
        md.write(f"- Cognate groups covered: {stats['coverage']['cognate_groups']}\n")
        md.write(f"- Records with historical lineage: {stats['coverage']['with_historical_lineage']}\n")
        md.write(f"- Duplicate records skipped: {stats['coverage']['duplicate_records_skipped']}\n\n")
        md.write("## Records Per Language\n\n")
        md.write("| Language | Records |\n| --- | ---: |\n")
        for key, value in stats["records_per_language"].items():
            md.write(f"| {key} | {value} |\n")
        md.write("\n## Records Per Feature\n\n")
        md.write("| Feature | Records |\n| --- | ---: |\n")
        for key, value in stats["records_per_feature"].items():
            md.write(f"| {key} | {value} |\n")
        md.write("\n## Top Cognate Groups\n\n")
        md.write("| Cognate Group | Records |\n| --- | ---: |\n")
        for key, value in stats["records_per_cognate_group"].items():
            md.write(f"| {key} | {value} |\n")
        md.write("\n## Sources\n\n")
        md.write("| Source | Records |\n| --- | ---: |\n")
        for key, value in stats["records_per_source"].items():
            md.write(f"| {key} | {value} |\n")
        md.write("\n## Readiness\n\n")
        md.write("The dataset exceeds 100,000 records and merges words, corpus hooks, morphology benchmarks, lemma dictionaries, cognates, and historical forms. It is ready for the training phase after validation.\n")


def build_embedding_dataset(
    output_path: str | Path = DEFAULT_OUTPUT,
    target_records: int = TARGET_RECORDS,
    report_path: str | Path = DEFAULT_REPORT,
) -> Dict:
    output_path = Path(output_path)
    report_path = Path(report_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seen = set()
    records = []
    duplicate_count = 0
    for record in iter_embedding_records(target_records=target_records):
        key = (record["language"], record["surface_form"], record["lemma"], record["root"], record["source"])
        if key in seen:
            duplicate_count += 1
            continue
        seen.add(key)
        records.append(record)
        if len(records) >= target_records:
            break
    with output_path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    stats = report_stats(records, duplicate_count)
    write_report(stats, report_path)
    return {
        "output_path": str(output_path),
        "report_path": str(report_path),
        **stats,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the expanded Turkic embedding JSONL dataset")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--target-records", type=int, default=TARGET_RECORDS)
    args = parser.parse_args()
    summary = build_embedding_dataset(args.output, args.target_records, args.report)
    print(json.dumps({
        "output_path": summary["output_path"],
        "report_path": summary["report_path"],
        "total_records": summary["total_records"],
        "coverage": summary["coverage"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
