from rest_framework import serializers
from .models import HistoricalForm, HistoricalRelation


class HistoricalFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalForm
        fields = '__all__'


class HistoricalRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalRelation
        fields = '__all__'
