import hashlib
from apps.corpus.models import CorpusDocument, CorpusSentence


class DedupeEngine:
    """Document and sentence level deduplication using SHA256 checksums."""

    @staticmethod
    def doc_exists(raw_text):
        checksum = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
        return CorpusDocument.objects.filter(checksum=checksum).exists()

    @staticmethod
    def sentence_exists(checksum):
        return CorpusSentence.objects.filter(checksum=checksum).exists()

    @staticmethod
    def remove_duplicate_documents():
        # naive approach: keep first, delete others with same checksum
        checks = CorpusDocument.objects.values('checksum').order_by('checksum').distinct()
        removed = 0
        for c in checks:
            docs = list(CorpusDocument.objects.filter(checksum=c['checksum']).order_by('imported_at'))
            if len(docs) > 1:
                for d in docs[1:]:
                    d.delete()
                    removed += 1
        return removed
