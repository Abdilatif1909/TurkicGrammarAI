from django.contrib import admin

from .models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "lemma", "language", "pos", "frequency", "source")
    list_filter = ("language", "pos", "source")
    search_fields = ("word", "lemma", "root", "meaning", "ipa")
    raw_id_fields = ("language",)
    ordering = ("language__name", "word")
