# Round 2 plate-check crops (P31-P87) from stitched Drive-viewer captures of Puech 2006 copy A.
# Key: registration/plate_check/round2/key.json (copy/radiograph page paths are local captures, not in Git).
# usage: python3 -I make_items.py key2.json outdir
import json,sys,os
from PIL import Image,ImageDraw
M=36; K=1.25
CODE={'I 12':'P67','II 3':'P31','III 1':'P61','III 8':'P72','III 11':'P49','VIII 14':'P84','IX 10':'P53','XI 8':'P87','XI 9':'P35'}
def band(path,y,sp,k=K):
    im=Image.open(path).convert('RGB'); W,H=im.size
    a,b=max(0,int(y-k*sp)),min(H,int(y+k*sp))
    c=im.crop((0,a,W,b)); out=Image.new('RGB',(W+2*M,c.size[1]),'white'); out.paste(c,(M,0))
    d,yy=ImageDraw.Draw(out),y-a
    d.polygon([(4,yy-12),(4,yy+12),(M-4,yy)],fill=(0,170,0))
    d.polygon([(W+2*M-4,yy-12),(W+2*M-4,yy+12),(W+M+4,yy)],fill=(0,170,0))
    return out
key=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
for line,it in key.items():
    code=CODE[line]
    band(it['copy'],it['copy_centre_y'],it['copy_line_spacing']).save(f'{out}/{code}_A.png')
    band(it['radio1'],it['radio1_centre_y'],it['radio_line_spacing'],1.6).save(f'{out}/{code}_B.png')
    band(it['radio2'],it['radio2_centre_y'],it['radio_line_spacing'],1.6).save(f'{out}/{code}_C.png')
    print(code,line)
