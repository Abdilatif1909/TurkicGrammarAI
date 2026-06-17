from pathlib import Path

from django.conf import settings
from django.db import transaction

from apps.core.seeding.base_seeder import BaseSeeder
from apps.languages.models import Language
from apps.languages.services.language_service import LanguageService


class LanguageImportService(BaseSeeder):
    default_path = settings.BASE_DIR / "data" / "languages" / "languages.json"

    required_fields = {
        "name",
        "native_name",
        "code",
        "iso639_3",
        "family",
        "branch",
        "writing_system",
        "speakers_count",
        "country",
        "description",
        "flag_url",
    }

    def __init__(self, path: str | Path | None = None):
        super().__init__(path)

    def run(self) -> dict[str, int]:
        records = self.load()
        created = 0
        skipped = 0
        existing_codes = set(Language.objects.values_list("code", flat=True))
        objects = []

        for record in records:
            missing = self.required_fields - set(record)
            if missing:
                raise ValueError(f"Language record is missing fields: {', '.join(sorted(missing))}")
            if record["code"] in existing_codes:
                skipped += 1
                continue
            objects.append(Language(**record))
            existing_codes.add(record["code"])

        with transaction.atomic():
            if objects:
                Language.objects.bulk_create(objects)
                created = len(objects)

        if created:
            LanguageService.clear_cache()

        return {"created": created, "skipped": skipped, "total": len(records)}
