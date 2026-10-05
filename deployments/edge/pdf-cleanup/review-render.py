"""Compare rendered pixels outside planned removals; no PDFs are modified."""
import collections
import json
import math
from pathlib import Path
import sys

import pymupdf
from pdf_cleanup.native import inspect_pdf

root = Path(sys.argv[1])
plan = json.loads((root / 'evidence/dry-run.json').read_text())
by_page = collections.defaultdict(list)
for row in plan['plan']:
    by_page[row['page'] - 1].append(row['bbox'])

source = pymupdf.open(root / 'input/source.pdf')
output = pymupdf.open(root / 'evidence/cleaned.pdf')
native = inspect_pdf(root / 'input/source.pdf')
assert len(source) == len(output) == plan['pages']
assert source.get_toc() == output.get_toc()
outside_changed = 0
page_results = []
for index, (original, cleaned) in enumerate(zip(source, output)):
    assert (tuple(original.mediabox), tuple(original.cropbox), original.rotation) == (
        tuple(cleaned.mediabox), tuple(cleaned.cropbox), cleaned.rotation)
    boxes = list(by_page[index])
    for widget in original.widgets() or []:
        if widget.xref in native[index]['widgets']:
            boxes.append(list(widget.rect))
    a = original.get_pixmap(alpha=False)
    b = cleaned.get_pixmap(alpha=False)
    assert (a.width, a.height, a.n) == (b.width, b.height, b.n)
    left, right = a.samples, b.samples
    masks = [(max(0, math.floor(x0) - 2), max(0, math.floor(y0) - 2),
              min(a.width, math.ceil(x1) + 2), min(a.height, math.ceil(y1) + 2))
             for x0, y0, x1, y1 in boxes]
    changed = 0
    for y in range(a.height):
        intervals = sorted((x0, x1) for x0, y0, x1, y1 in masks if y0 <= y < y1)
        start = 0
        for x0, x1 in intervals + [(a.width, a.width)]:
            if x0 > start:
                lo = (y * a.width + start) * a.n
                hi = (y * a.width + x0) * a.n
                if left[lo:hi] != right[lo:hi]:
                    changed += sum(left[p:p+a.n] != right[p:p+a.n]
                                   for p in range(lo, hi, a.n))
            start = max(start, x1)
    outside_changed += changed
    assert not cleaned.get_links()
    assert not list(cleaned.widgets() or [])
    page_results.append({'page': index + 1, 'outside_changed_pixels': changed})
    if index in (0, len(source) // 2, len(source) - 1):
        a.save(root / f'evidence/page-{index+1}-original.png')
        b.save(root / f'evidence/page-{index+1}-cleaned.png')

result = {'pages': len(source), 'dpi': 72, 'mask_padding_px': 2,
          'outside_changed_pixels': outside_changed,
          'page_geometry_and_bookmarks_preserved': True,
          'output_links_and_widgets_absent': True, 'page_results': page_results,
          'limitation': 'Masks come from the CLI dry-run plan and its update-widget classifier; this is a pixel preservation check, not independent layout classification.'}
(root / 'evidence/render-review.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'page_results'}))
if outside_changed:
    sys.exit(1)
