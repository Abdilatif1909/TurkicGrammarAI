# Generated for TurkicGrammarAI Phase 2 languages module.

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("name", models.CharField(max_length=120)),
                ("native_name", models.CharField(max_length=120)),
                ("code", models.CharField(db_index=True, max_length=16, unique=True)),
                ("iso639_3", models.CharField(max_length=3, unique=True)),
                ("family", models.CharField(db_index=True, max_length=120)),
                ("branch", models.CharField(db_index=True, max_length=120)),
                ("writing_system", models.CharField(max_length=255)),
                ("speakers_count", models.PositiveBigIntegerField(default=0)),
                ("country", models.CharField(db_index=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("flag_url", models.URLField(blank=True)),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["code", "is_active"], name="languages_l_code_ff2ad2_idx"),
                    models.Index(fields=["family", "branch"], name="languages_l_family_06bf3f_idx"),
                    models.Index(fields=["country"], name="languages_l_country_31221b_idx"),
                ],
            },
        ),
    ]
