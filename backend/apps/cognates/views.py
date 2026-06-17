from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from apps.cognates.models import CognateSet
from .serializers import CognateSetSerializer
from apps.cognates.services.cognate_service import CognateService
from apps.cognates.services.universal_cognates import UniversalCognateService


class CognateListView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CognateSet.objects.all()
    serializer_class = CognateSetSerializer


class CognateDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CognateSet.objects.all()
    serializer_class = CognateSetSerializer


class CognateSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Cognate search",
        description="Search for cognate sets by word and optional language filter.",
        parameters=[
            OpenApiParameter("word", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Search word"),
            OpenApiParameter("language", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Language code or UUID"),
        ],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        word = request.query_params.get('word')
        language = request.query_params.get('language')
        results = CognateService.comparative_search(word=word, language=language)
        return Response(results)


class UniversalCognateSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Universal cross-language cognate search",
        description="Search unified Turkic cognate groups across Uzbek, Turkish, Azerbaijani, Kazakh, Kyrgyz, Turkmen, Uyghur, and Old Turkic.",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Search form, e.g. tangri"),
            OpenApiParameter("word", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Alias for q"),
            OpenApiParameter("language", OpenApiTypes.STR, OpenApiParameter.QUERY, description="Optional source language code"),
            OpenApiParameter("limit", OpenApiTypes.INT, OpenApiParameter.QUERY, description="Maximum result count"),
        ],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        query = request.query_params.get("q") or request.query_params.get("word")
        language = request.query_params.get("language")
        try:
            limit = int(request.query_params.get("limit") or 10)
        except ValueError:
            limit = 10
        results = UniversalCognateService.search(query=query, language=language, limit=limit)
        return Response({"query": query, "results": results})


class CognateStatisticsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Cognates statistics",
        description="Return aggregated statistics about cognate sets and entries.",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        data = CognateService.get_statistics()
        return Response(data)
