"""Turkmen (Oghuz) dataset validator with two-way (a/e) vowel harmony.

Turkmen Latin uses 'y' for the close back unrounded vowel and 'ý' for the glide /j/;
only 'y' participates in vowel classification.
"""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class TurkmenValidator(BaseLanguageValidator):
    language_code = "tk"
    language_name = "Turkmen"

    alphabet = frozenset("abçdeäfghijžklmnňoöprsştuüwýyz")

    back_vowels = frozenset("aouy")
    front_vowels = frozenset("eäiöü")

    harmony_suffixes = (
        ("lar", "ler"),
        ("dan", "den"),
    )

    productive_suffixes = (
        "lar",
        "ler",
        "lyk",
        "lik",
        "çy",
        "çi",
        "dan",
        "den",
        "da",
        "de",
        "yň",
        "iň",
        "mak",
        "mek",
    )
