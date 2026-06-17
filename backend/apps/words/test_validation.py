import json
from pathlib import Path
import tempfile

from django.core.management import call_command
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.words.services.validation_service import (
    LANGUAGE_STEMS,
    DatasetQualityService,
    DatasetValidationService,
)
from validators import VALIDATORS, get_validator
from validators.base_validator import Severity
from validators.turkish_validator import TurkishValidator
from validators.uzbek_validator import UzbekValidator


def raw_record(**overrides):
    record = {
        "word": "evler",
        "lemma": "ev",
        "root": "ev",
        "pos": "noun",
        "ipa": "evler",
        "meaning": "houses",
        "frequency": 100,
        "source": "test",
        "notes": "",
    }
    record.update(overrides)
    return record


class ValidatorRegistryTests(SimpleTestCase):
    def test_every_language_has_a_validator(self):
        self.assertEqual(set(VALIDATORS), set(LANGUAGE_STEMS))

    def test_get_validator_returns_instance(self):
        self.assertIsInstance(get_validator("tr"), TurkishValidator)

    def test_get_validator_rejects_unknown_language(self):
        with self.assertRaises(ValueError):
            get_validator("xx")


class NormalizationTests(SimpleTestCase):
    def setUp(self):
        self.validator = TurkishValidator()

    def test_pos_is_uppercased_and_language_code_injected(self):
        normalized = self.validator.normalize(raw_record(pos="noun"))

        self.assertEqual(normalized["pos"], "NOUN")
        self.assertEqual(normalized["language_code"], "tr")

    def test_whitespace_collapsed_and_text_trimmed(self):
        normalized = self.validator.normalize(raw_record(word="  ev  ler  "))

        self.assertEqual(normalized["word"], "ev ler")

    def test_invalid_frequency_becomes_zero(self):
        self.assertEqual(self.validator.normalize(raw_record(frequency="abc"))["frequency"], 0)
        self.assertEqual(self.validator.normalize(raw_record(frequency=-5))["frequency"], 0)

    def test_normalized_record_has_full_schema(self):
        normalized = self.validator.normalize({"word": "ev", "pos": "noun"})

        self.assertEqual(
            set(normalized),
            {
                "language_code",
                "word",
                "lemma",
                "root",
                "pos",
                "ipa",
                "meaning",
                "frequency",
                "source",
                "notes",
            },
        )


class TurkishHarmonyTests(SimpleTestCase):
    def setUp(self):
        self.validator = TurkishValidator()

    def _codes(self, **overrides):
        record = self.validator.normalize(raw_record(**overrides))
        return {issue.code for issue in self.validator.validate(record)}

    def test_valid_harmony_forms_pass(self):
        for word, lemma in (("evler", "ev"), ("okullar", "okul"), ("kitaplar", "kitap")):
            self.assertNotIn("vowel_harmony", self._codes(word=word, lemma=lemma, meaning="x"))

    def test_invalid_harmony_forms_flagged(self):
        for word, lemma in (("evlar", "ev"), ("okuller", "okul"), ("kitapler", "kitap")):
            self.assertIn("vowel_harmony", self._codes(word=word, lemma=lemma, meaning="x"))

    def test_vowel_classification_helpers(self):
        self.assertEqual(self.validator.classify_vowel("a"), "back")
        self.assertEqual(self.validator.classify_vowel("e"), "front")
        self.assertIsNone(self.validator.classify_vowel("k"))
        self.assertEqual(self.validator.last_vowel_class("okul"), "back")
        self.assertIsNone(self.validator.last_vowel_class("kkk"))


class RulesEngineTests(SimpleTestCase):
    def setUp(self):
        self.validator = TurkishValidator()

    def _codes(self, record):
        normalized = self.validator.normalize(record)
        return {issue.code for issue in self.validator.validate(normalized)}

    def test_empty_required_field_is_error(self):
        self.assertIn("empty_field", self._codes(raw_record(word="")))

    def test_invalid_pos_detected(self):
        self.assertIn("invalid_pos", self._codes(raw_record(pos="gerund")))

    def test_malformed_ipa_with_digits(self):
        self.assertIn("malformed_ipa", self._codes(raw_record(ipa="ev3ler")))

    def test_invalid_unicode_detected(self):
        bad_word = "ev" + chr(0) + "ler"
        self.assertIn("invalid_unicode", self._codes(raw_record(word=bad_word)))

    def test_frequency_anomaly_is_warning(self):
        normalized = self.validator.normalize(raw_record(frequency=9_999_999))
        issues = self.validator.validate(normalized)
        anomaly = next(issue for issue in issues if issue.code == "frequency_anomaly")
        self.assertEqual(anomaly.severity, Severity.WARNING)

    def test_out_of_alphabet_is_warning(self):
        normalized = self.validator.normalize(raw_record(word="ev" + "л" + "er", meaning="x"))
        issues = self.validator.validate(normalized)
        self.assertTrue(any(issue.code == "out_of_alphabet" for issue in issues))


