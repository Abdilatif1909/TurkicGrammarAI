from apps.words.services.import_service import WordImportService


class WordImportBenchmarkService:
    target_seconds = 120

    @classmethod
    def run(cls, path=None, batch_size=5000) -> dict:
        result = WordImportService(path=path, batch_size=batch_size).run()
        total = int(result["total"])
        elapsed = float(result["elapsed_seconds"])
        rows_per_second = round(total / elapsed, 2) if elapsed else total
        result["rows_per_second"] = rows_per_second
        result["target_seconds"] = cls.target_seconds
        result["meets_target"] = elapsed <= cls.target_seconds
        return result
