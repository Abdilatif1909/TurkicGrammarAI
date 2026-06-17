from django.contrib import admin
from .models import CognateSet, CognateEntry


@admin.register(CognateSet)
class CognateSetAdmin(admin.ModelAdmin):
    list_display = ('proto_form', 'gloss', 'confidence_score', 'created_at')
    search_fields = ('proto_form', 'gloss')


@admin.register(CognateEntry)
class CognateEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'word', 'cognate_set', 'confidence_score')
    search_fields = ('word', 'lemma', 'meaning')
    list_filter = ('language',)
