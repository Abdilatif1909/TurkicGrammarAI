from django.db import models
from django.utils import timezone


class MorphologicalRule(models.Model):
    language = models.CharField(max_length=8)
    suffix = models.CharField(max_length=64)
    suffix_type = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    examples = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(default=1.0)

    class Meta:
        unique_together = ("language", "suffix", "suffix_type")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.language}:{self.suffix} ({self.suffix_type})"


class MorphologicalAnalysis(models.Model):
    language = models.CharField(max_length=8)
    surface_form = models.CharField(max_length=256)
    root = models.CharField(max_length=256)
    lemma = models.CharField(max_length=256)
    suffix_chain = models.JSONField(default=list)
    analysis_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.surface_form} -> {self.root} + {self.suffix_chain}"
