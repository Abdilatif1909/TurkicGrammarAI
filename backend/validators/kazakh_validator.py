"""Kazakh (Kipchak) dataset validator.

The datasets use a Latin transliteration (ı, ö, ğ, ş, w). Kazakh plural marking shows
both consonant alternation (l/d/t) and front/back vowel harmony; the rules engine checks
the vowel-harmony dimension across all three consonant skeletons.
"""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class KazakhValidator(BaseLanguageValidator):
    language_code = "kk"
    language_name = "Kazakh"

    alphabet = frozenset("abdefgğhıijklmnoöprsştuüwyzäñq")

    back_vowels = frozenset("aıou")
    front_vowels = frozenset("eäiöü")

    # -LAr / -DAr / -TAr each alternate lar/ler, dar/der, tar/ter by harmony.
    harmony_suffixes = (
        ("lar", "ler"),
        ("dar", "der"),
        ("tar", "ter"),
        ("dan", "den"),
        ("tan", "ten"),
    )

    productive_suffixes = (
        "lar",
        "ler",
        "dar",
        "der",
        "tar",
        "ter",
        "lıq",
        "lik",
        "şı",
        "şi",
        "dan",
        "den",
        "tan",
        "ten",
        "ğan",
        "gen",
    )
