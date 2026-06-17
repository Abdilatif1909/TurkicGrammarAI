from django.test import TestCase
from apps.corpus.models import CorpusSource, CorpusDocument, CorpusSentence, CorpusToken
from apps.corpus.services.normalization import normalize_text
from apps.corpus.services.segmentation import segment_sentences
from apps.corpus.services.tokenization import tokenize_text


class CorpusBasicTests(TestCase):
    def setUp(self):
        self.src = CorpusSource.objects.create(name='test_source')
        self.doc = CorpusDocument.objects.create(source=self.src, language='uz', title='t1', raw_text='Salom dunyo. Bu test.')

    def test_normalize(self):
        s = '  Hello\n\nWorld!! '
        n = normalize_text(s)
        self.assertIn('Hello', n)

    def test_segmentation(self):
        sents = segment_sentences(self.doc.raw_text)
        self.assertEqual(len(sents), 2)

    def test_tokenization(self):
        toks = tokenize_text('Bu bir test.')
        self.assertIn('Bu', toks)

    def test_sentence_and_token_building(self):
        # Build sentences
        sents = segment_sentences(self.doc.raw_text)
        for i, s in enumerate(sents, start=1):
            CorpusSentence.objects.create(document=self.doc, order=i, text=s)
        self.assertEqual(CorpusSentence.objects.filter(document=self.doc).count(), 2)
        # Build tokens for the first sentence
        sent = CorpusSentence.objects.filter(document=self.doc).first()
        toks = tokenize_text(sent.text)
        for i, t in enumerate(toks, start=1):
            CorpusToken.objects.create(sentence=sent, order=i, text=t, norm=t.lower())
        self.assertTrue(CorpusToken.objects.filter(sentence=sent).count() >= 1)
