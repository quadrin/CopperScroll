import sys; sys.path.insert(0,'/home/claude/cs/sat')
from hm import *
import cv2,numpy as np,json,hx
from pyproj import Transformer
P2I=Transformer.from_crs(28191,2039,always_xy=True); I2W=Transformer.from_crs(2039,4326,always_xy=True)
name,pe,pn,half=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])
A,B=sys.argv[5],sys.argv[6]
MA,MB=L(A),L(B); g=1.0
E0,N0=P2I.transform(pe*1000-half,pn*1000-half); E1,N1=E0+2*half,N0+2*half
oa,Es,Ns=ortho(MA,E0,N0,E1,N1,g); ob,_,_=ortho(MB,E0,N0,E1,N1,g)
n=min(oa.shape[0],oa.shape[1],ob.shape[0],ob.shape[1]); oa=oa[:n,:n].astype('float32'); ob=ob[:n,:n].astype('float32')
EE,NN=np.meshgrid(Es[:n],Ns[:n]); Z=np.asarray(zat_s(EE,NN),'float32')
v=np.array([-(MA['ce'][-1]-MB['ce'][-1]), (MA['cn'][-1]-MB['cn'][-1])])  # image px (x east, y south) per m of height, A relative to B
print('parallax px per m',v, 'B/H',np.hypot(*v))
def prep(a):
    a=cv2.normalize(a,None,0,255,cv2.NORM_MINMAX).astype('uint8'); return cv2.createCLAHE(3.0,(16,16)).apply(a).astype('float32')
a,b=prep(oa),prep(ob)
# global shift first
r=cv2.matchTemplate(b,a[100:-100,100:-100],cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(r); g0=(loc[0]-100,loc[1]-100); print('global shift B rel A',g0,mx)
T=int(sys.argv[7]) if len(sys.argv)>7 else 21; st=int(sys.argv[8]) if len(sys.argv)>8 else 3; SX,SY=(int(sys.argv[9]),int(sys.argv[10])) if len(sys.argv)>10 else (36,8); h=T//2
ys=list(range(h+SY+abs(g0[1])+2,n-h-SY-abs(g0[1])-2,st)); xs=list(range(h+SX+abs(g0[0])+2,n-h-SX-abs(g0[0])-2,st))
DX=np.full((len(ys),len(xs)),np.nan,'float32'); DY=DX.copy(); C=DX.copy()
for i,y in enumerate(ys):
    for j,x in enumerate(xs):
        t=a[y-h:y+h+1,x-h:x+h+1]
        if t.std()<4: continue
        yy,xx=y+g0[1],x+g0[0]
        w=b[yy-h-SY:yy+h+SY+1,xx-h-SX:xx+h+SX+1]
        r=cv2.matchTemplate(w,t,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(r)
        px,py=loc
        r2=r.copy(); cv2.circle(r2,loc,4,-1,-1)
        if mx<1.15*r2.max(): continue
        # subpixel
        def sp(m,c,z0):
            if 0<c<len(m)-1:
                d=m[c-1]-2*m[c]+m[c+1]; return c+(0.5*(m[c-1]-m[c+1])/d if d!=0 else 0)
            return c
        fx=sp(r[py,:],px,0); fy=sp(r[:,px],py,0)
        DX[i,j]=fx-SX+g0[0]; DY[i,j]=fy-SY+g0[1]; C[i,j]=mx
# A feature at x in A is at x+DX in B. A rel B displacement = -(DX,DY) = v*dh
dh=-(DX*v[0]+DY*v[1])/(v@v); cross=-(DX*(-v[1])+DY*v[0])/np.hypot(*v)
ok=(C>float(sys.argv[11]) if len(sys.argv)>11 else C>0.45)&np.isfinite(dh)
med=np.nanmedian(dh[ok]); cm=np.nanmedian(cross[ok]); ok&=(np.abs(cross-cm)<2.5)
print('blocks',C.size,'ok',int(ok.sum()),'median dh',med,'cross median',cm,'cross std',np.nanstd(cross[ok]))
YY,XX=np.meshgrid(ys,xs,indexing='ij'); Zb=Z[YY,XX]
# remove plane trend of dh (registration bias)
Am=np.c_[XX[ok],YY[ok],np.ones(ok.sum())]; co=np.linalg.lstsq(Am,dh[ok],rcond=None)[0]
res=dh-(XX*co[0]+YY*co[1]+co[2]); Hf=Zb+res; Hf[~ok]=np.nan
print('dh residual std',np.nanstd(res[ok]),'p5,p95',np.nanpercentile(res[ok],[5,95]))
np.savez_compressed(f'/home/claude/cs/st/{name}.npz',H=Hf,res=np.where(ok,res,np.nan),C=C,Z=Zb,xs=np.array(xs),ys=np.array(ys),E0=E0,N1=Ns[0],oa=oa.astype('uint8'),ob=ob.astype('uint8'),v=v)
