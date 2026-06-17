import json
from pathlib import Path
from typing import Any


class BaseSeeder:
    """Shared JSON seed loader for safe, repeatable seed commands."""

    default_path: Path | None = None

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else self.default_path
        if self.path is None:
            raise ValueError("A seed file path is required.")

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            raise FileNotFoundError(f"Seed file not found: {self.path}")
        with self.path.open("r", encoding="utf-8") as seed_file:
            data = json.load(seed_file)
        if not isinstance(data, list):
            raise ValueError("Seed file must contain a JSON list.")
        return data

    def run(self) -> dict[str, int]:
        raise NotImplementedError("Seeders must implement run().")
