from pathlib import Path
import shutil
import tempfile
import zipfile


docx_path = Path("paper_draft/paper_fixed_v2.docx")
figure_dir = Path("paper_package/figures")
replacements = {
    "word/media/image1.png": figure_dir / "figure1_embedding_architecture.png",
    "word/media/image2.png": figure_dir / "figure2_dataset_distribution.png",
    "word/media/image3.png": figure_dir / "figure3_embedding_performance_comparison.png",
    "word/media/image4.png": figure_dir / "figure4_positive_negative_similarity.png",
    "word/media/image5.png": figure_dir / "figure5_language_coverage.png",
    "word/media/image6.png": figure_dir / "figure5_language_coverage.png",
}

with tempfile.TemporaryDirectory() as directory:
    output = Path(directory) / docx_path.name
    with zipfile.ZipFile(docx_path, "r") as source, zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = replacements.get(item.filename)
            target.writestr(item, data.read_bytes() if data else source.read(item.filename))
    shutil.copy2(output, docx_path)
