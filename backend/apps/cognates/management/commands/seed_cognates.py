from django.core.management.base import BaseCommand
from django.db import transaction
from apps.cognates.services.import_service import CognateImportService
import os


class Command(BaseCommand):
    help = 'Seed cognates from backend/data/cognates/cognates.json'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default=os.path.join('backend', 'data', 'cognates'))
        parser.add_argument('--file', type=str, default='cognates.json')

    def handle(self, *args, **options):
        path = options['path']
        fname = options['file']
        service = CognateImportService(path)
        with transaction.atomic():
            res = service.seed_from_file(fname)
        self.stdout.write(self.style.SUCCESS(f"Created {res['created_sets']} sets and {res['created_entries']} entries."))
