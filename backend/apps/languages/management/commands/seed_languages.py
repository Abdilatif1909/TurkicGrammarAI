from django.core.management.base import BaseCommand, CommandError

from apps.languages.services.import_service import LanguageImportService


class Command(BaseCommand):
    help = "Seed Turkic language metadata from JSON."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=None,
            help="Optional path to a languages JSON file.",
        )

    def handle(self, *args, **options):
        try:
            result = LanguageImportService(path=options.get("path")).run()
        except (FileNotFoundError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        if options.get("verbosity", 1) > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "Languages seed completed: "
                    f"{result['created']} created, {result['skipped']} skipped, {result['total']} total."
                )
            )
