import sys,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import S,M
from PIL import Image,ImageDraw; Image.MAX_IMAGE_PIXELS=None
from pyproj import Transformer
be=[1.59005712e-02,7.14127736e+01]; bn=[-1.59448677e-02,3.14464989e+02]
I2O=Transformer.from_crs(2039,28191,always_xy=True)
def px(E,N):
    e,n=I2O.transform(E,N); return ((e/1000-be[1])/be[0],(n/1000-bn[1])/bn[0])
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; label=len(sys.argv)>6
im=Image.open('/home/claude/swarm/scratch/E2r2/tir_north.jpg').crop((x0,y0,x1,y1)).convert('RGB'); d=ImageDraw.Draw(im)
for s,m in zip(S,M):
    s=np.asarray(s,float); P=[px(e,n) for e,n in s]; P=[(a-x0,b-y0) for a,b in P]
    if all(not(0<=a<=x1-x0 and 0<=b<=y1-y0) for a,b in P): continue
    col={'Certain':(0,170,0),'Conjectured':(0,120,255),'Hypothetical':(255,150,0)}.get(m['cert'],(0,0,0))
    d.line(P,fill=col,width=4)
    if label:
        a,b=P[len(P)//2]; d.text((a+5,b),f"{m['fid']} {m['name']}",fill=col)
im.save(out); print(out,im.size)
