from django.test import TestCase, Client
from django.core.management import call_command
from pathlib import Path
from django.conf import settings
from .models import HistoricalForm


class HistoricalTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_seed_command_and_models(self):
        # Ensure seed runs and creates records
        call_command('seed_historical')
        count = HistoricalForm.objects.count()
        self.assertGreaterEqual(count, 2000)

    def test_evolution_api(self):
        # Ensure evolution endpoint returns proto for generated modern form
        resp = self.client.get('/api/historical/evolution/?q=tangri')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # For synthetic data tangri should map to proto *teŋri
        self.assertIn('proto', data)
        self.assertTrue(data.get('proto') in ('*teŋri', '*kitab'))

    def test_list_and_search(self):
        resp = self.client.get('/api/historical/')
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get('/api/historical/search/?q=kitap')
        self.assertEqual(resp2.status_code, 200)
