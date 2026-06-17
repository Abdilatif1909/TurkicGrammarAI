import csv
import io
import json
from pathlib import Path
import tempfile

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import UserRole
from apps.languages.models import Language
from apps.words.models import PartOfSpeech, Word

User = get_user_model()


def create_language(code="uz", name="Uzbek", iso639_3="uzb"):
    return Language.objects.create(
        name=name,
        native_name=name,
        code=code,
        iso639_3=iso639_3,
        family="Turkic",
        branch="Karluk",
        writing_system="Latin",
        speakers_count=1000,
        country="Uzbekistan",
        description="Test language.",
        flag_url="https://flagcdn.com/uz.svg",
    )


def word_payload(language, **overrides):
    payload = {
        "language": language,
        "word": "kelgan",
        "lemma": "kel",
        "root": "kel",
        "pos": PartOfSpeech.VERB,
        "ipa": "kelgan",
        "meaning": "to have come",
        "frequency": 100,
        "source": "test-source",
        "notes": "Test word.",
    }
    payload.update(overrides)
    return payload


def generated_record(language_code="uz", **overrides):
    record = {
        "language_code": language_code,
        "word": "kelgan",
        "lemma": "kel",
        "root": "kel",
        "pos": "VERB",
        "ipa": "kelgan",
        "meaning": "to have come",
        "frequency": 100,
        "source": "test-seed",
        "notes": "Generated test word.",
    }
    record.update(overrides)
    return record


class WordModelTests(APITestCase):
    def test_word_str_uses_word_and_language_code(self):
        language = create_language()
        word = Word.objects.create(**word_payload(language))

        self.assertEqual(str(word), "kelgan (uz)")
        self.assertIsNotNone(word.created_at)
        self.assertIsNotNone(word.updated_at)


class WordDatasetGenerationTests(APITestCase):
    def test_generate_words_dataset_command_writes_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            call_command("generate_words_dataset", size=14, output_dir=tmp_dir, verbosity=0)
            files = sorted(path.name for path in Path(tmp_dir).glob("*.json"))

            self.assertEqual(
                files,
                [
                    "azerbaijani_words.json",
                    "kazakh_words.json",
                    "kyrgyz_words.json",
                    "old_turkic_words.json",
                    "turkish_words.json",
                    "turkmen_words.json",
                    "uzbek_words.json",
                ],
            )
            total = 0
            for file_path in Path(tmp_dir).glob("*.json"):
                total += len(json.loads(file_path.read_text(encoding="utf-8")))
            self.assertEqual(total, 14)


