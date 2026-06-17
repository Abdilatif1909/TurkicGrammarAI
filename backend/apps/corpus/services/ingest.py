import json
import csv
import os
from xml.etree import ElementTree as ET
from django.conf import settings
from apps.corpus.models import CorpusSource, CorpusDocument


class CorpusIngestor:
    """Simple ingestion helper for TXT/JSON/CSV/XML files into CorpusDocument."""

    def __init__(self, source_name='user_upload', metadata=None):
        self.source, _ = CorpusSource.objects.get_or_create(name=source_name, defaults={'metadata': metadata or {}})

    def ingest_txt(self, file_path, language='und', title=None):
        with open(file_path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        doc = CorpusDocument.objects.create(source=self.source, language=language, title=title or os.path.basename(file_path), raw_text=text)
        return doc

    def ingest_json(self, file_path, language='und'):
        with open(file_path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        # Expect either {"text": "..."} or list of documents
        if isinstance(data, dict) and 'text' in data:
            return self._create_from_text(data['text'], language, data.get('title'))
        docs = []
        for item in data if isinstance(data, list) else [data]:
            text = item.get('text') or item.get('content')
            if text:
                docs.append(self._create_from_text(text, language, item.get('title')))
        return docs

    def ingest_csv(self, file_path, text_column='text', language='und'):
        docs = []
        with open(file_path, 'r', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                text = row.get(text_column)
                if text:
                    docs.append(self._create_from_text(text, language, row.get('title')))
        return docs

    def ingest_xml(self, file_path, xpath='//text', language='und'):
        tree = ET.parse(file_path)
        root = tree.getroot()
        texts = [elem.text for elem in root.findall(xpath) if elem.text]
        docs = []
        for t in texts:
            docs.append(self._create_from_text(t, language))
        return docs

    def _create_from_text(self, text, language, title=None):
        return CorpusDocument.objects.create(source=self.source, language=language, title=title or '', raw_text=text)
