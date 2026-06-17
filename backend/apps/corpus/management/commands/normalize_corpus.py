from django.core.management.base import BaseCommand
from apps.corpus.services.normalization import normalize_text
from apps.corpus.models import CorpusDocument, CorpusSentence


class Command(BaseCommand):
    help = 'Normalize corpus document texts and update sentence normalized fields'

    def handle(self, *args, **options):
        docs = CorpusDocument.objects.all()
        updated_docs = 0
        for d in docs:
            norm = normalize_text(d.raw_text, language=d.language)
            if norm != d.raw_text:
                d.raw_text = norm
                d.save()
                updated_docs += 1
        # Update sentences' normalized field if present
        for s in CorpusSentence.objects.all():
            s.normalized = normalize_text(s.text, language=s.document.language)
            s.save()
        self.stdout.write(self.style.SUCCESS(f'Normalized {updated_docs} documents and updated sentences.'))
