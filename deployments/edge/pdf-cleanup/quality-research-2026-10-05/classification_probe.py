"""Measure a remaining classification ambiguity, not a deployment test."""
import json, os, tempfile
from pathlib import Path
import pymupdf
from pdf_cleanup.core import cleanup

os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
with tempfile.TemporaryDirectory(dir='/out') as tmp:
    root=Path(tmp); source=root/'required-settings.pdf'; target=root/'cleaned.pdf'
    doc=pymupdf.open()
    for number in (1,2):
        page=doc.new_page(width=612,height=792)
        page.insert_text((72,100),'Configuration procedure',fontsize=11)
        page.insert_text((72,180),'The following setting is required:',fontsize=11)
        # Body content, not pagination: no PDF artifact tags, no table frame.
        page.insert_text((72,200),f'Required setting {number}',fontsize=11)
    doc.save(source); doc.close()
    result=cleanup(source,target)
    with pymupdf.open(target) as output:
        missing=[i+1 for i,page in enumerate(output) if 'Required setting' not in page.get_text()]
    evidence={'status':'known_classification_gap' if missing else 'preserved',
              'missing_body_rows_on_pages':missing,'cleanup_report':result,
              'meaning':'An untagged final body row with consecutive numbers can be mistaken for pagination. Content validation follows the deletion plan and cannot prove the plan is semantically correct.'}
    print(json.dumps(evidence,ensure_ascii=False,indent=2))
