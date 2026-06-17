import re
from typing import List


SENTENCE_END_RE = re.compile(r'(?<=[\.\!\?])\s+')


def segment_sentences(text: str) -> List[str]:
    """Very small sentence segmentation fallback. Replace with language-specific models later."""
    if not text:
        return []
    # Normalize newlines to space to avoid broken sentences
    t = text.replace('\n', ' ')
    parts = SENTENCE_END_RE.split(t)
    parts = [p.strip() for p in parts if p.strip()]
    return parts
