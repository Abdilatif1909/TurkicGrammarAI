import csv
import json
from pathlib import Path
from ..models import HistoricalForm


class ExportService:
    @staticmethod
    def export_json(path: str | Path):
        path = Path(path)
        qs = HistoricalForm.objects.all().values()
        data = list(qs)
        with path.open('w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return path

    @staticmethod
    def export_csv(path: str | Path):
        path = Path(path)
        qs = HistoricalForm.objects.all().values()
        if not qs:
            path.write_text('')
            return path
        keys = qs[0].keys()
        with path.open('w', encoding='utf-8', newline='') as fh:
            writer = csv.DictWriter(fh, fieldnames=keys)
            writer.writeheader()
            for row in qs:
                writer.writerow(row)
        return path
