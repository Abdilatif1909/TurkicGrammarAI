"""Dynamic loaders for TurkicGrammarAI raw word lists."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RAW_FILE_SUFFIX = "_words.json"


@dataclass(frozen=True)
class RawLexeme:
    """Normalized in-memory representation of one raw lexeme record."""

    surface_form: str
    language: str
    lemma: str
    root: str
    pos: str
    ipa: str
    meaning: str
    frequency: int
    source: str
    notes: str
    source_file: str

    @classmethod
    def from_raw(
        cls,
        record: dict[str, Any],
        *,
        language: str,
        source_file: str,
    ) -> "RawLexeme":
        required_fields = (
            "word",
            "lemma",
            "root",
            "pos",
            "ipa",
            "meaning",
            "frequency",
            "source",
            "notes",
        )
        missing = [
            field
            for field in required_fields
            if field not in record or record[field] in (None, "")
        ]
        if missing:
            joined = ", ".join(missing)
            raise ValueError(f"{source_file}: missing required fields: {joined}")

        return cls(
            surface_form=str(record["word"]),
            language=language,
            lemma=str(record["lemma"]),
            root=str(record["root"]),
            pos=str(record["pos"]),
            ipa=str(record["ipa"]),
            meaning=str(record["meaning"]),
            frequency=int(record["frequency"]),
            source=str(record["source"]),
            notes=str(record["notes"]),
            source_file=source_file,
        )


def detect_language(path: Path) -> str:
    """Infer language from a filename such as azerbaijani_words.json."""

    name = path.name
    if not name.endswith(RAW_FILE_SUFFIX):
        raise ValueError(f"Unsupported raw filename: {name}")
    return name[: -len(RAW_FILE_SUFFIX)]


def discover_word_files(raw_dir: str | Path) -> list[Path]:
    """Return all raw word files from a directory, sorted for repeatability."""

    directory = Path(raw_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Raw data directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Raw data path is not a directory: {directory}")
    return sorted(directory.glob(f"*{RAW_FILE_SUFFIX}"))


def load_language_file(path: str | Path) -> list[RawLexeme]:
    """Load one language file into RawLexeme records."""

    file_path = Path(path)
    language = detect_language(file_path)
    with file_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, list):
        raise ValueError(f"{file_path.name}: expected top-level JSON array")

    records: list[RawLexeme] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ValueError(f"{file_path.name}: record {index} is not an object")
        records.append(
            RawLexeme.from_raw(
                item,
                language=language,
                source_file=file_path.name,
            )
        )
    return records


def load_raw_lexicon(raw_dir: str | Path) -> list[RawLexeme]:
    """Load all available *_words.json files from raw_dir."""

    records: list[RawLexeme] = []
    for path in discover_word_files(raw_dir):
        records.extend(load_language_file(path))
    return records


def count_by_language(records: list[RawLexeme]) -> dict[str, int]:
    """Count loaded records by detected language."""

    counts: dict[str, int] = {}
    for record in records:
        counts[record.language] = counts.get(record.language, 0) + 1
    return dict(sorted(counts.items()))
