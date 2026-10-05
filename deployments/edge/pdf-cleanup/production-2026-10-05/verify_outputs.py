"""One-off, read-only verification of every production output."""
import json,time,traceback,hashlib,collections,re
from pathlib import Path
import pymupdf
from pdf_cleanup import core
from review_pdfium import compare
manifest=json.loads(Path('/audit/manifest.json').read_text());expected={r['path']:r for r in manifest['documents']}
root=Path('/out');reports=root/'reviews';reports.mkdir(exist_ok=True);plans={};original_inspect=core.inspect_pdf;inspections={}
def inspect(path):
 result=original_inspect(path);inspections[str(Path(path).resolve())]=result;return result
core.inspect_pdf=inspect
hashes={n:hashlib.sha256(Path(core.__file__).with_name(n).read_bytes()).hexdigest() for n in ('core.py','native.py','lexical.py')}
completed={json.loads(p.read_text())['path'] for p in reports.glob('*.json')}

while True:
 queued=sorted((root/'queue').glob('*.json'))
 work=[p for p in queued if not (reports/p.name).exists()]
 if not work:
  if (root/'batch-finished.json').exists():break
  time.sleep(1);continue
 path=work[0];row=json.loads(path.read_text());report={'image_id':row.get('image_id'),'path':row['path'],'input_sha256':row['input_sha256'],'output_sha256':row['output_sha256'],'source_hashes':hashes};started=time.monotonic()
 print(json.dumps({'event':'verify_start','path':row['path']},ensure_ascii=False),flush=True)
 try:
  source=Path('/input')/(row['input_sha256']+'.pdf');output=root/'published'/row['output_file'];assert core.sha256(source)==expected[row['path']]['sha256'];assert core.sha256(output)==row['output_sha256']
  if row['input_sha256'] not in plans:
   native=original_inspect(source)
   with pymupdf.open(source) as doc:
    widgets=[[list(w.rect) for w in (page.widgets() or []) if w.xref in native[i]['widgets']] for i,page in enumerate(doc)]
    for i,item in enumerate(native):
     if not item['widgets']:continue
     page=doc[i];targets=set(item['widgets'])
     for widget in list(page.widgets() or []):
      if widget.xref in targets:page.delete_widget(widget)
     page=doc.reload_page(page);kind,array=doc.xref_get_key(page.xref,'Annots')
     if kind=='xref':array=doc.xref_object(int(array.split()[0]),compressed=False)
     remaining={int(x) for x in re.findall(r'(\d+)\s+\d+\s+R',array)};core.unlink_annotations(doc,page,targets & remaining)
    plan=core.analyze(doc,native)
   plans[row['input_sha256']]=(native,plan,widgets)
  native,plan,widgets=plans[row['input_sha256']];masks=[list(map(list,p['rects'])) for p in plan]
  inspections.clear()
  with pymupdf.open(source) as source_doc:core.validate_output(output,source_doc,plan,native)
  after=inspections[str(output.resolve())];assert not any(p['links'] or p['widgets'] for p in after)
  report['native_validation']='passed'
  with pymupdf.open(output) as doc:
   repeat=core.analyze(doc,after);targets=[{'page':i+1,'role':p['selected'][j],'text':p['lines'][j]['text']} for i,p in enumerate(repeat) for j in sorted(p['selected'])]
  report['repeat_analysis']={'targets':targets,'inspected_sha256':core.sha256(output)}
  report['independent']=compare(str(source),str(output),masks,widgets)
  report['source_sha256_after']=core.sha256(source)
  assert report['source_sha256_after']==row['input_sha256'];assert core.sha256(output)==row['output_sha256']
  report['status']='passed' if not targets and report['independent']['status']=='passed' else 'differences'
 except Exception as error:report.update(status='error',error=str(error),traceback=traceback.format_exc())
 report['seconds']=round(time.monotonic()-started,3);temporary=reports/(path.name+'.part');temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2));temporary.replace(reports/path.name)
 print(json.dumps({'event':'verify_complete','path':row['path'],'status':report['status'],'seconds':report['seconds'],'error':report.get('error')},ensure_ascii=False),flush=True)
 completed.add(row['path'])
 needed={d['sha256'] for d in manifest['documents'] if d['path'] not in completed}
 for key in list(plans):
  if key not in needed:del plans[key]

rows=[json.loads(p.read_text()) for p in reports.glob('*.json')];print(json.dumps({'verified':len(rows),'passed':sum(r['status']=='passed' for r in rows)}),flush=True)
assert len(rows)==len(expected) and all(r['status']=='passed' for r in rows)
