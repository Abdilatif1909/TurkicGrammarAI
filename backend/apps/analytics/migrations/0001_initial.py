from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="QaErrorLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.TextField()),
                ("retrieved_sources", models.JSONField(blank=True, default=list)),
                ("answer", models.TextField(blank=True)),
                ("user_feedback", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="UserFeedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.TextField()),
                ("answer", models.TextField(blank=True)),
                ("rating", models.PositiveSmallIntegerField()),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="UsageEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(choices=[("search", "Search query"), ("qa", "QA question"), ("morphology", "Morphology request"), ("cognate", "Cognate lookup"), ("historical", "Historical lookup"), ("rag", "RAG retrieval"), ("other", "Other")], db_index=True, max_length=32)),
                ("query", models.TextField(blank=True)),
                ("language", models.CharField(blank=True, db_index=True, max_length=16)),
                ("path", models.CharField(blank=True, max_length=255)),
                ("method", models.CharField(blank=True, max_length=12)),
                ("status_code", models.PositiveIntegerField(default=0)),
                ("response_time_ms", models.FloatField(default=0)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["event_type", "created_at"], name="analytics_u_event_t_6dc5b0_idx"),
                    models.Index(fields=["language", "created_at"], name="analytics_u_languag_dfa80c_idx"),
                ],
            },
        ),
    ]
