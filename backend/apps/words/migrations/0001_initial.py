# Generated for TurkicGrammarAI Phase 3 words module.

import django.db.models.deletion
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("languages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Word",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("word", models.CharField(max_length=255)),
                ("lemma", models.CharField(max_length=255)),
                ("root", models.CharField(blank=True, max_length=255)),
                ("pos", models.CharField(choices=[("NOUN", "Noun"), ("VERB", "Verb"), ("ADJECTIVE", "Adjective"), ("ADVERB", "Adverb"), ("PRONOUN", "Pronoun"), ("NUMERAL", "Numeral"), ("POSTPOSITION", "Postposition"), ("CONJUNCTION", "Conjunction"), ("PARTICLE", "Particle"), ("INTERJECTION", "Interjection")], db_index=True, max_length=32)),
                ("ipa", models.CharField(blank=True, max_length=255)),
                ("meaning", models.TextField()),
                ("frequency", models.PositiveIntegerField(db_index=True, default=0)),
                ("source", models.CharField(blank=True, db_index=True, max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("language", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="words", to="languages.language")),
            ],
            options={
                "ordering": ["language__name", "word"],
                "indexes": [
                    models.Index(fields=["language", "word"], name="words_language_word_idx"),
                    models.Index(fields=["language", "lemma"], name="words_language_lemma_idx"),
                    models.Index(fields=["language", "pos"], name="words_language_pos_idx"),
                    models.Index(fields=["source"], name="words_source_idx"),
                ],
            },
        ),
    ]
