from django.conf import settings
from django.db import connection
from django.db.utils import OperationalError
import redis
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiTypes


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Health check",
        description="Return service health including DB and Redis connection status.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(
            {
                "status": "ok",
                "database": self._database_is_available(),
                "redis": self._redis_is_available(),
            }
        )

    @staticmethod
    def _database_is_available() -> bool:
        try:
            connection.ensure_connection()
            return True
        except OperationalError:
            return False

    @staticmethod
    def _redis_is_available() -> bool:
        try:
            client = redis.Redis.from_url(settings.REDIS_URL, socket_connect_timeout=1)
            return bool(client.ping())
        except redis.RedisError:
            return False
