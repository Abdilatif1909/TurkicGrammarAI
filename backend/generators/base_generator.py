import json
from pathlib import Path
import random
from typing import Any


class BaseDatasetGenerator:
    """Base class for deterministic, reusable dataset generators."""

    def __init__(self, output_dir: str | Path, seed: int = 42):
        self.output_dir = Path(output_dir)
        self.random = random.Random(seed)

    def ensure_output_dir(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_json(self, filename: str, records: list[dict[str, Any]]) -> Path:
        self.ensure_output_dir()
        path = self.output_dir / filename
        with path.open("w", encoding="utf-8") as output:
            json.dump(records, output, ensure_ascii=False, indent=2)
        return path

    def generate(self, *args, **kwargs):
        raise NotImplementedError("Generators must implement generate().")
