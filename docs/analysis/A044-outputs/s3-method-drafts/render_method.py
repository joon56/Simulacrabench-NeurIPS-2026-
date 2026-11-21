"""Render docs/method-4p.md; requires reportlab and pypdf.

Install dependencies separately from the submission environment. Explicit
Markdown pagebreak comments define the four-page method's section boundaries.
"""

import argparse
import json
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

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('candidate', choices=('E041', 'E025'))
parser.add_argument('attempt', type=int, choices=(1, 2, 3))
args = parser.parse_args()
SOURCE = ROOT / f'{args.candidate}-review.md'
OUTPUT = ROOT / f'{args.candidate}-review-attempt{args.attempt}.pdf'
assert not OUTPUT.exists(), 'preserve previous render'


def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',
                  r'<link href="\2" color="#244d70"><u>\1</u></link>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"`(.+?)`", r'<font name="Courier" size="8.4">\1</font>', text)


def render():
    assert SOURCE.parent == ROOT and OUTPUT.parent == ROOT
    body = ParagraphStyle("Body", fontName="Times-Roman", fontSize=10.4,
                          leading=12.6, spaceAfter=6, alignment=TA_JUSTIFY)
    title = ParagraphStyle("Title", fontName="Times-Bold", fontSize=16,
                           leading=18.5, spaceAfter=8, textColor=colors.HexColor('#19364b'))
    heading = ParagraphStyle("Heading", fontName="Times-Bold", fontSize=12,
                             leading=15, spaceBefore=5, spaceAfter=7,
                             keepWithNext=True)
    code = ParagraphStyle("Formula", fontName="Courier", fontSize=8.2,
                          leading=10.5, spaceBefore=1, spaceAfter=7)
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
            style = references if block.startswith("**References") else body
            story.append(Paragraph(inline(" ".join(block.splitlines())), style))

    def footer(canvas, doc):
        canvas.setStrokeColor(colors.HexColor("#a0a5aa"))
        canvas.line(margin, 36, width - margin, 36)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#505860"))
        canvas.drawString(margin, 24, f"HSCC 2026 | {args.candidate} | REVIEW DRAFT | 23 October 2026")
        canvas.drawRightString(width - margin, 24, f"{doc.page} / 4")
        canvas.setFont('Helvetica-Bold', 7.5)
        canvas.setFillColor(colors.HexColor('#8b3b2f'))
        canvas.drawString(margin, height - 25, 'REVIEW DRAFT - NOT FINAL TEST SELECTION')

    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=margin,
                                 rightMargin=margin, topMargin=40, bottomMargin=48,
                                 title=f"{args.candidate} method review draft - not final TEST selection",
                                 author="HSCC candidate review")
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    pages = PdfReader(OUTPUT).pages
    if len(pages) != 4:
        raise RuntimeError(f"Expected four pages; rendered {len(pages)}")
    final = ROOT / f'{args.candidate}-review.pdf'
    assert not final.exists(), 'do not overwrite a successful review PDF'
    final.write_bytes(OUTPUT.read_bytes())
    print(f"PASS: {OUTPUT} ({len(pages)} pages)")


if __name__ == "__main__":
    render()
