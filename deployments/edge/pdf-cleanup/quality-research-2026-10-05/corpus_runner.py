"""Isolated corpus experiment. Inputs must be snapshots mounted read-only."""
import importlib.util, json, os, time, traceback
from pathlib import Path
import pymupdf
from pdf_cleanup import core

ROOT=Path('/audit'); OUT=Path('/out/corpus'); OUT.mkdir(exist_ok=True)
os.environ['PDF_CLEANUP_ORIGINALS_DIR']='/input'
spec=importlib.util.spec_from_file_location('pdf_cleanup.reference_core','/usr/local/lib/python3.14/site-packages/pdf_cleanup/core.py')
reference=importlib.util.module_from_spec(spec); spec.loader.exec_module(reference)
original_analyze=core.analyze; original_save=pymupdf.Document.save
state={}
def selections(plan):
    return [{'page':i+1,'role':p['selected'][j],'text':p['lines'][j]['text'],'bbox':list(p['lines'][j]['bbox'])}
            for i,p in enumerate(plan) for j in sorted(p['selected'])]
def analyze(doc,native):
    try: state['baseline']={'status':'planned','selection':selections(reference.analyze(doc,native))}
    except Exception as e: state['baseline']={'status':'error','error':str(e),'rc':getattr(e,'rc',None)}
    plan=original_analyze(doc,native)
    state['selection']=selections(plan)
    state['masks']=[list(map(list,p['rects'])) for p in plan]
    state['widget_masks']=[]
    # Targeted widgets are already deleted in memory before analyze().
    with pymupdf.open(state['input']) as src:
        for i,page in enumerate(src):
            state['widget_masks'].append([list(w.rect) for w in (page.widgets() or []) if w.xref in native[i]['widgets']])
    return plan
def save(self,*args,**kwargs):
    kwargs.update(garbage=2,deflate=True,use_objstms=1)
    start=time.monotonic()
    try: return original_save(self,*args,**kwargs)
    finally: state.setdefault('saves',[]).append({'options':kwargs,'elapsed_seconds':round(time.monotonic()-start,3)})
core.analyze=analyze; pymupdf.Document.save=save
items=json.loads((ROOT/'manifest.json').read_text())['unique_documents']
priority=('wa7780_g3_user_guide','wa7785a_g3_user_guide','wa7780_g3_bios','wa7785a_g3_bios','lenovo_bmc_g3_redfish')
def rank(item):
    name=item['path'].lower()
    return (next((i for i,p in enumerate(priority) if p in name),len(priority)),name)
for position,item in enumerate(sorted(items,key=rank),1):
    result_path=OUT/(item['sha256']+'.json')
    if result_path.exists(): continue
    state.clear(); state.update(item,input=str(Path('/input')/(item['sha256']+'.pdf')))
    start=time.monotonic(); print(json.dumps({'event':'start','position':position,'path':item['path']},ensure_ascii=False),flush=True)
    try:
        output=OUT/(item['sha256']+'.pdf')
        state['result']=core.cleanup(state['input'],output)
        state.update(status='passed',output=str(output),output_bytes=output.stat().st_size)
    except Exception as e:
        state.update(status='error',error=str(e),rc=getattr(e,'rc',None),traceback=traceback.format_exc())
    state['elapsed_seconds']=round(time.monotonic()-start,3)
    result_path.write_text(json.dumps(state,ensure_ascii=False,indent=2))
    print(json.dumps({'event':'complete','position':position,'path':item['path'],'status':state['status'],'elapsed':state['elapsed_seconds'],'error':state.get('error'),'method':state.get('result',{}).get('cleanup_method')},ensure_ascii=False),flush=True)
