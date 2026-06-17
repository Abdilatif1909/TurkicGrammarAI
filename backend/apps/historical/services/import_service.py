import json
from django.db import transaction
from ..models import HistoricalForm
from pathlib import Path


class ImportService:
    @staticmethod
    def load_from_file(path: str | Path):
        p = Path(path)
        with p.open('r', encoding='utf-8') as fh:
            data = json.load(fh)
        return data

    @staticmethod
    def seed_from_list(records: list[dict]):
        created = 0
        to_create = []
        seen = set()
        # No-op diagnostics removed for production; keep dedupe logic
        for r in records:
            key = (r.get('proto_form'), r.get('modern_form'), r.get('modern_language'))
            if key in seen:
                continue
            seen.add(key)
            # (Skip DB-level existence check to allow bulk insert of generated dataset)
            to_create.append(HistoricalForm(
                proto_form=r.get('proto_form'),
                old_turkic_form=r.get('old_turkic_form'),
                middle_turkic_form=r.get('middle_turkic_form'),
                modern_language=r.get('modern_language') or 'und',
                modern_form=r.get('modern_form') or '',
                ipa=r.get('ipa'),
                gloss=r.get('gloss'),
                notes=r.get('notes'),
                source=r.get('source'),
                confidence_score=float(r.get('confidence_score') or 1.0)
            ))
        # Bulk insert in batches to avoid SQLite/DB parameter limits
        try:
            with transaction.atomic():
                batch_size = 200
                HistoricalForm.objects.bulk_create(to_create, batch_size=batch_size)
                created = len(to_create)
        except Exception:
            # Try per-object save as fallback
            created = 0
            with transaction.atomic():
                for obj in to_create:
                    obj.save()
                    created += 1
        return created
