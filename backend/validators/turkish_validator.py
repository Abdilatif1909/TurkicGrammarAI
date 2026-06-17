"""Turkish (Oghuz) dataset validator with two-way (a/e) vowel harmony."""

from __future__ import annotations

from validators.base_validator import BaseLanguageValidator


class TurkishValidator(BaseLanguageValidator):
    language_code = "tr"
    language_name = "Turkish"

    alphabet = frozenset("abcçdefgğhıijklmnoöprsştuüvyz")

    back_vowels = frozenset("aıou")
    front_vowels = frozenset("eiöü")

    # Plural -lar/-ler and locative/ablative skeletons follow the low-vowel (a/e) harmony.
    # evler ✓ / evlar ✗   okullar ✓ / okuller ✗   kitaplar ✓ / kitapler ✗
    harmony_suffixes = (
        ("lar", "ler"),
        ("dan", "den"),
        ("tan", "ten"),
    )

    productive_suffixes = (
        "lar",
        "ler",
        "lik",
        "lık",
        "luk",
        "lük",
        "ci",
        "cı",
        "cu",
        "cü",
        "den",
        "dan",
        "de",
        "da",
        "in",
        "ın",
        "miş",
        "mış",
        "iyor",
        "mek",
        "mak",
    )
