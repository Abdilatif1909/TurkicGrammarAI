from django.core.management.base import BaseCommand, CommandError

from apps.words.services.import_service import WordImportService


class Command(BaseCommand):
    help = "Seed generated word datasets using batched bulk inserts."

    def add_arguments(self, parser):
        parser.add_argument("--path", default=None, help="Optional JSON file or directory path.")
        parser.add_argument("--batch-size", type=int, default=5000, help="Bulk create batch size.")

    def handle(self, *args, **options):
        try:
            result = WordImportService(path=options.get("path"), batch_size=options["batch_size"]).run()
        except (FileNotFoundError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        if options.get("verbosity", 1) > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "Words seed completed: "
                    f"{result['created']} created, {result['skipped']} skipped, "
                    f"{result['total']} total in {result['elapsed_seconds']}s."
                )
            )
