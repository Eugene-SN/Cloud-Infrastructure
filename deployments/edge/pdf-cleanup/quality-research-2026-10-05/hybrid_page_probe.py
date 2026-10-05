"""Diagnostic only: isolate the known page-349 rewrite, not a deployment rule."""
import json,time,os,copy,hashlib
from pathlib import Path
import pymupdf
from pdf_cleanup import core
from pdf_cleanup.native import remove_text_shows
key='8921606e9e9fcc6b199f2c360787dc228f3180bd2448423d40bd1d101c13be71'
record=json.loads((Path('/out/corpus')/(key+'.json')).read_text());record.pop('result')
out=Path('/out/hybrid-page-probe');out.mkdir(exist_ok=True)
state={};original_analyze=core.analyze;original_add=pymupdf.Page.add_redact_annot;original_apply=pymupdf.Page.apply_redactions;original_save=pymupdf.Document.save
def analyze(doc,native):
 plan=original_analyze(doc,native)
 state['bbox_operator_pages']=[i+1 for i,p in enumerate(plan) if p['requires_text_operators']]
 for page in plan:page['requires_text_operators']=False
 state['plan']=plan;return plan
def add(page,*args,**kwargs):
 if page.number==348:return None
 return original_add(page,*args,**kwargs)
def apply(page,*args,**kwargs):
 if page.number==348:return False
 return original_apply(page,*args,**kwargs)
def save(doc,*args,**kwargs):
 plan=copy.deepcopy(state['plan'])
 for i,page in enumerate(plan):
  if i!=348:page['selected']={};page['rects']=[]
 remove_text_shows(doc,record['input'],plan)
 return original_save(doc,*args,**kwargs)
core.analyze=analyze;pymupdf.Page.add_redact_annot=add;pymupdf.Page.apply_redactions=apply;pymupdf.Document.save=save
os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
started=time.monotonic();output=out/(key+'.pdf');record['output']=str(output)
record.pop('output_bytes',None)
try:
 record['result']=core.cleanup(record['input'],output)
 record.update(status='passed',elapsed_seconds=round(time.monotonic()-started,3),experiment='page 349 text operators; other pages unchanged redaction; not a universal rule')
except Exception as error:record.update(status='error',error=str(error))
record['bbox_operator_pages']=state.get('bbox_operator_pages')
record['elapsed_seconds']=round(time.monotonic()-started,3)
(out/(key+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({k:record.get(k) for k in ('path','status','error','elapsed_seconds')},ensure_ascii=False),flush=True)
if record['status']=='passed':
 from review_pdfium import compare
 result=compare(record['input'],record['output'],record['masks'],record['widget_masks'])
 result['output_verified_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
 (out/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False),flush=True)
