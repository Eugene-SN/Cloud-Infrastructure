"""Operator-authorized, one-time full catalogue rebuild; no scheduler/workflow."""
import pathlib,json,subprocess,base64,shutil,hashlib,time,re,datetime,traceback
from dav import request
r=pathlib.Path(__file__).resolve().parent;m=json.loads((r/'audit/manifest.json').read_text());commit=(r/'source-commit').read_text().strip();out=r/'out'
for name in ('queue','published','batch-records'):(out/name).mkdir(exist_ok=True)
def call(payload):
 process=subprocess.run(['/usr/bin/python3','/opt/pdf-cleanup/job-command.py',base64.b64encode(json.dumps(payload).encode()).decode()],text=True,capture_output=True,timeout=940);assert process.returncode==0,process.stderr;return json.loads(process.stdout)
pattern=re.compile(r'(<script id="catalog-data" type="application/json">)([\s\S]*?)(</script>)')
def index_update(path=None):
 code,raw,_=request('GET','originals/INDEX.html');html=raw.decode();match=pattern.search(html);assert match;catalog=json.loads(match[2]);assert len(catalog['documents'])==len(m['documents']);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for doc in catalog['documents']:
  if path is None:doc.update(cleanup_status='pending');doc.pop('cleaned_at',None);doc.pop('cleaned_path',None)
  elif doc['path']==path:doc.update(cleanup_status='cleaned',cleaned_at=now,cleaned_path=path)
 catalog['generated_at']=now;html=pattern.sub(lambda z:z[1]+json.dumps(catalog,ensure_ascii=False,indent=2).replace('<','\\u003c')+z[3],html,count=1);status,_,_=request('PUT','originals/INDEX.html',html.encode(),'text/html; charset=utf-8');assert status in (200,201,204)
selected={x['path'] for x in json.loads((out/'fonttools-fonts.json').read_text())['records']}
image_id=json.loads((r/'new-deployment.json').read_text())['image_id']
for i,row in enumerate(m['documents']):
 if row['path'] not in selected:continue
 started=time.monotonic();record={'path':row['path'],'input_sha256':row['sha256'],'image_id':image_id};execution_id=str(202610059000+i);job=None
 print(json.dumps({'event':'cleanup_start','number':i+1,'total':len(m['documents']),'path':row['path']},ensure_ascii=False),flush=True)
 try:
  job=call({'action':'create','execution_id':execution_id});assert job['ok'];directory=pathlib.Path(job['job_dir']);shutil.copyfile(r/'inputs'/(row['sha256']+'.pdf'),directory/'input/source.pdf')
  result=call({'action':'process','job_dir':str(directory),'execution_id':execution_id,'upload_ok':True});record['adapter_result']=result;assert result['ok'],result.get('error');summary=result['summary'];assert summary['source_commit']==commit;assert summary['input_sha256']==row['sha256'];assert summary['validation']=='passed'
  pdf=(directory/'output/cleaned.pdf').read_bytes();digest=hashlib.sha256(pdf).hexdigest();assert digest==summary['output_sha256'];record['output_sha256']=digest
  code,_,_=request('PUT','cleaned/'+row['path'],pdf,'application/pdf');assert code in (200,201,204);record['put_status']=code
  code,published,_=request('GET','cleaned/'+row['path']);assert code==200 and hashlib.sha256(published).hexdigest()==digest;record['webdav_readback']='matched'
  filename=f'{i:03d}.pdf';(out/'published'/filename).write_bytes(published);record['output_file']=filename
  index_update(row['path']);record['index_updated']=True;record['status']='passed'
  queue=out/'queue'/f'{i:03d}.json';temp=queue.with_suffix('.part');temp.write_text(json.dumps(record,ensure_ascii=False,indent=2));temp.replace(queue)
 except Exception as error:record.update(status='error',error=str(error),traceback=traceback.format_exc())
 finally:
  if job and job.get('ok'):
   release=call({'action':'release','job_dir':job['job_dir'],'execution_id':execution_id});record['job_removed']=release.get('ok') and release.get('job_removed');assert record['job_removed']
 record['seconds']=round(time.monotonic()-started,3);(out/'batch-records'/f'{i:03d}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
 print(json.dumps({'event':'cleanup_complete','number':i+1,'path':row['path'],'status':record['status'],'seconds':record['seconds'],'error':record.get('error')},ensure_ascii=False),flush=True)
records=[json.loads(p.read_text()) for p in (out/'batch-records').glob('*.json')];summary={'total':len(records),'passed':sum(x['status']=='passed' for x in records)};(out/'batch-finished.json').write_text(json.dumps(summary));print(json.dumps(summary),flush=True);assert summary['passed']==len(m['documents'])
