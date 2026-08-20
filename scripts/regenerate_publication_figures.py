from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


OUTPUT = Path("paper_package/figures")
OUTPUT.mkdir(parents=True, exist_ok=True)

LANGUAGES = ["Uzbek", "Turkish", "Azerbaijani", "Kazakh", "Kyrgyz", "Turkmen", "Uyghur", "Old Turkic"]
RECORDS = [18314, 15798, 10372, 10582, 10499, 10102, 13916, 10417]
BASELINE = [15.62, 25.83, 35.49]
COGNATE_AWARE = [40.80, 73.66, 86.06]


def save(figure, name):
    figure.savefig(OUTPUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def architecture():
    figure, axis = plt.subplots(figsize=(10, 8))
    axis.set_xlim(0, 10)
    axis.set_ylim(0, 10)
    axis.axis("off")
    labels = ["Lexical resources", "Morphology", "Cognates", "Historical lineage", "FastText embeddings", "Semantic search", "RAG and QA"]
    for index, label in enumerate(labels):
        y = 9.1 - index * 1.25
        box = FancyBboxPatch((2.0, y - 0.35), 6.0, 0.7, boxstyle="round,pad=0.04", linewidth=2, edgecolor="#285c8f", facecolor="#eef6fc")
        axis.add_patch(box)
        axis.text(5, y, label, ha="center", va="center", fontsize=15, color="#17324d")
        if index < len(labels) - 1:
            axis.annotate("", xy=(5, y - 0.88), xytext=(5, y - 0.4), arrowprops={"arrowstyle": "->", "lw": 1.8, "color": "#444"})
    axis.set_title("Cognate-aware multilingual embedding framework", fontsize=18, pad=18)
    save(figure, "figure1_embedding_architecture.png")


def language_distribution():
    figure, axis = plt.subplots(figsize=(10, 8))
    bars = axis.bar(LANGUAGES, RECORDS, color="#285c8f")
    axis.set_title("Distribution of lexical resources", fontsize=18, pad=18)
    axis.set_ylabel("Records")
    axis.tick_params(axis="x", rotation=35)
    axis.grid(axis="y", alpha=0.25)
    axis.bar_label(bars, fmt="%d", padding=3, fontsize=10)
    figure.tight_layout()
    save(figure, "figure2_dataset_distribution.png")


def performance():
    figure, axis = plt.subplots(figsize=(10, 8))
    positions = range(3)
    width = 0.36
    axis.bar([p - width / 2 for p in positions], BASELINE, width, label="Vanilla FastText baseline", color="#8c9aa8")
    axis.bar([p + width / 2 for p in positions], COGNATE_AWARE, width, label="Cognate-aware model", color="#285c8f")
    axis.set_xticks(list(positions), ["Top-1", "Top-5", "Top-10"])
    axis.set_ylim(0, 100)
    axis.set_ylabel("Accuracy (%)")
    axis.set_title("Embedding performance comparison", fontsize=18, pad=18)
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    save(figure, "figure3_embedding_performance_comparison.png")


def similarity():
    figure, axis = plt.subplots(figsize=(10, 8))
    values = [0.452783, 0.520538, 0.595108, 0.472318]
    labels = ["Baseline positive", "Baseline negative", "Cognate-aware positive", "Cognate-aware negative"]
    colors = ["#8c9aa8", "#b8c2cc", "#285c8f", "#6f9fc4"]
    bars = axis.bar(labels, values, color=colors)
    axis.set_ylim(0, 0.7)
    axis.set_ylabel("Mean cosine similarity")
    axis.set_title("Positive and negative pair similarity", fontsize=18, pad=18)
    axis.tick_params(axis="x", rotation=25)
    axis.grid(axis="y", alpha=0.25)
    axis.bar_label(bars, fmt="%.3f", padding=3, fontsize=10)
    figure.tight_layout()
    save(figure, "figure4_positive_negative_similarity.png")


def coverage():
    figure, axis = plt.subplots(figsize=(14, 8))
    colors = ["#285c8f", "#3d729f", "#5388af", "#699dbf", "#7fb2cf", "#95c7df", "#abdced", "#c1e9f5"]
    axis.pie(RECORDS, labels=LANGUAGES, autopct="%.1f%%", startangle=90, colors=colors, textprops={"fontsize": 11})
    axis.set_title("Language coverage in the embedding corpus", fontsize=18, pad=18)
    figure.savefig(OUTPUT / "figure5_language_coverage.png", dpi=200, facecolor="white")
    plt.close(figure)


if __name__ == "__main__":
    architecture()
    language_distribution()
    performance()
    similarity()
    coverage()
