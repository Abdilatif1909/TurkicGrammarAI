from django.http import HttpResponse
from django.core.cache import cache
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsSuperAdmin

from .models import Language
from .serializers import LanguageSerializer, LanguageWriteSerializer
from .services.export_service import LanguageExportService
from .services.import_service import LanguageImportService
from .services.language_service import LANGUAGE_CACHE_TIMEOUT, LanguageService

FILTER_PARAMETERS = [
    OpenApiParameter("code", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Filter by language code."),
    OpenApiParameter("family", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Filter by language family."),
    OpenApiParameter("branch", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Filter by language branch."),
    OpenApiParameter("country", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Filter by country."),
]


from apps.core.serializers import ActionResultSerializer


@extend_schema(tags=["Languages"], parameters=FILTER_PARAMETERS)
class LanguageListView(generics.ListAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return LanguageService.filtered_queryset(self.request.query_params)

    def list(self, request, *args, **kwargs):
        cache_key = LanguageService.list_cache_key(request.query_params)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, LANGUAGE_CACHE_TIMEOUT)
        return response


@extend_schema(tags=["Languages"])
class LanguageDetailView(generics.RetrieveAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "id"

    def get_queryset(self):
        return LanguageService.active_queryset()

    def retrieve(self, request, *args, **kwargs):
        cache_key = LanguageService.detail_cache_key(kwargs["id"])
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, LANGUAGE_CACHE_TIMEOUT)
        return response


@extend_schema(
    tags=["Languages"],
    parameters=[
        OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Search text.")
    ],
)
class LanguageSearchView(generics.ListAPIView):
    serializer_class = LanguageSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return LanguageService.search(self.request.query_params.get("q", ""))


@extend_schema(tags=["Languages"])
class LanguageStatisticsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Language statistics",
        description="Return aggregated statistics about languages (counts, families, etc).",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(LanguageService.statistics())


@extend_schema(tags=["Admin Languages"], parameters=FILTER_PARAMETERS)
class AdminLanguageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        return LanguageService.filtered_queryset(self.request.query_params)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return LanguageWriteSerializer
        return LanguageSerializer

    def perform_create(self, serializer):
        serializer.instance = LanguageService.create(serializer.validated_data)


@extend_schema(tags=["Admin Languages"])
class AdminLanguageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LanguageWriteSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    lookup_field = "id"
    queryset = Language.objects.all()

    def perform_update(self, serializer):
        serializer.instance = LanguageService.update(self.get_object(), serializer.validated_data)

    def destroy(self, request, *args, **kwargs):
        language = self.get_object()
        LanguageService.deactivate(language)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Admin Languages"],
    parameters=[
        OpenApiParameter(
            "format",
            OpenApiTypes.STR,
            OpenApiParameter.QUERY,
            enum=["json", "csv"],
            description="Export format.",
        )
    ],
)
class AdminLanguageExportView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    @extend_schema(
        summary="Export languages",
        description="Export all languages in CSV or JSON format. Use `?format=csv` or `?format=json`.",
        parameters=[
            OpenApiParameter(
                "format",
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                enum=["json", "csv"],
                description="Export format.",
            )
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        export_format = request.query_params.get("format", "json").lower()
        queryset = Language.objects.all().order_by("name")

        if export_format == "csv":
            content = LanguageExportService.as_csv(queryset)
            response = HttpResponse(content, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="languages.csv"'
            return response
        if export_format == "json":
            return Response(LanguageExportService.as_json(queryset))
        return Response({"detail": "Unsupported export format."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Admin Seed"])
class AdminSeedLanguagesView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = ActionResultSerializer

    @extend_schema(
        summary="Seed languages",
        description="Run language import/seeding job. Returns a summary object with counts and status.",
        responses={200: ActionResultSerializer},
    )
    def post(self, request):
        result = LanguageImportService().run()
        return Response(result, status=status.HTTP_200_OK)
