"""PDF-only extraction, geometric checks and page rendering. No model imports."""
import json
from pathlib import Path
import sys

import pymupdf
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
mode = sys.argv[1]

if mode == 'originals':
    result = {}
    for candidate in ('E041', 'E025'):
        path = ROOT / 'submissions' / f'2026-09-25-{candidate}' / 'method-4p.pdf'
        reader = PdfReader(path)
        text = '\n\n'.join(page.extract_text() for page in reader.pages)
        (OUT / f'{candidate}-original-extracted.txt').write_text(text, encoding='utf-8')
        result[candidate] = {'pages': len(reader.pages), 'text_chars': len(text),
                             'historical_only': True, 'source': str(path)}
    (OUT / 'original-pdf-inspection.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))
else:
    assert mode in ('E041', 'E025')
    candidate = mode
    path = OUT / f'{candidate}-review.pdf'
    doc = pymupdf.open(path)
    assert len(doc) == 4
    report = {'candidate': candidate, 'pages': len(doc), 'page_results': []}
    for index, page in enumerate(doc):
        text = page.get_text(sort=True)
        assert candidate in text and 'REVIEW DRAFT' in text
        assert '\ufffd' not in text and '\x00' not in text
        assert len(text.strip()) > 600, (candidate, index, 'near-empty page')
        boxes = []
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    rect = pymupdf.Rect(span['bbox'])
                    assert rect.x0 >= 42 and rect.x1 <= page.rect.width - 40, (index, span)
                    assert rect.y0 >= 12 and rect.y1 <= page.rect.height - 15, (index, span)
                    boxes.append({'text': span['text'], 'bbox': list(rect), 'font': span['font'], 'size': span['size']})
        png = OUT / f'{candidate}-page-{index+1}.png'
        assert not png.exists()
        page.get_pixmap(dpi=130, alpha=False).save(png)
        (OUT / f'{candidate}-page-{index+1}.txt').write_text(text, encoding='utf-8')
        links = [link['uri'] for link in page.get_links() if link.get('uri')]
        report['page_results'].append({'page': index+1, 'characters': len(text),
                                       'text_bounds_pass': True, 'links': links,
                                       'fonts': sorted({box['font'] for box in boxes}), 'spans': boxes})
    assert sum(len(row['links']) for row in report['page_results']) == 6
    (OUT / f'{candidate}-pdf-inspection.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'page_results'}))
