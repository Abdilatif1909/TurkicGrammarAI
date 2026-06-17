from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from apps.analytics.models import QaErrorLog, UsageEvent, UserFeedback
from apps.analytics.qa_error_logger import log_qa_error
from apps.analytics.serializers import QaErrorLogSerializer, UsageEventSerializer, UserFeedbackSerializer


class FeedbackCreateView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Submit user feedback",
        request=UserFeedbackSerializer,
        responses={201: UserFeedbackSerializer, 400: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        serializer = UserFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save()
        if feedback.rating <= 2:
            log_qa_error(
                question=feedback.question,
                retrieved_sources=request.data.get("retrieved_sources", []),
                answer=feedback.answer,
                user_feedback=UserFeedbackSerializer(feedback).data,
            )
        return Response(UserFeedbackSerializer(feedback).data, status=201)


class AdminFeedbackListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer


class AdminQaErrorListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = QaErrorLog.objects.all()
    serializer_class = QaErrorLogSerializer


class UsageStatisticsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Usage statistics",
        parameters=[OpenApiParameter("days", OpenApiTypes.INT, OpenApiParameter.QUERY)],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        since_days = int(request.query_params.get("days") or 30)
        since = timezone.now() - timedelta(days=since_days)
        events = UsageEvent.objects.filter(created_at__gte=since)
        by_type = dict(events.values_list("event_type").annotate(count=Count("id")))
        return Response({
            "days": since_days,
            "total_events": events.count(),
            "events_by_type": by_type,
            "average_response_time_ms": round(events.aggregate(avg=Avg("response_time_ms"))["avg"] or 0, 3),
            "error_rate": self._error_rate(events),
        })

    @staticmethod
    def _error_rate(events):
        total = events.count()
        if not total:
            return 0
        errors = events.filter(status_code__gte=400).count()
        return round(errors / total * 100, 2)


class QaAccuracyTrendsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="QA feedback trends",
        parameters=[OpenApiParameter("days", OpenApiTypes.INT, OpenApiParameter.QUERY)],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        since_days = int(request.query_params.get("days") or 30)
        since = timezone.now() - timedelta(days=since_days)
        feedback = UserFeedback.objects.filter(created_at__gte=since)
        by_rating = dict(feedback.values_list("rating").annotate(count=Count("id")))
        total = feedback.count()
        positive = feedback.filter(rating__gte=4).count()
        return Response({
            "days": since_days,
            "feedback_count": total,
            "average_rating": round(feedback.aggregate(avg=Avg("rating"))["avg"] or 0, 3),
            "positive_feedback_rate": round(positive / total * 100, 2) if total else 0,
            "rating_distribution": by_rating,
        })


class MostRequestedWordsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Most requested words",
        parameters=[OpenApiParameter("limit", OpenApiTypes.INT, OpenApiParameter.QUERY)],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        limit = int(request.query_params.get("limit") or 50)
        rows = (
            UsageEvent.objects.exclude(query="")
            .values("query")
            .annotate(count=Count("id"))
            .order_by("-count", "query")[:limit]
        )
        return Response({"results": list(rows)})


class MostRequestedLanguagesView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="Most requested languages",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        rows = (
            UsageEvent.objects.exclude(language="")
            .values("language")
            .annotate(count=Count("id"))
            .order_by("-count", "language")
        )
        return Response({"results": list(rows)})


class AnalyticsEventListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UsageEvent.objects.all()
    serializer_class = UsageEventSerializer


class AnalyticsHealthView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Analytics health",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        return Response({
            "status": "ok",
            "analytics_events": UsageEvent.objects.count(),
            "feedback_count": UserFeedback.objects.count(),
            "qa_error_count": QaErrorLog.objects.count(),
        })
