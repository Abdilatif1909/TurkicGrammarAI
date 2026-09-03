"""Build Markdown result tables from evaluation JSON files."""

from __future__ import annotations

from collections import Counter

from common import load_json, load_jsonl, project_root


def pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def num(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.6f}"


def ci(metric: dict) -> str:
    interval = metric.get("wilson_95_ci")
    if not interval or interval["low"] is None:
        return "N/A"
    return f"{pct(interval['low'])} - {pct(interval['high'])}"


def feature_availability(entries: list[dict]) -> list[dict]:
    total = len(entries)
    counters = {
        "ROOT": sum(1 for entry in entries if entry.get("root")),
        "COGNATE": sum(1 for entry in entries if entry.get("cognate_ids")),
        "LINEAGE": sum(1 for entry in entries if entry.get("lineage_ids")),
        "LANGUAGE": sum(1 for entry in entries if entry.get("language")),
    }
    return [
        {
            "feature": name,
            "available_entries": count,
            "total_entries": total,
            "availability": count / total if total else None,
        }
        for name, count in counters.items()
    ]


def feature_hit_stats() -> list[dict]:
    root = project_root()
    embedding = load_jsonl(root / "data" / "benchmarks" / "embedding_quality_benchmark.jsonl")
    semantic = load_jsonl(root / "data" / "benchmarks" / "semantic_search_benchmark.jsonl")
    rag = load_jsonl(root / "data" / "benchmarks" / "rag_retrieval_benchmark.jsonl")
    qa = load_jsonl(root / "data" / "benchmarks" / "qa_benchmark.jsonl")

    embedding_sources = Counter(row["source"] for row in embedding)
    qa_types = Counter(row["answer_type"] for row in qa)
    return [
        {"feature": "ROOT", "benchmark_usage": "all lexicon rows include root; lemma/morphology used in RAG relevant sets", "count": len(rag)},
        {"feature": "COGNATE", "benchmark_usage": "semantic queries and cognate QA; embedding positives from cognate groups", "count": len(semantic) + qa_types["shared_cognate_languages"] + embedding_sources["cognate"]},
        {"feature": "LINEAGE", "benchmark_usage": "RAG queries, lineage QA, and lineage-sourced embedding positives", "count": len(rag) + qa_types["lineage_descendant_languages"] + embedding_sources["lineage"]},
        {"feature": "LANGUAGE", "benchmark_usage": "all benchmark rows carry language labels", "count": len(embedding) + len(semantic) + len(rag) + len(qa)},
    ]


