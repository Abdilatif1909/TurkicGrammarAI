"""Sentence segmentation producing CorpusSentence records."""

from __future__ import annotations

import re

from django.db import transaction

from apps.corpus.models import CorpusDocument, CorpusSentence
from apps.corpus.services.dedup_service import DeduplicationService

# Split on sentence-final punctuation (. ! ? plus their repetitions) or hard line breaks.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+|\n+")
_MIN_SENTENCE_LENGTH = 2


class SegmentationService:
    @staticmethod
    def segment(text: str) -> list[str]:
        if not text:
            return []
        candidates = _SENTENCE_BOUNDARY.split(text)
        sentences = []
        for candidate in candidates:
            cleaned = candidate.strip()
            if len(cleaned) >= _MIN_SENTENCE_LENGTH:
                sentences.append(cleaned)
        return sentences

    @classmethod
    @transaction.atomic
    def build_for_document(cls, document: CorpusDocument, seen_hashes: set[str] | None = None) -> dict[str, int]:
        """Create deduplicated sentence records for ``document``.

        ``seen_hashes`` may be supplied by a batch run to dedupe across documents without
        re-querying the database for every document.
        """
        document.sentences.all().delete()
        if seen_hashes is None:
            seen_hashes = DeduplicationService.sentence_hashes(document.language_id)

        created = 0
        duplicates = 0
        position = 0
        pending: list[CorpusSentence] = []

        for text in cls.segment(document.content):
            text_hash = DeduplicationService.hash_text(text)
            if text_hash in seen_hashes:
                duplicates += 1
                continue
            seen_hashes.add(text_hash)
            pending.append(
                CorpusSentence(
                    document=document,
                    language_id=document.language_id,
                    text=text,
                    text_hash=text_hash,
                    position=position,
                )
            )
            position += 1
            created += 1

        if pending:
            CorpusSentence.objects.bulk_create(pending, batch_size=2000)
        return {"created": created, "duplicates": duplicates}
