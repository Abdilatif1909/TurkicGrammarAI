from django.core.management.base import BaseCommand, CommandError

from apps.words.services.benchmark_service import WordImportBenchmarkService


class Command(BaseCommand):
    help = "Benchmark word import throughput against the 60,000 records under 2 minutes target."

    def add_arguments(self, parser):
        parser.add_argument("--path", default=None, help="Optional JSON file or directory path.")
        parser.add_argument("--batch-size", type=int, default=5000, help="Bulk create batch size.")

    def handle(self, *args, **options):
        try:
            result = WordImportBenchmarkService.run(path=options.get("path"), batch_size=options["batch_size"])
        except (FileNotFoundError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {result['created']} created / {result['total']} total in "
                f"{result['elapsed_seconds']}s ({result['rows_per_second']} rows/s). "
                f"Target met: {result['meets_target']}"
            )
        )
