from django.core.management.base import BaseCommand, CommandError

from generators.word_generator import DEFAULT_WORD_TARGETS, WordDatasetGenerator


class Command(BaseCommand):
    help = "Generate scalable synthetic Turkic word JSON datasets."

    def add_arguments(self, parser):
        parser.add_argument("--size", type=int, default=None, help="Total record count. Defaults to 60,000.")
        parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON files.")
        parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed.")

    def handle(self, *args, **options):
        size = options.get("size")
        if size is not None and size <= 0:
            raise CommandError("--size must be greater than zero.")

        targets = self._targets(size)
        summary = WordDatasetGenerator(output_dir=options.get("output_dir"), seed=options["seed"]).generate(targets)

        if options.get("verbosity", 1) > 0:
            total = sum(summary.values())
            self.stdout.write(self.style.SUCCESS(f"Generated {total} word records."))
            for filename, count in summary.items():
                self.stdout.write(f"{filename}: {count}")

    @staticmethod
    def _targets(size: int | None) -> dict[str, int]:
        if size is None:
            return DEFAULT_WORD_TARGETS
        codes = list(DEFAULT_WORD_TARGETS)
        base = size // len(codes)
        remainder = size % len(codes)
        return {code: base + (1 if index < remainder else 0) for index, code in enumerate(codes)}
