"""Uzbek (Karluk) dataset validator.

Standard Uzbek has largely lost productive vowel harmony, so instead of harmony checks
this validator verifies that inflected/derived forms are built from the lemma plus
recognised productive suffixes.
"""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator, RecordIssue, Severity


class UzbekValidator(BaseLanguageValidator):
    language_code = "uz"
    language_name = "Uzbek"

    # The apostrophe in o' / g' is handled separately; only letters are checked.
    alphabet = frozenset("abdefghijklmnopqrstuvxyzcʻ‘'")

    # No active harmony, but vowels are still declared for completeness.
    back_vowels = frozenset("aou")
    front_vowels = frozenset("ei")

    harmony_suffixes = ()

    productive_suffixes = (
        "lar",
        "ning",
        "ni",
        "ga",
        "da",
        "dan",
        "miz",
        "ngiz",
        "im",
        "ing",
        "i",
        "lik",
        "chi",
        "li",
        "siz",
        "chan",
        "roq",
        "gi",
        "iy",
        "gan",
        "di",
        "moqda",
        "adi",
        "sa",
        "ish",
        "ar",
        "uvchi",
        "cha",
        "dek",
        "gacha",
    )

    def check_morphology(self, record: dict) -> list[RecordIssue]:
        word = record.get("word", "").lower()
        lemma = record.get("lemma", "").lower()
        if not word or not lemma or word == lemma:
            return []
        if not word.startswith(lemma):
            # A stem change is plausible but worth surfacing for review.
            return [
                RecordIssue(
                    Severity.WARNING,
                    "non_productive",
                    f"form '{word}' does not start with its lemma '{lemma}'",
                )
            ]
        remainder = word[len(lemma) :]
        if remainder and not self.segment_suffixes(remainder):
            return [
                RecordIssue(
                    Severity.WARNING,
                    "non_productive",
                    f"suffix chain '-{remainder}' is not built from productive Uzbek suffixes",
                )
            ]
        return []
