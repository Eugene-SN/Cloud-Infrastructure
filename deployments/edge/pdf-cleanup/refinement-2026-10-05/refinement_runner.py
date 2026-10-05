"""One frozen candidate, complete PDFs, native + independent + repeat checks."""
import os,json,time,sys,traceback,hashlib
from pathlib import Path
import pymupdf
from pdf_cleanup import core
from review_pdfium import compare

os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
phase=sys.argv[1];worker=int(sys.argv[2]);workers=int(sys.argv[3])
manifest=json.loads(Path('/audit/manifest.json').read_text())
sample=json.loads(Path('/out/selection.json').read_text())['documents'];keys={r['sha256'] for r in sample}
items=sample if phase=='sample' else [r for r in manifest['unique_documents'] if r['sha256'] not in keys]
priority=('wr6220g5_user','wr5220g5_user','onecli','wr5220g3_user','wa7780g3_user','wa7785ag3_user','wr5225g3_user')
items=sorted(items,key=lambda row:(next((i for i,p in enumerate(priority) if p in row['path']),len(priority)),row['path']))
root=Path('/out/results');root.mkdir(exist_ok=True)
captured={};native_cache={};original_analyze=core.analyze;original_inspect=core.inspect_pdf
def inspect(path):
 result=original_inspect(path);native_cache[str(Path(path).resolve())]=result;return result
def analyze(doc,native):
 plan=original_analyze(doc,native);captured['plan']=plan;captured['native']=native;return plan
core.inspect_pdf=inspect;core.analyze=analyze
candidate_hashes={name:hashlib.sha256(Path(core.__file__).with_name(name).read_bytes()).hexdigest() for name in ('core.py','native.py','lexical.py')}
for position,row in enumerate(items):
 if position%workers!=worker:continue
 target=root/(row['sha256']+'.json')
 if target.exists():continue
 native_cache.clear();captured.clear();record=dict(row,phase=phase,candidate_hashes=candidate_hashes)
 source=Path('/input')/(row['sha256']+'.pdf');output=root/(row['sha256']+'.pdf');started=time.monotonic()
 print(json.dumps({'event':'start','path':row['path'],'phase':phase},ensure_ascii=False),flush=True)
 try:
  result=core.cleanup(source,output);record['cleanup_seconds']=round(time.monotonic()-started,3);record['result']=result
  plan=captured['plan'];native=captured['native']
  masks=[list(map(list,p['rects'])) for p in plan]
  with pymupdf.open(source) as doc:
   widgets=[[list(w.rect) for w in (page.widgets() or []) if w.xref in native[i]['widgets']] for i,page in enumerate(doc)]
  review=compare(str(source),str(output),masks,widgets);record['independent']=review
  if result['cleanup_method']=='exact_copy':
   assert result['input_sha256']==result['output_sha256']
   after=native
  else:
   written=[data for path,data in native_cache.items() if path!=str(source.resolve())]
   assert len(written)==1, list(native_cache)
   after=written[0]
  with pymupdf.open(output) as doc:
   second=original_analyze(doc,after)
   entries=[{'page':i+1,'role':p['selected'][j],'text':p['lines'][j]['text']} for i,p in enumerate(second) for j in sorted(p['selected'])]
  record['second_pass']={'status':'no_targets' if not entries else 'targets_detected','targets':entries}
  record['source_sha256_after']=core.sha256(source)
  assert record['source_sha256_after']==row['sha256']
  record['status']='passed' if review['status']=='passed' and not entries else 'differences'
 except Exception as error:
  record.update(status='error',error=str(error),rc=getattr(error,'rc',None),traceback=traceback.format_exc())
 record['total_seconds']=round(time.monotonic()-started,3)
 target.write_text(json.dumps(record,ensure_ascii=False,indent=2))
 print(json.dumps({'event':'complete','path':row['path'],'status':record['status'],'error':record.get('error'),'seconds':record['total_seconds'],'outside_pixels':record.get('independent',{}).get('pixels_outside_masks'),'repeat_targets':len(record.get('second_pass',{}).get('targets',[]))},ensure_ascii=False),flush=True)
