import json
from pathlib import Path
import pymupdf
from PIL import Image,ImageDraw
root=Path('/out/spot-check');root.mkdir(exist_ok=True)
records=[json.loads(p.read_text()) for p in Path('/out/results').glob('*.json')]
cases=[('wa5680g5_bios',5,False),('wr6220g5_user',349,True),('wr5225g3_user',296,True),('wr5220g5_user',82,True)]
for name,page,clip in cases:
 row=next((r for r in records if name in r['path']),None)
 if row is None:continue
 images=[]
 for label,path in [('source',Path('/input')/(row['sha256']+'.pdf')),('candidate',Path('/out/results')/(row['sha256']+'.pdf'))]:
  with pymupdf.open(path) as doc:
   p=doc[page-1];rect=p.rect
   if clip:rect=pymupdf.Rect(rect.x0,rect.height*.72,rect.x1,rect.y1)
   pix=p.get_pixmap(matrix=pymupdf.Matrix(1.25,1.25),clip=rect,alpha=False)
   im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
   images.append(im)
 canvas=Image.new('RGB',(sum(im.width for im in images),max(im.height for im in images)+28),'white');draw=ImageDraw.Draw(canvas);x=0
 for label,im in zip(('SOURCE','CANDIDATE'),images):
  draw.text((x+8,8),label,fill='black');canvas.paste(im,(x,28));x+=im.width
 output=root/(name+'-p'+str(page)+'.png');canvas.save(output)
 print(str(output),row['path'])
