import csv
import io

from apps.words.serializers import WordSerializer


class WordExportService:
    fields = [
        "id",
        "language_code",
        "word",
        "lemma",
        "root",
        "pos",
        "ipa",
        "meaning",
        "frequency",
        "source",
        "notes",
        "created_at",
        "updated_at",
    ]

    @staticmethod
    def as_json(queryset):
        return WordSerializer(queryset, many=True).data

    @classmethod
    def as_csv(cls, queryset):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cls.fields)
        writer.writeheader()
        for word in queryset:
            writer.writerow(
                {
                    "id": str(word.id),
                    "language_code": word.language.code,
                    "word": word.word,
                    "lemma": word.lemma,
                    "root": word.root,
                    "pos": word.pos,
                    "ipa": word.ipa,
                    "meaning": word.meaning,
                    "frequency": word.frequency,
                    "source": word.source,
                    "notes": word.notes,
                    "created_at": word.created_at.isoformat(),
                    "updated_at": word.updated_at.isoformat(),
                }
            )
        return output.getvalue()
