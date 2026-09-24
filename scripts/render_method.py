"""Render docs/method-4p.md; requires reportlab and pypdf.

Install dependencies separately from the submission environment. Explicit
Markdown pagebreak comments define the four-page method's section boundaries.
"""

import re
from html import escape
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/method-4p.md"
OUTPUT = ROOT / "output/pdf/method-4p.pdf"


def inline(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r'<font name="Courier" size="8.4">\1</font>', text)


def render():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    body = ParagraphStyle("Body", fontName="Times-Roman", fontSize=10.5,
                          leading=13.1, spaceAfter=7, alignment=TA_JUSTIFY)
    title = ParagraphStyle("Title", fontName="Times-Bold", fontSize=17,
                           leading=20, spaceAfter=9)
    heading = ParagraphStyle("Heading", fontName="Times-Bold", fontSize=12,
                             leading=15, spaceBefore=5, spaceAfter=7,
                             keepWithNext=True)
    code = ParagraphStyle("Formula", fontName="Courier", fontSize=8.2,
                          leading=11, spaceBefore=1, spaceAfter=8)
    cell = ParagraphStyle("Cell", fontName="Times-Roman", fontSize=9,
                          leading=11)
    references = ParagraphStyle("References", parent=body, alignment=TA_LEFT)
    width, height = A4
    margin = 48
    usable = width - 2 * margin
    story = []
    for block in re.split(r"\n\s*\n", SOURCE.read_text(encoding="utf-8").strip()):
        if block == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif block.startswith("# "):
            story.append(Paragraph(inline(block[2:]), title))
        elif block.startswith("## "):
            story.append(Paragraph(inline(block[3:]), heading))
        elif block.startswith("    "):
            story.append(Preformatted("\n".join(line[4:] for line in block.splitlines()), code))
        elif block.startswith("|"):
            rows = [line.strip().strip("|").split("|") for line in block.splitlines()]
            rows = [row for row in rows if not all(re.fullmatch(r"[\s:-]+", c) for c in row)]
            data = [[Paragraph(inline(c.strip()), cell) for c in row] for row in rows]
            widths = ([0.29, 0.28, 0.09, 0.34] if len(rows[0]) == 4
                      else [0.40, 0.28, 0.32])
            table = Table(data, colWidths=[usable * w for w in widths], repeatRows=1,
                          hAlign="LEFT", spaceAfter=9)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf0f2")),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#606870")),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#a0a5aa")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(table)
        else:
            style = references if block.startswith("**References.**") else body
            story.append(Paragraph(inline(" ".join(block.splitlines())), style))

    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor("#a0a5aa"))
        canvas.line(margin, 36, width - margin, 36)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#505860"))
        canvas.drawString(margin, 24, "HSCC 2026 | E041 | Method candidate")
        canvas.drawRightString(width - margin, 24, str(doc.page))

    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=margin,
                                 rightMargin=margin, topMargin=40, bottomMargin=48,
                                 title="Calibrated survey completion with section-specific retrieval",
                                 author="HSCC E041 method candidate")
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    pages = PdfReader(OUTPUT).pages
    if len(pages) != 4:
        raise RuntimeError(f"Expected four pages; rendered {len(pages)}")
    print(f"PASS: {OUTPUT} ({len(pages)} pages)")


if __name__ == "__main__":
    render()
