from django.contrib import admin
from .models import CorpusSource, CorpusDocument, CorpusSentence, CorpusToken


@admin.register(CorpusSource)
class CorpusSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(CorpusDocument)
class CorpusDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'language', 'title', 'imported_at')
    search_fields = ('title', 'raw_text')
    list_filter = ('language',)


@admin.register(CorpusSentence)
class CorpusSentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'order')
    search_fields = ('text',)


@admin.register(CorpusToken)
class CorpusTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sentence')
    search_fields = ('text',)