class UzbekMorphologyTests(SimpleTestCase):
    def setUp(self):
        self.validator = UzbekValidator()

    def _codes(self, **overrides):
        record = self.validator.normalize(raw_record(pos="noun", **overrides))
        return {issue.code for issue in self.validator.validate(record)}

    def test_productive_suffix_chain_passes(self):
        self.assertNotIn("non_productive", self._codes(word="kitoblar", lemma="kitob", root="kitob", meaning="books"))

    def test_unsegmentable_suffix_warns(self):
        codes = self._codes(word="kitobxyz", lemma="kitob", root="kitob", meaning="x")
        self.assertIn("non_productive", codes)

    def test_form_not_starting_with_lemma_warns(self):
        codes = self._codes(word="boshqa", lemma="kitob", root="kitob", meaning="x")
        self.assertIn("non_productive", codes)

    def test_segment_suffixes_helper(self):
        self.assertTrue(self.validator.segment_suffixes("lar"))
        self.assertFalse(self.validator.segment_suffixes("zzz"))
        self.assertTrue(self.validator.segment_suffixes(""))


class DatasetValidationServiceTests(SimpleTestCase):
    def _run(self, records, code="tr"):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        words_dir = base / "words"
        words_dir.mkdir()
        stem = LANGUAGE_STEMS[code]
        (words_dir / f"{stem}_words.json").write_text(json.dumps(records), encoding="utf-8")

        service = DatasetValidationService(
            words_dir=words_dir,
            reports_dir=base / "reports",
            normalized_dir=base / "normalized",
        )
        summary = service.run(languages=[code])
        return base, summary[code]

    def test_pipeline_removes_duplicates_and_invalid_forms(self):
        records = [
            raw_record(word="evler", lemma="ev", meaning="houses"),
            raw_record(word="evler", lemma="ev", meaning="houses"),  # duplicate
            raw_record(word="evlar", lemma="ev", meaning="x"),  # harmony error
            raw_record(word="", lemma="ev", meaning="x"),  # empty word
        ]
        base, report = self._run(records)

        self.assertEqual(report["total_records"], 4)
        self.assertEqual(report["valid_records"], 1)
        self.assertEqual(report["duplicates_removed"], 1)
        self.assertEqual(report["invalid_forms_removed"], 2)
        self.assertEqual(report["validation_score"], 25.0)

    def test_pipeline_writes_report_and_clean_files(self):
        base, report = self._run([raw_record(word="evler", lemma="ev", meaning="houses")])

        report_path = base / "reports" / "report_turkish.json"
        clean_path = base / "normalized" / "turkish_words_clean.json"
        self.assertTrue(report_path.exists())
        self.assertTrue(clean_path.exists())

        clean = json.loads(clean_path.read_text(encoding="utf-8"))
        self.assertEqual(clean[0]["pos"], "NOUN")
        self.assertEqual(clean[0]["language_code"], "tr")

    def test_missing_dataset_raises(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        service = DatasetValidationService(words_dir=Path(tmp.name))
        with self.assertRaises(FileNotFoundError):
            service.run(languages=["tr"])

    def test_non_list_dataset_raises(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        words_dir = Path(tmp.name) / "words"
        words_dir.mkdir()
        (words_dir / "turkish_words.json").write_text(json.dumps({"not": "a list"}), encoding="utf-8")
        service = DatasetValidationService(words_dir=words_dir)
        with self.assertRaises(ValueError):
            service.run(languages=["tr"])


class DatasetQualityServiceTests(SimpleTestCase):
    def test_summary_aggregates_reports(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        reports_dir = Path(tmp.name)
        (reports_dir / "report_turkish.json").write_text(
            json.dumps(
                {
                    "total_records": 10,
                    "valid_records": 8,
                    "invalid_records": 2,
                    "duplicates_removed": 1,
                    "validation_score": 80.0,
                }
            ),
            encoding="utf-8",
        )

        summary = DatasetQualityService(reports_dir=reports_dir).summary()

        self.assertEqual(set(summary), {"languages", "records", "duplicates", "validation_score"})
        self.assertEqual(summary["records"]["tr"], 10)
        self.assertEqual(summary["duplicates"]["tr"], 1)
        self.assertEqual(summary["validation_score"]["tr"], 80.0)
        self.assertEqual(summary["languages"]["tr"]["valid"], 8)

    def test_summary_is_empty_without_reports(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        summary = DatasetQualityService(reports_dir=Path(tmp.name)).summary()
        self.assertEqual(summary["records"], {})


class ValidateCommandTests(SimpleTestCase):
    def test_command_runs_and_writes_outputs(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        words_dir = base / "words"
        words_dir.mkdir()
        (words_dir / "uzbek_words.json").write_text(
            json.dumps([raw_record(word="kitoblar", lemma="kitob", root="kitob", pos="noun", meaning="books")]),
            encoding="utf-8",
        )

        call_command(
            "validate_words_dataset",
            words_dir=str(words_dir),
            reports_dir=str(base / "reports"),
            normalized_dir=str(base / "normalized"),
            language=["uz"],
            verbosity=0,
        )

        self.assertTrue((base / "reports" / "report_uzbek.json").exists())
        self.assertTrue((base / "normalized" / "uzbek_words_clean.json").exists())


class WordQualityApiTests(APITestCase):
    def test_quality_endpoint_returns_expected_shape(self):
        response = self.client.get(reverse("word-quality"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data),
            {"languages", "records", "duplicates", "validation_score"},
        )
