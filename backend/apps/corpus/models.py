import hashlib
import uuid
from django.db import models


class CorpusSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CorpusDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(CorpusSource, on_delete=models.SET_NULL, null=True, related_name='documents')
    language = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=1024, blank=True)
    raw_text = models.TextField()
    checksum = models.CharField(max_length=64, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['language', 'checksum']),]

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.checksum = hashlib.sha256(self.raw_text.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Document {self.id} ({self.language})"


class CorpusSentence(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(CorpusDocument, on_delete=models.CASCADE, related_name='sentences')
    order = models.IntegerField(db_index=True)
    text = models.TextField()
    checksum = models.CharField(max_length=64, db_index=True)
    normalized = models.TextField(blank=True)

    class Meta:
        unique_together = (('document', 'order'),)
        indexes = [models.Index(fields=['checksum']),]

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.checksum = hashlib.sha256(self.text.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sentence {self.id} (doc={self.document_id} ord={self.order})"


class CorpusToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    sentence = models.ForeignKey(CorpusSentence, on_delete=models.CASCADE, related_name='tokens')
    order = models.IntegerField(db_index=True)
    text = models.CharField(max_length=400)
    norm = models.CharField(max_length=400, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=['text']),]

    def __str__(self):
        return f"Token {self.text} (sent={self.sentence_id})"
