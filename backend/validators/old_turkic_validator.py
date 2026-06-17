"""Old Turkic dataset validator.

Old Turkic (Orkhon/Uyghur era) is given in Latin transliteration and shows strict
palatal (front/back) vowel harmony, which the rules engine validates on the plural and
case skeletons.
"""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class OldTurkicValidator(BaseLanguageValidator):
    language_code = "otk"
    language_name = "Old Turkic"

    alphabet = frozenset("abdegıiklmnoöprstuüwyzşğŋç")

    back_vowels = frozenset("aıou")
    front_vowels = frozenset("eiöü")

    harmony_suffixes = (
        ("lar", "ler"),
        ("dın", "din"),
        ("tın", "tin"),
    )

    productive_suffixes = (
        "lar",
        "ler",
        "lıg",
        "lig",
        "çı",
        "çi",
        "dın",
        "din",
        "ka",
        "ke",
        "ta",
        "te",
    )
