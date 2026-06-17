from rest_framework import serializers
from apps.corpus.models import CorpusDocument, CorpusSentence, CorpusToken


class CorpusDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusDocument
        fields = ['id', 'source', 'language', 'title', 'imported_at']


class CorpusSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusSentence
        fields = ['id', 'document', 'order', 'text']


class CorpusTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpusToken
        fields = ['id', 'sentence', 'order', 'text', 'norm']
