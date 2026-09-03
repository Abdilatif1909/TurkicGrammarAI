"""Normalization and manifest generation for raw lexeme records."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any
import re
import unicodedata

try:
    from .loader import RawLexeme
    from .schema import LexicalEntry
except ImportError:  # pragma: no cover - supports direct script execution
    from loader import RawLexeme
    from schema import LexicalEntry


WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(value: Any) -> str | None:
    """NFC-normalize text, collapse whitespace, and convert empty strings to None."""

    if value is None:
        return None
    text = unicodedata.normalize("NFC", str(value))
    text = WHITESPACE_RE.sub(" ", text).strip()
    return text or None


def normalize_raw_lexeme(record: RawLexeme) -> LexicalEntry:
    surface_form = normalize_text(record.surface_form)
    if surface_form is None:
        raise ValueError(f"{record.source_file}: surface form cannot be empty")

    language = normalize_text(record.language)
    if language is None:
        raise ValueError(f"{record.source_file}: language cannot be empty")

    pos = normalize_text(record.pos)
    if pos is None:
        raise ValueError(f"{record.source_file}: pos cannot be empty")

    lemma = normalize_text(record.lemma)
    root = normalize_text(record.root)
    semantic_description = normalize_text(record.meaning)
    ipa = normalize_text(record.ipa)
    source = normalize_text(record.source)
    notes = normalize_text(record.notes)

    lemma_inferred = lemma is None
    root_inferred = root is None
    if lemma_inferred:
        lemma = surface_form
    if root_inferred:
        root = surface_form

    is_historical = language == "old_turkic"
    source_metadata: dict[str, Any] = {
        "source": source,
        "notes": notes,
        "ipa": ipa,
        "frequency": record.frequency,
        "source_file": record.source_file,
        "lemma_inferred": lemma_inferred,
        "root_inferred": root_inferred,
        "is_historical": is_historical,
    }

    historical_lineage_metadata = {"is_historical": True} if is_historical else None

    return LexicalEntry(
        surface_form=surface_form,
        language=language,
        lemma=lemma,
        root=root,
        pos=pos,
        semantic_description=semantic_description,
        source_metadata=source_metadata,
        historical_lineage_metadata=historical_lineage_metadata,
    )


def normalize_lexicon(records: list[RawLexeme]) -> list[LexicalEntry]:
    return [normalize_raw_lexeme(record) for record in records]


def find_language_surface_duplicates(
    entries: list[LexicalEntry],
) -> dict[str, list[dict[str, Any]]]:
    """Find duplicates after normalization for each (language, surface_form)."""

    grouped: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, entry in enumerate(entries):
        grouped[(entry.language, entry.surface_form)].append(index)

    duplicates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (language, surface_form), indexes in grouped.items():
        if len(indexes) > 1:
            duplicates[language].append(
                {
                    "surface_form": surface_form,
                    "count": len(indexes),
                    "record_indexes": indexes,
                }
            )
    return {language: rows for language, rows in sorted(duplicates.items())}


def cross_language_surface_stats(entries: list[LexicalEntry]) -> dict[str, Any]:
    surface_languages: dict[str, set[str]] = defaultdict(set)
    for entry in entries:
        surface_languages[entry.surface_form].add(entry.language)

    shared_counts = Counter(len(languages) for languages in surface_languages.values())
    shared_forms = {
        surface: sorted(languages)
        for surface, languages in surface_languages.items()
        if len(languages) >= 2
    }

    return {
        "surface_forms_in_2_plus_languages": sum(
            count for language_count, count in shared_counts.items() if language_count >= 2
        ),
        "surface_forms_in_3_plus_languages": sum(
            count for language_count, count in shared_counts.items() if language_count >= 3
        ),
        "distribution_by_language_count": {
            str(language_count): count
            for language_count, count in sorted(shared_counts.items())
        },
        "shared_surface_forms": dict(sorted(shared_forms.items())),
    }


def build_dataset_manifest(entries: list[LexicalEntry]) -> dict[str, Any]:
    by_language: dict[str, list[LexicalEntry]] = defaultdict(list)
    for entry in entries:
        by_language[entry.language].append(entry)

    def unique_non_null(values: list[str | None]) -> int:
        return len({value for value in values if value is not None})

    languages: dict[str, Any] = {}
    pos_total: Counter[str] = Counter()
    lemma_inferred_total = 0
    root_inferred_total = 0

    for language, language_entries in sorted(by_language.items()):
        pos_counts = Counter(entry.pos for entry in language_entries)
        pos_total.update(pos_counts)
        lemma_inferred = sum(
            1 for entry in language_entries if entry.source_metadata["lemma_inferred"]
        )
        root_inferred = sum(
            1 for entry in language_entries if entry.source_metadata["root_inferred"]
        )
        lemma_inferred_total += lemma_inferred
        root_inferred_total += root_inferred

        languages[language] = {
            "records": len(language_entries),
            "unique_surface_forms": unique_non_null(
                [entry.surface_form for entry in language_entries]
            ),
            "unique_lemmas_with_fallback": unique_non_null(
                [entry.lemma for entry in language_entries]
            ),
            "unique_lemmas_without_fallback": unique_non_null(
                [
                    None if entry.source_metadata["lemma_inferred"] else entry.lemma
                    for entry in language_entries
                ]
            ),
            "unique_roots_with_fallback": unique_non_null(
                [entry.root for entry in language_entries]
            ),
            "unique_roots_without_fallback": unique_non_null(
                [
                    None if entry.source_metadata["root_inferred"] else entry.root
                    for entry in language_entries
                ]
            ),
            "pos_distribution": dict(sorted(pos_counts.items())),
            "lemma_inferred_records": lemma_inferred,
            "root_inferred_records": root_inferred,
        }

    duplicates = find_language_surface_duplicates(entries)

    return {
        "total_records": len(entries),
        "languages": languages,
        "totals": {
            "unique_surface_forms": unique_non_null(
                [entry.surface_form for entry in entries]
            ),
            "unique_lemmas_with_fallback": unique_non_null(
                [entry.lemma for entry in entries]
            ),
            "unique_lemmas_without_fallback": unique_non_null(
                [
                    None if entry.source_metadata["lemma_inferred"] else entry.lemma
                    for entry in entries
                ]
            ),
            "unique_roots_with_fallback": unique_non_null(
                [entry.root for entry in entries]
            ),
            "unique_roots_without_fallback": unique_non_null(
                [
                    None if entry.source_metadata["root_inferred"] else entry.root
                    for entry in entries
                ]
            ),
            "pos_distribution": dict(sorted(pos_total.items())),
            "lemma_inferred_records": lemma_inferred_total,
            "root_inferred_records": root_inferred_total,
            "language_surface_duplicate_pairs": sum(
                len(rows) for rows in duplicates.values()
            ),
        },
        "duplicates_after_normalization": duplicates,
        "cross_language_surface_form_statistics": cross_language_surface_stats(entries),
    }
