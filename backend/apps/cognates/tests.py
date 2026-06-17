from django.test import TestCase
from apps.cognates.models import CognateSet, CognateEntry
from django.core.management import call_command
from django.conf import settings
import os


class CognatesTests(TestCase):
    def setUp(self):
        # create a sample cognate set
        self.cs = CognateSet.objects.create(proto_form='*kitab', gloss='book', confidence_score=0.9)
        CognateEntry.objects.create(cognate_set=self.cs, language='uz', word='kitob')
        CognateEntry.objects.create(cognate_set=self.cs, language='tr', word='kitap')

    def test_comparative_search(self):
        from apps.cognates.services.cognate_service import CognateService
        res = CognateService.comparative_search(word='kitob', language='uz')
        self.assertTrue(len(res) >= 1)
        self.assertEqual(res[0]['proto_form'], '*kitab')

    def test_statistics(self):
        from apps.cognates.services.cognate_service import CognateService
        stats = CognateService.get_statistics()
        self.assertIn('cognate_sets', stats)
        self.assertIn('entries', stats)

    def test_seed_command(self):
        # create a small sample JSON file and run seed
        path = os.path.join('backend', 'data', 'cognates')
        os.makedirs(path, exist_ok=True)
        sample_file = os.path.join(path, 'sample_seed.json')
        data = [
            {'proto_form': '*testproto', 'gloss': 'test', 'entries': [
                {'language': 'uz', 'word': 'testuz'},
                {'language': 'tr', 'word': 'testtr'}
            ]}
        ]
        import json
        with open(sample_file, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False)
        call_command('seed_cognates', '--path', os.path.join('backend', 'data', 'cognates'), '--file', 'sample_seed.json')
        self.assertTrue(CognateSet.objects.filter(proto_form='*testproto').exists())
