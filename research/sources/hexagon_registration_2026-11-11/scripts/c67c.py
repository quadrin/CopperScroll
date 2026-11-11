import sys; sys.path.insert(0,'/home/claude/dem')
import c67b as B, c67reg as R, auto, numpy as np, cv2
from scipy import ndimage as ndi
def feat(a):
    a=a.astype(np.float32); a=cv2.GaussianBlur(a,(0,0),1.5); hpz=a-cv2.GaussianBlur(a,(0,0),12)
    return hpz
def match(name,A,centre,res=6,W=1000,blk=250,step=125,ms=170,valid_ref=None,refname=None):
    E,N=auto.T.transform(centre[1],centre[0]); E0=E-W*res/2; N0=N+W*res/2
    a=B.ref(refname or name,E0,N0,W,W,res); b=B.cor(name,A,E0,N0,W,W,res)
    fa=feat(a); fb=feat(b); out=[]
    for by in range(ms,W-blk-ms+1,step):
        for bx in range(ms,W-blk-ms+1,step):
            t=fb[by:by+blk,bx:bx+blk]; s=fa[by-ms:by+blk+ms,bx-ms:bx+blk+ms]
            if (b[by:by+blk,bx:bx+blk]==0).mean()>0.05 or (a[by-ms:by+blk+ms,bx-ms:bx+blk+ms]==0).mean()>0.05 or t.std()<1: continue
            r=cv2.matchTemplate(s,t,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(r)
            dx,dy=loc[0]-ms,loc[1]-ms
            # second peak
            r2=r.copy(); cv2.circle(r2,loc,12,-1,-1); m2=r2.max()
            out.append((bx+blk/2,by+blk/2,dx,dy,mx,m2))
    return np.array(out),(E0,N0,res)
if __name__=='__main__':
    A0=R.prior()
    o,_=match('jer',A0,(31.857,35.445)); np.set_printoptions(suppress=True,linewidth=200); print(np.round(o,2))
def cps(name,A,centre,**kw):
    o,(E0,N0,res)=match(name,A,centre,**kw)
    if len(o)==0: return np.zeros((0,3)),np.zeros((0,2)),o
    good=(o[:,4]>0.2)&(o[:,4]>1.3*o[:,5])
    o=o[good]; P=[];G=[]
    for bx,by,dx,dy,c,c2 in o:
        E=E0+bx*res; N=N0-by*res; x,y=auto.px(A,E,N); P.append([x,y,1]); G.append([E0+(bx+dx)*res,N0-(by+dy)*res])
    return np.array(P),np.array(G),o
