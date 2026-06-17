import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import List


DEFAULT_DATASET = Path("backend/data/embeddings/embedding_dataset.jsonl")
DEFAULT_OUTPUT = Path("backend/data/embeddings/fasttext_corpus.txt")


def normalize_token(value: str) -> str:
    return str(value or "").strip().replace(" ", "_")


def marker(prefix: str, value: str) -> str:
    value = normalize_token(value)
    return f"{prefix}_{value}" if value else ""


def cognate_token(cognate_group: str) -> str:
    value = normalize_token(cognate_group or "NONE")
    value = value.replace("cog_", "").replace("COG_", "")
    return f"COGNATE_{value.upper()}"


def lineage_tokens(record: dict) -> List[str]:
    tokens = []
    for item in record.get("historical_lineage") or []:
        stage = normalize_token(item.get("stage") or "").upper()
        form = normalize_token(item.get("form") or "")
        if stage:
            tokens.append(f"LINEAGE_{stage}")
        if form:
            tokens.append(f"LINEAGE_FORM_{form}")
    return tokens


def record_tokens(record: dict) -> List[str]:
    features = record.get("features") or []
    tokens = [
        normalize_token(record.get("surface_form")),
        normalize_token(record.get("lemma")),
        marker("ROOT", record.get("root")),
        marker("LANG", record.get("language")),
        cognate_token(record.get("cognate_group")),
    ]
    tokens.extend(f"FEATURE_{normalize_token(feature).upper()}" for feature in features)
    tokens.extend(lineage_tokens(record))
    return [token for token in tokens if token]


def grouped_signal_lines(records: List[dict]) -> List[List[str]]:
    by_cognate = defaultdict(list)
    by_root = defaultdict(list)
    by_feature = defaultdict(list)
    for record in records:
        if record.get("cognate_group"):
            by_cognate[record["cognate_group"]].append(record)
        if record.get("root"):
            by_root[(record.get("language"), record.get("root"))].append(record)
        for feature in record.get("features") or []:
            by_feature[feature].append(record)

    lines = []
    for cognate_group, items in by_cognate.items():
        forms = list(dict.fromkeys(normalize_token(item.get("surface_form")) for item in items if item.get("surface_form")))
        if len(forms) < 2:
            continue
        anchors = [cognate_token(cognate_group)]
        anchors.extend(lineage_tokens(items[0]))
        lines.append([*forms[:24], *anchors])
        lines.append([*anchors, *forms[:24]])

    for (_, root), items in by_root.items():
        forms = list(dict.fromkeys(normalize_token(item.get("surface_form")) for item in items if item.get("surface_form")))
        if len(forms) >= 2:
            lines.append([marker("ROOT", root), *forms[:16]])

    for feature, items in by_feature.items():
        forms = list(dict.fromkeys(normalize_token(item.get("surface_form")) for item in items if item.get("surface_form")))
        if len(forms) >= 2:
            lines.append([f"FEATURE_{normalize_token(feature).upper()}", *forms[:32]])
    return lines


def prepare_fasttext_corpus(dataset_path: str | Path = DEFAULT_DATASET, output_path: str | Path = DEFAULT_OUTPUT) -> dict:
    dataset_path = Path(dataset_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = 0
    tokens = 0
    records = []
    signal_lines = 0
    with dataset_path.open(encoding="utf-8") as src, output_path.open("w", encoding="utf-8") as dst:
        for line in src:
            record = json.loads(line)
            records.append(record)
            line_tokens = record_tokens(record)
            if not line_tokens:
                continue
            dst.write(" ".join(line_tokens) + "\n")
            lines += 1
            tokens += len(line_tokens)
        for line_tokens in grouped_signal_lines(records):
            if not line_tokens:
                continue
            dst.write(" ".join(line_tokens) + "\n")
            lines += 1
            signal_lines += 1
            tokens += len(line_tokens)
    return {"output_path": str(output_path), "lines": lines, "tokens": tokens, "signal_lines": signal_lines}


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare FastText training corpus from embedding JSONL")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    print(json.dumps(prepare_fasttext_corpus(args.dataset, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
