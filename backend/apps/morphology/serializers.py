from rest_framework import serializers


class SuffixSerializer(serializers.Serializer):
    suffix = serializers.CharField()
    type = serializers.CharField()
    confidence = serializers.FloatField()


class AnalysisSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    surface = serializers.CharField(required=False)
    root = serializers.CharField()
    lemma = serializers.CharField()
    suffixes = serializers.ListField(required=False)
    score = serializers.FloatField()
    confidence = serializers.FloatField(required=False)
    word = serializers.CharField(required=False)
    derivation = serializers.CharField(required=False)
    derivation_type = serializers.CharField(required=False)
    derivation_confidence = serializers.FloatField(required=False)


class MorphologyAnalysesResponseSerializer(serializers.Serializer):
    analyses = AnalysisSerializer(many=True)
