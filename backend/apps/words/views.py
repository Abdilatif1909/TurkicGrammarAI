from django.core.cache import cache
from django.http import HttpResponse
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import generics, status
from apps.core.serializers import ActionResultSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsSuperAdmin
from apps.words.models import Word
from apps.words.serializers import WordSerializer, WordWriteSerializer
from apps.words.services.benchmark_service import WordImportBenchmarkService
from apps.words.services.export_service import WordExportService
from apps.words.services.import_service import WordImportService
from apps.words.services.validation_service import DatasetQualityService
from apps.words.services.word_service import WORD_CACHE_TIMEOUT, WordService

WORD_FILTER_PARAMETERS = [
    OpenApiParameter("language", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Language UUID or code."),
    OpenApiParameter("language_code", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Language code."),
    OpenApiParameter("pos", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Part of speech."),
    OpenApiParameter("source", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Dataset source."),
]





@extend_schema(tags=["Words"], parameters=WORD_FILTER_PARAMETERS)
class WordListView(generics.ListAPIView):
    serializer_class = WordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return WordService.filtered_queryset(self.request.query_params)

    def list(self, request, *args, **kwargs):
        cache_key = WordService.list_cache_key(request.query_params)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, WORD_CACHE_TIMEOUT)
        return response


@extend_schema(tags=["Words"])
class WordDetailView(generics.RetrieveAPIView):
    serializer_class = WordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "id"
    queryset = WordService.queryset()

    def retrieve(self, request, *args, **kwargs):
        cache_key = WordService.detail_cache_key(kwargs["id"])
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, WORD_CACHE_TIMEOUT)
        return response


@extend_schema(
    tags=["Words"],
    parameters=[OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Search text.")],
)
class WordSearchView(generics.ListAPIView):
    serializer_class = WordSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return WordService.search(self.request.query_params.get("q", ""))


@extend_schema(tags=["Words"])
class WordStatisticsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Word statistics",
        description="Return aggregated statistics about words and datasets.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(WordService.statistics())


@extend_schema(tags=["Words"])
class WordQualityView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Dataset quality summary",
        description="Return dataset quality metrics used by the word validation service.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(DatasetQualityService().summary())


@extend_schema(tags=["Admin Words"], parameters=WORD_FILTER_PARAMETERS)
class AdminWordListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        return WordService.filtered_queryset(self.request.query_params)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WordWriteSerializer
        return WordSerializer

    def perform_create(self, serializer):
        serializer.instance = WordService.create(serializer.validated_data)


@extend_schema(tags=["Admin Words"])
class AdminWordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordWriteSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    lookup_field = "id"
    queryset = Word.objects.select_related("language").all()

    def perform_update(self, serializer):
        serializer.instance = WordService.update(self.get_object(), serializer.validated_data)

    def destroy(self, request, *args, **kwargs):
        WordService.delete(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Admin Words"],
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
class AdminWordExportView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    @extend_schema(
        summary="Export words",
        description="Export filtered words in CSV or JSON. Query params mirror the list endpoint.",
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
        queryset = WordService.filtered_queryset(request.query_params).order_by("language__name", "word")
        if export_format == "csv":
            response = HttpResponse(WordExportService.as_csv(queryset), content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="words.csv"'
            return response
        if export_format == "json":
            return Response(WordExportService.as_json(queryset))
        return Response({"detail": "Unsupported export format."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Admin Seed"])
class AdminSeedWordsView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = ActionResultSerializer

    @extend_schema(
        summary="Seed words",
        description="Run word import/seeding job. Returns a summary object with counts and status.",
        responses={200: ActionResultSerializer},
    )
    def post(self, request):
        result = WordImportService().run()
        return Response(result, status=status.HTTP_200_OK)


@extend_schema(tags=["Admin Benchmarks"])
class AdminWordImportBenchmarkView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = ActionResultSerializer

    @extend_schema(
        summary="Run word import benchmark",
        description="Execute benchmark routine for word import and return timings/metrics.",
        responses={200: ActionResultSerializer},
    )
    def post(self, request):
        result = WordImportBenchmarkService.run()
        return Response(result, status=status.HTTP_200_OK)
