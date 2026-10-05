import json,hashlib,time
from pathlib import Path
import pymupdf,pypdfium2 as pdfium
from review_pdfium import compare,glyphs,text_difference

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
out=Path('/out/review-corrected');out.mkdir(exist_ok=True)
for path in sorted(Path('/out/corpus').glob('*.json')):
 if (out/path.name).exists():continue
 record=json.loads(path.read_text())
 if record['status']!='passed':continue
 prior=json.loads((Path('/out/review')/path.name).read_text())
 assert digest(record['input'])==record['sha256']
 assert digest(record['output'])==record['result']['output_sha256']
 started=time.monotonic();failures=[]
 with pdfium.PdfDocument(record['input']) as src,pdfium.PdfDocument(record['output']) as dst,pymupdf.open(record['input']) as geometry:
  for i in range(len(src)):
   a=src[i];b=dst[i]
   try:
    g=geometry[i];g.set_rotation(0);matrix=g.transformation_matrix
    missing,extra,order,n=text_difference(glyphs(a,matrix),glyphs(b,matrix),record['masks'][i]+record['widget_masks'][i])
    if missing or extra or order:failures.append({'page':i+1,'missing_glyphs':sum(missing.values()),'extra_glyphs':sum(extra.values()),'reading_order_changed':order,'missing_examples':list(missing.items())[:3],'extra_examples':list(extra.items())[:3]})
   finally:a.close();b.close()
 prior['text_comparison_revision']='retained glyphs inside masks are preserved; only absent masked glyphs exempt'
 prior['text_failures']=failures
 prior['raster_failures']=[{'page':r['page'],'pixels_outside_masks':r['pixels_outside_masks']} for r in prior['failures'] if r['pixels_outside_masks']]
 prior['status']='differences' if failures or prior['raster_failures'] or prior['document_property_changes'] else 'passed'
 prior['source_verified_sha256']=digest(record['input']);prior['output_verified_sha256']=digest(record['output'])
 prior['text_recheck_seconds']=round(time.monotonic()-started,3)
 prior.pop('failures')
 (out/path.name).write_text(json.dumps(prior,ensure_ascii=False,indent=2))
 print(json.dumps({'path':record['path'],'status':prior['status'],'text_failures':len(failures)},ensure_ascii=False),flush=True)

out=Path('/out/review-v6');out.mkdir(exist_ok=True)
for path in sorted(Path('/out/repaired-v6').glob('*.json')):
 if (out/path.name).exists():continue
 record=json.loads(path.read_text());assert record['status']=='passed'
 if 'widget_masks' not in record:
  assert record['result']['removed_widgets']==0
  record['widget_masks']=[[] for _ in range(record['result']['pages'])]
 result=compare(record['input'],record['output'],record['masks'],record['widget_masks'])
 result.update(path=record['path'],sha256=record['sha256'],output_verified_sha256=digest(record['output']))
 (out/path.name).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps({'path':record['path'],'status':result['status'],'failures':len(result['failures'])},ensure_ascii=False),flush=True)
