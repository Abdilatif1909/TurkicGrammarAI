"""Text normalization pipeline for raw corpus content."""

from __future__ import annotations

import re
import unicodedata

# Map of typographic punctuation variants to their canonical ASCII equivalents.
_PUNCTUATION_MAP = {
    "‘": "'",  # left single quote
    "’": "'",  # right single quote
    "ʻ": "'",  # modifier letter turned comma (Uzbek o' / g')
    "ʼ": "'",  # modifier letter apostrophe
    "“": '"',  # left double quote
    "”": '"',  # right double quote
    "–": "-",  # en dash
    "—": "-",  # em dash
    "…": "...",  # ellipsis
    " ": " ",  # non-breaking space
}

# C0/C1 control characters except tab (\t), newline (\n) and carriage return (\r).
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
_MULTISPACE = re.compile(r"[ \t]+")
_MULTINEWLINE = re.compile(r"\n{3,}")


class NormalizationService:
    """Normalize Unicode form, punctuation, whitespace and language specifics."""

    @staticmethod
    def normalize_text(text: str, language_code: str | None = None) -> str:
        if not text:
            return ""
        text = unicodedata.normalize("NFC", text)
        text = _CONTROL_CHARS.sub("", text)
        for source, target in _PUNCTUATION_MAP.items():
            text = text.replace(source, target)
        text = NormalizationService._language_specific(text, language_code)
        # Whitespace cleanup: collapse runs of spaces/tabs and excess blank lines.
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = _MULTISPACE.sub(" ", text)
        text = _MULTINEWLINE.sub("\n\n", text)
        lines = [line.strip() for line in text.splitlines()]
        return "\n".join(lines).strip()

    @staticmethod
    def _language_specific(text: str, language_code: str | None) -> str:
        if language_code == "tr":
            # Collapse the combining-dot sequence some sources emit for dotted i.
            text = text.replace("i̇", "i")
        return text
