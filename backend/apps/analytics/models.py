from django.conf import settings
from django.db import models


class UsageEvent(models.Model):
    SEARCH = "search"
    QA = "qa"
    MORPHOLOGY = "morphology"
    COGNATE = "cognate"
    HISTORICAL = "historical"
    RAG = "rag"
    OTHER = "other"

    EVENT_TYPES = [
        (SEARCH, "Search query"),
        (QA, "QA question"),
        (MORPHOLOGY, "Morphology request"),
        (COGNATE, "Cognate lookup"),
        (HISTORICAL, "Historical lookup"),
        (RAG, "RAG retrieval"),
        (OTHER, "Other"),
    ]

    event_type = models.CharField(max_length=32, choices=EVENT_TYPES, db_index=True)
    query = models.TextField(blank=True)
    language = models.CharField(max_length=16, blank=True, db_index=True)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=12, blank=True)
    status_code = models.PositiveIntegerField(default=0)
    response_time_ms = models.FloatField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["language", "created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type}: {self.query[:80]}"


class UserFeedback(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"rating={self.rating} {self.question[:80]}"


class QaErrorLog(models.Model):
    question = models.TextField()
    retrieved_sources = models.JSONField(default=list, blank=True)
    answer = models.TextField(blank=True)
    user_feedback = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:80]
