from typing import Any, Dict, List

from apps.analytics.models import QaErrorLog


def log_qa_error(question: str, retrieved_sources: List[Dict[str, Any]], answer: str, user_feedback: Dict[str, Any] | None = None) -> QaErrorLog:
    return QaErrorLog.objects.create(
        question=question,
        retrieved_sources=retrieved_sources or [],
        answer=answer or "",
        user_feedback=user_feedback or {},
    )
