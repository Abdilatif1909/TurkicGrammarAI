"""Turkic linguistic dataset validators (Phase 4).

Each language validator subclasses :class:`BaseLanguageValidator` and encodes the
language-specific orthography, vowel-harmony rules, and productive morphology used
to detect malformed or linguistically impossible records before model training.
"""

from validators.azerbaijani_validator import AzerbaijaniValidator
from validators.base_validator import BaseLanguageValidator, RecordIssue, Severity
from validators.kazakh_validator import KazakhValidator
from validators.kyrgyz_validator import KyrgyzValidator
from validators.old_turkic_validator import OldTurkicValidator
from validators.turkish_validator import TurkishValidator
from validators.turkmen_validator import TurkmenValidator
from validators.uzbek_validator import UzbekValidator

VALIDATORS: dict[str, type[BaseLanguageValidator]] = {
    UzbekValidator.language_code: UzbekValidator,
    TurkishValidator.language_code: TurkishValidator,
    KazakhValidator.language_code: KazakhValidator,
    KyrgyzValidator.language_code: KyrgyzValidator,
    AzerbaijaniValidator.language_code: AzerbaijaniValidator,
    TurkmenValidator.language_code: TurkmenValidator,
    OldTurkicValidator.language_code: OldTurkicValidator,
}


def get_validator(language_code: str) -> BaseLanguageValidator:
    """Instantiate the validator registered for ``language_code``."""
    try:
        return VALIDATORS[language_code]()
    except KeyError as exc:
        raise ValueError(f"No validator registered for language '{language_code}'.") from exc


__all__ = [
    "BaseLanguageValidator",
    "RecordIssue",
    "Severity",
    "AzerbaijaniValidator",
    "KazakhValidator",
    "KyrgyzValidator",
    "OldTurkicValidator",
    "TurkishValidator",
    "TurkmenValidator",
    "UzbekValidator",
    "VALIDATORS",
    "get_validator",
]
