from rest_framework import serializers


class ActionResultSerializer(serializers.Serializer):
    success = serializers.BooleanField(required=False)
    detail = serializers.CharField(required=False)
    created = serializers.IntegerField(required=False)
