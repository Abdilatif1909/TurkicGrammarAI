from django.db import models


class HistoricalForm(models.Model):
    proto_form = models.CharField(max_length=200, blank=True, null=True)
    old_turkic_form = models.TextField(blank=True, null=True)
    middle_turkic_form = models.CharField(max_length=200, blank=True, null=True)
    modern_language = models.CharField(max_length=16)
    modern_form = models.CharField(max_length=200)
    ipa = models.CharField(max_length=200, blank=True, null=True)
    gloss = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    confidence_score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.modern_language}:{self.modern_form}"


class HistoricalRelation(models.Model):
    SOUND_CHANGE = "SOUND_CHANGE"
    MORPHOLOGICAL_CHANGE = "MORPHOLOGICAL_CHANGE"
    SEMANTIC_CHANGE = "SEMANTIC_CHANGE"
    ORTHOGRAPHIC_CHANGE = "ORTHOGRAPHIC_CHANGE"

    RELATION_CHOICES = [
        (SOUND_CHANGE, "Sound change"),
        (MORPHOLOGICAL_CHANGE, "Morphological change"),
        (SEMANTIC_CHANGE, "Semantic change"),
        (ORTHOGRAPHIC_CHANGE, "Orthographic change"),
    ]

    parent_form = models.ForeignKey(HistoricalForm, on_delete=models.CASCADE, related_name="children")
    child_form = models.ForeignKey(HistoricalForm, on_delete=models.CASCADE, related_name="parents")
    relation_type = models.CharField(max_length=32, choices=RELATION_CHOICES)
    description = models.TextField(blank=True, null=True)
    confidence_score = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.relation_type}: {self.parent_form} -> {self.child_form}"
