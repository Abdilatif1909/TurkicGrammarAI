from django.contrib import admin

from apps.analytics.models import QaErrorLog, UsageEvent, UserFeedback


@admin.register(UsageEvent)
class UsageEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "query", "language", "status_code", "response_time_ms", "created_at")
    list_filter = ("event_type", "language", "status_code", "created_at")
    search_fields = ("query", "path", "user_agent")
    readonly_fields = ("created_at",)


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ("rating", "question", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("question", "answer", "comment")
    readonly_fields = ("created_at",)


@admin.register(QaErrorLog)
class QaErrorLogAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at")
    search_fields = ("question", "answer")
    readonly_fields = ("created_at",)
