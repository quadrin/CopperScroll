import sys; sys.path.insert(0,'/home/claude/cs/sat')
from hm import *
import cv2,numpy as np,rasterio,json
from rasterio.windows import Window
from pyproj import Transformer
P2I=Transformer.from_crs(28191,2039,always_xy=True)
d=rasterio.open('/home/claude/cs/sat/tiles/D3C1209-200214A017_f.tif'); W,H=d.width,d.height
# coarse: aft8 flipped (U,V) -> ITM
E0r,N0r=P2I.transform(188400,137200); E1r,N1r=P2I.transform(192400,141200); Esr=np.arange(E0r,E1r,8.0); Nsr=np.arange(N1r,N0r,-8.0)
Mrot=cv2.getRotationMatrix2D((len(Esr)/2,len(Nsr)/2),4,1.15); Mi=cv2.invertAffineTransform(Mrot)
def aft_to_itm(x,y):
    U=(16000-x)/8.0; V=(H-y)/8.0; i=U-1242+80; j=V-1475+80
    c=Mi[0,0]*i+Mi[0,1]*j+Mi[0,2]; r=Mi[1,0]*i+Mi[1,1]*j+Mi[1,2]
    return E0r+8*c, Nsr[0]-8*r
# affine ground->aft px (3 points)
p=np.float32([[2000,8000],[9000,8000],[2000,15000]]); q=np.float32([aft_to_itm(*a) for a in p])
g=4.0; Ea,Na=P2I.transform(185000,135500); Eb,Nb=P2I.transform(193000,143500)
Es=np.arange(Ea,Eb,g); Ns=np.arange(Nb,Na,-g)
# grid px (c,r) -> aft px/4
gp=np.float32([[(e-Ea)/g,(Ns[0]-n)/g] for e,n in q]); A=cv2.getAffineTransform(gp,p/4.0)   # grid -> aft4
aft4=d.read(1,window=Window(0,0,20000,H),out_shape=(H//4,5000))
ps=cv2.warpAffine(aft4,A,(len(Es),len(Ns)),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP)
o,_,_=ortho(L('D74_F017b'),Ea,Na,Eb,Nb,g); n0=min(o.shape[0],ps.shape[0]); n1=min(o.shape[1],ps.shape[1]); o=o[:n0,:n1]; ps=ps[:n0,:n1]
cv2.imwrite('/home/claude/cs/st/aft_ps4.jpg',ps); cv2.imwrite('/home/claude/cs/st/fwd_o4.jpg',o)
def G(x): x=cv2.GaussianBlur(x.astype('float32'),(0,0),1.2); return np.hypot(cv2.Sobel(x,cv2.CV_32F,1,0),cv2.Sobel(x,cv2.CV_32F,0,1))
Go,Gp=G(o),G(ps); B=64; S=48; T=[]
for r in range(S,n0-B-S,32):
    for c in range(S,n1-B-S,32):
        if (ps[r:r+B,c:c+B]==0).mean()>0.05: continue
        res=cv2.matchTemplate(Gp[r-S:r+B+S,c-S:c+B+S],Go[r:r+B,c:c+B],cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(res)
        r2=res.copy(); cv2.circle(r2,loc,6,-1,-1)
        if mx>0.3 and mx>1.3*r2.max():
            cc=c+B/2; rr=r+B/2; cp=cc+loc[0]-S; rp=rr+loc[1]-S
            x4=A[0,0]*cp+A[0,1]*rp+A[0,2]; y4=A[1,0]*cp+A[1,1]*rp+A[1,2]
            T.append((x4*4,y4*4,Ea+g*cc,Ns[0]-g*rr,loc[0]-S,loc[1]-S,mx))
T=np.array(T); print('ties',len(T),'median shift px',np.median(T[:,4]),np.median(T[:,5]))
z=zat_s(T[:,2].reshape(-1,1),T[:,3].reshape(-1,1)).ravel(); Ad=design(T[:,0],T[:,1],z); keep=np.ones(len(T),bool)
for _ in range(6):
    ce=np.linalg.lstsq(Ad[keep],T[keep,2],rcond=None)[0]; cn=np.linalg.lstsq(Ad[keep],T[keep,3],rcond=None)[0]
    res=np.hypot(Ad@ce-T[:,2],Ad@cn-T[:,3]); rms=np.sqrt((res[keep]**2).mean()); keep=res<max(2*rms,8)
print('kept',keep.sum(),'rms',rms,'kE',ce[-1],'kN',cn[-1],'z range',z[keep].min(),z[keep].max())
M={'form':'E,N = [x/1e4,y/1e4,1,x2,xy,y2,z]','ce':list(map(float,ce)),'cn':list(map(float,cn)),'rms':float(rms),'n':int(keep.sum()),'zmin':float(z[keep].min()),'zmax':float(z[keep].max()),'item':'1209-200214A017','tile':'f','note':'local model for PG 185-193/135.5-143.5, fitted to the D74_F017b ortho, 14 Nov 2026'}
json.dump(M,open('/home/claude/cs/sat/D74_A017f_height_model.json','w'))
