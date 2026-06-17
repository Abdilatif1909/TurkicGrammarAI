from django.db import models

from apps.core.models import BaseModel


class Language(BaseModel):
    name = models.CharField(max_length=120)
    native_name = models.CharField(max_length=120)
    code = models.CharField(max_length=16, unique=True, db_index=True)
    iso639_3 = models.CharField(max_length=3, unique=True)
    family = models.CharField(max_length=120, db_index=True)
    branch = models.CharField(max_length=120, db_index=True)
    writing_system = models.CharField(max_length=255)
    speakers_count = models.PositiveBigIntegerField(default=0)
    country = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    flag_url = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code", "is_active"]),
            models.Index(fields=["family", "branch"]),
            models.Index(fields=["country"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
