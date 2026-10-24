"""Fit the Magen & Peleg Fig. 9 tracing (walls only, pools and L110 masked out) to the HEXAGON 1978 crop.
Similarity transform: image px = T + s^-1 R(theta) * plan metres. Score = masked normalised correlation between
plan walls (dilated, blurred) and the image edge strength."""
import json, numpy as np, cv2
from PIL import Image
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}
W=np.load('plan_walls.npy').astype(np.float32)   # rows z, cols x, 0.25 m cells, origin (-20,-42)
ox,oz=-20.0,-42.0; cell=0.25
POOLS=['L117','L118','L138','L48-L49','L50','L56','L58','L91','L68','L69','L71']
# pool mask in plan cells (dilated 1 m), plus L110 disc r=2.31+0.94+1
pm=np.zeros_like(W,dtype=np.uint8)
for k in POOLS:
    pts=np.array([[(x-ox)/cell,(z-oz)/cell] for x,z in E[k]['geometry']['points']],np.int32)
    cv2.fillPoly(pm,[pts],1)
pm=cv2.dilate(pm,np.ones((9,9),np.uint8))
cv2.circle(pm,(int(-ox/cell),int(-oz/cell)),int((2.31+0.94+1)/cell),1,-1)
np.save('plan_poolmask.npy',pm)
a=np.array(Image.open('F007_c_ruin_29180_19840.png')).astype(np.float32); X0,Y0=29180,19840
g=cv2.GaussianBlur(a,(0,0),0.7)
gx=cv2.Sobel(g,cv2.CV_32F,1,0); gy=cv2.Sobel(g,cv2.CV_32F,0,1)
edge=cv2.GaussianBlur(np.hypot(gx,gy),(0,0),1.0)
img=edge
def render(s,th,shape=(240,160),anchor=(40,60)):
    """Render plan walls into an image-pixel grid. Grid pixel (u,v) -> plan (x,z) = R(th)*(s*((u,v)-anchor))."""
    h,w=shape
    u,v=np.meshgrid(np.arange(w)-anchor[0],np.arange(h)-anchor[1])
    c,sn=np.cos(th),np.sin(th)
    x=s*(c*u - sn*v); z=s*(sn*u + c*v)
    cx=((x-ox)/cell).astype(np.float32); cz=((z-oz)/cell).astype(np.float32)
    # wall fraction over a pixel: blur the cell raster to the pixel footprint first
    k=max(1.0,s/cell/2.0)
    Wb=cv2.GaussianBlur(W,(0,0),k)
    t=cv2.remap(Wb,cx,cz,cv2.INTER_LINEAR,borderValue=0)
    m=cv2.remap(pm.astype(np.float32),cx,cz,cv2.INTER_NEAREST,borderValue=1)
    inside=cv2.remap(np.ones_like(W),cx,cz,cv2.INTER_NEAREST,borderValue=0)
    mask=((m<0.5)&(inside>0.5)).astype(np.float32)
    t=cv2.GaussianBlur(t,(0,0),1.0)
    return t,mask
best=[]
for s in np.arange(0.60,1.32,0.02):
    for thd in np.arange(-20,21,1.0):
        t,mask=render(s,np.radians(thd))
        r=cv2.matchTemplate(img,t,cv2.TM_CCOEFF_NORMED,mask=mask)
        # restrict to plausible placements: anchor near L110 guess (29346,19999) +-25 px
        ax,ay=29346-X0-40,19999-Y0-60
        sub=r[ay-25:ay+26,ax-25:ax+26]
        j=np.unravel_index(np.nanargmax(sub),sub.shape)
        best.append((float(sub[j]),round(float(s),3),float(thd),int(ax-25+j[1]),int(ay-25+j[0])))
best.sort(reverse=True)
for b in best[:12]: print(b)
json.dump(best[:50],open('fit_search.json','w'))
