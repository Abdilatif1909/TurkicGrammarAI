import unicodedata
import re


def normalize_text(text, language=None):
    """Basic unicode and punctuation normalization. Language-specific rules can be extended."""
    if not text:
        return text
    # Unicode normalization
    s = unicodedata.normalize('NFC', text)
    # Normalize spaces
    s = re.sub(r'\s+', ' ', s).strip()
    # Collapse repeated punctuation
    s = re.sub(r'([\.!?]){2,}', r'\1', s)
    # Trim stray punctuation
    s = s.strip(' \n\t')

    # Language-specific hooks
    if language:
        lang = language.lower()
        if lang in ('tr', 'turkish'):
            # Example: Normalize Turkish-specific characters if needed
            s = s.replace('\u2018', "'").replace('\u2019', "'")
    return s
