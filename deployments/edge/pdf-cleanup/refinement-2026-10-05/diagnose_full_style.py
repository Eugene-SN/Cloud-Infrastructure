import json,difflib
from pathlib import Path
import pymupdf
from pdf_cleanup import core
from pdf_cleanup.native import inspect_pdf,remove_text_shows
key='8921606e9e9fcc6b199f2c360787dc228f3180bd2448423d40bd1d101c13be71'
root=Path('/out/full-style-diagnostic');root.mkdir(exist_ok=True)
source_path=Path('/input')/(key+'.pdf')
first_native=inspect_pdf(source_path)
with pymupdf.open(source_path) as source:
 native=first_native
 plan=core.analyze(source,native)
 expected=plan[13]['body_signature']
 current=core.body_signature(core.lines_for(source[13]),plan[13]['selected'])
 print(json.dumps({'source_reextract_matches':core.geometry_equivalent(expected,current)},ensure_ascii=False),flush=True)
 with pymupdf.open(source_path) as target:
  remove_text_shows(target,source_path,plan);target.save(root/'edited.pdf',garbage=2,deflate=True,use_objstms=1)
 with pymupdf.open(root/'edited.pdf') as target:
  actual=core.body_signature(core.lines_for(target[13]));diffs=[]
  for i,(a,b) in enumerate(zip(expected,actual)):
   if not core.geometry_equivalent(a,b):
    diffs.append({'index':i,'expected':a,'actual':b})
  print(json.dumps({'expected_count':len(expected),'actual_count':len(actual),'mismatches':len(diffs),'examples':diffs[:15],'selected':[plan[13]['lines'][j]['text'] for j in plan[13]['selected']]},ensure_ascii=False),flush=True)
  (root/'signature.json').write_text(json.dumps({'expected':expected,'actual':actual,'mismatches':diffs},ensure_ascii=False,indent=2))
