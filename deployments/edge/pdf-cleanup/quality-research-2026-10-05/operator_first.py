import json,time,hashlib,os
from pathlib import Path
from pdf_cleanup import core
key='8921606e9e9fcc6b199f2c360787dc228f3180bd2448423d40bd1d101c13be71'
record=json.loads((Path('/out/corpus')/(key+'.json')).read_text())
out=Path('/out/operator-first');out.mkdir(exist_ok=True)
original=core.analyze
def analyze(doc,native):
 plan=original(doc,native)
 for page in plan:page['requires_text_operators']=True
 return plan
core.analyze=analyze
os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
started=time.monotonic();output=out/(key+'.pdf')
record.pop('output_bytes',None)
try:
 record['result']=core.cleanup(record['input'],output)
 record.update(status='passed',output=str(output),elapsed_seconds=round(time.monotonic()-started,3),experiment='operator-first on all pages; classifier unchanged')
except Exception as error:record.update(status='error',error=str(error))
if record['status']=='error':
 record['earlier_generation_result']=record.pop('result',None)
 record['output']=str(output)
record['elapsed_seconds']=round(time.monotonic()-started,3)
(out/(key+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2))
print(json.dumps({k:record.get(k) for k in ('path','status','error','elapsed_seconds','result')},ensure_ascii=False),flush=True)
if record['status']=='passed':
 from review_pdfium import compare
 result=compare(record['input'],record['output'],record['masks'],record['widget_masks'])
 result['output_verified_sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
 (out/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False),flush=True)
