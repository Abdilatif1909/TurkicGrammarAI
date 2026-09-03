"""Quick similarity sanity checks for the trained FastText model."""

from __future__ import annotations

from pathlib import Path
import sys

from gensim.models import FastText


PAIRS = [
    ("baş", "bosh"),
    ("kitab", "kitob"),
    ("söz", "so‘z"),
    ("ayak", "ayaq"),
    ("bilim", "білім"),
]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    project_root = Path(__file__).resolve().parents[2]
    model_path = project_root / "models" / "turkic_fasttext.model"
    model = FastText.load(str(model_path))

    for left, right in PAIRS:
        similarity = model.wv.similarity(left, right)
        print(f"{left}\t{right}\t{similarity:.6f}")


if __name__ == "__main__":
    main()
