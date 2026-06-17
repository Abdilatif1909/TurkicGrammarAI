from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from apps.embeddings.fasttext_service import model_status, nearest_neighbors, similarity, warm_fasttext_model
from apps.embeddings.semantic_search import semantic_search
from apps.embeddings.turkic_qa import ask
from apps.embeddings.turkic_retriever import retrieve


class EmbeddingSimilarityView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Embedding similarity",
        parameters=[
            OpenApiParameter("word_a", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("word_b", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        word_a = request.query_params.get("word_a")
        word_b = request.query_params.get("word_b")
        if not word_a or not word_b:
            return Response({"error": "word_a and word_b are required"}, status=400)
        try:
            return Response(similarity(word_a, word_b))
        except FileNotFoundError:
            return Response({"error": "FastText model is not trained yet"}, status=503)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)


class EmbeddingNeighborsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Embedding nearest neighbors",
        parameters=[
            OpenApiParameter("word", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("topn", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        word = request.query_params.get("word")
        if not word:
            return Response({"error": "word is required"}, status=400)
        try:
            topn = int(request.query_params.get("topn") or 20)
        except ValueError:
            topn = 20
        try:
            return Response(nearest_neighbors(word, topn=topn))
        except FileNotFoundError:
            return Response({"error": "FastText model is not trained yet"}, status=503)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)


class SemanticSearchView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Semantic search",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("topn", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        query = request.query_params.get("q") or request.query_params.get("query")
        if not query:
            return Response({"error": "q is required"}, status=400)
        try:
            topn = int(request.query_params.get("topn") or 20)
        except ValueError:
            topn = 20
        try:
            return Response(semantic_search(query, topn=topn))
        except FileNotFoundError as exc:
            return Response({"error": f"Semantic search asset missing: {exc}"}, status=503)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)


class TurkicRagRetrieveView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Turkic RAG retrieval",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("topn", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        query = request.query_params.get("q") or request.query_params.get("query")
        if not query:
            return Response({"error": "q is required"}, status=400)
        try:
            topn = int(request.query_params.get("topn") or 20)
        except ValueError:
            topn = 20
        try:
            return Response(retrieve(query, topn=topn))
        except FileNotFoundError as exc:
            return Response({"error": f"RAG retrieval asset missing: {exc}"}, status=503)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)


class TurkicQaAskView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Retrieval-based Turkic QA",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
            OpenApiParameter("topk", OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        question = request.query_params.get("q") or request.query_params.get("question")
        if not question:
            return Response({"error": "q is required"}, status=400)
        try:
            topk = int(request.query_params.get("topk") or 10)
        except ValueError:
            topk = 10
        try:
            return Response(ask(question, topk=topk))
        except FileNotFoundError as exc:
            return Response({"error": f"QA asset missing: {exc}"}, status=503)
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)


class EmbeddingWarmStartView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Warm FastText model cache",
        responses={200: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        try:
            status = warm_fasttext_model()
            semantic_search("kitob", topn=1)
            status["semantic_search_primed"] = True
            return Response(status)
        except FileNotFoundError:
            return Response({"error": "FastText model is not trained yet"}, status=503)


class EmbeddingModelStatusView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="FastText model cache status",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response(model_status())