class WordSeedTests(APITestCase):
    def setUp(self):
        self.language = create_language()

    def test_seed_words_bulk_inserts_and_skips_duplicates(self):
        records = [
            generated_record(word="kelgan", meaning="to have come"),
            generated_record(word="borgan", lemma="bor", root="bor", meaning="to have gone"),
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            seed_path = Path(tmp_dir) / "uzbek_words.json"
            seed_path.write_text(json.dumps(records), encoding="utf-8")

            call_command("seed_words", path=str(seed_path), batch_size=5000, verbosity=0)
            call_command("seed_words", path=str(seed_path), batch_size=5000, verbosity=0)

        self.assertEqual(Word.objects.count(), 2)

    def test_seed_words_supports_csv(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            seed_path = Path(tmp_dir) / "words.csv"
            with seed_path.open("w", encoding="utf-8", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=list(generated_record().keys()))
                writer.writeheader()
                writer.writerow(generated_record(word="yozdi", lemma="yoz", root="yoz", meaning="wrote"))

            call_command("seed_words", path=str(seed_path), verbosity=0)

        self.assertEqual(Word.objects.count(), 1)
        self.assertEqual(Word.objects.first().word, "yozdi")


class WordPublicApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.language = create_language()
        self.word = Word.objects.create(**word_payload(self.language))
        Word.objects.create(
            **word_payload(
                self.language,
                word="bosh",
                lemma="bosh",
                root="bosh",
                pos=PartOfSpeech.NOUN,
                meaning="head",
                frequency=200,
            )
        )

    def test_public_word_list_is_paginated_and_filterable(self):
        response = self.client.get(reverse("word-list"), {"language_code": "uz", "pos": "NOUN"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["word"], "bosh")

    def test_public_word_detail_is_available(self):
        response = self.client.get(reverse("word-detail", kwargs={"id": self.word.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["word"], "kelgan")

    def test_public_word_search_finds_meaning(self):
        response = self.client.get(reverse("word-search"), {"q": "head"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["lemma"], "bosh")

    def test_word_statistics_returns_totals(self):
        response = self.client.get(reverse("word-statistics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_words"], 2)
        self.assertEqual(response.data["languages"][0]["language__code"], "uz")

    def test_list_cache_is_invalidated_after_admin_create(self):
        first = self.client.get(reverse("word-list"))
        self.assertEqual(first.data["count"], 2)

        admin = User.objects.create_user(
            email="admin@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        self.client.force_authenticate(admin)
        response = self.client.post(
            reverse("admin-word-list"),
            {
                "language": str(self.language.id),
                "word": "suv",
                "lemma": "suv",
                "root": "suv",
                "pos": "NOUN",
                "ipa": "suv",
                "meaning": "water",
                "frequency": 300,
                "source": "test-source",
                "notes": "",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=None)
        second = self.client.get(reverse("word-list"))
        self.assertEqual(second.data["count"], 3)


class WordAdminApiTests(APITestCase):
    def setUp(self):
        self.language = create_language()
        self.word = Word.objects.create(**word_payload(self.language))
        self.super_admin = User.objects.create_user(
            email="super@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        self.student = User.objects.create_user(
            email="student@example.com",
            password="StrongPass123",
            role=UserRole.STUDENT,
        )

    def test_super_admin_can_crud_word(self):
        self.client.force_authenticate(self.super_admin)

        create_response = self.client.post(
            reverse("admin-word-list"),
            {
                "language": str(self.language.id),
                "word": "oqidi",
                "lemma": "oqi",
                "root": "oqi",
                "pos": "VERB",
                "ipa": "oqidi",
                "meaning": "read",
                "frequency": 150,
                "source": "test-source",
                "notes": "",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        word_id = create_response.data["id"]
        patch_response = self.client.patch(
            reverse("admin-word-detail", kwargs={"id": word_id}),
            {"frequency": 151},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["frequency"], 151)

        delete_response = self.client.delete(reverse("admin-word-detail", kwargs={"id": word_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Word.objects.filter(id=word_id).exists())

    def test_student_cannot_access_admin_word_api(self):
        self.client.force_authenticate(self.student)

        response = self.client.post(reverse("admin-word-list"), {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_super_admin_can_export_json_and_csv(self):
        self.client.force_authenticate(self.super_admin)

        json_response = self.client.get(reverse("admin-word-export"), {"format": "json"})
        self.assertEqual(json_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.data[0]["word"], "kelgan")

        csv_response = self.client.get(reverse("admin-word-export"), {"format": "csv"})
        self.assertEqual(csv_response.status_code, status.HTTP_200_OK)
        rows = list(csv.DictReader(io.StringIO(csv_response.content.decode("utf-8"))))
        self.assertEqual(rows[0]["word"], "kelgan")

    def test_super_admin_can_seed_words_via_api(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            seed_path = Path(tmp_dir) / "uzbek_words.json"
            seed_path.write_text(json.dumps([generated_record(word="til", lemma="til", root="til")]), encoding="utf-8")

            from apps.words.services.import_service import WordImportService

            original_default_dir = WordImportService.default_dir
            WordImportService.default_dir = Path(tmp_dir)
            try:
                self.client.force_authenticate(self.super_admin)
                response = self.client.post(reverse("admin-seed-words"))
            finally:
                WordImportService.default_dir = original_default_dir

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["created"], 1)

    def test_super_admin_can_run_import_benchmark(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            seed_path = Path(tmp_dir) / "uzbek_words.json"
            seed_path.write_text(json.dumps([generated_record(word="til", lemma="til", root="til")]), encoding="utf-8")

            from apps.words.services.import_service import WordImportService

            original_default_dir = WordImportService.default_dir
            WordImportService.default_dir = Path(tmp_dir)
            try:
                self.client.force_authenticate(self.super_admin)
                response = self.client.post(reverse("admin-word-benchmark-import"))
            finally:
                WordImportService.default_dir = original_default_dir

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["meets_target"])
