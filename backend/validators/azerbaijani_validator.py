"""Azerbaijani (Oghuz) dataset validator with two-way (a/ə) vowel harmony."""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class AzerbaijaniValidator(BaseLanguageValidator):
    language_code = "az"
    language_name = "Azerbaijani"

    alphabet = frozenset("abcçdeəfgğhxıijkqlmnoöprsştuüvyz")

    # 'ə' (schwa) and 'e' pattern as front; the plural alternates -lar/-lər.
    back_vowels = frozenset("aıou")
    front_vowels = frozenset("eəiöü")

    harmony_suffixes = (
        ("lar", "lər"),
        ("dan", "dən"),
    )

    productive_suffixes = (
        "lar",
        "lər",
        "lıq",
        "lik",
        "luq",
        "lük",
        "çı",
        "çi",
        "çu",
        "çü",
        "dan",
        "dən",
        "da",
        "də",
        "ın",
        "in",
        "miş",
        "mış",
        "maq",
        "mək",
    )
