import logging
import time

from django.utils.deprecation import MiddlewareMixin

from apps.analytics.models import UsageEvent

logger = logging.getLogger("analytics.request")


TRACKED_ENDPOINTS = [
    ("/api/search/semantic/", UsageEvent.SEARCH),
    ("/api/qa/ask/", UsageEvent.QA),
    ("/api/morphology/", UsageEvent.MORPHOLOGY),
    ("/api/cognates/", UsageEvent.COGNATE),
    ("/api/historical/", UsageEvent.HISTORICAL),
    ("/api/rag/retrieve/", UsageEvent.RAG),
]


class AnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._analytics_started_at = time.perf_counter()

    def process_response(self, request, response):
        event_type = self._event_type(request.path)
        if not event_type:
            return response
        elapsed = (time.perf_counter() - getattr(request, "_analytics_started_at", time.perf_counter())) * 1000
        query = request.GET.get("q") or request.GET.get("query") or request.GET.get("word") or request.POST.get("question", "")
        language = request.GET.get("language") or request.GET.get("lang") or ""
        try:
            UsageEvent.objects.create(
                event_type=event_type,
                query=query,
                language=language,
                path=request.path,
                method=request.method,
                status_code=getattr(response, "status_code", 0),
                response_time_ms=round(elapsed, 3),
                user=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
                ip_address=self._client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                metadata={"params": dict(request.GET.lists())},
            )
        except Exception as exc:
            logger.warning("analytics event write failed: %s", exc)
        return response

    @staticmethod
    def _event_type(path):
        for prefix, event_type in TRACKED_ENDPOINTS:
            if path.startswith(prefix):
                return event_type
        return ""

    @staticmethod
    def _client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
