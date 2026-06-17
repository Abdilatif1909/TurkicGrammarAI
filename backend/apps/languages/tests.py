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

User = get_user_model()


def language_payload(**overrides):
    payload = {
        "name": "Uzbek",
        "native_name": "O'zbek tili",
        "code": "uz",
        "iso639_3": "uzb",
        "family": "Turkic",
        "branch": "Karluk",
        "writing_system": "Latin, Cyrillic, Arabic",
        "speakers_count": 44000000,
        "country": "Uzbekistan",
        "description": "A Karluk Turkic language spoken primarily in Uzbekistan.",
        "flag_url": "https://flagcdn.com/uz.svg",
    }
    payload.update(overrides)
    return payload


class LanguageModelTests(APITestCase):
    def test_language_str_uses_name_and_code(self):
        language = Language.objects.create(**language_payload())

        self.assertEqual(str(language), "Uzbek (uz)")
        self.assertTrue(language.is_active)
        self.assertIsNotNone(language.created_at)
        self.assertIsNotNone(language.updated_at)


class LanguagePublicApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.uzbek = Language.objects.create(**language_payload())
        self.turkish = Language.objects.create(
            **language_payload(
                name="Turkish",
                native_name="Türkçe",
                code="tr",
                iso639_3="tur",
                branch="Oghuz",
                writing_system="Latin",
                speakers_count=85000000,
                country="Turkey",
                description="An Oghuz Turkic language.",
                flag_url="https://flagcdn.com/tr.svg",
            )
        )

    def test_public_language_list_is_paginated_and_filterable(self):
        response = self.client.get(reverse("language-list"), {"branch": "Oghuz"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["code"], "tr")

    def test_public_language_detail_is_available_without_authentication(self):
        response = self.client.get(reverse("language-detail", kwargs={"id": self.uzbek.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Uzbek")

    def test_public_search_finds_language_by_country(self):
        response = self.client.get(reverse("language-search"), {"q": "Turkey"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Turkish")

    def test_statistics_endpoint_returns_counts_and_dimensions(self):
        response = self.client.get(reverse("language-statistics"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_languages"], 2)
        self.assertIn("Turkic", response.data["families"])
        self.assertIn("Turkey", response.data["countries"])

    def test_list_cache_is_invalidated_after_admin_create(self):
        first = self.client.get(reverse("language-list"))
        self.assertEqual(first.data["count"], 2)

        admin = User.objects.create_user(
            email="admin@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        self.client.force_authenticate(admin)
        response = self.client.post(
            reverse("admin-language-list"),
            language_payload(
                name="Kazakh",
                native_name="Қазақ тілі",
                code="kk",
                iso639_3="kaz",
                branch="Kipchak",
                country="Kazakhstan",
                speakers_count=17000000,
                flag_url="https://flagcdn.com/kz.svg",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=None)
        second = self.client.get(reverse("language-list"))
        self.assertEqual(second.data["count"], 3)


class LanguageAdminApiTests(APITestCase):
    def setUp(self):
        self.super_admin = User.objects.create_user(
            email="super@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        self.researcher = User.objects.create_user(
            email="researcher@example.com",
            password="StrongPass123",
            role=UserRole.RESEARCHER,
        )
        self.language = Language.objects.create(**language_payload())

    def test_super_admin_can_create_update_and_delete_language(self):
        self.client.force_authenticate(self.super_admin)
        create_response = self.client.post(
            reverse("admin-language-list"),
            language_payload(
                name="Turkmen",
                native_name="Türkmen dili",
                code="tk",
                iso639_3="tuk",
                branch="Oghuz",
                country="Turkmenistan",
                speakers_count=7000000,
                flag_url="https://flagcdn.com/tm.svg",
            ),
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        language_id = create_response.data["id"]
        patch_response = self.client.patch(
            reverse("admin-language-detail", kwargs={"id": language_id}),
            {"description": "Updated description."},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["description"], "Updated description.")

        delete_response = self.client.delete(reverse("admin-language-detail", kwargs={"id": language_id}))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Language.objects.get(id=language_id).is_active)

    def test_researcher_cannot_access_admin_language_write_api(self):
        self.client.force_authenticate(self.researcher)

        response = self.client.post(
            reverse("admin-language-list"),
            language_payload(code="tr", iso639_3="tur"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_seed_languages(self):
        response = self.client.post(reverse("admin-seed-languages"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_super_admin_can_export_json_and_csv(self):
        self.client.force_authenticate(self.super_admin)

        json_response = self.client.get(reverse("admin-language-export"), {"format": "json"})
        self.assertEqual(json_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.data[0]["code"], "uz")

        csv_response = self.client.get(reverse("admin-language-export"), {"format": "csv"})
        self.assertEqual(csv_response.status_code, status.HTTP_200_OK)
        rows = list(csv.DictReader(io.StringIO(csv_response.content.decode("utf-8"))))
        self.assertEqual(rows[0]["code"], "uz")


class LanguageSeedCommandTests(APITestCase):
    def test_seed_languages_command_is_safe_to_rerun(self):
        call_command("seed_languages", verbosity=0)
        self.assertEqual(Language.objects.count(), 7)

        call_command("seed_languages", verbosity=0)
        self.assertEqual(Language.objects.count(), 7)

    def test_seed_languages_command_accepts_custom_path(self):
        data = [
            language_payload(
                name="Kyrgyz",
                native_name="Кыргыз тили",
                code="ky",
                iso639_3="kir",
                branch="Kipchak",
                country="Kyrgyzstan",
                speakers_count=6000000,
                flag_url="https://flagcdn.com/kg.svg",
            )
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            seed_path = Path(tmp_dir) / "languages.json"
            seed_path.write_text(json.dumps(data), encoding="utf-8")
            call_command("seed_languages", path=str(seed_path), verbosity=0)

        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(Language.objects.filter(code="ky").exists())

    def test_super_admin_can_seed_languages_via_api(self):
        super_admin = User.objects.create_user(
            email="seed-admin@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        self.client.force_authenticate(super_admin)

        response = self.client.post(reverse("admin-seed-languages"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["created"], 7)
        self.assertEqual(Language.objects.count(), 7)
