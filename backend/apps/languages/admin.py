from django.contrib import admin

from .models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "iso639_3", "family", "branch", "country", "is_active")
    list_filter = ("family", "branch", "country", "is_active")
    search_fields = ("name", "native_name", "code", "iso639_3", "country")
    ordering = ("name",)
