"""Hashing-based deduplication for documents and sentences."""

from __future__ import annotations

import hashlib

from apps.corpus.models import CorpusDocument, CorpusSentence


class DeduplicationService:
    """Compute stable content hashes and detect duplicates across the corpus."""

    @staticmethod
    def hash_text(text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def document_hashes(language_id) -> set[str]:
        return set(
            CorpusDocument.objects.filter(language_id=language_id).values_list("content_hash", flat=True)
        )

    @staticmethod
    def sentence_hashes(language_id) -> set[str]:
        return set(
            CorpusSentence.objects.filter(language_id=language_id).values_list("text_hash", flat=True)
        )

    @staticmethod
    def document_exists(language_id, content_hash: str) -> bool:
        return CorpusDocument.objects.filter(language_id=language_id, content_hash=content_hash).exists()
