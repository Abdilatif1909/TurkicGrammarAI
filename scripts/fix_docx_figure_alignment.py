from pathlib import Path
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ElementTree


DOCX = Path("paper_draft/paper_fixed_v2.docx")
WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DRAWING_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PACKAGE_REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def paragraph_text(paragraph):
    return "".join(node.text or "" for node in paragraph.iter(WORD_NS + "t"))


with tempfile.TemporaryDirectory() as directory:
    source_path = Path(directory) / DOCX.name
    shutil.copy2(DOCX, source_path)
    output_path = Path(directory) / "fixed.docx"
    with zipfile.ZipFile(source_path, "r") as source:
        document = ElementTree.fromstring(source.read("word/document.xml"))
        relationships = ElementTree.fromstring(source.read("word/_rels/document.xml.rels"))
        relationships[:] = [
            relationship for relationship in relationships
            if relationship.attrib.get("Id") != "rId16"
        ]
        paragraphs = list(document.iter(WORD_NS + "p"))
        for index, paragraph in enumerate(paragraphs):
            text = paragraph_text(paragraph)
            match = next((number for number in range(1, 6) if f"Figure {number}." in text), None)
            if match is None:
                continue
            image_paragraph = paragraph if list(paragraph.iter(DRAWING_NS + "blip")) else paragraphs[index - 1]
            blips = list(image_paragraph.iter(DRAWING_NS + "blip"))
            if len(blips) != 1:
                raise RuntimeError(f"Expected one image before Figure {match} caption")
            blips[0].set(REL_NS + "embed", f"rId{10 + match}")
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                if item.filename == "word/document.xml":
                    data = ElementTree.tostring(document, encoding="utf-8", xml_declaration=True)
                elif item.filename == "word/_rels/document.xml.rels":
                    data = ElementTree.tostring(relationships, encoding="utf-8", xml_declaration=True)
                elif item.filename == "word/media/image6.png":
                    continue
                else:
                    data = source.read(item.filename)
                target.writestr(item, data)
    shutil.copy2(output_path, DOCX)