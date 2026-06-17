import json
import csv
from pathlib import Path
import time

from django.conf import settings
from django.db import transaction

from apps.languages.models import Language
from apps.words.models import Word
from apps.words.services.word_service import WordService


class WordImportService:
    default_dir = settings.BASE_DIR / "data" / "words"
    batch_size = 5000
    required_fields = {
        "language_code",
        "word",
        "lemma",
        "root",
        "pos",
        "ipa",
        "meaning",
        "frequency",
        "source",
        "notes",
    }

    def __init__(self, path: str | Path | None = None, batch_size: int | None = None):
        self.path = Path(path) if path else self.default_dir
        self.batch_size = batch_size or self.batch_size

    def run(self) -> dict[str, int | float]:
        started = time.perf_counter()
        records = self._load_records()
        language_map = {language.code: language for language in Language.objects.all()}
        existing_keys = self._existing_keys()
        created = 0
        skipped = 0
        pending: list[Word] = []

        with transaction.atomic():
            for record in records:
                self._validate(record)
                language = language_map.get(record["language_code"])
                if language is None:
                    skipped += 1
                    continue

                dedupe_key = self._dedupe_key(language.id, record)
                if dedupe_key in existing_keys:
                    skipped += 1
                    continue

                pending.append(
                    Word(
                        language=language,
                        word=record["word"],
                        lemma=record["lemma"],
                        root=record.get("root", ""),
                        pos=record["pos"],
                        ipa=record.get("ipa", ""),
                        meaning=record["meaning"],
                        frequency=int(record.get("frequency") or 0),
                        source=record.get("source", ""),
                        notes=record.get("notes", ""),
                    )
                )
                existing_keys.add(dedupe_key)

                if len(pending) >= self.batch_size:
                    Word.objects.bulk_create(pending, batch_size=self.batch_size)
                    created += len(pending)
                    pending.clear()

            if pending:
                Word.objects.bulk_create(pending, batch_size=self.batch_size)
                created += len(pending)

        if created:
            WordService.clear_cache()

        elapsed = round(time.perf_counter() - started, 4)
        return {"created": created, "skipped": skipped, "total": len(records), "elapsed_seconds": elapsed}

    def _load_records(self) -> list[dict]:
        if self.path.is_dir():
            records = []
            for file_path in sorted(list(self.path.glob("*.json")) + list(self.path.glob("*.csv"))):
                records.extend(self._load_file(file_path))
            return records
        return self._load_file(self.path)

    def _load_file(self, path: Path) -> list[dict]:
        if not path.exists():
            raise FileNotFoundError(f"Words seed file not found: {path}")
        if path.suffix.lower() == ".csv":
            return self._load_csv(path)
        if path.suffix.lower() == ".json":
            return self._load_json(path)
        raise ValueError("Supported word import formats are JSON and CSV.")

    @staticmethod
    def _load_json(path: Path) -> list[dict]:
        with path.open("r", encoding="utf-8") as words_file:
            data = json.load(words_file)
        if not isinstance(data, list):
            raise ValueError("Words seed file must contain a JSON list.")
        return data

    @staticmethod
    def _load_csv(path: Path) -> list[dict]:
        with path.open("r", encoding="utf-8", newline="") as words_file:
            return list(csv.DictReader(words_file))

    def _validate(self, record: dict) -> None:
        missing = self.required_fields - set(record)
        if missing:
            raise ValueError(f"Word record is missing fields: {', '.join(sorted(missing))}")

    @staticmethod
    def _existing_keys() -> set[tuple]:
        return set(
            Word.objects.values_list(
                "language_id",
                "word",
                "lemma",
                "pos",
                "meaning",
            )
        )

    @staticmethod
    def _dedupe_key(language_id, record: dict) -> tuple:
        return (
            language_id,
            record["word"],
            record["lemma"],
            record["pos"],
            record["meaning"],
        )
