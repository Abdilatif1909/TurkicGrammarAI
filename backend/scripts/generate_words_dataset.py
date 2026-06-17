import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

import django  # noqa: E402

django.setup()

from generators.word_generator import DEFAULT_WORD_TARGETS, WordDatasetGenerator  # noqa: E402


def parse_targets(size: int | None) -> dict[str, int]:
    if size is None:
        return DEFAULT_WORD_TARGETS
    language_count = len(DEFAULT_WORD_TARGETS)
    base = size // language_count
    remainder = size % language_count
    targets = {}
    for index, code in enumerate(DEFAULT_WORD_TARGETS):
        targets[code] = base + (1 if index < remainder else 0)
    return targets


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic Turkic word datasets.")
    parser.add_argument("--size", type=int, default=None, help="Total target record count. Defaults to 60,000.")
    parser.add_argument("--output-dir", default=None, help="Output directory for generated JSON files.")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed.")
    args = parser.parse_args()

    summary = WordDatasetGenerator(output_dir=args.output_dir, seed=args.seed).generate(parse_targets(args.size))
    for filename, count in summary.items():
        print(f"{filename}: {count}")


if __name__ == "__main__":
    main()
