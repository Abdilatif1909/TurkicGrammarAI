"""Generate FastText training corpus from the full lexicon."""

from __future__ import annotations

import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def corpus_line(entry: dict) -> str:
    tokens = [entry["surface_form"], f"LANG_{entry['language']}"]

    lemma = entry.get("lemma")
    if lemma and lemma != entry["surface_form"]:
        tokens.append(lemma)

    tokens.extend(entry.get("cognate_ids", []))
    tokens.extend(entry.get("lineage_ids", []))

    pos = entry.get("pos")
    if pos:
        tokens.append(f"POS_{pos}")

    return " ".join(tokens)


def build_corpus(entries: list[dict]) -> list[str]:
    return [corpus_line(entry) for entry in entries]


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for line in lines:
            handle.write(line)
            handle.write("\n")


def write_format_doc(path: Path, lines: list[str]) -> None:
    examples = lines[:5]
    content = [
        "# FastText Corpus Format",
        "",
        "Stage: Bosqich 5 - FastText training corpus",
        "",
        "Each line in `data/processed/fasttext_corpus.txt` is one training sentence derived from one `LexicalEntry` in `lexicon_master_full.jsonl`.",
        "",
        "Token order:",
        "",
        "1. `surface_form`",
        "2. `LANG_<language>`",
        "3. `lemma`, only when `lemma != surface_form`",
        "4. zero or more `COGNATE_<id>` tokens",
        "5. zero or more `LINEAGE_<id>` tokens",
        "6. `POS_<pos>`",
        "",
        "The corpus contains one line per lexical entry. Tokens are separated with a single ASCII space.",
        "",
        "## Real Examples",
        "",
    ]
    content.extend(f"```text\n{line}\n```" for line in examples)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(content) + "\n", encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    lexicon_path = project_root / "data" / "processed" / "lexicon_master_full.jsonl"
    corpus_path = project_root / "data" / "processed" / "fasttext_corpus.txt"
    doc_path = project_root / "docs" / "reproducibility" / "corpus_format.md"

    entries = load_jsonl(lexicon_path)
    lines = build_corpus(entries)
    write_lines(corpus_path, lines)
    write_format_doc(doc_path, lines)

    print(f"entries: {len(entries)}")
    print(f"corpus_lines: {len(lines)}")
    print(f"wrote: {corpus_path}")
    print(f"wrote: {doc_path}")


if __name__ == "__main__":
    main()
