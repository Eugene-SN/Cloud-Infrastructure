"""Retry only corpus outputs that failed, using the final isolated candidate."""
import json,os,time,traceback,hashlib
from pathlib import Path
import pymupdf
from pdf_cleanup import core

ROOT=Path('/out/corpus'); OUT=Path('/out/repaired-v6');OUT.mkdir(exist_ok=True)
os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
original_analyze=core.analyze; original_save=pymupdf.Document.save; state={}
def analyze(doc,native):
    plan=original_analyze(doc,native)
    state['selection']=[{'page':i+1,'role':p['selected'][j],'text':p['lines'][j]['text'],'bbox':list(p['lines'][j]['bbox'])} for i,p in enumerate(plan) for j in sorted(p['selected'])]
    state['masks']=[list(map(list,p['rects'])) for p in plan]
    return plan
def save(self,*args,**kwargs):
    start=time.monotonic()
    try:return original_save(self,*args,**kwargs)
    finally:state.setdefault('saves',[]).append({'options':kwargs,'elapsed_seconds':round(time.monotonic()-start,3)})
core.analyze=analyze;pymupdf.Document.save=save
for path in sorted(ROOT.glob('*.json')):
    if path.name.endswith('.review.json'):continue
    old=json.loads(path.read_text())
    if old['status']=='passed':continue
    state.clear();state.update({k:old[k] for k in ('path','sha256','size','input','baseline','widget_masks') if k in old})
    start=time.monotonic();print(json.dumps({'event':'repair_start','path':old['path']},ensure_ascii=False),flush=True)
    try:
        output=OUT/(path.stem+'.pdf');state['result']=core.cleanup(old['input'],output)
        state.update(status='passed',output=str(output),output_bytes=output.stat().st_size)
    except Exception as e:state.update(status='error',error=str(e),rc=getattr(e,'rc',None),traceback=traceback.format_exc())
    state['elapsed_seconds']=round(time.monotonic()-start,3)
    state['candidate_core_sha256']=hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()
    state['candidate_native_sha256']=hashlib.sha256(Path(core.__file__).with_name('native.py').read_bytes()).hexdigest()
    (OUT/path.name).write_text(json.dumps(state,ensure_ascii=False,indent=2))
    print(json.dumps({'event':'repair_complete','path':state['path'],'status':state['status'],'elapsed':state['elapsed_seconds'],'error':state.get('error'),'method':state.get('result',{}).get('cleanup_method')},ensure_ascii=False),flush=True)
