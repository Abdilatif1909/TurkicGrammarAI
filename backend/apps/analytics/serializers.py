from rest_framework import serializers

from apps.analytics.models import QaErrorLog, UsageEvent, UserFeedback


class UsageEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageEvent
        fields = [
            "id",
            "event_type",
            "query",
            "language",
            "path",
            "method",
            "status_code",
            "response_time_ms",
            "ip_address",
            "metadata",
            "created_at",
        ]
        read_only_fields = fields


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = ["id", "question", "answer", "rating", "comment", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be between 1 and 5")
        return value


class QaErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaErrorLog
        fields = ["id", "question", "retrieved_sources", "answer", "user_feedback", "created_at"]
        read_only_fields = fields
