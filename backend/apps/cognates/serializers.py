from rest_framework import serializers
from apps.cognates.models import CognateSet, CognateEntry


class CognateEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CognateEntry
        fields = ['id', 'language', 'word', 'lemma', 'ipa', 'meaning', 'source', 'confidence_score']


class CognateSetSerializer(serializers.ModelSerializer):
    entries = CognateEntrySerializer(many=True, read_only=True)

    class Meta:
        model = CognateSet
        fields = ['id', 'proto_form', 'gloss', 'notes', 'confidence_score', 'created_at', 'updated_at', 'entries']
