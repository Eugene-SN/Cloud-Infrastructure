import json,collections
from pathlib import Path
import pymupdf
from pdf_cleanup.core import lines_for,numeric_component
root=Path('/audit');manifest=json.loads((root/'manifest.json').read_text())
names={
'WA5680 G3/lenovo_wentian_wa5680g3_user_guide.pdf':'small body raster differences',
'WA5480 G3/lenovo_bmc_event_reference_guide_g5_v4.pdf':'body raster difference',
'WA5480 G3/lenovo_wentian_os_installation_guide.pdf':'37 pages with body raster differences',
'WA7785a G3/lenovo_wentian_wa7785ag3_bios_user_guide.pdf':'singleton Roman and body raster difference',
'WR6220 G5/lenovo_wentian_wr6220g5_user_guide.pdf':'body space collapse; operator serialization refusal',
'WA7880a G3/lenovo_wentian_wa7880ag3_user_guide.pdf':'body raster difference',
'WR5220 G5/lp1728.pdf':'Lenovo Press graphics differences',
'WA7780 G3/lenovo_wentian_wa7780g3_user_guide.pdf':'clipped illustration and pure Footer Form',
'WA7785a G3/lenovo_wentian_wa7785ag3_user_guide.pdf':'clipped illustration and pure Footer Form',
'WR5225 G3/wr5225g3_user_guide_v6.pdf':'body/footer bbox overlap',
'WA7780 G3/lenovo_wentian_wa7780g3_bios_user_guide.pdf':'singleton Roman',
'WA5480 G3/lenovo_bmc_g3_redfish_guide_v11.pdf':'no footers but 133 links; huge xref',
'WR5220 G3/lp1705.pdf':'target Widget overlapping retained body',
'WA5680 G5/lp2469.pdf':'inline footer number and title',
'WA5480 G3/lxce_onecli_cplus_ug.pdf':'ambiguous numeral after first cleanup',
'WR5220 G3/lenovo_wentian_wr5220g3_user_guide_v18.pdf':'CJK guide and repeat ambiguity',
'WR5220 G5/lenovo_wentian_wr5220g5_user_guide_v7.pdf':'USB/OCP body mistaken for footer on repeat',
'WA5685 G5/lp2507.pdf':'two-page CFF/font and footerless Widget control',
}
sample=[];geometry=[]
for row in manifest['unique_documents']:
 with pymupdf.open('/input/'+row['sha256']+'.pdf') as doc:
  pages=len(doc)
  if row['path'] in names:sample.append(dict(row,pages=pages,reason=names[row['path']]))
  for i,page in enumerate(doc):
   lines=lines_for(page);last=max((line['y'] for line in lines),default=0)
   for line in lines:
    if numeric_component(line['text']) and last-line['y']<=line['size']*.5:
     geometry.append({'path':row['path'],'page':i+1,'text':line['text'],'baseline':line['y'],'height':page.rect.height,'size':line['size'],'ratio':line['y']/page.rect.height})
assert len(sample)==len(names)
Path('/out/selection.json').write_text(json.dumps({'documents':sorted(sample,key=lambda x:x['path']),'holdout_unique_documents':49-len(sample)},ensure_ascii=False,indent=2))
Path('/out/numeric-geometry.json').write_text(json.dumps(geometry,ensure_ascii=False,indent=2))
print(json.dumps({'sample':len(sample),'sample_pages':sum(x['pages'] for x in sample),'numeric_candidates':len(geometry),'below_90percent':[x for x in geometry if x['ratio']<.9][:25]},ensure_ascii=False),flush=True)
