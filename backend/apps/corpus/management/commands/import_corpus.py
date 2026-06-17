from django.core.management.base import BaseCommand, CommandError
from apps.corpus.services.ingest import CorpusIngestor
import os


class Command(BaseCommand):
    help = 'Import corpus files from backend/data/corpus/<lang> directories'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, default='user_upload')
        parser.add_argument('--path', type=str, default=os.path.join('backend', 'data', 'corpus'))

    def handle(self, *args, **options):
        path = options['path']
        source = options['source']
        if not os.path.isdir(path):
            raise CommandError(f'Path not found: {path}')
        ing = CorpusIngestor(source_name=source)
        imported = 0
        for lang in os.listdir(path):
            lang_path = os.path.join(path, lang)
            if not os.path.isdir(lang_path):
                continue
            for fn in os.listdir(lang_path):
                full = os.path.join(lang_path, fn)
                if not os.path.isfile(full):
                    continue
                lower = fn.lower()
                try:
                    if lower.endswith('.txt'):
                        ing.ingest_txt(full, language=lang)
                        imported += 1
                    elif lower.endswith('.json'):
                        ing.ingest_json(full, language=lang)
                        imported += 1
                    elif lower.endswith('.csv'):
                        ing.ingest_csv(full, language=lang)
                        imported += 1
                    elif lower.endswith('.xml'):
                        ing.ingest_xml(full, language=lang)
                        imported += 1
                except Exception as e:
                    self.stderr.write(f'Failed to import {full}: {e}')
        self.stdout.write(self.style.SUCCESS(f'Imported {imported} files.'))
