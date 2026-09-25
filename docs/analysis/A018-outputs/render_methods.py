"""Render both A018 methods without changing prior PDFs or the shared renderer."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tmp/pdf-deps"))
import fitz

spec = importlib.util.spec_from_file_location("method_renderer", Path(__file__).with_name("method_renderer.py"))
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
report = {}
for label in ("E041", "E025"):
    folder = ROOT / f"submissions/2026-09-25-{label}"
    renderer.SOURCE = folder / "method-4p.md"
    renderer.OUTPUT = folder / "method-4p.pdf"
    renderer.LABEL = label
    renderer.TITLE = renderer.SOURCE.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
    renderer.render()
    document = fitz.open(renderer.OUTPUT)
    assert len(document) == 4
    pages = []
    for index, page in enumerate(document):
        blocks = page.get_text("blocks")
        assert blocks
        assert all(0 <= b[0] < b[2] <= page.rect.width and
                   0 <= b[1] < b[3] <= page.rect.height for b in blocks)
        output = Path(__file__).parent / f"{label}-page-{index + 1}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(output)
        pages.append({"page": index + 1, "words": len(page.get_text().split()),
                      "bottom": max(b[3] for b in blocks), "png": output.name})
    report[label] = {"pages": pages, "text_bounds": "PASS"}
Path(__file__).with_name("method-layout.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
