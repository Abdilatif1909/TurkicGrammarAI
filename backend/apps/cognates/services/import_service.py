import json
from pathlib import Path
from django.db import transaction
from apps.cognates.models import CognateSet, CognateEntry


class CognateImportService:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def seed_from_file(self, filename: str, batch_size: int = 500):
        path = self.data_path / filename
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open('r', encoding='utf-8') as fh:
            data = json.load(fh)

        created_sets = 0
        created_entries = 0
        with transaction.atomic():
            for group in data:
                proto = group.get('proto_form')
                gloss = group.get('gloss', '')
                confidence = float(group.get('confidence_score', 0.0) or 0.0)
                cs, created = CognateSet.objects.get_or_create(proto_form=proto, defaults={'gloss': gloss, 'confidence_score': confidence})
                if created:
                    created_sets += 1
                entries = []
                for e in group.get('entries', []):
                    # deduplicate by set + language + word
                    if CognateEntry.objects.filter(cognate_set=cs, language=e.get('language'), word=e.get('word')).exists():
                        continue
                    entries.append(CognateEntry(
                        cognate_set=cs,
                        language=e.get('language'),
                        word=e.get('word'),
                        lemma=e.get('lemma', ''),
                        ipa=e.get('ipa', ''),
                        meaning=e.get('meaning', ''),
                        source=e.get('source', ''),
                        confidence_score=float(e.get('confidence_score', 0.0) or 0.0)
                    ))
                if entries:
                    CognateEntry.objects.bulk_create(entries)
                    created_entries += len(entries)
        return {'created_sets': created_sets, 'created_entries': created_entries}
