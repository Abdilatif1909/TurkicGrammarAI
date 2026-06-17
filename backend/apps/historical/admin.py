from django.contrib import admin
from .models import HistoricalForm, HistoricalRelation


@admin.register(HistoricalForm)
class HistoricalFormAdmin(admin.ModelAdmin):
    list_display = ("id", "modern_language", "modern_form", "proto_form", "confidence_score")
    search_fields = ("modern_form", "proto_form", "middle_turkic_form")


@admin.register(HistoricalRelation)
class HistoricalRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "relation_type", "parent_form", "child_form", "confidence_score")
    list_filter = ("relation_type",)
