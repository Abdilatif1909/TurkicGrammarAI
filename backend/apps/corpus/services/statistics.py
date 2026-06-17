from apps.corpus.models import CorpusDocument, CorpusSentence, CorpusToken


class CorpusStatistics:
    @staticmethod
    def summary():
        docs = CorpusDocument.objects.count()
        sents = CorpusSentence.objects.count()
        toks = CorpusToken.objects.count()
        langs = list(CorpusDocument.objects.values('language').distinct())
        lang_counts = {l['language']: CorpusDocument.objects.filter(language=l['language']).count() for l in langs}
        return {
            'documents': docs,
            'sentences': sents,
            'tokens': toks,
            'languages': lang_counts,
        }
