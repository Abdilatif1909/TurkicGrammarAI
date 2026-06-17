import uuid
from django.db import models


class CognateSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proto_form = models.CharField(max_length=255, blank=True, db_index=True)
    gloss = models.CharField(max_length=512, blank=True)
    notes = models.TextField(blank=True)
    confidence_score = models.FloatField(default=0.0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-confidence_score', 'proto_form']

    def __str__(self):
        return f"{self.proto_form} ({self.id})"


class CognateEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cognate_set = models.ForeignKey(CognateSet, on_delete=models.CASCADE, related_name='entries')
    language = models.CharField(max_length=16, db_index=True)
    word = models.CharField(max_length=255, db_index=True)
    lemma = models.CharField(max_length=255, blank=True)
    ipa = models.CharField(max_length=255, blank=True)
    meaning = models.CharField(max_length=512, blank=True)
    source = models.CharField(max_length=255, blank=True)
    confidence_score = models.FloatField(default=0.0, db_index=True)

    class Meta:
        indexes = [models.Index(fields=['language', 'word']),]

    def __str__(self):
        return f"{self.language}:{self.word} -> {self.cognate_set.proto_form}"
