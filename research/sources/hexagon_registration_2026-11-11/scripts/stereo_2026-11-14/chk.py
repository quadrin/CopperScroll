import sys; sys.path.insert(0,'/home/claude/cs/sat')
from hm import *
import cv2,numpy as np,math,json
from modern import modern,KM
from pyproj import Transformer
P2I=Transformer.from_crs(28191,2039,always_xy=True); W2P=Transformer.from_crs(4326,28191,always_xy=True)
def grad(a,s=1.5):
    a=cv2.GaussianBlur(a.astype('float32'),(0,0),s); return np.hypot(cv2.Sobel(a,cv2.CV_32F,1,0),cv2.Sobel(a,cv2.CV_32F,0,1))
def run(name,model,pe,pn,half=400):
    E0,N0=P2I.transform(pe*1000-half,pn*1000-half); E1,N1=P2I.transform(pe*1000+half,pn*1000+half)
    o,Es,Ns=ortho(L(model),E0,N0,E1,N1,1.0); o=o[:2*half,:2*half]
    m=modern(pe,pn,half,f'/home/claude/cs/chk/{name}_modern.jpg',res=1.0)
    m=cv2.resize(cv2.cvtColor(m,cv2.COLOR_BGR2GRAY),(2*half,2*half),interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'/home/claude/cs/chk/{name}_{model}.jpg',cv2.normalize(o,None,0,255,cv2.NORM_MINMAX).astype('uint8'))
    G1,G2=grad(o),grad(m); res=[]; S=80; B=200
    for y in range(S,2*half-B-S+1,100):
        for x in range(S,2*half-B-S+1,100):
            t=G1[y:y+B,x:x+B]; w=G2[y-S:y+B+S,x-S:x+B+S]
            r=cv2.matchTemplate(w,t,cv2.TM_CCOEFF_NORMED); _,mx,_,loc=cv2.minMaxLoc(r)
            # second peak
            r2=r.copy(); cv2.circle(r2,loc,12,-1,-1); mx2=r2.max()
            res.append((loc[0]-S,-(loc[1]-S),mx,mx/max(mx2,1e-6)))
    r=np.array(res); good=r[(r[:,2]>0.12)&(r[:,3]>1.25)]
    out=dict(name=name,model=model,n=len(r),n_good=len(good))
    if len(good)>=3:
        out.update(dE=float(np.median(good[:,0])),dN=float(np.median(good[:,1])),sE=float(np.std(good[:,0])),sN=float(np.std(good[:,1])),corr=float(np.median(good[:,2])))
    print(json.dumps(out)); return out
sites=[('qumran','D74_F017b',193.56,127.65),('qumran','M78_F007c',193.56,127.65),('qumran','J74_F015d',193.56,127.65),
('quruntul','D74_F017b',190.855,142.411),('quruntul','M78_F007c',190.855,142.411),
('cypros','D74_F017b',190.44,139.165),('cypros','M78_F007c',190.44,139.165),
('feshkha','D74_F017b',192.81,124.83)]
e,n=W2P.transform(35.3311,31.7049); sites.append(('marsaba','D74_F018b',e/1000,n/1000)); sites.append(('marsaba','J74_F015d',e/1000,n/1000))
R=[]
for s in sites:
    try: R.append(run(*s))
    except Exception as ex: print(s[0],s[1],'failed',repr(ex)[:150])
json.dump(R,open('/home/claude/cs/chk/result.json','w'))
