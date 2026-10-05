import sys,json,time,hashlib,faulthandler,subprocess
from pathlib import Path
import pymupdf
from pdf_cleanup import core
mode=sys.argv[1];root=Path('/audit');out=Path('/out')/mode;out.mkdir(exist_ok=True)
item=next(x for x in json.loads((root/'manifest.json').read_text())['unique_documents'] if x['path'].endswith('lenovo_bmc_g3_redfish_guide_v11.pdf'))
inp=Path('/input')/(item['sha256']+'.pdf'); started=time.monotonic()
def log(event,**data): print(json.dumps({'seconds':round(time.monotonic()-started,3),'event':event,**data},ensure_ascii=False),flush=True)
original=pymupdf.Document.save
def save(self,*args,**kwargs):
 if mode.startswith('g2'): kwargs['garbage']=2
 if mode.endswith('obj'): kwargs['use_objstms']=1
 log('save_start',options=kwargs,xref_length=self.xref_length());t=time.monotonic()
 try: return original(self,*args,**kwargs)
 finally: log('save_end',elapsed=round(time.monotonic()-t,3))
pymupdf.Document.save=save
faulthandler.dump_traceback_later(60,repeat=True)
try:
 result=core.cleanup(inp,out/'cleaned.pdf')
 log('complete',result=result,size=(out/'cleaned.pdf').stat().st_size)
 (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
except Exception as error: log('error',error=str(error));raise
finally: faulthandler.cancel_dump_traceback_later()
