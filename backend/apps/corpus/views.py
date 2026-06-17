from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiTypes
from apps.corpus.services.statistics import CorpusStatistics


class CorpusStatisticsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Corpus statistics",
        description="Return corpus-level aggregated statistics (documents, sentences, tokens).",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        data = CorpusStatistics.summary()
        return Response(data)
