import numpy as np, render, time, sys
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.optimize import minimize
W,H=220,160
ph=np.asarray(Image.open('frame_area2.png').resize((W,H),Image.LANCZOS),float)
def ln(a,s1=1.0,s2=7):
    a=gaussian_filter(a,s1)-gaussian_filter(a,s2)
    sd=np.sqrt(gaussian_filter(a*a,12))+1e-6
    a=a/sd; return (a-a.mean())/(a.std()+1e-9)
P=ln(ph)
def score(cam,step=3):
    img,cov=render.render(cam,W,H,step=step)
    if cov<0.9: return -1
    return float((ln(img)*P).mean())
seed=int(sys.argv[1]); rng=np.random.default_rng(seed)
hlo,hhi=float(sys.argv[2]),float(sys.argv[3])
cands=[]
for i in range(7000):
    hf=rng.uniform(34,48)
    cam=[rng.uniform(-15000,6000),rng.uniform(-10000,12000),rng.uniform(2600,3300),rng.uniform(hlo,hhi),rng.uniform(15,45),rng.uniform(-6,6),W/2/np.tan(np.radians(hf/2))]
    cands.append((score(cam),cam))
cands.sort(key=lambda x:-x[0]); print('rand',[round(c[0],3) for c in cands[:8]],flush=True)
res=[]
for s0,c0 in cands[:10]:
    r=minimize(lambda x:-score(list(x),step=2),c0,method='Nelder-Mead',options={'maxiter':300})
    res.append((-r.fun,list(r.x))); print(round(s0,3),'->',round(-r.fun,3),[round(float(v),1) for v in r.x],flush=True)
res.sort(key=lambda x:-x[0]); np.save(f'search4_{seed}.npy',np.array([[s,*c] for s,c in res]))
