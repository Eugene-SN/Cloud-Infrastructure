import os,json,subprocess,hashlib
from pathlib import Path
import pymupdf
root=Path('/out/cli-smoke');root.mkdir(exist_ok=True)
doc=pymupdf.open();page=doc.new_page();page.insert_text((72,100),'Useful body; no targets')
source=root/'input.pdf';doc.save(source);doc.close()
records=[]
for name,env,expected in (
 ('exact-copy',dict(os.environ,PDF_CLEANUP_ORIGINALS_DIR='/input'),0),
 ('reject-relative-originals',dict(os.environ,PDF_CLEANUP_ORIGINALS_DIR='relative'),2)):
 output=root/(name+'.pdf')
 result=subprocess.run(['pdf-cleanup',str(source),str(output)],env=env,text=True,capture_output=True)
 assert result.returncode==expected,(result.returncode,result.stdout,result.stderr)
 report=json.loads(result.stdout);assert report['schema_version']==1
 if expected==0:
  assert report['cleanup_method']=='exact_copy'
  assert output.read_bytes()==source.read_bytes()
 else:assert not output.exists()
 records.append({'name':name,'exit_code':result.returncode,'report':report,'stderr':result.stderr})
(root/'result.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print(json.dumps(records,ensure_ascii=False),flush=True)
