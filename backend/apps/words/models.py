import uuid

from django.db import models

from apps.languages.models import Language


class PartOfSpeech(models.TextChoices):
    NOUN = "NOUN", "Noun"
    VERB = "VERB", "Verb"
    ADJECTIVE = "ADJECTIVE", "Adjective"
    ADVERB = "ADVERB", "Adverb"
    PRONOUN = "PRONOUN", "Pronoun"
    NUMERAL = "NUMERAL", "Numeral"
    POSTPOSITION = "POSTPOSITION", "Postposition"
    CONJUNCTION = "CONJUNCTION", "Conjunction"
    PARTICLE = "PARTICLE", "Particle"
    INTERJECTION = "INTERJECTION", "Interjection"


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="words")
    word = models.CharField(max_length=255)
    lemma = models.CharField(max_length=255)
    root = models.CharField(max_length=255, blank=True)
    pos = models.CharField(max_length=32, choices=PartOfSpeech.choices, db_index=True)
    ipa = models.CharField(max_length=255, blank=True)
    meaning = models.TextField()
    frequency = models.PositiveIntegerField(default=0, db_index=True)
    source = models.CharField(max_length=255, blank=True, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["language__name", "word"]
        indexes = [
            models.Index(fields=["language", "word"], name="words_language_word_idx"),
            models.Index(fields=["language", "lemma"], name="words_language_lemma_idx"),
            models.Index(fields=["language", "pos"], name="words_language_pos_idx"),
            models.Index(fields=["source"], name="words_source_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.word} ({self.language.code})"
