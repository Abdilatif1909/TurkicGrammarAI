from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import UserRole
from apps.core.permissions import IsResearcher, IsStudent, IsSuperAdmin

User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_user_can_register_login_refresh_and_view_profile(self):
        register_payload = {
            "email": "student@example.com",
            "password": "StrongPass123",
            "first_name": "Test",
            "last_name": "Student",
            "role": UserRole.STUDENT,
        }

        register_response = self.client.post(reverse("auth-register"), register_payload, format="json")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            reverse("auth-login"),
            {"email": "student@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

        refresh_response = self.client.post(
            reverse("auth-refresh"),
            {"refresh": login_response.data["refresh"]},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        profile_response = self.client.get(reverse("auth-profile"))
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["user"]["email"], "student@example.com")

    def test_profile_can_be_updated(self):
        user = User.objects.create_user(email="researcher@example.com", password="StrongPass123")
        self.client.force_authenticate(user)

        response = self.client.patch(
            reverse("auth-profile"),
            {
                "user": {"first_name": "Ayla", "last_name": "Researcher"},
                "institution": "Turkic Linguistics Lab",
                "research_area": "Comparative morphology",
                "bio": "Research profile",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Ayla")
        self.assertEqual(user.profile.institution, "Turkic Linguistics Lab")

    def test_super_admin_cannot_be_self_registered(self):
        response = self.client.post(
            reverse("auth-register"),
            {
                "email": "admin@example.com",
                "password": "StrongPass123",
                "role": UserRole.SUPER_ADMIN,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PermissionTests(APITestCase):
    def test_role_permissions_match_user_roles(self):
        super_admin = User.objects.create_user(
            email="super@example.com",
            password="StrongPass123",
            role=UserRole.SUPER_ADMIN,
        )
        researcher = User.objects.create_user(
            email="research@example.com",
            password="StrongPass123",
            role=UserRole.RESEARCHER,
        )
        student = User.objects.create_user(
            email="student2@example.com",
            password="StrongPass123",
            role=UserRole.STUDENT,
        )

        class Request:
            def __init__(self, user):
                self.user = user

        self.assertTrue(IsSuperAdmin().has_permission(Request(super_admin), None))
        self.assertTrue(IsResearcher().has_permission(Request(researcher), None))
        self.assertTrue(IsStudent().has_permission(Request(student), None))
        self.assertFalse(IsSuperAdmin().has_permission(Request(student), None))
        self.assertFalse(IsResearcher().has_permission(Request(student), None))
