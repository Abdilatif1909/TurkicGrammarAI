"""Dataset validation, normalization and quality-reporting pipeline (Phase 4)."""

from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings

from validators import get_validator
from validators.base_validator import Severity

# Maps language code -> dataset stem used across input, report and normalized filenames.
LANGUAGE_STEMS = {
    "uz": "uzbek",
    "tr": "turkish",
    "kk": "kazakh",
    "ky": "kyrgyz",
    "az": "azerbaijani",
    "tk": "turkmen",
    "otk": "old_turkic",
}

# Cap stored warnings so reports stay small on large datasets.
WARNINGS_LIMIT = 100


class DatasetValidationService:
    """Validate and normalize every Turkic word dataset, writing reports and clean files."""

    def __init__(
        self,
        words_dir: str | Path | None = None,
        reports_dir: str | Path | None = None,
        normalized_dir: str | Path | None = None,
    ):
        base = settings.BASE_DIR / "data"
        self.words_dir = Path(words_dir) if words_dir else base / "words"
        self.reports_dir = Path(reports_dir) if reports_dir else base / "reports"
        self.normalized_dir = Path(normalized_dir) if normalized_dir else base / "normalized"

    def run(self, languages: list[str] | None = None) -> dict[str, dict]:
        codes = languages or list(LANGUAGE_STEMS)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.normalized_dir.mkdir(parents=True, exist_ok=True)

        summary: dict[str, dict] = {}
        for code in codes:
            summary[code] = self.validate_language(code)
        return summary

    def validate_language(self, code: str) -> dict:
        stem = LANGUAGE_STEMS[code]
        validator = get_validator(code)
        records = self._load_records(self.words_dir / f"{stem}_words.json")

        clean: list[dict] = []
        warnings: list[str] = []
        seen: set[tuple] = set()
        duplicates_removed = 0
        invalid_forms_removed = 0

        for record in records:
            normalized = validator.normalize(record)
            issues = validator.validate(normalized)
            errors = [issue for issue in issues if issue.severity == Severity.ERROR]
            for issue in issues:
                if issue.severity == Severity.WARNING and len(warnings) < WARNINGS_LIMIT:
                    warnings.append(issue.as_warning(normalized.get("word", "")))

            if errors:
                invalid_forms_removed += 1
                continue

            key = validator.dedupe_key(normalized)
            if key in seen:
                duplicates_removed += 1
                continue
            seen.add(key)
            clean.append(normalized)

        total = len(records)
        valid = len(clean)
        report = {
            "total_records": total,
            "valid_records": valid,
            "invalid_records": invalid_forms_removed,
            "duplicates_removed": duplicates_removed,
            "invalid_forms_removed": invalid_forms_removed,
            "warnings": warnings,
        }

        report_meta = {
            **report,
            "language_code": code,
            "language": stem,
            "validation_score": round((valid / total) * 100, 2) if total else 0.0,
            "warnings_truncated": len(warnings) >= WARNINGS_LIMIT,
        }

        self._write_json(self.reports_dir / f"report_{stem}.json", report_meta)
        self._write_json(self.normalized_dir / f"{stem}_words_clean.json", clean)
        return report_meta

    @staticmethod
    def _load_records(path: Path) -> list[dict]:
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")
        with path.open("r", encoding="utf-8") as dataset_file:
            data = json.load(dataset_file)
        if not isinstance(data, list):
            raise ValueError(f"Dataset {path.name} must contain a JSON list.")
        return data

    @staticmethod
    def _write_json(path: Path, payload) -> None:
        with path.open("w", encoding="utf-8") as output:
            json.dump(payload, output, ensure_ascii=False, indent=2)


class DatasetQualityService:
    """Aggregate the written validation reports into the quality-summary API payload."""

    def __init__(self, reports_dir: str | Path | None = None):
        self.reports_dir = Path(reports_dir) if reports_dir else settings.BASE_DIR / "data" / "reports"

    def summary(self) -> dict:
        languages: dict[str, dict] = {}
        records: dict[str, int] = {}
        duplicates: dict[str, int] = {}
        validation_score: dict[str, float] = {}

        for code, stem in LANGUAGE_STEMS.items():
            report = self._load_report(stem)
            if report is None:
                continue
            total = report.get("total_records", 0)
            valid = report.get("valid_records", 0)
            languages[code] = {
                "language": stem,
                "total": total,
                "valid": valid,
                "invalid": report.get("invalid_records", 0),
            }
            records[code] = total
            duplicates[code] = report.get("duplicates_removed", 0)
            validation_score[code] = report.get(
                "validation_score",
                round((valid / total) * 100, 2) if total else 0.0,
            )

        return {
            "languages": languages,
            "records": records,
            "duplicates": duplicates,
            "validation_score": validation_score,
        }

    def _load_report(self, stem: str) -> dict | None:
        path = self.reports_dir / f"report_{stem}.json"
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as report_file:
            return json.load(report_file)
