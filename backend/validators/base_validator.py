"""Base linguistic validator and rules engine shared by all Turkic validators."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

# Mirrors apps.words.models.PartOfSpeech to keep validators import-light (no Django).
VALID_POS = frozenset(
    {
        "NOUN",
        "VERB",
        "ADJECTIVE",
        "ADVERB",
        "PRONOUN",
        "NUMERAL",
        "POSTPOSITION",
        "CONJUNCTION",
        "PARTICLE",
        "INTERJECTION",
    }
)

# Fields that must be present and non-empty for a record to be seedable.
NON_EMPTY_FIELDS = ("word", "lemma", "pos", "meaning")

# Full schema written to normalized output (language_code is injected during normalization).
NORMALIZED_FIELDS = (
    "language_code",
    "word",
    "lemma",
    "root",
    "pos",
    "ipa",
    "meaning",
    "frequency",
    "source",
    "notes",
)

# Unicode categories that should never appear inside a lexical record.
_FORBIDDEN_UNICODE_CATEGORIES = {"Cc", "Cf", "Co", "Cs", "Cn"}

# IPA strings may contain letters, common phonetic marks, hyphens and spaces but never digits.
_IPA_FORBIDDEN = re.compile(r"[0-9]")


class Severity:
    """Issue severities. ``ERROR`` drops the record; ``WARNING`` keeps but reports it."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class RecordIssue:
    severity: str
    code: str
    message: str

    def as_warning(self, word: str) -> str:
        return f"[{self.code}] '{word}': {self.message}"


