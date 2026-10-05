import json,sys,subprocess,hashlib,importlib.metadata as md,platform,pymupdf
from pathlib import Path
from pdf_cleanup import core
root=Path('/out');rows=[json.loads(p.read_text()) for p in sorted((root/'batch-records').glob('*.json')) if json.loads(p.read_text()).get('adapter_result',{}).get('stderr')]
assert len(rows)==3
mode=sys.argv[1];result={'mode':mode,'versions':{n:md.version(n) for n in ('pypdf','PyMuPDF','cryptography')},'python':platform.python_version(),'source_hashes':{n:hashlib.sha256(Path(core.__file__).with_name(n).read_bytes()).hexdigest() for n in ('core.py','native.py','lexical.py')},'records':[]}
if mode=='fonts':result['versions']['fonttools']=md.version('fonttools')
for row in rows:
 source=Path('/input')/(row['input_sha256']+'.pdf');output=root/'published'/row['output_file'];record={'path':row['path'],'source_native':core.inspect_pdf(source),'output_native':core.inspect_pdf(output)}
 if mode=='fonts':
  dest=root/'fonts-check'/row['output_file'];dest.parent.mkdir(exist_ok=True)
  if not dest.exists():
   process=subprocess.run(['pdf-cleanup',str(source),str(dest)],capture_output=True,text=True,timeout=900)
   record.update(cli_rc=process.returncode,stderr=process.stderr,summary=json.loads(process.stdout))
   assert process.returncode==0 and not process.stderr,record
  else:record['reuse']='Previously generated candidate; CLI returned 0 with empty stderr; verifier stopped on trailer-ID comparison'
  record.update(output_sha256=core.sha256(dest),expected_sha256=row['output_sha256'])
  with pymupdf.open(output) as old,pymupdf.open(dest) as new:
   assert old.xref_length()==new.xref_length()
   for i in range(1,old.xref_length()):
    assert old.xref_stream(i)==new.xref_stream(i)
    if old.xref_get_key(i,'Type')==('name','/XRef'):
     assert {k:old.xref_get_key(i,k) for k in old.xref_get_keys(i) if k!='ID'}=={k:new.xref_get_key(i,k) for k in new.xref_get_keys(i) if k!='ID'}
    else:assert old.xref_object(i)==new.xref_object(i)
   assert {k:old.xref_get_key(-1,k) for k in old.xref_get_keys(-1) if k!='ID'}=={k:new.xref_get_key(-1,k) for k in new.xref_get_keys(-1) if k!='ID'}
   record['all_objects_streams_and_non_ID_trailer_equal']=True
 result['records'].append(record)
(root/('fonttools-'+mode+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
if mode=='fonts':
 previous=json.loads((root/'fonttools-before.json').read_text())
 assert result['source_hashes']==previous['source_hashes'] and result['python']==previous['python']
 for n,v in previous['versions'].items():assert result['versions'][n]==v
 for before,after in zip(previous['records'],result['records']):
  assert before['path']==after['path'] and before['source_native']==after['source_native'] and before['output_native']==after['output_native']
print(json.dumps({'mode':mode,'files':len(rows),'native_evidence_unchanged':mode=='fonts','all_objects_streams_unchanged':mode=='fonts','versions':result['versions']}),flush=True)
