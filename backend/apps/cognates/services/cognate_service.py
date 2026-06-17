from typing import Dict, List
from django.db.models import Q
from apps.cognates.models import CognateSet, CognateEntry


class CognateService:
    @staticmethod
    def get_statistics() -> Dict:
        total_sets = CognateSet.objects.count()
        total_entries = CognateEntry.objects.count()
        languages = list(CognateEntry.objects.values_list('language', flat=True).distinct())
        lang_counts = {lang: CognateEntry.objects.filter(language=lang).count() for lang in languages}
        return {'cognate_sets': total_sets, 'entries': total_entries, 'languages': lang_counts}

    @staticmethod
    def comparative_search(word: str = None, language: str = None) -> List[Dict]:
        """Find cognate groups that match the given word (and optional language).

        Returns list of dicts: {proto_form, cognates: [{language, word}, ...]}
        """
        if not word:
            return []
        qs = CognateEntry.objects.filter(word__iexact=word)
        if language:
            qs = qs.filter(language__iexact=language)
        results = []
        seen = set()
        for entry in qs.select_related('cognate_set'):
            cs = entry.cognate_set
            if cs.id in seen:
                continue
            seen.add(cs.id)
            entries = cs.entries.all()
            cognates = [{'language': e.language, 'word': e.word} for e in entries]
            results.append({'proto_form': cs.proto_form, 'cognates': cognates})
        return results