class BaseLanguageValidator:
    """Validate and normalize a single Turkic language dataset.

    Subclasses declare the language orthography (``alphabet``), the vowel inventory
    (``back_vowels`` / ``front_vowels``) and the harmony-sensitive suffix skeletons
    (``harmony_suffixes``) used by the rules engine.
    """

    language_code = ""
    language_name = ""

    # Lowercase letters considered native to the language. Apostrophes/hyphens are always allowed.
    alphabet: frozenset[str] = frozenset()

    back_vowels: frozenset[str] = frozenset()
    front_vowels: frozenset[str] = frozenset()

    # Harmony-sensitive suffix pairs as (back_form, front_form). The engine flags a record
    # when the attached variant disagrees with the stem's final vowel class.
    harmony_suffixes: tuple[tuple[str, str], ...] = ()

    # Productive suffixes used for derivational/inflectional segmentation checks.
    productive_suffixes: tuple[str, ...] = ()

    valid_pos: frozenset[str] = VALID_POS

    # Frequency sanity bounds for anomaly detection.
    min_frequency = 0
    max_frequency = 1_000_000

    # --- public API -----------------------------------------------------------------

    @property
    def vowels(self) -> frozenset[str]:
        return self.back_vowels | self.front_vowels

    def normalize(self, record: dict) -> dict:
        """Return an NFC-normalized, schema-complete copy of ``record``.

        Whitespace is trimmed, ``pos`` is upper-cased, ``frequency`` is coerced to a
        non-negative int, and ``language_code`` is injected from the validator.
        """
        normalized: dict = {}
        for field in ("word", "lemma", "root", "ipa", "meaning", "source", "notes"):
            value = record.get(field, "")
            normalized[field] = self._clean_text(value)
        normalized["pos"] = self._clean_text(record.get("pos", "")).upper()
        normalized["frequency"] = self._coerce_frequency(record.get("frequency"))
        normalized["language_code"] = self.language_code
        return {field: normalized.get(field, "") for field in NORMALIZED_FIELDS}

    def validate(self, record: dict) -> list[RecordIssue]:
        """Run the full rules engine against an already-normalized ``record``."""
        issues: list[RecordIssue] = []
        issues.extend(self._check_required(record))
        # Without a word the remaining lexical checks are meaningless.
        if any(issue.code == "empty_field" and "word" in issue.message for issue in issues):
            return issues
        issues.extend(self._check_unicode(record))
        issues.extend(self._check_pos(record))
        issues.extend(self._check_ipa(record))
        issues.extend(self._check_frequency(record))
        issues.extend(self._check_alphabet(record))
        issues.extend(self.check_morphology(record))
        return issues

    def dedupe_key(self, record: dict) -> tuple:
        return (record["word"], record["lemma"], record["pos"], record["meaning"])

    # --- individual rules -------------------------------------------------------------

    def _check_required(self, record: dict) -> list[RecordIssue]:
        issues = []
        for field in NON_EMPTY_FIELDS:
            if not str(record.get(field, "")).strip():
                issues.append(RecordIssue(Severity.ERROR, "empty_field", f"missing required field '{field}'"))
        return issues

    def _check_unicode(self, record: dict) -> list[RecordIssue]:
        for field in ("word", "lemma", "root"):
            value = record.get(field, "")
            for char in value:
                if unicodedata.category(char) in _FORBIDDEN_UNICODE_CATEGORIES:
                    code_point = f"U+{ord(char):04X}"
                    return [
                        RecordIssue(
                            Severity.ERROR,
                            "invalid_unicode",
                            f"field '{field}' contains invalid character {code_point}",
                        )
                    ]
        return []

    def _check_pos(self, record: dict) -> list[RecordIssue]:
        pos = record.get("pos", "")
        if pos and pos not in self.valid_pos:
            return [RecordIssue(Severity.ERROR, "invalid_pos", f"unknown part of speech '{pos}'")]
        return []

    def _check_ipa(self, record: dict) -> list[RecordIssue]:
        ipa = record.get("ipa", "")
        if not ipa:
            return []
        if _IPA_FORBIDDEN.search(ipa):
            return [RecordIssue(Severity.ERROR, "malformed_ipa", f"IPA transcription '{ipa}' contains digits")]
        for char in ipa:
            if unicodedata.category(char) in _FORBIDDEN_UNICODE_CATEGORIES:
                return [RecordIssue(Severity.ERROR, "malformed_ipa", f"IPA transcription '{ipa}' has control chars")]
        return []

    def _check_frequency(self, record: dict) -> list[RecordIssue]:
        frequency = record.get("frequency", 0)
        if frequency < self.min_frequency or frequency > self.max_frequency:
            return [
                RecordIssue(
                    Severity.WARNING,
                    "frequency_anomaly",
                    f"frequency {frequency} outside [{self.min_frequency}, {self.max_frequency}]",
                )
            ]
        return []

    def _check_alphabet(self, record: dict) -> list[RecordIssue]:
        if not self.alphabet:
            return []
        word = record.get("word", "")
        for char in word.lower():
            if char.isalpha() and char not in self.alphabet:
                return [
                    RecordIssue(
                        Severity.WARNING,
                        "out_of_alphabet",
                        f"character '{char}' is not in the {self.language_name} alphabet",
                    )
                ]
        return []

    def check_morphology(self, record: dict) -> list[RecordIssue]:
        """Default morphology check: vowel-harmony validation on harmony-sensitive suffixes."""
        return self._check_vowel_harmony(record)

    # --- rules-engine helpers ---------------------------------------------------------

    def classify_vowel(self, char: str) -> str | None:
        if char in self.back_vowels:
            return "back"
        if char in self.front_vowels:
            return "front"
        return None

    def last_vowel_class(self, stem: str) -> str | None:
        for char in reversed(stem.lower()):
            klass = self.classify_vowel(char)
            if klass is not None:
                return klass
        return None

    def _check_vowel_harmony(self, record: dict) -> list[RecordIssue]:
        word = record.get("word", "").lower()
        for back_form, front_form in self.harmony_suffixes:
            for attached, attached_class in ((back_form, "back"), (front_form, "front")):
                # Require a real stem of at least two letters to avoid flagging short roots.
                if not word.endswith(attached) or len(word) - len(attached) < 2:
                    continue
                stem = word[: -len(attached)]
                expected = self.last_vowel_class(stem)
                if expected is None or expected == attached_class:
                    return []
                correct = front_form if expected == "front" else back_form
                return [
                    RecordIssue(
                        Severity.ERROR,
                        "vowel_harmony",
                        f"suffix '-{attached}' violates vowel harmony after '{stem}'; expected '-{correct}'",
                    )
                ]
        return []

    def segment_suffixes(self, remainder: str) -> bool:
        """Greedily segment ``remainder`` into known productive suffixes (longest-match)."""
        ordered = sorted(self.productive_suffixes, key=len, reverse=True)
        cursor = remainder
        while cursor:
            for suffix in ordered:
                if suffix and cursor.startswith(suffix):
                    cursor = cursor[len(suffix) :]
                    break
            else:
                return False
        return True

    # --- internal utilities -----------------------------------------------------------

    @staticmethod
    def _clean_text(value) -> str:
        if value is None:
            return ""
        text = unicodedata.normalize("NFC", str(value))
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _coerce_frequency(value) -> int:
        try:
            frequency = int(value)
        except (TypeError, ValueError):
            return 0
        return max(0, frequency)
