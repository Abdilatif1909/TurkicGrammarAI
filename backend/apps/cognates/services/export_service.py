import csv
import json
from io import StringIO
from typing import Iterable
from apps.cognates.models import CognateSet


class CognateExportService:
    @staticmethod
    def export_json(queryset: Iterable[object]):
        data = []
        for cs in queryset:
            entries = list(cs.entries.values('language', 'word', 'lemma', 'ipa', 'meaning', 'source', 'confidence_score'))
            data.append({'proto_form': cs.proto_form, 'gloss': cs.gloss, 'confidence_score': cs.confidence_score, 'entries': entries})
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def export_csv(queryset: Iterable[object]):
        out = StringIO()
        writer = csv.writer(out)
        writer.writerow(['proto_form', 'gloss', 'cognate_language', 'word', 'lemma', 'ipa', 'meaning', 'source', 'entry_confidence'])
        for cs in queryset:
            for e in cs.entries.all():
                writer.writerow([cs.proto_form, cs.gloss, e.language, e.word, e.lemma, e.ipa, e.meaning, e.source, e.confidence_score])
        return out.getvalue()
