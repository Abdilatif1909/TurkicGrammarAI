"""Diagnose circular evaluation risks in RAG/QA benchmarks."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time

from gensim.models import FastText, KeyedVectors

from common import load_jsonl, project_root, write_json
from eval_qa import evaluate_embedding_only as evaluate_qa_embedding_only
from eval_rag_retrieval import evaluate_embedding_only as evaluate_rag_embedding_only


VECTOR_SIZE = 300
WINDOW = 5
MIN_COUNT = 1
EPOCHS = 20
BUCKET = 50000


class LineSentence:
    def __init__(self, path: Path) -> None:
        self.path = path

    def __iter__(self):
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                tokens = line.strip().split()
                if tokens:
                    yield tokens


def build_surface_pos_corpus(entries: list[dict], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for entry in entries:
            handle.write(f"{entry['surface_form']} POS_{entry['pos']}\n")
            count += 1
    return count


def train_surface_pos_model(corpus_path: Path, model_path: Path, vector_path: Path) -> dict:
    workers = os.cpu_count() or 1
    started_at = datetime.now(timezone.utc)
    start = time.perf_counter()
    model = FastText(
        vector_size=VECTOR_SIZE,
        window=WINDOW,
        min_count=MIN_COUNT,
        workers=workers,
        sg=1,
        seed=42,
        bucket=BUCKET,
    )
    model.build_vocab(corpus_iterable=LineSentence(corpus_path))
    model.train(
        corpus_iterable=LineSentence(corpus_path),
        total_examples=model.corpus_count,
        epochs=EPOCHS,
    )
    elapsed = time.perf_counter() - start
    finished_at = datetime.now(timezone.utc)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(model_path))
    model.wv.save_word2vec_format(str(vector_path))
    return {
        "corpus_path": str(corpus_path.relative_to(project_root())).replace("\\", "/"),
        "model_path": str(model_path.relative_to(project_root())).replace("\\", "/"),
        "vector_path": str(vector_path.relative_to(project_root())).replace("\\", "/"),
        "vector_size": VECTOR_SIZE,
        "window": WINDOW,
        "min_count": MIN_COUNT,
        "epochs": EPOCHS,
        "bucket": BUCKET,
        "workers": workers,
        "vocabulary_size": len(model.wv),
        "training_time_seconds": elapsed,
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": finished_at.isoformat(),
    }


def pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def write_markdown(path: Path, payload: dict) -> None:
    tagged_rag = payload["tagged_model"]["rag"]["embedding_only_cross_language"]["metrics"]
    plain_rag = payload["surface_pos_model"]["rag"]["embedding_only_cross_language"]["metrics"]
    tagged_qa = payload["tagged_model"]["qa"]["embedding_only"]
    plain_qa = payload["surface_pos_model"]["qa"]["embedding_only"]

    lines = [
        "# Leakage Diagnosis",
        "",
        "Stage: Bosqich 7.5 - Leakage/tautology check",
        "",
        "## Diagnosis",
        "",
        "- RAG benchmark relevant sets are generated from `lineage_links.jsonl`, which itself is generated from `cognate_id`/`lineage_id` metadata. A metadata lookup retriever and the benchmark answer key would therefore use the same source. That oracle setup is tautological and only measures internal metadata consistency.",
        "- The Bosqich 7 RAG evaluator used cosine nearest neighbors, not direct metadata lookup, but the benchmark relevant set includes same-language morphological variants. That makes Recall@1 artificially easy because near-inflectional variants are often the nearest vector neighbors.",
        "- QA 100% accuracy is confirmed to be database/template lookup, not open-ended QA. The engine parses the generated template and reads the exact answer from cognate/lineage/lexicon metadata.",
        "- The training corpus includes `COGNATE_` and `LINEAGE_` tokens. This can make metadata-derived retrieval easier because all members of a group co-occur with the same artificial tags during training.",
        "",
        "## No-Tag Model Check",
        "",
        "A comparison model was trained from only `surface_form POS_<pos>` lines. This removes `LANG_`, `lemma`, `COGNATE_`, and `LINEAGE_` training tokens. The diagnostic model uses `bucket=50000` to avoid the 2M default FastText subword allocation in the constrained local environment.",
        "",
        f"- Surface+POS corpus lines: **{payload['surface_pos_model']['training']['corpus_lines']}**",
        f"- Surface+POS vocabulary size: **{payload['surface_pos_model']['training']['vocabulary_size']}**",
        f"- Surface+POS training time seconds: **{payload['surface_pos_model']['training']['training_time_seconds']:.6f}**",
        "",
        "## Cross-Language Embedding-Only RAG Comparison",
        "",
        "| Model | Recall@1 | Recall@5 | Recall@10 | MRR | N |",
        "|---|---:|---:|---:|---:|---:|",
        f"| Tagged training corpus | {pct(tagged_rag['recall_at_1']['value'])} | {pct(tagged_rag['recall_at_5']['value'])} | {pct(tagged_rag['recall_at_10']['value'])} | {tagged_rag['mrr']['value']:.6f} | {tagged_rag['recall_at_1']['n']} |",
        f"| Surface+POS only corpus | {pct(plain_rag['recall_at_1']['value'])} | {pct(plain_rag['recall_at_5']['value'])} | {pct(plain_rag['recall_at_10']['value'])} | {plain_rag['mrr']['value']:.6f} | {plain_rag['recall_at_1']['n']} |",
        "",
        "## Embedding-Based QA Comparison",
        "",
        "Lemma lookup questions are skipped in embedding-only QA because answering them exactly requires direct lexicon lookup.",
        "",
        "| Model | Answer Accuracy | Source Accuracy | Evaluated | Skipped |",
        "|---|---:|---:|---:|---:|",
        f"| Tagged training corpus | {pct(tagged_qa['answer_accuracy']['value'])} | {pct(tagged_qa['source_accuracy']['value'])} | {tagged_qa['evaluated_questions']} | {tagged_qa['skipped_questions']} |",
        f"| Surface+POS only corpus | {pct(plain_qa['answer_accuracy']['value'])} | {pct(plain_qa['source_accuracy']['value'])} | {plain_qa['evaluated_questions']} | {plain_qa['skipped_questions']} |",
        "",
        "## Conclusion",
        "",
        "Tautology is confirmed for oracle/metadata-based RAG and template QA. Paper results should report oracle numbers only as pipeline consistency checks. The credible model-performance numbers are the embedding-only cross-language RAG and embedding-based QA results, preferably with the surface+POS no-tag comparison disclosed.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = project_root()
    entries = load_jsonl(root / "data" / "processed" / "lexicon_master_full.jsonl")
    rag_rows = load_jsonl(root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl")
    qa_rows = load_jsonl(root / "data" / "benchmarks" / "qa_benchmark.jsonl")

    surface_pos_corpus = root / "data" / "processed" / "fasttext_surface_pos_corpus.txt"
    corpus_lines = build_surface_pos_corpus(entries, surface_pos_corpus)
    training = train_surface_pos_model(
        surface_pos_corpus,
        root / "models" / "turkic_fasttext_surface_pos.model",
        root / "models" / "turkic_fasttext_surface_pos.vec",
    )
    training["corpus_lines"] = corpus_lines

    tagged_kv = KeyedVectors.load_word2vec_format(str(root / "models" / "turkic_fasttext.vec"))
    plain_kv = KeyedVectors.load_word2vec_format(
        str(root / "models" / "turkic_fasttext_surface_pos.vec")
    )

    payload = {
        "diagnosis": {
            "rag_oracle_tautology_confirmed": True,
            "qa_template_lookup_tautology_confirmed": True,
            "tag_tokens_can_ease_metadata_derived_retrieval": True,
            "final_recommended_model_metric": "surface_pos_model.embedding_only_cross_language for RAG; surface_pos_model.embedding_only for QA",
        },
        "tagged_model": {
            "rag": {
                "embedding_only": evaluate_rag_embedding_only(tagged_kv, rag_rows),
                "embedding_only_cross_language": evaluate_rag_embedding_only(
                    tagged_kv,
                    rag_rows,
                    cross_language_only=True,
                ),
            },
            "qa": {"embedding_only": evaluate_qa_embedding_only(qa_rows, tagged_kv)},
        },
        "surface_pos_model": {
            "training": training,
            "rag": {
                "embedding_only": evaluate_rag_embedding_only(plain_kv, rag_rows),
                "embedding_only_cross_language": evaluate_rag_embedding_only(
                    plain_kv,
                    rag_rows,
                    cross_language_only=True,
                ),
            },
            "qa": {"embedding_only": evaluate_qa_embedding_only(qa_rows, plain_kv)},
        },
    }
    write_json(root / "docs" / "reproducibility" / "leakage_diagnosis.json", payload)
    write_markdown(root / "docs" / "reproducibility" / "leakage_diagnosis.md", payload)
    print("rag_oracle_tautology_confirmed: true")
    print("qa_template_lookup_tautology_confirmed: true")
    plain_rag = payload["surface_pos_model"]["rag"]["embedding_only_cross_language"]["metrics"]
    plain_qa = payload["surface_pos_model"]["qa"]["embedding_only"]
    print(f"surface_pos_rag_recall_at_1: {plain_rag['recall_at_1']['value']:.6f}")
    print(f"surface_pos_rag_recall_at_5: {plain_rag['recall_at_5']['value']:.6f}")
    print(f"surface_pos_rag_recall_at_10: {plain_rag['recall_at_10']['value']:.6f}")
    print(f"surface_pos_rag_mrr: {plain_rag['mrr']['value']:.6f}")
    print(f"surface_pos_qa_answer_accuracy: {plain_qa['answer_accuracy']['value']:.6f}")
    print(f"surface_pos_qa_source_accuracy: {plain_qa['source_accuracy']['value']:.6f}")


if __name__ == "__main__":
    main()
