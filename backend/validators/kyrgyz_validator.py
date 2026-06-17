"""Kyrgyz (Kipchak) dataset validator.

Kyrgyz has full four-way (front/back + rounded) harmony. The datasets use a Latin
transliteration ('y' for the close back unrounded vowel). The rules engine validates the
front/back dimension across the plural skeletons -lar/-ler/-lor/-lör.
"""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class KyrgyzValidator(BaseLanguageValidator):
    language_code = "ky"
    language_name = "Kyrgyz"

    alphabet = frozenset("abdefgğhijklmnñoöprsştuüwyz")

    back_vowels = frozenset("aouy")
    front_vowels = frozenset("eiöü")

    harmony_suffixes = (
        ("lar", "ler"),
        ("lor", "lör"),
        ("dan", "den"),
    )

    productive_suffixes = (
        "lar",
        "ler",
        "lor",
        "lör",
        "luu",
        "syz",
        "chy",
        "chi",
        "dan",
        "den",
        "gan",
        "gen",
        "dyn",
        "din",
    )
