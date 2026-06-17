from django.core.management.base import BaseCommand
from apps.corpus.services.tokenization import tokenize_text
from apps.corpus.models import CorpusSentence, CorpusToken


class Command(BaseCommand):
    help = 'Tokenize CorpusSentence texts and create CorpusToken records'

    def handle(self, *args, **options):
        created = 0
        for s in CorpusSentence.objects.all():
            toks = tokenize_text(s.normalized or s.text)
            # delete existing tokens
            CorpusToken.objects.filter(sentence=s).delete()
            for i, t in enumerate(toks, start=1):
                CorpusToken.objects.create(sentence=s, order=i, text=t, norm=t.lower())
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created} tokens.'))
