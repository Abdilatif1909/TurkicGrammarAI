from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from apps.morphology.services.morphology_service import analyze, batch_analyze
from apps.morphology.services.universal_morphology import are_equivalent, detect_language, universal_analyze
from apps.morphology.models import MorphologicalRule, MorphologicalAnalysis
from apps.morphology.serializers import MorphologyAnalysesResponseSerializer


def _suffix_chain(analysis):
    chain = []
    for item in analysis.get("suffixes", []):
        if isinstance(item, dict):
            chain.append(item.get("suffix"))
        else:
            chain.append(item)
    return [s for s in chain if s]


class AnalyzeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Analyze morphology",
        parameters=[
            OpenApiParameter("word", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("language", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
        ],
        responses={200: MorphologyAnalysesResponseSerializer, 400: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        word = request.GET.get("word")
        lang = request.GET.get("language")
        if not word or not lang:
            return Response({"detail": "word and language required"}, status=400)
        analyses = analyze(word, lang)
        # Persist the top analysis if available
        if analyses:
            top = analyses[0]
            MorphologicalAnalysis.objects.create(
                language=lang,
                surface_form=word,
                root=top["root"],
                lemma=top["lemma"],
                suffix_chain=_suffix_chain(top),
                analysis_json=top,
            )
        return Response({"analyses": analyses})


class BatchAnalyzeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Batch morphology analysis",
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        words = request.data.get("words") or request.data.get("items")
        lang = request.data.get("language")
        if not words or not lang:
            return Response({"detail": "words and language required"}, status=400)
        results = batch_analyze(words, lang)
        instances = []
        for res in results:
            if res:
                top = res[0]
                instances.append(
                    MorphologicalAnalysis(
                        language=lang,
                        surface_form=top["lemma"],
                        root=top["root"],
                        lemma=top["lemma"],
                        suffix_chain=_suffix_chain(top),
                        analysis_json=top,
                    )
                )
        if instances:
            MorphologicalAnalysis.objects.bulk_create(instances)
        return Response({"analyses": results})


class UniversalAnalyzeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Universal morphology analysis or equivalence check",
        parameters=[
            OpenApiParameter("word", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("language", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("word_a", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("word_b", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("language_a", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("language_b", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        word = request.GET.get("word")
        lang = request.GET.get("language")
        word_a = request.GET.get("word_a") or request.GET.get("left")
        word_b = request.GET.get("word_b") or request.GET.get("right")
        lang_a = request.GET.get("language_a") or request.GET.get("lang_a")
        lang_b = request.GET.get("language_b") or request.GET.get("lang_b")

        if word_a and word_b:
            lang_a = lang_a or detect_language(word_a)
            lang_b = lang_b or detect_language(word_b)
            if not lang_a or not lang_b:
                return Response({"detail": "language_a and language_b required when language cannot be detected"}, status=400)
            left = universal_analyze(word_a, lang_a)
            right = universal_analyze(word_b, lang_b)
            return Response(are_equivalent(left, right))

        if not word:
            return Response({"detail": "word required"}, status=400)
        lang = lang or detect_language(word)
        if not lang:
            return Response({"detail": "language required when language cannot be detected"}, status=400)
        return Response({"analysis": universal_analyze(word, lang).to_dict()})


class StatisticsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary="Morphology statistics",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        rules_count = MorphologicalRule.objects.count()
        analyses_count = MorphologicalAnalysis.objects.count()
        return Response({"rules": rules_count, "analyses": analyses_count})
