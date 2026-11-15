import numpy as np,cv2,sys
from pyproj import Transformer
name=sys.argv[1]; d=np.load(name+'.npz'); H=d['H']; res=d['res']; xs,ys=d['xs'],d['ys']; oa,ob=d['oa'],d['ob']; Z=d['Z']
st=xs[1]-xs[0]
def fill(a):
    m=np.isnan(a).astype('uint8'); b=np.where(m,0,a).astype('float32'); return cv2.inpaint(b,m,3,cv2.INPAINT_NS) if m.any() else b
def shade(a,cell):
    a=cv2.GaussianBlur(a,(0,0),1.0); gy,gx=np.gradient(a,cell); az,alt=np.radians(315),np.radians(40)
    sl=np.arctan(np.hypot(gx,gy)); asp=np.arctan2(-gx,gy)
    s=np.sin(alt)*np.cos(sl)+np.cos(alt)*np.sin(sl)*np.cos(az-asp); return np.clip(s*255,0,255).astype('uint8')
Hf=cv2.medianBlur(fill(H),5); S=shade(Hf,st); S0=shade(Z.astype('float32'),st)
x0,x1,y0,y1=xs[0],xs[-1],ys[0],ys[-1]; n=x1-x0
big=lambda a:cv2.resize(a,(n,n),interpolation=cv2.INTER_CUBIC)
r=np.clip((fill(res)+25)/50*255,0,255).astype('uint8'); r=cv2.applyColorMap(big(cv2.medianBlur(r,5)),cv2.COLORMAP_JET)
g=lambda a:cv2.cvtColor(a,cv2.COLOR_GRAY2BGR)
ia=g(cv2.createCLAHE(2.0,(8,8)).apply(oa[y0:y1,x0:x1])); ib=g(cv2.createCLAHE(2.0,(8,8)).apply(ob[y0:y1,x0:x1]))
marks=[tuple(map(float,m.split(','))) for m in sys.argv[2:]]
P2I=Transformer.from_crs(28191,2039,always_xy=True)
panels=[ia,ib,g(big(S0)),g(big(S)),r]
for p in panels:
    for (pe,pn) in marks:
        E,N=P2I.transform(pe*1000,pn*1000); u=int(E-float(d['E0'])-x0); v=int(float(d['N1'])-N-y0); cv2.circle(p,(u,v),14,(0,255,255),1)
for p,t in zip(panels,['A','B','DEM 30 m shade','stereo shade','dh (blue -25 .. red +25 m)']): cv2.putText(p,t,(8,22),0,0.7,(0,255,0),2)
k=600/n; rs=lambda a:cv2.resize(a,(600,600),interpolation=cv2.INTER_AREA)
cv2.imwrite(name+'_view.jpg',np.vstack([np.hstack([rs(ia),rs(ib),rs(panels[2])]),np.hstack([rs(panels[3]),rs(r),np.zeros((600,600,3),'uint8')])]),[cv2.IMWRITE_JPEG_QUALITY,85])
