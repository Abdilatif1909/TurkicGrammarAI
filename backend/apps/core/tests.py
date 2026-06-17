from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("apps.core.views.redis.Redis.from_url")
    def test_health_endpoint_returns_database_and_redis_status(self, redis_from_url):
        redis_from_url.return_value.ping.return_value = True

        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
        self.assertTrue(response.data["database"])
        self.assertTrue(response.data["redis"])
