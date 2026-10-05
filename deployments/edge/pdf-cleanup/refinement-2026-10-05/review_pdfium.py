"""Independent PDFium source/output comparison; never edits PDFs."""
import json, math, sys, time, traceback
from pathlib import Path
import numpy as np
import pypdfium2 as pdfium
import pymupdf
from pdf_cleanup.core import character_difference
from collections import Counter

def document_properties(doc):
    def canonical(value):
        if isinstance(value,pymupdf.Point): return list(value)
        if isinstance(value,dict): return {k:canonical(v) for k,v in value.items() if k!='xref'}
        if isinstance(value,(tuple,list)): return [canonical(v) for v in value]
        return value
    return {'bookmarks':canonical(doc.get_toc(simple=False)),
            'page_labels':doc.get_page_labels(),
            'metadata':{k:v for k,v in doc.metadata.items() if k not in ('format','encryption')},
            'xml_metadata':doc.get_xml_metadata()}

def glyphs(page, matrix, masks=()):
    text=page.get_textpage(); result=[]
    try:
        for index in range(text.count_chars()):
            code=pdfium.raw.FPDFText_GetUnicode(text.raw,index)
            if not code or chr(code).isspace(): continue
            left,bottom,right,top=text.get_charbox(index)
            center=pymupdf.Point((left+right)/2,(bottom+top)/2)*matrix
            if any(pymupdf.Rect(box).contains(center) for box in masks): continue
            result.append((chr(code),round(center.x,4),round(center.y,4)))
        return result
    finally: text.close()

def text_difference(source_glyphs, actual_glyphs, boxes):
    missing,extra=character_difference(Counter(source_glyphs),Counter(actual_glyphs),.02)
    allowed=Counter({key:count for key,count in missing.items() if any(pymupdf.Rect(box).contains(pymupdf.Point(key[1],key[2])) for box in boxes)})
    unwanted=missing-allowed;remaining=allowed.copy();retained=[]
    for glyph in source_glyphs:
        if remaining[glyph]:remaining[glyph]-=1
        else:retained.append(glyph)
    order_changed=[g[0] for g in retained]!=[g[0] for g in actual_glyphs]
    return unwanted,extra,order_changed,len(retained)

def compare(source,output,masks,widget_masks,scale=2):
    started=time.monotonic(); failures=[]; outside_total=0; changed_total=0; glyph_total=0
    with pdfium.PdfDocument(source) as src, pdfium.PdfDocument(output) as dst, pymupdf.open(source) as geometry, pymupdf.open(output) as output_geometry:
        source_properties=document_properties(geometry); output_properties=document_properties(output_geometry)
        property_changes=[k for k in source_properties if source_properties[k]!=output_properties[k]]
        src.init_forms(); dst.init_forms()
        if len(src)!=len(dst): raise ValueError('PDFium page counts differ')
        for i in range(len(src)):
            page=src[i]; actual=dst[i]; a=b=None
            try:
                boxes=masks[i]+widget_masks[i]
                # Extracted glyph boxes are unrotated. In 1.28.2 the matrix of
                # a rotated/cropped page drops the crop origin; obtain it from
                # a rotation-zero in-memory geometry view, never saved.
                geometry_page=geometry[i]; geometry_page.set_rotation(0)
                matrix=geometry_page.transformation_matrix
                source_glyphs=glyphs(page,matrix); actual_glyphs=glyphs(actual,matrix)
                missing,extra,order_changed,retained=text_difference(source_glyphs,actual_glyphs,boxes)
                glyph_total+=retained
                a=page.render(scale=scale,draw_annots=True); b=actual.render(scale=scale,draw_annots=True)
                array_a=a.to_numpy(); array_b=b.to_numpy()
                if array_a.shape!=array_b.shape: raise ValueError(f'Page {i+1}: bitmap dimensions differ')
                different=np.any(array_a!=array_b,axis=2); changed=int(different.sum()); changed_total+=changed
                # Mask only exact removed glyph/widget bounds, with 2 raster-pixel
                # margin for anti-aliasing. No broad header/footer bands.
                posconv=a.get_posconv(page); inverse=~matrix
                for box in boxes:
                    rect=pymupdf.Rect(box)
                    points=[pymupdf.Point(x,y)*inverse for x,y in ((rect.x0,rect.y0),(rect.x0,rect.y1),(rect.x1,rect.y0),(rect.x1,rect.y1))]
                    pixels=[posconv.to_bitmap(p.x,p.y) for p in points]
                    x0=max(0,math.floor(min(p[0] for p in pixels))-2); x1=min(different.shape[1],math.ceil(max(p[0] for p in pixels))+3)
                    y0=max(0,math.floor(min(p[1] for p in pixels))-2); y1=min(different.shape[0],math.ceil(max(p[1] for p in pixels))+3)
                    different[y0:y1,x0:x1]=False
                outside=int(different.sum()); outside_total+=outside
                if outside or missing or extra or order_changed:
                    failures.append({'page':i+1,'pixels_outside_masks':outside,'missing_glyphs':sum(missing.values()),'extra_glyphs':sum(extra.values()),'reading_order_changed':order_changed,'missing_examples':list(missing.items())[:3],'extra_examples':list(extra.items())[:3]})
                if (i+1)%50==0: print(json.dumps({'event':'review_progress','file':Path(source).name,'page':i+1,'pages':len(src),'failures':len(failures)}),flush=True)
            finally:
                if a is not None: a.close()
                if b is not None: b.close()
                page.close(); actual.close()
        return {'status':'passed' if not failures and not property_changes else 'differences','engine':str(pdfium.PDFIUM_INFO),'pypdfium2':str(pdfium.PYPDFIUM_INFO),'dpi':scale*72,'pages':len(src),'body_glyphs':glyph_total,'changed_pixels_total':changed_total,'pixels_outside_masks':outside_total,'failures':failures,'document_property_changes':property_changes,'elapsed_seconds':round(time.monotonic()-started,3)}

if __name__=='__main__':
    root=Path('/out/review'); root.mkdir(exist_ok=True)
    records={}
    for directory in (Path('/out/corpus'),Path('/out/repaired')):
        for path in directory.glob('*.json'):
            if path.name.endswith('.review.json'):continue
            record=json.loads(path.read_text())
            if record['status']=='passed':records[record['sha256']]=record
    for key,record in sorted(records.items()):
        target=root/(key+'.json')
        if target.exists() or record['status']!='passed': continue
        print(json.dumps({'event':'review_start','path':record['path']},ensure_ascii=False),flush=True)
        try: result=compare(record['input'],record['output'],record['masks'],record['widget_masks'])
        except Exception as e: result={'status':'error','error':str(e),'traceback':traceback.format_exc()}
        result['path']=record['path']; result['sha256']=record['sha256']
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2))
        print(json.dumps({'event':'review_complete','path':record['path'],'status':result['status'],'pages':result.get('pages'),'failures':len(result.get('failures',[])),'elapsed':result.get('elapsed_seconds'),'error':result.get('error')},ensure_ascii=False),flush=True)
