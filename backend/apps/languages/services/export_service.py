import csv
import io

from apps.languages.models import Language
from apps.languages.serializers import LanguageSerializer


class LanguageExportService:
    fields = [
        "id",
        "name",
        "native_name",
        "code",
        "iso639_3",
        "family",
        "branch",
        "writing_system",
        "speakers_count",
        "country",
        "description",
        "flag_url",
        "is_active",
        "created_at",
        "updated_at",
    ]

    @staticmethod
    def as_json(queryset):
        return LanguageSerializer(queryset, many=True).data

    @classmethod
    def as_csv(cls, queryset):
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=cls.fields)
        writer.writeheader()
        for language in queryset:
            row = {field: getattr(language, field) for field in cls.fields}
            row["id"] = str(row["id"])
            row["created_at"] = row["created_at"].isoformat()
            row["updated_at"] = row["updated_at"].isoformat()
            writer.writerow(row)
        return output.getvalue()