def build_markdown() -> str:
    root = project_root()
    embedding = load_json(root / "docs" / "reproducibility" / "results_embedding_quality.json")
    semantic = load_json(root / "docs" / "reproducibility" / "results_semantic_search.json")
    rag = load_json(root / "docs" / "reproducibility" / "results_rag_retrieval.json")
    qa = load_json(root / "docs" / "reproducibility" / "results_qa.json")
    leakage_path = root / "docs" / "reproducibility" / "leakage_diagnosis.json"
    leakage = load_json(leakage_path) if leakage_path.exists() else None
    entries = load_jsonl(root / "data" / "processed" / "lexicon_master_full.jsonl")
    rag_oracle = rag["oracle_metadata"]
    rag_embedding = rag["embedding_only_cross_language"]
    qa_oracle = qa["oracle_template_lookup"]
    qa_embedding = qa["embedding_only"]

    lines = [
        "# Results Tables",
        "",
        "Stage: Bosqich 7 - Evaluation",
        "",
        "## Table 4 - Embedding Quality Results",
        "",
        "| Metric | Value | N | Notes |",
        "|---|---:|---:|---|",
        f"| Mean positive similarity | {num(embedding['mean_positive_similarity'])} | {embedding['positive_similarity_pairs']} | Cosine over positive pairs |",
        f"| Mean negative similarity | {num(embedding['mean_negative_similarity'])} | {embedding['negative_similarity_pairs']} | Cosine over fixed-seed negative controls |",
        f"| Separation margin | {num(embedding['separation_margin'])} | {embedding['similarity_evaluated_pairs']} | Positive mean minus negative mean |",
    ]
    for key, label in [("top_1_accuracy", "Top-1 accuracy"), ("top_5_accuracy", "Top-5 accuracy"), ("top_10_accuracy", "Top-10 accuracy")]:
        metric = embedding["topk"][key]
        lines.append(f"| {label} | {pct(metric['value'])} | {metric['n']} | Nearest-neighbor target hit |")

    lines.extend([
        "",
        "## Table 5 - Wilson 95% Confidence Intervals",
        "",
        "| Metric | Estimate | Wilson 95% CI | Successes | N |",
        "|---|---:|---:|---:|---:|",
    ])
    for source, metrics in [
        ("Embedding", embedding["topk"]),
        ("Semantic", semantic["metrics"]),
        ("RAG embedding cross-language", {key: value for key, value in rag_embedding["metrics"].items() if key.startswith("recall")}),
    ]:
        for key, metric in metrics.items():
            lines.append(f"| {source} {key} | {pct(metric['value'])} | {ci(metric)} | {metric['hits']} | {metric['n']} |")
    for key, metric in [("QA embedding answer_accuracy", qa_embedding["answer_accuracy"]), ("QA embedding source_accuracy", qa_embedding["source_accuracy"])]:
        lines.append(f"| {key} | {pct(metric['value'])} | {ci(metric)} | {metric['hits']} | {metric['n']} |")

    lines.extend([
        "",
        "## Table 6 - Feature Availability And Benchmark Usage",
        "",
        "| Feature | Available entries | Total entries | Availability | Benchmark usage count | Usage definition |",
        "|---|---:|---:|---:|---:|---|",
    ])
    usage = {row["feature"]: row for row in feature_hit_stats()}
    for row in feature_availability(entries):
        hit = usage[row["feature"]]
        lines.append(
            f"| {row['feature']} | {row['available_entries']} | {row['total_entries']} | {pct(row['availability'])} | {hit['count']} | {hit['benchmark_usage']} |"
        )

    lines.extend([
        "",
        "## Table 7 - Category-Level Evaluation",
        "",
        "N/A - insufficient category granularity in the current dataset. The lexicon has POS labels and cognate/lineage groups, but no independent semantic category taxonomy suitable for a separate Table 7 without inventing labels.",
        "",
        "## Semantic Search Results",
        "",
        "| Metric | Value | Hits | N |",
        "|---|---:|---:|---:|",
    ])
    for key, metric in semantic["metrics"].items():
        lines.append(f"| {key} | {pct(metric['value'])} | {metric['hits']} | {metric['n']} |")

    lines.extend([
        "",
        "## RAG Retrieval Results - Oracle Vs Embedding",
        "",
        "Oracle/metadata-based retrieval demonstrates pipeline correctness. Embedding-based retrieval demonstrates model behavior; the cross-language row excludes same-language morphology hits.",
        "",
        "| Mode | Recall@1 | Recall@5 | Recall@10 | MRR | N |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for label, result in [
        ("oracle_metadata", rag_oracle),
        ("embedding_only_all_relevant", rag["embedding_only"]),
        ("embedding_only_cross_language", rag_embedding),
    ]:
        metrics = result["metrics"]
        lines.append(
            f"| {label} | {pct(metrics['recall_at_1']['value'])} | {pct(metrics['recall_at_5']['value'])} | {pct(metrics['recall_at_10']['value'])} | {num(metrics['mrr']['value'])} | {result['evaluated_queries']} |"
        )

    lines.extend([
        "",
        "## QA Results - Oracle Vs Embedding",
        "",
        "Oracle/template lookup demonstrates database consistency. Embedding-based QA derives answer languages from top-10 vector neighbors; lemma lookup questions are skipped because exact lemma answers require direct database lookup.",
        "",
        "| Mode | Answer Accuracy | Source Accuracy | Evaluated | Skipped |",
        "|---|---:|---:|---:|---:|",
        f"| oracle_template_lookup | {pct(qa_oracle['answer_accuracy']['value'])} | {pct(qa_oracle['source_accuracy']['value'])} | {qa_oracle['evaluated_questions']} | {qa_oracle['skipped_questions']} |",
        f"| embedding_only_tagged_model | {pct(qa_embedding['answer_accuracy']['value'])} | {pct(qa_embedding['source_accuracy']['value'])} | {qa_embedding['evaluated_questions']} | {qa_embedding['skipped_questions']} |",
    ])

    if leakage:
        no_tag_rag = leakage["surface_pos_model"]["rag"]["embedding_only_cross_language"]
        no_tag_qa = leakage["surface_pos_model"]["qa"]["embedding_only"]
        lines.extend([
            "",
            "## Leakage Diagnostic - No-Tag Model",
            "",
            "The no-tag comparison model was trained with only `surface_form POS_<pos>` lines. It removes `LANG_`, `lemma`, `COGNATE_`, and `LINEAGE_` corpus tokens.",
            "",
            "| Task | Metric | Tagged model | Surface+POS no-tag model | N |",
            "|---|---|---:|---:|---:|",
            f"| RAG cross-language | Recall@1 | {pct(rag_embedding['metrics']['recall_at_1']['value'])} | {pct(no_tag_rag['metrics']['recall_at_1']['value'])} | {no_tag_rag['evaluated_queries']} |",
            f"| RAG cross-language | Recall@5 | {pct(rag_embedding['metrics']['recall_at_5']['value'])} | {pct(no_tag_rag['metrics']['recall_at_5']['value'])} | {no_tag_rag['evaluated_queries']} |",
            f"| RAG cross-language | Recall@10 | {pct(rag_embedding['metrics']['recall_at_10']['value'])} | {pct(no_tag_rag['metrics']['recall_at_10']['value'])} | {no_tag_rag['evaluated_queries']} |",
            f"| RAG cross-language | MRR | {num(rag_embedding['metrics']['mrr']['value'])} | {num(no_tag_rag['metrics']['mrr']['value'])} | {no_tag_rag['evaluated_queries']} |",
            f"| QA embedding | Answer accuracy | {pct(qa_embedding['answer_accuracy']['value'])} | {pct(no_tag_qa['answer_accuracy']['value'])} | {no_tag_qa['evaluated_questions']} |",
            f"| QA embedding | Source accuracy | {pct(qa_embedding['source_accuracy']['value'])} | {pct(no_tag_qa['source_accuracy']['value'])} | {no_tag_qa['evaluated_questions']} |",
        ])

    lines.extend([
        "",
        "## Limitations Of Current Evaluation Scale",
        "",
        "- RAG evaluation uses only 43 queries because it is limited to Old Turkic-attested lineage groups.",
        "- QA evaluation uses 197 generated template questions, so confidence intervals are wider than for the embedding benchmark.",
        "- Oracle RAG and template QA are circular by construction and should be reported only as metadata pipeline consistency checks.",
        "- The tagged training corpus includes `COGNATE_` and `LINEAGE_` tokens, so tagged embedding results can overstate generalization on metadata-derived benchmarks.",
        "- The benchmark is derived from the same lexicon used to build the corpus, so even embedding-only results test internal retrieval consistency more than external generalization.",
        "- The current dataset lacks an independent semantic category taxonomy, so category-level claims should not be made.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    output_path = project_root() / "docs" / "reproducibility" / "results_tables.md"
    output_path.write_text(build_markdown(), encoding="utf-8")
    print(f"wrote: {output_path}")


if __name__ == "__main__":
    main()
