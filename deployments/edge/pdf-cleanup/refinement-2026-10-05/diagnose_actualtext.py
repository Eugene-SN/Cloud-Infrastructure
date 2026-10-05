import json
from pathlib import Path
import pymupdf
from review_pdfium import compare
from pdf_cleanup import core
from pdf_cleanup.native import inspect_pdf
source='/input/8921606e9e9fcc6b199f2c360787dc228f3180bd2448423d40bd1d101c13be71.pdf'
output='/out/full-style-diagnostic/edited.pdf';root=Path('/out/full-style-diagnostic')
result={}
for role,path in (('source',source),('output',output)):
 with pymupdf.open(path) as doc:
  page=doc[13]
  flags=pymupdf.TEXTFLAGS_RAWDICT & ~pymupdf.TEXT_PRESERVE_IMAGES
  chars=[{'span':{k:v for k,v in span.items() if k!='chars'},'char':char} for block in page.get_text('rawdict',flags=flags)['blocks'] for line in block.get('lines',[]) for span in line['spans'] for char in span['chars'] if char['c']=='表' and abs(char['origin'][1]-89.54)<1]
  trace=[span for span in page.get_texttrace() if any(abs(char[2][1]-89.54)<1 for char in span['chars'])]
  contents=page.read_contents();result[role]={'raw_char':chars,'trace':trace,'actualtext_lines':[line.decode('latin1') for line in contents.splitlines() if b'ActualText' in line][:5]}
  small=pymupdf.open();small.insert_pdf(doc,from_page=13,to_page=13);small.save(root/(role+'-page14.pdf'));small.close()
native=inspect_pdf('/out/style-diagnostic/source.pdf')
with pymupdf.open(source) as doc:
 p=doc[13];plan=core.analyze(pymupdf.open('/out/style-diagnostic/source.pdf'),native)[13]
 masks=[list(map(list,plan['rects']))]
result['independent_page14']=compare(str(root/'source-page14.pdf'),str(root/'output-page14.pdf'),masks,[[]])
(root/'actualtext.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False),flush=True)
