from rest_framework import serializers

from .models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "native_name",
            "code",
            "iso639_3",
            "family",
            "branch",
            "writing_system",
            "speakers_count",
            "country",
            "description",
            "flag_url",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class LanguageWriteSerializer(LanguageSerializer):
    class Meta(LanguageSerializer.Meta):
        read_only_fields = ("id", "created_at", "updated_at")
