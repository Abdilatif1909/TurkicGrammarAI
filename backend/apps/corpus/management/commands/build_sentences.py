from django.core.management.base import BaseCommand
from apps.corpus.services.segmentation import segment_sentences
from apps.corpus.models import CorpusDocument, CorpusSentence


class Command(BaseCommand):
    help = 'Build CorpusSentence records by segmenting documents'

    def handle(self, *args, **options):
        created = 0
        for doc in CorpusDocument.objects.all():
            sents = segment_sentences(doc.raw_text)
            # delete existing sentences for document
            CorpusSentence.objects.filter(document=doc).delete()
            for i, s in enumerate(sents, start=1):
                CorpusSentence.objects.create(document=doc, order=i, text=s)
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} sentences.'))
