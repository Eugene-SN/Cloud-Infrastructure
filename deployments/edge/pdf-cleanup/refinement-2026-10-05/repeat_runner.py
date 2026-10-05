import os,json,hashlib,time,sys,traceback
from pathlib import Path
import pymupdf
from pdf_cleanup import core
os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
worker,workers=map(int,sys.argv[1:]);manifest=json.loads(Path('/audit/manifest.json').read_text())
root=Path('/out/results');root.mkdir(exist_ok=True)
original_inspect=core.inspect_pdf;cache={};cache_hashes={}
def inspect(path):
 data=original_inspect(path);key=str(Path(path).resolve());cache[key]=data;cache_hashes[key]=core.sha256(path);return data
core.inspect_pdf=inspect
hashes={name:hashlib.sha256(Path(core.__file__).with_name(name).read_bytes()).hexdigest() for name in ('core.py','native.py','lexical.py')}
for index,row in enumerate(sorted(manifest['unique_documents'],key=lambda x:x['path'])):
 if index%workers!=worker:continue
 record_path=root/(row['sha256']+'.json')
 if record_path.exists():continue
 source=Path('/input')/(row['sha256']+'.pdf');output=root/(row['sha256']+'.pdf');cache.clear();cache_hashes.clear();started=time.monotonic();record=dict(row,candidate_hashes=hashes)
 print(json.dumps({'event':'start','path':row['path']},ensure_ascii=False),flush=True)
 try:
  result=core.cleanup(source,output);record['result']=result
  if result['cleanup_method']=='exact_copy':
   assert result['input_sha256']==result['output_sha256']
   after=cache[str(source.resolve())];origin='verified_identical_bytes'
  else:
   written=[(path,data) for path,data in cache.items() if path!=str(source.resolve())]
   assert len(written)==1,{'unexpected_inspection_paths':list(cache)}
   stage,after=written[0];origin='written_stage_inspected_by_output_validator'
   assert Path(stage).parent==output.parent
   record['inspected_stage_sha256']=cache_hashes[stage]
   assert cache_hashes[stage]==result['output_sha256']
   record['inspected_stage_path']=stage
  assert not any(p['links'] or p['widgets'] for p in after)
  with pymupdf.open(output) as doc:
   plan=core.analyze(doc,after);entries=[{'page':i+1,'role':p['selected'][j],'text':p['lines'][j]['text']} for i,p in enumerate(plan) for j in sorted(p['selected'])]
  record['native_evidence_origin']=origin
  record['native_evidence_sha256']=hashlib.sha256(json.dumps(after,sort_keys=True).encode()).hexdigest()
  record['native_pagination_points']=sum(len(p['points']) for p in after)
  record['second_pass']={'status':'no_targets' if not entries else 'targets_detected','targets':entries}
  record['source_sha256_after']=core.sha256(source);assert record['source_sha256_after']==row['sha256']
  record['status']='passed' if not entries else 'differences'
 except Exception as error:record.update(status='error',error=str(error),traceback=traceback.format_exc())
 record['elapsed_seconds']=round(time.monotonic()-started,3)
 record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'event':'complete','path':row['path'],'status':record['status'],'error':record.get('error'),'seconds':record['elapsed_seconds'],'targets':record.get('second_pass',{}).get('targets')},ensure_ascii=False),flush=True)
