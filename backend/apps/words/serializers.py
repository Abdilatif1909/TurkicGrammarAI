from rest_framework import serializers

from apps.languages.serializers import LanguageSerializer

from .models import Word


class WordSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)
    language_id = serializers.UUIDField(source="language.id", read_only=True)
    language_code = serializers.CharField(source="language.code", read_only=True)

    class Meta:
        model = Word
        fields = (
            "id",
            "language",
            "language_id",
            "language_code",
            "word",
            "lemma",
            "root",
            "pos",
            "ipa",
            "meaning",
            "frequency",
            "source",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class WordWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = (
            "id",
            "language",
            "word",
            "lemma",
            "root",
            "pos",
            "ipa",
            "meaning",
            "frequency",
            "source",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
