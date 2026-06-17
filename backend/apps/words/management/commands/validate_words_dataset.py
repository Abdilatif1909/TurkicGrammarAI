from django.core.management.base import BaseCommand, CommandError

from apps.words.services.validation_service import LANGUAGE_STEMS, DatasetValidationService


class Command(BaseCommand):
    help = "Validate and normalize Turkic word datasets, writing reports and clean files."

    def add_arguments(self, parser):
        parser.add_argument("--words-dir", default=None, help="Input directory of raw word datasets.")
        parser.add_argument("--reports-dir", default=None, help="Output directory for validation reports.")
        parser.add_argument("--normalized-dir", default=None, help="Output directory for normalized datasets.")
        parser.add_argument(
            "--language",
            action="append",
            choices=sorted(LANGUAGE_STEMS),
            help="Limit validation to specific language code(s). Repeatable.",
        )

    def handle(self, *args, **options):
        service = DatasetValidationService(
            words_dir=options.get("words_dir"),
            reports_dir=options.get("reports_dir"),
            normalized_dir=options.get("normalized_dir"),
        )
        try:
            summary = service.run(languages=options.get("language"))
        except (FileNotFoundError, ValueError) as exc:
            raise CommandError(str(exc)) from exc

        if options.get("verbosity", 1) > 0:
            for code, report in summary.items():
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{code}: {report['valid_records']}/{report['total_records']} valid "
                        f"({report['validation_score']}%), "
                        f"{report['duplicates_removed']} duplicates, "
                        f"{report['invalid_forms_removed']} invalid forms removed."
                    )
                )
