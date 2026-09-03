"""Unified lexical schema for processed TurkicGrammarAI data."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class LexicalEntry:
    """One normalized lexical entry in the master lexicon."""

    surface_form: str
    language: str
    lemma: str | None
    root: str | None
    pos: str
    semantic_description: str | None
    source_metadata: dict[str, Any]
    historical_lineage_metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
