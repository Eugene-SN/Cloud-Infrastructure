"""Compare exact pypdf fallback/enabled CFF paths on Lenovo Press PDFs."""
import json,hashlib,logging
from pathlib import Path
import pypdf,pypdf._font,fontTools
from pdf_cleanup.native import inspect_pdf

class Warnings(logging.Handler):
    def __init__(self): super().__init__(); self.count=0
    def emit(self,record):
        if 'fontTools is required' in record.getMessage(): self.count+=1

handler=Warnings(); logger=logging.getLogger('pypdf'); logger.handlers=[handler];logger.propagate=False
items=[x for x in json.loads(Path('/audit/manifest.json').read_text())['unique_documents'] if Path(x['path']).name.startswith('lp')]
rows=[]
for item in items:
    path=Path('/input')/(item['sha256']+'.pdf'); data={}
    for enabled in (False,True):
        pypdf._font.HAS_FONTTOOLS=enabled; handler.count=0
        native=inspect_pdf(path); reader=pypdf.PdfReader(path); text='\n'.join(page.extract_text() for page in reader.pages)
        data[str(enabled)]={'native':native,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'text_characters':len(text),'cff_dependency_warnings':handler.count}
    rows.append({'path':item['path'],'sha256':item['sha256'],'native_evidence_equal':data['False']['native']==data['True']['native'],
                 'text_equal':data['False']['text_sha256']==data['True']['text_sha256'],
                 'without_fonttools':{k:v for k,v in data['False'].items() if k!='native'},'with_fonttools':{k:v for k,v in data['True'].items() if k!='native'}})
print(json.dumps({'fonttools':fontTools.__version__,'pypdf':pypdf.__version__,'documents':rows},ensure_ascii=False,indent=2))
